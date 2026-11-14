"""Nominal periodic-3D arbitrary-rank scientific-model base."""

from abc import ABC, abstractmethod

from projectkoios.numerics.numpy.typing import Complex128Array, Float64Array

from ksdft2effmass.periodic.periodic3d.models import Periodic3DModel
from ksdft2effmass.periodic.periodic3d.operators import Periodic3DBasisIdentity


class Periodic3DRankNModel(Periodic3DModel, ABC):
    """Identify periodic-3D models with an explicit finite retained basis.

    Notes
    -----
    Spatial dimension and retained rank are independent. This owner fixes spatial
    dimension three while concrete descendants provide both a positive retained rank
    and an exact ordered :class:`Periodic3DBasisIdentity` of that size.
    """

    __slots__ = ()

    @property
    @abstractmethod
    def basis_identity(self) -> Periodic3DBasisIdentity:
        """Return the exact ordered basis of the retained band subspace.

        Returns
        -------
        Periodic3DBasisIdentity
            Compatibility-bearing coordinate sequence for the retained
            three-dimensional periodic operator space.

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


class Periodic3DRankNParentModel(Periodic3DRankNModel, ABC):
    """Define the reusable field contract for a finite-rank periodic-3D parent.

    Concrete analytic, provider-backed, and calculation-owned parent families supply
    their own spectra, ambient embedding, support, and isolation-gap lower bound.
    Alignment and locality actions consume this contract without owning those formulas.
    """

    __slots__ = ()

    @property
    @abstractmethod
    def positive_bonds(self) -> tuple[tuple[int, int, int], ...]:
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


__all__ = ["Periodic3DRankNModel", "Periodic3DRankNParentModel"]
