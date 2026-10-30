"""Immutable channel, support, and mesh results for higher-rank alignment."""

from __future__ import annotations

import math
from collections.abc import Mapping
from dataclasses import dataclass
from typing import Self

import numpy as np
from projectkoios.numerics.numpy.typing import Float64Array, Int64Array

from ksdft2effmass.serialization import BaseTypedRecord, SerializableValue

from ._record_admission import (
    _decoded_bool,
    _decoded_float,
    _decoded_optional_float,
    _finite_nonnegative,
    _float_array,
    _int_array,
    _mapping_value,
    _nonempty,
    _tuple_of_mappings,
)
from .calculation import Periodic1DHigherRankAlignmentCalculationControls
from .configuration import Periodic1DHigherRankAlignmentConfiguration
from .definition import (
    Periodic1DHigherRankAlignmentChannel,
    Periodic1DHigherRankAlignmentStatus,
)
from .diagnostics import (
    Periodic1DHigherRankFrameErrorResult,
    Periodic1DHigherRankMatrixComparisonResult,
    Periodic1DHigherRankMatrixErrorResult,
    Periodic1DHigherRankModelDiagnostics,
    Periodic1DHigherRankProcrustesDiagnostics,
)
from .result import (
    Periodic1DHigherRankAlignmentStatusResult,
    Periodic1DHigherRankAlignmentTransportBackendFailureResult,
    Periodic1DHigherRankAlignmentTransportOwnerResult,
)

_ODD_CENTERED_NO_NYQUIST_DISPOSITION = "inapplicable-odd-centered-no-nyquist"


@dataclass(frozen=True, slots=True)
class Periodic1DHigherRankSupportResult(BaseTypedRecord):
    """Retain one declared symmetric support and its separate error channels."""

    maximum_range: int
    rank: int
    energy_reference: float
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
        if (
            type(self.rank) is not int
            or self.rank
            not in Periodic1DHigherRankAlignmentConfiguration.RETAINED_RANKS
        ):
            raise ValueError("rank must be in the frozen retained-rank inventory")
        if self.energy_reference != (
            Periodic1DHigherRankAlignmentCalculationControls.ENERGY_REFERENCE
        ):
            raise ValueError("energy_reference must equal the frozen normalization")
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
        if self.omitted_frobenius_l2_norm != math.sqrt(
            self.omitted_squared_frobenius_weight
        ):
            raise ValueError("omitted l2 norm must be the square root of the weight")
        squared_scale = self.rank * self.energy_reference**2
        linear_scale = math.sqrt(self.rank) * self.energy_reference
        normalized = (
            self.normalized_omitted_squared_frobenius_weight,
            self.normalized_omitted_frobenius_l2_norm,
            self.normalized_omitted_block_l1_norm,
        )
        expected_normalized = (
            self.omitted_squared_frobenius_weight / squared_scale,
            self.omitted_frobenius_l2_norm / linear_scale,
            self.omitted_block_l1_norm / linear_scale,
        )
        if normalized != expected_normalized:
            raise ValueError("normalized tail fields are inconsistent")
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
            "rank": self.rank,
            "energy_reference": self.energy_reference,
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
            "rank",
            "energy_reference",
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
        rank = values["rank"]
        translations = values["retained_translations"]
        if type(maximum_range) is not int or type(rank) is not int:
            raise TypeError("maximum_range and rank must decode to integers")
        if not isinstance(translations, tuple) or any(
            type(value) is not int for value in translations
        ):
            raise TypeError("retained_translations must decode to built-in integers")
        return cls(
            maximum_range=maximum_range,
            rank=rank,
            energy_reference=_decoded_float(
                values["energy_reference"], "energy_reference"
            ),
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


@dataclass(frozen=True, slots=True, eq=False)
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
    coefficient_translations: Int64Array
    block_raw_frobenius_norms: Float64Array
    block_normalized_frobenius_norms: Float64Array
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
            if bool((raw < 0.0).any()) or bool((normalized < 0.0).any()):
                raise ValueError("block norm inventories must be nonnegative")
            block_scale = (
                math.sqrt(self.status.retained_rank)
                * Periodic1DHigherRankAlignmentCalculationControls.ENERGY_REFERENCE
            )
            if not np.array_equal(normalized, raw / block_scale):
                raise ValueError("normalized block norms are inconsistent")
            if any(
                support.rank != self.status.retained_rank
                or support.energy_reference
                != Periodic1DHigherRankAlignmentCalculationControls.ENERGY_REFERENCE
                for support in self.supports
            ):
                raise ValueError("support normalization must match the channel status")
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
            coefficient_translations=_int_array(
                arrays["coefficient_translations"], "coefficient_translations"
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


@dataclass(frozen=True, slots=True, eq=False)
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
        if self.model_diagnostics.construction_mesh_size != self.construction_mesh_size:
            raise ValueError("model diagnostics must match the construction mesh")
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
                self.transport_backend_failure.construction_mesh_size
                != self.construction_mesh_size
            ):
                raise ValueError(
                    "transport backend failure must match the construction mesh"
                )
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
