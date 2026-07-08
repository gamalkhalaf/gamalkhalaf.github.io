import importlib.util
import tempfile
import textwrap
import unittest
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = REPO_ROOT / 'scripts' / 'generate_cms.py'

spec = importlib.util.spec_from_file_location('generate_cms', MODULE_PATH)
generate_cms = importlib.util.module_from_spec(spec)
spec.loader.exec_module(generate_cms)


class GenerateCmsTest(unittest.TestCase):
    def test_preserves_existing_collections_and_adds_subject_collections(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            subjects_dir = root / 'docs' / 'admin' / 'subjects'
            subjects_dir.mkdir(parents=True)
            config_path = root / 'docs' / 'admin' / 'config.yml'
            config_path.parent.mkdir(parents=True, exist_ok=True)
            config_path.write_text(
                textwrap.dedent(
                    """\
                    backend:
                      name: github
                    media_folder: docs/assets/images
                    public_folder: /assets/images
                    collections:
                      - name: subjects
                        label: المواد الدراسية
                        folder: docs/admin/subjects
                        create: true
                        extension: yml
                        format: yaml
                        fields: []
                      - name: adab_lessons
                        label: دروس في الأدب
                        folder: docs/adab
                        create: true
                        slug: '{{slug}}'
                        fields: []
                      - name: legacy_lessons
                        label: دروس قديمة
                        folder: docs/legacy
                        create: true
                        slug: '{{slug}}'
                        fields: []
                    """
                ),
                encoding='utf-8',
            )
            (subjects_dir / 'adab.yml').write_text('slug: adab\nlabel: الأدب\n', encoding='utf-8')

            generate_cms.ROOT = str(root)
            generate_cms.SUBJECTS_DIR = str(subjects_dir)
            generate_cms.CONFIG_PATH = str(config_path)
            generate_cms.main()

            with config_path.open('r', encoding='utf-8') as handle:
                generated = yaml.safe_load(handle)

            names = [collection['name'] for collection in generated['collections']]
            self.assertIn('subjects', names)
            self.assertIn('adab_lessons', names)
            self.assertIn('legacy_lessons', names)
            self.assertEqual(names.count('adab_lessons'), 1)


if __name__ == '__main__':
    unittest.main()
