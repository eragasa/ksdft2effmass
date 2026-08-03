r"""Software verification of ``EnergyReference`` value semantics.

Facet and represented DataObject
--------------------------------
This module owns frozen and slotted state plus exact structural equality for the
``EnergyReference`` DataObject. Its exact state is the textual zero-convention
identifier ``zero`` and textual energy-unit label ``unit``; no numerical offset
is represented.

Ownership and evidence interpretation
-------------------------------------
Equality is exact metadata identity, not physical equivalence. Relational
compatibility belongs to ``OperatorRecordCompatibilityAnalyzer`` and nested JSON
representation belongs to ``OperatorRecordJsonSerializer``. The approved public
contract and synchronized Sphinx documentation are the oracle. Passing
establishes DataObject value semantics; failure may indicate an implementation
regression, documentation mismatch, or evidence defect.

VVUQ boundaries
---------------
This module provides software-verification evidence ``SV-ER-010`` through
``SV-ER-012``. ``EnergyReference`` owns no numerical algorithm, so numerical
verification is not applicable. Synthetic metadata are not supplied by DFT,
Wannier, experiment, or an impurity calculation. No physical equivalence,
scientific validation, uncertainty quantification, or Rust conformance is
established. Hash behavior is intentionally unspecified and untested.
"""

from dataclasses import FrozenInstanceError

import pytest

from ksdft2effmass.operators import EnergyReference

pytestmark = pytest.mark.software_verification


def make_energy_reference(
    *,
    zero: str = "valence-band maximum",
    unit: str = "eV",
) -> EnergyReference:
    """Construct valid synthetic ``EnergyReference`` metadata unchanged.

    Evidence ID
        Supporting helper for ``SV-ER-010`` through ``SV-ER-012``; it owns no
        separate executable evidence identifier.
    Requirement
        Synthetic fixtures pass the two typed textual fields unchanged to the
        public constructor.
    Method
        Construct ``EnergyReference(zero=zero, unit=unit)`` without preprocessing.
    Oracle
        The approved DataObject contract defines the two stored fields and exact
        pass-through behavior.
    Acceptance
        A valid public ``EnergyReference`` is returned.
    Interpretation
        The helper supplies independently constructible synthetic metadata.
    Limitations
        It performs no normalization, conversion, vocabulary lookup, DFT,
        Wannier, experimental, or impurity calculation. Construction establishes
        no physical or scientific validity, scientific validation, uncertainty
        quantification, or Rust conformance.
    """

    return EnergyReference(zero=zero, unit=unit)


def test_stored_state_is_frozen_and_slotted() -> None:
    """SV-ER-010: verify frozen fields and absence of dynamic state.

    Evidence ID
        ``SV-ER-010``.
    Requirement
        ``zero`` and ``unit`` cannot be reassigned, arbitrary attributes cannot
        be added, and slotted instances expose no per-instance ``__dict__``.
    Method
        Attempt ordinary assignment to both fields and one undeclared name,
        then inspect the instance dictionary boundary.
    Oracle
        The approved frozen, slotted two-field DataObject contract defines the
        exact public exception taxonomy.
    Acceptance
        Every assignment raises exactly ``FrozenInstanceError`` and
        ``__dict__`` is absent.
    Interpretation
        Passing establishes ordinary public-API immutable slotted state.
    Limitations
        It does not use invariant bypasses, assert hash behavior, test nested
        serialization, perform scientific validation or UQ, or establish Rust
        conformance.
    """

    reference = make_energy_reference()

    for attribute, replacement in (
        ("zero", "other zero"),
        ("unit", "hartree"),
        ("dynamic_attribute", "forbidden"),
    ):
        with pytest.raises(FrozenInstanceError) as exc_info:
            setattr(reference, attribute, replacement)
        assert type(exc_info.value) is FrozenInstanceError
    assert not hasattr(reference, "__dict__")


def test_exact_structural_equality_uses_both_stored_fields() -> None:
    """SV-ER-011: verify exact equality across both textual fields.

    Evidence ID
        ``SV-ER-011``.
    Requirement
        Independently constructed references with identical ``zero`` and
        ``unit`` compare equal; changing either field makes them unequal.
    Method
        Compare one baseline with an identical object and two independently
        constructed single-field variants.
    Oracle
        The approved dataclass value contract defines exact structural equality
        across the two stored fields.
    Acceptance
        The identical object compares equal and each single-field variant does
        not.
    Interpretation
        Passing establishes exact DataObject equality rather than object identity.
    Limitations
        It does not determine physical equivalence, execute compatibility rules,
        assert hash behavior, perform scientific validation or UQ, or establish
        Rust conformance.
    """

    reference = make_energy_reference()
    identical = make_energy_reference()
    different_zero = make_energy_reference(zero="explicit zero")
    different_unit = make_energy_reference(unit="hartree")

    assert reference == identical
    assert reference != different_zero
    assert reference != different_unit


@pytest.mark.parametrize(
    ("zero", "unit"),
    [
        pytest.param(
            "Valence-Band Maximum",
            "eV",
            id="SV-ER-012-zero-case",
        ),
        pytest.param(
            "valence band maximum",
            "eV",
            id="SV-ER-012-zero-spacing-punctuation",
        ),
        pytest.param(
            "valence-band maximum",
            "EV",
            id="SV-ER-012-unit-case",
        ),
        pytest.param(
            "valence-band maximum",
            "Ha",
            id="SV-ER-012-unit-spelling",
        ),
    ],
)
def test_equality_is_case_punctuation_spacing_and_spelling_sensitive(
    zero: str,
    unit: str,
) -> None:
    """SV-ER-012: distinguish exact string representations in equality.

    Evidence ID
        ``SV-ER-012``; stable parameter IDs identify each exact representation
        distinction.
    Requirement
        Equality is sensitive to zero-label case, punctuation or spacing, and
        unit-label case or spelling.
    Method
        Compare a fixed synthetic baseline with one-field representation
        variants passed unchanged through the public constructor.
    Oracle
        Exact Python string inequality over stored fields is the approved oracle.
    Acceptance
        Every variant compares unequal to the baseline.
    Interpretation
        Passing establishes literal metadata identity for equality.
    Limitations
        It does not claim that ``eV`` and ``EV`` or ``hartree`` and ``Ha`` are
        physically inequivalent, execute the compatibility analyzer, perform
        scientific validation or UQ, or establish Rust conformance.
    """

    reference = make_energy_reference()
    variant = make_energy_reference(zero=zero, unit=unit)

    assert reference != variant
