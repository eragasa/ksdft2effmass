"""Canonical authenticated projections for embedded rank-two rendering."""

from __future__ import annotations

import hashlib
import math
from collections.abc import Mapping
from dataclasses import dataclass
from typing import ClassVar, Self

from ksdft2effmass.serialization import SerializableValue
from ksdft2effmass.visualizations import BaseVisualizationData

from ..amplitude_refinement.analysis import (
    Periodic1DRank2AdaptiveAmplitudeConverged,
    Periodic1DRank2AdaptiveAmplitudeEvaluationsExhausted,
    Periodic1DRank2AdaptiveAmplitudeLevelsExhausted,
    Periodic1DRank2AmplitudeRefinementLevel,
    Periodic1DRank2AmplitudeValidation,
)
from ..parent_family.analysis import (
    Periodic1DRank2ParentFamilyAnalysis,
)
from ..parent_scale.results import (
    Periodic1DRank2Analysis,
    Periodic1DRank2QualifiedParent,
)
from .records import (
    Periodic1DRank2CalculationRecord,
    Periodic1DRank2ParentFamilyAnalysisRecord,
)


def _digest(value: str) -> None:
    if (
        type(value) is not str
        or len(value) != 64
        or any(character not in "0123456789abcdef" for character in value)
    ):
        raise ValueError("source_sha256 must be a lowercase SHA-256 digest")


def _float_tuple(
    values: Mapping[str, SerializableValue], name: str
) -> tuple[float, ...]:
    value = values[name]
    if type(value) is not tuple or any(type(item) is not float for item in value):
        raise TypeError(f"{name} must decode to a tuple of built-in floats")
    return value


def _int_tuple(values: Mapping[str, SerializableValue], name: str) -> tuple[int, ...]:
    value = values[name]
    if type(value) is not tuple or any(type(item) is not int for item in value):
        raise TypeError(f"{name} must decode to a tuple of built-in integers")
    return value


def _bool_tuple(values: Mapping[str, SerializableValue], name: str) -> tuple[bool, ...]:
    value = values[name]
    if type(value) is not tuple or any(type(item) is not bool for item in value):
        raise TypeError(f"{name} must decode to a tuple of built-in booleans")
    return value


def _float_rows(
    values: Mapping[str, SerializableValue], name: str
) -> tuple[tuple[float, ...], ...]:
    value = values[name]
    if type(value) is not tuple:
        raise TypeError(f"{name} must decode to a tuple")
    rows: list[tuple[float, ...]] = []
    for row in value:
        if type(row) is not tuple or any(type(item) is not float for item in row):
            raise TypeError(f"{name} must contain tuples of built-in floats")
        rows.append(row)
    return tuple(rows)


def _finite_tuple(values: tuple[float, ...], name: str) -> None:
    if type(values) is not tuple or not values:
        raise TypeError(f"{name} must be a nonempty tuple")
    if any(type(value) is not float or not math.isfinite(value) for value in values):
        raise TypeError(f"{name} must contain finite built-in floats")


def _nonnegative_tuple(values: tuple[float, ...], name: str) -> None:
    _finite_tuple(values, name)
    if any(value < 0.0 for value in values):
        raise ValueError(f"{name} must be nonnegative")


def _rows(
    values: tuple[tuple[float, ...], ...],
    *,
    row_count: int,
    width: int,
    name: str,
    signed: bool = False,
) -> None:
    if type(values) is not tuple or len(values) != row_count:
        raise ValueError(f"{name} must match its row inventory")
    for row in values:
        if type(row) is not tuple or len(row) != width:
            raise ValueError(f"{name} row width does not match its inventory")
        _finite_tuple(row, name)
        if not signed and any(value < 0.0 for value in row):
            raise ValueError(f"{name} must be nonnegative")


