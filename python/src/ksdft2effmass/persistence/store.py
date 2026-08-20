"""Opaque single-stream revision persistence contracts.

This module defines immutable generic revision values and the structural
:class:`AtomicRevisionStore` protocol.  A revision carries exact identities and
opaque bytes; the store does not interpret Harness, Workflow, calculator, or
scientific state.  Compare-and-swap, idempotency, and closed read and commit
outcomes belong to a concrete store implementation.

The contracts provide software behavior only.  They do not establish durable
storage, domain validity, numerical verification, scientific validation, or
uncertainty quantification.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Protocol, runtime_checkable

IdentityObservation = tuple[tuple[str, str | None], ...]


def _require_identifier(value: object, field: str) -> str:
    if type(value) is not str:
        raise TypeError(f"{field} must be a built-in str")
    if not value:
        raise ValueError(f"{field} must not be empty")
    return value


def _require_optional_identifier(value: object, field: str) -> str | None:
    if value is None:
        return None
    return _require_identifier(value, field)


def _require_tuple_of_strings(value: object, field: str) -> tuple[str, ...]:
    if type(value) is not tuple:
        raise TypeError(f"{field} must be a tuple")
    for item in value:
        _require_identifier(item, f"{field} item")
    return value


def _require_observation(value: object, field: str) -> IdentityObservation:
    if type(value) is not tuple:
        raise TypeError(f"{field} must be a tuple")
    names: list[str] = []
    for item in value:
        if type(item) is not tuple or len(item) != 2:
            raise TypeError(f"{field} items must be two-item tuples")
        name, identity = item
        names.append(_require_identifier(name, f"{field} field name"))
        _require_optional_identifier(identity, f"{field} identity")
    if names != sorted(names) or len(names) != len(set(names)):
        raise ValueError(f"{field} field names must be unique and sorted")
    return value


def _require_enum(value: object, expected: type[StrEnum], field: str) -> None:
    if type(value) is not expected:
        raise TypeError(f"{field} must be {expected.__name__}")


class RevisionSelector(StrEnum):
    """Select the latest or one explicit revision of a stream."""

    LATEST = "latest"
    """Observe the stream's latest revision without reconciliation expectations."""

    EXPLICIT_REVISION = "explicit_revision"
    """Observe one exact revision, optionally with complete expectations."""


class RevisionReadStatus(StrEnum):
    """Closed outcome vocabulary for a generic revision read."""

    FOUND = "found"
    """A well-formed revision satisfying every supplied expectation was found."""
    ABSENT = "absent"
    """The exact requested address was established as absent."""
    MISMATCH = "mismatch"
    """Stored generic identities conflict with supplied expectations."""
    INCOMPATIBLE = "incompatible"
    """A store or revision-envelope version is unsupported."""
    CORRUPT = "corrupt"
    """Generic revision or content integrity failed."""
    INDETERMINATE = "indeterminate"
    """Presence or integrity could not be established."""
    ERROR = "error"
    """An operational failure establishes neither presence nor absence."""


class CommitStatus(StrEnum):
    """Closed outcome vocabulary for an atomic commit."""

    COMMITTED = "committed"
    """The candidate is committed, including an exact idempotency replay."""
    CONFLICT = "conflict"
    """Compare-and-swap or idempotency closure conflicts with stored state."""
    INDETERMINATE = "indeterminate"
    """The durable commit outcome could not be established."""
    ERROR = "error"
    """An operational failure does not imply a commit or conflict."""


@dataclass(frozen=True, slots=True)
class Revision:
    """Represent one complete opaque revision of one stream.

    Parameters
    ----------
    stream_id
        Logical single-stream identity.
    revision_id
        Identity of this exact revision.
    predecessor_revision_id
        Exact predecessor revision identity, or ``None`` for the first revision.
    schema_id
        Identity of the payload schema; the shared store does not interpret it.
    content_id
        Identity of the exact payload bytes under the caller's domain contract.
    payload
        Exact immutable built-in bytes for the complete aggregate.

    Raises
    ------
    TypeError
        If an identity is not a built-in string or ``payload`` is not built-in
        :class:`bytes`.
    ValueError
        If a required identity is empty or a revision names itself as predecessor.
    """

    stream_id: str
    revision_id: str
    predecessor_revision_id: str | None
    schema_id: str
    content_id: str
    payload: bytes

    def __post_init__(self) -> None:
        _require_identifier(self.stream_id, "stream_id")
        _require_identifier(self.revision_id, "revision_id")
        _require_optional_identifier(
            self.predecessor_revision_id, "predecessor_revision_id"
        )
        _require_identifier(self.schema_id, "schema_id")
        _require_identifier(self.content_id, "content_id")
        if type(self.payload) is not bytes:
            raise TypeError("payload must be built-in bytes")
        if self.predecessor_revision_id == self.revision_id:
            raise ValueError("a revision must not name itself as predecessor")


