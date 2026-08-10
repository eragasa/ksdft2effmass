r"""Software verification of ``Basis``.

Evidence profile: claim_bearing

Bounded artifact scope: the module's declared evidence owner.

Facet and represented meaning

-----------------------------
This class-owned module owns the value semantics facet. This module owns
frozen/slotted stored state and exact structural equality. For
:math:`\mathcal B=(|b_0\rangle,\ldots,|b_{N-1}\rangle)`, the ordering tuple is
semantic coordinate metadata: reordering or changing label spelling changes the
represented Basis value.

Equality covers exactly ``identifier``, ``kind``, canonical tuple ``ordering``,
and exact Boolean ``orthonormal``. It is neither approximate nor physical basis
equivalence. ``OperatorRecord`` separately owns matrix/state-space agreement and
its orthonormal-basis policy. Tuple canonicalization belongs to construction; no
vectors or overlap matrix exist here. The approved architecture and Sphinx
contract are the oracle. Failure may indicate an implementation regression,
contract/documentation mismatch, or evidence defect.

This module provides only software-verification evidence ``SV-B-017`` and
``SV-B-018``. Passing establishes immutable slotted state and ordering-sensitive
exact equality. Hash behavior is intentionally unspecified and untested. No
linear independence, completeness, numerical orthogonality, matrix compatibility,
gauge alignment, physical equivalence, scientific validation, uncertainty
quantification, or Rust conformance is established.

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

from dataclasses import FrozenInstanceError, fields

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
    r"""Evidence ID: Owns no identifier; supports evidence in this module.

    Requirement: Value fixtures use typed abstract labels and pass all four fields
    unchanged to the
    public constructor.

    Method: Construct an independent ``Basis`` from explicit keyword arguments.

    Oracle: The approved DataObject contract defines exact four-field state.

    Acceptance: A valid synthetic ``Basis`` is returned.

    Interpretation: The helper supplies independently constructible metadata values.

    Limitations: It constructs no vectors or overlap matrix, performs no orthogonality
    calculation,
    and establishes no physical validity, scientific validation, uncertainty
    quantification, or Rust conformance.
    """

    return Basis(
        identifier=identifier,
        kind=kind,
        ordering=ordering,
        orthonormal=orthonormal,
    )


@pytest.mark.parametrize(
    ("field_name", "replacement"),
    [
        pytest.param("identifier", "other", id="identifier"),
        pytest.param("kind", "other kind", id="kind"),
        pytest.param("ordering", ("b", "a"), id="ordering"),
        pytest.param("orthonormal", False, id="orthonormal"),
    ],
)
def test_field__stored_state_is_frozen_and_slotted__is_exact(
    field_name: str,
    replacement: object,
) -> None:
    r"""Evidence ID: SV-B-017

    Requirement: Dataclass state is exactly identifier, kind, ordering, and orthonormal;
    no instance
    dictionary exists and ordinary assignment is forbidden.

    Method: Inspect standard dataclass fields and ``__dict__``, then use ordinary
    ``setattr`` on
    each declared field.

    Oracle: The approved frozen, slotted four-field DataObject contract defines state.

    Acceptance: Exact field names are present, ``__dict__`` is absent, and each
    assignment raises
    exactly ``FrozenInstanceError``.

    Interpretation: Passing establishes API-level immutable slotted metadata state.

    Limitations: No invariant bypass, ``object.__setattr__``, hash behavior,
    cross-object behavior,
    scientific validation, UQ, or Rust conformance is tested.
    """

    basis = make_basis()
    field_names = tuple(field.name for field in fields(Basis))

    assert field_names == ("identifier", "kind", "ordering", "orthonormal")
    assert not hasattr(basis, "__dict__")
    with pytest.raises(FrozenInstanceError):
        setattr(basis, field_name, replacement)


def test_method__eq__covers_ordered_complete_state() -> None:
    r"""Evidence ID: SV-B-018

    Requirement: Independent identical metadata values compare equal; identifier, kind,
    label order,
    label spelling, and orthonormal changes compare unequal.

    Method: Construct a baseline, an identical value, and one variant for each
    observable
    distinction, then compare without approximation.

    Oracle: Frozen-dataclass structural equality and exact ordered-label semantics
    define the
    expected relations.

    Acceptance: Only the independently identical Basis equals the baseline; all five
    variants are
    unequal, including ``("a", "b")`` versus ``("b", "a")``.

    Interpretation: Passing establishes exact metadata value semantics, not object
    identity or physical
    basis equivalence.

    Limitations: Approximate/gauge/physical equivalence, matrix compatibility, hash
    behavior,
    scientific validation, UQ, and Rust conformance are untested.
    """

    first = make_basis()
    identical = make_basis()
    different_identifier = make_basis(identifier="other")
    different_kind = make_basis(kind="other kind")
    reordered = make_basis(ordering=("b", "a"))
    different_spelling = make_basis(ordering=("a", "B"))
    different_orthonormal = make_basis(orthonormal=False)

    assert first == identical
    assert first != different_identifier
    assert first != different_kind
    assert first != reordered
    assert first != different_spelling
    assert first != different_orthonormal
