r"""Software verification of ``EnergyReference`` intrinsic invariants.

Facet and represented DataObject
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
"""

from typing import Any, cast

import pytest

from ksdft2effmass.operators import EnergyReference

pytestmark = pytest.mark.software_verification


@pytest.mark.parametrize(
    "invalid_zero",
    [
        pytest.param(None, id="SV-ER-006-none"),
        pytest.param(True, id="SV-ER-006-boolean-true"),
        pytest.param(False, id="SV-ER-006-boolean-false"),
        pytest.param(1, id="SV-ER-006-integer"),
        pytest.param(1.0, id="SV-ER-006-float"),
        pytest.param(b"zero", id="SV-ER-006-bytes"),
        pytest.param(object(), id="SV-ER-006-arbitrary-object"),
    ],
)
def test_invalid_zero_semantic_types_are_rejected(invalid_zero: object) -> None:
    """SV-ER-006: require zero-convention string semantics independently.

    Evidence ID
        ``SV-ER-006``; stable parameter IDs identify each wrong semantic family.
    Requirement
        ``zero`` must be a Python string; ``None``, Booleans, numbers, bytes,
        and arbitrary objects are not coerced into convention identifiers.
    Method
        Keep ``unit`` valid and use ``Any``/``cast`` only at the deliberate
        invalid ``zero`` constructor boundary.
    Oracle
        The approved field-specific contract requires an energy-reference zero
        string and the repository wrong-type taxonomy.
    Acceptance
        Every case raises ``TypeError`` and the diagnostic identifies ``zero``
        and the string requirement without freezing the complete message.
    Interpretation
        Passing establishes zero-field typing independently of unit typing.
    Limitations
        It does not interpret labels, execute compatibility or serialization,
        perform scientific validation or UQ, or establish Rust conformance.
    """

    with pytest.raises(TypeError) as exc_info:
        EnergyReference(cast(Any, invalid_zero), "eV")

    message = str(exc_info.value)
    assert "zero" in message
    assert "string" in message


def test_empty_zero_is_rejected_without_normalization() -> None:
    """SV-ER-007: reject the empty zero-convention string.

    Evidence ID
        ``SV-ER-007``.
    Requirement
        A correctly typed zero-convention label must be nonempty; construction
        performs no trimming or replacement.
    Method
        Construct with ``zero=""`` and a valid unit.
    Oracle
        The approved intrinsic nonempty invariant defines field-specific
        ``ValueError``.
    Acceptance
        Construction raises ``ValueError`` and identifies the empty zero field.
    Interpretation
        Passing establishes the correct-type/value taxonomy boundary.
    Limitations
        Every nonempty string, including whitespace-only metadata, remains
        governed by exact preservation; no physical interpretation, scientific
        validation, UQ, or Rust conformance is established.
    """

    with pytest.raises(ValueError) as exc_info:
        EnergyReference("", "eV")

    message = str(exc_info.value)
    assert "zero" in message
    assert "must not be empty" in message


@pytest.mark.parametrize(
    "invalid_unit",
    [
        pytest.param(None, id="SV-ER-008-none"),
        pytest.param(True, id="SV-ER-008-boolean-true"),
        pytest.param(False, id="SV-ER-008-boolean-false"),
        pytest.param(1, id="SV-ER-008-integer"),
        pytest.param(1.0, id="SV-ER-008-float"),
        pytest.param(b"eV", id="SV-ER-008-bytes"),
        pytest.param(object(), id="SV-ER-008-arbitrary-object"),
    ],
)
def test_invalid_unit_semantic_types_are_rejected(invalid_unit: object) -> None:
    """SV-ER-008: require energy-unit string semantics independently.

    Evidence ID
        ``SV-ER-008``; stable parameter IDs independently identify the same
        semantic families used at the separate zero boundary.
    Requirement
        ``unit`` must be a Python string; ``None``, Booleans, numbers, bytes,
        and arbitrary objects are not coerced into unit labels.
    Method
        Keep ``zero`` valid and use ``Any``/``cast`` only at the deliberate
        invalid ``unit`` constructor boundary.
    Oracle
        The approved field-specific contract requires an energy-reference unit
        string and the repository wrong-type taxonomy.
    Acceptance
        Every case raises ``TypeError`` and the diagnostic identifies ``unit``
        and the string requirement without freezing the complete message.
    Interpretation
        Passing establishes unit typing independently of zero typing.
    Limitations
        It does not introduce a registry or conversion, execute compatibility or
        serialization, perform scientific validation or UQ, or establish Rust
        conformance.
    """

    with pytest.raises(TypeError) as exc_info:
        EnergyReference("explicit zero", cast(Any, invalid_unit))

    message = str(exc_info.value)
    assert "unit" in message
    assert "string" in message


def test_empty_unit_is_rejected_without_unit_lookup() -> None:
    """SV-ER-009: reject the empty energy-unit string.

    Evidence ID
        ``SV-ER-009``.
    Requirement
        A correctly typed unit label must be nonempty while remaining an open
        textual vocabulary.
    Method
        Construct with a valid zero convention and ``unit=""``.
    Oracle
        The approved intrinsic nonempty invariant defines field-specific
        ``ValueError``.
    Acceptance
        Construction raises ``ValueError`` and identifies the empty unit field.
    Interpretation
        Passing establishes the correct-type/value taxonomy boundary.
    Limitations
        It validates no label vocabulary, dimensions, or conversions and
        establishes no scientific validation, UQ, or Rust conformance.
    """

    with pytest.raises(ValueError) as exc_info:
        EnergyReference("explicit zero", "")

    message = str(exc_info.value)
    assert "unit" in message
    assert "must not be empty" in message
