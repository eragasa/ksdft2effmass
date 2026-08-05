"""Evidence class and represented meaning
Software verification of immutable execution-attempt manifests.
Owned contract, oracle, and scope
RunManifest is the SUT; exact safe fields, canonical tuples, real timestamps, and state
rules are the oracle.
VVUQ and scientific exclusions
Evidence excludes execution, numerical verification, scientific validation, UQ, physical
correctness, and cross-language conformance.
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
    with pytest.raises(TypeError):
        _manifest(input_artifact_ids=["a"])
    with pytest.raises(ValueError):
        _manifest(input_artifact_ids=("b", "a"))
    with pytest.raises(ValueError):
        _manifest(dependency_manifest_ids=("a", "a"))


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
    for changes in (
        {"state": ManifestState.DECLARED, "finished_at": "2026-08-05T12:01:00Z"},
        {"state": ManifestState.FAILED},
        {"state": ManifestState.COMPLETE, "finished_at": "2026-08-05T11:59:59Z"},
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
