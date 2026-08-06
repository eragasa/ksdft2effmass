"""Represented artifact-identity verification and execution correlation.

This module defines immutable ResultObjects and stateless ActionObjects for two
nonnumerical operations.  :class:`ArtifactIdentityVerifier` compares an
already-observed SHA-256 digest and byte count with the expected values in an
:class:`~ksdft2effmass.provenance.ArtifactReference`.
:class:`ExecutionOutcomeCorrelator` compares the request, correlation, and
attempt identifiers of an immutable request and outcome.  Both operations use
exact equality and return deterministically represented findings.

The actions validate their direct scalar inputs but do not acquire observations,
read artifacts, resolve locations, execute tools, mutate records, or perform
serialization.  Digest-and-size agreement establishes represented byte identity,
not artifact availability, format validity, provenance truth, authorization, or
scientific meaning.  Identity correlation is independent of whether the outcome
represents completion or failure and does not establish successful execution,
solver convergence, numerical acceptance, scientific validation, or uncertainty
quantification.
"""

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


class ArtifactIdentityVerificationStatus(StrEnum):
    """Derived result of exact represented artifact-identity verification.

    Attributes
    ----------
    VERIFIED
        The observed lowercase SHA-256 digest and unsigned 64-bit byte size
        both equal the expected values exactly.
    MISMATCH
        The observed digest, byte size, or both differ from the expected
        values.

    Notes
    -----
    These values classify only the comparison represented by
    :class:`ArtifactIdentityVerificationResult`.  ``VERIFIED`` does not claim
    that this module observed or read the bytes, nor does it establish format,
    provenance, availability, or scientific validity.
    """

    VERIFIED = "verified"
    MISMATCH = "mismatch"


class CorrelationStatus(StrEnum):
    """Derived result of exact request/outcome identity correlation.

    Attributes
    ----------
    CORRELATED
        Request, correlation, and attempt identifiers all agree exactly.
    MISMATCH
        At least one of the three required identifiers differs.

    Notes
    -----
    Correlation is an identity claim, not a completion claim.  A structured
    failure with matching identifiers is ``CORRELATED``; a completed result
    with any differing identifier is ``MISMATCH``.
    """

    CORRELATED = "correlated"
    MISMATCH = "mismatch"


class CorrelationIssue(StrEnum):
    """Closed, deterministically ordered execution-correlation issue set.

    Attributes
    ----------
    REQUEST_ID_MISMATCH
        The outcome's request identifier differs from the inspected request's
        identifier.
    CORRELATION_ID_MISMATCH
        The outcome's correlation identifier differs from the inspected
        request's correlation identifier.
    ATTEMPT_ID_MISMATCH
        The outcome's attempt identifier differs from the inspected request's
        attempt identifier.

    Notes
    -----
    Issue tuples use the declaration order shown above: request, correlation,
    then attempt.  The vocabulary does not describe authorization, retry
    lineage, execution completion, output correctness, or scientific meaning.
    """

    REQUEST_ID_MISMATCH = "request_id_mismatch"
    CORRELATION_ID_MISMATCH = "correlation_id_mismatch"
    ATTEMPT_ID_MISMATCH = "attempt_id_mismatch"


