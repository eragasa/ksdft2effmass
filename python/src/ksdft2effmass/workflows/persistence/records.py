"""Immutable WorkflowRun persistence inputs and operation outcomes."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from enum import StrEnum
from typing import Literal, Protocol, runtime_checkable

from ksdft2effmass.persistence import (
    CommitResult,
    Revision,
    RevisionReadRequest,
    RevisionReadResult,
)

from ..model import (
    ResultObject,
    ResultObjectIdentity,
    WorkflowRunIdentity,
)
from ..runs.aggregate import WorkflowRun
from ..runs.authority import WorkflowRunClaimCommitReceipt
from ..runs.identities import (
    AuthorityReservationOutcomeIdentity,
    ResultObjectContentIdentity,
    ResultObjectDomainIdentity,
    ResultObjectTypeIdentity,
    WorkflowRunRevisionIdentity,
)


class WorkflowPersistenceFailureCode(StrEnum):
    """Closed represented codec and persistence failure categories.

    Attributes
    ----------
    UNSUPPORTED_TYPE, UNSUPPORTED_VERSION
        No selected concrete type or wire-version implementation exists.
    MALFORMED_REPRESENTATION
        Known wire grammar, canonical bytes or field closure is violated.
    IDENTITY_MISMATCH, CONTENT_MISMATCH
        Nominal correlation or represented content binding disagrees.
    INVARIANT_VIOLATION
        Reconstructed known-domain values violate their constructor contract.
    REPRESENTATION_LIMIT
        Allocation or recursion limits prevented completion.
    CODEC_ERROR
        The operation failed without a reconstructed value.
    """

    UNSUPPORTED_TYPE = "unsupported_type"
    UNSUPPORTED_VERSION = "unsupported_version"
    MALFORMED_REPRESENTATION = "malformed_representation"
    IDENTITY_MISMATCH = "identity_mismatch"
    CONTENT_MISMATCH = "content_mismatch"
    INVARIANT_VIOLATION = "invariant_violation"
    REPRESENTATION_LIMIT = "representation_limit"
    CODEC_ERROR = "codec_error"


@dataclass(frozen=True, slots=True, kw_only=True)
class WorkflowPersistenceFailure:
    """Immutable sanitized failure evidence, never a partial successful value.

    Parameters
    ----------
    implementation_identity
        Nonempty codec or persistence implementation and version label.
    phase
        Nonempty operation phase, such as ``encode`` or ``decode``.
    code
        Exact closed failure category.
    input_identities
        Ordered immutable tuple of nonempty applicable input identity labels.
        Empty means none was available; labels are observations, not authentication.
    expected, observed
        Nonempty represented expected and observed conditions.
    diagnostic
        Nonempty sanitized diagnostic. Implementations must not copy arbitrary
        exception text, payloads, credentials or native output here.
    claim_boundary
        Nonempty explicit limitation of the failure evidence.

    Raises
    ------
    TypeError
        A field has the wrong exact semantic type.
    ValueError
        A required label or tuple member is empty.
    """

    implementation_identity: str
    phase: str
    code: WorkflowPersistenceFailureCode
    input_identities: tuple[str, ...]
    expected: str
    observed: str
    diagnostic: str
    claim_boundary: str

    def __post_init__(self) -> None:
        """Enforce immutable exact field and nonempty-label invariants."""
        for value in (
            self.implementation_identity,
            self.phase,
            self.expected,
            self.observed,
            self.diagnostic,
            self.claim_boundary,
        ):
            if type(value) is not str:
                raise TypeError("failure labels must be exact strings")
            if not value:
                raise ValueError("failure labels must not be empty")
        if type(self.code) is not WorkflowPersistenceFailureCode:
            raise TypeError("code must be WorkflowPersistenceFailureCode")
        if type(self.input_identities) is not tuple or any(
            type(value) is not str for value in self.input_identities
        ):
            raise TypeError("input_identities must be a tuple of exact strings")
        if any(not value for value in self.input_identities):
            raise ValueError("input identities must not be empty")


@dataclass(frozen=True, slots=True, kw_only=True)
class WorkflowEncodedResultValue:
    """One complete concrete result envelope with exact SHA-256 byte binding.

    Parameters
    ----------
    result_identity
        Exact nominal identity of the concrete result.
    concrete_type_identity
        Exact supported import-name/version label selected by its codec.
    owning_domain_identity
        Exact domain owner of the concrete value contract.
    schema_identity
        Nonempty concrete payload schema label. This record does not decide support.
    content_identity
        Exact owning content label. Historical opaque labels are not interpreted
        as hashes; a separate payload digest always binds these bytes.
    payload
        Exact immutable bytes containing the complete concrete representation.
    payload_digest
        Lowercase SHA-256 hexadecimal digest of ``payload``. Construction checks
        exact agreement, but does not decode or authenticate the representation.

    Raises
    ------
    TypeError
        A field has the wrong exact semantic type, including mutable byte buffers.
    ValueError
        The schema is empty or the payload digest disagrees.
    """

    result_identity: ResultObjectIdentity
    concrete_type_identity: ResultObjectTypeIdentity
    owning_domain_identity: ResultObjectDomainIdentity
    schema_identity: str
    content_identity: ResultObjectContentIdentity
    payload: bytes
    payload_digest: str

    def __post_init__(self) -> None:
        """Enforce nominal fields and the exact-byte digest invariant."""
        if type(self.result_identity) is not ResultObjectIdentity:
            raise TypeError("result_identity must be ResultObjectIdentity")
        if type(self.concrete_type_identity) is not ResultObjectTypeIdentity:
            raise TypeError("concrete_type_identity must be ResultObjectTypeIdentity")
        if type(self.owning_domain_identity) is not ResultObjectDomainIdentity:
            raise TypeError("owning_domain_identity must be ResultObjectDomainIdentity")
        if type(self.content_identity) is not ResultObjectContentIdentity:
            raise TypeError("content_identity must be ResultObjectContentIdentity")
        if type(self.schema_identity) is not str:
            raise TypeError("schema_identity must be an exact string")
        if not self.schema_identity:
            raise ValueError("schema_identity must not be empty")
        if type(self.payload) is not bytes:
            raise TypeError("payload must be exact bytes")
        if type(self.payload_digest) is not str:
            raise TypeError("payload_digest must be an exact string")
        if self.payload_digest != hashlib.sha256(self.payload).hexdigest():
            raise ValueError("payload_digest must match the exact payload SHA-256")


@dataclass(frozen=True, slots=True, kw_only=True)
class WorkflowResultValueEncodeResult:
    """Closed result of encoding one explicitly supported concrete value.

    Parameters
    ----------
    status
        Exactly ``encoded``, ``incompatible``, ``invalid`` or ``error``.
    encoded
        Complete envelope on success only; otherwise ``None``.
    failure
        Structured failure on nonsuccess only; otherwise ``None``.

    Raises
    ------
    TypeError
        Status, envelope or failure has the wrong semantic type.
    ValueError
        The status is unknown or fields do not match its variant.
    """

    status: Literal["encoded", "incompatible", "invalid", "error"]
    encoded: WorkflowEncodedResultValue | None = None
    failure: WorkflowPersistenceFailure | None = None

    def __post_init__(self) -> None:
        """Reject open statuses and success/failure field mixing."""
        if type(self.status) is not str:
            raise TypeError("status must be an exact string")
        if self.status not in ("encoded", "incompatible", "invalid", "error"):
            raise ValueError("unknown encode status")
        if (
            self.encoded is not None
            and type(self.encoded) is not WorkflowEncodedResultValue
        ):
            raise TypeError("encoded must be WorkflowEncodedResultValue or None")
        if (
            self.failure is not None
            and type(self.failure) is not WorkflowPersistenceFailure
        ):
            raise TypeError("failure must be WorkflowPersistenceFailure or None")
        if self.status == "encoded":
            if self.encoded is None or self.failure is not None:
                raise ValueError("encoded alone carries an envelope and no failure")
        elif self.encoded is not None or self.failure is None:
            raise ValueError("encode failure carries failure evidence and no envelope")


@dataclass(frozen=True, slots=True, kw_only=True)
class WorkflowResultValueDecodeResult:
    """Closed concrete result reconstruction outcome.

    Parameters
    ----------
    status
        Exactly ``decoded``, ``incompatible``, ``corrupt`` or ``error``.
    value
        Concrete ResultObject on success only. The selected codec, not structural
        protocol membership or this container, establishes supported exact type,
        complete reconstruction and operational immutability.
    failure
        Structured failure on nonsuccess only; otherwise ``None``.

    Raises
    ------
    TypeError
        Status, result identity or failure has the wrong semantic type.
    ValueError
        The status is unknown or fields do not match its variant.
    """

    status: Literal["decoded", "incompatible", "corrupt", "error"]
    value: ResultObject | None = None
    failure: WorkflowPersistenceFailure | None = None

    def __post_init__(self) -> None:
        """Validate result shape without claiming arbitrary protocol serialization."""
        if type(self.status) is not str:
            raise TypeError("status must be an exact string")
        if self.status not in ("decoded", "incompatible", "corrupt", "error"):
            raise ValueError("unknown decode status")
        if self.value is not None and (
            not isinstance(self.value, ResultObject)
            or type(self.value.identity) is not ResultObjectIdentity
        ):
            raise TypeError("value must expose an exact ResultObjectIdentity")
        if (
            self.failure is not None
            and type(self.failure) is not WorkflowPersistenceFailure
        ):
            raise TypeError("failure must be WorkflowPersistenceFailure or None")
        if self.status == "decoded":
            if self.value is None or self.failure is not None:
                raise ValueError("decoded alone carries a value and no failure")
        elif self.value is not None or self.failure is None:
            raise ValueError("decode failure carries failure evidence and no value")


@runtime_checkable
class WorkflowResultValueCodec(Protocol):
    """Explicit injected port for complete, versioned concrete result values.

    Domain implementations use exact concrete branches, not reflection or a registry.
    Unknown concrete types/versions are incompatible. Canonical known-wire corruption
    is distinct from incompatibility and operational error. Implementations perform
    no native-file reads or effects and retain no mutable serializer/cache state.
    """

    def encode(self, value: ResultObject) -> WorkflowResultValueEncodeResult:
        """Encode a supported exact concrete value or return a closed failure.

        Parameters
        ----------
        value
            A workflow-facing result, not a promise of serializability.

        Returns
        -------
        WorkflowResultValueEncodeResult
            Complete encoded value or incompatible, invalid or error evidence.

        Raises
        ------
        TypeError
            Input does not expose an exact nominal ResultObject identity.
        """
        ...

    def decode(
        self, value: WorkflowEncodedResultValue
    ) -> WorkflowResultValueDecodeResult:
        """Decode one complete concrete envelope without interpreting authority.

        Parameters
        ----------
        value
            Exact nominal metadata and content-bound immutable payload.

        Returns
        -------
        WorkflowResultValueDecodeResult
            Complete concrete value or incompatible, corrupt or error evidence.

        Raises
        ------
        TypeError
            Input is not an exact WorkflowEncodedResultValue.
        """
        ...


@dataclass(frozen=True, slots=True, kw_only=True)
class WorkflowRunCommitBinding:
    """Durable labels to include in the complete aggregate payload.

    Parameters
    ----------
    transaction_identity
        Nonempty explicit caller-supplied stable operation label. Changing it must
        change the serialized aggregate bytes and content identity.
    commit_idempotency_identity
        Nonempty shared Commit key. Observing this label in bytes does not confirm
        the actual stored key; exact complete-expectation reconciliation is required.
    persistence_implementation_identity
        Nonempty historical writer/version label, never the current reader label.
        Future v1 writes require
        ``ksdft2effmass.workflows.WorkflowRunAtomicRepository:1``; readers must
        recognize support explicitly, not replace unknown writers.

    Raises
    ------
    TypeError
        Any label is not an exact built-in string.
    ValueError
        Any label is empty.

    Notes
    -----
    This intrinsic record alone derives no receipt, confirms no commit and grants no
    advancement or effect permission. Aggregate binding and reconciliation remain
    responsibilities of the serializer and future repository.
    """

    transaction_identity: str
    commit_idempotency_identity: str
    persistence_implementation_identity: str

    def __post_init__(self) -> None:
        """Enforce exact nonempty durable labels without selecting support."""
        for value in (
            self.transaction_identity,
            self.commit_idempotency_identity,
            self.persistence_implementation_identity,
        ):
            if type(value) is not str:
                raise TypeError("commit binding labels must be exact strings")
            if not value:
                raise ValueError("commit binding labels must not be empty")


@dataclass(frozen=True, slots=True, kw_only=True)
class WorkflowEncodedRun:
    """Complete aggregate bytes and their domain content binding.

    Parameters
    ----------
    schema_identity
        Nonempty aggregate wire schema label; support is decided by the serializer.
    content_identity
        Exactly ``schema_identity + ':sha256:' + sha256(payload).hexdigest()``.
    payload
        Exact immutable bytes. Construction checks binding, not wire validity.

    Raises
    ------
    TypeError
        A field is not an exact string or exact bytes as declared.
    ValueError
        The schema is empty or the content identity does not bind these bytes.
    """

    schema_identity: str
    content_identity: str
    payload: bytes

    def __post_init__(self) -> None:
        """Check exact representation types and intrinsic content binding."""
        if (
            type(self.schema_identity) is not str
            or type(self.content_identity) is not str
        ):
            raise TypeError("schema and content identities must be exact strings")
        if type(self.payload) is not bytes:
            raise TypeError("payload must be exact bytes")
        if not self.schema_identity:
            raise ValueError("schema_identity must not be empty")
        expected = (
            self.schema_identity + ":sha256:" + hashlib.sha256(self.payload).hexdigest()
        )
        if self.content_identity != expected:
            raise ValueError("content_identity must bind schema and exact payload")


@dataclass(frozen=True, slots=True, kw_only=True)
class WorkflowRunEncodeResult:
    """Closed aggregate encoding outcome without partial successful bytes.

    Parameters
    ----------
    status
        Exactly ``encoded``, ``incompatible``, ``invalid`` or ``error``.
    encoded
        Complete encoded run on success only; otherwise None.
    failure
        Complete sanitized failure on nonsuccess only; otherwise None.

    Raises
    ------
    TypeError
        A field has the wrong exact semantic type.
    ValueError
        Status or success/failure field closure is invalid.
    """

    status: Literal["encoded", "incompatible", "invalid", "error"]
    encoded: WorkflowEncodedRun | None = None
    failure: WorkflowPersistenceFailure | None = None

    def __post_init__(self) -> None:
        """Enforce exact closed variant fields."""
        if type(self.status) is not str:
            raise TypeError("status must be an exact string")
        if self.status not in ("encoded", "incompatible", "invalid", "error"):
            raise ValueError("unknown aggregate encode status")
        if self.encoded is not None and type(self.encoded) is not WorkflowEncodedRun:
            raise TypeError("encoded must be WorkflowEncodedRun or None")
        if (
            self.failure is not None
            and type(self.failure) is not WorkflowPersistenceFailure
        ):
            raise TypeError("failure must be WorkflowPersistenceFailure or None")
        if self.status == "encoded":
            if self.encoded is None or self.failure is not None:
                raise ValueError("encoded requires bytes and prohibits failure")
        elif self.encoded is not None or self.failure is None:
            raise ValueError("nonsuccess requires failure and prohibits bytes")


@dataclass(frozen=True, slots=True, kw_only=True)
class WorkflowRunDecodeResult:
    """Closed complete aggregate and durable-binding reconstruction outcome.

    Parameters
    ----------
    status
        Exactly ``decoded``, ``incompatible``, ``corrupt`` or ``error``.
    run
        Complete immutable run on success only. No replay equality is implied.
    binding
        Complete persisted transaction/key/historical-writer labels on success only.
    failure
        Structured evidence on nonsuccess only; never a partial run or binding.

    Raises
    ------
    TypeError
        A field has the wrong exact semantic type.
    ValueError
        Status or success/failure field closure is invalid.
    """

    status: Literal["decoded", "incompatible", "corrupt", "error"]
    run: WorkflowRun | None = None
    binding: WorkflowRunCommitBinding | None = None
    failure: WorkflowPersistenceFailure | None = None

    def __post_init__(self) -> None:
        """Keep complete successful reconstruction separate from failures."""
        if type(self.status) is not str:
            raise TypeError("status must be an exact string")
        if self.status not in ("decoded", "incompatible", "corrupt", "error"):
            raise ValueError("unknown aggregate decode status")
        if self.run is not None and type(self.run) is not WorkflowRun:
            raise TypeError("run must be WorkflowRun or None")
        if (
            self.binding is not None
            and type(self.binding) is not WorkflowRunCommitBinding
        ):
            raise TypeError("binding must be WorkflowRunCommitBinding or None")
        if (
            self.failure is not None
            and type(self.failure) is not WorkflowPersistenceFailure
        ):
            raise TypeError("failure must be WorkflowPersistenceFailure or None")
        if self.status == "decoded":
            if self.run is None or self.binding is None or self.failure is not None:
                raise ValueError("decoded requires complete run and binding only")
        elif self.run is not None or self.binding is not None or self.failure is None:
            raise ValueError("nonsuccess requires failure without run or binding")


@dataclass(frozen=True, slots=True, kw_only=True)
class WorkflowRunTransaction:
    """One complete candidate and explicit durable compare-and-swap metadata.

    Parameters
    ----------
    binding
        Single immutable owner of transaction, commit-key and historical writer labels.
    run_identity
        Exact nominal run targeted by the transaction.
    expected_predecessor_revision_identity
        Exact predecessor slot; None means genesis, not an unspecified expectation.
    candidate
        Complete immutable proposed run. Cross-object correlation, serialization,
        append-only history and version support belong to the transaction validator.
    schema_identity, content_identity
        Nonempty exact labels claimed for the complete candidate representation.
        Construction does not compute or verify its bytes.

    Raises
    ------
    TypeError
        A field has the wrong exact semantic type.
    ValueError
        A schema or content label is empty.

    Notes
    -----
    Merely constructing this record never submits a commit or validates a candidate.
    """

    binding: WorkflowRunCommitBinding
    run_identity: WorkflowRunIdentity
    expected_predecessor_revision_identity: WorkflowRunRevisionIdentity | None
    candidate: WorkflowRun
    schema_identity: str
    content_identity: str

    def __post_init__(self) -> None:
        """Check only intrinsic field types and nonempty labels."""
        if type(self.binding) is not WorkflowRunCommitBinding:
            raise TypeError("binding must be WorkflowRunCommitBinding")
        if type(self.run_identity) is not WorkflowRunIdentity:
            raise TypeError("run_identity must be WorkflowRunIdentity")
        if (
            self.expected_predecessor_revision_identity is not None
            and type(self.expected_predecessor_revision_identity)
            is not WorkflowRunRevisionIdentity
        ):
            raise TypeError(
                "expected predecessor must be WorkflowRunRevisionIdentity or None"
            )
        if type(self.candidate) is not WorkflowRun:
            raise TypeError("candidate must be WorkflowRun")
        for value in (self.schema_identity, self.content_identity):
            if type(value) is not str:
                raise TypeError("representation labels must be exact strings")
            if not value:
                raise ValueError("representation labels must not be empty")

    @property
    def transaction_identity(self) -> str:
        """Exact operation label from the sole durable binding."""
        return self.binding.transaction_identity

    @property
    def commit_idempotency_identity(self) -> str:
        """Exact commit key from the sole durable binding, not store confirmation."""
        return self.binding.commit_idempotency_identity


@dataclass(frozen=True, slots=True, kw_only=True)
class WorkflowRunSnapshot:
    """Complete reconstructed run, durable binding and exact retained revision.

    Parameters
    ----------
    run
        Complete immutable run; no identity-only or partial stand-in is accepted.
    binding
        Persisted transaction/key/historical-writer labels, not a reconstructed receipt.
    revision
        Exact shared revision envelope including immutable payload bytes.
        The repository, not this intrinsic container, verifies cross-object binding,
        digest, version and structural closure before returning a loaded snapshot.

    Raises
    ------
    TypeError
        Any input is not its exact declared concrete record type.

    Notes
    -----
    This container establishes neither durable presence nor replay equality, authority,
    advancement permission or effect entry. It performs no serialization or store I/O.
    """

    run: WorkflowRun
    binding: WorkflowRunCommitBinding
    revision: Revision

    def __post_init__(self) -> None:
        """Reject partial and wrong-type snapshot fields."""
        if type(self.run) is not WorkflowRun:
            raise TypeError("run must be WorkflowRun")
        if type(self.binding) is not WorkflowRunCommitBinding:
            raise TypeError("binding must be WorkflowRunCommitBinding")
        if type(self.revision) is not Revision:
            raise TypeError("revision must be Revision")


@dataclass(frozen=True, slots=True, kw_only=True)
class WorkflowRunLoadResult:
    """Closed domain read outcome preserving complete shared read evidence.

    Parameters
    ----------
    status
        Exactly loaded, absent, mismatch, incompatible, corrupt, indeterminate or error.
    request
        Exact read request, including selector and every reconciliation expectation.
    store_result
        Complete shared result when a store observation exists; otherwise None.
        Its result/request/store identities and variant-specific evidence are retained.
    snapshot
        Complete snapshot only for loaded; otherwise None.
    failure
        Domain failure for pre-read or domain rejection, otherwise None. Shared
        nonsuccess evidence may suffice without a separate domain failure.

    Raises
    ------
    TypeError
        An input has the wrong exact semantic type.
    ValueError
        Status or variant evidence closure fails.

    Notes
    -----
    Correlation of the independent request, shared observation and snapshot belongs
    to the repository. Construction is not a read and does not verify those links.
    """

    status: Literal[
        "loaded",
        "absent",
        "mismatch",
        "incompatible",
        "corrupt",
        "indeterminate",
        "error",
    ]
    request: RevisionReadRequest
    store_result: RevisionReadResult | None = None
    snapshot: WorkflowRunSnapshot | None = None
    failure: WorkflowPersistenceFailure | None = None

    def __post_init__(self) -> None:
        """Enforce success-only snapshots and retained nonsuccess evidence."""
        if type(self.status) is not str:
            raise TypeError("status must be an exact string")
        if self.status not in (
            "loaded",
            "absent",
            "mismatch",
            "incompatible",
            "corrupt",
            "indeterminate",
            "error",
        ):
            raise ValueError("unknown domain load status")
        if type(self.request) is not RevisionReadRequest:
            raise TypeError("request must be RevisionReadRequest")
        if (
            self.store_result is not None
            and type(self.store_result) is not RevisionReadResult
        ):
            raise TypeError("store_result must be RevisionReadResult or None")
        if self.snapshot is not None and type(self.snapshot) is not WorkflowRunSnapshot:
            raise TypeError("snapshot must be WorkflowRunSnapshot or None")
        if (
            self.failure is not None
            and type(self.failure) is not WorkflowPersistenceFailure
        ):
            raise TypeError("failure must be WorkflowPersistenceFailure or None")
        if self.status == "loaded":
            if (
                self.snapshot is None
                or self.store_result is None
                or self.store_result.status.value != "found"
                or self.failure is not None
            ):
                raise ValueError("loaded requires snapshot and found evidence only")
        elif self.status == "absent" and (
            self.store_result is None or self.store_result.status.value != "absent"
        ):
            raise ValueError("absent requires shared absence evidence")
        elif self.snapshot is not None:
            raise ValueError("nonsuccess prohibits a snapshot")
        elif self.failure is None and (
            self.store_result is None or self.store_result.status.value != self.status
        ):
            raise ValueError(
                "nonsuccess requires matching shared or domain failure evidence"
            )


@dataclass(frozen=True, slots=True, kw_only=True)
class WorkflowRunWriteResult:
    """Closed domain commit outcome without lost shared evidence or effect permission.

    Parameters
    ----------
    status
        Exactly committed, conflict, indeterminate, error, invalid or incompatible.
    transaction
        Exact candidate transaction addressed by this outcome.
    store_result
        Complete shared commit result when submitted and observed, otherwise None.
    predecessor_load
        Complete predecessor-read evidence when obtained, otherwise None. This
        preserves read uncertainty or rejection without fabricating a commit result.
    snapshot
        Complete bound snapshot only for committed, otherwise None.
    claim_receipts
        Immutable ordered newly appended historical claim receipts on committed only;
        may be empty. They grant no effect-entry permission.
    failure
        Domain failure for rejection or operational error; None on committed.
        Shared nonsuccess evidence may suffice without a second domain failure.

    Raises
    ------
    TypeError
        An input has the wrong exact type or receipts are not an immutable tuple.
    ValueError
        Status or variant evidence closure fails, or receipt identities repeat.
    """

    status: Literal[
        "committed", "conflict", "indeterminate", "error", "invalid", "incompatible"
    ]
    transaction: WorkflowRunTransaction
    store_result: CommitResult | None = None
    predecessor_load: WorkflowRunLoadResult | None = None
    snapshot: WorkflowRunSnapshot | None = None
    claim_receipts: tuple[WorkflowRunClaimCommitReceipt, ...] = ()
    failure: WorkflowPersistenceFailure | None = None

    def __post_init__(self) -> None:
        """Keep acknowledged snapshots separate from rejection and uncertainty."""
        if type(self.status) is not str:
            raise TypeError("status must be an exact string")
        if self.status not in (
            "committed",
            "conflict",
            "indeterminate",
            "error",
            "invalid",
            "incompatible",
        ):
            raise ValueError("unknown domain write status")
        if type(self.transaction) is not WorkflowRunTransaction:
            raise TypeError("transaction must be WorkflowRunTransaction")
        if (
            self.store_result is not None
            and type(self.store_result) is not CommitResult
        ):
            raise TypeError("store_result must be CommitResult or None")
        if (
            self.predecessor_load is not None
            and type(self.predecessor_load) is not WorkflowRunLoadResult
        ):
            raise TypeError("predecessor_load must be WorkflowRunLoadResult or None")
        if self.snapshot is not None and type(self.snapshot) is not WorkflowRunSnapshot:
            raise TypeError("snapshot must be WorkflowRunSnapshot or None")
        if (
            self.failure is not None
            and type(self.failure) is not WorkflowPersistenceFailure
        ):
            raise TypeError("failure must be WorkflowPersistenceFailure or None")
        if type(self.claim_receipts) is not tuple or any(
            type(receipt) is not WorkflowRunClaimCommitReceipt
            for receipt in self.claim_receipts
        ):
            raise TypeError("claim_receipts must be a tuple of exact claim receipts")
        identities = tuple(receipt.identity for receipt in self.claim_receipts)
        if len(set(identities)) != len(identities):
            raise ValueError("claim receipt identities must not repeat")
        if self.status == "committed":
            if (
                self.snapshot is None
                or self.store_result is None
                or self.store_result.status.value != "committed"
                or self.failure is not None
            ):
                raise ValueError(
                    "committed requires snapshot and acknowledged shared evidence"
                )
        elif self.status == "conflict" and (
            self.store_result is None or self.store_result.status.value != "conflict"
        ):
            raise ValueError("conflict requires shared conflict evidence")
        elif self.snapshot is not None or self.claim_receipts:
            raise ValueError("nonsuccess prohibits snapshot and claim receipts")
        elif self.failure is None and (
            self.store_result is None or self.store_result.status.value != self.status
        ):
            raise ValueError(
                "nonsuccess requires matching shared or domain failure evidence"
            )
        if self.status in ("invalid", "incompatible") and self.store_result is not None:
            raise ValueError("pre-store rejection prohibits a shared commit result")


@dataclass(frozen=True, slots=True, kw_only=True)
class WorkflowRunClaimLoadResult:
    """Closed historical claim observation, never effect-entry permission.

    Parameters
    ----------
    status
        Same seven statuses as WorkflowRunLoadResult. Only loaded carries a receipt.
    claimed_reservation_identity
        Exact requested nominal claim selector, retained even on nonsuccess.
    request
        Exact read request including every historical reconciliation expectation.
    store_result
        Complete underlying shared read evidence when present, otherwise None.
    snapshot
        Complete historical run snapshot on loaded only; otherwise None.
    receipt
        Reconstructed historical claim receipt on loaded only; otherwise None.
    failure
        Claim-specific failure on rejection after a loaded run; otherwise None.
        A matching shared nonsuccess may propagate without a second failure.

    Raises
    ------
    TypeError
        An input has the wrong exact semantic type.
    ValueError
        Status or success/failure closure fails.

    Notes
    -----
    The repository owns exact-revision expectation confirmation and receipt derivation.
    This record only retains the result and grants no advancement or effect authority.
    """

    status: Literal[
        "loaded",
        "absent",
        "mismatch",
        "incompatible",
        "corrupt",
        "indeterminate",
        "error",
    ]
    claimed_reservation_identity: AuthorityReservationOutcomeIdentity
    request: RevisionReadRequest
    store_result: RevisionReadResult | None = None
    snapshot: WorkflowRunSnapshot | None = None
    receipt: WorkflowRunClaimCommitReceipt | None = None
    failure: WorkflowPersistenceFailure | None = None

    def __post_init__(self) -> None:
        """Require both historical snapshot and receipt for loaded only."""
        if type(self.status) is not str:
            raise TypeError("status must be an exact string")
        if self.status not in (
            "loaded",
            "absent",
            "mismatch",
            "incompatible",
            "corrupt",
            "indeterminate",
            "error",
        ):
            raise ValueError("unknown claim-load status")
        if (
            type(self.claimed_reservation_identity)
            is not AuthorityReservationOutcomeIdentity
        ):
            raise TypeError(
                "claimed_reservation_identity must be "
                "AuthorityReservationOutcomeIdentity"
            )
        if type(self.request) is not RevisionReadRequest:
            raise TypeError("request must be RevisionReadRequest")
        if (
            self.store_result is not None
            and type(self.store_result) is not RevisionReadResult
        ):
            raise TypeError("store_result must be RevisionReadResult or None")
        if self.snapshot is not None and type(self.snapshot) is not WorkflowRunSnapshot:
            raise TypeError("snapshot must be WorkflowRunSnapshot or None")
        if (
            self.receipt is not None
            and type(self.receipt) is not WorkflowRunClaimCommitReceipt
        ):
            raise TypeError("receipt must be WorkflowRunClaimCommitReceipt or None")
        if (
            self.failure is not None
            and type(self.failure) is not WorkflowPersistenceFailure
        ):
            raise TypeError("failure must be WorkflowPersistenceFailure or None")
        if self.status == "loaded":
            if (
                self.snapshot is None
                or self.store_result is None
                or self.store_result.status.value != "found"
                or self.receipt is None
                or self.failure is not None
            ):
                raise ValueError("loaded claim requires loaded run and receipt only")
        elif self.snapshot is not None or self.receipt is not None:
            raise ValueError("nonsuccess prohibits snapshot and claim receipt")
        elif self.status == "absent" and (
            self.store_result is None or self.store_result.status.value != "absent"
        ):
            raise ValueError("absent requires shared absence evidence")
        elif self.failure is None and (
            self.store_result is None or self.store_result.status.value != self.status
        ):
            raise ValueError(
                "claim rejection requires shared or domain failure evidence"
            )


@dataclass(frozen=True, slots=True, kw_only=True)
class WorkflowRunValidationResult:
    """Record validation bound to the exact transaction and predecessor inputs.

    Parameters
    ----------
    status
        Exactly ``valid``, ``invalid``, ``incompatible`` or ``error``.
    transaction
        The complete input transaction, retained without replacement.
    predecessor
        Explicit historical snapshot input, or None for genesis. This record alone
        does not establish that the predecessor was stored.
    encoded
        Exact validated candidate representation on valid only, otherwise None.
    failure
        Structured diagnostic on nonsuccess only, otherwise None.

    Raises
    ------
    TypeError
        A field has the wrong exact semantic type.
    ValueError
        The status, variant closure or encoded transaction labels disagree.

    Notes
    -----
    This immutable result does not establish replay equality, stored presence,
    historical authentication, execution authority or scientific acceptance.
    """

    status: Literal["valid", "invalid", "incompatible", "error"]
    transaction: WorkflowRunTransaction
    predecessor: WorkflowRunSnapshot | None = None
    encoded: WorkflowEncodedRun | None = None
    failure: WorkflowPersistenceFailure | None = None

    def __post_init__(self) -> None:
        """Check exact fields and closed success/failure representation."""
        if type(self.status) is not str:
            raise TypeError("status must be an exact string")
        if self.status not in ("valid", "invalid", "incompatible", "error"):
            raise ValueError("unknown transaction validation status")
        if type(self.transaction) is not WorkflowRunTransaction:
            raise TypeError("transaction must be WorkflowRunTransaction")
        if (
            self.predecessor is not None
            and type(self.predecessor) is not WorkflowRunSnapshot
        ):
            raise TypeError("predecessor must be WorkflowRunSnapshot or None")
        if self.encoded is not None and type(self.encoded) is not WorkflowEncodedRun:
            raise TypeError("encoded must be WorkflowEncodedRun or None")
        if (
            self.failure is not None
            and type(self.failure) is not WorkflowPersistenceFailure
        ):
            raise TypeError("failure must be WorkflowPersistenceFailure or None")
        if self.status == "valid":
            if self.encoded is None or self.failure is not None:
                raise ValueError("valid requires encoded candidate without failure")
            if (
                self.encoded.schema_identity != self.transaction.schema_identity
                or self.encoded.content_identity != self.transaction.content_identity
            ):
                raise ValueError("encoded labels must match the input transaction")
        elif self.encoded is not None or self.failure is None:
            raise ValueError("nonsuccess requires failure without encoded candidate")
