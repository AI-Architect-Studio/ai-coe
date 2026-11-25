import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("coe", ROOT / "scripts/coe.py")
coe = importlib.util.module_from_spec(spec)
spec.loader.exec_module(coe)


class MissionTests(unittest.TestCase):
    def setUp(self):
        self.intake, self.sources, self.snapshots = coe.load_intake(ROOT / "examples/founder/input.json")
        self.bp = json.loads((ROOT / "blueprints/founder/blueprint.json").read_text())

    def output(self):
        assessment = coe.assess(self.intake, self.sources, self.bp)
        return coe.prepare(self.intake, self.sources, self.snapshots, self.bp, assessment)

    def test_all_profiles(self):
        for audience in ("personal", "creator", "founder", "enterprise"):
            with self.subTest(audience=audience):
                self.intake["audience"] = audience
                self.bp = json.loads((ROOT / "blueprints" / audience / "blueprint.json").read_text())
                result = self.output()
                self.assertTrue((ROOT / self.bp["role"]).is_file())
                self.assertTrue((ROOT / self.bp["template"]).is_file())
                self.assertEqual(json.loads(result["configuration.json"])["blueprint"], audience)
                self.assertEqual(len(json.loads(result["assessments/baseline.json"])["domains"]), 11)

    def test_replay_after_move(self):
        files = self.output()
        with tempfile.TemporaryDirectory() as temp:
            workspace = Path(temp)
            coe.publish(workspace, files, True)
            copied, sources, snapshots = coe.load_intake(workspace / ".ai-coe/replay/input.json")
            baseline = coe.assess(copied, sources, self.bp)
            repeat = coe.prepare(copied, sources, snapshots, self.bp, baseline)
            for key in ["decisions/first-mission.md", "evaluations/receipt.json","assessments/baseline.json"]:
                self.assertEqual(files[key], repeat[key])

    def test_opposition_changes_disposition(self):
        self.intake["candidates"][0]["challenges"].append("studio-note")
        receipt = json.loads(self.output()["evaluations/receipt.json"])
        self.assertEqual(receipt["disposition"], "resolve conflicting evidence")
        self.assertIsNone(receipt["lead"])

    def test_tie_withholds_lead(self):
        self.intake["candidates"][1]["supports"] = ["interview-a", "interview-b"]
        self.assertEqual(json.loads(self.output()["evaluations/receipt.json"])["disposition"], "collect evidence")

    def test_maturity_requires_sequential_distinct_evidence(self):
        claims = self.intake["attestations"]
        for gate in ["repeated", "connected", "governed", "improved"]:
            claims.append({"domain":"human-expertise", "gate":gate, "source":"studio-note"})
        def level():
            return json.loads(self.output()["assessments/baseline.json"])["domains"]["human-expertise"]["level"]
        self.assertEqual(level(), 1)
        next(c for c in claims if c["gate"] == "repeated")["source"] = "interview-a"
        self.assertEqual(level(), 2)

    def test_checked_example_matches_runner(self):
        example = ROOT / "examples/founder/workspace"
        for name, body in self.output().items():
            with self.subTest(path=name):
                self.assertEqual((example / name).read_bytes(), body.encode())
