"""Evidence class and represented meaning
Software verification of immutable manifest-to-artifact provenance links.
Owned contract, oracle, and scope
ProvenanceRecord is the SUT; exact identifiers and canonical tuple invariants are the
oracle.
VVUQ and scientific exclusions
Evidence excludes truth of asserted provenance, numerical verification, scientific
validation, UQ, and cross-language conformance.
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
