"""Install a selected, pinned set of CoE skills in a local Git workspace."""

import argparse
import io
import json
from pathlib import Path
import subprocess
import tarfile
import tempfile


ROOT = Path(__file__).resolve().parents[2]
LOCK = Path(__file__).with_name("skills.lock.json")


def git_bytes(repo, *args):
    return subprocess.check_output(["git", "--no-replace-objects", "-C", str(repo), *args])


def upstream_files(repo, revision, source):
    archive = git_bytes(repo, "archive", "--format=tar", revision, "--", source, "LICENSE")
    files = {}
    with tarfile.open(fileobj=io.BytesIO(archive), mode="r:") as bundle:
        for member in bundle:
            if member.isdir():
                continue
            if not member.isfile():
                raise ValueError(f"unsupported dependency file: {member.name}")
            if member.name == "LICENSE":
                relative = Path("UPSTREAM-LICENSE")
            else:
                relative = Path(member.name).relative_to(source)
            if relative.is_absolute() or ".." in relative.parts:
                raise ValueError("unsafe dependency path")
            files[relative] = bundle.extractfile(member).read()
    if Path("SKILL.md") not in files or Path("UPSTREAM-LICENSE") not in files:
        raise ValueError(f"incomplete locked dependency: {source}")
    return files


def check_destination(path):
    if path.is_symlink() or (path.exists() and not path.is_dir()):
        raise ValueError(f"expected an ordinary directory: {path}")


def matches(path, files):
    actual = {}
    for item in path.rglob("*"):
        if item.is_symlink() or not (item.is_dir() or item.is_file()):
            return False
        if item.is_file():
            actual[item.relative_to(path)] = item.read_bytes()
    return actual == files


def install(workspace, upstream, selected, apply):
    lock = json.loads(LOCK.read_text())
    workspace = workspace.resolve(strict=True)
    if not workspace.is_dir():
        raise ValueError("workspace must be an existing directory")
    agent_dir = workspace / ".agents"
    target = agent_dir / "skills"
    for directory in (agent_dir, target):
        check_destination(directory)

    wanted = set(selected or lock["skills"])
    unknown = wanted - lock["skills"].keys()
    if unknown:
        raise ValueError("unknown skills: " + ", ".join(sorted(unknown)))
    plan = []
    for name in sorted(wanted):
        source = lock["skills"][name]
        if source["owner"] == "local":
            files = {Path(item): (ROOT / source["path"] / item).read_bytes()
                     for item in ("SKILL.md", "LICENSE")}
        else:
            if upstream is None:
                raise ValueError("provide --upstream with the locked skill repository or select only ai-coe-assessment")
            files = upstream_files(upstream, lock["revision"], source["path"])
        dest = target / name
        check_destination(dest)
        if dest.exists():
            if not matches(dest, files):
                raise ValueError(f"local edits or unrelated content at {dest}; resolve before installing")
            status = "present"
        else:
            status = "install" if apply else "would_install"
        plan.append((dest, status, files))

    # Preflight the complete selection before publishing any skill. Each skill
    # appears as an entire directory; interruption is safe to retry.
    if apply:
        target.mkdir(parents=True, exist_ok=True)
        for dest, status, files in plan:
            if status == "present":
                continue
            with tempfile.TemporaryDirectory(dir=target) as temp:
                staged = Path(temp) / "package"
                for relative, data in files.items():
                    path = staged / relative
                    path.parent.mkdir(parents=True, exist_ok=True)
                    path.write_bytes(data)
                try:
                    staged.rename(dest)
                except OSError:
                    if dest.is_symlink() or not dest.is_dir() or not matches(dest, files):
                        raise
    return {dest.name: status for dest, status, _files in plan}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", required=True, type=Path)
    parser.add_argument("--upstream", type=Path, help="local checkout containing the locked Git revision")
    parser.add_argument("--skill", action="append", help="select a skill by name; repeats allowed")
    parser.add_argument("--apply", action="store_true", help="apply the displayed installation to this workspace")
    args = parser.parse_args()
    try:
        result = install(args.workspace, args.upstream, args.skill, args.apply)
    except (OSError, ValueError, subprocess.CalledProcessError, tarfile.TarError) as exc:
        parser.exit(1, f"skill install failed: {exc}\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
