"""Integration checks use temporary homes via Path.home mocking, never real user config."""
import contextlib
import importlib.util
import io
import os
from pathlib import Path
import shutil
import subprocess
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


class InstallFixture:
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


class InstallTests(InstallFixture, unittest.TestCase):
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
                        self.assertEqual(len(list((ROOT / 'skills').glob('*/SKILL.md'))), len(list(skills.glob('*/SKILL.md'))))
                        self.assertEqual(not copy, (skills / 'coding').is_symlink())
                        self.assertFalse((skills / 'coding/coding').exists())
                        self.assertEqual(len(list((ROOT / 'agents').glob('*.agent.md'))), len(list((base / 'agents').iterdir())))
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

    def test_paper_reviewer_deployment_preserves_config_and_migrates_legacy(self):
        base = self.user / '.codex'
        base.mkdir()
        config = base / 'config.toml'
        config.write_text('[mcp_servers.zotero.env]\nZOTERO_LOCAL = "true"\n')
        before = config.read_bytes()
        legacy = base / 'skills/paper-review'
        shutil.copytree(ROOT / 'skills/paper-review', legacy)
        self.run_install('--codex', '--copy')
        agent_path = base / 'agents/paper-reviewer.toml'
        agent = tomllib.loads(agent_path.read_text())
        installed_skill = self.user / '.agents/skills/paper-review/SKILL.md'
        self.assertIn(str(installed_skill), agent['developer_instructions'])
        self.assertEqual((ROOT / 'skills/paper-review/SKILL.md').read_bytes(), installed_skill.read_bytes())
        self.assertNotIn('sandbox_mode', agent)
        self.assertNotIn('model', agent)
        self.assertFalse(legacy.exists())
        self.assertEqual(before, config.read_bytes())
        generated = agent_path.read_bytes()
        self.run_install('--codex', '--copy')
        self.assertEqual(generated, agent_path.read_bytes())
        self.assertEqual(before, config.read_bytes())

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


