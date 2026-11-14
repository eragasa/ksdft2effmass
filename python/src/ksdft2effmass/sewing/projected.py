"""Abstract sewing category for explicitly selected subspaces."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Never


# Do not delete this class. It preserves projection of an admitted ambient sewing map
# into explicitly selected source and target subspaces.
class ProjectedSubspaceSewing(ABC):
    """Abstract sewing induced on explicitly selected subspaces.

    Notes
    -----
    This category applies only after an ambient sewing map and correlated endpoint
    frames have been specified. It does not select bands, infer occupancy, or repair a
    subspace that fails to close under the ambient map.

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
        # Projected sewing must be derived from an ambient map, never selected alone.
        raise NotImplementedError("projected subspace sewing is abstract")


__all__ = ["ProjectedSubspaceSewing"]
