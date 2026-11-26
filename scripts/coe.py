#!/usr/bin/env python3
"""Assess evidence and activate an owner-controlled CoE with Python 3.10+."""
import argparse
from collections import Counter
from hashlib import sha256
import html
import json
import os
from pathlib import Path
import re
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
RUBRIC = json.loads((ROOT / "assessments/rubric.json").read_text())
SCHEMA = json.loads((ROOT / "schemas/intake.schema.json").read_text())
LIMIT = 256 * 1024


def require(ok, message):
    if not ok:
        raise ValueError(message)


def as_json(value):
    return json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + "\n"


def validate(value, schema, where):
    """The subset of JSON Schema used by the bundled intake contract."""
    kind = schema["type"]
    expected = {"object": dict, "array": list, "string": str, "integer": int}[kind]
    require(type(value) is expected, f"{where}: expected {kind}")
    if "enum" in schema:
        require(value in schema["enum"], f"{where}: unknown choice")
    if "const" in schema:
        require(value == schema["const"], f"{where}: unsupported version")
    if kind == "string":
        require(value.strip() and len(value) <= schema.get("maxLength", 1500), f"{where}: invalid length")
        if "pattern" in schema:
            require(re.fullmatch(schema["pattern"], value), f"{where}: invalid identifier")
    if kind == "array":
        require(schema["minItems"] <= len(value) <= schema["maxItems"], f"{where}: invalid count")
        if schema["uniqueItems"]:
            unique = {json.dumps(v, sort_keys=True) for v in value}
            require(len(unique) == len(value), f"{where}: duplicate item")
        for i, item in enumerate(value):
            validate(item, schema["items"], f"{where}[{i}]")
    if kind == "object":
        if "properties" in schema:
            require(set(value) == set(schema["required"]), f"{where}: missing or unexpected fields")
            for key, item in value.items():
                validate(item, schema["properties"][key], f"{where}.{key}")
        else:
            require(schema["minProperties"] <= len(value) <= schema["maxProperties"], f"{where}: invalid count")
            for key, item in value.items():
                validate(key, schema["propertyNames"], where)
                validate(item, schema["additionalProperties"], f"{where}.{key}")


def unique_fields(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, f"duplicate JSON field: {key}")
        result[key] = value
    return result


def bounded_bytes(path):
    require(path.is_file(), f"expected regular file: {path.name}")
    with path.open("rb") as stream:
        data = stream.read(LIMIT + 1)
    require(len(data) <= LIMIT, f"{path.name}: file exceeds 256 KiB")
    return data


def load_intake(path):
    path = path.absolute()
    require(not path.is_symlink(), "intake must be a regular file")
    intake = json.loads(bounded_bytes(path), object_pairs_hook=unique_fields)
    validate(intake, SCHEMA, "intake")
    sources = {}
    snapshots = {}
    for key, spec in intake["sources"].items():
        rel = Path(spec["file"])
        require(not rel.is_absolute() and ".." not in rel.parts and rel.parts, f"{key}: invalid evidence path")
        source = path.parent
        for part in rel.parts:
            source = source / part
            require(not source.is_symlink(), f"{key}: evidence must be inside intake directory without symlinks")
        data = bounded_bytes(source)
        require(spec["excerpt"] in data.decode("utf-8"), f"{key}: excerpt missing from source")
        digest = sha256(data).hexdigest()
        snapshots[digest] = data.decode("utf-8")
        sources[key] = {**spec, "sha256": digest}
    ids = set()
    for candidate in intake["candidates"]:
        cid = candidate["id"]
        require(cid not in ids, f"duplicate candidate: {cid}")
        ids.add(cid)
        support, challenge = map(set, (candidate["supports"], candidate["challenges"]))
        require((support | challenge) <= sources.keys(), f"{cid}: unknown source")
        require(not support & challenge, f"{cid}: same reference on both sides")
    for entry in intake["attestations"]:
        require(entry["source"] in sources, "unknown assessment source")
    return intake, sources, snapshots


def assess(intake, sources, blueprint):
    rows = {}
    for domain, first_action in RUBRIC["domains"].items():
        claims = {level["gate"]: set() for level in RUBRIC["levels"]}
        for entry in intake["attestations"]:
            if entry["domain"] == domain:
                claims[entry["gate"]].add(entry["source"])
        level = 0
        evidence = []
        seen = set()
        for step in RUBRIC["levels"]:
            ids = sorted(claims[step["gate"]])
            distinct = {sources[i]["sha256"] for i in ids}
            if not distinct - seen:
                break
            level = step["level"]
            seen.update(distinct)
            evidence.extend(ids)
        next_action = first_action if not level else (
            RUBRIC["levels"][level]["requirement"] if level < 5 else "Repeat the comparison with a new mission.")
        rows[domain] = {"level": level or None, "evidence": evidence, "next_evidence": next_action}
    tools = Counter(t.strip().casefold() for t in intake["tools"])
    return {"version": 1, "blueprint": intake["audience"], "goal": intake["goal"], "evidence_status":"owner-attested; excerpts and distinct artifact hashes checked", "domains": rows,
            "roadmap": [{"domain": d, "collect": rows[d]["next_evidence"]} for d in blueprint["priority_domains"]],
            "tool_review": {"duplicate_labels": sorted(t for t, count in tools.items() if count > 1),
                            "required_for_first_mission": ["Python 3.10+"], "declared": intake["tools"]}}


def markdown_text(text):
    text = " ".join(text.split())
    return re.sub(r"([\\`*_{}\[\]()#+.!|~>-])", r"\\\1", html.escape(text))


