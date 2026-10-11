"""FR-CON-001/002, AC-002: lifecycle claims are never authenticated approval."""

from copy import deepcopy
from dataclasses import FrozenInstanceError, replace
from datetime import datetime, timedelta, timezone
import json
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from pact_core.domain import (
    ApprovalRequiredError, ContractStatus, DomainValidationError, ModelTransitionError,
    UntrustedApprovalSnapshot, UntrustedContractState, canonical_bytes, contract_digest,
    import_candidate, new_draft_version, parse_contract, require_authenticated_approval,
    transition_model,
)

FIXTURE = Path(__file__).parent / "fixtures/contracts/valid-v1.json"
NOW = datetime(2026, 10, 10, 12, 0, tzinfo=timezone.utc)


def draft():
    return import_candidate(FIXTURE.read_bytes(), claimed_author_ref="synthetic-author")


def move(record, target, event, snapshot=None):
    return transition_model(record, target, event_id=event, expected_revision=record.revision,
                            expected_digest=record.content_digest, claimed_snapshot=snapshot)


def ready():
    return move(draft(), ContractStatus.NEEDS_REVIEW, "request-review")


def snapshot(record, **changes):
    data = dict(body=record.body, content_digest=record.content_digest,
                claimed_author_ref=record.claimed_author_ref,
                claimed_reviewer_ref="synthetic-reviewer", claimed_review_ref="claimed-approval",
                claimed_reviewed_at=NOW)
    data.update(changes)
    return UntrustedApprovalSnapshot(**data)


def approved():
    record = ready()
    return move(record, ContractStatus.APPROVED, "claimed-approval", snapshot(record))


