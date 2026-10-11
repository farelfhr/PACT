"""M1-05 provisional parser checks; mocks confer no fixture/target approval."""

from copy import deepcopy
from dataclasses import FrozenInstanceError, replace
import json
from pathlib import Path
import random
import re
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest

PACKAGE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PACKAGE))

from pact_core.domain import (Actor, ActorId, DomainCatalog, Resource, ResourceId,
                              ResourceTypeId, RoleId, Tenant, TenantId,
                              contract_digest, parse_contract)
from pact_core.scenarios import (DeclaredRoute, ScenarioDeclarations,
                                 ScenarioValidationError, parse_scenario,
                                 scenario_json_schema)

FIXTURES = Path(__file__).parent / "fixtures/scenarios"


def declarations():
    body = parse_contract((Path(__file__).parent / "fixtures/contracts/valid-v1.json").read_bytes())
    a, b = ActorId("seller-a"), ActorId("seller-b")
    ta, tb = TenantId("tenant-a"), TenantId("tenant-b")
    catalog = DomainCatalog(body.roles, body.resource_types, (Tenant(ta), Tenant(tb)),
        (Actor(a, ta, (RoleId("seller"),), (ta,)), Actor(b, tb, (RoleId("seller"),), (tb,))),
        (Resource(ResourceId("order-a"), ta, ResourceTypeId("order"), a, ()),
         Resource(ResourceId("order-b"), tb, ResourceTypeId("order"), b, ())))
    return ScenarioDeclarations("mock-marketplace-v1", body, catalog,
                                (DeclaredRoute("order-read", ("orders",), ResourceTypeId("order")),))


def example():
    return json.loads((FIXTURES / "valid-read-v1.json").read_text(encoding="utf-8"))


def parse(data):
    return parse_scenario(json.dumps(data), declarations())