def prepare(intake, sources, snapshots, blueprint, assessment):
    candidates = intake["candidates"]
    def distinct(ids):
        return len({sources[key]["sha256"] for key in ids})
    ranked = sorted(candidates, key=lambda c: (-distinct(c["supports"]), c["id"]))
    top = ranked[0]
    supports = distinct(top["supports"])
    tied = sum(distinct(c["supports"]) == supports for c in ranked) > 1
    decision = "review experiment"
    if not supports or tied:
        decision = "collect evidence"
    elif distinct(top["challenges"]) >= supports:
        decision = "resolve conflicting evidence"
    brief = [f"# {blueprint['artifact'].capitalize()}", "", markdown_text(intake["goal"]), "",
             f"Owner: {markdown_text(intake['owner'])}", f"Disposition: {decision}.", ""]
    for candidate in ranked:
        brief += [f"## {markdown_text(candidate['action'])}", ""]
        for label in ("supports", "challenges"):
            brief += [f"**{label.title()}**"]
            for key in candidate[label]:
                brief += [f"- {key} — {markdown_text(sources[key]['excerpt'])}"]
            if not candidate[label]:
                brief += ["- No supplied observation."]
        brief += ["", f"Experiment: {markdown_text(candidate['experiment'])}", ""]
    brief += [blueprint["review_question"], "", "Decision owner sign-off: pending."]
    receipt = {"version": 1, "disposition": decision, "lead": top["id"] if decision == "review experiment" else None,
               "candidates": len(ranked), "source_files_by_digest": distinct(sources.keys()),
               "challenges_on_lead": top["challenges"], "provider_calls": 0, "provider_cost": {"currency":"USD","amount":0},
               "checks": {"all_excerpts_match":True,"lead_has_counterevidence":bool(top["challenges"]),
                          "unique_lead_with_support":bool(supports and not tied)},
               "human_review": "pending", "model_quality_evaluated": False}
    replay_sources = {k: {"excerpt": v["excerpt"], "file": f"evidence/{v['sha256']}.txt"}
                      for k, v in sources.items()}
    evidence_files = {f"replay/evidence/{digest}.txt": body for digest, body in snapshots.items()}
    return {
        **evidence_files,
        "replay/input.json": as_json({**intake, "sources":replay_sources}),
        ".gitignore": "*\n",
        "configuration.json": as_json({**blueprint,"owner":intake["owner"],"tools":intake["tools"],
                                       "external_actions":"require separate owner approval","agent_runtime":"unbound"}),
        "knowledge/sources.json": as_json(sources), "decisions/first-mission.md": "\n".join(brief)+"\n",
        "evaluations/receipt.json": as_json(receipt), "assessments/baseline.json": as_json(assessment),
        "workflows/first-mission.md": (ROOT/"workflows/first-mission.md").read_text(),
        "roles/mission-owner.md": f"# Mission owner\n\nOwn the decision and the review question. "
            f"Record a reason for accepting, revising or rejecting the proposed experiment.\n\n"
            f"Upstream role: https://github.com/AI-Architect-Studio/ai-coe/blob/main/{blueprint['role']}\n",
        "improvements/proposal.json":as_json({"state":"proposed","owner":intake["owner"],
            "change":"Collect a fresh disconfirming observation and repeat the decision.",
            "learning_question":blueprint["review_question"],"baseline":receipt["source_files_by_digest"],
            "comparison":"Compare accepted decision, contradictory observations and operator interventions on the next run.",
            "required_review":["source owner","workflow owner"],"automatically_applied":False})}


def publish(workspace, files, apply):
    workspace = workspace.absolute()
    require(workspace.is_dir() and workspace == workspace.resolve(), "provide an existing workspace without symlink components")
    destination = workspace / ".ai-coe"
    require(not os.path.lexists(destination), "workspace already contains .ai-coe; existing state preserved")
    if not apply:
        return
    lock = workspace / ".ai-coe-activation.lock"
    with lock.open("x"):
        try:
            require(not os.path.lexists(destination), "workspace already active")
            with tempfile.TemporaryDirectory(prefix=".coe-stage-", dir=workspace) as stage:
                (Path(stage) / ".gitignore").write_text("*\n", encoding="ascii")
                generated = Path(stage) / "workspace"
                generated.mkdir(mode=0o700)
                for name, content in files.items():
                    target = generated/name
                    target.parent.mkdir(parents=True, exist_ok=True)
                    target.write_bytes(content.encode("utf-8"))
                generated.rename(destination)
        finally:
            lock.unlink()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    assessment = commands.add_parser("assess")
    activation = commands.add_parser("activate")
    for p in (assessment, activation):
        p.add_argument("--input", type=Path, required=True)
    activation.add_argument("--workspace", type=Path, required=True)
    activation.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    intake, sources, snapshots = load_intake(args.input)
    blueprint = json.loads((ROOT / "blueprints" / intake["audience"] / "blueprint.json").read_text())
    report = assess(intake, sources, blueprint)
    if args.command == "assess":
        return report
    files = prepare(intake, sources, snapshots, blueprint, report)
    publish(args.workspace, files, args.apply)
    return {"mode":"applied" if args.apply else "dry-run","blueprint":intake["audience"],
            "destination":str(args.workspace / ".ai-coe"),"files":sorted(files),
            "mission":json.loads(files["evaluations/receipt.json"])}


if __name__ == "__main__":
    try:
        print(as_json(main()), end="")
    except (OSError, ValueError, RecursionError) as error:
        print(f"coe: {error}", file=sys.stderr)
        sys.exit(2)
