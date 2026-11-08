"""Complete periodic-3D rank-two block-hopping scientific model."""

from __future__ import annotations

from dataclasses import dataclass
from typing import final

from projectkoios.physkit.periodic.lattice import DirectLattice3D, DirectLatticeMetric
from projectkoios.physkit.periodic.lattice.finite_domain import LatticeDimension
from projectkoios.physkit.periodic.lattice.hopping import (
    BaseBlockHoppingModel,
    DenseBlockHoppingModel,
    SparseBlockHoppingModel,
)

from ksdft2effmass.periodic.models.base import PeriodicModelRole
from ksdft2effmass.periodic.models.block_hopping import PeriodicBlockHoppingModel
from ksdft2effmass.periodic.periodic3d.operators import Periodic3DBasisIdentity
from ksdft2effmass.periodic.periodic3d.rank2.models.base import Periodic3DRank2Model
from ksdft2effmass.periodic3d.geometry import Periodic3DLatticeGeometry


@final
@dataclass(frozen=True, slots=True, eq=False)
class Periodic3DRank2BlockHoppingModel(
    Periodic3DRank2Model,
    PeriodicBlockHoppingModel,
):
    """Represent one complete periodic-3D rank-two block-hopping model.

    Parameters
    ----------
    identifier
        Stable nonempty KSD scientific-model identity.
    role
        Exact scientific role without implying validation or acceptance.
    geometry
        Immutable ordered three-dimensional primitive basis together with its explicit
        physical length unit.
    basis
        Exact ordered three-dimensional periodic basis identity with two coordinates.
        Coordinate order is the row and column order of every hopping block.
    representation
        Immutable PhysKit ordinary-lattice model with three-dimensional displacements
        and exact ``2 x 2`` coefficient blocks.

    Raises
    ------
    TypeError
        If a value lacks its exact nominal owner.
    ValueError
        If dimension, retained rank, geometry, or exact Hermiticity is inconsistent.

    Notes
    -----
    The first inheritance branch refines the three-dimensional finite-rank scientific
    model to rank two. The second branch contributes dimension-neutral block-hopping
    representation behavior. PhysKit owns provider coefficient storage and lattice
    primitives; KSD owns basis correlation, unit-bearing geometry, model identity,
    role, and scientific admissibility.

    """

    identifier: str
    role: PeriodicModelRole
    geometry: Periodic3DLatticeGeometry
    basis: Periodic3DBasisIdentity
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
        if type(self.geometry) is not Periodic3DLatticeGeometry:
            raise TypeError("geometry must be Periodic3DLatticeGeometry")
        # The rank-two branch fixes the retained dimension. The block-hopping branch
        # owns basis-shape and Hermiticity admission. This concrete child supplies the
        # exact three-dimensional owner types required by that shared validation.
        self._validate_block_hopping_model(
            expected_dimension=LatticeDimension.THREE,
            expected_lattice_type=DirectLattice3D,
            expected_basis_type=Periodic3DBasisIdentity,
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
    def direct_lattice(self) -> DirectLattice3D:
        """Return a fresh exact PhysKit three-dimensional direct lattice.

        Returns
        -------
        DirectLattice3D
            Provider primitive reconstructed from the immutable physical geometry.

        """
        return self.geometry.direct_lattice

    @property
    def lattice_geometry(self) -> Periodic3DLatticeGeometry:
        """Return the immutable ordered three-dimensional lattice geometry.

        Returns
        -------
        Periodic3DLatticeGeometry
            Primitive-basis matrix snapshot together with its physical length unit.

        """
        return self.geometry

    @property
    def direct_metric(self) -> DirectLatticeMetric:
        """Return the metric derived from the exact lattice geometry.

        Returns
        -------
        DirectLatticeMetric
            Fresh metric backed by the reconstructed ``DirectLattice3D`` value.

        """
        return self.geometry.direct_metric

    @property
    def basis_identity(self) -> Periodic3DBasisIdentity:
        """Return the exact ordered basis of every hopping block.

        Returns
        -------
        Periodic3DBasisIdentity
            Two-coordinate basis value supplied explicitly at construction.

        Notes
        -----
        The basis coordinates identify block rows and columns. Ordinary-lattice
        displacements identify hopping support and remain separate values.

        """
        return self.basis

    @property
    def block_hopping_model(self) -> BaseBlockHoppingModel:
        """Return the immutable PhysKit block-hopping representation.

        Returns
        -------
        BaseBlockHoppingModel
            Exact dense or sparse provider value admitted by this model.

        """
        return self.representation


__all__ = ["Periodic3DRank2BlockHoppingModel"]
