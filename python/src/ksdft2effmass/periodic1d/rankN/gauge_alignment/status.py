"""Typed gauge-alignment status records for the higher-rank study."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Self

from numpy.linalg import LinAlgError

from ksdft2effmass.periodic1d.rankN.band_alignment.protocol import (
    CIRCUIT_DEPTHS,
    CONSTRUCTION_MESH_SIZES,
    RETAINED_RANKS,
)
from ksdft2effmass.serialization import (
    BaseTypedRecord,
    SerializableValue,
    StringWireEnum,
)

from .definition import Periodic1DRankNGaugeAlignment


class Periodic1DRankNAlignmentStatus(StringWireEnum):
    """Retain the exact disposition of one gauge alignment."""

    QUALIFIED = "qualified"
    AGGREGATE_RANK_DEFICIENT = "aggregate-rank-deficient"
    POINTWISE_RANK_DEFICIENT = "pointwise-rank-deficient"
    NUMERICALLY_UNRESOLVED = "alignment-numerically-unresolved"
    INTEGRITY_FAILED = "alignment-integrity-failed"
    ORACLE_INTEGRITY_FAILED = "oracle-integrity-failed"


class Periodic1DRankNGlobalUnitaryDownstreamApplicability(StringWireEnum):
    """State whether global-unitary alignment has downstream values."""

    APPLICABLE = "applicable"
    INAPPLICABLE_AGGREGATE_RANK_DEFICIENT = "inapplicable-aggregate-rank-deficient"


class Periodic1DRankNAlignmentBackendExceptionCode(StringWireEnum):
    """Classify an alignment backend failure without retaining exception text."""

    ARITHMETIC_NONFINITE = "backend-arithmetic-nonfinite"
    NONCONVERGENCE = "backend-nonconvergence"
    VALIDATION_FAILED = "backend-validation-failed"

    @classmethod
    def from_procrustes_exception(
        cls,
        exception: ArithmeticError | RuntimeError | ValueError,
    ) -> Self:
        """Classify one admitted Procrustes failure without retaining its message."""
        if not isinstance(exception, (ArithmeticError, RuntimeError, ValueError)):
            raise TypeError("exception must be an admitted Procrustes failure")
        if isinstance(exception, FloatingPointError):
            return cls.ARITHMETIC_NONFINITE
        if isinstance(exception, (LinAlgError, RuntimeError)):
            return cls.NONCONVERGENCE
        return cls.VALIDATION_FAILED


@dataclass(frozen=True, slots=True)
class Periodic1DRankNAlignmentStatusResult(BaseTypedRecord):
    """Record the outcome of one alignment family on one construction mesh.

    Parameters
    ----------
    case_identity
        Nonempty rank/depth identity ``rNN-LNN``.
    retained_rank, circuit_depth
        Built-in unitless integers selected from the band-alignment protocol.
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
    Python integers do not overflow; the protocol inventories bound their values.
    Boolean values and numeric strings are rejected. No absent downstream quantity is
    represented by a fabricated numeric zero.
    """

    case_identity: str
    retained_rank: int
    circuit_depth: int
    construction_mesh_size: int
    gauge_alignment: Periodic1DRankNGaugeAlignment
    status: Periodic1DRankNAlignmentStatus
    global_unitary_downstream_applicability: (
        Periodic1DRankNGlobalUnitaryDownstreamApplicability | None
    )
    backend_exception_code: Periodic1DRankNAlignmentBackendExceptionCode | None

    @classmethod
    def from_disposition(
        cls,
        *,
        case_identity: str,
        retained_rank: int,
        circuit_depth: int,
        construction_mesh_size: int,
        gauge_alignment: Periodic1DRankNGaugeAlignment,
        status: Periodic1DRankNAlignmentStatus,
        backend_exception_code: (
            Periodic1DRankNAlignmentBackendExceptionCode | None
        ) = None,
    ) -> Periodic1DRankNAlignmentStatusResult:
        """Construct one status with derived downstream applicability."""
        global_applicability_type = Periodic1DRankNGlobalUnitaryDownstreamApplicability
        applicability = None
        if (
            gauge_alignment is Periodic1DRankNGaugeAlignment.GLOBAL_UNITARY
            and status is Periodic1DRankNAlignmentStatus.QUALIFIED
        ):
            applicability = global_applicability_type.APPLICABLE
        elif (
            gauge_alignment is Periodic1DRankNGaugeAlignment.GLOBAL_UNITARY
            and status is Periodic1DRankNAlignmentStatus.AGGREGATE_RANK_DEFICIENT
        ):
            applicability = (
                global_applicability_type.INAPPLICABLE_AGGREGATE_RANK_DEFICIENT
            )
        return cls(
            case_identity=case_identity,
            retained_rank=retained_rank,
            circuit_depth=circuit_depth,
            construction_mesh_size=construction_mesh_size,
            gauge_alignment=gauge_alignment,
            status=status,
            global_unitary_downstream_applicability=applicability,
            backend_exception_code=backend_exception_code,
        )

    def __post_init__(self) -> None:
        """Validate the closed gauge-alignment-specific disposition inventory."""
        if type(self.case_identity) is not str:
            raise TypeError("case_identity must be a built-in string")
        if not self.case_identity:
            raise ValueError("case_identity must be nonempty")
        for value, name, allowed in (
            (self.retained_rank, "retained_rank", RETAINED_RANKS),
            (self.circuit_depth, "circuit_depth", CIRCUIT_DEPTHS),
            (
                self.construction_mesh_size,
                "construction_mesh_size",
                CONSTRUCTION_MESH_SIZES,
            ),
        ):
            if type(value) is not int:
                raise TypeError(f"{name} must be a built-in integer")
            if value not in allowed:
                raise ValueError(f"{name} is not in the frozen inventory")
        expected_case_identity = f"r{self.retained_rank:02d}-L{self.circuit_depth:02d}"
        if self.case_identity != expected_case_identity:
            raise ValueError("case_identity is inconsistent with rank and depth")
        if type(self.gauge_alignment) is not Periodic1DRankNGaugeAlignment:
            raise TypeError(
                "gauge_alignment must be the exact higher-rank gauge-alignment enum"
            )
        if type(self.status) is not Periodic1DRankNAlignmentStatus:
            raise TypeError("status must be the exact higher-rank status enum")
        if (
            self.global_unitary_downstream_applicability is not None
            and type(self.global_unitary_downstream_applicability)
            is not Periodic1DRankNGlobalUnitaryDownstreamApplicability
        ):
            raise TypeError(
                "global_unitary_downstream_applicability must be its exact enum or None"
            )
        if (
            self.backend_exception_code is not None
            and type(self.backend_exception_code)
            is not Periodic1DRankNAlignmentBackendExceptionCode
        ):
            raise TypeError("backend_exception_code must be its exact enum or None")

        permitted = {
            Periodic1DRankNGaugeAlignment.IDENTITY: (
                Periodic1DRankNAlignmentStatus.QUALIFIED,
                Periodic1DRankNAlignmentStatus.NUMERICALLY_UNRESOLVED,
            ),
            Periodic1DRankNGaugeAlignment.GLOBAL_UNITARY: (
                Periodic1DRankNAlignmentStatus.QUALIFIED,
                Periodic1DRankNAlignmentStatus.AGGREGATE_RANK_DEFICIENT,
                Periodic1DRankNAlignmentStatus.NUMERICALLY_UNRESOLVED,
                Periodic1DRankNAlignmentStatus.INTEGRITY_FAILED,
            ),
            Periodic1DRankNGaugeAlignment.POINTWISE_UNITARY: (
                Periodic1DRankNAlignmentStatus.QUALIFIED,
                Periodic1DRankNAlignmentStatus.POINTWISE_RANK_DEFICIENT,
                Periodic1DRankNAlignmentStatus.NUMERICALLY_UNRESOLVED,
                Periodic1DRankNAlignmentStatus.INTEGRITY_FAILED,
            ),
            Periodic1DRankNGaugeAlignment.KNOWN_INVERSE_ORACLE: (
                Periodic1DRankNAlignmentStatus.QUALIFIED,
                Periodic1DRankNAlignmentStatus.NUMERICALLY_UNRESOLVED,
                Periodic1DRankNAlignmentStatus.ORACLE_INTEGRITY_FAILED,
            ),
        }
        if self.status not in permitted[self.gauge_alignment]:
            raise ValueError(
                "status is not admissible for the selected gauge alignment"
            )

        if self.gauge_alignment is Periodic1DRankNGaugeAlignment.GLOBAL_UNITARY:
            expected_applicability = {
                Periodic1DRankNAlignmentStatus.QUALIFIED: (
                    Periodic1DRankNGlobalUnitaryDownstreamApplicability.APPLICABLE
                ),
                Periodic1DRankNAlignmentStatus.AGGREGATE_RANK_DEFICIENT: (
                    Periodic1DRankNGlobalUnitaryDownstreamApplicability.INAPPLICABLE_AGGREGATE_RANK_DEFICIENT
                ),
                Periodic1DRankNAlignmentStatus.NUMERICALLY_UNRESOLVED: None,
                Periodic1DRankNAlignmentStatus.INTEGRITY_FAILED: None,
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

        if self.status is Periodic1DRankNAlignmentStatus.NUMERICALLY_UNRESOLVED:
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
            "gauge_alignment": self.gauge_alignment.to_wire(),
            "status": self.status.to_wire(),
            "global_unitary_downstream_applicability": (
                None
                if self.global_unitary_downstream_applicability is None
                else self.global_unitary_downstream_applicability.to_wire()
            ),
            "backend_exception_code": (
                None
                if self.backend_exception_code is None
                else self.backend_exception_code.to_wire()
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
            gauge_alignment=Periodic1DRankNGaugeAlignment.from_wire(gauge_alignment),
            status=Periodic1DRankNAlignmentStatus.from_wire(status),
            global_unitary_downstream_applicability=(
                None
                if applicability is None
                else Periodic1DRankNGlobalUnitaryDownstreamApplicability.from_wire(
                    applicability
                )
            ),
            backend_exception_code=(
                None
                if exception_code is None
                else Periodic1DRankNAlignmentBackendExceptionCode.from_wire(
                    exception_code
                )
            ),
        )


__all__ = [
    "Periodic1DRankNAlignmentBackendExceptionCode",
    "Periodic1DRankNAlignmentStatus",
    "Periodic1DRankNAlignmentStatusResult",
    "Periodic1DRankNGlobalUnitaryDownstreamApplicability",
]
