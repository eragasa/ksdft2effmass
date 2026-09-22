r"""Software verification of ``RunManifest``.

Evidence profile: claim_bearing

Bounded artifact scope: the module's declared evidence owner.

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

FROZEN_FIELDS = (
    "manifest_id",
    "specification_id",
    "input_artifact_ids",
    "started_at",
    "finished_at",
    "output_artifact_ids",
    "dependency_manifest_ids",
    "state",
)
EQUALITY_FIELDS = (
    "manifest_id",
    "specification_id",
    "input_artifact_ids",
    "started_at",
    "finished_at",
    "output_artifact_ids",
    "dependency_manifest_ids",
    "state",
)


def make_run_manifest(**changes: object) -> RunManifest:
    """Evidence ID: Owns no identifier; supports SV-PROV-020 through SV-PROV-023,
    SV-PROV-077,
    SV-PROV-093 through SV-PROV-097, SV-PROV-110 through SV-PROV-112, and
    SV-PROV-122 through SV-PROV-128.

    Requirement: Construct explicit valid synthetic manifests without hidden raw runtime
    channels.

    Method: Merge named variations into visible canonical public defaults.

    Oracle: Defaults independently satisfy the documented version-1 constructor
    contract.

    Acceptance: The public constructor receives exactly the approved fields.

    Interpretation: Helper failure is setup failure rather than independent evidence.

    Limitations: Synthetic identifiers and times have no scientific or execution
    meaning.
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


def test_constructor__manifest_fields__maps_safe_state() -> None:
    """Evidence ID: SV-PROV-020

    Requirement: A manifest contains exactly safe identity, artifact, timestamp,
    dependency, and
    state fields without unsafe raw runtime channels.

    Method: Construct a declared manifest and inspect the dataclass inventory and stored
    values.

    Oracle: The corrected eight-field contract explicitly removes raw arguments and
    environment
    values.

    Acceptance: Fields match the exact inventory and stored tuple/state values are
    exact.

    Interpretation: Failure indicates field leakage or constructor mapping drift.

    Limitations: Referenced artifacts and timestamps are not externally observed.
    """
    value = make_run_manifest()
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


@pytest.mark.parametrize(
    "field_name",
    [
        pytest.param("manifest_id", id="manifest_id"),
        pytest.param("specification_id", id="specification_id"),
        pytest.param("input_artifact_ids", id="input_artifact_ids"),
        pytest.param("started_at", id="started_at"),
        pytest.param("finished_at", id="finished_at"),
        pytest.param("output_artifact_ids", id="output_artifact_ids"),
        pytest.param("dependency_manifest_ids", id="dependency_manifest_ids"),
        pytest.param("state", id="state"),
    ],
)
def test_field__frozen_assignment__rejects_every_public_field(
    field_name: str,
) -> None:
    """Evidence ID: SV-PROV-110

    Requirement: Every public RunManifest field is frozen against ordinary reassignment.

    Method: Construct a valid manifest and attempt reassignment of each field named in
    the
    complete FROZEN_FIELDS inventory; no warning is expected or suppressed.

    Oracle: The public frozen DataObject contract requires FrozenInstanceError for each
    of the
    eight published fields.

    Acceptance: Every named field reassignment raises exactly FrozenInstanceError.

    Interpretation: Failure identifies a mutable public field, an incomplete inventory,
    or architecture
    drift.

    Limitations: Hostile reflection, referenced execution, scientific validation, UQ,
    and
    cross-language claims are excluded.
    """
    assert field_name in FROZEN_FIELDS
    value = make_run_manifest()
    with pytest.raises(FrozenInstanceError):
        setattr(value, field_name, getattr(value, field_name))


