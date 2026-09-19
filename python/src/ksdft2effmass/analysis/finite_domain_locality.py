"""Minimum-image locality partitions and sparse represented residual diagnostics."""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np
from scipy import sparse  # type: ignore[import-untyped]

from ksdft2effmass.operators import PhysicalUnit, Unitless
from ksdft2effmass.solid_state import (
    FiniteLatticeCoordinateResolver,
    FiniteLatticeShape,
    LatticeCoordinate,
    ScalarFiniteLatticeOperator,
    ScalarFiniteLatticeOperatorCompatibilityResult,
)

type LocalityResidualUnit = PhysicalUnit | Unitless
"""Closed unit union for sparse locality residuals."""


@dataclass(frozen=True, slots=True)
class MinimumImageChebyshevPartition:
    """Retain exact site shells around one canonical finite-lattice origin."""

    shape: FiniteLatticeShape
    origin: LatticeCoordinate
    core_radius: int
    site_shells: tuple[int, ...]
    core_indices: tuple[int, ...]
    exterior_indices: tuple[int, ...]

    def __post_init__(self) -> None:
        """Validate dimension, shell assignment, and complete index partition."""
        if type(self.shape) is not FiniteLatticeShape:
            raise TypeError("shape must be FiniteLatticeShape")
        if type(self.origin) is not LatticeCoordinate:
            raise TypeError("origin must be LatticeCoordinate")
        if self.origin.dimension is not self.shape.dimension:
            raise ValueError("origin and finite shape dimensions must agree")
        if any(
            component < 0 or component >= extent
            for component, extent in zip(
                self.origin.components, self.shape.extents, strict=True
            )
        ):
            raise ValueError("origin must be a canonical finite-lattice coordinate")
        if type(self.core_radius) is not int:
            raise TypeError("core_radius must be a built-in int")
        if self.core_radius < 0:
            raise ValueError("core_radius must be nonnegative")
        if type(self.site_shells) is not tuple or any(
            type(shell) is not int for shell in self.site_shells
        ):
            raise TypeError("site_shells must be a tuple of built-in ints")
        if len(self.site_shells) != self.shape.cell_count:
            raise ValueError("site_shells must contain one shell per lattice site")
        if any(shell < 0 for shell in self.site_shells):
            raise ValueError("site shells must be nonnegative")
        for indices, name in (
            (self.core_indices, "core_indices"),
            (self.exterior_indices, "exterior_indices"),
        ):
            if type(indices) is not tuple or any(
                type(index) is not int for index in indices
            ):
                raise TypeError(f"{name} must be a tuple of built-in ints")
            if tuple(sorted(set(indices))) != indices:
                raise ValueError(f"{name} must be sorted and unique")
            if any(index < 0 or index >= self.shape.cell_count for index in indices):
                raise ValueError(f"{name} contains an out-of-range site")
        expected_core = tuple(
            index
            for index, shell in enumerate(self.site_shells)
            if shell <= self.core_radius
        )
        expected_exterior = tuple(
            index
            for index, shell in enumerate(self.site_shells)
            if shell > self.core_radius
        )
        if (
            self.core_indices != expected_core
            or self.exterior_indices != expected_exterior
        ):
            raise ValueError("core and exterior indices must agree with site shells")

    @property
    def shell_count(self) -> int:
        """Return the number of represented exact-distance shells."""
        return max(self.site_shells) + 1

    def indices_for_shell(self, shell: int) -> tuple[int, ...]:
        """Return sorted site indices assigned to one exact shell."""
        if type(shell) is not int:
            raise TypeError("shell must be a built-in int")
        if shell < 0 or shell >= self.shell_count:
            raise ValueError("shell must identify a represented shell")
        return tuple(
            index
            for index, assigned in enumerate(self.site_shells)
            if assigned == shell
        )


