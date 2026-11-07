"""Complete periodic-3D rank-two block-hopping scientific model."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, final

from projectkoios.physkit.periodic.lattice import DirectLattice3D, DirectLatticeMetric
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
from ksdft2effmass.periodic3d.geometry import Periodic3DLatticeGeometry


@final
@dataclass(frozen=True, slots=True, eq=False)
class Periodic3DRank2BlockHoppingModel(PeriodicRank2BlockHoppingModel):
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
    representation
        Immutable PhysKit ordinary-lattice model with three-dimensional displacements
        and exact ``2 x 2`` coefficient blocks.

    Raises
    ------
    TypeError
        If a value lacks its exact nominal owner.
    ValueError
        If dimension, retained rank, geometry, or exact Hermiticity is inconsistent.

    """

    identifier: str
    role: PeriodicModelRole
    geometry: Periodic3DLatticeGeometry
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
        # The shared parent owns rank and Hermiticity admission; this child supplies
        # the exact ordered, unit-bearing dimensional lattice geometry.
        self._validate_rank2_block_hopping_model(
            expected_dimension=LatticeDimension.THREE,
            expected_lattice_type=DirectLattice3D,
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
    def block_hopping_model(self) -> BaseBlockHoppingModel:
        """Return the immutable PhysKit block-hopping representation.

        Returns
        -------
        BaseBlockHoppingModel
            Exact dense or sparse provider value admitted by this model.

        """
        return self.representation

    @property
    def spatial_dimension(self) -> Literal[3]:
        """Return the exact built-in periodic spatial dimension three.

        Returns
        -------
        Literal[3]
            Built-in integer three.

        """
        return 3


__all__ = ["Periodic3DRank2BlockHoppingModel"]