@pytest.mark.parametrize(
    ("field_name", "invalid"),
    [
        pytest.param(
            "input_artifact_ids", ("b", "a"), id="unsorted_tuple_input_identifiers"
        ),
        pytest.param(
            "output_artifact_ids", ("b", "a"), id="unsorted_tuple_output_identifiers"
        ),
        pytest.param(
            "dependency_manifest_ids",
            ("b", "a"),
            id="unsorted_tuple_dependency_identifiers",
        ),
        pytest.param(
            "input_artifact_ids", ("a", "a"), id="duplicate_tuple_input_identifiers"
        ),
        pytest.param(
            "output_artifact_ids", ("a", "a"), id="duplicate_tuple_output_identifiers"
        ),
        pytest.param(
            "dependency_manifest_ids",
            ("a", "a"),
            id="duplicate_tuple_dependency_identifiers",
        ),
    ],
)
def test_constructor__canonical_identifier_tuple_values__reject_noncanonical_order(
    field_name: str, invalid: tuple[str, ...]
) -> None:
    """Evidence ID: SV-PROV-021

    Requirement: Manifest identifier tuples are lexically sorted and duplicate-free.

    Method: Replace the named tuple with the named noncanonical tuple.

    Oracle: Lexical ordering and set cardinality independently classify both cases.

    Acceptance: Construction raises ValueError.

    Interpretation: Failure permits nondeterministic or duplicate manifest
    relationships.

    Limitations: Synthetic metadata only; scientific validation, UQ, physical
    correctness, and
    cross-language conformance are excluded.
    """
    with pytest.raises(ValueError):
        make_run_manifest(**{field_name: invalid})


@pytest.mark.parametrize(
    "field_name",
    [
        pytest.param("input_artifact_ids", id="input_identifiers"),
        pytest.param("output_artifact_ids", id="output_identifiers"),
        pytest.param("dependency_manifest_ids", id="dependency_identifiers"),
    ],
)
def test_constructor__identifier_collection_semantic_types__reject_lists(
    field_name: str,
) -> None:
    """Evidence ID: SV-PROV-122

    Requirement: Manifest identifier collections require exact built-in tuples.

    Method: Replace the named collection with a one-member list.

    Oracle: The public exact collection-type contract classifies lists.

    Acceptance: Construction raises TypeError.

    Interpretation: Failure permits mutable manifest collection state.

    Limitations: Synthetic metadata only; scientific validation, UQ, physical
    correctness, and
    cross-language conformance are excluded.
    """
    with pytest.raises(TypeError):
        make_run_manifest(**{field_name: ["a"]})


@pytest.mark.parametrize(
    "changes",
    [
        pytest.param(
            {"state": ManifestState.DECLARED, "finished_at": "2026-08-05T12:01:00Z"},
            id="declared_with_finish",
        ),
        pytest.param({"state": ManifestState.FAILED}, id="terminal_without_finish"),
    ],
)
def test_constructor__lifecycle_finish_presence__enforces_state_boundary(
    changes: dict[str, object],
) -> None:
    """Evidence ID: SV-PROV-022

    Requirement: Declared manifests omit finished_at and terminal manifests require it.

    Method: Construct the named invalid lifecycle/finish-presence combination.

    Oracle: The public lifecycle table fixes presence independently of timestamp
    parsing.

    Acceptance: Construction raises ValueError.

    Interpretation: Failure weakens manifest lifecycle correlation.

    Limitations: Synthetic metadata only; scientific validation, UQ, physical
    correctness, and
    cross-language conformance are excluded.
    """
    with pytest.raises(ValueError):
        make_run_manifest(**changes)


def test_constructor__timestamp_order__rejects_finish_before_start() -> None:
    """Evidence ID: SV-PROV-123

    Requirement: A terminal finished_at must not precede started_at.

    Method: Construct a complete manifest with finish one second before start.

    Oracle: Chronological ordering of the fixed UTC literals supplies the oracle.

    Acceptance: Construction raises ValueError.

    Interpretation: Failure admits negative represented attempt duration.

    Limitations: Synthetic metadata only; scientific validation, UQ, physical
    correctness, and
    cross-language conformance are excluded.
    """
    with pytest.raises(ValueError):
        make_run_manifest(
            state=ManifestState.COMPLETE, finished_at="2026-08-05T11:59:59Z"
        )


