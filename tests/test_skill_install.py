import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("skill_installer", ROOT / "integrations/codex/install.py")
installer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(installer)
ASSESS = ["ai-coe-assessment"]


class TestSkillInstall(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.space = Path(temp.name)
        self.installed = self.space / ".agents/skills/ai-coe-assessment"

    def apply(self, enabled=True):
        return installer.install(self.space, None, ASSESS, enabled)

    def test_preview_and_idempotent_install(self):
        self.assertEqual(self.apply(False)[ASSESS[0]], "would_install")
        self.assertEqual(list(self.space.iterdir()), [])
        self.assertEqual(self.apply()[ASSESS[0]], "install")
        self.assertIn("MIT License", (self.installed / "LICENSE").read_text())
        self.assertEqual(self.apply()[ASSESS[0]], "present")

    def test_existing_changes_survive(self):
        self.apply()
        local = self.installed / "SKILL.md"
        local.write_text("user-authored local work")
        with self.assertRaisesRegex(ValueError, "local edits"):
            self.apply()
        self.assertEqual(local.read_text(), "user-authored local work")

    def test_symlink_destination_rejected(self):
        with tempfile.TemporaryDirectory() as outside:
            (self.space / ".agents").symlink_to(outside, target_is_directory=True)
            with self.assertRaisesRegex(ValueError, "ordinary directory"):
                self.apply()
            self.assertEqual(list(Path(outside).iterdir()), [])

    def test_unresolved_dependency_leaves_no_partial_install(self):
        with self.assertRaisesRegex(ValueError, "upstream"):
            installer.install(self.space, None, None, True)
        self.assertEqual(list(self.space.iterdir()), [])

    def test_blob_from_pinned_commit_and_attribution(self):
        # A synthetic upstream lets CI exercise the immutable fetch with no network.
        repo = self.space / "upstream"
        repo.mkdir()
        subprocess.run(["git", "init", "-q", str(repo)], check=True)
        package = repo / "skills/research/claim-verification"
        package.mkdir(parents=True)
        payload = package / "SKILL.md"
        payload.write_text("approved v1")
        (repo / "LICENSE").write_text("fixture attribution")
        cmd = ["git", "-C", str(repo)]
        subprocess.run([*cmd, "add", "."], check=True)
        subprocess.run([*cmd, "-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid",
                        "commit", "-qm", "fixture"], check=True)
        revision = subprocess.check_output([*cmd, "rev-parse", "HEAD"], text=True).strip()
        payload.write_text("unreviewed worktree")
        files = installer.upstream_files(repo, revision, "skills/research/claim-verification")
        self.assertEqual(files[Path("SKILL.md")], b"approved v1")
        self.assertEqual(files[Path("UPSTREAM-LICENSE")], b"fixture attribution")


class TestFounderClaimReview(unittest.TestCase):
    def test_source_grounding_and_uncertainty(self):
        review = json.loads((ROOT / "integrations/codex/examples/founder-claim-review.json").read_text())
        intake = json.loads((ROOT / "examples/founder/input.json").read_text())
        references = {Path("examples/founder") / item["file"] for item in intake["sources"].values()}
        self.assertEqual(review["verdict"], "unverifiable")
        self.assertGreaterEqual(len(review["evidence"]), 3)
        for evidence in review["evidence"]:
            path = Path(evidence["source"])
            self.assertIn(path, references)
            self.assertIn(evidence["quote"], (ROOT / path).read_text())
