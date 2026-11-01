"""Immutable results for one gauge alignment on one mesh."""

from __future__ import annotations

import math
from collections.abc import Mapping
from dataclasses import dataclass
from typing import TYPE_CHECKING, Self

import numpy as np
from projectkoios.numerics.numpy.typing import Float64Array, Int64Array

from ksdft2effmass.gauge_alignment import (
    GaugeAlignmentActionConvention,
    GaugeAlignmentAnalysisIdentity,
    GaugeAlignmentInnerProductConvention,
)
from ksdft2effmass.periodic1d.gauge_alignment import (
    Periodic1DGaugeAlignmentAnalysis,
)
from ksdft2effmass.serialization import BaseTypedRecord, SerializableValue

if TYPE_CHECKING:
    from ksdft2effmass.periodic1d.rankN.hopping_locality.result import (
        Periodic1DRankNHoppingTailResult,
    )

from ksdft2effmass.periodic1d.rankN._record_admission import (
    _finite_nonnegative,
    _float_array,
    _int_array,
    _mapping_value,
    _nonempty,
    _tuple_of_mappings,
)
from ksdft2effmass.periodic1d.rankN.band_alignment.calculation import (
    Periodic1DRankNAlignmentCalculationControls,
)
from ksdft2effmass.periodic1d.rankN.diagnostics import (
    Periodic1DRankNFrameErrorResult,
    Periodic1DRankNMatrixComparisonResult,
    Periodic1DRankNMatrixErrorResult,
)
from ksdft2effmass.periodic1d.rankN.gauge_alignment.definition import (
    Periodic1DRankNGaugeAlignment,
)
from ksdft2effmass.periodic1d.rankN.gauge_alignment.nyquist import (
    NyquistModeDispositionEnum,
)
from ksdft2effmass.periodic1d.rankN.gauge_alignment.status import (
    Periodic1DRankNAlignmentStatus,
    Periodic1DRankNAlignmentStatusResult,
)
from ksdft2effmass.periodic1d.rankN.support_truncation.result import (
    Periodic1DRankNSupportResult,
)


