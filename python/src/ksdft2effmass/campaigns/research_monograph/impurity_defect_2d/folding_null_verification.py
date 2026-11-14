"""Independent Kronecker reconstruction for folding/null-control results.

This module imports neither the production calculator nor the reusable quotient-seam
constructor. It reconstructs seam shifts, Fourier folding, primitive energies, and the
known null-alignment attack through separate dense Kronecker arithmetic.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np
import numpy.typing as npt

from .folding_null import (
    FoldingMetrics,
    FoldingNullCaseResult,
    FoldingNullCriterionEvaluator,
    FoldingNullResult,
    NullAlignmentMetrics,
)

type ComplexMatrix = npt.NDArray[np.complex128]
type RealVector = npt.NDArray[np.float64]
type IntegerComponents = tuple[int] | tuple[int, int] | tuple[int, int, int]
type FloatComponents = tuple[float] | tuple[float, float] | tuple[float, float, float]


def _integer_pair(value: IntegerComponents) -> tuple[int, int]:
    """Close one already validated two-dimensional integer tuple."""
    if len(value) != 2:
        raise AssertionError("two-dimensional integer components were lost")
    return value[0], value[1]


def _float_pair(value: FloatComponents) -> tuple[float, float]:
    """Close one already validated two-dimensional floating tuple."""
    if len(value) != 2:
        raise AssertionError("two-dimensional floating components were lost")
    return value[0], value[1]


@dataclass(frozen=True, slots=True)
class FoldingNullVerificationResult:
    """Retain independent reconstruction and criterion-correlation evidence."""

    source: FoldingNullResult
    reconstruction_relative_tolerance: float
    reconstruction_absolute_tolerance: float
    maximum_metric_absolute_difference: float
    reconstructed_failed_criteria: tuple[str, ...]
    reconstruction_passed: bool
    criteria_match: bool

    def __post_init__(self) -> None:
        """Validate exact source, tolerances, metrics, and derived dispositions."""
        if type(self.source) is not FoldingNullResult:
            raise TypeError("source must be FoldingNullResult")
        for value, name in (
            (
                self.reconstruction_relative_tolerance,
                "reconstruction_relative_tolerance",
            ),
            (
                self.reconstruction_absolute_tolerance,
                "reconstruction_absolute_tolerance",
            ),
            (
                self.maximum_metric_absolute_difference,
                "maximum_metric_absolute_difference",
            ),
        ):
            if type(value) is not float:
                raise TypeError(f"{name} must be a built-in float")
            if not math.isfinite(value) or value < 0.0:
                raise ValueError(f"{name} must be finite and nonnegative")
        if type(self.reconstructed_failed_criteria) is not tuple or any(
            type(value) is not str or not value
            for value in self.reconstructed_failed_criteria
        ):
            raise TypeError(
                "reconstructed_failed_criteria must contain nonempty strings"
            )
        if type(self.reconstruction_passed) is not bool:
            raise TypeError("reconstruction_passed must be a built-in bool")
        if type(self.criteria_match) is not bool:
            raise TypeError("criteria_match must be a built-in bool")
        if self.criteria_match != (
            self.reconstructed_failed_criteria == self.source.failed_criteria
        ):
            raise ValueError("criteria_match must reflect exact failure correlation")

    @property
    def passes(self) -> bool:
        """Return whether arithmetic reconstruction and criterion correlation pass."""
        return self.reconstruction_passed and self.criteria_match


class FoldingNullIndependentVerifier:
    """Reconstruct folding/null metrics without production construction algorithms."""

    __slots__ = ()

    def execute(
        self,
        source: FoldingNullResult,
        *,
        relative_tolerance: float,
        absolute_tolerance: float,
    ) -> FoldingNullVerificationResult:
        """Return independent metric reconstruction and failure correlation."""
        if type(source) is not FoldingNullResult:
            raise TypeError("source must be FoldingNullResult")
        for value, name in (
            (relative_tolerance, "relative_tolerance"),
            (absolute_tolerance, "absolute_tolerance"),
        ):
            if type(value) is not float:
                raise TypeError(f"{name} must be a built-in float")
            if not math.isfinite(value) or value < 0.0:
                raise ValueError(f"{name} must be finite and nonnegative")

        reconstructed_cases: list[FoldingNullCaseResult] = []
        maximum_difference = 0.0
        reconstruction_passed = True
        for retained in source.cases:
            reconstructed = self._case(source, retained)
            reconstructed_cases.append(reconstructed)
            for observed, expected in self._metric_pairs(retained, reconstructed):
                difference = abs(observed - expected)
                maximum_difference = max(maximum_difference, difference)
                if not math.isclose(
                    observed,
                    expected,
                    rel_tol=relative_tolerance,
                    abs_tol=absolute_tolerance,
                ):
                    reconstruction_passed = False
        closed = tuple(reconstructed_cases)
        failures = FoldingNullCriterionEvaluator().execute(
            closed, source.definition.tolerances
        )
        return FoldingNullVerificationResult(
            source=source,
            reconstruction_relative_tolerance=relative_tolerance,
            reconstruction_absolute_tolerance=absolute_tolerance,
            maximum_metric_absolute_difference=maximum_difference,
            reconstructed_failed_criteria=failures,
            reconstruction_passed=reconstruction_passed,
            criteria_match=failures == source.failed_criteria,
        )

    def _case(
        self, source: FoldingNullResult, retained: FoldingNullCaseResult
    ) -> FoldingNullCaseResult:
        """Reconstruct one case through dense Kronecker seam arithmetic."""
        case = retained.case
        nx, ny = _integer_pair(case.shape.extents)
        phi_x, phi_y = _float_pair(case.twist.turns)
        dimension = case.shape.cell_count
        hamiltonian = np.zeros((dimension, dimension), dtype=np.complex128)
        for term in source.definition.parent.terms:
            displacement_x, displacement_y = _integer_pair(term.displacement.components)
            hamiltonian += term.value * np.kron(
                self._seam_shift(nx, displacement_x, phi_x),
                self._seam_shift(ny, displacement_y, phi_y),
            )
        folding = np.kron(self._fourier(nx, phi_x), self._fourier(ny, phi_y))
        expected = self._energy_grid(source, retained)
        represented = folding.conjugate().transpose() @ hamiltonian @ folding
        diagonal = np.diag(np.diag(represented))
        folding_metrics = FoldingMetrics(
            unitarity_maximum_absolute_defect=self._maximum_absolute(
                folding.conjugate().transpose() @ folding
                - np.eye(dimension, dtype=np.complex128)
            ),
            hermiticity_maximum_absolute_defect=self._maximum_absolute(
                hamiltonian - hamiltonian.conjugate().transpose()
            ),
            off_diagonal_maximum_absolute=self._maximum_absolute(
                represented - diagonal
            ),
            primitive_energy_maximum_absolute_defect=self._maximum_absolute(
                represented - np.diag(expected)
            ),
            eigenvalue_maximum_absolute_defect=float(
                np.max(
                    np.abs(np.sort(np.linalg.eigvalsh(hamiltonian)) - np.sort(expected))
                )
            ),
        )
        attack = source.definition.null_attack
        permutation = np.kron(
            self._forward_permutation(nx, attack.translation_cells[0]),
            self._forward_permutation(ny, attack.translation_cells[1]),
        )
        x = np.repeat(np.arange(nx, dtype=np.float64), ny)
        y = np.tile(np.arange(ny, dtype=np.float64), nx)
        diagonal_phase = np.diag(
            np.exp(
                1.0j
                * (
                    attack.site_phase_steps_radians[0] * x
                    + attack.site_phase_steps_radians[1] * y
                )
            )
        )
        transform = permutation @ diagonal_phase
        identity = np.eye(dimension, dtype=np.complex128)
        attacked = (
            transform @ hamiltonian @ transform.conjugate().transpose()
            + attack.energy_reference_shift * identity
        )
        recovered = (
            transform.conjugate().transpose()
            @ (attacked - attack.energy_reference_shift * identity)
            @ transform
            - hamiltonian
        )
        null_metrics = NullAlignmentMetrics(
            transform_unitarity_maximum_absolute_defect=self._maximum_absolute(
                transform.conjugate().transpose() @ transform - identity
            ),
            recovered_maximum_absolute_defect=self._maximum_absolute(recovered),
            recovered_frobenius_defect=float(np.linalg.norm(recovered, ord="fro")),
        )
        return FoldingNullCaseResult(case, folding_metrics, null_metrics)

    @staticmethod
    def _seam_shift(size: int, displacement: int, twist: float) -> ComplexMatrix:
        """Construct one independent one-dimensional quotient-seam shift."""
        result = np.zeros((size, size), dtype=np.complex128)
        for source in range(size):
            quotient, target = divmod(source + displacement, size)
            result[source, target] = np.exp(2.0j * np.pi * float(quotient) * twist)
        return result

    @staticmethod
    def _fourier(size: int, twist: float) -> ComplexMatrix:
        """Construct one independently normalized twisted Fourier matrix."""
        positions = np.arange(size, dtype=np.float64)[:, np.newaxis]
        indices = np.arange(size, dtype=np.float64)[np.newaxis, :]
        result: ComplexMatrix = np.exp(
            2.0j * np.pi * positions * (indices + twist) / float(size)
        ).astype(np.complex128)
        result /= math.sqrt(float(size))
        return result

    @staticmethod
    def _energy_grid(
        source: FoldingNullResult, retained: FoldingNullCaseResult
    ) -> RealVector:
        """Evaluate primitive energies by independent vectorized finite sums."""
        nx, ny = _integer_pair(retained.case.shape.extents)
        phi_x, phi_y = _float_pair(retained.case.twist.turns)
        kx = (np.arange(nx, dtype=np.float64) + phi_x) / float(nx)
        ky = (np.arange(ny, dtype=np.float64) + phi_y) / float(ny)
        values = np.zeros((nx, ny), dtype=np.complex128)
        for term in source.definition.parent.terms:
            displacement_x, displacement_y = _integer_pair(term.displacement.components)
            values += term.value * np.exp(
                2.0j
                * np.pi
                * (
                    float(displacement_x) * kx[:, np.newaxis]
                    + float(displacement_y) * ky[np.newaxis, :]
                )
            )
        if float(np.max(np.abs(values.imag))) > 1.0e-11:
            raise ValueError("independent primitive energy must remain real")
        return values.real.reshape(nx * ny)

    @staticmethod
    def _forward_permutation(size: int, displacement: int) -> ComplexMatrix:
        """Construct one independent forward cyclic permutation."""
        result = np.zeros((size, size), dtype=np.complex128)
        for source in range(size):
            result[(source + displacement) % size, source] = 1.0
        return result

    @staticmethod
    def _metric_pairs(
        retained: FoldingNullCaseResult, reconstructed: FoldingNullCaseResult
    ) -> tuple[tuple[float, float], ...]:
        """Return retained/reconstructed metric pairs in canonical order."""
        left_folding = retained.folding
        right_folding = reconstructed.folding
        left_null = retained.null_extraction
        right_null = reconstructed.null_extraction
        return (
            (
                left_folding.unitarity_maximum_absolute_defect,
                right_folding.unitarity_maximum_absolute_defect,
            ),
            (
                left_folding.hermiticity_maximum_absolute_defect,
                right_folding.hermiticity_maximum_absolute_defect,
            ),
            (
                left_folding.off_diagonal_maximum_absolute,
                right_folding.off_diagonal_maximum_absolute,
            ),
            (
                left_folding.primitive_energy_maximum_absolute_defect,
                right_folding.primitive_energy_maximum_absolute_defect,
            ),
            (
                left_folding.eigenvalue_maximum_absolute_defect,
                right_folding.eigenvalue_maximum_absolute_defect,
            ),
            (
                left_null.transform_unitarity_maximum_absolute_defect,
                right_null.transform_unitarity_maximum_absolute_defect,
            ),
            (
                left_null.recovered_maximum_absolute_defect,
                right_null.recovered_maximum_absolute_defect,
            ),
            (
                left_null.recovered_frobenius_defect,
                right_null.recovered_frobenius_defect,
            ),
        )

    @staticmethod
    def _maximum_absolute(value: ComplexMatrix) -> float:
        """Return the finite maximum absolute matrix entry."""
        return float(np.max(np.abs(value), initial=0.0))
