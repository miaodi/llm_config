"""Install the shared sources into native product layouts (Python 3.11+, PyYAML)."""
import argparse
import json
import os
from pathlib import Path
import re
import shutil
import sys
import tempfile
import tomllib

try:
    import yaml
except ImportError:
    sys.exit('error: install PyYAML for python3 before running setup.sh')

SOURCE = Path(__file__).resolve().parents[1]
BEGIN = '<!-- llm-config:begin -->'
END = '<!-- llm-config:end -->'


def frontmatter(path):
    text = path.read_text()
    parts = text.split('---', 2)
    if len(parts) != 3 or parts[0]:
        raise ValueError(f'{path}: expected YAML frontmatter')
    meta = yaml.safe_load(parts[1])
    for key in ('name', 'description'):
        if not isinstance(meta.get(key), str) or not meta[key].strip():
            raise ValueError(f'{path}: missing {key}')
    return meta, parts[2].lstrip()


def same_tree(left, right):
    """Compare bytes, not timestamps; copied resources can contain directories."""
    if left.is_dir() and right.is_dir():
        a = {p.name for p in left.iterdir()}
        b = {p.name for p in right.iterdir()}
        return a == b and all(same_tree(left / n, right / n) for n in a)
    return left.is_file() and right.is_file() and left.read_bytes() == right.read_bytes()


class Installer:
    def __init__(self, base, copy):
        self.base = base
        self.copy = copy
        self.backup_root = None

    def backup(self, dst):
        protected = [SOURCE / name for name in ('skills', 'agents', 'templates', 'docs', 'memory')]
        if any(dst.parent.resolve().is_relative_to(path) for path in protected):
            raise ValueError(f'{dst}: refusing to move source content')
        if not dst.exists() and not dst.is_symlink():
            return
        if self.backup_root is None:
            parent = self.base / '.llm-config-backups'
            parent.mkdir(parents=True, exist_ok=True)
            self.backup_root = Path(tempfile.mkdtemp(prefix='install-', dir=parent))
        # Preserve symlinks themselves; never move or modify their source targets.
        slot = self.backup_root / str(len(list(self.backup_root.iterdir())))
        slot.mkdir()
        (slot / 'original-path.txt').write_text(str(dst) + '\n')
        shutil.move(str(dst), str(slot / dst.name))

    def install(self, dst, src=None, text=None):
        protected = [SOURCE / name for name in ('skills', 'agents', 'templates', 'docs', 'memory')]
        if any(dst.parent.resolve().is_relative_to(path) for path in protected):
            raise ValueError(f'{dst}: refusing to install into the source content')
        dst.parent.mkdir(parents=True, exist_ok=True)
        if text is not None:
            if dst.is_file() and not dst.is_symlink() and dst.read_text() == text:
                return
        elif not self.copy:
            if dst.is_symlink() and dst.resolve() == src.resolve():
                return
        elif not dst.is_symlink() and same_tree(src, dst):
            return
        self.backup(dst)
        if text is not None:
            dst.write_text(text)
        elif self.copy:
            if src.is_dir():
                shutil.copytree(src, dst)
            else:
                shutil.copy2(src, dst)
        else:
            dst.symlink_to(src.resolve(), target_is_directory=src.is_dir())

    def instructions(self, dst, content):
        previous = dst.read_text() if dst.exists() else ''
        if previous.count(BEGIN) != previous.count(END) or previous.count(BEGIN) > 1:
            raise ValueError(f'{dst}: malformed llm-config instruction markers')
        block = BEGIN + '\n' + content.rstrip() + '\n' + END
        if BEGIN in previous:
            if previous.index(BEGIN) > previous.index(END):
                raise ValueError(f'{dst}: reversed llm-config instruction markers')
            updated = re.sub(re.escape(BEGIN) + r'.*?' + re.escape(END),
                             lambda _: block, previous, flags=re.S)
        else:
            updated = previous + ('\n\n' if previous else '') + block + '\n'
        self.install(dst, text=updated)


def arguments():
    parser = argparse.ArgumentParser(description=__doc__)
    target = parser.add_mutually_exclusive_group(required=True)
    for product in ('copilot', 'codex', 'opencode'):
        target.add_argument('--' + product, action='store_true')
        flags = ['--' + product + '-project']
        if product == 'copilot':
            flags.append('--project')
        target.add_argument(*flags, type=Path, metavar='PATH')
    parser.add_argument('--copy', action='store_true', help='Copy sources instead of symlinking')
    return parser.parse_args()