class ScenarioTests(unittest.TestCase):
    def test_example_round_trip_own_and_cross_owner_data_only(self):
        for name in ("valid-read-v1.json", "valid-deny-v1.json"):
            with self.subTest(fixture=name):
                value = json.loads((FIXTURES / name).read_text(encoding="utf-8"))
                scenario = parse(value)
                self.assertEqual(scenario.to_mapping(), value)
                self.assertEqual(parse(scenario.to_mapping()), scenario)
                self.assertFalse(scenario.is_authoritative)
                self.assertFalse(declarations().is_authoritative)
                self.assertEqual(scenario.steps[1].method.value, "GET")

    def test_immutable_detached_model_and_catalog(self):
        scenario = parse(example())
        with self.assertRaises(FrozenInstanceError):
            scenario.scenario_id = "changed"
        with self.assertRaises(FrozenInstanceError):
            scenario.steps[1].route.resource_ref = ResourceId("order-b")
        detached = scenario.to_mapping()
        detached["steps"][0]["actors"].clear()
        self.assertEqual(len(scenario.steps[0].actors), 2)
        with self.assertRaises(ScenarioValidationError):
            replace(scenario, steps=list(scenario.steps))
        with self.assertRaises(ScenarioValidationError):
            replace(declarations(), routes=list(declarations().routes))

    def test_schema_artifact_and_local_refs(self):
        schema = scenario_json_schema()
        self.assertEqual(json.loads((PACKAGE / "schemas/scenario-1.0.schema.json").read_bytes()), schema)
        self.assertEqual(schema["properties"]["steps"]["maxItems"], 32)
        def walk(node):
            if isinstance(node, dict):
                if "$ref" in node:
                    self.assertTrue(node["$ref"].startswith("#/$defs/"))
                    self.assertIn(node["$ref"].split("/")[-1], schema["$defs"])
                if node.get("type") == "object":
                    self.assertFalse(node["additionalProperties"])
                    self.assertEqual(set(node["required"]), set(node["properties"]))
                for value in node.values():
                    walk(value)
            elif isinstance(node, list):
                for value in node:
                    walk(value)
        walk(schema)
        # JSON Schema regex '$' alone can match before a final newline.
        for bad in ("seller\n", "seller\r", "seller/other", "seller%2f", "seller\u00e9"):
            self.assertIsNotNone(re.search(schema["$defs"]["identifier"]["not"]["pattern"], bad))
        schema["properties"].clear()
        self.assertIn("steps", scenario_json_schema()["properties"])

    def test_every_operation_missing_or_extra_field(self):
        for index in range(3):
            original = example()["steps"][index]
            for key in original:
                data = example()
                del data["steps"][index][key]
                with self.subTest(step=index, missing=key), self.assertRaises(ScenarioValidationError):
                    parse(data)
            for key in ("command", "python", "url", "headers", "token", "approved", "target"):
                data = example()
                data["steps"][index][key] = "untrusted"
                with self.subTest(step=index, extra=key), self.assertRaises(ScenarioValidationError):
                    parse(data)

    def test_unknown_operations_methods_and_versions(self):
        for value in ("shell", "python", "fixture.exec", "http.download", "eval", "", 1, None):
            data = example()
            data["steps"][1]["operation"] = value
            with self.subTest(operation=value), self.assertRaises(ScenarioValidationError):
                parse(data)
        for value in ("POST", "CONNECT", "get", "GET /", 1):
            data = example()
            data["steps"][1]["method"] = value
            with self.subTest(method=value), self.assertRaises(ScenarioValidationError):
                parse(data)
        for value in ("2.0", "1.1", 1, True):
            data = example()
            data["schema_version"] = value
            with self.subTest(version=value), self.assertRaises(ScenarioValidationError):
                parse(data)

    def test_privileged_and_unexpected_fields_at_all_boundaries(self):
        paths = [(), ("contract_ref",), ("steps", 1, "route"),
                 ("steps", 1, "assertions", 0), ("steps", 1, "assertions", 1)]
        for path in paths:
            for key in ("status", "reviewer", "APPROVED", "approved", "target_url", "headers", "command", "credentials"):
                data = example()
                node = data
                for part in path:
                    node = node[part]
                node[key] = "untrusted"
                with self.subTest(path=path, key=key), self.assertRaises(ScenarioValidationError):
                    parse(data)
            data = example()
            node = data
            for part in path:
                node = node[part]
            for key in list(node):
                changed = deepcopy(data)
                child = changed
                for part in path:
                    child = child[part]
                del child[key]
                with self.subTest(path=path, missing=key), self.assertRaises(ScenarioValidationError):
                    parse(changed)

    def test_undeclared_refs_and_wrong_contract_binding(self):
        mutations = [(("fixture_adapter",), "other-adapter"),
                     (("contract_ref", "contract_id"), "other-policy"),
                     (("contract_ref", "project_ref"), "other-project"),
                     (("contract_ref", "version"), 2),
                     (("contract_ref", "digest"), "0" * 64),
                     (("steps", 0, "actors", 0), "unknown-actor"),
                     (("steps", 0, "resources", 0), "unknown-resource"),
                     (("steps", 1, "as_actor"), "unknown-actor"),
                     (("steps", 1, "route", "route_ref"), "unknown-route"),
                     (("steps", 1, "route", "resource_ref"), "unknown-resource"),
                     (("steps", 1, "expected_rule"), "unknown-rule")]
        for path, value in mutations:
            data = example()
            node = data
            for part in path[:-1]:
                node = node[part]
            node[path[-1]] = value
            with self.subTest(path=path), self.assertRaises(ScenarioValidationError):
                parse(data)
        data = example()
        data["steps"][0]["actors"] = ["seller-b"]
        with self.assertRaises(ScenarioValidationError):
            parse(data)
        data = example()
        data["steps"][0]["resources"] = ["order-b"]
        with self.assertRaises(ScenarioValidationError):
            parse(data)

    def test_assertions_cannot_override_rule_profile_or_resource(self):
        for field, value in (("expected", "DENY"), ("profile", "object-read-deny-403-404-v1"),
                             ("profile", "custom-profile"), ("kind", "python")):
            data = example()
            data["steps"][1]["assertions"][0][field] = value
            with self.subTest(field=field, value=value), self.assertRaises(ScenarioValidationError):
                parse(data)
        for values in ([], example()["steps"][1]["assertions"][:1],
                       example()["steps"][1]["assertions"] * 2,
                       list(reversed(example()["steps"][1]["assertions"]))):
            data = example()
            data["steps"][1]["assertions"] = values
            with self.subTest(assertions=values), self.assertRaises(ScenarioValidationError):
                parse(data)
        data = example()
        data["steps"][1]["assertions"][1]["resource_ref"] = "order-b"
        with self.assertRaises(ScenarioValidationError):
            parse(data)
        deny = json.loads((FIXTURES / "valid-deny-v1.json").read_bytes())
        for index in (1, 2):
            data = deepcopy(deny)
            del data["steps"][1]["assertions"][index]
            with self.subTest(denial_assertion=index), self.assertRaises(ScenarioValidationError):
                parse(data)

    def test_stage_order_unique_steps_and_setup_refs(self):
        base = example()["steps"]
        for steps in ([], base[:2], base[1:], base[::-1], base + base,
                      [base[0], base[0], base[1], base[2]], [base[0], base[2], base[1]]):
            data = example()
            data["steps"] = deepcopy(steps)
            with self.subTest(steps=steps), self.assertRaises(ScenarioValidationError):
                parse(data)
        data = example()
        data["steps"][1]["id"] = "setup"
        with self.assertRaises(ScenarioValidationError):
            parse(data)
        for key in ("actors", "resources"):
            data = example()
            data["steps"][0][key] *= 2
            with self.assertRaises(ScenarioValidationError):
                parse(data)

    def test_steps_identifier_and_input_boundaries(self):
        for count in (1, 30):
            data = example()
            request = data["steps"][1]
            data["steps"] = [data["steps"][0]] + [dict(deepcopy(request), id=f"read-{i}")
                                                        for i in range(count)] + [data["steps"][2]]
            self.assertEqual(len(parse(data).steps), count + 2)
            if count == 30:
                data["steps"].insert(1, dict(deepcopy(request), id="one-too-many"))
                with self.assertRaises(ScenarioValidationError):
                    parse(data)
        data = example()
        data["scenario_id"] = "a" * 96
        self.assertEqual(parse(data).scenario_id, "a" * 96)
        data["scenario_id"] += "a"
        with self.assertRaises(ScenarioValidationError):
            parse(data)
        raw = json.dumps(example())
        self.assertEqual(parse_scenario(raw + " " * (65536 - len(raw)), declarations()), parse(example()))
        with self.assertRaises(ScenarioValidationError) as caught:
            parse_scenario(raw + " " * (65537 - len(raw)), declarations())
        self.assertEqual(caught.exception.code, "INPUT_SIZE")
        for depth in (16, 17, 5000):
            raw = "[" * depth + "0" + "]" * depth
            with self.assertRaises(ScenarioValidationError) as caught:
                parse_scenario(raw, declarations())
            self.assertEqual(caught.exception.code, "INPUT_DEPTH" if depth > 16 else "INVALID_STRUCTURE")

    def test_decoder_wrong_scalars_duplicate_keys_and_bad_bytes(self):
        raw = json.dumps(example())
        for text in (raw.replace('"schema_version": "1.0"', '"schema_version":"1.0","schema_version":"1.0"'),
                     raw.replace('"version": 1', '"version": 1.0'),
                     raw.replace('"version": 1', '"version": 1e0'),
                     raw.replace('"version": 1', '"version": NaN'),
                     raw.replace('"version": 1', '"version": true'),
                     raw.replace('"version": 1', '"version": null'),
                     raw.replace('"version": 1', '"version": ' + '9' * 1000),
                     raw + "{}", "schema_version: 1.0", "\ufeff" + raw,
                     raw.replace("own-read", "own-\u00e9"), '"\\ud800"'):
            with self.subTest(input=text[:32]), self.assertRaises(ScenarioValidationError):
                parse_scenario(text, declarations())
        for value in (b"\xff", b"\xef\xbb\xbf" + raw.encode(), {}, None, 3):
            with self.subTest(type=type(value).__name__), self.assertRaises(ScenarioValidationError):
                parse_scenario(value, declarations())
        for key, replacement in (("id", '"id":"read","id"'),
                                 ("route_ref", '"route_ref":"order-read","route_ref"')):
            duplicate = raw.replace('"' + key + '"', replacement, 1)
            with self.subTest(duplicate=key), self.assertRaises(ScenarioValidationError) as caught:
                parse_scenario(duplicate, declarations())
            self.assertEqual(caught.exception.code, "DUPLICATE_KEY")

    def test_declared_collection_and_contract_version_boundaries(self):
        base = declarations()
        tenant = base.fixtures.tenants[0]
        actors = tuple(Actor(ActorId(f"actor-{i}"), tenant.id, (RoleId("seller"),), (tenant.id,)) for i in range(64))
        resources = tuple(Resource(ResourceId(f"resource-{i}"), tenant.id, ResourceTypeId("order"), actors[i].id, ()) for i in range(64))
        fixtures = DomainCatalog(base.fixtures.roles, base.fixtures.resource_types, (tenant,), actors, resources)
        routes = tuple(DeclaredRoute(f"route-{i}", ("orders",), ResourceTypeId("order")) for i in range(64))
        catalog = replace(base, fixtures=fixtures, routes=routes)
        data = example()
        data["steps"][0]["actors"] = [actor.id.value for actor in actors]
        data["steps"][0]["resources"] = [resource.id.value for resource in resources]
        data["steps"][1]["as_actor"] = "actor-0"
        data["steps"][1]["route"] = {"route_ref": "route-0", "resource_ref": "resource-0"}
        data["steps"][1]["assertions"][1]["resource_ref"] = "resource-0"
        self.assertEqual(len(parse_scenario(json.dumps(data), catalog).steps[0].actors), 64)
        for key in ("actors", "resources"):
            bad = deepcopy(data)
            bad["steps"][0][key].append("one-too-many")
            with self.subTest(collection=key), self.assertRaises(ScenarioValidationError):
                parse_scenario(json.dumps(bad), catalog)
        with self.assertRaises(ScenarioValidationError):
            replace(catalog, routes=routes + (DeclaredRoute("one-too-many", ("orders",), ResourceTypeId("order")),))
        for version in (1, 2147483647):
            contract = replace(base.contract, version=version)
            catalog = replace(base, contract=contract)
            value = example()
            value["contract_ref"]["version"] = version
            value["contract_ref"]["digest"] = contract_digest(contract)
            self.assertEqual(parse_scenario(json.dumps(value), catalog).contract_ref.version, version)
        for version in (0, -1, 2147483648, True, "1"):
            value = example()
            value["contract_ref"]["version"] = version
            with self.subTest(version=version), self.assertRaises(ScenarioValidationError):
                parse(value)
        viewer = replace(base.fixtures.actors[0], roles=(RoleId("viewer"),))
        wrong_roles = replace(base, fixtures=replace(base.fixtures, actors=(viewer, base.fixtures.actors[1])))
        with self.assertRaises(ScenarioValidationError):
            parse_scenario(json.dumps(example()), wrong_roles)

    def test_seeded_valid_round_trip_property_cases(self):
        rng = random.Random(105)
        allow = example()["steps"][1]
        deny = json.loads((FIXTURES / "valid-deny-v1.json").read_bytes())["steps"][1]
        for case in range(128):
            value = example()
            value["scenario_id"] = f"case-{case}"
            count = rng.randint(1, 30)
            requests = [dict(deepcopy(rng.choice((allow, deny))), id=f"request-{i}") for i in range(count)]
            value["steps"] = [value["steps"][0], *requests, value["steps"][2]]
            text = json.dumps(value, indent=rng.choice((None, 1, 2)), sort_keys=bool(rng.randrange(2)))
            typed = parse_scenario(text, declarations())
            with self.subTest(case=case):
                self.assertEqual(typed.to_mapping(), value)
                self.assertEqual(parse(typed.to_mapping()), typed)


    def test_malicious_strings_in_every_string_leaf(self):
        payloads = ["$(whoami)", "`whoami`", "a;cmd", "__import__('os').system('x')",
                    "eval('x')", "${fixtures.order_b.id}", "{{ actor.token }}", "${host}",
                    "http://127.0.0.1/", "//evil.invalid", "file:///tmp/x", "../x", "%2f",
                    "%252f", "\\host\\share", "a\r\nHost: evil", "\u202e", "\x00"]
        def paths(value, prefix=()):
            if isinstance(value, dict):
                for key, child in value.items():
                    yield from paths(child, prefix + (key,))
            elif isinstance(value, list):
                for index, child in enumerate(value):
                    yield from paths(child, prefix + (index,))
            elif isinstance(value, str):
                yield prefix
        for path in paths(example()):
            for payload in payloads:
                data = example()
                node = data
                for part in path[:-1]:
                    node = node[part]
                node[path[-1]] = payload
                with self.subTest(path=path, payload=payload), self.assertRaises(ScenarioValidationError) as caught:
                    parse(data)
                self.assertNotIn(payload, str(caught.exception))

    def test_seeded_negative_property_mutations(self):
        rng = random.Random(105)
        for index in range(512):
            data = example()
            op = "unknown-" + "".join(rng.choice("abcdefghijklmnopqrstuvwxyz") for _ in range(rng.randint(1, 60)))
            data["steps"][rng.randrange(3)]["operation"] = op
            with self.subTest(case=index), self.assertRaises(ScenarioValidationError):
                parse(data)
        for index in range(256):
            # Arbitrary malformed bytes may be rejected; none can become executable input.
            raw = bytes(rng.randrange(256) for _ in range(rng.randrange(1, 128)))
            with self.subTest(bytes=index), self.assertRaises(ScenarioValidationError):
                parse_scenario(raw, declarations())

    def test_catalog_routes_are_declarations_not_templates_or_origins(self):
        for value in ("../orders", "http://x", "//x", "${host}", "{{x}}", ".", "..", "%2f", "a/b", "a\\b", "a:b", "a?b", "a#b", ""):
            with self.subTest(segment=value), self.assertRaises(ScenarioValidationError):
                DeclaredRoute("read", (value,), ResourceTypeId("order"))
        self.assertEqual(DeclaredRoute("read", ("a" * 32,) * 8, ResourceTypeId("order")).segments[0], "a" * 32)
        for segments in ((), ("a" * 33,), ("orders",) * 9, ["orders"]):
            with self.assertRaises(ScenarioValidationError):
                DeclaredRoute("read", segments, ResourceTypeId("order"))
        with self.assertRaises(ScenarioValidationError):
            replace(declarations(), routes=declarations().routes * 2)
        data = example()
        catalog = declarations()
        wrong = replace(catalog, routes=(DeclaredRoute("order-read", ("documents",), ResourceTypeId("document")),))
        with self.assertRaises(ScenarioValidationError):
            parse_scenario(json.dumps(data), wrong)
        with self.assertRaises(ScenarioValidationError):
            parse_scenario(json.dumps(data), None)

    def test_fresh_import_and_parse_have_no_audited_side_effects(self):
        script = '''
import os, sys
sys.path.insert(0, sys.argv[1])
sys.path.insert(0, sys.argv[2])
before = dict(os.environ)
def guard(event, args):
    if event == 'open':
        mode, flags = args[1], args[2]
        writing = isinstance(mode, str) and any(c in mode for c in 'wax+')
        writing |= isinstance(flags, int) and bool(flags & (os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_TRUNC | os.O_APPEND))
        if writing: raise RuntimeError('write attempted')
    if event.startswith(('socket.', 'subprocess.', 'ctypes.')) or event in {'os.system', 'os.mkdir', 'os.remove', 'os.rename', 'os.putenv', 'os.unsetenv', 'os.chdir'}:
        raise RuntimeError('side effect attempted')
sys.addaudithook(guard)
from test_scenarios import declarations, example, parse
from pact_core.scenarios import scenario_json_schema
model = parse(example())
assert not model.is_authoritative
assert model.to_mapping() == example()
assert scenario_json_schema()['$id'] == 'urn:pact:provisional-scenario:1.0'
assert dict(os.environ) == before
print('pure scenario parse')
'''
        with TemporaryDirectory(prefix="PACT-M1-05-import-") as directory:
            result = subprocess.run([sys.executable, "-I", "-B", "-c", script, str(PACKAGE),
                                     str(Path(__file__).parent)], cwd=directory, capture_output=True,
                                    text=True, timeout=15, check=False)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(result.stdout.strip(), "pure scenario parse")
            self.assertEqual(list(Path(directory).iterdir()), [])


if __name__ == "__main__":
    unittest.main()
