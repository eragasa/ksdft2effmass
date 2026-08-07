r"""Software verification of ``Basis``.

Facet and represented meaning
-----------------------------
This class-owned module owns the construction facet. This module owns public
construction, field mapping, ordered-sequence-to-tuple
canonicalization, defensive ownership, exact label preservation, both Boolean
orthonormality states, and standalone-serialization exclusion. For
:math:`\mathcal B=(|b_0\rangle,\ldots,|b_{N-1}\rangle)`, ``ordering[i]`` is the
exact coordinate label for :math:`|b_i\rangle`; order and spelling are semantic.

``Basis`` owns nonempty unique labels and canonical tuple storage.
``OperatorRecord`` separately owns ordering-length/matrix agreement and its
schema-version-1 orthonormal-basis requirement. ``orthonormal`` is metadata, not
numerical proof: no vectors or overlap matrix are stored. The approved public
architecture and Sphinx contract are the oracle. Failure may indicate an
implementation regression, contract/documentation mismatch, or evidence defect.

This software-verification module owns ``SV-B-001`` through ``SV-B-006``.
Passing establishes only the documented metadata behavior. It establishes no
basis-vector existence, linear independence, completeness, orthogonality,
StateSpace or matrix compatibility, gauge alignment, physical equivalence,
scientific validation, uncertainty quantification, or Rust conformance.

Intrinsic and cross-object scope
--------------------------------
The primary owner is ``Basis``; collaborators only construct inputs or expose public
outcomes. Accepted public contracts, literal expected values, Python language
semantics, and assigned schema or fixture artifacts provide the oracles. No runtime
warning is accepted unless a test explicitly states otherwise.

VVUQ and scientific exclusions
------------------------------
Passing establishes only the documented software contract and exact or explicitly
bounded acceptance rules. Failure may identify implementation, fixture, oracle,
environment, or contract defects. It does not establish numerical verification,
physical correctness, scientific validation, UQ, portability, or cross-language
agreement.
"""

import pytest

from ksdft2effmass.operators import Basis

pytestmark = pytest.mark.software_verification

SUT = Basis


def make_basis(
    *,
    identifier: str = "canonical",
    kind: str = "orthonormal test basis",
    ordering: tuple[str, ...] = ("a", "b"),
    orthonormal: bool = True,
) -> Basis:
    r"""Evidence ID
    Owns no identifier; supports evidence in this module.
    Requirement
    Valid fixtures pass typed abstract coordinate labels and metadata to the public
    constructor without hidden mutation or coercion.
    Method
    Construct ``Basis`` from explicit keyword arguments.
    Oracle
    The approved four-field public contract defines the constructor roles.
    Acceptance
    A valid synthetic ``Basis`` is returned.
    Interpretation
    The helper constructs metadata only; labels are abstract coordinates.
    Limitations
    It constructs no vectors or overlap matrix, performs no orthogonality calculation,
    and establishes no physical validity, scientific validation, uncertainty
    quantification, or Rust conformance.
    """

    return Basis(
        identifier=identifier,
        kind=kind,
        ordering=ordering,
        orthonormal=orthonormal,
    )


def test_constructor__public_fields_are_mapped_exactly__is_enforced() -> None:
    r"""Evidence ID
    SV-B-001
    Requirement
    Construction stores identifier, kind, ordering, and orthonormal metadata in their
    exact declared roles and canonical built-in types.
    Method
    Construct one valid object through the public package API and inspect only its four
    public fields.
    Oracle
    The approved represented-object declaration fixes values and types.
    Acceptance
    Values match exactly and types are ``str``, ``str``, ``tuple``, ``bool``.
    Interpretation
    Passing establishes public construction and exact stored-field mapping.
    Limitations
    Source location, matrix compatibility, scientific validation, UQ, and Rust
    conformance are not inspected or established.
    """

    basis = Basis(
        identifier="canonical",
        kind="orthonormal test basis",
        ordering=("a", "b"),
        orthonormal=True,
    )

    assert basis.identifier == "canonical"
    assert basis.kind == "orthonormal test basis"
    assert basis.ordering == ("a", "b")
    assert basis.orthonormal is True
    assert type(basis.identifier) is str
    assert type(basis.kind) is str
    assert type(basis.ordering) is tuple
    assert type(basis.orthonormal) is bool


