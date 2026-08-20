r"""Software verification of ksdft2effmass.persistence public store contract.

Evidence profile: claim_bearing

Bounded artifact scope: ``ksdft2effmass.persistence`` public store contract.

Facet and represented meaning

The module verifies immutable revisions, exact read selectors and expectations,
compare-and-swap commits, closed result variants, and the structural store protocol.

Intrinsic and cross-object scope

The artifact owner is the complete public ``persistence.store`` contract. Tests use
accepted architecture prose and exact Python type semantics as independent oracles;
no concrete storage implementation is exercised.

VVUQ and scientific exclusions

Passing establishes software-contract behavior only. It does not establish durable
storage, SQLite behavior, domain validity, numerical verification, scientific
validation, uncertainty quantification, or human acceptance.
"""

from dataclasses import FrozenInstanceError
from typing import TypedDict

import pytest

from ksdft2effmass.persistence import (
    AtomicRevisionStore,
    Commit,
    CommitResult,
    CommitStatus,
    Revision,
    RevisionReadRequest,
    RevisionReadResult,
    RevisionReadStatus,
    RevisionSelector,
    StoreOperationalFailure,
)

pytestmark = pytest.mark.software_verification


class ReadResultCommon(TypedDict):
    """Type the common synthetic read-result constructor fields."""

    result_id: str
    request_id: str
    stream_id: str
    selector: RevisionSelector
    store_implementation_id: str
    store_version_id: str
    diagnostics: tuple[str, ...]
    claim_boundary: str


class CommitResultCommon(TypedDict):
    """Type the common synthetic commit-result constructor fields."""

    result_id: str
    idempotency_id: str
    stream_id: str
    store_implementation_id: str
    store_version_id: str
    diagnostics: tuple[str, ...]
    claim_boundary: str


def make_revision(*, predecessor: str | None = None) -> Revision:
    """Return one synthetic opaque revision used by contract examples.

    Evidence ID: Helper owns no identifier.

    Requirement: Support store-contract evidence without an independent claim.

    Method: Construct one explicit public revision.

    Oracle: Consuming tests own all expected values.

    Acceptance: Return the declared immutable revision.

    Interpretation: Failure blocks the consuming evidence owners.

    Limitations: This helper establishes no independent evidence.
    """
    return Revision(
        "stream.a", "revision.1", predecessor, "schema.1", "content.1", b"x"
    )


def make_failure() -> StoreOperationalFailure:
    """Return one sanitized synthetic operational failure.

    Evidence ID: Helper owns no identifier.

    Requirement: Support failure-variant evidence without an independent claim.

    Method: Construct one explicit public failure.

    Oracle: Consuming tests own all expected values.

    Acceptance: Return the declared immutable failure.

    Interpretation: Failure blocks the consuming evidence owners.

    Limitations: This helper establishes no independent evidence.
    """
    return StoreOperationalFailure(
        "failure.1",
        "read.observe",
        "store.memory.1",
        "io",
        "readable",
        "unavailable",
        "sanitized",
        None,
        "no presence or absence claim",
    )


def test_artifact__revision__retains_exact_immutable_opaque_state() -> None:
    """Evidence ID: SV-PS-001

    Requirement: A revision retains exact stream, revision, predecessor, schema,
    content, and immutable built-in payload bytes without domain interpretation.

    Method: Construct a first revision and attempt field reassignment.

    Oracle: The accepted shared-store contract defines these six exact fields and
    frozen DataObject semantics.

    Acceptance: Every field equals the supplied value and reassignment raises
    ``FrozenInstanceError``.

    Interpretation: Failure identifies identity, byte-preservation, or immutability
    drift.

    Limitations: Synthetic bytes establish no content-digest correctness.
    """
    revision = make_revision()
    assert revision == Revision(
        "stream.a", "revision.1", None, "schema.1", "content.1", b"x"
    )
    with pytest.raises(FrozenInstanceError):
        revision.payload = b"y"  # type: ignore[misc]


