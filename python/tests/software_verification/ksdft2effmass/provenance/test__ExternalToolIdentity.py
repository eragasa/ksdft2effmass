"""Evidence class and represented meaning
Software verification of immutable external-tool family identity.
Owned contract, oracle, and scope
ExternalToolIdentity is the SUT; its exact two-field portable contract is the oracle.
VVUQ and scientific exclusions
Evidence excludes dynamic imports, tool discovery, execution, numerical verification,
scientific validation, UQ, and cross-language conformance.
"""

from dataclasses import FrozenInstanceError

import pytest

from ksdft2effmass.provenance import ExternalToolIdentity

SUT = ExternalToolIdentity
pytestmark = pytest.mark.software_verification


def test_constructor__portable_identity_fields__maps_exact_values_and_is_frozen() -> (
    None
):
    """Evidence ID
    SV-PROV-024
    Requirement
    Tool identity stores only stable tool and implementation-family identifiers in
    frozen state.
    Method
    Construct through the public API, inspect fields, and attempt reassignment.
    Oracle
    The accepted portable two-field record contract is exact.
    Acceptance
    Fields equal inputs and mutation raises FrozenInstanceError.
    Interpretation
    Failure indicates field or immutability drift.
    Limitations
    No implementation is imported, located, or executed.
    """
    value = SUT("qe", "quantum-espresso")
    assert (value.tool_id, value.implementation_family) == ("qe", "quantum-espresso")
    with pytest.raises(FrozenInstanceError):
        value.tool_id = "other"  # type: ignore[misc]


def test_constructor__identifier_types__rejects_strings_with_invalid_grammar() -> None:
    """Evidence ID
    SV-PROV-025
    Requirement
    Both fields are nonempty bounded portable identifiers and are not coerced.
    Method
    Pass empty, whitespace, mapping, and overlength alternatives.
    Oracle
    The public identifier grammar and semantic type policy determine rejection.
    Acceptance
    Mapping raises TypeError and malformed strings raise ValueError.
    Interpretation
    Failure indicates unintended coercion or grammar weakening.
    Limitations
    Identifier namespace registration is outside this intrinsic check.
    """
    with pytest.raises(TypeError):
        SUT({}, "family")  # type: ignore[arg-type]
    for text in ("", "has space", "a" * 129):
        with pytest.raises(ValueError):
            SUT("tool", text)
