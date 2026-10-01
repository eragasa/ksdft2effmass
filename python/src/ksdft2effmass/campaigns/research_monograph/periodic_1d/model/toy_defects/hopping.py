"""Finite-hopping periodic-1D toy parents and represented Hamiltonians."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import numpy.typing as npt

type ComplexMatrix = npt.NDArray[np.complex128]


@dataclass(frozen=True, slots=True)
class Periodic1DHoppingBlock:
    """Represent one directed hopping block at an integer cell displacement."""

    displacement_cells: int
    matrix: ComplexMatrix

    def __post_init__(self) -> None:
        if isinstance(self.displacement_cells, bool) or not isinstance(
            self.displacement_cells, int
        ):
            raise TypeError("displacement_cells must be an integer")
        value = np.asarray(self.matrix, dtype=np.complex128)
        if value.ndim != 2 or value.shape[0] == 0 or value.shape[0] != value.shape[1]:
            raise ValueError("matrix must be nonempty and square")
        if not np.all(np.isfinite(value)):
            raise ValueError("matrix must contain only finite values")
        immutable = np.frombuffer(
            value.tobytes(order="C"), dtype=np.complex128
        ).reshape(value.shape)
        object.__setattr__(self, "matrix", immutable)

    @property
    def orbital_count(self) -> int:
        """Return the represented orbital count."""
        return int(self.matrix.shape[0])


@dataclass(frozen=True, slots=True)
class Periodic1DFiniteHoppingToyModel:
    """Represent a finite Hermitian hopping family for a periodic-1D toy parent."""

    blocks: tuple[Periodic1DHoppingBlock, ...]
    energy_unit: str
    hermiticity_tolerance: float

    def __post_init__(self) -> None:
        if not self.blocks:
            raise ValueError("blocks must be nonempty")
        if not self.energy_unit:
            raise ValueError("energy_unit must be nonempty")
        if type(self.hermiticity_tolerance) is not float:
            raise TypeError("hermiticity_tolerance must be a float")
        if (
            not np.isfinite(self.hermiticity_tolerance)
            or self.hermiticity_tolerance <= 0.0
        ):
            raise ValueError("hermiticity_tolerance must be positive and finite")
        displacements = tuple(block.displacement_cells for block in self.blocks)
        if displacements != tuple(sorted(set(displacements))):
            raise ValueError("block displacements must be sorted and unique")
        if 0 not in displacements:
            raise ValueError("blocks must contain the zero-displacement block")
        orbital_count = self.blocks[0].orbital_count
        if any(block.orbital_count != orbital_count for block in self.blocks):
            raise ValueError("all hopping blocks must have the same shape")
        by_displacement = {block.displacement_cells: block for block in self.blocks}
        if tuple(sorted(by_displacement)) != tuple(
            range(min(displacements), max(displacements) + 1)
        ):
            raise ValueError("hopping displacements must form a contiguous range")
        for displacement, block in by_displacement.items():
            opposite = by_displacement.get(-displacement)
            if opposite is None or not np.allclose(
                block.matrix,
                opposite.matrix.conj().T,
                rtol=0.0,
                atol=self.hermiticity_tolerance,
            ):
                raise ValueError("hopping blocks must satisfy Hermiticity")

    @property
    def orbital_count(self) -> int:
        """Return the common hopping-block dimension."""
        return self.blocks[0].orbital_count


@dataclass(frozen=True, slots=True)
class Periodic1DPrimitiveFiberHamiltonianRequest:
    """Request one primitive-cell Bloch fiber from a finite-hopping toy model."""

    model: Periodic1DFiniteHoppingToyModel
    reduced_momentum: float | np.float64

    def __post_init__(self) -> None:
        if type(self.model) is not Periodic1DFiniteHoppingToyModel:
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

    model: Periodic1DFiniteHoppingToyModel
    cell_count: int
    reduced_momentum: float | np.float64

    def __post_init__(self) -> None:
        if type(self.model) is not Periodic1DFiniteHoppingToyModel:
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
