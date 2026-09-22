r"""Software verification of ``ScientificDecisionRequest``.

Evidence profile: routine

Bounded artifact scope: the public ``ScientificDecisionRequest`` contract.

Facet and represented meaning

This module verifies intrinsic represented behavior owned by
``ScientificDecisionRequest``.

Intrinsic and cross-object scope

Constructor and field invariants belong to this class. Complete cross-record replay
and package-export agreement remain with their separate owners.

VVUQ and scientific exclusions

This is software verification only. It establishes no execution, persistence,
scientific validation, uncertainty quantification, authority, or human acceptance.
"""

from dataclasses import fields, replace

import pytest

from ksdft2effmass.petrinet.colored import ColoredPetriNetTransitionIdentity
from ksdft2effmass.workflows import (
    TaskInstanceIdentity,
    WorkflowIdentity,
    WorkflowRunIdentity,
)
from ksdft2effmass.workflows.runs import (
    AuthorityContextIdentity,
    ResponseSourceIdentity,
    ScientificDecisionOption,
    ScientificDecisionOptionIdentity,
    ScientificDecisionRequest,
    ScientificDecisionRequestIdentity,
)

pytestmark = pytest.mark.software_verification
SUT = ScientificDecisionRequest


class TestScientificDecisionRequest:
    """Own software evidence for ``ScientificDecisionRequest``."""

    def test_fields__public_contract__matches_exact_inventory(self) -> None:
        """Expose the exact documented immutable field inventory.

        Evidence ID: SV-WFR-SCIENTIFIC-DECISION-REQUEST-001

        Requirement: ``ScientificDecisionRequest`` declares exactly its
        documented public DataObject
        or ResultObject fields in constructor order.

        Acceptance: :func:`dataclasses.fields` returns the exact field-name tuple.
        """
        assert tuple(field.name for field in fields(SUT)) == (
            "identity",
            "question",
            "options",
            "declared_scope",
            "workflow_identity",
            "workflow_run_identity",
            "affected_task_instance_identity",
            "affected_transition_identity",
            "required_response_source_identity",
            "required_authority_context_identity",
            "definition_identity",
            "definition_version",
        )

    def test_constructor__scientific_decision_request__requires_canonical_options(
        self,
    ) -> None:
        """Require exact canonical options and an exact positive definition version.

        Evidence ID: SV-WFR-CONTROL-005

        Requirement: A scientific-decision request retains one nonempty ordered option
        set and rejects booleans as integer versions.

        Acceptance: Canonical options construct; reversed options and Boolean version
        each raise their documented exception.
        """
        request = self.make_decision_request()

        assert tuple(option.identity.value for option in request.options) == (
            "option.a",
            "option.b",
        )
        with pytest.raises(ValueError):
            replace(request, options=tuple(reversed(request.options)))
        with pytest.raises(TypeError):
            replace(request, definition_version=True)

    @staticmethod
    def make_decision_request() -> ScientificDecisionRequest:
        """Construct one canonical synthetic scientific-decision request."""
        return ScientificDecisionRequest(
            identity=ScientificDecisionRequestIdentity("decision-request.one"),
            question="Select the represented synthetic branch.",
            options=(
                ScientificDecisionOption(
                    ScientificDecisionOptionIdentity("option.a"), "A"
                ),
                ScientificDecisionOption(
                    ScientificDecisionOptionIdentity("option.b"), "B"
                ),
            ),
            declared_scope="synthetic software-verification branch",
            workflow_identity=WorkflowIdentity("workflow.one"),
            workflow_run_identity=WorkflowRunIdentity("run.one"),
            affected_task_instance_identity=TaskInstanceIdentity("instance.one"),
            affected_transition_identity=ColoredPetriNetTransitionIdentity(
                "decision.ingress"
            ),
            required_response_source_identity=ResponseSourceIdentity("source.one"),
            required_authority_context_identity=AuthorityContextIdentity(
                "authority-context.one"
            ),
            definition_identity="scientific-decision-request.v1",
            definition_version=1,
        )
