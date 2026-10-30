"""Bounded M1/M2 Hamiltonian diagnostics for synthetic finite-strain paths."""

from __future__ import annotations

import math
from collections.abc import Mapping
from dataclasses import dataclass
from enum import Enum
from typing import Self

import numpy as np
from projectkoios.numerics.finite_periodic.meshes import CenteredUniformMesh
from projectkoios.numerics.finite_periodic.numpy.matrix_series import (
    NumpyFiniteFourierMatrixSeries,
)
from projectkoios.numerics.finite_periodic.numpy.tensor_product_evaluation import (
    NumpyTensorProductFourierMatrixEvaluationDefinition,
    NumpyTensorProductFourierMatrixSeriesEvaluator,
)
from projectkoios.numerics.finite_periodic.numpy.transforms import (
    NumpyCenteredUniformMeshMatrixFourierTransformDefinition,
    NumpyCenteredUniformMeshMatrixFourierTransformer,
)
from projectkoios.numerics.numpy.typing import BoolArray
from projectkoios.numerics.numpy.typing import Complex128Array as ComplexArray
from projectkoios.numerics.numpy.typing import Float64Array as FloatArray

from ksdft2effmass.serialization import BaseTypedRecord, SerializableValue

from .alignment import restricted_alignment
from .strain import SyntheticStrainPathEnum

_SEED = np.eye(4, 2, dtype=np.complex128)


class StrainResponseModelEnum(Enum):
    """Select a frozen or radial-response four-state strain control."""

    def to_wire(self) -> str:
        """Return the stable wire label."""
        return str(self.value)

    @classmethod
    def from_wire(cls, wire: str) -> Self:
        """Reconstruct a model from its stable wire label."""
        if type(wire) is not str:
            raise TypeError("wire must be a built-in string")
        for member in cls:
            if member.to_wire() == wire:
                return member
        raise ValueError(f"unsupported strain-response model wire label: {wire!r}")

    M1_FROZEN = "M1-frozen-four-state-bipartite"
    M2_RADIAL = "M2-fixed-radial-response"


class StrainWitnessControlEnum(Enum):
    """Select one independently interpreted strain witness control."""

    def to_wire(self) -> str:
        """Return the stable wire label."""
        return str(self.value)

    @classmethod
    def from_wire(cls, wire: str) -> Self:
        """Reconstruct a control from its stable wire label."""
        if type(wire) is not str:
            raise TypeError("wire must be a built-in string")
        for member in cls:
            if member.to_wire() == wire:
                return member
        raise ValueError(f"unsupported strain-witness control wire label: {wire!r}")

    GEOMETRY_ONLY = "geometry-only-control"
    FROZEN_PARENT = "frozen-parent-null-response-control"
    RADIAL_RESPONSE = "synthetic-radial-response-control"


@dataclass(frozen=True, slots=True)
class StrainErrorChannels(BaseTypedRecord):
    """Retain normalized matrix and sorted-band discrepancies."""

    maximum_hamiltonian: float
    rms_hamiltonian: float
    maximum_band: float
    rms_band: float

    def _mapping(self) -> Mapping[str, SerializableValue]:
        return {
            "maximum_hamiltonian": self.maximum_hamiltonian,
            "rms_hamiltonian": self.rms_hamiltonian,
            "maximum_band": self.maximum_band,
            "rms_band": self.rms_band,
        }

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        required = {
            "maximum_hamiltonian",
            "rms_hamiltonian",
            "maximum_band",
            "rms_band",
        }
        if set(values) != required:
            raise ValueError("strain-error channel fields do not match")
        scalars: dict[str, float] = {}
        for name in required:
            value = values[name]
            if type(value) is not float:
                raise TypeError("strain-error channels must decode to floats")
            scalars[name] = value
        return cls(
            maximum_hamiltonian=scalars["maximum_hamiltonian"],
            rms_hamiltonian=scalars["rms_hamiltonian"],
            maximum_band=scalars["maximum_band"],
            rms_band=scalars["rms_band"],
        )


@dataclass(frozen=True, slots=True)
class StrainResponseCutoffDiagnostic(BaseTypedRecord):
    """Retain three-channel errors at one complete physical-radius support."""

    tail_tolerance: float
    physical_radius: float | None
    retained_blocks: int | None
    omitted_power: float
    truncation: StrainErrorChannels | None
    total: StrainErrorChannels | None
    delta_omitted_power: float
    delta_truncation: StrainErrorChannels | None
    delta_total: StrainErrorChannels | None

    def _mapping(self) -> Mapping[str, SerializableValue]:
        return {
            "tail_tolerance": self.tail_tolerance,
            "physical_radius": self.physical_radius,
            "retained_blocks": self.retained_blocks,
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
            "physical_radius",
            "retained_blocks",
            "omitted_power",
            "truncation",
            "total",
            "delta_omitted_power",
            "delta_truncation",
            "delta_total",
        }
        if set(values) != required:
            raise ValueError("strain-response cutoff fields do not match")
        tail = values["tail_tolerance"]
        radius = values["physical_radius"]
        blocks = values["retained_blocks"]
        omitted = values["omitted_power"]
        delta_omitted = values["delta_omitted_power"]
        if (
            type(tail) is not float
            or type(omitted) is not float
            or type(delta_omitted) is not float
        ):
            raise TypeError("cutoff powers and tolerance must decode to floats")
        if radius is not None and type(radius) is not float:
            raise TypeError("physical_radius must decode to a float or None")
        if blocks is not None and type(blocks) is not int:
            raise TypeError("retained_blocks must decode to an integer or None")
        decoded: dict[str, StrainErrorChannels | None] = {}
        for name in ("truncation", "total", "delta_truncation", "delta_total"):
            value = values[name]
            if value is None:
                decoded[name] = None
            elif isinstance(value, Mapping):
                decoded[name] = StrainErrorChannels.from_dict(value)
            else:
                raise TypeError(f"{name} must decode to a mapping or None")
        return cls(
            tail_tolerance=tail,
            physical_radius=radius,
            retained_blocks=blocks,
            omitted_power=omitted,
            truncation=decoded["truncation"],
            total=decoded["total"],
            delta_omitted_power=delta_omitted,
            delta_truncation=decoded["delta_truncation"],
            delta_total=decoded["delta_total"],
        )


