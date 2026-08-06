r"""Software verification of ``DeclaredCapability``.

Facet and represented meaning
-----------------------------
This class-owned evidence verifies capability construction, enum typing, identifier invariants, immutability, equality, and durable-state exclusion..

Intrinsic and cross-object scope
--------------------------------
The sole primary SUT is ``DeclaredCapability``; collaborators only supply public constructor
inputs or expose declared Python value semantics. Oracles are the accepted
field, enum, dataclass, tuple, and exception contracts. Values are synthetic,
dimensionless metadata at ordinary lexical scales; no warnings are expected.

VVUQ and scientific exclusions
------------------------------
Passing establishes only the stated software contract. Failure indicates a
production, test-input, or accepted-contract mismatch. This evidence does not
establish numerical verification, physical correctness, scientific validation,
uncertainty quantification, portability, or cross-language agreement.
"""

# ruff: noqa: E501

from dataclasses import FrozenInstanceError, astuple, fields
from typing import Any, cast

import pytest

from ksdft2effmass.provenance import CapabilityKind, DeclaredCapability

SUT = DeclaredCapability
pytestmark = pytest.mark.software_verification


def test_constructor__field_mapping__stores_exact_declaration() -> None:
    """Evidence ID
    SV-PROV-028
    Requirement
    A capability stores five exact declaration fields including the semantic enum member.
    Method
    Construct fixed synthetic capability metadata and inspect public dataclass state.
    Oracle
    The accepted signature and literals define exact field order and values.
    Acceptance
    All names, values, and semantic types match exactly.
    Interpretation
    A pass confirms this bounded software contract; a failure identifies an implementation, test-input, or contract mismatch.
    Limitations
    Synthetic metadata only; no external execution, numerical verification, scientific validation, UQ, portability, or cross-language claim.
    """
    record = SUT("cap-1", "qe", CapabilityKind.EXECUTE, "run-pw", "v1")
    assert tuple(field.name for field in fields(record)) == (
        "capability_id",
        "tool_id",
        "kind",
        "name",
        "specification_version",
    )
    assert astuple(record) == ("cap-1", "qe", CapabilityKind.EXECUTE, "run-pw", "v1")
    assert type(record.kind) is CapabilityKind


@pytest.mark.parametrize(
    "field_name",
    [
        pytest.param("capability_id", id="capability_id"),
        pytest.param("tool_id", id="tool_id"),
        pytest.param("name", id="capability_name"),
        pytest.param("specification_version", id="specification_version"),
    ],
)
def test_constructor__text_semantic_type__rejects_non_string(field_name: str) -> None:
    """Evidence ID
    SV-PROV-029
    Requirement
    Capability textual fields require exact built-in strings.
    Method
    Replace each valid textual field with bytes under explicit semantic IDs.
    Oracle
    The public type contract excludes bytes.
    Acceptance
    Every partition raises TypeError.
    Interpretation
    A pass confirms this bounded software contract; a failure identifies an implementation, test-input, or contract mismatch.
    Limitations
    Synthetic metadata only; no external execution, numerical verification, scientific validation, UQ, portability, or cross-language claim.
    """
    kwargs: dict[str, Any] = {
        "capability_id": "cap-1",
        "tool_id": "qe",
        "kind": CapabilityKind.EXECUTE,
        "name": "run-pw",
        "specification_version": "v1",
    }
    kwargs[field_name] = b"wrong"
    with pytest.raises(TypeError):
        SUT(**kwargs)


def test_constructor__kind_semantic_type__rejects_string_lookalike() -> None:
    """Evidence ID
    SV-PROV-200
    Requirement
    Capability kind requires a CapabilityKind member, not its wire string.
    Method
    Pass the string lookalike with otherwise valid state.
    Oracle
    The accepted semantic type is the public enum class.
    Acceptance
    Construction raises TypeError.
    Interpretation
    A pass confirms this bounded software contract; a failure identifies an implementation, test-input, or contract mismatch.
    Limitations
    Synthetic metadata only; no external execution, numerical verification, scientific validation, UQ, portability, or cross-language claim.
    """
    with pytest.raises(TypeError):
        SUT("cap-1", "qe", cast(Any, "execute"), "run-pw", "v1")


def test_constructor__portable_text_value__rejects_invalid_identifier() -> None:
    """Evidence ID
    SV-PROV-201
    Requirement
    Capability identifiers obey the portable lexical grammar.
    Method
    Pass an embedded-space capability identifier.
    Oracle
    The fixed grammar excludes spaces.
    Acceptance
    Construction raises ValueError.
    Interpretation
    A pass confirms this bounded software contract; a failure identifies an implementation, test-input, or contract mismatch.
    Limitations
    Synthetic metadata only; no external execution, numerical verification, scientific validation, UQ, portability, or cross-language claim.
    """
    with pytest.raises(ValueError):
        SUT("bad id", "qe", CapabilityKind.EXECUTE, "run-pw", "v1")


def test_field__frozen_assignment__rejects_reassignment() -> None:
    """Evidence ID
    SV-PROV-202
    Requirement
    Capability declarations are operationally immutable.
    Method
    Attempt assignment to the public name field.
    Oracle
    Frozen dataclass semantics require FrozenInstanceError.
    Acceptance
    Assignment raises FrozenInstanceError.
    Interpretation
    A pass confirms this bounded software contract; a failure identifies an implementation, test-input, or contract mismatch.
    Limitations
    Synthetic metadata only; no external execution, numerical verification, scientific validation, UQ, portability, or cross-language claim.
    """
    record = SUT("cap-1", "qe", CapabilityKind.EXECUTE, "run-pw", "v1")
    with pytest.raises(FrozenInstanceError):
        field_name = "name"
        setattr(record, field_name, "other")


def test_method__eq__compares_complete_represented_state() -> None:
    """Evidence ID
    SV-PROV-203
    Requirement
    Equality covers the complete capability declaration.
    Method
    Compare equal instances and one differing only in kind.
    Oracle
    Dataclass equality over all fields is the oracle.
    Acceptance
    Complete equality is true and one-field inequality is false.
    Interpretation
    A pass confirms this bounded software contract; a failure identifies an implementation, test-input, or contract mismatch.
    Limitations
    Synthetic metadata only; no external execution, numerical verification, scientific validation, UQ, portability, or cross-language claim.
    """
    left = SUT("cap-1", "qe", CapabilityKind.EXECUTE, "run-pw", "v1")
    assert left == SUT("cap-1", "qe", CapabilityKind.EXECUTE, "run-pw", "v1")
    assert left != SUT("cap-1", "qe", CapabilityKind.PARSE, "run-pw", "v1")


def test_field__durable_surface__excludes_runtime_state() -> None:
    """Evidence ID
    SV-PROV-204
    Requirement
    A declaration contains no runtime or credential state.
    Method
    Inspect public dataclass field names against prohibited runtime names.
    Oracle
    The durable boundary excludes command, credential, client, process, and handle.
    Acceptance
    The sets are disjoint.
    Interpretation
    A pass confirms this bounded software contract; a failure identifies an implementation, test-input, or contract mismatch.
    Limitations
    Synthetic metadata only; no external execution, numerical verification, scientific validation, UQ, portability, or cross-language claim.
    """
    assert {f.name for f in fields(SUT)}.isdisjoint(
        {"command", "credential", "client", "process", "handle"}
    )
