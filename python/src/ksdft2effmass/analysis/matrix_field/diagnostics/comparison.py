"""Matrix/spectrum errors, perturbation bounds, and error decompositions."""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np

from ._validation import (
    ComplexArray,
    FloatArray,
    matrix_field,
    nonnegative_float,
    positive_float,
)


@dataclass(frozen=True, slots=True)
class MatrixFieldErrorSummary:
    """Retain raw and rank/energy-normalized matrix and spectral errors.

    ``matrix_frobenius_rms`` and ``ordered_spectrum_l2_rms`` are root-mean-square
    pointwise norms. Their normalized forms divide by ``sqrt(rank) * energy_reference``.
    The ordered-spectrum maximum is a componentwise maximum and divides only by the
    positive energy reference.
    """

    rank: int
    energy_reference: float
    matrix_frobenius_maximum: float
    matrix_frobenius_rms: float
    normalized_matrix_frobenius_maximum: float
    normalized_matrix_frobenius_rms: float
    ordered_spectrum_maximum: float
    ordered_spectrum_l2_rms: float
    normalized_ordered_spectrum_maximum: float
    normalized_ordered_spectrum_l2_rms: float

    def __post_init__(self) -> None:
        """Validate exact scalar types, finiteness, and normalization identities."""
        if type(self.rank) is not int:
            raise TypeError("rank must be a built-in int")
        if self.rank <= 0:
            raise ValueError("rank must be positive")
        energy_reference = positive_float("energy_reference", self.energy_reference)
        for name, value in (
            ("matrix_frobenius_maximum", self.matrix_frobenius_maximum),
            ("matrix_frobenius_rms", self.matrix_frobenius_rms),
            (
                "normalized_matrix_frobenius_maximum",
                self.normalized_matrix_frobenius_maximum,
            ),
            (
                "normalized_matrix_frobenius_rms",
                self.normalized_matrix_frobenius_rms,
            ),
            ("ordered_spectrum_maximum", self.ordered_spectrum_maximum),
            ("ordered_spectrum_l2_rms", self.ordered_spectrum_l2_rms),
            (
                "normalized_ordered_spectrum_maximum",
                self.normalized_ordered_spectrum_maximum,
            ),
            (
                "normalized_ordered_spectrum_l2_rms",
                self.normalized_ordered_spectrum_l2_rms,
            ),
        ):
            nonnegative_float(name, value)
        matrix_scale = math.sqrt(self.rank) * energy_reference
        expected = (
            self.matrix_frobenius_maximum / matrix_scale,
            self.matrix_frobenius_rms / matrix_scale,
            self.ordered_spectrum_maximum / energy_reference,
            self.ordered_spectrum_l2_rms / matrix_scale,
        )
        observed = (
            self.normalized_matrix_frobenius_maximum,
            self.normalized_matrix_frobenius_rms,
            self.normalized_ordered_spectrum_maximum,
            self.normalized_ordered_spectrum_l2_rms,
        )
        if observed != expected:
            raise ValueError("normalized error fields are inconsistent")