def test_artifact__revision__rejects_wrong_types_and_self_predecessor() -> None:
    """Evidence ID: SV-PS-002

    Requirement: Public revision fields reject semantic type errors, empty required
    identities, and a self-predecessor cycle.

    Method: Construct values violating each representative intrinsic partition.

    Oracle: Source documentation and exact Python type semantics define the exception
    taxonomy and self-predecessor prohibition.

    Acceptance: Wrong semantic types raise ``TypeError`` and invalid string relations
    raise ``ValueError``.

    Interpretation: Failure identifies coercion or weakened intrinsic closure.

    Limitations: Multi-revision graph consistency belongs to a concrete store.
    """
    with pytest.raises(TypeError, match="built-in str"):
        Revision(1, "r", None, "s", "c", b"")  # type: ignore[arg-type]
    with pytest.raises(TypeError, match="built-in bytes"):
        Revision("s", "r", None, "schema", "content", bytearray())  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="must not be empty"):
        Revision("", "r", None, "schema", "content", b"")
    with pytest.raises(ValueError, match="must not name itself"):
        Revision("s", "r", "r", "schema", "content", b"")


def test_artifact__read_request__enforces_selector_and_expectation_closure() -> None:
    """Evidence ID: SV-PS-003

    Requirement: Latest reads prohibit explicit addresses and expectations, while
    explicit reads require a revision and accept only an absent or complete
    reconciliation group.

    Method: Construct valid latest, explicit, and no-predecessor reconciliation
    requests, then representative prohibited combinations.

    Oracle: The accepted selector table and all-or-none expectation rule provide the
    exact expected combinations.

    Acceptance: Valid requests preserve their discriminants and invalid combinations
    raise ``ValueError``.

    Interpretation: Failure identifies ambient-discovery or partial-reconciliation
    contract drift.

    Limitations: Request execution is not exercised.
    """
    latest = RevisionReadRequest("request.latest", "stream.a", RevisionSelector.LATEST)
    explicit = RevisionReadRequest(
        "request.exact", "stream.a", RevisionSelector.EXPLICIT_REVISION, "revision.1"
    )
    reconcile = RevisionReadRequest(
        "request.reconcile",
        "stream.a",
        RevisionSelector.EXPLICIT_REVISION,
        "revision.1",
        None,
        "schema.1",
        "content.1",
        "idempotency.1",
    )
    assert latest.has_reconciliation_expectations is False
    assert explicit.has_reconciliation_expectations is False
    assert reconcile.has_reconciliation_expectations is True
    assert reconcile.expected_predecessor_revision_id is None
    with pytest.raises(ValueError, match="latest reads prohibit"):
        RevisionReadRequest(
            "request.bad", "stream.a", RevisionSelector.LATEST, "revision.1"
        )
    with pytest.raises(ValueError, match="require revision_id"):
        RevisionReadRequest(
            "request.bad", "stream.a", RevisionSelector.EXPLICIT_REVISION
        )
    with pytest.raises(ValueError, match="must be complete"):
        RevisionReadRequest(
            "request.bad",
            "stream.a",
            RevisionSelector.EXPLICIT_REVISION,
            "revision.1",
            None,
            "schema.1",
        )
    with pytest.raises(ValueError, match="must be complete"):
        RevisionReadRequest(
            "request.bad",
            "stream.a",
            RevisionSelector.EXPLICIT_REVISION,
            "revision.1",
            "revision.0",
        )


