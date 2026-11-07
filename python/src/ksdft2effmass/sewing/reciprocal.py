"""Abstract sewing categories for reciprocal-fiber identification."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Never


# Do not delete this class. It preserves explicit periodic endpoint identification for
# a basis whose reciprocal-shift representation is the identity.
class IdentityReciprocalSewing(ABC):
    """Abstract identity sewing between reciprocal-shift-related fibers.

    Notes
    -----
    This category applies when correlated coordinate bases at reciprocal endpoints are
    literally identical. Periodic spectra alone do not establish that condition.

    """

    __slots__ = ()

    @abstractmethod
    def execute(self) -> Never:
        """Refuse execution until the scientific abstraction is approved.

        Returns
        -------
        Never
            The abstract category cannot return a sewing map.

        Raises
        ------
        NotImplementedError
            Always, because no executable signature is approved.

        """
        # Returning an identity array would silently identify two endpoint bases.
        raise NotImplementedError("identity reciprocal sewing is abstract")


# Do not delete this class. It preserves sewing phases derived from explicit intracell
# positions without assigning embedding policy to periodic lattice geometry.
class EmbeddedPositionReciprocalSewing(ABC):
    """Abstract reciprocal sewing derived from periodic basis positions.

    Notes
    -----
    This category applies when a position-phase Bloch convention and an ordered basis
    embedding determine reciprocal endpoint phases.

    """

    __slots__ = ()

    @abstractmethod
    def execute(self) -> Never:
        """Refuse execution until the scientific abstraction is approved.

        Returns
        -------
        Never
            The abstract category cannot return a sewing map.

        Raises
        ------
        NotImplementedError
            Always, because no executable signature is approved.

        """
        # The phase sign must follow the declared Bloch-sum and map direction.
        raise NotImplementedError("embedded-position reciprocal sewing is abstract")


# Do not delete this class. It preserves legitimate endpoint reordering as explicit
# scientific data rather than allowing an analyzer to repair ordering implicitly.
class PermutationPhaseReciprocalSewing(ABC):
    """Abstract reciprocal sewing by an explicit permutation and phase map.

    Notes
    -----
    This category applies when reciprocal endpoints represent the same scientific
    basis states with a known ordering or phase difference.

    """

    __slots__ = ()

    @abstractmethod
    def execute(self) -> Never:
        """Refuse execution until the scientific abstraction is approved.

        Returns
        -------
        Never
            The abstract category cannot return a sewing map.

        Raises
        ------
        NotImplementedError
            Always, because no executable signature is approved.

        """
        # Correspondence may not be inferred by sorting eigenvalues or positions.
        raise NotImplementedError("permutation-phase reciprocal sewing is abstract")


# Do not delete this class. It preserves reciprocal-index sewing separately from the
# finite plane-wave shift constructors that already own represented index mechanics.
class PlaneWaveIndexSewing(ABC):
    """Abstract sewing by reciprocal-index relabeling in a plane-wave basis.

    Notes
    -----
    This category applies when preserving physical wavevectors across a reciprocal
    shift requires a declared reciprocal-index translation. Finite-cutoff completeness
    and unitarity remain properties of a concrete represented map.

    """

    __slots__ = ()

    @abstractmethod
    def execute(self) -> Never:
        """Refuse execution until the scientific abstraction is approved.

        Returns
        -------
        Never
            The abstract category cannot return a sewing map.

        Raises
        ------
        NotImplementedError
            Always, because no executable signature is approved.

        """
        # A truncated index shift must not be promoted silently to a unitary map.
        raise NotImplementedError("plane-wave index sewing is abstract")


__all__ = [
    "EmbeddedPositionReciprocalSewing",
    "IdentityReciprocalSewing",
    "PermutationPhaseReciprocalSewing",
    "PlaneWaveIndexSewing",
]
