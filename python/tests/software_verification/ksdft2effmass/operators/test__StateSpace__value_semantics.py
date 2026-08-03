r"""Software verification of ``StateSpace`` value semantics.

Facet and represented meaning
-----------------------------
This module owns frozen and slotted stored state plus exact structural equality.
``StateSpace`` represents finite metadata for :math:`\dim\mathcal H=N` and
stores exactly ``identifier``, ``kind``, and canonical built-in ``dimension``.

Intrinsic and cross-object scope
--------------------------------
Equality is exact over all three intrinsic metadata fields. It is not physical
equivalence and does not compare bases, matrices, geometry, or energy references.
Cross-object agreement belongs to ``OperatorRecord``. The approved architecture
and Sphinx contract are the oracle. Passing establishes DataObject value
semantics; failure may indicate an implementation regression, documentation
mismatch, or evidence defect.

VVUQ and scientific exclusions
------------------------------
This module provides software-verification evidence ``SV-SS-012`` and
``SV-SS-013``. It establishes no basis completeness, operator-domain correctness,
matrix compatibility, DFT or Wannier validity, scientific validation,
uncertainty quantification, or Rust conformance. Hash behavior is intentionally
unspecified and untested.
"""

from dataclasses import FrozenInstanceError, fields

import pytest

from ksdft2effmass.operators import StateSpace

pytestmark = pytest.mark.software_verification


def make_state_space(
    *,
    identifier: str = "two-level",
    kind: str = "finite synthetic",
    dimension: int = 2,
) -> StateSpace:
    """Construct valid synthetic values for ``SV-SS-012`` and ``SV-SS-013``.

    Evidence ID
        Supporting helper for ``SV-SS-012`` and ``SV-SS-013``; it owns no
        separate evidence identifier.
    Requirement
        Value-semantics fixtures use typed valid fields passed unchanged to the
        public constructor.
    Method
        Construct independent ``StateSpace`` objects from explicit keyword
        arguments.
    Oracle
        The approved DataObject contract defines the three stored fields and
        constructor-owned canonicalization.
    Acceptance
        A valid public synthetic ``StateSpace`` is returned.
    Interpretation
        The helper supplies independently constructible metadata values.
    Limitations
        It constructs no basis, allocates no vector or matrix, and establishes
        no physical validity, scientific validation, uncertainty quantification,
        or Rust conformance.
    """

    return StateSpace(identifier=identifier, kind=kind, dimension=dimension)


@pytest.mark.parametrize(
    ("field_name", "replacement"),
    [
        pytest.param("identifier", "other-space", id="SV-SS-012-identifier"),
        pytest.param("kind", "other kind", id="SV-SS-012-kind"),
        pytest.param("dimension", 3, id="SV-SS-012-dimension"),
    ],
)
def test_stored_state_is_frozen_and_slotted(
    field_name: str,
    replacement: object,
) -> None:
    """SV-SS-012: verify exact fields, slots, and frozen assignment.

    Evidence ID
        ``SV-SS-012``; stable parameter IDs identify every declared field.
    Requirement
        Dataclass state is exactly ``identifier``, ``kind``, and ``dimension``;
        no instance dictionary exists and ordinary assignment is forbidden.
    Method
        Inspect standard dataclass fields, inspect the instance ``__dict__``
        boundary, and attempt ordinary ``setattr`` for each declared field.
    Oracle
        The approved frozen, slotted three-field DataObject contract defines
        stored state.
    Acceptance
        Field names match exactly, ``__dict__`` is absent, and every assignment
        raises exactly ``FrozenInstanceError``.
    Interpretation
        Passing establishes API-level immutable slotted metadata state.
    Limitations
        No invariant bypass, ``object.__setattr__``, hash behavior, cross-object
        behavior, scientific validation, UQ, or Rust conformance is tested.
    """

    state_space = make_state_space()
    field_names = tuple(field.name for field in fields(StateSpace))

    assert field_names == ("identifier", "kind", "dimension")
    assert not hasattr(state_space, "__dict__")
    with pytest.raises(FrozenInstanceError):
        setattr(state_space, field_name, replacement)


def test_exact_structural_equality_uses_all_stored_fields() -> None:
    """SV-SS-013: verify exact equality across all three fields.

    Evidence ID
        ``SV-SS-013``.
    Requirement
        Independently constructed objects with identical canonical metadata are
        equal; changing identifier, kind, or dimension independently makes them
        unequal.
    Method
        Construct a baseline, an identical value, and three single-field
        variants, then compare without approximation.
    Oracle
        The approved frozen dataclass contract defines exact structural equality
        over every stored field.
    Acceptance
        The identical value compares equal and each variant compares unequal.
    Interpretation
        Passing establishes exact metadata value semantics, not identity or
        physical equivalence.
    Limitations
        Approximate or physical equivalence, basis and matrix compatibility, hash
        behavior, scientific validation, UQ, and Rust conformance are unspecified
        or untested.
    """

    first = make_state_space()
    identical = make_state_space()
    different_identifier = make_state_space(identifier="other-space")
    different_kind = make_state_space(kind="other kind")
    different_dimension = make_state_space(dimension=3)

    assert first == identical
    assert first != different_identifier
    assert first != different_kind
    assert first != different_dimension
