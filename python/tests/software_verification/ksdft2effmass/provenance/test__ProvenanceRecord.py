r"""Software verification of ``ProvenanceRecord``.

Evidence profile: claim_bearing

Bounded artifact scope: the module's declared evidence owner.

Facet and represented meaning

-----------------------------
This module verifies immutable manifest, parent-provenance, and artifact links
represented by a durable provenance record.

Intrinsic and cross-object scope

--------------------------------
``ProvenanceRecord`` is the sole SUT; scalar, tuple, direct self-parent, immutability,
and value invariants are intrinsic. Linked-object existence and graph-wide cycles are
excluded.

VVUQ and scientific exclusions

------------------------------
Evidence excludes truth of asserted provenance, numerical verification, scientific
validation, UQ, physical correctness, and cross-language conformance.
"""

from dataclasses import FrozenInstanceError

import pytest

from ksdft2effmass.provenance import ProvenanceRecord

SUT = ProvenanceRecord
pytestmark = pytest.mark.software_verification


def test_constructor__provenance_fields__maps_canonical_links() -> None:
    """Evidence ID: SV-PROV-014

    Requirement: Provenance identifiers, parents, manifest, and artifacts map exactly in
    canonical
    order.

    Method: Construct a public record with two sorted parent and artifact identifiers.

    Oracle: The accepted field mapping and lexical tuple order are fixed.

    Acceptance: The complete field tuple equals the supplied values exactly.

    Interpretation: Failure indicates mapping or ordering drift.

    Limitations: Existence and truth of linked records are not checked.
    """
    value = SUT("prov-2", "manifest-1", ("prov-0", "prov-1"), ("a", "b"))
    assert (
        value.provenance_id,
        value.manifest_id,
        value.parent_provenance_ids,
        value.artifact_ids,
    ) == ("prov-2", "manifest-1", ("prov-0", "prov-1"), ("a", "b"))


@pytest.mark.parametrize(
    "parents",
    [
        pytest.param(("b", "a"), id="unsorted_parents"),
        pytest.param(("a", "a"), id="duplicate_parents"),
    ],
)
def test_constructor__canonical_parent_links__reject_noncanonical_tuples(
    parents: tuple[str, ...],
) -> None:
    """Evidence ID: SV-PROV-015

    Requirement: Parent-provenance links are lexically sorted and duplicate-free.

    Method: Construct with the named unsorted or duplicate parent tuple.

    Oracle: Lexical ordering and set cardinality independently classify both fixed
    tuples.

    Acceptance: Construction raises ValueError.

    Interpretation: Failure permits nondeterministic or duplicate provenance parent
    state.

    Limitations: Synthetic metadata only; scientific validation, UQ, physical
    correctness, and
    cross-language conformance are excluded.
    """
    with pytest.raises(ValueError):
        SUT("p", "m", parents, ())


def test_constructor__direct_self_parent__rejects_record_local_cycle() -> None:
    """Evidence ID: SV-PROV-137

    Requirement: A ProvenanceRecord cannot name its own provenance_id as a direct
    parent.

    Method: Construct an otherwise valid record with the sole parent equal to
    provenance_id.

    Oracle: Exact equality of the two public identifier inputs supplies the oracle.

    Acceptance: Construction raises ValueError.

    Interpretation: Failure permits a record-local provenance self-edge.

    Limitations: General graph cycles, scientific validation, UQ, and cross-language
    conformance
    are excluded.
    """
    with pytest.raises(ValueError):
        SUT("p", "m", ("p",), ())


def test_constructor__parent_collection_semantic_type__rejects_list() -> None:
    """Evidence ID: SV-PROV-129

    Requirement: parent_provenance_ids requires an exact built-in tuple.

    Method: Construct with an empty list in the parent field.

    Oracle: The public exact collection-type contract classifies lists.

    Acceptance: Construction raises TypeError.

    Interpretation: Failure permits mutable parent collection state.

    Limitations: Synthetic metadata only; scientific validation, UQ, physical
    correctness, and
    cross-language conformance are excluded.
    """
    with pytest.raises(TypeError):
        SUT("p", "m", [], ())  # type: ignore[arg-type]