@dataclass(frozen=True, slots=True)
class Periodic1DRank2VisualizationData(BaseVisualizationData):
    """Project one qualified embedded analysis for authenticated rendering."""

    source_sha256: str
    amplitudes: tuple[float, ...]
    correlations: tuple[float, ...]
    operator_thresholds: tuple[float, ...]
    joint_thresholds: tuple[float, ...]
    reference_nonzero_weights: tuple[float, ...]
    comparison_nonzero_weights: tuple[float, ...]
    band_defects: tuple[float, ...]
    reconstruction_defects: tuple[float, ...]
    reference_parseval_defects: tuple[float, ...]
    comparison_parseval_defects: tuple[float, ...]
    hopping_displacements: tuple[int, ...]
    reference_hopping_powers: tuple[tuple[float, ...], ...]
    comparison_hopping_powers: tuple[tuple[float, ...], ...]

    def __post_init__(self) -> None:
        _digest(self.source_sha256)
        if not self.amplitudes:
            if any(
                getattr(self, name)
                for name in (
                    "correlations",
                    "operator_thresholds",
                    "joint_thresholds",
                    "reference_nonzero_weights",
                    "comparison_nonzero_weights",
                    "band_defects",
                    "reconstruction_defects",
                    "reference_parseval_defects",
                    "comparison_parseval_defects",
                    "hopping_displacements",
                    "reference_hopping_powers",
                    "comparison_hopping_powers",
                )
            ):
                raise ValueError("stopped projection must not contain point channels")
            return
        _finite_tuple(self.amplitudes, "amplitudes")
        count = len(self.amplitudes)
        if (
            any(
                type(value) is not float or not -1.0 <= value <= 1.0
                for value in self.correlations
            )
            or len(self.correlations) != count
        ):
            raise ValueError("correlations must match amplitudes and lie in [-1, 1]")
        for name in (
            "operator_thresholds",
            "joint_thresholds",
            "reference_nonzero_weights",
            "comparison_nonzero_weights",
            "band_defects",
            "reconstruction_defects",
            "reference_parseval_defects",
            "comparison_parseval_defects",
        ):
            values = getattr(self, name)
            if len(values) != count:
                raise ValueError(f"{name} must match amplitudes")
            _nonnegative_tuple(values, name)
        if (
            type(self.hopping_displacements) is not tuple
            or not self.hopping_displacements
            or any(type(value) is not int for value in self.hopping_displacements)
        ):
            raise TypeError("hopping_displacements must contain built-in integers")
        if tuple(sorted(set(self.hopping_displacements))) != (
            self.hopping_displacements
        ):
            raise ValueError("hopping_displacements must be unique and increasing")
        width = len(self.hopping_displacements)
        _rows(
            self.reference_hopping_powers,
            row_count=count,
            width=width,
            name="reference_hopping_powers",
        )
        _rows(
            self.comparison_hopping_powers,
            row_count=count,
            width=width,
            name="comparison_hopping_powers",
        )

    @classmethod
    def from_analysis(
        cls,
        analysis: Periodic1DRank2Analysis,
        *,
        source_sha256: str,
    ) -> Self:
        """Project one qualified authoritative analysis without rerunning it."""
        if type(analysis) is not Periodic1DRank2Analysis:
            raise TypeError("analysis must be an embedded rank-two analysis")
        if type(analysis.qualification) is not (Periodic1DRank2QualifiedParent):
            return cls(
                source_sha256=source_sha256,
                amplitudes=(),
                correlations=(),
                operator_thresholds=(),
                joint_thresholds=(),
                reference_nonzero_weights=(),
                comparison_nonzero_weights=(),
                band_defects=(),
                reconstruction_defects=(),
                reference_parseval_defects=(),
                comparison_parseval_defects=(),
                hopping_displacements=(),
                reference_hopping_powers=(),
                comparison_hopping_powers=(),
            )
        first = analysis.points[0]
        return cls(
            source_sha256=source_sha256,
            amplitudes=tuple(point.amplitude for point in analysis.points),
            correlations=tuple(
                point.discrete_maximum_correlation for point in analysis.points
            ),
            operator_thresholds=tuple(
                point.minimum_operator_threshold for point in analysis.points
            ),
            joint_thresholds=tuple(
                point.exact_spectrum_joint_operator_threshold
                for point in analysis.points
            ),
            reference_nonzero_weights=tuple(
                point.reference_nonzero_hopping_weight for point in analysis.points
            ),
            comparison_nonzero_weights=tuple(
                point.comparison_nonzero_hopping_weight for point in analysis.points
            ),
            band_defects=tuple(point.maximum_band_defect for point in analysis.points),
            reconstruction_defects=tuple(
                point.minimum_loss_reconstruction_defect for point in analysis.points
            ),
            reference_parseval_defects=tuple(
                point.reference_parseval_defect for point in analysis.points
            ),
            comparison_parseval_defects=tuple(
                point.comparison_parseval_defect for point in analysis.points
            ),
            hopping_displacements=tuple(
                item.displacement for item in first.hopping_powers
            ),
            reference_hopping_powers=tuple(
                tuple(
                    item.reference_normalized_squared_frobenius_norm
                    for item in point.hopping_powers
                )
                for point in analysis.points
            ),
            comparison_hopping_powers=tuple(
                tuple(
                    item.comparison_normalized_squared_frobenius_norm
                    for item in point.hopping_powers
                )
                for point in analysis.points
            ),
        )

    def _mapping(self) -> Mapping[str, SerializableValue]:
        return {
            "source_sha256": self.source_sha256,
            "amplitudes": self.amplitudes,
            "correlations": self.correlations,
            "operator_thresholds": self.operator_thresholds,
            "joint_thresholds": self.joint_thresholds,
            "reference_nonzero_weights": self.reference_nonzero_weights,
            "comparison_nonzero_weights": self.comparison_nonzero_weights,
            "band_defects": self.band_defects,
            "reconstruction_defects": self.reconstruction_defects,
            "reference_parseval_defects": self.reference_parseval_defects,
            "comparison_parseval_defects": self.comparison_parseval_defects,
            "hopping_displacements": self.hopping_displacements,
            "reference_hopping_powers": self.reference_hopping_powers,
            "comparison_hopping_powers": self.comparison_hopping_powers,
        }

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        expected = {
            "source_sha256",
            "amplitudes",
            "correlations",
            "operator_thresholds",
            "joint_thresholds",
            "reference_nonzero_weights",
            "comparison_nonzero_weights",
            "band_defects",
            "reconstruction_defects",
            "reference_parseval_defects",
            "comparison_parseval_defects",
            "hopping_displacements",
            "reference_hopping_powers",
            "comparison_hopping_powers",
        }
        if set(values) != expected:
            raise ValueError("embedded visualization-data fields do not match")
        digest = values["source_sha256"]
        if type(digest) is not str:
            raise TypeError("source_sha256 must decode to a built-in string")
        return cls(
            source_sha256=digest,
            amplitudes=_float_tuple(values, "amplitudes"),
            correlations=_float_tuple(values, "correlations"),
            operator_thresholds=_float_tuple(values, "operator_thresholds"),
            joint_thresholds=_float_tuple(values, "joint_thresholds"),
            reference_nonzero_weights=_float_tuple(values, "reference_nonzero_weights"),
            comparison_nonzero_weights=_float_tuple(
                values, "comparison_nonzero_weights"
            ),
            band_defects=_float_tuple(values, "band_defects"),
            reconstruction_defects=_float_tuple(values, "reconstruction_defects"),
            reference_parseval_defects=_float_tuple(
                values, "reference_parseval_defects"
            ),
            comparison_parseval_defects=_float_tuple(
                values, "comparison_parseval_defects"
            ),
            hopping_displacements=_int_tuple(values, "hopping_displacements"),
            reference_hopping_powers=_float_rows(values, "reference_hopping_powers"),
            comparison_hopping_powers=_float_rows(values, "comparison_hopping_powers"),
        )


