"""Run a real repository-selection mission using public Git objects in this checkout."""
import argparse
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
BASE = "064826f3c6c9f662c6f3f9b364ff428b48efcd91"


def git(*args):
    return subprocess.check_output(["git", "-C", str(ROOT), *args])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", type=Path, required=True)
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    scope = {
        "governance": ["governance/trust-tiers.md", "governance/data-boundaries.md"],
        "operations": ["operating-model/01-intake.md", "operating-model/04-review.md"],
        "roles": ["agents/chief-of-staff.md", "agents/governance-agent.md"],
    }
    with tempfile.TemporaryDirectory() as directory:
        brief = Path(directory)
        sources = {}
        for key, paths in scope.items():
            facts = [f"{path} SHA256 {sha256(git('show', BASE + ':' + path)).hexdigest()}" for path in paths]
            (brief / (key + ".txt")).write_text("\n".join(facts) + "\n")
            sources[key] = {"file": key + ".txt", "excerpt": facts[0]}
        names = git("ls-tree", "--name-only", BASE).decode().splitlines()
        license_fact = f"Root LICENSE present at {BASE}: {'yes' if 'LICENSE' in names else 'no'}."
        (brief / "licensing.txt").write_text(license_fact + "\n")
        sources["licensing"] = {"file":"licensing.txt", "excerpt":license_fact}
        intake = {"version":1, "audience":"founder", "owner":"CoE release reviewer",
                  "goal":"Choose a repository to extend for workspace activation.", "tools":["Git","Python"],
                  "sources":sources, "attestations":[],
                  "candidates":[{"id":"extend", "action":"Extend the existing CoE operating model.",
                                 "supports":list(scope), "challenges":["licensing"],
                                 "experiment":"Add an activation contribution with explicit license scope and run a clean-checkout review."},
                                {"id":"separate","action":"Establish a separate repository.",
                                 "supports":["licensing"], "challenges":["operations","roles"],
                                 "experiment":"Identify a capability owner the existing project cannot serve."}]}
        (brief / "input.json").write_text(json.dumps(intake))
        cmd = [sys.executable, str(ROOT/"scripts/coe.py"), "activate", "--input", str(brief/"input.json"),
               "--workspace", str(args.workspace)]
        if args.apply:
            cmd.append("--apply")
        subprocess.run(cmd, check=True)


if __name__ == "__main__":
    main()
