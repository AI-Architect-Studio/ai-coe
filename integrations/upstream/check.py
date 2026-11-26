#!/usr/bin/env python3
"""Exercise two pinned optional upstreams locally against their synthetic fixtures."""
import argparse
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


def run(args, folder):
    return subprocess.run(args, cwd=folder, check=True, capture_output=True,
                          encoding="utf-8", timeout=60).stdout.strip()


def check_revision(folder, revision):
    actual = run(["git", "rev-parse", "HEAD"], folder)
    if actual != revision or run(["git", "status", "--porcelain"], folder):
        raise ValueError(f"Expected clean checkout of {revision} at {folder}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--quote", type=Path, required=True)
    parser.add_argument("--harness", type=Path, required=True)
    args = parser.parse_args()
    registry = Path(__file__).resolve().parents[2] / "registry/capabilities.json"
    records = {r["id"]: r for r in json.loads(registry.read_text())["capabilities"]}
    check_revision(args.quote, records["commercial-workflow"]["revision"])
    check_revision(args.harness, records["model-economics"]["revision"])
    output = run([sys.executable, "-B", "fleet/harness_eval.py", "selftest"], args.harness)
    if "selftest OK: all 22 checkers pass ground truth" not in output:
        raise ValueError("Pinned harness checker result differed from its baseline")

    with tempfile.TemporaryDirectory() as work:
        workspace = str(Path(work) / "quote")
        command = [shutil.which("npm") or "npm", "run", "--silent", "quote:desk", "--"]
        example = "skills/quote-desk/examples/"
        config = json.loads(run(command + ["init", "--workspace", workspace, "--principal",
                               example + "principal.json", "--catalog", example + "catalog.json"], args.quote))
        intake = command + ["intake", "--workspace", workspace, "--request", example + "request.json",
                            "--service", "inspect", "--quantity", "1"]
        result = json.loads(run(intake, args.quote))
        duplicate = json.loads(run(intake, args.quote))
        record = result["record"]
        if (config["synthetic"] is not True or record["qualification"] != "fit"
                or record["price"]["subtotal"] != "120.00" or record["price"]["currency"] != "EUR"
                or record["approvalRequired"] is not True or record["outbound"] != "disabled"
                or duplicate["id"] != result["id"] or duplicate["duplicate"] is not True):
            raise ValueError("Quote result, outbound gate or idempotence differed from its baseline")

    print(json.dumps({"harness": output, "synthetic_quote_id": result["id"],
                      "draft_subtotal_eur": record["price"]["subtotal"],
                      "human_approval_required": record["approvalRequired"], "outbound": record["outbound"],
                      "duplicate_preserved": duplicate["duplicate"], "model_calls": 0}, indent=2))


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, subprocess.SubprocessError) as exc:
        sys.exit(f"upstream check failed: {exc}")