@dataclass(frozen=True, slots=True)
class Periodic1DRank2ParentFamilyVisualizationData(BaseVisualizationData):
    """Project one fully qualified parent family for authenticated rendering."""

    source_sha256: str
    parent_hopping_scales: tuple[float, ...]
    amplitudes: tuple[float, ...]
    minimum_external_gaps: tuple[float, ...]
    minimum_transport_singular_values: tuple[float, ...]
    correlations: tuple[tuple[float, ...], ...]
    operator_thresholds: tuple[tuple[float, ...], ...]
    reference_nonzero_weights: tuple[tuple[float, ...], ...]
    comparison_nonzero_weights: tuple[tuple[float, ...], ...]

    def __post_init__(self) -> None:
        _digest(self.source_sha256)
        _finite_tuple(self.parent_hopping_scales, "parent_hopping_scales")
        _finite_tuple(self.amplitudes, "amplitudes")
        count = len(self.parent_hopping_scales)
        width = len(self.amplitudes)
        for name in (
            "minimum_external_gaps",
            "minimum_transport_singular_values",
        ):
            values = getattr(self, name)
            if len(values) != count:
                raise ValueError(f"{name} must match parent_hopping_scales")
            _nonnegative_tuple(values, name)
        _rows(
            self.correlations,
            row_count=count,
            width=width,
            name="correlations",
            signed=True,
        )
        if any(not -1.0 <= value <= 1.0 for row in self.correlations for value in row):
            raise ValueError("correlations must lie in [-1, 1]")
        for name in (
            "operator_thresholds",
            "reference_nonzero_weights",
            "comparison_nonzero_weights",
        ):
            _rows(
                getattr(self, name),
                row_count=count,
                width=width,
                name=name,
            )

    @classmethod
    def from_analysis(
        cls,
        analysis: Periodic1DRank2ParentFamilyAnalysis,
        *,
        source_sha256: str,
    ) -> Self:
        """Project a fully qualified family without rerunning its analyzer."""
        if type(analysis) is not Periodic1DRank2ParentFamilyAnalysis:
            raise TypeError("analysis must be an embedded rank-two parent family")
        if any(
            type(member.qualification) is not Periodic1DRank2QualifiedParent
            for member in analysis.members
        ):
            raise ValueError("visualization requires a fully qualified parent family")
        qualifications = tuple(member.qualification for member in analysis.members)
        return cls(
            source_sha256=source_sha256,
            parent_hopping_scales=analysis.request.parent_hopping_scales,
            amplitudes=analysis.request.template_request.amplitudes,
            minimum_external_gaps=tuple(
                qualification.minimum_external_gap for qualification in qualifications
            ),
            minimum_transport_singular_values=tuple(
                qualification.minimum_transport_singular_value
                for qualification in qualifications
                if type(qualification) is Periodic1DRank2QualifiedParent
            ),
            correlations=tuple(
                tuple(point.discrete_maximum_correlation for point in member.points)
                for member in analysis.members
            ),
            operator_thresholds=tuple(
                tuple(point.minimum_operator_threshold for point in member.points)
                for member in analysis.members
            ),
            reference_nonzero_weights=tuple(
                tuple(point.reference_nonzero_hopping_weight for point in member.points)
                for member in analysis.members
            ),
            comparison_nonzero_weights=tuple(
                tuple(
                    point.comparison_nonzero_hopping_weight for point in member.points
                )
                for member in analysis.members
            ),
        )

    def _mapping(self) -> Mapping[str, SerializableValue]:
        return {
            "source_sha256": self.source_sha256,
            "parent_hopping_scales": self.parent_hopping_scales,
            "amplitudes": self.amplitudes,
            "minimum_external_gaps": self.minimum_external_gaps,
            "minimum_transport_singular_values": (
                self.minimum_transport_singular_values
            ),
            "correlations": self.correlations,
            "operator_thresholds": self.operator_thresholds,
            "reference_nonzero_weights": self.reference_nonzero_weights,
            "comparison_nonzero_weights": self.comparison_nonzero_weights,
        }

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        expected = {
            "source_sha256",
            "parent_hopping_scales",
            "amplitudes",
            "minimum_external_gaps",
            "minimum_transport_singular_values",
            "correlations",
            "operator_thresholds",
            "reference_nonzero_weights",
            "comparison_nonzero_weights",
        }
        if set(values) != expected:
            raise ValueError("family visualization-data fields do not match")
        digest = values["source_sha256"]
        if type(digest) is not str:
            raise TypeError("source_sha256 must decode to a built-in string")
        return cls(
            source_sha256=digest,
            parent_hopping_scales=_float_tuple(values, "parent_hopping_scales"),
            amplitudes=_float_tuple(values, "amplitudes"),
            minimum_external_gaps=_float_tuple(values, "minimum_external_gaps"),
            minimum_transport_singular_values=_float_tuple(
                values, "minimum_transport_singular_values"
            ),
            correlations=_float_rows(values, "correlations"),
            operator_thresholds=_float_rows(values, "operator_thresholds"),
            reference_nonzero_weights=_float_rows(values, "reference_nonzero_weights"),
            comparison_nonzero_weights=_float_rows(
                values, "comparison_nonzero_weights"
            ),
        )