def test_constructor__started_at_lexical_value__rejects_malformed_text() -> None:
    """Evidence ID: SV-PROV-124

    Requirement: started_at must match the public RFC-3339 UTC-second form.

    Method: Construct with the literal not-time as started_at.

    Oracle: The documented timestamp grammar excludes that literal.

    Acceptance: Construction raises ValueError.

    Interpretation: Failure admits malformed start timestamp text.

    Limitations: Synthetic metadata only; scientific validation, UQ, physical
    correctness, and
    cross-language conformance are excluded.
    """
    with pytest.raises(ValueError):
        make_run_manifest(started_at="not-time")


def test_constructor__finished_at_lexical_value__rejects_malformed_text() -> None:
    """Evidence ID: SV-PROV-125

    Requirement: A terminal finished_at must match the RFC-3339 UTC-second form.

    Method: Construct a complete manifest with not-time as its finish.

    Oracle: The documented timestamp grammar excludes that literal.

    Acceptance: Construction raises ValueError.

    Interpretation: Failure admits malformed finish timestamp text.

    Limitations: Synthetic metadata only; scientific validation, UQ, physical
    correctness, and
    cross-language conformance are excluded.
    """
    with pytest.raises(ValueError):
        make_run_manifest(state=ManifestState.COMPLETE, finished_at="not-time")


@pytest.mark.parametrize(
    ("state", "finished_at"),
    [
        pytest.param(
            ManifestState.COMPLETE, "2026-08-05T12:01:00Z", id="complete_terminal_state"
        ),
        pytest.param(
            ManifestState.FAILED, "2026-08-05T12:00:00Z", id="failed_terminal_state"
        ),
    ],
)
def test_constructor__terminal_states__accept_valid_finish(
    state: ManifestState, finished_at: str
) -> None:
    """Evidence ID: SV-PROV-126

    Requirement: Complete and failed terminal states accept a valid nonpreceding finish.

    Method: Construct the named terminal state with its fixed valid finish.

    Oracle: The lifecycle table and chronological ordering classify each pair as valid.

    Acceptance: Construction succeeds and stores the exact selected state.

    Interpretation: Failure rejects an authorized terminal lifecycle representation.

    Limitations: Synthetic metadata only; scientific validation, UQ, physical
    correctness, and
    cross-language conformance are excluded.
    """
    assert make_run_manifest(state=state, finished_at=finished_at).state is state


def test_field__manifest_state_enum_values__match_lifecycle_vocabulary() -> None:
    """Evidence ID: SV-PROV-023

    Requirement: Manifest states are exactly declared, complete, and failed.

    Method: Enumerate public values without invoking execution behavior.

    Oracle: The accepted version-1 lifecycle vocabulary is exact.

    Acceptance: The value tuple matches exactly.

    Interpretation: Failure indicates lifecycle vocabulary drift.

    Limitations: COMPLETE is not scientific acceptance.
    """
    assert tuple(item.value for item in ManifestState) == (
        "declared",
        "complete",
        "failed",
    )


@pytest.mark.parametrize(
    "timestamp",
    [
        pytest.param("2026-02-29T12:00:00Z", id="non_leap_february_29"),
        pytest.param("2024-02-30T12:00:00Z", id="february_30"),
        pytest.param("2026-04-31T12:00:00Z", id="april_31"),
    ],
)
def test_constructor__started_at_calendar_value__rejects_impossible_dates(
    timestamp: str,
) -> None:
    """Evidence ID: SV-PROV-077

    Requirement: started_at denotes a real Gregorian calendar instant, not only numeric
    syntax.

    Method: Construct with the named impossible start timestamp.

    Oracle: Gregorian month lengths independently classify every fixed literal as
    impossible.

    Acceptance: Construction raises ValueError.

    Interpretation: Failure indicates regex-only started_at admission or stale evidence.

    Limitations: Leap seconds, non-Z offsets, scientific validation, UQ, and
    cross-language
    conformance are excluded.
    """
    with pytest.raises(ValueError):
        make_run_manifest(started_at=timestamp)


