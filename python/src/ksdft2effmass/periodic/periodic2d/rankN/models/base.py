"""Nominal periodic-2D arbitrary-rank scientific-model base."""

from abc import ABC, abstractmethod

from projectkoios.numerics.numpy.typing import Complex128Array, Float64Array

from ksdft2effmass.periodic.periodic2d.models import Periodic2DModel
from ksdft2effmass.periodic.periodic2d.operators import Periodic2DBasisIdentity


class Periodic2DRankNModel(Periodic2DModel, ABC):
    """Identify periodic-2D models with an explicit finite retained basis.

    Notes
    -----
    Spatial dimension and retained rank are independent. This owner fixes spatial
    dimension two while concrete descendants provide both a positive retained rank
    and an exact ordered :class:`Periodic2DBasisIdentity` of that size.
    """

    __slots__ = ()

    @property
    @abstractmethod
    def basis_identity(self) -> Periodic2DBasisIdentity:
        """Return the exact ordered basis of the retained band subspace.

        Returns
        -------
        Periodic2DBasisIdentity
            Compatibility-bearing coordinate sequence for the retained two-dimensional
            periodic operator space.

        Notes
        -----
        Concrete families must establish this identity explicitly. Provider labels,
        model names, retained rank, geometry, and hopping support do not determine it.
        """

    @property
    @abstractmethod
    def band_subspace_rank(self) -> int:
        """Return the concrete family's admitted finite band-subspace rank.

        Returns
        -------
        int
            Positive built-in retained-space dimension supplied by a concrete family.

        """


class Periodic2DRankNParentModel(Periodic2DRankNModel, ABC):
    """Define the reusable field contract for a finite-rank periodic-2D parent.

    Concrete analytic, provider-backed, and calculation-owned parent families supply
    their own spectra, ambient embedding, support, and isolation-gap lower bound.
    Alignment and locality actions consume this contract without owning those formulas.
    """

    __slots__ = ()

    @property
    @abstractmethod
    def model_id(self) -> str:
        """Return the stable identity of the concrete parent model."""

    @property
    @abstractmethod
    def positive_bonds(self) -> tuple[tuple[int, int], ...]:
        """Return the ordered positive harmonic-bond support."""

    @property
    @abstractmethod
    def parent_scale(self) -> float:
        """Return the concrete parent's dimensionless coupling scale."""

    @property
    @abstractmethod
    def ambient_dimension(self) -> int:
        """Return the dimension of the parent operator representation."""

    @property
    @abstractmethod
    def isolation_gap_lower_bound(self) -> float:
        """Return the concrete family's declared isolation-gap lower bound."""

    @abstractmethod
    def structure_factor(
        self,
        reduced_coordinates: Float64Array,
    ) -> Float64Array:
        """Return the concrete parent's dimensionless harmonic structure factor."""

    @abstractmethod
    def retained_energies(
        self,
        reduced_coordinates: Float64Array,
    ) -> Float64Array:
        """Return ordered retained-sector energies at supplied coordinates."""

    @abstractmethod
    def exterior_energies(
        self,
        reduced_coordinates: Float64Array,
    ) -> Float64Array:
        """Return ordered exterior-sector energies at supplied coordinates."""

    @abstractmethod
    def parent_hamiltonians(
        self,
        reduced_coordinates: Float64Array,
    ) -> Complex128Array:
        """Return parent operators in their ambient basis."""

    @abstractmethod
    def reference_frames(
        self,
        reduced_coordinates: Float64Array,
    ) -> Complex128Array:
        """Return frames embedding the retained sector into the parent space."""

    @abstractmethod
    def exact_reduced_hamiltonians(
        self,
        reduced_coordinates: Float64Array,
    ) -> Complex128Array:
        """Return exact retained operators in the reference frame."""


__all__ = ["Periodic2DRankNModel", "Periodic2DRankNParentModel"]
