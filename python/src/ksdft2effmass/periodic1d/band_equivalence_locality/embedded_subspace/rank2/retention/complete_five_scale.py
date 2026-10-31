"""Canonical aggregate for one complete five-scale rank-two calculation."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Self

from ksdft2effmass.serialization import BaseTypedRecord, SerializableValue

from ..amplitude_refinement.analysis import (
    Periodic1DRank2AdaptiveAmplitudeAnalysis,
    Periodic1DRank2AdaptiveAmplitudeConverged,
    Periodic1DRank2AdaptiveAmplitudeEvaluationsExhausted,
    Periodic1DRank2AdaptiveAmplitudeLevelsExhausted,
    Periodic1DRank2AdaptiveAmplitudeQualificationStopped,
)
from ..momentum_refinement.family import (
    Periodic1DRank2MomentumRefinementFamilyAnalysis,
)
from ..parent_family.analysis import Periodic1DRank2ParentFamilyAnalysis
from ..truncation.family import Periodic1DRank2TruncationFamilyAnalysis
from ..truncation.mesh_stability import (
    Periodic1DRank2TruncationMeshStabilityAssessment,
)
from .records import (
    Periodic1DRank2AdaptiveAmplitudeAnalysisRecord,
    Periodic1DRank2MomentumRefinementFamilyAnalysisRecord,
    Periodic1DRank2ParentFamilyAnalysisRecord,
    Periodic1DRank2TruncationFamilyAnalysisRecord,
)


@dataclass(frozen=True, slots=True)
class Periodic1DRank2CompleteFiveScaleCalculationRecord(BaseTypedRecord):
    """Compose the complete parent, momentum, amplitude, and truncation scope.

    This value retains a five-member parent-scale family. It does not assert evidence
    sealing, scientific validation, or convergence beyond its closed scientific
    outcomes.
    """

    parent_family: Periodic1DRank2ParentFamilyAnalysis
    momentum_refinement_family: Periodic1DRank2MomentumRefinementFamilyAnalysis
    adaptive_amplitude: Periodic1DRank2AdaptiveAmplitudeAnalysis
    truncation_mesh_stability: Periodic1DRank2TruncationMeshStabilityAssessment

    def __post_init__(self) -> None:
        if type(self.parent_family) is not Periodic1DRank2ParentFamilyAnalysis:
            raise TypeError("parent_family must be a parent-family analysis")
        scales = self.parent_family.request.parent_hopping_scales
        if len(scales) != 5:
            raise ValueError("parent_family must contain exactly five parent scales")
        if type(self.momentum_refinement_family) is not (
            Periodic1DRank2MomentumRefinementFamilyAnalysis
        ):
            raise TypeError(
                "momentum_refinement_family must be a refinement-family analysis"
            )
        if type(self.adaptive_amplitude) not in (
            Periodic1DRank2AdaptiveAmplitudeQualificationStopped,
            Periodic1DRank2AdaptiveAmplitudeConverged,
            Periodic1DRank2AdaptiveAmplitudeEvaluationsExhausted,
            Periodic1DRank2AdaptiveAmplitudeLevelsExhausted,
        ):
            raise TypeError("adaptive_amplitude must be one closed adaptive outcome")
        if type(self.truncation_mesh_stability) is not (
            Periodic1DRank2TruncationMeshStabilityAssessment
        ):
            raise TypeError(
                "truncation_mesh_stability must be a mesh-stability assessment"
            )
        if (
            self.momentum_refinement_family.request.parent_family_request.parent_hopping_scales
            != scales
        ):
            raise ValueError(
                "momentum refinement must cover the parent-scale inventory"
            )
        truncation_scales = self.truncation_mesh_stability.refinement_families[
            0
        ].request.parent_family_request.parent_hopping_scales
        if truncation_scales != scales:
            raise ValueError("truncation refinement must cover every parent scale")
        if (
            self.adaptive_amplitude.request.template_request.parent_hopping_scale
            != scales[-1]
        ):
            raise ValueError("adaptive amplitude must retain the final parent scale")
        parent_mesh_size = (
            self.parent_family.request.template_request.reciprocal_mesh_size
        )
        if (
            self.truncation_mesh_stability.construction_mesh_sizes.count(
                parent_mesh_size
            )
            != 1
        ):
            raise ValueError(
                "truncation refinement must contain one principal construction mesh"
            )

    @property
    def principal_truncation_family(
        self,
    ) -> Periodic1DRank2TruncationFamilyAnalysis:
        """Return the truncation family on the parent-family construction mesh."""
        parent_mesh_size = (
            self.parent_family.request.template_request.reciprocal_mesh_size
        )
        return next(
            family
            for family in self.truncation_mesh_stability.refinement_families
            if (
                family.request.parent_family_request.template_request.reciprocal_mesh_size
                == parent_mesh_size
            )
        )

    def _mapping(self) -> Mapping[str, SerializableValue]:
        return {
            "parent_family": Periodic1DRank2ParentFamilyAnalysisRecord(
                self.parent_family
            ).to_dict(),
            "momentum_refinement_family": (
                Periodic1DRank2MomentumRefinementFamilyAnalysisRecord(
                    self.momentum_refinement_family
                ).to_dict()
            ),
            "adaptive_amplitude": Periodic1DRank2AdaptiveAmplitudeAnalysisRecord(
                self.adaptive_amplitude
            ).to_dict(),
            "truncation_mesh_stability": tuple(
                Periodic1DRank2TruncationFamilyAnalysisRecord(family).to_dict()
                for family in self.truncation_mesh_stability.refinement_families
            ),
        }

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        if set(values) != {
            "parent_family",
            "momentum_refinement_family",
            "adaptive_amplitude",
            "truncation_mesh_stability",
        }:
            raise ValueError("complete-five-scale calculation fields do not match")
        parent_family = values["parent_family"]
        momentum_family = values["momentum_refinement_family"]
        adaptive_amplitude = values["adaptive_amplitude"]
        truncation_families = values["truncation_mesh_stability"]
        if not isinstance(parent_family, Mapping) or any(
            type(key) is not str for key in parent_family
        ):
            raise TypeError("parent_family must decode to a string-keyed mapping")
        if not isinstance(momentum_family, Mapping) or any(
            type(key) is not str for key in momentum_family
        ):
            raise TypeError(
                "momentum_refinement_family must decode to a string-keyed mapping"
            )
        if not isinstance(adaptive_amplitude, Mapping) or any(
            type(key) is not str for key in adaptive_amplitude
        ):
            raise TypeError("adaptive_amplitude must decode to a string-keyed mapping")
        if type(truncation_families) is not tuple:
            raise TypeError("truncation_mesh_stability must decode to a tuple")
        if any(
            not isinstance(value, Mapping) or any(type(key) is not str for key in value)
            for value in truncation_families
        ):
            raise TypeError("truncation_mesh_stability members must decode to mappings")
        return cls(
            parent_family=Periodic1DRank2ParentFamilyAnalysisRecord.from_dict(
                parent_family
            ).analysis,
            momentum_refinement_family=(
                Periodic1DRank2MomentumRefinementFamilyAnalysisRecord.from_dict(
                    momentum_family
                ).analysis
            ),
            adaptive_amplitude=(
                Periodic1DRank2AdaptiveAmplitudeAnalysisRecord.from_dict(
                    adaptive_amplitude
                ).analysis
            ),
            truncation_mesh_stability=(
                Periodic1DRank2TruncationMeshStabilityAssessment(
                    tuple(
                        Periodic1DRank2TruncationFamilyAnalysisRecord.from_dict(
                            family
                        ).analysis
                        for family in truncation_families
                    )
                )
            ),
        )


__all__ = ["Periodic1DRank2CompleteFiveScaleCalculationRecord"]
