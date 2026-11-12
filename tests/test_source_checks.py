import importlib.util
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('check_source', ROOT / 'scripts/check-source.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

class TestSourceChecker(unittest.TestCase):
    def test_project_passes(self):
        self.assertEqual(module.check(ROOT), [])
    def test_duplicate_label_detected(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)
            (path / 'index.qmd').write_text('# A {#sec-a}\n# B {#sec-a}\n')
            (path / 'references.bib').write_text('')
            self.assertTrue(any('duplicate' in err for err in module.check(path)))
    def test_missing_citation_detected(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)
            (path / 'index.qmd').write_text('Citation [@missing].\n')
            (path / 'references.bib').write_text('')
            self.assertTrue(any('missing bibliography' in err for err in module.check(path)))

if __name__ == '__main__':
    unittest.main()
