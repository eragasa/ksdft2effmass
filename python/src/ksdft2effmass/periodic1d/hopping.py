"""Finite-hopping one-dimensional periodic toy models.

The module owns the scientific toy parent and its immutable directed hopping blocks.
Finite-fiber and supercell construction remain campaign numerical mechanics until
their represented-operator migration is completed.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
import numpy.typing as npt

from ksdft2effmass.analysis.hopping_fits import (
    BlockHoppingLeastSquaresFitResult1D,
)
from ksdft2effmass.periodic import (
    Periodic1DModel,
    PeriodicModelRole,
    PeriodicRetainedOperator,
)
from ksdft2effmass.solid_state import (
    BlockHoppingModel1D,
    BlockHoppingTruncationResult1D,
    ReciprocalOperatorFourierTransformResult1D,
)

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
        self._check_args_model_identity()
        self._check_args_block_inventory()
        self._check_args_energy_metadata()
        self._check_args_block_order_and_dimension()
        self._check_args_pairwise_hermiticity()

    def _check_args_model_identity(self) -> None:
        """Require one exact nonempty configured-model identity."""
        if type(self.model_id) is not str:
            raise TypeError("model_id must be a built-in str")
        if self.model_id == "":
            raise ValueError("model_id must be nonempty")

    def _check_args_block_inventory(self) -> None:
        """Require one nonempty immutable inventory of exact hopping blocks."""
        if type(self.blocks) is not tuple:
            raise TypeError("blocks must be an exact tuple")
        if not self.blocks:
            raise ValueError("blocks must be nonempty")
        if any(type(block) is not Periodic1DHoppingBlock for block in self.blocks):
            raise TypeError("every block must be Periodic1DHoppingBlock")

    def _check_args_energy_metadata(self) -> None:
        """Require an explicit unit and positive finite Hermiticity tolerance."""
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

    def _check_args_block_order_and_dimension(self) -> None:
        """Require contiguous ordered displacements and one orbital dimension."""
        displacements = tuple(block.displacement_cells for block in self.blocks)
        if displacements != tuple(sorted(set(displacements))):
            raise ValueError("block displacements must be sorted and unique")
        if 0 not in displacements:
            raise ValueError("blocks must contain the zero-displacement block")
        orbital_count = self.blocks[0].orbital_count
        if any(block.orbital_count != orbital_count for block in self.blocks):
            raise ValueError("all hopping blocks must have the same shape")
        if displacements != tuple(range(min(displacements), max(displacements) + 1)):
            raise ValueError("hopping displacements must form a contiguous range")

    def _check_args_pairwise_hermiticity(self) -> None:
        """Require every directed block to equal its opposite adjoint."""
        by_displacement = {block.displacement_cells: block for block in self.blocks}
        # A finite hopping family represents one Hermitian parent only when every
        # directed coefficient has the explicitly stored opposite-cell adjoint.
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


@dataclass(frozen=True, slots=True, eq=False)
class Periodic1DCompleteHoppingRepresentationResult:
    """Bind a complete finite-mesh hopping transform to an exact retained operator.

    Parameters
    ----------
    retained_operator
        Exact scientific operator on the identified retained space.
    transform
        Complete centered Born--von Karman Fourier-transform result retaining every
        mesh representative and its reconstruction diagnostics.

    Raises
    ------
    TypeError
        If either field has the wrong exact public type.
    ValueError
        If hopping-block dimension differs from retained-space rank.

    Notes
    -----
    This AbstractResultObject is an operator representation, not an effective model.
    A failed reconstruction diagnostic remains represented explicitly and is not
    converted to
    acceptance by construction.
    """

    retained_operator: PeriodicRetainedOperator
    transform: ReciprocalOperatorFourierTransformResult1D

    def __post_init__(self) -> None:
        """Validate exact types and retained-operator representation rank."""
        if type(self.retained_operator) is not PeriodicRetainedOperator:
            raise TypeError("retained_operator must be PeriodicRetainedOperator")
        if type(self.transform) is not ReciprocalOperatorFourierTransformResult1D:
            raise TypeError(
                "transform must be ReciprocalOperatorFourierTransformResult1D"
            )
        if (
            self.transform.hopping_model.matrix_dimension
            != self.retained_operator.retained_subspace.rank
        ):
            raise ValueError("complete hopping dimension must equal retained rank")


@dataclass(frozen=True, slots=True, eq=False)
class Periodic1DTruncatedHoppingEffectiveModelResult:
    """Identify one finite-range effective model constructed by truncation.

    Parameters
    ----------
    effective_model_id
        Stable nonempty identity of the approximate model.
    retained_operator
        Exact retained operator approximated by the effective model.
    truncation
        Explicit symmetric finite-range truncation result, including complete source
        coefficients, retained range, truncated coefficients, and omitted norm.

    Raises
    ------
    TypeError
        If identity or composed result fields have incorrect exact types.
    ValueError
        If identity is empty or model dimension differs from retained rank.

    Notes
    -----
    Construction records approximation provenance but makes no accuracy or acceptance
    claim; those conclusions remain with separate comparison results.
    """

    effective_model_id: str
    retained_operator: PeriodicRetainedOperator
    truncation: BlockHoppingTruncationResult1D

    def __post_init__(self) -> None:
        """Validate identity, exact types, and retained-operator rank."""
        if type(self.effective_model_id) is not str:
            raise TypeError("effective_model_id must be a built-in str")
        if self.effective_model_id == "":
            raise ValueError("effective_model_id must be nonempty")
        if type(self.retained_operator) is not PeriodicRetainedOperator:
            raise TypeError("retained_operator must be PeriodicRetainedOperator")
        if type(self.truncation) is not BlockHoppingTruncationResult1D:
            raise TypeError("truncation must be BlockHoppingTruncationResult1D")
        if (
            self.truncation.truncated.matrix_dimension
            != self.retained_operator.retained_subspace.rank
        ):
            raise ValueError("truncated hopping dimension must equal retained rank")

    @property
    def model(self) -> BlockHoppingModel1D:
        """Return the finite-range effective hopping coefficients."""
        return self.truncation.truncated


@dataclass(frozen=True, slots=True, eq=False)
class Periodic1DFittedHoppingEffectiveModelResult:
    """Identify one finite-range effective model constructed by weighted fitting.

    Parameters
    ----------
    effective_model_id
        Stable nonempty identity of the approximate model.
    retained_operator
        Exact retained operator approximated by the effective model.
    fit
        Explicit weighted least-squares result, including source samples, coefficient
        representatives, weights, fitted coefficients, rank, conditioning, and
        training residuals.

    Raises
    ------
    TypeError
        If identity or composed result fields have incorrect exact types.
    ValueError
        If identity is empty or fitted dimension differs from retained rank.

    Notes
    -----
    Construction does not imply identifiability, approximation adequacy, withheld-data
    agreement, scientific validation, or uncertainty quantification.
    """

    effective_model_id: str
    retained_operator: PeriodicRetainedOperator
    fit: BlockHoppingLeastSquaresFitResult1D

    def __post_init__(self) -> None:
        """Validate identity, exact types, and retained-operator rank."""
        if type(self.effective_model_id) is not str:
            raise TypeError("effective_model_id must be a built-in str")
        if self.effective_model_id == "":
            raise ValueError("effective_model_id must be nonempty")
        if type(self.retained_operator) is not PeriodicRetainedOperator:
            raise TypeError("retained_operator must be PeriodicRetainedOperator")
        if type(self.fit) is not BlockHoppingLeastSquaresFitResult1D:
            raise TypeError("fit must be BlockHoppingLeastSquaresFitResult1D")
        if (
            self.fit.fitted_model.matrix_dimension
            != self.retained_operator.retained_subspace.rank
        ):
            raise ValueError("fitted hopping dimension must equal retained rank")

    @property
    def model(self) -> BlockHoppingModel1D:
        """Return the fitted finite-range effective hopping coefficients."""
        return self.fit.fitted_model


__all__ = [
    "Periodic1DCompleteHoppingRepresentationResult",
    "Periodic1DFiniteHoppingToyModel",
    "Periodic1DFittedHoppingEffectiveModelResult",
    "Periodic1DHoppingBlock",
    "Periodic1DTruncatedHoppingEffectiveModelResult",
]
