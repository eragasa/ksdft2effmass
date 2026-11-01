"""Immutable rank-N gauge-alignment Procrustes evidence."""

from __future__ import annotations

import math
from collections.abc import Mapping
from dataclasses import dataclass
from typing import Self

import numpy as np
from projectkoios.numerics.numpy.typing import Float64Array, Int64Array
from projectkoios.physkit.units import ComplexMatrixQuantity, Unitless

from ksdft2effmass.periodic1d.rankN._record_admission import (
    _finite_nonnegative,
    _float_array,
    _int_array,
    _mapping_value,
    _nonempty,
)
from ksdft2effmass.periodic1d.rankN.band_alignment.protocol import (
    CONSTRUCTION_MESH_SIZES,
)
from ksdft2effmass.serialization import BaseTypedRecord, SerializableValue

from ..definition import Periodic1DRankNGaugeAlignment
from ..status import (
    Periodic1DRankNAlignmentBackendExceptionCode,
    Periodic1DRankNAlignmentStatus,
    Periodic1DRankNAlignmentStatusResult,
)


@dataclass(frozen=True, slots=True, eq=False)
class Periodic1DRankNProcrustesDiagnostics(BaseTypedRecord):
    """Retain complete rank and integrity evidence for global or pointwise selection."""

    status: Periodic1DRankNAlignmentStatusResult
    selection_mesh_size: int
    cross_singular_values: Float64Array
    numerical_ranks: Int64Array
    applied_rank_cutoffs: Float64Array
    rank_margins: Float64Array
    spectral_condition_numbers: tuple[float | None, ...]
    deficient_point_indices: tuple[int, ...]
    deficient_point_count: int
    normalized_optimal_residuals: Float64Array
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

    @classmethod
    def numerically_unresolved(
        cls,
        *,
        case_identity: str,
        retained_rank: int,
        circuit_depth: int,
        gauge_alignment: Periodic1DRankNGaugeAlignment,
        selection_mesh_size: int,
        backend_exception_code: Periodic1DRankNAlignmentBackendExceptionCode,
    ) -> Self:
        """Construct diagnostics for one admitted numerical backend failure."""
        return cls(
            status=Periodic1DRankNAlignmentStatusResult.from_disposition(
                case_identity=case_identity,
                retained_rank=retained_rank,
                circuit_depth=circuit_depth,
                construction_mesh_size=selection_mesh_size,
                gauge_alignment=gauge_alignment,
                status=Periodic1DRankNAlignmentStatus.NUMERICALLY_UNRESOLVED,
                backend_exception_code=backend_exception_code,
            ),
            selection_mesh_size=selection_mesh_size,
            cross_singular_values=np.empty((0, retained_rank), dtype=np.float64),
            numerical_ranks=np.empty(0, dtype=np.int64),
            applied_rank_cutoffs=np.empty(0, dtype=np.float64),
            rank_margins=np.empty(0, dtype=np.float64),
            spectral_condition_numbers=(),
            deficient_point_indices=(),
            deficient_point_count=0,
            normalized_optimal_residuals=np.empty(0, dtype=np.float64),
            normalized_objective_maximum=None,
            normalized_objective_rms=None,
            minimum_rank_margin=None,
            maximum_unitarity_defect=None,
            maximum_stationarity_defect=None,
            maximum_objective_identity_defect=None,
            maximum_psd_defect=None,
            selected_global_right_unitary=None,
            backend_identifier=None,
            backend_version=None,
        )

    def __post_init__(self) -> None:
        if type(self.status) is not Periodic1DRankNAlignmentStatusResult:
            raise TypeError("status must be the exact alignment status record")
        if self.status.gauge_alignment not in (
            Periodic1DRankNGaugeAlignment.GLOBAL_UNITARY,
            Periodic1DRankNGaugeAlignment.POINTWISE_UNITARY,
        ):
            raise ValueError(
                "Procrustes diagnostics require global or pointwise alignment"
            )
        if type(self.selection_mesh_size) is not int:
            raise TypeError("selection_mesh_size must be a built-in integer")
        if self.selection_mesh_size not in CONSTRUCTION_MESH_SIZES:
            raise ValueError("selection_mesh_size is not a construction mesh")
        if self.status.construction_mesh_size != self.selection_mesh_size:
            raise ValueError("selection status must match the selection mesh")
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
            self.status.status is Periodic1DRankNAlignmentStatus.NUMERICALLY_UNRESOLVED
        )
        expected_count = (
            0
            if unresolved
            else (
                1
                if self.status.gauge_alignment
                is Periodic1DRankNGaugeAlignment.GLOBAL_UNITARY
                else self.selection_mesh_size
            )
        )
        if singular.shape != (expected_count, self.status.retained_rank):
            raise ValueError(
                "cross_singular_values shape disagrees with gauge_alignment and rank"
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
                if self.status.gauge_alignment
                is Periodic1DRankNGaugeAlignment.POINTWISE_UNITARY
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
                self.status.gauge_alignment
                is Periodic1DRankNGaugeAlignment.GLOBAL_UNITARY
                and self.status.status is Periodic1DRankNAlignmentStatus.QUALIFIED
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
            status=Periodic1DRankNAlignmentStatusResult.from_dict(
                _mapping_value(values["status"], "status")
            ),
            selection_mesh_size=mesh,
            cross_singular_values=arrays["cross_singular_values"],
            numerical_ranks=_int_array(arrays["numerical_ranks"], "numerical_ranks"),
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


__all__ = ["Periodic1DRankNProcrustesDiagnostics"]
