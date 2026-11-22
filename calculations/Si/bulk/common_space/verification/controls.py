"""Independent deficient-direction intervals and exact unitary controls."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction

from ksdft2effmass.serialization.enums import StrWireEnum

from .gram_rank import (
    _ExactComplex,
    _ExactGramRankEncloser,
    _ExactMatrix,
)
from .native_precision import (
    CommonSpaceMatrixUncertainty,
    CommonSpaceNativeRankAssessment,
)


class CommonSpaceDirectionOutcome(StrWireEnum):
    """A numerical direction result, never scientific acceptance."""

    enclosed = "isolated-direction-enclosed"
    full_rank = "not-applicable-full-rank"
    rank_unresolved = "rank-unresolved"
    multiple_directions = "multiple-unresolved-directions"
    arithmetic_gap_unresolved = "arithmetic-eigenvalue-gap-unresolved"
    input_gap_unresolved = "native-eigenvalue-gap-unresolved"


@dataclass(frozen=True, slots=True, kw_only=True)
class CommonSpaceWeightInterval:
    """Exact dimensionless probability interval; endpoints are built-in Fractions."""

    lower: Fraction
    upper: Fraction

    def __post_init__(self) -> None:
        if type(self.lower) is not Fraction or type(self.upper) is not Fraction:
            raise TypeError("weight interval endpoints must be built-in Fractions")
        if not 0 <= self.lower <= self.upper <= 1:
            raise ValueError("weight interval must lie in [0, 1]")


@dataclass(frozen=True, slots=True, kw_only=True)
class CommonSpaceDeficientDirection:
    """Conditional minimum-eigendirection weights in the admitted atomic order.

    Ten orbital intervals and three aggregate intervals (s, p, s-star) are present
    only for an isolated, covered rank-nine direction. Bounds describe projectors,
    not phase-dependent eigenvector coordinates or symmetry representations.
    """

    outcome: CommonSpaceDirectionOutcome
    nominal_weights: tuple[Fraction, ...] = ()
    orbital_intervals: tuple[CommonSpaceWeightInterval, ...] = ()
    group_intervals: tuple[CommonSpaceWeightInterval, ...] = ()
    arithmetic_projector_error: Fraction | None = None
    input_projector_error: Fraction | None = None
    rayleigh_residual_squared: Fraction | None = None
    eigenvalue_gap_lower: Fraction | None = None

    def __post_init__(self) -> None:
        if type(self.outcome) is not CommonSpaceDirectionOutcome:
            raise TypeError("outcome must be a CommonSpaceDirectionOutcome")
        if type(self.nominal_weights) is not tuple or any(
            type(value) is not Fraction or not 0 <= value <= 1
            for value in self.nominal_weights
        ):
            raise TypeError("nominal weights must be a tuple of exact probabilities")
        if self.nominal_weights and (
            len(self.nominal_weights) != 10 or sum(self.nominal_weights) != 1
        ):
            raise ValueError("nominal atomic weights must sum exactly to one")
        for intervals in (self.orbital_intervals, self.group_intervals):
            if type(intervals) is not tuple or any(
                type(value) is not CommonSpaceWeightInterval for value in intervals
            ):
                raise TypeError("weight intervals must be an immutable typed tuple")
        for bound in (
            self.arithmetic_projector_error,
            self.input_projector_error,
            self.rayleigh_residual_squared,
            self.eigenvalue_gap_lower,
        ):
            if bound is not None and (type(bound) is not Fraction or bound < 0):
                raise ValueError("direction bounds must be nonnegative Fractions")
        if self.outcome is CommonSpaceDirectionOutcome.enclosed and (
            len(self.nominal_weights) != 10
            or len(self.orbital_intervals) != 10
            or len(self.group_intervals) != 3
            or self.arithmetic_projector_error is None
            or self.input_projector_error is None
            or self.rayleigh_residual_squared is None
            or self.eigenvalue_gap_lower is None
            or self.eigenvalue_gap_lower <= 0
        ):
            raise ValueError("an enclosed direction requires complete bounds")
        if self.outcome is not CommonSpaceDirectionOutcome.enclosed and (
            self.orbital_intervals or self.group_intervals
        ):
            raise ValueError("unresolved directions cannot carry resolved weights")


@dataclass(frozen=True, slots=True, kw_only=True)
class CommonSpaceDeficientDirectionAnalysis:
    """Bound a minimum direction without trusting an eigensolver normalization.

    Uses exact Rayleigh residuals and an arithmetic eigenvalue-gap lower bound.
    Native/parse perturbations use a singular-gap bound, avoiding squared-gap loss.
    Rational bounds have no fixed-width overflow; resource errors propagate. No
    singular-value threshold, weight tolerance, or symmetry interpretation is chosen.
    """

    assessment: CommonSpaceNativeRankAssessment

    def __post_init__(self) -> None:
        if type(self.assessment) is not CommonSpaceNativeRankAssessment:
            raise TypeError("assessment must be a CommonSpaceNativeRankAssessment")

    def execute(self) -> CommonSpaceDeficientDirection:
        rank = self.assessment.resolved_rank
        if rank is None:
            return CommonSpaceDeficientDirection(
                outcome=CommonSpaceDirectionOutcome.rank_unresolved
            )
        if rank == 10:
            return CommonSpaceDeficientDirection(
                outcome=CommonSpaceDirectionOutcome.full_rank
            )
        if rank != 9:
            return CommonSpaceDeficientDirection(
                outcome=CommonSpaceDirectionOutcome.multiple_directions
            )
        arithmetic = self.assessment.arithmetic
        vector = _ExactMatrix(
            rows=tuple(
                (_ExactComplex(real=real, imaginary=imaginary),)
                for real, imaginary in arithmetic.minimum_eigenvector
            )
        )
        norm_squared = sum(
            (row[0].real ** 2 + row[0].imaginary ** 2 for row in vector.rows),
            start=Fraction(0),
        )
        nominal = tuple(
            (row[0].real ** 2 + row[0].imaginary ** 2) / norm_squared
            for row in vector.rows
        )
        overlap = self.assessment.overlap._matrix
        gram = overlap.adjoint().multiply(overlap)
        image = gram.multiply(vector)
        numerator = vector.adjoint().multiply(image).rows[0][0]
        if numerator.imaginary != 0:
            raise RuntimeError("Hermitian Rayleigh quotient has an imaginary part")
        rayleigh = numerator.real / norm_squared
        residual = image.subtract(vector.multiply(_ExactMatrix.diagonal((rayleigh,))))
        residual_squared = (
            sum(
                (row[0].real ** 2 + row[0].imaginary ** 2 for row in residual.rows),
                start=Fraction(0),
            )
            / norm_squared
        )
        first, second = arithmetic.eigenvalue_intervals[:2]
        rayleigh_gap = second.lower - rayleigh
        gap = second.lower - first.upper
        if gap <= 0 or rayleigh_gap <= 0:
            return CommonSpaceDeficientDirection(
                outcome=CommonSpaceDirectionOutcome.arithmetic_gap_unresolved,
                nominal_weights=nominal,
            )
        arithmetic_error = min(
            Fraction(1),
            CommonSpaceMatrixUncertainty._sqrt_upper(
                residual_squared / rayleigh_gap**2
            ),
        )
        if arithmetic_error >= 1:
            return CommonSpaceDeficientDirection(
                outcome=CommonSpaceDirectionOutcome.arithmetic_gap_unresolved,
                nominal_weights=nominal,
            )
        overlap_error = self.assessment.uncertainty.combined_error_bound
        minimum_upper = CommonSpaceMatrixUncertainty._sqrt_upper(
            max(Fraction(0), first.upper)
        )
        next_lower = CommonSpaceMatrixUncertainty._sqrt_lower(
            max(Fraction(0), second.lower)
        )
        if next_lower - minimum_upper <= 2 * overlap_error:
            return CommonSpaceDeficientDirection(
                outcome=CommonSpaceDirectionOutcome.input_gap_unresolved,
                nominal_weights=nominal,
                arithmetic_projector_error=arithmetic_error,
                rayleigh_residual_squared=residual_squared,
                eigenvalue_gap_lower=gap,
            )
        input_error = (
            Fraction(0)
            if overlap_error == 0
            else min(
                Fraction(1),
                (minimum_upper + overlap_error) / (next_lower - overlap_error),
            )
        )
        weight_error = arithmetic_error + input_error
        if weight_error >= 1:
            return CommonSpaceDeficientDirection(
                outcome=CommonSpaceDirectionOutcome.input_gap_unresolved,
                nominal_weights=nominal,
                arithmetic_projector_error=arithmetic_error,
                input_projector_error=input_error,
                eigenvalue_gap_lower=gap,
            )

        def interval(value: Fraction) -> CommonSpaceWeightInterval:
            return CommonSpaceWeightInterval(
                lower=max(Fraction(0), value - weight_error),
                upper=min(Fraction(1), value + weight_error),
            )

        groups = ((0, 5), (1, 2, 3, 6, 7, 8), (4, 9))
        return CommonSpaceDeficientDirection(
            outcome=CommonSpaceDirectionOutcome.enclosed,
            nominal_weights=nominal,
            orbital_intervals=tuple(interval(value) for value in nominal),
            group_intervals=tuple(
                interval(sum((nominal[index] for index in group), start=Fraction(0)))
                for group in groups
            ),
            arithmetic_projector_error=arithmetic_error,
            input_projector_error=input_error,
            rayleigh_residual_squared=residual_squared,
            eigenvalue_gap_lower=gap,
        )


@dataclass(frozen=True, slots=True, kw_only=True)
class CommonSpaceUnitaryInvariance:
    """One fixed exact rational retained-basis control, not a fitted alignment Q(k)."""

    assessment: CommonSpaceNativeRankAssessment

    def __post_init__(self) -> None:
        if type(self.assessment) is not CommonSpaceNativeRankAssessment:
            raise TypeError("assessment must be a CommonSpaceNativeRankAssessment")

    def execute(self) -> bool:
        """Require exact Gram identity and compatible independent arithmetic bounds."""
        rows: list[tuple[_ExactComplex, ...]] = []
        signs = ((1, 1, 1, 1), (1, 1, -1, -1), (1, -1, 1, -1), (1, -1, -1, 1))
        for row in range(10):
            entries: list[_ExactComplex] = []
            for column in range(10):
                if row < 8 and row // 4 == column // 4:
                    entry = _ExactComplex(real=Fraction(signs[row % 4][column % 4], 2))
                elif row == column == 8:
                    entry = _ExactComplex(imaginary=Fraction(1))
                elif row == column == 9:
                    entry = _ExactComplex(imaginary=Fraction(-1))
                else:
                    entry = _ExactComplex()
                entries.append(entry)
            rows.append(tuple(entries))
        unitary = _ExactMatrix(rows=tuple(rows[1:] + rows[:1]))
        identity = _ExactMatrix.diagonal((Fraction(1),) * 10)
        if unitary.adjoint().multiply(unitary) != identity:
            raise RuntimeError("fixed retained-basis control is not exactly unitary")
        overlap = self.assessment.overlap._matrix
        rotated = unitary.adjoint().multiply(overlap)
        if rotated.adjoint().multiply(rotated) != overlap.adjoint().multiply(overlap):
            return False
        alternate = _ExactGramRankEncloser(
            independent_overlap=rotated,
            rank_threshold=self.assessment.frozen_rank_threshold,
        ).execute()
        original = self.assessment.arithmetic
        if original.failure is not None or alternate.failure is not None:
            return False
        return (
            original.resolved_rank == alternate.resolved_rank
            and original.resolved_rank is not None
            and all(
                max(left.lower, right.lower) <= min(left.upper, right.upper)
                for left, right in zip(
                    original.eigenvalue_intervals,
                    alternate.eigenvalue_intervals,
                    strict=True,
                )
            )
        )
