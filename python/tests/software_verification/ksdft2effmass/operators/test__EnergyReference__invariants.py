r"""Software verification of ``EnergyReference``.

Facet and represented meaning
-----------------------------
This class-owned module owns the invariants facet. Facet and represented DataObject
--------------------------------
This module owns independent semantic-type and empty-value rejection for the
``EnergyReference.zero`` energy-origin-convention identifier and
``EnergyReference.unit`` energy-unit label. Both are textual metadata stored
without normalization or conversion.

Ownership and evidence interpretation
-------------------------------------
These tests address only DataObject-owned intrinsic validation. Exact relational
compatibility belongs to ``OperatorRecordCompatibilityAnalyzer``; nested JSON
validation belongs to ``OperatorRecordJsonSerializer``. The approved public
contract and synchronized Sphinx documentation are the oracle. Passing
establishes the constructor exception taxonomy; failure may indicate an
implementation regression, documentation mismatch, or evidence defect.

VVUQ boundaries
---------------
This module provides software-verification evidence ``SV-ER-006`` through
``SV-ER-009``. ``EnergyReference`` owns no numerical algorithm, so numerical
verification is not applicable. The synthetic strings are not supplied by DFT,
Wannier, experiment, or an impurity calculation. No physical-unit validity,
scientific validation, uncertainty quantification, or Rust conformance is
established.

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

from typing import Any, cast

import pytest

from ksdft2effmass.operators import EnergyReference

pytestmark = pytest.mark.software_verification

SUT = EnergyReference


@pytest.mark.parametrize(
    "invalid_zero",
    [
        pytest.param(None, id="none"),
        pytest.param(True, id="sv_er_006_boolean_true"),
        pytest.param(False, id="sv_er_006_boolean_false"),
        pytest.param(1, id="sv_er_006_integer"),
        pytest.param(1.0, id="sv_er_006_float"),
        pytest.param(b"zero", id="bytes"),
        pytest.param(object(), id="sv_er_006_arbitrary_object"),
    ],
)
def test_constructor__invalid_zero_wrong_types_are_rejected__is_enforced(
    invalid_zero: object,
) -> None:
    r"""Evidence ID
    SV-ER-006
    Requirement
    ``zero`` must be a Python string; ``None``, Booleans, numbers, bytes, and arbitrary
    objects are not coerced into convention identifiers.
    Method
    Keep ``unit`` valid and use ``Any``/``cast`` only at the deliberate invalid ``zero``
    constructor boundary.
    Oracle
    The approved field-specific contract requires an energy-reference zero string and
    the repository wrong-type taxonomy.
    Acceptance
    Every case raises ``TypeError`` and the diagnostic identifies ``zero`` and the
    string requirement without freezing the complete message.
    Interpretation
    Passing establishes zero-field typing independently of unit typing.
    Limitations
    It does not interpret labels, execute compatibility or serialization, perform
    scientific validation or UQ, or establish Rust conformance.
    """

    with pytest.raises(TypeError) as exc_info:
        EnergyReference(cast(Any, invalid_zero), "eV")

    message = str(exc_info.value)
    assert "zero" in message
    assert "string" in message


def test_constructor__empty_zero_is_rejected_without__is_enforced() -> None:
    r"""Evidence ID
    SV-ER-007
    Requirement
    A correctly typed zero-convention label must be nonempty; construction performs no
    trimming or replacement.
    Method
    Construct with ``zero=""`` and a valid unit.
    Oracle
    The approved intrinsic nonempty invariant defines field-specific ``ValueError``.
    Acceptance
    Construction raises ``ValueError`` and identifies the empty zero field.
    Interpretation
    Passing establishes the correct-type/value taxonomy boundary.
    Limitations
    Every nonempty string, including whitespace-only metadata, remains governed by exact
    preservation; no physical interpretation, scientific validation, UQ, or Rust
    conformance is established.
    """

    with pytest.raises(ValueError) as exc_info:
        EnergyReference("", "eV")

    message = str(exc_info.value)
    assert "zero" in message
    assert "must not be empty" in message


@pytest.mark.parametrize(
    "invalid_unit",
    [
        pytest.param(None, id="none"),
        pytest.param(True, id="sv_er_008_boolean_true"),
        pytest.param(False, id="sv_er_008_boolean_false"),
        pytest.param(1, id="sv_er_008_integer"),
        pytest.param(1.0, id="sv_er_008_float"),
        pytest.param(b"eV", id="bytes"),
        pytest.param(object(), id="sv_er_008_arbitrary_object"),
    ],
)
def test_constructor__invalid_unit_wrong_types_are_rejected__is_enforced(
    invalid_unit: object,
) -> None:
    r"""Evidence ID
    SV-ER-008
    Requirement
    ``unit`` must be a Python string; ``None``, Booleans, numbers, bytes, and arbitrary
    objects are not coerced into unit labels.
    Method
    Keep ``zero`` valid and use ``Any``/``cast`` only at the deliberate invalid ``unit``
    constructor boundary.
    Oracle
    The approved field-specific contract requires an energy-reference unit string and
    the repository wrong-type taxonomy.
    Acceptance
    Every case raises ``TypeError`` and the diagnostic identifies ``unit`` and the
    string requirement without freezing the complete message.
    Interpretation
    Passing establishes unit typing independently of zero typing.
    Limitations
    It does not introduce a registry or conversion, execute compatibility or
    serialization, perform scientific validation or UQ, or establish Rust conformance.
    """

    with pytest.raises(TypeError) as exc_info:
        EnergyReference("explicit zero", cast(Any, invalid_unit))

    message = str(exc_info.value)
    assert "unit" in message
    assert "string" in message


def test_constructor__empty_unit_is_rejected_without_unit_lookup__is_enforced() -> None:
    r"""Evidence ID
    SV-ER-009
    Requirement
    A correctly typed unit label must be nonempty while remaining an open textual
    vocabulary.
    Method
    Construct with a valid zero convention and ``unit=""``.
    Oracle
    The approved intrinsic nonempty invariant defines field-specific ``ValueError``.
    Acceptance
    Construction raises ``ValueError`` and identifies the empty unit field.
    Interpretation
    Passing establishes the correct-type/value taxonomy boundary.
    Limitations
    It validates no label vocabulary, dimensions, or conversions and establishes no
    scientific validation, UQ, or Rust conformance.
    """

    with pytest.raises(ValueError) as exc_info:
        EnergyReference("explicit zero", "")

    message = str(exc_info.value)
    assert "unit" in message
    assert "must not be empty" in message
