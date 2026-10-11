"""Local import/dependency checks; no assertion of runner containment."""

import ast
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest

PACKAGE = Path(__file__).resolve().parents[1]


class ImportTests(unittest.TestCase):
    def test_domain_imports_only_standard_library_and_relative_domain_modules(self):
        for path in (PACKAGE / "pact_core/domain").glob("*.py"):
            with self.subTest(module=path.name):
                tree = ast.parse(path.read_text(encoding="utf-8"))
                for node in ast.walk(tree):
                    if isinstance(node, ast.Import):
                        for alias in node.names:
                            self.assertIn(alias.name.split(".")[0], sys.stdlib_module_names)
                    elif isinstance(node, ast.ImportFrom) and node.level == 0:
                        self.assertIn(node.module.split(".")[0], sys.stdlib_module_names)
                    elif isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                        self.assertNotIn(node.func.id, {"eval", "exec", "__import__", "open"})

    def test_fresh_import_and_construction_have_no_audited_side_effects(self):
        script = """
import os, sys
sys.path.insert(0, sys.argv[1])
before_environment = dict(os.environ)
def guard(event, args):
    if event == 'open':
        mode, flags = args[1], args[2]
        writing = isinstance(mode, str) and any(c in mode for c in 'wax+')
        writing |= isinstance(flags, int) and bool(flags & (
            os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_TRUNC | os.O_APPEND))
        if writing:
            raise RuntimeError('import attempted filesystem write')
    if event.startswith(('socket.', 'subprocess.', 'ctypes.')) or event in {
        'os.system', 'os.mkdir', 'os.remove', 'os.rmdir', 'os.rename', 'os.link',
        'os.symlink', 'os.chmod', 'os.chown', 'os.truncate', 'os.putenv',
        'os.unsetenv', 'os.chdir', 'os.fork', 'os.exec', 'os.posix_spawn'}:
        raise RuntimeError('import attempted privileged or external side effect')
sys.addaudithook(guard)
from pact_core.domain import (Tenant, TenantId, parse_contract, canonical_bytes, contract_digest,
    import_candidate, transition_model, ContractStatus, UntrustedApprovalSnapshot,
    require_authenticated_approval, ApprovalRequiredError)
from datetime import datetime, timezone
from pact_core.domain.schema import contract_json_schema
assert Tenant(TenantId('synthetic-tenant')).id == TenantId('synthetic-tenant')
with open(sys.argv[2], 'rb') as fixture:
    body = parse_contract(fixture.read())
assert parse_contract(canonical_bytes(body)) == body
assert contract_digest(body) == '3efd267a7de481b330a8641880f3ef1e7d7e48a8f93b545913503169ea1a29ab'
assert contract_json_schema()['$id'] == 'urn:pact:contract-policy:1.0'
with open(sys.argv[2], 'rb') as fixture:
    model = import_candidate(fixture.read(), claimed_author_ref='synthetic-author')
model = transition_model(model, ContractStatus.NEEDS_REVIEW, event_id='request',
    expected_revision=0, expected_digest=model.content_digest)
claim = UntrustedApprovalSnapshot(model.body, model.content_digest, model.claimed_author_ref,
    'synthetic-reviewer', 'claimed-approval', datetime(2026, 10, 10, tzinfo=timezone.utc))
model = transition_model(model, ContractStatus.APPROVED, event_id='claimed-approval',
    expected_revision=1, expected_digest=model.content_digest, claimed_snapshot=claim)
assert not model.is_authoritative
try:
    require_authenticated_approval(model)
except ApprovalRequiredError:
    pass
else:
    raise AssertionError('untrusted model established authority')
assert dict(os.environ) == before_environment
print('pure import and construction')
"""
        with TemporaryDirectory(prefix="PACT-M1-01-import-") as directory:
            result = subprocess.run(
                [sys.executable, "-I", "-B", "-c", script, str(PACKAGE),
                 str(PACKAGE / "tests/fixtures/contracts/valid-v1.json")],
                cwd=directory, capture_output=True, text=True, timeout=15, check=False)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(result.stdout.strip(), "pure import and construction")
            self.assertEqual(list(Path(directory).iterdir()), [])


if __name__ == "__main__":
    unittest.main()
