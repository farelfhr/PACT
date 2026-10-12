"""M0-07 portable-bootstrap models and disabled CI; all data synthetic/offline."""

import hashlib
import importlib.util
import io
from pathlib import Path
import sys
import tarfile
from types import SimpleNamespace

import pytest

ROOT = Path(__file__).resolve().parents[1]


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


workspace = load("workspace_ci_tests", ROOT / "tools/workspace.py")
ci = load("ci_preparation_tests", ROOT / "tools/ci.py")


def member(name, *, kind=tarfile.REGTYPE, link="", mode=0o644, size=0):
    result = tarfile.TarInfo(name)
    result.type, result.linkname, result.mode, result.size = kind, link, mode, size
    return result


@pytest.mark.parametrize(
    "system,machine,wanted", [("win32", "AMD64", "windows"), ("linux", "x86_64", "linux")]
)
def test_supported_platform_layout(tmp_path, system, machine, wanted):
    assert workspace.platform_name(system, machine) == wanted
    uv, python, scripts = workspace.layout(tmp_path, "3.14.8", wanted)
    assert uv.is_relative_to(tmp_path) and python.is_relative_to(tmp_path)
    assert scripts == ("Scripts" if wanted == "windows" else "bin")
    assert python.name == ("python.exe" if wanted == "windows" else "python3")


@pytest.mark.parametrize(
    "system,machine",
    [("linux", "aarch64"), ("darwin", "x86_64"), ("win32", "ARM64"), ("linux", "AMD64")],
)
def test_unknown_platform_has_no_fallback(system, machine):
    with pytest.raises(ValueError, match="unsupported"):
        workspace.platform_name(system, machine)


@pytest.mark.parametrize("version", ["3.14.4", "3.15.0", "../../python", ""])
def test_unreviewed_patch_rejected(tmp_path, version):
    with pytest.raises(ValueError, match="layout"):
        workspace.layout(tmp_path, version, "linux")


def test_case_distinct_linux_plan_and_windows_collision():
    values = [member("python/A"), member("python/a")]
    assert workspace.runtime_plan(values, windows=False) == values
    with pytest.raises(ValueError):
        workspace.runtime_plan(values, windows=True)


def test_bounded_internal_symlink_plan():
    values = [
        member("python/bin/python3", mode=0o755),
        member("python/bin/python", kind=tarfile.SYMTYPE, link="python3"),
    ]
    assert workspace.runtime_plan(values, windows=False) == values
    with pytest.raises(ValueError, match="links/special"):
        workspace.runtime_plan(values, windows=True)


@pytest.mark.parametrize(
    "name,kind,link,mode",
    [
        ("../escape", tarfile.REGTYPE, "", 0o644),
        ("python/link", tarfile.SYMTYPE, "/etc/passwd", 0o644),
        ("python/link", tarfile.SYMTYPE, "../outside", 0o644),
        ("python/link", tarfile.SYMTYPE, "missing", 0o644),
        ("python/link", tarfile.LNKTYPE, "python/file", 0o644),
        ("python/device", tarfile.CHRTYPE, "", 0o644),
        ("python/fifo", tarfile.FIFOTYPE, "", 0o644),
        ("python/file", tarfile.REGTYPE, "", 0o4755),
        ("other/file", tarfile.REGTYPE, "", 0o644),
    ],
)
def test_unsafe_archive_plan_rejected(name, kind, link, mode):
    with pytest.raises(ValueError):
        workspace.runtime_plan([member(name, kind=kind, link=link, mode=mode)], windows=False)


def test_symlink_cycle_and_nested_link_rejected():
    values = [
        member("python/a", kind=tarfile.SYMTYPE, link="b"),
        member("python/b", kind=tarfile.SYMTYPE, link="a"),
    ]
    with pytest.raises(ValueError, match="cyclic"):
        workspace.runtime_plan(values, windows=False)
    values = [
        member("python/a", kind=tarfile.SYMTYPE, link="b"),
        member("python/b", kind=tarfile.DIRTYPE),
        member("python/a/file"),
    ]
    with pytest.raises(ValueError, match="parent"):
        workspace.runtime_plan(values, windows=False)


def test_expansion_budget_rejected_without_reading_payload():
    values = [member(f"python/{i}", size=128 * 1024**2) for i in range(5)]
    with pytest.raises(ValueError, match="expanded"):
        workspace.runtime_plan(values, windows=False)


def test_no_partial_writes_before_full_archive_validation(tmp_path):
    stream = io.BytesIO()
    with tarfile.open(fileobj=stream, mode="w") as archive:
        archive.addfile(member("python/safe"))
        archive.addfile(member("../escape"))
    stream.seek(0)
    with tarfile.open(fileobj=stream) as archive, pytest.raises(ValueError):
        workspace.extract_runtime(archive, tmp_path, windows=True)
    assert list(tmp_path.iterdir()) == []


