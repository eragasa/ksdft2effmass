"""Rank-one alignment applicability vocabulary."""

from __future__ import annotations

from ksdft2effmass.serialization import StringWireEnum


class Periodic1DRank1AlignmentApplicability(StringWireEnum):
    """State why nontrivial internal alignment is absent at rank one."""

    OPERATOR_TRIVIAL = "operator-trivial"


__all__ = ["Periodic1DRank1AlignmentApplicability"]
