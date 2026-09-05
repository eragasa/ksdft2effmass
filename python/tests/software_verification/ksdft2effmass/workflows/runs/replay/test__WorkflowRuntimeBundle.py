r"""Software verification of ``WorkflowRuntimeBundle``.

Evidence profile: routine

Bounded artifact scope: the public ``WorkflowRuntimeBundle`` contract.

Facet and represented meaning

This module verifies the exact public structure owned by ``WorkflowRuntimeBundle``.

Intrinsic and cross-object scope

The evidence is limited to the class-owned field, member, or constructor contract.
Cross-record replay and package-export agreement remain with their owning evidence.

VVUQ and scientific exclusions

This is software verification only. It establishes no execution, persistence,
scientific validation, uncertainty quantification, authority, or human acceptance.
"""

from dataclasses import fields

import pytest

from ksdft2effmass.workflows.runs import WorkflowRuntimeBundle

pytestmark = pytest.mark.software_verification
SUT = WorkflowRuntimeBundle


class TestWorkflowRuntimeBundle:
    """Own software evidence for ``WorkflowRuntimeBundle``."""

    def test_fields__public_contract__matches_exact_inventory(self) -> None:
        """Expose the exact documented immutable field inventory.

        Evidence ID: SV-WFR-WORKFLOW-RUNTIME-BUNDLE-001

        Requirement: ``WorkflowRuntimeBundle`` declares exactly its documented
        public DataObject
        or ResultObject fields in constructor order.

        Acceptance: :func:`dataclasses.fields` returns the exact field-name tuple.
        """
        assert tuple(field.name for field in fields(SUT)) == (
            "identity",
            "definition_reference",
            "schema_version",
            "workflow_identity",
            "definition",
            "task_definition_identities",
            "adapter_implementation_identity",
            "expression_evaluator_identity",
            "ordering_policy_identity",
            "transition_enabler_identity",
            "binding_selector_identity",
            "transition_firer_identity",
        )