@dataclass(frozen=True, slots=True)
class StrainResponsePointDiagnostic(BaseTypedRecord):
    """Retain M1/M2 qualification and approximation channels at one strain."""

    strain_fraction: float
    path_parameter: float
    metric: tuple[tuple[float, ...], ...]
    minimum_parent_bond_length: float
    maximum_parent_bond_length: float
    minimum_hopping_response: float
    maximum_hopping_response: float
    minimum_sampled_external_isolation_gap: float
    minimum_seed_overlap: float
    minimum_frame_overlap_singular_value: float
    maximum_pointwise_frame_alignment_residual: float
    restricted_global_frame_alignment_residual: float
    aligned_strain_perturbation: StrainErrorChannels
    maximum_scalar_strain_component: float
    rms_scalar_strain_component: float
    maximum_traceless_strain_component: float
    rms_traceless_strain_component: float
    delta_onsite_power: float
    delta_offsite_power: float
    interpolation: StrainErrorChannels
    delta_interpolation: StrainErrorChannels
    nyquist_power: float
    delta_nyquist_power: float
    cutoffs: tuple[StrainResponseCutoffDiagnostic, ...]

    def _mapping(self) -> Mapping[str, SerializableValue]:
        return {
            "strain_fraction": self.strain_fraction,
            "path_parameter": self.path_parameter,
            "metric": self.metric,
            "minimum_parent_bond_length": self.minimum_parent_bond_length,
            "maximum_parent_bond_length": self.maximum_parent_bond_length,
            "minimum_hopping_response": self.minimum_hopping_response,
            "maximum_hopping_response": self.maximum_hopping_response,
            "minimum_sampled_external_isolation_gap": (
                self.minimum_sampled_external_isolation_gap
            ),
            "minimum_seed_overlap": self.minimum_seed_overlap,
            "minimum_frame_overlap_singular_value": (
                self.minimum_frame_overlap_singular_value
            ),
            "maximum_pointwise_frame_alignment_residual": (
                self.maximum_pointwise_frame_alignment_residual
            ),
            "restricted_global_frame_alignment_residual": (
                self.restricted_global_frame_alignment_residual
            ),
            "aligned_strain_perturbation": self.aligned_strain_perturbation,
            "maximum_scalar_strain_component": self.maximum_scalar_strain_component,
            "rms_scalar_strain_component": self.rms_scalar_strain_component,
            "maximum_traceless_strain_component": (
                self.maximum_traceless_strain_component
            ),
            "rms_traceless_strain_component": self.rms_traceless_strain_component,
            "delta_onsite_power": self.delta_onsite_power,
            "delta_offsite_power": self.delta_offsite_power,
            "interpolation": self.interpolation,
            "delta_interpolation": self.delta_interpolation,
            "nyquist_power": self.nyquist_power,
            "delta_nyquist_power": self.delta_nyquist_power,
            "cutoffs": self.cutoffs,
        }

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        scalar_names = {
            "strain_fraction",
            "path_parameter",
            "minimum_parent_bond_length",
            "maximum_parent_bond_length",
            "minimum_hopping_response",
            "maximum_hopping_response",
            "minimum_sampled_external_isolation_gap",
            "minimum_seed_overlap",
            "minimum_frame_overlap_singular_value",
            "maximum_pointwise_frame_alignment_residual",
            "restricted_global_frame_alignment_residual",
            "maximum_scalar_strain_component",
            "rms_scalar_strain_component",
            "maximum_traceless_strain_component",
            "rms_traceless_strain_component",
            "delta_onsite_power",
            "delta_offsite_power",
            "nyquist_power",
            "delta_nyquist_power",
        }
        required = scalar_names | {
            "metric",
            "aligned_strain_perturbation",
            "interpolation",
            "delta_interpolation",
            "cutoffs",
        }
        if set(values) != required:
            raise ValueError("strain-response point fields do not match")
        scalars: dict[str, float] = {}
        for name in scalar_names:
            value = values[name]
            if type(value) is not float:
                raise TypeError("strain-response point scalars must decode to floats")
            scalars[name] = value
        metric = values["metric"]
        if not isinstance(metric, tuple) or any(
            not isinstance(row, tuple)
            or any(type(component) is not float for component in row)
            for row in metric
        ):
            raise TypeError("metric must decode to a tuple of float tuples")
        channels: dict[str, StrainErrorChannels] = {}
        for name in (
            "aligned_strain_perturbation",
            "interpolation",
            "delta_interpolation",
        ):
            value = values[name]
            if not isinstance(value, Mapping):
                raise TypeError(f"{name} must decode to a mapping")
            channels[name] = StrainErrorChannels.from_dict(value)
        cutoff_values = values["cutoffs"]
        if not isinstance(cutoff_values, tuple) or any(
            not isinstance(value, Mapping) for value in cutoff_values
        ):
            raise TypeError("cutoffs must decode to a tuple of mappings")
        return cls(
            strain_fraction=scalars["strain_fraction"],
            path_parameter=scalars["path_parameter"],
            metric=metric,
            minimum_parent_bond_length=scalars["minimum_parent_bond_length"],
            maximum_parent_bond_length=scalars["maximum_parent_bond_length"],
            minimum_hopping_response=scalars["minimum_hopping_response"],
            maximum_hopping_response=scalars["maximum_hopping_response"],
            minimum_sampled_external_isolation_gap=scalars[
                "minimum_sampled_external_isolation_gap"
            ],
            minimum_seed_overlap=scalars["minimum_seed_overlap"],
            minimum_frame_overlap_singular_value=scalars[
                "minimum_frame_overlap_singular_value"
            ],
            maximum_pointwise_frame_alignment_residual=scalars[
                "maximum_pointwise_frame_alignment_residual"
            ],
            restricted_global_frame_alignment_residual=scalars[
                "restricted_global_frame_alignment_residual"
            ],
            aligned_strain_perturbation=channels["aligned_strain_perturbation"],
            maximum_scalar_strain_component=scalars["maximum_scalar_strain_component"],
            rms_scalar_strain_component=scalars["rms_scalar_strain_component"],
            maximum_traceless_strain_component=scalars[
                "maximum_traceless_strain_component"
            ],
            rms_traceless_strain_component=scalars["rms_traceless_strain_component"],
            delta_onsite_power=scalars["delta_onsite_power"],
            delta_offsite_power=scalars["delta_offsite_power"],
            interpolation=channels["interpolation"],
            delta_interpolation=channels["delta_interpolation"],
            nyquist_power=scalars["nyquist_power"],
            delta_nyquist_power=scalars["delta_nyquist_power"],
            cutoffs=tuple(
                StrainResponseCutoffDiagnostic.from_dict(value)
                for value in cutoff_values
            ),
        )


