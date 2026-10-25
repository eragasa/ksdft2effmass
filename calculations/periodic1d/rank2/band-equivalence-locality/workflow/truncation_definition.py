"""Definitions for finite-range consequences of the non-flat realization."""

from __future__ import annotations

from dataclasses import dataclass

from .nonflat_definition import SmoothFourStateDefinition

SMOOTH_FOUR_STATE_TRUNCATION_METHOD_ID = (
    "nonflat-four-state-ordinary-lattice-truncation.v1"
)


@dataclass(frozen=True, slots=True)
class SmoothFourStateTruncationDefinition:
    """Declare one sampled finite-range comparison.

    ``maximum_ranges`` contains ordinary-lattice cutoffs.  The even-mesh cyclic
    Nyquist representative is removed before these cutoffs are applied and is reported
    separately.  Evaluation coordinates are a deterministically shifted mesh disjoint
    from the construction mesh.
    """

    model: SmoothFourStateDefinition
    maximum_ranges: tuple[int, ...]
    evaluation_mesh_size: int

    def __post_init__(self) -> None:
        """Reject cyclic, undersampled, or ambiguous cutoff inventories."""
        if type(self.model) is not SmoothFourStateDefinition:
            raise TypeError("model must be SmoothFourStateDefinition")
        if type(self.maximum_ranges) is not tuple or not self.maximum_ranges:
            raise TypeError("maximum_ranges must be a nonempty tuple")
        if any(type(value) is not int for value in self.maximum_ranges):
            raise TypeError("maximum_ranges must contain built-in ints")
        if tuple(sorted(set(self.maximum_ranges))) != self.maximum_ranges:
            raise ValueError("maximum_ranges must be unique and strictly increasing")
        if self.maximum_ranges[0] < 0:
            raise ValueError("maximum_ranges must be nonnegative")
        if self.maximum_ranges[-1] >= self.model.reciprocal_mesh_size // 2:
            raise ValueError("maximum_ranges must exclude the cyclic Nyquist index")
        if type(self.evaluation_mesh_size) is not int:
            raise TypeError("evaluation_mesh_size must be a built-in int")
        if self.evaluation_mesh_size < 2 * self.model.reciprocal_mesh_size + 1:
            raise ValueError(
                "evaluation_mesh_size must be at least 2*N+1 for disjoint evaluation"
            )
