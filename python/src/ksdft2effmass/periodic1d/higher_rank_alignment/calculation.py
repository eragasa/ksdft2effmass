"""Immutable request and result records for higher-rank calculation production."""

from __future__ import annotations

import math
from collections.abc import Mapping
from dataclasses import dataclass
from typing import ClassVar, Self

import numpy as np
from numpy.typing import NDArray
from projectkoios.physkit.units import ComplexMatrixQuantity, Unitless

from ksdft2effmass.analysis.matrix_field.diagnostics import (
    MatrixFieldComparisonDiagnostics,
    MatrixFieldErrorSummary,
)
from ksdft2effmass.serialization import BaseTypedRecord, SerializableValue

from .configuration import Periodic1DHigherRankAlignmentConfiguration
from .definition import (
    Periodic1DHigherRankAlignmentChannel,
    Periodic1DHigherRankAlignmentStatus,
)
from .request import Periodic1DHigherRankAlignmentTransportRequest
from .result import (
    Periodic1DHigherRankAlignmentStatusResult,
    Periodic1DHigherRankAlignmentTransportBackendFailureResult,
    Periodic1DHigherRankAlignmentTransportOwnerResult,
)

FloatArray = NDArray[np.float64]
IntArray = NDArray[np.int64]

_ODD_CENTERED_NO_NYQUIST_DISPOSITION = "inapplicable-odd-centered-no-nyquist"


def _nonempty(value: str, name: str) -> None:
    if type(value) is not str:
        raise TypeError(f"{name} must be a built-in string")
    if not value:
        raise ValueError(f"{name} must be nonempty")


def _finite_nonnegative(value: float, name: str) -> None:
    if type(value) is not float:
        raise TypeError(f"{name} must be a built-in float")
    if not math.isfinite(value) or value < 0.0:
        raise ValueError(f"{name} must be finite and nonnegative")


def _positive(value: float, name: str) -> None:
    _finite_nonnegative(value, name)
    if value == 0.0:
        raise ValueError(f"{name} must be positive")


def _float_array(value: FloatArray, name: str, *, ndim: int = 1) -> FloatArray:
    if type(value) is not np.ndarray or value.dtype != np.dtype(np.float64):
        raise TypeError(f"{name} must be an exact float64 numpy.ndarray")
    if value.ndim != ndim:
        raise ValueError(f"{name} must have {ndim} dimensions")
    if not bool(np.isfinite(value).all()):
        raise ValueError(f"{name} must be finite")
    normalized = np.array(value, dtype=np.float64, copy=True)
    normalized.flags.writeable = False
    return normalized


def _int_array(value: IntArray, name: str) -> IntArray:
    if type(value) is not np.ndarray or value.dtype != np.dtype(np.int64):
        raise TypeError(f"{name} must be an exact int64 numpy.ndarray")
    if value.ndim != 1:
        raise ValueError(f"{name} must be one dimensional")
    normalized = np.array(value, dtype=np.int64, copy=True)
    normalized.flags.writeable = False
    return normalized


def _decoded_float(value: SerializableValue, name: str) -> float:
    if type(value) is not float:
        raise TypeError(f"{name} must decode to a built-in float")
    return value


def _decoded_bool(value: SerializableValue, name: str) -> bool:
    if type(value) is not bool:
        raise TypeError(f"{name} must decode to a built-in bool")
    return value


def _decoded_int(value: SerializableValue, name: str) -> int:
    if type(value) is not int:
        raise TypeError(f"{name} must decode to a built-in integer")
    return value


def _decoded_optional_float(
    value: SerializableValue,
    name: str,
) -> float | None:
    if value is None:
        return None
    if type(value) is not float:
        raise TypeError(f"{name} must decode to a built-in float or None")
    return value


def _mapping_value(
    value: SerializableValue, name: str
) -> Mapping[str, SerializableValue]:
    if not isinstance(value, Mapping):
        raise TypeError(f"{name} must decode to a mapping")
    return value


def _tuple_of_mappings(
    value: SerializableValue,
    name: str,
) -> tuple[Mapping[str, SerializableValue], ...]:
    if not isinstance(value, tuple):
        raise TypeError(f"{name} must decode to a tuple")
    decoded: list[Mapping[str, SerializableValue]] = []
    for item in value:
        if not isinstance(item, Mapping):
            raise TypeError(f"{name} entries must decode to mappings")
        decoded.append(item)
    return tuple(decoded)


@dataclass(frozen=True, slots=True)
class Periodic1DHigherRankAlignmentCalculationControls(BaseTypedRecord):
    """Store frozen supports, normalizations, resource bounds, and tolerances."""

    support_radii: tuple[int, ...]
    maximum_recorded_block_range: int
    energy_reference: float
    saturation_denominator_floor: float
    refinement_denominator_floor: float
    maximum_working_elements: int
    model_structure_tolerance: float
    alignment_integrity_tolerance: float
    direct_recovery_tolerance: float
    fourier_consistency_tolerance: float
    error_decomposition_tolerance: float
    tail_monotonicity_tolerance: float
    perturbation_bound_tolerance: float
    final_interpolation_operator_tolerance: float
    final_interpolation_spectrum_tolerance: float
    refinement_absolute_tolerance: float
    refinement_relative_tolerance: float

    SUPPORT_RADII: ClassVar[tuple[int, ...]] = (0, 1, 2, 4, 8, 16, 32, 64, 128)
    MAXIMUM_RECORDED_BLOCK_RANGE: ClassVar[int] = 128
    ENERGY_REFERENCE: ClassVar[float] = 1.0
    SATURATION_DENOMINATOR_FLOOR: ClassVar[float] = 1.0e-30
    REFINEMENT_DENOMINATOR_FLOOR: ClassVar[float] = 1.0e-30
    MAXIMUM_WORKING_ELEMENTS: ClassVar[int] = 1_000_000
    MODEL_STRUCTURE_TOLERANCE: ClassVar[float] = 1.0e-12
    ALIGNMENT_INTEGRITY_TOLERANCE: ClassVar[float] = 1.0e-12
    DIRECT_RECOVERY_TOLERANCE: ClassVar[float] = 1.0e-11
    FOURIER_CONSISTENCY_TOLERANCE: ClassVar[float] = 2.0e-11
    ERROR_DECOMPOSITION_TOLERANCE: ClassVar[float] = 2.0e-11
    TAIL_MONOTONICITY_TOLERANCE: ClassVar[float] = 2.0e-11
    PERTURBATION_BOUND_TOLERANCE: ClassVar[float] = 1.0e-11
    FINAL_INTERPOLATION_OPERATOR_TOLERANCE: ClassVar[float] = 1.0e-9
    FINAL_INTERPOLATION_SPECTRUM_TOLERANCE: ClassVar[float] = 1.0e-10
    REFINEMENT_ABSOLUTE_TOLERANCE: ClassVar[float] = 1.0e-10
    REFINEMENT_RELATIVE_TOLERANCE: ClassVar[float] = 1.0e-6

    def __post_init__(self) -> None:
        """Reject any control that differs from the version-one protocol."""
        if type(self.support_radii) is not tuple or any(
            type(value) is not int for value in self.support_radii
        ):
            raise TypeError("support_radii must be an exact integer tuple")
        if self.support_radii != self.SUPPORT_RADII:
            raise ValueError("support_radii must match the frozen support inventory")
        for value, expected, name in (
            (
                self.maximum_recorded_block_range,
                self.MAXIMUM_RECORDED_BLOCK_RANGE,
                "maximum_recorded_block_range",
            ),
            (
                self.maximum_working_elements,
                self.MAXIMUM_WORKING_ELEMENTS,
                "maximum_working_elements",
            ),
        ):
            if type(value) is not int:
                raise TypeError(f"{name} must be a built-in integer")
            if value != expected:
                raise ValueError(f"{name} must match the frozen protocol")
        actual_tolerances = (
            self.energy_reference,
            self.saturation_denominator_floor,
            self.refinement_denominator_floor,
            self.model_structure_tolerance,
            self.alignment_integrity_tolerance,
            self.direct_recovery_tolerance,
            self.fourier_consistency_tolerance,
            self.error_decomposition_tolerance,
            self.tail_monotonicity_tolerance,
            self.perturbation_bound_tolerance,
            self.final_interpolation_operator_tolerance,
            self.final_interpolation_spectrum_tolerance,
            self.refinement_absolute_tolerance,
            self.refinement_relative_tolerance,
        )
        expected_tolerances = (
            self.ENERGY_REFERENCE,
            self.SATURATION_DENOMINATOR_FLOOR,
            self.REFINEMENT_DENOMINATOR_FLOOR,
            self.MODEL_STRUCTURE_TOLERANCE,
            self.ALIGNMENT_INTEGRITY_TOLERANCE,
            self.DIRECT_RECOVERY_TOLERANCE,
            self.FOURIER_CONSISTENCY_TOLERANCE,
            self.ERROR_DECOMPOSITION_TOLERANCE,
            self.TAIL_MONOTONICITY_TOLERANCE,
            self.PERTURBATION_BOUND_TOLERANCE,
            self.FINAL_INTERPOLATION_OPERATOR_TOLERANCE,
            self.FINAL_INTERPOLATION_SPECTRUM_TOLERANCE,
            self.REFINEMENT_ABSOLUTE_TOLERANCE,
            self.REFINEMENT_RELATIVE_TOLERANCE,
        )
        for tolerance_value, tolerance_name in zip(
            actual_tolerances, self._float_names(), strict=True
        ):
            _finite_nonnegative(tolerance_value, tolerance_name)
        if actual_tolerances != expected_tolerances:
            raise ValueError("calculation controls must match the frozen protocol")

    @classmethod
    def frozen(cls) -> Self:
        """Return the complete version-one control inventory."""
        return cls(
            support_radii=cls.SUPPORT_RADII,
            maximum_recorded_block_range=cls.MAXIMUM_RECORDED_BLOCK_RANGE,
            energy_reference=cls.ENERGY_REFERENCE,
            saturation_denominator_floor=cls.SATURATION_DENOMINATOR_FLOOR,
            refinement_denominator_floor=cls.REFINEMENT_DENOMINATOR_FLOOR,
            maximum_working_elements=cls.MAXIMUM_WORKING_ELEMENTS,
            model_structure_tolerance=cls.MODEL_STRUCTURE_TOLERANCE,
            alignment_integrity_tolerance=cls.ALIGNMENT_INTEGRITY_TOLERANCE,
            direct_recovery_tolerance=cls.DIRECT_RECOVERY_TOLERANCE,
            fourier_consistency_tolerance=cls.FOURIER_CONSISTENCY_TOLERANCE,
            error_decomposition_tolerance=cls.ERROR_DECOMPOSITION_TOLERANCE,
            tail_monotonicity_tolerance=cls.TAIL_MONOTONICITY_TOLERANCE,
            perturbation_bound_tolerance=cls.PERTURBATION_BOUND_TOLERANCE,
            final_interpolation_operator_tolerance=cls.FINAL_INTERPOLATION_OPERATOR_TOLERANCE,
            final_interpolation_spectrum_tolerance=cls.FINAL_INTERPOLATION_SPECTRUM_TOLERANCE,
            refinement_absolute_tolerance=cls.REFINEMENT_ABSOLUTE_TOLERANCE,
            refinement_relative_tolerance=cls.REFINEMENT_RELATIVE_TOLERANCE,
        )

    @classmethod
    def _float_names(cls) -> tuple[str, ...]:
        return (
            "energy_reference",
            "saturation_denominator_floor",
            "refinement_denominator_floor",
            "model_structure_tolerance",
            "alignment_integrity_tolerance",
            "direct_recovery_tolerance",
            "fourier_consistency_tolerance",
            "error_decomposition_tolerance",
            "tail_monotonicity_tolerance",
            "perturbation_bound_tolerance",
            "final_interpolation_operator_tolerance",
            "final_interpolation_spectrum_tolerance",
            "refinement_absolute_tolerance",
            "refinement_relative_tolerance",
        )

    def _mapping(self) -> Mapping[str, SerializableValue]:
        return {
            "support_radii": self.support_radii,
            "maximum_recorded_block_range": self.maximum_recorded_block_range,
            "energy_reference": self.energy_reference,
            "saturation_denominator_floor": self.saturation_denominator_floor,
            "refinement_denominator_floor": self.refinement_denominator_floor,
            "maximum_working_elements": self.maximum_working_elements,
            "model_structure_tolerance": self.model_structure_tolerance,
            "alignment_integrity_tolerance": self.alignment_integrity_tolerance,
            "direct_recovery_tolerance": self.direct_recovery_tolerance,
            "fourier_consistency_tolerance": self.fourier_consistency_tolerance,
            "error_decomposition_tolerance": self.error_decomposition_tolerance,
            "tail_monotonicity_tolerance": self.tail_monotonicity_tolerance,
            "perturbation_bound_tolerance": self.perturbation_bound_tolerance,
            "final_interpolation_operator_tolerance": (
                self.final_interpolation_operator_tolerance
            ),
            "final_interpolation_spectrum_tolerance": (
                self.final_interpolation_spectrum_tolerance
            ),
            "refinement_absolute_tolerance": self.refinement_absolute_tolerance,
            "refinement_relative_tolerance": self.refinement_relative_tolerance,
        }

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        required = {
            "support_radii",
            "maximum_recorded_block_range",
            "maximum_working_elements",
            *cls._float_names(),
        }
        if set(values) != required:
            raise ValueError("calculation control fields do not match")
        supports = values["support_radii"]
        if not isinstance(supports, tuple) or any(
            type(value) is not int for value in supports
        ):
            raise TypeError("support_radii must decode to built-in integers")
        integers: dict[str, int] = {}
        for name in ("maximum_recorded_block_range", "maximum_working_elements"):
            value = values[name]
            if type(value) is not int:
                raise TypeError(f"{name} must decode to a built-in integer")
            integers[name] = value
        floats: dict[str, float] = {}
        for name in cls._float_names():
            value = values[name]
            if type(value) is not float:
                raise TypeError(f"{name} must decode to a built-in float")
            floats[name] = value
        return cls(
            support_radii=supports,
            maximum_recorded_block_range=integers["maximum_recorded_block_range"],
            maximum_working_elements=integers["maximum_working_elements"],
            **floats,
        )


