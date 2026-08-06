r"""Software verification of ``InstallationObservation``.

Facet and represented meaning
-----------------------------
This class-owned evidence verifies installation field mapping, optional digest states, lifecycle separation, strict rejection, immutability, and equality..

Intrinsic and cross-object scope
--------------------------------
The sole primary SUT is ``InstallationObservation``; collaborators only supply public constructor
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

from ksdft2effmass.provenance import InstallationObservation

SUT = InstallationObservation
pytestmark = pytest.mark.software_verification


def test_constructor__field_mapping__stores_exact_installation_metadata() -> None:
    """Evidence ID
    SV-PROV-031
    Requirement
    Installation observation stores all eight exact fields with optional digest state.
    Method
    Construct fixed already-observed metadata with absent digest.
    Oracle
    The public signature and literals define exact mapping and types.
    Acceptance
    Field names and values match exactly, including None.
    Interpretation
    A pass confirms this bounded software contract; a failure identifies an implementation, test-input, or contract mismatch.
    Limitations
    Synthetic metadata only; no external execution, numerical verification, scientific validation, UQ, portability, or cross-language claim.
    """
    record = SUT("install-1", "spec-1", "qe", "7.4", "pw.x", None, "env-1", "prov-1")
    assert tuple(f.name for f in fields(record)) == (
        "installation_id",
        "specification_id",
        "tool_id",
        "observed_version",
        "executable_or_package_id",
        "executable_sha256",
        "environment_record_id",
        "provenance_id",
    )
    assert astuple(record) == (
        "install-1",
        "spec-1",
        "qe",
        "7.4",
        "pw.x",
        None,
        "env-1",
        "prov-1",
    )


def test_field__lifecycle_boundary__excludes_capability_verification_status() -> None:
    """Evidence ID
    SV-PROV-032
    Requirement
    Installation observation remains distinct from capability verification.
    Method
    Inspect its public field inventory.
    Oracle
    The accepted lifecycle separates installation metadata from capability_id and status.
    Acceptance
    Neither verification field is present.
    Interpretation
    A pass confirms this bounded software contract; a failure identifies an implementation, test-input, or contract mismatch.
    Limitations
    Synthetic metadata only; no external execution, numerical verification, scientific validation, UQ, portability, or cross-language claim.
    """
    assert {f.name for f in fields(SUT)}.isdisjoint({"capability_id", "status"})


@pytest.mark.parametrize(
    "digest",
    [
        pytest.param(None, id="absent_digest"),
        pytest.param("a" * 64, id="present_lowercase_sha256"),
    ],
)
def test_constructor__optional_digest__accepts_declared_states(
    digest: str | None,
) -> None:
    """Evidence ID
    SV-PROV-033
    Requirement
    Executable digest accepts exactly absent or valid lowercase SHA-256 states.
    Method
    Construct one absent and one present valid state with explicit IDs.
    Oracle
    None and a 64-character lowercase hexadecimal literal are accepted states.
    Acceptance
    Construction preserves the selected digest exactly.
    Interpretation
    A pass confirms this bounded software contract; a failure identifies an implementation, test-input, or contract mismatch.
    Limitations
    Synthetic metadata only; no external execution, numerical verification, scientific validation, UQ, portability, or cross-language claim.
    """
    record = SUT(
        "install-1", "spec-1", "qe", "7.4", "pw.x", cast(Any, digest), "env-1", "prov-1"
    )
    assert record.executable_sha256 == digest


@pytest.mark.parametrize(
    "digest",
    [
        pytest.param(1, id="integer_wrong_type"),
        pytest.param("A" * 64, id="uppercase_digest"),
        pytest.param("a" * 63, id="short_digest"),
    ],
)
def test_constructor__optional_digest__rejects_wrong_type_or_value(
    digest: object,
) -> None:
    """Evidence ID
    SV-PROV-205
    Requirement
    Present executable digest must be a built-in string matching lowercase SHA-256 grammar.
    Method
    Construct with explicit wrong-type, uppercase, and short partitions.
    Oracle
    The accepted digest grammar and exception taxonomy determine rejection.
    Acceptance
    Wrong type raises TypeError; malformed strings raise ValueError.
    Interpretation
    A pass confirms this bounded software contract; a failure identifies an implementation, test-input, or contract mismatch.
    Limitations
    Synthetic metadata only; no external execution, numerical verification, scientific validation, UQ, portability, or cross-language claim.
    """
    error = TypeError if type(digest) is not str else ValueError
    with pytest.raises(error):
        SUT(
            "install-1",
            "spec-1",
            "qe",
            "7.4",
            "pw.x",
            cast(Any, digest),
            "env-1",
            "prov-1",
        )


def test_constructor__identifier_and_version_boundaries__reject_invalid_values() -> (
    None
):
    """Evidence ID
    SV-PROV-206
    Requirement
    Identifier and version fields enforce their distinct portable grammars.
    Method
    Construct once with an invalid identifier and once with invalid leading-hyphen version.
    Oracle
    The accepted grammars exclude spaces and require an alphanumeric version prefix.
    Acceptance
    Both constructions raise ValueError.
    Interpretation
    A pass confirms this bounded software contract; a failure identifies an implementation, test-input, or contract mismatch.
    Limitations
    Synthetic metadata only; no external execution, numerical verification, scientific validation, UQ, portability, or cross-language claim.
    """
    with pytest.raises(ValueError):
        SUT("bad id", "spec-1", "qe", "7.4", "pw.x", None, "env-1", "prov-1")
    with pytest.raises(ValueError):
        SUT("install-1", "spec-1", "qe", "-7.4", "pw.x", None, "env-1", "prov-1")


def test_constructor__text_semantic_type__rejects_non_string() -> None:
    """Evidence ID
    SV-PROV-207
    Requirement
    Required installation textual fields reject non-string values.
    Method
    Pass bytes as installation_id with other state valid.
    Oracle
    The exact type contract requires built-in str.
    Acceptance
    Construction raises TypeError.
    Interpretation
    A pass confirms this bounded software contract; a failure identifies an implementation, test-input, or contract mismatch.
    Limitations
    Synthetic metadata only; no external execution, numerical verification, scientific validation, UQ, portability, or cross-language claim.
    """
    with pytest.raises(TypeError):
        SUT(
            cast(Any, b"install"),
            "spec-1",
            "qe",
            "7.4",
            "pw.x",
            None,
            "env-1",
            "prov-1",
        )


def test_field__frozen_assignment__rejects_reassignment() -> None:
    """Evidence ID
    SV-PROV-208
    Requirement
    Installation observations are frozen.
    Method
    Assign observed_version after construction.
    Oracle
    Frozen dataclass semantics are the oracle.
    Acceptance
    FrozenInstanceError is raised.
    Interpretation
    A pass confirms this bounded software contract; a failure identifies an implementation, test-input, or contract mismatch.
    Limitations
    Synthetic metadata only; no external execution, numerical verification, scientific validation, UQ, portability, or cross-language claim.
    """
    record = SUT("install-1", "spec-1", "qe", "7.4", "pw.x", None, "env-1", "prov-1")
    with pytest.raises(FrozenInstanceError):
        field_name = "observed_version"
        setattr(record, field_name, "8.0")


def test_method__eq__compares_complete_represented_state() -> None:
    """Evidence ID
    SV-PROV-209
    Requirement
    Equality covers complete installation state including optional digest.
    Method
    Compare identical absent-digest records and a present-digest record.
    Oracle
    Dataclass complete-state equality defines the result.
    Acceptance
    Identical records compare equal and digest-different records compare unequal.
    Interpretation
    A pass confirms this bounded software contract; a failure identifies an implementation, test-input, or contract mismatch.
    Limitations
    Synthetic metadata only; no external execution, numerical verification, scientific validation, UQ, portability, or cross-language claim.
    """
    record = SUT("install-1", "spec-1", "qe", "7.4", "pw.x", None, "env-1", "prov-1")
    assert record == SUT(
        "install-1", "spec-1", "qe", "7.4", "pw.x", None, "env-1", "prov-1"
    )
    assert record != SUT(
        "install-1", "spec-1", "qe", "7.4", "pw.x", "a" * 64, "env-1", "prov-1"
    )


def test_field__durable_surface__excludes_runtime_credentials_and_handles() -> None:
    """Evidence ID
    SV-PROV-210
    Requirement
    Installation metadata stores no runtime or credential handles.
    Method
    Inspect field names against prohibited runtime state.
    Oracle
    The accepted durable boundary excludes command, credential, client, process, and handle.
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
