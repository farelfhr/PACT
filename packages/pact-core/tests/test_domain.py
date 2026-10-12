"""FR-AUT-001/002: structural validation, not authorization execution."""

from copy import deepcopy
from dataclasses import FrozenInstanceError, replace
from pathlib import Path
import json
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from pact_core.domain import (
    Actor, ActorId, ActorSelector, AssertionProfile, Binding,
    Decision, DomainCatalog, DomainValidationError, Predicate, Relation,
    Resource, ResourceId, ResourceSelector, ResourceTypeId, RoleId, Rule,
    RuleId, ScenarioVerdict, Tenant, TenantId,
)


def catalog_data():
    return {
        "roles": ["seller", "viewer"], "resource_types": ["order", "document"],
        "tenants": [{"id": "tenant-a"}, {"id": "tenant-b"}],
        "actors": [
            {"id": "seller-a", "tenant": "tenant-a", "roles": ["seller"],
             "memberships": ["tenant-a", "tenant-b"]},
            {"id": "seller-b", "tenant": "tenant-b", "roles": ["seller"],
             "memberships": ["tenant-b"]},
        ],
        "resources": [
            {"id": "order-a", "tenant": "tenant-a", "type": "order",
             "owner": "seller-a", "shared_with": ["seller-b"]},
            {"id": "order-b", "tenant": "tenant-b", "type": "order",
             "owner": "seller-b", "shared_with": []},
        ],
    }


def rule_data():
    return {
        "rule_id": "own-tenant", "actor": {"role": "seller"},
        "resource": {"type": "order"}, "action": "read",
        "when": [{"relation": "same_tenant", "subject": "actor.tenant",
                  "object": "resource.tenant"}],
        "expect": "ALLOW", "assertion_profile": "object-read-allow-v1",
    }