def main():
    args = arguments()
    product = next(p for p in ('copilot', 'codex', 'opencode')
                   if getattr(args, p) or getattr(args, p + '_project'))
    project = getattr(args, product + '_project')
    if project is not None:
        project = project.resolve(strict=True)
        if not project.is_dir():
            raise ValueError('project path must be a directory')
    user_home = Path.home()
    if product == 'codex':
        base = project / '.codex' if project else Path(os.environ.get('CODEX_HOME', user_home / '.codex')).resolve()
        skills = (project / '.agents' if project else user_home / '.agents') / 'skills'
        instructions = project / 'AGENTS.md' if project else base / 'AGENTS.md'
    elif product == 'copilot':
        base = project / '.github' if project else Path(os.environ.get('COPILOT_HOME', user_home / '.copilot')).resolve()
        skills = (project if project else user_home) / '.agents/skills'
        instructions = base / 'copilot-instructions.md'
    else:
        config_home = Path(os.environ.get('XDG_CONFIG_HOME', user_home / '.config'))
        base = project / '.opencode' if project else Path(os.environ.get('OPENCODE_CONFIG_DIR', config_home / 'opencode')).resolve()
        skills = (project if project else user_home) / '.agents/skills'
        # OpenCode global rules live in the standard global config directory.
        instructions = project / 'AGENTS.md' if project else config_home / 'opencode/AGENTS.md'
    agents = base / 'agents'
    resources = base / 'llm-config'
    install = Installer(base, args.copy)

    # Validate all sources before installing anything.
    skill_sources = sorted((SOURCE / 'skills').glob('*/SKILL.md'))
    agent_sources = sorted((SOURCE / 'agents').glob('*.agent.md'))
    for path in skill_sources:
        meta, _ = frontmatter(path)
        if (meta['name'] != path.parent.name or len(meta['name']) > 64
                or not re.fullmatch(r'[a-z0-9]+(-[a-z0-9]+)*', meta['name'])
                or len(meta['description']) > 1024):
            raise ValueError(f'{path}: invalid skill name or description')
    parsed = [(p, *frontmatter(p)) for p in agent_sources]
    for path, meta, _ in parsed:
        if not isinstance(meta.get('tools'), list) or set(meta['tools']) - {'read', 'edit', 'search', 'execute', 'web'}:
            raise ValueError(f'{path}: unsupported tool list')

    # The managed block supplies a path map for source-relative references in skills.
    memory = '\n\n'.join(p.read_text().strip() for p in sorted((SOURCE / 'memory').glob('*.md')))
    guidance = (f'## llm-config resources\n\n'
                f'Resolve references to `skills/<name>/SKILL.md` through the skill catalog, '
                f'or under `{skills}`. Resolve llm-config `templates/`, `docs/`, '
                f'and source `agents/` references under `{resources}`. '
                'These paths describe instruction resources, not the project being edited.\n\n' + memory)
    # Check malformed markers before other writes.
    previous = instructions.read_text() if instructions.exists() else ''
    if (previous.count(BEGIN) != previous.count(END) or previous.count(BEGIN) > 1
            or (BEGIN in previous and previous.index(BEGIN) > previous.index(END))):
        raise ValueError(f'{instructions}: malformed llm-config instruction markers')

    for folder in ('templates', 'docs', 'agents', 'memory'):
        install.install(resources / folder, src=SOURCE / folder)
    for path in skill_sources:
        install.install(skills / path.parent.name, src=path.parent)
    for path, meta, body in parsed:
        name = path.name.removesuffix('.agent.md')
        # Agents are generated for every product so installed resource paths are explicit.
        body = re.sub(r'(?<![\w/])skills/([a-z0-9-]+)/SKILL\.md',
                      lambda m: str(skills / m[1] / 'SKILL.md'), body)
        for folder in ('templates', 'docs', 'agents'):
            body = body.replace('`' + folder + '/', '`' + str(resources / folder) + '/')
        body += '\n\n' + memory + '\n'
        if product == 'codex':
            data = {'name': name, 'description': meta['description'], 'developer_instructions': body}
            if 'edit' not in meta['tools']:
                data['sandbox_mode'] = 'read-only'
            rendered = '\n'.join(f'{k} = {json.dumps(v, ensure_ascii=False)}' for k, v in data.items()) + '\n'
            tomllib.loads(rendered)
            output = agents / (name + '.toml')
        else:
            if product == 'opencode':
                # Preserve the source allowlist, including denial of unlisted MCP tools.
                # Skills and questions are needed to use these instruction-only agents.
                permission = {'*': 'deny', 'skill': 'allow', 'question': 'allow',
                              'external_directory': {'*': 'ask', str(skills) + '/*': 'allow',
                                                     str(resources) + '/*': 'allow',
                                                     str(SOURCE / 'skills') + '/*': 'allow',
                                                     **{str(SOURCE / folder) + '/*': 'allow'
                                                        for folder in ('templates', 'docs', 'agents', 'memory')}}}
                mapping = {'read': ['read'], 'edit': ['edit'], 'search': ['glob', 'grep', 'list'],
                           'execute': ['bash'], 'web': ['webfetch', 'websearch']}
                for capability, keys in mapping.items():
                    if capability in meta['tools']:
                        action = 'allow' if capability in ('read', 'search') else 'ask'
                        permission.update(dict.fromkeys(keys, action))
                meta = {'description': meta['description'], 'mode': 'subagent', 'permission': permission}
            rendered = '---\n' + yaml.safe_dump(meta, sort_keys=False, allow_unicode=True) + '---\n\n' + body
            output = agents / (name + ('.md' if product == 'opencode' else '.agent.md'))
        install.install(output, text=rendered)
    install.instructions(instructions, guidance)

    # Migrate matching product-specific skills to the shared discovery root.
    for path in skill_sources:
        old = base / 'skills' / path.parent.name
        if old == skills / path.parent.name:
            continue
        if old.is_symlink() and old.resolve() == path.parent.resolve():
            install.backup(old)
        elif old.is_dir() and not old.is_symlink() and same_tree(old, path.parent):
            install.backup(old)
        elif old.exists() or old.is_symlink():
            print(f'Warning: retained modified legacy skill {old}; check for duplicate discovery.')
    if product == 'codex':
        for path in agent_sources:
            old = agents / path.name
            if old.is_file() and old.read_bytes() == path.read_bytes():
                install.backup(old)
    print(f'Installed {len(skill_sources)} skills in {skills}')
    print(f'Generated {len(agent_sources)} {product} agents in {agents}')
    print(f'Updated managed instructions in {instructions}')
    if install.backup_root:
        print(f'Previous files saved in {install.backup_root}')
    print('Restart the client. Re-run this command after changing agents, memory, or copied sources.')


if __name__ == '__main__':
    try:
        main()
    except (OSError, ValueError, yaml.YAMLError) as error:
        sys.exit(f'error: {error}')
