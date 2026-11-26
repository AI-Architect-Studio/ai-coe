"""Black-box acceptance checks for owner-controlled activation workspaces."""

from concurrent.futures import ThreadPoolExecutor
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


REPO = Path(__file__).resolve().parents[1]
CLI = REPO / "scripts" / "coe.py"


class LocalBoundaries(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        self.brief = self.root / "brief"
        shutil.copytree(REPO / "examples" / "founder", self.brief)
        self.intake = self.brief / "input.json"

    def assess(self):
        return subprocess.run(
            [sys.executable, "-B", str(CLI), "assess", "--input", str(self.intake)],
            capture_output=True, text=True, cwd=self.root, check=False,
        )

    def test_unknown_excerpt_is_rejected_without_echoing_private_source(self):
        source = self.brief / "evidence" / "interview-a.txt"
        sensitive_marker = "Synthetic private interview content, outside the approved excerpt."
        source.write_text(sensitive_marker, encoding="utf-8")
        result = self.assess()
        self.assertNotEqual(result.returncode, 0)
        self.assertNotIn(sensitive_marker, result.stdout + result.stderr)

    def test_evidence_must_belong_to_the_intake_directory(self):
        data = json.loads(self.intake.read_text(encoding="utf-8"))
        entry = data["sources"]["interview-a"]
        relative = Path("..") / "separate-interview.txt"
        (self.root / relative.name).write_text(entry["excerpt"], encoding="utf-8")
        entry["file"] = str(relative)
        self.intake.write_text(json.dumps(data), encoding="utf-8")
        self.assertNotEqual(self.assess().returncode, 0)

    def test_assessment_preserves_input_files(self):
        def snapshot():
            return {p.relative_to(self.root): p.read_bytes()
                    for p in self.root.rglob("*") if p.is_file()}
        before = snapshot()
        result = self.assess()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(snapshot(), before)

    def activation(self, workspace, *args):
        return subprocess.run(
            [sys.executable, "-B", str(CLI), "activate", "--input", str(self.intake),
             "--workspace", str(workspace), *args],
            capture_output=True, text=True, cwd=self.root, check=False,
        )

    def test_preview_has_no_filesystem_side_effect(self):
        workspace = self.root / "work"
        workspace.mkdir()
        result = self.activation(workspace)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["mode"], "dry-run")
        self.assertEqual(list(workspace.iterdir()), [])

    def test_owner_change_survives_second_apply(self):
        workspace = self.root / "work"
        workspace.mkdir()
        first = self.activation(workspace, "--apply")
        self.assertEqual(first.returncode, 0, first.stderr)
        decision = workspace / ".ai-coe" / "decisions" / "first-mission.md"
        local_text = "A human decided to run a different experiment."
        decision.write_text(local_text, encoding="utf-8")
        rerun = self.activation(workspace, "--apply")
        self.assertNotEqual(rerun.returncode, 0)
        self.assertEqual(decision.read_text(encoding="utf-8"), local_text)

    def test_generated_evidence_ignored_by_git(self):
        workspace = self.root / "work"
        workspace.mkdir()
        subprocess.run(["git", "init", "-q", str(workspace)], check=True)
        result = self.activation(workspace, "--apply")
        self.assertEqual(result.returncode, 0, result.stderr)
        ignored = subprocess.run(
            ["git", "-C", str(workspace), "check-ignore", "-q", ".ai-coe/knowledge/sources.json"],
            check=False,
        )
        self.assertEqual(ignored.returncode, 0)


    def test_simultaneous_activations_publish_one_complete_workspace(self):
        workspace = self.root / "work"
        workspace.mkdir()
        preview = self.activation(workspace)
        self.assertEqual(preview.returncode, 0, preview.stderr)
        planned = set(json.loads(preview.stdout)["files"])
        with ThreadPoolExecutor(max_workers=2) as pool:
            attempts = [pool.submit(self.activation, workspace, "--apply") for _ in range(2)]
            results = [attempt.result() for attempt in attempts]
        self.assertEqual(sum(result.returncode == 0 for result in results), 1)
        installed = workspace / ".ai-coe"
        actual = {p.relative_to(installed).as_posix() for p in installed.rglob("*") if p.is_file()}
        self.assertEqual(actual, planned)
        self.assertEqual(list(workspace.iterdir()), [installed])
