"""Typed backend-failure evidence for rank-N frame transport."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Self

from projectkoios.physkit.solidstate.electronic.frame_transport import (
    ClosedLoopPolarFrameTransportBackendFailure,
    ClosedLoopPolarFrameTransportBackendFailureReason,
    ClosedLoopPolarFrameTransportBackendOperation,
)

from ksdft2effmass.periodic1d.rankN.band_alignment.configuration import (
    Periodic1DRankNAlignmentConfiguration,
)
from ksdft2effmass.serialization import (
    BaseTypedRecord,
    SerializableValue,
    StringWireEnum,
)


class Periodic1DRankNTransportBackendExceptionCode(StringWireEnum):
    """Classify a frame-transport backend failure without exception text."""

    ARITHMETIC_NONFINITE = "backend-arithmetic-nonfinite"
    NONCONVERGENCE = "backend-nonconvergence"
    VALIDATION_FAILED = "backend-validation-failed"

    @classmethod
    def from_owner_reason(
        cls,
        reason: ClosedLoopPolarFrameTransportBackendFailureReason,
    ) -> Self:
        """Classify one admitted PhysKit frame-transport failure reason."""
        if type(reason) is not ClosedLoopPolarFrameTransportBackendFailureReason:
            raise TypeError("reason must be the exact transport failure-reason enum")
        return {
            ClosedLoopPolarFrameTransportBackendFailureReason.NONFINITE_OUTPUT: (
                cls.ARITHMETIC_NONFINITE
            ),
            ClosedLoopPolarFrameTransportBackendFailureReason.NONCONVERGENCE: (
                cls.NONCONVERGENCE
            ),
            ClosedLoopPolarFrameTransportBackendFailureReason.INVALID_DECOMPOSITION: (
                cls.VALIDATION_FAILED
            ),
        }[reason]


@dataclass(frozen=True, slots=True)
class Periodic1DRankNAlignmentTransportBackendFailureResult(BaseTypedRecord):
    """Record one numerical transport failure without runtime exception text.

    Parameters
    ----------
    case_identity
        Nonempty rank/depth identity ``rNN-LNN``.
    retained_rank, circuit_depth
        Built-in unitless integers selected from the frozen inventories.
    construction_mesh_size
        Built-in integer route length ``M``.
    operation, reason
        Exact upstream operation and closed failure-reason enums.
    link_index
        Zero-based built-in integer route-link index. The closure link is ``M - 1``.
    backend_exception_code
        Stable frame-transport classification derived from ``reason``.

    Notes
    -----
    Python integers do not overflow and are bounded by the selected inventories. Boolean
    values are rejected. Backend exception messages are intentionally excluded because
    they are unstable and may disclose environment-specific information.
    """

    case_identity: str
    retained_rank: int
    circuit_depth: int
    construction_mesh_size: int
    operation: ClosedLoopPolarFrameTransportBackendOperation
    reason: ClosedLoopPolarFrameTransportBackendFailureReason
    link_index: int
    backend_exception_code: Periodic1DRankNTransportBackendExceptionCode

    def __post_init__(self) -> None:
        """Validate case, route index, and exact owner classification."""
        if type(self.case_identity) is not str:
            raise TypeError("case_identity must be a built-in string")
        if not self.case_identity:
            raise ValueError("case_identity must be nonempty")
        if self.case_identity != f"r{self.retained_rank:02d}-L{self.circuit_depth:02d}":
            raise ValueError("case_identity is inconsistent with rank and depth")
        for value, name, allowed in (
            (
                self.retained_rank,
                "retained_rank",
                Periodic1DRankNAlignmentConfiguration.RETAINED_RANKS,
            ),
            (
                self.circuit_depth,
                "circuit_depth",
                Periodic1DRankNAlignmentConfiguration.CIRCUIT_DEPTHS,
            ),
            (
                self.construction_mesh_size,
                "construction_mesh_size",
                Periodic1DRankNAlignmentConfiguration.CONSTRUCTION_MESH_SIZES,
            ),
        ):
            if type(value) is not int:
                raise TypeError(f"{name} must be a built-in integer")
            if value not in allowed:
                raise ValueError(f"{name} is not in the frozen inventory")
        if type(self.operation) is not ClosedLoopPolarFrameTransportBackendOperation:
            raise TypeError("operation must be the exact owner operation enum")
        if type(self.reason) is not ClosedLoopPolarFrameTransportBackendFailureReason:
            raise TypeError("reason must be the exact owner failure-reason enum")
        if type(self.link_index) is not int:
            raise TypeError("link_index must be a built-in integer")
        if not 0 <= self.link_index < self.construction_mesh_size:
            raise ValueError("link_index lies outside the selected closed route")
        if (
            self.operation
            is ClosedLoopPolarFrameTransportBackendOperation.CLOSURE_SCHUR
            and self.link_index != self.construction_mesh_size - 1
        ):
            raise ValueError("closure Schur failures must identify the closure link")
        if type(self.backend_exception_code) is not (
            Periodic1DRankNTransportBackendExceptionCode
        ):
            raise TypeError("backend_exception_code must be the exact transport enum")
        expected_code = Periodic1DRankNTransportBackendExceptionCode.from_owner_reason(
            self.reason
        )
        if self.backend_exception_code is not expected_code:
            raise ValueError(
                "owner failure reason and transport exception code disagree"
            )

    @classmethod
    def from_owner_failure(
        cls,
        *,
        case_identity: str,
        retained_rank: int,
        circuit_depth: int,
        construction_mesh_size: int,
        failure: ClosedLoopPolarFrameTransportBackendFailure,
    ) -> Self:
        """Translate only the closed typed owner failure inventory."""
        if type(failure) is not ClosedLoopPolarFrameTransportBackendFailure:
            raise TypeError(
                "failure must be ClosedLoopPolarFrameTransportBackendFailure"
            )
        return cls(
            case_identity=case_identity,
            retained_rank=retained_rank,
            circuit_depth=circuit_depth,
            construction_mesh_size=construction_mesh_size,
            operation=failure.operation,
            reason=failure.reason,
            link_index=failure.link_index,
            backend_exception_code=(
                Periodic1DRankNTransportBackendExceptionCode.from_owner_reason(
                    failure.reason
                )
            ),
        )

    def _mapping(self) -> Mapping[str, SerializableValue]:
        return {
            "case_identity": self.case_identity,
            "retained_rank": self.retained_rank,
            "circuit_depth": self.circuit_depth,
            "construction_mesh_size": self.construction_mesh_size,
            "operation": self.operation.value,
            "reason": self.reason.value,
            "link_index": self.link_index,
            "backend_exception_code": self.backend_exception_code.value,
        }

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        required = {
            "case_identity",
            "retained_rank",
            "circuit_depth",
            "construction_mesh_size",
            "operation",
            "reason",
            "link_index",
            "backend_exception_code",
        }
        if set(values) != required:
            raise ValueError("transport backend-failure result fields do not match")
        case_identity = values["case_identity"]
        operation = values["operation"]
        reason = values["reason"]
        exception_code = values["backend_exception_code"]
        if type(case_identity) is not str:
            raise TypeError("case_identity must decode to a string")
        if (
            type(operation) is not str
            or type(reason) is not str
            or type(exception_code) is not str
        ):
            raise TypeError("operation, reason, and exception code must be strings")
        integer_names = (
            "retained_rank",
            "circuit_depth",
            "construction_mesh_size",
            "link_index",
        )
        integers: dict[str, int] = {}
        for name in integer_names:
            value = values[name]
            if type(value) is not int:
                raise TypeError(f"{name} must decode to a built-in integer")
            integers[name] = value
        return cls(
            case_identity=case_identity,
            retained_rank=integers["retained_rank"],
            circuit_depth=integers["circuit_depth"],
            construction_mesh_size=integers["construction_mesh_size"],
            operation=ClosedLoopPolarFrameTransportBackendOperation(operation),
            reason=ClosedLoopPolarFrameTransportBackendFailureReason(reason),
            link_index=integers["link_index"],
            backend_exception_code=Periodic1DRankNTransportBackendExceptionCode(
                exception_code
            ),
        )


__all__ = [
    "Periodic1DRankNAlignmentTransportBackendFailureResult",
    "Periodic1DRankNTransportBackendExceptionCode",
]
