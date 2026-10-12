"""Disabled development-CI preparation, not Security Contract approval authority.

Acquisition is modeled through injected responses only. No HTTP client or CLI
activation switch exists here; a future exact remote grant must be implemented
and reviewed before any GitHub or dependency request.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
import re
import time
from typing import Callable, Iterable
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_HASH = "8fedff4be21abac355b8b9251d55608f75c7e2864bb6e7676c53c00cf32deefe"
CHECKOUT = "d23441a48e516b6c34aea4fa41551a30e30af803"
REMOTE_ENABLED = False
BRANCH = "refs/heads/codex/m0-07-ci"
REPOSITORY = "farelfhr/PACT"
ARTIFACT_TOTAL = 314881608
CDN_HOSTS = {"release-assets.githubusercontent.com", "objects.githubusercontent.com"}


@dataclass(frozen=True)
class Artifact:
    filename: str
    url: str
    sha256: str
    size_bytes: int


@dataclass(frozen=True)
class Response:
    status: int
    chunks: Iterable[bytes] = ()
    redirect: str | None = None


def artifacts(root: Path) -> tuple[Artifact, ...]:
    raw = (root / "docs/bootstrap-artifacts.json").read_bytes()
    if hashlib.sha256(raw).hexdigest() != MANIFEST_HASH:
        raise ValueError("reviewed manifest changed")
    data = json.loads(raw)
    values = [a for p in data["packages"] for a in p["artifacts"]] + data["runtimes"]
    result = tuple(Artifact(a["filename"], a["url"], a["sha256"], a["size_bytes"]) for a in values)
    if len(result) != 36 or sum(a.size_bytes for a in result) != ARTIFACT_TOTAL:
        raise ValueError("artifact set changed")
    return result


def destination(url: str, artifact: Artifact, *, initial: bool) -> None:
    parsed = urlsplit(url)
    if (
        parsed.scheme != "https"
        or parsed.username is not None
        or parsed.password is not None
        or parsed.port not in (None, 443)
        or parsed.fragment
        or any(c in url for c in "\r\n\\\0")
    ):
        raise ValueError("unsafe artifact destination")
    if initial:
        if url != artifact.url or parsed.hostname not in {"files.pythonhosted.org", "github.com"}:
            raise ValueError("unreviewed artifact URL")
        if parsed.query:
            raise ValueError("unexpected initial URL query")
    elif parsed.hostname not in CDN_HOSTS or urlsplit(artifact.url).hostname != "github.com":
        raise ValueError("unapproved artifact redirect")


def inspect_response(
    artifact: Artifact,
    receive: Callable[[str, int], Response],
    *,
    clock: Callable[[], float] = time.monotonic,
    canceled: Callable[[], bool] = lambda: False,
) -> tuple[bytes, int]:
    """Offline conformance model; receive must not be mistaken for a live client.

    A future client must disable proxies/cookies/auth and automatic redirects,
    enforce bounded reads/timeouts, and wire cancellation before this model is
    used for actual acquisition. URLs/chunks never enter diagnostics.
    """
    started = clock()
    url = artifact.url
    hops = 0
    total = 0
    payload = bytearray()
    hasher = hashlib.sha256()

    def check_budget() -> None:
        if canceled():
            raise ValueError("acquisition canceled")
        if clock() - started >= 60:
            raise ValueError("artifact acquisition timeout")

    while True:
        check_budget()
        destination(url, artifact, initial=hops == 0)
        response = receive(url, 10)  # Fixed seconds; no auth/credential arguments.
        check_budget()
        if response.status in {301, 302, 303, 307, 308}:
            if response.redirect is None or hops >= 3:
                raise ValueError("artifact redirect budget exhausted")
            # Do not consume redirect bodies; only bounded redirect metadata is used.
            url = response.redirect
            hops += 1
            continue
        if response.status != 200 or response.redirect is not None:
            raise ValueError("artifact response failed")
        for chunk in response.chunks:
            check_budget()
            if type(chunk) is not bytes or len(chunk) > 1024 * 1024:
                raise ValueError("artifact chunk bound violated")
            total += len(chunk)
            if total > artifact.size_bytes:
                raise ValueError("artifact response size exceeded")
            payload.extend(chunk)
            hasher.update(chunk)
        if total != artifact.size_bytes or hasher.hexdigest() != artifact.sha256:
            raise ValueError("artifact response hash/length mismatch")
        return bytes(payload), hops


def validate_event(event: dict, approved_sha: str) -> None:
    """Validate metadata only; input JSON is not an authenticated owner grant."""
    if type(approved_sha) is not str or not re.fullmatch(r"[0-9a-f]{40}", approved_sha):
        raise ValueError("missing exact source SHA")
    if type(event) is not dict or type(event.get("repository")) is not dict:
        raise ValueError("invalid CI event schema")
    if (
        event.get("name") != "push"
        or event.get("ref") != BRANCH
        or event.get("after") != approved_sha
        or event.get("repository") != {"full_name": REPOSITORY, "private": True}
        or event["repository"].get("private") is not True
        or set(event) != {"name", "ref", "after", "repository"}
    ):
        raise ValueError("CI repository/ref/source metadata mismatch")


def require_remote_grant() -> None:
    # Intentionally independent of event JSON, Markdown, env vars or CLI flags.
    if not REMOTE_ENABLED:
        raise ValueError("REMOTE_CI_DISABLED: owner remote grant and verified controls absent")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("inventory", "preflight", "acquire"))
    args = parser.parse_args()
    if args.action != "inventory":
        require_remote_grant()
        raise ValueError("live preflight/acquisition adapter not implemented")
    values = artifacts(ROOT)
    print(
        json.dumps(
            {
                "status": "DISABLED_NOT_RUN",
                "checkout": CHECKOUT,
                "artifact_count": len(values),
                "artifact_bytes_per_cell": sum(a.size_bytes for a in values),
                "matrix_cells": 6,
                "live_client": "NOT_IMPLEMENTED",
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (ValueError, OSError) as failure:
        print(str(failure))
        raise SystemExit(1) from None