@pytest.mark.parametrize(
    "timestamp",
    [
        pytest.param("2026-02-29T12:00:00Z", id="non_leap_february_29"),
        pytest.param("2024-02-30T12:00:00Z", id="february_30"),
        pytest.param("2026-04-31T12:00:00Z", id="april_31"),
    ],
)
def test_constructor__finished_at_calendar_value__rejects_impossible_dates(
    timestamp: str,
) -> None:
    """Evidence ID: SV-PROV-139

    Requirement: A terminal finished_at denotes a real Gregorian calendar instant.

    Method: Construct a complete manifest with the named impossible finish timestamp.

    Oracle: Gregorian month lengths independently classify every fixed literal as
    impossible.

    Acceptance: Construction raises ValueError.

    Interpretation: Failure indicates regex-only finished_at admission or stale
    evidence.

    Limitations: Leap seconds, non-Z offsets, scientific validation, UQ, and
    cross-language
    conformance are excluded.
    """
    with pytest.raises(ValueError):
        make_run_manifest(state=ManifestState.COMPLETE, finished_at=timestamp)


def test_constructor__declared_output_ids__preserves_preallocation() -> None:
    """Evidence ID: SV-PROV-093

    Requirement: A DECLARED manifest may store preallocated expected output identities
    before bytes
    or a terminal outcome exists.

    Method: Construct a declared manifest with a sorted nonempty output tuple and no
    finish
    time.

    Oracle: The implementation and directly synchronized documentation explicitly define
    outputs
    as expected identities rather than observations.

    Acceptance: Construction succeeds, state remains DECLARED, finish is absent, and
    outputs are
    exact.

    Interpretation: Failure would restore an unapproved requirement that declared
    outputs already exist.

    Limitations: The test does not assert that output bytes exist, were observed, or are
    accepted.
    """
    value = make_run_manifest(output_artifact_ids=("output-a", "output-b"))
    assert value.state is ManifestState.DECLARED
    assert value.finished_at is None
    assert value.output_artifact_ids == ("output-a", "output-b")


@pytest.mark.parametrize(
    ("field", "invalid"),
    [
        pytest.param("manifest_id", "", id="empty_identifier_manifest_identifier"),
        pytest.param(
            "specification_id", "", id="empty_identifier_specification_identifier"
        ),
        pytest.param("manifest_id", "bad id", id="embedded_space_manifest_identifier"),
        pytest.param(
            "specification_id", "bad id", id="embedded_space_specification_identifier"
        ),
        pytest.param(
            "manifest_id", "e\u0301", id="non_nfc_identifier_manifest_identifier"
        ),
        pytest.param(
            "specification_id",
            "e\u0301",
            id="non_nfc_identifier_specification_identifier",
        ),
        pytest.param(
            "manifest_id", "\ud800", id="unicode_surrogate_manifest_identifier"
        ),
        pytest.param(
            "specification_id",
            "\ud800",
            id="unicode_surrogate_specification_identifier",
        ),
        pytest.param(
            "manifest_id", "a" * 129, id="overlength_identifier_manifest_identifier"
        ),
        pytest.param(
            "specification_id",
            "a" * 129,
            id="overlength_identifier_specification_identifier",
        ),
    ],
)
def test_field__manifest_scalar_identifier_values__reject_nonportable_text(
    field: str, invalid: str
) -> None:
    """Evidence ID: SV-PROV-094

    Requirement: Manifest scalar identifiers are nonempty NFC bounded identifiers.

    Method: Replace the named scalar with the named malformed string.

    Oracle: The identifier grammar and NFC definition classify each literal.

    Acceptance: Construction raises ValueError.

    Interpretation: Failure admits malformed durable manifest identity.

    Limitations: Synthetic metadata only; scientific validation, UQ, physical
    correctness, and
    cross-language conformance are excluded.
    """
    with pytest.raises(ValueError):
        make_run_manifest(**{field: invalid})


@pytest.mark.parametrize(
    "field",
    [
        pytest.param("manifest_id", id="manifest_identifier"),
        pytest.param("specification_id", id="specification_identifier"),
    ],
)
def test_field__manifest_scalar_identifier_semantic_types__reject_bytes(
    field: str,
) -> None:
    """Evidence ID: SV-PROV-127

    Requirement: Manifest scalar identifiers require built-in strings.

    Method: Replace the named scalar with bytes.

    Oracle: The exact semantic-type contract classifies bytes.

    Acceptance: Construction raises TypeError.

    Interpretation: Failure indicates unintended scalar identifier coercion.

    Limitations: Synthetic metadata only; scientific validation, UQ, physical
    correctness, and
    cross-language conformance are excluded.
    """
    with pytest.raises(TypeError):
        make_run_manifest(**{field: b"id"})


