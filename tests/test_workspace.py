"""M0-07 artifact, lock and installed import checks; no target/provider calls."""

import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory

import pytest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("workspace", ROOT / "tools/workspace.py")
workspace = importlib.util.module_from_spec(spec)
spec.loader.exec_module(workspace)


@pytest.mark.parametrize(
    "name",
    [
        "../escape",
        "/absolute",
        "C:/drive",
        "a\\b",
        "a/../x",
        "a\0x",
        "CON",
        "AUX.txt",
        "name.",
        "name ",
    ],
)
def test_extraction_rejects_unsafe_windows_paths(tmp_path, name):
    with pytest.raises(ValueError):
        workspace.inside(tmp_path, name)


def test_artifact_hash_failure_prevents_use(tmp_path):
    folder = tmp_path / workspace.QUARANTINE
    folder.mkdir(parents=True)
    (folder / "fake.whl").write_bytes(b"tampered")
    with pytest.raises(ValueError, match="length/hash"):
        workspace.check_artifact(
            tmp_path, {"filename": "fake.whl", "size_bytes": 8, "sha256": "0" * 64}
        )


def test_lock_requires_measured_hashes_for_every_local_wheel(tmp_path):
    data = json.loads((ROOT / "docs/bootstrap-artifacts.json").read_bytes())
    text = (ROOT / "uv.lock").read_text()
    (tmp_path / "uv.lock").write_text(text)
    (tmp_path / "build-constraints.txt").write_bytes((ROOT / "build-constraints.txt").read_bytes())
    workspace.validate_lock(tmp_path, data)
    altered = text.replace('hash = "sha256:', 'unverified_hash = "sha256:', 1)
    (tmp_path / "uv.lock").write_text(altered)
    with pytest.raises(ValueError, match="hash/size"):
        workspace.validate_lock(tmp_path, data)


def test_build_transitive_missing_hash_fails_closed(tmp_path):
    data = json.loads((ROOT / "docs/bootstrap-artifacts.json").read_bytes())
    (tmp_path / "uv.lock").write_bytes((ROOT / "uv.lock").read_bytes())
    lines = (ROOT / "build-constraints.txt").read_text().splitlines()
    (tmp_path / "build-constraints.txt").write_text("\n".join(lines[:-1]) + "\n")
    with pytest.raises(ValueError, match="closure"):
        workspace.validate_lock(tmp_path, data)


def test_installed_smoke_in_fresh_isolated_process():
    with TemporaryDirectory(prefix="PACT-workspace-smoke-") as directory:
        env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", PYTHONNOUSERSITE="1")
        result = subprocess.run(
            [sys.executable, "-I", "-B", str(ROOT / "tools/smoke.py")],
            cwd=directory,
            env=env,
            capture_output=True,
            text=True,
            timeout=30,
        )
        assert result.returncode == 0, result.stderr
        assert "approval remains unavailable" in result.stdout
        assert list(Path(directory).iterdir()) == []
