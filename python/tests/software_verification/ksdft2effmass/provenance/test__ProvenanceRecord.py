r"""Software verification of ``ProvenanceRecord``.

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
    """Evidence ID
    SV-PROV-014
    Requirement
    Provenance identifiers, parents, manifest, and artifacts map exactly in canonical
    order.
    Method
    Construct a public record with two sorted parent and artifact identifiers.
    Oracle
    The accepted field mapping and lexical tuple order are fixed.
    Acceptance
    The complete field tuple equals the supplied values exactly.
    Interpretation
    Failure indicates mapping or ordering drift.
    Limitations
    Existence and truth of linked records are not checked.
    """
    value = SUT("prov-2", "manifest-1", ("prov-0", "prov-1"), ("a", "b"))
    assert (
        value.provenance_id,
        value.manifest_id,
        value.parent_provenance_ids,
        value.artifact_ids,
    ) == ("prov-2", "manifest-1", ("prov-0", "prov-1"), ("a", "b"))


def test_constructor__canonical_links__rejects_unsorted_duplicate_or_self() -> None:
    """Evidence ID
    SV-PROV-015
    Requirement
    Identifier collections are built-in sorted unique tuples and a record cannot parent
    itself.
    Method
    Pass a list, unsorted tuple, duplicate tuple, and self-parent tuple.
    Oracle
    The public canonical tuple and acyclic self-edge invariants define rejection.
    Acceptance
    List raises TypeError and each noncanonical or self-referential tuple raises
    ValueError.
    Interpretation
    Failure indicates noncanonical provenance state can be constructed.
    Limitations
    General graph cycles across multiple records are outside this intrinsic invariant.
    """
    with pytest.raises(TypeError):
        SUT("p", "m", [], ())  # type: ignore[arg-type]
    for parents in (("b", "a"), ("a", "a"), ("p",)):
        with pytest.raises(ValueError):
            SUT("p", "m", parents, ())


def test_field__operational_immutability__rejects_reassignment() -> None:
    """Evidence ID
    SV-PROV-016
    Requirement
    Provenance records are operationally immutable.
    Method
    Construct with immutable tuples and attempt field reassignment.
    Oracle
    Frozen DataObject semantics are the accepted architecture.
    Acceptance
    Reassignment raises FrozenInstanceError.
    Interpretation
    Failure indicates mutable durable provenance.
    Limitations
    Hostile reflection is excluded.
    """
    value = SUT("p", "m", (), ())
    with pytest.raises(FrozenInstanceError):
        value.manifest_id = "other"  # type: ignore[misc]


@pytest.mark.parametrize("field", ["provenance_id", "manifest_id"])
def test_field__scalar_identifiers__enforce_portable_contract(field: str) -> None:
    """Evidence ID
    SV-PROV-098
    Requirement
    Provenance and manifest scalar identities are built-in nonempty NFC identifiers.
    Method
    Replace each field with wrong-type, empty, invalid-grammar, Unicode, and length
    cases.
    Oracle
    The public bounded identifier grammar independently classifies the values.
    Acceptance
    Bytes raise TypeError and every invalid string raises ValueError for both fields.
    Interpretation
    Failure admits nonportable provenance state.
    Limitations
    Identifier existence and global uniqueness are excluded.
    """
    defaults: dict[str, object] = {
        "provenance_id": "p",
        "manifest_id": "m",
        "parent_provenance_ids": (),
        "artifact_ids": (),
    }
    for invalid in (b"id", "", "bad id", "e\u0301", "\ud800", "a" * 129):
        expected = TypeError if type(invalid) is bytes else ValueError
        with pytest.raises(expected):
            SUT(**(defaults | {field: invalid}))  # type: ignore[arg-type]


@pytest.mark.parametrize("field", ["parent_provenance_ids", "artifact_ids"])
def test_field__identifier_collections__enforce_tuple_member_and_order_contract(
    field: str,
) -> None:
    """Evidence ID
    SV-PROV-099
    Requirement
    Both identifier collections are built-in sorted unique tuples of portable
    identifiers.
    Method
    For each collection pass a list, unsorted and duplicate tuples, plus invalid
    members.
    Oracle
    The public canonical tuple and identifier contracts classify every partition.
    Acceptance
    Lists and bytes members raise TypeError; other prohibited values raise ValueError.
    Interpretation
    Failure permits mutable, nondeterministic, or nonportable provenance links.
    Limitations
    Relationship existence and general graph validity are excluded.
    """
    defaults: dict[str, object] = {
        "provenance_id": "p",
        "manifest_id": "m",
        "parent_provenance_ids": (),
        "artifact_ids": (),
    }
    with pytest.raises(TypeError):
        SUT(**(defaults | {field: ["a"]}))  # type: ignore[arg-type]
    for invalid_tuple in (
        ("b", "a"),
        ("a", "a"),
        ("",),
        ("bad id",),
        ("e\u0301",),
        ("\ud800",),
        ("a" * 129,),
    ):
        with pytest.raises(ValueError):
            SUT(**(defaults | {field: invalid_tuple}))  # type: ignore[arg-type]
    with pytest.raises(TypeError):
        SUT(**(defaults | {field: (b"id",)}))  # type: ignore[arg-type]


def test_property__exact_value_semantics__includes_all_provenance_links() -> None:
    """Evidence ID
    SV-PROV-100
    Requirement
    ProvenanceRecord equality is exact over all four represented fields.
    Method
    Compare equal public values and one value with a different artifact tuple.
    Oracle
    Frozen dataclass fields define exact equality.
    Acceptance
    Equal records compare equal and the changed artifact relation compares unequal.
    Interpretation
    Failure indicates incomplete durable value semantics.
    Limitations
    Equality does not establish truth of provenance claims.
    """
    value = SUT("p", "m", ("parent",), ("a",))
    assert value == SUT("p", "m", ("parent",), ("a",))
    assert value != SUT("p", "m", ("parent",), ("b",))