class ApprovalModelTests(unittest.TestCase):
    def test_all_statuses_and_exact_transition_matrix(self):
        states = {ContractStatus.DRAFT: draft(), ContractStatus.NEEDS_REVIEW: ready(),
                  ContractStatus.APPROVED: approved(),
                  ContractStatus.REJECTED: move(ready(), ContractStatus.REJECTED, "reject"),
                  ContractStatus.SUPERSEDED: move(approved(), ContractStatus.SUPERSEDED, "supersede"),
                  ContractStatus.DEPRECATED: move(approved(), ContractStatus.DEPRECATED, "deprecate")}
        allowed = {(ContractStatus.DRAFT, ContractStatus.NEEDS_REVIEW),
                   (ContractStatus.NEEDS_REVIEW, ContractStatus.APPROVED),
                   (ContractStatus.NEEDS_REVIEW, ContractStatus.REJECTED),
                   (ContractStatus.APPROVED, ContractStatus.SUPERSEDED),
                   (ContractStatus.APPROVED, ContractStatus.DEPRECATED)}
        self.assertEqual({state.value for state in states},
                         {"DRAFT", "NEEDS_REVIEW", "APPROVED", "REJECTED", "SUPERSEDED", "DEPRECATED"})
        for source, record in states.items():
            for target in states:
                with self.subTest(source=source.value, target=target.value):
                    claim = snapshot(record, claimed_review_ref="fresh-event") if target == ContractStatus.APPROVED else None
                    if (source, target) in allowed:
                        changed = move(record, target, "fresh-event", claim)
                        self.assertEqual(changed.status, target)
                        self.assertEqual(changed.revision, record.revision + 1)
                        self.assertEqual(changed.history[:-1], record.history)
                        self.assertEqual(changed.body, record.body)
                        self.assertFalse(changed.is_authoritative)
                    else:
                        with self.assertRaises(ModelTransitionError):
                            move(record, target, "fresh-event", claim)

    def test_revision_digest_and_duplicate_event_replay(self):
        record = ready()
        for revision, digest in ((0, record.content_digest), (True, record.content_digest),
                                 (1, "0" * 64), (1, record.content_digest.upper())):
            with self.subTest(revision=revision, digest=digest):
                with self.assertRaises(ModelTransitionError):
                    transition_model(record, ContractStatus.REJECTED, event_id="new-event",
                                     expected_revision=revision, expected_digest=digest)
        with self.assertRaises(ModelTransitionError) as caught:
            move(record, ContractStatus.REJECTED, "request-review")
        self.assertEqual(caught.exception.code, "REPLAY")
        completed = approved()
        with self.assertRaises(ModelTransitionError):
            move(completed, ContractStatus.APPROVED, "claimed-approval", completed.snapshot)
        self.assertEqual(record.status, ContractStatus.NEEDS_REVIEW)

    def test_modeled_approval_requires_exact_bound_snapshot(self):
        record = ready()
        with self.assertRaises(ModelTransitionError):
            move(record, ContractStatus.APPROVED, "claimed-approval")
        for changes in ({"claimed_author_ref": "different-author"},
                        {"claimed_review_ref": "different-event"}):
            with self.subTest(changes=changes), self.assertRaises(ModelTransitionError):
                move(record, ContractStatus.APPROVED, "claimed-approval", snapshot(record, **changes))
        data = record.body.to_mapping()
        data["version"] = 2
        other = parse_contract(json.dumps(data))
        foreign = snapshot(record, body=other, content_digest=contract_digest(other))
        with self.assertRaises(ModelTransitionError):
            move(record, ContractStatus.APPROVED, "claimed-approval", foreign)
        with self.assertRaises(ModelTransitionError):
            move(record, ContractStatus.REJECTED, "reject", snapshot(record))

    def test_snapshot_and_history_are_immutable_and_digest_bound(self):
        record = approved()
        claim = record.snapshot
        self.assertEqual(claim.canonical_body, canonical_bytes(record.body))
        self.assertEqual(claim.content_digest, contract_digest(record.body))
        self.assertEqual(claim.body.source_refs, record.body.source_refs)
        for value, field, replacement in ((record, "body", None), (claim, "content_digest", "0" * 64),
                                          (claim.body, "version", 2), (record.history[0], "event_id", "edited")):
            with self.subTest(field=field), self.assertRaises(FrozenInstanceError):
                setattr(value, field, replacement)
        data = record.body.to_mapping()
        data["rules"][0]["rule_id"] = "edited-rule"
        edited = parse_contract(json.dumps(data))
        with self.assertRaises(DomainValidationError):
            replace(record, body=edited)
        with self.assertRaises(DomainValidationError):
            replace(claim, body=edited)
        with self.assertRaises(DomainValidationError):
            replace(claim, content_digest="0" * 64)
        exported = claim.to_mapping()
        exported["body"]["rules"].clear()
        self.assertEqual(claim.content_digest, contract_digest(record.body))

    def test_edits_create_new_draft_version_without_rewriting_history(self):
        for record in (draft(), ready(), approved(), move(ready(), ContractStatus.REJECTED, "reject")):
            with self.subTest(status=record.status.value):
                old_hash = record.content_digest
                old_history = record.history
                data = record.body.to_mapping()
                data["version"] += 1
                data["rules"][0]["rule_id"] = "edited-rule"
                changed = new_draft_version(record, parse_contract(json.dumps(data)))
                self.assertEqual(changed.status, ContractStatus.DRAFT)
                self.assertEqual(changed.revision, 0)
                self.assertEqual(changed.history, ())
                self.assertIsNone(changed.snapshot)
                self.assertEqual(changed.body.version, record.body.version + 1)
                self.assertEqual(record.content_digest, old_hash)
                self.assertEqual(record.history, old_history)
                self.assertNotEqual(changed.content_digest, old_hash)
        record = approved()
        for field, value in (("version", 1), ("version", 3), ("contract_id", "other-policy"),
                             ("project_ref", "other-project")):
            data = record.body.to_mapping()
            data["version"] = 2
            data[field] = value
            with self.subTest(field=field), self.assertRaises(DomainValidationError):
                new_draft_version(record, parse_contract(json.dumps(data)))

    def test_imported_approval_claims_and_execution_authority_always_rejected(self):
        base = json.loads(FIXTURE.read_bytes())
        claim = approved().snapshot
        for field, value in (("status", "APPROVED"), ("approved", True),
                             ("review", {"reviewer": "human"}), ("content_digest", contract_digest(FIXTURE.read_bytes())),
                             ("snapshot", claim.to_mapping()), ("receipt", "synthetic-replayed-receipt")):
            data = deepcopy(base)
            data[field] = value
            with self.subTest(field=field), self.assertRaises(DomainValidationError):
                import_candidate(json.dumps(data), claimed_author_ref="synthetic-author")
        with self.assertRaises(DomainValidationError):
            import_candidate(json.dumps(claim.to_mapping()), claimed_author_ref="synthetic-author")
        for value in (draft(), ready(), approved(), claim, claim.to_mapping(),
                      json.dumps(claim.to_mapping()), {"status": "APPROVED"}, None, True):
            with self.subTest(value_type=type(value).__name__), self.assertRaises(ApprovalRequiredError):
                require_authenticated_approval(value)
        self.assertFalse(claim.is_authoritative)
        self.assertEqual(claim.to_mapping()["kind"], "UNTRUSTED_APPROVAL_MODEL")
        # Valid imports always start as candidates; no approval fields are stripped.
        self.assertEqual(draft().status, ContractStatus.DRAFT)

    def test_constructor_cannot_skip_or_rewrite_history(self):
        record = approved()
        for changes in ({"status": ContractStatus.APPROVED, "history": (), "revision": 0},
                        {"status": "APPROVED"}, {"revision": True}, {"history": list(record.history)},
                        {"snapshot": None}, {"history": record.history[::-1]},
                        {"claimed_author_ref": "other-author"}):
            with self.subTest(changes=changes), self.assertRaises(DomainValidationError):
                replace(record, **changes)
        event = record.history[0]
        with self.assertRaises(DomainValidationError):
            replace(record, history=(event, event))
        with self.assertRaises(DomainValidationError):
            replace(record.history[0], expected_revision=True)

    def test_forked_replayed_or_transplanted_claims_never_become_trusted(self):
        pending = ready()
        claim = snapshot(pending)
        first = move(pending, ContractStatus.APPROVED, "claimed-approval", claim)
        replayed_copy = move(pending, ContractStatus.APPROVED, "claimed-approval", claim)
        # No durable nonce store or atomic application transaction exists here.
        # An old model can be copied, but neither copy is approval authority.
        for value in (first, replayed_copy, replace(claim, claimed_reviewed_at=NOW - timedelta(days=365)),
                      {"status": "APPROVED", "is_authoritative": True}):
            with self.subTest(value_type=type(value).__name__), self.assertRaises(ApprovalRequiredError):
                require_authenticated_approval(value)
        data = pending.body.to_mapping()
        data["project_ref"] = "other-project"
        foreign = import_candidate(json.dumps(data), claimed_author_ref=pending.claimed_author_ref)
        foreign = move(foreign, ContractStatus.NEEDS_REVIEW, "request-review")
        with self.assertRaises(ModelTransitionError):
            move(foreign, ContractStatus.APPROVED, "claimed-approval", claim)
        for field, value in (("contract_id", "other-policy"), ("version", 2)):
            data = pending.body.to_mapping()
            data[field] = value
            changed = parse_contract(json.dumps(data))
            foreign = replace(foreign, body=changed, history=(), revision=0, status=ContractStatus.DRAFT)
            foreign = move(foreign, ContractStatus.NEEDS_REVIEW, "request-review")
            with self.subTest(field=field), self.assertRaises(ModelTransitionError):
                move(foreign, ContractStatus.APPROVED, "claimed-approval", claim)

    def test_strict_metadata_and_timezone_without_authentication_claim(self):
        record = ready()
        for changes in ({"claimed_reviewer_ref": ""}, {"claimed_review_ref": "../unsafe"},
                        {"claimed_author_ref": True}, {"claimed_reviewed_at": NOW.replace(tzinfo=None)},
                        {"claimed_reviewed_at": NOW.astimezone(timezone(timedelta(hours=1)))},
                        {"claimed_reviewed_at": "2026-10-10T12:00:00Z"},
                        {"content_digest": record.content_digest.upper()}):
            with self.subTest(changes=changes), self.assertRaises(DomainValidationError):
                snapshot(record, **changes)
        for target in ("APPROVED", None, True):
            with self.subTest(target=target), self.assertRaises(DomainValidationError):
                move(record, target, "synthetic-event")
        for event in ("", "../event", True):
            with self.subTest(event=event), self.assertRaises(DomainValidationError):
                move(record, ContractStatus.REJECTED, event)
        for value in (None, {}, True, FIXTURE.read_bytes()):
            with self.subTest(model=type(value).__name__), self.assertRaises(DomainValidationError):
                new_draft_version(value, record.body)


if __name__ == "__main__":
    unittest.main()