def test_field__operational_immutability__rejects_reassignment() -> None:
    """Evidence ID: SV-PROV-016

    Requirement: Provenance records are operationally immutable.

    Method: Construct with immutable tuples and attempt field reassignment.

    Oracle: Frozen DataObject semantics are the accepted architecture.

    Acceptance: Reassignment raises FrozenInstanceError.

    Interpretation: Failure indicates mutable durable provenance.

    Limitations: Hostile reflection is excluded.
    """
    value = SUT("p", "m", (), ())
    with pytest.raises(FrozenInstanceError):
        value.manifest_id = "other"  # type: ignore[misc]


@pytest.mark.parametrize(
    "field",
    [
        pytest.param("provenance_id", id="provenance_identifier"),
        pytest.param("manifest_id", id="manifest_identifier"),
    ],
)
@pytest.mark.parametrize(
    "invalid",
    [
        pytest.param("", id="empty_identifier"),
        pytest.param("bad id", id="embedded_space"),
        pytest.param("e\u0301", id="non_nfc_identifier"),
        pytest.param("\ud800", id="unicode_surrogate"),
        pytest.param("a" * 129, id="overlength_identifier"),
    ],
)
def test_field__scalar_identifier_values__reject_nonportable_text(
    field: str, invalid: str
) -> None:
    """Evidence ID: SV-PROV-098

    Requirement: Provenance scalar identifiers are nonempty NFC bounded identifiers.

    Method: Replace the named scalar with the named malformed string.

    Oracle: The identifier grammar and NFC definition classify each literal.

    Acceptance: Construction raises ValueError.

    Interpretation: Failure admits malformed provenance identity state.

    Limitations: Synthetic metadata only; scientific validation, UQ, physical
    correctness, and
    cross-language conformance are excluded.
    """
    values: dict[str, object] = {
        "provenance_id": "p",
        "manifest_id": "m",
        "parent_provenance_ids": (),
        "artifact_ids": (),
    }
    with pytest.raises(ValueError):
        SUT(**(values | {field: invalid}))  # type: ignore[arg-type]


@pytest.mark.parametrize(
    "field",
    [
        pytest.param("provenance_id", id="provenance_identifier"),
        pytest.param("manifest_id", id="manifest_identifier"),
    ],
)
def test_field__scalar_identifier_semantic_types__reject_bytes(field: str) -> None:
    """Evidence ID: SV-PROV-130

    Requirement: Provenance scalar identifiers require built-in strings.

    Method: Replace the named scalar with bytes.

    Oracle: The exact semantic-type contract classifies bytes.

    Acceptance: Construction raises TypeError.

    Interpretation: Failure indicates unintended provenance scalar coercion.

    Limitations: Synthetic metadata only; scientific validation, UQ, physical
    correctness, and
    cross-language conformance are excluded.
    """
    values: dict[str, object] = {
        "provenance_id": "p",
        "manifest_id": "m",
        "parent_provenance_ids": (),
        "artifact_ids": (),
    }
    with pytest.raises(TypeError):
        SUT(**(values | {field: b"id"}))  # type: ignore[arg-type]