@dataclass(frozen=True, slots=True)
class SyntheticStrainResponseResult(BaseTypedRecord):
    """Retain one bounded M1 or M2 strain-response sequence."""

    path: SyntheticStrainPathEnum
    model: StrainResponseModelEnum
    construction_size: int
    evaluation_size: int
    evaluation_shift: float
    maximum_rotation_amplitude: float
    radial_decay_beta: float
    tail_tolerances: tuple[float, ...]
    points: tuple[StrainResponsePointDiagnostic, ...]
    status: str = "bounded-synthetic-strain-response-development-not-retained-evidence"

    def _mapping(self) -> Mapping[str, SerializableValue]:
        return {
            "path": self.path.to_wire(),
            "model": self.model.to_wire(),
            "construction_size": self.construction_size,
            "evaluation_size": self.evaluation_size,
            "evaluation_shift": self.evaluation_shift,
            "maximum_rotation_amplitude": self.maximum_rotation_amplitude,
            "radial_decay_beta": self.radial_decay_beta,
            "tail_tolerances": self.tail_tolerances,
            "points": self.points,
            "status": self.status,
        }

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        required = {
            "path",
            "model",
            "construction_size",
            "evaluation_size",
            "evaluation_shift",
            "maximum_rotation_amplitude",
            "radial_decay_beta",
            "tail_tolerances",
            "points",
            "status",
        }
        if set(values) != required:
            raise ValueError("synthetic-strain response fields do not match")
        path = values["path"]
        model = values["model"]
        construction_size = values["construction_size"]
        evaluation_size = values["evaluation_size"]
        status = values["status"]
        if type(path) is not str or type(model) is not str or type(status) is not str:
            raise TypeError("response labels must decode to strings")
        if type(construction_size) is not int or type(evaluation_size) is not int:
            raise TypeError("response sizes must decode to integers")
        scalars: dict[str, float] = {}
        for name in (
            "evaluation_shift",
            "maximum_rotation_amplitude",
            "radial_decay_beta",
        ):
            value = values[name]
            if type(value) is not float:
                raise TypeError("response controls must decode to floats")
            scalars[name] = value
        tolerances = values["tail_tolerances"]
        points_value = values["points"]
        if not isinstance(tolerances, tuple) or any(
            type(value) is not float for value in tolerances
        ):
            raise TypeError("tail_tolerances must decode to a float tuple")
        if not isinstance(points_value, tuple) or any(
            not isinstance(value, Mapping) for value in points_value
        ):
            raise TypeError("response points must decode to a tuple of mappings")
        return cls(
            path=SyntheticStrainPathEnum.from_wire(path),
            model=StrainResponseModelEnum.from_wire(model),
            construction_size=construction_size,
            evaluation_size=evaluation_size,
            evaluation_shift=scalars["evaluation_shift"],
            maximum_rotation_amplitude=scalars["maximum_rotation_amplitude"],
            radial_decay_beta=scalars["radial_decay_beta"],
            tail_tolerances=tolerances,
            points=tuple(
                StrainResponsePointDiagnostic.from_dict(value) for value in points_value
            ),
            status=status,
        )


@dataclass(frozen=True, slots=True)
class StrainWitnessPointDiagnostic(BaseTypedRecord):
    """Retain sampled representation-witness requirements at one strain."""

    strain_fraction: float
    path_parameter: float
    volume_defect: float
    maximum_direct_band_defect: float
    splitting_scale: float
    finite_mesh_maximum_correlation: float
    pointwise_optimized_operator_threshold: float
    fixed_candidate_operator_threshold: float
    optimized_threshold_over_sqrt_splitting: float
    fixed_candidate_threshold_over_sqrt_splitting: float

    def _mapping(self) -> Mapping[str, SerializableValue]:
        return {
            "strain_fraction": self.strain_fraction,
            "path_parameter": self.path_parameter,
            "volume_defect": self.volume_defect,
            "maximum_direct_band_defect": self.maximum_direct_band_defect,
            "splitting_scale": self.splitting_scale,
            "finite_mesh_maximum_correlation": self.finite_mesh_maximum_correlation,
            "pointwise_optimized_operator_threshold": (
                self.pointwise_optimized_operator_threshold
            ),
            "fixed_candidate_operator_threshold": (
                self.fixed_candidate_operator_threshold
            ),
            "optimized_threshold_over_sqrt_splitting": (
                self.optimized_threshold_over_sqrt_splitting
            ),
            "fixed_candidate_threshold_over_sqrt_splitting": (
                self.fixed_candidate_threshold_over_sqrt_splitting
            ),
        }

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        required = {
            "strain_fraction",
            "path_parameter",
            "volume_defect",
            "maximum_direct_band_defect",
            "splitting_scale",
            "finite_mesh_maximum_correlation",
            "pointwise_optimized_operator_threshold",
            "fixed_candidate_operator_threshold",
            "optimized_threshold_over_sqrt_splitting",
            "fixed_candidate_threshold_over_sqrt_splitting",
        }
        if set(values) != required:
            raise ValueError("strain-witness point fields do not match")
        scalars: dict[str, float] = {}
        for name in required:
            value = values[name]
            if type(value) is not float:
                raise TypeError("strain-witness point values must decode to floats")
            scalars[name] = value
        return cls(**scalars)


