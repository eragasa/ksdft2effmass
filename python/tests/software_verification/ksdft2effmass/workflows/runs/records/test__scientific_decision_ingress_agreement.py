r"""Software verification of scientific-decision ingress agreement.

Evidence profile: routine

Bounded artifact scope: no-Task decision ingress provenance and append-only correction
records.

Facet and represented meaning

The artifact verifies agreement between represented decision-ingress provenance and its
initial or correcting resolution.

Intrinsic and cross-object scope

The participating records retain their intrinsic class-owned modules; this artifact
owns only their cross-record agreement.

VVUQ and scientific exclusions

This is software verification only. It establishes no execution, persistence,
scientific validation, uncertainty quantification, authority, or human acceptance.
"""

from dataclasses import fields

import pytest

from ksdft2effmass.workflows import (
    ResultObjectIdentity,
    WorkflowIdentity,
    WorkflowRunIdentity,
)
from ksdft2effmass.workflows.runs import (
    AuthorityContextIdentity,
    BoundaryReceiptIdentity,
    RepresentedScientificDecisionIngressProducer,
    ResponseSourceIdentity,
    ResultObjectContentIdentity,
    ResultProducerProvenanceIdentity,
    ScientificDecisionOptionIdentity,
    ScientificDecisionRecorderIdentity,
    ScientificDecisionRequestIdentity,
    ScientificDecisionResolution,
    ScientificDecisionTransitionRecordIdentity,
)

pytestmark = pytest.mark.software_verification


class TestScientificDecisionIngressAgreement:
    """Own cross-record agreement evidence."""

    def test_constructor__scientific_decision_resolution__owns_no_task_lineage(
        self,
    ) -> None:
        """Retain exact no-Task ingress provenance and append-only correction.

        Evidence ID: SV-WFR-CONTROL-006

        Requirement: A resolution is a ResultObject with request, verbatim response,
        direct source/authority identities, and no Task/activation/attempt fields;
        correction names and supersedes the same exact predecessor.

        Acceptance: Initial and corrected resolutions construct with no prohibited
        lineage fields, while mismatched correction references raise ``ValueError``.
        """
        initial = self.make_resolution("resolution.one")
        corrected = self.make_resolution(
            "resolution.two",
            predecessor=initial.identity,
            supersedes=initial.identity,
        )
        prohibited_fields = {
            "task_instance_identity",
            "activation_identity",
            "operation_identity",
            "attempt_identity",
            "production_identity",
        }

        assert prohibited_fields.isdisjoint(
            field.name for field in fields(RepresentedScientificDecisionIngressProducer)
        )
        assert corrected.predecessor_resolution_identity == initial.identity
        with pytest.raises(ValueError):
            self.make_resolution(
                "resolution.invalid",
                predecessor=initial.identity,
                supersedes=ResultObjectIdentity("resolution.other"),
            )

    @staticmethod
    def make_resolution(
        identity: str,
        *,
        predecessor: ResultObjectIdentity | None = None,
        supersedes: ResultObjectIdentity | None = None,
    ) -> ScientificDecisionResolution:
        """Construct one initial or correcting no-Task resolution."""
        resolution_identity = ResultObjectIdentity(identity)
        source_identity = ResponseSourceIdentity("source.one")
        authority_identity = AuthorityContextIdentity("authority-context.one")
        request_identity = ScientificDecisionRequestIdentity("decision-request.one")
        producer = RepresentedScientificDecisionIngressProducer(
            identity=ResultProducerProvenanceIdentity(f"producer.{identity}"),
            workflow_identity=WorkflowIdentity("workflow.one"),
            workflow_run_identity=WorkflowRunIdentity("run.one"),
            request_identity=request_identity,
            transition_record_identity=ScientificDecisionTransitionRecordIdentity(
                f"transition.{identity}"
            ),
            recorder_identity=ScientificDecisionRecorderIdentity("recorder.v1"),
            response_source_identity=source_identity,
            authority_context_identity=authority_identity,
            resolution_identity=resolution_identity,
        )
        return ScientificDecisionResolution(
            identity=resolution_identity,
            content_identity=ResultObjectContentIdentity(f"content.{identity}"),
            request_identity=request_identity,
            verbatim_response="A",
            normalized_option_identity=ScientificDecisionOptionIdentity("option.a"),
            response_source_identity=source_identity,
            authority_context_identity=authority_identity,
            boundary_receipt_identity=BoundaryReceiptIdentity("receipt.one"),
            predecessor_resolution_identity=predecessor,
            supersedes_resolution_identity=supersedes,
            producer_provenance=producer,
        )
