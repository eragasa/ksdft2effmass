r"""Numerical verification of ``FiniteSequenceParameterStudyRefiner``.

Evidence profile: claim_bearing

Bounded artifact scope: stopping and successor behavior for one synthetic
scalar-QoI sequence.

Facet and represented meaning

The artifact represents exact absolute changes between adjacent synthetic scalar
QoI values and the inclusive stopping rule for one fixed-subject numerical study.

Intrinsic and cross-object scope

The test fixes immutable candidates, one criterion, normalized observation
requirements, exact algorithm/configuration identities, evaluations, and state.

VVUQ and scientific exclusions

The values are synthetic exact binary fractions. This establishes numerical
agreement with the documented stopping rule only; it is not a DFT result, production
cutoff, scientific validation, uncertainty quantification, or acceptance decision.
"""

import pytest

from ksdft2effmass.analysis._parameter_study import (
    FiniteSequenceParameterStudyRefiner,
    NormalizedObservationRequirementIdentity,
    ParameterFactorKind,
    ParameterStudyCandidate,
    ParameterStudyCandidateIdentity,
    ParameterStudyIdentity,
    ParameterStudyKind,
    ParameterStudyRefinementComplete,
    ParameterStudyRefinementConfigurationIdentity,
    ParameterStudyRefinementIdentity,
    ParameterStudyRefinementOutcome,
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
    ScalarQuantityOfInterestEvaluation,
)

pytestmark = pytest.mark.numerical_verification
SUT = FiniteSequenceParameterStudyRefiner


class TestFiniteSequenceParameterStudyRefiner:
    """Own synthetic stopping-rule verification for the private refiner."""

    @staticmethod
    def make_revision() -> ParameterStudyRevision:
        """Return one fixed-subject synthetic cutoff-study revision."""
        subject = ParameterStudySubjectIdentity("synthetic.fixed-model")
        candidates = tuple(
            ParameterStudyCandidate(
                ParameterStudyCandidateIdentity(f"candidate.{index}"),
                subject,
                ParameterFactorKind.NUMERICAL,
                "wavefunction_cutoff",
                value,
                "rydberg",
            )
            for index, value in enumerate((30.0, 36.0, 42.0))
        )
        return ParameterStudyRevision(
            ParameterStudyRevisionIdentity("synthetic.cutoff.revision.1"),
            ParameterStudyIdentity("synthetic.cutoff"),
            ParameterStudyKind.NUMERICAL_CONVERGENCE,
            candidates,
            (
                ScalarQuantityOfInterestCriterion(
                    QuantityOfInterestIdentity("synthetic-energy"),
                    "synthetic_energy_unit",
                    0.25,
                ),
            ),
            None,
        )

    @staticmethod
    def make_definition() -> QuantityOfInterestDefinition:
        """Return the synthetic QoI's exact normalized observation requirement."""
        return QuantityOfInterestDefinition(
            QuantityOfInterestIdentity("synthetic-energy"),
            (NormalizedObservationRequirementIdentity("normalized.synthetic-energy"),),
            QuantityOfInterestCompleteness.COMPLETE,
        )

    @staticmethod
    def make_evaluation(
        candidate: ParameterStudyCandidate,
        value: float,
    ) -> ScalarQuantityOfInterestEvaluation:
        """Return one synthetic scalar-QoI evaluation."""
        return ScalarQuantityOfInterestEvaluation(
            candidate.identity,
            QuantityOfInterestIdentity("synthetic-energy"),
            value,
            "synthetic_energy_unit",
        )

    @staticmethod
    def make_refiner() -> FiniteSequenceParameterStudyRefiner:
        """Return the explicitly configured finite-sequence refiner."""
        return SUT(
            ParameterStudyRefinementIdentity("finite-sequence.v1"),
            ParameterStudyRefinementConfigurationIdentity(
                "finite-sequence.synthetic.v1"
            ),
        )

    @classmethod
    def make_request(
        cls,
        revision: ParameterStudyRevision,
        evaluations: tuple[ScalarQuantityOfInterestEvaluation, ...],
        state: ParameterStudyRefinementState,
        budget: int,
    ) -> ParameterStudyRefinementRequest:
        """Return one exact correlated refinement request."""
        return ParameterStudyRefinementRequest(
            revision,
            (cls.make_definition(),),
            evaluations,
            ParameterStudyRefinementIdentity("finite-sequence.v1"),
            ParameterStudyRefinementConfigurationIdentity(
                "finite-sequence.synthetic.v1"
            ),
            state,
            budget,
        )

    def test_artifact__inclusive_tolerance__stops_at_equal_change(self) -> None:
        """Evidence ID: NV-PLANE-WAVE-REFINEMENT-001

        Requirement: For the finite-sequence algorithm, adjacent absolute change
        less than or equal to the declared tolerance selects the later setting.

        Acceptance: Synthetic changes ``0.5`` then exactly ``0.25`` first produce
        the third-candidate proposal and then complete at that candidate with exact
        represented change ``0.25``.
        """
        revision = self.make_revision()
        first, second, third = revision.candidates
        initial = ParameterStudyRefinementState(
            ParameterStudyRefinementStateIdentity("state.two-evaluated"),
            None,
            (first.identity, second.identity),
        )
        first_two = (
            self.make_evaluation(first, -10.0),
            self.make_evaluation(second, -10.5),
        )
        proposed = self.make_refiner().execute(
            self.make_request(revision, first_two, initial, 1)
        )
        assert type(proposed) is ParameterStudyRefinementProposed
        assert proposed.outcome is ParameterStudyRefinementOutcome.PROPOSED
        assert proposed.candidate is third
        assert proposed.state.predecessor_identity == initial.identity

        all_three = first_two + (self.make_evaluation(third, -10.75),)
        complete = self.make_refiner().execute(
            self.make_request(revision, all_three, proposed.state, 0)
        )
        assert type(complete) is ParameterStudyRefinementComplete
        assert complete.outcome is ParameterStudyRefinementOutcome.COMPLETE
        assert complete.selected_candidate_identity == third.identity
        assert complete.absolute_change == 0.25
