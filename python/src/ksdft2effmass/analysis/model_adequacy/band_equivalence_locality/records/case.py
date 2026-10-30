"""Case-resolved and amplitude-resolution result values."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Self

from ksdft2effmass.serialization import BaseTypedRecord, SerializableValue

from ..results import (
    BandEquivalenceLocalityAmplitudeMidpointAnalysis,
    BandEquivalenceLocalityCaseAnalysis,
    BandEquivalenceLocalityFlatAmplitudeResolutionAnalysis,
)
from .point import PointDiagnostic


@dataclass(frozen=True, slots=True)
class FlatAmplitudeResolutionDiagnostic(BaseTypedRecord):
    """Retain analytic flat-parent midpoint interpolation defects."""

    amplitude_intervals: int
    amplitude_nodes: int
    maximum_operator_threshold_midpoint_interpolation_defect: float
    maximum_joint_threshold_midpoint_interpolation_defect: float
    passes_unit_scale_draft_tolerance: bool | None
    tolerance_inapplicable_reason: str

    @classmethod
    def from_analysis(
        cls, analysis: BandEquivalenceLocalityFlatAmplitudeResolutionAnalysis
    ) -> Self:
        """Project one plain scientific value into a retained record."""
        if type(analysis) is not BandEquivalenceLocalityFlatAmplitudeResolutionAnalysis:
            raise TypeError(
                "analysis must be "
                "BandEquivalenceLocalityFlatAmplitudeResolutionAnalysis"
            )
        return cls(
            amplitude_intervals=analysis.amplitude_intervals,
            amplitude_nodes=analysis.amplitude_nodes,
            maximum_operator_threshold_midpoint_interpolation_defect=analysis.maximum_operator_threshold_midpoint_interpolation_defect,
            maximum_joint_threshold_midpoint_interpolation_defect=analysis.maximum_joint_threshold_midpoint_interpolation_defect,
            passes_unit_scale_draft_tolerance=analysis.passes_unit_scale_draft_tolerance,
            tolerance_inapplicable_reason=analysis.tolerance_inapplicable_reason,
        )

    def _mapping(self) -> Mapping[str, SerializableValue]:
        return {
            "amplitude_intervals": self.amplitude_intervals,
            "amplitude_nodes": self.amplitude_nodes,
            "maximum_operator_threshold_midpoint_interpolation_defect": (
                self.maximum_operator_threshold_midpoint_interpolation_defect
            ),
            "maximum_joint_threshold_midpoint_interpolation_defect": (
                self.maximum_joint_threshold_midpoint_interpolation_defect
            ),
            "passes_unit_scale_draft_tolerance": self.passes_unit_scale_draft_tolerance,
            "tolerance_inapplicable_reason": self.tolerance_inapplicable_reason,
        }

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        required = {
            "amplitude_intervals",
            "amplitude_nodes",
            "maximum_operator_threshold_midpoint_interpolation_defect",
            "maximum_joint_threshold_midpoint_interpolation_defect",
            "passes_unit_scale_draft_tolerance",
            "tolerance_inapplicable_reason",
        }
        if set(values) != required:
            raise ValueError("FlatAmplitudeResolutionDiagnostic fields do not match")
        amplitude_intervals = values["amplitude_intervals"]
        amplitude_nodes = values["amplitude_nodes"]
        maximum_operator_threshold_midpoint_interpolation_defect = values[
            "maximum_operator_threshold_midpoint_interpolation_defect"
        ]
        maximum_joint_threshold_midpoint_interpolation_defect = values[
            "maximum_joint_threshold_midpoint_interpolation_defect"
        ]
        passes_unit_scale_draft_tolerance = values["passes_unit_scale_draft_tolerance"]
        tolerance_inapplicable_reason = values["tolerance_inapplicable_reason"]
        if (
            type(maximum_operator_threshold_midpoint_interpolation_defect) is not float
            or type(maximum_joint_threshold_midpoint_interpolation_defect) is not float
        ):
            raise TypeError("float fields must use exact built-in types")
        if type(amplitude_intervals) is not int or type(amplitude_nodes) is not int:
            raise TypeError("integer fields must use exact built-in types")
        if type(tolerance_inapplicable_reason) is not str:
            raise TypeError("string fields must use exact built-in types")
        if (
            passes_unit_scale_draft_tolerance is not None
            and type(passes_unit_scale_draft_tolerance) is not bool
        ):
            raise TypeError("optional Boolean fields have invalid types")
        return cls(
            amplitude_intervals=amplitude_intervals,
            amplitude_nodes=amplitude_nodes,
            maximum_operator_threshold_midpoint_interpolation_defect=maximum_operator_threshold_midpoint_interpolation_defect,
            maximum_joint_threshold_midpoint_interpolation_defect=maximum_joint_threshold_midpoint_interpolation_defect,
            passes_unit_scale_draft_tolerance=passes_unit_scale_draft_tolerance,
            tolerance_inapplicable_reason=tolerance_inapplicable_reason,
        )


@dataclass(frozen=True, slots=True)
class AmplitudeMidpointDiagnostic(BaseTypedRecord):
    """Retain direct midpoint-versus-linear-interpolation defects."""

    amplitude_nodes: int
    applicable: bool
    inapplicable_reason: str | None
    endpoint_minimum_threshold_over_sqrt_splitting: float | None
    maximum_correlation_midpoint_defect: float | None
    maximum_operator_threshold_midpoint_defect: float | None
    maximum_joint_threshold_midpoint_defect: float | None
    maximum_nonzero_hopping_weight_midpoint_defect: float | None
    maximum_hopping_block_power_midpoint_defect: float | None

    @classmethod
    def from_analysis(
        cls, analysis: BandEquivalenceLocalityAmplitudeMidpointAnalysis
    ) -> Self:
        """Project one plain scientific value into a retained record."""
        if type(analysis) is not BandEquivalenceLocalityAmplitudeMidpointAnalysis:
            raise TypeError(
                "analysis must be BandEquivalenceLocalityAmplitudeMidpointAnalysis"
            )
        return cls(
            amplitude_nodes=analysis.amplitude_nodes,
            applicable=analysis.applicable,
            inapplicable_reason=analysis.inapplicable_reason,
            endpoint_minimum_threshold_over_sqrt_splitting=analysis.endpoint_minimum_threshold_over_sqrt_splitting,
            maximum_correlation_midpoint_defect=analysis.maximum_correlation_midpoint_defect,
            maximum_operator_threshold_midpoint_defect=analysis.maximum_operator_threshold_midpoint_defect,
            maximum_joint_threshold_midpoint_defect=analysis.maximum_joint_threshold_midpoint_defect,
            maximum_nonzero_hopping_weight_midpoint_defect=analysis.maximum_nonzero_hopping_weight_midpoint_defect,
            maximum_hopping_block_power_midpoint_defect=analysis.maximum_hopping_block_power_midpoint_defect,
        )

    def _mapping(self) -> Mapping[str, SerializableValue]:
        return {
            "amplitude_nodes": self.amplitude_nodes,
            "applicable": self.applicable,
            "inapplicable_reason": self.inapplicable_reason,
            "endpoint_minimum_threshold_over_sqrt_splitting": (
                self.endpoint_minimum_threshold_over_sqrt_splitting
            ),
            "maximum_correlation_midpoint_defect": (
                self.maximum_correlation_midpoint_defect
            ),
            "maximum_operator_threshold_midpoint_defect": (
                self.maximum_operator_threshold_midpoint_defect
            ),
            "maximum_joint_threshold_midpoint_defect": (
                self.maximum_joint_threshold_midpoint_defect
            ),
            "maximum_nonzero_hopping_weight_midpoint_defect": (
                self.maximum_nonzero_hopping_weight_midpoint_defect
            ),
            "maximum_hopping_block_power_midpoint_defect": (
                self.maximum_hopping_block_power_midpoint_defect
            ),
        }

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        required = {
            "amplitude_nodes",
            "applicable",
            "inapplicable_reason",
            "endpoint_minimum_threshold_over_sqrt_splitting",
            "maximum_correlation_midpoint_defect",
            "maximum_operator_threshold_midpoint_defect",
            "maximum_joint_threshold_midpoint_defect",
            "maximum_nonzero_hopping_weight_midpoint_defect",
            "maximum_hopping_block_power_midpoint_defect",
        }
        if set(values) != required:
            raise ValueError("AmplitudeMidpointDiagnostic fields do not match")
        amplitude_nodes = values["amplitude_nodes"]
        applicable = values["applicable"]
        inapplicable_reason = values["inapplicable_reason"]
        endpoint_minimum_threshold_over_sqrt_splitting = values[
            "endpoint_minimum_threshold_over_sqrt_splitting"
        ]
        maximum_correlation_midpoint_defect = values[
            "maximum_correlation_midpoint_defect"
        ]
        maximum_operator_threshold_midpoint_defect = values[
            "maximum_operator_threshold_midpoint_defect"
        ]
        maximum_joint_threshold_midpoint_defect = values[
            "maximum_joint_threshold_midpoint_defect"
        ]
        maximum_nonzero_hopping_weight_midpoint_defect = values[
            "maximum_nonzero_hopping_weight_midpoint_defect"
        ]
        maximum_hopping_block_power_midpoint_defect = values[
            "maximum_hopping_block_power_midpoint_defect"
        ]
        if type(amplitude_nodes) is not int:
            raise TypeError("integer fields must use exact built-in types")
        if type(applicable) is not bool:
            raise TypeError("Boolean fields must use exact built-in types")
        if (
            (
                endpoint_minimum_threshold_over_sqrt_splitting is not None
                and type(endpoint_minimum_threshold_over_sqrt_splitting) is not float
            )
            or (
                maximum_correlation_midpoint_defect is not None
                and type(maximum_correlation_midpoint_defect) is not float
            )
            or (
                maximum_operator_threshold_midpoint_defect is not None
                and type(maximum_operator_threshold_midpoint_defect) is not float
            )
            or (
                maximum_joint_threshold_midpoint_defect is not None
                and type(maximum_joint_threshold_midpoint_defect) is not float
            )
            or (
                maximum_nonzero_hopping_weight_midpoint_defect is not None
                and type(maximum_nonzero_hopping_weight_midpoint_defect) is not float
            )
            or (
                maximum_hopping_block_power_midpoint_defect is not None
                and type(maximum_hopping_block_power_midpoint_defect) is not float
            )
        ):
            raise TypeError("optional float fields have invalid types")
        if inapplicable_reason is not None and type(inapplicable_reason) is not str:
            raise TypeError("optional string fields have invalid types")
        return cls(
            amplitude_nodes=amplitude_nodes,
            applicable=applicable,
            inapplicable_reason=inapplicable_reason,
            endpoint_minimum_threshold_over_sqrt_splitting=endpoint_minimum_threshold_over_sqrt_splitting,
            maximum_correlation_midpoint_defect=maximum_correlation_midpoint_defect,
            maximum_operator_threshold_midpoint_defect=maximum_operator_threshold_midpoint_defect,
            maximum_joint_threshold_midpoint_defect=maximum_joint_threshold_midpoint_defect,
            maximum_nonzero_hopping_weight_midpoint_defect=maximum_nonzero_hopping_weight_midpoint_defect,
            maximum_hopping_block_power_midpoint_defect=maximum_hopping_block_power_midpoint_defect,
        )


@dataclass(frozen=True, slots=True)
class CaseDiagnostic(BaseTypedRecord):
    """Retain all points for one independently interpreted geometry and parent."""

    name: str
    metric_covariance_defect: float
    construction_evaluation_minimum_separation: float
    amplitude_midpoint: AmplitudeMidpointDiagnostic
    flat_amplitude_resolution: tuple[FlatAmplitudeResolutionDiagnostic, ...]
    points: tuple[PointDiagnostic, ...]

    @classmethod
    def from_analysis(cls, analysis: BandEquivalenceLocalityCaseAnalysis) -> Self:
        """Project one plain scientific value into a retained record."""
        if type(analysis) is not BandEquivalenceLocalityCaseAnalysis:
            raise TypeError("analysis must be BandEquivalenceLocalityCaseAnalysis")
        return cls(
            name=analysis.name,
            metric_covariance_defect=analysis.metric_covariance_defect,
            construction_evaluation_minimum_separation=analysis.construction_evaluation_minimum_separation,
            amplitude_midpoint=AmplitudeMidpointDiagnostic.from_analysis(
                analysis.amplitude_midpoint
            ),
            flat_amplitude_resolution=tuple(
                FlatAmplitudeResolutionDiagnostic.from_analysis(value)
                for value in analysis.flat_amplitude_resolution
            ),
            points=tuple(
                PointDiagnostic.from_analysis(value) for value in analysis.points
            ),
        )

    def _mapping(self) -> Mapping[str, SerializableValue]:
        return {
            "name": self.name,
            "metric_covariance_defect": self.metric_covariance_defect,
            "construction_evaluation_minimum_separation": (
                self.construction_evaluation_minimum_separation
            ),
            "amplitude_midpoint": self.amplitude_midpoint,
            "flat_amplitude_resolution": self.flat_amplitude_resolution,
            "points": self.points,
        }

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        required = {
            "name",
            "metric_covariance_defect",
            "construction_evaluation_minimum_separation",
            "amplitude_midpoint",
            "flat_amplitude_resolution",
            "points",
        }
        if set(values) != required:
            raise ValueError("CaseDiagnostic fields do not match")
        name = values["name"]
        metric_covariance_defect = values["metric_covariance_defect"]
        construction_evaluation_minimum_separation = values[
            "construction_evaluation_minimum_separation"
        ]
        amplitude_midpoint_value = values["amplitude_midpoint"]
        flat_amplitude_resolution_values = values["flat_amplitude_resolution"]
        points_values = values["points"]
        if (
            type(metric_covariance_defect) is not float
            or type(construction_evaluation_minimum_separation) is not float
        ):
            raise TypeError("float fields must use exact built-in types")
        if type(name) is not str:
            raise TypeError("string fields must use exact built-in types")
        if not isinstance(amplitude_midpoint_value, Mapping):
            raise TypeError("amplitude_midpoint must decode to a mapping")
        if not isinstance(flat_amplitude_resolution_values, tuple) or any(
            not isinstance(item, Mapping) for item in flat_amplitude_resolution_values
        ):
            raise TypeError(
                "flat_amplitude_resolution must decode to a tuple of mappings"
            )
        if not isinstance(points_values, tuple) or any(
            not isinstance(item, Mapping) for item in points_values
        ):
            raise TypeError("points must decode to a tuple of mappings")
        return cls(
            name=name,
            metric_covariance_defect=metric_covariance_defect,
            construction_evaluation_minimum_separation=construction_evaluation_minimum_separation,
            amplitude_midpoint=AmplitudeMidpointDiagnostic.from_dict(
                amplitude_midpoint_value
            ),
            flat_amplitude_resolution=tuple(
                FlatAmplitudeResolutionDiagnostic.from_dict(item)
                for item in flat_amplitude_resolution_values
            ),
            points=tuple(PointDiagnostic.from_dict(item) for item in points_values),
        )
