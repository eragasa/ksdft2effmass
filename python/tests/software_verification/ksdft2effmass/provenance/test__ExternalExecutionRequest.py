r"""Software verification of ``ExternalExecutionRequest``.

Facet and represented meaning
-----------------------------
This class-owned evidence verifies request field mapping, optional retry lineage, canonical tuples, strict rejection, durable boundaries, immutability, and equality..

Intrinsic and cross-object scope
--------------------------------
The sole primary SUT is ``ExternalExecutionRequest``; collaborators only supply public constructor
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

from ksdft2effmass.provenance import ExternalExecutionRequest

SUT = ExternalExecutionRequest
pytestmark = pytest.mark.software_verification


def test_constructor__field_mapping__stores_exact_request_payload() -> None:
    """Evidence ID
    SV-PROV-037
    Requirement
    Request construction stores all eleven exact immutable intent fields.
    Method
    Construct fixed separately authorized synthetic request metadata.
    Oracle
    The public signature and literals define exact field order and values.
    Acceptance
    All fields match exactly, including absent retry parent and canonical tuples.
    Interpretation
    A pass confirms this bounded software contract; a failure identifies an implementation, test-input, or contract mismatch.
    Limitations
    Synthetic metadata only; no external execution, numerical verification, scientific validation, UQ, portability, or cross-language claim.
    """
    record = SUT(
        "request-1",
        "corr-1",
        "attempt-1",
        None,
        "qe",
        "cap-1",
        "install-1",
        "auth-1",
        ("input-1", "input-2"),
        ("log", "output"),
        "prov-1",
    )
    assert tuple(f.name for f in fields(record)) == (
        "request_id",
        "correlation_id",
        "attempt_id",
        "retry_parent_request_id",
        "tool_id",
        "capability_id",
        "installation_id",
        "authorization_id",
        "input_artifact_ids",
        "expected_output_roles",
        "provenance_id",
    )
    assert astuple(record) == (
        "request-1",
        "corr-1",
        "attempt-1",
        None,
        "qe",
        "cap-1",
        "install-1",
        "auth-1",
        ("input-1", "input-2"),
        ("log", "output"),
        "prov-1",
    )
    assert type(record.input_artifact_ids) is tuple
    assert type(record.expected_output_roles) is tuple


@pytest.mark.parametrize(
    ("parent", "case_id"),
    [
        pytest.param(None, "absent", id="absent_retry_parent"),
        pytest.param("request-0", "present", id="distinct_retry_parent"),
    ],
)
def test_constructor__retry_parent__accepts_optional_distinct_states(
    parent: str | None, case_id: str
) -> None:
    """Evidence ID
    SV-PROV-078
    Requirement
    Retry lineage accepts absent or a distinct valid prior request identity.
    Method
    Construct explicit absent and present optional states.
    Oracle
    The accepted lineage relation allows None or a distinct portable identifier.
    Acceptance
    The selected parent is stored exactly.
    Interpretation
    A pass confirms this bounded software contract; a failure identifies an implementation, test-input, or contract mismatch.
    Limitations
    Synthetic metadata only; no external execution, numerical verification, scientific validation, UQ, portability, or cross-language claim.
    """
    record = SUT(
        "request-1",
        "corr-1",
        "attempt-1",
        parent,
        "qe",
        "cap-1",
        "install-1",
        "auth-1",
        (),
        (),
        "prov-1",
    )
    assert record.retry_parent_request_id == parent


def test_constructor__retry_parent__rejects_self_reference() -> None:
    """Evidence ID
    SV-PROV-217
    Requirement
    A retry request cannot name itself as its parent.
    Method
    Construct with identical request and retry-parent identities.
    Oracle
    The accepted irreflexive lineage invariant requires distinct values.
    Acceptance
    Construction raises ValueError.
    Interpretation
    A pass confirms this bounded software contract; a failure identifies an implementation, test-input, or contract mismatch.
    Limitations
    Synthetic metadata only; no external execution, numerical verification, scientific validation, UQ, portability, or cross-language claim.
    """
    with pytest.raises(ValueError):
        SUT(
            "request-1",
            "corr-1",
            "attempt-1",
            "request-1",
            "qe",
            "cap-1",
            "install-1",
            "auth-1",
            (),
            (),
            "prov-1",
        )


@pytest.mark.parametrize(
    ("field_name", "value"),
    [
        pytest.param("input_artifact_ids", (), id="empty_inputs"),
        pytest.param("expected_output_roles", (), id="empty_roles"),
        pytest.param("input_artifact_ids", ("a", "b"), id="sorted_inputs"),
        pytest.param("expected_output_roles", ("a", "b"), id="sorted_roles"),
    ],
)
def test_constructor__identifier_collections__accepts_canonical_tuples(
    field_name: str, value: tuple[str, ...]
) -> None:
    """Evidence ID
    SV-PROV-038
    Requirement
    Request identifier collections accept empty or sorted unique tuples.
    Method
    Replace one collection with explicit canonical cardinality partitions.
    Oracle
    The accepted canonical tuple invariant supplies expected state.
    Acceptance
    The selected tuple is preserved exactly.
    Interpretation
    A pass confirms this bounded software contract; a failure identifies an implementation, test-input, or contract mismatch.
    Limitations
    Synthetic metadata only; no external execution, numerical verification, scientific validation, UQ, portability, or cross-language claim.
    """
    kwargs: dict[str, Any] = {
        "request_id": "request-1",
        "correlation_id": "corr-1",
        "attempt_id": "attempt-1",
        "retry_parent_request_id": None,
        "tool_id": "qe",
        "capability_id": "cap-1",
        "installation_id": "install-1",
        "authorization_id": "auth-1",
        "input_artifact_ids": (),
        "expected_output_roles": (),
        "provenance_id": "prov-1",
    }
    kwargs[field_name] = value
    assert getattr(SUT(**kwargs), field_name) == value


@pytest.mark.parametrize(
    ("field_name", "value", "error"),
    [
        pytest.param("input_artifact_ids", ["a"], TypeError, id="inputs_list"),
        pytest.param(
            "expected_output_roles", (1,), TypeError, id="roles_integer_member"
        ),
        pytest.param(
            "input_artifact_ids", ("b", "a"), ValueError, id="inputs_reverse_order"
        ),
        pytest.param(
            "expected_output_roles", ("a", "a"), ValueError, id="roles_duplicate"
        ),
    ],
)
def test_constructor__identifier_collections__rejects_noncanonical_state(
    field_name: str, value: object, error: type[Exception]
) -> None:
    """Evidence ID
    SV-PROV-218
    Requirement
    Request collections require built-in tuples of valid unique sorted strings.
    Method
    Exercise explicit container, member, ordering, and duplicate partitions.
    Oracle
    The accepted type and canonical relation contracts determine exception classes.
    Acceptance
    Each partition raises its exact declared exception.
    Interpretation
    A pass confirms this bounded software contract; a failure identifies an implementation, test-input, or contract mismatch.
    Limitations
    Synthetic metadata only; no external execution, numerical verification, scientific validation, UQ, portability, or cross-language claim.
    """
    kwargs: dict[str, Any] = {
        "request_id": "request-1",
        "correlation_id": "corr-1",
        "attempt_id": "attempt-1",
        "retry_parent_request_id": None,
        "tool_id": "qe",
        "capability_id": "cap-1",
        "installation_id": "install-1",
        "authorization_id": "auth-1",
        "input_artifact_ids": (),
        "expected_output_roles": (),
        "provenance_id": "prov-1",
    }
    kwargs[field_name] = value
    with pytest.raises(error):
        SUT(**kwargs)


def test_constructor__identifier_type_and_value__reject_invalid_state() -> None:
    """Evidence ID
    SV-PROV-219
    Requirement
    Required request identifiers are exact portable built-in strings.
    Method
    Construct a bytes request ID and embedded-space request ID.
    Oracle
    The accepted type and lexical grammar define TypeError and ValueError boundaries.
    Acceptance
    Wrong type and malformed value raise their exact exceptions.
    Interpretation
    A pass confirms this bounded software contract; a failure identifies an implementation, test-input, or contract mismatch.
    Limitations
    Synthetic metadata only; no external execution, numerical verification, scientific validation, UQ, portability, or cross-language claim.
    """
    with pytest.raises(TypeError):
        SUT(
            cast(Any, b"request"),
            "corr-1",
            "attempt-1",
            None,
            "qe",
            "cap-1",
            "install-1",
            "auth-1",
            (),
            (),
            "prov-1",
        )
    with pytest.raises(ValueError):
        SUT(
            "bad id",
            "corr-1",
            "attempt-1",
            None,
            "qe",
            "cap-1",
            "install-1",
            "auth-1",
            (),
            (),
            "prov-1",
        )


def test_field__durable_payload__excludes_runtime_credentials_and_handles() -> None:
    """Evidence ID
    SV-PROV-039
    Requirement
    Durable requests contain authorization identity but no command, credential, client, process, scheduler, or handle.
    Method
    Inspect the public field inventory against fixed prohibited runtime names.
    Oracle
    The accepted durable boundary explicitly excludes runtime state.
    Acceptance
    The name sets are disjoint while authorization_id remains present.
    Interpretation
    A pass confirms this bounded software contract; a failure identifies an implementation, test-input, or contract mismatch.
    Limitations
    Synthetic metadata only; no external execution, numerical verification, scientific validation, UQ, portability, or cross-language claim.
    """
    names = {f.name for f in fields(SUT)}
    assert "authorization_id" in names
    assert names.isdisjoint(
        {
            "command",
            "credential",
            "password",
            "token",
            "client",
            "process",
            "scheduler",
            "handle",
        }
    )


def test_field__frozen_assignment__rejects_reassignment() -> None:
    """Evidence ID
    SV-PROV-220
    Requirement
    Execution requests are frozen.
    Method
    Attempt request_id assignment after construction.
    Oracle
    Frozen dataclass semantics are the oracle.
    Acceptance
    FrozenInstanceError is raised.
    Interpretation
    A pass confirms this bounded software contract; a failure identifies an implementation, test-input, or contract mismatch.
    Limitations
    Synthetic metadata only; no external execution, numerical verification, scientific validation, UQ, portability, or cross-language claim.
    """
    record = SUT(
        "request-1",
        "corr-1",
        "attempt-1",
        None,
        "qe",
        "cap-1",
        "install-1",
        "auth-1",
        ("input-1", "input-2"),
        ("log", "output"),
        "prov-1",
    )
    with pytest.raises(FrozenInstanceError):
        field_name = "request_id"
        setattr(record, field_name, "request-2")


def test_method__eq__compares_complete_represented_state() -> None:
    """Evidence ID
    SV-PROV-221
    Requirement
    Equality covers all request fields including optional lineage and tuples.
    Method
    Compare identical records and a record differing in retry parent.
    Oracle
    Dataclass full-state equality determines the result.
    Acceptance
    Complete state compares equal and one-field difference compares unequal.
    Interpretation
    A pass confirms this bounded software contract; a failure identifies an implementation, test-input, or contract mismatch.
    Limitations
    Synthetic metadata only; no external execution, numerical verification, scientific validation, UQ, portability, or cross-language claim.
    """
    record = SUT(
        "request-1",
        "corr-1",
        "attempt-1",
        None,
        "qe",
        "cap-1",
        "install-1",
        "auth-1",
        ("input-1", "input-2"),
        ("log", "output"),
        "prov-1",
    )
    assert record == SUT(
        "request-1",
        "corr-1",
        "attempt-1",
        None,
        "qe",
        "cap-1",
        "install-1",
        "auth-1",
        ("input-1", "input-2"),
        ("log", "output"),
        "prov-1",
    )
    assert record != SUT(
        "request-1",
        "corr-1",
        "attempt-1",
        "request-0",
        "qe",
        "cap-1",
        "install-1",
        "auth-1",
        ("input-1", "input-2"),
        ("log", "output"),
        "prov-1",
    )
