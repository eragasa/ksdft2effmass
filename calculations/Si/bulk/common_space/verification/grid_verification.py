"""Independent complete-grid computation and only-then producer correlation."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction

from ksdft2effmass.serialization.enums import StrWireEnum
from projectkoios.integrations.wannier90 import Wannier90NativeArtifactIdentity

from .controls import (
    CommonSpaceDeficientDirection,
    CommonSpaceDeficientDirectionAnalysis,
    CommonSpaceDirectionOutcome,
    CommonSpaceUnitaryInvariance,
)
from .native_overlap import CommonSpaceNativeOverlapReconstruction
from .native_precision import (
    CommonSpaceNativePrecisionAssessment,
    CommonSpaceNativeRankAssessment,
)
from .source_admission import CommonSpaceEvidenceRole, CommonSpaceSourceAdmission


class CommonSpaceVerificationOutcome(StrWireEnum):
    independent_result_complete = "independent-result-complete-pending-comparison"
    numerically_inconclusive = "numerically-inconclusive"
    producer_mismatch = "producer-mismatch"
    rank_diagnosis_correlated = "rank-diagnosis-correlated-under-declared-contract"


@dataclass(frozen=True, slots=True, kw_only=True)
class CommonSpacePointVerification:
    assessment: CommonSpaceNativeRankAssessment
    direction: CommonSpaceDeficientDirection
    unitary_invariance_passed: bool

    def __post_init__(self) -> None:
        if (
            type(self.assessment) is not CommonSpaceNativeRankAssessment
            or type(self.direction) is not CommonSpaceDeficientDirection
            or type(self.unitary_invariance_passed) is not bool
        ):
            raise TypeError("point verification requires exact declared record types")

    @property
    def conclusive(self) -> bool:
        return (
            self.assessment.resolved_rank is not None
            and self.unitary_invariance_passed
            and self.direction.outcome
            in (
                CommonSpaceDirectionOutcome.enclosed,
                CommonSpaceDirectionOutcome.full_rank,
            )
        )


@dataclass(frozen=True, slots=True, kw_only=True)
class CommonSpaceIndependentGridResult:
    """Completed independent result; contains no producer computational input."""

    admission: CommonSpaceSourceAdmission
    points: tuple[CommonSpacePointVerification, ...]

    def __post_init__(self) -> None:
        if type(self.admission) is not CommonSpaceSourceAdmission:
            raise TypeError("admission must be CommonSpaceSourceAdmission")
        if (
            type(self.points) is not tuple
            or len(self.points) != 216
            or any(
                type(point) is not CommonSpacePointVerification for point in self.points
            )
        ):
            raise ValueError("independent grid result requires all 216 typed points")
        for index, point in enumerate(self.points):
            if (
                point.assessment.overlap.ordered_index != index
                or point.assessment.overlap.parsed_inputs
                is not self.admission.parsed_inputs
                or point.assessment.rounding_model != self.admission.rounding_model
                or point.assessment.frozen_rank_threshold
                != self.admission.frozen_rank_threshold
            ):
                raise ValueError("independent point/source/policy correlation differs")

    @property
    def outcome(self) -> CommonSpaceVerificationOutcome:
        if all(point.conclusive for point in self.points):
            return CommonSpaceVerificationOutcome.independent_result_complete
        return CommonSpaceVerificationOutcome.numerically_inconclusive

    @property
    def deficient_indices(self) -> tuple[int, ...]:
        return tuple(
            index
            for index, point in enumerate(self.points)
            if point.assessment.resolved_rank is not None
            and point.assessment.resolved_rank < 10
        )


@dataclass(frozen=True, slots=True, kw_only=True)
class CommonSpaceIndependentVerification:
    """Verify the complete C6 field after admission, without reading a producer.

    This action is not execution authorization. Native sources must already be parsed
    through the shared provider boundary. Exact reconstruction, precision coverage,
    isolated-direction weights, and one fixed unitary control are computed per point.
    Inconclusiveness remains visible; no point or unresolved direction is dropped.
    """

    admission: CommonSpaceSourceAdmission

    def __post_init__(self) -> None:
        if type(self.admission) is not CommonSpaceSourceAdmission:
            raise TypeError("admission must be CommonSpaceSourceAdmission")

    def execute(self) -> CommonSpaceIndependentGridResult:
        self.admission.authenticate()
        points: list[CommonSpacePointVerification] = []
        for index in range(216):
            overlap = CommonSpaceNativeOverlapReconstruction(
                parsed_inputs=self.admission.parsed_inputs, ordered_index=index
            ).execute()
            assessment = CommonSpaceNativePrecisionAssessment(
                overlap=overlap,
                rounding_model=self.admission.rounding_model,
                frozen_rank_threshold=self.admission.frozen_rank_threshold,
            ).execute()
            points.append(
                CommonSpacePointVerification(
                    assessment=assessment,
                    direction=CommonSpaceDeficientDirectionAnalysis(
                        assessment=assessment
                    ).execute(),
                    unitary_invariance_passed=CommonSpaceUnitaryInvariance(
                        assessment=assessment
                    ).execute(),
                )
            )
        return CommonSpaceIndependentGridResult(
            admission=self.admission, points=tuple(points)
        )


@dataclass(frozen=True, slots=True, kw_only=True)
class CommonSpaceProducerPoint:
    """Post-computation comparison data, not inputs to independent reconstruction.

    Spectrum order is maximum, next-to-minimum, minimum. Numeric values must be
    nonnegative built-in Fractions. Weights use the exact ten-coordinate atomic order;
    full-rank points carry no deficient vector. Reported group weights are ordered
    s, p, s-star and are not reconstructed from the atomic values during comparison.
    No weight tolerance is inferred from the singular-value threshold.
    """

    ordered_index: int
    resolved_rank: int
    singular_values: tuple[Fraction, Fraction, Fraction]
    atomic_weights: tuple[Fraction, ...]
    group_weights: tuple[Fraction, ...]

    def __post_init__(self) -> None:
        if type(self.ordered_index) is not int or not 0 <= self.ordered_index < 216:
            raise ValueError("producer index must be a built-in integer in [0, 216)")
        if type(self.resolved_rank) is not int or not 0 <= self.resolved_rank <= 10:
            raise ValueError("producer rank must be a built-in integer in [0, 10]")
        if (
            type(self.singular_values) is not tuple
            or len(self.singular_values) != 3
            or any(
                type(value) is not Fraction or value < 0
                for value in self.singular_values
            )
        ):
            raise ValueError("producer spectrum must be three nonnegative Fractions")
        if (
            not self.singular_values[0]
            >= self.singular_values[1]
            >= self.singular_values[2]
        ):
            raise ValueError("producer spectrum order differs")
        if type(self.atomic_weights) is not tuple or any(
            type(value) is not Fraction or not 0 <= value <= 1
            for value in self.atomic_weights
        ):
            raise ValueError("producer weights must be exact probability values")
        if len(self.atomic_weights) != (10 if self.resolved_rank < 10 else 0):
            raise ValueError("every deficient point needs all ten comparison weights")
        if type(self.group_weights) is not tuple or any(
            type(value) is not Fraction or not 0 <= value <= 1
            for value in self.group_weights
        ):
            raise ValueError("producer group weights must be exact probability values")
        if len(self.group_weights) != (3 if self.resolved_rank < 10 else 0):
            raise ValueError(
                "every deficient point needs all three reported group weights"
            )


@dataclass(frozen=True, slots=True, kw_only=True)
class CommonSpaceProducerReference:
    """Complete source-bound numerical view decoded from an original producer result."""

    state_assertions_sha256: str
    producer_result_identity: Wannier90NativeArtifactIdentity
    native_identities: tuple[Wannier90NativeArtifactIdentity, ...]
    frozen_rank_threshold: Fraction
    points: tuple[CommonSpaceProducerPoint, ...]

    def __post_init__(self) -> None:
        if type(self.producer_result_identity) is not Wannier90NativeArtifactIdentity:
            raise TypeError(
                "producer result identity must use the exact provider record"
            )
        if (
            type(self.state_assertions_sha256) is not str
            or len(self.state_assertions_sha256) != 64
            or any(
                value not in "0123456789abcdef"
                for value in self.state_assertions_sha256
            )
        ):
            raise ValueError("producer assertion binding must be a lowercase SHA-256")
        if (
            type(self.native_identities) is not tuple
            or len(self.native_identities) != 3
            or any(
                type(value) is not Wannier90NativeArtifactIdentity
                for value in self.native_identities
            )
        ):
            raise TypeError("producer native identities must be a complete typed tuple")
        if (
            type(self.frozen_rank_threshold) is not Fraction
            or self.frozen_rank_threshold < 0
        ):
            raise ValueError("producer threshold must be a nonnegative Fraction")
        if (
            type(self.points) is not tuple
            or len(self.points) != 216
            or any(
                type(point) is not CommonSpaceProducerPoint
                or point.ordered_index != index
                for index, point in enumerate(self.points)
            )
        ):
            raise ValueError("producer reference must include every ordered C6 point")


@dataclass(frozen=True, slots=True, kw_only=True)
class CommonSpaceProducerCorrelation:
    """Compare only a finished independent result, using derived error intervals.

    Singular-value checks use arithmetic intervals expanded by the conditional overlap
    perturbation bound. Weight checks use projector-error intervals, never a borrowed
    singular-value tolerance. Source mismatch raises; numerical mismatch is reported.
    The result is a tuple of explicit mismatch descriptions, not scientific acceptance.
    """

    independent: CommonSpaceIndependentGridResult
    producer: CommonSpaceProducerReference

    def __post_init__(self) -> None:
        if (
            type(self.independent) is not CommonSpaceIndependentGridResult
            or type(self.producer) is not CommonSpaceProducerReference
        ):
            raise TypeError(
                "correlation requires complete independent and producer records"
            )

    def execute(self) -> tuple[str, ...]:
        admission = self.independent.admission
        assertion = next(
            item.expected
            for item in admission.evidence
            if item.role is CommonSpaceEvidenceRole.state_assertions
        )
        if (
            self.producer.state_assertions_sha256 != assertion.sha256
            or self.producer.producer_result_identity
            != next(
                item.expected
                for item in admission.evidence
                if item.role is CommonSpaceEvidenceRole.producer_reconstruction
            )
            or self.producer.native_identities
            != admission.parsed_inputs.contract.identities
            or self.producer.frozen_rank_threshold != admission.frozen_rank_threshold
        ):
            raise ValueError("producer source/state/threshold identities differ")
        mismatches: list[str] = []
        for index, (independent, producer) in enumerate(
            zip(self.independent.points, self.producer.points, strict=True)
        ):
            if not independent.conclusive:
                mismatches.append(f"point {index}: independent result is inconclusive")
                continue
            if independent.assessment.resolved_rank != producer.resolved_rank:
                mismatches.append(f"point {index}: resolved rank differs")
                continue
            arithmetic = independent.assessment.arithmetic
            perturbation = independent.assessment.uncertainty.combined_error_bound
            for location, candidate in zip(
                (-1, 1, 0), producer.singular_values, strict=True
            ):
                interval = arithmetic.eigenvalue_intervals[location]
                lower, upper = interval.nonnegative_bounds
                if (candidate + perturbation) ** 2 < lower or (
                    candidate > perturbation and (candidate - perturbation) ** 2 > upper
                ):
                    mismatches.append(f"point {index}: singular value differs")
            if producer.resolved_rank < 10:
                intervals = independent.direction.orbital_intervals
                if len(intervals) != 10 or any(
                    not interval.lower <= value <= interval.upper
                    for interval, value in zip(
                        intervals, producer.atomic_weights, strict=True
                    )
                ):
                    mismatches.append(
                        f"point {index}: deficient-direction weights differ"
                    )
                for value, group_interval in zip(
                    producer.group_weights,
                    independent.direction.group_intervals,
                    strict=True,
                ):
                    if not group_interval.lower <= value <= group_interval.upper:
                        mismatches.append(
                            f"point {index}: aggregate orbital weights differ"
                        )
        return tuple(mismatches)
