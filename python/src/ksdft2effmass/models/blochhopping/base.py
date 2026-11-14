"""Dimension-neutral Bloch-hopping model contract."""

from __future__ import annotations

from abc import ABC, abstractmethod

from projectkoios.physkit.periodic.lattice.hopping import DenseBlockHoppingModel

from ksdft2effmass.models.base import Model


class BlochHoppingModel(Model, ABC):
    """Bind a PhysKit block-hopping representation to a retained state space.

    Notes
    -----
    PhysKit owns immutable hopping storage. Dimensional and rank specializations own
    scientific interpretation, geometry, and admissibility policy. The retained-space
    rank is distinct from the algebraic rank of any individual coefficient matrix.
    """

    __slots__ = ()

    @property
    @abstractmethod
    def block_hopping_model(self) -> DenseBlockHoppingModel:
        """Return the composed ordinary-lattice hopping model.

        Returns
        -------
        DenseBlockHoppingModel
            Exact immutable PhysKit model retained by the specialization.
        """

    @property
    @abstractmethod
    def band_subspace_rank(self) -> int:
        """Return the retained-space dimension.

        Returns
        -------
        int
            Positive retained basis size, not algebraic matrix rank.
        """


__all__ = ["BlochHoppingModel"]