@pytest.mark.parametrize(
    "ordering",
    [
        pytest.param(("a", "b"), id="tuple"),
        pytest.param(["a", "b"], id="list"),
    ],
)
def test_constructor__accepted_ordering_sequences_canonicalize_to__is_enforced(
    ordering: tuple[str, ...] | list[str],
) -> None:
    r"""Evidence ID
    SV-B-002
    Requirement
    Approved ordered sequences preserve values and become exact built-in tuple storage.
    Method
    Construct independently from a typed tuple and typed list.
    Oracle
    The public contract admits ordered sequences and fixes tuple storage.
    Acceptance
    Each stored ordering equals ``("a", "b")`` and has exact type ``tuple``.
    Interpretation
    Passing synchronizes constructor input typing and canonical stored state.
    Limitations
    Bare strings and non-sequence iterables are not approved by this evidence; no
    numerical or scientific validation, UQ, or Rust conformance follows.
    """

    basis = Basis(
        identifier="canonical",
        kind="orthonormal test basis",
        ordering=ordering,
        orthonormal=True,
    )

    assert type(basis.ordering) is tuple
    assert basis.ordering == ("a", "b")


def test_field__caller_owned_list_cannot_mutate_stored_ordering__is_exact() -> None:
    r"""Evidence ID
    SV-B-003
    Requirement
    Canonical tuple state must not alias caller-owned mutable list storage.
    Method
    Construct from a list, then replace and append caller-list elements.
    Oracle
    Defensive sequence-to-tuple canonicalization fixes the original order.
    Acceptance
    Stored ordering remains exactly ``("a", "b")``.
    Interpretation
    Passing establishes defensive ownership without mutating the frozen object.
    Limitations
    No vector storage, matrix storage, scientific validation, UQ, or Rust conformance is
    tested.
    """

    source = ["a", "b"]
    basis = Basis(
        identifier="canonical",
        kind="orthonormal test basis",
        ordering=source,
        orthonormal=True,
    )
    source[0] = "changed"
    source.append("c")

    assert basis.ordering == ("a", "b")


def test_field__represented__exact_label_order_and_spelling_are_preserved() -> None:
    r"""Evidence ID
    SV-B-004
    Requirement
    Construction performs no sorting, case folding, trimming, orbital-name
    interpretation, or Unicode normalization.
    Method
    Store mixed-case labels and separately construct a reordered object.
    Oracle
    The ordered-basis convention defines exact sequence equality.
    Acceptance
    Original labels are unchanged and reordered labels compare differently.
    Interpretation
    Passing establishes observable ordering and spelling preservation.
    Limitations
    It does not interpret orbital names or establish physical equivalence, scientific
    validation, uncertainty quantification, or Rust conformance.
    """

    ordering = ("p_z", "s", "P_X")
    basis = make_basis(ordering=ordering)
    reordered = make_basis(ordering=("s", "p_z", "P_X"))

    assert basis.ordering == ordering
    assert reordered.ordering != basis.ordering


def test_field__represented__both_exact_boolean_orthonormality_states_are() -> None:
    r"""Evidence ID
    SV-B-005
    Requirement
    ``Basis`` admits exact Python ``True`` and ``False`` as metadata.
    Method
    Construct independent objects differing only in ``orthonormal``.
    Oracle
    The Basis contract admits both states; ``OperatorRecord`` separately rejects
    ``False`` under schema version 1.
    Acceptance
    Stored values are exactly ``True`` and ``False`` respectively.
    Interpretation
    Passing establishes metadata representation only; it does not prove :math:`\langle
    b_i|b_j\rangle=\delta_{ij}` for actual vectors.
    Limitations
    No vectors, overlap matrix, orthogonality computation, record construction,
    scientific validation, UQ, or Rust conformance is involved.
    """

    orthonormal_basis = make_basis(orthonormal=True)
    nonorthonormal_basis = make_basis(orthonormal=False)

    assert orthonormal_basis.orthonormal is True
    assert nonorthonormal_basis.orthonormal is False


def test_method__serialize__basis_has_no_standalone_serialization_api() -> None:
    r"""Evidence ID
    SV-B-006
    Requirement
    Neither instance nor class exposes unapproved standalone JSON, dictionary,
    serializer, or deserializer method names.
    Method
    Inspect a valid instance and public class for six excluded names.
    Oracle
    ``OperatorRecordJsonSerializer`` owns Basis serialization only as nested record
    state; no independent Basis schema is approved.
    Acceptance
    Every excluded name is absent from instance and class.
    Interpretation
    Passing establishes the current standalone-serialization exclusion.
    Limitations
    Pickling and future schemas are unspecified; no round trip, scientific validation,
    uncertainty quantification, or Rust conformance is tested.
    """

    basis = make_basis()

    assert all(
        (not hasattr(basis, method_name)) and (not hasattr(Basis, method_name))
        for method_name in (
            "to_json",
            "to_dict",
            "serialize",
            "from_json",
            "from_dict",
            "deserialize",
        )
    )