@pytest.mark.parametrize(
    ("field_name", "invalid"),
    [
        pytest.param(
            "input_artifact_ids", "", id="empty_identifier_input_artifact_identifiers"
        ),
        pytest.param(
            "output_artifact_ids", "", id="empty_identifier_output_artifact_identifiers"
        ),
        pytest.param(
            "dependency_manifest_ids",
            "",
            id="empty_identifier_dependency_manifest_identifiers",
        ),
        pytest.param(
            "input_artifact_ids",
            "bad id",
            id="embedded_space_input_artifact_identifiers",
        ),
        pytest.param(
            "output_artifact_ids",
            "bad id",
            id="embedded_space_output_artifact_identifiers",
        ),
        pytest.param(
            "dependency_manifest_ids",
            "bad id",
            id="embedded_space_dependency_manifest_identifiers",
        ),
        pytest.param(
            "input_artifact_ids",
            "e\u0301",
            id="non_nfc_identifier_input_artifact_identifiers",
        ),
        pytest.param(
            "output_artifact_ids",
            "e\u0301",
            id="non_nfc_identifier_output_artifact_identifiers",
        ),
        pytest.param(
            "dependency_manifest_ids",
            "e\u0301",
            id="non_nfc_identifier_dependency_manifest_identifiers",
        ),
        pytest.param(
            "input_artifact_ids",
            "\ud800",
            id="unicode_surrogate_input_artifact_identifiers",
        ),
        pytest.param(
            "output_artifact_ids",
            "\ud800",
            id="unicode_surrogate_output_artifact_identifiers",
        ),
        pytest.param(
            "dependency_manifest_ids",
            "\ud800",
            id="unicode_surrogate_dependency_manifest_identifiers",
        ),
        pytest.param(
            "input_artifact_ids",
            "a" * 129,
            id="overlength_identifier_input_artifact_identifiers",
        ),
        pytest.param(
            "output_artifact_ids",
            "a" * 129,
            id="overlength_identifier_output_artifact_identifiers",
        ),
        pytest.param(
            "dependency_manifest_ids",
            "a" * 129,
            id="overlength_identifier_dependency_manifest_identifiers",
        ),
    ],
)
def test_field__identifier_tuple_member_values__reject_nonportable_text(
    field_name: str, invalid: str
) -> None:
    """Evidence ID: SV-PROV-095

    Requirement: Every manifest tuple member is a nonempty NFC bounded identifier.

    Method: Put the named malformed string into the selected otherwise valid tuple.

    Oracle: The identifier grammar and NFC definition classify each literal.

    Acceptance: Construction raises ValueError.

    Interpretation: Failure admits malformed manifest relationship identity.

    Limitations: Synthetic metadata only; scientific validation, UQ, physical
    correctness, and
    cross-language conformance are excluded.
    """
    with pytest.raises(ValueError):
        make_run_manifest(**{field_name: (invalid,)})


@pytest.mark.parametrize(
    "field_name",
    [
        pytest.param("input_artifact_ids", id="input_artifact_identifiers"),
        pytest.param("output_artifact_ids", id="output_artifact_identifiers"),
        pytest.param("dependency_manifest_ids", id="dependency_manifest_identifiers"),
    ],
)
def test_field__identifier_tuple_member_semantic_types__reject_bytes(
    field_name: str,
) -> None:
    """Evidence ID: SV-PROV-128

    Requirement: Every manifest tuple member requires a built-in string.

    Method: Put bytes into the selected otherwise valid tuple.

    Oracle: The exact member semantic-type contract classifies bytes.

    Acceptance: Construction raises TypeError.

    Interpretation: Failure indicates unintended tuple-member coercion.

    Limitations: Synthetic metadata only; scientific validation, UQ, physical
    correctness, and
    cross-language conformance are excluded.
    """
    with pytest.raises(TypeError):
        make_run_manifest(**{field_name: (b"id",)})