@dataclass(frozen=True, slots=True)
class RevisionReadRequest:
    """Request one explicit, identity-bound revision observation.

    ``latest`` prohibits an explicit revision and reconciliation expectations.
    ``explicit_revision`` requires ``revision_id`` and accepts either no
    expectations or the complete four-field expectation group.  In a complete
    group, ``expected_predecessor_revision_id=None`` explicitly means that no
    predecessor is expected; presence of the other three required identities
    distinguishes this from an absent expectation group.

    Parameters
    ----------
    request_id
        Identity of this read request.
    stream_id
        Exact stream to observe.
    selector
        Latest-versus-explicit selector.
    revision_id
        Exact requested revision for ``explicit_revision``; otherwise ``None``.
    expected_predecessor_revision_id
        Expected predecessor slot, including explicit ``None`` for no predecessor.
    expected_schema_id, expected_content_id, expected_idempotency_id
        Remaining exact reconciliation identities.  They are all ``None`` when
        expectations are absent and all non-``None`` when expectations are present.

    Raises
    ------
    TypeError
        If an identity or selector has the wrong semantic type.
    ValueError
        If an identity is empty or selector/address/expectation closure fails.
    """

    request_id: str
    stream_id: str
    selector: RevisionSelector
    revision_id: str | None = None
    expected_predecessor_revision_id: str | None = None
    expected_schema_id: str | None = None
    expected_content_id: str | None = None
    expected_idempotency_id: str | None = None

    def __post_init__(self) -> None:
        _require_identifier(self.request_id, "request_id")
        _require_identifier(self.stream_id, "stream_id")
        _require_enum(self.selector, RevisionSelector, "selector")
        _require_optional_identifier(self.revision_id, "revision_id")
        _require_optional_identifier(
            self.expected_predecessor_revision_id,
            "expected_predecessor_revision_id",
        )
        expectation_tail = (
            self.expected_schema_id,
            self.expected_content_id,
            self.expected_idempotency_id,
        )
        for field, value in zip(
            ("expected_schema_id", "expected_content_id", "expected_idempotency_id"),
            expectation_tail,
            strict=True,
        ):
            _require_optional_identifier(value, field)
        if self.selector is RevisionSelector.LATEST:
            if self.revision_id is not None or any(
                value is not None
                for value in (
                    self.expected_predecessor_revision_id,
                    *expectation_tail,
                )
            ):
                raise ValueError(
                    "latest reads prohibit revision and reconciliation expectations"
                )
        elif self.revision_id is None:
            raise ValueError("explicit_revision reads require revision_id")
        present = tuple(value is not None for value in expectation_tail)
        if (any(present) and not all(present)) or (
            self.expected_predecessor_revision_id is not None and not all(present)
        ):
            raise ValueError("reconciliation expectations must be complete")

    @property
    def has_reconciliation_expectations(self) -> bool:
        """Whether the complete reconciliation expectation group is present."""
        return self.expected_schema_id is not None


@dataclass(frozen=True, slots=True)
class Commit:
    """Bind one candidate revision to compare-and-swap and idempotency identities.

    Parameters
    ----------
    expected_revision_id
        Expected current revision, or ``None`` when the stream must be absent.
    candidate
        Complete candidate whose predecessor must equal the expected revision.
    idempotency_id
        Identity binding the complete commit, including all candidate bytes.

    Raises
    ------
    TypeError
        If a field has the wrong semantic type.
    ValueError
        If an identity is empty or the predecessor and expectation differ.
    """

    expected_revision_id: str | None
    candidate: Revision
    idempotency_id: str

    def __post_init__(self) -> None:
        _require_optional_identifier(self.expected_revision_id, "expected_revision_id")
        if type(self.candidate) is not Revision:
            raise TypeError("candidate must be Revision")
        _require_identifier(self.idempotency_id, "idempotency_id")
        if self.candidate.predecessor_revision_id != self.expected_revision_id:
            raise ValueError(
                "candidate predecessor_revision_id must equal expected_revision_id"
            )