@dataclass(frozen=True, slots=True)
class MatrixPerturbationBoundDiagnostics:
    """Retain finite-dimensional eigenvalue and matrix-norm bound diagnostics."""

    energy_reference: float
    maximum_ordered_spectrum_minus_spectral_norm: float
    maximum_ordered_spectrum_minus_frobenius_norm: float
    maximum_spectral_norm_minus_frobenius_norm: float
    normalized_maximum_ordered_spectrum_minus_spectral_norm: float
    normalized_maximum_ordered_spectrum_minus_frobenius_norm: float
    normalized_maximum_spectral_norm_minus_frobenius_norm: float
    saturation_denominator_floor: float
    band_over_spectral_eligible_count: int
    band_over_frobenius_eligible_count: int
    maximum_band_over_spectral_ratio: float | None
    maximum_band_over_frobenius_ratio: float | None

    def __post_init__(self) -> None:
        """Validate bound violations, eligibility, ratios, and normalizations."""
        energy_reference = positive_float("energy_reference", self.energy_reference)
        for name, value in (
            (
                "maximum_ordered_spectrum_minus_spectral_norm",
                self.maximum_ordered_spectrum_minus_spectral_norm,
            ),
            (
                "maximum_ordered_spectrum_minus_frobenius_norm",
                self.maximum_ordered_spectrum_minus_frobenius_norm,
            ),
            (
                "maximum_spectral_norm_minus_frobenius_norm",
                self.maximum_spectral_norm_minus_frobenius_norm,
            ),
            (
                "normalized_maximum_ordered_spectrum_minus_spectral_norm",
                self.normalized_maximum_ordered_spectrum_minus_spectral_norm,
            ),
            (
                "normalized_maximum_ordered_spectrum_minus_frobenius_norm",
                self.normalized_maximum_ordered_spectrum_minus_frobenius_norm,
            ),
            (
                "normalized_maximum_spectral_norm_minus_frobenius_norm",
                self.normalized_maximum_spectral_norm_minus_frobenius_norm,
            ),
            ("saturation_denominator_floor", self.saturation_denominator_floor),
        ):
            nonnegative_float(name, value)
        raw = (
            self.maximum_ordered_spectrum_minus_spectral_norm,
            self.maximum_ordered_spectrum_minus_frobenius_norm,
            self.maximum_spectral_norm_minus_frobenius_norm,
        )
        normalized = (
            self.normalized_maximum_ordered_spectrum_minus_spectral_norm,
            self.normalized_maximum_ordered_spectrum_minus_frobenius_norm,
            self.normalized_maximum_spectral_norm_minus_frobenius_norm,
        )
        if normalized != tuple(value / energy_reference for value in raw):
            raise ValueError("normalized perturbation-bound fields are inconsistent")
        for count_name, ratio_name in (
            (
                "band_over_spectral_eligible_count",
                "maximum_band_over_spectral_ratio",
            ),
            (
                "band_over_frobenius_eligible_count",
                "maximum_band_over_frobenius_ratio",
            ),
        ):
            if count_name == "band_over_spectral_eligible_count":
                count = self.band_over_spectral_eligible_count
                ratio = self.maximum_band_over_spectral_ratio
            else:
                count = self.band_over_frobenius_eligible_count
                ratio = self.maximum_band_over_frobenius_ratio
            if type(count) is not int:
                raise TypeError(f"{count_name} must be a built-in int")
            if count < 0:
                raise ValueError(f"{count_name} must be nonnegative")
            if count == 0:
                if ratio is not None:
                    raise ValueError(f"{ratio_name} must be absent without eligibility")
            else:
                if ratio is None:
                    raise ValueError(f"{ratio_name} is required when eligible")
                nonnegative_float(ratio_name, ratio)


@dataclass(frozen=True, slots=True)
class MatrixFieldComparisonDiagnostics:
    """Combine error summaries with pointwise perturbation-bound diagnostics."""

    errors: MatrixFieldErrorSummary
    perturbation_bounds: MatrixPerturbationBoundDiagnostics

    def __post_init__(self) -> None:
        """Require exact records with one energy reference."""
        if type(self.errors) is not MatrixFieldErrorSummary:
            raise TypeError("errors must be MatrixFieldErrorSummary")
        if type(self.perturbation_bounds) is not MatrixPerturbationBoundDiagnostics:
            raise TypeError(
                "perturbation_bounds must be MatrixPerturbationBoundDiagnostics"
            )
        if self.errors.energy_reference != self.perturbation_bounds.energy_reference:
            raise ValueError("comparison diagnostics must use one energy reference")