class ExtendedInstallTests(InstallFixture, unittest.TestCase):
    def setUp(self):
        super().setUp()
        self.source = self.root / 'fixture source'
        for folder in ('skills', 'agents', 'templates', 'docs', 'memory'):
            (self.source / folder).mkdir(parents=True)
        skill = self.source / 'skills/example'
        skill.mkdir()
        (skill / 'SKILL.md').write_text(
            '---\nname: example\ndescription: Example skill\n---\nExample instructions.\n')
        self.agent = self.source / 'agents/example.agent.md'
        self.agent.write_text(
            '---\nname: example\ndescription: Example agent\ntools: [read, edit]\n---\n'
            'Use skills/example/SKILL.md and `docs/guide.md`.\n')
        (self.source / 'docs/guide.md').write_text('Guide')
        self.source_mock = patch.object(installer, 'SOURCE', self.source)
        self.source_mock.start()
        self.addCleanup(self.source_mock.stop)

    def test_every_memory_reaches_global_instructions_and_agents_on_update(self):
        (self.source / 'memory/z.md').write_text('Unique final preference')
        (self.source / 'memory/a.md').write_text('Unique first preference')
        self.run_install('--codex')
        base = self.user / '.codex'
        for text in ((base / 'AGENTS.md').read_text(),
                     tomllib.loads((base / 'agents/example.toml').read_text())['developer_instructions']):
            self.assertLess(text.index('Unique first preference'), text.index('Unique final preference'))
        (self.source / 'memory/a.md').write_text('Replacement preference')
        (self.source / 'memory/z.md').unlink()
        self.run_install('--codex')
        for text in ((base / 'AGENTS.md').read_text(),
                     tomllib.loads((base / 'agents/example.toml').read_text())['developer_instructions']):
            self.assertIn('Replacement preference', text)
            self.assertNotIn('Unique first preference', text)
            self.assertNotIn('Unique final preference', text)

    def test_generated_instructions_roundtrip_special_characters(self):
        special = 'Unicode: α 中文; quotes: "hello"; backslash: \\; newline:\nnext line'
        with self.agent.open('a') as f:
            f.write(special)
        self.run_install('--codex')
        base = self.user / '.codex'
        result = tomllib.loads((base / 'agents/example.toml').read_text())
        self.assertIn(special, result['developer_instructions'])
        self.assertIn(str(self.user / '.agents/skills/example/SKILL.md'), result['developer_instructions'])
        self.assertIn(str(base / 'llm-config/docs/guide.md'), result['developer_instructions'])
        self.assertNotIn('sandbox_mode', result)

    def test_invalid_sources_fail_before_destination_writes(self):
        cases = [
            'no frontmatter',
            '---\n- not a mapping\n---\nbody',
            '---\nnull\n---\nbody',
            '---\nname: example\n---\nbody',
            '---\nname: example\ndescription: 42\ntools: [read]\n---\nbody',
            '---\nname: example\ndescription: ok\ntools: read\n---\nbody',
            '---\nname: example\ndescription: ok\ntools: [unknown]\n---\nbody',
            '---\nname: example\ndescription: ok\ntools: [[read]]\n---\nbody',
        ]
        for source in cases:
            with self.subTest(source=source):
                self.agent.write_text(source)
                with self.assertRaises(ValueError):
                    self.run_install('--codex')
                self.assertFalse((self.user / '.codex').exists())
                self.assertFalse((self.user / '.agents').exists())

    def test_skill_validation_rejects_bad_name_and_description(self):
        skill = self.source / 'skills/example/SKILL.md'
        for name, description in [('different', 'ok'), ('example', 'x' * 1025)]:
            with self.subTest(name=name, length=len(description)):
                skill.write_text(f'---\nname: {name}\ndescription: {description}\n---\nbody')
                with self.assertRaises(ValueError):
                    self.run_install('--codex')
                self.assertFalse((self.user / '.codex').exists())

    def test_marker_errors_preserve_existing_file_and_make_no_install(self):
        dest = self.project / 'AGENTS.md'
        for text in [installer.END, installer.END + installer.BEGIN,
                     installer.BEGIN + installer.END + installer.BEGIN + installer.END]:
            with self.subTest(text=text):
                dest.write_text(text)
                with self.assertRaises(ValueError):
                    self.run_install('--codex-project', self.project)
                self.assertEqual(text, dest.read_text())
                self.assertFalse((self.project / '.codex').exists())
                self.assertFalse((self.project / '.agents').exists())

    def test_managed_update_preserves_prefix_suffix_and_unrelated_files(self):
        base = self.user / '.codex'
        (base / 'agents').mkdir(parents=True)
        unrelated = base / 'agents/custom.toml'
        unrelated.write_text('user-owned content')
        dest = base / 'AGENTS.md'
        dest.write_text('Prefix\n' + installer.BEGIN + '\nOld block\n' + installer.END + '\nSuffix\n')
        self.run_install('--codex')
        self.assertTrue(dest.read_text().startswith('Prefix\n' + installer.BEGIN))
        self.assertTrue(dest.read_text().endswith(installer.END + '\nSuffix\n'))
        self.assertNotIn('Old block', dest.read_text())
        self.assertEqual('user-owned content', unrelated.read_text())
        before = sorted(str(p) for p in (base / '.llm-config-backups').rglob('*'))
        self.run_install('--codex')
        self.assertEqual(before, sorted(str(p) for p in (base / '.llm-config-backups').rglob('*')))

    def test_missing_project_and_file_project_are_rejected(self):
        file = self.root / 'a file'
        file.write_text('keep')
        for path in (self.root / 'missing', file):
            with self.subTest(path=path), self.assertRaises((OSError, ValueError)):
                self.run_install('--codex-project', path)
        self.assertEqual('keep', file.read_text())
        self.assertFalse((self.user / '.agents').exists())

    def test_backup_preserves_broken_symlink_and_original_path(self):
        dst = self.project / 'broken'
        target = self.root / 'nonexistent'
        dst.symlink_to(target)
        writer = installer.Installer(self.project, False)
        writer.install(dst, text='replacement')
        backup = next(writer.backup_root.glob('*/broken'))
        self.assertTrue(backup.is_symlink())
        self.assertEqual(str(target), os.readlink(backup))
        self.assertEqual(str(dst), (backup.parent / 'original-path.txt').read_text().strip())
        self.assertEqual('replacement', dst.read_text())

    def test_backup_failure_preserves_destination(self):
        dst = self.project / 'existing'
        dst.write_text('original')
        writer = installer.Installer(self.project, False)
        with patch.object(installer.shutil, 'move', side_effect=PermissionError('denied')):
            with self.assertRaises(PermissionError):
                writer.install(dst, text='replacement')
        self.assertEqual('original', dst.read_text())

    def test_write_failure_leaves_original_recoverable_in_backup(self):
        dst = self.project / 'existing'
        dst.write_text('original')
        writer = installer.Installer(self.project, False)
        original_write = Path.write_text
        def failing_write(path, *args, **kwargs):
            if path == dst:
                raise OSError('simulated disk full')
            return original_write(path, *args, **kwargs)
        with patch.object(Path, 'write_text', failing_write):
            with self.assertRaisesRegex(OSError, 'disk full'):
                writer.install(dst, text='replacement')
        self.assertEqual('original', next(writer.backup_root.glob('*/existing')).read_text())


class EntryPointTests(unittest.TestCase):
    def run_cli(self, *args, no_site=False):
        return subprocess.run([sys.executable, *(['-S'] if no_site else []),
                               str(ROOT / 'scripts/install.py'), *args],
                              text=True, capture_output=True, timeout=20)

    def test_invalid_cli_arguments_fail(self):
        for args in [(), ('--codex', '--copilot'), ('--unknown',)]:
            with self.subTest(args=args):
                result = self.run_cli(*args)
                self.assertEqual(2, result.returncode)
                self.assertIn('usage:', result.stderr)

    def test_missing_dependency_reports_actionable_error(self):
        result = self.run_cli('--codex', no_site=True)
        self.assertNotEqual(0, result.returncode)
        self.assertIn('install PyYAML', result.stderr)
        self.assertNotIn('Traceback', result.stderr)

    def test_setup_shell_entry_point_with_spaces(self):
        with tempfile.TemporaryDirectory(prefix='installer shell test ') as tmp:
            base = Path(tmp)
            project = base / 'project with spaces'
            project.mkdir()
            env = dict(os.environ, PATH=str(Path(sys.executable).parent) + os.pathsep + os.defpath)
            result = subprocess.run(['/bin/bash', str(ROOT / 'setup.sh'),
                                     '--codex-project', str(project)],
                                    env=env, cwd=base, text=True, capture_output=True, timeout=20)
            self.assertEqual(0, result.returncode, result.stderr)
            self.assertTrue((project / 'AGENTS.md').is_file())
            self.assertTrue((project / '.codex/agents/paper-reviewer.toml').is_file())


if __name__ == '__main__':
    unittest.main()