def test_artifact__commit__binds_candidate_predecessor_and_idempotency() -> None:
    """Evidence ID: SV-PS-004

    Requirement: A commit binds one complete candidate to an expected current
    revision and idempotency identity, with candidate predecessor equal to expected.

    Method: Construct matching initial and successor commits and one stale binding.

    Oracle: The accepted compare-and-swap correlation invariant requires exact
    predecessor equality.

    Acceptance: Matching commits retain exact fields and the stale binding raises
    ``ValueError``.

    Interpretation: Failure identifies weakened compare-and-swap input closure.

    Limitations: Atomicity and replay behavior require a concrete implementation.
    """
    first = Commit(None, make_revision(), "idempotency.1")
    successor = Commit(
        "revision.0", make_revision(predecessor="revision.0"), "idempotency.2"
    )
    assert first.expected_revision_id is None
    assert successor.candidate.predecessor_revision_id == "revision.0"
    with pytest.raises(ValueError, match="must equal expected_revision_id"):
        Commit("revision.other", make_revision(), "idempotency.bad")


def test_artifact__read_result__enforces_closed_variants() -> None:
    """Evidence ID: SV-PS-005

    Requirement: Read results enforce the seven closed variants and only ``found``
    carries a revision.

    Method: Construct representative found, mismatch, and indeterminate results and
    prohibited variant-field combinations.

    Oracle: The accepted read-result status table fixes required and prohibited
    fields.

    Acceptance: Valid variants retain their evidence; missing or prohibited fields
    and a false found expectation confirmation raise ``ValueError``.

    Interpretation: Failure identifies fabricated revision or variant leakage.

    Limitations: Findings are synthetic and establish no actual store observation.
    """
    common: ReadResultCommon = {
        "result_id": "result.1",
        "request_id": "request.1",
        "stream_id": "stream.a",
        "selector": RevisionSelector.EXPLICIT_REVISION,
        "store_implementation_id": "store.memory",
        "store_version_id": "1",
        "diagnostics": (),
        "claim_boundary": "software observation only",
    }
    found = RevisionReadResult(
        **common,
        status=RevisionReadStatus.FOUND,
        revision=make_revision(),
        expectations_matched=True,
    )
    absent = RevisionReadResult(
        **common,
        status=RevisionReadStatus.ABSENT,
        requested_revision_id="revision.1",
        absence_observation="consistent read found no address",
    )
    expected = (
        ("content_id", "content.1"),
        ("idempotency_id", "idempotency.1"),
        ("predecessor_revision_id", None),
        ("schema_id", "schema.1"),
    )
    mismatch = RevisionReadResult(
        **common,
        status=RevisionReadStatus.MISMATCH,
        requested_revision_id="revision.1",
        expected_identities=expected,
        observed_identities=(("content_id", "content.2"),),
        mismatched_fields=("content_id",),
    )
    incompatible = RevisionReadResult(
        **common,
        status=RevisionReadStatus.INCOMPATIBLE,
        unsupported_version_ids=("envelope.2",),
        compatibility_finding="envelope version unsupported",
    )
    corrupt = RevisionReadResult(
        **common,
        status=RevisionReadStatus.CORRUPT,
        integrity_findings=("content identity differs",),
    )
    indeterminate = RevisionReadResult(
        **common, status=RevisionReadStatus.INDETERMINATE, failure=make_failure()
    )
    error = RevisionReadResult(
        **common, status=RevisionReadStatus.ERROR, failure=make_failure()
    )
    assert found.revision == make_revision()
    assert absent.revision is None
    assert mismatch.revision is None
    assert incompatible.unsupported_version_ids == ("envelope.2",)
    assert corrupt.integrity_findings == ("content identity differs",)
    assert indeterminate.failure == make_failure()
    assert error.failure == make_failure()
    with pytest.raises(ValueError, match="absent requires absence"):
        RevisionReadResult(
            **common,
            status=RevisionReadStatus.ABSENT,
            requested_revision_id="revision.1",
        )
    with pytest.raises(ValueError, match="requires requested_revision_id"):
        RevisionReadResult(
            **common,
            status=RevisionReadStatus.ABSENT,
            absence_observation="consistent read found no address",
        )
    with pytest.raises(ValueError, match="prohibits revision"):
        RevisionReadResult(
            **common,
            status=RevisionReadStatus.ABSENT,
            revision=make_revision(),
            requested_revision_id="revision.1",
            absence_observation="consistent read found no address",
        )
    with pytest.raises(ValueError, match="complete expected generic identity set"):
        RevisionReadResult(
            **common,
            status=RevisionReadStatus.MISMATCH,
            requested_revision_id="revision.1",
            expected_identities=(("content_id", "content.1"),),
            observed_identities=(("content_id", "content.2"),),
            mismatched_fields=("content_id",),
        )
    with pytest.raises(ValueError, match="must equal mismatched_fields"):
        RevisionReadResult(
            **common,
            status=RevisionReadStatus.MISMATCH,
            requested_revision_id="revision.1",
            expected_identities=expected,
            observed_identities=(("schema_id", "schema.2"),),
            mismatched_fields=("content_id",),
        )
    with pytest.raises(ValueError, match="cannot report failed"):
        RevisionReadResult(
            **common,
            status=RevisionReadStatus.FOUND,
            revision=make_revision(),
            expectations_matched=False,
        )


