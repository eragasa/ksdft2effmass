"""Periodic-2D rank-two direct-lifecycle records."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Self

from ksdft2effmass.band_equivalence_hopping_locality.definitions import (
    BandEquivalenceHoppingLocalityFamilyEnum,
)
from ksdft2effmass.band_equivalence_hopping_locality.lifecycle import (
    BandEquivalenceHoppingLocalityExecution,
    BandEquivalenceHoppingLocalityExecutionVerification,
    BandEquivalenceHoppingLocalityRendering,
)
from ksdft2effmass.serialization import SerializableValue

from .visualizations.data import (
    Periodic2DRank2BandEquivalenceHoppingLocalityVisualizationData,
)

_PERIODIC2D_IDENTITIES = {
    "periodic2d-rank2-orthogonal-band-equivalence-locality": (
        BandEquivalenceHoppingLocalityFamilyEnum.SQUARE.to_wire()
    ),
    "periodic2d-rank2-nonorthogonal-band-equivalence-locality": (
        BandEquivalenceHoppingLocalityFamilyEnum.GRAPHENE_INSPIRED.to_wire()
    ),
}


def _validate_periodic2d_identity(calculation_family: str, study_family: str) -> None:
    expected = _PERIODIC2D_IDENTITIES.get(calculation_family)
    if expected is None:
        raise ValueError(
            "calculation_family must identify a periodic-2D rank-two study"
        )
    if study_family != expected:
        raise ValueError("study_family must match the periodic-2D calculation family")


@dataclass(frozen=True, slots=True)
class Periodic2DRank2BandEquivalenceHoppingLocalityExecution(
    BandEquivalenceHoppingLocalityExecution,
):
    """Describe one completed unsealed periodic-2D rank-two execution."""

    def __post_init__(self) -> None:
        super().__post_init__()
        _validate_periodic2d_identity(self.calculation_family, self.study_family)


@dataclass(frozen=True, slots=True)
class Periodic2DRank2BandEquivalenceHoppingLocalityExecutionVerification(
    BandEquivalenceHoppingLocalityExecutionVerification,
):
    """Bind independent verification to one periodic-2D direct result."""

    def __post_init__(self) -> None:
        super().__post_init__()
        _validate_periodic2d_identity(self.calculation_family, self.study_family)
        if (
            type(self.visualization_data)
            is not Periodic2DRank2BandEquivalenceHoppingLocalityVisualizationData
        ):
            raise TypeError("visualization_data must retain periodic-2D ownership")

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        common = BandEquivalenceHoppingLocalityExecutionVerification._from_mapping(
            values
        )
        return cls(
            schema_version=common.schema_version,
            schema=common.schema,
            calculation_family=common.calculation_family,
            study_family=common.study_family,
            execution_id=common.execution_id,
            verification=common.verification,
            visualization_data=(
                Periodic2DRank2BandEquivalenceHoppingLocalityVisualizationData.from_dict(
                    common.visualization_data.to_dict()
                )
            ),
            comparison_count=common.comparison_count,
            result_sha256=common.result_sha256,
            script_sha256=common.script_sha256,
            claim_boundary=common.claim_boundary,
        )


@dataclass(frozen=True, slots=True)
class Periodic2DRank2BandEquivalenceHoppingLocalityRendering(
    BandEquivalenceHoppingLocalityRendering,
):
    """Authenticate one periodic-2D rank-two rendering inventory."""

    def __post_init__(self) -> None:
        super().__post_init__()
        _validate_periodic2d_identity(self.calculation_family, self.study_family)


__all__ = [
    "Periodic2DRank2BandEquivalenceHoppingLocalityExecution",
    "Periodic2DRank2BandEquivalenceHoppingLocalityExecutionVerification",
    "Periodic2DRank2BandEquivalenceHoppingLocalityRendering",
]
