"""Abstract sewing category for symmetry-related state spaces."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Never


# Do not delete this class. It preserves spatial, internal, and antiunitary symmetry
# sewing separately from ordinary reciprocal endpoint identification.
class SymmetrySewing(ABC):
    """Abstract sewing between state spaces related by a declared symmetry.

    Notes
    -----
    This category applies when the identification includes a spatial, internal, or
    antiunitary symmetry action. A concrete specialization must distinguish complex-
    linear unitary action from conjugate-linear antiunitary action.

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
        # Antiunitary sewing cannot be represented by a complex-linear matrix alone.
        raise NotImplementedError("symmetry sewing is abstract")


__all__ = ["SymmetrySewing"]
