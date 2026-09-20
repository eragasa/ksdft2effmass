r"""Software verification of ``NestedWorkflowInvocationIntent``.

Evidence profile: claim_bearing

Bounded artifact scope: immutable intent fields and intrinsic correlations.

Facet and represented meaning

One intent retains its original STARTED record and contains no terminal state.

Intrinsic and cross-object scope

Exact types, distinct child and immutable input order are intrinsic. Cross-record
STARTED status, membership, introduction revision and source existence are excluded.

VVUQ and scientific exclusions

Synthetic identities establish no execution, stored history, replay or science.
"""

from dataclasses import FrozenInstanceError, fields, replace
from typing import Literal

import pytest

from ksdft2effmass.workflows import (
    AttemptIdentity,
    ChildWorkflowCreationIdempotencyIdentity,
    NestedWorkflowInvocationIdentity,
    NestedWorkflowInvocationIntent,
    NestedWorkflowInvocationIntentIdentity,
    OperationIdentity,
    ResultObjectReferenceIdentity,
    TaskActivationIdentity,
    TaskAttemptRecordIdentity,
    TaskInstanceIdentity,
    WorkflowIdentity,
    WorkflowRunIdentity,
    WorkflowRunRevisionIdentity,
)

pytestmark = pytest.mark.software_verification
SUT = NestedWorkflowInvocationIntent

type IntentField = Literal[
    "identity",
    "parent_workflow_run_identity",
    "parent_revision_identity",
    "parent_task_instance_identity",
    "activation_identity",
    "operation_identity",
    "attempt_identity",
    "started_attempt_record_identity",
    "child_workflow_identity",
    "child_workflow_run_identity",
    "input_result_reference_identities",
    "child_creation_idempotency_identity",
]
type WrongIntentValue = (
    str
    | bool
    | NestedWorkflowInvocationIdentity
    | tuple[str, ...]
    | list[ResultObjectReferenceIdentity]
)