@dataclass(frozen=True, slots=True)
class Periodic1DHigherRankAlignmentCalculationRequest(BaseTypedRecord):
    """Bind one rank/depth calculation to exact controls and physical identities."""

    configuration: Periodic1DHigherRankAlignmentConfiguration
    controls: Periodic1DHigherRankAlignmentCalculationControls
    retained_rank: int
    circuit_depth: int
    ambient_basis_identifier: str
    retained_frame_identifier: str
    endpoint_sewing_identifier: str
    represented_basis_identifier: str
    energy_reference_identifier: str

    def __post_init__(self) -> None:
        if type(self.configuration) is not Periodic1DHigherRankAlignmentConfiguration:
            raise TypeError("configuration must be the exact higher-rank configuration")
        if type(self.controls) is not Periodic1DHigherRankAlignmentCalculationControls:
            raise TypeError("controls must be the exact calculation controls")
        if (
            type(self.retained_rank) is not int
            or self.retained_rank not in self.configuration.retained_ranks
        ):
            raise ValueError("retained_rank must be a configured built-in integer")
        if (
            type(self.circuit_depth) is not int
            or self.circuit_depth not in self.configuration.circuit_depths
        ):
            raise ValueError("circuit_depth must be a configured built-in integer")
        for value, name in (
            (self.ambient_basis_identifier, "ambient_basis_identifier"),
            (self.retained_frame_identifier, "retained_frame_identifier"),
            (self.endpoint_sewing_identifier, "endpoint_sewing_identifier"),
            (self.represented_basis_identifier, "represented_basis_identifier"),
            (self.energy_reference_identifier, "energy_reference_identifier"),
        ):
            _nonempty(value, name)

    @property
    def case_identity(self) -> str:
        return f"r{self.retained_rank:02d}-L{self.circuit_depth:02d}"

    def transport_request(
        self, construction_mesh_size: int
    ) -> Periodic1DHigherRankAlignmentTransportRequest:
        """Return the exact transport request for one configured construction mesh."""
        return Periodic1DHigherRankAlignmentTransportRequest(
            configuration=self.configuration,
            retained_rank=self.retained_rank,
            circuit_depth=self.circuit_depth,
            construction_mesh_size=construction_mesh_size,
            ambient_basis_identifier=self.ambient_basis_identifier,
            retained_frame_identifier=self.retained_frame_identifier,
            endpoint_sewing_identifier=self.endpoint_sewing_identifier,
        )

    def _mapping(self) -> Mapping[str, SerializableValue]:
        return {
            "configuration": self.configuration,
            "controls": self.controls,
            "retained_rank": self.retained_rank,
            "circuit_depth": self.circuit_depth,
            "ambient_basis_identifier": self.ambient_basis_identifier,
            "retained_frame_identifier": self.retained_frame_identifier,
            "endpoint_sewing_identifier": self.endpoint_sewing_identifier,
            "represented_basis_identifier": self.represented_basis_identifier,
            "energy_reference_identifier": self.energy_reference_identifier,
        }

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        required = {
            "configuration",
            "controls",
            "retained_rank",
            "circuit_depth",
            "ambient_basis_identifier",
            "retained_frame_identifier",
            "endpoint_sewing_identifier",
            "represented_basis_identifier",
            "energy_reference_identifier",
        }
        if set(values) != required:
            raise ValueError("calculation request fields do not match")
        rank = values["retained_rank"]
        depth = values["circuit_depth"]
        if type(rank) is not int or type(depth) is not int:
            raise TypeError("rank and depth must decode to built-in integers")
        strings: dict[str, str] = {}
        for name in required - {
            "configuration",
            "controls",
            "retained_rank",
            "circuit_depth",
        }:
            value = values[name]
            if type(value) is not str:
                raise TypeError(f"{name} must decode to a built-in string")
            strings[name] = value
        return cls(
            configuration=Periodic1DHigherRankAlignmentConfiguration.from_dict(
                _mapping_value(values["configuration"], "configuration")
            ),
            controls=Periodic1DHigherRankAlignmentCalculationControls.from_dict(
                _mapping_value(values["controls"], "controls")
            ),
            retained_rank=rank,
            circuit_depth=depth,
            **strings,
        )


@dataclass(frozen=True, slots=True)
class Periodic1DHigherRankModelDiagnostics(BaseTypedRecord):
    """Retain analytic-gap, sampled-gap, structure, and recovery diagnostics."""

    retained_rank: int
    exact_analytic_isolation_gap: float
    sampled_isolation_gaps: FloatArray
    exact_analytic_attack_angle_maximum: float
    sampled_attack_angle_maxima: FloatArray
    parent_hermiticity_defect: float
    reference_frame_isometry_defect: float
    gauge_unitarity_defect: float
    attacked_frame_isometry_defect: float
    attacked_projector_equality_defect: float
    reference_projector_hermiticity_defect: float
    reference_projector_idempotency_defect: float
    reference_operator_recovery_defect: float
    reference_spectrum_recovery_defect: float
    attacked_operator_recovery_defect: float
    attacked_spectrum_recovery_defect: float
    oracle_frame_recovery_defect: float
    oracle_operator_recovery_defect: float

    def __post_init__(self) -> None:
        if (
            type(self.retained_rank) is not int
            or self.retained_rank
            not in Periodic1DHigherRankAlignmentConfiguration.RETAINED_RANKS
        ):
            raise ValueError("retained_rank must be in the frozen inventory")
        if self.exact_analytic_isolation_gap != 2.1:
            raise ValueError(
                "exact_analytic_isolation_gap must equal the protocol value"
            )
        sampled = _float_array(
            self.sampled_isolation_gaps,
            "sampled_isolation_gaps",
        )
        if sampled.shape != (
            len(Periodic1DHigherRankAlignmentConfiguration.CONSTRUCTION_MESH_SIZES),
        ):
            raise ValueError(
                "sampled_isolation_gaps must cover every construction mesh"
            )
        if bool((sampled < self.exact_analytic_isolation_gap).any()):
            raise ValueError(
                "sampled isolation gaps must respect the analytic certificate"
            )
        q = (math.sqrt(41.0) - 3.0) / 8.0
        harmonic_maximum = math.sqrt(1.0 - q**2) * (0.75 + 0.5 * q)
        expected_angle = (
            0.35
            * (1.0 + 0.15 * (self.retained_rank - 2) / (self.retained_rank - 1))
            * harmonic_maximum
        )
        if self.exact_analytic_attack_angle_maximum != expected_angle:
            raise ValueError(
                "exact_analytic_attack_angle_maximum is inconsistent with rank"
            )
        sampled_angles = _float_array(
            self.sampled_attack_angle_maxima,
            "sampled_attack_angle_maxima",
        )
        if sampled_angles.shape != sampled.shape:
            raise ValueError("sampled attack angles must cover every construction mesh")
        if bool((sampled_angles > self.exact_analytic_attack_angle_maximum).any()):
            raise ValueError("sampled attack angle exceeds the analytic certificate")
        for value, name in (
            (self.exact_analytic_isolation_gap, "exact_analytic_isolation_gap"),
            (
                self.exact_analytic_attack_angle_maximum,
                "exact_analytic_attack_angle_maximum",
            ),
            (self.parent_hermiticity_defect, "parent_hermiticity_defect"),
            (
                self.reference_frame_isometry_defect,
                "reference_frame_isometry_defect",
            ),
            (self.gauge_unitarity_defect, "gauge_unitarity_defect"),
            (
                self.attacked_frame_isometry_defect,
                "attacked_frame_isometry_defect",
            ),
            (
                self.attacked_projector_equality_defect,
                "attacked_projector_equality_defect",
            ),
            (
                self.reference_projector_hermiticity_defect,
                "reference_projector_hermiticity_defect",
            ),
            (
                self.reference_projector_idempotency_defect,
                "reference_projector_idempotency_defect",
            ),
            (
                self.reference_operator_recovery_defect,
                "reference_operator_recovery_defect",
            ),
            (
                self.reference_spectrum_recovery_defect,
                "reference_spectrum_recovery_defect",
            ),
            (
                self.attacked_operator_recovery_defect,
                "attacked_operator_recovery_defect",
            ),
            (
                self.attacked_spectrum_recovery_defect,
                "attacked_spectrum_recovery_defect",
            ),
            (self.oracle_frame_recovery_defect, "oracle_frame_recovery_defect"),
            (
                self.oracle_operator_recovery_defect,
                "oracle_operator_recovery_defect",
            ),
        ):
            _finite_nonnegative(value, name)
        object.__setattr__(self, "sampled_isolation_gaps", sampled)
        object.__setattr__(self, "sampled_attack_angle_maxima", sampled_angles)

    def _mapping(self) -> Mapping[str, SerializableValue]:
        return {
            "retained_rank": self.retained_rank,
            "exact_analytic_isolation_gap": self.exact_analytic_isolation_gap,
            "sampled_isolation_gaps": self.sampled_isolation_gaps,
            "exact_analytic_attack_angle_maximum": (
                self.exact_analytic_attack_angle_maximum
            ),
            "sampled_attack_angle_maxima": self.sampled_attack_angle_maxima,
            "parent_hermiticity_defect": self.parent_hermiticity_defect,
            "reference_frame_isometry_defect": self.reference_frame_isometry_defect,
            "gauge_unitarity_defect": self.gauge_unitarity_defect,
            "attacked_frame_isometry_defect": self.attacked_frame_isometry_defect,
            "attacked_projector_equality_defect": (
                self.attacked_projector_equality_defect
            ),
            "reference_projector_hermiticity_defect": (
                self.reference_projector_hermiticity_defect
            ),
            "reference_projector_idempotency_defect": (
                self.reference_projector_idempotency_defect
            ),
            "reference_operator_recovery_defect": (
                self.reference_operator_recovery_defect
            ),
            "reference_spectrum_recovery_defect": (
                self.reference_spectrum_recovery_defect
            ),
            "attacked_operator_recovery_defect": (
                self.attacked_operator_recovery_defect
            ),
            "attacked_spectrum_recovery_defect": (
                self.attacked_spectrum_recovery_defect
            ),
            "oracle_frame_recovery_defect": self.oracle_frame_recovery_defect,
            "oracle_operator_recovery_defect": self.oracle_operator_recovery_defect,
        }

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        if set(values) != {
            "retained_rank",
            "exact_analytic_isolation_gap",
            "sampled_isolation_gaps",
            "exact_analytic_attack_angle_maximum",
            "sampled_attack_angle_maxima",
            "parent_hermiticity_defect",
            "reference_frame_isometry_defect",
            "gauge_unitarity_defect",
            "attacked_frame_isometry_defect",
            "attacked_projector_equality_defect",
            "reference_projector_hermiticity_defect",
            "reference_projector_idempotency_defect",
            "reference_operator_recovery_defect",
            "reference_spectrum_recovery_defect",
            "attacked_operator_recovery_defect",
            "attacked_spectrum_recovery_defect",
            "oracle_frame_recovery_defect",
            "oracle_operator_recovery_defect",
        }:
            raise ValueError("model diagnostic fields do not match")
        sampled = values["sampled_isolation_gaps"]
        sampled_angles = values["sampled_attack_angle_maxima"]
        rank = values["retained_rank"]
        if not isinstance(sampled, np.ndarray) or not isinstance(
            sampled_angles, np.ndarray
        ):
            raise TypeError("sampled diagnostics must decode to numpy.ndarray")
        if type(rank) is not int:
            raise TypeError("retained_rank must decode to a built-in integer")
        return cls(
            retained_rank=rank,
            exact_analytic_isolation_gap=_decoded_float(
                values["exact_analytic_isolation_gap"],
                "exact_analytic_isolation_gap",
            ),
            sampled_isolation_gaps=sampled,
            exact_analytic_attack_angle_maximum=_decoded_float(
                values["exact_analytic_attack_angle_maximum"],
                "exact_analytic_attack_angle_maximum",
            ),
            sampled_attack_angle_maxima=sampled_angles,
            parent_hermiticity_defect=_decoded_float(
                values["parent_hermiticity_defect"], "parent_hermiticity_defect"
            ),
            reference_frame_isometry_defect=_decoded_float(
                values["reference_frame_isometry_defect"],
                "reference_frame_isometry_defect",
            ),
            gauge_unitarity_defect=_decoded_float(
                values["gauge_unitarity_defect"], "gauge_unitarity_defect"
            ),
            attacked_frame_isometry_defect=_decoded_float(
                values["attacked_frame_isometry_defect"],
                "attacked_frame_isometry_defect",
            ),
            attacked_projector_equality_defect=_decoded_float(
                values["attacked_projector_equality_defect"],
                "attacked_projector_equality_defect",
            ),
            reference_projector_hermiticity_defect=_decoded_float(
                values["reference_projector_hermiticity_defect"],
                "reference_projector_hermiticity_defect",
            ),
            reference_projector_idempotency_defect=_decoded_float(
                values["reference_projector_idempotency_defect"],
                "reference_projector_idempotency_defect",
            ),
            reference_operator_recovery_defect=_decoded_float(
                values["reference_operator_recovery_defect"],
                "reference_operator_recovery_defect",
            ),
            reference_spectrum_recovery_defect=_decoded_float(
                values["reference_spectrum_recovery_defect"],
                "reference_spectrum_recovery_defect",
            ),
            attacked_operator_recovery_defect=_decoded_float(
                values["attacked_operator_recovery_defect"],
                "attacked_operator_recovery_defect",
            ),
            attacked_spectrum_recovery_defect=_decoded_float(
                values["attacked_spectrum_recovery_defect"],
                "attacked_spectrum_recovery_defect",
            ),
            oracle_frame_recovery_defect=_decoded_float(
                values["oracle_frame_recovery_defect"],
                "oracle_frame_recovery_defect",
            ),
            oracle_operator_recovery_defect=_decoded_float(
                values["oracle_operator_recovery_defect"],
                "oracle_operator_recovery_defect",
            ),
        )


