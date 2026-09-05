r"""Software verification of ``ScientificDecisionWorkflowTransitionRecord``.

Evidence profile: routine

Bounded artifact scope: the public ``ScientificDecisionWorkflowTransitionRecord``
contract.

Facet and represented meaning

This module verifies the exact public structure owned by
``ScientificDecisionWorkflowTransitionRecord``.

Intrinsic and cross-object scope

The evidence is limited to the class-owned field, member, or constructor contract.
Cross-record replay and package-export agreement remain with their owning evidence.

VVUQ and scientific exclusions

This is software verification only. It establishes no execution, persistence,
scientific validation, uncertainty quantification, authority, or human acceptance.
"""

from dataclasses import fields

import pytest

from ksdft2effmass.workflows.runs import ScientificDecisionWorkflowTransitionRecord

pytestmark = pytest.mark.software_verification
SUT = ScientificDecisionWorkflowTransitionRecord


class TestScientificDecisionWorkflowTransitionRecord:
    """Own software evidence for ``ScientificDecisionWorkflowTransitionRecord``."""

    def test_fields__public_contract__matches_exact_inventory(self) -> None:
        """Expose the exact documented immutable field inventory.

        Evidence ID: SV-WFR-SCIENTIFIC-DECISION-WORKFLOW-TRANSITION-RECORD-001

        Requirement: ``ScientificDecisionWorkflowTransitionRecord`` declares
        exactly its documented public DataObject
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
            "request_identity",
            "resolution_identity",
            "producer_provenance_identity",
            "firing_result",
        )
