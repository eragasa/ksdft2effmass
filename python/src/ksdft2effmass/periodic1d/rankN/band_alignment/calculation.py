"""Immutable controls and requests for higher-rank calculation production."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import ClassVar, Self

from ksdft2effmass.periodic1d.rankN._record_admission import (
    _finite_nonnegative,
    _mapping_value,
    _nonempty,
)
from ksdft2effmass.serialization import BaseTypedRecord, SerializableValue

from .configuration import Periodic1DRankNAlignmentConfiguration
from .frame_transport.request import Periodic1DRankNAlignmentTransportRequest


@dataclass(frozen=True, slots=True)
class Periodic1DRankNAlignmentCalculationControls(BaseTypedRecord):
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

    @staticmethod
    def _float_names() -> tuple[str, ...]:
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
class Periodic1DRankNAlignmentCalculationRequest(BaseTypedRecord):
    """Bind one rank/depth calculation to exact controls and physical identities."""

    configuration: Periodic1DRankNAlignmentConfiguration
    controls: Periodic1DRankNAlignmentCalculationControls
    retained_rank: int
    circuit_depth: int
    ambient_basis_identifier: str
    retained_frame_identifier: str
    endpoint_sewing_identifier: str
    represented_basis_identifier: str
    energy_reference_identifier: str

    def __post_init__(self) -> None:
        if type(self.configuration) is not Periodic1DRankNAlignmentConfiguration:
            raise TypeError("configuration must be the exact higher-rank configuration")
        if type(self.controls) is not Periodic1DRankNAlignmentCalculationControls:
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
    ) -> Periodic1DRankNAlignmentTransportRequest:
        """Return the exact transport request for one configured construction mesh."""
        return Periodic1DRankNAlignmentTransportRequest(
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
            configuration=Periodic1DRankNAlignmentConfiguration.from_dict(
                _mapping_value(values["configuration"], "configuration")
            ),
            controls=Periodic1DRankNAlignmentCalculationControls.from_dict(
                _mapping_value(values["controls"], "controls")
            ),
            retained_rank=rank,
            circuit_depth=depth,
            **strings,
        )
