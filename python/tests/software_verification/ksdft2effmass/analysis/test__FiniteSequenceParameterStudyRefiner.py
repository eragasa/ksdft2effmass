r"""Software verification of ``FiniteSequenceParameterStudyRefiner``.

Evidence profile: routine

Bounded artifact scope: nominal refinement extension and finite candidate sequencing.

Facet and represented meaning

The module verifies deterministic proposal behavior for one explicitly configured
finite-sequence refinement algorithm.

Intrinsic and cross-object scope

``FiniteSequenceParameterStudyRefiner`` is the sole system under test. Independent
proposal validation, backend compilation, execution, and acceptance are excluded.

VVUQ and scientific exclusions

This is software verification with synthetic values. It establishes no production
convergence, physical correctness, scientific validation, or uncertainty result.
"""

from dataclasses import FrozenInstanceError

import pytest

from ksdft2effmass.analysis._parameter_study import (
    FiniteSequenceParameterStudyRefiner,
    NormalizedObservationRequirementIdentity,
    ParameterFactorKind,
    ParameterStudyCandidate,
    ParameterStudyCandidateIdentity,
    ParameterStudyIdentity,
    ParameterStudyKind,
    ParameterStudyRefinementConfigurationIdentity,
    ParameterStudyRefinementFailure,
    ParameterStudyRefinementFailureCode,
    ParameterStudyRefinementIdentity,
    ParameterStudyRefinementOutcome,
    ParameterStudyRefinementProposed,
    ParameterStudyRefinementRequest,
    ParameterStudyRefinementState,
    ParameterStudyRefinementStateIdentity,
    ParameterStudyRefiner,
    ParameterStudyRevision,
    ParameterStudyRevisionIdentity,
    ParameterStudySubjectIdentity,
    QuantityOfInterestCompleteness,
    QuantityOfInterestDefinition,
    QuantityOfInterestIdentity,
    ScalarQuantityOfInterestCriterion,
)

pytestmark = pytest.mark.software_verification
SUT = FiniteSequenceParameterStudyRefiner


class TestFiniteSequenceParameterStudyRefiner:
    """Own software evidence for finite-sequence refinement behavior."""

    @staticmethod
    def revision(
        values: tuple[float, ...] = (30.0, 36.0, 42.0),
    ) -> ParameterStudyRevision:
        """Return one fixed-subject synthetic cutoff revision."""
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
            for index, value in enumerate(values)
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
        """Return the synthetic QoI and normalized observation requirement."""
        return QuantityOfInterestDefinition(
            QuantityOfInterestIdentity("total-energy-per-atom"),
            (NormalizedObservationRequirementIdentity("normalized.total-energy"),),
            QuantityOfInterestCompleteness.COMPLETE,
        )

    @staticmethod
    def state(
        considered: tuple[ParameterStudyCandidateIdentity, ...] = (),
    ) -> ParameterStudyRefinementState:
        """Return one immutable synthetic refinement state."""
        suffix = ".".join(item.value for item in considered) or "initial"
        return ParameterStudyRefinementState(
            ParameterStudyRefinementStateIdentity(f"state.{suffix}"),
            None,
            considered,
        )

    @classmethod
    def request(
        cls,
        revision: ParameterStudyRevision,
        state: ParameterStudyRefinementState,
        budget: int,
    ) -> ParameterStudyRefinementRequest:
        """Return one exact request without completed evaluations."""
        return ParameterStudyRefinementRequest(
            revision,
            (cls.definition(),),
            (),
            ParameterStudyRefinementIdentity("finite-sequence.v1"),
            ParameterStudyRefinementConfigurationIdentity("finite-sequence.cutoff.v1"),
            state,
            budget,
        )

    @staticmethod
    def refiner() -> FiniteSequenceParameterStudyRefiner:
        """Return the explicitly configured system under test."""
        return SUT(
            ParameterStudyRefinementIdentity("finite-sequence.v1"),
            ParameterStudyRefinementConfigurationIdentity("finite-sequence.cutoff.v1"),
        )

    def test_constructor__nominal_abc__requires_concrete_subclass(self) -> None:
        """Evidence ID: SV-PLANE-WAVE-STUDY-002

        Requirement: Adaptive algorithms use the nominal ``ParameterStudyRefiner``
        ABC and explicit concrete subclasses rather than structural discovery.

        Acceptance: The system under test is a nominal immutable subclass with exact
        algorithm and configuration identities.
        """
        refiner = self.refiner()
        assert issubclass(SUT, ParameterStudyRefiner)
        assert isinstance(refiner, ParameterStudyRefiner)
        assert refiner.refinement_identity.value == "finite-sequence.v1"
        assert refiner.configuration_identity.value == "finite-sequence.cutoff.v1"
        with pytest.raises(FrozenInstanceError):
            refiner._refinement_identity = ParameterStudyRefinementIdentity(  # type: ignore[misc]
                "replacement"
            )

    def test_method__execute__proposes_only_next_declared_candidate(self) -> None:
        """Evidence ID: SV-PLANE-WAVE-STUDY-003

        Requirement: The refiner proposes only the next candidate in the declared
        ordered domain and externalizes exact successor-state lineage.

        Acceptance: The initial request proposes the first candidate; submitting the
        pending state returns insufficient information rather than another proposal.
        """
        revision = self.revision()
        request = self.request(revision, self.state(), 3)
        result = self.refiner().execute(request)
        assert type(result) is ParameterStudyRefinementProposed
        assert result.candidate is revision.candidates[0]
        assert result.state.predecessor_identity == request.state.identity
        assert result.state.considered_candidate_identities == (
            revision.candidates[0].identity,
        )

        pending = self.refiner().execute(self.request(revision, result.state, 2))
        assert type(pending) is ParameterStudyRefinementFailure
        assert (
            pending.outcome is ParameterStudyRefinementOutcome.INSUFFICIENT_INFORMATION
        )
        assert (
            pending.code
            is ParameterStudyRefinementFailureCode.PROPOSED_CANDIDATE_NOT_EVALUATED
        )

    def test_method__execute__rejects_nonincreasing_sequence(self) -> None:
        """Evidence ID: SV-PLANE-WAVE-STUDY-006

        Requirement: The finite candidate sequence is strictly increasing.

        Acceptance: Equal adjacent values return the exact closed invalid result.
        """
        revision = self.revision((30.0, 30.0))
        result = self.refiner().execute(self.request(revision, self.state(), 2))
        assert type(result) is ParameterStudyRefinementFailure
        assert result.outcome is ParameterStudyRefinementOutcome.INVALID
        assert result.code is (
            ParameterStudyRefinementFailureCode.CANDIDATE_SEQUENCE_NOT_INCREASING
        )