@dataclass(frozen=True, slots=True)
class Periodic1DHigherRankProcrustesDiagnostics(BaseTypedRecord):
    """Retain complete rank and integrity evidence for global or pointwise selection."""

    status: Periodic1DHigherRankAlignmentStatusResult
    selection_mesh_size: int
    cross_singular_values: FloatArray
    numerical_ranks: IntArray
    applied_rank_cutoffs: FloatArray
    rank_margins: FloatArray
    spectral_condition_numbers: tuple[float | None, ...]
    deficient_point_indices: tuple[int, ...]
    deficient_point_count: int
    normalized_optimal_residuals: FloatArray
    normalized_objective_maximum: float | None
    normalized_objective_rms: float | None
    minimum_rank_margin: float | None
    maximum_unitarity_defect: float | None
    maximum_stationarity_defect: float | None
    maximum_objective_identity_defect: float | None
    maximum_psd_defect: float | None
    selected_global_right_unitary: ComplexMatrixQuantity | None
    backend_identifier: str | None
    backend_version: str | None

    def __post_init__(self) -> None:
        if type(self.status) is not Periodic1DHigherRankAlignmentStatusResult:
            raise TypeError("status must be the exact alignment status record")
        if self.status.channel not in (
            Periodic1DHigherRankAlignmentChannel.GLOBAL_UNITARY,
            Periodic1DHigherRankAlignmentChannel.POINTWISE_UNITARY,
        ):
            raise ValueError(
                "Procrustes diagnostics require global or pointwise alignment"
            )
        if type(self.selection_mesh_size) is not int:
            raise TypeError("selection_mesh_size must be a built-in integer")
        if (
            self.selection_mesh_size
            not in Periodic1DHigherRankAlignmentConfiguration.CONSTRUCTION_MESH_SIZES
        ):
            raise ValueError("selection_mesh_size is not a construction mesh")
        singular = _float_array(
            self.cross_singular_values, "cross_singular_values", ndim=2
        )
        ranks = _int_array(self.numerical_ranks, "numerical_ranks")
        cutoffs = _float_array(self.applied_rank_cutoffs, "applied_rank_cutoffs")
        margins = _float_array(self.rank_margins, "rank_margins")
        residuals = _float_array(
            self.normalized_optimal_residuals, "normalized_optimal_residuals"
        )
        unresolved = (
            self.status.status
            is Periodic1DHigherRankAlignmentStatus.NUMERICALLY_UNRESOLVED
        )
        expected_count = (
            0
            if unresolved
            else (
                1
                if self.status.channel
                is Periodic1DHigherRankAlignmentChannel.GLOBAL_UNITARY
                else self.selection_mesh_size
            )
        )
        if singular.shape != (expected_count, self.status.retained_rank):
            raise ValueError(
                "cross_singular_values shape disagrees with channel and rank"
            )
        if (
            ranks.shape != (expected_count,)
            or cutoffs.shape != (expected_count,)
            or margins.shape != (expected_count,)
            or residuals.shape != (expected_count,)
            or type(self.spectral_condition_numbers) is not tuple
            or len(self.spectral_condition_numbers) != expected_count
            or type(self.deficient_point_indices) is not tuple
            or any(type(value) is not int for value in self.deficient_point_indices)
            or type(self.deficient_point_count) is not int
        ):
            raise ValueError(
                "rank, cutoff, and residual arrays must match the selection inventory"
            )
        optional_evidence = (
            self.normalized_objective_maximum,
            self.normalized_objective_rms,
            self.minimum_rank_margin,
            self.maximum_unitarity_defect,
            self.maximum_stationarity_defect,
            self.maximum_objective_identity_defect,
            self.maximum_psd_defect,
            self.selected_global_right_unitary,
            self.backend_identifier,
            self.backend_version,
        )
        if unresolved:
            if any(value is not None for value in optional_evidence):
                raise ValueError(
                    "unresolved Procrustes selection must not claim backend evidence"
                )
        else:
            if (
                bool((singular < 0.0).any())
                or bool((cutoffs < 0.0).any())
                or bool((residuals < 0.0).any())
            ):
                raise ValueError(
                    "singular values, cutoffs, and residuals must be nonnegative"
                )
            if bool((ranks < 0).any()) or bool(
                (ranks > self.status.retained_rank).any()
            ):
                raise ValueError("numerical ranks lie outside the retained dimension")
            expected_margins = np.asarray(singular[:, -1] - cutoffs, dtype=np.float64)
            if not np.array_equal(margins, expected_margins):
                raise ValueError("rank_margins are inconsistent")
            expected_deficient_indices = (
                tuple(
                    int(index)
                    for index in np.flatnonzero(
                        (ranks < self.status.retained_rank) | (margins <= 0.0)
                    )
                )
                if self.status.channel
                is Periodic1DHigherRankAlignmentChannel.POINTWISE_UNITARY
                else ()
            )
            if (
                self.deficient_point_indices != expected_deficient_indices
                or self.deficient_point_count != len(expected_deficient_indices)
            ):
                raise ValueError("deficient point evidence is inconsistent")
            expected_conditions = tuple(
                float(values[0] / values[-1])
                if rank == self.status.retained_rank and values[-1] > cutoff
                else None
                for values, rank, cutoff in zip(singular, ranks, cutoffs, strict=True)
            )
            if self.spectral_condition_numbers != expected_conditions:
                raise ValueError("spectral_condition_numbers are inconsistent")
            if any(
                value is not None
                and (
                    type(value) is not float or not math.isfinite(value) or value < 1.0
                )
                for value in self.spectral_condition_numbers
            ):
                raise ValueError(
                    "spectral condition numbers must be finite floats or None"
                )
            expected_margin = float(np.min(margins))
            if self.minimum_rank_margin != expected_margin:
                raise ValueError("minimum_rank_margin is inconsistent")
            expected_maximum = float(np.max(residuals))
            expected_rms = float(np.sqrt(np.mean(residuals**2)))
            if (
                self.normalized_objective_maximum != expected_maximum
                or self.normalized_objective_rms != expected_rms
            ):
                raise ValueError("normalized objective summaries are inconsistent")
            for value, name in (
                (self.normalized_objective_maximum, "normalized_objective_maximum"),
                (self.normalized_objective_rms, "normalized_objective_rms"),
                (self.maximum_unitarity_defect, "maximum_unitarity_defect"),
                (self.maximum_stationarity_defect, "maximum_stationarity_defect"),
                (
                    self.maximum_objective_identity_defect,
                    "maximum_objective_identity_defect",
                ),
                (self.maximum_psd_defect, "maximum_psd_defect"),
            ):
                if value is None:
                    raise ValueError(f"{name} is required for a resolved selection")
                _finite_nonnegative(value, name)
            if type(self.minimum_rank_margin) is not float or not math.isfinite(
                self.minimum_rank_margin
            ):
                raise ValueError("minimum_rank_margin must be a finite built-in float")
            if (
                self.status.channel
                is Periodic1DHigherRankAlignmentChannel.GLOBAL_UNITARY
                and self.status.status is Periodic1DHigherRankAlignmentStatus.QUALIFIED
            ):
                if type(
                    self.selected_global_right_unitary
                ) is not ComplexMatrixQuantity or not isinstance(
                    self.selected_global_right_unitary.unit, Unitless
                ):
                    raise TypeError(
                        "qualified global selection requires a unitless complex matrix"
                    )
                if self.selected_global_right_unitary.magnitude.shape != (
                    self.status.retained_rank,
                    self.status.retained_rank,
                ):
                    raise ValueError(
                        "global right unitary must match the retained rank"
                    )
            elif self.selected_global_right_unitary is not None:
                raise ValueError(
                    "only qualified global selection retains a right unitary"
                )
            if self.backend_identifier is None or self.backend_version is None:
                raise ValueError("resolved selection requires backend evidence")
            _nonempty(self.backend_identifier, "backend_identifier")
            _nonempty(self.backend_version, "backend_version")
        object.__setattr__(self, "cross_singular_values", singular)
        object.__setattr__(self, "numerical_ranks", ranks)
        object.__setattr__(self, "applied_rank_cutoffs", cutoffs)
        object.__setattr__(self, "rank_margins", margins)
        object.__setattr__(self, "normalized_optimal_residuals", residuals)
        if unresolved and (
            self.deficient_point_indices or self.deficient_point_count != 0
        ):
            raise ValueError(
                "unresolved selection cannot claim deficient point evidence"
            )

    def _mapping(self) -> Mapping[str, SerializableValue]:
        return {
            "status": self.status,
            "selection_mesh_size": self.selection_mesh_size,
            "cross_singular_values": self.cross_singular_values,
            "numerical_ranks": self.numerical_ranks,
            "applied_rank_cutoffs": self.applied_rank_cutoffs,
            "rank_margins": self.rank_margins,
            "spectral_condition_numbers": self.spectral_condition_numbers,
            "deficient_point_indices": self.deficient_point_indices,
            "deficient_point_count": self.deficient_point_count,
            "normalized_optimal_residuals": self.normalized_optimal_residuals,
            "normalized_objective_maximum": self.normalized_objective_maximum,
            "normalized_objective_rms": self.normalized_objective_rms,
            "minimum_rank_margin": self.minimum_rank_margin,
            "maximum_unitarity_defect": self.maximum_unitarity_defect,
            "maximum_stationarity_defect": self.maximum_stationarity_defect,
            "maximum_objective_identity_defect": (
                self.maximum_objective_identity_defect
            ),
            "maximum_psd_defect": self.maximum_psd_defect,
            "selected_global_right_unitary": self.selected_global_right_unitary,
            "backend_identifier": self.backend_identifier,
            "backend_version": self.backend_version,
        }

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        required = {
            "status",
            "selection_mesh_size",
            "cross_singular_values",
            "numerical_ranks",
            "applied_rank_cutoffs",
            "rank_margins",
            "spectral_condition_numbers",
            "deficient_point_indices",
            "deficient_point_count",
            "normalized_optimal_residuals",
            "normalized_objective_maximum",
            "normalized_objective_rms",
            "minimum_rank_margin",
            "maximum_unitarity_defect",
            "maximum_stationarity_defect",
            "maximum_objective_identity_defect",
            "maximum_psd_defect",
            "selected_global_right_unitary",
            "backend_identifier",
            "backend_version",
        }
        if set(values) != required:
            raise ValueError("Procrustes diagnostic fields do not match")
        mesh = values["selection_mesh_size"]
        if type(mesh) is not int:
            raise TypeError("selection_mesh_size must decode to a built-in integer")
        arrays: dict[str, np.ndarray] = {}
        for name in (
            "cross_singular_values",
            "numerical_ranks",
            "applied_rank_cutoffs",
            "rank_margins",
            "normalized_optimal_residuals",
        ):
            value = values[name]
            if not isinstance(value, np.ndarray):
                raise TypeError(f"{name} must decode to numpy.ndarray")
            arrays[name] = value
        floats: dict[str, float | None] = {}
        for name in (
            "normalized_objective_maximum",
            "normalized_objective_rms",
            "minimum_rank_margin",
            "maximum_unitarity_defect",
            "maximum_stationarity_defect",
            "maximum_objective_identity_defect",
            "maximum_psd_defect",
        ):
            value = values[name]
            if value is not None and type(value) is not float:
                raise TypeError(f"{name} must decode to a built-in float or None")
            floats[name] = value
        deficient_indices_value = values["deficient_point_indices"]
        deficient_count = values["deficient_point_count"]
        if not isinstance(deficient_indices_value, tuple) or any(
            type(value) is not int for value in deficient_indices_value
        ):
            raise TypeError("deficient_point_indices must decode to integer tuple")
        if type(deficient_count) is not int:
            raise TypeError("deficient_point_count must decode to built-in int")
        conditions_value = values["spectral_condition_numbers"]
        if not isinstance(conditions_value, tuple) or any(
            value is not None and type(value) is not float for value in conditions_value
        ):
            raise TypeError(
                "spectral_condition_numbers must decode to a tuple of floats or None"
            )
        selected = values["selected_global_right_unitary"]
        if selected is not None and type(selected) is not ComplexMatrixQuantity:
            raise TypeError(
                "selected_global_right_unitary must decode to a complex matrix or None"
            )
        backend_identifier = values["backend_identifier"]
        backend_version = values["backend_version"]
        if backend_identifier is not None and type(backend_identifier) is not str:
            raise TypeError("backend_identifier must decode to a string or None")
        if backend_version is not None and type(backend_version) is not str:
            raise TypeError("backend_version must decode to a string or None")
        return cls(
            status=Periodic1DHigherRankAlignmentStatusResult.from_dict(
                _mapping_value(values["status"], "status")
            ),
            selection_mesh_size=mesh,
            cross_singular_values=arrays["cross_singular_values"],
            numerical_ranks=np.asarray(arrays["numerical_ranks"], dtype=np.int64),
            applied_rank_cutoffs=arrays["applied_rank_cutoffs"],
            rank_margins=arrays["rank_margins"],
            spectral_condition_numbers=conditions_value,
            deficient_point_indices=deficient_indices_value,
            deficient_point_count=deficient_count,
            normalized_optimal_residuals=arrays["normalized_optimal_residuals"],
            selected_global_right_unitary=selected,
            backend_identifier=backend_identifier,
            backend_version=backend_version,
            **floats,
        )


