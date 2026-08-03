r"""Residual metric analysis for represented operator differences.

This module owns residual norm computation for an already constructed
:class:`~ksdft2effmass.operators.difference.OperatorRecordDifferenceResult` in
the decomposition ``compatibility -> represented difference -> residual analysis
-> comparison Workflow``.  It does not inspect raw operator records, enforce
compatibility, subtract matrices, align bases, convert units, or attach impurity
interpretations.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

import numpy as np

from .difference import OperatorRecordDifferenceResult


@dataclass(frozen=True, slots=True)
class OperatorRecordComparisonResult:
    r"""Immutable structural residual metrics for a represented difference.

    Parameters
    ----------
    reference_identifier
        Nonempty identifier of the reference record carried through the
        compatibility and difference results. It is provenance for the metric
        report and is not used in numerical calculation.
    candidate_identifier
        Nonempty identifier of the candidate record carried through the
        compatibility and difference results. It is provenance for the metric
        report and is not used in numerical calculation.
    matrix_dimension
        Positive represented dimension ``N`` of the square difference matrix.
        Python ``int`` and NumPy integer scalars are accepted and canonicalized
        to built-in ``int``. Booleans, strings, floats, complex numbers, and
        nonpositive integers are rejected.
    energy_unit
        Nonempty common energy-unit string for all metric fields. This object
        performs no unit conversion and stores no energy-zero policy.
    maximum_absolute_residual
        Entrywise maximum residual :math:`\varepsilon_{\max}` in
        ``energy_unit``. Accepted Python and NumPy real scalars are
        canonicalized to built-in ``float``; booleans, strings, complex values,
        nonfinite values, and negative values are rejected.
    frobenius_residual
        Frobenius residual :math:`\varepsilon_{\mathrm F}` in ``energy_unit``.
        The accepted scalar taxonomy and canonical storage match
        ``maximum_absolute_residual``.
    spectral_residual
        Induced matrix 2-norm residual :math:`\varepsilon_2` in ``energy_unit``.
        The accepted scalar taxonomy and canonical storage match
        ``maximum_absolute_residual``.

    Raises
    ------
    TypeError
        If a string field is not a string, ``matrix_dimension`` is not an
        integer scalar, or a metric is not an accepted real scalar. Booleans and
        numeric strings are rejected rather than coerced.
    ValueError
        If a string field is empty, ``matrix_dimension`` is nonpositive, a
        metric is nonfinite or negative, scalar conversion overflows, or the
        exact stored ordering
        ``maximum_absolute_residual <= spectral_residual <= frobenius_residual``
        is violated.

    Notes
    -----
    This ResultObject is structural only. It owns scalar field validation,
    canonical Python scalar storage, and exact stored metric-order invariants.
    It does not own matrix operations, machine-epsilon policy, numerical error
    estimates, roundoff repair, or maximum-dimension limits; those policies
    belong to :class:`OperatorRecordResidualAnalyzer`.
    """

    reference_identifier: str
    candidate_identifier: str
    matrix_dimension: int
    energy_unit: str
    maximum_absolute_residual: float
    frobenius_residual: float
    spectral_residual: float

    def __post_init__(self) -> None:
        """Canonicalize fields and validate structural metric invariants.

        Raises
        ------
        TypeError
            If identifiers or ``energy_unit`` are not strings,
            ``matrix_dimension`` is not a Python or NumPy integer scalar, or any
            residual metric is not an accepted Python or NumPy real scalar.
            Booleans, numeric strings, bytes, and complex scalars are rejected
            rather than coerced.
        ValueError
            If a string field is empty, ``matrix_dimension`` is nonpositive, a
            metric is negative or nonfinite, scalar conversion overflows, or the
            exact stored ordering
            ``maximum_absolute_residual <= spectral_residual <= frobenius_residual``
            is violated.

        Notes
        -----
        This private dataclass hook owns only intrinsic structural validation of
        the immutable ResultObject and canonical Python scalar storage. It does
        not perform matrix operations, estimate numerical roundoff, repair metric
        ordering, or impose analyzer policy; those responsibilities belong to
        ``OperatorRecordResidualAnalyzer``.
        """

        self._require_string(self.reference_identifier, "reference identifier")
        self._require_string(self.candidate_identifier, "candidate identifier")
        self._require_string(self.energy_unit, "energy unit")
        if isinstance(self.matrix_dimension, bool) or not isinstance(
            self.matrix_dimension, int | np.integer
        ):
            msg = "matrix_dimension must be a positive integer"
            raise TypeError(msg)
        matrix_dimension = int(self.matrix_dimension)
        if matrix_dimension <= 0:
            msg = "matrix_dimension must be positive"
            raise ValueError(msg)
        object.__setattr__(self, "matrix_dimension", matrix_dimension)
        for field_name in (
            "maximum_absolute_residual",
            "frobenius_residual",
            "spectral_residual",
        ):
            canonical_metric = self._finite_nonnegative_real(
                getattr(self, field_name), field_name
            )
            object.__setattr__(self, field_name, canonical_metric)
        if self.maximum_absolute_residual > self.spectral_residual:
            msg = "maximum_absolute_residual must not exceed spectral_residual"
            raise ValueError(msg)
        if self.spectral_residual > self.frobenius_residual:
            msg = "spectral_residual must not exceed frobenius_residual"
            raise ValueError(msg)

    @staticmethod
    def _require_string(value: object, name: str) -> None:
        """Validate a nonempty public string field owned by this result.

        Parameters
        ----------
        value
            Candidate public identifier or unit value. Numeric-looking strings
            remain strings; non-strings are rejected instead of converted.
        name
            Human-readable field name for deterministic diagnostics.

        Raises
        ------
        TypeError
            If ``value`` is not a string.
        ValueError
            If ``value`` is empty.
        """

        if not isinstance(value, str):
            msg = f"{name} must be a string"
            raise TypeError(msg)
        if value == "":
            msg = f"{name} must not be empty"
            raise ValueError(msg)

    @staticmethod
    def _finite_nonnegative_real(value: object, name: str) -> float:
        """Return a canonical finite non-negative Python float.

        Parameters
        ----------
        value
            Candidate metric scalar. Python and NumPy integer or floating
            scalars are accepted. Booleans, strings, bytes, complex scalars,
            nonnumeric objects, nonfinite values, and negative values are
            rejected at the public Python/Rust boundary.
        name
            Metric field name used in exception messages.

        Returns
        -------
        float
            Built-in Python scalar stored on the immutable ResultObject.

        Raises
        ------
        TypeError
            If ``value`` is not an accepted real scalar type.
        ValueError
            If ``value`` is nonfinite, negative, or cannot be represented as a
            finite binary64 value.
        """

        if isinstance(
            value, bool | np.bool_ | str | bytes | complex | np.complexfloating
        ):
            msg = f"{name} must be a real number"
            raise TypeError(msg)
        if not isinstance(value, int | float | np.integer | np.floating):
            msg = f"{name} must be a real number"
            raise TypeError(msg)
        try:
            real = float(value)
        except OverflowError as exc:
            msg = f"{name} must be finite"
            raise ValueError(msg) from exc
        if not np.isfinite(real):
            msg = f"{name} must be finite"
            raise ValueError(msg)
        if real < 0.0:
            msg = f"{name} must be non-negative"
            raise ValueError(msg)
        return real


class OperatorRecordComparisonNumericalErrorCode(StrEnum):
    r"""Stable residual-analysis numerical-error categories.

    Attributes
    ----------
    NONFINITE_METRIC
        A residual metric calculation produced a nonfinite scalar after the
        represented difference itself was already finite.
    LINEAR_ALGEBRA_FAILURE
        Singular-value computation failed or returned nonfinite singular values
        while computing :math:`\varepsilon_2`.
    METRIC_ORDER_VIOLATION
        Independently computed raw norms violated
        ``epsilon_max <= epsilon_2 <= epsilon_F`` by more than the
        analyzer-owned roundoff allowance.
    """

    NONFINITE_METRIC = "nonfinite_metric"
    LINEAR_ALGEBRA_FAILURE = "linear_algebra_failure"
    METRIC_ORDER_VIOLATION = "metric_order_violation"


class OperatorRecordComparisonNumericalError(ValueError):
    """Raised when residual metric computation fails numerically.

    Parameters
    ----------
    code
        Closed structured enum code identifying the residual-analysis failure.
        Arbitrary strings are rejected so Python behavior maps directly to a
        future Rust error enum.

    Attributes
    ----------
    code
        Public structured residual-analysis code.
    Raises
    ------
    TypeError
        If ``code`` is not an
        :class:`OperatorRecordComparisonNumericalErrorCode`.
    """

    code: OperatorRecordComparisonNumericalErrorCode

    def __init__(self, code: OperatorRecordComparisonNumericalErrorCode) -> None:
        """Retain the structured residual-analysis enum code."""

        if not isinstance(code, OperatorRecordComparisonNumericalErrorCode):
            msg = (
                "comparison numerical-error code must be an "
                "OperatorRecordComparisonNumericalErrorCode"
            )
            raise TypeError(msg)
        self.code = code
        super().__init__(f"operator-record residual numerical failure: {code.value}")


@dataclass(frozen=True, slots=True)
class OperatorRecordResidualAnalyzer:
    r"""ActionObject that computes residual norms from a represented difference.

    The analyzer computes :math:`\varepsilon_{\max}` as the entrywise maximum,
    :math:`\varepsilon_{\mathrm F}` with scale-safe sum of squares, and
    :math:`\varepsilon_2` by singular-value analysis after power-of-two scaling.
    Direct complex division by a subnormal scale is avoided because it can
    overflow inside NumPy's complex division even when the mathematically scaled
    matrix is finite.  For binary exponent ``e`` obtained from the finite scale,

    .. math::

       \widetilde{\mathbf H}=2^{-e}\Delta\mathbf H,
       \qquad
       \|\Delta\mathbf H\|_2=2^e\|\widetilde{\mathbf H}\|_2.

    Raw norm ordering is allowed to differ only within an allowance containing a
    relative component and a lower-ULP component. Exact zero metrics receive zero
    allowance. Within allowance, ``epsilon_2`` and ``epsilon_F`` are
    canonicalized upward; true nonrepresentable metrics raise structured
    numerical errors. These are software-verification metrics, not scientific
    acceptance thresholds.
    """

    def execute(
        self, difference: OperatorRecordDifferenceResult
    ) -> OperatorRecordComparisonResult:
        r"""Return residual metrics for a represented operator difference.

        Parameters
        ----------
        difference
            Public represented-difference result containing the finite
            ``np.complex128`` matrix :math:`\Delta\mathbf H`, common energy unit,
            and provenance identifiers.

        Returns
        -------
        OperatorRecordComparisonResult
            Structural metric result containing :math:`\varepsilon_{\max}`,
            :math:`\varepsilon_{\mathrm F}`, and :math:`\varepsilon_2` in the
            difference energy unit.

        Raises
        ------
        TypeError
            If ``difference`` is not an
            :class:`OperatorRecordDifferenceResult`.
        OperatorRecordComparisonNumericalError
            If a metric is nonfinite, singular-value computation fails, or raw
            metric ordering violates the mathematical norm inequalities by more
            than analyzer-owned roundoff allowance.
        """

        if not isinstance(difference, OperatorRecordDifferenceResult):
            msg = "difference must be an OperatorRecordDifferenceResult"
            raise TypeError(msg)
        # Compute the three public norms independently so each algorithm remains
        # auditable; any ordering repair is handled only after all raw metrics
        # exist in the common energy unit.
        maximum_absolute_residual = self._maximum_absolute_residual(difference.matrix)
        frobenius_residual = self._scale_safe_frobenius_norm(difference.matrix)
        spectral_residual = self._scale_safe_spectral_norm(difference.matrix)
        (
            maximum_absolute_residual,
            spectral_residual,
            frobenius_residual,
        ) = self._canonicalize_metric_order_for_roundoff(
            maximum_absolute_residual=maximum_absolute_residual,
            spectral_residual=spectral_residual,
            frobenius_residual=frobenius_residual,
            matrix_dimension=difference.matrix_dimension,
        )
        return OperatorRecordComparisonResult(
            reference_identifier=difference.reference_identifier,
            candidate_identifier=difference.candidate_identifier,
            matrix_dimension=difference.matrix_dimension,
            energy_unit=difference.energy_unit,
            maximum_absolute_residual=maximum_absolute_residual,
            frobenius_residual=frobenius_residual,
            spectral_residual=spectral_residual,
        )

    @classmethod
    def _canonicalize_metric_order_for_roundoff(
        cls,
        *,
        maximum_absolute_residual: float,
        spectral_residual: float,
        frobenius_residual: float,
        matrix_dimension: int,
    ) -> tuple[float, float, float]:
        r"""Canonicalize norm ordering or raise for material inversions.

        Parameters
        ----------
        maximum_absolute_residual
            Raw :math:`\varepsilon_{\max}` metric in the common energy unit.
        spectral_residual
            Raw :math:`\varepsilon_2` metric in the common energy unit.
        frobenius_residual
            Raw :math:`\varepsilon_{\mathrm F}` metric in the common energy
            unit.
        matrix_dimension
            Positive represented dimension ``N`` used only in the
            dimensionless roundoff factor.

        Returns
        -------
        tuple[float, float, float]
            ``(maximum, spectral, frobenius)`` metrics canonicalized upward when
            raw ordering differences are within analyzer-owned roundoff.

        Raises
        ------
        OperatorRecordComparisonNumericalError
            If a raw metric-order inversion exceeds the dimensionally
            consistent allowance.

        Notes
        -----
        This private helper owns residual-analyzer numerical policy. The common
        metric scale carries the shared energy unit. The allowance is the larger
        of a relative component and a lower-ULP component, avoiding a zero
        allowance for positive subnormal metrics without introducing a public
        scientific acceptance threshold.
        """

        common_metric_scale = max(
            maximum_absolute_residual, spectral_residual, frobenius_residual
        )
        allowance = cls._metric_order_allowance(
            matrix_dimension=matrix_dimension,
            common_metric_scale=common_metric_scale,
        )
        if maximum_absolute_residual > spectral_residual:
            if maximum_absolute_residual - spectral_residual > allowance:
                raise OperatorRecordComparisonNumericalError(
                    OperatorRecordComparisonNumericalErrorCode.METRIC_ORDER_VIOLATION
                )
            spectral_residual = maximum_absolute_residual
        if spectral_residual > frobenius_residual:
            if spectral_residual - frobenius_residual > allowance:
                raise OperatorRecordComparisonNumericalError(
                    OperatorRecordComparisonNumericalErrorCode.METRIC_ORDER_VIOLATION
                )
            frobenius_residual = spectral_residual
        return maximum_absolute_residual, spectral_residual, frobenius_residual

    @staticmethod
    def _metric_order_allowance(
        *, matrix_dimension: int, common_metric_scale: float
    ) -> float:
        """Return dimensionally consistent unit-bearing roundoff allowance.

        Parameters
        ----------
        matrix_dimension
            Positive represented dimension controlling the dimensionless factor
            ``4 * max(1, N)``.
        common_metric_scale
            Largest raw residual metric, carrying the common energy unit.

        Returns
        -------
        float
            Unit-bearing allowance in the same energy unit as the metrics.

        Raises
        ------
        OperatorRecordComparisonNumericalError
            If allowance arithmetic produces a nonfinite value for a positive
            finite metric scale.

        Notes
        -----
        The allowance is ``max(relative_allowance, ulp_allowance)`` where
        ``relative_allowance = 4 * max(1, N) * eps * common_metric_scale`` and
        ``ulp_allowance = 4 * max(1, N) * lower_ulp``. The lower ULP is computed
        as ``common_metric_scale - nextafter(common_metric_scale, 0.0)`` rather
        than ``np.spacing`` so the calculation is well-defined near the largest
        finite float. A zero scale produces zero allowance.
        """

        if common_metric_scale == 0.0:
            return 0.0
        dimension_factor = 4.0 * max(1, matrix_dimension)
        with np.errstate(over="ignore", under="ignore", invalid="ignore"):
            lower_neighbor = float(np.nextafter(common_metric_scale, 0.0))
            lower_ulp = common_metric_scale - lower_neighbor
            relative_allowance = (
                dimension_factor * np.finfo(np.float64).eps * common_metric_scale
            )
            ulp_allowance = dimension_factor * lower_ulp
            allowance = max(relative_allowance, ulp_allowance)
        if not np.isfinite(allowance):
            raise OperatorRecordComparisonNumericalError(
                OperatorRecordComparisonNumericalErrorCode.NONFINITE_METRIC
            )
        return allowance

    @staticmethod
    def _maximum_absolute_residual(matrix: np.ndarray) -> float:
        r"""Return finite entrywise maximum magnitude.

        Parameters
        ----------
        matrix
            Finite square complex represented-difference matrix in the common
            energy unit. The public ``OperatorRecordDifferenceResult`` owns the
            dtype, shape, finiteness, and immutability checks before this helper
            is called.

        Returns
        -------
        float
            Built-in finite non-negative :math:`\varepsilon_{\max}` value in the
            common energy unit.

        Raises
        ------
        OperatorRecordComparisonNumericalError
            If the absolute-value reduction produces a nonfinite metric.

        Notes
        -----
        This private helper owns only the public maximum-entry residual
        definition and residual-analysis nonfinite metric detection.
        """

        # Absolute values convert complex signed entries into the magnitudes used
        # by epsilon_max while preserving the matrix energy unit.
        maximum = float(np.max(np.abs(matrix)))
        if not np.isfinite(maximum):
            raise OperatorRecordComparisonNumericalError(
                OperatorRecordComparisonNumericalErrorCode.NONFINITE_METRIC
            )
        return maximum

    @staticmethod
    def _scale_safe_frobenius_norm(matrix: np.ndarray) -> float:
        r"""Return scale-safe Frobenius norm.

        Parameters
        ----------
        matrix
            Finite square complex represented-difference matrix in the common
            energy unit. The accepted-input scope is a matrix already validated
            by ``OperatorRecordDifferenceResult``.

        Returns
        -------
        float
            Built-in finite non-negative :math:`\varepsilon_{\mathrm F}` value in
            the common energy unit.

        Raises
        ------
        OperatorRecordComparisonNumericalError
            If scaling or the scaled sum-of-squares reduction produces a
            nonfinite metric.

        Notes
        -----
        Scaling by the largest entry magnitude avoids avoidable overflow for
        large finite matrices and avoidable underflow for small finite matrices.
        The scaled sum is dimensionless and multiplication by ``scale`` restores
        the common energy unit. This private helper is not a general norm API.
        """

        magnitudes = np.abs(matrix)
        # ``scale`` is the unit-bearing factor extracted before squaring; zero
        # scale means every represented difference entry is exactly zero.
        scale = float(np.max(magnitudes))
        if scale == 0.0:
            return 0.0
        if not np.isfinite(scale):
            raise OperatorRecordComparisonNumericalError(
                OperatorRecordComparisonNumericalErrorCode.NONFINITE_METRIC
            )
        # ``scaled`` is dimensionless, so the sum of squares cannot overflow
        # merely because the original unit-bearing matrix entries were large.
        scaled = magnitudes / scale
        norm = scale * float(np.sqrt(np.sum(scaled * scaled)))
        if not np.isfinite(norm):
            raise OperatorRecordComparisonNumericalError(
                OperatorRecordComparisonNumericalErrorCode.NONFINITE_METRIC
            )
        return norm

    @staticmethod
    def _scale_safe_spectral_norm(matrix: np.ndarray) -> float:
        r"""Return scale-safe spectral norm by singular-value analysis.

        Parameters
        ----------
        matrix
            Finite square complex represented-difference matrix in the common
            energy unit. The accepted-input scope is a matrix already validated
            by ``OperatorRecordDifferenceResult``.

        Returns
        -------
        float
            Built-in finite non-negative :math:`\varepsilon_2` value in the
            common energy unit.

        Raises
        ------
        OperatorRecordComparisonNumericalError
            If scaling is nonfinite, singular-value computation raises
            ``np.linalg.LinAlgError``, singular values are nonfinite, or the
            rescaled spectral norm is nonfinite.

        Notes
        -----
        Singular values are computed on a dimensionless matrix scaled by an
        exact power of two, not by complex division through a possibly subnormal
        scale. If ``scale = m 2^e`` from ``np.frexp``, the helper forms
        ``2^-e * matrix`` with ``np.ldexp`` applied separately to real and
        imaginary parts, computes the dimensionless singular values, and restores
        the unit-bearing norm with ``np.ldexp(raw_norm, e)``. Linear algebra
        failures, nonfinite scaled matrices, nonfinite singular values, and true
        nonrepresentable restored norms are mapped to the closed
        residual-analysis error enum.
        """

        magnitudes = np.abs(matrix)
        # The same largest-entry scale used for Frobenius norm makes the SVD
        # input dimensionless while preserving exact zero handling.
        scale = float(np.max(magnitudes))
        if scale == 0.0:
            return 0.0
        if not np.isfinite(scale):
            raise OperatorRecordComparisonNumericalError(
                OperatorRecordComparisonNumericalErrorCode.NONFINITE_METRIC
            )
        _, exponent = np.frexp(scale)
        with np.errstate(over="ignore", under="ignore", invalid="ignore"):
            scaled_real = np.ldexp(matrix.real, -exponent)
            scaled_imag = np.ldexp(matrix.imag, -exponent)
            scaled_matrix = scaled_real + 1j * scaled_imag
        if not np.all(np.isfinite(scaled_matrix)):
            raise OperatorRecordComparisonNumericalError(
                OperatorRecordComparisonNumericalErrorCode.NONFINITE_METRIC
            )
        try:
            # Singular values of the power-of-two scaled matrix are
            # dimensionless; the largest value becomes epsilon_2 after exact
            # exponent restoration.
            singular_values = np.linalg.svd(scaled_matrix, compute_uv=False)
        except np.linalg.LinAlgError as exc:
            raise OperatorRecordComparisonNumericalError(
                OperatorRecordComparisonNumericalErrorCode.LINEAR_ALGEBRA_FAILURE
            ) from exc
        if not np.all(np.isfinite(singular_values)):
            raise OperatorRecordComparisonNumericalError(
                OperatorRecordComparisonNumericalErrorCode.LINEAR_ALGEBRA_FAILURE
            )
        # Restoring the binary exponent returns the unit-bearing spectral norm
        # without division by a subnormal complex scale.
        with np.errstate(over="ignore", under="ignore", invalid="ignore"):
            norm = float(np.ldexp(float(singular_values[0]), exponent))
        if not np.isfinite(norm):
            raise OperatorRecordComparisonNumericalError(
                OperatorRecordComparisonNumericalErrorCode.NONFINITE_METRIC
            )
        return norm