def test_linux_file_mode_and_link_creation_mocked(tmp_path, monkeypatch):
    """Mode/link calls verified, not Windows symlink privilege or Linux execution."""
    calls = []
    monkeypatch.setattr(workspace, "require_case_sensitive", lambda base: None)
    monkeypatch.setattr(Path, "chmod", lambda path, mode: calls.append(("mode", path.name, mode)))
    monkeypatch.setattr(
        Path, "symlink_to", lambda path, target: calls.append(("link", path.name, target))
    )
    stream = io.BytesIO()
    with tarfile.open(fileobj=stream, mode="w") as archive:
        archive.addfile(member("python/bin/python3", mode=0o755))
        archive.addfile(member("python/bin/python", kind=tarfile.SYMTYPE, link="python3"))
    stream.seek(0)
    with tarfile.open(fileobj=stream) as archive:
        workspace.extract_runtime(archive, tmp_path, windows=False)
    assert calls == [("mode", "python3", 0o755), ("link", "python", "python3")]


def test_linux_preparation_disabled_without_cli_or_environment_bypass(tmp_path, monkeypatch):
    monkeypatch.setenv("PACT_LINUX_APPROVED", "true")
    with pytest.raises(ValueError, match="not authorized"):
        workspace.prepare(tmp_path, {}, "3.14.8", "linux")
    assert list(tmp_path.iterdir()) == []


@pytest.mark.parametrize("name", ["../escape", "/absolute", "C:/drive", "a\\b", "a\0x"])
def test_linux_path_guards(tmp_path, name):
    with pytest.raises(ValueError):
        workspace.inside(tmp_path, name, windows=False)


def test_linux_case_probe_cannot_use_windows_host(tmp_path):
    if sys.platform == "win32":
        with pytest.raises(ValueError, match="Linux filesystem"):
            workspace.require_case_sensitive(tmp_path)
    else:
        workspace.require_case_sensitive(tmp_path)
    assert list(tmp_path.iterdir()) == []


def test_build_environment_excludes_host_credentials_and_provider_configuration(
    tmp_path, monkeypatch
):
    for key in ["OPENAI_API_KEY", "GH_TOKEN", "HTTP_PROXY", "PYTHONPATH", "UV_INDEX_URL"]:
        monkeypatch.setenv(key, "synthetic-do-not-inherit")
    env, path = workspace.environment(tmp_path, "3.14.8")
    assert path == tmp_path / ".venv"
    assert not any("synthetic-do-not-inherit" in value for value in env.values())
    assert env["UV_OFFLINE"] == "1" and env["PIP_NO_INDEX"] == "1"


def test_each_failed_command_preserves_its_own_log(tmp_path, monkeypatch):
    ticks = iter([11, 12])
    monkeypatch.setattr(workspace, "additional_storage", lambda root: 0)
    monkeypatch.setattr(workspace.time, "time_ns", lambda: next(ticks))
    monkeypatch.setattr(
        workspace.subprocess,
        "run",
        lambda *args, **kwargs: SimpleNamespace(
            returncode=2, stdout="synthetic failure", stderr=""
        ),
    )
    for _ in range(2):
        with pytest.raises(RuntimeError, match="exit 2"):
            workspace.run(tmp_path, ["synthetic-no-execution"], {}, "negative")
    records = list((tmp_path / ".bootstrap/workspace-checks").glob("negative-*.json"))
    assert len(records) == 2
    assert all('"exit_code": 2' in path.read_text() for path in records)


@pytest.mark.parametrize("private", [1, "true", None, False])
def test_private_flag_requires_literal_boolean(private):
    sha = "a" * 40
    event = {
        "name": "push",
        "ref": ci.BRANCH,
        "after": sha,
        "repository": {"full_name": ci.REPOSITORY, "private": private},
    }
    with pytest.raises(ValueError):
        ci.validate_event(event, sha)


def test_unexpected_initial_url_does_not_call_receiver():
    bad = ci.Artifact("file", "https://attacker.invalid/file", "0" * 64, 1)
    with pytest.raises(ValueError, match="unreviewed"):
        ci.inspect_response(bad, lambda *args: pytest.fail("must not receive"))


def test_midstream_cancel_and_oversized_chunk():
    canceled = iter([False, False, True])
    with pytest.raises(ValueError, match="canceled"):
        ci.inspect_response(
            artifact(),
            lambda *args: ci.Response(200, [b"synthetic"]),
            canceled=lambda: next(canceled),
        )
    with pytest.raises(ValueError, match="chunk bound"):
        ci.inspect_response(artifact(), lambda *args: ci.Response(200, [b"x" * (1024**2 + 1)]))


def test_redirect_query_and_response_body_never_enter_error_message():
    secret = "synthetic-private-query"
    responses = iter(
        [
            ci.Response(
                302, redirect="https://release-assets.githubusercontent.com/pinned?token=" + secret
            ),
            ci.Response(500, [secret.encode()]),
        ]
    )
    with pytest.raises(ValueError) as failure:
        ci.inspect_response(artifact(github=True), lambda *args: next(responses))
    assert secret not in str(failure.value)