@dataclass(frozen=True, slots=True, eq=False)
class Periodic1DRankNGaugeAlignmentMeshResult(
    BaseTypedRecord,
    Periodic1DGaugeAlignmentAnalysis,
):
    """Retain transform, interpolation, and locality evidence for one alignment."""

    status: Periodic1DRankNAlignmentStatusResult
    transform_backend_identifier: str | None
    transform_backend_version: str | None
    fourier_representative_count: int | None
    fourier_representative_inventory_ordered_unique: bool | None
    fourier_inversion_closed: bool | None
    fourier_index_bijection_pass: bool | None
    nyquist_mode_disposition: NyquistModeDispositionEnum | None
    coefficient_translations: Int64Array
    block_raw_frobenius_norms: Float64Array
    block_normalized_frobenius_norms: Float64Array
    frame_recovery: Periodic1DRankNFrameErrorResult | None
    known_frame_recovery_pass: bool | None
    represented_operator_recovery: Periodic1DRankNMatrixErrorResult | None
    known_operator_recovery_pass: bool | None
    reconstruction: Periodic1DRankNMatrixErrorResult | None
    reconstruction_pass: bool | None
    interpolation: Periodic1DRankNMatrixComparisonResult | None
    final_interpolation_operator_pass: bool | None
    final_interpolation_spectrum_pass: bool | None
    parseval_relative_defect: float | None
    parseval_pass: bool | None
    ordinary_hermiticity_defect: float | None
    ordinary_hermiticity_pass: bool | None
    twisted_cyclic_hermiticity_defect: float | None
    twisted_cyclic_hermiticity_pass: bool | None
    supports: tuple[Periodic1DRankNSupportResult, ...]
    maximum_tail_increase: float | None
    all_tail_monotonicity_checks_pass: bool | None

    def __post_init__(self) -> None:
        if type(self.status) is not Periodic1DRankNAlignmentStatusResult:
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
            type(value) is not Periodic1DRankNSupportResult for value in self.supports
        ):
            raise TypeError("supports must contain exact support result records")
        if (
            self.fourier_representative_count is not None
            and type(self.fourier_representative_count) is not int
        ):
            raise TypeError(
                "fourier_representative_count must be a built-in integer or None"
            )
        qualified = self.status.status is Periodic1DRankNAlignmentStatus.QUALIFIED
        required_values = (
            self.transform_backend_identifier,
            self.transform_backend_version,
            self.fourier_representative_count,
            self.fourier_representative_inventory_ordered_unique,
            self.fourier_inversion_closed,
            self.fourier_index_bijection_pass,
            self.nyquist_mode_disposition,
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
                    "qualified alignment requires complete transform diagnostics"
                )
            if (
                tuple(result.maximum_range for result in self.supports)
                != Periodic1DRankNAlignmentCalculationControls.SUPPORT_RADII
            ):
                raise ValueError("qualified alignment must retain every frozen support")
            expected_translations = np.arange(
                -Periodic1DRankNAlignmentCalculationControls.MAXIMUM_RECORDED_BLOCK_RANGE,
                Periodic1DRankNAlignmentCalculationControls.MAXIMUM_RECORDED_BLOCK_RANGE
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
                * Periodic1DRankNAlignmentCalculationControls.ENERGY_REFERENCE
            )
            if not np.array_equal(normalized, raw / block_scale):
                raise ValueError("normalized block norms are inconsistent")
            if any(
                support.rank != self.status.retained_rank
                or support.energy_reference
                != Periodic1DRankNAlignmentCalculationControls.ENERGY_REFERENCE
                for support in self.supports
            ):
                raise ValueError(
                    "support normalization must match the alignment status"
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
            if (
                self.nyquist_mode_disposition
                is not NyquistModeDispositionEnum.ABSENT_ON_ODD_MESH
            ):
                raise ValueError("odd mesh must have no self-inverse Nyquist mode")
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
                    "unqualified alignment must not claim downstream diagnostics"
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
                raise ValueError("qualified alignment requires gate evidence")
            controls = Periodic1DRankNAlignmentCalculationControls
            tolerance = controls.FOURIER_CONSISTENCY_TOLERANCE
            known_recovery_applicable = self.status.gauge_alignment in (
                Periodic1DRankNGaugeAlignment.POINTWISE_UNITARY,
                Periodic1DRankNGaugeAlignment.KNOWN_INVERSE_ORACLE,
            )
            if known_recovery_applicable:
                if (
                    self.frame_recovery is None
                    or self.represented_operator_recovery is None
                ):
                    raise ValueError(
                        "known-recovery alignments require recovery evidence"
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
                raise ValueError("other alignments cannot claim known-recovery gates")
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
                raise ValueError("gauge-alignment gate disposition is inconsistent")
        for text_value, name in (
            (self.transform_backend_identifier, "transform_backend_identifier"),
            (self.transform_backend_version, "transform_backend_version"),
        ):
            if text_value is not None:
                _nonempty(text_value, name)
        object.__setattr__(self, "coefficient_translations", translations)
        object.__setattr__(self, "block_raw_frobenius_norms", raw)
        object.__setattr__(self, "block_normalized_frobenius_norms", normalized)

    @property
    def hopping_locality_tails(
        self,
    ) -> tuple[Periodic1DRankNHoppingTailResult, ...]:
        """Project stored combined bytes into hopping-locality diagnostic values."""
        from ksdft2effmass.periodic1d.rankN.hopping_locality.result import (
            Periodic1DRankNHoppingTailResult,
        )

        translations = tuple(int(value) for value in self.coefficient_translations)
        return tuple(
            Periodic1DRankNHoppingTailResult(
                maximum_range=support.maximum_range,
                rank=support.rank,
                norm_energy_scale=support.energy_reference,
                retained_translations=support.retained_translations,
                omitted_translations=tuple(
                    value
                    for value in translations
                    if abs(value) > support.maximum_range
                ),
                omitted_squared_frobenius_weight=(
                    support.omitted_squared_frobenius_weight
                ),
                normalized_omitted_squared_frobenius_weight=(
                    support.normalized_omitted_squared_frobenius_weight
                ),
                omitted_frobenius_l2_norm=support.omitted_frobenius_l2_norm,
                normalized_omitted_frobenius_l2_norm=(
                    support.normalized_omitted_frobenius_l2_norm
                ),
                omitted_block_l1_norm=support.omitted_block_l1_norm,
                normalized_omitted_block_l1_norm=(
                    support.normalized_omitted_block_l1_norm
                ),
            )
            for support in self.supports
        )

    @property
    def analysis_identity(self) -> GaugeAlignmentAnalysisIdentity:
        """Return the finite higher-rank alignment identity."""
        rank = self.status.retained_rank
        return GaugeAlignmentAnalysisIdentity(
            retained_rank=rank,
            gauge_group=f"U({rank})",
            alignment_sample_count=self.status.construction_mesh_size,
            action_convention=GaugeAlignmentActionConvention.RIGHT,
            inner_product_convention=(
                GaugeAlignmentInnerProductConvention.EUCLIDEAN_ORTHONORMAL
            ),
        )

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
            "nyquist_mode_disposition": (
                None
                if self.nyquist_mode_disposition is None
                else self.nyquist_mode_disposition.to_wire()
            ),
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
            "nyquist_mode_disposition",
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
            raise ValueError("gauge-alignment mesh fields do not match")
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
        nyquist_mode_value = values["nyquist_mode_disposition"]
        if nyquist_mode_value is None:
            nyquist_mode_disposition = None
        else:
            if type(nyquist_mode_value) is not str:
                raise TypeError(
                    "nyquist_mode_disposition must decode to string or None"
                )
            nyquist_mode_disposition = NyquistModeDispositionEnum.from_wire(
                nyquist_mode_value
            )
        frame_recovery_value = values["frame_recovery"]
        represented_operator_recovery_value = values["represented_operator_recovery"]
        reconstruction_value = values["reconstruction"]
        interpolation_value = values["interpolation"]
        supports = tuple(
            Periodic1DRankNSupportResult.from_dict(item)
            for item in _tuple_of_mappings(values["supports"], "supports")
        )
        return cls(
            status=Periodic1DRankNAlignmentStatusResult.from_dict(
                _mapping_value(values["status"], "status")
            ),
            fourier_representative_count=representative_count,
            fourier_representative_inventory_ordered_unique=optional_bools[
                "fourier_representative_inventory_ordered_unique"
            ],
            fourier_inversion_closed=optional_bools["fourier_inversion_closed"],
            fourier_index_bijection_pass=optional_bools["fourier_index_bijection_pass"],
            nyquist_mode_disposition=nyquist_mode_disposition,
            coefficient_translations=_int_array(
                arrays["coefficient_translations"], "coefficient_translations"
            ),
            block_raw_frobenius_norms=arrays["block_raw_frobenius_norms"],
            block_normalized_frobenius_norms=arrays["block_normalized_frobenius_norms"],
            frame_recovery=None
            if frame_recovery_value is None
            else Periodic1DRankNFrameErrorResult.from_dict(
                _mapping_value(frame_recovery_value, "frame_recovery")
            ),
            known_frame_recovery_pass=optional_bools["known_frame_recovery_pass"],
            represented_operator_recovery=None
            if represented_operator_recovery_value is None
            else Periodic1DRankNMatrixErrorResult.from_dict(
                _mapping_value(
                    represented_operator_recovery_value,
                    "represented_operator_recovery",
                )
            ),
            known_operator_recovery_pass=optional_bools["known_operator_recovery_pass"],
            reconstruction=None
            if reconstruction_value is None
            else Periodic1DRankNMatrixErrorResult.from_dict(
                _mapping_value(reconstruction_value, "reconstruction")
            ),
            interpolation=None
            if interpolation_value is None
            else Periodic1DRankNMatrixComparisonResult.from_dict(
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


__all__ = ["Periodic1DRankNGaugeAlignmentMeshResult"]