@dataclass(frozen=True, slots=True)
class SyntheticStrainWitnessScanResult(BaseTypedRecord):
    """Retain one sampled strain-witness requirement envelope."""

    path: SyntheticStrainPathEnum
    control: StrainWitnessControlEnum
    construction_size: int
    maximum_rotation_amplitude: float
    radial_decay_beta: float
    points: tuple[StrainWitnessPointDiagnostic, ...]
    sampled_maximum_optimized_operator_threshold: float
    sampled_maximum_fixed_candidate_operator_threshold: float
    status: str = "sampled-development-scan-not-continuum-certificate"

    def _mapping(self) -> Mapping[str, SerializableValue]:
        return {
            "path": self.path.to_wire(),
            "control": self.control.to_wire(),
            "construction_size": self.construction_size,
            "maximum_rotation_amplitude": self.maximum_rotation_amplitude,
            "radial_decay_beta": self.radial_decay_beta,
            "points": self.points,
            "sampled_maximum_optimized_operator_threshold": (
                self.sampled_maximum_optimized_operator_threshold
            ),
            "sampled_maximum_fixed_candidate_operator_threshold": (
                self.sampled_maximum_fixed_candidate_operator_threshold
            ),
            "status": self.status,
        }

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        required = {
            "path",
            "control",
            "construction_size",
            "maximum_rotation_amplitude",
            "radial_decay_beta",
            "points",
            "sampled_maximum_optimized_operator_threshold",
            "sampled_maximum_fixed_candidate_operator_threshold",
            "status",
        }
        if set(values) != required:
            raise ValueError("synthetic-strain witness fields do not match")
        path = values["path"]
        control = values["control"]
        size = values["construction_size"]
        status = values["status"]
        if type(path) is not str or type(control) is not str or type(status) is not str:
            raise TypeError("witness labels must decode to strings")
        if type(size) is not int:
            raise TypeError("construction_size must decode to an integer")
        scalars: dict[str, float] = {}
        for name in (
            "maximum_rotation_amplitude",
            "radial_decay_beta",
            "sampled_maximum_optimized_operator_threshold",
            "sampled_maximum_fixed_candidate_operator_threshold",
        ):
            value = values[name]
            if type(value) is not float:
                raise TypeError("witness scalars must decode to floats")
            scalars[name] = value
        points_value = values["points"]
        if not isinstance(points_value, tuple) or any(
            not isinstance(value, Mapping) for value in points_value
        ):
            raise TypeError("witness points must decode to a tuple of mappings")
        return cls(
            path=SyntheticStrainPathEnum.from_wire(path),
            control=StrainWitnessControlEnum.from_wire(control),
            construction_size=size,
            maximum_rotation_amplitude=scalars["maximum_rotation_amplitude"],
            radial_decay_beta=scalars["radial_decay_beta"],
            points=tuple(
                StrainWitnessPointDiagnostic.from_dict(value) for value in points_value
            ),
            sampled_maximum_optimized_operator_threshold=scalars[
                "sampled_maximum_optimized_operator_threshold"
            ],
            sampled_maximum_fixed_candidate_operator_threshold=scalars[
                "sampled_maximum_fixed_candidate_operator_threshold"
            ],
            status=status,
        )


def _coordinate_axis(size: int, offset: float) -> FloatArray:
    return np.asarray(
        -0.5 + (np.arange(size, dtype=np.float64) + offset) / float(size),
        dtype=np.float64,
    )


def _coordinates(size: int, dimension: int, offset: float) -> FloatArray:
    axis = _coordinate_axis(size, offset)
    return np.stack(np.meshgrid(*(axis,) * dimension, indexing="ij"), axis=-1)


def _hopping_responses(
    path: SyntheticStrainPathEnum,
    model: StrainResponseModelEnum,
    fraction: float,
    beta: float,
) -> FloatArray:
    count = path.spatial_dimension + 1
    if model is StrainResponseModelEnum.M1_FROZEN:
        return np.ones(count, dtype=np.float64)
    reference = path.bond_lengths(path.metric(0.0))
    strained = path.bond_lengths(path.metric(fraction))
    return np.exp(-beta * (strained / reference - 1.0))


def _parent_field(
    path: SyntheticStrainPathEnum,
    coordinates: FloatArray,
    responses: FloatArray,
) -> ComplexArray:
    translations = path.parent_translations().astype(np.float64)
    arguments = np.einsum("...d,bd->...b", coordinates, translations)
    gamma = np.sum(responses * np.exp(-2.0j * np.pi * arguments), axis=-1) / float(
        len(translations)
    )
    shape = coordinates.shape[:-1]
    sublattice = np.empty((*shape, 2, 2), dtype=np.complex128)
    sublattice[..., 0, 0] = 0.0
    sublattice[..., 0, 1] = gamma
    sublattice[..., 1, 0] = gamma.conjugate()
    sublattice[..., 1, 1] = 0.0
    result = np.zeros((*shape, 4, 4), dtype=np.complex128)
    identity = np.eye(2, dtype=np.complex128)
    result[..., :2, :2] = -1.20 * identity + 0.30 * sublattice
    result[..., 2:, 2:] = 1.20 * identity + 0.10 * sublattice
    result[..., :2, 2:] = 0.08 * identity
    result[..., 2:, :2] = 0.08 * identity
    return result


