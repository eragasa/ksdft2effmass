r"""Software verification of ``EnergyReference`` construction.

Facet and represented DataObject
--------------------------------
This module owns public construction, exact stored-field mapping, exact
zero-convention and unit-label preservation, numerical-offset exclusion, and
standalone-serialization exclusion for the ``EnergyReference`` DataObject. The
object stores textual metadata only: ``zero`` identifies an energy-origin
convention and ``unit`` labels the matrix energy unit.

Ownership and evidence interpretation
-------------------------------------
``EnergyReference`` validates its two intrinsic strings. Exact compatibility
between two references belongs to ``OperatorRecordCompatibilityAnalyzer``.
Nested record JSON representation belongs to ``OperatorRecordJsonSerializer``.
The approved public contract and synchronized Sphinx documentation are the
oracle. Passing establishes the documented Python construction boundary;
failure may indicate an implementation regression, documentation mismatch, or
evidence defect.

VVUQ boundaries
---------------
This module provides software-verification evidence ``SV-ER-001`` through
``SV-ER-005``. ``EnergyReference`` owns no numerical algorithm, so numerical
verification is not applicable. Synthetic labels are not supplied by DFT,
Wannier, experiment, or an impurity calculation. No physical interpretation,
scientific validation, uncertainty quantification, or Rust conformance is
performed.
"""

from dataclasses import fields
from typing import Any, cast

import pytest

from ksdft2effmass.operators import EnergyReference

pytestmark = pytest.mark.software_verification


class SyntheticString(str):
    """Provide a synthetic ``str`` subclass for preservation evidence.

    Evidence ID
        Supporting fixture type for ``SV-ER-002`` and ``SV-ER-003``; it owns no
        separate executable evidence identifier.
    Requirement
        The public constructor accepts Python ``str`` instances and performs no
        canonicalization of accepted textual metadata.
    Method
        Create researcher-authored metadata whose string subtype remains
        observable after construction.
    Oracle
        The approved exact-pass-through contract requires the supplied string
        object and its content to remain unchanged.
    Acceptance
        Owning tests observe the same object and exact textual value.
    Interpretation
        This type supports detection of otherwise invisible string coercion.
    Limitations
        Instances contain synthetic metadata and are passed through unchanged;
        the type performs no normalization or conversion. No DFT, Wannier,
        experimental, or impurity calculation supplies the values, and
        construction establishes no physical or scientific validity, scientific
        validation, uncertainty quantification, or Rust conformance.
    """


def test_public_construction_and_exact_stored_field_mapping() -> None:
    """SV-ER-001: verify public construction and exact field roles.

    Evidence ID
        ``SV-ER-001``.
    Requirement
        Public construction stores exactly ``zero`` and ``unit`` with the
        supplied textual values in their distinct roles.
    Method
        Construct through the supported public import and inspect public
        dataclass fields and values.
    Oracle
        The approved two-field DataObject contract defines the field names,
        ordering, meanings, and exact supplied values.
    Acceptance
        The public stored fields are exactly ``("zero", "unit")`` and both
        values equal their corresponding inputs without preprocessing.
    Interpretation
        Passing establishes exact constructor-to-field mapping for synthetic
        metadata.
    Limitations
        It does not interpret the zero convention or unit, establish record
        compatibility, test nested JSON, perform scientific validation or UQ,
        or establish Rust conformance.
    """

    reference = EnergyReference("valence-band maximum", "eV")

    assert tuple(field.name for field in fields(EnergyReference)) == ("zero", "unit")
    assert reference.zero == "valence-band maximum"
    assert reference.unit == "eV"


@pytest.mark.parametrize(
    "zero",
    [
        pytest.param("explicit zero", id="SV-ER-002-spaces"),
        pytest.param("valence-band maximum", id="SV-ER-002-hyphenation"),
        pytest.param("Valence-Band Maximum", id="SV-ER-002-case"),
        pytest.param("vacuum level (synthetic)", id="SV-ER-002-punctuation"),
        pytest.param("   ", id="SV-ER-002-whitespace-only"),
        pytest.param(
            SyntheticString("synthetic zero"),
            id="SV-ER-002-string-subclass",
        ),
    ],
)
def test_zero_convention_strings_are_preserved_exactly(zero: str) -> None:
    """SV-ER-002: preserve representative zero labels exactly.

    Evidence ID
        ``SV-ER-002``; stable parameter IDs identify the represented character
        distinction.
    Requirement
        Nonempty zero-convention strings retain case, spaces, punctuation, and
        hyphenation without normalization or interpretation.
    Method
        Construct independently with each synthetic label and a fixed valid
        unit, passing the string directly to the public constructor.
    Oracle
        Exact Python string equality with the independently supplied input is
        the approved preservation oracle.
    Acceptance
        ``reference.zero == zero`` for every case.
    Interpretation
        Passing establishes literal metadata preservation for these examples.
    Limitations
        It does not decide whether any label is physically meaningful, compare
        references, perform scientific validation or UQ, or establish Rust
        conformance.
    """

    reference = EnergyReference(zero, "eV")

    assert reference.zero == zero
    assert reference.zero is zero


