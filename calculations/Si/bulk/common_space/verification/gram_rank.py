"""Exact a posteriori Gram-rank bounds; not a complete CSD1-V verifier."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from math import isfinite

import numpy as np
from ksdft2effmass.serialization.enums import StrWireEnum
from numpy.typing import NDArray


class GramRankDisposition(StrWireEnum):
    """Numerical rank resolution, never scientific gate passage."""

    rank_resolved = "rank-resolved"
    numerically_inconclusive = "numerically-inconclusive"


class GramRankFailure(StrWireEnum):
    """Closed arithmetic failures, distinct from threshold overlap."""

    unrepresentable_gram = "unrepresentable-floating-gram"
    eigensolver_failure = "eigensolver-failure"
    invalid_eigensystem = "invalid-eigensystem"
    uncertified_frame = "uncertified-eigenvector-frame"
    negative_eigenvalue_interval = "materially-negative-eigenvalue-interval"


@dataclass(frozen=True, slots=True, kw_only=True)
class GramEigenvalueInterval:
    """An exact rational, dimensionless arithmetic interval, not native uncertainty."""

    lower: Fraction
    upper: Fraction

    def __post_init__(self) -> None:
        if type(self.lower) is not Fraction or type(self.upper) is not Fraction:
            raise TypeError("eigenvalue endpoints must be exact built-in Fractions")
        if self.lower > self.upper:
            raise ValueError("eigenvalue interval endpoints are reversed")

    @property
    def nonnegative_bounds(self) -> tuple[Fraction, Fraction]:
        """Use Gram positivity only if the interval is not materially negative."""
        if self.upper < 0:
            raise ValueError(
                "materially negative eigenvalue interval cannot be clamped"
            )
        return max(Fraction(0), self.lower), self.upper


@dataclass(frozen=True, slots=True, kw_only=True)
class CommonSpaceGramRankEnclosure:
    """Immutable finite-matrix certificate, without source or CSD1-V authority.

    Bounds are exact dimensionless Fractions. Rank uses strict ``sigma > threshold``;
    failure or threshold overlap never yields a resolved rank. No displayed floating
    square roots or fitted comparison tolerances participate in classification.
    """

    dimension: int
    rank_threshold: Fraction
    eigenvalue_intervals: tuple[GramEigenvalueInterval, ...] = ()
    orthonormality_defect_bound: Fraction | None = None
    spectral_error_bound: Fraction | None = None
    eigenpair_residual_bounds: tuple[Fraction, ...] = ()
    minimum_eigenvector: tuple[tuple[Fraction, Fraction], ...] = ()
    failure: GramRankFailure | None = None

    def __post_init__(self) -> None:
        if type(self.dimension) is not int or self.dimension <= 0:
            raise ValueError("dimension must be a positive built-in integer")
        if type(self.rank_threshold) is not Fraction or self.rank_threshold < 0:
            raise ValueError("rank_threshold must be a nonnegative built-in Fraction")
        if self.failure is not None and type(self.failure) is not GramRankFailure:
            raise TypeError("failure must be a GramRankFailure or None")
        if type(self.eigenvalue_intervals) is not tuple or any(
            type(interval) is not GramEigenvalueInterval
            for interval in self.eigenvalue_intervals
        ):
            raise TypeError("eigenvalue_intervals must be a tuple of exact intervals")
        if len(self.eigenvalue_intervals) not in (0, self.dimension):
            raise ValueError("eigenvalue interval count differs from dimension")
        if type(self.eigenpair_residual_bounds) is not tuple or any(
            type(bound) is not Fraction or bound < 0
            for bound in self.eigenpair_residual_bounds
        ):
            raise TypeError("residual bounds must be a tuple of nonnegative Fractions")
        if len(self.eigenpair_residual_bounds) not in (0, self.dimension):
            raise ValueError("residual bound count differs from dimension")
        if type(self.minimum_eigenvector) is not tuple or any(
            type(value) is not tuple
            or len(value) != 2
            or any(type(component) is not Fraction for component in value)
            for value in self.minimum_eigenvector
        ):
            raise TypeError(
                "minimum_eigenvector must contain exact rational component pairs"
            )
        if len(self.minimum_eigenvector) not in (0, self.dimension):
            raise ValueError("minimum eigenvector dimension differs")
        for bound in (self.orthonormality_defect_bound, self.spectral_error_bound):
            if bound is not None and (type(bound) is not Fraction or bound < 0):
                raise ValueError("arithmetic bounds must be nonnegative Fractions")
        if self.failure is None:
            if (
                len(self.eigenvalue_intervals) != self.dimension
                or len(self.eigenpair_residual_bounds) != self.dimension
                or self.orthonormality_defect_bound is None
                or self.orthonormality_defect_bound >= 1
                or self.spectral_error_bound is None
                or len(self.minimum_eigenvector) != self.dimension
                or not any(
                    real or imaginary for real, imaginary in self.minimum_eigenvector
                )
            ):
                raise ValueError("a complete arithmetic certificate is required")
            for interval in self.eigenvalue_intervals:
                _ = interval.nonnegative_bounds

    @property
    def hermiticity_defect_bound(self) -> Fraction:
        """The exact Gram construction has zero Hermiticity defect."""
        return Fraction(0)

    @property
    def rank_lower_bound(self) -> int:
        if self.failure is not None:
            return 0
        squared_threshold = self.rank_threshold**2
        return sum(
            interval.nonnegative_bounds[0] > squared_threshold
            for interval in self.eigenvalue_intervals
        )

    @property
    def rank_upper_bound(self) -> int:
        if self.failure is not None:
            return self.dimension
        squared_threshold = self.rank_threshold**2
        return sum(
            interval.upper > squared_threshold for interval in self.eigenvalue_intervals
        )

    @property
    def resolved_rank(self) -> int | None:
        if self.failure is not None or self.rank_lower_bound != self.rank_upper_bound:
            return None
        return self.rank_lower_bound

    @property
    def disposition(self) -> GramRankDisposition:
        if self.resolved_rank is None:
            return GramRankDisposition.numerically_inconclusive
        return GramRankDisposition.rank_resolved


@dataclass(frozen=True, slots=True, kw_only=True)
class _ExactComplex:
    real: Fraction = Fraction(0)
    imaginary: Fraction = Fraction(0)

    def __post_init__(self) -> None:
        if type(self.real) is not Fraction or type(self.imaginary) is not Fraction:
            raise TypeError("exact complex components must be built-in Fractions")

    def add(self, other: _ExactComplex) -> _ExactComplex:
        return _ExactComplex(
            real=self.real + other.real, imaginary=self.imaginary + other.imaginary
        )

    def subtract(self, other: _ExactComplex) -> _ExactComplex:
        return _ExactComplex(
            real=self.real - other.real, imaginary=self.imaginary - other.imaginary
        )

    def multiply(self, other: _ExactComplex) -> _ExactComplex:
        return _ExactComplex(
            real=self.real * other.real - self.imaginary * other.imaginary,
            imaginary=self.real * other.imaginary + self.imaginary * other.real,
        )

    def conjugate(self) -> _ExactComplex:
        return _ExactComplex(real=self.real, imaginary=-self.imaginary)

    @property
    def absolute_bound(self) -> Fraction:
        return abs(self.real) + abs(self.imaginary)


@dataclass(frozen=True, slots=True, kw_only=True)
class _ExactMatrix:
    rows: tuple[tuple[_ExactComplex, ...], ...]

    def __post_init__(self) -> None:
        if type(self.rows) is not tuple or not self.rows:
            raise ValueError("exact matrix must have nonempty tuple rows")
        if any(
            type(row) is not tuple
            or not row
            or len(row) != len(self.rows[0])
            or any(type(value) is not _ExactComplex for value in row)
            for row in self.rows
        ):
            raise ValueError(
                "exact matrix must be rectangular with exact complex entries"
            )

    @classmethod
    def from_binary64(cls, values: tuple[tuple[complex, ...], ...]) -> _ExactMatrix:
        return cls(
            rows=tuple(
                tuple(
                    _ExactComplex(
                        real=Fraction.from_float(value.real),
                        imaginary=Fraction.from_float(value.imag),
                    )
                    for value in row
                )
                for row in values
            )
        )

    @classmethod
    def diagonal(cls, values: tuple[Fraction, ...]) -> _ExactMatrix:
        return cls(
            rows=tuple(
                tuple(
                    _ExactComplex(real=value if row == column else Fraction(0))
                    for column in range(len(values))
                )
                for row, value in enumerate(values)
            )
        )

    def adjoint(self) -> _ExactMatrix:
        return _ExactMatrix(
            rows=tuple(
                tuple(
                    self.rows[column][row].conjugate()
                    for column in range(len(self.rows))
                )
                for row in range(len(self.rows[0]))
            )
        )

    def multiply(self, other: _ExactMatrix) -> _ExactMatrix:
        if len(self.rows[0]) != len(other.rows):
            raise ValueError("exact matrix product dimensions differ")

        def entry(row: int, column: int) -> _ExactComplex:
            value = _ExactComplex()
            for index in range(len(self.rows[0])):
                value = value.add(
                    self.rows[row][index].multiply(other.rows[index][column])
                )
            return value

        return _ExactMatrix(
            rows=tuple(
                tuple(entry(row, column) for column in range(len(other.rows[0])))
                for row in range(len(self.rows))
            )
        )

    def subtract(self, other: _ExactMatrix) -> _ExactMatrix:
        if (len(self.rows), len(self.rows[0])) != (len(other.rows), len(other.rows[0])):
            raise ValueError("exact matrix dimensions differ")
        return _ExactMatrix(
            rows=tuple(
                tuple(
                    left.subtract(right)
                    for left, right in zip(row, other_row, strict=True)
                )
                for row, other_row in zip(self.rows, other.rows, strict=True)
            )
        )

    @property
    def hermitian_norm_bound(self) -> Fraction:
        """Bound spectral norm only after checking exact Hermiticity."""
        if len(self.rows) != len(self.rows[0]):
            raise ValueError("Hermitian norm bound requires a square matrix")
        if any(
            self.rows[row][column] != self.rows[column][row].conjugate()
            for row in range(len(self.rows))
            for column in range(len(self.rows))
        ):
            raise ValueError("Hermitian norm bound requires an exact Hermitian matrix")
        return max(
            sum((value.absolute_bound for value in row), start=Fraction(0))
            for row in self.rows
        )

    @property
    def column_residual_bounds(self) -> tuple[Fraction, ...]:
        return tuple(
            sum((row[column].absolute_bound for row in self.rows), start=Fraction(0))
            for column in range(len(self.rows[0]))
        )

    def to_numpy(self) -> NDArray[np.complex128]:
        """Generate candidates only; conversion error is covered a posteriori."""
        return np.asarray(
            tuple(
                tuple(
                    complex(float(value.real), float(value.imaginary)) for value in row
                )
                for row in self.rows
            ),
            dtype=np.complex128,
        )


@dataclass(frozen=True, slots=True, kw_only=True)
class CommonSpaceGramRankEncloser:
    """Enclose rank of a supplied dimensionless finite complex overlap.

    ``independent_overlap`` must be nested built-in tuples of finite built-in complex
    scalars, not producer output in a CSD1-V composition. ``rank_threshold`` must be
    a nonnegative built-in Fraction. Gram and certificate arithmetic are exact for
    these input binary64 values; native-decimal and upstream errors are not included.
    Floating conversion overflow or eigensolver failure returns inconclusiveness;
    candidate underflow remains covered by exact residuals. Resource errors propagate.
    No source authentication, square-root rounding, tolerance selection, or CSD1-V
    gate authorization occurs here.
    """

    independent_overlap: tuple[tuple[complex, ...], ...]
    rank_threshold: Fraction

    def __post_init__(self) -> None:
        if type(self.rank_threshold) is not Fraction or self.rank_threshold < 0:
            raise ValueError("rank_threshold must be a nonnegative built-in Fraction")
        if type(self.independent_overlap) is not tuple or not self.independent_overlap:
            raise ValueError("independent_overlap must be a nonempty tuple")
        for row in self.independent_overlap:
            if type(row) is not tuple or len(row) != len(self.independent_overlap):
                raise ValueError("independent_overlap must have square tuple rows")
            if any(
                type(value) is not complex
                or not isfinite(value.real)
                or not isfinite(value.imag)
                for value in row
            ):
                raise ValueError(
                    "overlap entries must be finite built-in complex scalars"
                )

    def execute(self) -> CommonSpaceGramRankEnclosure:
        """Form an exact Gram matrix and certify a floating eigenvalue candidate."""
        return _ExactGramRankEncloser(
            independent_overlap=_ExactMatrix.from_binary64(self.independent_overlap),
            rank_threshold=self.rank_threshold,
        ).execute()


@dataclass(frozen=True, slots=True, kw_only=True)
class _ExactGramRankEncloser:
    """Certify an exact reconstructed overlap without a floating intermediate."""

    independent_overlap: _ExactMatrix
    rank_threshold: Fraction

    def __post_init__(self) -> None:
        if type(self.independent_overlap) is not _ExactMatrix:
            raise TypeError("independent_overlap must be an exact matrix")
        if len(self.independent_overlap.rows) != len(self.independent_overlap.rows[0]):
            raise ValueError("independent_overlap must be square")
        if type(self.rank_threshold) is not Fraction or self.rank_threshold < 0:
            raise ValueError("rank_threshold must be a nonnegative built-in Fraction")

    def execute(self) -> CommonSpaceGramRankEnclosure:
        gram = self.independent_overlap.adjoint().multiply(self.independent_overlap)
        candidate = self._candidate(gram)
        if isinstance(candidate, GramRankFailure):
            return self._failure(candidate)
        eigenvalues, vectors = candidate
        diagonal = _ExactMatrix.diagonal(eigenvalues)
        adjoint = vectors.adjoint()
        defect = (
            adjoint.multiply(vectors)
            .subtract(_ExactMatrix.diagonal(tuple(Fraction(1) for _ in eigenvalues)))
            .hermitian_norm_bound
        )
        residuals = (
            gram.multiply(vectors)
            .subtract(vectors.multiply(diagonal))
            .column_residual_bounds
        )
        if defect >= 1:
            return self._failure(
                GramRankFailure.uncertified_frame,
                defect=defect,
                residuals=residuals,
            )
        diagonalization = adjoint.multiply(gram).multiply(vectors).subtract(diagonal)
        error = (
            diagonalization.hermitian_norm_bound
            + gram.hermitian_norm_bound * defect / (2 - defect) * (2 + defect)
        )
        intervals = tuple(
            GramEigenvalueInterval(lower=value - error, upper=value + error)
            for value in eigenvalues
        )
        failure = (
            GramRankFailure.negative_eigenvalue_interval
            if any(interval.upper < 0 for interval in intervals)
            else None
        )
        return CommonSpaceGramRankEnclosure(
            dimension=len(eigenvalues),
            rank_threshold=self.rank_threshold,
            eigenvalue_intervals=intervals,
            orthonormality_defect_bound=defect,
            spectral_error_bound=error,
            eigenpair_residual_bounds=residuals,
            minimum_eigenvector=tuple(
                (row[0].real, row[0].imaginary) for row in vectors.rows
            ),
            failure=failure,
        )

    def _candidate(
        self, gram: _ExactMatrix
    ) -> tuple[tuple[Fraction, ...], _ExactMatrix] | GramRankFailure:
        try:
            approximate = gram.to_numpy()
        except OverflowError:
            return GramRankFailure.unrepresentable_gram
        if not np.all(np.isfinite(approximate)):
            return GramRankFailure.unrepresentable_gram
        try:
            with np.errstate(over="raise", invalid="raise", under="ignore"):
                eigenvalues, vectors = np.linalg.eigh(approximate)
        except np.linalg.LinAlgError, FloatingPointError:
            return GramRankFailure.eigensolver_failure
        dimension = len(self.independent_overlap.rows)
        if (
            eigenvalues.shape != (dimension,)
            or vectors.shape != (dimension, dimension)
            or eigenvalues.dtype != np.dtype(np.float64)
            or vectors.dtype != np.dtype(np.complex128)
            or not np.all(np.isfinite(eigenvalues))
            or not np.all(np.isfinite(vectors))
        ):
            return GramRankFailure.invalid_eigensystem
        order = sorted(range(dimension), key=lambda index: float(eigenvalues[index]))
        return (
            tuple(Fraction.from_float(float(eigenvalues[index])) for index in order),
            _ExactMatrix.from_binary64(
                tuple(
                    tuple(complex(vectors[row, column]) for column in order)
                    for row in range(dimension)
                )
            ),
        )

    def _failure(
        self,
        failure: GramRankFailure,
        *,
        defect: Fraction | None = None,
        residuals: tuple[Fraction, ...] = (),
    ) -> CommonSpaceGramRankEnclosure:
        return CommonSpaceGramRankEnclosure(
            dimension=len(self.independent_overlap.rows),
            rank_threshold=self.rank_threshold,
            failure=failure,
            orthonormality_defect_bound=defect,
            eigenpair_residual_bounds=residuals,
        )