def _retained_frame(
    parent: ComplexArray,
) -> tuple[ComplexArray, FloatArray, FloatArray]:
    eigenvalues, eigenvectors = np.linalg.eigh(parent)
    low = eigenvectors[..., :, :2]
    projector = low @ np.swapaxes(low.conjugate(), -1, -2)
    projected_seed = projector @ _SEED
    gram = np.swapaxes(projected_seed.conjugate(), -1, -2) @ projected_seed
    gram_values, gram_vectors = np.linalg.eigh(gram)
    inverse_root = (
        gram_vectors * (1.0 / np.sqrt(gram_values))[..., None, :]
    ) @ np.swapaxes(gram_vectors.conjugate(), -1, -2)
    return projected_seed @ inverse_root, eigenvalues, gram_values


def _retained_field(frame: ComplexArray, parent: ComplexArray) -> ComplexArray:
    return np.swapaxes(frame.conjugate(), -1, -2) @ parent @ frame


def _gauge_rotations(
    path: SyntheticStrainPathEnum, coordinates: FloatArray, amplitude: float
) -> ComplexArray:
    bonds = path.rotation_bonds().astype(np.float64)
    arguments = np.einsum("...d,bd->...b", coordinates, bonds)
    angles = amplitude * np.mean(np.sin(2.0 * np.pi * arguments), axis=-1)
    result = np.empty((*angles.shape, 2, 2), dtype=np.complex128)
    result[..., 0, 0] = np.cos(angles)
    result[..., 0, 1] = -np.sin(angles)
    result[..., 1, 0] = np.sin(angles)
    result[..., 1, 1] = np.cos(angles)
    return result


def _pointwise_alignment(
    moving: ComplexArray, reference: ComplexArray
) -> tuple[ComplexArray, float, float]:
    overlaps = np.swapaxes(moving.conjugate(), -1, -2) @ reference
    left, singular, right = np.linalg.svd(overlaps)
    unitaries = left @ right
    aligned = moving @ unitaries
    residual = float(np.max(np.linalg.norm(aligned - reference, axis=(-2, -1))))
    return unitaries, float(np.min(singular)), residual


def _global_alignment_residual(moving: ComplexArray, reference: ComplexArray) -> float:
    overlaps = np.swapaxes(moving.conjugate(), -1, -2) @ reference
    aggregate = np.sum(overlaps.reshape((-1, 2, 2)), axis=0)
    left, _, right = np.linalg.svd(aggregate)
    unitary = left @ right
    difference = moving @ unitary - reference
    return float(np.sqrt(np.mean(np.sum(np.abs(difference) ** 2, axis=(-2, -1))) / 2.0))


def _aligned_attacked_field(
    retained: ComplexArray, alignment: ComplexArray, rotations: ComplexArray
) -> ComplexArray:
    aligned = np.swapaxes(alignment.conjugate(), -1, -2) @ retained @ alignment
    return np.swapaxes(rotations.conjugate(), -1, -2) @ aligned @ rotations


def _errors(approximation: ComplexArray, direct: ComplexArray) -> StrainErrorChannels:
    difference = approximation - direct
    matrix = np.linalg.norm(difference, axis=(-2, -1)) / math.sqrt(2.0)
    band = np.abs(np.linalg.eigvalsh(approximation) - np.linalg.eigvalsh(direct))
    return StrainErrorChannels(
        maximum_hamiltonian=float(np.max(matrix)),
        rms_hamiltonian=float(np.sqrt(np.mean(matrix**2))),
        maximum_band=float(np.max(band)),
        rms_band=float(np.sqrt(np.mean(band**2))),
    )


def _powers(blocks: ComplexArray) -> FloatArray:
    return np.sum(np.abs(blocks) ** 2, axis=(-2, -1)) / 2.0


def _select_support(
    squared_radii: FloatArray,
    powers: FloatArray,
    nyquist_power: float,
    tolerance: float,
) -> tuple[BoolArray | None, float | None, int | None, float]:
    order = np.argsort(squared_radii, kind="stable")
    radii = squared_radii[order]
    ordered_power = powers[order]
    total = float(np.sum(powers)) + nyquist_power
    retained = 0.0
    index = 0
    while index < len(radii):
        radius = float(radii[index])
        stop = index + 1
        tie = 1.0e-12 * max(1.0, abs(radius))
        while stop < len(radii) and abs(float(radii[stop]) - radius) <= tie:
            stop += 1
        retained += float(np.sum(ordered_power[index:stop]))
        omitted = max(nyquist_power, total - retained)
        if omitted <= tolerance:
            support = squared_radii <= radius + tie
            return (
                support,
                math.sqrt(max(0.0, radius)),
                int(np.count_nonzero(support)),
                omitted,
            )
        index = stop
    return None, None, None, total


