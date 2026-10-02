"""Finite-hopping one-dimensional periodic toy models.

The module owns the scientific toy parent and its immutable directed hopping blocks.
Finite-fiber and supercell construction remain campaign numerical mechanics until
their represented-operator migration is completed.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
import numpy.typing as npt

from ksdft2effmass.periodic import Periodic1DModel, PeriodicModelRole

type ComplexMatrix = npt.NDArray[np.complex128]


@dataclass(frozen=True, slots=True)
class Periodic1DHoppingBlock:
    """Represent one directed hopping block at an integer cell displacement.

    Parameters
    ----------
    displacement_cells
        Exact built-in integer displacement from source cell to target cell.
    matrix
        Nonempty square finite NumPy matrix. Integer, floating, and complex NumPy
        dtypes are accepted and copied into non-writeable C-contiguous
        ``complex128`` storage. Boolean, string, byte, and object arrays are
        rejected rather than coerced.

    Raises
    ------
    TypeError
        If displacement is not exactly a built-in integer, matrix is not a NumPy
        array, or its scalar dtype is not integer, floating, or complex.
    ValueError
        If matrix is empty, nonsquare, not two-dimensional, nonfinite, or cannot
        be represented as finite ``complex128`` values.

    Notes
    -----
    This record stores one directed coefficient only. Pairwise Hermiticity is a
    relation owned by :class:`Periodic1DFiniteHoppingToyModel`.
    """

    displacement_cells: int
    matrix: ComplexMatrix

    def __post_init__(self) -> None:
        """Validate and defensively canonicalize one hopping block."""
        if type(self.displacement_cells) is not int:
            raise TypeError("displacement_cells must be a built-in int")
        if not isinstance(self.matrix, np.ndarray):
            raise TypeError("matrix must be a numpy.ndarray")
        if self.matrix.dtype.kind not in "iufc":
            raise TypeError("matrix dtype must be integer, floating, or complex")
        try:
            value = np.asarray(self.matrix, dtype=np.complex128)
        except (OverflowError, ValueError) as exc:
            raise ValueError(
                "matrix values must be representable as complex128"
            ) from exc
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


@dataclass(frozen=True, slots=True, init=False)
class Periodic1DFiniteHoppingToyModel(Periodic1DModel):
    """Represent a finite Hermitian hopping family as a nominal 1D toy model.

    Parameters
    ----------
    model_id
        Stable nonempty identity of this configured scientific toy model.
    blocks
        Nonempty exact tuple of directed hopping blocks. Displacements must be
        unique, increasing, contiguous, include zero, and use one common square
        orbital dimension. Every displacement ``R`` must have ``-R`` and satisfy
        ``H_R = H_{-R}^dagger`` under ``hermiticity_tolerance``.
    energy_unit
        Nonempty exact textual unit shared by all hopping blocks. This class does
        not interpret or convert the unit.
    hermiticity_tolerance
        Positive finite built-in float used as an inclusive absolute tolerance
        with zero relative tolerance for pairwise block Hermiticity.

    Raises
    ------
    TypeError
        If identity, block tuple, block members, unit, or tolerance has the wrong
        semantic type.
    ValueError
        If identity or unit is empty, tolerance is not positive and finite, block
        dimensions or displacements disagree, or pairwise Hermiticity fails.

    Attributes
    ----------
    blocks
        Ordered immutable hopping-block tuple.
    energy_unit
        Exact hopping-energy unit string.
    hermiticity_tolerance
        Absolute pairwise Hermiticity tolerance.

    Notes
    -----
    The model has the exact :attr:`~ksdft2effmass.periodic.PeriodicModelRole.TOY`
    role and nominal one-dimensional membership. Passing its structural and
    Hermiticity checks is software verification, not evidence for a material,
    physical completeness, scientific validation, or uncertainty quantification.
    """

    _model_id: str = field(repr=False)
    blocks: tuple[Periodic1DHoppingBlock, ...]
    energy_unit: str
    hermiticity_tolerance: float

    def __init__(
        self,
        model_id: str,
        blocks: tuple[Periodic1DHoppingBlock, ...],
        energy_unit: str,
        hermiticity_tolerance: float,
    ) -> None:
        """Store constructor arguments before intrinsic validation."""
        object.__setattr__(self, "_model_id", model_id)
        object.__setattr__(self, "blocks", blocks)
        object.__setattr__(self, "energy_unit", energy_unit)
        object.__setattr__(self, "hermiticity_tolerance", hermiticity_tolerance)
        self.__post_init__()

    def __post_init__(self) -> None:
        """Validate identity, ordered block family, dimensions, and Hermiticity."""
        if type(self.model_id) is not str:
            raise TypeError("model_id must be a built-in str")
        if self.model_id == "":
            raise ValueError("model_id must be nonempty")
        if type(self.blocks) is not tuple:
            raise TypeError("blocks must be an exact tuple")
        if not self.blocks:
            raise ValueError("blocks must be nonempty")
        if any(type(block) is not Periodic1DHoppingBlock for block in self.blocks):
            raise TypeError("every block must be Periodic1DHoppingBlock")
        if type(self.energy_unit) is not str:
            raise TypeError("energy_unit must be a built-in str")
        if self.energy_unit == "":
            raise ValueError("energy_unit must be nonempty")
        if type(self.hermiticity_tolerance) is not float:
            raise TypeError("hermiticity_tolerance must be a built-in float")
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
    def model_id(self) -> str:
        """Return the stable configured-model identity."""
        return self._model_id

    @property
    def model_role(self) -> PeriodicModelRole:
        """Return the exact toy-model evidentiary role."""
        return PeriodicModelRole.TOY

    @property
    def orbital_count(self) -> int:
        """Return the common hopping-block dimension."""
        return self.blocks[0].orbital_count


__all__ = ["Periodic1DFiniteHoppingToyModel", "Periodic1DHoppingBlock"]
