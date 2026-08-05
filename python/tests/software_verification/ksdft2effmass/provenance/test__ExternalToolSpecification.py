"""Evidence class and represented meaning
Software verification of immutable requested external-tool specifications.
Owned contract, oracle, and scope
ExternalToolSpecification is the SUT; exact identifiers and narrow portable version text
are the oracle.
VVUQ and scientific exclusions
Evidence excludes installation, resolution, execution, numerical verification,
scientific validation, UQ, and cross-language conformance.
"""

from dataclasses import FrozenInstanceError

import pytest

from ksdft2effmass.provenance import ExternalToolSpecification

SUT = ExternalToolSpecification
pytestmark = pytest.mark.software_verification


def test_constructor__declared_specification_fields__maps_exact_portable_values() -> (
    None
):
    """Evidence ID
    SV-PROV-026
    Requirement
    Specification, tool, portable version, and executable/package identifiers map
    exactly and remain immutable.
    Method
    Construct with narrow version text, inspect fields, and attempt reassignment.
    Oracle
    The accepted four-field declaration and lexical version grammar are exact.
    Acceptance
    Fields equal inputs and reassignment raises FrozenInstanceError.
    Interpretation
    Failure indicates mapping, normalization, or mutability drift.
    Limitations
    No version solver, package manager, or executable is consulted.
    """
    value = SUT("spec-1", "qe", "7.2+build.1", "pw.x")
    assert (
        value.specification_id,
        value.tool_id,
        value.requested_version,
        value.executable_or_package_id,
    ) == ("spec-1", "qe", "7.2+build.1", "pw.x")
    with pytest.raises(FrozenInstanceError):
        value.requested_version = "7.3"  # type: ignore[misc]


def test_constructor__version_text_and_identifiers__rejects_raw_or_wrong_inputs() -> (
    None
):
    """Evidence ID
    SV-PROV-027
    Requirement
    Version is built-in portable lexical text limited to 64 characters; identity fields
    follow portable grammar.
    Method
    Pass numeric, empty, comparator, whitespace, slash, and overlength versions plus a
    path-like executable.
    Oracle
    Public type, version regex, and identifier grammar independently define rejection.
    Acceptance
    Numeric version raises TypeError and each invalid string raises ValueError.
    Interpretation
    Failure indicates raw version admission or coercion.
    Limitations
    Version precedence and compatibility interpretation are excluded.
    """
    with pytest.raises(TypeError):
        SUT("spec", "tool", 7, "exe")  # type: ignore[arg-type]
    for version in ("", ">=7.2,<8", "7 2", "v/7", "a" * 65):
        with pytest.raises(ValueError):
            SUT("spec", "tool", version, "exe")
    with pytest.raises(ValueError):
        SUT("spec", "tool", "7", "bin/tool")
