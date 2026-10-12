"""FR-CON-001 / FR-INT-002: canonical candidate policy, never approval."""

from copy import deepcopy
from dataclasses import FrozenInstanceError, replace
import hashlib
from itertools import combinations, product
import json
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from pact_core.domain import (
    AmbiguousContractError, ContractBody, ContractValidationError,
    canonical_bytes, contract_digest, normalize_contract, parse_contract,
)
from pact_core.domain.schema import contract_json_schema

ROOT = Path(__file__).resolve().parents[3]
PACKAGE = Path(__file__).resolve().parents[1]
FIXTURES = Path(__file__).parent / "fixtures/contracts"
EXAMPLE = ROOT / "docs/adr/examples/0001-valid-contract.json"


def example():
    return json.loads(EXAMPLE.read_text(encoding="utf-8"))


def reversed_keys(value):
    if type(value) is dict:
        return {key: reversed_keys(value[key]) for key in reversed(value)}
    if type(value) is list:
        return [reversed_keys(item) for item in value]
    return value


class ContractTests(unittest.TestCase):
    def test_golden_digest_and_exact_canonical_bytes(self):
        raw = EXAMPLE.read_bytes()
        expected = json.dumps(example(), sort_keys=True, separators=(",", ":")).encode("utf-8")
        self.assertEqual(canonical_bytes(raw), expected)
        self.assertEqual(contract_digest(raw),
                         "3efd267a7de481b330a8641880f3ef1e7d7e48a8f93b545913503169ea1a29ab")
        self.assertEqual(contract_digest(raw), hashlib.sha256(expected).hexdigest())
        self.assertFalse(expected.startswith(b"\xef\xbb\xbf"))
        self.assertFalse(expected.endswith(b"\n"))

    def test_object_order_whitespace_and_ascii_escape_equivalence(self):
        data = reversed_keys(example())
        variations = [json.dumps(data), json.dumps(data, indent=4),
                      "\n\t" + json.dumps(data) + " \r\n",
                      json.dumps(data).replace('"seller"', '"\\u0073eller"')]
        for text in variations:
            with self.subTest(formatting=text[:24]):
                self.assertEqual(contract_digest(text), contract_digest(EXAMPLE.read_bytes()))

    def test_array_order_is_bound_even_when_rule_meaning_is_unchanged(self):
        for key in ("roles", "resource_types", "rules", "source_refs", "when"):
            with self.subTest(array=key):
                original = example()
                if key == "source_refs":
                    original[key].append("REQ-SECOND")
                changed = deepcopy(original)
                values = changed["rules"][0]["when"] if key == "when" else changed[key]
                values.reverse()
                self.assertNotEqual(contract_digest(json.dumps(original)),
                                    contract_digest(json.dumps(changed)))

    def test_different_content_is_bound(self):
        mutations = [("contract_id", "orders.other"), ("project_ref", "other-project"),
                     ("version", 2), ("source_refs", ["REQ-OTHER"]),
                     ("roles", ["seller", "viewer", "unused-role"]),
                     ("resource_types", ["order", "document", "unused-type"])]
        for key, value in mutations:
            with self.subTest(field=key):
                data = example()
                data[key] = value
                self.assertNotEqual(contract_digest(json.dumps(data)),
                                    contract_digest(EXAMPLE.read_bytes()))
        data = example()
        data["rules"][1]["assertion_profile"] = "object-read-deny-401-403-404-v1"
        self.assertNotEqual(contract_digest(json.dumps(data)), contract_digest(EXAMPLE.read_bytes()))

    def test_valid_fixtures_round_trip_without_approval_fields(self):
        for name in ("valid-v1.json", "sharing-v1.json"):
            with self.subTest(fixture=name):
                body = parse_contract((FIXTURES / name).read_bytes())
                normalized = normalize_contract(body)
                self.assertEqual(parse_contract(canonical_bytes(normalized)), normalized)
                self.assertEqual(ContractBody.from_mapping(body.to_mapping()), body)
                self.assertEqual(contract_digest(body), contract_digest(canonical_bytes(body)))
                self.assertNotIn("status", body.to_mapping())

    def test_structural_adr_cases_and_separate_ownership_ambiguity(self):
        cases = json.loads((ROOT / "docs/adr/examples/0001-cases.json").read_text())
        for case in cases["validation_cases"]:
            with self.subTest(case=case["id"]):
                data = example()
                for change in case["changes"]:
                    target = data
                    for key in change["path"][:-1]:
                        target = target[key]
                    if change.get("remove") is True:
                        del target[change["path"][-1]]
                    else:
                        target[change["path"][-1]] = deepcopy(change["value"])
                if case["expected"] == "VALID":
                    body = ContractBody.from_mapping(data)
                    if case["id"] == "V-02-owns":
                        with self.assertRaises(AmbiguousContractError):
                            normalize_contract(body)
                    else:
                        self.assertEqual(parse_contract(canonical_bytes(body)), body)
                else:
                    with self.assertRaises(ContractValidationError):
                        ContractBody.from_mapping(data)
        for case in cases["decoding_cases"]:
            with self.subTest(decoding=case["id"]), self.assertRaises(ContractValidationError):
                parse_contract(case["text"])

    def test_complete_invalid_fixtures(self):
        for name in ("invalid-forged-approval.json", "invalid-schema-v2.json"):
            with self.subTest(fixture=name):
                with self.assertRaises(ContractValidationError):
                    parse_contract((FIXTURES / name).read_bytes())
        with self.assertRaises(AmbiguousContractError):
            canonical_bytes((FIXTURES / "ambiguous-conflict-v1.json").read_bytes())

    def test_potential_overlap_rejected_without_assuming_role_exclusivity(self):
        for role, when in (("seller", example()["rules"][0]["when"]),
                           ("viewer", example()["rules"][0]["when"]),
                           ("seller", [{"relation": "owns", "subject": "actor", "object": "resource"}])):
            with self.subTest(role=role, when=when):
                data = example()
                data["rules"][1].update(actor={"role": role}, when=when)
                body = ContractBody.from_mapping(data)
                for operation in (normalize_contract, canonical_bytes, contract_digest):
                    with self.subTest(operation=operation.__name__):
                        with self.assertRaises(AmbiguousContractError) as caught:
                            operation(body)
                        self.assertEqual(caught.exception.review_state, "NEEDS_REVIEW")
                        self.assertEqual(caught.exception.code, "POSSIBLE_CONFLICT")

    def test_profile_conflict_unsatisfiable_and_disjoint_controls(self):
        data = example()
        extra = deepcopy(data["rules"][1])
        extra.update(rule_id="second-denial", assertion_profile="object-read-deny-401-403-404-v1")
        data["rules"].append(extra)
        with self.assertRaises(AmbiguousContractError):
            normalize_contract(json.dumps(data))
        data = example()
        data["rules"][0]["when"].append(data["rules"][1]["when"][0])
        with self.assertRaises(AmbiguousContractError) as caught:
            normalize_contract(json.dumps(data))
        self.assertEqual(caught.exception.code, "UNSATISFIABLE_RULE")
        data = example()
        extra = deepcopy(data["rules"][0])
        extra["rule_id"] = "agreeing-rule"
        data["rules"].append(extra)
        self.assertEqual(len(normalize_contract(json.dumps(data)).rules), 3)
        data = example()
        data["rules"][1].update(resource={"type": "document"}, when=data["rules"][0]["when"])
        self.assertEqual(len(normalize_contract(json.dumps(data)).rules), 2)

    def test_no_implicit_policy_for_uncovered_cases(self):
        data = example()
        data["rules"] = data["rules"][:1]
        body = normalize_contract(json.dumps(data))
        self.assertEqual(body.on_unmatched, "NEEDS_REVIEW")
        self.assertEqual(len(body.rules), 1)
        for value in ("ALLOW", "DENY", "first_match"):
            with self.subTest(unmatched=value):
                data["on_unmatched"] = value
                with self.assertRaises(ContractValidationError):
                    parse_contract(json.dumps(data))

    def test_conflict_detection_against_exhaustive_independent_fixture_facts(self):
        # Ownership, membership and sharing independently vary; tenant equality
        # has exactly two alternatives. Actors can hold both tested roles.
        worlds = []
        for owns, member, shared, same in product((False, True), repeat=4):
            facts = {"same_tenant" if same else "different_tenant"}
            facts.update(name for name, present in (("owns", owns), ("member_of", member),
                                                    ("shared_with", shared)) if present)
            worlds.append(facts)
        signatures = {"owns": ("actor", "resource"), "member_of": ("actor", "resource.tenant"),
                      "shared_with": ("resource", "actor"),
                      "same_tenant": ("actor.tenant", "resource.tenant"),
                      "different_tenant": ("actor.tenant", "resource.tenant")}
        conditions = [set(items) for size in range(1, 6)
                      for items in combinations(signatures, size)
                      if any(set(items) <= world for world in worlds)]
        for left, right in product(conditions, repeat=2):
            with self.subTest(allow=sorted(left), deny=sorted(right)):
                data = example()
                data["rules"][1]["actor"]["role"] = "viewer"
                for rule, names in zip(data["rules"], (left, right)):
                    rule["when"] = [{"relation": name, "subject": signatures[name][0],
                                     "object": signatures[name][1]} for name in sorted(names)]
                overlaps = any(left <= world and right <= world for world in worlds)
                body = ContractBody.from_mapping(data)
                if overlaps:
                    with self.assertRaises(AmbiguousContractError):
                        normalize_contract(body)
                else:
                    self.assertEqual(normalize_contract(body), body)

    def test_duplicate_json_keys_at_root_and_nested_levels(self):
        text = json.dumps(example())
        variants = [text.replace('"version": 1', '"version": 1, "version": 1'),
                    text.replace('"role": "seller"', '"role": "seller", "role": "viewer"', 1),
                    text.replace('"version": 1', '"version": 1, "\\u0076ersion": 1')]
        for raw in variants:
            with self.subTest(duplicate=raw[:36]):
                with self.assertRaises(ContractValidationError) as caught:
                    parse_contract(raw)
                self.assertEqual(caught.exception.code, "DUPLICATE_KEY")

    def test_malformed_grammar_numeric_tokens_and_encoding(self):
        raw = json.dumps(example())
        variants = ["", "{}", "[]", "null", raw + "{}", raw[:-1], raw + ",",
                    raw.replace('"version": 1', '"version": 1.0'),
                    raw.replace('"version": 1', '"version": 1e0'),
                    raw.replace('"version": 1', '"version": NaN'),
                    raw.replace('"version": 1', '"version": Infinity'),
                    raw.replace('"version": 1', '"version": ' + "9" * 5000),
                    raw.replace('"version": 1', '"version": true'),
                    raw.replace('"version": 1', '"version": null'),
                    raw.replace('"seller"', '"é"'), raw.replace('"seller"', '"\\ud800"'),
                    b"\xff", b"\xef\xbb\xbf" + raw.encode(), raw.encode("utf-16"), "\ud800"]
        for value in variants:
            with self.subTest(input_type=type(value).__name__, size=len(value)):
                with self.assertRaises(ContractValidationError):
                    parse_contract(value)

    def test_required_fields_and_untrusted_privileged_extras(self):
        for field in example():
            with self.subTest(missing=field):
                data = example()
                del data[field]
                with self.assertRaises(ContractValidationError):
                    ContractBody.from_mapping(data)
        for field in ("status", "approved", "reviewer", "receipt", "target_url", "credentials", "runner"):
            with self.subTest(extra=field):
                data = example()
                data[field] = "synthetic-untrusted"
                with self.assertRaises(ContractValidationError):
                    canonical_bytes(json.dumps(data))
        for field in ("action", "resource"):
            with self.subTest(rule_missing=field):
                data = example()
                del data["rules"][0][field]
                with self.assertRaises(ContractValidationError):
                    parse_contract(json.dumps(data))

    def test_undeclared_duplicate_and_unsupported_values(self):
        mutations = [("schema_version", "1.1"), ("canonicalization", "other"),
                     ("combining", "deny_overrides"), ("version", 0),
                     ("version", 2147483648), ("version", True), ("version", 1.0),
                     ("actions", ["read", "read"]), ("actions", ["write"]),
                     ("roles", ["viewer"]), ("resource_types", ["document"]),
                     ("roles", ["seller", "seller"])]
        for key, value in mutations:
            with self.subTest(key=key, value=value):
                data = example()
                data[key] = value
                with self.assertRaises(ContractValidationError):
                    ContractBody.from_mapping(data)
        data = example()
        data["rules"][1]["rule_id"] = data["rules"][0]["rule_id"]
        with self.assertRaises(ContractValidationError):
            ContractBody.from_mapping(data)
        shared = "synthetic"
        for _ in range(4):
            shared = [shared] * 64
        data = example()
        data["roles"] = shared
        with self.assertRaises(ContractValidationError) as caught:
            ContractBody.from_mapping(data)
        self.assertEqual(caught.exception.code, "INPUT_SIZE")
        data = example()
        data["source_refs"] = ["a" * 65537]
        with self.assertRaises(ContractValidationError) as caught:
            ContractBody.from_mapping(data)
        self.assertEqual(caught.exception.code, "INPUT_SIZE")

    def test_version_and_collection_limits(self):
        for version in (1, 2147483647):
            with self.subTest(version=version):
                data = example()
                data["version"] = version
                self.assertEqual(parse_contract(json.dumps(data)).version, version)
        for field, maximum in (("roles", 64), ("resource_types", 64), ("source_refs", 32), ("rules", 64)):
            with self.subTest(array=field):
                data = example()
                while len(data[field]) < maximum:
                    if field == "rules":
                        item = deepcopy(data["rules"][0])
                        item["rule_id"] = f"rule-{len(data[field])}"
                    else:
                        item = f"name-{len(data[field])}"
                    data[field].append(item)
                self.assertEqual(len(parse_contract(json.dumps(data)).to_mapping()[field]), maximum)
                data[field].append(deepcopy(data[field][-1]))
                with self.assertRaises(ContractValidationError):
                    parse_contract(json.dumps(data))
        for field in ("source_refs", "roles", "resource_types", "actions", "rules"):
            data = example()
            data[field] = []
            with self.subTest(empty=field), self.assertRaises(ContractValidationError):
                ContractBody.from_mapping(data)
        for length in (1, 8, 9):
            data = example()
            data["rules"][0]["when"] = [deepcopy(data["rules"][0]["when"][0])] * length
            with self.subTest(predicates=length):
                if length <= 8:
                    self.assertEqual(len(parse_contract(json.dumps(data)).rules[0].when), length)
                else:
                    with self.assertRaises(ContractValidationError):
                        parse_contract(json.dumps(data))

    def test_byte_and_predecode_depth_limits(self):
        raw = EXAMPLE.read_bytes()
        padded = raw + b" " * (65536 - len(raw))
        self.assertEqual(contract_digest(padded), contract_digest(raw))
        with self.assertRaises(ContractValidationError) as caught:
            parse_contract(padded + b" ")
        self.assertEqual(caught.exception.code, "INPUT_SIZE")
        for depth in (16, 17, 2000):
            with self.subTest(depth=depth):
                with self.assertRaises(ContractValidationError) as caught:
                    parse_contract("[" * depth + "0" + "]" * depth)
                self.assertEqual(caught.exception.code == "INPUT_DEPTH", depth > 16)
        data = example()
        data["unused"] = [data]
        with self.assertRaises(ContractValidationError):
            ContractBody.from_mapping(data)

    def test_json_compatible_yaml_and_unsupported_formats(self):
        raw = EXAMPLE.read_bytes()
        self.assertEqual(parse_contract(raw, format="yaml"), parse_contract(raw, format="json"))
        for value in ("schema_version: 1.0\nrules: []", "!!python/object/apply:os.system []", "---\n{}"):
            with self.subTest(yaml=value), self.assertRaises(ContractValidationError):
                parse_contract(value, format="yaml")
        for value in ("xml", "YAML", None):
            with self.subTest(format=value), self.assertRaises(ContractValidationError):
                parse_contract(raw, format=value)

    def test_detached_immutable_body_and_strict_constructor(self):
        data = example()
        body = ContractBody.from_mapping(data)
        original = contract_digest(body)
        data["rules"][0]["when"].clear()
        exported = body.to_mapping()
        exported["roles"].clear()
        self.assertEqual(contract_digest(body), original)
        with self.assertRaises(FrozenInstanceError):
            body.version = 2
        for field, value in (("version", True), ("rules", list(body.rules)), ("schema_version", "2.0")):
            with self.subTest(constructor=field), self.assertRaises(ContractValidationError):
                replace(body, **{field: value})
        for value in (None, {}, [], 1, True, bytearray(b"{}")):
            with self.subTest(input_type=type(value).__name__), self.assertRaises(ContractValidationError):
                normalize_contract(value)

    def test_versioned_schema_artifact_and_local_references(self):
        schema = contract_json_schema()
        self.assertEqual(schema, json.loads((PACKAGE / "schemas/contract-1.0.schema.json").read_text()))
        self.assertEqual(schema["$schema"], "https://json-schema.org/draft/2020-12/schema")
        self.assertEqual(schema["$id"], "urn:pact:contract-policy:1.0")
        self.assertEqual(set(schema["required"]), set(example()))
        self.assertFalse(schema["additionalProperties"])
        self.assertEqual(schema["properties"]["version"]["maximum"], 2147483647)
        self.assertEqual(schema["properties"]["source_refs"]["maxItems"], 32)
        self.assertEqual(schema["properties"]["rules"]["maxItems"], 64)
        definitions = schema["$defs"]
        for name in ("actor", "resource", "predicate", "rule"):
            self.assertFalse(definitions[name]["additionalProperties"])
            self.assertEqual(set(definitions[name]["required"]), set(definitions[name]["properties"]))
        self.assertEqual(len(definitions["predicate"]["oneOf"]), 5)
        self.assertEqual(definitions["rule"]["properties"]["when"]["maxItems"], 8)
        def check_refs(value):
            if type(value) is dict:
                if "$ref" in value:
                    self.assertTrue(value["$ref"].startswith("#/$defs/"))
                    self.assertIn(value["$ref"].split("/")[-1], definitions)
                for child in value.values():
                    check_refs(child)
            elif type(value) is list:
                for child in value:
                    check_refs(child)
        check_refs(schema)
        schema["properties"]["version"]["maximum"] = 0
        self.assertEqual(contract_json_schema()["properties"]["version"]["maximum"], 2147483647)


if __name__ == "__main__":
    unittest.main()
