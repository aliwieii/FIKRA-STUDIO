import json
import subprocess
import unittest
from pathlib import Path

from fikra_v3 import repo_root
from fikra_v3.integrity_validator import run_integrity_audit
from fikra_v3.regression_guard import run_regression_checks


class TestEnginesIntegrityAndRegression(unittest.TestCase):
    def test_node_remotion_timeline_validator(self):
        r = repo_root()
        script = r / "08_PROJECT_ASSETS/CODE_AND_SCRIPTS/MOTALIM_REMOTION_VIDEO_TEMPLATE/scripts/validate-timeline.mjs"
        res = subprocess.run(["node", str(script)], capture_output=True, text=True)
        self.assertEqual(res.returncode, 0, msg=res.stderr)
        data = json.loads(res.stdout)
        self.assertTrue(data["pass"])
        self.assertEqual(data["total_words"], 13)

    def test_hyperframes_template_schema_and_rtl(self):
        r = repo_root()
        hf = r / "08_PROJECT_ASSETS/CODE_AND_SCRIPTS/HYPERFRAMES_HTML_VIDEO_TEMPLATE"
        v = json.loads((hf / "variables.json").read_text(encoding="utf-8"))
        for key in ("project_id", "episode_title", "fps", "duration_sec", "width", "height"):
            self.assertIn(key, v)
        html = (hf / "index.html").read_text(encoding="utf-8")
        self.assertIn('dir="rtl"', html)
        self.assertIn("seekToFrame", html)

    def test_regression_guard_all_pass(self):
        rep = run_regression_checks()
        self.assertTrue(rep["pass"], msg=json.dumps(rep, indent=2, ensure_ascii=False))

    def test_integrity_validator_all_pass(self):
        rep = run_integrity_audit()
        self.assertTrue(rep["pass"], msg=json.dumps(rep, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    unittest.main()
