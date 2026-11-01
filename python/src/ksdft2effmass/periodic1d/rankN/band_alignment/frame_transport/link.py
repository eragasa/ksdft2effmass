"""Typed link evidence for rank-N closed-loop frame transport."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Self

from projectkoios.physkit.solidstate.electronic.frame_transport import (
    ClosedLoopPolarFrameTransportLinkDiagnostic,
    ClosedLoopPolarFrameTransportLinkKind,
    ClosedLoopPolarFrameTransportLinkStatus,
)

from ksdft2effmass.serialization import BaseTypedRecord, SerializableValue

from ._decoding import _Periodic1DRankNTransportRecordDecoder


@dataclass(frozen=True, slots=True)
class Periodic1DRankNAlignmentTransportLinkResult(BaseTypedRecord):
    """Record numerical-rank evidence for one neighbor or closure link.

    Parameters
    ----------
    index
        Zero-based built-in integer route-link index.
    kind, status
        Exact enums distinguishing neighbor from closure links and qualified,
        rank-deficient, or unattempted evaluation.
    singular_values
        Ordered tuple of finite nonnegative unitless binary64 singular values, or
        ``None`` when the link was not attempted.
    applied_rank_cutoff
        Finite nonnegative unitless binary64 threshold, or ``None`` when unattempted.
    rank_margin
        Finite unitless binary64 value ``sigma_min - cutoff``; it may be negative for a
        deficient link and is ``None`` when unattempted.
    numerical_rank
        Built-in integer matrix rank, or ``None`` when unattempted.
    maximum_absolute_entry_unitarity_defect
        Finite nonnegative unitless binary64 backend-validation residual, or ``None``
        when no polar factor was produced.

    Notes
    -----
    Python integers do not overflow. Binary64 overflow to infinity and all nonfinite
    values are rejected by the upstream diagnostic contract.
    """

    index: int
    kind: ClosedLoopPolarFrameTransportLinkKind
    status: ClosedLoopPolarFrameTransportLinkStatus
    singular_values: tuple[float, ...] | None
    applied_rank_cutoff: float | None
    rank_margin: float | None
    numerical_rank: int | None
    maximum_absolute_entry_unitarity_defect: float | None

    def __post_init__(self) -> None:
        """Delegate exact diagnostic invariants to the numerical owner contract."""
        ClosedLoopPolarFrameTransportLinkDiagnostic(
            index=self.index,
            kind=self.kind,
            status=self.status,
            singular_values=self.singular_values,
            applied_rank_cutoff=self.applied_rank_cutoff,
            rank_margin=self.rank_margin,
            numerical_rank=self.numerical_rank,
            maximum_absolute_entry_unitarity_defect=(
                self.maximum_absolute_entry_unitarity_defect
            ),
        )

    @classmethod
    def from_owner_diagnostic(
        cls,
        diagnostic: ClosedLoopPolarFrameTransportLinkDiagnostic,
    ) -> Self:
        """Copy one validated immutable owner diagnostic onto the KSD wire."""
        if type(diagnostic) is not ClosedLoopPolarFrameTransportLinkDiagnostic:
            raise TypeError(
                "diagnostic must be ClosedLoopPolarFrameTransportLinkDiagnostic"
            )
        return cls(
            index=diagnostic.index,
            kind=diagnostic.kind,
            status=diagnostic.status,
            singular_values=diagnostic.singular_values,
            applied_rank_cutoff=diagnostic.applied_rank_cutoff,
            rank_margin=diagnostic.rank_margin,
            numerical_rank=diagnostic.numerical_rank,
            maximum_absolute_entry_unitarity_defect=(
                diagnostic.maximum_absolute_entry_unitarity_defect
            ),
        )

    def _mapping(self) -> Mapping[str, SerializableValue]:
        return {
            "index": self.index,
            "kind": self.kind.value,
            "status": self.status.value,
            "singular_values": self.singular_values,
            "applied_rank_cutoff": self.applied_rank_cutoff,
            "rank_margin": self.rank_margin,
            "numerical_rank": self.numerical_rank,
            "maximum_absolute_entry_unitarity_defect": (
                self.maximum_absolute_entry_unitarity_defect
            ),
        }

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        required = {
            "index",
            "kind",
            "status",
            "singular_values",
            "applied_rank_cutoff",
            "rank_margin",
            "numerical_rank",
            "maximum_absolute_entry_unitarity_defect",
        }
        if set(values) != required:
            raise ValueError("transport-link result fields do not match")
        decoder = _Periodic1DRankNTransportRecordDecoder(values)
        index = values["index"]
        kind = values["kind"]
        status = values["status"]
        singular_values = decoder.optional_float_tuple("singular_values")
        applied_rank_cutoff = decoder.optional_float("applied_rank_cutoff")
        rank_margin = decoder.optional_float("rank_margin")
        numerical_rank = values["numerical_rank"]
        unitarity_defect = decoder.optional_float(
            "maximum_absolute_entry_unitarity_defect"
        )
        if type(index) is not int:
            raise TypeError("index must decode to a built-in integer")
        if type(kind) is not str or type(status) is not str:
            raise TypeError("link kind and status must decode to strings")
        if numerical_rank is not None and type(numerical_rank) is not int:
            raise TypeError("numerical_rank must decode to an integer or None")
        return cls(
            index=index,
            kind=ClosedLoopPolarFrameTransportLinkKind(kind),
            status=ClosedLoopPolarFrameTransportLinkStatus(status),
            singular_values=singular_values,
            applied_rank_cutoff=applied_rank_cutoff,
            rank_margin=rank_margin,
            numerical_rank=numerical_rank,
            maximum_absolute_entry_unitarity_defect=unitarity_defect,
        )


__all__ = ["Periodic1DRankNAlignmentTransportLinkResult"]