@dataclass(frozen=True, slots=True)
class ArtifactIdentityVerificationResult:
    """Immutable result of an exact represented-byte identity comparison.

    Parameters
    ----------
    artifact_id
        Portable identifier of the referenced artifact.  It must be a built-in
        string matching ``[A-Za-z0-9][A-Za-z0-9._:-]{0,127}``.
    expected_sha256
        Expected SHA-256 digest, represented by exactly 64 lowercase
        hexadecimal characters.
    observed_sha256
        Already-observed SHA-256 digest, represented by exactly 64 lowercase
        hexadecimal characters.
    expected_byte_size
        Expected byte count as a built-in integer in the inclusive unsigned
        64-bit range $[0, 2^{64}-1]$.  Booleans are rejected.
    observed_byte_size
        Already-observed byte count under the same unsigned 64-bit contract.

    Raises
    ------
    TypeError
        If an identifier or digest is not a built-in :class:`str`, or a byte
        size is not a built-in :class:`int` excluding :class:`bool`.
    ValueError
        If the identifier grammar, exact digest representation, or unsigned
        64-bit range is violated.

    Notes
    -----
    All five fields are stored unchanged; construction performs no
    canonicalization, hashing, byte observation, or input/output.  ``status`` is
    derived on access and is neither stored constructor state nor a wire field.
    Agreement establishes only exact equality of the represented digest and
    size, not collision-free identity, format validity, provenance truth,
    artifact availability, or scientific validity.
    """

    artifact_id: str
    expected_sha256: str
    observed_sha256: str
    expected_byte_size: int
    observed_byte_size: int

    def __post_init__(self) -> None:
        """Validate the intrinsic identifier, digest, and byte-size fields."""
        if type(self.artifact_id) is not str:
            raise TypeError("artifact_id must be a built-in str")
        if (
            re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._:-]{0,127}\Z", self.artifact_id)
            is None
        ):
            raise ValueError("artifact_id is not a portable identifier")

        if type(self.expected_byte_size) is not int:
            raise TypeError("expected_byte_size must be a built-in int excluding bool")
        if type(self.observed_byte_size) is not int:
            raise TypeError("observed_byte_size must be a built-in int excluding bool")
        if not 0 <= self.expected_byte_size <= 18_446_744_073_709_551_615:
            raise ValueError("expected_byte_size must be in the unsigned 64-bit range")
        if not 0 <= self.observed_byte_size <= 18_446_744_073_709_551_615:
            raise ValueError("observed_byte_size must be in the unsigned 64-bit range")

        if type(self.expected_sha256) is not str:
            raise TypeError("expected_sha256 must be a built-in str")
        if re.fullmatch(r"[0-9a-f]{64}\Z", self.expected_sha256) is None:
            raise ValueError("expected_sha256 must be a lowercase SHA-256 digest")
        if type(self.observed_sha256) is not str:
            raise TypeError("observed_sha256 must be a built-in str")
        if re.fullmatch(r"[0-9a-f]{64}\Z", self.observed_sha256) is None:
            raise ValueError("observed_sha256 must be a lowercase SHA-256 digest")

    @property
    def status(self) -> ArtifactIdentityVerificationStatus:
        """Derive the exact represented identity-verification status.

        Returns
        -------
        ArtifactIdentityVerificationStatus
            :attr:`ArtifactIdentityVerificationStatus.VERIFIED` exactly when
            both digest and byte-size pairs compare equal; otherwise
            :attr:`ArtifactIdentityVerificationStatus.MISMATCH`.

        Notes
        -----
        The property has no tolerance, normalization, caching, mutation, or
        input/output.  Its result is not stored or serialized.
        """
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
    """Stateless ActionObject for exact represented artifact-identity comparison.

    The action has no constructor parameters or stored policy.  Callers provide
    an immutable reference and values observed elsewhere to :meth:`execute`.
    The action performs no file access, digest computation, location resolution,
    observation acquisition, or artifact mutation.
    """

    def execute(
        self,
        reference: ArtifactReference,
        observed_sha256: str,
        observed_byte_size: int,
    ) -> ArtifactIdentityVerificationResult:
        """Compare already-observed content identity with a reference.

        Parameters
        ----------
        reference
            Immutable artifact reference supplying ``artifact_id``, expected
            lowercase SHA-256 digest, and expected byte size.
        observed_sha256
            Digest obtained by a separately controlled observation boundary,
            expressed as exactly 64 lowercase hexadecimal characters.  The
            value is checked but not normalized or recomputed.
        observed_byte_size
            Byte count obtained by that boundary, expressed as a built-in
            integer in $[0, 2^{64}-1]$; booleans are rejected.

        Returns
        -------
        ArtifactIdentityVerificationResult
            Immutable expected/observed values whose ``status`` is derived by
            exact digest and size equality.

        Raises
        ------
        TypeError
            If ``reference`` is not an :class:`ArtifactReference`, the digest
            is not a built-in string, or the size is not a built-in integer
            excluding booleans.
        ValueError
            If the observed digest is not exactly 64 lowercase hexadecimal
            characters or the observed size is outside the unsigned 64-bit
            range.

        Notes
        -----
        The result reports represented identity agreement only.  This method
        neither reads bytes nor establishes format correctness, provenance,
        availability, authorization, or scientific acceptance.
        """
        if not isinstance(reference, ArtifactReference):
            raise TypeError("reference must be an ArtifactReference")
        if type(observed_sha256) is not str:
            raise TypeError("observed_sha256 must be a built-in str")
        if re.fullmatch(r"[0-9a-f]{64}\Z", observed_sha256) is None:
            raise ValueError("observed_sha256 must be a lowercase SHA-256 digest")
        if type(observed_byte_size) is not int:
            raise TypeError("observed_byte_size must be a built-in int excluding bool")
        if not 0 <= observed_byte_size <= 18_446_744_073_709_551_615:
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
    """Immutable result of exact request/outcome identity correlation.

    Parameters
    ----------
    request_id
        Portable identifier of the inspected request, stored unchanged.  It
        must match ``[A-Za-z0-9][A-Za-z0-9._:-]{0,127}``.
    outcome_id
        Portable ``result_id`` or ``failure_id`` of the inspected outcome,
        stored unchanged under the same identifier grammar.
    issues
        Built-in tuple of :class:`CorrelationIssue` members.  Members must be
        unique and appear in deterministic request, correlation, then attempt
        order; any ordered subset is valid.

    Raises
    ------
    TypeError
        If an identifier is not a built-in string, ``issues`` is not a built-in
        tuple, or a member is not a :class:`CorrelationIssue`.
    ValueError
        If an identifier violates the portable grammar or issues are duplicated
        or out of deterministic order.

    Notes
    -----
    Construction performs validation but no canonicalization: identifiers and
    the issue tuple are retained as supplied.  ``status`` is derived from issue
    emptiness and is neither stored constructor state nor a wire field.  The
    result does not retain the correlation or attempt identifiers themselves;
    it records their mismatches through ``issues``.  Correlation neither
    executes a request nor interprets completion, failure, artifacts,
    authorization, retry lineage, or scientific correctness.
    """

    request_id: str
    outcome_id: str
    issues: tuple[CorrelationIssue, ...]

    def __post_init__(self) -> None:
        """Validate identifiers and the canonical issue-set representation."""
        if type(self.request_id) is not str:
            raise TypeError("request_id must be a built-in str")
        if (
            re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._:-]{0,127}\Z", self.request_id)
            is None
        ):
            raise ValueError("request_id is not a portable identifier")
        if type(self.outcome_id) is not str:
            raise TypeError("outcome_id must be a built-in str")
        if (
            re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._:-]{0,127}\Z", self.outcome_id)
            is None
        ):
            raise ValueError("outcome_id is not a portable identifier")
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
        """Derive identity-correlation status from the exact issue tuple.

        Returns
        -------
        CorrelationStatus
            :attr:`CorrelationStatus.CORRELATED` when ``issues`` is empty;
            otherwise :attr:`CorrelationStatus.MISMATCH`.

        Notes
        -----
        The property is unstored and has no side effects.  It intentionally
        does not consult an external result's completion status or distinguish
        a completed result from a structured failure.
        """
        return (
            CorrelationStatus.CORRELATED
            if not self.issues
            else CorrelationStatus.MISMATCH
        )


