"""Fresh local JSON Schema: structural companion, not a semantic validator."""


def scenario_json_schema() -> dict[str, object]:
    def closed(properties):
        return {"type": "object", "properties": properties, "required": list(properties),
                "additionalProperties": False}

    def array(items, minimum, maximum, unique=False):
        value = {"type": "array", "items": items, "minItems": minimum, "maxItems": maximum}
        if unique:
            value["uniqueItems"] = True
        return value

    identifier = {"type": "string", "pattern": r"^[A-Za-z][A-Za-z0-9._-]{0,95}$",
                  "minLength": 1, "maxLength": 96,
                  "not": {"pattern": r"[^A-Za-z0-9._-]"}}
    name = {"$ref": "#/$defs/identifier"}
    profiles = ["object-read-allow-v1", "object-read-deny-403-404-v1",
                "object-read-deny-401-403-404-v1"]
    decision = closed({"kind": {"const": "decision"}, "expected": {"enum": ["ALLOW", "DENY"]},
                       "profile": {"enum": profiles}})
    decision["oneOf"] = [{"properties": {"expected": {"const": "ALLOW"}, "profile": {"const": profiles[0]}}},
                         {"properties": {"expected": {"const": "DENY"}, "profile": {"enum": profiles[1:]}}}]
    resource = closed({"kind": {"enum": ["intended_resource", "no_protected_resource_disclosure",
                                         "no_protected_state_change"]}, "resource_ref": name})
    request = closed({"id": name, "operation": {"const": "http.request"}, "as_actor": name,
                      "method": {"const": "GET"},
                      "route": closed({"route_ref": name, "resource_ref": name}),
                      "expected_rule": name,
                      "assertions": array({"oneOf": [{"$ref": "#/$defs/decision"},
                                                       {"$ref": "#/$defs/resource_assertion"}]}, 2, 3)})
    setup = closed({"id": name, "operation": {"const": "fixture.setup"},
                    "actors": array(name, 1, 64, True), "resources": array(name, 1, 64, True)})
    teardown = closed({"id": name, "operation": {"const": "fixture.teardown"}})
    schema = closed({"schema_version": {"const": "1.0"}, "scenario_id": name,
                     "contract_ref": closed({"contract_id": name, "project_ref": name,
                         "version": {"type": "integer", "minimum": 1, "maximum": 2147483647},
                         "digest": {"type": "string", "pattern": "^[a-f0-9]{64}$", "minLength": 64, "maxLength": 64}}),
                     "fixture_adapter": name,
                     "steps": array({"oneOf": [{"$ref": "#/$defs/setup"}, {"$ref": "#/$defs/request"},
                                                {"$ref": "#/$defs/teardown"}]}, 3, 32)})
    schema.update({"$schema": "https://json-schema.org/draft/2020-12/schema",
                   "$id": "urn:pact:provisional-scenario:1.0",
                   "title": "PROVISIONAL PACT scenario 1.0 (parser-only, not approved)",
                   "$comment": "M1-05 scoped mock-based proposal. Parser additionally enforces UTF-8/ASCII, "
                   "64 KiB/depth 16, duplicate JSON keys, exact integer tokens, unique step IDs, "
                   "setup/request/teardown ordering, required assertion sequence and candidate/catalog bindings. "
                   "No templates, URLs, credentials or executable operations. Schema validity grants no authority. "
                   "The external metaschema URI is metadata only and is never fetched.",
                   "$defs": {"identifier": identifier, "setup": setup, "request": request,
                             "teardown": teardown, "decision": decision, "resource_assertion": resource}})
    return schema
