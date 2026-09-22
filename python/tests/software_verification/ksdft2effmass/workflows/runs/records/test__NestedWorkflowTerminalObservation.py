r"""Software verification of ``NestedWorkflowTerminalObservation``.

Evidence profile: claim_bearing

Bounded artifact scope: immutable terminal fields, typed intent links and variants.

Facet and represented meaning

A separate first-terminal observation carries only the evidence for its variant.

Intrinsic and cross-object scope

These cases verify intrinsic field validity, not predecessor intent existence,
terminal-attempt status, exact generic outcome closure or durable uniqueness.

VVUQ and scientific exclusions

Synthetic child revision and replay labels are not computed child replay evidence.
No persistence, effects, authority, numerical verification or science is claimed.
"""

from dataclasses import FrozenInstanceError, fields, replace
from typing import Literal

import pytest

from ksdft2effmass.workflows import (
    NestedWorkflowInvocationIdentity,
    NestedWorkflowInvocationIntentIdentity,
    NestedWorkflowInvocationKind,
    NestedWorkflowObservationIdentity,
    NestedWorkflowTerminalObservation,
    NestedWorkflowTerminalObservationKind,
    ResultDependencyIdentity,
    ResultObjectReferenceIdentity,
    TaskAttemptRecordIdentity,
    TaskFailureRecordIdentity,
    TaskInvocationOutcomeIdentity,
    WorkflowRunIdentity,
    WorkflowRunReplayResultIdentity,
    WorkflowRunRevisionIdentity,
)

pytestmark = pytest.mark.software_verification
SUT = NestedWorkflowTerminalObservation

type ObservationField = Literal[
    "identity",
    "intent_identity",
    "parent_workflow_run_identity",
    "parent_revision_identity",
    "terminal_attempt_record_identity",
    "outcome_identity",
    "kind",
    "terminal_child_revision_identity",
    "replay_equal_child_result_identity",
    "exported_result_reference_identities",
    "export_admission_dependency_identities",
    "failure_record_identity",
    "reconciliation_identity_values",
]
type ObservationValue = (
    None
    | str
    | bool
    | NestedWorkflowInvocationKind
    | NestedWorkflowTerminalObservationKind
    | NestedWorkflowObservationIdentity
    | WorkflowRunRevisionIdentity
    | WorkflowRunReplayResultIdentity
    | TaskFailureRecordIdentity
    | tuple[ResultObjectReferenceIdentity, ...]
    | tuple[ResultDependencyIdentity, ...]
    | tuple[str, ...]
    | tuple[int, ...]
    | list[str]
)