@dataclass(frozen=True, slots=True)
class Periodic1DHigherRankMatrixErrorResult(BaseTypedRecord):
    """Retain one raw and rank/energy-normalized matrix and spectrum error summary."""

    rank: int
    energy_reference: float
    matrix_frobenius_maximum: float
    matrix_frobenius_rms: float
    normalized_matrix_frobenius_maximum: float
    normalized_matrix_frobenius_rms: float
    ordered_spectrum_maximum: float
    ordered_spectrum_l2_rms: float
    normalized_ordered_spectrum_maximum: float
    normalized_ordered_spectrum_l2_rms: float

    def __post_init__(self) -> None:
        MatrixFieldErrorSummary(
            rank=self.rank,
            energy_reference=self.energy_reference,
            matrix_frobenius_maximum=self.matrix_frobenius_maximum,
            matrix_frobenius_rms=self.matrix_frobenius_rms,
            normalized_matrix_frobenius_maximum=(
                self.normalized_matrix_frobenius_maximum
            ),
            normalized_matrix_frobenius_rms=self.normalized_matrix_frobenius_rms,
            ordered_spectrum_maximum=self.ordered_spectrum_maximum,
            ordered_spectrum_l2_rms=self.ordered_spectrum_l2_rms,
            normalized_ordered_spectrum_maximum=(
                self.normalized_ordered_spectrum_maximum
            ),
            normalized_ordered_spectrum_l2_rms=(
                self.normalized_ordered_spectrum_l2_rms
            ),
        )

    @classmethod
    def from_diagnostics(cls, value: MatrixFieldErrorSummary) -> Self:
        """Copy one validated matrix-field diagnostic onto the calculation wire."""
        if type(value) is not MatrixFieldErrorSummary:
            raise TypeError("value must be MatrixFieldErrorSummary")
        return cls(
            rank=value.rank,
            energy_reference=value.energy_reference,
            matrix_frobenius_maximum=value.matrix_frobenius_maximum,
            matrix_frobenius_rms=value.matrix_frobenius_rms,
            normalized_matrix_frobenius_maximum=(
                value.normalized_matrix_frobenius_maximum
            ),
            normalized_matrix_frobenius_rms=value.normalized_matrix_frobenius_rms,
            ordered_spectrum_maximum=value.ordered_spectrum_maximum,
            ordered_spectrum_l2_rms=value.ordered_spectrum_l2_rms,
            normalized_ordered_spectrum_maximum=(
                value.normalized_ordered_spectrum_maximum
            ),
            normalized_ordered_spectrum_l2_rms=(
                value.normalized_ordered_spectrum_l2_rms
            ),
        )

    def _mapping(self) -> Mapping[str, SerializableValue]:
        return {
            "rank": self.rank,
            "energy_reference": self.energy_reference,
            "matrix_frobenius_maximum": self.matrix_frobenius_maximum,
            "matrix_frobenius_rms": self.matrix_frobenius_rms,
            "normalized_matrix_frobenius_maximum": (
                self.normalized_matrix_frobenius_maximum
            ),
            "normalized_matrix_frobenius_rms": (self.normalized_matrix_frobenius_rms),
            "ordered_spectrum_maximum": self.ordered_spectrum_maximum,
            "ordered_spectrum_l2_rms": self.ordered_spectrum_l2_rms,
            "normalized_ordered_spectrum_maximum": (
                self.normalized_ordered_spectrum_maximum
            ),
            "normalized_ordered_spectrum_l2_rms": (
                self.normalized_ordered_spectrum_l2_rms
            ),
        }

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        if set(values) != {
            "rank",
            "energy_reference",
            "matrix_frobenius_maximum",
            "matrix_frobenius_rms",
            "normalized_matrix_frobenius_maximum",
            "normalized_matrix_frobenius_rms",
            "ordered_spectrum_maximum",
            "ordered_spectrum_l2_rms",
            "normalized_ordered_spectrum_maximum",
            "normalized_ordered_spectrum_l2_rms",
        }:
            raise ValueError("matrix error fields do not match")
        rank = values["rank"]
        if type(rank) is not int:
            raise TypeError("rank must decode to a built-in integer")
        return cls(
            rank=rank,
            energy_reference=_decoded_float(
                values["energy_reference"], "energy_reference"
            ),
            matrix_frobenius_maximum=_decoded_float(
                values["matrix_frobenius_maximum"], "matrix_frobenius_maximum"
            ),
            matrix_frobenius_rms=_decoded_float(
                values["matrix_frobenius_rms"], "matrix_frobenius_rms"
            ),
            normalized_matrix_frobenius_maximum=_decoded_float(
                values["normalized_matrix_frobenius_maximum"],
                "normalized_matrix_frobenius_maximum",
            ),
            normalized_matrix_frobenius_rms=_decoded_float(
                values["normalized_matrix_frobenius_rms"],
                "normalized_matrix_frobenius_rms",
            ),
            ordered_spectrum_maximum=_decoded_float(
                values["ordered_spectrum_maximum"], "ordered_spectrum_maximum"
            ),
            ordered_spectrum_l2_rms=_decoded_float(
                values["ordered_spectrum_l2_rms"], "ordered_spectrum_l2_rms"
            ),
            normalized_ordered_spectrum_maximum=_decoded_float(
                values["normalized_ordered_spectrum_maximum"],
                "normalized_ordered_spectrum_maximum",
            ),
            normalized_ordered_spectrum_l2_rms=_decoded_float(
                values["normalized_ordered_spectrum_l2_rms"],
                "normalized_ordered_spectrum_l2_rms",
            ),
        )


@dataclass(frozen=True, slots=True)
class Periodic1DHigherRankMatrixComparisonResult(BaseTypedRecord):
    """Retain matrix/spectrum errors and pointwise perturbation-bound evidence."""

    errors: Periodic1DHigherRankMatrixErrorResult
    maximum_ordered_spectrum_minus_spectral_norm: float
    maximum_ordered_spectrum_minus_frobenius_norm: float
    maximum_spectral_norm_minus_frobenius_norm: float
    applied_perturbation_bound_tolerance: float
    all_perturbation_bounds_pass: bool
    maximum_band_over_spectral_ratio: float | None
    maximum_band_over_frobenius_ratio: float | None

    def __post_init__(self) -> None:
        if type(self.errors) is not Periodic1DHigherRankMatrixErrorResult:
            raise TypeError("errors must be the exact matrix error record")
        for value, name in (
            (
                self.maximum_ordered_spectrum_minus_spectral_norm,
                "maximum_ordered_spectrum_minus_spectral_norm",
            ),
            (
                self.maximum_ordered_spectrum_minus_frobenius_norm,
                "maximum_ordered_spectrum_minus_frobenius_norm",
            ),
            (
                self.maximum_spectral_norm_minus_frobenius_norm,
                "maximum_spectral_norm_minus_frobenius_norm",
            ),
            (
                self.applied_perturbation_bound_tolerance,
                "applied_perturbation_bound_tolerance",
            ),
        ):
            _finite_nonnegative(value, name)
        if type(self.all_perturbation_bounds_pass) is not bool:
            raise TypeError("all_perturbation_bounds_pass must be a built-in bool")
        observed = max(
            self.maximum_ordered_spectrum_minus_spectral_norm,
            self.maximum_ordered_spectrum_minus_frobenius_norm,
            self.maximum_spectral_norm_minus_frobenius_norm,
        )
        if self.all_perturbation_bounds_pass is not (
            observed <= self.applied_perturbation_bound_tolerance
        ):
            raise ValueError("perturbation-bound disposition is inconsistent")
        for optional_value, name in (
            (
                self.maximum_band_over_spectral_ratio,
                "maximum_band_over_spectral_ratio",
            ),
            (
                self.maximum_band_over_frobenius_ratio,
                "maximum_band_over_frobenius_ratio",
            ),
        ):
            if optional_value is not None:
                _finite_nonnegative(optional_value, name)

    @classmethod
    def from_diagnostics(
        cls,
        value: MatrixFieldComparisonDiagnostics,
        applied_tolerance: float,
    ) -> Self:
        """Copy one matrix comparison and its frozen gate onto the calculation wire."""
        if type(value) is not MatrixFieldComparisonDiagnostics:
            raise TypeError("value must be MatrixFieldComparisonDiagnostics")
        _finite_nonnegative(applied_tolerance, "applied_tolerance")
        bounds = value.perturbation_bounds
        observed = max(
            bounds.maximum_ordered_spectrum_minus_spectral_norm,
            bounds.maximum_ordered_spectrum_minus_frobenius_norm,
            bounds.maximum_spectral_norm_minus_frobenius_norm,
        )
        return cls(
            errors=Periodic1DHigherRankMatrixErrorResult.from_diagnostics(value.errors),
            maximum_ordered_spectrum_minus_spectral_norm=bounds.maximum_ordered_spectrum_minus_spectral_norm,
            maximum_ordered_spectrum_minus_frobenius_norm=bounds.maximum_ordered_spectrum_minus_frobenius_norm,
            maximum_spectral_norm_minus_frobenius_norm=bounds.maximum_spectral_norm_minus_frobenius_norm,
            applied_perturbation_bound_tolerance=applied_tolerance,
            all_perturbation_bounds_pass=observed <= applied_tolerance,
            maximum_band_over_spectral_ratio=bounds.maximum_band_over_spectral_ratio,
            maximum_band_over_frobenius_ratio=bounds.maximum_band_over_frobenius_ratio,
        )

    def _mapping(self) -> Mapping[str, SerializableValue]:
        return {
            "errors": self.errors,
            "maximum_ordered_spectrum_minus_spectral_norm": (
                self.maximum_ordered_spectrum_minus_spectral_norm
            ),
            "maximum_ordered_spectrum_minus_frobenius_norm": (
                self.maximum_ordered_spectrum_minus_frobenius_norm
            ),
            "maximum_spectral_norm_minus_frobenius_norm": (
                self.maximum_spectral_norm_minus_frobenius_norm
            ),
            "applied_perturbation_bound_tolerance": (
                self.applied_perturbation_bound_tolerance
            ),
            "all_perturbation_bounds_pass": self.all_perturbation_bounds_pass,
            "maximum_band_over_spectral_ratio": (self.maximum_band_over_spectral_ratio),
            "maximum_band_over_frobenius_ratio": (
                self.maximum_band_over_frobenius_ratio
            ),
        }

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        if set(values) != {
            "errors",
            "maximum_ordered_spectrum_minus_spectral_norm",
            "maximum_ordered_spectrum_minus_frobenius_norm",
            "maximum_spectral_norm_minus_frobenius_norm",
            "applied_perturbation_bound_tolerance",
            "all_perturbation_bounds_pass",
            "maximum_band_over_spectral_ratio",
            "maximum_band_over_frobenius_ratio",
        }:
            raise ValueError("matrix comparison fields do not match")
        return cls(
            errors=Periodic1DHigherRankMatrixErrorResult.from_dict(
                _mapping_value(values["errors"], "errors")
            ),
            maximum_ordered_spectrum_minus_spectral_norm=_decoded_float(
                values["maximum_ordered_spectrum_minus_spectral_norm"],
                "maximum_ordered_spectrum_minus_spectral_norm",
            ),
            maximum_ordered_spectrum_minus_frobenius_norm=_decoded_float(
                values["maximum_ordered_spectrum_minus_frobenius_norm"],
                "maximum_ordered_spectrum_minus_frobenius_norm",
            ),
            maximum_spectral_norm_minus_frobenius_norm=_decoded_float(
                values["maximum_spectral_norm_minus_frobenius_norm"],
                "maximum_spectral_norm_minus_frobenius_norm",
            ),
            applied_perturbation_bound_tolerance=_decoded_float(
                values["applied_perturbation_bound_tolerance"],
                "applied_perturbation_bound_tolerance",
            ),
            all_perturbation_bounds_pass=_decoded_bool(
                values["all_perturbation_bounds_pass"],
                "all_perturbation_bounds_pass",
            ),
            maximum_band_over_spectral_ratio=_decoded_optional_float(
                values["maximum_band_over_spectral_ratio"],
                "maximum_band_over_spectral_ratio",
            ),
            maximum_band_over_frobenius_ratio=_decoded_optional_float(
                values["maximum_band_over_frobenius_ratio"],
                "maximum_band_over_frobenius_ratio",
            ),
        )


