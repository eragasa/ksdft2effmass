r"""Software verification of ``WorkflowDefinitionReference``.

Evidence profile: routine

Bounded artifact scope: the public ``WorkflowDefinitionReference`` contract.

Facet and represented meaning

This module verifies intrinsic represented behavior owned by
``WorkflowDefinitionReference``.

Intrinsic and cross-object scope

Constructor and field invariants belong to this class. Complete cross-record replay
and package-export agreement remain with their separate owners.

VVUQ and scientific exclusions

This is software verification only. It establishes no execution, persistence,
scientific validation, uncertainty quantification, authority, or human acceptance.
"""

from dataclasses import fields, replace

import pytest

from ksdft2effmass.petrinet.colored import (
    ColoredPetriNetDefinitionIdentity,
)
from ksdft2effmass.workflows import (
    TaskDefinitionIdentity,
    WorkflowIdentity,
)
from ksdft2effmass.workflows.runs import (
    WorkflowDefinitionReference,
    WorkflowDefinitionReferenceIdentity,
)

pytestmark = pytest.mark.software_verification
SUT = WorkflowDefinitionReference


class TestWorkflowDefinitionReference:
    """Own software evidence for ``WorkflowDefinitionReference``."""

    def test_fields__public_contract__matches_exact_inventory(self) -> None:
        """Expose the exact documented immutable field inventory.

        Evidence ID: SV-WFR-WORKFLOW-DEFINITION-REFERENCE-001

        Requirement: ``WorkflowDefinitionReference`` declares exactly its
        documented public DataObject
        or ResultObject fields in constructor order.

        Acceptance: :func:`dataclasses.fields` returns the exact field-name tuple.
        """
        assert tuple(field.name for field in fields(SUT)) == (
            "identity",
            "workflow_identity",
            "workflow_definition_version",
            "colored_petri_net_definition_identity",
            "colored_petri_net_definition_version",
            "task_definition_identities",
            "schema_version",
        )

    def test_constructor__workflow_definition_reference__binds_exact_versions(
        self,
    ) -> None:
        """Bind Workflow, CPN, Task-definition, and schema versions explicitly.

        Evidence ID: SV-WFR-RECORDS-007

        Requirement: Replay input names one immutable definition reference with exact
        positive built-in integer versions and canonical Task-definition identities.

        Acceptance: The exact reference constructs and Boolean Workflow version raises
        ``TypeError``.
        """
        reference = WorkflowDefinitionReference(
            identity=WorkflowDefinitionReferenceIdentity("definition-reference.one"),
            workflow_identity=WorkflowIdentity("workflow.one"),
            workflow_definition_version=1,
            colored_petri_net_definition_identity=ColoredPetriNetDefinitionIdentity(
                "definition.one"
            ),
            colored_petri_net_definition_version=1,
            task_definition_identities=(TaskDefinitionIdentity("task.one"),),
            schema_version=1,
        )

        assert reference.workflow_definition_version == 1
        with pytest.raises(TypeError):
            replace(reference, workflow_definition_version=True)