class MinimumImageChebyshevPartitioner:
    """Construct exact Chebyshev shells using periodic minimum-image distances."""

    __slots__ = ()

    def execute(
        self,
        shape: FiniteLatticeShape,
        origin: LatticeCoordinate,
        *,
        core_radius: int,
    ) -> MinimumImageChebyshevPartition:
        """Return one complete site partition in last-axis-fastest ordering."""
        if type(shape) is not FiniteLatticeShape:
            raise TypeError("shape must be FiniteLatticeShape")
        if type(origin) is not LatticeCoordinate:
            raise TypeError("origin must be LatticeCoordinate")
        if origin.dimension is not shape.dimension:
            raise ValueError("origin and finite shape dimensions must agree")
        if any(
            component < 0 or component >= extent
            for component, extent in zip(origin.components, shape.extents, strict=True)
        ):
            raise ValueError("origin must be a canonical finite-lattice coordinate")
        if type(core_radius) is not int:
            raise TypeError("core_radius must be a built-in int")
        if core_radius < 0:
            raise ValueError("core_radius must be nonnegative")
        resolver = FiniteLatticeCoordinateResolver()
        site_shells: list[int] = []
        for index in range(shape.cell_count):
            coordinate = resolver.execute(shape, index)
            axis_distances = tuple(
                min(
                    (coordinate.components[axis] - origin.components[axis])
                    % shape.extents[axis],
                    (origin.components[axis] - coordinate.components[axis])
                    % shape.extents[axis],
                )
                for axis in range(shape.dimension.value)
            )
            site_shells.append(max(axis_distances))
        shells = tuple(site_shells)
        core_indices = tuple(
            index for index, shell in enumerate(shells) if shell <= core_radius
        )
        exterior_indices = tuple(
            index for index, shell in enumerate(shells) if shell > core_radius
        )
        return MinimumImageChebyshevPartition(
            shape, origin, core_radius, shells, core_indices, exterior_indices
        )


@dataclass(frozen=True, slots=True)
class SparseLocalityResidualResult:
    """Retain global and partition-resolved sparse matrix residual metrics."""

    reference: ScalarFiniteLatticeOperator
    candidate: ScalarFiniteLatticeOperator
    partition: MinimumImageChebyshevPartition
    unit: LocalityResidualUnit
    maximum_absolute_residual: float
    frobenius_residual: float
    core_frobenius_residual: float
    exterior_frobenius_residual: float
    core_exterior_frobenius_residual: float
    shell_row_frobenius_residuals: tuple[float, ...]

    def __post_init__(self) -> None:
        """Validate correlations, finite metrics, and Frobenius decompositions."""
        if type(self.reference) is not ScalarFiniteLatticeOperator:
            raise TypeError("reference must be ScalarFiniteLatticeOperator")
        if type(self.candidate) is not ScalarFiniteLatticeOperator:
            raise TypeError("candidate must be ScalarFiniteLatticeOperator")
        if type(self.partition) is not MinimumImageChebyshevPartition:
            raise TypeError("partition must be MinimumImageChebyshevPartition")
        if (
            self.partition.shape != self.reference.shape
            or self.partition.shape != self.candidate.shape
        ):
            raise ValueError("partition and represented operator shapes must agree")
        if not isinstance(self.unit, PhysicalUnit | Unitless):
            raise TypeError("unit must be PhysicalUnit or Unitless")
        if (
            self.unit != self.reference.matrix.unit
            or self.unit != self.candidate.matrix.unit
        ):
            raise ValueError("residual and represented operator units must agree")
        metrics = (
            self.maximum_absolute_residual,
            self.frobenius_residual,
            self.core_frobenius_residual,
            self.exterior_frobenius_residual,
            self.core_exterior_frobenius_residual,
        )
        if any(type(value) is not float for value in metrics):
            raise TypeError("residual metrics must be built-in floats")
        if any(not math.isfinite(value) or value < 0.0 for value in metrics):
            raise ValueError("residual metrics must be finite and nonnegative")
        if self.maximum_absolute_residual > self.frobenius_residual:
            raise ValueError("maximum residual must not exceed Frobenius residual")
        if type(self.shell_row_frobenius_residuals) is not tuple or any(
            type(value) is not float for value in self.shell_row_frobenius_residuals
        ):
            raise TypeError("shell residuals must be a tuple of built-in floats")
        if len(self.shell_row_frobenius_residuals) != self.partition.shell_count:
            raise ValueError("shell residual count must match the partition")
        if any(
            not math.isfinite(value) or value < 0.0
            for value in self.shell_row_frobenius_residuals
        ):
            raise ValueError("shell residuals must be finite and nonnegative")
        total_squared = self.frobenius_residual * self.frobenius_residual
        block_squared = math.fsum(
            (
                self.core_frobenius_residual * self.core_frobenius_residual,
                self.exterior_frobenius_residual * self.exterior_frobenius_residual,
                self.core_exterior_frobenius_residual
                * self.core_exterior_frobenius_residual,
            )
        )
        shell_squared = math.fsum(
            value * value for value in self.shell_row_frobenius_residuals
        )
        scale = max(1.0, total_squared, block_squared, shell_squared)
        allowance = 32.0 * np.finfo(np.float64).eps * scale
        if abs(total_squared - block_squared) > allowance:
            raise ValueError("block residuals must decompose the Frobenius residual")
        if abs(total_squared - shell_squared) > allowance:
            raise ValueError("shell residuals must decompose the Frobenius residual")