@dataclass(frozen=True, slots=True)
class Periodic1DHigherRankSupportResult(BaseTypedRecord):
    """Retain one declared symmetric support and its separate error channels."""

    maximum_range: int
    retained_translations: tuple[int, ...]
    omitted_squared_frobenius_weight: float
    normalized_omitted_squared_frobenius_weight: float
    omitted_frobenius_l2_norm: float
    normalized_omitted_frobenius_l2_norm: float
    omitted_block_l1_norm: float
    normalized_omitted_block_l1_norm: float
    construction_parseval_relative_defect: float
    construction_parseval_pass: bool
    truncation: Periodic1DHigherRankMatrixComparisonResult
    total: Periodic1DHigherRankMatrixComparisonResult
    error_decomposition_defect: float
    normalized_error_decomposition_defect: float
    error_decomposition_pass: bool

    def __post_init__(self) -> None:
        if (
            type(self.maximum_range) is not int
            or self.maximum_range
            not in Periodic1DHigherRankAlignmentCalculationControls.SUPPORT_RADII
        ):
            raise ValueError("maximum_range must be a frozen built-in support radius")
        if type(self.retained_translations) is not tuple or any(
            type(value) is not int for value in self.retained_translations
        ):
            raise TypeError("retained_translations must be an exact integer tuple")
        if self.retained_translations != tuple(
            range(-self.maximum_range, self.maximum_range + 1)
        ):
            raise ValueError(
                "retained_translations must equal the declared symmetric support"
            )
        for value, name in (
            (
                self.omitted_squared_frobenius_weight,
                "omitted_squared_frobenius_weight",
            ),
            (
                self.normalized_omitted_squared_frobenius_weight,
                "normalized_omitted_squared_frobenius_weight",
            ),
            (self.omitted_frobenius_l2_norm, "omitted_frobenius_l2_norm"),
            (
                self.normalized_omitted_frobenius_l2_norm,
                "normalized_omitted_frobenius_l2_norm",
            ),
            (self.omitted_block_l1_norm, "omitted_block_l1_norm"),
            (
                self.normalized_omitted_block_l1_norm,
                "normalized_omitted_block_l1_norm",
            ),
            (
                self.construction_parseval_relative_defect,
                "construction_parseval_relative_defect",
            ),
            (self.error_decomposition_defect, "error_decomposition_defect"),
            (
                self.normalized_error_decomposition_defect,
                "normalized_error_decomposition_defect",
            ),
        ):
            _finite_nonnegative(value, name)
        if type(self.construction_parseval_pass) is not bool:
            raise TypeError("construction_parseval_pass must be a built-in bool")
        controls = Periodic1DHigherRankAlignmentCalculationControls
        fourier_tolerance = controls.FOURIER_CONSISTENCY_TOLERANCE
        if self.construction_parseval_pass is not (
            self.construction_parseval_relative_defect <= fourier_tolerance
        ):
            raise ValueError("construction Parseval disposition is inconsistent")
        if type(self.error_decomposition_pass) is not bool:
            raise TypeError("error_decomposition_pass must be a built-in bool")
        decomposition_tolerance = controls.ERROR_DECOMPOSITION_TOLERANCE
        if self.error_decomposition_pass is not (
            self.normalized_error_decomposition_defect <= decomposition_tolerance
        ):
            raise ValueError("error-decomposition disposition is inconsistent")
        if (
            type(self.truncation) is not Periodic1DHigherRankMatrixComparisonResult
            or type(self.total) is not Periodic1DHigherRankMatrixComparisonResult
        ):
            raise TypeError("truncation and total must be exact comparison records")

    def _mapping(self) -> Mapping[str, SerializableValue]:
        return {
            "maximum_range": self.maximum_range,
            "retained_translations": self.retained_translations,
            "omitted_squared_frobenius_weight": (self.omitted_squared_frobenius_weight),
            "normalized_omitted_squared_frobenius_weight": (
                self.normalized_omitted_squared_frobenius_weight
            ),
            "omitted_frobenius_l2_norm": self.omitted_frobenius_l2_norm,
            "normalized_omitted_frobenius_l2_norm": (
                self.normalized_omitted_frobenius_l2_norm
            ),
            "omitted_block_l1_norm": self.omitted_block_l1_norm,
            "normalized_omitted_block_l1_norm": (self.normalized_omitted_block_l1_norm),
            "construction_parseval_relative_defect": (
                self.construction_parseval_relative_defect
            ),
            "construction_parseval_pass": self.construction_parseval_pass,
            "truncation": self.truncation,
            "total": self.total,
            "error_decomposition_defect": self.error_decomposition_defect,
            "normalized_error_decomposition_defect": (
                self.normalized_error_decomposition_defect
            ),
            "error_decomposition_pass": self.error_decomposition_pass,
        }

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        if set(values) != {
            "maximum_range",
            "retained_translations",
            "omitted_squared_frobenius_weight",
            "normalized_omitted_squared_frobenius_weight",
            "omitted_frobenius_l2_norm",
            "normalized_omitted_frobenius_l2_norm",
            "omitted_block_l1_norm",
            "normalized_omitted_block_l1_norm",
            "construction_parseval_relative_defect",
            "construction_parseval_pass",
            "truncation",
            "total",
            "error_decomposition_defect",
            "normalized_error_decomposition_defect",
            "error_decomposition_pass",
        }:
            raise ValueError("support result fields do not match")
        maximum_range = values["maximum_range"]
        translations = values["retained_translations"]
        if type(maximum_range) is not int:
            raise TypeError("maximum_range must decode to a built-in integer")
        if not isinstance(translations, tuple) or any(
            type(value) is not int for value in translations
        ):
            raise TypeError("retained_translations must decode to built-in integers")
        return cls(
            maximum_range=maximum_range,
            retained_translations=translations,
            omitted_squared_frobenius_weight=_decoded_float(
                values["omitted_squared_frobenius_weight"],
                "omitted_squared_frobenius_weight",
            ),
            normalized_omitted_squared_frobenius_weight=_decoded_float(
                values["normalized_omitted_squared_frobenius_weight"],
                "normalized_omitted_squared_frobenius_weight",
            ),
            omitted_frobenius_l2_norm=_decoded_float(
                values["omitted_frobenius_l2_norm"], "omitted_frobenius_l2_norm"
            ),
            normalized_omitted_frobenius_l2_norm=_decoded_float(
                values["normalized_omitted_frobenius_l2_norm"],
                "normalized_omitted_frobenius_l2_norm",
            ),
            omitted_block_l1_norm=_decoded_float(
                values["omitted_block_l1_norm"], "omitted_block_l1_norm"
            ),
            normalized_omitted_block_l1_norm=_decoded_float(
                values["normalized_omitted_block_l1_norm"],
                "normalized_omitted_block_l1_norm",
            ),
            construction_parseval_relative_defect=_decoded_float(
                values["construction_parseval_relative_defect"],
                "construction_parseval_relative_defect",
            ),
            construction_parseval_pass=_decoded_bool(
                values["construction_parseval_pass"],
                "construction_parseval_pass",
            ),
            truncation=Periodic1DHigherRankMatrixComparisonResult.from_dict(
                _mapping_value(values["truncation"], "truncation")
            ),
            total=Periodic1DHigherRankMatrixComparisonResult.from_dict(
                _mapping_value(values["total"], "total")
            ),
            error_decomposition_defect=_decoded_float(
                values["error_decomposition_defect"],
                "error_decomposition_defect",
            ),
            normalized_error_decomposition_defect=_decoded_float(
                values["normalized_error_decomposition_defect"],
                "normalized_error_decomposition_defect",
            ),
            error_decomposition_pass=_decoded_bool(
                values["error_decomposition_pass"],
                "error_decomposition_pass",
            ),
        )


@dataclass(frozen=True, slots=True)
class Periodic1DHigherRankFrameErrorResult(BaseTypedRecord):
    """Retain raw and rank-normalized Frobenius errors for one frame field."""

    rank: int
    frobenius_maximum: float
    frobenius_rms: float
    normalized_frobenius_maximum: float
    normalized_frobenius_rms: float

    def __post_init__(self) -> None:
        if type(self.rank) is not int or self.rank <= 0:
            raise ValueError("rank must be a positive built-in integer")
        for value, name in (
            (self.frobenius_maximum, "frobenius_maximum"),
            (self.frobenius_rms, "frobenius_rms"),
            (self.normalized_frobenius_maximum, "normalized_frobenius_maximum"),
            (self.normalized_frobenius_rms, "normalized_frobenius_rms"),
        ):
            _finite_nonnegative(value, name)
        scale = math.sqrt(self.rank)
        if not math.isclose(
            self.frobenius_maximum / scale,
            self.normalized_frobenius_maximum,
            rel_tol=2.0e-15,
            abs_tol=0.0,
        ) or not math.isclose(
            self.frobenius_rms / scale,
            self.normalized_frobenius_rms,
            rel_tol=2.0e-15,
            abs_tol=0.0,
        ):
            raise ValueError("normalized frame errors disagree with rank normalization")

    def _mapping(self) -> Mapping[str, SerializableValue]:
        return {
            "rank": self.rank,
            "frobenius_maximum": self.frobenius_maximum,
            "frobenius_rms": self.frobenius_rms,
            "normalized_frobenius_maximum": self.normalized_frobenius_maximum,
            "normalized_frobenius_rms": self.normalized_frobenius_rms,
        }

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        if set(values) != {
            "rank",
            "frobenius_maximum",
            "frobenius_rms",
            "normalized_frobenius_maximum",
            "normalized_frobenius_rms",
        }:
            raise ValueError("frame error fields do not match")
        rank = values["rank"]
        if type(rank) is not int:
            raise TypeError("rank must decode to a built-in integer")
        return cls(
            rank=rank,
            frobenius_maximum=_decoded_float(
                values["frobenius_maximum"], "frobenius_maximum"
            ),
            frobenius_rms=_decoded_float(values["frobenius_rms"], "frobenius_rms"),
            normalized_frobenius_maximum=_decoded_float(
                values["normalized_frobenius_maximum"],
                "normalized_frobenius_maximum",
            ),
            normalized_frobenius_rms=_decoded_float(
                values["normalized_frobenius_rms"], "normalized_frobenius_rms"
            ),
        )