@dataclass(frozen=True, slots=True)
class StoreOperationalFailure:
    """Represent a sanitized generic store-operation failure.

    Parameters
    ----------
    failure_id
        Identity of this failure observation.
    operation_phase
        Exact read or commit phase that failed.
    implementation_id
        Exact implementation identity that produced the failure.
    code
        Stable implementation-owned failure code.
    expected_condition, observed_condition
        Sanitized expected and observed conditions.
    diagnostic
        Sanitized diagnostic text.
    retryable
        Explicit retryability when known, otherwise ``None``.
    claim_boundary
        Non-empty statement limiting what the failure establishes.
    """

    failure_id: str
    operation_phase: str
    implementation_id: str
    code: str
    expected_condition: str
    observed_condition: str
    diagnostic: str
    retryable: bool | None
    claim_boundary: str

    def __post_init__(self) -> None:
        for field in (
            "failure_id",
            "operation_phase",
            "implementation_id",
            "code",
            "expected_condition",
            "observed_condition",
            "diagnostic",
            "claim_boundary",
        ):
            _require_identifier(getattr(self, field), field)
        if self.retryable is not None and type(self.retryable) is not bool:
            raise TypeError("retryable must be bool or None")


@dataclass(frozen=True, slots=True)
class RevisionReadResult:
    """Represent one closed generic revision-read outcome.

    Parameters
    ----------
    result_id, request_id, stream_id
        Exact result, originating request, and observed stream identities.
    selector
        Selector copied from the originating request.
    store_implementation_id, store_version_id
        Exact concrete-store implementation and version identities.
    status
        Closed read outcome discriminant.
    diagnostics
        Ordered sanitized diagnostic strings; an empty tuple is permitted.
    claim_boundary
        Non-empty statement limiting what the observation establishes.
    revision
        Complete revision, required only for ``found``.
    expectations_matched
        ``True`` when supplied reconciliation expectations matched; ``None`` when
        no confirmation is represented.  ``False`` is prohibited for ``found``.
    requested_revision_id, absence_observation
        Optional explicit address and required absence evidence for ``absent``.
    expected_identities, observed_identities
        Sorted immutable ``(field_name, identity_or_none)`` observations used by
        ``mismatch`` and, for observed identities only, ``corrupt``.
    mismatched_fields
        Ordered non-empty mismatched field names required by ``mismatch``.
    unsupported_version_ids, compatibility_finding
        Ordered non-empty unsupported store or envelope version identities and a
        sanitized finding required for ``incompatible``.
    integrity_findings
        Ordered non-empty integrity findings required by ``corrupt``.
    failure
        Structured failure required by ``indeterminate`` and ``error``.

    Raises
    ------
    TypeError
        If a field has the wrong semantic type.
    ValueError
        If an identity, observation ordering, or status-variant invariant fails.

    Notes
    -----
    Only ``found`` contains a revision. Identity observations diagnose generic
    conflicts and never contain a domain snapshot.
    """

    result_id: str
    request_id: str
    stream_id: str
    selector: RevisionSelector
    store_implementation_id: str
    store_version_id: str
    status: RevisionReadStatus
    diagnostics: tuple[str, ...]
    claim_boundary: str
    revision: Revision | None = None
    expectations_matched: bool | None = None
    requested_revision_id: str | None = None
    absence_observation: str | None = None
    expected_identities: IdentityObservation = ()
    observed_identities: IdentityObservation = ()
    mismatched_fields: tuple[str, ...] = ()
    unsupported_version_ids: tuple[str, ...] = ()
    compatibility_finding: str | None = None
    integrity_findings: tuple[str, ...] = ()
    failure: StoreOperationalFailure | None = None

    def __post_init__(self) -> None:
        for field in (
            "result_id",
            "request_id",
            "stream_id",
            "store_implementation_id",
            "store_version_id",
            "claim_boundary",
        ):
            _require_identifier(getattr(self, field), field)
        _require_enum(self.selector, RevisionSelector, "selector")
        _require_enum(self.status, RevisionReadStatus, "status")
        _require_tuple_of_strings(self.diagnostics, "diagnostics")
        _require_optional_identifier(
            self.requested_revision_id, "requested_revision_id"
        )
        _require_optional_identifier(self.absence_observation, "absence_observation")
        _require_observation(self.expected_identities, "expected_identities")
        _require_observation(self.observed_identities, "observed_identities")
        _require_tuple_of_strings(self.mismatched_fields, "mismatched_fields")
        _require_tuple_of_strings(
            self.unsupported_version_ids, "unsupported_version_ids"
        )
        _require_optional_identifier(
            self.compatibility_finding, "compatibility_finding"
        )
        _require_tuple_of_strings(self.integrity_findings, "integrity_findings")
        if self.revision is not None and type(self.revision) is not Revision:
            raise TypeError("revision must be Revision or None")
        if (
            self.expectations_matched is not None
            and type(self.expectations_matched) is not bool
        ):
            raise TypeError("expectations_matched must be bool or None")
        if (
            self.failure is not None
            and type(self.failure) is not StoreOperationalFailure
        ):
            raise TypeError("failure must be StoreOperationalFailure or None")
        self._validate_variant()

    def _validate_variant(self) -> None:
        variant_fields = {
            "revision": self.revision is not None,
            "expectations": self.expectations_matched is not None,
            "requested": self.requested_revision_id is not None,
            "absence": self.absence_observation is not None,
            "expected": bool(self.expected_identities),
            "observed": bool(self.observed_identities),
            "mismatched": bool(self.mismatched_fields),
            "unsupported": bool(self.unsupported_version_ids),
            "compatibility": self.compatibility_finding is not None,
            "integrity": bool(self.integrity_findings),
            "failure": self.failure is not None,
        }
        required: set[str]
        allowed: set[str]
        if self.status is RevisionReadStatus.FOUND:
            required = {"revision"}
            allowed = {"revision", "expectations"}
            if self.revision is not None and self.revision.stream_id != self.stream_id:
                raise ValueError("found revision stream_id must equal result stream_id")
        elif self.status is RevisionReadStatus.ABSENT:
            required = {"absence"}
            allowed = {"requested", "absence"}
            if (
                self.selector is RevisionSelector.EXPLICIT_REVISION
                and self.requested_revision_id is None
            ):
                raise ValueError(
                    "explicit_revision absent requires requested_revision_id"
                )
        elif self.status is RevisionReadStatus.MISMATCH:
            required = {"expected", "observed", "mismatched"}
            allowed = required | {"requested"}
            expected_names = tuple(name for name, _ in self.expected_identities)
            observed_names = tuple(name for name, _ in self.observed_identities)
            required_expected_names = (
                "content_id",
                "idempotency_id",
                "predecessor_revision_id",
                "schema_id",
            )
            if expected_names != required_expected_names:
                raise ValueError(
                    "mismatch requires the complete expected generic identity set"
                )
            if tuple(sorted(set(self.mismatched_fields))) != self.mismatched_fields:
                raise ValueError("mismatched_fields must be unique and sorted")
            if observed_names != self.mismatched_fields:
                raise ValueError(
                    "observed mismatch identities must equal mismatched_fields"
                )
            if (
                self.selector is RevisionSelector.EXPLICIT_REVISION
                and self.requested_revision_id is None
            ):
                raise ValueError(
                    "explicit_revision mismatch requires requested_revision_id"
                )
        elif self.status is RevisionReadStatus.INCOMPATIBLE:
            required = {"unsupported", "compatibility"}
            allowed = required
        elif self.status is RevisionReadStatus.CORRUPT:
            required = {"integrity"}
            allowed = required | {"observed"}
        else:
            required = {"failure"}
            allowed = required
        present = {name for name, is_present in variant_fields.items() if is_present}
        if not required <= present:
            missing = sorted(required - present)[0]
            raise ValueError(f"{self.status.value} requires {missing}")
        prohibited = present - allowed
        if prohibited:
            raise ValueError(f"{self.status.value} prohibits {sorted(prohibited)[0]}")
        if (
            self.status is RevisionReadStatus.FOUND
            and self.expectations_matched is False
        ):
            raise ValueError("found result cannot report failed expectations")


