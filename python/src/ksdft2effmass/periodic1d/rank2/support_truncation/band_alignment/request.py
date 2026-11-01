"""Support-truncation requests for the rank-two band-alignment study."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from projectkoios.physkit.units import Unitless

from ksdft2effmass.analysis.periodic_bands import BandSpectrumSamples1D
from ksdft2effmass.periodic1d.rank2.band_alignment.configuration import (
    Periodic1DCompositeBandAlignmentConfiguration,
)
from ksdft2effmass.periodic1d.rank2.hopping_locality.result import (
    Periodic1DRank2HoppingLocalityAnalysis,
)
from ksdft2effmass.periodic1d.support_truncation.base import (
    Periodic1DSupportTruncationAnalysisRequest,
)
from ksdft2effmass.solidstate.hopping_transforms import ReciprocalOperatorSamples1D


@dataclass(frozen=True, slots=True, eq=False)
class Periodic1DRank2SupportTruncationAnalysisRequest(
    Periodic1DSupportTruncationAnalysisRequest
):
    """Bind one channel's locality evidence to support-removal evaluation fields."""

    configuration: Periodic1DCompositeBandAlignmentConfiguration
    hopping_locality_analysis: Periodic1DRank2HoppingLocalityAnalysis
    construction_target: BandSpectrumSamples1D
    complete_evaluation: ReciprocalOperatorSamples1D
    direct_evaluation: ReciprocalOperatorSamples1D

    def __post_init__(self) -> None:
        if (
            type(self.configuration)
            is not Periodic1DCompositeBandAlignmentConfiguration
        ):
            raise TypeError(
                "configuration must be Periodic1DCompositeBandAlignmentConfiguration"
            )
        if (
            type(self.hopping_locality_analysis)
            is not Periodic1DRank2HoppingLocalityAnalysis
        ):
            raise TypeError(
                "hopping_locality_analysis must be the exact rank-two analysis"
            )
        if (
            self.hopping_locality_analysis.request.configuration
            is not self.configuration
        ):
            raise ValueError(
                "hopping locality must derive from the bound configuration"
            )
        if (
            tuple(
                item.diagnostic_range for item in self.hopping_locality_analysis.tails
            )
            != self.configuration.support_range_inventory.ranges
        ):
            raise ValueError(
                "hopping diagnostics must cover every candidate support range"
            )
        if type(self.construction_target) is not BandSpectrumSamples1D:
            raise TypeError("construction_target must be BandSpectrumSamples1D")
        if type(self.complete_evaluation) is not ReciprocalOperatorSamples1D:
            raise TypeError("complete_evaluation must be reciprocal-operator samples")
        if type(self.direct_evaluation) is not ReciprocalOperatorSamples1D:
            raise TypeError("direct_evaluation must be reciprocal-operator samples")
        expected_construction = np.asarray(
            self.configuration.construction_reduced_momenta(),
            dtype=np.float64,
        )
        if not np.array_equal(
            self.construction_target.coordinates.magnitude,
            expected_construction,
        ):
            raise ValueError("construction target must match the construction mesh")
        if self.construction_target.band_count != self.configuration.retained_rank:
            raise ValueError("construction target must contain the retained spectrum")
        if (
            not isinstance(self.construction_target.reciprocal_period.unit, Unitless)
            or self.construction_target.reciprocal_period.magnitude != 1.0
        ):
            raise ValueError(
                "construction target must use the unitless reciprocal period"
            )
        expected_evaluation = np.asarray(
            self.configuration.evaluation_reduced_momenta(),
            dtype=np.float64,
        )
        for samples, name in (
            (self.complete_evaluation, "complete_evaluation"),
            (self.direct_evaluation, "direct_evaluation"),
        ):
            if not np.array_equal(
                samples.coordinates.magnitude,
                expected_evaluation,
            ):
                raise ValueError(f"{name} must match the evaluation mesh")
            if (
                not isinstance(samples.reciprocal_period.unit, Unitless)
                or samples.reciprocal_period.magnitude != 1.0
            ):
                raise ValueError(
                    "evaluation fields must use the unitless reciprocal period"
                )
            expected_shape = (
                self.configuration.retained_rank,
                self.configuration.retained_rank,
            )
            if samples.matrices[0].magnitude.shape != expected_shape:
                raise ValueError("evaluation operators must act on retained states")
        if not np.array_equal(
            self.complete_evaluation.coordinates.magnitude,
            self.direct_evaluation.coordinates.magnitude,
        ):
            raise ValueError("complete and direct evaluation coordinates must agree")
        if (
            self.complete_evaluation.reciprocal_period
            != self.direct_evaluation.reciprocal_period
        ):
            raise ValueError("complete and direct reciprocal periods must agree")

    @property
    def channel(self) -> str:
        """Return the frozen locality channel bound to this request."""
        return self.hopping_locality_analysis.request.channel


__all__ = ["Periodic1DRank2SupportTruncationAnalysisRequest"]
