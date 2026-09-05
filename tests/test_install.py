"""Integration checks use temporary homes via Path.home mocking, never real user config."""
import contextlib
import importlib.util
import io
import os
from pathlib import Path
import shutil
import sys
import tempfile
import tomllib
import unittest
from unittest.mock import patch

import yaml

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('installer', ROOT / 'scripts/install.py')
installer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(installer)


class InstallTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='llm-config-test-')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.user = self.root / 'user with spaces'
        self.user.mkdir()
        self.project = self.root / 'project with spaces'
        self.project.mkdir()
        self.home_mock = patch.object(Path, 'home', return_value=self.user)
        self.home_mock.start()
        self.addCleanup(self.home_mock.stop)
        self.env = patch.dict(os.environ, {}, clear=True)
        self.env.start()
        self.addCleanup(self.env.stop)

    def run_install(self, *args):
        with patch.object(sys, 'argv', ['setup.sh', *map(str, args)]), contextlib.redirect_stdout(io.StringIO()):
            installer.main()

    def test_all_targets_repeat_and_mode_switch(self):
        for product in ('codex', 'copilot', 'opencode'):
            for local in (False, True):
                with self.subTest(product=product, local=local):
                    args = [f'--{product}-project', self.project] if local else [f'--{product}']
                    base = ((self.project / {'codex': '.codex', 'copilot': '.github', 'opencode': '.opencode'}[product]) if local
                            else self.user / {'codex': '.codex', 'copilot': '.copilot', 'opencode': '.config/opencode'}[product])
                    skills = (self.project if local else self.user) / '.agents/skills'
                    for copy in (False, False, True, True, False):
                        self.run_install(*args, *(['--copy'] if copy else []))
                        self.assertEqual(27, len(list(skills.glob('*/SKILL.md'))))
                        self.assertEqual(not copy, (skills / 'coding').is_symlink())
                        self.assertFalse((skills / 'coding/coding').exists())
                        self.assertEqual(14, len(list((base / 'agents').iterdir())))
                        self.assertTrue((base / 'llm-config/templates/commit-message/git-p4-commit-message-template.txt').is_file())
                    # Source files remain untouched after copying over symlinks.
                    self.assertTrue((ROOT / 'skills/coding/SKILL.md').is_file())

    def test_native_formats_and_references(self):
        self.run_install('--codex-project', self.project, '--copy')
        for path in (self.project / '.codex/agents').glob('*.toml'):
            meta = tomllib.loads(path.read_text())
            self.assertEqual(path.stem, meta['name'])
            self.assertTrue(meta['description'])
            self.assertIn(str(self.project / '.agents/skills'), meta['developer_instructions'])
        p4 = tomllib.loads((self.project / '.codex/agents/p4-reviewer.toml').read_text())
        self.assertEqual('read-only', p4['sandbox_mode'])
        self.run_install('--opencode-project', self.project)
        p4, _ = installer.frontmatter(ROOT / 'agents/p4-reviewer.agent.md')
        rendered = yaml.safe_load((self.project / '.opencode/agents/p4-reviewer.md').read_text().split('---', 2)[1])
        self.assertEqual('subagent', rendered['mode'])
        self.assertEqual('deny', rendered['permission']['*'])
        self.assertNotIn('edit', rendered['permission'])
        self.assertEqual('ask', rendered['permission']['bash'])
        self.assertEqual('allow', rendered['permission']['skill'])
        self.run_install('--copilot-project', self.project)
        generated = yaml.safe_load((self.project / '.github/agents/p4-reviewer.agent.md').read_text().split('---', 2)[1])
        self.assertEqual(p4['tools'], generated['tools'])

    def test_instructions_preserve_unmanaged_text(self):
        dest = self.project / 'AGENTS.md'
        dest.write_text('# Existing rules\n\nKeep this exactly.\n')
        self.run_install('--codex-project', self.project)
        first = dest.read_text()
        self.run_install('--codex-project', self.project)
        self.assertEqual(first, dest.read_text())
        self.assertTrue(first.startswith('# Existing rules\n\nKeep this exactly.\n'))
        self.assertEqual(1, first.count(installer.BEGIN))
        self.assertIn('functional-programming', first)
        self.assertTrue(list((self.project / '.codex/.llm-config-backups').glob('*/0/AGENTS.md')))

    def test_malformed_instructions_fail_before_install(self):
        (self.project / 'AGENTS.md').write_text(installer.BEGIN)
        with self.assertRaises(ValueError):
            self.run_install('--codex-project', self.project)
        self.assertFalse((self.project / '.agents').exists())

    def test_legacy_migration_and_modified_copy_retention(self):
        base = self.project / '.codex'
        (base / 'skills').mkdir(parents=True)
        (base / 'skills/coding').symlink_to(ROOT / 'skills/coding')
        shutil.copytree(ROOT / 'skills/writing', base / 'skills/writing')
        (base / 'skills/writing/local.txt').write_text('keep my edit')
        (base / 'agents').mkdir()
        (base / 'agents/cpp-engineer.agent.md').symlink_to(ROOT / 'agents/cpp-engineer.agent.md')
        self.run_install('--codex-project', self.project)
        self.assertFalse((base / 'skills/coding').is_symlink())
        self.assertFalse((base / 'agents/cpp-engineer.agent.md').exists())
        self.assertEqual('keep my edit', (base / 'skills/writing/local.txt').read_text())
        self.assertTrue(list((base / '.llm-config-backups').glob('*/*/coding')))

    def test_custom_config_directories(self):
        os.environ['CODEX_HOME'] = str(self.root / 'custom-codex')
        self.run_install('--codex')
        self.assertTrue((self.root / 'custom-codex/agents/cpp-engineer.toml').is_file())
        self.assertTrue((self.user / '.agents/skills/coding/SKILL.md').is_file())
        os.environ['XDG_CONFIG_HOME'] = str(self.root / 'xdg')
        os.environ['OPENCODE_CONFIG_DIR'] = str(self.root / 'custom-opencode')
        self.run_install('--opencode')
        self.assertTrue((self.root / 'custom-opencode/agents/cpp-engineer.md').is_file())
        self.assertTrue((self.root / 'xdg/opencode/AGENTS.md').is_file())

    def test_source_parent_symlink_is_never_modified(self):
        linked = self.project / 'source-link'
        linked.symlink_to(ROOT / 'skills')
        writer = installer.Installer(self.project, True)
        with self.assertRaises(ValueError):
            writer.install(linked / 'coding', src=ROOT / 'skills/writing')
        with self.assertRaises(ValueError):
            writer.backup(linked / 'coding')
        self.assertTrue((ROOT / 'skills/coding/SKILL.md').exists())


    def test_copy_update_replaces_stale_content_without_nesting(self):
        src = self.root / 'source'
        src.mkdir()
        (src / 'SKILL.md').write_text('version one')
        dst = self.project / 'skills/example'
        writer = installer.Installer(self.project, True)
        writer.install(dst, src=src)
        (src / 'SKILL.md').write_text('version two')
        writer.install(dst, src=src)
        self.assertEqual('version two', (dst / 'SKILL.md').read_text())
        self.assertFalse((dst / 'source').exists())
        self.assertEqual('version one', next(writer.backup_root.glob('*/example/SKILL.md')).read_text())


class ContentTests(unittest.TestCase):
    def test_sources_and_skill_references(self):
        import re
        for path in [*ROOT.glob('skills/*/SKILL.md'), *ROOT.glob('agents/*.agent.md')]:
            meta, body = installer.frontmatter(path)
            self.assertTrue(body.strip())
            if path.name == 'SKILL.md':
                self.assertEqual(path.parent.name, meta['name'])
                self.assertLessEqual(len(meta['description']), 1024)
            for name in re.findall(r'skills/([a-z0-9-]+)/SKILL\.md', body):
                self.assertTrue((ROOT / 'skills' / name / 'SKILL.md').exists(), (path, name))


if __name__ == '__main__':
    unittest.main()
