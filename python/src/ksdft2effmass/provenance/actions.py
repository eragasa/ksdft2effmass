"""Stateless provenance verification and correlation ActionObjects."""

from __future__ import annotations

import re
from dataclasses import dataclass
from enum import StrEnum

from .records import ArtifactReference
from .tools import (
    ExternalExecutionFailure,
    ExternalExecutionOutcome,
    ExternalExecutionRequest,
    ExternalExecutionResult,
)

_MAX_U64 = 18_446_744_073_709_551_615
_ID_PATTERN = re.compile(r"[A-Za-z0-9][A-Za-z0-9._:-]{0,127}\Z")
_SHA256_PATTERN = re.compile(r"[0-9a-f]{64}\Z")


def _require_identifier(value: object, name: str) -> str:
    """Validate an owner-local portable result identifier."""
    if type(value) is not str:
        raise TypeError(f"{name} must be a built-in str")
    if _ID_PATTERN.fullmatch(value) is None:
        raise ValueError(f"{name} is not a portable identifier")
    return value


def _require_sha256(value: object, name: str) -> str:
    """Validate an owner-local lowercase SHA-256 digest."""
    if type(value) is not str:
        raise TypeError(f"{name} must be a built-in str")
    if _SHA256_PATTERN.fullmatch(value) is None:
        raise ValueError(f"{name} must be a lowercase SHA-256 digest")
    return value


class ArtifactIdentityVerificationStatus(StrEnum):
    """Derived exact content-identity verification outcome.

    Attributes
    ----------
    VERIFIED
        Observed digest and size both equal their expected values.
    MISMATCH
        At least one observed identity component differs.
    """

    VERIFIED = "verified"
    MISMATCH = "mismatch"


class CorrelationStatus(StrEnum):
    """Derived request/outcome identity-correlation outcome.

    Attributes
    ----------
    CORRELATED
        Request, correlation, and attempt identities all match.
    MISMATCH
        At least one required identity differs.
    """

    CORRELATED = "correlated"
    MISMATCH = "mismatch"


class CorrelationIssue(StrEnum):
    """Closed set of request/outcome correlation defects.

    Attributes
    ----------
    REQUEST_ID_MISMATCH, CORRELATION_ID_MISMATCH, ATTEMPT_ID_MISMATCH
        The corresponding immutable identity differs across the boundary.
    """

    REQUEST_ID_MISMATCH = "request_id_mismatch"
    CORRELATION_ID_MISMATCH = "correlation_id_mismatch"
    ATTEMPT_ID_MISMATCH = "attempt_id_mismatch"


@dataclass(frozen=True, slots=True)
class ArtifactIdentityVerificationResult:
    """Immutable result of exact SHA-256 and byte-size verification.

    Parameters
    ----------
    artifact_id
        Stable identity copied from the verified reference.
    expected_sha256, observed_sha256
        Expected and observed lowercase SHA-256 digests.
    expected_byte_size, observed_byte_size
        Expected and observed unsigned 64-bit byte sizes.

    Notes
    -----
    This result verifies represented bytes only.  It does not establish format
    validity, provenance truth, scientific meaning, or human acceptance.
    """

    artifact_id: str
    expected_sha256: str
    observed_sha256: str
    expected_byte_size: int
    observed_byte_size: int

    def __post_init__(self) -> None:
        _require_identifier(self.artifact_id, "artifact_id")
        if type(self.expected_byte_size) is not int:
            raise TypeError("expected_byte_size must be a built-in int excluding bool")
        if type(self.observed_byte_size) is not int:
            raise TypeError("observed_byte_size must be a built-in int excluding bool")
        if not 0 <= self.expected_byte_size <= _MAX_U64:
            raise ValueError("expected_byte_size must be in the unsigned 64-bit range")
        if not 0 <= self.observed_byte_size <= _MAX_U64:
            raise ValueError("observed_byte_size must be in the unsigned 64-bit range")
        _require_sha256(self.expected_sha256, "expected_sha256")
        _require_sha256(self.observed_sha256, "observed_sha256")

    @property
    def status(self) -> ArtifactIdentityVerificationStatus:
        """Derive verification status from exact digest and size equality."""
        matches = (
            self.expected_sha256 == self.observed_sha256
            and self.expected_byte_size == self.observed_byte_size
        )
        return (
            ArtifactIdentityVerificationStatus.VERIFIED
            if matches
            else ArtifactIdentityVerificationStatus.MISMATCH
        )