def _error_evidence(
    approximation: ComplexArray,
    reference: ComplexArray,
    energy_reference: float,
) -> tuple[MatrixFieldErrorSummary, ComplexArray, FloatArray, FloatArray]:
    """Return one summary and reusable pointwise norm evidence."""
    rank = int(approximation.shape[-1])
    difference = np.asarray(approximation - reference, dtype=np.complex128)
    frobenius = np.asarray(
        np.linalg.norm(difference, axis=(-2, -1)),
        dtype=np.float64,
    )
    approximate_bands = np.linalg.eigvalsh(approximation)
    reference_bands = np.linalg.eigvalsh(reference)
    band_difference = np.asarray(
        np.abs(approximate_bands - reference_bands),
        dtype=np.float64,
    )
    band_maximum = np.asarray(np.max(band_difference, axis=-1), dtype=np.float64)
    band_l2 = np.asarray(
        np.linalg.norm(band_difference, axis=-1),
        dtype=np.float64,
    )
    matrix_scale = math.sqrt(rank) * energy_reference
    matrix_maximum = float(np.max(frobenius))
    matrix_rms = float(np.sqrt(np.mean(frobenius**2)))
    spectrum_maximum = float(np.max(band_difference))
    spectrum_l2_rms = float(np.sqrt(np.mean(band_l2**2)))
    summary = MatrixFieldErrorSummary(
        rank=rank,
        energy_reference=energy_reference,
        matrix_frobenius_maximum=matrix_maximum,
        matrix_frobenius_rms=matrix_rms,
        normalized_matrix_frobenius_maximum=matrix_maximum / matrix_scale,
        normalized_matrix_frobenius_rms=matrix_rms / matrix_scale,
        ordered_spectrum_maximum=spectrum_maximum,
        ordered_spectrum_l2_rms=spectrum_l2_rms,
        normalized_ordered_spectrum_maximum=spectrum_maximum / energy_reference,
        normalized_ordered_spectrum_l2_rms=spectrum_l2_rms / matrix_scale,
    )
    return summary, difference, frobenius, band_maximum


class MatrixFieldErrorAnalyzer:
    """Calculate rank-generic matrix and ordered-spectrum error summaries."""

    __slots__ = ()

    def execute(
        self,
        approximation: ComplexArray,
        reference: ComplexArray,
        energy_reference: float,
    ) -> MatrixFieldErrorSummary:
        """Return raw and normalized errors on any common leading sample shape."""
        approximation = matrix_field("approximation", approximation)
        reference = matrix_field("reference", reference)
        if approximation.shape != reference.shape:
            raise ValueError("approximation and reference shapes must agree")
        energy_reference = positive_float("energy_reference", energy_reference)
        summary, _, _, _ = _error_evidence(
            approximation,
            reference,
            energy_reference,
        )
        return summary


class MatrixFieldComparisonAnalyzer:
    """Compare equally shaped finite Hermitian matrix fields without fitting."""

    __slots__ = ()

    def execute(
        self,
        approximation: ComplexArray,
        reference: ComplexArray,
        energy_reference: float,
        saturation_denominator_floor: float,
    ) -> MatrixFieldComparisonDiagnostics:
        """Return matrix/spectrum errors and Weyl/norm bound diagnostics.

        The inputs may have any nonempty leading sample shape. Matrices are interpreted
        pointwise. Hermitian eigenvalues are evaluated with ``numpy.linalg.eigvalsh``;
        the caller owns any scientific assertion that the supplied fields are Hermitian.
        """
        approximation = matrix_field("approximation", approximation)
        reference = matrix_field("reference", reference)
        if approximation.shape != reference.shape:
            raise ValueError("approximation and reference shapes must agree")
        energy_reference = positive_float("energy_reference", energy_reference)
        floor = nonnegative_float(
            "saturation_denominator_floor", saturation_denominator_floor
        )
        errors, difference, frobenius, band_maximum = _error_evidence(
            approximation,
            reference,
            energy_reference,
        )
        spectral = np.asarray(
            np.linalg.norm(difference, ord=2, axis=(-2, -1)),
            dtype=np.float64,
        )
        violation_band_spectral = np.maximum(0.0, band_maximum - spectral)
        violation_band_frobenius = np.maximum(0.0, band_maximum - frobenius)
        violation_spectral_frobenius = np.maximum(0.0, spectral - frobenius)
        spectral_eligible = spectral > floor
        frobenius_eligible = frobenius > floor
        spectral_ratio = (
            float(np.max(band_maximum[spectral_eligible] / spectral[spectral_eligible]))
            if bool(np.any(spectral_eligible))
            else None
        )
        frobenius_ratio = (
            float(
                np.max(band_maximum[frobenius_eligible] / frobenius[frobenius_eligible])
            )
            if bool(np.any(frobenius_eligible))
            else None
        )
        raw_violations = (
            float(np.max(violation_band_spectral)),
            float(np.max(violation_band_frobenius)),
            float(np.max(violation_spectral_frobenius)),
        )
        bounds = MatrixPerturbationBoundDiagnostics(
            energy_reference=energy_reference,
            maximum_ordered_spectrum_minus_spectral_norm=raw_violations[0],
            maximum_ordered_spectrum_minus_frobenius_norm=raw_violations[1],
            maximum_spectral_norm_minus_frobenius_norm=raw_violations[2],
            normalized_maximum_ordered_spectrum_minus_spectral_norm=(
                raw_violations[0] / energy_reference
            ),
            normalized_maximum_ordered_spectrum_minus_frobenius_norm=(
                raw_violations[1] / energy_reference
            ),
            normalized_maximum_spectral_norm_minus_frobenius_norm=(
                raw_violations[2] / energy_reference
            ),
            saturation_denominator_floor=floor,
            band_over_spectral_eligible_count=int(np.count_nonzero(spectral_eligible)),
            band_over_frobenius_eligible_count=int(
                np.count_nonzero(frobenius_eligible)
            ),
            maximum_band_over_spectral_ratio=spectral_ratio,
            maximum_band_over_frobenius_ratio=frobenius_ratio,
        )
        return MatrixFieldComparisonDiagnostics(errors, bounds)