@pytest.mark.parametrize(
    "field",
    [
        pytest.param("parent_provenance_ids", id="parent_provenance_identifiers"),
        pytest.param("artifact_ids", id="artifact_identifiers"),
    ],
)
@pytest.mark.parametrize(
    "invalid_tuple",
    [
        pytest.param(("b", "a"), id="unsorted_tuple"),
        pytest.param(("a", "a"), id="duplicate_tuple"),
        pytest.param(("",), id="empty_member"),
        pytest.param(("bad id",), id="embedded_space"),
        pytest.param(("e\u0301",), id="non_nfc_member"),
        pytest.param(("\ud800",), id="unicode_surrogate"),
        pytest.param(("a" * 129,), id="overlength_member"),
    ],
)
def test_field__identifier_collection_values__reject_noncanonical_tuples(
    field: str, invalid_tuple: tuple[str, ...]
) -> None:
    """Evidence ID: SV-PROV-099

    Requirement: Provenance identifier tuples are sorted, unique, and contain portable
    identifiers.

    Method: Replace the named collection with the named invalid built-in tuple.

    Oracle: Ordering, uniqueness, identifier grammar, and NFC classify each tuple.

    Acceptance: Construction raises ValueError.

    Interpretation: Failure permits nondeterministic or malformed provenance links.

    Limitations: Synthetic metadata only; scientific validation, UQ, physical
    correctness, and
    cross-language conformance are excluded.
    """
    values: dict[str, object] = {
        "provenance_id": "p",
        "manifest_id": "m",
        "parent_provenance_ids": (),
        "artifact_ids": (),
    }
    with pytest.raises(ValueError):
        SUT(**(values | {field: invalid_tuple}))  # type: ignore[arg-type]


@pytest.mark.parametrize(
    "field",
    [
        pytest.param("parent_provenance_ids", id="parent_provenance_identifiers"),
        pytest.param("artifact_ids", id="artifact_identifiers"),
    ],
)
def test_field__identifier_collection_semantic_types__reject_lists(field: str) -> None:
    """Evidence ID: SV-PROV-131

    Requirement: Provenance identifier collections require exact built-in tuples.

    Method: Replace the named collection with a one-member list.

    Oracle: The public exact collection-type contract classifies lists.

    Acceptance: Construction raises TypeError.

    Interpretation: Failure permits mutable provenance collection state.

    Limitations: Synthetic metadata only; scientific validation, UQ, physical
    correctness, and
    cross-language conformance are excluded.
    """
    values: dict[str, object] = {
        "provenance_id": "p",
        "manifest_id": "m",
        "parent_provenance_ids": (),
        "artifact_ids": (),
    }
    with pytest.raises(TypeError):
        SUT(**(values | {field: ["a"]}))  # type: ignore[arg-type]


@pytest.mark.parametrize(
    "field",
    [
        pytest.param("parent_provenance_ids", id="parent_provenance_identifiers"),
        pytest.param("artifact_ids", id="artifact_identifiers"),
    ],
)
def test_field__identifier_collection_member_semantic_types__reject_bytes(
    field: str,
) -> None:
    """Evidence ID: SV-PROV-132

    Requirement: Every provenance identifier tuple member requires a built-in string.

    Method: Put bytes into the named otherwise valid tuple.

    Oracle: The exact member semantic-type contract classifies bytes.

    Acceptance: Construction raises TypeError.

    Interpretation: Failure indicates unintended tuple-member coercion.

    Limitations: Synthetic metadata only; scientific validation, UQ, physical
    correctness, and
    cross-language conformance are excluded.
    """
    values: dict[str, object] = {
        "provenance_id": "p",
        "manifest_id": "m",
        "parent_provenance_ids": (),
        "artifact_ids": (),
    }
    with pytest.raises(TypeError):
        SUT(**(values | {field: (b"id",)}))  # type: ignore[arg-type]


def test_method__eq__includes_all_provenance_links() -> None:
    """Evidence ID: SV-PROV-100

    Requirement: ProvenanceRecord equality distinguishes otherwise equal records when
    the artifact
    relation tuple differs.

    Method: Compare equal public values and one value with a different artifact tuple.

    Oracle: Frozen dataclass fields define exact equality.

    Acceptance: Equal records compare equal and the changed artifact relation compares
    unequal.

    Interpretation: Failure indicates incomplete durable value semantics.

    Limitations: Equality does not establish truth of provenance claims.
    """
    value = SUT("p", "m", ("parent",), ("a",))
    assert value == SUT("p", "m", ("parent",), ("a",))
    assert value != SUT("p", "m", ("parent",), ("b",))