@dataclass(frozen=True, slots=True)
class Periodic1DHigherRankChannelMeshResult(BaseTypedRecord):
    """Retain one channel's transform, interpolation, locality, and gate evidence."""

    status: Periodic1DHigherRankAlignmentStatusResult
    transform_backend_identifier: str | None
    transform_backend_version: str | None
    fourier_representative_count: int | None
    fourier_representative_inventory_ordered_unique: bool | None
    fourier_inversion_closed: bool | None
    fourier_index_bijection_pass: bool | None
    no_nyquist_disposition: str | None
    coefficient_translations: IntArray
    block_raw_frobenius_norms: FloatArray
    block_normalized_frobenius_norms: FloatArray
    frame_recovery: Periodic1DHigherRankFrameErrorResult | None
    known_frame_recovery_pass: bool | None
    represented_operator_recovery: Periodic1DHigherRankMatrixErrorResult | None
    known_operator_recovery_pass: bool | None
    reconstruction: Periodic1DHigherRankMatrixErrorResult | None
    reconstruction_pass: bool | None
    interpolation: Periodic1DHigherRankMatrixComparisonResult | None
    final_interpolation_operator_pass: bool | None
    final_interpolation_spectrum_pass: bool | None
    parseval_relative_defect: float | None
    parseval_pass: bool | None
    ordinary_hermiticity_defect: float | None
    ordinary_hermiticity_pass: bool | None
    twisted_cyclic_hermiticity_defect: float | None
    twisted_cyclic_hermiticity_pass: bool | None
    supports: tuple[Periodic1DHigherRankSupportResult, ...]
    maximum_tail_increase: float | None
    all_tail_monotonicity_checks_pass: bool | None

    def __post_init__(self) -> None:
        if type(self.status) is not Periodic1DHigherRankAlignmentStatusResult:
            raise TypeError("status must be the exact alignment status record")
        translations = _int_array(
            self.coefficient_translations, "coefficient_translations"
        )
        raw = _float_array(self.block_raw_frobenius_norms, "block_raw_frobenius_norms")
        normalized = _float_array(
            self.block_normalized_frobenius_norms, "block_normalized_frobenius_norms"
        )
        if translations.shape != raw.shape or raw.shape != normalized.shape:
            raise ValueError("block inventories must have one common shape")
        if type(self.supports) is not tuple or any(
            type(value) is not Periodic1DHigherRankSupportResult
            for value in self.supports
        ):
            raise TypeError("supports must contain exact support result records")
        qualified = self.status.status is Periodic1DHigherRankAlignmentStatus.QUALIFIED
        required_values = (
            self.transform_backend_identifier,
            self.transform_backend_version,
            self.fourier_representative_count,
            self.fourier_representative_inventory_ordered_unique,
            self.fourier_inversion_closed,
            self.fourier_index_bijection_pass,
            self.no_nyquist_disposition,
            self.frame_recovery,
            self.represented_operator_recovery,
            self.reconstruction,
            self.reconstruction_pass,
            self.interpolation,
            self.final_interpolation_operator_pass,
            self.final_interpolation_spectrum_pass,
            self.parseval_relative_defect,
            self.parseval_pass,
            self.ordinary_hermiticity_defect,
            self.ordinary_hermiticity_pass,
            self.twisted_cyclic_hermiticity_defect,
            self.twisted_cyclic_hermiticity_pass,
            self.maximum_tail_increase,
            self.all_tail_monotonicity_checks_pass,
        )
        if qualified:
            if any(value is None for value in required_values):
                raise ValueError(
                    "qualified channel requires complete transform diagnostics"
                )
            if (
                tuple(result.maximum_range for result in self.supports)
                != Periodic1DHigherRankAlignmentCalculationControls.SUPPORT_RADII
            ):
                raise ValueError("qualified channel must retain every frozen support")
            expected_translations = np.arange(
                -Periodic1DHigherRankAlignmentCalculationControls.MAXIMUM_RECORDED_BLOCK_RANGE,
                Periodic1DHigherRankAlignmentCalculationControls.MAXIMUM_RECORDED_BLOCK_RANGE
                + 1,
                dtype=np.int64,
            )
            if not np.array_equal(translations, expected_translations):
                raise ValueError(
                    "qualified block inventory must cover the declared recorded range"
                )
            if self.fourier_representative_count != self.status.construction_mesh_size:
                raise ValueError(
                    "Fourier representative count must equal the construction mesh size"
                )
            if (
                self.fourier_representative_inventory_ordered_unique is not True
                or self.fourier_inversion_closed is not True
                or self.fourier_index_bijection_pass is not True
            ):
                raise ValueError("qualified Fourier index identities must pass")
            if self.no_nyquist_disposition != _ODD_CENTERED_NO_NYQUIST_DISPOSITION:
                raise ValueError("odd-mesh no-Nyquist disposition is invalid")
        else:
            if (
                any(value is not None for value in required_values)
                or self.known_frame_recovery_pass is not None
                or self.known_operator_recovery_pass is not None
                or self.supports
                or translations.size
                or raw.size
                or normalized.size
            ):
                raise ValueError(
                    "unqualified channel must not claim downstream diagnostics"
                )
        for value, name in (
            (self.parseval_relative_defect, "parseval_relative_defect"),
            (self.ordinary_hermiticity_defect, "ordinary_hermiticity_defect"),
            (
                self.twisted_cyclic_hermiticity_defect,
                "twisted_cyclic_hermiticity_defect",
            ),
            (self.maximum_tail_increase, "maximum_tail_increase"),
        ):
            if value is not None:
                _finite_nonnegative(value, name)
        for value, name in (
            (
                self.fourier_representative_inventory_ordered_unique,
                "fourier_representative_inventory_ordered_unique",
            ),
            (self.fourier_inversion_closed, "fourier_inversion_closed"),
            (self.fourier_index_bijection_pass, "fourier_index_bijection_pass"),
            (self.known_frame_recovery_pass, "known_frame_recovery_pass"),
            (self.known_operator_recovery_pass, "known_operator_recovery_pass"),
            (self.reconstruction_pass, "reconstruction_pass"),
            (
                self.final_interpolation_operator_pass,
                "final_interpolation_operator_pass",
            ),
            (
                self.final_interpolation_spectrum_pass,
                "final_interpolation_spectrum_pass",
            ),
            (self.parseval_pass, "parseval_pass"),
            (self.ordinary_hermiticity_pass, "ordinary_hermiticity_pass"),
            (
                self.twisted_cyclic_hermiticity_pass,
                "twisted_cyclic_hermiticity_pass",
            ),
            (
                self.all_tail_monotonicity_checks_pass,
                "all_tail_monotonicity_checks_pass",
            ),
        ):
            if value is not None and type(value) is not bool:
                raise TypeError(f"{name} must be bool or None")
        if qualified:
            if (
                self.reconstruction is None
                or self.interpolation is None
                or self.parseval_relative_defect is None
                or self.ordinary_hermiticity_defect is None
                or self.twisted_cyclic_hermiticity_defect is None
            ):
                raise ValueError("qualified channel requires gate evidence")
            controls = Periodic1DHigherRankAlignmentCalculationControls
            tolerance = controls.FOURIER_CONSISTENCY_TOLERANCE
            known_recovery_applicable = self.status.channel in (
                Periodic1DHigherRankAlignmentChannel.POINTWISE_UNITARY,
                Periodic1DHigherRankAlignmentChannel.KNOWN_INVERSE_ORACLE,
            )
            if known_recovery_applicable:
                if (
                    self.frame_recovery is None
                    or self.represented_operator_recovery is None
                ):
                    raise ValueError(
                        "known-recovery channels require recovery evidence"
                    )
                if self.known_frame_recovery_pass is not (
                    self.frame_recovery.normalized_frobenius_maximum
                    <= controls.DIRECT_RECOVERY_TOLERANCE
                ):
                    raise ValueError("known frame-recovery disposition is inconsistent")
                if self.known_operator_recovery_pass is not (
                    self.represented_operator_recovery.normalized_matrix_frobenius_maximum
                    <= controls.DIRECT_RECOVERY_TOLERANCE
                ):
                    raise ValueError(
                        "known operator-recovery disposition is inconsistent"
                    )
            elif (
                self.known_frame_recovery_pass is not None
                or self.known_operator_recovery_pass is not None
            ):
                raise ValueError(
                    "unknown-recovery channels cannot claim known-recovery gates"
                )
            expected_gate_values = (
                (
                    self.reconstruction_pass,
                    self.reconstruction.normalized_matrix_frobenius_maximum
                    <= tolerance,
                ),
                (
                    self.final_interpolation_operator_pass,
                    self.interpolation.errors.normalized_matrix_frobenius_maximum
                    <= controls.FINAL_INTERPOLATION_OPERATOR_TOLERANCE,
                ),
                (
                    self.final_interpolation_spectrum_pass,
                    self.interpolation.errors.normalized_ordered_spectrum_maximum
                    <= controls.FINAL_INTERPOLATION_SPECTRUM_TOLERANCE,
                ),
                (self.parseval_pass, self.parseval_relative_defect <= tolerance),
                (
                    self.ordinary_hermiticity_pass,
                    self.ordinary_hermiticity_defect <= tolerance,
                ),
                (
                    self.twisted_cyclic_hermiticity_pass,
                    self.twisted_cyclic_hermiticity_defect <= tolerance,
                ),
            )
            if any(actual is not expected for actual, expected in expected_gate_values):
                raise ValueError("channel gate disposition is inconsistent")
        for text_value, name in (
            (self.transform_backend_identifier, "transform_backend_identifier"),
            (self.transform_backend_version, "transform_backend_version"),
        ):
            if text_value is not None:
                _nonempty(text_value, name)
        object.__setattr__(self, "coefficient_translations", translations)
        object.__setattr__(self, "block_raw_frobenius_norms", raw)
        object.__setattr__(self, "block_normalized_frobenius_norms", normalized)

    def _mapping(self) -> Mapping[str, SerializableValue]:
        return {
            "status": self.status,
            "transform_backend_identifier": self.transform_backend_identifier,
            "transform_backend_version": self.transform_backend_version,
            "fourier_representative_count": self.fourier_representative_count,
            "fourier_representative_inventory_ordered_unique": (
                self.fourier_representative_inventory_ordered_unique
            ),
            "fourier_inversion_closed": self.fourier_inversion_closed,
            "fourier_index_bijection_pass": self.fourier_index_bijection_pass,
            "no_nyquist_disposition": self.no_nyquist_disposition,
            "coefficient_translations": self.coefficient_translations,
            "block_raw_frobenius_norms": self.block_raw_frobenius_norms,
            "block_normalized_frobenius_norms": (self.block_normalized_frobenius_norms),
            "frame_recovery": self.frame_recovery,
            "known_frame_recovery_pass": self.known_frame_recovery_pass,
            "represented_operator_recovery": self.represented_operator_recovery,
            "known_operator_recovery_pass": self.known_operator_recovery_pass,
            "reconstruction": self.reconstruction,
            "reconstruction_pass": self.reconstruction_pass,
            "interpolation": self.interpolation,
            "final_interpolation_operator_pass": (
                self.final_interpolation_operator_pass
            ),
            "final_interpolation_spectrum_pass": (
                self.final_interpolation_spectrum_pass
            ),
            "parseval_relative_defect": self.parseval_relative_defect,
            "parseval_pass": self.parseval_pass,
            "ordinary_hermiticity_defect": self.ordinary_hermiticity_defect,
            "ordinary_hermiticity_pass": self.ordinary_hermiticity_pass,
            "twisted_cyclic_hermiticity_defect": (
                self.twisted_cyclic_hermiticity_defect
            ),
            "twisted_cyclic_hermiticity_pass": (self.twisted_cyclic_hermiticity_pass),
            "supports": self.supports,
            "maximum_tail_increase": self.maximum_tail_increase,
            "all_tail_monotonicity_checks_pass": (
                self.all_tail_monotonicity_checks_pass
            ),
        }

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        if set(values) != {
            "status",
            "transform_backend_identifier",
            "transform_backend_version",
            "fourier_representative_count",
            "fourier_representative_inventory_ordered_unique",
            "fourier_inversion_closed",
            "fourier_index_bijection_pass",
            "no_nyquist_disposition",
            "coefficient_translations",
            "block_raw_frobenius_norms",
            "block_normalized_frobenius_norms",
            "frame_recovery",
            "known_frame_recovery_pass",
            "represented_operator_recovery",
            "known_operator_recovery_pass",
            "reconstruction",
            "reconstruction_pass",
            "interpolation",
            "final_interpolation_operator_pass",
            "final_interpolation_spectrum_pass",
            "parseval_relative_defect",
            "parseval_pass",
            "ordinary_hermiticity_defect",
            "ordinary_hermiticity_pass",
            "twisted_cyclic_hermiticity_defect",
            "twisted_cyclic_hermiticity_pass",
            "supports",
            "maximum_tail_increase",
            "all_tail_monotonicity_checks_pass",
        }:
            raise ValueError("channel mesh fields do not match")
        arrays: dict[str, np.ndarray] = {}
        for name in (
            "coefficient_translations",
            "block_raw_frobenius_norms",
            "block_normalized_frobenius_norms",
        ):
            value = values[name]
            if not isinstance(value, np.ndarray):
                raise TypeError(f"{name} must decode to numpy.ndarray")
            arrays[name] = value
        optional_strings: dict[str, str | None] = {}
        for name in (
            "transform_backend_identifier",
            "transform_backend_version",
            "no_nyquist_disposition",
        ):
            value = values[name]
            if value is not None and type(value) is not str:
                raise TypeError(f"{name} must decode to string or None")
            optional_strings[name] = value
        optional_floats: dict[str, float | None] = {}
        for name in (
            "parseval_relative_defect",
            "ordinary_hermiticity_defect",
            "twisted_cyclic_hermiticity_defect",
            "maximum_tail_increase",
        ):
            value = values[name]
            if value is not None and type(value) is not float:
                raise TypeError(f"{name} must decode to float or None")
            optional_floats[name] = value
        optional_bools: dict[str, bool | None] = {}
        for name in (
            "fourier_representative_inventory_ordered_unique",
            "fourier_inversion_closed",
            "fourier_index_bijection_pass",
            "known_frame_recovery_pass",
            "known_operator_recovery_pass",
            "reconstruction_pass",
            "final_interpolation_operator_pass",
            "final_interpolation_spectrum_pass",
            "parseval_pass",
            "ordinary_hermiticity_pass",
            "twisted_cyclic_hermiticity_pass",
            "all_tail_monotonicity_checks_pass",
        ):
            value = values[name]
            if value is not None and type(value) is not bool:
                raise TypeError(f"{name} must decode to bool or None")
            optional_bools[name] = value
        representative_count = values["fourier_representative_count"]
        if representative_count is not None and type(representative_count) is not int:
            raise TypeError(
                "fourier_representative_count must decode to built-in int or None"
            )
        frame_recovery_value = values["frame_recovery"]
        represented_operator_recovery_value = values["represented_operator_recovery"]
        reconstruction_value = values["reconstruction"]
        interpolation_value = values["interpolation"]
        supports = tuple(
            Periodic1DHigherRankSupportResult.from_dict(item)
            for item in _tuple_of_mappings(values["supports"], "supports")
        )
        return cls(
            status=Periodic1DHigherRankAlignmentStatusResult.from_dict(
                _mapping_value(values["status"], "status")
            ),
            fourier_representative_count=representative_count,
            fourier_representative_inventory_ordered_unique=optional_bools[
                "fourier_representative_inventory_ordered_unique"
            ],
            fourier_inversion_closed=optional_bools["fourier_inversion_closed"],
            fourier_index_bijection_pass=optional_bools["fourier_index_bijection_pass"],
            no_nyquist_disposition=optional_strings["no_nyquist_disposition"],
            coefficient_translations=np.asarray(
                arrays["coefficient_translations"], dtype=np.int64
            ),
            block_raw_frobenius_norms=arrays["block_raw_frobenius_norms"],
            block_normalized_frobenius_norms=arrays["block_normalized_frobenius_norms"],
            frame_recovery=None
            if frame_recovery_value is None
            else Periodic1DHigherRankFrameErrorResult.from_dict(
                _mapping_value(frame_recovery_value, "frame_recovery")
            ),
            known_frame_recovery_pass=optional_bools["known_frame_recovery_pass"],
            represented_operator_recovery=None
            if represented_operator_recovery_value is None
            else Periodic1DHigherRankMatrixErrorResult.from_dict(
                _mapping_value(
                    represented_operator_recovery_value,
                    "represented_operator_recovery",
                )
            ),
            known_operator_recovery_pass=optional_bools["known_operator_recovery_pass"],
            reconstruction=None
            if reconstruction_value is None
            else Periodic1DHigherRankMatrixErrorResult.from_dict(
                _mapping_value(reconstruction_value, "reconstruction")
            ),
            interpolation=None
            if interpolation_value is None
            else Periodic1DHigherRankMatrixComparisonResult.from_dict(
                _mapping_value(interpolation_value, "interpolation")
            ),
            supports=supports,
            reconstruction_pass=optional_bools["reconstruction_pass"],
            final_interpolation_operator_pass=optional_bools[
                "final_interpolation_operator_pass"
            ],
            final_interpolation_spectrum_pass=optional_bools[
                "final_interpolation_spectrum_pass"
            ],
            parseval_pass=optional_bools["parseval_pass"],
            ordinary_hermiticity_pass=optional_bools["ordinary_hermiticity_pass"],
            twisted_cyclic_hermiticity_pass=optional_bools[
                "twisted_cyclic_hermiticity_pass"
            ],
            all_tail_monotonicity_checks_pass=optional_bools[
                "all_tail_monotonicity_checks_pass"
            ],
            transform_backend_identifier=optional_strings[
                "transform_backend_identifier"
            ],
            transform_backend_version=optional_strings["transform_backend_version"],
            parseval_relative_defect=optional_floats["parseval_relative_defect"],
            ordinary_hermiticity_defect=optional_floats["ordinary_hermiticity_defect"],
            twisted_cyclic_hermiticity_defect=optional_floats[
                "twisted_cyclic_hermiticity_defect"
            ],
            maximum_tail_increase=optional_floats["maximum_tail_increase"],
        )


