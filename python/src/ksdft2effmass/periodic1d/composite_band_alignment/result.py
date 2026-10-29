"""Typed result records for direct rank-two composite-band alignment."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from math import isfinite
from typing import ClassVar, Self

from projectkoios.physkit.units import (
    ComplexMatrixQuantity,
    MatrixQuantity,
    ScalarQuantity,
    Unitless,
)

from ksdft2effmass.serialization import BaseTypedRecord, SerializableValue

from .configuration import Periodic1DCompositeBandAlignmentConfiguration


@dataclass(frozen=True, slots=True)
class Periodic1DCompositeBandAlignmentDiagnostics(BaseTypedRecord):
    """Retain finite gap, transport, alignment, and operator diagnostics."""

    minimum_sampled_gap: ScalarQuantity
    minimum_overlap_singular_value: float
    closure_eigenphases: tuple[float, ...]
    attack_frame_maximum_frobenius_defect: float
    pointwise_frame_maximum_frobenius_defect: float
    pointwise_projector_maximum_frobenius_defect: float
    pointwise_rotation_recovery_maximum_frobenius_defect: float
    global_frame_maximum_frobenius_defect: float
    attacked_operator_maximum_frobenius_defect: ScalarQuantity
    pointwise_operator_maximum_frobenius_defect: ScalarQuantity
    global_operator_maximum_frobenius_defect: ScalarQuantity
    pointwise_minimum_cross_singular_value: float
    global_minimum_cross_singular_value: float
    pointwise_maximum_rank_cutoff: float
    global_rank_cutoff: float

    def __post_init__(self) -> None:
        """Validate scalar types, units, and nonnegative finite diagnostics."""
        for value, name in (
            (self.minimum_sampled_gap, "minimum_sampled_gap"),
            (
                self.attacked_operator_maximum_frobenius_defect,
                "attacked_operator_maximum_frobenius_defect",
            ),
            (
                self.pointwise_operator_maximum_frobenius_defect,
                "pointwise_operator_maximum_frobenius_defect",
            ),
            (
                self.global_operator_maximum_frobenius_defect,
                "global_operator_maximum_frobenius_defect",
            ),
        ):
            if type(value) is not ScalarQuantity or not isinstance(
                value.unit, Unitless
            ):
                raise TypeError(f"{name} must be a unitless ScalarQuantity")
            if not isfinite(value.magnitude) or value.magnitude < 0.0:
                raise ValueError(f"{name} must be finite and nonnegative")
        if (
            not isinstance(self.closure_eigenphases, tuple)
            or len(self.closure_eigenphases) != 2
        ):
            raise ValueError("closure_eigenphases must contain the rank-two inventory")
        numerical = (
            (self.minimum_overlap_singular_value, "minimum_overlap_singular_value"),
            (
                self.attack_frame_maximum_frobenius_defect,
                "attack_frame_maximum_frobenius_defect",
            ),
            (
                self.pointwise_frame_maximum_frobenius_defect,
                "pointwise_frame_maximum_frobenius_defect",
            ),
            (
                self.pointwise_projector_maximum_frobenius_defect,
                "pointwise_projector_maximum_frobenius_defect",
            ),
            (
                self.pointwise_rotation_recovery_maximum_frobenius_defect,
                "pointwise_rotation_recovery_maximum_frobenius_defect",
            ),
            (
                self.global_frame_maximum_frobenius_defect,
                "global_frame_maximum_frobenius_defect",
            ),
            (
                self.pointwise_minimum_cross_singular_value,
                "pointwise_minimum_cross_singular_value",
            ),
            (
                self.global_minimum_cross_singular_value,
                "global_minimum_cross_singular_value",
            ),
            (self.pointwise_maximum_rank_cutoff, "pointwise_maximum_rank_cutoff"),
            (self.global_rank_cutoff, "global_rank_cutoff"),
        )
        for scalar, name in numerical:
            if type(scalar) is not float or not isfinite(scalar):
                raise TypeError(f"{name} must be a finite built-in float")
            if scalar < 0.0:
                raise ValueError(f"{name} must be nonnegative")
        if any(
            type(value) is not float or not isfinite(value)
            for value in self.closure_eigenphases
        ):
            raise TypeError("closure_eigenphases must contain finite built-in floats")

    def _mapping(self) -> Mapping[str, SerializableValue]:
        return {
            "minimum_sampled_gap": self.minimum_sampled_gap,
            "minimum_overlap_singular_value": self.minimum_overlap_singular_value,
            "closure_eigenphases": self.closure_eigenphases,
            "attack_frame_maximum_frobenius_defect": (
                self.attack_frame_maximum_frobenius_defect
            ),
            "pointwise_frame_maximum_frobenius_defect": (
                self.pointwise_frame_maximum_frobenius_defect
            ),
            "pointwise_projector_maximum_frobenius_defect": (
                self.pointwise_projector_maximum_frobenius_defect
            ),
            "pointwise_rotation_recovery_maximum_frobenius_defect": (
                self.pointwise_rotation_recovery_maximum_frobenius_defect
            ),
            "global_frame_maximum_frobenius_defect": (
                self.global_frame_maximum_frobenius_defect
            ),
            "attacked_operator_maximum_frobenius_defect": (
                self.attacked_operator_maximum_frobenius_defect
            ),
            "pointwise_operator_maximum_frobenius_defect": (
                self.pointwise_operator_maximum_frobenius_defect
            ),
            "global_operator_maximum_frobenius_defect": (
                self.global_operator_maximum_frobenius_defect
            ),
            "pointwise_minimum_cross_singular_value": (
                self.pointwise_minimum_cross_singular_value
            ),
            "global_minimum_cross_singular_value": (
                self.global_minimum_cross_singular_value
            ),
            "pointwise_maximum_rank_cutoff": self.pointwise_maximum_rank_cutoff,
            "global_rank_cutoff": self.global_rank_cutoff,
        }

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        required = {
            "minimum_sampled_gap",
            "minimum_overlap_singular_value",
            "closure_eigenphases",
            "attack_frame_maximum_frobenius_defect",
            "pointwise_frame_maximum_frobenius_defect",
            "pointwise_projector_maximum_frobenius_defect",
            "pointwise_rotation_recovery_maximum_frobenius_defect",
            "global_frame_maximum_frobenius_defect",
            "attacked_operator_maximum_frobenius_defect",
            "pointwise_operator_maximum_frobenius_defect",
            "global_operator_maximum_frobenius_defect",
            "pointwise_minimum_cross_singular_value",
            "global_minimum_cross_singular_value",
            "pointwise_maximum_rank_cutoff",
            "global_rank_cutoff",
        }
        if set(values) != required:
            raise ValueError("composite-band diagnostic fields do not match")
        scalar_names = (
            "minimum_sampled_gap",
            "attacked_operator_maximum_frobenius_defect",
            "pointwise_operator_maximum_frobenius_defect",
            "global_operator_maximum_frobenius_defect",
        )
        scalars: dict[str, ScalarQuantity] = {}
        for name in scalar_names:
            value = values[name]
            if type(value) is not ScalarQuantity:
                raise TypeError(f"{name} must decode to ScalarQuantity")
            scalars[name] = value
        phases = values["closure_eigenphases"]
        if not isinstance(phases, tuple):
            raise TypeError("closure_eigenphases must decode to a tuple")
        float_names = tuple(
            required.difference(scalar_names).difference({"closure_eigenphases"})
        )
        floats: dict[str, float] = {}
        for name in float_names:
            value = values[name]
            if type(value) is not float:
                raise TypeError(f"{name} must decode to a built-in float")
            floats[name] = value
        return cls(
            minimum_sampled_gap=scalars["minimum_sampled_gap"],
            minimum_overlap_singular_value=floats["minimum_overlap_singular_value"],
            closure_eigenphases=tuple(phases),
            attack_frame_maximum_frobenius_defect=floats[
                "attack_frame_maximum_frobenius_defect"
            ],
            pointwise_frame_maximum_frobenius_defect=floats[
                "pointwise_frame_maximum_frobenius_defect"
            ],
            pointwise_projector_maximum_frobenius_defect=floats[
                "pointwise_projector_maximum_frobenius_defect"
            ],
            pointwise_rotation_recovery_maximum_frobenius_defect=floats[
                "pointwise_rotation_recovery_maximum_frobenius_defect"
            ],
            global_frame_maximum_frobenius_defect=floats[
                "global_frame_maximum_frobenius_defect"
            ],
            attacked_operator_maximum_frobenius_defect=scalars[
                "attacked_operator_maximum_frobenius_defect"
            ],
            pointwise_operator_maximum_frobenius_defect=scalars[
                "pointwise_operator_maximum_frobenius_defect"
            ],
            global_operator_maximum_frobenius_defect=scalars[
                "global_operator_maximum_frobenius_defect"
            ],
            pointwise_minimum_cross_singular_value=floats[
                "pointwise_minimum_cross_singular_value"
            ],
            global_minimum_cross_singular_value=floats[
                "global_minimum_cross_singular_value"
            ],
            pointwise_maximum_rank_cutoff=floats["pointwise_maximum_rank_cutoff"],
            global_rank_cutoff=floats["global_rank_cutoff"],
        )


@dataclass(frozen=True, slots=True)
class Periodic1DCompositeBandAlignmentTransformResult(BaseTypedRecord):
    """Retain a cyclic transform and its ordinary-lattice conversion channels."""

    channel: str
    representatives: tuple[int, ...]
    hopping_blocks: tuple[ComplexMatrixQuantity, ...]
    ordinary_representatives: tuple[int, ...]
    cyclic_conversion_representative: int
    cyclic_conversion_power: ScalarQuantity
    reconstruction_maximum_frobenius_error: ScalarQuantity
    hermiticity_maximum_frobenius_error: ScalarQuantity
    evaluation_interpolation_hamiltonian_maximum_error: ScalarQuantity
    evaluation_interpolation_spectral_maximum_error: ScalarQuantity

    CHANNELS: ClassVar[tuple[str, ...]] = ("reference", "attacked", "pointwise")

    def __post_init__(self) -> None:
        if self.channel not in self.CHANNELS:
            raise ValueError("transform channel is unsupported")
        if (
            not isinstance(self.representatives, tuple)
            or not self.representatives
            or any(type(value) is not int for value in self.representatives)
            or self.representatives != tuple(sorted(set(self.representatives)))
        ):
            raise ValueError("representatives must be a sorted unique integer tuple")
        if len(self.representatives) % 2 != 0:
            raise ValueError("the cyclic representative inventory must have even size")
        if type(self.cyclic_conversion_representative) is not int:
            raise TypeError("cyclic_conversion_representative must be a built-in int")
        if self.cyclic_conversion_representative != -len(self.representatives) // 2:
            raise ValueError("cyclic conversion must remove the negative Nyquist class")
        expected_ordinary = tuple(
            representative
            for representative in self.representatives
            if representative != self.cyclic_conversion_representative
        )
        if self.ordinary_representatives != expected_ordinary:
            raise ValueError(
                "ordinary_representatives must remove only the cyclic Nyquist class"
            )
        if not isinstance(self.hopping_blocks, tuple) or len(
            self.hopping_blocks
        ) != len(self.representatives):
            raise ValueError("hopping blocks must match the representative inventory")
        for block in self.hopping_blocks:
            if type(block) is not ComplexMatrixQuantity:
                raise TypeError("every hopping block must be ComplexMatrixQuantity")
            if block.magnitude.shape != (2, 2) or not isinstance(block.unit, Unitless):
                raise ValueError(
                    "every hopping block must be a unitless two-by-two matrix"
                )
        for value, name in (
            (self.cyclic_conversion_power, "cyclic_conversion_power"),
            (
                self.reconstruction_maximum_frobenius_error,
                "reconstruction_maximum_frobenius_error",
            ),
            (
                self.hermiticity_maximum_frobenius_error,
                "hermiticity_maximum_frobenius_error",
            ),
            (
                self.evaluation_interpolation_hamiltonian_maximum_error,
                "evaluation_interpolation_hamiltonian_maximum_error",
            ),
            (
                self.evaluation_interpolation_spectral_maximum_error,
                "evaluation_interpolation_spectral_maximum_error",
            ),
        ):
            if type(value) is not ScalarQuantity or not isinstance(
                value.unit, Unitless
            ):
                raise TypeError(f"{name} must be a unitless ScalarQuantity")
            if not isfinite(value.magnitude) or value.magnitude < 0.0:
                raise ValueError(f"{name} must be finite and nonnegative")

    def _mapping(self) -> Mapping[str, SerializableValue]:
        return {
            "channel": self.channel,
            "representatives": self.representatives,
            "hopping_blocks": self.hopping_blocks,
            "ordinary_representatives": self.ordinary_representatives,
            "cyclic_conversion_representative": (self.cyclic_conversion_representative),
            "cyclic_conversion_power": self.cyclic_conversion_power,
            "reconstruction_maximum_frobenius_error": (
                self.reconstruction_maximum_frobenius_error
            ),
            "hermiticity_maximum_frobenius_error": (
                self.hermiticity_maximum_frobenius_error
            ),
            "evaluation_interpolation_hamiltonian_maximum_error": (
                self.evaluation_interpolation_hamiltonian_maximum_error
            ),
            "evaluation_interpolation_spectral_maximum_error": (
                self.evaluation_interpolation_spectral_maximum_error
            ),
        }

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        required = {
            "channel",
            "representatives",
            "hopping_blocks",
            "ordinary_representatives",
            "cyclic_conversion_representative",
            "cyclic_conversion_power",
            "reconstruction_maximum_frobenius_error",
            "hermiticity_maximum_frobenius_error",
            "evaluation_interpolation_hamiltonian_maximum_error",
            "evaluation_interpolation_spectral_maximum_error",
        }
        if set(values) != required:
            raise ValueError("transform fields do not match")
        channel = values["channel"]
        representatives = values["representatives"]
        ordinary_representatives = values["ordinary_representatives"]
        blocks = values["hopping_blocks"]
        conversion_representative = values["cyclic_conversion_representative"]
        scalar_names = (
            "cyclic_conversion_power",
            "reconstruction_maximum_frobenius_error",
            "hermiticity_maximum_frobenius_error",
            "evaluation_interpolation_hamiltonian_maximum_error",
            "evaluation_interpolation_spectral_maximum_error",
        )
        if type(channel) is not str:
            raise TypeError("channel must decode to a string")
        if not isinstance(representatives, tuple) or not isinstance(
            ordinary_representatives, tuple
        ):
            raise TypeError("representative inventories must decode to tuples")
        if not isinstance(blocks, tuple):
            raise TypeError("hopping blocks must decode to a tuple")
        if type(conversion_representative) is not int:
            raise TypeError("cyclic conversion representative must decode to an int")
        if any(type(block) is not ComplexMatrixQuantity for block in blocks):
            raise TypeError("hopping blocks must decode to ComplexMatrixQuantity")
        if any(type(value) is not int for value in representatives) or any(
            type(value) is not int for value in ordinary_representatives
        ):
            raise TypeError("representatives must decode to built-in integers")
        scalars: dict[str, ScalarQuantity] = {}
        for name in scalar_names:
            value = values[name]
            if type(value) is not ScalarQuantity:
                raise TypeError(f"{name} must decode to ScalarQuantity")
            scalars[name] = value
        return cls(
            channel=channel,
            representatives=tuple(representatives),
            hopping_blocks=tuple(blocks),
            ordinary_representatives=tuple(ordinary_representatives),
            cyclic_conversion_representative=conversion_representative,
            cyclic_conversion_power=scalars["cyclic_conversion_power"],
            reconstruction_maximum_frobenius_error=scalars[
                "reconstruction_maximum_frobenius_error"
            ],
            hermiticity_maximum_frobenius_error=scalars[
                "hermiticity_maximum_frobenius_error"
            ],
            evaluation_interpolation_hamiltonian_maximum_error=scalars[
                "evaluation_interpolation_hamiltonian_maximum_error"
            ],
            evaluation_interpolation_spectral_maximum_error=scalars[
                "evaluation_interpolation_spectral_maximum_error"
            ],
        )


@dataclass(frozen=True, slots=True)
class Periodic1DCompositeBandAlignmentChannelRangeResult(BaseTypedRecord):
    """Retain ordinary-tail, truncation, and total errors for one channel."""

    channel: str
    ordinary_omitted_block_l2_norm: ScalarQuantity
    construction_total_spectral_maximum_error: ScalarQuantity
    evaluation_truncation_hamiltonian_maximum_error: ScalarQuantity
    evaluation_total_hamiltonian_maximum_error: ScalarQuantity
    evaluation_truncation_spectral_maximum_error: ScalarQuantity
    evaluation_total_spectral_maximum_error: ScalarQuantity

    def __post_init__(self) -> None:
        if self.channel not in Periodic1DCompositeBandAlignmentTransformResult.CHANNELS:
            raise ValueError("range channel is unsupported")
        for value, name in (
            (
                self.ordinary_omitted_block_l2_norm,
                "ordinary_omitted_block_l2_norm",
            ),
            (
                self.construction_total_spectral_maximum_error,
                "construction_total_spectral_maximum_error",
            ),
            (
                self.evaluation_truncation_hamiltonian_maximum_error,
                "evaluation_truncation_hamiltonian_maximum_error",
            ),
            (
                self.evaluation_total_hamiltonian_maximum_error,
                "evaluation_total_hamiltonian_maximum_error",
            ),
            (
                self.evaluation_truncation_spectral_maximum_error,
                "evaluation_truncation_spectral_maximum_error",
            ),
            (
                self.evaluation_total_spectral_maximum_error,
                "evaluation_total_spectral_maximum_error",
            ),
        ):
            if type(value) is not ScalarQuantity or not isinstance(
                value.unit, Unitless
            ):
                raise TypeError(f"{name} must be a unitless ScalarQuantity")
            if not isfinite(value.magnitude) or value.magnitude < 0.0:
                raise ValueError(f"{name} must be finite and nonnegative")

    def _mapping(self) -> Mapping[str, SerializableValue]:
        return {
            "channel": self.channel,
            "ordinary_omitted_block_l2_norm": (self.ordinary_omitted_block_l2_norm),
            "construction_total_spectral_maximum_error": (
                self.construction_total_spectral_maximum_error
            ),
            "evaluation_truncation_hamiltonian_maximum_error": (
                self.evaluation_truncation_hamiltonian_maximum_error
            ),
            "evaluation_total_hamiltonian_maximum_error": (
                self.evaluation_total_hamiltonian_maximum_error
            ),
            "evaluation_truncation_spectral_maximum_error": (
                self.evaluation_truncation_spectral_maximum_error
            ),
            "evaluation_total_spectral_maximum_error": (
                self.evaluation_total_spectral_maximum_error
            ),
        }

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        scalar_names = (
            "ordinary_omitted_block_l2_norm",
            "construction_total_spectral_maximum_error",
            "evaluation_truncation_hamiltonian_maximum_error",
            "evaluation_total_hamiltonian_maximum_error",
            "evaluation_truncation_spectral_maximum_error",
            "evaluation_total_spectral_maximum_error",
        )
        if set(values) != {"channel", *scalar_names}:
            raise ValueError("channel-range fields do not match")
        channel = values["channel"]
        if type(channel) is not str:
            raise TypeError("channel must decode to a string")
        scalars: dict[str, ScalarQuantity] = {}
        for name in scalar_names:
            value = values[name]
            if type(value) is not ScalarQuantity:
                raise TypeError(f"{name} must decode to ScalarQuantity")
            scalars[name] = value
        return cls(
            channel=channel,
            ordinary_omitted_block_l2_norm=scalars["ordinary_omitted_block_l2_norm"],
            construction_total_spectral_maximum_error=scalars[
                "construction_total_spectral_maximum_error"
            ],
            evaluation_truncation_hamiltonian_maximum_error=scalars[
                "evaluation_truncation_hamiltonian_maximum_error"
            ],
            evaluation_total_hamiltonian_maximum_error=scalars[
                "evaluation_total_hamiltonian_maximum_error"
            ],
            evaluation_truncation_spectral_maximum_error=scalars[
                "evaluation_truncation_spectral_maximum_error"
            ],
            evaluation_total_spectral_maximum_error=scalars[
                "evaluation_total_spectral_maximum_error"
            ],
        )


@dataclass(frozen=True, slots=True)
class Periodic1DCompositeBandAlignmentRangeResult(BaseTypedRecord):
    """Retain all three channel results for one symmetric hopping range."""

    maximum_range: int
    channels: tuple[Periodic1DCompositeBandAlignmentChannelRangeResult, ...]

    def __post_init__(self) -> None:
        if type(self.maximum_range) is not int or self.maximum_range < 0:
            raise ValueError("maximum_range must be a nonnegative built-in integer")
        if (
            not isinstance(self.channels, tuple)
            or tuple(channel.channel for channel in self.channels)
            != Periodic1DCompositeBandAlignmentTransformResult.CHANNELS
        ):
            raise ValueError("range channels must match the declared channel order")

    def _mapping(self) -> Mapping[str, SerializableValue]:
        return {"maximum_range": self.maximum_range, "channels": self.channels}

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        if set(values) != {"maximum_range", "channels"}:
            raise ValueError("range-result fields do not match")
        maximum_range = values["maximum_range"]
        channels = values["channels"]
        if type(maximum_range) is not int or not isinstance(channels, tuple):
            raise TypeError("range-result values decode to wrong types")
        decoded: list[Periodic1DCompositeBandAlignmentChannelRangeResult] = []
        for channel in channels:
            if not isinstance(channel, Mapping):
                raise TypeError("range channels must decode to mappings")
            decoded.append(
                Periodic1DCompositeBandAlignmentChannelRangeResult.from_dict(channel)
            )
        return cls(maximum_range=maximum_range, channels=tuple(decoded))


@dataclass(frozen=True, slots=True, eq=False)
class Periodic1DCompositeBandAlignmentCalculationResult(BaseTypedRecord):
    """Compose authoritative rank-two samples, frames, operators, and locality."""

    calculation_family: str
    configuration: Periodic1DCompositeBandAlignmentConfiguration
    construction_reduced_momenta: tuple[float, ...]
    evaluation_reduced_momenta: tuple[float, ...]
    construction_parent_spectrum: MatrixQuantity
    evaluation_parent_spectrum: MatrixQuantity
    reference_frames: tuple[ComplexMatrixQuantity, ...]
    attacked_frames: tuple[ComplexMatrixQuantity, ...]
    pointwise_aligned_frames: tuple[ComplexMatrixQuantity, ...]
    globally_aligned_frames: tuple[ComplexMatrixQuantity, ...]
    pointwise_rotations: tuple[ComplexMatrixQuantity, ...]
    global_rotation: ComplexMatrixQuantity
    reference_operators: tuple[ComplexMatrixQuantity, ...]
    attacked_operators: tuple[ComplexMatrixQuantity, ...]
    pointwise_aligned_operators: tuple[ComplexMatrixQuantity, ...]
    globally_aligned_operators: tuple[ComplexMatrixQuantity, ...]
    diagnostics: Periodic1DCompositeBandAlignmentDiagnostics
    transforms: tuple[Periodic1DCompositeBandAlignmentTransformResult, ...]
    ranges: tuple[Periodic1DCompositeBandAlignmentRangeResult, ...]

    CALCULATION_FAMILY: ClassVar[str] = (
        "periodic1d-rank2-composite-band-alignment-locality"
    )

    def __post_init__(self) -> None:
        """Validate section identities and concise cross-section correlations."""
        if self.calculation_family != self.CALCULATION_FAMILY:
            raise ValueError("calculation_family does not identify the rank-two family")
        if (
            type(self.configuration)
            is not Periodic1DCompositeBandAlignmentConfiguration
        ):
            raise TypeError("configuration has the wrong exact type")
        construction_size = self.configuration.construction_size
        evaluation_size = self.configuration.evaluation_size
        if (
            self.construction_reduced_momenta
            != self.configuration.construction_reduced_momenta()
        ):
            raise ValueError("construction coordinates differ from configuration")
        if (
            self.evaluation_reduced_momenta
            != self.configuration.evaluation_reduced_momenta()
        ):
            raise ValueError("evaluation coordinates differ from configuration")
        for values, size, name in (
            (self.construction_reduced_momenta, construction_size, "construction"),
            (self.evaluation_reduced_momenta, evaluation_size, "evaluation"),
        ):
            if (
                not isinstance(values, tuple)
                or len(values) != size
                or any(
                    type(value) is not float or not isfinite(value) for value in values
                )
            ):
                raise TypeError(f"{name} coordinates must be finite float tuples")
        for spectrum, shape, name in (
            (
                self.construction_parent_spectrum,
                (construction_size, 4),
                "construction_parent_spectrum",
            ),
            (
                self.evaluation_parent_spectrum,
                (evaluation_size, 4),
                "evaluation_parent_spectrum",
            ),
        ):
            if (
                type(spectrum) is not MatrixQuantity
                or spectrum.magnitude.shape != shape
            ):
                raise TypeError(f"{name} has the wrong quantity type or shape")
            if not isinstance(spectrum.unit, Unitless):
                raise ValueError(f"{name} must be unitless")
        frame_fields = (
            self.reference_frames,
            self.attacked_frames,
            self.pointwise_aligned_frames,
            self.globally_aligned_frames,
        )
        for frames in frame_fields:
            self._validate_matrix_inventory(frames, construction_size, (4, 2), "frame")
        self._validate_matrix_inventory(
            self.pointwise_rotations, construction_size, (2, 2), "rotation"
        )
        if type(
            self.global_rotation
        ) is not ComplexMatrixQuantity or self.global_rotation.magnitude.shape != (
            2,
            2,
        ):
            raise TypeError("global_rotation must be a two-by-two complex quantity")
        operator_fields = (
            self.reference_operators,
            self.attacked_operators,
            self.pointwise_aligned_operators,
            self.globally_aligned_operators,
        )
        for operators in operator_fields:
            self._validate_matrix_inventory(
                operators, construction_size, (2, 2), "represented operator"
            )
        if type(self.diagnostics) is not Periodic1DCompositeBandAlignmentDiagnostics:
            raise TypeError("diagnostics has the wrong exact type")
        if (
            not isinstance(self.transforms, tuple)
            or tuple(transform.channel for transform in self.transforms)
            != Periodic1DCompositeBandAlignmentTransformResult.CHANNELS
        ):
            raise ValueError("transforms must match the declared channel order")
        if (
            not isinstance(self.ranges, tuple)
            or tuple(result.maximum_range for result in self.ranges)
            != self.configuration.hopping_ranges
        ):
            raise ValueError("ranges must match the configuration inventory")

    @staticmethod
    def _validate_matrix_inventory(
        values: tuple[ComplexMatrixQuantity, ...],
        expected_length: int,
        expected_shape: tuple[int, int],
        name: str,
    ) -> None:
        if not isinstance(values, tuple) or len(values) != expected_length:
            raise ValueError(f"{name} inventory has the wrong length")
        for value in values:
            if type(value) is not ComplexMatrixQuantity:
                raise TypeError(f"every {name} must be ComplexMatrixQuantity")
            if value.magnitude.shape != expected_shape or not isinstance(
                value.unit, Unitless
            ):
                raise ValueError(f"every {name} must have the declared unitless shape")

    def _mapping(self) -> Mapping[str, SerializableValue]:
        return {
            "calculation_family": self.calculation_family,
            "configuration": self.configuration,
            "sample_coordinates": {
                "construction": self.construction_reduced_momenta,
                "evaluation": self.evaluation_reduced_momenta,
            },
            "parent_spectra": {
                "construction": self.construction_parent_spectrum,
                "evaluation": self.evaluation_parent_spectrum,
            },
            "frames": {
                "reference": self.reference_frames,
                "attacked": self.attacked_frames,
                "pointwise_aligned": self.pointwise_aligned_frames,
                "globally_aligned": self.globally_aligned_frames,
            },
            "alignment_transformations": {
                "pointwise": self.pointwise_rotations,
                "global": self.global_rotation,
            },
            "represented_operators": {
                "reference": self.reference_operators,
                "attacked": self.attacked_operators,
                "pointwise_aligned": self.pointwise_aligned_operators,
                "globally_aligned": self.globally_aligned_operators,
            },
            "diagnostics": self.diagnostics,
            "complete_transforms": self.transforms,
            "range_study": self.ranges,
        }

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        required = {
            "calculation_family",
            "configuration",
            "sample_coordinates",
            "parent_spectra",
            "frames",
            "alignment_transformations",
            "represented_operators",
            "diagnostics",
            "complete_transforms",
            "range_study",
        }
        if set(values) != required:
            raise ValueError("composite-band result fields do not match")

        def mapping(name: str) -> Mapping[str, SerializableValue]:
            value = values[name]
            if not isinstance(value, Mapping):
                raise TypeError(f"{name} must decode to a mapping")
            return value

        family = values["calculation_family"]
        if type(family) is not str:
            raise TypeError("calculation_family must decode to a string")
        coordinates = mapping("sample_coordinates")
        spectra = mapping("parent_spectra")
        frames = mapping("frames")
        transformations = mapping("alignment_transformations")
        operators = mapping("represented_operators")
        configuration_value = values["configuration"]
        diagnostics_value = values["diagnostics"]
        transforms_value = values["complete_transforms"]
        ranges_value = values["range_study"]
        if not isinstance(configuration_value, Mapping) or not isinstance(
            diagnostics_value, Mapping
        ):
            raise TypeError("configuration and diagnostics must decode to mappings")
        if not isinstance(transforms_value, tuple) or not isinstance(
            ranges_value, tuple
        ):
            raise TypeError("transform and range inventories must decode to tuples")
        construction_coordinates = coordinates.get("construction")
        evaluation_coordinates = coordinates.get("evaluation")
        construction_spectrum = spectra.get("construction")
        evaluation_spectrum = spectra.get("evaluation")
        if not isinstance(construction_coordinates, tuple) or not isinstance(
            evaluation_coordinates, tuple
        ):
            raise TypeError("sample coordinates must decode to tuples")
        if (
            type(construction_spectrum) is not MatrixQuantity
            or type(evaluation_spectrum) is not MatrixQuantity
        ):
            raise TypeError("parent spectra must decode to MatrixQuantity")

        def complex_tuple(
            container: Mapping[str, SerializableValue], name: str
        ) -> tuple[ComplexMatrixQuantity, ...]:
            value = container.get(name)
            if not isinstance(value, tuple) or any(
                type(item) is not ComplexMatrixQuantity for item in value
            ):
                raise TypeError(f"{name} must decode to complex matrix quantities")
            return tuple(value)

        global_rotation = transformations.get("global")
        if type(global_rotation) is not ComplexMatrixQuantity:
            raise TypeError("global rotation must decode to ComplexMatrixQuantity")
        decoded_transforms: list[Periodic1DCompositeBandAlignmentTransformResult] = []
        for transform in transforms_value:
            if not isinstance(transform, Mapping):
                raise TypeError("transforms must decode to mappings")
            decoded_transforms.append(
                Periodic1DCompositeBandAlignmentTransformResult.from_dict(transform)
            )
        decoded_ranges: list[Periodic1DCompositeBandAlignmentRangeResult] = []
        for range_value in ranges_value:
            if not isinstance(range_value, Mapping):
                raise TypeError("range results must decode to mappings")
            decoded_ranges.append(
                Periodic1DCompositeBandAlignmentRangeResult.from_dict(range_value)
            )
        return cls(
            calculation_family=family,
            configuration=Periodic1DCompositeBandAlignmentConfiguration.from_dict(
                configuration_value
            ),
            construction_reduced_momenta=tuple(construction_coordinates),
            evaluation_reduced_momenta=tuple(evaluation_coordinates),
            construction_parent_spectrum=construction_spectrum,
            evaluation_parent_spectrum=evaluation_spectrum,
            reference_frames=complex_tuple(frames, "reference"),
            attacked_frames=complex_tuple(frames, "attacked"),
            pointwise_aligned_frames=complex_tuple(frames, "pointwise_aligned"),
            globally_aligned_frames=complex_tuple(frames, "globally_aligned"),
            pointwise_rotations=complex_tuple(transformations, "pointwise"),
            global_rotation=global_rotation,
            reference_operators=complex_tuple(operators, "reference"),
            attacked_operators=complex_tuple(operators, "attacked"),
            pointwise_aligned_operators=complex_tuple(operators, "pointwise_aligned"),
            globally_aligned_operators=complex_tuple(operators, "globally_aligned"),
            diagnostics=Periodic1DCompositeBandAlignmentDiagnostics.from_dict(
                diagnostics_value
            ),
            transforms=tuple(decoded_transforms),
            ranges=tuple(decoded_ranges),
        )


__all__ = [
    "Periodic1DCompositeBandAlignmentCalculationResult",
    "Periodic1DCompositeBandAlignmentChannelRangeResult",
    "Periodic1DCompositeBandAlignmentDiagnostics",
    "Periodic1DCompositeBandAlignmentRangeResult",
    "Periodic1DCompositeBandAlignmentTransformResult",
]