def test_artifact__commit_result__enforces_closed_variants() -> None:
    """Evidence ID: SV-PS-006

    Requirement: Commit results represent exactly committed, conflict,
    indeterminate, or error; only committed contains a revision.

    Method: Construct one value per variant and representative missing or leaking
    variant fields.

    Oracle: The accepted commit-result closure defines exact presence semantics.

    Acceptance: Four valid variants construct; malformed variants raise
    ``ValueError``.

    Interpretation: Failure identifies guessed commit state or closed-variant drift.

    Limitations: No concrete acknowledgement or reconciliation is performed.
    """
    common: CommitResultCommon = {
        "result_id": "result.1",
        "idempotency_id": "idempotency.1",
        "stream_id": "stream.a",
        "store_implementation_id": "store.memory",
        "store_version_id": "1",
        "diagnostics": (),
        "claim_boundary": "software observation only",
    }
    committed = CommitResult(
        **common, status=CommitStatus.COMMITTED, revision=make_revision()
    )
    conflict = CommitResult(
        **common,
        status=CommitStatus.CONFLICT,
        conflict_code="compare_and_swap",
        expected_revision_id="revision.0",
        observed_revision_id="revision.other",
    )
    indeterminate = CommitResult(
        **common, status=CommitStatus.INDETERMINATE, failure=make_failure()
    )
    error = CommitResult(**common, status=CommitStatus.ERROR, failure=make_failure())
    assert committed.revision == make_revision()
    assert conflict.conflict_code == "compare_and_swap"
    assert indeterminate.revision is None
    assert error.failure == make_failure()
    with pytest.raises(ValueError, match="committed requires revision"):
        CommitResult(**common, status=CommitStatus.COMMITTED)
    with pytest.raises(ValueError, match="conflict requires conflict_code"):
        CommitResult(**common, status=CommitStatus.CONFLICT)


def test_artifact__protocol__accepts_structural_store_only() -> None:
    """Evidence ID: SV-PS-007

    Requirement: ``AtomicRevisionStore`` is a runtime-checkable structural protocol
    requiring read and commit operations without nominal inheritance.

    Method: Check a synthetic object with both methods and one missing ``commit``.

    Oracle: Python runtime protocol semantics and the accepted structural contract are
    independent of implementation internals.

    Acceptance: The complete object satisfies ``isinstance`` and the incomplete one
    does not.

    Interpretation: Failure identifies nominal coupling or protocol-surface drift.

    Limitations: Runtime protocol checks signatures by attribute presence only.
    """

    class CompleteStore:
        def read(self, request: RevisionReadRequest) -> RevisionReadResult:
            raise NotImplementedError

        def commit(self, commit: Commit) -> CommitResult:
            raise NotImplementedError

    class ReadOnlyStore:
        def read(self, request: RevisionReadRequest) -> RevisionReadResult:
            raise NotImplementedError

    assert isinstance(CompleteStore(), AtomicRevisionStore)
    assert not isinstance(ReadOnlyStore(), AtomicRevisionStore)
