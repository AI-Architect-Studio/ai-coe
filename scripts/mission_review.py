#!/usr/bin/env python3
"""Record a local human review and compare two reviewed missions."""
import argparse
from hashlib import sha256
import json
import os
from pathlib import Path
import sys
import tempfile

sys.dont_write_bytecode = True

from coe import as_json, bounded_bytes, load_intake, require


def activation(workspace):
    workspace = workspace.absolute()
    root = workspace / ".ai-coe"
    require(root.is_dir() and root.resolve() == root, "expected an activated local workspace without symlinks")
    return root


def asset(root, path):
    file = root / path
    require(file == file.resolve(), f"expected ordinary workspace artifact: {path}")
    return bounded_bytes(file)


def identity(root):
    config = json.loads(asset(root, "configuration.json"))
    baseline = json.loads(asset(root, "assessments/baseline.json"))
    return {"owner":config["owner"], "blueprint": config["blueprint"], "goal":baseline["goal"]}


def digests(root):
    paths = ["decisions/first-mission.md", "evaluations/receipt.json", "assessments/baseline.json",
             "knowledge/sources.json", "replay/input.json"]
    recorded = {name: sha256(asset(root, name)).hexdigest() for name in paths}
    _, replay, _ = load_intake(root / "replay/input.json")
    manifest = json.loads(asset(root, "knowledge/sources.json"))
    require(isinstance(manifest, dict) and replay.keys() == manifest.keys(), "source inventory changed")
    for key, source in replay.items():
        require(isinstance(manifest[key], dict)
                and all(source[field] == manifest[key].get(field) for field in ("sha256", "excerpt")),
                "replay and recorded source evidence differ")
    return recorded


def record(args):
    root = activation(args.workspace)
    require(args.reviewer.strip() and len(args.reviewer) <= 120, "provide the reviewer name")
    require(args.reason.strip() and len(args.reason) <= 2000, "provide a bounded reason")
    require(0 <= args.minutes <= 1000000 and 0 <= args.interventions <= 1000000, "metrics must be nonnegative and bounded")
    review = {"version":1, **identity(root), "reviewer":args.reviewer, "decision":args.decision,
              "reason":args.reason, "minutes":args.minutes, "interventions":args.interventions,
              "status":"operator-attested", "artifact_sha256":digests(root)}
    dest = root / "evaluations/human-review.json"
    require(not os.path.lexists(dest), "a review already exists; preserve this record and review a new run")
    if args.apply:
        # A complete file is linked into place exclusively, including when two reviewers race.
        temp = tempfile.NamedTemporaryFile(dir=dest.parent, prefix=".review-", delete=False)
        staged = Path(temp.name)
        try:
            with temp:
                temp.write(as_json(review).encode())
            os.link(staged, dest)
        finally:
            staged.unlink(missing_ok=True)
    return {"mode":"applied" if args.apply else "dry-run", "review":review}


def reviewed(workspace):
    root = activation(workspace)
    review = json.loads(asset(root, "evaluations/human-review.json"))
    require(isinstance(review, dict) and review.get("version") == 1
            and review.get("status") == "operator-attested", "invalid review record")
    for field, limit in [("reviewer", 120), ("reason", 2000)]:
        value = review.get(field)
        require(isinstance(value, str) and value.strip() and len(value) <= limit, f"invalid review {field}")
    require(review["artifact_sha256"] == digests(root), "artifacts changed since review; compare a reviewed snapshot")
    require(all(review[k] == v for k,v in identity(root).items()), "review identity differs from workspace")
    for field in ["minutes", "interventions"]:
        require(type(review[field]) is int and 0 <= review[field] <= 1000000, f"invalid reviewed metric: {field}")
    require(review["decision"] in ["accept", "revise", "stop"], "unknown review decision")
    return review


def compare(args):
    require(args.before.resolve() != args.after.resolve(), "supply two distinct reviewed workspaces")
    before, after = reviewed(args.before), reviewed(args.after)
    for key in ["owner","blueprint","goal"]:
        require(before[key] == after[key], f"comparison requires matching {key}")
    return {"version":1, "goal":before["goal"], "decision_before":before["decision"], "decision_after":after["decision"],
            "minutes_delta":after["minutes"]-before["minutes"],
            "interventions_delta":after["interventions"]-before["interventions"],
            "basis":"Operator-attested measurements; review both evidence sets and workload before attributing a change.",
            "shared_workflow_modified":False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    review = sub.add_parser("record")
    review.add_argument("--workspace", type=Path, required=True)
    review.add_argument("--reviewer", required=True)
    review.add_argument("--decision", choices=["accept","revise","stop"], required=True)
    review.add_argument("--reason", required=True)
    review.add_argument("--minutes", type=int, required=True)
    review.add_argument("--interventions", type=int, required=True)
    review.add_argument("--apply", action="store_true")
    diff = sub.add_parser("compare")
    diff.add_argument("--before", type=Path, required=True)
    diff.add_argument("--after", type=Path, required=True)
    args = parser.parse_args()
    return record(args) if args.command == "record" else compare(args)


if __name__ == "__main__":
    try:
        print(as_json(main()), end="")
    except (KeyError, OSError, TypeError, ValueError) as error:
        sys.exit(f"coe review: {error}")
