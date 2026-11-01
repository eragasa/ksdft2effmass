"""Matrix/spectrum errors, perturbation bounds, and error decompositions."""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np
from projectkoios.numerics.validation import exact_nonnegative_float

from ..normalization import positive_norm_energy_scale
from ..validation import ComplexArray, matrix_field


@dataclass(frozen=True, slots=True)
class MatrixFieldErrorSummary:
    """Retain raw and rank/energy-normalized matrix and spectral errors.

    ``matrix_frobenius_rms`` and ``ordered_spectrum_l2_rms`` are root-mean-square
    pointwise norms. Their normalized forms divide by
    ``sqrt(rank) * norm_energy_scale``. The ordered-spectrum maximum is a
    componentwise maximum and divides only by the positive normalization energy scale.
    """

    rank: int
    norm_energy_scale: float
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
        norm_energy_scale = positive_norm_energy_scale(self.norm_energy_scale)
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
            exact_nonnegative_float(value, name)
        matrix_scale = math.sqrt(self.rank) * norm_energy_scale
        expected = (
            self.matrix_frobenius_maximum / matrix_scale,
            self.matrix_frobenius_rms / matrix_scale,
            self.ordered_spectrum_maximum / norm_energy_scale,
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

    norm_energy_scale: float
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
        norm_energy_scale = positive_norm_energy_scale(self.norm_energy_scale)
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
            exact_nonnegative_float(value, name)
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
        if normalized != tuple(value / norm_energy_scale for value in raw):
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
                exact_nonnegative_float(ratio, ratio_name)


@dataclass(frozen=True, slots=True)
class MatrixFieldComparisonDiagnostics:
    """Combine error summaries with pointwise perturbation-bound diagnostics."""

    errors: MatrixFieldErrorSummary
    perturbation_bounds: MatrixPerturbationBoundDiagnostics

    def __post_init__(self) -> None:
        """Require exact records with one normalization energy scale."""
        if type(self.errors) is not MatrixFieldErrorSummary:
            raise TypeError("errors must be MatrixFieldErrorSummary")
        if type(self.perturbation_bounds) is not MatrixPerturbationBoundDiagnostics:
            raise TypeError(
                "perturbation_bounds must be MatrixPerturbationBoundDiagnostics"
            )
        if self.errors.norm_energy_scale != self.perturbation_bounds.norm_energy_scale:
            raise ValueError(
                "comparison diagnostics must use one normalization energy scale"
            )


class MatrixFieldErrorAnalyzer:
    """Calculate errors for one immutable, constructor-bound matrix-field pair."""

    __slots__ = ("_approximation", "_norm_energy_scale", "_reference")

    def __init__(
        self,
        *,
        approximation: ComplexArray,
        reference: ComplexArray,
        norm_energy_scale: float,
    ) -> None:
        approximation_value = matrix_field("approximation", approximation)
        reference_value = matrix_field("reference", reference)
        if approximation_value.shape != reference_value.shape:
            raise ValueError("approximation and reference shapes must agree")
        self._approximation = np.array(
            approximation_value,
            dtype=np.complex128,
            copy=True,
        )
        self._approximation.flags.writeable = False
        self._reference = np.array(
            reference_value,
            dtype=np.complex128,
            copy=True,
        )
        self._reference.flags.writeable = False
        self._norm_energy_scale = positive_norm_energy_scale(norm_energy_scale)

    def result(self) -> MatrixFieldErrorSummary:
        """Return raw and normalized errors on the bound common sample shape."""
        rank = int(self._approximation.shape[-1])
        difference = np.asarray(
            self._approximation - self._reference,
            dtype=np.complex128,
        )
        frobenius = np.asarray(
            np.linalg.norm(difference, axis=(-2, -1)),
            dtype=np.float64,
        )
        band_difference = np.asarray(
            np.abs(
                np.linalg.eigvalsh(self._approximation)
                - np.linalg.eigvalsh(self._reference)
            ),
            dtype=np.float64,
        )
        band_l2 = np.asarray(
            np.linalg.norm(band_difference, axis=-1),
            dtype=np.float64,
        )
        matrix_scale = math.sqrt(rank) * self._norm_energy_scale
        matrix_maximum = float(np.max(frobenius))
        matrix_rms = float(np.sqrt(np.mean(frobenius**2)))
        spectrum_maximum = float(np.max(band_difference))
        spectrum_l2_rms = float(np.sqrt(np.mean(band_l2**2)))
        return MatrixFieldErrorSummary(
            rank=rank,
            norm_energy_scale=self._norm_energy_scale,
            matrix_frobenius_maximum=matrix_maximum,
            matrix_frobenius_rms=matrix_rms,
            normalized_matrix_frobenius_maximum=matrix_maximum / matrix_scale,
            normalized_matrix_frobenius_rms=matrix_rms / matrix_scale,
            ordered_spectrum_maximum=spectrum_maximum,
            ordered_spectrum_l2_rms=spectrum_l2_rms,
            normalized_ordered_spectrum_maximum=(
                spectrum_maximum / self._norm_energy_scale
            ),
            normalized_ordered_spectrum_l2_rms=spectrum_l2_rms / matrix_scale,
        )


class MatrixFieldComparisonAnalyzer:
    """Compare one bound pair of equally shaped finite Hermitian matrix fields."""

    __slots__ = (
        "_approximation",
        "_norm_energy_scale",
        "_reference",
        "_saturation_denominator_floor",
    )

    def __init__(
        self,
        *,
        approximation: ComplexArray,
        reference: ComplexArray,
        norm_energy_scale: float,
        saturation_denominator_floor: float,
    ) -> None:
        approximation_value = matrix_field("approximation", approximation)
        reference_value = matrix_field("reference", reference)
        if approximation_value.shape != reference_value.shape:
            raise ValueError("approximation and reference shapes must agree")
        self._approximation = np.array(
            approximation_value,
            dtype=np.complex128,
            copy=True,
        )
        self._approximation.flags.writeable = False
        self._reference = np.array(reference_value, dtype=np.complex128, copy=True)
        self._reference.flags.writeable = False
        self._norm_energy_scale = positive_norm_energy_scale(norm_energy_scale)
        self._saturation_denominator_floor = exact_nonnegative_float(
            saturation_denominator_floor,
            "saturation_denominator_floor",
        )

    def execute(self) -> MatrixFieldComparisonDiagnostics:
        """Return matrix/spectrum errors and Weyl/norm bound diagnostics.

        The bound inputs may have any nonempty leading sample shape. Matrices are
        interpreted pointwise. Hermitian eigenvalues are evaluated with
        ``numpy.linalg.eigvalsh``; the caller owns any scientific assertion that the
        supplied fields are Hermitian.
        """
        difference = np.asarray(
            self._approximation - self._reference,
            dtype=np.complex128,
        )
        frobenius = np.asarray(
            np.linalg.norm(difference, axis=(-2, -1)),
            dtype=np.float64,
        )
        band_difference = np.asarray(
            np.abs(
                np.linalg.eigvalsh(self._approximation)
                - np.linalg.eigvalsh(self._reference)
            ),
            dtype=np.float64,
        )
        band_maximum = np.asarray(
            np.max(band_difference, axis=-1),
            dtype=np.float64,
        )
        errors = MatrixFieldErrorAnalyzer(
            approximation=self._approximation,
            reference=self._reference,
            norm_energy_scale=self._norm_energy_scale,
        ).result()
        spectral = np.asarray(
            np.linalg.norm(difference, ord=2, axis=(-2, -1)),
            dtype=np.float64,
        )
        violation_band_spectral = np.maximum(0.0, band_maximum - spectral)
        violation_band_frobenius = np.maximum(0.0, band_maximum - frobenius)
        violation_spectral_frobenius = np.maximum(0.0, spectral - frobenius)
        spectral_eligible = spectral > self._saturation_denominator_floor
        frobenius_eligible = frobenius > self._saturation_denominator_floor
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
            norm_energy_scale=self._norm_energy_scale,
            maximum_ordered_spectrum_minus_spectral_norm=raw_violations[0],
            maximum_ordered_spectrum_minus_frobenius_norm=raw_violations[1],
            maximum_spectral_norm_minus_frobenius_norm=raw_violations[2],
            normalized_maximum_ordered_spectrum_minus_spectral_norm=(
                raw_violations[0] / self._norm_energy_scale
            ),
            normalized_maximum_ordered_spectrum_minus_frobenius_norm=(
                raw_violations[1] / self._norm_energy_scale
            ),
            normalized_maximum_spectral_norm_minus_frobenius_norm=(
                raw_violations[2] / self._norm_energy_scale
            ),
            saturation_denominator_floor=self._saturation_denominator_floor,
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
    norm_energy_scale: float
    maximum_frobenius_defect: float
    normalized_maximum_frobenius_defect: float

    def __post_init__(self) -> None:
        """Validate rank, values, and the declared normalization."""
        if type(self.rank) is not int:
            raise TypeError("rank must be a built-in int")
        if self.rank <= 0:
            raise ValueError("rank must be positive")
        norm_energy_scale = positive_norm_energy_scale(self.norm_energy_scale)
        defect = exact_nonnegative_float(
            self.maximum_frobenius_defect, "maximum_frobenius_defect"
        )
        normalized = exact_nonnegative_float(
            self.normalized_maximum_frobenius_defect,
            "normalized_maximum_frobenius_defect",
        )
        expected = defect / (math.sqrt(self.rank) * norm_energy_scale)
        if normalized != expected:
            raise ValueError("normalized decomposition defect is inconsistent")


class MatrixErrorDecompositionAnalyzer:
    """Check one bound interpolation/truncation/total error decomposition."""

    __slots__ = (
        "_norm_energy_scale",
        "_interpolation_error",
        "_total_error",
        "_truncation_error",
    )

    def __init__(
        self,
        *,
        interpolation_error: ComplexArray,
        truncation_error: ComplexArray,
        total_error: ComplexArray,
        norm_energy_scale: float,
    ) -> None:
        interpolation_value = matrix_field(
            "interpolation_error",
            interpolation_error,
        )
        truncation_value = matrix_field("truncation_error", truncation_error)
        total_value = matrix_field("total_error", total_error)
        if not (
            interpolation_value.shape == truncation_value.shape == total_value.shape
        ):
            raise ValueError("all error fields must have one shape")
        self._interpolation_error = np.array(
            interpolation_value,
            dtype=np.complex128,
            copy=True,
        )
        self._interpolation_error.flags.writeable = False
        self._truncation_error = np.array(
            truncation_value,
            dtype=np.complex128,
            copy=True,
        )
        self._truncation_error.flags.writeable = False
        self._total_error = np.array(total_value, dtype=np.complex128, copy=True)
        self._total_error.flags.writeable = False
        self._norm_energy_scale = positive_norm_energy_scale(norm_energy_scale)

    def execute(self) -> MatrixErrorDecompositionDiagnostics:
        """Return the maximum pointwise Frobenius identity defect."""
        rank = int(self._total_error.shape[-1])
        residual = (
            self._total_error - self._interpolation_error - self._truncation_error
        )
        defect = float(np.max(np.linalg.norm(residual, axis=(-2, -1))))
        return MatrixErrorDecompositionDiagnostics(
            rank=rank,
            norm_energy_scale=self._norm_energy_scale,
            maximum_frobenius_defect=defect,
            normalized_maximum_frobenius_defect=(
                defect / (math.sqrt(rank) * self._norm_energy_scale)
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
