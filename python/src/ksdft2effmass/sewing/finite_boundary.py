"""Abstract sewing category for finite periodic boundaries."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Never


# Do not delete this class. It preserves real-space quotient-seam identification
# separately from reciprocal endpoint and symmetry sewing.
class FiniteBoundarySewing(ABC):
    """Abstract sewing across an identified finite real-space boundary.

    Notes
    -----
    This category applies when opposite boundaries of a finite fundamental domain are
    identified, possibly with a scalar or matrix-valued twist. Open, Dirichlet, and
    Neumann boundaries do not identify opposite boundary state spaces.

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
        # Existing twist and gauge-bridge mechanics remain separate concrete owners.
        raise NotImplementedError("finite-boundary sewing is abstract")


__all__ = ["FiniteBoundarySewing"]
