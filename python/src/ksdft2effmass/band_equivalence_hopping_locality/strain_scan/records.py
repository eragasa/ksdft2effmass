"""Immutable synthetic-strain scan assessment records."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Self

from ksdft2effmass.serialization import BaseTypedRecord, SerializableValue

from ..strain_response import StrainWitnessControlEnum


@dataclass(frozen=True, slots=True)
class StrainWitnessRequirementEnvelope(BaseTypedRecord):
    """Retain sampled extrema for one representation-witness control."""

    control: StrainWitnessControlEnum
    optimized_maximum: float
    optimized_maximum_strain_fraction: float
    fixed_candidate_maximum: float
    fixed_candidate_maximum_strain_fraction: float
    minimum_splitting_scale: float
    minimum_splitting_scale_strain_fraction: float
    maximum_splitting_scale: float
    maximum_splitting_scale_strain_fraction: float
    minimum_correlation: float
    minimum_correlation_strain_fraction: float
    maximum_correlation: float
    maximum_correlation_strain_fraction: float

    def _mapping(self) -> Mapping[str, SerializableValue]:
        return {
            "control": self.control.to_wire(),
            "optimized_maximum": self.optimized_maximum,
            "optimized_maximum_strain_fraction": self.optimized_maximum_strain_fraction,
            "fixed_candidate_maximum": self.fixed_candidate_maximum,
            "fixed_candidate_maximum_strain_fraction": (
                self.fixed_candidate_maximum_strain_fraction
            ),
            "minimum_splitting_scale": self.minimum_splitting_scale,
            "minimum_splitting_scale_strain_fraction": (
                self.minimum_splitting_scale_strain_fraction
            ),
            "maximum_splitting_scale": self.maximum_splitting_scale,
            "maximum_splitting_scale_strain_fraction": (
                self.maximum_splitting_scale_strain_fraction
            ),
            "minimum_correlation": self.minimum_correlation,
            "minimum_correlation_strain_fraction": (
                self.minimum_correlation_strain_fraction
            ),
            "maximum_correlation": self.maximum_correlation,
            "maximum_correlation_strain_fraction": (
                self.maximum_correlation_strain_fraction
            ),
        }

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        required = {
            "control",
            "optimized_maximum",
            "optimized_maximum_strain_fraction",
            "fixed_candidate_maximum",
            "fixed_candidate_maximum_strain_fraction",
            "minimum_splitting_scale",
            "minimum_splitting_scale_strain_fraction",
            "maximum_splitting_scale",
            "maximum_splitting_scale_strain_fraction",
            "minimum_correlation",
            "minimum_correlation_strain_fraction",
            "maximum_correlation",
            "maximum_correlation_strain_fraction",
        }
        if set(values) != required:
            raise ValueError("StrainWitnessRequirementEnvelope fields do not match")
        control_wire = values["control"]
        optimized_maximum = values["optimized_maximum"]
        optimized_maximum_strain_fraction = values["optimized_maximum_strain_fraction"]
        fixed_candidate_maximum = values["fixed_candidate_maximum"]
        fixed_candidate_maximum_strain_fraction = values[
            "fixed_candidate_maximum_strain_fraction"
        ]
        minimum_splitting_scale = values["minimum_splitting_scale"]
        minimum_splitting_scale_strain_fraction = values[
            "minimum_splitting_scale_strain_fraction"
        ]
        maximum_splitting_scale = values["maximum_splitting_scale"]
        maximum_splitting_scale_strain_fraction = values[
            "maximum_splitting_scale_strain_fraction"
        ]
        minimum_correlation = values["minimum_correlation"]
        minimum_correlation_strain_fraction = values[
            "minimum_correlation_strain_fraction"
        ]
        maximum_correlation = values["maximum_correlation"]
        maximum_correlation_strain_fraction = values[
            "maximum_correlation_strain_fraction"
        ]
        if (
            type(optimized_maximum) is not float
            or type(optimized_maximum_strain_fraction) is not float
            or type(fixed_candidate_maximum) is not float
            or type(fixed_candidate_maximum_strain_fraction) is not float
            or type(minimum_splitting_scale) is not float
            or type(minimum_splitting_scale_strain_fraction) is not float
            or type(maximum_splitting_scale) is not float
            or type(maximum_splitting_scale_strain_fraction) is not float
            or type(minimum_correlation) is not float
            or type(minimum_correlation_strain_fraction) is not float
            or type(maximum_correlation) is not float
            or type(maximum_correlation_strain_fraction) is not float
        ):
            raise TypeError("float fields must use exact built-in types")
        if type(control_wire) is not str:
            raise TypeError("enum fields must decode to built-in strings")
        return cls(
            control=StrainWitnessControlEnum.from_wire(control_wire),
            optimized_maximum=optimized_maximum,
            optimized_maximum_strain_fraction=optimized_maximum_strain_fraction,
            fixed_candidate_maximum=fixed_candidate_maximum,
            fixed_candidate_maximum_strain_fraction=fixed_candidate_maximum_strain_fraction,
            minimum_splitting_scale=minimum_splitting_scale,
            minimum_splitting_scale_strain_fraction=minimum_splitting_scale_strain_fraction,
            maximum_splitting_scale=maximum_splitting_scale,
            maximum_splitting_scale_strain_fraction=maximum_splitting_scale_strain_fraction,
            minimum_correlation=minimum_correlation,
            minimum_correlation_strain_fraction=minimum_correlation_strain_fraction,
            maximum_correlation=maximum_correlation,
            maximum_correlation_strain_fraction=maximum_correlation_strain_fraction,
        )


@dataclass(frozen=True, slots=True)
class StrainLocalityEnvelope(BaseTypedRecord):
    """Retain sampled physical-range and block-count maxima at one tolerance."""

    tail_tolerance: float
    maximum_physical_radius: float | None
    maximum_physical_radius_strain_fraction: float | None
    maximum_retained_blocks: int | None
    maximum_retained_blocks_strain_fraction: float | None

    def _mapping(self) -> Mapping[str, SerializableValue]:
        return {
            "tail_tolerance": self.tail_tolerance,
            "maximum_physical_radius": self.maximum_physical_radius,
            "maximum_physical_radius_strain_fraction": (
                self.maximum_physical_radius_strain_fraction
            ),
            "maximum_retained_blocks": self.maximum_retained_blocks,
            "maximum_retained_blocks_strain_fraction": (
                self.maximum_retained_blocks_strain_fraction
            ),
        }

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        required = {
            "tail_tolerance",
            "maximum_physical_radius",
            "maximum_physical_radius_strain_fraction",
            "maximum_retained_blocks",
            "maximum_retained_blocks_strain_fraction",
        }
        if set(values) != required:
            raise ValueError("StrainLocalityEnvelope fields do not match")
        tail_tolerance = values["tail_tolerance"]
        maximum_physical_radius = values["maximum_physical_radius"]
        maximum_physical_radius_strain_fraction = values[
            "maximum_physical_radius_strain_fraction"
        ]
        maximum_retained_blocks_strain_fraction = values[
            "maximum_retained_blocks_strain_fraction"
        ]
        maximum_retained_blocks = values["maximum_retained_blocks"]
        if type(tail_tolerance) is not float:
            raise TypeError("float fields must use exact built-in types")
        if (
            (
                maximum_physical_radius is not None
                and type(maximum_physical_radius) is not float
            )
            or (
                maximum_physical_radius_strain_fraction is not None
                and type(maximum_physical_radius_strain_fraction) is not float
            )
            or (
                maximum_retained_blocks_strain_fraction is not None
                and type(maximum_retained_blocks_strain_fraction) is not float
            )
        ):
            raise TypeError("optional float fields have invalid types")
        if (
            maximum_retained_blocks is not None
            and type(maximum_retained_blocks) is not int
        ):
            raise TypeError("optional integer fields have invalid types")
        return cls(
            tail_tolerance=tail_tolerance,
            maximum_physical_radius=maximum_physical_radius,
            maximum_physical_radius_strain_fraction=maximum_physical_radius_strain_fraction,
            maximum_retained_blocks=maximum_retained_blocks,
            maximum_retained_blocks_strain_fraction=maximum_retained_blocks_strain_fraction,
        )


@dataclass(frozen=True, slots=True)
class StrainResponseEnvelope(BaseTypedRecord):
    """Retain one sampled aligned strain-response maximum."""

    control: StrainWitnessControlEnum
    maximum_aligned_hamiltonian_defect: float
    maximum_strain_fraction: float

    def _mapping(self) -> Mapping[str, SerializableValue]:
        return {
            "control": self.control.to_wire(),
            "maximum_aligned_hamiltonian_defect": (
                self.maximum_aligned_hamiltonian_defect
            ),
            "maximum_strain_fraction": self.maximum_strain_fraction,
        }

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        required = {
            "control",
            "maximum_aligned_hamiltonian_defect",
            "maximum_strain_fraction",
        }
        if set(values) != required:
            raise ValueError("StrainResponseEnvelope fields do not match")
        control_wire = values["control"]
        maximum_aligned_hamiltonian_defect = values[
            "maximum_aligned_hamiltonian_defect"
        ]
        maximum_strain_fraction = values["maximum_strain_fraction"]
        if (
            type(maximum_aligned_hamiltonian_defect) is not float
            or type(maximum_strain_fraction) is not float
        ):
            raise TypeError("float fields must use exact built-in types")
        if type(control_wire) is not str:
            raise TypeError("enum fields must decode to built-in strings")
        return cls(
            control=StrainWitnessControlEnum.from_wire(control_wire),
            maximum_aligned_hamiltonian_defect=maximum_aligned_hamiltonian_defect,
            maximum_strain_fraction=maximum_strain_fraction,
        )


@dataclass(frozen=True, slots=True)
class SampledStrainMaximum(BaseTypedRecord):
    """Retain one sampled maximum and the first strain where it occurs."""

    value: float
    strain_fraction: float

    def _mapping(self) -> Mapping[str, SerializableValue]:
        return {"value": self.value, "strain_fraction": self.strain_fraction}

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        required = {
            "value",
            "strain_fraction",
        }
        if set(values) != required:
            raise ValueError("SampledStrainMaximum fields do not match")
        value = values["value"]
        strain_fraction = values["strain_fraction"]
        if type(value) is not float or type(strain_fraction) is not float:
            raise TypeError("float fields must use exact built-in types")
        return cls(
            value=value,
            strain_fraction=strain_fraction,
        )


@dataclass(frozen=True, slots=True)
class SampledStrainMinimum(BaseTypedRecord):
    """Retain one sampled minimum and the first strain where it occurs."""

    value: float
    strain_fraction: float

    def _mapping(self) -> Mapping[str, SerializableValue]:
        return {"value": self.value, "strain_fraction": self.strain_fraction}

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        required = {
            "value",
            "strain_fraction",
        }
        if set(values) != required:
            raise ValueError("SampledStrainMinimum fields do not match")
        value = values["value"]
        strain_fraction = values["strain_fraction"]
        if type(value) is not float or type(strain_fraction) is not float:
            raise TypeError("float fields must use exact built-in types")
        return cls(
            value=value,
            strain_fraction=strain_fraction,
        )


@dataclass(frozen=True, slots=True)
class StrainQualificationEnvelope(BaseTypedRecord):
    """Retain sampled subspace and frame qualification extrema."""

    control: StrainWitnessControlEnum
    external_isolation_gap: SampledStrainMinimum
    seed_overlap: SampledStrainMinimum
    frame_overlap_singular_value: SampledStrainMinimum
    pointwise_frame_alignment_residual: SampledStrainMaximum
    restricted_global_frame_alignment_residual: SampledStrainMaximum

    def _mapping(self) -> Mapping[str, SerializableValue]:
        return {
            "control": self.control.to_wire(),
            "external_isolation_gap": self.external_isolation_gap,
            "seed_overlap": self.seed_overlap,
            "frame_overlap_singular_value": self.frame_overlap_singular_value,
            "pointwise_frame_alignment_residual": (
                self.pointwise_frame_alignment_residual
            ),
            "restricted_global_frame_alignment_residual": (
                self.restricted_global_frame_alignment_residual
            ),
        }

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        required = {
            "control",
            "external_isolation_gap",
            "seed_overlap",
            "frame_overlap_singular_value",
            "pointwise_frame_alignment_residual",
            "restricted_global_frame_alignment_residual",
        }
        if set(values) != required:
            raise ValueError("StrainQualificationEnvelope fields do not match")
        control_wire = values["control"]
        external_isolation_gap_value = values["external_isolation_gap"]
        seed_overlap_value = values["seed_overlap"]
        frame_overlap_singular_value_value = values["frame_overlap_singular_value"]
        pointwise_frame_alignment_residual_value = values[
            "pointwise_frame_alignment_residual"
        ]
        restricted_global_frame_alignment_residual_value = values[
            "restricted_global_frame_alignment_residual"
        ]
        if type(control_wire) is not str:
            raise TypeError("enum fields must decode to built-in strings")
        if not isinstance(external_isolation_gap_value, Mapping):
            raise TypeError("external_isolation_gap must decode to a mapping")
        if not isinstance(seed_overlap_value, Mapping):
            raise TypeError("seed_overlap must decode to a mapping")
        if not isinstance(frame_overlap_singular_value_value, Mapping):
            raise TypeError("frame_overlap_singular_value must decode to a mapping")
        if not isinstance(pointwise_frame_alignment_residual_value, Mapping):
            raise TypeError(
                "pointwise_frame_alignment_residual must decode to a mapping"
            )
        if not isinstance(restricted_global_frame_alignment_residual_value, Mapping):
            raise TypeError(
                "restricted_global_frame_alignment_residual must decode to a mapping"
            )
        return cls(
            control=StrainWitnessControlEnum.from_wire(control_wire),
            external_isolation_gap=SampledStrainMinimum.from_dict(
                external_isolation_gap_value
            ),
            seed_overlap=SampledStrainMinimum.from_dict(seed_overlap_value),
            frame_overlap_singular_value=SampledStrainMinimum.from_dict(
                frame_overlap_singular_value_value
            ),
            pointwise_frame_alignment_residual=SampledStrainMaximum.from_dict(
                pointwise_frame_alignment_residual_value
            ),
            restricted_global_frame_alignment_residual=SampledStrainMaximum.from_dict(
                restricted_global_frame_alignment_residual_value
            ),
        )


@dataclass(frozen=True, slots=True)
class StrainErrorChannelEnvelope(BaseTypedRecord):
    """Retain sampled maxima of one four-component error channel."""

    sample_count: int
    maximum_hamiltonian: SampledStrainMaximum
    rms_hamiltonian: SampledStrainMaximum
    maximum_band: SampledStrainMaximum
    rms_band: SampledStrainMaximum

    def _mapping(self) -> Mapping[str, SerializableValue]:
        return {
            "sample_count": self.sample_count,
            "maximum_hamiltonian": self.maximum_hamiltonian,
            "rms_hamiltonian": self.rms_hamiltonian,
            "maximum_band": self.maximum_band,
            "rms_band": self.rms_band,
        }

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        required = {
            "sample_count",
            "maximum_hamiltonian",
            "rms_hamiltonian",
            "maximum_band",
            "rms_band",
        }
        if set(values) != required:
            raise ValueError("StrainErrorChannelEnvelope fields do not match")
        sample_count = values["sample_count"]
        maximum_hamiltonian_value = values["maximum_hamiltonian"]
        rms_hamiltonian_value = values["rms_hamiltonian"]
        maximum_band_value = values["maximum_band"]
        rms_band_value = values["rms_band"]
        if type(sample_count) is not int:
            raise TypeError("integer fields must use exact built-in types")
        if not isinstance(maximum_hamiltonian_value, Mapping):
            raise TypeError("maximum_hamiltonian must decode to a mapping")
        if not isinstance(rms_hamiltonian_value, Mapping):
            raise TypeError("rms_hamiltonian must decode to a mapping")
        if not isinstance(maximum_band_value, Mapping):
            raise TypeError("maximum_band must decode to a mapping")
        if not isinstance(rms_band_value, Mapping):
            raise TypeError("rms_band must decode to a mapping")
        return cls(
            sample_count=sample_count,
            maximum_hamiltonian=SampledStrainMaximum.from_dict(
                maximum_hamiltonian_value
            ),
            rms_hamiltonian=SampledStrainMaximum.from_dict(rms_hamiltonian_value),
            maximum_band=SampledStrainMaximum.from_dict(maximum_band_value),
            rms_band=SampledStrainMaximum.from_dict(rms_band_value),
        )


@dataclass(frozen=True, slots=True)
class StrainCutoffApproximationEnvelope(BaseTypedRecord):
    """Retain sampled error and omitted-power extrema at one cutoff rule."""

    tail_tolerance: float
    omitted_power: SampledStrainMaximum
    truncation: StrainErrorChannelEnvelope | None
    total: StrainErrorChannelEnvelope | None
    delta_omitted_power: SampledStrainMaximum
    delta_truncation: StrainErrorChannelEnvelope | None
    delta_total: StrainErrorChannelEnvelope | None

    def _mapping(self) -> Mapping[str, SerializableValue]:
        return {
            "tail_tolerance": self.tail_tolerance,
            "omitted_power": self.omitted_power,
            "truncation": self.truncation,
            "total": self.total,
            "delta_omitted_power": self.delta_omitted_power,
            "delta_truncation": self.delta_truncation,
            "delta_total": self.delta_total,
        }

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        required = {
            "tail_tolerance",
            "omitted_power",
            "truncation",
            "total",
            "delta_omitted_power",
            "delta_truncation",
            "delta_total",
        }
        if set(values) != required:
            raise ValueError("StrainCutoffApproximationEnvelope fields do not match")
        tail_tolerance = values["tail_tolerance"]
        omitted_power_value = values["omitted_power"]
        delta_omitted_power_value = values["delta_omitted_power"]
        truncation_value = values["truncation"]
        total_value = values["total"]
        delta_truncation_value = values["delta_truncation"]
        delta_total_value = values["delta_total"]
        if type(tail_tolerance) is not float:
            raise TypeError("float fields must use exact built-in types")
        if not isinstance(omitted_power_value, Mapping):
            raise TypeError("omitted_power must decode to a mapping")
        if not isinstance(delta_omitted_power_value, Mapping):
            raise TypeError("delta_omitted_power must decode to a mapping")
        if truncation_value is not None and not isinstance(truncation_value, Mapping):
            raise TypeError("truncation must decode to a mapping or None")
        if total_value is not None and not isinstance(total_value, Mapping):
            raise TypeError("total must decode to a mapping or None")
        if delta_truncation_value is not None and not isinstance(
            delta_truncation_value, Mapping
        ):
            raise TypeError("delta_truncation must decode to a mapping or None")
        if delta_total_value is not None and not isinstance(delta_total_value, Mapping):
            raise TypeError("delta_total must decode to a mapping or None")
        return cls(
            tail_tolerance=tail_tolerance,
            omitted_power=SampledStrainMaximum.from_dict(omitted_power_value),
            truncation=None
            if truncation_value is None
            else StrainErrorChannelEnvelope.from_dict(truncation_value),
            total=None
            if total_value is None
            else StrainErrorChannelEnvelope.from_dict(total_value),
            delta_omitted_power=SampledStrainMaximum.from_dict(
                delta_omitted_power_value
            ),
            delta_truncation=None
            if delta_truncation_value is None
            else StrainErrorChannelEnvelope.from_dict(delta_truncation_value),
            delta_total=None
            if delta_total_value is None
            else StrainErrorChannelEnvelope.from_dict(delta_total_value),
        )


@dataclass(frozen=True, slots=True)
class StrainApproximationEnvelope(BaseTypedRecord):
    """Retain sampled numerical-approximation extrema for one response control."""

    control: StrainWitnessControlEnum
    aligned_strain_perturbation: StrainErrorChannelEnvelope
    interpolation: StrainErrorChannelEnvelope
    delta_interpolation: StrainErrorChannelEnvelope
    nyquist_power: SampledStrainMaximum
    delta_nyquist_power: SampledStrainMaximum
    cutoffs: tuple[StrainCutoffApproximationEnvelope, ...]

    def _mapping(self) -> Mapping[str, SerializableValue]:
        return {
            "control": self.control.to_wire(),
            "aligned_strain_perturbation": self.aligned_strain_perturbation,
            "interpolation": self.interpolation,
            "delta_interpolation": self.delta_interpolation,
            "nyquist_power": self.nyquist_power,
            "delta_nyquist_power": self.delta_nyquist_power,
            "cutoffs": self.cutoffs,
        }

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        required = {
            "control",
            "aligned_strain_perturbation",
            "interpolation",
            "delta_interpolation",
            "nyquist_power",
            "delta_nyquist_power",
            "cutoffs",
        }
        if set(values) != required:
            raise ValueError("StrainApproximationEnvelope fields do not match")
        control_wire = values["control"]
        aligned_strain_perturbation_value = values["aligned_strain_perturbation"]
        interpolation_value = values["interpolation"]
        delta_interpolation_value = values["delta_interpolation"]
        nyquist_power_value = values["nyquist_power"]
        delta_nyquist_power_value = values["delta_nyquist_power"]
        cutoffs_values = values["cutoffs"]
        if type(control_wire) is not str:
            raise TypeError("enum fields must decode to built-in strings")
        if not isinstance(aligned_strain_perturbation_value, Mapping):
            raise TypeError("aligned_strain_perturbation must decode to a mapping")
        if not isinstance(interpolation_value, Mapping):
            raise TypeError("interpolation must decode to a mapping")
        if not isinstance(delta_interpolation_value, Mapping):
            raise TypeError("delta_interpolation must decode to a mapping")
        if not isinstance(nyquist_power_value, Mapping):
            raise TypeError("nyquist_power must decode to a mapping")
        if not isinstance(delta_nyquist_power_value, Mapping):
            raise TypeError("delta_nyquist_power must decode to a mapping")
        if not isinstance(cutoffs_values, tuple) or any(
            not isinstance(item, Mapping) for item in cutoffs_values
        ):
            raise TypeError("cutoffs must decode to a tuple of mappings")
        return cls(
            control=StrainWitnessControlEnum.from_wire(control_wire),
            aligned_strain_perturbation=StrainErrorChannelEnvelope.from_dict(
                aligned_strain_perturbation_value
            ),
            interpolation=StrainErrorChannelEnvelope.from_dict(interpolation_value),
            delta_interpolation=StrainErrorChannelEnvelope.from_dict(
                delta_interpolation_value
            ),
            nyquist_power=SampledStrainMaximum.from_dict(nyquist_power_value),
            delta_nyquist_power=SampledStrainMaximum.from_dict(
                delta_nyquist_power_value
            ),
            cutoffs=tuple(
                StrainCutoffApproximationEnvelope.from_dict(item)
                for item in cutoffs_values
            ),
        )


@dataclass(frozen=True, slots=True)
class StrainResponseMechanismEnvelope(BaseTypedRecord):
    """Retain sampled extrema that attribute the synthetic response mechanism."""

    control: StrainWitnessControlEnum
    hopping_response_minimum: SampledStrainMinimum
    hopping_response_maximum: SampledStrainMaximum
    scalar_component_maximum: SampledStrainMaximum
    scalar_component_rms_maximum: SampledStrainMaximum
    traceless_component_maximum: SampledStrainMaximum
    traceless_component_rms_maximum: SampledStrainMaximum
    delta_onsite_power_maximum: SampledStrainMaximum
    delta_offsite_power_maximum: SampledStrainMaximum

    def _mapping(self) -> Mapping[str, SerializableValue]:
        return {
            "control": self.control.to_wire(),
            "hopping_response_minimum": self.hopping_response_minimum,
            "hopping_response_maximum": self.hopping_response_maximum,
            "scalar_component_maximum": self.scalar_component_maximum,
            "scalar_component_rms_maximum": self.scalar_component_rms_maximum,
            "traceless_component_maximum": self.traceless_component_maximum,
            "traceless_component_rms_maximum": self.traceless_component_rms_maximum,
            "delta_onsite_power_maximum": self.delta_onsite_power_maximum,
            "delta_offsite_power_maximum": self.delta_offsite_power_maximum,
        }

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        required = {
            "control",
            "hopping_response_minimum",
            "hopping_response_maximum",
            "scalar_component_maximum",
            "scalar_component_rms_maximum",
            "traceless_component_maximum",
            "traceless_component_rms_maximum",
            "delta_onsite_power_maximum",
            "delta_offsite_power_maximum",
        }
        if set(values) != required:
            raise ValueError("StrainResponseMechanismEnvelope fields do not match")
        control_wire = values["control"]
        hopping_response_minimum_value = values["hopping_response_minimum"]
        hopping_response_maximum_value = values["hopping_response_maximum"]
        scalar_component_maximum_value = values["scalar_component_maximum"]
        scalar_component_rms_maximum_value = values["scalar_component_rms_maximum"]
        traceless_component_maximum_value = values["traceless_component_maximum"]
        traceless_component_rms_maximum_value = values[
            "traceless_component_rms_maximum"
        ]
        delta_onsite_power_maximum_value = values["delta_onsite_power_maximum"]
        delta_offsite_power_maximum_value = values["delta_offsite_power_maximum"]
        if type(control_wire) is not str:
            raise TypeError("enum fields must decode to built-in strings")
        if not isinstance(hopping_response_minimum_value, Mapping):
            raise TypeError("hopping_response_minimum must decode to a mapping")
        if not isinstance(hopping_response_maximum_value, Mapping):
            raise TypeError("hopping_response_maximum must decode to a mapping")
        if not isinstance(scalar_component_maximum_value, Mapping):
            raise TypeError("scalar_component_maximum must decode to a mapping")
        if not isinstance(scalar_component_rms_maximum_value, Mapping):
            raise TypeError("scalar_component_rms_maximum must decode to a mapping")
        if not isinstance(traceless_component_maximum_value, Mapping):
            raise TypeError("traceless_component_maximum must decode to a mapping")
        if not isinstance(traceless_component_rms_maximum_value, Mapping):
            raise TypeError("traceless_component_rms_maximum must decode to a mapping")
        if not isinstance(delta_onsite_power_maximum_value, Mapping):
            raise TypeError("delta_onsite_power_maximum must decode to a mapping")
        if not isinstance(delta_offsite_power_maximum_value, Mapping):
            raise TypeError("delta_offsite_power_maximum must decode to a mapping")
        return cls(
            control=StrainWitnessControlEnum.from_wire(control_wire),
            hopping_response_minimum=SampledStrainMinimum.from_dict(
                hopping_response_minimum_value
            ),
            hopping_response_maximum=SampledStrainMaximum.from_dict(
                hopping_response_maximum_value
            ),
            scalar_component_maximum=SampledStrainMaximum.from_dict(
                scalar_component_maximum_value
            ),
            scalar_component_rms_maximum=SampledStrainMaximum.from_dict(
                scalar_component_rms_maximum_value
            ),
            traceless_component_maximum=SampledStrainMaximum.from_dict(
                traceless_component_maximum_value
            ),
            traceless_component_rms_maximum=SampledStrainMaximum.from_dict(
                traceless_component_rms_maximum_value
            ),
            delta_onsite_power_maximum=SampledStrainMaximum.from_dict(
                delta_onsite_power_maximum_value
            ),
            delta_offsite_power_maximum=SampledStrainMaximum.from_dict(
                delta_offsite_power_maximum_value
            ),
        )


@dataclass(frozen=True, slots=True)
class SyntheticStrainScanSummary(BaseTypedRecord):
    """Combine independently interpreted sampled scan envelopes."""

    base_sample_count: int
    maximum_volume_defect: float
    maximum_volume_defect_strain_fraction: float
    maximum_direct_band_defect: float
    maximum_direct_band_defect_strain_fraction: float
    witness_requirements: tuple[StrainWitnessRequirementEnvelope, ...]
    locality: tuple[StrainLocalityEnvelope, ...]
    responses: tuple[StrainResponseEnvelope, ...]
    qualifications: tuple[StrainQualificationEnvelope, ...]
    approximations: tuple[StrainApproximationEnvelope, ...]
    mechanisms: tuple[StrainResponseMechanismEnvelope, ...]
    status: str = "sampled-development-summary-not-continuum-certificate"

    def _mapping(self) -> Mapping[str, SerializableValue]:
        return {
            "base_sample_count": self.base_sample_count,
            "maximum_volume_defect": self.maximum_volume_defect,
            "maximum_volume_defect_strain_fraction": (
                self.maximum_volume_defect_strain_fraction
            ),
            "maximum_direct_band_defect": self.maximum_direct_band_defect,
            "maximum_direct_band_defect_strain_fraction": (
                self.maximum_direct_band_defect_strain_fraction
            ),
            "witness_requirements": self.witness_requirements,
            "locality": self.locality,
            "responses": self.responses,
            "qualifications": self.qualifications,
            "approximations": self.approximations,
            "mechanisms": self.mechanisms,
            "status": self.status,
        }

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        required = {
            "base_sample_count",
            "maximum_volume_defect",
            "maximum_volume_defect_strain_fraction",
            "maximum_direct_band_defect",
            "maximum_direct_band_defect_strain_fraction",
            "witness_requirements",
            "locality",
            "responses",
            "qualifications",
            "approximations",
            "mechanisms",
            "status",
        }
        if set(values) != required:
            raise ValueError("SyntheticStrainScanSummary fields do not match")
        base_sample_count = values["base_sample_count"]
        maximum_volume_defect = values["maximum_volume_defect"]
        maximum_volume_defect_strain_fraction = values[
            "maximum_volume_defect_strain_fraction"
        ]
        maximum_direct_band_defect = values["maximum_direct_band_defect"]
        maximum_direct_band_defect_strain_fraction = values[
            "maximum_direct_band_defect_strain_fraction"
        ]
        witness_requirements_values = values["witness_requirements"]
        locality_values = values["locality"]
        responses_values = values["responses"]
        qualifications_values = values["qualifications"]
        approximations_values = values["approximations"]
        mechanisms_values = values["mechanisms"]
        status = values["status"]
        if (
            type(maximum_volume_defect) is not float
            or type(maximum_volume_defect_strain_fraction) is not float
            or type(maximum_direct_band_defect) is not float
            or type(maximum_direct_band_defect_strain_fraction) is not float
        ):
            raise TypeError("float fields must use exact built-in types")
        if type(base_sample_count) is not int:
            raise TypeError("integer fields must use exact built-in types")
        if type(status) is not str:
            raise TypeError("string fields must use exact built-in types")
        if not isinstance(witness_requirements_values, tuple) or any(
            not isinstance(item, Mapping) for item in witness_requirements_values
        ):
            raise TypeError("witness_requirements must decode to a tuple of mappings")
        if not isinstance(locality_values, tuple) or any(
            not isinstance(item, Mapping) for item in locality_values
        ):
            raise TypeError("locality must decode to a tuple of mappings")
        if not isinstance(responses_values, tuple) or any(
            not isinstance(item, Mapping) for item in responses_values
        ):
            raise TypeError("responses must decode to a tuple of mappings")
        if not isinstance(qualifications_values, tuple) or any(
            not isinstance(item, Mapping) for item in qualifications_values
        ):
            raise TypeError("qualifications must decode to a tuple of mappings")
        if not isinstance(approximations_values, tuple) or any(
            not isinstance(item, Mapping) for item in approximations_values
        ):
            raise TypeError("approximations must decode to a tuple of mappings")
        if not isinstance(mechanisms_values, tuple) or any(
            not isinstance(item, Mapping) for item in mechanisms_values
        ):
            raise TypeError("mechanisms must decode to a tuple of mappings")
        return cls(
            base_sample_count=base_sample_count,
            maximum_volume_defect=maximum_volume_defect,
            maximum_volume_defect_strain_fraction=maximum_volume_defect_strain_fraction,
            maximum_direct_band_defect=maximum_direct_band_defect,
            maximum_direct_band_defect_strain_fraction=maximum_direct_band_defect_strain_fraction,
            witness_requirements=tuple(
                StrainWitnessRequirementEnvelope.from_dict(item)
                for item in witness_requirements_values
            ),
            locality=tuple(
                StrainLocalityEnvelope.from_dict(item) for item in locality_values
            ),
            responses=tuple(
                StrainResponseEnvelope.from_dict(item) for item in responses_values
            ),
            qualifications=tuple(
                StrainQualificationEnvelope.from_dict(item)
                for item in qualifications_values
            ),
            approximations=tuple(
                StrainApproximationEnvelope.from_dict(item)
                for item in approximations_values
            ),
            mechanisms=tuple(
                StrainResponseMechanismEnvelope.from_dict(item)
                for item in mechanisms_values
            ),
            status=status,
        )