class TestNestedWorkflowTerminalObservation:
    """Own intrinsic first-terminal observation evidence."""

    def test_field__public_inventory__matches_exact_names(self) -> None:
        """Keep stable child intent fields out of the terminal observation.

        Evidence ID: SV-WFR-NESTED-TERMINAL-001

        Requirement: The observation declares exactly its thirteen approved fields.

        Method: Inspect the public dataclass field sequence.

        Oracle: The independently enumerated terminal observation contract.

        Acceptance: Exact field-name tuple equality.

        Interpretation: Intent is linked, not copied into changing state records.

        Limitations: No record linkage or persistence is established.
        """
        assert tuple(field.name for field in fields(SUT)) == (
            "identity",
            "intent_identity",
            "parent_workflow_run_identity",
            "parent_revision_identity",
            "terminal_attempt_record_identity",
            "outcome_identity",
            "kind",
            "terminal_child_revision_identity",
            "replay_equal_child_result_identity",
            "exported_result_reference_identities",
            "export_admission_dependency_identities",
            "failure_record_identity",
            "reconciliation_identity_values",
        )

    def test_constructor__confirmed__retains_paired_exports(self) -> None:
        """Retain explicit confirmed child evidence and positional admissions.

        Evidence ID: SV-WFR-NESTED-TERMINAL-002

        Requirement: Confirmed retains child revision/replay labels and nonempty
        lexical exports paired with equal-length lexical admissions.

        Method: Construct a literal two-export observation.

        Oracle: Independent child labels and ordered export/admission pairs.

        Acceptance: The exact labels and pairs are retained without failure or
        reconciliation fields.

        Interpretation: Confirmed evidence is represented, not recomputed.

        Limitations: No child read, replay equality or admission closure is proven.
        """
        observation = self.make_confirmed()
        assert observation.kind is NestedWorkflowTerminalObservationKind.CONFIRMED
        assert (
            observation.terminal_child_revision_identity
            == WorkflowRunRevisionIdentity("child.terminal")
        )
        assert (
            observation.replay_equal_child_result_identity
            == WorkflowRunReplayResultIdentity("c" * 64)
        )
        assert tuple(
            zip(
                observation.exported_result_reference_identities,
                observation.export_admission_dependency_identities,
                strict=True,
            )
        ) == (
            (
                ResultObjectReferenceIdentity("export.a"),
                ResultDependencyIdentity("admission.b"),
            ),
            (
                ResultObjectReferenceIdentity("export.z"),
                ResultDependencyIdentity("admission.y"),
            ),
        )
        assert observation.failure_record_identity is None
        assert observation.reconciliation_identity_values == ()

    @pytest.mark.parametrize(
        "kind,failure,reconciliations",
        (
            pytest.param(
                NestedWorkflowTerminalObservationKind.REJECTED,
                TaskFailureRecordIdentity("failure"),
                (),
                id="rejected_failure",
            ),
            pytest.param(
                NestedWorkflowTerminalObservationKind.INDETERMINATE,
                None,
                ("child.read", "external.query"),
                id="indeterminate_reconciliation",
            ),
        ),
    )
    def test_constructor__nonconfirmed__retains_only_own_evidence(
        self,
        kind: NestedWorkflowTerminalObservationKind,
        failure: TaskFailureRecordIdentity | None,
        reconciliations: tuple[str, ...],
    ) -> None:
        """Represent nonconfirmed evidence without terminal child claims.

        Evidence ID: SV-WFR-NESTED-TERMINAL-003

        Requirement: Rejected carries failure only; indeterminate carries
        reconciliation only; both omit child terminal labels and exports.

        Method: Construct from the two explicit variant partitions.

        Oracle: The supplied failure/reconciliation fields and empty defaults.

        Acceptance: Exact values retained; child revision/replay and exports absent.

        Interpretation: Nonconfirmed evidence cannot imply confirmed child exports.

        Limitations: Failure and reconciliation labels are synthetic, not resolved.
        """
        observation = SUT(
            identity=NestedWorkflowObservationIdentity("observation"),
            intent_identity=NestedWorkflowInvocationIntentIdentity("intent"),
            parent_workflow_run_identity=WorkflowRunIdentity("parent"),
            parent_revision_identity=WorkflowRunRevisionIdentity("terminal"),
            terminal_attempt_record_identity=TaskAttemptRecordIdentity(
                "terminal.attempt"
            ),
            outcome_identity=TaskInvocationOutcomeIdentity("outcome"),
            kind=kind,
            failure_record_identity=failure,
            reconciliation_identity_values=reconciliations,
        )
        assert observation.kind is kind
        assert observation.failure_record_identity == failure
        assert observation.reconciliation_identity_values == reconciliations
        assert observation.terminal_child_revision_identity is None
        assert observation.replay_equal_child_result_identity is None
        assert observation.exported_result_reference_identities == ()
        assert observation.export_admission_dependency_identities == ()

    def test_field__intent_reference__preserves_nominal_alternative(self) -> None:
        """Retain same-string references to two distinct source types.

        Evidence ID: SV-WFR-NESTED-TERMINAL-004

        Requirement: The intent link is a closed union, not a bare string key.

        Method: Reconstruct the observation with a same-string combined identity.

        Oracle: Nominal dataclass equality and exact public field types.

        Acceptance: Both references construct, retain their type and compare unequal.

        Interpretation: A combined pending source is not fabricated as a new intent.

        Limitations: The combined source's actual pending state is not resolved here.
        """
        separate = self.make_confirmed()
        combined = replace(
            separate, intent_identity=NestedWorkflowInvocationIdentity("intent")
        )
        assert type(separate.intent_identity) is NestedWorkflowInvocationIntentIdentity
        assert type(combined.intent_identity) is NestedWorkflowInvocationIdentity
        assert separate.intent_identity.value == combined.intent_identity.value
        assert separate != combined

    @pytest.mark.parametrize(
        "field,value",
        (
            pytest.param("identity", "observation", id="observation_string"),
            pytest.param("intent_identity", "intent", id="intent_string"),
            pytest.param(
                "intent_identity",
                NestedWorkflowObservationIdentity("intent"),
                id="wrong_nominal_intent",
            ),
            pytest.param(
                "parent_workflow_run_identity", "parent", id="parent_run_string"
            ),
            pytest.param(
                "parent_revision_identity", "revision", id="parent_revision_string"
            ),
            pytest.param(
                "terminal_attempt_record_identity",
                "attempt",
                id="terminal_attempt_string",
            ),
            pytest.param("outcome_identity", "outcome", id="outcome_string"),
            pytest.param("kind", "confirmed", id="kind_string"),
            pytest.param(
                "kind", NestedWorkflowInvocationKind.CONFIRMED, id="combined_kind_enum"
            ),
            pytest.param(
                "kind", NestedWorkflowInvocationKind.PENDING, id="pending_kind_enum"
            ),
            pytest.param(
                "terminal_child_revision_identity",
                "revision",
                id="child_revision_string",
            ),
            pytest.param(
                "replay_equal_child_result_identity", "c" * 64, id="replay_string"
            ),
            pytest.param("failure_record_identity", "failure", id="failure_string"),
            pytest.param(
                "exported_result_reference_identities",
                (ResultDependencyIdentity("wrong"),),
                id="export_wrong_nominal",
            ),
            pytest.param(
                "export_admission_dependency_identities",
                (ResultObjectReferenceIdentity("wrong"),),
                id="admission_wrong_nominal",
            ),
            pytest.param(
                "exported_result_reference_identities", ["export"], id="mutable_exports"
            ),
            pytest.param(
                "export_admission_dependency_identities",
                ["admission"],
                id="mutable_admissions",
            ),
            pytest.param(
                "reconciliation_identity_values", ["query"], id="mutable_reconciliation"
            ),
            pytest.param(
                "reconciliation_identity_values", (1,), id="non_string_reconciliation"
            ),
            pytest.param(
                "reconciliation_identity_values", True, id="boolean_reconciliation"
            ),
        ),
    )
    def test_constructor__semantic_types__rejects_wrong_fields(
        self, field: ObservationField, value: ObservationValue
    ) -> None:
        """Reject exact-type violations before variant validation.

        Evidence ID: SV-WFR-NESTED-TERMINAL-005

        Requirement: All fields retain their exact semantic types.

        Method: Reconstruct through dataclasses.replace with a single closed
        field/value substitution, invoking the public constructor.

        Oracle: TypeError naming the invalid field.

        Acceptance: Every substitution raises the specified TypeError.

        Interpretation: No string coercion, nominal erasure or mutable tuple enters.

        Limitations: Explicit partitions are not exhaustive Python-type coverage.
        """
        with pytest.raises(TypeError, match=field):
            replace(self.make_confirmed(), **{field: value})  # type: ignore[arg-type]

    @pytest.mark.parametrize(
        "field,value",
        (
            pytest.param(
                "terminal_child_revision_identity", None, id="missing_child_revision"
            ),
            pytest.param(
                "replay_equal_child_result_identity", None, id="missing_child_replay"
            ),
            pytest.param(
                "exported_result_reference_identities", (), id="missing_exports"
            ),
            pytest.param(
                "export_admission_dependency_identities", (), id="missing_admissions"
            ),
            pytest.param(
                "export_admission_dependency_identities",
                (ResultDependencyIdentity("admission.b"),),
                id="unpaired_admission",
            ),
            pytest.param(
                "failure_record_identity",
                TaskFailureRecordIdentity("failure"),
                id="prohibited_failure",
            ),
            pytest.param(
                "reconciliation_identity_values",
                ("query",),
                id="prohibited_reconciliation",
            ),
        ),
    )
    def test_constructor__confirmed__rejects_incomplete_or_foreign_evidence(
        self, field: ObservationField, value: ObservationValue
    ) -> None:
        """Reject incomplete confirmed evidence and foreign variant fields.

        Evidence ID: SV-WFR-NESTED-TERMINAL-006

        Requirement: Confirmed has complete paired child evidence and nothing else.

        Method: Change one field in an independently constructed confirmed record.

        Oracle: The selected closed confirmed-variant contract.

        Acceptance: Each substitution raises ValueError for the terminal variant.

        Interpretation: Missing evidence is not accepted as a confirmed observation.

        Limitations: Presence of labels does not establish their authenticity.
        """
        with pytest.raises(ValueError, match="terminal variant"):
            replace(self.make_confirmed(), **{field: value})  # type: ignore[arg-type]

    @pytest.mark.parametrize(
        "field,value",
        (
            pytest.param(
                "exported_result_reference_identities",
                (
                    ResultObjectReferenceIdentity("z"),
                    ResultObjectReferenceIdentity("a"),
                ),
                id="reversed_exports",
            ),
            pytest.param(
                "exported_result_reference_identities",
                (
                    ResultObjectReferenceIdentity("a"),
                    ResultObjectReferenceIdentity("a"),
                ),
                id="duplicate_exports",
            ),
            pytest.param(
                "export_admission_dependency_identities",
                (ResultDependencyIdentity("z"), ResultDependencyIdentity("a")),
                id="reversed_admissions",
            ),
            pytest.param(
                "export_admission_dependency_identities",
                (ResultDependencyIdentity("a"), ResultDependencyIdentity("a")),
                id="duplicate_admissions",
            ),
            pytest.param(
                "reconciliation_identity_values", ("",), id="empty_reconciliation_label"
            ),
            pytest.param(
                "reconciliation_identity_values",
                ("z", "a"),
                id="reversed_reconciliation",
            ),
            pytest.param(
                "reconciliation_identity_values",
                ("a", "a"),
                id="duplicate_reconciliation",
            ),
        ),
    )
    def test_constructor__tuple_values__rejects_noncanonical_order(
        self, field: ObservationField, value: ObservationValue
    ) -> None:
        """Reject tuple value violations without sorting or normalization.

        Evidence ID: SV-WFR-NESTED-TERMINAL-007

        Requirement: Identity tuples are lexical and unique; reconciliation
        strings are additionally nonempty.

        Method: Substitute one explicitly noncanonical tuple.

        Oracle: Intrinsic ordering, uniqueness and nonempty-label invariants.

        Acceptance: ValueError reports the tuple invariant, not the variant check.

        Interpretation: Positional pairings cannot be silently changed by sorting.

        Limitations: No cross-object admission or reference matching is checked.
        """
        with pytest.raises(ValueError, match="sorted|must not be empty"):
            replace(self.make_confirmed(), **{field: value})  # type: ignore[arg-type]

    @pytest.mark.parametrize(
        "kind,field,value",
        (
            pytest.param(
                NestedWorkflowTerminalObservationKind.REJECTED,
                "failure_record_identity",
                None,
                id="rejected_missing_failure",
            ),
            pytest.param(
                NestedWorkflowTerminalObservationKind.REJECTED,
                "terminal_child_revision_identity",
                WorkflowRunRevisionIdentity("child"),
                id="rejected_child_revision",
            ),
            pytest.param(
                NestedWorkflowTerminalObservationKind.REJECTED,
                "replay_equal_child_result_identity",
                WorkflowRunReplayResultIdentity("c" * 64),
                id="rejected_child_replay",
            ),
            pytest.param(
                NestedWorkflowTerminalObservationKind.REJECTED,
                "exported_result_reference_identities",
                (ResultObjectReferenceIdentity("export"),),
                id="rejected_exports",
            ),
            pytest.param(
                NestedWorkflowTerminalObservationKind.REJECTED,
                "export_admission_dependency_identities",
                (ResultDependencyIdentity("admission"),),
                id="rejected_admissions",
            ),
            pytest.param(
                NestedWorkflowTerminalObservationKind.REJECTED,
                "reconciliation_identity_values",
                ("query",),
                id="rejected_reconciliation",
            ),
            pytest.param(
                NestedWorkflowTerminalObservationKind.INDETERMINATE,
                "reconciliation_identity_values",
                (),
                id="indeterminate_missing_reconciliation",
            ),
            pytest.param(
                NestedWorkflowTerminalObservationKind.INDETERMINATE,
                "failure_record_identity",
                TaskFailureRecordIdentity("failure"),
                id="indeterminate_failure",
            ),
            pytest.param(
                NestedWorkflowTerminalObservationKind.INDETERMINATE,
                "terminal_child_revision_identity",
                WorkflowRunRevisionIdentity("child"),
                id="indeterminate_child_revision",
            ),
            pytest.param(
                NestedWorkflowTerminalObservationKind.INDETERMINATE,
                "replay_equal_child_result_identity",
                WorkflowRunReplayResultIdentity("c" * 64),
                id="indeterminate_child_replay",
            ),
            pytest.param(
                NestedWorkflowTerminalObservationKind.INDETERMINATE,
                "exported_result_reference_identities",
                (ResultObjectReferenceIdentity("export"),),
                id="indeterminate_exports",
            ),
            pytest.param(
                NestedWorkflowTerminalObservationKind.INDETERMINATE,
                "export_admission_dependency_identities",
                (ResultDependencyIdentity("admission"),),
                id="indeterminate_admissions",
            ),
        ),
    )
    def test_constructor__nonconfirmed__rejects_missing_or_foreign_evidence(
        self,
        kind: NestedWorkflowTerminalObservationKind,
        field: ObservationField,
        value: ObservationValue,
    ) -> None:
        """Keep rejected and indeterminate evidence disjoint.

        Evidence ID: SV-WFR-NESTED-TERMINAL-008

        Requirement: Each nonconfirmed variant has exactly its own evidence.

        Method: Reconstruct a valid nonconfirmed record, then substitute one
        prohibited or missing field through the dataclass constructor entry point.

        Oracle: The explicit rejected/indeterminate contract partitions.

        Acceptance: Each substitution raises ValueError for the terminal variant.

        Interpretation: Variant fields cannot leak into another terminal kind.

        Limitations: No subsequent reconciliation lifecycle is implemented here.
        """
        base = replace(
            self.make_confirmed(),
            kind=kind,
            terminal_child_revision_identity=None,
            replay_equal_child_result_identity=None,
            exported_result_reference_identities=(),
            export_admission_dependency_identities=(),
            failure_record_identity=(
                TaskFailureRecordIdentity("failure")
                if kind is NestedWorkflowTerminalObservationKind.REJECTED
                else None
            ),
            reconciliation_identity_values=(
                ("query",)
                if kind is NestedWorkflowTerminalObservationKind.INDETERMINATE
                else ()
            ),
        )
        with pytest.raises(ValueError, match="terminal variant"):
            replace(base, **{field: value})  # type: ignore[arg-type]

    def test_field__terminal_attempt__is_frozen(self) -> None:
        """Reject ordinary rewriting of terminal evidence.

        Evidence ID: SV-WFR-NESTED-TERMINAL-009

        Requirement: The terminal observation is frozen.

        Method: Assign a different terminal attempt through its public field.

        Oracle: Frozen dataclass assignment semantics.

        Acceptance: FrozenInstanceError and unchanged terminal attempt identity.

        Interpretation: Ordinary public mutation cannot rewrite the observation.

        Limitations: Deliberate Python runtime bypasses are excluded.
        """
        observation = self.make_confirmed()
        changed = TaskAttemptRecordIdentity("changed")
        with pytest.raises(FrozenInstanceError):
            observation.terminal_attempt_record_identity = changed  # type: ignore[misc]
        assert (
            observation.terminal_attempt_record_identity
            == TaskAttemptRecordIdentity("terminal.attempt")
        )

    def test_constructor__confirmed_exports__rejects_empty_pair(self) -> None:
        """Require actual exports even when empty tuples have equal lengths.

        Evidence ID: SV-WFR-NESTED-TERMINAL-010

        Requirement: Confirmed exports are nonempty, independently of equal-length
        admission pairing.

        Method: Clear both tuples on an otherwise valid confirmed observation.

        Oracle: The existing nonempty-confirmed-export contract.

        Acceptance: ValueError reports the terminal variant.

        Interpretation: Equal tuple lengths alone do not establish valid exports.

        Limitations: Export content and child provenance remain cross-object checks.
        """
        with pytest.raises(ValueError, match="terminal variant"):
            replace(
                self.make_confirmed(),
                exported_result_reference_identities=(),
                export_admission_dependency_identities=(),
            )

    @staticmethod
    def make_confirmed() -> NestedWorkflowTerminalObservation:
        """Supply one synthetic confirmed graph with independent ordered labels."""
        return SUT(
            identity=NestedWorkflowObservationIdentity("observation"),
            intent_identity=NestedWorkflowInvocationIntentIdentity("intent"),
            parent_workflow_run_identity=WorkflowRunIdentity("parent"),
            parent_revision_identity=WorkflowRunRevisionIdentity("terminal"),
            terminal_attempt_record_identity=TaskAttemptRecordIdentity(
                "terminal.attempt"
            ),
            outcome_identity=TaskInvocationOutcomeIdentity("outcome"),
            kind=NestedWorkflowTerminalObservationKind.CONFIRMED,
            terminal_child_revision_identity=WorkflowRunRevisionIdentity(
                "child.terminal"
            ),
            replay_equal_child_result_identity=WorkflowRunReplayResultIdentity(
                "c" * 64
            ),
            exported_result_reference_identities=(
                ResultObjectReferenceIdentity("export.a"),
                ResultObjectReferenceIdentity("export.z"),
            ),
            export_admission_dependency_identities=(
                ResultDependencyIdentity("admission.b"),
                ResultDependencyIdentity("admission.y"),
            ),
        )
