"""Authenticated summary projection for the complete five-scale aggregate."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Self

from ksdft2effmass.serialization import SerializableValue
from ksdft2effmass.visualizations import BaseVisualizationData

from ..amplitude_refinement.analysis import (
    Periodic1DRank2AdaptiveAmplitudeConverged,
    Periodic1DRank2AdaptiveAmplitudeEvaluationsExhausted,
    Periodic1DRank2AdaptiveAmplitudeLevelsExhausted,
    Periodic1DRank2AdaptiveAmplitudeQualificationStopped,
)
from ..momentum_refinement.analysis import (
    Periodic1DRank2MomentumRefinementConverged,
    Periodic1DRank2MomentumRefinementQualificationStopped,
    Periodic1DRank2MomentumRefinementUnresolved,
)
from ..truncation.results import Periodic1DRank2TruncationCompleted
from .complete_five_scale import Periodic1DRank2CompleteFiveScaleCalculationRecord


@dataclass(frozen=True, slots=True)
class Periodic1DRank2CompleteFiveScaleVisualizationData(BaseVisualizationData):
    """Project authenticated family coverage and closed outcome dispositions."""

    source_sha256: str
    parent_hopping_scales: tuple[float, ...]
    momentum_dispositions: tuple[str, ...]
    adaptive_amplitude_disposition: str
    construction_mesh_sizes: tuple[int, ...]
    evaluation_mesh_sizes: tuple[int, ...]
    adjacent_decision_change_counts: tuple[int, ...]
    principal_truncation_point_counts: tuple[int, ...]
    principal_truncation_range_counts: tuple[int, ...]

    def __post_init__(self) -> None:
        if type(self.source_sha256) is not str:
            raise TypeError("source_sha256 must be a built-in string")
        if len(self.source_sha256) != 64 or any(
            character not in "0123456789abcdef" for character in self.source_sha256
        ):
            raise ValueError("source_sha256 must be a lowercase SHA-256 digest")
        if type(self.parent_hopping_scales) is not tuple:
            raise TypeError("parent_hopping_scales must be a tuple")
        if len(self.parent_hopping_scales) != 5:
            raise ValueError("parent_hopping_scales must contain five values")
        if any(type(value) is not float for value in self.parent_hopping_scales):
            raise TypeError("parent_hopping_scales must contain built-in floats")
        if type(self.momentum_dispositions) is not tuple:
            raise TypeError("momentum_dispositions must be a tuple")
        if len(self.momentum_dispositions) != 5:
            raise ValueError("momentum_dispositions must contain five values")
        if any(type(value) is not str for value in self.momentum_dispositions):
            raise TypeError("momentum_dispositions must contain built-in strings")
        if any(
            value not in {"qualification_stopped", "converged", "unresolved"}
            for value in self.momentum_dispositions
        ):
            raise ValueError("momentum_dispositions contain an unknown outcome")
        if type(self.adaptive_amplitude_disposition) is not str:
            raise TypeError("adaptive_amplitude_disposition must be a built-in string")
        if self.adaptive_amplitude_disposition not in {
            "qualification_stopped",
            "converged",
            "evaluations_exhausted",
            "levels_exhausted",
        }:
            raise ValueError("adaptive_amplitude_disposition is unknown")
        for name in (
            "construction_mesh_sizes",
            "evaluation_mesh_sizes",
            "adjacent_decision_change_counts",
            "principal_truncation_point_counts",
            "principal_truncation_range_counts",
        ):
            values = getattr(self, name)
            if type(values) is not tuple:
                raise TypeError(f"{name} must be a tuple")
            if not values:
                raise ValueError(f"{name} must be nonempty")
            if any(type(value) is not int for value in values):
                raise TypeError(f"{name} must contain built-in integers")
            if any(value < 0 for value in values):
                raise ValueError(f"{name} must be nonnegative")
        if len(self.construction_mesh_sizes) != len(self.evaluation_mesh_sizes):
            raise ValueError("construction and evaluation mesh inventories must align")
        if len(self.adjacent_decision_change_counts) != (
            len(self.construction_mesh_sizes) - 1
        ):
            raise ValueError("decision changes must align with adjacent mesh pairs")
        if (
            len(self.principal_truncation_point_counts) != 5
            or len(self.principal_truncation_range_counts) != 5
        ):
            raise ValueError("principal truncation counts must align with five scales")

    @classmethod
    def from_record(
        cls,
        record: Periodic1DRank2CompleteFiveScaleCalculationRecord,
        *,
        source_sha256: str,
    ) -> Self:
        """Project stored values without rerunning a scientific calculation."""
        if type(record) is not Periodic1DRank2CompleteFiveScaleCalculationRecord:
            raise TypeError("record must be a complete-five-scale calculation record")
        momentum_dispositions: list[str] = []
        for momentum_member in record.momentum_refinement_family.members:
            if (
                type(momentum_member)
                is Periodic1DRank2MomentumRefinementQualificationStopped
            ):
                momentum_dispositions.append("qualification_stopped")
            elif type(momentum_member) is Periodic1DRank2MomentumRefinementConverged:
                momentum_dispositions.append("converged")
            elif type(momentum_member) is Periodic1DRank2MomentumRefinementUnresolved:
                momentum_dispositions.append("unresolved")
            else:
                raise TypeError("momentum member is not one closed outcome")
        adaptive = record.adaptive_amplitude
        if type(adaptive) is Periodic1DRank2AdaptiveAmplitudeQualificationStopped:
            adaptive_disposition = "qualification_stopped"
        elif type(adaptive) is Periodic1DRank2AdaptiveAmplitudeConverged:
            adaptive_disposition = "converged"
        elif type(adaptive) is Periodic1DRank2AdaptiveAmplitudeEvaluationsExhausted:
            adaptive_disposition = "evaluations_exhausted"
        elif type(adaptive) is Periodic1DRank2AdaptiveAmplitudeLevelsExhausted:
            adaptive_disposition = "levels_exhausted"
        else:
            raise TypeError("adaptive amplitude is not one closed outcome")
        point_counts: list[int] = []
        range_counts: list[int] = []
        for truncation_member in record.principal_truncation_family.members:
            if type(truncation_member) is Periodic1DRank2TruncationCompleted:
                point_counts.append(len(truncation_member.points))
                range_counts.append(
                    sum(len(point.ranges) for point in truncation_member.points)
                )
            else:
                point_counts.append(0)
                range_counts.append(0)
        return cls(
            source_sha256=source_sha256,
            parent_hopping_scales=record.parent_family.request.parent_hopping_scales,
            momentum_dispositions=tuple(momentum_dispositions),
            adaptive_amplitude_disposition=adaptive_disposition,
            construction_mesh_sizes=(
                record.truncation_mesh_stability.construction_mesh_sizes
            ),
            evaluation_mesh_sizes=record.truncation_mesh_stability.evaluation_mesh_sizes,
            adjacent_decision_change_counts=(
                record.truncation_mesh_stability.adjacent_decision_change_counts
            ),
            principal_truncation_point_counts=tuple(point_counts),
            principal_truncation_range_counts=tuple(range_counts),
        )

    def _mapping(self) -> Mapping[str, SerializableValue]:
        return {
            "source_sha256": self.source_sha256,
            "parent_hopping_scales": self.parent_hopping_scales,
            "momentum_dispositions": self.momentum_dispositions,
            "adaptive_amplitude_disposition": self.adaptive_amplitude_disposition,
            "construction_mesh_sizes": self.construction_mesh_sizes,
            "evaluation_mesh_sizes": self.evaluation_mesh_sizes,
            "adjacent_decision_change_counts": self.adjacent_decision_change_counts,
            "principal_truncation_point_counts": (
                self.principal_truncation_point_counts
            ),
            "principal_truncation_range_counts": (
                self.principal_truncation_range_counts
            ),
        }

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        expected = {
            "source_sha256",
            "parent_hopping_scales",
            "momentum_dispositions",
            "adaptive_amplitude_disposition",
            "construction_mesh_sizes",
            "evaluation_mesh_sizes",
            "adjacent_decision_change_counts",
            "principal_truncation_point_counts",
            "principal_truncation_range_counts",
        }
        if set(values) != expected:
            raise ValueError("complete-five-scale visualization fields do not match")
        source_sha256 = values["source_sha256"]
        parent_hopping_scales = values["parent_hopping_scales"]
        momentum_dispositions = values["momentum_dispositions"]
        adaptive_amplitude_disposition = values["adaptive_amplitude_disposition"]
        if type(source_sha256) is not str:
            raise TypeError("source_sha256 must decode to a built-in string")
        if type(parent_hopping_scales) is not tuple or any(
            type(value) is not float for value in parent_hopping_scales
        ):
            raise TypeError("parent_hopping_scales must decode to built-in floats")
        if type(momentum_dispositions) is not tuple or any(
            type(value) is not str for value in momentum_dispositions
        ):
            raise TypeError("momentum_dispositions must decode to built-in strings")
        if type(adaptive_amplitude_disposition) is not str:
            raise TypeError(
                "adaptive_amplitude_disposition must decode to a built-in string"
            )
        integer_fields: dict[str, tuple[int, ...]] = {}
        for name in (
            "construction_mesh_sizes",
            "evaluation_mesh_sizes",
            "adjacent_decision_change_counts",
            "principal_truncation_point_counts",
            "principal_truncation_range_counts",
        ):
            value = values[name]
            if type(value) is not tuple or any(type(item) is not int for item in value):
                raise TypeError(f"{name} must decode to built-in integers")
            integer_fields[name] = value
        return cls(
            source_sha256=source_sha256,
            parent_hopping_scales=parent_hopping_scales,
            momentum_dispositions=momentum_dispositions,
            adaptive_amplitude_disposition=adaptive_amplitude_disposition,
            construction_mesh_sizes=integer_fields["construction_mesh_sizes"],
            evaluation_mesh_sizes=integer_fields["evaluation_mesh_sizes"],
            adjacent_decision_change_counts=integer_fields[
                "adjacent_decision_change_counts"
            ],
            principal_truncation_point_counts=integer_fields[
                "principal_truncation_point_counts"
            ],
            principal_truncation_range_counts=integer_fields[
                "principal_truncation_range_counts"
            ],
        )


__all__ = ["Periodic1DRank2CompleteFiveScaleVisualizationData"]
