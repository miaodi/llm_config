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
    if not isinstance(meta, dict):
        raise ValueError(f'{path}: expected YAML frontmatter mapping')
    for key in ('name', 'description'):
        if not isinstance(meta.get(key), str) or not meta[key].strip():
            raise ValueError(f'{path}: missing {key}')
    return meta, parts[2].lstrip()


def same_tree(left, right):
    """Compare bytes, not timestamps; copied resources can contain directories."""
    if left.is_symlink() or right.is_symlink():
        return left.is_symlink() and right.is_symlink() and os.readlink(left) == os.readlink(right)
    if left.is_dir() and right.is_dir():
        a = {p.name for p in left.iterdir()}
        b = {p.name for p in right.iterdir()}
        return a == b and all(same_tree(left / n, right / n) for n in a)
    return left.is_file() and right.is_file() and left.read_bytes() == right.read_bytes()


def check_destination(dst):
    protected = [SOURCE / name for name in ('skills', 'agents', 'templates', 'docs', 'memory')]
    if any(dst.parent.resolve().is_relative_to(path.resolve()) for path in protected):
        raise ValueError(f'{dst}: refusing to modify source content')


def remove_entry(dst):
    """Remove the installed entry itself; never follow a directory symlink."""
    check_destination(dst)
    if dst.is_symlink() or dst.is_file():
        dst.unlink()
    elif dst.exists():
        shutil.rmtree(dst)


class Installer:
    def __init__(self, base, copy):
        self.base = base
        self.copy = copy

    def matches(self, dst, src=None, text=None):
        if text is not None:
            return dst.is_file() and not dst.is_symlink() and dst.read_text() == text
        if dst.is_symlink():
            return not self.copy and dst.resolve() == src.resolve()
        return self.copy and same_tree(src, dst)

    def install(self, dst, src=None, text=None):
        check_destination(dst)
        if self.matches(dst, src, text):
            return
        dst.parent.mkdir(parents=True, exist_ok=True)
        # Prepare on the same filesystem before replacing any existing content.
        with tempfile.TemporaryDirectory(prefix='.llm-config-stage-', dir=dst.parent) as tmp:
            staged = Path(tmp) / dst.name
            if text is not None:
                staged.write_text(text)
            elif self.copy:
                if src.is_dir():
                    shutil.copytree(src, staged, symlinks=True)
                else:
                    shutil.copy2(src, staged)
            else:
                staged.symlink_to(src.resolve(), target_is_directory=src.is_dir())
            # POSIX rename cannot replace a nonempty directory. Files and links
            # are replaced atomically; directory replacement is recoverable by rerun.
            if ((dst.is_dir() and not dst.is_symlink())
                    or (staged.is_dir() and not staged.is_symlink())):
                remove_entry(dst)
            os.replace(staged, dst)


def render_instructions(dst, content):
    previous = dst.read_text() if dst.exists() else ''
    if (previous.count(BEGIN) != previous.count(END) or previous.count(BEGIN) > 1
            or (BEGIN in previous and previous.index(BEGIN) > previous.index(END))):
        raise ValueError(f'{dst}: malformed llm-config instruction markers')
    block = BEGIN + '\n' + content.rstrip() + '\n' + END
    if BEGIN in previous:
        return re.sub(re.escape(BEGIN) + r'.*?' + re.escape(END),
                      lambda _: block, previous, flags=re.S)
    return previous + ('\n\n' if previous else '') + block + '\n'


