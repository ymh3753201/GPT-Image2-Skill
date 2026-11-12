"""Local-package installation works without fetching a repository."""
import importlib.util
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("install_skills", ROOT / "scripts/install_skills.py")
installer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(installer)


class InstallTests(unittest.TestCase):
    def test_install_bundles_backend_and_updates_only_its_two_skills(self):
        with tempfile.TemporaryDirectory() as tmp:
            destination = Path(tmp) / 'skills'
            other = destination / 'another-skill'
            other.mkdir(parents=True)
            (other / 'keep.txt').write_text('keep')
            installer.install(ROOT, destination)
            launcher = destination / 'gpt-image/scripts/generate.py'
            self.assertTrue((launcher.parent / 'gpt_image_cli/cli.py').is_file())
            result = subprocess.run([sys.executable, str(launcher), '--help'],
                                    cwd=tmp, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn('--base-url', result.stdout)
            self.assertIn('gpt-image-2.6-sunburst', result.stdout)
            with self.assertRaises(ValueError):
                installer.install(ROOT, destination)
            old = destination / 'gpt-image/obsolete.txt'
            old.write_text('old')
            installer.install(ROOT, destination, replace=True)
            self.assertFalse(old.exists())
            self.assertEqual((other / 'keep.txt').read_text(), 'keep')

    def test_incomplete_package_preserves_existing_install(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / 'incomplete'
            target = Path(tmp) / 'installed'
            target.mkdir()
            marker = target / 'gpt-image'
            marker.mkdir()
            (marker / 'SKILL.md').write_text('keep')
            with self.assertRaises(ValueError):
                installer.install(source, target, replace=True)
            self.assertEqual((marker / 'SKILL.md').read_text(), 'keep')