@dataclass(frozen=True, slots=True)
class Periodic1DHigherRankMeshCalculationResult(BaseTypedRecord):
    """Retain one construction-mesh calculation with common transport evidence."""

    construction_mesh_size: int
    model_diagnostics: Periodic1DHigherRankModelDiagnostics
    transport: Periodic1DHigherRankAlignmentTransportOwnerResult | None
    transport_backend_failure: (
        Periodic1DHigherRankAlignmentTransportBackendFailureResult | None
    )
    endpoint_closure_defect: float | None
    primitive_closure_defect: float | None
    pointwise_selection: Periodic1DHigherRankProcrustesDiagnostics
    channels: tuple[Periodic1DHigherRankChannelMeshResult, ...]

    def __post_init__(self) -> None:
        if (
            type(self.construction_mesh_size) is not int
            or self.construction_mesh_size
            not in Periodic1DHigherRankAlignmentConfiguration.CONSTRUCTION_MESH_SIZES
        ):
            raise ValueError("construction_mesh_size must be a frozen mesh size")
        if type(self.model_diagnostics) is not Periodic1DHigherRankModelDiagnostics:
            raise TypeError(
                "model_diagnostics must be the exact model diagnostic record"
            )
        if (self.transport is None) == (self.transport_backend_failure is None):
            raise ValueError(
                "exactly one transport outcome or backend failure is required"
            )
        if self.transport is not None:
            if (
                type(self.transport)
                is not Periodic1DHigherRankAlignmentTransportOwnerResult
                or self.transport.construction_mesh_size != self.construction_mesh_size
            ):
                raise ValueError("transport result must match the construction mesh")
            if (
                self.endpoint_closure_defect is None
                or self.primitive_closure_defect is None
            ):
                raise ValueError(
                    "transport outcome requires normalized closure defects"
                )
        else:
            if (
                type(self.transport_backend_failure)
                is not Periodic1DHigherRankAlignmentTransportBackendFailureResult
            ):
                raise TypeError("transport_backend_failure must be its exact record")
            if (
                self.endpoint_closure_defect is not None
                or self.primitive_closure_defect is not None
            ):
                raise ValueError("failed transport must not claim closure defects")
        for value, name in (
            (self.endpoint_closure_defect, "endpoint_closure_defect"),
            (self.primitive_closure_defect, "primitive_closure_defect"),
        ):
            if value is not None:
                _finite_nonnegative(value, name)
        if (
            type(self.pointwise_selection)
            is not Periodic1DHigherRankProcrustesDiagnostics
            or self.pointwise_selection.selection_mesh_size
            != self.construction_mesh_size
        ):
            raise ValueError("pointwise selection must match this construction mesh")
        if (
            type(self.channels) is not tuple
            or tuple(item.status.channel for item in self.channels)
            != Periodic1DHigherRankAlignmentConfiguration.ALIGNMENT_CHANNELS
        ):
            raise ValueError("channels must use the frozen semantic order")
        if any(
            item.status.construction_mesh_size != self.construction_mesh_size
            for item in self.channels
        ):
            raise ValueError("every channel status must match the construction mesh")

    def _mapping(self) -> Mapping[str, SerializableValue]:
        return {
            "construction_mesh_size": self.construction_mesh_size,
            "model_diagnostics": self.model_diagnostics,
            "transport": self.transport,
            "transport_backend_failure": self.transport_backend_failure,
            "endpoint_closure_defect": self.endpoint_closure_defect,
            "primitive_closure_defect": self.primitive_closure_defect,
            "pointwise_selection": self.pointwise_selection,
            "channels": self.channels,
        }

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        if set(values) != {
            "construction_mesh_size",
            "model_diagnostics",
            "transport",
            "transport_backend_failure",
            "endpoint_closure_defect",
            "primitive_closure_defect",
            "pointwise_selection",
            "channels",
        }:
            raise ValueError("mesh calculation fields do not match")
        mesh = values["construction_mesh_size"]
        if type(mesh) is not int:
            raise TypeError("construction_mesh_size must decode to an integer")
        transport_value = values["transport"]
        failure_value = values["transport_backend_failure"]
        endpoint = values["endpoint_closure_defect"]
        primitive = values["primitive_closure_defect"]
        for value, name in (
            (endpoint, "endpoint_closure_defect"),
            (primitive, "primitive_closure_defect"),
        ):
            if value is not None and type(value) is not float:
                raise TypeError(f"{name} must decode to float or None")
        return cls(
            construction_mesh_size=mesh,
            model_diagnostics=Periodic1DHigherRankModelDiagnostics.from_dict(
                _mapping_value(values["model_diagnostics"], "model_diagnostics")
            ),
            transport=None
            if transport_value is None
            else Periodic1DHigherRankAlignmentTransportOwnerResult.from_dict(
                _mapping_value(transport_value, "transport")
            ),
            transport_backend_failure=None
            if failure_value is None
            else Periodic1DHigherRankAlignmentTransportBackendFailureResult.from_dict(
                _mapping_value(failure_value, "transport_backend_failure")
            ),
            endpoint_closure_defect=_decoded_optional_float(
                endpoint, "endpoint_closure_defect"
            ),
            primitive_closure_defect=_decoded_optional_float(
                primitive, "primitive_closure_defect"
            ),
            pointwise_selection=Periodic1DHigherRankProcrustesDiagnostics.from_dict(
                _mapping_value(values["pointwise_selection"], "pointwise_selection")
            ),
            channels=tuple(
                Periodic1DHigherRankChannelMeshResult.from_dict(item)
                for item in _tuple_of_mappings(values["channels"], "channels")
            ),
        )


@dataclass(frozen=True, slots=True)
class Periodic1DHigherRankBlockRefinementResult(BaseTypedRecord):
    """Retain all recorded block-norm changes for one channel and mesh pair."""

    channel: Periodic1DHigherRankAlignmentChannel
    coarse_mesh_size: int
    fine_mesh_size: int
    translations: IntArray
    coarse_normalized_block_norms: FloatArray
    fine_normalized_block_norms: FloatArray
    absolute_changes: FloatArray
    relative_changes: FloatArray
    applied_tolerances: FloatArray
    signed_margins: FloatArray
    all_pass: bool

    def __post_init__(self) -> None:
        if type(self.channel) is not Periodic1DHigherRankAlignmentChannel:
            raise TypeError("channel must be the exact alignment enum")
        if (
            type(self.coarse_mesh_size) is not int
            or type(self.fine_mesh_size) is not int
            or not self.coarse_mesh_size < self.fine_mesh_size
        ):
            raise ValueError("mesh sizes must be increasing built-in integers")
        translations = _int_array(self.translations, "translations")
        arrays = [
            _float_array(
                self.coarse_normalized_block_norms,
                "coarse_normalized_block_norms",
            ),
            _float_array(
                self.fine_normalized_block_norms,
                "fine_normalized_block_norms",
            ),
            _float_array(self.absolute_changes, "absolute_changes"),
            _float_array(self.relative_changes, "relative_changes"),
            _float_array(self.applied_tolerances, "applied_tolerances"),
            _float_array(self.signed_margins, "signed_margins"),
        ]
        if any(array.shape != translations.shape for array in arrays):
            raise ValueError("refinement arrays must share the translation shape")
        if type(self.all_pass) is not bool:
            raise TypeError("all_pass must be a built-in bool")
        if self.all_pass is not bool(np.all(arrays[-1] >= 0.0)):
            raise ValueError("all_pass must agree with signed margins")
        object.__setattr__(self, "translations", translations)
        object.__setattr__(self, "coarse_normalized_block_norms", arrays[0])
        object.__setattr__(self, "fine_normalized_block_norms", arrays[1])
        object.__setattr__(self, "absolute_changes", arrays[2])
        object.__setattr__(self, "relative_changes", arrays[3])
        object.__setattr__(self, "applied_tolerances", arrays[4])
        object.__setattr__(self, "signed_margins", arrays[5])

    def _mapping(self) -> Mapping[str, SerializableValue]:
        return {
            "channel": self.channel.value,
            "coarse_mesh_size": self.coarse_mesh_size,
            "fine_mesh_size": self.fine_mesh_size,
            "translations": self.translations,
            "coarse_normalized_block_norms": self.coarse_normalized_block_norms,
            "fine_normalized_block_norms": self.fine_normalized_block_norms,
            "absolute_changes": self.absolute_changes,
            "relative_changes": self.relative_changes,
            "applied_tolerances": self.applied_tolerances,
            "signed_margins": self.signed_margins,
            "all_pass": self.all_pass,
        }

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        required = {
            "channel",
            "coarse_mesh_size",
            "fine_mesh_size",
            "translations",
            "coarse_normalized_block_norms",
            "fine_normalized_block_norms",
            "absolute_changes",
            "relative_changes",
            "applied_tolerances",
            "signed_margins",
            "all_pass",
        }
        if set(values) != required:
            raise ValueError("block refinement fields do not match")
        channel = values["channel"]
        coarse = values["coarse_mesh_size"]
        fine = values["fine_mesh_size"]
        all_pass = values["all_pass"]
        if (
            type(channel) is not str
            or type(coarse) is not int
            or type(fine) is not int
            or type(all_pass) is not bool
        ):
            raise TypeError(
                "refinement identities and disposition have wrong decoded types"
            )
        arrays: dict[str, np.ndarray] = {}
        for name in required - {
            "channel",
            "coarse_mesh_size",
            "fine_mesh_size",
            "all_pass",
        }:
            value = values[name]
            if not isinstance(value, np.ndarray):
                raise TypeError(f"{name} must decode to numpy.ndarray")
            arrays[name] = value
        return cls(
            channel=Periodic1DHigherRankAlignmentChannel(channel),
            coarse_mesh_size=coarse,
            fine_mesh_size=fine,
            all_pass=all_pass,
            translations=np.asarray(arrays["translations"], dtype=np.int64),
            coarse_normalized_block_norms=arrays["coarse_normalized_block_norms"],
            fine_normalized_block_norms=arrays["fine_normalized_block_norms"],
            absolute_changes=arrays["absolute_changes"],
            relative_changes=arrays["relative_changes"],
            applied_tolerances=arrays["applied_tolerances"],
            signed_margins=arrays["signed_margins"],
        )


@dataclass(frozen=True, slots=True)
class Periodic1DHigherRankScalarRefinementResult(BaseTypedRecord):
    """Retain one final-mesh scalar refinement value and frozen gate."""

    channel: Periodic1DHigherRankAlignmentChannel
    diagnostic_path: str
    coarse_mesh_size: int
    fine_mesh_size: int
    coarse_value: float
    fine_value: float
    absolute_change: float
    relative_change: float
    applied_tolerance: float
    signed_margin: float
    passes: bool

    def __post_init__(self) -> None:
        if type(self.channel) is not Periodic1DHigherRankAlignmentChannel:
            raise TypeError("channel must be the exact alignment enum")
        _nonempty(self.diagnostic_path, "diagnostic_path")
        if (self.coarse_mesh_size, self.fine_mesh_size) != (1025, 2049):
            raise ValueError("scalar refinement must use the frozen final mesh pair")
        for value, name in (
            (self.coarse_value, "coarse_value"),
            (self.fine_value, "fine_value"),
            (self.absolute_change, "absolute_change"),
            (self.relative_change, "relative_change"),
            (self.applied_tolerance, "applied_tolerance"),
        ):
            _finite_nonnegative(value, name)
        if type(self.signed_margin) is not float or not math.isfinite(
            self.signed_margin
        ):
            raise ValueError("signed_margin must be a finite built-in float")
        expected_change = abs(self.fine_value - self.coarse_value)
        expected_relative = expected_change / max(
            abs(self.coarse_value),
            abs(self.fine_value),
            Periodic1DHigherRankAlignmentCalculationControls.REFINEMENT_DENOMINATOR_FLOOR,
        )
        controls = Periodic1DHigherRankAlignmentCalculationControls
        expected_tolerance = controls.REFINEMENT_ABSOLUTE_TOLERANCE + (
            controls.REFINEMENT_RELATIVE_TOLERANCE
            * max(abs(self.coarse_value), abs(self.fine_value))
        )
        if (
            self.absolute_change != expected_change
            or self.relative_change != expected_relative
            or self.applied_tolerance != expected_tolerance
            or self.signed_margin != expected_tolerance - expected_change
        ):
            raise ValueError("scalar refinement arithmetic is inconsistent")
        if type(self.passes) is not bool or self.passes is not (
            self.signed_margin >= 0.0
        ):
            raise ValueError("scalar refinement disposition is inconsistent")

    def _mapping(self) -> Mapping[str, SerializableValue]:
        return {
            "channel": self.channel.value,
            "diagnostic_path": self.diagnostic_path,
            "coarse_mesh_size": self.coarse_mesh_size,
            "fine_mesh_size": self.fine_mesh_size,
            "coarse_value": self.coarse_value,
            "fine_value": self.fine_value,
            "absolute_change": self.absolute_change,
            "relative_change": self.relative_change,
            "applied_tolerance": self.applied_tolerance,
            "signed_margin": self.signed_margin,
            "passes": self.passes,
        }

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        required = {
            "channel",
            "diagnostic_path",
            "coarse_mesh_size",
            "fine_mesh_size",
            "coarse_value",
            "fine_value",
            "absolute_change",
            "relative_change",
            "applied_tolerance",
            "signed_margin",
            "passes",
        }
        if set(values) != required:
            raise ValueError("scalar refinement fields do not match")
        channel = values["channel"]
        path = values["diagnostic_path"]
        coarse = values["coarse_mesh_size"]
        fine = values["fine_mesh_size"]
        passes = values["passes"]
        if type(channel) is not str or type(path) is not str:
            raise TypeError("scalar refinement identities must decode to strings")
        if type(coarse) is not int or type(fine) is not int:
            raise TypeError("scalar refinement mesh sizes must decode to integers")
        if type(passes) is not bool:
            raise TypeError("scalar refinement passes must decode to bool")
        floats: dict[str, float] = {}
        for name in required - {
            "channel",
            "diagnostic_path",
            "coarse_mesh_size",
            "fine_mesh_size",
            "passes",
        }:
            floats[name] = _decoded_float(values[name], name)
        return cls(
            channel=Periodic1DHigherRankAlignmentChannel(channel),
            diagnostic_path=path,
            coarse_mesh_size=coarse,
            fine_mesh_size=fine,
            passes=passes,
            **floats,
        )


