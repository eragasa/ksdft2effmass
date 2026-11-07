"""Complete periodic-1D rank-two block-hopping scientific model."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, final

from projectkoios.physkit.periodic.lattice import DirectLattice1D
from projectkoios.physkit.periodic.lattice.finite_domain import LatticeDimension
from projectkoios.physkit.periodic.lattice.hopping import (
    BaseBlockHoppingModel,
    DenseBlockHoppingModel,
    SparseBlockHoppingModel,
)

from ksdft2effmass.periodic.models.base import PeriodicModelRole
from ksdft2effmass.periodic.models.block_hopping import (
    PeriodicRank2BlockHoppingModel,
)
from ksdft2effmass.periodic1d.geometry import Periodic1DLatticeGeometry


@final
@dataclass(frozen=True, slots=True, eq=False)
class Periodic1DRank2BlockHoppingModel(PeriodicRank2BlockHoppingModel):
    """Represent one complete periodic-1D rank-two block-hopping model.

    Parameters
    ----------
    identifier
        Stable nonempty KSD scientific-model identity.
    role
        Exact scientific role without implying validation or acceptance.
    geometry
        Immutable physical primitive-period convention for the one-dimensional
        lattice.
    representation
        Immutable PhysKit ordinary-lattice model with one-dimensional displacements
        and exact ``2 x 2`` coefficient blocks.

    Raises
    ------
    TypeError
        If a value lacks its exact nominal owner.
    ValueError
        If dimension, retained rank, geometry, or exact Hermiticity is inconsistent.

    Notes
    -----
    PhysKit owns the reconstructed :class:`DirectLattice1D` primitive. KSD retains
    :class:`Periodic1DLatticeGeometry` because the scientific model must also bind the
    caller-declared physical length unit, which is not part of the provider lattice.

    """

    identifier: str
    role: PeriodicModelRole
    geometry: Periodic1DLatticeGeometry
    representation: DenseBlockHoppingModel | SparseBlockHoppingModel

    def __post_init__(self) -> None:
        """Validate the complete dimensional scientific-model contract.

        Raises
        ------
        TypeError
            If identity, role, geometry, lattice, representation, or terms lack their
            exact nominal owners.
        ValueError
            If identity is empty or dimension, rank, support, or exact Hermiticity is
            inconsistent.

        """
        if type(self.geometry) is not Periodic1DLatticeGeometry:
            raise TypeError("geometry must be Periodic1DLatticeGeometry")
        # The shared parent owns rank and Hermiticity admission; this child supplies
        # the exact one-dimensional lattice reconstructed from immutable geometry.
        self._validate_rank2_block_hopping_model(
            expected_dimension=LatticeDimension.ONE,
            expected_lattice_type=DirectLattice1D,
        )

    @property
    def model_id(self) -> str:
        """Return the stable KSD scientific-model identity.

        Returns
        -------
        str
            Nonempty identity supplied at construction.

        """
        return self.identifier

    @property
    def model_role(self) -> PeriodicModelRole:
        """Return the exact scientific-model role.

        Returns
        -------
        PeriodicModelRole
            Closed evidentiary role supplied at construction.

        """
        return self.role

    @property
    def direct_lattice(self) -> DirectLattice1D:
        """Return a fresh exact PhysKit one-dimensional direct lattice.

        Returns
        -------
        DirectLattice1D
            Provider primitive reconstructed from the immutable physical geometry.

        """
        return self.geometry.direct_lattice

    @property
    def lattice_geometry(self) -> Periodic1DLatticeGeometry:
        """Return the immutable physical one-dimensional lattice geometry.

        Returns
        -------
        Periodic1DLatticeGeometry
            Primitive period together with its explicit physical length unit.

        """
        return self.geometry

    @property
    def block_hopping_model(self) -> BaseBlockHoppingModel:
        """Return the immutable PhysKit block-hopping representation.

        Returns
        -------
        BaseBlockHoppingModel
            Exact dense or sparse provider value admitted by this model.

        """
        return self.representation

    @property
    def spatial_dimension(self) -> Literal[1]:
        """Return the exact built-in periodic spatial dimension one.

        Returns
        -------
        Literal[1]
            Built-in integer one.

        """
        return 1


__all__ = ["Periodic1DRank2BlockHoppingModel"]
