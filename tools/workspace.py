"""Offline, owner-authorized developer setup; never a PACT approval authority.

No downloads or global installs. Obtain the exact reviewed artifacts through a
separately authorized acquisition before using this script on a fresh checkout.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import stat
import subprocess
import sys
import tarfile
import time
import tomllib
import zipfile

ROOT = Path(__file__).resolve().parents[1]
QUARANTINE = Path(".bootstrap/quarantine/EV-0068-d6e690c")
MANIFEST_HASH = "8fedff4be21abac355b8b9251d55608f75c7e2864bb6e7676c53c00cf32deefe"
PYTHONS = ("3.12.15", "3.13.16", "3.14.8")
UV_RELATIVE = Path(".bootstrap/tools/uv-0.13.0/uv-0.13.0.data/scripts/uv.exe")
START = time.monotonic()


def digest(path: Path) -> str:
    with path.open("rb") as source:
        result = hashlib.file_digest(source, "sha256")
    return result.hexdigest()


def inside(root: Path, name: str) -> Path:
    """Reject archive traversal and Windows aliases before creating any file."""
    parsed = PurePosixPath(name)
    if parsed.is_absolute() or ".." in parsed.parts or any(c in name for c in "\\:\0"):
        raise ValueError("unsafe bootstrap archive path")
    if not parsed.parts:
        raise ValueError("empty bootstrap path")
    for part in parsed.parts:
        stem = part.split(".")[0].upper()
        if (
            part.endswith((".", " "))
            or stem in {"CON", "PRN", "AUX", "NUL"}
            or (len(stem) == 4 and stem[:3] in {"COM", "LPT"} and stem[3] in "123456789")
        ):
            raise ValueError("unsafe Windows bootstrap alias")
    path = root.joinpath(*parsed.parts)
    if not path.resolve().is_relative_to(root.resolve()):
        raise ValueError("bootstrap destination escapes root")
    return path


def manifest(root: Path) -> dict:
    if not (root / QUARANTINE).resolve().is_relative_to(root.resolve()):
        raise ValueError("quarantine escapes project root")
    source = root / "docs/bootstrap-artifacts.json"
    if digest(source) != MANIFEST_HASH:
        raise ValueError("reviewed bootstrap manifest digest changed")
    data = json.loads(source.read_bytes())
    for package in data["packages"]:
        for artifact in package["artifacts"]:
            check_artifact(root, artifact)
    for runtime in data["runtimes"]:
        check_artifact(root, runtime)
    return data


def check_artifact(root: Path, artifact: dict) -> None:
    path = inside(root / QUARANTINE, artifact["filename"])
    if path.stat().st_size != artifact["size_bytes"] or digest(path) != artifact["sha256"]:
        raise ValueError("bootstrap artifact length/hash mismatch")


def validate_lock(root: Path, data: dict) -> None:
    """uv's local flat-index resolver omits hashes; require measured bindings."""
    lock = tomllib.loads((root / "uv.lock").read_text(encoding="utf8"))
    expected = {p["name"]: p for p in data["packages"] if p["name"] != "uv"}
    actual = {p["name"]: p for p in lock["package"]}
    if set(actual) != set(expected) | {"pact-core", "pact-workspace"}:
        raise ValueError("unexpected locked package identity")
    for name, package in expected.items():
        locked = actual[name]
        if locked["version"] != package["version"] or locked["source"] != {
            "registry": QUARANTINE.as_posix()
        }:
            raise ValueError("locked pin/source differs from reviewed set")
        artifacts = {a["filename"]: a for a in package["artifacts"]}
        wheels = locked.get("wheels", [])
        if {w["path"] for w in wheels} != set(artifacts):
            raise ValueError("locked wheel set differs from reviewed set")
        for wheel in wheels:
            artifact = artifacts[wheel["path"]]
            if (
                wheel.get("hash") != "sha256:" + artifact["sha256"]
                or wheel.get("size") != artifact["size_bytes"]
            ):
                raise ValueError("locked artifact hash/size missing or changed")
    wanted = {
        p["name"] + "==" + p["version"] + " --hash=sha256:" + p["artifacts"][0]["sha256"]
        for p in data["packages"]
        if p["build_dependency"]
    }
    constraints = set((root / "build-constraints.txt").read_text(encoding="utf8").splitlines())
    if constraints != wanted:
        raise ValueError("build dependency pin/hash closure changed")


