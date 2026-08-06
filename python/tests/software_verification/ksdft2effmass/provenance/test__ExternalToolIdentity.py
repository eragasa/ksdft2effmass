r"""Software verification of ``ExternalToolIdentity``.

Facet and represented meaning
-----------------------------
This class-owned evidence verifies constructor mapping, strict portable identifiers, immutability, equality, and durable field boundaries..

Intrinsic and cross-object scope
--------------------------------
The sole primary SUT is ``ExternalToolIdentity``; collaborators only supply public constructor
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

from dataclasses import FrozenInstanceError, fields
from typing import Any

import pytest

from ksdft2effmass.provenance import ExternalToolIdentity

SUT = ExternalToolIdentity
pytestmark = pytest.mark.software_verification


def test_constructor__field_mapping__stores_exact_declared_types_and_values() -> None:
    """Evidence ID
    SV-PROV-024
    Requirement
    Construction stores the complete accepted field mapping with exact built-in semantic types.
    Method
    Construct the SUT from fixed valid synthetic metadata and inspect public dataclass fields.
    Oracle
    The accepted constructor signature and supplied literals define exact names, order, values, and types.
    Acceptance
    The public field sequence and stored tuple equal the declared literals exactly.
    Interpretation
    A pass confirms this bounded software contract; a failure identifies an implementation, test-input, or contract mismatch.
    Limitations
    Synthetic metadata only; no external execution, numerical verification, scientific validation, UQ, portability, or cross-language claim.
    """
    record = SUT(tool_id="qe", implementation_family="quantum-espresso")
    assert tuple(field.name for field in fields(record)) == (
        "tool_id",
        "implementation_family",
    )
    assert tuple(getattr(record, field.name) for field in fields(record)) == (
        "qe",
        "quantum-espresso",
    )
    assert all(
        type(getattr(record, field.name)) is type(value)
        for field, value in zip(
            fields(record),
            (
                "qe",
                "quantum-espresso",
            ),
            strict=True,
        )
    )


@pytest.mark.parametrize(
    "field_name",
    [
        pytest.param("tool_id", id="tool_id"),
        pytest.param("implementation_family", id="implementation_family"),
    ],
)
def test_constructor__text_semantic_type__rejects_non_builtin_string(
    field_name: str,
) -> None:
    """Evidence ID
    SV-PROV-025
    Requirement
    Every textual field requires a built-in string rather than a lookalike value.
    Method
    Replace one valid field at a time with bytes using explicit semantic field IDs.
    Oracle
    The accepted type taxonomy requires exact built-in str fields.
    Acceptance
    Every partition raises TypeError.
    Interpretation
    A pass confirms this bounded software contract; a failure identifies an implementation, test-input, or contract mismatch.
    Limitations
    Synthetic metadata only; no external execution, numerical verification, scientific validation, UQ, portability, or cross-language claim.
    """
    kwargs: dict[str, Any] = {
        "tool_id": "qe",
        "implementation_family": "quantum-espresso",
    }
    kwargs[field_name] = b"wrong"
    with pytest.raises(TypeError):
        SUT(**kwargs)


@pytest.mark.parametrize(
    "invalid_text",
    [
        pytest.param("", id="empty_text"),
        pytest.param("embedded space", id="embedded_space"),
        pytest.param("e\u0301", id="non_nfc_text"),
        pytest.param(chr(0xD800), id="unicode_surrogate"),
        pytest.param("x" * 129, id="overlength_text"),
    ],
)
def test_constructor__portable_text_value__rejects_invalid_grammar(
    invalid_text: str,
) -> None:
    """Evidence ID
    SV-PROV-191
    Requirement
    Portable identifier text is nonempty NFC, surrogate-free, grammar-conforming, and at most 128 characters.
    Method
    Replace the first identifier with explicit invalid lexical partitions.
    Oracle
    The accepted literal identifier grammar supplies the independent rejection set.
    Acceptance
    Every partition raises ValueError.
    Interpretation
    A pass confirms this bounded software contract; a failure identifies an implementation, test-input, or contract mismatch.
    Limitations
    Synthetic metadata only; no external execution, numerical verification, scientific validation, UQ, portability, or cross-language claim.
    """
    kwargs: dict[str, Any] = {
        "tool_id": "qe",
        "implementation_family": "quantum-espresso",
    }
    kwargs["tool_id"] = invalid_text
    with pytest.raises(ValueError):
        SUT(**kwargs)


def test_field__frozen_assignment__rejects_reassignment() -> None:
    """Evidence ID
    SV-PROV-192
    Requirement
    The maintained record is operationally immutable after construction.
    Method
    Assign a different valid value to one public field.
    Oracle
    Frozen dataclass semantics require FrozenInstanceError.
    Acceptance
    Assignment raises FrozenInstanceError and cannot mutate state.
    Interpretation
    A pass confirms this bounded software contract; a failure identifies an implementation, test-input, or contract mismatch.
    Limitations
    Synthetic metadata only; no external execution, numerical verification, scientific validation, UQ, portability, or cross-language claim.
    """
    record = SUT(tool_id="qe", implementation_family="quantum-espresso")
    with pytest.raises(FrozenInstanceError):
        field_name = "tool_id"
        setattr(record, field_name, "replacement")


def test_method__eq__compares_complete_represented_state() -> None:
    """Evidence ID
    SV-PROV-193
    Requirement
    Exact equality compares the full represented constructor state.
    Method
    Compare equal records and a record differing in one field.
    Oracle
    Dataclass value semantics over all declared fields define equality.
    Acceptance
    Equal full state compares true and one-field-different state compares false.
    Interpretation
    A pass confirms this bounded software contract; a failure identifies an implementation, test-input, or contract mismatch.
    Limitations
    Synthetic metadata only; no external execution, numerical verification, scientific validation, UQ, portability, or cross-language claim.
    """
    left = SUT(tool_id="qe", implementation_family="quantum-espresso")
    equal = SUT(tool_id="qe", implementation_family="quantum-espresso")
    changed_kwargs: dict[str, Any] = {
        "tool_id": "qe",
        "implementation_family": "quantum-espresso",
    }
    changed_kwargs["tool_id"] = "replacement"
    assert left == equal
    assert left != SUT(**changed_kwargs)


def test_field__durable_surface__excludes_runtime_credentials_and_handles() -> None:
    """Evidence ID
    SV-PROV-194
    Requirement
    The durable record surface excludes runtime commands, credentials, clients, processes, and handles.
    Method
    Compare public dataclass field names with a fixed prohibited runtime-state vocabulary.
    Oracle
    The accepted durable-token boundary declares those field names absent.
    Acceptance
    The two name sets are disjoint.
    Interpretation
    A pass confirms this bounded software contract; a failure identifies an implementation, test-input, or contract mismatch.
    Limitations
    Synthetic metadata only; no external execution, numerical verification, scientific validation, UQ, portability, or cross-language claim.
    """
    prohibited = {
        "command",
        "credential",
        "password",
        "token",
        "client",
        "process",
        "handle",
        "scheduler",
    }
    assert {field.name for field in fields(SUT)}.isdisjoint(prohibited)