class Ownership:
    """Store names within fixed roots, never arbitrary paths to delete."""
    def __init__(self, path, groups):
        self.path = path
        self.groups = groups
        self.previous = {group: set() for group in groups}
        if path.is_symlink():
            raise ValueError(f'{path}: ownership manifest must not be a symlink')
        if path.exists():
            data = json.loads(path.read_text())
            if (not isinstance(data, dict) or data.get('version') != 1
                    or not isinstance(data.get('entries'), dict)
                    or set(data['entries']) != set(groups)):
                raise ValueError(f'{path}: invalid ownership manifest')
            for group, names in data['entries'].items():
                if (not isinstance(names, list)
                        or any(not isinstance(name, str) or not re.fullmatch(groups[group][1], name)
                               for name in names)
                        or len(names) != len(set(names))):
                    raise ValueError(f'{path}: invalid owned names for {group}')
                self.previous[group] = set(names)
        self.desired = {group: set() for group in groups}

    def prepare(self, plans):
        for group, name, src, text in plans:
            if not re.fullmatch(self.groups[group][1], name):
                raise ValueError(f'{name}: invalid managed entry name')
            dst = self.groups[group][0] / name
            check_destination(dst)
            self.desired[group].add(name)
            if name in self.previous[group] or not (dst.exists() or dst.is_symlink()):
                continue
            # Bootstrap old installs only when their contents or source link match.
            matches = (dst.is_file() and not dst.is_symlink() and dst.read_text() == text
                       if text is not None else
                       (dst.is_symlink() and dst.resolve() == src.resolve())
                       or (not dst.is_symlink() and same_tree(src, dst)))
            if not matches:
                raise ValueError(f'{dst}: untracked destination conflicts with repository content')
        for group, names in self.previous.items():
            for name in names:
                check_destination(self.groups[group][0] / name)

    def save(self, writer, entries):
        text = json.dumps({'version': 1, 'entries': {group: sorted(names)
                          for group, names in entries.items()}}, indent=2) + '\n'
        writer.install(self.path, text=text)

    def claim(self, writer):
        # Keep old and new ownership until sync completes, so retries can clean up
        # after a failed write or interrupted directory replacement.
        self.save(writer, {group: self.previous[group] | self.desired[group]
                           for group in self.groups})

    def finish(self, writer):
        removed = 0
        for group, names in self.previous.items():
            for name in sorted(names - self.desired[group]):
                dst = self.groups[group][0] / name
                remove_entry(dst)
                removed += 1
        self.save(writer, self.desired)
        return removed


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
    for folder in ('skills', 'agents', 'templates', 'docs', 'memory'):
        if not (SOURCE / folder).is_dir():
            raise ValueError(f'{SOURCE / folder}: missing source directory')
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
        if (not isinstance(meta.get('tools'), list)
                or any(not isinstance(tool, str) or tool not in {'read', 'edit', 'search', 'execute', 'web'}
                       for tool in meta['tools'])):
            raise ValueError(f'{path}: unsupported tool list')

    # The managed block supplies a path map for source-relative references in skills.
    memory = '\n\n'.join(p.read_text().strip() for p in sorted((SOURCE / 'memory').glob('*.md')))
    guidance = (f'## llm-config resources\n\n'
                f'Resolve references to `skills/<name>/SKILL.md` through the skill catalog, '
                f'or under `{skills}`. Resolve llm-config `templates/`, `docs/`, '
                f'and source `agents/` references under `{resources}`. '
                'These paths describe instruction resources, not the project being edited.\n\n' + memory)
    instruction_text = render_instructions(instructions, guidance)
    product_plans = [('resources', folder, SOURCE / folder, None)
                     for folder in ('templates', 'docs', 'agents', 'memory')]
    skill_plans = [('skills', path.parent.name, path.parent, None) for path in skill_sources]
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
        product_plans.append(('agents', output.name, None, rendered))
    # Shared skills have one manifest regardless of which product installs them.
    # Refuse redirected managed roots before loading ownership or touching files.
    for directory in (base / 'agents', resources, skills.parent, skills, base / 'skills'):
        if directory.is_symlink():
            raise ValueError(f'{directory}: managed directory must not be a symlink')
    suffix = {'codex': r'\.toml', 'copilot': r'\.agent\.md', 'opencode': r'\.md'}[product]
    owned_product = Ownership(base / '.llm-config-manifest.json', {
        'agents': (agents, r'[a-z0-9]+(?:-[a-z0-9]+)*' + suffix),
        'resources': (resources, r'(?:templates|docs|agents|memory)'),
    })
    owned_skills = Ownership(skills.parent / '.llm-config-skills.json', {
        'skills': (skills, r'[a-z0-9]+(?:-[a-z0-9]+)*'),
    })
    owned_product.prepare(product_plans)
    owned_skills.prepare(skill_plans)
    check_destination(instructions)
    # Record intended ownership before writing destinations; no backups are made.
    owned_product.claim(install)
    owned_skills.claim(install)
    for owner, plans in ((owned_product, product_plans), (owned_skills, skill_plans)):
        for group, name, src, text in plans:
            install.install(owner.groups[group][0] / name, src=src, text=text)
    install.install(instructions, text=instruction_text)
    removed = owned_product.finish(install) + owned_skills.finish(install)

    # Remove matching legacy entries. Untracked modified copies remain unrelated
    # until ownership can be established, and are never deleted by name alone.
    for path in skill_sources:
        old = base / 'skills' / path.parent.name
        if old == skills / path.parent.name:
            continue
        if ((old.is_symlink() and old.resolve() == path.parent.resolve())
                or (old.is_dir() and not old.is_symlink() and same_tree(old, path.parent))):
            remove_entry(old)
        elif old.exists() or old.is_symlink():
            print(f'Warning: retained untracked legacy skill {old}; check for duplicate discovery.')
    if product == 'codex':
        for path in agent_sources:
            old = agents / path.name
            if old.is_file() and old.read_bytes() == path.read_bytes():
                remove_entry(old)
    print(f'Installed {len(skill_sources)} skills in {skills}')
    print(f'Generated {len(agent_sources)} {product} agents in {agents}')
    print(f'Updated managed instructions in {instructions}')
    print(f'Removed {removed} obsolete managed entries; no backups created.')
    print('Restart the client. Re-run this command after changing agents, memory, or copied sources.')


if __name__ == '__main__':
    try:
        main()
    except (OSError, ValueError, yaml.YAMLError) as error:
        sys.exit(f'error: {error}')