@dataclass(frozen=True, slots=True)
class ExecutionOutcomeCorrelator:
    """Stateless ActionObject for request/result-or-failure identity correlation.

    The action has no constructor parameters or stored policy.  It compares
    three immutable identity joins and emits a deterministic issue tuple.  It
    performs no external execution, input/output, retry, authorization check,
    output inspection, or mutation.
    """

    def execute(
        self,
        request: ExternalExecutionRequest,
        outcome: ExternalExecutionOutcome,
    ) -> ExecutionCorrelationResult:
        """Correlate a request with an immutable result or failure.

        Parameters
        ----------
        request
            Immutable request supplying the authoritative ``request_id``,
            ``correlation_id``, and ``attempt_id`` for this comparison.
        outcome
            Immutable :class:`ExternalExecutionResult` or
            :class:`ExternalExecutionFailure` supplying copied join identities
            and its own ``result_id`` or ``failure_id``.

        Returns
        -------
        ExecutionCorrelationResult
            Result containing the request identifier, the outcome's own
            identifier, and a unique issue tuple ordered by request,
            correlation, then attempt mismatch.

        Raises
        ------
        TypeError
            If ``request`` is not an :class:`ExternalExecutionRequest` or
            ``outcome`` is neither an :class:`ExternalExecutionResult` nor an
            :class:`ExternalExecutionFailure`.  Inputs are not coerced.

        Notes
        -----
        Each identifier comparison uses exact string equality.  A matching
        failure is correlated, while a completed result with a differing join
        identity is not.  The method does not execute the request or establish
        authorization, completion, output validity, provenance truth, solver
        convergence, numerical acceptance, or scientific validity.
        """
        if not isinstance(request, ExternalExecutionRequest):
            raise TypeError("request must be an ExternalExecutionRequest")
        if not isinstance(outcome, (ExternalExecutionResult, ExternalExecutionFailure)):
            raise TypeError(
                "outcome must be an ExternalExecutionResult or ExternalExecutionFailure"
            )

        # The public issue order is part of the deterministic result contract.
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
