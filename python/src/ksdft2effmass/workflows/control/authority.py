"""Effect-free simulation-execution authorization ActionObject."""

from __future__ import annotations

from typing import final

from ..runs.authority import (
    ScientificExecutionAuthorityGrant,
    ScientificExecutionAuthoritySnapshot,
    ScientificExecutionAuthorityVerificationKind,
    ScientificExecutionGrantState,
    SimulationExecutionAuthorizationOutcomeKind,
    SimulationExecutionAuthorizationPhase,
    SimulationExecutionAuthorizationRequest,
    SimulationExecutionAuthorizationResult,
)

__all__ = [
    "ScientificExecutionAuthorityGrant",
    "ScientificExecutionAuthoritySnapshot",
    "ScientificExecutionAuthorityVerificationKind",
    "ScientificExecutionGrantState",
    "SimulationExecutionAuthorizationOutcomeKind",
    "SimulationExecutionAuthorizationPhase",
    "SimulationExecutionAuthorizationRequest",
    "SimulationExecutionAuthorizationResult",
    "SimulationExecutionAuthorizer",
]


@final
class SimulationExecutionAuthorizer:
    """Authorize one exact preparation or claim against supplied authority state.

    The ActionObject is deterministic and effect-free.  It compares independently
    valid immutable inputs and returns a closed result.  Verification failure,
    stale or revoked state, phase mismatch, and scope mismatch are denials;
    indeterminate authority checks are errors.  Only an exact authorized result may
    proceed to reservation or dispatch.
    """

    @staticmethod
    def execute(
        request: SimulationExecutionAuthorizationRequest,
    ) -> SimulationExecutionAuthorizationResult:
        """Evaluate one exact request without issuing authority or effects."""
        return SimulationExecutionAuthorizationResult.evaluate(request)

    @staticmethod
    def implementation_identity() -> str:
        """Return the exact in-memory authorizer implementation identity."""
        return SimulationExecutionAuthorizationResult.implementation_identity()
