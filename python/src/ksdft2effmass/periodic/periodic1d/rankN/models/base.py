"""Nominal periodic-1D arbitrary-rank scientific-model bases."""

from abc import ABC, abstractmethod

from projectkoios.physkit.numerics.typing.numpy.arrays import ComplexArray, RealArray

from ksdft2effmass.periodic.periodic1d.models import Periodic1DModel
from ksdft2effmass.periodic.periodic1d.operators import Periodic1DBasisIdentity


class Periodic1DRankNModel(Periodic1DModel, ABC):
    """Identify periodic-1D models with an explicit finite retained basis.

    Notes
    -----
    Spatial dimension and retained rank are independent. This owner fixes spatial
    dimension one while concrete descendants provide both a positive retained rank
    and an exact ordered :class:`Periodic1DBasisIdentity` of that size.
    """

    __slots__ = ()

    @property
    @abstractmethod
    def basis_identity(self) -> Periodic1DBasisIdentity:
        """Return the exact ordered basis of the retained band subspace.

        Returns
        -------
        Periodic1DBasisIdentity
            Compatibility-bearing coordinate sequence for the retained one-dimensional
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


class Periodic1DRankNParentModel(Periodic1DRankNModel, ABC):
    """Define the reusable field contract for a finite-rank parent model.

    Concrete analytic, provider-backed, and calculation-owned parent families supply
    their own spectra, ambient embedding, and exact isolation certificate. Numerical
    alignment and locality actions consume this contract without owning those formulas.
    """

    __slots__ = ()

    @property
    @abstractmethod
    def ambient_dimension(self) -> int:
        """Return the dimension of the parent operator representation."""

    @property
    @abstractmethod
    def endpoint_sewing_map(self) -> ComplexArray:
        """Return the ambient-dimensional reciprocal-endpoint sewing map."""

    @property
    @abstractmethod
    def exact_isolation_gap(self) -> float:
        """Return the concrete family's declared exact isolation gap."""

    @abstractmethod
    def retained_energies(self, reduced_coordinates: RealArray) -> RealArray:
        """Return ordered retained-sector energies at supplied coordinates."""

    @abstractmethod
    def exterior_energies(self, reduced_coordinates: RealArray) -> RealArray:
        """Return ordered exterior-sector energies at supplied coordinates."""

    @abstractmethod
    def parent_hamiltonians(self, reduced_coordinates: RealArray) -> ComplexArray:
        """Return parent operators in their ambient basis."""

    @abstractmethod
    def reference_frames(self, reduced_coordinates: RealArray) -> ComplexArray:
        """Return frames embedding the retained sector into the parent space."""

    @abstractmethod
    def exact_reduced_hamiltonians(
        self,
        reduced_coordinates: RealArray,
    ) -> ComplexArray:
        """Return exact retained operators in the reference frame."""


__all__ = ["Periodic1DRankNModel", "Periodic1DRankNParentModel"]
