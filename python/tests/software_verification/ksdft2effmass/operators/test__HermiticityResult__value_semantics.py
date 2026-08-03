r"""Software verification of ``HermiticityResult`` value semantics.

Facet and contract
------------------
This module owns frozen and slotted stored state plus exact structural equality.
The only stored dataclass fields are residual :math:`\varepsilon_{\mathrm H}`,
tolerance :math:`\tau`, and their common ``energy_unit``. ``is_hermitian`` is a
derived property and is not dataclass state.

Ownership and scope
-------------------
Equality compares the three canonical stored fields exactly. It is not an
approximate comparison and does not imply physical equivalence or physical
Hermiticity. These tests use synthetic scalars and invoke no matrix operation or
``HermiticityAnalyzer``. The approved architecture and Sphinx contracts are the
oracle. Failure may indicate a value-semantics regression, contract/documentation
mismatch, or evidence defect.

VVUQ boundaries
---------------
This module provides software-verification evidence ``SV-HR-014`` and
``SV-HR-015``. Passing establishes immutable slotted state and exact value
semantics only. It does not establish residual numerical accuracy, tolerance
appropriateness, DFT or Wannier validity, scientific validation, uncertainty
quantification, or Rust conformance. Hash behavior is intentionally unspecified.
"""

from dataclasses import FrozenInstanceError, fields

import pytest

from ksdft2effmass.operators import HermiticityResult

pytestmark = pytest.mark.software_verification


def make_result(
    *,
    residual: float = 2.0e-13,
    tolerance: float = 1.0e-12,
    energy_unit: str = "eV",
) -> HermiticityResult:
    """Construct valid synthetic value fixtures for ``SV-HR-014`` and ``015``.

    Evidence ID
        Supporting helper for ``SV-HR-014`` and ``SV-HR-015``; it owns no
        separate evidence identifier.
    Requirement
        Equality and immutability fixtures use only values intended to satisfy
        the public semantic types and pass each field unchanged.
    Method
        Call the public three-field constructor with typed keyword arguments.
    Oracle
        The approved ResultObject contract defines the three stored fields and
        their canonicalization.
    Acceptance
        A valid public synthetic ResultObject is returned.
    Interpretation
        The helper supplies independently constructible exact value states.
    Limitations
        It performs no matrix analysis, unit conversion, numerical verification,
        scientific validation, UQ, or Rust-conformance check and establishes no
        scientific validity.
    """

    return HermiticityResult(
        residual=residual,
        tolerance=tolerance,
        energy_unit=energy_unit,
    )


@pytest.mark.parametrize(
    ("field_name", "replacement"),
    [
        pytest.param("residual", 3.0e-13, id="SV-HR-014-residual"),
        pytest.param("tolerance", 2.0e-12, id="SV-HR-014-tolerance"),
        pytest.param("energy_unit", "Ha", id="SV-HR-014-energy-unit"),
    ],
)
def test_stored_state_is_frozen_and_slotted(
    field_name: str,
    replacement: object,
) -> None:
    """SV-HR-014: verify exact fields, slots, and frozen assignment behavior.

    Evidence ID
        ``SV-HR-014``; parameter IDs identify each declared stored field without
        creating additional evidence identifiers.
    Requirement
        Stored dataclass fields are exactly ``residual``, ``tolerance``, and
        ``energy_unit``; no instance dictionary exists; ordinary assignment to
        each field is forbidden; ``is_hermitian`` is not stored state.
    Method
        Inspect public dataclass metadata, inspect the instance dictionary
        boundary, and attempt ordinary assignment with ``setattr`` for each
        declared field.
    Oracle
        The approved frozen, slotted ResultObject contract and public dataclass
        field declaration define stored state.
    Acceptance
        Field names match exactly, ``__dict__`` is absent,
        ``is_hermitian`` is not a field, and each assignment raises exactly
        ``FrozenInstanceError``.
    Interpretation
        Passing establishes API-level immutable slotted stored state.
    Limitations
        No invariant bypass, ``object.__setattr__``, derived-property assignment,
        hashability, Analyzer behavior, numerical verification, scientific
        validation, UQ, or Rust conformance is tested.
    """

    result = make_result()
    field_names = tuple(field.name for field in fields(HermiticityResult))

    assert field_names == ("residual", "tolerance", "energy_unit")
    assert "is_hermitian" not in field_names
    assert not hasattr(result, "__dict__")
    with pytest.raises(FrozenInstanceError):
        setattr(result, field_name, replacement)


def test_exact_structural_equality_uses_all_stored_fields() -> None:
    """SV-HR-015: verify exact equality and independent field inequality.

    Evidence ID
        ``SV-HR-015``.
    Requirement
        Independently constructed objects with identical canonical stored fields
        compare equal; changing residual, tolerance, or unit independently makes
        them unequal.
    Method
        Construct one baseline, one identical value, and three single-field
        variants and compare them without approximate assertions.
    Oracle
        The approved frozen dataclass contract defines exact structural equality
        across all three stored fields.
    Acceptance
        The identical object compares equal and each independently varied object
        compares unequal.
    Interpretation
        Passing establishes exact ResultObject value semantics, not object
        identity or scientific equivalence.
    Limitations
        Approximate equality, unrelated-object comparison, hash behavior,
        physical equivalence, Analyzer accuracy, scientific validation, UQ, and
        Rust conformance are unspecified or untested.
    """

    first = make_result()
    identical = make_result()
    different_residual = make_result(residual=3.0e-13)
    different_tolerance = make_result(tolerance=2.0e-12)
    different_energy_unit = make_result(energy_unit="Ha")

    assert first == identical
    assert first != different_residual
    assert first != different_tolerance
    assert first != different_energy_unit
