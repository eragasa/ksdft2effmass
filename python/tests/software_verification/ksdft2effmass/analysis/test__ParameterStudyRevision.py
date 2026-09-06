r"""Software verification of ``ParameterStudyRevision``.

Evidence profile: routine

Bounded artifact scope: immutable parameter-study revision kind and candidate closure.

Facet and represented meaning

The module verifies that one numerical-convergence revision cannot cross modeled
physical branches.

Intrinsic and cross-object scope

``ParameterStudyRevision`` is the sole system under test. Refinement, calculator
binding, execution, and scientific acceptance are excluded.

VVUQ and scientific exclusions

This is software verification with synthetic identities. It establishes no physical
convergence, scientific validation, uncertainty quantification, or accepted setting.
"""

import pytest

from ksdft2effmass.analysis._parameter_study import (
    ParameterFactorKind,
    ParameterStudyCandidate,
    ParameterStudyCandidateIdentity,
    ParameterStudyIdentity,
    ParameterStudyKind,
    ParameterStudyRevision,
    ParameterStudyRevisionIdentity,
    ParameterStudySubjectIdentity,
    QuantityOfInterestIdentity,
    ScalarQuantityOfInterestCriterion,
)

pytestmark = pytest.mark.software_verification
SUT = ParameterStudyRevision


class TestParameterStudyRevision:
    """Own software evidence for immutable study-revision semantics."""

    @staticmethod
    def candidates(
        subjects: tuple[ParameterStudySubjectIdentity, ...],
        values: tuple[float, ...],
    ) -> tuple[ParameterStudyCandidate, ...]:
        """Return ordered synthetic cutoff candidates."""
        return tuple(
            ParameterStudyCandidate(
                ParameterStudyCandidateIdentity(f"candidate.{index}.{value:g}"),
                subject,
                ParameterFactorKind.NUMERICAL,
                "wavefunction_cutoff",
                value,
                "rydberg",
            )
            for index, (value, subject) in enumerate(zip(values, subjects, strict=True))
        )

    def test_constructor__study_kind__rejects_numerical_branch_drift(self) -> None:
        """Evidence ID: SV-PLANE-WAVE-STUDY-001

        Requirement: Numerical-convergence candidates vary a numerical factor under
        one fixed modeled-subject identity, while physical-branch comparison remains
        a distinct study kind.

        Acceptance: A numerical revision with two subject identities raises
        ``ValueError`` and an explicitly typed physical-branch revision admits them.
        """
        scalar = ParameterStudySubjectIdentity("model.scalar.non-soc")
        soc = ParameterStudySubjectIdentity("model.spinor.soc")
        candidates = self.candidates((scalar, soc), (30.0, 36.0))
        criterion = ScalarQuantityOfInterestCriterion(
            QuantityOfInterestIdentity("total-energy-per-atom"),
            "rydberg_per_atom",
            0.25,
        )
        with pytest.raises(ValueError, match="fixed subject"):
            SUT(
                ParameterStudyRevisionIdentity("cutoff-study.revision.1"),
                ParameterStudyIdentity("cutoff-study"),
                ParameterStudyKind.NUMERICAL_CONVERGENCE,
                candidates,
                (criterion,),
                None,
            )

        branch_candidates = tuple(
            ParameterStudyCandidate(
                ParameterStudyCandidateIdentity(f"branch.{index}"),
                subject,
                ParameterFactorKind.PHYSICAL_BRANCH,
                "relativistic_spin_branch",
                float(index),
                "branch_index",
            )
            for index, subject in enumerate((scalar, soc))
        )
        revision = SUT(
            ParameterStudyRevisionIdentity("branch-study.revision.1"),
            ParameterStudyIdentity("branch-study"),
            ParameterStudyKind.PHYSICAL_BRANCH_COMPARISON,
            branch_candidates,
            (criterion,),
            None,
        )
        assert revision.kind is ParameterStudyKind.PHYSICAL_BRANCH_COMPARISON