@pytest.mark.parametrize(
    "unit",
    [
        pytest.param("eV", id="SV-ER-003-eV"),
        pytest.param("EV", id="SV-ER-003-EV"),
        pytest.param("hartree", id="SV-ER-003-hartree"),
        pytest.param("Ha", id="SV-ER-003-Ha"),
        pytest.param("   ", id="SV-ER-003-whitespace-only"),
        pytest.param(SyntheticString("Ry"), id="SV-ER-003-string-subclass"),
    ],
)
def test_energy_unit_strings_are_preserved_exactly(unit: str) -> None:
    """SV-ER-003: preserve representative energy-unit labels exactly.

    Evidence ID
        ``SV-ER-003``; stable parameter IDs retain case-sensitive spellings.
    Requirement
        Nonempty unit strings are stored literally without registry lookup,
        alias resolution, normalization, dimensional analysis, or conversion.
    Method
        Construct independently with each synthetic label and compare it with
        the directly supplied input.
    Oracle
        Exact Python string equality is the approved preservation oracle.
    Acceptance
        ``reference.unit == unit`` for every case.
    Interpretation
        Passing establishes literal storage, including case distinctions.
    Limitations
        It does not recognize units, assert equivalence between labels, verify a
        conversion factor, perform scientific validation or UQ, or establish
        Rust conformance.
    """

    reference = EnergyReference("explicit zero", unit)

    assert reference.unit == unit
    assert reference.unit is unit


def test_numerical_offset_constructor_and_stored_state_are_excluded() -> None:
    """SV-ER-004: exclude numerical-offset constructor and field state.

    Evidence ID
        ``SV-ER-004``.
    Requirement
        ``EnergyReference`` accepts exactly two constructor roles and stores no
        numerical ``value``, ``offset``, ``energy_offset``, or
        ``reference_energy`` field.
    Method
        Deliberately call the public constructor with one additional positional
        value and each specified offset keyword, using ``Any`` only at these
        invalid boundaries; inspect a valid instance for forbidden attributes.
    Oracle
        The approved metadata-only contract contains no numerical offset.
    Acceptance
        Every unsupported constructor call raises ``TypeError`` and a valid
        instance exposes none of the forbidden stored attributes.
    Interpretation
        Passing establishes exclusion from this public DataObject only.
    Limitations
        It does not duplicate malformed serializer-payload evidence, interpret
        energy alignment, perform scientific validation or UQ, or establish
        Rust conformance.
    """

    constructor = cast(Any, EnergyReference)
    with pytest.raises(TypeError):
        constructor("explicit zero", "eV", 0.0)
    for keyword in ("value", "offset", "energy_offset", "reference_energy"):
        with pytest.raises(TypeError):
            constructor("explicit zero", "eV", **{keyword: 0.0})

    reference = EnergyReference("explicit zero", "eV")
    for attribute in ("value", "offset", "energy_offset", "reference_energy"):
        assert not hasattr(reference, attribute)


def test_energy_reference_has_no_standalone_serialization_api() -> None:
    """SV-ER-005: verify standalone serialization exclusion.

    Evidence ID
        ``SV-ER-005``.
    Requirement
        Neither instance nor class owns standalone serialization, JSON, or
        dictionary conversion APIs.
    Method
        Inspect a valid instance and the public class for all six excluded
        method names.
    Oracle
        ``OperatorRecordJsonSerializer`` exclusively owns the nested record JSON
        representation; no independent ``EnergyReference`` wire format exists.
    Acceptance
        Every excluded method is absent from both instance and class.
    Interpretation
        Passing establishes the current nested-only serialization boundary.
    Limitations
        It does not test private serializer mechanics, record round trips,
        pickling, scientific validation, UQ, or Rust conformance.
    """

    reference = EnergyReference("explicit zero", "eV")

    for method_name in (
        "serialize",
        "deserialize",
        "to_json",
        "from_json",
        "to_dict",
        "from_dict",
    ):
        assert not hasattr(reference, method_name)
        assert not hasattr(EnergyReference, method_name)
