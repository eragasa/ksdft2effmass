r"""Software verification of ``TaskWorkflowTransitionRecord``.

Evidence profile: routine

Bounded artifact scope: the public ``TaskWorkflowTransitionRecord`` contract.

Facet and represented meaning

This module verifies the exact public structure owned by
``TaskWorkflowTransitionRecord``.

Intrinsic and cross-object scope

The evidence is limited to the class-owned field, member, or constructor contract.
Cross-record replay and package-export agreement remain with their owning evidence.

VVUQ and scientific exclusions

This is software verification only. It establishes no execution, persistence,
scientific validation, uncertainty quantification, authority, or human acceptance.
"""

from dataclasses import fields

import pytest

from ksdft2effmass.workflows.runs import TaskWorkflowTransitionRecord

pytestmark = pytest.mark.software_verification
SUT = TaskWorkflowTransitionRecord


class TestTaskWorkflowTransitionRecord:
    """Own software evidence for ``TaskWorkflowTransitionRecord``."""

    def test_fields__public_contract__matches_exact_inventory(self) -> None:
        """Expose the exact documented immutable field inventory.

        Evidence ID: SV-WFR-TASK-WORKFLOW-TRANSITION-RECORD-001

        Requirement: ``TaskWorkflowTransitionRecord`` declares exactly its
        documented public DataObject
        or ResultObject fields in constructor order.

        Acceptance: :func:`dataclasses.fields` returns the exact field-name tuple.
        """
        assert tuple(field.name for field in fields(SUT)) == (
            "identity",
            "sequence_identity",
            "sequence_index",
            "workflow_identity",
            "workflow_run_identity",
            "definition_reference_identity",
            "runtime_bundle_identity",
            "activation_identity",
            "operation_identity",
            "attempt_identity",
            "terminal_attempt_record_identity",
            "outcome_identity",
            "result_production_identities",
            "firing_result",
            "request_correlation_identity",
            "dispatch_outcome_record_identity",
        )