@dataclass(frozen=True, slots=True)
class Periodic1DRank2CalculationVisualizationData(BaseVisualizationData):
    """Project the cohesive aggregate into separate renderable channels."""

    MOMENTUM_CHANNELS: ClassVar[tuple[str, ...]] = (
        "parent diagnostic change",
        "correlation change",
        "operator-threshold change",
        "hopping-weight change",
        "hopping-power change",
        "maximizing-angle change",
        "band defect",
        "reconstruction defect",
        "Parseval defect",
    )
    AMPLITUDE_CHANNELS: ClassVar[tuple[str, ...]] = (
        "correlation defect",
        "operator-threshold defect",
        "joint-threshold defect",
        "hopping-weight defect",
        "hopping-power defect",
    )
    TRUNCATION_POWER_CHANNELS: ClassVar[tuple[str, ...]] = (
        "reference ordinary omitted power",
        "comparison ordinary omitted power",
        "reference total omitted power",
        "comparison total omitted power",
    )
    TRUNCATION_ERROR_CHANNELS: ClassVar[tuple[str, ...]] = (
        "reference Hamiltonian truncation error",
        "reference spectral truncation error",
        "comparison Hamiltonian truncation error",
        "comparison spectral truncation error",
        "comparison total Hamiltonian error",
        "comparison total spectral error",
    )
    INTERPOLATION_CHANNELS: ClassVar[tuple[str, ...]] = (
        "direct spectral defect",
        "comparison interpolation Hamiltonian error",
        "comparison interpolation spectral error",
    )

    source_sha256: str
    parent_family_visualization_data_sha256: str
    momentum_fine_mesh_sizes: tuple[int, ...]
    momentum_defects: tuple[tuple[float, ...], ...]
    momentum_within_tolerances: tuple[bool, ...]
    adaptive_level_indices: tuple[int, ...]
    adaptive_midpoint_defects: tuple[tuple[float, ...], ...]
    adaptive_validation_level_indices: tuple[int, ...]
    adaptive_validation_defects: tuple[tuple[float, ...], ...]
    truncation_maximum_ranges: tuple[int, ...]
    truncation_omitted_powers: tuple[tuple[float, ...], ...]
    truncation_maximum_errors: tuple[tuple[float, ...], ...]
    truncation_amplitudes: tuple[float, ...]
    truncation_interpolation_maximum_errors: tuple[tuple[float, ...], ...]

    def __post_init__(self) -> None:
        _digest(self.source_sha256)
        _digest(self.parent_family_visualization_data_sha256)
        self._validate_channel(
            self.momentum_fine_mesh_sizes,
            self.momentum_defects,
            len(self.MOMENTUM_CHANNELS),
            int,
            "momentum_defects",
        )
        if len(self.momentum_within_tolerances) != len(
            self.momentum_fine_mesh_sizes
        ) or any(type(value) is not bool for value in self.momentum_within_tolerances):
            raise ValueError("momentum dispositions must match the mesh inventory")
        self._validate_channel(
            self.adaptive_level_indices,
            self.adaptive_midpoint_defects,
            len(self.AMPLITUDE_CHANNELS),
            int,
            "adaptive_midpoint_defects",
        )
        self._validate_channel(
            self.adaptive_validation_level_indices,
            self.adaptive_validation_defects,
            len(self.AMPLITUDE_CHANNELS),
            int,
            "adaptive_validation_defects",
        )
        self._validate_channel(
            self.truncation_maximum_ranges,
            self.truncation_omitted_powers,
            len(self.TRUNCATION_POWER_CHANNELS),
            int,
            "truncation_omitted_powers",
        )
        self._validate_channel(
            self.truncation_maximum_ranges,
            self.truncation_maximum_errors,
            len(self.TRUNCATION_ERROR_CHANNELS),
            int,
            "truncation_maximum_errors",
        )
        self._validate_channel(
            self.truncation_amplitudes,
            self.truncation_interpolation_maximum_errors,
            len(self.INTERPOLATION_CHANNELS),
            float,
            "truncation_interpolation_maximum_errors",
        )

    @staticmethod
    def _validate_channel(
        inventory: tuple[int, ...] | tuple[float, ...],
        rows: tuple[tuple[float, ...], ...],
        row_count: int,
        scalar_type: type[int] | type[float],
        name: str,
    ) -> None:
        if type(inventory) is not tuple:
            raise TypeError(f"{name} inventory must be a tuple")
        if not inventory:
            if rows:
                raise ValueError(f"empty {name} inventory requires empty channels")
            return
        if any(type(value) is not scalar_type for value in inventory):
            raise TypeError(f"{name} inventory has an invalid scalar type")
        if any(
            type(value) is float and not math.isfinite(value) for value in inventory
        ):
            raise ValueError(f"{name} inventory must be finite")
        if any(value < 0 for value in inventory):
            raise ValueError(f"{name} inventory must be nonnegative")
        if tuple(sorted(set(inventory))) != inventory:
            raise ValueError(f"{name} inventory must be unique and increasing")
        _rows(rows, row_count=row_count, width=len(inventory), name=name)

    @classmethod
    def from_record(
        cls,
        record: Periodic1DRank2CalculationRecord,
        *,
        source_sha256: str,
    ) -> Self:
        """Project retained values without rerunning a scientific owner."""
        if type(record) is not Periodic1DRank2CalculationRecord:
            raise TypeError("record must be an embedded rank-two calculation record")
        family_bytes = Periodic1DRank2ParentFamilyAnalysisRecord(
            record.parent_family
        ).to_json()
        family_sha256 = hashlib.sha256(family_bytes).hexdigest()
        family_data = Periodic1DRank2ParentFamilyVisualizationData.from_analysis(
            record.parent_family,
            source_sha256=family_sha256,
        )
        momentum = record.momentum_refinement.refinements
        adaptive = record.adaptive_amplitude
        if type(adaptive) is (Periodic1DRank2AdaptiveAmplitudeConverged):
            levels = adaptive.levels
            validations = adaptive.validations
        elif type(adaptive) is (Periodic1DRank2AdaptiveAmplitudeLevelsExhausted):
            levels = adaptive.levels
            validations = adaptive.validations
        elif type(adaptive) is (Periodic1DRank2AdaptiveAmplitudeEvaluationsExhausted):
            levels = adaptive.levels
            validations = adaptive.validations
        else:
            levels = ()
            validations = ()
        from ..truncation.results import (
            Periodic1DRank2TruncationCompleted,
        )

        truncation = record.truncation
        if type(truncation) is Periodic1DRank2TruncationCompleted:
            ranges = truncation.request.maximum_ranges
            points = truncation.points
            omitted_powers = tuple(
                tuple(
                    max(getattr(point.ranges[index], field) for point in points)
                    for index in range(len(ranges))
                )
                for field in (
                    "reference_ordinary_omitted_power",
                    "comparison_ordinary_omitted_power",
                    "reference_total_omitted_power",
                    "comparison_total_omitted_power",
                )
            )
            maximum_errors = tuple(
                tuple(
                    max(getattr(point.ranges[index], field) for point in points)
                    for index in range(len(ranges))
                )
                for field in (
                    "reference_truncation_hamiltonian_maximum_error",
                    "reference_truncation_spectral_maximum_error",
                    "comparison_truncation_hamiltonian_maximum_error",
                    "comparison_truncation_spectral_maximum_error",
                    "comparison_total_hamiltonian_maximum_error",
                    "comparison_total_spectral_maximum_error",
                )
            )
            amplitudes = tuple(point.amplitude for point in points)
            interpolation_errors = tuple(
                tuple(getattr(point, field) for point in points)
                for field in (
                    "direct_spectral_maximum_defect",
                    "comparison_interpolation_hamiltonian_maximum_error",
                    "comparison_interpolation_spectral_maximum_error",
                )
            )
        else:
            ranges = ()
            omitted_powers = ()
            maximum_errors = ()
            amplitudes = ()
            interpolation_errors = ()
        return cls(
            source_sha256=source_sha256,
            parent_family_visualization_data_sha256=hashlib.sha256(
                family_data.to_json()
            ).hexdigest(),
            momentum_fine_mesh_sizes=tuple(step.fine_mesh_size for step in momentum),
            momentum_defects=tuple(
                tuple(getattr(step, field) for step in momentum)
                for field in (
                    "maximum_parent_diagnostic_change",
                    "maximum_correlation_change",
                    "maximum_threshold_change",
                    "maximum_hopping_weight_change",
                    "maximum_hopping_power_change",
                    "maximum_angle_change",
                    "maximum_band_defect",
                    "maximum_reconstruction_defect",
                    "maximum_parseval_defect",
                )
            )
            if momentum
            else (),
            momentum_within_tolerances=tuple(
                step.within_tolerances for step in momentum
            ),
            adaptive_level_indices=tuple(level.level_index for level in levels),
            adaptive_midpoint_defects=cls._amplitude_defects(levels),
            adaptive_validation_level_indices=tuple(
                validation.level_index for validation in validations
            ),
            adaptive_validation_defects=cls._amplitude_defects(validations),
            truncation_maximum_ranges=ranges,
            truncation_omitted_powers=omitted_powers,
            truncation_maximum_errors=maximum_errors,
            truncation_amplitudes=amplitudes,
            truncation_interpolation_maximum_errors=interpolation_errors,
        )

    @staticmethod
    def _amplitude_defects(
        values: tuple[
            Periodic1DRank2AmplitudeRefinementLevel
            | Periodic1DRank2AmplitudeValidation,
            ...,
        ],
    ) -> tuple[tuple[float, ...], ...]:
        if not values:
            return ()
        return tuple(
            tuple(getattr(value, field) for value in values)
            for field in (
                "maximum_correlation_defect",
                "maximum_operator_threshold_defect",
                "maximum_joint_threshold_defect",
                "maximum_hopping_weight_defect",
                "maximum_hopping_power_defect",
            )
        )

    def _mapping(self) -> Mapping[str, SerializableValue]:
        return {
            "source_sha256": self.source_sha256,
            "parent_family_visualization_data_sha256": (
                self.parent_family_visualization_data_sha256
            ),
            "momentum_fine_mesh_sizes": self.momentum_fine_mesh_sizes,
            "momentum_defects": self.momentum_defects,
            "momentum_within_tolerances": self.momentum_within_tolerances,
            "adaptive_level_indices": self.adaptive_level_indices,
            "adaptive_midpoint_defects": self.adaptive_midpoint_defects,
            "adaptive_validation_level_indices": (
                self.adaptive_validation_level_indices
            ),
            "adaptive_validation_defects": self.adaptive_validation_defects,
            "truncation_maximum_ranges": self.truncation_maximum_ranges,
            "truncation_omitted_powers": self.truncation_omitted_powers,
            "truncation_maximum_errors": self.truncation_maximum_errors,
            "truncation_amplitudes": self.truncation_amplitudes,
            "truncation_interpolation_maximum_errors": (
                self.truncation_interpolation_maximum_errors
            ),
        }

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        expected = {
            "source_sha256",
            "parent_family_visualization_data_sha256",
            "momentum_fine_mesh_sizes",
            "momentum_defects",
            "momentum_within_tolerances",
            "adaptive_level_indices",
            "adaptive_midpoint_defects",
            "adaptive_validation_level_indices",
            "adaptive_validation_defects",
            "truncation_maximum_ranges",
            "truncation_omitted_powers",
            "truncation_maximum_errors",
            "truncation_amplitudes",
            "truncation_interpolation_maximum_errors",
        }
        if set(values) != expected:
            raise ValueError("calculation visualization-data fields do not match")
        source = values["source_sha256"]
        family = values["parent_family_visualization_data_sha256"]
        if type(source) is not str or type(family) is not str:
            raise TypeError("visualization identities must decode to strings")
        return cls(
            source_sha256=source,
            parent_family_visualization_data_sha256=family,
            momentum_fine_mesh_sizes=_int_tuple(values, "momentum_fine_mesh_sizes"),
            momentum_defects=_float_rows(values, "momentum_defects"),
            momentum_within_tolerances=_bool_tuple(
                values, "momentum_within_tolerances"
            ),
            adaptive_level_indices=_int_tuple(values, "adaptive_level_indices"),
            adaptive_midpoint_defects=_float_rows(values, "adaptive_midpoint_defects"),
            adaptive_validation_level_indices=_int_tuple(
                values, "adaptive_validation_level_indices"
            ),
            adaptive_validation_defects=_float_rows(
                values, "adaptive_validation_defects"
            ),
            truncation_maximum_ranges=_int_tuple(values, "truncation_maximum_ranges"),
            truncation_omitted_powers=_float_rows(values, "truncation_omitted_powers"),
            truncation_maximum_errors=_float_rows(values, "truncation_maximum_errors"),
            truncation_amplitudes=_float_tuple(values, "truncation_amplitudes"),
            truncation_interpolation_maximum_errors=_float_rows(
                values, "truncation_interpolation_maximum_errors"
            ),
        )


__all__ = [
    "Periodic1DRank2CalculationVisualizationData",
    "Periodic1DRank2ParentFamilyVisualizationData",
    "Periodic1DRank2VisualizationData",
]
