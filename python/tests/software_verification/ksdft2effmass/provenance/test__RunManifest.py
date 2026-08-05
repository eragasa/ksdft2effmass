r"""Software verification of ``RunManifest``.

Facet and represented meaning
-----------------------------
This module verifies immutable declared and terminal execution-attempt manifests,
including expected output identities, timestamps, lifecycle state, and dependencies.

Intrinsic and cross-object scope
--------------------------------
``RunManifest`` is the sole SUT; field-local invariants and direct self-dependency are
intrinsic. Cross-manifest existence, graph-wide cycles, and execution are excluded.

VVUQ and scientific exclusions
------------------------------
Evidence excludes external execution, output-byte observation, numerical verification,
scientific validation, UQ, physical correctness, and cross-language conformance.
"""

from dataclasses import FrozenInstanceError, fields

import pytest

from ksdft2effmass.provenance import ManifestState, RunManifest

SUT = RunManifest
pytestmark = pytest.mark.software_verification


def _manifest(**changes: object) -> RunManifest:
    """Evidence ID
    Supports SV-PROV-020 through SV-PROV-023 and SV-PROV-077; owns no identifier.
    Requirement
    Construct explicit valid synthetic manifests without hidden raw runtime channels.
    Method
    Merge named variations into visible canonical public defaults.
    Oracle
    Defaults independently satisfy the documented version-1 constructor contract.
    Acceptance
    The public constructor receives exactly the approved fields.
    Interpretation
    Helper failure is setup failure rather than independent evidence.
    Limitations
    Synthetic identifiers and times have no scientific or execution meaning.
    """
    values: dict[str, object] = {
        "manifest_id": "manifest-1",
        "specification_id": "spec-1",
        "input_artifact_ids": ("input-a", "input-b"),
        "started_at": "2026-08-05T12:00:00Z",
        "finished_at": None,
        "output_artifact_ids": (),
        "dependency_manifest_ids": (),
        "state": ManifestState.DECLARED,
    }
    values.update(changes)
    return SUT(**values)  # type: ignore[arg-type]


def test_constructor__manifest_fields_and_ownership__maps_safe_immutable_state() -> (
    None
):
    """Evidence ID
    SV-PROV-020
    Requirement
    A manifest contains exactly safe identity, artifact, timestamp, dependency, and
    state fields in frozen form.
    Method
    Construct a declared manifest, inspect the dataclass inventory, and attempt
    mutation.
    Oracle
    The corrected eight-field contract explicitly removes raw arguments and environment
    values.
    Acceptance
    Fields match the exact inventory, tuples retain exact values, and reassignment
    raises FrozenInstanceError.
    Interpretation
    Failure indicates field leakage, mapping drift, or operational mutability.
    Limitations
    Referenced artifacts and timestamps are not externally observed.
    """
    value = _manifest()
    assert tuple(field.name for field in fields(SUT)) == (
        "manifest_id",
        "specification_id",
        "input_artifact_ids",
        "started_at",
        "finished_at",
        "output_artifact_ids",
        "dependency_manifest_ids",
        "state",
    )
    assert value.input_artifact_ids == ("input-a", "input-b")
    assert value.state is ManifestState.DECLARED
    with pytest.raises(FrozenInstanceError):
        value.state = ManifestState.COMPLETE  # type: ignore[misc]


def test_constructor__canonical_identifier_tuples__rejects_noncanonical_inputs() -> (
    None
):
    """Evidence ID
    SV-PROV-021
    Requirement
    Artifact and dependency identifiers are built-in lexically sorted unique tuples.
    Method
    Pass a list, unsorted tuple, and duplicate tuple to the public constructor.
    Oracle
    The canonical tuple contract fixes the invalid partitions independently of count.
    Acceptance
    The list raises TypeError and noncanonical tuples raise ValueError.
    Interpretation
    Failure indicates mutable or nondeterministic manifest state.
    Limitations
    Cross-record existence is outside intrinsic construction.
    """
    for field_name in (
        "input_artifact_ids",
        "output_artifact_ids",
        "dependency_manifest_ids",
    ):
        with pytest.raises(TypeError):
            _manifest(**{field_name: ["a"]})
        with pytest.raises(ValueError):
            _manifest(**{field_name: ("b", "a")})
        with pytest.raises(ValueError):
            _manifest(**{field_name: ("a", "a")})


