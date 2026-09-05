r"""Software verification of ``WorkflowRunReplayIssueCode``.

Evidence profile: routine

Bounded artifact scope: the public ``WorkflowRunReplayIssueCode`` contract.

Facet and represented meaning

This module verifies the exact public structure owned by ``WorkflowRunReplayIssueCode``.

Intrinsic and cross-object scope

The evidence is limited to the class-owned field, member, or constructor contract.
Cross-record replay and package-export agreement remain with their owning evidence.

VVUQ and scientific exclusions

This is software verification only. It establishes no execution, persistence,
scientific validation, uncertainty quantification, authority, or human acceptance.
"""

import pytest

from ksdft2effmass.workflows.runs import WorkflowRunReplayIssueCode

pytestmark = pytest.mark.software_verification
SUT = WorkflowRunReplayIssueCode


class TestWorkflowRunReplayIssueCode:
    """Own software evidence for ``WorkflowRunReplayIssueCode``."""

    def test_fields__members__match_closed_contract(self) -> None:
        """Retain the exact closed member inventory.

        Evidence ID: SV-WFR-WORKFLOW-RUN-REPLAY-ISSUE-CODE-001

        Requirement: ``WorkflowRunReplayIssueCode`` exposes exactly its
        documented string-valued
        members in declaration order.

        Acceptance: Iteration returns the exact member-name and value tuple.
        """
        assert tuple((member.name, member.value) for member in SUT) == (
            ("RUNTIME_BUNDLE_MISMATCH", "runtime_bundle_mismatch"),
            ("SCHEMA_VERSION_MISMATCH", "schema_version_mismatch"),
            ("WORKFLOW_IDENTITY_MISMATCH", "workflow_identity_mismatch"),
            ("DEFINITION_IDENTITY_MISMATCH", "definition_identity_mismatch"),
            ("TASK_DEFINITION_MISMATCH", "task_definition_mismatch"),
            ("IMPLEMENTATION_IDENTITY_MISMATCH", "implementation_identity_mismatch"),
            ("ACTIVATION_CORRELATION_ERROR", "activation_correlation_error"),
            ("ATTEMPT_CORRELATION_ERROR", "attempt_correlation_error"),
            ("OUTCOME_CORRELATION_ERROR", "outcome_correlation_error"),
            ("RESULT_CORRELATION_ERROR", "result_correlation_error"),
            ("DEPENDENCY_CORRELATION_ERROR", "dependency_correlation_error"),
            ("FAILURE_CORRELATION_ERROR", "failure_correlation_error"),
            ("MEMBERSHIP_CORRELATION_ERROR", "membership_correlation_error"),
            ("NESTED_WORKFLOW_CORRELATION_ERROR", "nested_workflow_correlation_error"),
            (
                "NESTED_WORKFLOW_EXPORT_CORRELATION_ERROR",
                "nested_workflow_export_correlation_error",
            ),
            ("CONTROL_STATE_CORRELATION_ERROR", "control_state_correlation_error"),
            (
                "SCIENTIFIC_DECISION_CORRELATION_ERROR",
                "scientific_decision_correlation_error",
            ),
            ("NONCANONICAL_TRANSITION_ORDER", "noncanonical_transition_order"),
            ("PREDECESSOR_MARKING_MISMATCH", "predecessor_marking_mismatch"),
            ("FIRING_REPLAY_FAILED", "firing_replay_failed"),
            ("FIRING_RESULT_MISMATCH", "firing_result_mismatch"),
            ("CURRENT_MARKING_UNEQUAL", "current_marking_unequal"),
        )
