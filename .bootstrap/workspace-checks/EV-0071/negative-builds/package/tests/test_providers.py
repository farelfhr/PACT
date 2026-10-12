"""FR-AI-001/002: offline provider conformance, not real inference or approval."""

import ast
from dataclasses import FrozenInstanceError, replace
import json
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest

PACKAGE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PACKAGE))

from pact_core.domain import ContractStatus, canonical_bytes, require_authenticated_approval, ApprovalRequiredError
from pact_core.providers import (
    CandidateDraft, ContractProvider, FakeProvider, FakeFailure, GenerationError,
    GenerationErrorCode, GenerationProvenance, GenerationRequest, ProviderValidationError,
)

FIXTURES = Path(__file__).parent / "fixtures/contracts"
CANARY = "synthetic-private-token-do-not-export"


def valid_text():
    return (FIXTURES / "valid-v1.json").read_text(encoding="utf-8")


def request():
    return GenerationRequest("synthetic-marketplace", "Synthetic seller reads its own order.")


class ProviderTests(unittest.TestCase):
    def test_valid_draft_protocol_and_repeated_offline_results(self):
        provider: ContractProvider = FakeProvider(response=valid_text())
        first = provider.generate_structured_contract(request())
        self.assertIs(type(first), CandidateDraft)
        self.assertEqual(first, provider.generate_structured_contract(request()))
        self.assertEqual(first.status, ContractStatus.DRAFT)
        self.assertFalse(first.is_authoritative)
        self.assertEqual(first.body.project_ref, request().project_ref)
        self.assertEqual(first.provenance, GenerationProvenance("fake", "offline-fixture", "m2-01-1", True))
        self.assertTrue(first.provenance.is_synthetic)
        self.assertEqual(json.loads(canonical_bytes(first.body)), json.loads(valid_text()))
        with self.assertRaises(ApprovalRequiredError):
            require_authenticated_approval(first)

    def test_invalid_output_and_ambiguous_fixture_classification(self):
        for name, code in [
            ("invalid-schema-v2.json", GenerationErrorCode.INVALID_OUTPUT),
            ("invalid-forged-approval.json", GenerationErrorCode.INVALID_OUTPUT),
            ("ambiguous-conflict-v1.json", GenerationErrorCode.NEEDS_REVIEW),
        ]:
            with self.subTest(fixture=name):
                result = FakeProvider(response=(FIXTURES / name).read_bytes()).generate_structured_contract(request())
                self.assertIs(type(result), GenerationError)
                self.assertEqual(result.code, code)
                self.assertFalse(result.is_authoritative)
                self.assertEqual(result.review_state, ContractStatus.NEEDS_REVIEW if code == GenerationErrorCode.NEEDS_REVIEW else None)

    def test_malformed_unsupported_privileged_and_oversized_output(self):
        data = json.loads(valid_text())
        unknown_relation = json.loads(valid_text())
        unknown_relation["rules"][0]["when"][0]["relation"] = "execute_python"
        values = ["{", "null", "[]", "```json\n{}\n```", b"\xff", " " * 65537,
                  '{"x":1,"x":2}', json.dumps(unknown_relation)]
        for privileged in ["status", "reviewer", "approve", "execution_scope", "provider_config"]:
            values.append(json.dumps({**data, privileged: CANARY}))
        for raw in values:
            with self.subTest(output=str(raw)[:16]):
                result = FakeProvider(response=raw).generate_structured_contract(request())
                self.assertIs(type(result), GenerationError)
                self.assertEqual(result.code, GenerationErrorCode.INVALID_OUTPUT)
                self.assertNotIn(CANARY, repr(result))
                self.assertNotIn(CANARY, result.message)

    def test_cross_project_output_is_never_a_draft(self):
        data = json.loads(valid_text())
        data["project_ref"] = "another-project"
        result = FakeProvider(response=json.dumps(data)).generate_structured_contract(request())
        self.assertEqual(result.code, GenerationErrorCode.PROJECT_MISMATCH)

    def test_simulated_transport_failure_and_timeout_without_fallback(self):
        for failure, expected in [(FakeFailure.TRANSPORT, GenerationErrorCode.TRANSPORT_FAILURE),
                                  (FakeFailure.TIMEOUT, GenerationErrorCode.TIMEOUT)]:
            with self.subTest(failure=failure):
                provider: ContractProvider = FakeProvider(failure=failure)
                result = provider.generate_structured_contract(request())
                self.assertIs(type(result), GenerationError)
                self.assertEqual(result.code, expected)
                self.assertEqual(result, provider.generate_structured_contract(request()))
                self.assertIsNone(result.review_state)

    def test_request_bounds_types_and_invalid_request_result(self):
        self.assertEqual(GenerationRequest("a" * 96, "x" * 8192).project_ref, "a" * 96)
        self.assertEqual(len(GenerationRequest("a", "\u00e9" * 4096).requirement), 4096)
        for project, requirement in [("a" * 97, "x"), ("../a", "x"), ("a\n", "x"),
                                     (False, "x"), ("a", ""), ("a", "  "), ("a", 1),
                                     ("a", "x" * 8193), ("a", "\u00e9" * 4097), ("a", "\ud800")]:
            with self.subTest(project=project, length=len(requirement) if type(requirement) is str else None):
                with self.assertRaises(ProviderValidationError):
                    GenerationRequest(project, requirement)
        for bad in [None, {}, {"project_ref": "demo-marketplace", "status": "APPROVED"}, "request"]:
            self.assertEqual(FakeProvider(response=valid_text()).generate_structured_contract(bad).code,
                             GenerationErrorCode.INVALID_REQUEST)

    def test_strict_result_fake_and_metadata_constructors(self):
        for kwargs in [{}, {"response": valid_text(), "failure": FakeFailure.TIMEOUT},
                       {"response": {}}, {"failure": "TIMEOUT"}]:
            with self.subTest(kwargs=list(kwargs)):
                with self.assertRaises(ProviderValidationError):
                    FakeProvider(**kwargs)
        for args in [("x", "y", "z", True), (CANARY + "\n", "x", "y", True),
                     (False, "x", "y", True), ("x", "y", "z", "true")]:
            if args == ("x", "y", "z", True):
                GenerationProvenance(*args)
            else:
                with self.assertRaises(ProviderValidationError):
                    GenerationProvenance(*args)
        with self.assertRaises(ProviderValidationError):
            GenerationError("TIMEOUT")
        with self.assertRaises(ProviderValidationError):
            CandidateDraft({}, GenerationProvenance("fake", "offline-fixture", "m2-01-1", True))
        with self.assertRaises(TypeError):
            GenerationRequest("project", "requirement", approved=True)

    def test_immutable_payloads_and_safe_repr_no_logging(self):
        provider = FakeProvider(response=valid_text())
        draft = provider.generate_structured_contract(request())
        for value, field, new in [(draft, "body", None), (provider, "response", CANARY),
                                  (request(), "project_ref", "other")]:
            with self.subTest(kind=type(value).__name__):
                with self.assertRaises(FrozenInstanceError):
                    setattr(value, field, new)
        with self.assertRaises(TypeError):
            replace(draft, status=ContractStatus.APPROVED)
        with self.assertLogs("pact_core.providers", level="INFO") as caught:
            # Only a test-owned message supplies an observation for assertLogs.
            import logging
            logging.getLogger("pact_core.providers").info("test-owned-marker")
            FakeProvider(response=CANARY).generate_structured_contract(GenerationRequest("project", CANARY))
        self.assertEqual(caught.output, ["INFO:pact_core.providers:test-owned-marker"])
        self.assertNotIn(CANARY, repr(GenerationRequest("project", CANARY)))
        self.assertNotIn(CANARY, repr(FakeProvider(response=CANARY)))

    def test_core_import_boundaries_and_single_protocol_method(self):
        for folder in ["pact_core/domain", "pact_core/providers"]:
            for path in (PACKAGE / folder).glob("*.py"):
                tree = ast.parse(path.read_text(encoding="utf-8"))
                for node in ast.walk(tree):
                    if isinstance(node, ast.Import):
                        for alias in node.names:
                            self.assertIn(alias.name.split(".")[0], sys.stdlib_module_names)
                    elif isinstance(node, ast.ImportFrom) and node.level == 0:
                        self.assertIn(node.module.split(".")[0], sys.stdlib_module_names)
                    elif isinstance(node, ast.ImportFrom) and folder.endswith("domain"):
                        self.assertFalse((node.module or "").startswith(("providers", "scenarios")))
                    elif isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                        self.assertNotIn(node.func.id, {"eval", "exec", "__import__", "open"})
        tree = ast.parse((PACKAGE / "pact_core/providers/port.py").read_text())
        protocol = next(n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == "ContractProvider")
        self.assertEqual([n.name for n in protocol.body if isinstance(n, ast.FunctionDef)],
                         ["generate_structured_contract"])

    def test_fresh_import_generation_no_network_sdk_or_write(self):
        script = """
import os, sys
sys.path.insert(0, sys.argv[1])
with open(sys.argv[2], 'rb') as fixture:
    raw = fixture.read()
before = dict(os.environ)
def guard(event, args):
    if event == 'open':
        mode, flags = args[1], args[2]
        if (isinstance(mode, str) and any(c in mode for c in 'wax+')) or (isinstance(flags, int) and flags & (os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_TRUNC | os.O_APPEND)):
            raise RuntimeError('provider attempted filesystem write')
    if event.startswith(('socket.', 'http.client.', 'urllib.', 'subprocess.', 'ctypes.')) or event in {'os.system', 'os.mkdir', 'os.remove', 'os.rmdir', 'os.rename', 'os.link', 'os.symlink', 'os.chmod', 'os.putenv', 'os.unsetenv', 'os.chdir', 'os.fork', 'os.exec', 'os.posix_spawn'}:
        raise RuntimeError('provider attempted external side effect')
    if event == 'import' and str(args[0]).split('.')[0] in {'openai', 'anthropic', 'google', 'httpx', 'requests', 'mcp'}:
        raise RuntimeError('provider attempted vendor/client import')
sys.addaudithook(guard)
from pact_core.providers import FakeProvider, FakeFailure, GenerationRequest, CandidateDraft, GenerationError
req = GenerationRequest('synthetic-marketplace', 'synthetic requirement')
assert type(FakeProvider(response=raw).generate_structured_contract(req)) is CandidateDraft
assert type(FakeProvider(response='invalid').generate_structured_contract(req)) is GenerationError
assert type(FakeProvider(failure=FakeFailure.TIMEOUT).generate_structured_contract(req)) is GenerationError
assert dict(os.environ) == before
print('offline provider import and generation')
"""
        with TemporaryDirectory(prefix="PACT-M2-01-import-") as directory:
            result = subprocess.run([sys.executable, "-I", "-B", "-c", script, str(PACKAGE),
                                     str(FIXTURES / "valid-v1.json")],
                                    cwd=directory, capture_output=True, text=True, timeout=15)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(result.stdout.strip(), "offline provider import and generation")
            self.assertEqual(list(Path(directory).iterdir()), [])


if __name__ == "__main__":
    unittest.main()