def test_constructor__state_timestamp_correlation__enforces_terminal_boundaries() -> (
    None
):
    """Evidence ID
    SV-PROV-022
    Requirement
    Declared manifests omit finished_at; terminal manifests require a real nonpreceding
    UTC-second finish.
    Method
    Construct one valid complete state and invalid declared, missing-terminal,
    preceding, and malformed cases.
    Oracle
    The public lifecycle invariant and chronological ordering define the partition.
    Acceptance
    Valid completion succeeds and every invalid combination raises ValueError.
    Interpretation
    Failure indicates lifecycle or timestamp-correlation drift.
    Limitations
    Clock provenance and elapsed-time accuracy are excluded.
    """
    assert (
        _manifest(
            state=ManifestState.COMPLETE,
            finished_at="2026-08-05T12:01:00Z",
            output_artifact_ids=("output-a",),
        ).state
        is ManifestState.COMPLETE
    )
    assert (
        _manifest(
            state=ManifestState.FAILED,
            finished_at="2026-08-05T12:00:00Z",
        ).state
        is ManifestState.FAILED
    )
    for changes in (
        {"state": ManifestState.DECLARED, "finished_at": "2026-08-05T12:01:00Z"},
        {"state": ManifestState.FAILED},
        {"state": ManifestState.COMPLETE, "finished_at": "2026-08-05T11:59:59Z"},
        {"state": ManifestState.COMPLETE, "finished_at": "not-time"},
        {"started_at": "not-time"},
    ):
        with pytest.raises(ValueError):
            _manifest(**changes)


def test_field__manifest_state_enum_values__match_lifecycle_vocabulary() -> None:
    """Evidence ID
    SV-PROV-023
    Requirement
    Manifest states are exactly declared, complete, and failed.
    Method
    Enumerate public values without invoking execution behavior.
    Oracle
    The accepted version-1 lifecycle vocabulary is exact.
    Acceptance
    The value tuple matches exactly.
    Interpretation
    Failure indicates lifecycle vocabulary drift.
    Limitations
    COMPLETE is not scientific acceptance.
    """
    assert tuple(item.value for item in ManifestState) == (
        "declared",
        "complete",
        "failed",
    )


def test_constructor__calendar_timestamps__rejects_impossible_dates() -> None:
    """Evidence ID
    SV-PROV-077
    Requirement
    Timestamp strings denote real Gregorian calendar instants rather than only matching
    numeric syntax.
    Method
    Attempt impossible February, day-zero, and April-31 start or finish timestamps.
    Oracle
    Gregorian calendar month lengths independently classify all literals as impossible.
    Acceptance
    Every impossible start or finish raises ValueError.
    Interpretation
    Failure indicates regex-only timestamp admission or stale evidence.
    Limitations
    Leap seconds, offsets other than Z, and timezone databases are excluded.
    """
    for timestamp in (
        "2026-02-29T12:00:00Z",
        "2024-02-30T12:00:00Z",
        "2026-04-31T12:00:00Z",
    ):
        with pytest.raises(ValueError):
            _manifest(started_at=timestamp)
        with pytest.raises(ValueError):
            _manifest(state=ManifestState.COMPLETE, finished_at=timestamp)


def test_constructor__declared_output_ids__preserves_preallocation() -> None:
    """Evidence ID
    SV-PROV-093
    Requirement
    A DECLARED manifest may store preallocated expected output identities before bytes
    or a terminal outcome exists.
    Method
    Construct a declared manifest with a sorted nonempty output tuple and no finish
    time.
    Oracle
    The implementation and directly synchronized documentation explicitly define outputs
    as expected identities rather than observations.
    Acceptance
    Construction succeeds, state remains DECLARED, finish is absent, and outputs are
    exact.
    Interpretation
    Failure would restore an unapproved requirement that declared outputs already exist.
    Limitations
    The test does not assert that output bytes exist, were observed, or are accepted.
    """
    value = _manifest(output_artifact_ids=("output-a", "output-b"))
    assert value.state is ManifestState.DECLARED
    assert value.finished_at is None
    assert value.output_artifact_ids == ("output-a", "output-b")