@dataclass(frozen=True, slots=True)
class MatrixErrorDecompositionDiagnostics:
    """Retain the maximum defect in ``total = interpolation + truncation``."""

    rank: int
    energy_reference: float
    maximum_frobenius_defect: float
    normalized_maximum_frobenius_defect: float

    def __post_init__(self) -> None:
        """Validate rank, values, and the declared normalization."""
        if type(self.rank) is not int:
            raise TypeError("rank must be a built-in int")
        if self.rank <= 0:
            raise ValueError("rank must be positive")
        energy_reference = positive_float("energy_reference", self.energy_reference)
        defect = nonnegative_float(
            "maximum_frobenius_defect", self.maximum_frobenius_defect
        )
        normalized = nonnegative_float(
            "normalized_maximum_frobenius_defect",
            self.normalized_maximum_frobenius_defect,
        )
        expected = defect / (math.sqrt(self.rank) * energy_reference)
        if normalized != expected:
            raise ValueError("normalized decomposition defect is inconsistent")


class MatrixErrorDecompositionAnalyzer:
    """Check an explicitly supplied interpolation/truncation/total decomposition."""

    __slots__ = ()

    def execute(
        self,
        interpolation_error: ComplexArray,
        truncation_error: ComplexArray,
        total_error: ComplexArray,
        energy_reference: float,
    ) -> MatrixErrorDecompositionDiagnostics:
        """Return the maximum pointwise Frobenius identity defect."""
        interpolation_error = matrix_field("interpolation_error", interpolation_error)
        truncation_error = matrix_field("truncation_error", truncation_error)
        total_error = matrix_field("total_error", total_error)
        if not (
            interpolation_error.shape == truncation_error.shape == total_error.shape
        ):
            raise ValueError("all error fields must have one shape")
        energy_reference = positive_float("energy_reference", energy_reference)
        rank = int(total_error.shape[-1])
        residual = total_error - interpolation_error - truncation_error
        defect = float(np.max(np.linalg.norm(residual, axis=(-2, -1))))
        return MatrixErrorDecompositionDiagnostics(
            rank=rank,
            energy_reference=energy_reference,
            maximum_frobenius_defect=defect,
            normalized_maximum_frobenius_defect=(
                defect / (math.sqrt(rank) * energy_reference)
            ),
        )


__all__ = [
    "MatrixErrorDecompositionAnalyzer",
    "MatrixErrorDecompositionDiagnostics",
    "MatrixFieldComparisonAnalyzer",
    "MatrixFieldComparisonDiagnostics",
    "MatrixFieldErrorAnalyzer",
    "MatrixFieldErrorSummary",
    "MatrixPerturbationBoundDiagnostics",
]
