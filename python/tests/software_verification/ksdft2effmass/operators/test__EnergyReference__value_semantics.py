r"""Software verification of ``EnergyReference``.

Evidence profile: claim_bearing

Bounded artifact scope: the module's declared evidence owner.

Facet and represented meaning

-----------------------------
This class-owned module owns the value semantics facet. Facet and represented
DataObject
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

Intrinsic and cross-object scope

--------------------------------
The primary owner is ``EnergyReference``; collaborators only construct inputs or
expose public outcomes. Accepted public contracts, literal expected values, Python
language semantics, and assigned schema or fixture artifacts provide the oracles. No
runtime warning is accepted unless a test explicitly states otherwise.

VVUQ and scientific exclusions

------------------------------
Passing establishes only the documented software contract and exact or explicitly
bounded acceptance rules. Failure may identify implementation, fixture, oracle,
environment, or contract defects. It does not establish numerical verification,
physical correctness, scientific validation, UQ, portability, or cross-language
agreement.
"""

from dataclasses import FrozenInstanceError

import pytest

from ksdft2effmass.operators import EnergyReference

pytestmark = pytest.mark.software_verification

SUT = EnergyReference


def make_energy_reference(
    *,
    zero: str = "valence-band maximum",
    unit: str = "eV",
) -> EnergyReference:
    r"""Evidence ID: Owns no identifier; supports evidence in this module.

    Requirement: Synthetic fixtures pass the two typed textual fields unchanged to the
    public
    constructor.

    Method: Construct ``EnergyReference(zero=zero, unit=unit)`` without preprocessing.

    Oracle: The approved DataObject contract defines the two stored fields and exact
    pass-through behavior.

    Acceptance: A valid public ``EnergyReference`` is returned.

    Interpretation: The helper supplies independently constructible synthetic metadata.

    Limitations: It performs no normalization, conversion, vocabulary lookup, DFT,
    Wannier,
    experimental, or impurity calculation. Construction establishes no physical or
    scientific validity, scientific validation, uncertainty quantification, or Rust
    conformance.
    """

    return EnergyReference(zero=zero, unit=unit)


@pytest.mark.parametrize(
    ("attribute", "replacement"),
    [
        pytest.param("zero", "other zero", id="zero_field"),
        pytest.param("unit", "hartree", id="unit_field"),
        pytest.param("dynamic_attribute", "forbidden", id="undeclared_field"),
    ],
)
def test_field__stored_state_is_frozen_and_slotted__is_exact(
    attribute: str, replacement: str
) -> None:
    r"""Evidence ID: SV-ER-010

    Requirement: ``zero`` and ``unit`` cannot be reassigned, arbitrary attributes cannot
    be added,
    and slotted instances expose no per-instance ``__dict__``.

    Method: Attempt ordinary assignment to both fields and one undeclared name, then
    inspect the
    instance dictionary boundary.

    Oracle: The approved frozen, slotted two-field DataObject contract defines the exact
    public
    exception taxonomy.

    Acceptance: Every assignment raises exactly ``FrozenInstanceError`` and ``__dict__``
    is absent.

    Interpretation: Passing establishes ordinary public-API immutable slotted state.

    Limitations: It does not use invariant bypasses, assert hash behavior, test nested
    serialization,
    perform scientific validation or UQ, or establish Rust conformance.
    """

    reference = make_energy_reference()

    with pytest.raises(FrozenInstanceError) as exc_info:
        setattr(reference, attribute, replacement)
    assert type(exc_info.value) is FrozenInstanceError
    assert not hasattr(reference, "__dict__")


def test_method__eq__exact_structural_equality_uses_both_stored_fields() -> None:
    r"""Evidence ID: SV-ER-011

    Requirement: Independently constructed references with identical ``zero`` and
    ``unit`` compare
    equal; changing either field makes them unequal.

    Method: Compare one baseline with an identical object and two independently
    constructed
    single-field variants.

    Oracle: The approved dataclass value contract defines exact structural equality
    across the
    two stored fields.

    Acceptance: The identical object compares equal and each single-field variant does
    not.

    Interpretation: Passing establishes exact DataObject equality rather than object
    identity.

    Limitations: It does not determine physical equivalence, execute compatibility
    rules, assert hash
    behavior, perform scientific validation or UQ, or establish Rust conformance.
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
        pytest.param("Valence-Band Maximum", "eV", id="zero_case"),
        pytest.param("valence band maximum", "eV", id="zero_spacing_punctuation"),
        pytest.param("valence-band maximum", "EV", id="unit_case"),
        pytest.param("valence-band maximum", "Ha", id="unit_spelling"),
    ],
)
def test_method__eq__preserves_exact_text(
    zero: str,
    unit: str,
) -> None:
    r"""Evidence ID: SV-ER-012

    Requirement: Equality is sensitive to zero-label case, punctuation or spacing, and
    unit-label
    case or spelling.

    Method: Compare a fixed synthetic baseline with one-field representation variants
    passed
    unchanged through the public constructor.

    Oracle: Exact Python string inequality over stored fields is the approved oracle.

    Acceptance: Every variant compares unequal to the baseline.

    Interpretation: Passing establishes literal metadata identity for equality.

    Limitations: It does not claim that ``eV`` and ``EV`` or ``hartree`` and ``Ha`` are
    physically
    inequivalent, execute the compatibility analyzer, perform scientific validation or
    UQ, or establish Rust conformance.
    """

    reference = make_energy_reference()
    variant = make_energy_reference(zero=zero, unit=unit)

    assert reference != variant
