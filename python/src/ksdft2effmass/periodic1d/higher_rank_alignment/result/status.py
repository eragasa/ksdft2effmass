"""Typed gauge-alignment status records for the higher-rank study."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Self

from ksdft2effmass.serialization import BaseTypedRecord, SerializableValue

from ..configuration import Periodic1DHigherRankAlignmentConfiguration
from ..definition import (
    Periodic1DHigherRankAlignmentBackendExceptionCode,
    Periodic1DHigherRankAlignmentStatus,
    Periodic1DHigherRankGlobalUnitaryDownstreamApplicability,
)
from ..gauge_alignment.definition import (
    GaugeAlignmentWireMapping,
    Periodic1DHigherRankGaugeAlignment,
)


def _case_identity(retained_rank: int, circuit_depth: int) -> str:
    return f"r{retained_rank:02d}-L{circuit_depth:02d}"


def _nonempty_text(value: str, name: str) -> None:
    if type(value) is not str:
        raise TypeError(f"{name} must be a built-in string")
    if not value:
        raise ValueError(f"{name} must be nonempty")


@dataclass(frozen=True, slots=True)
class Periodic1DHigherRankAlignmentStatusResult(BaseTypedRecord):
    """Record the outcome of one alignment family on one construction mesh.

    Parameters
    ----------
    case_identity
        Nonempty rank/depth identity ``rNN-LNN``.
    retained_rank, circuit_depth
        Built-in unitless integers selected from the frozen study inventories.
    construction_mesh_size
        Built-in integer number of construction-mesh points.
    gauge_alignment, status
        Exact alignment-family and outcome enums.
    global_unitary_downstream_applicability
        Applicability of downstream global-unitary observables, or ``None`` for other
        gauge alignments and unresolved failures.
    backend_exception_code
        Closed numerical-failure classification, present only for numerically unresolved
        alignment.

    Notes
    -----
    Python integers do not overflow; the frozen inventories bound their values. Boolean
    values and numeric strings are rejected. No absent downstream quantity is
    represented by a fabricated numeric zero.
    """

    case_identity: str
    retained_rank: int
    circuit_depth: int
    construction_mesh_size: int
    gauge_alignment: Periodic1DHigherRankGaugeAlignment
    status: Periodic1DHigherRankAlignmentStatus
    global_unitary_downstream_applicability: (
        Periodic1DHigherRankGlobalUnitaryDownstreamApplicability | None
    )
    backend_exception_code: Periodic1DHigherRankAlignmentBackendExceptionCode | None

    def __post_init__(self) -> None:
        """Validate the closed gauge-alignment-specific disposition inventory."""
        _nonempty_text(self.case_identity, "case_identity")
        for value, name, allowed in (
            (
                self.retained_rank,
                "retained_rank",
                Periodic1DHigherRankAlignmentConfiguration.RETAINED_RANKS,
            ),
            (
                self.circuit_depth,
                "circuit_depth",
                Periodic1DHigherRankAlignmentConfiguration.CIRCUIT_DEPTHS,
            ),
            (
                self.construction_mesh_size,
                "construction_mesh_size",
                Periodic1DHigherRankAlignmentConfiguration.CONSTRUCTION_MESH_SIZES,
            ),
        ):
            if type(value) is not int:
                raise TypeError(f"{name} must be a built-in integer")
            if value not in allowed:
                raise ValueError(f"{name} is not in the frozen inventory")
        if self.case_identity != _case_identity(self.retained_rank, self.circuit_depth):
            raise ValueError("case_identity is inconsistent with rank and depth")
        if type(self.gauge_alignment) is not Periodic1DHigherRankGaugeAlignment:
            raise TypeError(
                "gauge_alignment must be the exact higher-rank gauge-alignment enum"
            )
        if type(self.status) is not Periodic1DHigherRankAlignmentStatus:
            raise TypeError("status must be the exact higher-rank status enum")
        if (
            self.global_unitary_downstream_applicability is not None
            and type(self.global_unitary_downstream_applicability)
            is not Periodic1DHigherRankGlobalUnitaryDownstreamApplicability
        ):
            raise TypeError(
                "global_unitary_downstream_applicability must be its exact enum or None"
            )
        if (
            self.backend_exception_code is not None
            and type(self.backend_exception_code)
            is not Periodic1DHigherRankAlignmentBackendExceptionCode
        ):
            raise TypeError("backend_exception_code must be its exact enum or None")

        permitted = {
            Periodic1DHigherRankGaugeAlignment.IDENTITY: (
                Periodic1DHigherRankAlignmentStatus.QUALIFIED,
                Periodic1DHigherRankAlignmentStatus.NUMERICALLY_UNRESOLVED,
            ),
            Periodic1DHigherRankGaugeAlignment.GLOBAL_UNITARY: (
                Periodic1DHigherRankAlignmentStatus.QUALIFIED,
                Periodic1DHigherRankAlignmentStatus.AGGREGATE_RANK_DEFICIENT,
                Periodic1DHigherRankAlignmentStatus.NUMERICALLY_UNRESOLVED,
                Periodic1DHigherRankAlignmentStatus.INTEGRITY_FAILED,
            ),
            Periodic1DHigherRankGaugeAlignment.POINTWISE_UNITARY: (
                Periodic1DHigherRankAlignmentStatus.QUALIFIED,
                Periodic1DHigherRankAlignmentStatus.POINTWISE_RANK_DEFICIENT,
                Periodic1DHigherRankAlignmentStatus.NUMERICALLY_UNRESOLVED,
                Periodic1DHigherRankAlignmentStatus.INTEGRITY_FAILED,
            ),
            Periodic1DHigherRankGaugeAlignment.KNOWN_INVERSE_ORACLE: (
                Periodic1DHigherRankAlignmentStatus.QUALIFIED,
                Periodic1DHigherRankAlignmentStatus.NUMERICALLY_UNRESOLVED,
                Periodic1DHigherRankAlignmentStatus.ORACLE_INTEGRITY_FAILED,
            ),
        }
        if self.status not in permitted[self.gauge_alignment]:
            raise ValueError(
                "status is not admissible for the selected gauge alignment"
            )

        if self.gauge_alignment is Periodic1DHigherRankGaugeAlignment.GLOBAL_UNITARY:
            expected_applicability = {
                Periodic1DHigherRankAlignmentStatus.QUALIFIED: (
                    Periodic1DHigherRankGlobalUnitaryDownstreamApplicability.APPLICABLE
                ),
                Periodic1DHigherRankAlignmentStatus.AGGREGATE_RANK_DEFICIENT: (
                    Periodic1DHigherRankGlobalUnitaryDownstreamApplicability.INAPPLICABLE_AGGREGATE_RANK_DEFICIENT
                ),
                Periodic1DHigherRankAlignmentStatus.NUMERICALLY_UNRESOLVED: None,
                Periodic1DHigherRankAlignmentStatus.INTEGRITY_FAILED: None,
            }[self.status]
            if (
                self.global_unitary_downstream_applicability
                is not expected_applicability
            ):
                raise ValueError(
                    "global-unitary status and downstream applicability disagree"
                )
        elif self.global_unitary_downstream_applicability is not None:
            raise ValueError(
                "only global-unitary alignment may retain downstream applicability"
            )

        if self.status is Periodic1DHigherRankAlignmentStatus.NUMERICALLY_UNRESOLVED:
            if self.backend_exception_code is None:
                raise ValueError(
                    "numerically unresolved alignment requires a backend exception code"
                )
        elif self.backend_exception_code is not None:
            raise ValueError(
                "backend exception codes are reserved for numerically unresolved status"
            )

    def _mapping(self) -> Mapping[str, SerializableValue]:
        return {
            "case_identity": self.case_identity,
            "retained_rank": self.retained_rank,
            "circuit_depth": self.circuit_depth,
            "construction_mesh_size": self.construction_mesh_size,
            "gauge_alignment": GaugeAlignmentWireMapping.to_wire(self.gauge_alignment),
            "status": self.status.value,
            "global_unitary_downstream_applicability": (
                None
                if self.global_unitary_downstream_applicability is None
                else self.global_unitary_downstream_applicability.value
            ),
            "backend_exception_code": (
                None
                if self.backend_exception_code is None
                else self.backend_exception_code.value
            ),
        }

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        required = {
            "case_identity",
            "retained_rank",
            "circuit_depth",
            "construction_mesh_size",
            "gauge_alignment",
            "status",
            "global_unitary_downstream_applicability",
            "backend_exception_code",
        }
        if set(values) != required:
            raise ValueError("higher-rank alignment status fields do not match")
        case_identity = values["case_identity"]
        retained_rank = values["retained_rank"]
        circuit_depth = values["circuit_depth"]
        construction_mesh_size = values["construction_mesh_size"]
        gauge_alignment = values["gauge_alignment"]
        status = values["status"]
        applicability = values["global_unitary_downstream_applicability"]
        exception_code = values["backend_exception_code"]
        if type(case_identity) is not str:
            raise TypeError("case_identity must decode to a string")
        if (
            type(retained_rank) is not int
            or type(circuit_depth) is not int
            or type(construction_mesh_size) is not int
        ):
            raise TypeError("rank, depth, and mesh size must decode to integers")
        if type(gauge_alignment) is not str or type(status) is not str:
            raise TypeError("gauge_alignment and status must decode to strings")
        if applicability is not None and type(applicability) is not str:
            raise TypeError(
                "global-unitary applicability must decode to a string or None"
            )
        if exception_code is not None and type(exception_code) is not str:
            raise TypeError("backend exception code must decode to a string or None")
        return cls(
            case_identity=case_identity,
            retained_rank=retained_rank,
            circuit_depth=circuit_depth,
            construction_mesh_size=construction_mesh_size,
            gauge_alignment=GaugeAlignmentWireMapping.from_wire(gauge_alignment),
            status=Periodic1DHigherRankAlignmentStatus(status),
            global_unitary_downstream_applicability=(
                None
                if applicability is None
                else Periodic1DHigherRankGlobalUnitaryDownstreamApplicability(
                    applicability
                )
            ),
            backend_exception_code=(
                None
                if exception_code is None
                else Periodic1DHigherRankAlignmentBackendExceptionCode(exception_code)
            ),
        )


__all__ = ["Periodic1DHigherRankAlignmentStatusResult"]
