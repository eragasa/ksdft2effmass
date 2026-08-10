r"""Software verification of ``EnergyReference``.

Evidence profile: claim_bearing

Bounded artifact scope: the module's declared evidence owner.

Facet and represented meaning

-----------------------------
This class-owned module owns the construction facet. Facet and represented
DataObject
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

from dataclasses import fields
from typing import Any, cast

import pytest

from ksdft2effmass.operators import EnergyReference

pytestmark = pytest.mark.software_verification

SUT = EnergyReference


class SyntheticString(str):
    r"""Provide a synthetic ``str`` subclass for preservation evidence.

    Evidence ID: Supporting fixture type for ``SV-ER-002`` and ``SV-ER-003``; it owns no
    separate executable evidence identifier.

    Requirement: The public constructor accepts Python ``str`` instances and performs no
    canonicalization of accepted textual metadata.

    Method: Create researcher-authored metadata whose string subtype remains
    observable after construction.

    Oracle: The approved exact-pass-through contract requires the supplied string
    object and its content to remain unchanged.

    Acceptance: Owning tests observe the same object and exact textual value.

    Interpretation: This type supports detection of otherwise invisible string coercion.

    Limitations: Instances contain synthetic metadata and are passed through unchanged;
    the type performs no normalization or conversion. No DFT, Wannier,
    experimental, or impurity calculation supplies the values, and
    construction establishes no physical or scientific validity, scientific
    validation, uncertainty quantification, or Rust conformance.
    """


def test_constructor__public_fields_are_mapped_exactly__is_enforced() -> None:
    r"""Evidence ID: SV-ER-001

    Requirement: Public construction stores exactly ``zero`` and ``unit`` with the
    supplied textual
    values in their distinct roles.

    Method: Construct through the supported public import and inspect public dataclass
    fields
    and values.

    Oracle: The approved two-field DataObject contract defines the field names,
    ordering,
    meanings, and exact supplied values.

    Acceptance: The public stored fields are exactly ``("zero", "unit")`` and both
    values equal
    their corresponding inputs without preprocessing.

    Interpretation: Passing establishes exact constructor-to-field mapping for synthetic
    metadata.

    Limitations: It does not interpret the zero convention or unit, establish record
    compatibility,
    test nested JSON, perform scientific validation or UQ, or establish Rust
    conformance.
    """

    reference = EnergyReference("valence-band maximum", "eV")

    assert tuple(field.name for field in fields(EnergyReference)) == ("zero", "unit")
    assert reference.zero == "valence-band maximum"
    assert reference.unit == "eV"


@pytest.mark.parametrize(
    "zero",
    [
        pytest.param("explicit zero", id="sv_er_002_spaces"),
        pytest.param("valence-band maximum", id="sv_er_002_hyphenation"),
        pytest.param("Valence-Band Maximum", id="case"),
        pytest.param("vacuum level (synthetic)", id="sv_er_002_punctuation"),
        pytest.param("   ", id="sv_er_002_whitespace_only"),
        pytest.param(SyntheticString("synthetic zero"), id="sv_er_002_string_subclass"),
    ],
)
def test_field__represented__zero_convention_strings_are_preserved_exactly(
    zero: str,
) -> None:
    r"""Evidence ID: SV-ER-002

    Requirement: Nonempty zero-convention strings retain case, spaces, punctuation, and
    hyphenation
    without normalization or interpretation.

    Method: Construct independently with each synthetic label and a fixed valid unit,
    passing
    the string directly to the public constructor.

    Oracle: Exact Python string equality with the independently supplied input is the
    approved
    preservation oracle.

    Acceptance: ``reference.zero == zero`` for every case.

    Interpretation: Passing establishes literal metadata preservation for these
    examples.

    Limitations: It does not decide whether any label is physically meaningful, compare
    references,
    perform scientific validation or UQ, or establish Rust conformance.
    """

    reference = EnergyReference(zero, "eV")

    assert reference.zero == zero
    assert reference.zero is zero


@pytest.mark.parametrize(
    "unit",
    [
        pytest.param("eV", id="sv_er_003_ev"),
        pytest.param("EV", id="sv_er_003_ev"),
        pytest.param("hartree", id="sv_er_003_hartree"),
        pytest.param("Ha", id="sv_er_003_ha"),
        pytest.param("   ", id="sv_er_003_whitespace_only"),
        pytest.param(SyntheticString("Ry"), id="sv_er_003_string_subclass"),
    ],
)
def test_field__energy_unit_strings_are_preserved_exactly__is_exact(
    unit: str,
) -> None:
    r"""Evidence ID: SV-ER-003

    Requirement: Nonempty unit strings are stored literally without registry lookup,
    alias
    resolution, normalization, dimensional analysis, or conversion.

    Method: Construct independently with each synthetic label and compare it with the
    directly
    supplied input.

    Oracle: Exact Python string equality is the approved preservation oracle.

    Acceptance: ``reference.unit == unit`` for every case.

    Interpretation: Passing establishes literal storage, including case distinctions.

    Limitations: It does not recognize units, assert equivalence between labels, verify
    a conversion
    factor, perform scientific validation or UQ, or establish Rust conformance.
    """

    reference = EnergyReference("explicit zero", unit)

    assert reference.unit == unit
    assert reference.unit is unit


@pytest.mark.parametrize(
    "keyword",
    [
        pytest.param("value", id="value_keyword"),
        pytest.param("offset", id="offset_keyword"),
        pytest.param("energy_offset", id="energy_offset_keyword"),
        pytest.param("reference_energy", id="reference_energy_keyword"),
    ],
)
def test_constructor__numerical_offset_keywords__are_rejected(keyword: str) -> None:
    r"""Evidence ID: SV-ER-004

    Requirement: ``EnergyReference`` rejects each unapproved numerical-offset keyword
    role.

    Method: Call the public constructor through ``Any`` with one named finite offset.

    Oracle: The accepted constructor owns exactly ``zero`` and ``unit``.

    Acceptance: Every named case raises exactly ``TypeError``.

    Interpretation: A pass confirms closed keyword roles; failure indicates API or
    contract drift.

    Limitations: Positional arity, stored fields, validation, UQ, and Rust are excluded.
    """
    with pytest.raises(TypeError):
        cast(Any, EnergyReference)("explicit zero", "eV", **{keyword: 0.0})


def test_constructor__numerical_offset_positional_argument__is_rejected() -> None:
    r"""Evidence ID: SV-ER-013

    Requirement: ``EnergyReference`` rejects an unapproved third positional offset.

    Method: Call the public constructor through ``Any`` with an additional finite float.

    Oracle: The accepted constructor has exactly two positional roles.

    Acceptance: Exactly ``TypeError`` is raised.

    Interpretation: A pass confirms positional arity; failure indicates public API
    drift.

    Limitations: Keyword rejection, represented state, validation, UQ, and Rust are
    excluded.
    """
    with pytest.raises(TypeError):
        cast(Any, EnergyReference)("explicit zero", "eV", 0.0)


def test_field__numerical_offset_attributes__are_absent() -> None:
    r"""Evidence ID: SV-ER-014

    Requirement: A valid energy reference stores no numerical offset field under
    approved names.

    Method: Inspect the public instance for the four explicitly excluded names.

    Oracle: Accepted represented state contains only ``zero`` and ``unit``.

    Acceptance: All four names are absent exactly.

    Interpretation: A pass confirms represented-state exclusion; failure indicates API
    drift.

    Limitations: Private state, scientific alignment, validation, UQ, and Rust are
    excluded.
    """
    reference = EnergyReference("explicit zero", "eV")
    assert all(
        not hasattr(reference, name)
        for name in ("value", "offset", "energy_offset", "reference_energy")
    )


def test_public_api__serialization__is_absent() -> None:
    r"""Evidence ID: SV-ER-005

    Requirement: Neither instance nor class owns standalone serialization, JSON, or
    dictionary
    conversion APIs.

    Method: Inspect a valid instance and the public class for all six excluded method
    names.

    Oracle: ``OperatorRecordJsonSerializer`` exclusively owns the nested record JSON
    representation; no independent ``EnergyReference`` wire format exists.

    Acceptance: Every excluded method is absent from both instance and class.

    Interpretation: Passing establishes the current nested-only serialization boundary.

    Limitations: It does not test private serializer mechanics, record round trips,
    pickling,
    scientific validation, UQ, or Rust conformance.
    """

    reference = EnergyReference("explicit zero", "eV")

    assert all(
        (not hasattr(reference, method_name))
        and (not hasattr(EnergyReference, method_name))
        for method_name in (
            "serialize",
            "deserialize",
            "to_json",
            "from_json",
            "to_dict",
            "from_dict",
        )
    )