class TestNestedWorkflowInvocationIntent:
    """Own the immutable intent record's intrinsic evidence."""

    def test_field__public_inventory__matches_exact_names(self) -> None:
        """Keep terminal evidence off the intent record.

        Evidence ID: SV-WFR-NESTED-INTENT-001

        Requirement: Intent declares exactly the twelve approved stable fields.

        Method: Inspect the public dataclass field sequence.

        Oracle: The independently listed intent contract, without status fields.

        Acceptance: Exact field-name tuple equality.

        Interpretation: Intent has no terminal state to rewrite.

        Limitations: Field inventory alone does not establish durable append behavior.
        """
        assert tuple(field.name for field in fields(SUT)) == (
            "identity",
            "parent_workflow_run_identity",
            "parent_revision_identity",
            "parent_task_instance_identity",
            "activation_identity",
            "operation_identity",
            "attempt_identity",
            "started_attempt_record_identity",
            "child_workflow_identity",
            "child_workflow_run_identity",
            "input_result_reference_identities",
            "child_creation_idempotency_identity",
        )

    @pytest.mark.parametrize(
        "inputs",
        (
            pytest.param((), id="empty_inputs"),
            pytest.param(
                (
                    ResultObjectReferenceIdentity("input.a"),
                    ResultObjectReferenceIdentity("input.z"),
                ),
                id="ordered_inputs",
            ),
        ),
    )
    def test_constructor__inputs__preserves_exact_tuple(
        self, inputs: tuple[ResultObjectReferenceIdentity, ...]
    ) -> None:
        """Retain exact typed input values without normalization.

        Evidence ID: SV-WFR-NESTED-INTENT-002

        Requirement: Empty or unique lexical input tuples are valid.

        Method: Reconstruct a valid intent with explicit input tuples.

        Oracle: Independently supplied ordered reference identities.

        Acceptance: Exact input tuple equality.

        Interpretation: Intent preserves the represented child inputs.

        Limitations: Referenced results and activation closure are not resolved.
        """
        intent = replace(self.make_intent(), input_result_reference_identities=inputs)
        assert intent.input_result_reference_identities == inputs

    @pytest.mark.parametrize(
        "field,value",
        (
            pytest.param(
                "identity",
                NestedWorkflowInvocationIdentity("intent"),
                id="combined_identity",
            ),
            pytest.param(
                "parent_workflow_run_identity", "parent", id="parent_run_string"
            ),
            pytest.param("parent_revision_identity", "revision", id="revision_string"),
            pytest.param("parent_task_instance_identity", "task", id="instance_string"),
            pytest.param("activation_identity", "activation", id="activation_string"),
            pytest.param("operation_identity", "operation", id="operation_string"),
            pytest.param("attempt_identity", "attempt", id="attempt_string"),
            pytest.param(
                "started_attempt_record_identity", "started", id="started_record_string"
            ),
            pytest.param(
                "child_workflow_identity", "workflow", id="child_workflow_string"
            ),
            pytest.param("child_workflow_run_identity", "child", id="child_run_string"),
            pytest.param(
                "child_creation_idempotency_identity", "key", id="creation_key_string"
            ),
            pytest.param(
                "input_result_reference_identities",
                [ResultObjectReferenceIdentity("input")],
                id="mutable_inputs",
            ),
            pytest.param(
                "input_result_reference_identities",
                ("input",),
                id="untyped_input_member",
            ),
            pytest.param(
                "input_result_reference_identities", True, id="boolean_inputs"
            ),
        ),
    )
    def test_constructor__semantic_types__rejects_wrong_fields(
        self, field: IntentField, value: WrongIntentValue
    ) -> None:
        """Enforce exact nominal and immutable collection types.

        Evidence ID: SV-WFR-NESTED-INTENT-003

        Requirement: Every field retains its declared exact semantic type.

        Method: Use the public dataclass reconstruction entry point with one
        closed field/value substitution; replace invokes the constructor.

        Oracle: TypeError for the named field, not an incidental attribute error.

        Acceptance: Each case raises TypeError naming that field.

        Interpretation: Wrong runtime types cannot enter a new intent.

        Limitations: Bounded representatives do not exhaust all Python objects.
        """
        with pytest.raises(TypeError, match=field):
            replace(self.make_intent(), **{field: value})  # type: ignore[arg-type]

    @pytest.mark.parametrize(
        "inputs",
        (
            pytest.param(
                (
                    ResultObjectReferenceIdentity("b"),
                    ResultObjectReferenceIdentity("a"),
                ),
                id="reversed_inputs",
            ),
            pytest.param(
                (
                    ResultObjectReferenceIdentity("a"),
                    ResultObjectReferenceIdentity("a"),
                ),
                id="duplicate_inputs",
            ),
        ),
    )
    def test_constructor__input_order__rejects_noncanonical_tuple(
        self, inputs: tuple[ResultObjectReferenceIdentity, ...]
    ) -> None:
        """Reject bad order rather than changing the represented inputs.

        Evidence ID: SV-WFR-NESTED-INTENT-004

        Requirement: Inputs are unique in lexical identity order.

        Method: Substitute reversed or duplicate nominal reference tuples.

        Oracle: The declared order and uniqueness invariant.

        Acceptance: ValueError reports noncanonical inputs.

        Interpretation: No hidden sorting or deduplication occurs.

        Limitations: Input identity/content agreement is a cross-object concern.
        """
        with pytest.raises(ValueError, match="unique and lexically sorted"):
            replace(self.make_intent(), input_result_reference_identities=inputs)

    def test_constructor__child__rejects_parent_run(self) -> None:
        """Exclude a self-child intent.

        Evidence ID: SV-WFR-NESTED-INTENT-005

        Requirement: The child run must be distinct from the parent.

        Method: Give the child the exact parent run identity.

        Oracle: The distinct-child invariant.

        Acceptance: ValueError is raised.

        Interpretation: An intent cannot identify its parent as its child.

        Limitations: No global cycle or multi-run graph analysis is claimed.
        """
        intent = self.make_intent()
        with pytest.raises(ValueError, match="distinct from its parent"):
            replace(
                intent, child_workflow_run_identity=intent.parent_workflow_run_identity
            )

    def test_field__started_record__is_frozen(self) -> None:
        """Retain the original attempt observation rather than terminal replacement.

        Evidence ID: SV-WFR-NESTED-INTENT-006

        Requirement: The STARTED record identity is immutable intent data.

        Method: Attempt public field reassignment to a terminal record identity.

        Oracle: Frozen dataclass assignment semantics.

        Acceptance: FrozenInstanceError and unchanged original STARTED label.

        Interpretation: Local mutation cannot turn intent into terminal evidence.

        Limitations: The label's actual STARTED status needs structural validation.
        """
        intent = self.make_intent()
        terminal = TaskAttemptRecordIdentity("terminal")
        with pytest.raises(FrozenInstanceError):
            intent.started_attempt_record_identity = terminal  # type: ignore[misc]
        assert intent.started_attempt_record_identity == TaskAttemptRecordIdentity(
            "started"
        )

    @staticmethod
    def make_intent() -> NestedWorkflowInvocationIntent:
        """Supply one independent synthetic stable-intent constructor graph."""
        return SUT(
            identity=NestedWorkflowInvocationIntentIdentity("intent"),
            parent_workflow_run_identity=WorkflowRunIdentity("parent"),
            parent_revision_identity=WorkflowRunRevisionIdentity("introduced"),
            parent_task_instance_identity=TaskInstanceIdentity("task"),
            activation_identity=TaskActivationIdentity("activation"),
            operation_identity=OperationIdentity("operation"),
            attempt_identity=AttemptIdentity("attempt"),
            started_attempt_record_identity=TaskAttemptRecordIdentity("started"),
            child_workflow_identity=WorkflowIdentity("child.workflow"),
            child_workflow_run_identity=WorkflowRunIdentity("child"),
            input_result_reference_identities=(),
            child_creation_idempotency_identity=ChildWorkflowCreationIdempotencyIdentity(
                "create"
            ),
        )
