"""Conditional native/parse uncertainty bounds, separate from the frozen rank gate."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from math import isfinite, isqrt, ulp
from sys import float_info

from projectkoios.physkit.units.quantities import ComplexMatrixQuantity, Unitless

from .gram_rank import CommonSpaceGramRankEnclosure, GramRankDisposition, _ExactMatrix
from .native_overlap import CommonSpaceReconstructedOverlap


@dataclass(frozen=True, slots=True, kw_only=True)
class CommonSpaceNativeRoundingModel:
    """Declared absolute error per real/imaginary native component, dimensionless.

    Each bound is a nonnegative built-in Fraction. The model does not infer precision
    or rounding mode from parsed values, prove that native output honors a declaration,
    or replace the frozen singular-value threshold. Exact rational operations have no
    fixed-width overflow; resource errors propagate.
    """

    amn_component_error: Fraction
    gauge_component_error: Fraction
    disentanglement_component_error: Fraction

    def __post_init__(self) -> None:
        for value in (
            self.amn_component_error,
            self.gauge_component_error,
            self.disentanglement_component_error,
        ):
            if type(value) is not Fraction or value < 0:
                raise ValueError(
                    "native component errors must be nonnegative built-in Fractions"
                )

    @classmethod
    def from_nearest_decimal_places(
        cls, *, amn: int, gauge: int, disentanglement: int
    ) -> CommonSpaceNativeRoundingModel:
        """Assume nearest rounding to absolute decimal steps, not mantissa digits.

        Counts must be nonnegative built-in integers; booleans and strings are rejected.
        Each component error is exactly 1/(2*10**count). This is a conditional declared
        model, not verification of a formatter. Huge counts may exhaust resources but
        never silently underflow to zero or alter the scientific threshold.
        """
        if any(
            type(value) is not int or value < 0
            for value in (amn, gauge, disentanglement)
        ):
            raise ValueError(
                "decimal-place counts must be nonnegative built-in integers"
            )
        return cls(
            amn_component_error=Fraction(1, 2 * 10**amn),
            gauge_component_error=Fraction(1, 2 * 10**gauge),
            disentanglement_component_error=Fraction(1, 2 * 10**disentanglement),
        )


@dataclass(frozen=True, slots=True, kw_only=True)
class CommonSpaceMatrixUncertainty:
    """Exact upper spectral-norm bounds for one parsed dimensionless matrix.

    Row/column counts are positive built-in integers. Norm/error bounds are nonnegative
    built-in Fractions. Parsing bounds assume correctly rounded binary64 conversion;
    they are upper bounds, not measured errors or a second native-text parser.
    """

    row_count: int
    column_count: int
    nominal_norm_bound: Fraction
    parsing_error_bound: Fraction
    native_error_bound: Fraction

    def __post_init__(self) -> None:
        if any(
            type(value) is not int or value <= 0
            for value in (self.row_count, self.column_count)
        ):
            raise ValueError("matrix dimensions must be positive built-in integers")
        for value in (
            self.nominal_norm_bound,
            self.parsing_error_bound,
            self.native_error_bound,
        ):
            if type(value) is not Fraction or value < 0:
                raise ValueError(
                    "matrix norm bounds must be nonnegative built-in Fractions"
                )

    @classmethod
    def from_parsed_matrix(
        cls, *, matrix: ComplexMatrixQuantity, native_component_error: Fraction
    ) -> CommonSpaceMatrixUncertainty:
        """Bound a finite unitless parsed complex128 matrix without assuming isometry.

        Source entries are explicitly snapshotted as built-in complex binary64 values.
        Half-ULPs are formed as Fractions before division, retaining subnormal bounds.
        Overflow-free rational Gram/Frobenius bounds cover each matrix independently.
        This method does not verify the declared decimal policy against native bytes.
        """
        if (
            type(matrix) is not ComplexMatrixQuantity
            or type(matrix.unit) is not Unitless
        ):
            raise TypeError("matrix must be an exact unitless ComplexMatrixQuantity")
        if type(native_component_error) is not Fraction or native_component_error < 0:
            raise ValueError(
                "native_component_error must be a nonnegative built-in Fraction"
            )
        if (float_info.radix, float_info.mant_dig, float_info.max_exp) != (2, 53, 1024):
            raise RuntimeError("parsing-error model requires IEEE binary64 floats")
        values = tuple(
            tuple(complex(value) for value in row) for row in matrix.magnitude
        )
        if (
            not values
            or not values[0]
            or any(
                not isfinite(value.real) or not isfinite(value.imag)
                for row in values
                for value in row
            )
        ):
            raise ValueError("parsed matrix must be nonempty and finite")
        exact = _ExactMatrix.from_binary64(values)
        nominal_squared_bound = exact.adjoint().multiply(exact).hermitian_norm_bound
        parsing_squared_bound = sum(
            (
                (Fraction.from_float(ulp(value.real)) / 2) ** 2
                + (Fraction.from_float(ulp(value.imag)) / 2) ** 2
                for row in values
                for value in row
            ),
            start=Fraction(0),
        )
        rows, columns = len(values), len(values[0])
        return cls(
            row_count=rows,
            column_count=columns,
            nominal_norm_bound=cls._sqrt_upper(nominal_squared_bound),
            parsing_error_bound=cls._sqrt_upper(parsing_squared_bound),
            native_error_bound=cls._sqrt_upper(
                2 * rows * columns * native_component_error**2
            ),
        )

    @staticmethod
    def _sqrt_lower(value: Fraction) -> Fraction:
        """Use floor(sqrt(n*d))/d: an exact lower bound without a tolerance."""
        return Fraction(isqrt(value.numerator * value.denominator), value.denominator)

    @staticmethod
    def _sqrt_upper(value: Fraction) -> Fraction:
        """Use ceil(sqrt(n*d))/d for n/d: exact upper bound with no chosen tolerance."""
        product = value.numerator * value.denominator
        root = isqrt(product)
        if root * root < product:
            root += 1
        return Fraction(root, value.denominator)


@dataclass(frozen=True, slots=True, kw_only=True)
class CommonSpaceOverlapUncertainty:
    """Conditional perturbation bounds for B=U† U_dis† A T† with exact unitary T.

    Nominal norms refer to parsed matrices. Parsing and native terms are partitioned
    sequentially, retaining all mixed terms. No unitary/isometry assumption is imposed
    on parsed U or U_dis, and no physical, parent-model, or reduction error is included.
    """

    amn: CommonSpaceMatrixUncertainty
    gauge: CommonSpaceMatrixUncertainty
    disentanglement: CommonSpaceMatrixUncertainty

    def __post_init__(self) -> None:
        if any(
            type(value) is not CommonSpaceMatrixUncertainty
            for value in (self.amn, self.gauge, self.disentanglement)
        ):
            raise TypeError("overlap uncertainty requires exact matrix-bound records")
        if (
            self.gauge.row_count != self.gauge.column_count
            or self.disentanglement.column_count != self.gauge.row_count
            or self.amn.row_count != self.disentanglement.row_count
            or self.amn.column_count != self.gauge.row_count
        ):
            raise ValueError("overlap uncertainty matrix dimensions do not correlate")

    @property
    def parsing_error_bound(self) -> Fraction:
        return self._decimal_norm_product - self._parsed_norm_product

    @property
    def native_error_bound(self) -> Fraction:
        return self._unrounded_norm_product - self._decimal_norm_product

    @property
    def combined_error_bound(self) -> Fraction:
        return self._unrounded_norm_product - self._parsed_norm_product

    @property
    def _parsed_norm_product(self) -> Fraction:
        return (
            self.amn.nominal_norm_bound
            * self.gauge.nominal_norm_bound
            * self.disentanglement.nominal_norm_bound
        )

    @property
    def _decimal_norm_product(self) -> Fraction:
        return (
            (self.amn.nominal_norm_bound + self.amn.parsing_error_bound)
            * (self.gauge.nominal_norm_bound + self.gauge.parsing_error_bound)
            * (
                self.disentanglement.nominal_norm_bound
                + self.disentanglement.parsing_error_bound
            )
        )

    @property
    def _unrounded_norm_product(self) -> Fraction:
        return (
            (
                self.amn.nominal_norm_bound
                + self.amn.parsing_error_bound
                + self.amn.native_error_bound
            )
            * (
                self.gauge.nominal_norm_bound
                + self.gauge.parsing_error_bound
                + self.gauge.native_error_bound
            )
            * (
                self.disentanglement.nominal_norm_bound
                + self.disentanglement.parsing_error_bound
                + self.disentanglement.native_error_bound
            )
        )


@dataclass(frozen=True, slots=True, kw_only=True)
class CommonSpaceNativeRankAssessment:
    """A point rank is reportable only if arithmetic resolves and the bound is covered.

    Coverage is conditional on the supplied native/parse model. An uncovered upper
    bound does not prove that the true error exceeds the frozen threshold; it gives
    numerical inconclusiveness. This object never declares CSD0 or CSD1-V passage.
    """

    overlap: CommonSpaceReconstructedOverlap
    rounding_model: CommonSpaceNativeRoundingModel
    uncertainty: CommonSpaceOverlapUncertainty
    arithmetic: CommonSpaceGramRankEnclosure

    def __post_init__(self) -> None:
        if (
            type(self.overlap) is not CommonSpaceReconstructedOverlap
            or type(self.rounding_model) is not CommonSpaceNativeRoundingModel
            or type(self.uncertainty) is not CommonSpaceOverlapUncertainty
            or type(self.arithmetic) is not CommonSpaceGramRankEnclosure
        ):
            raise TypeError(
                "native rank assessment must use exact declared record types"
            )
        if (
            self.arithmetic.dimension != 10
            or self.uncertainty.gauge.row_count != 10
            or self.uncertainty.amn.row_count
            != self.overlap.parsed_inputs.contract.parent_band_count
        ):
            raise ValueError(
                "native rank assessment dimensions differ from source contract"
            )

    @property
    def frozen_rank_threshold(self) -> Fraction:
        return self.arithmetic.rank_threshold

    @property
    def uncertainty_bound_covered(self) -> bool:
        return self.uncertainty.combined_error_bound <= self.frozen_rank_threshold

    @property
    def coverage_margin(self) -> Fraction:
        return self.frozen_rank_threshold - self.uncertainty.combined_error_bound

    @property
    def resolved_rank(self) -> int | None:
        if not self.uncertainty_bound_covered:
            return None
        return self.arithmetic.resolved_rank

    @property
    def disposition(self) -> GramRankDisposition:
        if self.resolved_rank is None:
            return GramRankDisposition.numerically_inconclusive
        return GramRankDisposition.rank_resolved


@dataclass(frozen=True, slots=True, kw_only=True)
class CommonSpaceNativePrecisionAssessment:
    """Assess one independently reconstructed point under explicit error assumptions.

    Frozen threshold and native component bounds are nonnegative built-in Fractions.
    No source decimals, threshold, or comparison tolerance are inferred or adjusted.
    Rounding-error propagation is rational and overflow-free; Gram candidate overflow
    remains inconclusive and resource failures propagate without producing a rank.
    """

    overlap: CommonSpaceReconstructedOverlap
    rounding_model: CommonSpaceNativeRoundingModel
    frozen_rank_threshold: Fraction

    def __post_init__(self) -> None:
        if type(self.overlap) is not CommonSpaceReconstructedOverlap:
            raise TypeError("overlap must be a CommonSpaceReconstructedOverlap")
        if type(self.rounding_model) is not CommonSpaceNativeRoundingModel:
            raise TypeError("rounding_model must be a CommonSpaceNativeRoundingModel")
        if (
            type(self.frozen_rank_threshold) is not Fraction
            or self.frozen_rank_threshold < 0
        ):
            raise ValueError(
                "frozen_rank_threshold must be a nonnegative built-in Fraction"
            )

    def execute(self) -> CommonSpaceNativeRankAssessment:
        index = self.overlap.ordered_index
        inputs = self.overlap.parsed_inputs
        uncertainty = CommonSpaceOverlapUncertainty(
            amn=CommonSpaceMatrixUncertainty.from_parsed_matrix(
                matrix=inputs.trial_overlaps.matrices[index],
                native_component_error=self.rounding_model.amn_component_error,
            ),
            gauge=CommonSpaceMatrixUncertainty.from_parsed_matrix(
                matrix=inputs.gauge.matrices[index],
                native_component_error=self.rounding_model.gauge_component_error,
            ),
            disentanglement=CommonSpaceMatrixUncertainty.from_parsed_matrix(
                matrix=inputs.disentanglement.matrices[index],
                native_component_error=self.rounding_model.disentanglement_component_error,
            ),
        )
        return CommonSpaceNativeRankAssessment(
            overlap=self.overlap,
            rounding_model=self.rounding_model,
            uncertainty=uncertainty,
            arithmetic=self.overlap.enclose_rank(
                rank_threshold=self.frozen_rank_threshold
            ),
        )
