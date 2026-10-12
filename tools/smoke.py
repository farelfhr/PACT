"""Installed-package smoke with observed import effects guarded, not a sandbox."""

import importlib.resources
import json
import os
from pathlib import Path
import sys


def guard(event: str, args: tuple) -> None:
    if event == "open":
        mode, flags = args[1:3]
        writing = isinstance(mode, str) and any(letter in mode for letter in "wax+")
        writing |= isinstance(flags, int) and bool(
            flags & (os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_TRUNC | os.O_APPEND)
        )
        if writing:
            raise RuntimeError("package import attempted a file write")
    if event.startswith(("socket.", "subprocess.", "ctypes.")) or event in {
        "os.system",
        "os.mkdir",
        "os.remove",
        "os.rmdir",
        "os.rename",
        "os.link",
        "os.symlink",
        "os.chmod",
        "os.chdir",
        "os.putenv",
        "os.unsetenv",
        "os.startfile",
        "os.fork",
        "os.exec",
        "os.posix_spawn",
    }:
        raise RuntimeError("package import attempted an external side effect")


def main() -> int:
    before = dict(os.environ)
    sys.addaudithook(guard)
    import pact_core
    from pact_core.domain import (
        ApprovalRequiredError,
        Tenant,
        TenantId,
        require_authenticated_approval,
    )
    from pact_core.domain.schema import contract_json_schema
    from pact_core.scenarios import scenario_json_schema
    import pact_core.providers

    assert Path(pact_core.__file__).resolve().is_relative_to(Path(sys.prefix).resolve())
    assert "site-packages" in Path(pact_core.__file__).parts
    assert Tenant(TenantId("synthetic-smoke")).id.value == "synthetic-smoke"
    resources = importlib.resources.files(pact_core)
    for name, generator in (
        ("contract-1.0.schema.json", contract_json_schema),
        ("scenario-1.0.schema.json", scenario_json_schema),
    ):
        assert json.loads(resources.joinpath("schemas", name).read_text()) == generator()
    assert resources.joinpath("py.typed").is_file()
    try:
        require_authenticated_approval({"status": "APPROVED"})
    except ApprovalRequiredError:
        pass
    else:
        raise AssertionError("untrusted state granted approval")
    assert dict(os.environ) == before
    print("installed pact-core smoke: schema resources match; approval remains unavailable")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
