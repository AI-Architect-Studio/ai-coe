"""Confirm installed skills through Codex app-server. No model turn is started."""

import argparse
import asyncio
import json
import os
from pathlib import Path
import subprocess
import tempfile


async def request(process, message):
    process.stdin.write((json.dumps(message) + "\n").encode())
    await process.stdin.drain()
    if "id" not in message:
        return
    while line := await process.stdout.readline():
        response = json.loads(line)
        if response.get("id") == message["id"]:
            if "error" in response:
                raise RuntimeError(str(response["error"]))
            return response["result"]
    raise RuntimeError("Codex closed before returning the response")


async def probe(workspace, names, profile):
    process = await asyncio.create_subprocess_exec(
        "codex", "app-server", cwd=workspace, env={**os.environ, "CODEX_HOME": profile}, stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.DEVNULL,
        limit=8 * 1024 * 1024,
    )
    try:
        await request(process, {"id": 1, "method": "initialize", "params": {
            "clientInfo": {"name": "coe-compatibility", "version": "1.0"},
            "capabilities": {"experimentalApi": True},
        }})
        await request(process, {"method": "initialized", "params": {}})
        result = await request(process, {"id": 2, "method": "skills/list", "params": {
            "cwds": [str(workspace)], "forceReload": True,
        }})
        observed = set()
        for entry in result["data"]:
            for skill in entry["skills"]:
                name = skill["name"]
                expected = workspace / ".agents" / "skills" / name / "SKILL.md"
                if name in names and skill["scope"] == "repo" and skill["enabled"] and Path(skill["path"]) == expected:
                    observed.add(name)
        missing = set(names) - observed
        if missing:
            raise RuntimeError("missing project skills: " + ", ".join(sorted(missing)))
        return sorted(observed)
    finally:
        if process.returncode is None:
            process.terminate()
        await process.wait()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", required=True, type=Path)
    parser.add_argument("--skill", action="append")
    args = parser.parse_args()
    lock = json.loads(Path(__file__).with_name("skills.lock.json").read_text())
    try:
        with tempfile.TemporaryDirectory(prefix="coe-codex-probe-") as profile:
            result = asyncio.run(asyncio.wait_for(probe(args.workspace.resolve(), args.skill or list(lock["skills"]), profile), timeout=30))
        version = subprocess.check_output(["codex", "--version"], text=True).strip()
    except (OSError, RuntimeError, TimeoutError, KeyError, ValueError) as exc:
        parser.exit(1, f"Codex discovery failed: {exc}\n")
    print(json.dumps({"client": version, "method": "skills/list", "enabled_repo_skills": result,
                      "model_turns": 0}, indent=2))


if __name__ == "__main__":
    main()