class SparseLocalityResidualAnalyzer:
    """Analyze one compatible represented difference without densification."""

    __slots__ = ()

    @staticmethod
    def frobenius(matrix: sparse.sparray) -> float:
        """Return the sparse Frobenius norm from stored finite values."""
        return math.sqrt(math.fsum(float(abs(value) ** 2) for value in matrix.data))

    def execute(
        self,
        reference: ScalarFiniteLatticeOperator,
        candidate: ScalarFiniteLatticeOperator,
        compatibility: ScalarFiniteLatticeOperatorCompatibilityResult,
        partition: MinimumImageChebyshevPartition,
    ) -> SparseLocalityResidualResult:
        """Return global, core, exterior, coupling, and exact-shell residuals."""
        if type(reference) is not ScalarFiniteLatticeOperator:
            raise TypeError("reference must be ScalarFiniteLatticeOperator")
        if type(candidate) is not ScalarFiniteLatticeOperator:
            raise TypeError("candidate must be ScalarFiniteLatticeOperator")
        if type(compatibility) is not ScalarFiniteLatticeOperatorCompatibilityResult:
            raise TypeError("compatibility has the wrong result type")
        if compatibility.left is not reference or compatibility.right is not candidate:
            raise ValueError("compatibility result must correlate the exact operands")
        if not compatibility.compatible:
            raise ValueError("compatibility result must pass before residual analysis")
        if type(partition) is not MinimumImageChebyshevPartition:
            raise TypeError("partition must be MinimumImageChebyshevPartition")
        if partition.shape != reference.shape:
            raise ValueError("partition and represented operator shapes must agree")
        residual = candidate.matrix.to_csr() - reference.matrix.to_csr()
        residual.sum_duplicates()
        residual.eliminate_zeros()
        maximum = (
            0.0 if residual.data.size == 0 else float(np.max(np.abs(residual.data)))
        )
        frobenius = self.frobenius(residual)
        core = np.asarray(partition.core_indices, dtype=np.int64)
        exterior = np.asarray(partition.exterior_indices, dtype=np.int64)
        core_block = residual[core, :][:, core]
        exterior_block = residual[exterior, :][:, exterior]
        core_to_exterior = residual[core, :][:, exterior]
        exterior_to_core = residual[exterior, :][:, core]
        core_frobenius = self.frobenius(core_block)
        exterior_frobenius = self.frobenius(exterior_block)
        coupling_frobenius = math.sqrt(
            self.frobenius(core_to_exterior) ** 2
            + self.frobenius(exterior_to_core) ** 2
        )
        shell_residuals: list[float] = []
        for shell in range(partition.shell_count):
            rows = np.asarray(partition.indices_for_shell(shell), dtype=np.int64)
            shell_residuals.append(self.frobenius(residual[rows, :]))
        return SparseLocalityResidualResult(
            reference,
            candidate,
            partition,
            reference.matrix.unit,
            maximum,
            frobenius,
            core_frobenius,
            exterior_frobenius,
            coupling_frobenius,
            tuple(shell_residuals),
        )
