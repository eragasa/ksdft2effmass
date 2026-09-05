r"""Software verification of ``RepresentedScientificDecisionIngressProducer``.

Evidence profile: routine

Bounded artifact scope: the public ``RepresentedScientificDecisionIngressProducer``
contract.

Facet and represented meaning

This module verifies the exact public structure owned by
``RepresentedScientificDecisionIngressProducer``.

Intrinsic and cross-object scope

The evidence is limited to the class-owned field, member, or constructor contract.
Cross-record replay and package-export agreement remain with their owning evidence.

VVUQ and scientific exclusions

This is software verification only. It establishes no execution, persistence,
scientific validation, uncertainty quantification, authority, or human acceptance.
"""

from dataclasses import fields

import pytest

from ksdft2effmass.workflows.runs import RepresentedScientificDecisionIngressProducer

pytestmark = pytest.mark.software_verification
SUT = RepresentedScientificDecisionIngressProducer


class TestRepresentedScientificDecisionIngressProducer:
    """Own software evidence for ``RepresentedScientificDecisionIngressProducer``."""

    def test_fields__public_contract__matches_exact_inventory(self) -> None:
        """Expose the exact documented immutable field inventory.

        Evidence ID: SV-WFR-REPRESENTED-SCIENTIFIC-DECISION-INGRESS-PRODUCER-001

        Requirement: ``RepresentedScientificDecisionIngressProducer`` declares
        exactly its documented public DataObject
        or ResultObject fields in constructor order.

        Acceptance: :func:`dataclasses.fields` returns the exact field-name tuple.
        """
        assert tuple(field.name for field in fields(SUT)) == (
            "identity",
            "workflow_identity",
            "workflow_run_identity",
            "request_identity",
            "transition_record_identity",
            "recorder_identity",
            "response_source_identity",
            "authority_context_identity",
            "resolution_identity",
        )
