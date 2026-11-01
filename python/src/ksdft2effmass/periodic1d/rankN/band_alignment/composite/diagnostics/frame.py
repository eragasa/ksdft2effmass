"""Frame-field recovery diagnostics."""

from __future__ import annotations

import math
from collections.abc import Mapping
from dataclasses import dataclass
from typing import Self

from ksdft2effmass.serialization import BaseTypedRecord, SerializableValue

from .._record_admission import _decoded_float, _finite_nonnegative


@dataclass(frozen=True, slots=True)
class Periodic1DRankNFrameErrorResult(BaseTypedRecord):
    """Retain raw and rank-normalized Frobenius errors for one frame field."""

    rank: int
    frobenius_maximum: float
    frobenius_rms: float
    normalized_frobenius_maximum: float
    normalized_frobenius_rms: float

    def __post_init__(self) -> None:
        if type(self.rank) is not int or self.rank <= 0:
            raise ValueError("rank must be a positive built-in integer")
        for value, name in (
            (self.frobenius_maximum, "frobenius_maximum"),
            (self.frobenius_rms, "frobenius_rms"),
            (self.normalized_frobenius_maximum, "normalized_frobenius_maximum"),
            (self.normalized_frobenius_rms, "normalized_frobenius_rms"),
        ):
            _finite_nonnegative(value, name)
        scale = math.sqrt(self.rank)
        if not math.isclose(
            self.frobenius_maximum / scale,
            self.normalized_frobenius_maximum,
            rel_tol=2.0e-15,
            abs_tol=0.0,
        ) or not math.isclose(
            self.frobenius_rms / scale,
            self.normalized_frobenius_rms,
            rel_tol=2.0e-15,
            abs_tol=0.0,
        ):
            raise ValueError("normalized frame errors disagree with rank normalization")

    def _mapping(self) -> Mapping[str, SerializableValue]:
        return {
            "rank": self.rank,
            "frobenius_maximum": self.frobenius_maximum,
            "frobenius_rms": self.frobenius_rms,
            "normalized_frobenius_maximum": self.normalized_frobenius_maximum,
            "normalized_frobenius_rms": self.normalized_frobenius_rms,
        }

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        if set(values) != {
            "rank",
            "frobenius_maximum",
            "frobenius_rms",
            "normalized_frobenius_maximum",
            "normalized_frobenius_rms",
        }:
            raise ValueError("frame error fields do not match")
        rank = values["rank"]
        if type(rank) is not int:
            raise TypeError("rank must decode to a built-in integer")
        return cls(
            rank=rank,
            frobenius_maximum=_decoded_float(
                values["frobenius_maximum"], "frobenius_maximum"
            ),
            frobenius_rms=_decoded_float(values["frobenius_rms"], "frobenius_rms"),
            normalized_frobenius_maximum=_decoded_float(
                values["normalized_frobenius_maximum"],
                "normalized_frobenius_maximum",
            ),
            normalized_frobenius_rms=_decoded_float(
                values["normalized_frobenius_rms"], "normalized_frobenius_rms"
            ),
        )