@dataclass(frozen=True, slots=True)
class Periodic1DHigherRankEvaluationIndependenceResult(BaseTypedRecord):
    """Retain exact mesh separation and selection-input provenance."""

    construction_mesh_sizes: tuple[int, ...]
    evaluation_mesh_size: int
    evaluation_shift_numerator: int
    evaluation_shift_denominator: int
    global_selection_mesh_size: int
    pointwise_selection_mesh_sizes: tuple[int, ...]
    construction_evaluation_disjoint: bool
    evaluation_mesh_excluded_from_selection: bool

    def __post_init__(self) -> None:
        configuration = Periodic1DHigherRankAlignmentConfiguration
        if self.construction_mesh_sizes != configuration.CONSTRUCTION_MESH_SIZES:
            raise ValueError("construction mesh provenance must match the protocol")
        if self.evaluation_mesh_size != configuration.EVALUATION_MESH_SIZE:
            raise ValueError("evaluation mesh provenance must match the protocol")
        if (
            self.evaluation_shift_numerator != configuration.EVALUATION_SHIFT_NUMERATOR
            or self.evaluation_shift_denominator
            != configuration.EVALUATION_SHIFT_DENOMINATOR
        ):
            raise ValueError("evaluation shift provenance must match the protocol")
        if (
            self.global_selection_mesh_size
            != configuration.GLOBAL_UNITARY_SELECTION_MESH_SIZE
        ):
            raise ValueError("global selection provenance must match the protocol")
        if self.pointwise_selection_mesh_sizes != self.construction_mesh_sizes:
            raise ValueError("pointwise selection must use every construction mesh")
        if type(self.construction_evaluation_disjoint) is not bool:
            raise TypeError("construction_evaluation_disjoint must be a built-in bool")
        if self.construction_evaluation_disjoint is not True:
            raise ValueError("construction and evaluation coordinates must be disjoint")
        if type(self.evaluation_mesh_excluded_from_selection) is not bool:
            raise TypeError(
                "evaluation_mesh_excluded_from_selection must be a built-in bool"
            )
        expected_exclusion = (
            self.evaluation_mesh_size != self.global_selection_mesh_size
            and self.evaluation_mesh_size not in self.pointwise_selection_mesh_sizes
        )
        if self.evaluation_mesh_excluded_from_selection is not expected_exclusion:
            raise ValueError("selection-input mesh provenance is inconsistent")
        if self.evaluation_mesh_excluded_from_selection is not True:
            raise ValueError("evaluation mesh must not be a selection input")

    def _mapping(self) -> Mapping[str, SerializableValue]:
        return {
            "construction_mesh_sizes": self.construction_mesh_sizes,
            "evaluation_mesh_size": self.evaluation_mesh_size,
            "evaluation_shift_numerator": self.evaluation_shift_numerator,
            "evaluation_shift_denominator": self.evaluation_shift_denominator,
            "global_selection_mesh_size": self.global_selection_mesh_size,
            "pointwise_selection_mesh_sizes": self.pointwise_selection_mesh_sizes,
            "construction_evaluation_disjoint": (self.construction_evaluation_disjoint),
            "evaluation_mesh_excluded_from_selection": (
                self.evaluation_mesh_excluded_from_selection
            ),
        }

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        if set(values) != {
            "construction_mesh_sizes",
            "evaluation_mesh_size",
            "evaluation_shift_numerator",
            "evaluation_shift_denominator",
            "global_selection_mesh_size",
            "pointwise_selection_mesh_sizes",
            "construction_evaluation_disjoint",
            "evaluation_mesh_excluded_from_selection",
        }:
            raise ValueError("evaluation-independence fields do not match")
        construction_sizes = values["construction_mesh_sizes"]
        pointwise_sizes = values["pointwise_selection_mesh_sizes"]
        if not isinstance(construction_sizes, tuple) or any(
            type(value) is not int for value in construction_sizes
        ):
            raise TypeError("construction mesh sizes must decode to integers")
        if not isinstance(pointwise_sizes, tuple) or any(
            type(value) is not int for value in pointwise_sizes
        ):
            raise TypeError("pointwise selection mesh sizes must decode to integers")
        return cls(
            construction_mesh_sizes=construction_sizes,
            evaluation_mesh_size=_decoded_int(
                values["evaluation_mesh_size"], "evaluation_mesh_size"
            ),
            evaluation_shift_numerator=_decoded_int(
                values["evaluation_shift_numerator"],
                "evaluation_shift_numerator",
            ),
            evaluation_shift_denominator=_decoded_int(
                values["evaluation_shift_denominator"],
                "evaluation_shift_denominator",
            ),
            global_selection_mesh_size=_decoded_int(
                values["global_selection_mesh_size"],
                "global_selection_mesh_size",
            ),
            pointwise_selection_mesh_sizes=pointwise_sizes,
            construction_evaluation_disjoint=_decoded_bool(
                values["construction_evaluation_disjoint"],
                "construction_evaluation_disjoint",
            ),
            evaluation_mesh_excluded_from_selection=_decoded_bool(
                values["evaluation_mesh_excluded_from_selection"],
                "evaluation_mesh_excluded_from_selection",
            ),
        )


@dataclass(frozen=True, slots=True)
class Periodic1DHigherRankAlignmentCalculationResult(BaseTypedRecord):
    """Retain one complete request-bound rank/depth calculation."""

    request: Periodic1DHigherRankAlignmentCalculationRequest
    global_selection: Periodic1DHigherRankProcrustesDiagnostics
    meshes: tuple[Periodic1DHigherRankMeshCalculationResult, ...]
    evaluation_independence: Periodic1DHigherRankEvaluationIndependenceResult
    block_refinements: tuple[Periodic1DHigherRankBlockRefinementResult, ...]
    scalar_refinements: tuple[Periodic1DHigherRankScalarRefinementResult, ...]

    def __post_init__(self) -> None:
        if type(self.request) is not Periodic1DHigherRankAlignmentCalculationRequest:
            raise TypeError("request must be the exact calculation request")
        if type(self.global_selection) is not Periodic1DHigherRankProcrustesDiagnostics:
            raise TypeError("global_selection must be the exact Procrustes record")
        if (
            self.global_selection.status.channel
            is not Periodic1DHigherRankAlignmentChannel.GLOBAL_UNITARY
        ):
            raise ValueError(
                "global_selection must describe the global-unitary channel"
            )
        if (
            self.global_selection.selection_mesh_size
            != self.request.configuration.global_unitary_selection_mesh_size
        ):
            raise ValueError("global selection must use the frozen selection mesh")
        global_status = self.global_selection.status
        if (
            global_status.case_identity != self.request.case_identity
            or global_status.retained_rank != self.request.retained_rank
            or global_status.circuit_depth != self.request.circuit_depth
        ):
            raise ValueError("global selection must match the calculation request")
        if (
            type(self.meshes) is not tuple
            or tuple(item.construction_mesh_size for item in self.meshes)
            != self.request.configuration.construction_mesh_sizes
        ):
            raise ValueError("meshes must match the complete construction inventory")
        for mesh in self.meshes:
            if (
                mesh.transport is not None
                and mesh.transport.request
                != self.request.transport_request(mesh.construction_mesh_size)
            ):
                raise ValueError("mesh transport must match the calculation request")
            statuses = (
                mesh.pointwise_selection.status,
                *(channel.status for channel in mesh.channels),
            )
            if any(
                status.case_identity != self.request.case_identity
                or status.retained_rank != self.request.retained_rank
                or status.circuit_depth != self.request.circuit_depth
                for status in statuses
            ):
                raise ValueError("mesh status must match the calculation request")
        if (
            type(self.evaluation_independence)
            is not Periodic1DHigherRankEvaluationIndependenceResult
        ):
            raise TypeError(
                "evaluation_independence must be the exact provenance record"
            )
        if (
            self.evaluation_independence.construction_mesh_sizes
            != self.request.configuration.construction_mesh_sizes
            or self.evaluation_independence.evaluation_mesh_size
            != self.request.configuration.evaluation_mesh_size
        ):
            raise ValueError(
                "evaluation-independence provenance must match the request"
            )
        if type(self.block_refinements) is not tuple or any(
            type(item) is not Periodic1DHigherRankBlockRefinementResult
            for item in self.block_refinements
        ):
            raise TypeError("block_refinements must contain exact refinement records")
        expected_pairs = tuple(
            zip(
                self.request.configuration.construction_mesh_sizes[:-1],
                self.request.configuration.construction_mesh_sizes[1:],
                strict=True,
            )
        )
        expected_keys = tuple(
            (channel, coarse, fine)
            for channel in self.request.configuration.alignment_channels
            for coarse, fine in expected_pairs
            if all(
                next(
                    result
                    for result in mesh.channels
                    if result.status.channel is channel
                ).status.status
                is Periodic1DHigherRankAlignmentStatus.QUALIFIED
                for mesh in self.meshes
                if mesh.construction_mesh_size in (coarse, fine)
            )
        )
        actual_keys = tuple(
            (item.channel, item.coarse_mesh_size, item.fine_mesh_size)
            for item in self.block_refinements
        )
        if actual_keys != expected_keys:
            raise ValueError(
                "block_refinements must match all qualified adjacent mesh pairs"
            )
        if type(self.scalar_refinements) is not tuple or any(
            type(item) is not Periodic1DHigherRankScalarRefinementResult
            for item in self.scalar_refinements
        ):
            raise TypeError(
                "scalar_refinements must contain exact scalar refinement records"
            )
        scalar_keys = tuple(
            (item.channel, item.diagnostic_path) for item in self.scalar_refinements
        )
        if len(set(scalar_keys)) != len(scalar_keys):
            raise ValueError("scalar refinement channel/path keys must be unique")
        final_meshes = {
            mesh.construction_mesh_size: mesh
            for mesh in self.meshes
            if mesh.construction_mesh_size in (1025, 2049)
        }
        expected_scalar_channels = tuple(
            channel
            for channel in self.request.configuration.alignment_channels
            if all(
                next(
                    result
                    for result in final_meshes[size].channels
                    if result.status.channel is channel
                ).status.status
                is Periodic1DHigherRankAlignmentStatus.QUALIFIED
                for size in (1025, 2049)
            )
        )
        if tuple(dict.fromkeys(item.channel for item in self.scalar_refinements)) != (
            expected_scalar_channels
        ):
            raise ValueError(
                "scalar refinements must cover every qualified final-mesh channel"
            )

    def _mapping(self) -> Mapping[str, SerializableValue]:
        return {
            "request": self.request,
            "global_selection": self.global_selection,
            "meshes": self.meshes,
            "evaluation_independence": self.evaluation_independence,
            "block_refinements": self.block_refinements,
            "scalar_refinements": self.scalar_refinements,
        }

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        if set(values) != {
            "request",
            "global_selection",
            "meshes",
            "evaluation_independence",
            "block_refinements",
            "scalar_refinements",
        }:
            raise ValueError("calculation result fields do not match")
        return cls(
            request=Periodic1DHigherRankAlignmentCalculationRequest.from_dict(
                _mapping_value(values["request"], "request")
            ),
            global_selection=Periodic1DHigherRankProcrustesDiagnostics.from_dict(
                _mapping_value(values["global_selection"], "global_selection")
            ),
            meshes=tuple(
                Periodic1DHigherRankMeshCalculationResult.from_dict(item)
                for item in _tuple_of_mappings(values["meshes"], "meshes")
            ),
            evaluation_independence=(
                Periodic1DHigherRankEvaluationIndependenceResult.from_dict(
                    _mapping_value(
                        values["evaluation_independence"],
                        "evaluation_independence",
                    )
                )
            ),
            block_refinements=tuple(
                Periodic1DHigherRankBlockRefinementResult.from_dict(item)
                for item in _tuple_of_mappings(
                    values["block_refinements"], "block_refinements"
                )
            ),
            scalar_refinements=tuple(
                Periodic1DHigherRankScalarRefinementResult.from_dict(item)
                for item in _tuple_of_mappings(
                    values["scalar_refinements"], "scalar_refinements"
                )
            ),
        )


__all__ = [
    "Periodic1DHigherRankAlignmentCalculationControls",
    "Periodic1DHigherRankAlignmentCalculationRequest",
    "Periodic1DHigherRankAlignmentCalculationResult",
    "Periodic1DHigherRankBlockRefinementResult",
    "Periodic1DHigherRankChannelMeshResult",
    "Periodic1DHigherRankEvaluationIndependenceResult",
    "Periodic1DHigherRankFrameErrorResult",
    "Periodic1DHigherRankMatrixComparisonResult",
    "Periodic1DHigherRankMatrixErrorResult",
    "Periodic1DHigherRankMeshCalculationResult",
    "Periodic1DHigherRankModelDiagnostics",
    "Periodic1DHigherRankProcrustesDiagnostics",
    "Periodic1DHigherRankScalarRefinementResult",
    "Periodic1DHigherRankSupportResult",
]