def write_member(base: Path, name: str, content: bytes) -> None:
    path = inside(base, name)
    if path.exists():
        if path.read_bytes() != content:
            raise ValueError("prepared tool/runtime bytes were modified")
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("xb") as output:
        output.write(content)


def prepare(root: Path, data: dict, version: str) -> None:
    """Extract only selected Windows artifacts, retaining all licenses/SBOM."""
    runtime = next(
        r
        for r in data["runtimes"]
        if r["version"] == version and r["matrix_cell"].startswith("windows-")
    )
    base = root / f".bootstrap/runtimes/cpython-{version}-windows-x64"
    if not base.resolve().is_relative_to(root.resolve()):
        raise ValueError("runtime root escapes project")
    with tarfile.open(root / QUARANTINE / runtime["filename"]) as archive:
        seen: set[str] = set()
        for member in archive:
            inside(base, member.name)
            key = member.name.casefold()
            if key in seen or len(seen) >= 100000 or member.size > 128 * 1024**2:
                raise ValueError("runtime member/type/size constraint")
            seen.add(key)
            if member.isdir():
                continue
            if not member.isfile():
                raise ValueError("runtime links/special files forbidden in Windows profile")
            stream = archive.extractfile(member)
            if stream is None:
                raise ValueError("missing runtime payload")
            with stream:
                write_member(base, member.name, stream.read())
    uv = next(p for p in data["packages"] if p["name"] == "uv")
    wheel = next(a for a in uv["artifacts"] if "win_amd64" in a["filename"])
    base = root / ".bootstrap/tools/uv-0.13.0"
    if not base.resolve().is_relative_to(root.resolve()):
        raise ValueError("tool root escapes project")
    with zipfile.ZipFile(root / QUARANTINE / wheel["filename"]) as archive:
        for member in archive.infolist():
            if stat.S_ISLNK(member.external_attr >> 16):
                raise ValueError("tool archive symlink forbidden")
            write_member(base, member.filename, archive.read(member))


def environment(root: Path, version: str) -> tuple[dict[str, str], Path]:
    # Neither API credentials nor Python/uv configuration from the calling host
    # are inherited into builds/tests. These flags do not claim OS containment.
    values = {
        k: v
        for k, v in os.environ.items()
        if k.upper() in {"SYSTEMROOT", "WINDIR", "COMSPEC", "PATH", "TEMP", "TMP", "PATHEXT"}
    }
    target = root / (".venv" if version == "3.14.8" else f".venv-cp{version[:4].replace('.', '')}")
    values.update(
        UV_OFFLINE="1",
        UV_NO_CONFIG="1",
        UV_PYTHON_DOWNLOADS="never",
        UV_NO_MANAGED_PYTHON="1",
        UV_CACHE_DIR=str(root / ".bootstrap/workspace-checks/uv-cache"),
        UV_PROJECT_ENVIRONMENT=str(target),
        UV_BUILD_CONSTRAINT=str(root / "build-constraints.txt"),
        PYTHONDONTWRITEBYTECODE="1",
        PYTHONNOUSERSITE="1",
        PYTEST_DISABLE_PLUGIN_AUTOLOAD="1",
        PIP_NO_INDEX="1",
        PIP_DISABLE_PIP_VERSION_CHECK="1",
        NO_COLOR="1",
    )
    return values, target