@dataclass(frozen=True, slots=True)
class ArtifactIdentityVerifier:
    """Stateless exact verifier for an observed artifact identity.

    The action accepts already observed values and performs no file access.
    """

    def execute(
        self,
        reference: ArtifactReference,
        observed_sha256: str,
        observed_byte_size: int,
    ) -> ArtifactIdentityVerificationResult:
        """Compare observed content identity with an artifact reference.

        Parameters
        ----------
        reference
            Portable artifact reference supplying expected identity.
        observed_sha256
            Observed 64-character lowercase SHA-256 digest.
        observed_byte_size
            Observed byte size in the unsigned 64-bit range.

        Returns
        -------
        ArtifactIdentityVerificationResult
            Exact, immutable comparison result.

        Raises
        ------
        TypeError
            If an argument has the wrong semantic type; booleans are not sizes.
        ValueError
            If an observed digest or byte size violates its intrinsic format.
        """
        if not isinstance(reference, ArtifactReference):
            raise TypeError("reference must be an ArtifactReference")
        _require_sha256(observed_sha256, "observed_sha256")
        if type(observed_byte_size) is not int:
            raise TypeError("observed_byte_size must be a built-in int excluding bool")
        if not 0 <= observed_byte_size <= _MAX_U64:
            raise ValueError("observed_byte_size must be in the unsigned 64-bit range")
        return ArtifactIdentityVerificationResult(
            artifact_id=reference.artifact_id,
            expected_sha256=reference.sha256,
            observed_sha256=observed_sha256,
            expected_byte_size=reference.byte_size,
            observed_byte_size=observed_byte_size,
        )


@dataclass(frozen=True, slots=True)
class ExecutionCorrelationResult:
    """Immutable result of request/outcome identity correlation.

    Parameters
    ----------
    request_id, outcome_id
        Inspected request and result-or-failure identities.
    issues
        Deterministically ordered request, correlation, and attempt defects.
    """

    request_id: str
    outcome_id: str
    issues: tuple[CorrelationIssue, ...]

    def __post_init__(self) -> None:
        _require_identifier(self.request_id, "request_id")
        _require_identifier(self.outcome_id, "outcome_id")
        if type(self.issues) is not tuple:
            raise TypeError("issues must be a built-in tuple")
        issues = tuple(self.issues)
        if not all(isinstance(issue, CorrelationIssue) for issue in issues):
            raise TypeError("issues must contain only CorrelationIssue values")
        canonical = tuple(
            issue
            for issue in (
                CorrelationIssue.REQUEST_ID_MISMATCH,
                CorrelationIssue.CORRELATION_ID_MISMATCH,
                CorrelationIssue.ATTEMPT_ID_MISMATCH,
            )
            if issue in issues
        )
        if canonical != issues or len(set(issues)) != len(issues):
            raise ValueError("issues must be unique and in deterministic enum order")

    @property
    def status(self) -> CorrelationStatus:
        """Derive correlation status from the exact issue tuple."""
        return (
            CorrelationStatus.CORRELATED
            if not self.issues
            else CorrelationStatus.MISMATCH
        )


@dataclass(frozen=True, slots=True)
class ExecutionOutcomeCorrelator:
    """Stateless verifier of immutable request/result-or-failure correlation."""

    def execute(
        self,
        request: ExternalExecutionRequest,
        outcome: ExternalExecutionOutcome,
    ) -> ExecutionCorrelationResult:
        """Verify request, correlation, and attempt IDs without mutation.

        Parameters
        ----------
        request
            Immutable external execution request.
        outcome
            Immutable external result or structured failure.

        Returns
        -------
        ExecutionCorrelationResult
            Deterministically ordered correlation findings.

        Raises
        ------
        TypeError
            If either argument is not an accepted public record type.
        """
        if not isinstance(request, ExternalExecutionRequest):
            raise TypeError("request must be an ExternalExecutionRequest")
        if not isinstance(outcome, (ExternalExecutionResult, ExternalExecutionFailure)):
            raise TypeError(
                "outcome must be an ExternalExecutionResult or ExternalExecutionFailure"
            )
        issues: list[CorrelationIssue] = []
        if request.request_id != outcome.request_id:
            issues.append(CorrelationIssue.REQUEST_ID_MISMATCH)
        if request.correlation_id != outcome.correlation_id:
            issues.append(CorrelationIssue.CORRELATION_ID_MISMATCH)
        if request.attempt_id != outcome.attempt_id:
            issues.append(CorrelationIssue.ATTEMPT_ID_MISMATCH)
        outcome_id = (
            outcome.result_id
            if isinstance(outcome, ExternalExecutionResult)
            else outcome.failure_id
        )
        return ExecutionCorrelationResult(
            request_id=request.request_id,
            outcome_id=outcome_id,
            issues=tuple(issues),
        )
