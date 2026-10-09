"""Represented Hamiltonian mechanics for finite-hopping periodic-1D toys."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import numpy.typing as npt

import ksdft2effmass.periodic1d as periodic1d

type ComplexMatrix = npt.NDArray[np.complex128]


@dataclass(frozen=True, slots=True)
class Periodic1DPrimitiveFiberHamiltonianRequest:
    """Request one primitive-cell Bloch fiber from a finite-hopping toy model."""

    model: periodic1d.Periodic1DFiniteHoppingToyModel
    reduced_momentum: float | np.float64

    def __post_init__(self) -> None:
        if type(self.model) is not periodic1d.Periodic1DFiniteHoppingToyModel:
            raise TypeError("model must be Periodic1DFiniteHoppingToyModel")
        if type(self.reduced_momentum) not in (float, np.float64):
            raise TypeError("reduced_momentum must be a float or numpy.float64")
        if not np.isfinite(self.reduced_momentum):
            raise ValueError("reduced_momentum must be finite")
        object.__setattr__(self, "reduced_momentum", float(self.reduced_momentum))


@dataclass(frozen=True, slots=True)
class Periodic1DPrimitiveFiberHamiltonianResult:
    """Retain one operationally immutable primitive-cell Bloch matrix."""

    matrix: ComplexMatrix

    def __post_init__(self) -> None:
        value = np.asarray(self.matrix, dtype=np.complex128)
        if value.ndim != 2 or value.shape[0] == 0 or value.shape[0] != value.shape[1]:
            raise ValueError("matrix must be nonempty and square")
        if not np.all(np.isfinite(value)):
            raise ValueError("matrix must contain only finite values")
        immutable = np.frombuffer(
            value.tobytes(order="C"), dtype=np.complex128
        ).reshape(value.shape)
        object.__setattr__(self, "matrix", immutable)


class Periodic1DPrimitiveFiberHamiltonianConstructor:
    """Construct primitive-cell Bloch fibers from finite hopping blocks."""

    __slots__ = ()

    def execute(
        self, request: Periodic1DPrimitiveFiberHamiltonianRequest
    ) -> Periodic1DPrimitiveFiberHamiltonianResult:
        """Construct the fiber using the authored reduced-momentum convention."""
        model = request.model
        result = np.zeros(
            (model.orbital_count, model.orbital_count), dtype=np.complex128
        )
        for block in model.blocks:
            result += (
                np.exp(2j * np.pi * request.reduced_momentum * block.displacement_cells)
                * block.matrix
            )
        return Periodic1DPrimitiveFiberHamiltonianResult(result)


@dataclass(frozen=True, slots=True)
class Periodic1DSupercellHamiltonianRequest:
    """Request one twisted finite supercell representation."""

    model: periodic1d.Periodic1DFiniteHoppingToyModel
    cell_count: int
    reduced_momentum: float | np.float64

    def __post_init__(self) -> None:
        if type(self.model) is not periodic1d.Periodic1DFiniteHoppingToyModel:
            raise TypeError("model must be Periodic1DFiniteHoppingToyModel")
        if isinstance(self.cell_count, bool) or not isinstance(self.cell_count, int):
            raise TypeError("cell_count must be an integer")
        if self.cell_count < 1:
            raise ValueError("cell_count must be positive")
        if type(self.reduced_momentum) not in (float, np.float64):
            raise TypeError("reduced_momentum must be a float or numpy.float64")
        if not np.isfinite(self.reduced_momentum):
            raise ValueError("reduced_momentum must be finite")
        object.__setattr__(self, "reduced_momentum", float(self.reduced_momentum))


@dataclass(frozen=True, slots=True)
class Periodic1DSupercellHamiltonianResult:
    """Retain one operationally immutable twisted-supercell matrix."""

    matrix: ComplexMatrix

    def __post_init__(self) -> None:
        value = np.asarray(self.matrix, dtype=np.complex128)
        if value.ndim != 2 or value.shape[0] == 0 or value.shape[0] != value.shape[1]:
            raise ValueError("matrix must be nonempty and square")
        if not np.all(np.isfinite(value)):
            raise ValueError("matrix must contain only finite values")
        immutable = np.frombuffer(
            value.tobytes(order="C"), dtype=np.complex128
        ).reshape(value.shape)
        object.__setattr__(self, "matrix", immutable)


class Periodic1DSupercellHamiltonianConstructor:
    """Construct a twisted finite supercell from a finite-hopping toy model."""

    __slots__ = ()

    def execute(
        self, request: Periodic1DSupercellHamiltonianRequest
    ) -> Periodic1DSupercellHamiltonianResult:
        """Construct the matrix with explicit boundary-crossing phases."""
        model = request.model
        block_size = model.orbital_count
        result = np.zeros(
            (block_size * request.cell_count, block_size * request.cell_count),
            dtype=np.complex128,
        )
        for source in range(request.cell_count):
            for block in model.blocks:
                raw_target = source + block.displacement_cells
                target = raw_target % request.cell_count
                crossings = (raw_target - target) // request.cell_count
                phase = np.exp(
                    2j
                    * np.pi
                    * request.reduced_momentum
                    * request.cell_count
                    * crossings
                )
                result[
                    block_size * source : block_size * (source + 1),
                    block_size * target : block_size * (target + 1),
                ] += phase * block.matrix
        return Periodic1DSupercellHamiltonianResult(result)


__all__ = [
    "Periodic1DPrimitiveFiberHamiltonianConstructor",
    "Periodic1DPrimitiveFiberHamiltonianRequest",
    "Periodic1DPrimitiveFiberHamiltonianResult",
    "Periodic1DSupercellHamiltonianConstructor",
    "Periodic1DSupercellHamiltonianRequest",
    "Periodic1DSupercellHamiltonianResult",
]
