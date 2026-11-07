"""Complete periodic-2D rank-two block-hopping scientific model."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, final

from projectkoios.physkit.periodic.lattice import DirectLattice2D, DirectLatticeMetric
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
from ksdft2effmass.periodic2d.geometry import Periodic2DLatticeGeometry


@final
@dataclass(frozen=True, slots=True, eq=False)
class Periodic2DRank2BlockHoppingModel(PeriodicRank2BlockHoppingModel):
    """Represent one complete periodic-2D rank-two block-hopping model.

    Parameters
    ----------
    identifier
        Stable nonempty KSD scientific-model identity.
    role
        Exact scientific role without implying validation or acceptance.
    geometry
        Immutable ordered two-dimensional primitive basis together with its explicit
        physical length unit.
    representation
        Immutable PhysKit ordinary-lattice model with two-dimensional displacements
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
    geometry: Periodic2DLatticeGeometry
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
        if type(self.geometry) is not Periodic2DLatticeGeometry:
            raise TypeError("geometry must be Periodic2DLatticeGeometry")
        # The shared parent owns rank and Hermiticity admission; this child supplies
        # the exact ordered, unit-bearing dimensional lattice geometry.
        self._validate_rank2_block_hopping_model(
            expected_dimension=LatticeDimension.TWO,
            expected_lattice_type=DirectLattice2D,
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
    def direct_lattice(self) -> DirectLattice2D:
        """Return a fresh exact PhysKit two-dimensional direct lattice.

        Returns
        -------
        DirectLattice2D
            Provider primitive reconstructed from the immutable physical geometry.

        """
        return self.geometry.direct_lattice

    @property
    def lattice_geometry(self) -> Periodic2DLatticeGeometry:
        """Return the immutable ordered two-dimensional lattice geometry.

        Returns
        -------
        Periodic2DLatticeGeometry
            Primitive-basis matrix snapshot together with its physical length unit.

        """
        return self.geometry

    @property
    def direct_metric(self) -> DirectLatticeMetric:
        """Return the metric derived from the exact lattice geometry.

        Returns
        -------
        DirectLatticeMetric
            Fresh metric backed by the reconstructed ``DirectLattice2D`` value.

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
    def spatial_dimension(self) -> Literal[2]:
        """Return the exact built-in periodic spatial dimension two.

        Returns
        -------
        Literal[2]
            Built-in integer two.

        """
        return 2


__all__ = ["Periodic2DRank2BlockHoppingModel"]
