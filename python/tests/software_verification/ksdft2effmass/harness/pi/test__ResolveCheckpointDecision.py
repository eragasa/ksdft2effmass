r"""Software verification of ``ResolveCheckpointDecision``.

Facet and represented meaning
Software verification of pure deterministic generic checkpoint transformation.

Intrinsic and cross-object scope
The sole primary SUT is ``ResolveCheckpointDecision``. Explicit status matching,
option membership, immutable field replacement and preservation, idempotency,
conflicts, deterministic findings, nonmutation, and no operational side effects are in
scope. Human-intent interpretation and project-local JSON patching are excluded.

VVUQ and scientific exclusions
Passing establishes only deterministic software behavior, not scientific validity,
uncertainty quantification, human acceptance, persistence, or task resumption.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest

from ksdft2effmass.harness.pi import (
    CheckpointDecisionResolutionRequest,
    CheckpointRecord,
    ResolveCheckpointDecision,
)

pytestmark = pytest.mark.software_verification
SUT = ResolveCheckpointDecision


def make_checkpoint_for_resolution(
    *,
    status: str = "pending",
    human_response: str | None = None,
    normalized_decision: str | None = None,
    resolved_at: str | None = None,
    authorized_scope: str | None = None,
) -> CheckpointRecord:
    """Evidence ID
    Owns no identifier; supports checkpoint-transformation evidence.
    Requirement
    Action tests require exact synthetic generic checkpoint states.
    Method
    Construct CheckpointRecord from fixed fields and explicit lifecycle overrides.
    Oracle
    The public generic record contract defines valid represented support states.
    Acceptance
    Return one immutable checkpoint preserving fixed nonresolution fields.
    Interpretation
    Failure indicates invalid setup rather than Action behavior.
    Limitations
    This helper owns no independent evidence claim or local checkpoint fields.
    """
    return CheckpointRecord(
        1,
        "T1-HC01",
        "T1",
        "episode-T1",
        status,
        "contract",
        "2026-08-04T00:00:00Z",
        "Choose an option.",
        (("A", "Accept.", None), ("B", "Defer.", "Remain blocked.")),
        human_response,
        normalized_decision,
        resolved_at,
        authorized_scope,
        ("checkpoints/T1.json", "tasks/T1.json"),
        "blocked",
    )


def make_resolution_request(
    checkpoint: CheckpointRecord,
    *,
    expected_status: str = "pending",
    human_response: str = "Approve A exactly.",
    normalized_decision: str = "A",
    resolved_at: str = "2026-08-04T00:01:02Z",
    authorized_scope: str = "bounded implementation",
) -> CheckpointDecisionResolutionRequest:
    """Evidence ID
    Owns no identifier; supports checkpoint-transformation evidence.
    Requirement
    Action tests require complete explicit decision-bearing inputs.
    Method
    Construct a request from one checkpoint and caller-selected overrides.
    Oracle
    The accepted request contract fixes valid support values.
    Acceptance
    Return one immutable request without interpretation or clock access.
    Interpretation
    Failure indicates invalid setup rather than Action behavior.
    Limitations
    This helper owns no independent evidence claim.
    """
    return CheckpointDecisionResolutionRequest(
        checkpoint,
        expected_status,
        "resolved",
        human_response,
        normalized_decision,
        resolved_at,
        authorized_scope,
    )


def test_constructor__action_object__is_stateless_and_fieldless() -> None:
    """Evidence ID
    SV-HARNESS-105
    Requirement
    ResolveCheckpointDecision is a concrete fieldless stateless ActionObject.
    Method
    Construct two instances and inspect their public storage boundary.
    Oracle
    The accepted ActionObject contract requires empty slots and no dictionary.
    Acceptance
    Both instances construct without mutable instance state.
    Interpretation
    Failure indicates hidden state or public ActionObject drift.
    Limitations
    Structural statelessness alone does not establish transformation correctness.
    """
    assert SUT.__slots__ == ()
    assert not hasattr(SUT(), "__dict__")
    assert not hasattr(SUT(), "__dict__")


def test_method__execute__resolves_pending_with_exact_changes_and_preservation() -> (
    None
):
    """Evidence ID
    SV-HARNESS-106
    Requirement
    A matching pending checkpoint resolves with only five resolution fields changed.
    Method
    Execute option A against a synthetic pending record and compare every field.
    Oracle
    The explicit request and original immutable record fix changed and preserved state.
    Acceptance
    Result is PASS/changed, exact decision fields are set, all listed nonresolution
    fields and option ordering are preserved, and input remains unchanged.
    Interpretation
    Failure indicates transformation, option matching, preservation, or mutation drift.
    Limitations
    No project-local fields, persistence, or human interpretation are represented.
    """
    checkpoint = make_checkpoint_for_resolution()
    request = make_resolution_request(checkpoint)
    result = SUT().execute(request)
    assert result.validation.status == "PASS" and result.changed is True
    assert result.checkpoint is not None and result.checkpoint is not checkpoint
    resolved = result.checkpoint
    assert resolved.status == "resolved"
    assert resolved.human_response == request.human_response
    assert resolved.normalized_decision == "A"
    assert resolved.resolved_at == request.resolved_at
    assert resolved.authorized_scope == request.authorized_scope
    assert (
        resolved.schema_version,
        resolved.checkpoint_id,
        resolved.task_id,
        resolved.episode_id,
        resolved.decision_class,
        resolved.created_at,
        resolved.question,
        resolved.options,
        resolved.record_paths,
        resolved.resumption_status,
    ) == (
        checkpoint.schema_version,
        checkpoint.checkpoint_id,
        checkpoint.task_id,
        checkpoint.episode_id,
        checkpoint.decision_class,
        checkpoint.created_at,
        checkpoint.question,
        checkpoint.options,
        checkpoint.record_paths,
        checkpoint.resumption_status,
    )
    assert checkpoint.status == "pending"
    assert checkpoint.human_response is None
    assert checkpoint.normalized_decision is None
    assert checkpoint.resolved_at is None
    assert checkpoint.authorized_scope is None


def test_method__execute__resolves_blocked_when_explicitly_expected() -> None:
    """Evidence ID
    SV-HARNESS-107
    Requirement
    A blocked checkpoint resolves only when blocked is the explicit expected status.
    Method
    Supply a blocked record and expected_status='blocked' with declared option B.
    Oracle
    Exact request status and option fields determine the transformation.
    Acceptance
    Result is changed/PASS and records option B without altering resumption status.
    Interpretation
    Failure indicates hard-coded pending status, option choice, or resumption drift.
    Limitations
    The action does not infer that blocked should resolve or resume a task.
    """
    checkpoint = make_checkpoint_for_resolution(status="blocked")
    request = make_resolution_request(
        checkpoint,
        expected_status="blocked",
        human_response="Defer with B.",
        normalized_decision="B",
        authorized_scope="remain blocked",
    )
    result = SUT().execute(request)
    assert result.validation.status == "PASS" and result.changed is True
    assert result.checkpoint is not None
    assert result.checkpoint.normalized_decision == "B"
    assert result.checkpoint.resumption_status == "blocked"


def test_method__execute__unknown_option_and_partial_state_return_ordered_failure() -> (
    None
):
    """Evidence ID
    SV-HARNESS-108
    Requirement
    Unknown exact option IDs and partial unresolved resolution state fail
    structurally with deterministic ordering and no partial record.
    Method
    Request lowercase undeclared option 'a' from pending state containing two
    contradictory resolution fields.
    Oracle
    Closed issue-code lexical ordering fixes DECISION_UNKNOWN before
    STATE_CONTRADICTION and exact related field ordering.
    Acceptance
    Both exact codes and related IDs are ordered, checkpoint is None, changed=False.
    Interpretation
    Failure indicates case-insensitive matching, partial resolution, or ordering drift.
    Limitations
    The action does not explain or reinterpret the unknown human decision.
    """
    checkpoint = make_checkpoint_for_resolution(
        human_response="partial", authorized_scope="partial scope"
    )
    result = SUT().execute(make_resolution_request(checkpoint, normalized_decision="a"))
    assert [issue.code for issue in result.validation.issues] == [
        "PIH.CHECKPOINT.DECISION_UNKNOWN",
        "PIH.CHECKPOINT.STATE_CONTRADICTION",
    ]
    assert result.validation.issues[0].related_ids == ("a",)
    assert result.validation.issues[1].related_ids == (
        "authorized_scope",
        "human_response",
    )
    assert result.checkpoint is None and result.changed is False


def test_method__execute__identical_repetition_returns_unchanged_checkpoint() -> None:
    """Evidence ID
    SV-HARNESS-109
    Requirement
    Repeating an identical explicit resolution is a successful idempotent no-op.
    Method
    Resolve pending state, then execute the same decision values on its result.
    Oracle
    Exact checkpoint/request field equality fixes idempotent repetition.
    Acceptance
    First result is changed, second is PASS/unchanged and returns the existing object.
    Interpretation
    Failure indicates duplicate resolution or idempotency drift.
    Limitations
    No persistence or replay protocol is exercised.
    """
    request = make_resolution_request(make_checkpoint_for_resolution())
    first = SUT().execute(request)
    assert first.checkpoint is not None and first.changed is True
    repeated_request = make_resolution_request(first.checkpoint)
    second = SUT().execute(repeated_request)
    assert second.validation.status == "PASS"
    assert second.changed is False
    assert second.checkpoint is first.checkpoint


@pytest.mark.parametrize(
    ("overrides", "related_id"),
    [
        ({"human_response": "Different response."}, "human_response"),
        ({"normalized_decision": "B"}, "normalized_decision"),
        ({"resolved_at": "2026-08-04T00:02:00Z"}, "resolved_at"),
        ({"authorized_scope": "different scope"}, "authorized_scope"),
    ],
    ids=[
        "human_response_conflict",
        "decision_conflict",
        "timestamp_conflict",
        "authorized_scope_conflict",
    ],
)
def test_method__execute__resolved_field_conflict_returns_structured_failure(
    overrides: dict[str, str], related_id: str
) -> None:
    """Evidence ID
    SV-HARNESS-110
    Requirement
    Any differing explicit resolution field conflicts with already-resolved state.
    Method
    Change one response, decision, timestamp, or scope field per semantic partition.
    Oracle
    Exact field equality and the closed RESOLUTION_CONFLICT code are the oracle.
    Acceptance
    Each case returns the exact code/field and no checkpoint or changed result.
    Interpretation
    Failure indicates silent overwrite or conflict-classification drift.
    Limitations
    Multi-field conflicts are represented by the same sorted related-ID mechanism.
    """
    checkpoint = make_checkpoint_for_resolution(
        status="resolved",
        human_response="Approve A exactly.",
        normalized_decision="A",
        resolved_at="2026-08-04T00:01:02Z",
        authorized_scope="bounded implementation",
    )
    values: dict[str, Any] = {
        "checkpoint": checkpoint,
        "expected_status": "pending",
        "human_response": "Approve A exactly.",
        "normalized_decision": "A",
        "resolved_at": "2026-08-04T00:01:02Z",
        "authorized_scope": "bounded implementation",
    }
    values.update(overrides)
    result = SUT().execute(make_resolution_request(**values))
    assert [issue.code for issue in result.validation.issues] == [
        "PIH.CHECKPOINT.RESOLUTION_CONFLICT"
    ]
    assert result.validation.issues[0].related_ids == (related_id,)
    assert result.checkpoint is None and result.changed is False


def test_method__execute__unexpected_status_returns_status_conflict() -> None:
    """Evidence ID
    SV-HARNESS-111
    Requirement
    Current status outside both explicit request statuses fails deterministically.
    Method
    Execute a pending-to-resolved request against a cancelled checkpoint.
    Oracle
    Exact status comparison and STATUS_CONFLICT define the partition.
    Acceptance
    The singleton issue identifies all sorted statuses and no checkpoint is returned.
    Interpretation
    Failure indicates implicit lifecycle choice or status-conflict drift.
    Limitations
    Profile-relative lifecycle validity remains ValidateCheckpointSet's concern.
    """
    checkpoint = make_checkpoint_for_resolution(status="cancelled")
    result = SUT().execute(make_resolution_request(checkpoint))
    assert [issue.code for issue in result.validation.issues] == [
        "PIH.CHECKPOINT.STATUS_CONFLICT"
    ]
    assert result.validation.issues[0].related_ids == (
        "cancelled",
        "pending",
        "resolved",
    )
    assert result.checkpoint is None and result.changed is False


def test_method__execute__uses_only_explicit_state_without_operational_effects(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Evidence ID
    SV-HARNESS-112
    Requirement
    Transformation has no task, chain, filesystem, clock, Git, resumption, or
    successor effect and depends only on explicit request state.
    Method
    Execute twice from an unrelated empty CWD, snapshot directory state, and inspect
    preserved task/resumption fields and deterministic equality.
    Oracle
    Empty-directory state, explicit timestamp, exact result equality, and preserved
    fields provide independent observable oracles.
    Acceptance
    Results are equal, directory remains empty, explicit timestamp is used, and task
    and resumption fields are unchanged.
    Interpretation
    Failure indicates ambient input, nondeterminism, write, or lifecycle side effect.
    Limitations
    This behavioral check does not invoke Git, a clock API, or successor machinery.
    """
    elsewhere = tmp_path / "unrelated-cwd"
    elsewhere.mkdir()
    checkpoint = make_checkpoint_for_resolution()
    request = make_resolution_request(checkpoint)
    monkeypatch.chdir(elsewhere)
    before = tuple(elsewhere.iterdir())
    first = SUT().execute(request)
    second = SUT().execute(request)
    assert first == second
    assert tuple(elsewhere.iterdir()) == before == ()
    assert first.checkpoint is not None
    assert first.checkpoint.resolved_at == request.resolved_at
    assert first.checkpoint.task_id == checkpoint.task_id
    assert first.checkpoint.resumption_status == checkpoint.resumption_status