@dataclass(frozen=True, slots=True)
class CommitResult:
    """Represent one closed atomic-commit outcome.

    Parameters
    ----------
    result_id, idempotency_id, stream_id
        Exact result, originating idempotency, and target stream identities.
    store_implementation_id, store_version_id
        Exact concrete-store implementation and version identities.
    status
        Closed commit outcome discriminant.
    diagnostics
        Ordered sanitized diagnostic strings; an empty tuple is permitted.
    claim_boundary
        Non-empty statement limiting what the outcome establishes.
    revision
        Committed revision, required only for ``committed``.  An exact idempotency
        replay returns the original committed revision through this field.
    conflict_code
        Stable implementation-owned code required by ``conflict``.
    expected_revision_id, observed_revision_id
        Compare-and-swap revision slots available only for ``conflict``; either may
        be ``None`` to represent an absent stream slot.
    failure
        Structured failure required by ``indeterminate`` and ``error``.

    Raises
    ------
    TypeError
        If a field has the wrong semantic type.
    ValueError
        If an identity or status-variant invariant fails.

    Notes
    -----
    Indeterminate and error outcomes never imply presence, absence, or permission
    to retry.
    """

    result_id: str
    idempotency_id: str
    stream_id: str
    store_implementation_id: str
    store_version_id: str
    status: CommitStatus
    diagnostics: tuple[str, ...]
    claim_boundary: str
    revision: Revision | None = None
    conflict_code: str | None = None
    expected_revision_id: str | None = None
    observed_revision_id: str | None = None
    failure: StoreOperationalFailure | None = None

    def __post_init__(self) -> None:
        for field in (
            "result_id",
            "idempotency_id",
            "stream_id",
            "store_implementation_id",
            "store_version_id",
            "claim_boundary",
        ):
            _require_identifier(getattr(self, field), field)
        _require_enum(self.status, CommitStatus, "status")
        _require_tuple_of_strings(self.diagnostics, "diagnostics")
        _require_optional_identifier(self.conflict_code, "conflict_code")
        _require_optional_identifier(self.expected_revision_id, "expected_revision_id")
        _require_optional_identifier(self.observed_revision_id, "observed_revision_id")
        if self.revision is not None and type(self.revision) is not Revision:
            raise TypeError("revision must be Revision or None")
        if (
            self.failure is not None
            and type(self.failure) is not StoreOperationalFailure
        ):
            raise TypeError("failure must be StoreOperationalFailure or None")
        if self.status is CommitStatus.COMMITTED:
            if self.revision is None:
                raise ValueError("committed requires revision")
            if self.revision.stream_id != self.stream_id:
                raise ValueError(
                    "committed revision stream_id must equal result stream_id"
                )
            if (
                self.conflict_code is not None
                or self.expected_revision_id is not None
                or self.observed_revision_id is not None
                or self.failure is not None
            ):
                raise ValueError("committed prohibits conflict and failure fields")
        elif self.status is CommitStatus.CONFLICT:
            if self.conflict_code is None:
                raise ValueError("conflict requires conflict_code")
            if self.revision is not None or self.failure is not None:
                raise ValueError("conflict prohibits revision and failure")
        else:
            if self.failure is None:
                raise ValueError(f"{self.status.value} requires failure")
            if self.revision is not None or self.conflict_code is not None:
                raise ValueError(
                    f"{self.status.value} prohibits revision and conflict fields"
                )
            if (
                self.expected_revision_id is not None
                or self.observed_revision_id is not None
            ):
                raise ValueError(
                    f"{self.status.value} prohibits revision-presence claims"
                )


@runtime_checkable
class AtomicRevisionStore(Protocol):
    """Structural protocol for atomic opaque single-stream revision storage."""

    def read(self, request: RevisionReadRequest) -> RevisionReadResult:
        """Observe one exact latest-or-explicit revision request.

        Parameters
        ----------
        request
            Exact immutable request; implementations perform no ambient selector or
            stream discovery.

        Returns
        -------
        RevisionReadResult
            One closed generic observation.
        """
        ...

    def commit(self, commit: Commit) -> CommitResult:
        """Atomically compare and commit one complete candidate revision.

        Parameters
        ----------
        commit
            Exact immutable compare-and-swap and idempotency binding.

        Returns
        -------
        CommitResult
            One closed generic commit outcome.
        """
        ...
