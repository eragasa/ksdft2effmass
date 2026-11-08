"""Dimension-neutral periodic rank-two block-hopping model contracts."""

from __future__ import annotations

from abc import abstractmethod
from typing import Literal, final

import numpy as np
from projectkoios.physkit.numerics.typing.numpy.arrays import ComplexMatrix
from projectkoios.physkit.periodic.lattice import (
    DirectLattice1D,
    DirectLattice2D,
    DirectLattice3D,
)
from projectkoios.physkit.periodic.lattice.finite_domain import LatticeDimension
from projectkoios.physkit.periodic.lattice.hopping import (
    BaseBlockHoppingModel,
    DenseBlockHoppingModel,
    DenseBlockHoppingTerm,
    SparseBlockHoppingModel,
    SparseBlockHoppingTerm,
)

from .base import PeriodicModel, PeriodicModelRole


class PeriodicBlockHoppingModel(PeriodicModel):
    """Bind a periodic scientific model to an ordinary block-hopping representation.

    This owner fixes the representation family without selecting retained rank or
    spatial dimension. PhysKit owns immutable dense and sparse coefficient storage;
    KSD owns scientific-model identity, dimensional geometry, role, and admissibility.
    """

    __slots__ = ()

    @property
    @abstractmethod
    def block_hopping_model(self) -> BaseBlockHoppingModel:
        """Return the exact immutable PhysKit block-hopping representation.

        Returns
        -------
        BaseBlockHoppingModel
            Provider-owned dense or sparse ordinary-lattice coefficient storage.

        """

    @property
    @abstractmethod
    def direct_lattice(
        self,
    ) -> DirectLattice1D | DirectLattice2D | DirectLattice3D:
        """Return the exact PhysKit direct lattice bound to the model.

        Returns
        -------
        DirectLattice1D | DirectLattice2D | DirectLattice3D
            Provider lattice whose primitive geometry defines ordinary displacements.

        Notes
        -----
        Dimensional children may retain richer immutable geometry or metric values, but
        the shared model family requires only their exact PhysKit direct lattice.

        """

    @property
    @abstractmethod
    def band_subspace_rank(self) -> int:
        """Return the retained primitive-cell state-space dimension.

        Returns
        -------
        int
            Positive built-in rank of each hopping coefficient block.

        """


class PeriodicRank2BlockHoppingModel(PeriodicBlockHoppingModel):
    """Fix retained rank two for periodic block-hopping scientific models.

    The class remains abstract in effect because it does not choose a spatial
    dimension, concrete lattice geometry, scientific role, identity, or provider
    representation. Dimensional children complete those contracts.
    """

    __slots__ = ()

    def __init_subclass__(cls) -> None:
        """Reject attempts to replace the inherited rank-two identity.

        Raises
        ------
        TypeError
            If a child declares its own ``band_subspace_rank`` property.

        """
        super().__init_subclass__()
        if "band_subspace_rank" in cls.__dict__:
            raise TypeError(
                "PeriodicRank2BlockHoppingModel subclasses cannot override "
                "band_subspace_rank"
            )

    @property
    @final
    def band_subspace_rank(self) -> Literal[2]:
        """Return the exact retained band-subspace rank two.

        Returns
        -------
        Literal[2]
            Built-in integer two fixed by the inherited model family.

        """
        return 2

    def _validate_rank2_block_hopping_model(
        self,
        *,
        expected_dimension: LatticeDimension,
        expected_lattice_type: (
            type[DirectLattice1D] | type[DirectLattice2D] | type[DirectLattice3D]
        ),
    ) -> None:
        """Validate shared rank, dimension, geometry, and Hermiticity invariants.

        Parameters
        ----------
        expected_dimension
            Exact PhysKit ordinary-lattice dimension required by the dimensional
            scientific-model child.
        expected_lattice_type
            Exact PhysKit direct-lattice class required by the child.

        Raises
        ------
        TypeError
            If identity, role, lattice, or provider representation lacks its exact
            nominal owner.
        ValueError
            If identity is empty, dimensions disagree, coefficient blocks are not
            ``2 x 2``, or ordinary support is not exactly Hermitian.

        """
        if type(self.model_id) is not str:
            raise TypeError("model_id must be a built-in string")
        if not self.model_id:
            raise ValueError("model_id must be nonempty")
        if type(self.model_role) is not PeriodicModelRole:
            raise TypeError("model_role must be PeriodicModelRole")
        if type(self.direct_lattice) is not expected_lattice_type:
            raise TypeError(
                f"direct_lattice must be the exact {expected_lattice_type.__name__}"
            )

        representation = self.block_hopping_model
        if type(representation) not in (
            DenseBlockHoppingModel,
            SparseBlockHoppingModel,
        ):
            raise TypeError(
                "block_hopping_model must be an exact PhysKit dense or sparse "
                "block-hopping model"
            )
        if representation.dimension is not expected_dimension:
            raise ValueError(
                "block_hopping_model dimension must match the dimensional model"
            )
        if representation.basis_size != 2:
            raise ValueError("block_hopping_model must have retained basis size two")

        # Index coefficients by ordinary-lattice displacement so admissibility is
        # independent of provider term order and dense versus sparse storage.
        coefficients: dict[tuple[int, ...], ComplexMatrix] = {}
        for term in representation.terms:
            if type(term) is DenseBlockHoppingTerm:
                coefficient = term.coefficient.magnitude
            elif type(term) is SparseBlockHoppingTerm:
                # Hermiticity is a scientific admissibility check. Sparse provider
                # storage is materialized only at this explicit validation boundary.
                coefficient = term.coefficient.to_dense().magnitude
            else:
                raise TypeError(
                    "block_hopping_model terms must use one exact PhysKit block term"
                )
            coefficients[term.displacement.components] = np.asarray(
                coefficient,
                dtype=np.complex128,
            )

        # Scientific-model admission is exact: no tolerance is introduced here.
        # Numerically approximate transformed coefficients remain representations
        # until a separately specified model-construction policy resolves roundoff.
        for displacement, coefficient in coefficients.items():
            opposite_displacement = tuple(-component for component in displacement)
            opposite = coefficients.get(opposite_displacement)
            if opposite is None:
                raise ValueError(
                    "every hopping displacement must have its conjugate partner"
                )
            if not np.array_equal(opposite, np.conjugate(coefficient.T)):
                raise ValueError(
                    "opposite hopping coefficients must be exact conjugate transposes"
                )


__all__ = ["PeriodicBlockHoppingModel", "PeriodicRank2BlockHoppingModel"]
