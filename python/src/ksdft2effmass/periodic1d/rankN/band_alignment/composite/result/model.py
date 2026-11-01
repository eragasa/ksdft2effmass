"""Analytic-model and Procrustes diagnostics."""

from __future__ import annotations

import math
from collections.abc import Mapping
from dataclasses import dataclass
from typing import Self

import numpy as np
from projectkoios.numerics.numpy.typing import Float64Array

from ksdft2effmass.periodic1d.rankN._record_admission import (
    _decoded_float,
    _finite_nonnegative,
    _float_array,
    _nonempty,
)
from ksdft2effmass.periodic1d.rankN.band_alignment.configuration import (
    Periodic1DRankNAlignmentConfiguration,
)
from ksdft2effmass.serialization import BaseTypedRecord, SerializableValue


@dataclass(frozen=True, slots=True, eq=False)
class Periodic1DRankNModelDiagnostics(BaseTypedRecord):
    """Retain analytic-gap, sampled-gap, structure, and recovery diagnostics."""

    case_identity: str
    retained_rank: int
    circuit_depth: int
    construction_mesh_size: int
    exact_analytic_isolation_gap: float
    sampled_isolation_gaps: Float64Array
    exact_analytic_attack_angle_maximum: float
    sampled_attack_angle_maxima: Float64Array
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
        _nonempty(self.case_identity, "case_identity")
        if (
            type(self.retained_rank) is not int
            or self.retained_rank
            not in Periodic1DRankNAlignmentConfiguration.RETAINED_RANKS
        ):
            raise ValueError("retained_rank must be in the frozen inventory")
        if (
            type(self.circuit_depth) is not int
            or self.circuit_depth
            not in Periodic1DRankNAlignmentConfiguration.CIRCUIT_DEPTHS
        ):
            raise ValueError("circuit_depth must be in the frozen inventory")
        if (
            type(self.construction_mesh_size) is not int
            or self.construction_mesh_size
            not in Periodic1DRankNAlignmentConfiguration.CONSTRUCTION_MESH_SIZES
        ):
            raise ValueError("construction_mesh_size must be in the frozen inventory")
        expected_case_identity = f"r{self.retained_rank:02d}-L{self.circuit_depth:02d}"
        if self.case_identity != expected_case_identity:
            raise ValueError("case_identity is inconsistent with rank and depth")
        if self.exact_analytic_isolation_gap != 2.1:
            raise ValueError(
                "exact_analytic_isolation_gap must equal the protocol value"
            )
        sampled = _float_array(
            self.sampled_isolation_gaps,
            "sampled_isolation_gaps",
        )
        if sampled.shape != (
            len(Periodic1DRankNAlignmentConfiguration.CONSTRUCTION_MESH_SIZES),
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
            "case_identity": self.case_identity,
            "retained_rank": self.retained_rank,
            "circuit_depth": self.circuit_depth,
            "construction_mesh_size": self.construction_mesh_size,
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
            "case_identity",
            "retained_rank",
            "circuit_depth",
            "construction_mesh_size",
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
        case_identity = values["case_identity"]
        rank = values["retained_rank"]
        circuit_depth = values["circuit_depth"]
        construction_mesh_size = values["construction_mesh_size"]
        if not isinstance(sampled, np.ndarray) or not isinstance(
            sampled_angles, np.ndarray
        ):
            raise TypeError("sampled diagnostics must decode to numpy.ndarray")
        if type(case_identity) is not str:
            raise TypeError("case_identity must decode to a built-in string")
        if (
            type(rank) is not int
            or type(circuit_depth) is not int
            or type(construction_mesh_size) is not int
        ):
            raise TypeError("rank, depth, and mesh size must decode to integers")
        return cls(
            case_identity=case_identity,
            retained_rank=rank,
            circuit_depth=circuit_depth,
            construction_mesh_size=construction_mesh_size,
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
