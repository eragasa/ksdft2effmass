"""Dimension-neutral Bloch-hopping model contract."""

from __future__ import annotations

from abc import ABC, abstractmethod

from projectkoios.physkit.periodic.lattice.hopping import DenseBlockHoppingModel


class BlochHoppingModel(ABC):
    """Bind a PhysKit block-hopping representation to a retained state space.

    PhysKit owns immutable hopping storage. Dimensional and rank specializations own
    scientific interpretation, geometry, and admissibility policy.
    """

    __slots__ = ()

    @property
    @abstractmethod
    def block_hopping_model(self) -> DenseBlockHoppingModel:
        """Return the exact composed PhysKit ordinary-lattice model."""

    @property
    @abstractmethod
    def band_subspace_rank(self) -> int:
        """Return the retained-space dimension, not algebraic matrix rank."""


__all__ = ["BlochHoppingModel"]