def _validate_definition(
    path: SyntheticStrainPathEnum,
    model: StrainResponseModelEnum,
    construction_size: int,
    evaluation_size: int,
    evaluation_shift: float,
    strain_fractions: tuple[float, ...],
    amplitude: float,
    beta: float,
    tail_tolerances: tuple[float, ...],
) -> None:
    if type(path) is not SyntheticStrainPathEnum:
        raise TypeError("path must be SyntheticStrainPathEnum")
    if type(model) is not StrainResponseModelEnum:
        raise TypeError("model must be StrainResponseModelEnum")
    if (
        type(construction_size) is not int
        or construction_size < 4
        or construction_size % 2
    ):
        raise ValueError(
            "construction_size must be an even built-in integer at least four"
        )
    if type(evaluation_size) is not int or evaluation_size < 3:
        raise ValueError("evaluation_size must be a built-in integer at least three")
    if type(evaluation_shift) is not float or not 0.0 < evaluation_shift < 1.0:
        raise ValueError("evaluation_shift must be a built-in float in (0, 1)")
    if not strain_fractions or strain_fractions != tuple(sorted(set(strain_fractions))):
        raise ValueError("strain_fractions must be nonempty, sorted, and unique")
    if any(
        type(value) is not float or not 0.0 <= value <= 1.0
        for value in strain_fractions
    ):
        raise ValueError("strain fractions must be built-in floats in [0, 1]")
    if type(amplitude) is not float or not 0.0 <= amplitude <= math.pi / 4.0:
        raise ValueError("amplitude must be a built-in float in [0, pi/4]")
    if type(beta) is not float or beta < 0.0:
        raise ValueError("beta must be a nonnegative built-in float")
    if model is StrainResponseModelEnum.M1_FROZEN and beta != 0.0:
        raise ValueError("M1 requires beta=0")
    if model is StrainResponseModelEnum.M2_RADIAL and beta != 1.0:
        raise ValueError("the frozen M2 development contract requires beta=1")
    if not tail_tolerances or any(
        type(value) is not float or value <= 0.0 for value in tail_tolerances
    ):
        raise ValueError("tail tolerances must be positive built-in floats")