class DomainTests(unittest.TestCase):
    def test_accepted_adr_example_rules(self):
        root = Path(__file__).resolve().parents[3]
        data = json.loads((root / "docs/adr/examples/0001-valid-contract.json").read_text())
        catalog = DomainCatalog.from_mapping(catalog_data())
        for index, expected in enumerate((Decision.ALLOW, Decision.DENY)):
            with self.subTest(rule=index):
                rule = Rule.from_mapping(data["rules"][index])
                catalog.validate_rule(rule)
                self.assertEqual(rule.expect, expected)

    def test_exact_collection_limits_and_detached_inputs(self):
        data = catalog_data()
        data["roles"] = ["seller"] + [f"role-{i}" for i in range(63)]
        data["resource_types"] = ["order"] + [f"type-{i}" for i in range(63)]
        catalog = DomainCatalog.from_mapping(data)
        data["actors"][0]["roles"][0] = "changed"
        self.assertEqual(catalog.actors[0].roles, (RoleId("seller"),))
        self.assertEqual(len(catalog.roles), 64)
        data = rule_data()
        data["when"] *= 8
        rule = Rule.from_mapping(data)
        self.assertEqual(len(rule.when), 8)
        data["when"][0]["relation"] = "changed"
        self.assertEqual(rule.when[0].relation, Relation.SAME_TENANT)

    def test_valid_catalog_and_explicit_cross_tenant_edges(self):
        catalog = DomainCatalog.from_mapping(catalog_data())
        catalog.validate_rule(Rule.from_mapping(rule_data()))
        self.assertEqual(catalog.actors[0].tenant, TenantId("tenant-a"))
        self.assertIn(TenantId("tenant-b"), catalog.actors[0].memberships)
        self.assertEqual(catalog.resources[0].shared_with, (ActorId("seller-b"),))
        self.assertNotEqual(ActorId("same"), TenantId("same"))
        self.assertNotEqual(TenantId("same"), ResourceId("same"))

    def test_primary_tenant_does_not_invent_membership_or_shares(self):
        data = catalog_data()
        data["actors"][0]["memberships"] = []
        data["resources"][0]["shared_with"] = []
        catalog = DomainCatalog.from_mapping(data)
        self.assertEqual(catalog.actors[0].memberships, ())
        self.assertEqual(catalog.resources[0].shared_with, ())

    def test_all_relation_signatures(self):
        signatures = [
            ("owns", "actor", "resource"),
            ("member_of", "actor", "resource.tenant"),
            ("shared_with", "resource", "actor"),
            ("same_tenant", "actor.tenant", "resource.tenant"),
            ("different_tenant", "actor.tenant", "resource.tenant"),
        ]
        for relation, subject, object_ in signatures:
            with self.subTest(relation=relation):
                predicate = Predicate.from_mapping(
                    {"relation": relation, "subject": subject, "object": object_})
                self.assertEqual(predicate.relation.value, relation)

    def test_wrong_relation_bindings_and_expressions(self):
        for relation in Relation:
            for subject in Binding:
                for object_ in Binding:
                    accepted = {
                        Relation.OWNS: (Binding.ACTOR, Binding.RESOURCE),
                        Relation.MEMBER_OF: (Binding.ACTOR, Binding.RESOURCE_TENANT),
                        Relation.SHARED_WITH: (Binding.RESOURCE, Binding.ACTOR),
                        Relation.SAME_TENANT: (Binding.ACTOR_TENANT, Binding.RESOURCE_TENANT),
                        Relation.DIFFERENT_TENANT: (Binding.ACTOR_TENANT, Binding.RESOURCE_TENANT),
                    }[relation]
                    if (subject, object_) != accepted:
                        with self.subTest(relation=relation, subject=subject, object=object_):
                            with self.assertRaises(DomainValidationError):
                                Predicate(relation, subject, object_)
        for value in ("unknown", "__import__('os').system('never-run')", "${actor}"):
            for field in ("relation", "subject", "object"):
                with self.subTest(field=field, value=value):
                    data = {"relation": "owns", "subject": "actor", "object": "resource"}
                    data[field] = value
                    with self.assertRaises(DomainValidationError):
                        Predicate.from_mapping(data)

    def test_decision_profile_pairings(self):
        for decision in Decision:
            for profile in AssertionProfile:
                with self.subTest(decision=decision, profile=profile):
                    data = rule_data()
                    data.update(expect=decision.value, assertion_profile=profile.value)
                    valid = ((decision == Decision.ALLOW) ==
                             (profile == AssertionProfile.OBJECT_READ_ALLOW))
                    if valid:
                        self.assertEqual(Rule.from_mapping(data).expect, decision)
                    else:
                        with self.assertRaises(DomainValidationError):
                            Rule.from_mapping(data)

    def test_unknown_policy_enums(self):
        for field, values in {
            "action": ["write", "READ", "", 1, True, None],
            "expect": ["PASS", "allow", "APPROVED", 1, None],
            "assertion_profile": ["status-only", "object-read-allow-v2", 403, None],
        }.items():
            for value in values:
                with self.subTest(field=field, value=value):
                    data = rule_data()
                    data[field] = value
                    with self.assertRaises(DomainValidationError):
                        Rule.from_mapping(data)

    def test_missing_every_required_rule_field(self):
        for field in rule_data():
            with self.subTest(field=field):
                data = rule_data()
                del data[field]
                with self.assertRaises(DomainValidationError):
                    Rule.from_mapping(data)

    def test_privileged_fields_rejected_at_every_mapping_boundary(self):
        samples = [
            (Tenant, {"id": "tenant-a"}),
            (Actor, catalog_data()["actors"][0]),
            (Resource, catalog_data()["resources"][0]),
            (ActorSelector, {"role": "seller"}),
            (ResourceSelector, {"type": "order"}),
            (Predicate, rule_data()["when"][0]),
            (Rule, rule_data()), (DomainCatalog, catalog_data()),
        ]
        for cls, data in samples:
            for key in ("status", "approved", "reviewer", "target_url", "command", "verdict"):
                with self.subTest(entity=cls.__name__, key=key):
                    forged = deepcopy(data)
                    forged[key] = "synthetic-untrusted"
                    with self.assertRaises(DomainValidationError):
                        cls.from_mapping(forged)

    def test_nested_missing_and_extra_fields(self):
        for field, inner in (("actor", "role"), ("resource", "type")):
            for mutation in ("missing", "privileged"):
                with self.subTest(field=field, mutation=mutation):
                    data = rule_data()
                    if mutation == "missing":
                        del data[field][inner]
                    else:
                        data[field]["approved"] = True
                    with self.assertRaises(DomainValidationError):
                        Rule.from_mapping(data)
        data = rule_data()
        data["when"][0]["command"] = "never-run"
        with self.assertRaises(DomainValidationError):
            Rule.from_mapping(data)

    def test_identifier_boundaries_and_kinds(self):
        classes = (ActorId, TenantId, ResourceId, RoleId, ResourceTypeId, RuleId)
        for cls in classes:
            for value in ("A", "a._-09", "a" * 96):
                with self.subTest(kind=cls.__name__, valid=value):
                    self.assertEqual(cls(value).value, value)
            for value in ("", "1a", "a" * 97, "tenant/a", "a b", "é", "a\n", 1, True, None):
                with self.subTest(kind=cls.__name__, invalid=value):
                    with self.assertRaises(DomainValidationError):
                        cls(value)
        for value in (ActorId("tenant-a"), ResourceId("tenant-a"), "tenant-a"):
            with self.subTest(tenant_kind=type(value).__name__):
                with self.assertRaises(DomainValidationError):
                    Tenant(value)

    def test_missing_or_unknown_fixture_references(self):
        mutations = [
            ("actors", "tenant", "absent"),
            ("actors", "memberships", ["absent"]),
            ("actors", "roles", ["absent"]),
            ("resources", "tenant", "absent"),
            ("resources", "owner", "absent"),
            ("resources", "shared_with", ["absent"]),
            ("resources", "type", "absent"),
        ]
        for category, field, value in mutations:
            with self.subTest(category=category, field=field):
                data = catalog_data()
                data[category][0][field] = value
                with self.assertRaises(DomainValidationError):
                    DomainCatalog.from_mapping(data)
        for field in catalog_data()["resources"][0]:
            with self.subTest(missing_resource_field=field):
                data = catalog_data()
                del data["resources"][0][field]
                with self.assertRaises(DomainValidationError):
                    DomainCatalog.from_mapping(data)

    def test_duplicate_declarations_and_references(self):
        for field in catalog_data():
            with self.subTest(field=field):
                data = catalog_data()
                data[field].append(deepcopy(data[field][0]))
                with self.assertRaises(DomainValidationError):
                    DomainCatalog.from_mapping(data)
        for category, field in (("actors", "roles"), ("actors", "memberships"),
                                ("resources", "shared_with")):
            with self.subTest(category=category, field=field):
                data = catalog_data()
                data[category][0][field] *= 2
                with self.assertRaises(DomainValidationError):
                    DomainCatalog.from_mapping(data)

    def test_undeclared_rule_selectors(self):
        catalog = DomainCatalog.from_mapping(catalog_data())
        for field, inner in (("actor", "role"), ("resource", "type")):
            with self.subTest(field=field):
                data = rule_data()
                data[field][inner] = "absent"
                with self.assertRaises(DomainValidationError):
                    catalog.validate_rule(Rule.from_mapping(data))

    def test_empty_excessive_and_wrong_collection_types(self):
        for field in ("roles", "resource_types", "tenants", "actors", "resources"):
            for value in ([], None, "value", (), [None], ["a"] * 65):
                with self.subTest(field=field, value_type=type(value).__name__):
                    data = catalog_data()
                    data[field] = value
                    with self.assertRaises(DomainValidationError):
                        DomainCatalog.from_mapping(data)
        for value in ([], None, "actor.tenant == resource.tenant", (), [rule_data()["when"][0]] * 9):
            with self.subTest(when=value):
                data = rule_data()
                data["when"] = value
                with self.assertRaises(DomainValidationError):
                    Rule.from_mapping(data)

    def test_immutability_and_no_constructor_coercion(self):
        catalog = DomainCatalog.from_mapping(catalog_data())
        for entity in (catalog, catalog.actors[0], catalog.resources[0],
                       catalog.tenants[0], TenantId("tenant-a"), Rule.from_mapping(rule_data())):
            with self.subTest(entity=type(entity).__name__):
                with self.assertRaises((FrozenInstanceError, AttributeError, TypeError)):
                    entity.status = "APPROVED"
        actor = catalog.actors[0]
        for field, value in (("id", TenantId("seller-a")), ("tenant", ActorId("tenant-a")),
                             ("roles", [RoleId("seller")]), ("memberships", [TenantId("tenant-a")])):
            with self.subTest(field=field):
                with self.assertRaises(DomainValidationError):
                    replace(actor, **{field: value})
        rule = Rule.from_mapping(rule_data())
        for field, value in (("action", "read"), ("expect", "ALLOW"),
                             ("when", list(rule.when)), ("resource", None)):
            with self.subTest(field=field):
                with self.assertRaises(DomainValidationError):
                    replace(rule, **{field: value})

    def test_mappings_are_closed_plain_data(self):
        for value in (None, [], "{}", 1, True, {1: "non-string-key"}):
            for cls in (Tenant, Actor, Resource, Predicate, Rule, DomainCatalog):
                with self.subTest(entity=cls.__name__, value=value):
                    with self.assertRaises(DomainValidationError):
                        cls.from_mapping(value)

    def test_verdict_enum_is_separate_from_expected_decision(self):
        self.assertEqual({v.value for v in ScenarioVerdict},
                         {"PASS", "VIOLATION", "INCONCLUSIVE", "ERROR", "SKIPPED", "CANCELED"})
        self.assertEqual({v.value for v in Decision}, {"ALLOW", "DENY"})
        for value in ("APPROVED", "NEEDS_REVIEW", "ALLOW", "COMPLETED", "secure"):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    ScenarioVerdict(value)


if __name__ == "__main__":
    unittest.main()