def test_constructor__direct_self_dependency__rejects_record_local_cycle() -> None:
    """Evidence ID: SV-PROV-096

    Requirement: A manifest cannot list its own manifest_id as a direct dependency.

    Method: Construct an otherwise valid manifest whose sole dependency equals
    manifest_id.

    Oracle: Equality of the two public identifier values is an independent exact oracle.

    Acceptance: Construction raises ValueError.

    Interpretation: Failure permits a record-local dependency self-edge.

    Limitations: Indirect and graph-wide cycles across multiple manifests are excluded.
    """
    with pytest.raises(ValueError):
        make_run_manifest(dependency_manifest_ids=("manifest-1",))


def test_field__timestamp_semantic_types__reject_bytes() -> None:
    """Evidence ID: SV-PROV-097

    Requirement: started_at and present finished_at require built-in strings.

    Method: Construct once with bytes at each timestamp boundary.

    Oracle: The public exact semantic-type contract classifies bytes for both fields.

    Acceptance: Each construction raises TypeError.

    Interpretation: Failure indicates unintended timestamp coercion or missing type
    enforcement.

    Limitations: Clock accuracy, execution observation, scientific validation, UQ, and
    cross-language behavior are excluded.
    """
    with pytest.raises(TypeError):
        make_run_manifest(started_at=b"2026-08-05T12:00:00Z")
    with pytest.raises(TypeError):
        make_run_manifest(state=ManifestState.COMPLETE, finished_at=b"time")


def test_field__state_semantic_type__rejects_string_lookalike() -> None:
    """Evidence ID: SV-PROV-111

    Requirement: state requires a ManifestState member and rejects its wire-string
    lookalike.

    Method: Construct through the public helper using the string ``declared``.

    Oracle: The public enum semantic-type contract classifies the string as invalid.

    Acceptance: Construction raises TypeError.

    Interpretation: Failure indicates unintended enum coercion or stale evidence.

    Limitations: Execution state truth, validation, UQ, and cross-language behavior are
    excluded.
    """
    with pytest.raises(TypeError):
        make_run_manifest(state="declared")


@pytest.mark.parametrize(
    ("field_name", "changed_value"),
    [
        pytest.param("manifest_id", "manifest-2", id="manifest_id"),
        pytest.param("specification_id", "spec-2", id="specification_id"),
        pytest.param("input_artifact_ids", ("input-c",), id="input_artifact_ids"),
        pytest.param("started_at", "2026-08-05T11:00:00Z", id="started_at"),
        pytest.param("finished_at", "2026-08-05T13:00:01Z", id="finished_at"),
        pytest.param("output_artifact_ids", ("output-a",), id="output_artifact_ids"),
        pytest.param(
            "dependency_manifest_ids", ("manifest-2",), id="dependency_manifest_ids"
        ),
        pytest.param("state", ManifestState.FAILED, id="state"),
    ],
)
def test_method__eq__distinguishes_every_public_field(
    field_name: str, changed_value: object
) -> None:
    """Evidence ID: SV-PROV-112

    Requirement: RunManifest equality is exact over all eight fields in complete
    represented state.

    Method: Compare two independently constructed equal terminal manifests, then vary
    exactly
    one field named by EQUALITY_FIELDS while keeping every constructor state valid.

    Oracle: The literal eight-field inventory and exact Python dataclass value contract
    define
    equality independently of object identity.

    Acceptance: Equal state compares equal and each of the eight one-field variants
    compares
    unequal.

    Interpretation: Failure indicates incomplete equality, invalid test construction, or
    contract drift.

    Limitations: Equality proves no execution, output existence, scientific validation,
    UQ, or
    cross-language conformance.
    """
    baseline_changes: dict[str, object] = {
        "state": ManifestState.COMPLETE,
        "finished_at": "2026-08-05T13:00:00Z",
    }
    assert field_name in EQUALITY_FIELDS
    baseline = make_run_manifest(**baseline_changes)
    changed = {**baseline_changes, field_name: changed_value}
    assert baseline == make_run_manifest(**baseline_changes)
    assert baseline != make_run_manifest(**changed)
