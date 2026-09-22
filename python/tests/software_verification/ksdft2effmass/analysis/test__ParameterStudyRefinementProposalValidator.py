r"""Software verification of ``ParameterStudyRefinementProposalValidator``.

Evidence profile: routine

Bounded artifact scope: independent validation of one adaptive successor proposal.

Facet and represented meaning

The module verifies evaluation-prefix closure, exact state lineage, successor
identity freshness, and declared candidate-domain membership.

Intrinsic and cross-object scope

``ParameterStudyRefinementProposalValidator`` is the sole system under test. Concrete
refinement-algorithm behavior, backend compilation, and execution are excluded.

VVUQ and scientific exclusions

This is software verification using synthetic identities and values. It establishes
no physical convergence, scientific validation, UQ, or accepted parameter.
"""

from dataclasses import replace

import pytest

from ksdft2effmass.analysis._parameter_study import (
    NormalizedObservationRequirementIdentity,
    ParameterFactorKind,
    ParameterStudyCandidate,
    ParameterStudyCandidateIdentity,
    ParameterStudyIdentity,
    ParameterStudyKind,
    ParameterStudyProposalValidationCode,
    ParameterStudyRefinementConfigurationIdentity,
    ParameterStudyRefinementIdentity,
    ParameterStudyRefinementOutcome,
    ParameterStudyRefinementProposalInvalid,
    ParameterStudyRefinementProposalValidator,
    ParameterStudyRefinementProposed,
    ParameterStudyRefinementRequest,
    ParameterStudyRefinementState,
    ParameterStudyRefinementStateIdentity,
    ParameterStudyRevision,
    ParameterStudyRevisionIdentity,
    ParameterStudySubjectIdentity,
    QuantityOfInterestCompleteness,
    QuantityOfInterestDefinition,
    QuantityOfInterestIdentity,
    ScalarQuantityOfInterestCriterion,
)

pytestmark = pytest.mark.software_verification
SUT = ParameterStudyRefinementProposalValidator


class TestParameterStudyRefinementProposalValidator:
    """Own software evidence for independent proposal validation."""

    @staticmethod
    def revision() -> ParameterStudyRevision:
        """Return one valid finite numerical-convergence domain."""
        subject = ParameterStudySubjectIdentity("model.scalar.non-soc")
        candidates = tuple(
            ParameterStudyCandidate(
                ParameterStudyCandidateIdentity(f"candidate.{index}.{value:g}"),
                subject,
                ParameterFactorKind.NUMERICAL,
                "wavefunction_cutoff",
                value,
                "rydberg",
            )
            for index, value in enumerate((30.0, 36.0, 42.0))
        )
        return ParameterStudyRevision(
            ParameterStudyRevisionIdentity("cutoff-study.revision.1"),
            ParameterStudyIdentity("cutoff-study"),
            ParameterStudyKind.NUMERICAL_CONVERGENCE,
            candidates,
            (
                ScalarQuantityOfInterestCriterion(
                    QuantityOfInterestIdentity("total-energy-per-atom"),
                    "rydberg_per_atom",
                    0.25,
                ),
            ),
            None,
        )

    @staticmethod
    def definition() -> QuantityOfInterestDefinition:
        """Return the exact synthetic QoI definition."""
        return QuantityOfInterestDefinition(
            QuantityOfInterestIdentity("total-energy-per-atom"),
            (NormalizedObservationRequirementIdentity("normalized.total-energy"),),
            QuantityOfInterestCompleteness.COMPLETE,
        )

    @classmethod
    def request(
        cls,
        revision: ParameterStudyRevision,
        state: ParameterStudyRefinementState,
    ) -> ParameterStudyRefinementRequest:
        """Return one exact proposal-validation predecessor request."""
        return ParameterStudyRefinementRequest(
            revision,
            (cls.definition(),),
            (),
            ParameterStudyRefinementIdentity("finite-sequence.v1"),
            ParameterStudyRefinementConfigurationIdentity("finite-sequence.cutoff.v1"),
            state,
            2,
        )

    @staticmethod
    def initial_state() -> ParameterStudyRefinementState:
        """Return one empty evaluated-prefix state."""
        return ParameterStudyRefinementState(
            ParameterStudyRefinementStateIdentity("state.initial"), None, ()
        )

    def test_method__execute__rejects_malformed_predecessor_and_reused_identity(
        self,
    ) -> None:
        """Evidence ID: SV-PLANE-WAVE-STUDY-004

        Requirement: Validation establishes predecessor evaluation-prefix closure
        and requires a distinct successor-state identity.

        Acceptance: A predecessor claiming an unevaluated candidate and a proposal
        reusing the predecessor identity return exact rejection codes.
        """
        revision = self.revision()
        malformed_state = ParameterStudyRefinementState(
            ParameterStudyRefinementStateIdentity("state.malformed"),
            None,
            (revision.candidates[1].identity,),
        )
        request = self.request(revision, malformed_state)
        proposal = ParameterStudyRefinementProposed(
            ParameterStudyRefinementOutcome.PROPOSED,
            request.refinement_identity,
            request.configuration_identity,
            revision.identity,
            revision.candidates[0],
            ParameterStudyRefinementState(
                ParameterStudyRefinementStateIdentity("state.successor"),
                malformed_state.identity,
                malformed_state.considered_candidate_identities
                + (revision.candidates[0].identity,),
            ),
        )
        rejected = SUT().execute(request, proposal)
        assert type(rejected) is ParameterStudyRefinementProposalInvalid
        assert rejected.code is (
            ParameterStudyProposalValidationCode.PREDECESSOR_STATE_NOT_EVALUATED_PREFIX
        )

        initial = self.initial_state()
        valid_request = self.request(revision, initial)
        reused_proposal = replace(
            proposal,
            state=ParameterStudyRefinementState(
                initial.identity,
                None,
                (revision.candidates[0].identity,),
            ),
        )
        identity_rejected = SUT().execute(valid_request, reused_proposal)
        assert type(identity_rejected) is ParameterStudyRefinementProposalInvalid
        assert identity_rejected.code is (
            ParameterStudyProposalValidationCode.SUCCESSOR_STATE_IDENTITY_REUSED
        )

    def test_method__execute__rejects_candidate_outside_declared_domain(self) -> None:
        """Evidence ID: SV-PLANE-WAVE-STUDY-005

        Requirement: A proposal candidate belongs to the exact declared domain.

        Acceptance: An externally constructed out-of-domain candidate returns the
        exact closed domain rejection.
        """
        revision = self.revision()
        request = self.request(revision, self.initial_state())
        outside = ParameterStudyCandidate(
            ParameterStudyCandidateIdentity("candidate.outside"),
            revision.candidates[0].subject_identity,
            ParameterFactorKind.NUMERICAL,
            "wavefunction_cutoff",
            48.0,
            "rydberg",
        )
        proposal = ParameterStudyRefinementProposed(
            ParameterStudyRefinementOutcome.PROPOSED,
            request.refinement_identity,
            request.configuration_identity,
            revision.identity,
            outside,
            ParameterStudyRefinementState(
                ParameterStudyRefinementStateIdentity("state.outside"),
                request.state.identity,
                (outside.identity,),
            ),
        )
        rejected = SUT().execute(request, proposal)
        assert type(rejected) is ParameterStudyRefinementProposalInvalid
        assert rejected.code is (
            ParameterStudyProposalValidationCode.CANDIDATE_OUTSIDE_DOMAIN
        )