@pytest.mark.parametrize("field", ["manifest_id", "specification_id"])
def test_field__manifest_scalar_identifiers__enforce_portable_contract(
    field: str,
) -> None:
    """Evidence ID
    SV-PROV-094
    Requirement
    Manifest and specification identities are built-in, nonempty NFC bounded
    identifiers.
    Method
    Replace each scalar field with wrong-type and invalid Unicode or grammar values.
    Oracle
    The public identifier contract independently classifies the supplied partitions.
    Acceptance
    Bytes raise TypeError and all invalid strings raise ValueError for both fields.
    Interpretation
    Failure admits a nonportable durable manifest identity.
    Limitations
    Cross-record existence and uniqueness are excluded.
    """
    for invalid in (b"id", "", "bad id", "e\u0301", "\ud800", "a" * 129):
        expected = TypeError if type(invalid) is bytes else ValueError
        with pytest.raises(expected):
            _manifest(**{field: invalid})


@pytest.mark.parametrize(
    "field_name",
    ["input_artifact_ids", "output_artifact_ids", "dependency_manifest_ids"],
)
def test_field__identifier_tuple_members__enforce_portable_contract(
    field_name: str,
) -> None:
    """Evidence ID
    SV-PROV-095
    Requirement
    Every member of each manifest identifier tuple is a portable built-in identifier.
    Method
    Put wrong-type, empty, spaced, decomposed, surrogate, and overlength members into
    each otherwise valid tuple.
    Oracle
    The tuple-member identifier grammar classifies the same partitions for all fields.
    Acceptance
    Wrong-type members raise TypeError and invalid strings raise ValueError.
    Interpretation
    Failure exposes incomplete validation in the named collection.
    Limitations
    Referenced artifacts and manifests are not resolved.
    """
    for invalid in (b"id", "", "bad id", "e\u0301", "\ud800", "a" * 129):
        expected = TypeError if type(invalid) is bytes else ValueError
        with pytest.raises(expected):
            _manifest(**{field_name: (invalid,)})


def test_constructor__direct_self_dependency__rejects_record_local_cycle() -> None:
    """Evidence ID
    SV-PROV-096
    Requirement
    A manifest cannot list its own manifest_id as a direct dependency.
    Method
    Construct an otherwise valid manifest whose sole dependency equals manifest_id.
    Oracle
    Equality of the two public identifier values is an independent exact oracle.
    Acceptance
    Construction raises ValueError.
    Interpretation
    Failure permits a record-local dependency self-edge.
    Limitations
    Indirect and graph-wide cycles across multiple manifests are excluded.
    """
    with pytest.raises(ValueError):
        _manifest(dependency_manifest_ids=("manifest-1",))


def test_property__timestamp_types_and_exact_value_semantics__enforce_contract() -> (
    None
):
    """Evidence ID
    SV-PROV-097
    Requirement
    Timestamps are built-in strings and manifest equality is exact over represented
    state.
    Method
    Pass bytes for each timestamp boundary, then compare equal and output-different
    records.
    Oracle
    Public semantic types and frozen dataclass fields define the expected outcomes.
    Acceptance
    Bytes raise TypeError; equal records compare equal and changed outputs compare
    unequal.
    Interpretation
    Failure indicates timestamp coercion or incomplete value semantics.
    Limitations
    Clock accuracy and execution observation are excluded.
    """
    with pytest.raises(TypeError):
        _manifest(started_at=b"2026-08-05T12:00:00Z")
    with pytest.raises(TypeError):
        _manifest(state=ManifestState.COMPLETE, finished_at=b"time")
    with pytest.raises(TypeError):
        _manifest(state="declared")
    assert _manifest() == _manifest()
    assert _manifest() != _manifest(output_artifact_ids=("output-a",))