def run(root: Path, args: list[str], env: dict[str, str], label: str) -> None:
    if additional_storage(root) > 2 * 1024**3:
        raise RuntimeError("workspace additional-storage budget exhausted")
    remaining = 3600 - (time.monotonic() - START)
    if remaining <= 0:
        raise TimeoutError("workspace executable time budget exhausted")
    result = subprocess.run(
        args,
        cwd=root,
        env=env,
        text=True,
        encoding="utf8",
        errors="replace",
        capture_output=True,
        timeout=min(300, remaining),
        check=False,
    )
    folder = root / ".bootstrap/workspace-checks"
    folder.mkdir(parents=True, exist_ok=True)
    (folder / (label + ".json")).write_text(
        json.dumps(
            {
                "argv": args,
                "exit_code": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr,
            },
            indent=2,
        )
        + "\n",
        encoding="utf8",
    )
    print(result.stdout, end="")
    print(result.stderr, end="", file=sys.stderr)
    if result.returncode:
        raise RuntimeError(f"workspace command failed: {label} (exit {result.returncode})")
    if additional_storage(root) > 2 * 1024**3:
        raise RuntimeError("workspace additional-storage budget exhausted")


def additional_storage(root: Path) -> int:
    existing = (root / QUARANTINE).resolve()
    folders = [root / ".bootstrap", root / ".venv", root / ".venv-cp312", root / ".venv-cp313"]
    return sum(
        path.stat().st_size
        for folder in folders
        if folder.exists()
        for path in folder.rglob("*")
        if path.is_file() and not path.resolve().is_relative_to(existing)
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("prepare", "sync", "check", "build"))
    parser.add_argument("--python", choices=PYTHONS, default="3.14.8")
    args = parser.parse_args()
    if sys.platform != "win32":
        parser.error("this approved executable profile is Windows only; Linux remains gated")
    data = manifest(ROOT)
    validate_lock(ROOT, data)
    prepare(ROOT, data, args.python)
    if args.action == "prepare":
        return 0
    env, target = environment(ROOT, args.python)
    uv = str(ROOT / UV_RELATIVE)
    interpreter = str(
        ROOT / f".bootstrap/runtimes/cpython-{args.python}-windows-x64/python/python.exe"
    )
    common = [
        "--offline",
        "--no-index",
        "--find-links",
        QUARANTINE.as_posix(),
        "--no-python-downloads",
        "--python",
        interpreter,
    ]
    if args.action == "sync":
        run(ROOT, [uv, "lock", "--check", *common], env, "lock-check-" + args.python)
        command = [
            uv,
            "sync",
            "--locked",
            "--no-editable",
            "--all-packages",
            "--group",
            "dev",
            "--require-build-hashes",
            "--reinstall-package",
            "pact-core",
            *common,
        ]
        for package in data["packages"]:
            if package["name"] != "uv":
                command.extend(["--no-build-package", package["name"]])
        run(ROOT, command, env, "sync-" + args.python)
    elif args.action == "build":
        run(
            ROOT,
            [
                uv,
                "build",
                "--package",
                "pact-core",
                "--build-constraints",
                str(ROOT / "build-constraints.txt"),
                "--require-build-hashes",
                *common,
            ],
            env,
            "build-" + args.python,
        )
    else:
        python = str(target / "Scripts/python.exe")
        run(ROOT, [python, "-I", "-B", str(ROOT / "tools/smoke.py")], env, "smoke-" + args.python)
        run(ROOT, [python, "-I", "-B", "-m", "pytest", "-q"], env, "pytest-" + args.python)
        run(
            ROOT,
            [python, "-I", "-B", "-m", "mypy", "--config-file", "pyproject.toml"],
            env,
            "mypy-" + args.python,
        )
        run(ROOT, [str(target / "Scripts/ruff.exe"), "check", "."], env, "ruff-" + args.python)
        run(
            ROOT,
            [str(target / "Scripts/ruff.exe"), "format", "--check", "tools", "tests"],
            env,
            "format-" + args.python,
        )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (ValueError, OSError, RuntimeError) as failure:
        print(str(failure), file=sys.stderr)
        raise SystemExit(1) from None