def calculate_synthetic_strain_response(
    path: SyntheticStrainPathEnum,
    model: StrainResponseModelEnum,
    construction_size: int,
    evaluation_size: int,
    evaluation_shift: float,
    strain_fractions: tuple[float, ...],
    maximum_rotation_amplitude: float,
    radial_decay_beta: float,
    tail_tolerances: tuple[float, ...],
) -> SyntheticStrainResponseResult:
    """Calculate one bounded M1 or M2 synthetic strain-response sequence."""
    _validate_definition(
        path,
        model,
        construction_size,
        evaluation_size,
        evaluation_shift,
        strain_fractions,
        maximum_rotation_amplitude,
        radial_decay_beta,
        tail_tolerances,
    )
    dimension = path.spatial_dimension
    construction = _coordinates(construction_size, dimension, 0.5)
    evaluation = _coordinates(evaluation_size, dimension, 0.5 + evaluation_shift)
    source_mesh = CenteredUniformMesh(
        dimension,
        construction_size,
        (0.5,) * dimension,
    )
    evaluation_axis = _coordinate_axis(
        evaluation_size,
        0.5 + evaluation_shift,
    )
    evaluation_axes = (evaluation_axis,) * dimension
    rotations = _gauge_rotations(path, construction, maximum_rotation_amplitude)
    rotations_eval = _gauge_rotations(path, evaluation, maximum_rotation_amplitude)

    reference_responses = _hopping_responses(path, model, 0.0, radial_decay_beta)
    reference_parent = _parent_field(path, construction, reference_responses)
    reference_frame, _, _ = _retained_frame(reference_parent)
    reference_retained = _retained_field(reference_frame, reference_parent)
    reference_attacked = (
        np.swapaxes(rotations.conjugate(), -1, -2) @ reference_retained @ rotations
    )
    reference_parent_eval = _parent_field(path, evaluation, reference_responses)
    reference_frame_eval, _, _ = _retained_frame(reference_parent_eval)
    reference_retained_eval = _retained_field(
        reference_frame_eval, reference_parent_eval
    )
    reference_attacked_eval = (
        np.swapaxes(rotations_eval.conjugate(), -1, -2)
        @ reference_retained_eval
        @ rotations_eval
    )

    points: list[StrainResponsePointDiagnostic] = []
    for fraction in strain_fractions:
        metric = path.metric(fraction)
        responses = _hopping_responses(path, model, fraction, radial_decay_beta)
        parent = _parent_field(path, construction, responses)
        frame, eigenvalues, seed_values = _retained_frame(parent)
        retained = _retained_field(frame, parent)
        alignment, minimum_singular, pointwise_residual = _pointwise_alignment(
            frame, reference_frame
        )
        attacked = _aligned_attacked_field(retained, alignment, rotations)

        parent_eval = _parent_field(path, evaluation, responses)
        frame_eval, _, _ = _retained_frame(parent_eval)
        retained_eval = _retained_field(frame_eval, parent_eval)
        alignment_eval, _, _ = _pointwise_alignment(frame_eval, reference_frame_eval)
        attacked_eval = _aligned_attacked_field(
            retained_eval, alignment_eval, rotations_eval
        )
        delta = attacked - reference_attacked
        delta_eval = attacked_eval - reference_attacked_eval

        attacked_transform = NumpyCenteredUniformMeshMatrixFourierTransformer(
            definition=NumpyCenteredUniformMeshMatrixFourierTransformDefinition.from_array(
                source_mesh,
                attacked,
            )
        ).result()
        delta_transform = NumpyCenteredUniformMeshMatrixFourierTransformer(
            definition=NumpyCenteredUniformMeshMatrixFourierTransformDefinition.from_array(
                source_mesh,
                delta,
            )
        ).result()
        displacements = attacked_transform.series.integer_modes
        blocks = attacked_transform.series.matrix_coefficients
        delta_displacements = delta_transform.series.integer_modes
        delta_blocks = delta_transform.series.matrix_coefficients
        if not np.array_equal(displacements, delta_displacements):
            raise RuntimeError("Hamiltonian and strain-difference inventories differ")
        nyquist = np.any(displacements == -construction_size // 2, axis=1)
        ordinary_displacements = displacements[~nyquist]
        ordinary_blocks = blocks[~nyquist]
        ordinary_delta_blocks = delta_blocks[~nyquist]
        power = _powers(ordinary_blocks)
        delta_power = _powers(ordinary_delta_blocks)
        onsite = np.all(ordinary_displacements == 0, axis=1)
        nyquist_power = float(np.sum(_powers(blocks[nyquist])))
        delta_nyquist_power = float(np.sum(_powers(delta_blocks[nyquist])))
        ordinary_series = NumpyFiniteFourierMatrixSeries.from_arrays(
            dimension,
            ordinary_displacements,
            ordinary_blocks,
        )
        ordinary_delta_series = NumpyFiniteFourierMatrixSeries.from_arrays(
            dimension,
            ordinary_displacements,
            ordinary_delta_blocks,
        )
        full_eval = (
            NumpyTensorProductFourierMatrixSeriesEvaluator(
                definition=NumpyTensorProductFourierMatrixEvaluationDefinition.from_arrays(
                    source_mesh,
                    ordinary_series,
                    evaluation_axes,
                )
            )
            .result()
            .matrix_values
        )
        full_delta_eval = (
            NumpyTensorProductFourierMatrixSeriesEvaluator(
                definition=NumpyTensorProductFourierMatrixEvaluationDefinition.from_arrays(
                    source_mesh,
                    ordinary_delta_series,
                    evaluation_axes,
                )
            )
            .result()
            .matrix_values
        )
        interpolation = _errors(full_eval, attacked_eval)
        delta_interpolation = _errors(full_delta_eval, delta_eval)
        squared_radii = np.einsum(
            "ri,ij,rj->r", ordinary_displacements, metric, ordinary_displacements
        )

        cutoffs: list[StrainResponseCutoffDiagnostic] = []
        for tolerance in tail_tolerances:
            support, radius, count, omitted = _select_support(
                squared_radii, power, nyquist_power, tolerance
            )
            if support is None:
                cutoffs.append(
                    StrainResponseCutoffDiagnostic(
                        tail_tolerance=tolerance,
                        physical_radius=None,
                        retained_blocks=None,
                        omitted_power=omitted,
                        truncation=None,
                        total=None,
                        delta_omitted_power=float(np.sum(delta_power))
                        + delta_nyquist_power,
                        delta_truncation=None,
                        delta_total=None,
                    )
                )
                continue
            truncated_series = NumpyFiniteFourierMatrixSeries.from_arrays(
                dimension,
                ordinary_displacements[support],
                ordinary_blocks[support],
            )
            truncated_delta_series = NumpyFiniteFourierMatrixSeries.from_arrays(
                dimension,
                ordinary_displacements[support],
                ordinary_delta_blocks[support],
            )
            truncated_eval = (
                NumpyTensorProductFourierMatrixSeriesEvaluator(
                    definition=NumpyTensorProductFourierMatrixEvaluationDefinition.from_arrays(
                        source_mesh,
                        truncated_series,
                        evaluation_axes,
                    )
                )
                .result()
                .matrix_values
            )
            truncated_delta_eval = (
                NumpyTensorProductFourierMatrixSeriesEvaluator(
                    definition=NumpyTensorProductFourierMatrixEvaluationDefinition.from_arrays(
                        source_mesh,
                        truncated_delta_series,
                        evaluation_axes,
                    )
                )
                .result()
                .matrix_values
            )
            delta_omitted = float(np.sum(delta_power[~support])) + delta_nyquist_power
            cutoffs.append(
                StrainResponseCutoffDiagnostic(
                    tail_tolerance=tolerance,
                    physical_radius=radius,
                    retained_blocks=count,
                    omitted_power=omitted,
                    truncation=_errors(truncated_eval, full_eval),
                    total=_errors(truncated_eval, attacked_eval),
                    delta_omitted_power=delta_omitted,
                    delta_truncation=_errors(truncated_delta_eval, full_delta_eval),
                    delta_total=_errors(truncated_delta_eval, delta_eval),
                )
            )

        trace = np.trace(delta_eval, axis1=-2, axis2=-1) / 2.0
        traceless = delta_eval - trace[..., None, None] * np.eye(2, dtype=np.complex128)
        scalar_magnitude = np.abs(trace)
        traceless_magnitude = np.linalg.norm(traceless, axis=(-2, -1)) / math.sqrt(2.0)
        lengths = path.bond_lengths(metric)
        points.append(
            StrainResponsePointDiagnostic(
                strain_fraction=fraction,
                path_parameter=path.path_parameter(fraction),
                metric=tuple(tuple(float(value) for value in row) for row in metric),
                minimum_parent_bond_length=float(np.min(lengths)),
                maximum_parent_bond_length=float(np.max(lengths)),
                minimum_hopping_response=float(np.min(responses)),
                maximum_hopping_response=float(np.max(responses)),
                minimum_sampled_external_isolation_gap=float(
                    np.min(eigenvalues[..., 2] - eigenvalues[..., 1])
                ),
                minimum_seed_overlap=float(np.min(seed_values)),
                minimum_frame_overlap_singular_value=minimum_singular,
                maximum_pointwise_frame_alignment_residual=pointwise_residual,
                restricted_global_frame_alignment_residual=_global_alignment_residual(
                    frame, reference_frame
                ),
                aligned_strain_perturbation=_errors(
                    attacked_eval, reference_attacked_eval
                ),
                maximum_scalar_strain_component=float(np.max(scalar_magnitude)),
                rms_scalar_strain_component=float(
                    np.sqrt(np.mean(scalar_magnitude**2))
                ),
                maximum_traceless_strain_component=float(np.max(traceless_magnitude)),
                rms_traceless_strain_component=float(
                    np.sqrt(np.mean(traceless_magnitude**2))
                ),
                delta_onsite_power=float(np.sum(delta_power[onsite])),
                delta_offsite_power=float(np.sum(delta_power[~onsite]))
                + delta_nyquist_power,
                interpolation=interpolation,
                delta_interpolation=delta_interpolation,
                nyquist_power=nyquist_power,
                delta_nyquist_power=delta_nyquist_power,
                cutoffs=tuple(cutoffs),
            )
        )
    return SyntheticStrainResponseResult(
        path=path,
        model=model,
        construction_size=construction_size,
        evaluation_size=evaluation_size,
        evaluation_shift=evaluation_shift,
        maximum_rotation_amplitude=maximum_rotation_amplitude,
        radial_decay_beta=radial_decay_beta,
        tail_tolerances=tail_tolerances,
        points=tuple(points),
    )


def calculate_strain_witness_scan(
    path: SyntheticStrainPathEnum,
    control: StrainWitnessControlEnum,
    construction_size: int,
    strain_fractions: tuple[float, ...],
    maximum_rotation_amplitude: float,
) -> SyntheticStrainWitnessScanResult:
    """Scan sampled representation-witness requirements along one strain path."""
    if type(path) is not SyntheticStrainPathEnum:
        raise TypeError("path must be SyntheticStrainPathEnum")
    if type(control) is not StrainWitnessControlEnum:
        raise TypeError("control must be StrainWitnessControlEnum")
    if (
        type(construction_size) is not int
        or construction_size < 4
        or construction_size % 2
    ):
        raise ValueError(
            "construction_size must be an even built-in integer at least four"
        )
    if not strain_fractions or strain_fractions != tuple(sorted(set(strain_fractions))):
        raise ValueError("strain_fractions must be nonempty, sorted, and unique")
    if any(
        type(value) is not float or not 0.0 <= value <= 1.0
        for value in strain_fractions
    ):
        raise ValueError("strain fractions must be built-in floats in [0, 1]")
    if (
        type(maximum_rotation_amplitude) is not float
        or not 0.0 <= maximum_rotation_amplitude <= math.pi / 4.0
    ):
        raise ValueError("maximum_rotation_amplitude must be a float in [0, pi/4]")

    dimension = path.spatial_dimension
    coordinates = _coordinates(construction_size, dimension, 0.5)
    rotations = _gauge_rotations(path, coordinates, maximum_rotation_amplitude)
    constant_parent = np.broadcast_to(
        np.diag(np.asarray((1.0, -1.0), dtype=np.complex128)),
        (*coordinates.shape[:-1], 2, 2),
    ).copy()
    response_model = (
        StrainResponseModelEnum.M1_FROZEN
        if control is StrainWitnessControlEnum.FROZEN_PARENT
        else StrainResponseModelEnum.M2_RADIAL
    )
    radial_beta = 1.0 if control is StrainWitnessControlEnum.RADIAL_RESPONSE else 0.0

    points: list[StrainWitnessPointDiagnostic] = []
    for fraction in strain_fractions:
        metric = path.metric(fraction)
        if control is StrainWitnessControlEnum.GEOMETRY_ONLY:
            reference = constant_parent
        else:
            responses = _hopping_responses(
                path,
                response_model,
                fraction,
                radial_beta,
            )
            parent = _parent_field(path, coordinates, responses)
            frame, _, _ = _retained_frame(parent)
            reference = _retained_field(frame, parent)
        comparison = np.swapaxes(rotations.conjugate(), -1, -2) @ reference @ rotations
        (
            _,
            _,
            splitting_scale,
            correlation,
            optimized_threshold,
            reference_threshold,
        ) = restricted_alignment(reference, comparison)
        if correlation is None or splitting_scale <= 0.0:
            raise RuntimeError(
                "strain witness scan requires nonzero retained splitting"
            )
        root_splitting = math.sqrt(splitting_scale)
        points.append(
            StrainWitnessPointDiagnostic(
                strain_fraction=fraction,
                path_parameter=path.path_parameter(fraction),
                volume_defect=abs(float(np.linalg.det(metric)) - 1.0),
                maximum_direct_band_defect=float(
                    np.max(
                        np.abs(
                            np.linalg.eigvalsh(reference)
                            - np.linalg.eigvalsh(comparison)
                        )
                    )
                ),
                splitting_scale=splitting_scale,
                finite_mesh_maximum_correlation=correlation,
                pointwise_optimized_operator_threshold=optimized_threshold,
                fixed_candidate_operator_threshold=reference_threshold,
                optimized_threshold_over_sqrt_splitting=(
                    optimized_threshold / root_splitting
                ),
                fixed_candidate_threshold_over_sqrt_splitting=(
                    reference_threshold / root_splitting
                ),
            )
        )
    immutable_points = tuple(points)
    return SyntheticStrainWitnessScanResult(
        path=path,
        control=control,
        construction_size=construction_size,
        maximum_rotation_amplitude=maximum_rotation_amplitude,
        radial_decay_beta=radial_beta,
        points=immutable_points,
        sampled_maximum_optimized_operator_threshold=max(
            point.pointwise_optimized_operator_threshold for point in immutable_points
        ),
        sampled_maximum_fixed_candidate_operator_threshold=max(
            point.fixed_candidate_operator_threshold for point in immutable_points
        ),
    )


__all__ = [
    "StrainErrorChannels",
    "StrainResponseCutoffDiagnostic",
    "StrainResponseModelEnum",
    "StrainResponsePointDiagnostic",
    "StrainWitnessControlEnum",
    "StrainWitnessPointDiagnostic",
    "SyntheticStrainResponseResult",
    "SyntheticStrainWitnessScanResult",
    "calculate_strain_witness_scan",
    "calculate_synthetic_strain_response",
]
