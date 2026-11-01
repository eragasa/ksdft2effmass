"""Requests for ordinary-lattice truncation of embedded rank-two fields."""

from __future__ import annotations

from dataclasses import dataclass

from ksdft2effmass.periodic1d.band_equivalence_locality.embedded_subspace.rank2.parent_scale.request import (  # noqa: E501
    Periodic1DRank2Request,
)
from ksdft2effmass.periodic1d.support_truncation import (
    Periodic1DSupportTruncationAnalysisRequest,
)
from ksdft2effmass.periodic1d.support_truncation.inventory import (
    Periodic1DSymmetricSupportInventory,
)


@dataclass(frozen=True, slots=True)
class Periodic1DRank2SupportTruncationAnalysisRequest(
    Periodic1DSupportTruncationAnalysisRequest
):
    """Bind one qualified parent to support cutoffs and a disjoint mesh."""

    template_request: Periodic1DRank2Request
    maximum_ranges: tuple[int, ...]
    evaluation_mesh_size: int

    @classmethod
    def every_integer_through(
        cls,
        *,
        template_request: Periodic1DRank2Request,
        maximum_range: int,
        evaluation_mesh_size: int,
    ) -> Periodic1DRank2SupportTruncationAnalysisRequest:
        """Construct the candidate cutoff inventory ``0, ..., maximum_range``."""
        if type(maximum_range) is not int:
            raise TypeError("maximum_range must be a built-in int")
        if maximum_range < 0:
            raise ValueError("maximum_range must be nonnegative")
        return cls(
            template_request=template_request,
            maximum_ranges=tuple(range(maximum_range + 1)),
            evaluation_mesh_size=evaluation_mesh_size,
        )

    def __post_init__(self) -> None:
        if type(self.template_request) is not Periodic1DRank2Request:
            raise TypeError("template_request must be Periodic1DRank2Request")
        if type(self.maximum_ranges) is not tuple or any(
            type(value) is not int for value in self.maximum_ranges
        ):
            raise TypeError("maximum_ranges must contain built-in ints")
        support_inventory = Periodic1DSymmetricSupportInventory.from_maximum_ranges(
            self.maximum_ranges
        )
        if (
            support_inventory.maximum_ranges[-1]
            >= self.template_request.reciprocal_mesh_size // 2
        ):
            raise ValueError("maximum_ranges must exclude the cyclic Nyquist index")
        if type(self.evaluation_mesh_size) is not int:
            raise TypeError("evaluation_mesh_size must be a built-in int")
        if (
            self.evaluation_mesh_size
            < 2 * self.template_request.reciprocal_mesh_size + 1
        ):
            raise ValueError(
                "evaluation_mesh_size must be at least 2*N+1 for disjoint evaluation"
            )

    @property
    def support_inventory(self) -> Periodic1DSymmetricSupportInventory:
        """Return the typed candidate retained-support inventory."""
        return Periodic1DSymmetricSupportInventory.from_maximum_ranges(
            self.maximum_ranges
        )

    @property
    def has_dense_integer_inventory(self) -> bool:
        """Return whether every integer cutoff through the cap is present."""
        return self.maximum_ranges == tuple(range(self.maximum_ranges[-1] + 1))


__all__ = ["Periodic1DRank2SupportTruncationAnalysisRequest"]
