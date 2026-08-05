"""Evidence class and represented meaning
Software verification of declared external-tool capabilities.
Owned contract, oracle, and scope
DeclaredCapability is the SUT; exact field mapping and version-1 CapabilityKind
vocabulary are the oracle.
VVUQ and scientific exclusions
Evidence excludes capability probing, execution, numerical verification, scientific
validation, UQ, and cross-language conformance.
"""

import pytest

from ksdft2effmass.provenance import CapabilityKind, DeclaredCapability

SUT = DeclaredCapability
pytestmark = pytest.mark.software_verification


def test_constructor__capability_fields__maps_exact_declaration() -> None:
    """Evidence ID
    SV-PROV-028
    Requirement
    Capability identity, provider, kind, name, and contract version map exactly.
    Method
    Construct one parse capability through public imports and inspect all fields.
    Oracle
    The accepted five-field DataObject vocabulary is exact.
    Acceptance
    The complete field tuple equals the supplied values.
    Interpretation
    Failure indicates field or enum mapping drift.
    Limitations
    Declaring capability does not install or verify it.
    """
    value = SUT("cap-1", "qe", CapabilityKind.PARSE, "parse-output", "v1")
    assert (
        value.capability_id,
        value.tool_id,
        value.kind,
        value.name,
        value.specification_version,
    ) == ("cap-1", "qe", CapabilityKind.PARSE, "parse-output", "v1")


def test_constructor__kind_semantic_type__rejects_string_lookalike() -> None:
    """Evidence ID
    SV-PROV-029
    Requirement
    Capability kind is the exact public enum rather than a wire string at runtime.
    Method
    Pass the valid wire spelling directly to the public constructor.
    Oracle
    Public runtime typing requires TypeError without coercion.
    Acceptance
    The string lookalike raises TypeError.
    Interpretation
    Failure indicates unintended boundary coercion.
    Limitations
    JSON enum decoding is owned by the serializer evidence.
    """
    with pytest.raises(TypeError):
        SUT("cap", "tool", "parse", "name", "v1")  # type: ignore[arg-type]


def test_field__capability_enum_values__match_closed_vocabulary() -> None:
    """Evidence ID
    SV-PROV-030
    Requirement
    Version-1 capabilities are exactly execute, parse, render, and transfer.
    Method
    Enumerate public CapabilityKind values.
    Oracle
    The accepted closed enum artifact fixes the exact tuple.
    Acceptance
    Values equal the expected strings in declared order.
    Interpretation
    Failure indicates public and wire vocabulary drift.
    Limitations
    The test does not claim any provider supports a category.
    """
    assert tuple(item.value for item in CapabilityKind) == (
        "execute",
        "parse",
        "render",
        "transfer",
    )