def test_source_event_metadata_is_not_remote_authority(monkeypatch):
    sha = "a" * 40
    event = {
        "name": "push",
        "ref": ci.BRANCH,
        "after": sha,
        "repository": {"full_name": ci.REPOSITORY, "private": True},
    }
    ci.validate_event(event, sha)
    monkeypatch.setenv("PACT_CI_APPROVED", "true")
    with pytest.raises(ValueError, match="REMOTE_CI_DISABLED"):
        ci.require_remote_grant()


@pytest.mark.parametrize(
    "field,value",
    [
        ("name", "pull_request_target"),
        ("ref", "refs/heads/main"),
        ("after", "b" * 40),
        ("repository", {"full_name": ci.REPOSITORY, "private": False}),
        ("approved", True),
    ],
)
def test_wrong_or_forged_ci_metadata_rejected(field, value):
    sha = "a" * 40
    event = {
        "name": "push",
        "ref": ci.BRANCH,
        "after": sha,
        "repository": {"full_name": ci.REPOSITORY, "private": True},
    }
    event[field] = value
    with pytest.raises(ValueError):
        ci.validate_event(event, sha)


def artifact(payload=b"synthetic", github=False):
    url = (
        "https://github.com/astral-sh/example/releases/download/pin/file"
        if github
        else "https://files.pythonhosted.org/packages/pinned/file"
    )
    return ci.Artifact("file", url, hashlib.sha256(payload).hexdigest(), len(payload))


def test_fake_response_hash_and_no_credentials():
    calls = []

    def receive(url, timeout):
        calls.append((url, timeout))
        return ci.Response(200, [b"synthetic"])

    assert ci.inspect_response(artifact(), receive) == (b"synthetic", 0)
    assert calls == [(artifact().url, 10)]


def test_fake_github_redirect():
    responses = iter(
        [
            ci.Response(
                302,
                redirect="https://release-assets.githubusercontent.com/pinned?signature=synthetic",
            ),
            ci.Response(200, [b"synthetic"]),
        ]
    )
    assert ci.inspect_response(artifact(github=True), lambda *args: next(responses)) == (
        b"synthetic",
        1,
    )


@pytest.mark.parametrize(
    "url",
    [
        "http://release-assets.githubusercontent.com/file",
        "https://attacker.invalid/file",
        "https://release-assets.githubusercontent.com.attacker.invalid/file",
        "https://user:password@release-assets.githubusercontent.com/file",
        "https://release-assets.githubusercontent.com:444/file",
        "https://release-assets.githubusercontent.com/file#fragment",
        "https://release-assets.githubusercontent.com/file\r\nAuthorization: secret",
    ],
)
def test_redirect_escape_blocked_before_second_request(url):
    calls = []

    def receive(destination, timeout):
        calls.append(destination)
        return ci.Response(302, redirect=url)

    with pytest.raises(ValueError):
        ci.inspect_response(artifact(github=True), receive)
    assert len(calls) == 1


@pytest.mark.parametrize(
    "response",
    [
        ci.Response(500),
        ci.Response(200, [b"wrong"]),
        ci.Response(200, [b"synthetic-extra"]),
        ci.Response(200, [b""]),
        ci.Response(200, ["not bytes"]),
        ci.Response(200, [b"synthetic"], redirect="https://attacker.invalid"),
    ],
)
def test_failed_bad_or_partial_response_never_succeeds(response):
    with pytest.raises(ValueError):
        ci.inspect_response(artifact(), lambda *args: response)


def test_redirect_and_cancel_time_budgets():
    calls = []

    def receive(url, timeout):
        calls.append(url)
        return ci.Response(302, redirect="https://objects.githubusercontent.com/next")

    with pytest.raises(ValueError, match="redirect budget"):
        ci.inspect_response(artifact(github=True), receive)
    assert len(calls) == 4
    with pytest.raises(ValueError, match="canceled"):
        ci.inspect_response(
            artifact(), lambda *args: pytest.fail("no request"), canceled=lambda: True
        )
    clock = iter([0, 60])
    with pytest.raises(ValueError, match="timeout"):
        ci.inspect_response(
            artifact(), lambda *args: pytest.fail("no request"), clock=lambda: next(clock)
        )


def test_reviewed_artifact_set_and_disabled_workflow():
    values = ci.artifacts(ROOT)
    assert len(values) == 36 and sum(a.size_bytes for a in values) == 314881608
    workflow = (ROOT / ".github/workflows/baseline.yml").read_text()
    assert "if: ${{ false }}" in workflow and ci.CHECKOUT in workflow
    assert "persist-credentials: false" in workflow
    assert "continue-on-error" not in workflow
    assert "max-parallel: 1" in workflow
    assert "pull_request_target:" not in workflow
