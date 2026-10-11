"""Offline, fresh JSON Schema description of candidate policy structure."""


def contract_json_schema() -> dict[str, object]:
    """No remote resolution or filesystem access; semantic normalization is separate."""
    identifier = {"type": "string", "minLength": 1, "maxLength": 96,
                  "pattern": "^[A-Za-z][A-Za-z0-9._-]{0,95}$",
                  "not": {"pattern": "[^A-Za-z0-9._-]"}}

    def closed(properties):
        return {"type": "object", "properties": properties,
                "required": list(properties), "additionalProperties": False}

    def bounded(items, maximum, unique=False):
        return {"type": "array", "items": items, "minItems": 1,
                "maxItems": maximum, "uniqueItems": unique}

    signatures = [("owns", "actor", "resource"),
                  ("member_of", "actor", "resource.tenant"),
                  ("shared_with", "resource", "actor"),
                  ("same_tenant", "actor.tenant", "resource.tenant"),
                  ("different_tenant", "actor.tenant", "resource.tenant")]
    predicate = closed({"relation": {"enum": [item[0] for item in signatures]},
                        "subject": {"enum": ["actor", "resource", "actor.tenant"]},
                        "object": {"enum": ["actor", "resource", "resource.tenant"]}})
    predicate["oneOf"] = [{"properties": {"relation": {"const": relation},
                                        "subject": {"const": subject},
                                        "object": {"const": target}}}
                          for relation, subject, target in signatures]
    profiles = ["object-read-allow-v1", "object-read-deny-403-404-v1",
                "object-read-deny-401-403-404-v1"]
    rule = closed({"rule_id": {"$ref": "#/$defs/identifier"},
                   "actor": {"$ref": "#/$defs/actor"},
                   "resource": {"$ref": "#/$defs/resource"},
                   "action": {"const": "read"},
                   "when": bounded({"$ref": "#/$defs/predicate"}, 8),
                   "expect": {"enum": ["ALLOW", "DENY"]},
                   "assertion_profile": {"enum": profiles}})
    rule["oneOf"] = [
        {"properties": {"expect": {"const": "ALLOW"},
                        "assertion_profile": {"const": profiles[0]}}},
        {"properties": {"expect": {"const": "DENY"},
                        "assertion_profile": {"enum": profiles[1:]}}}]
    schema = closed({
        "schema_version": {"const": "1.0"},
        "canonicalization": {"const": "pact-json-1"},
        "contract_id": {"$ref": "#/$defs/identifier"},
        "project_ref": {"$ref": "#/$defs/identifier"},
        "version": {"type": "integer", "minimum": 1, "maximum": 2147483647},
        "source_refs": bounded({"$ref": "#/$defs/identifier"}, 32),
        "roles": bounded({"$ref": "#/$defs/identifier"}, 64, True),
        "resource_types": bounded({"$ref": "#/$defs/identifier"}, 64, True),
        "actions": bounded({"const": "read"}, 1, True),
        "combining": {"const": "reject_conflicts"},
        "on_unmatched": {"const": "NEEDS_REVIEW"},
        "rules": bounded({"$ref": "#/$defs/rule"}, 64)})
    schema.update({"$schema": "https://json-schema.org/draft/2020-12/schema",
                   "$id": "urn:pact:contract-policy:1.0",
                   "title": "PACT 1.0 candidate policy body (not approval)",
                   "$comment": "The decoder additionally enforces 64 KiB UTF-8, depth 16, "
                   "duplicate-key rejection and integer-token grammar (no floats/non-finite values). "
                   "Domain checks enforce declared selectors and unique rule IDs. Normalization "
                   "rejects possible decision/profile conflicts and unsatisfiable tenant conjunctions. "
                   "This schema and any body digest confer no approval or execution authority.",
                   "$defs": {"identifier": identifier,
                             "actor": closed({"role": {"$ref": "#/$defs/identifier"}}),
                             "resource": closed({"type": {"$ref": "#/$defs/identifier"}}),
                             "predicate": predicate, "rule": rule}})
    return schema
