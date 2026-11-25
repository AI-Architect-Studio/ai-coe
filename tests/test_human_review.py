import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class HumanReview(unittest.TestCase):
    def setUp(self):
        scratch = tempfile.TemporaryDirectory()
        self.addCleanup(scratch.cleanup)
        self.before = Path(scratch.name) / "before"
        self.after = Path(scratch.name) / "after"
        for directory in (self.before, self.after):
            directory.mkdir()
            subprocess.run([sys.executable, "-B", str(ROOT / "scripts/coe.py"), "activate", "--input",
                            str(ROOT / "examples/founder/input.json"), "--workspace", str(directory), "--apply"],
                           check=True, capture_output=True)

    def call(self, *args):
        return subprocess.run([sys.executable, "-B", str(ROOT/"scripts/mission_review.py"), *map(str,args)],
                              capture_output=True, text=True)

    def review(self, workspace, minutes, *args):
        return self.call("record","--workspace",workspace,"--reviewer","Synthetic reviewer","--decision","revise",
                         "--reason","The decision needs a second operator.","--minutes",minutes,"--interventions","1",*args)

    def test_dry_run_and_preserve_review(self):
        target = self.before / ".ai-coe/evaluations/human-review.json"
        self.assertEqual(self.review(self.before,10).returncode, 0)
        self.assertFalse(target.exists())
        self.assertEqual(self.review(self.before,10,"--apply").returncode, 0)
        self.assertNotEqual(self.review(self.before,5,"--apply").returncode, 0)
        self.assertEqual(json.loads(target.read_text())["minutes"], 10)

    def test_measurement_and_changed_artifact(self):
        self.review(self.before,12,"--apply").check_returncode()
        self.review(self.after,8,"--apply").check_returncode()
        args = ("compare","--before",self.before,"--after",self.after)
        result = json.loads(self.call(*args).stdout)
        self.assertEqual(result["minutes_delta"], -4)
        (self.after / ".ai-coe/decisions/first-mission.md").write_text("changed")
        self.assertNotEqual(self.call(*args).returncode, 0)

    def test_unknown_outcome_stays_pending(self):
        self.assertNotEqual(self.call("compare","--before",self.before,"--after",self.after).returncode, 0)
        self.assertNotEqual(self.review(self.before,-1,"--apply").returncode, 0)

    def test_changed_evidence_and_malformed_review(self):
        self.review(self.before,12,"--apply").check_returncode()
        self.review(self.after,8,"--apply").check_returncode()
        args = ("compare","--before",self.before,"--after",self.after)
        source = next((self.after / ".ai-coe/replay/evidence").iterdir())
        original = source.read_bytes()
        source.write_bytes(original + b"Additional source material.")
        self.assertNotEqual(self.call(*args).returncode, 0)
        source.write_bytes(original)
        review = self.after / ".ai-coe/evaluations/human-review.json"
        data = json.loads(review.read_text())
        for invalid in [None, [], {**data, "minutes": 1000001}]:
            review.write_text(json.dumps(invalid))
            result = self.call(*args)
            self.assertNotEqual(result.returncode, 0)
            self.assertNotIn("Traceback", result.stderr)
