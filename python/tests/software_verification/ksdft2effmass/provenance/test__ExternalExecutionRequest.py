"""Evidence class and represented meaning
Software verification of immutable authorized external-execution requests.
Owned contract, oracle, and scope
ExternalExecutionRequest is the SUT; attempt/retry correlation, canonical tuples, and
safe payload exclusion are the oracle.
VVUQ and scientific exclusions
Evidence performs no execution and excludes numerical verification, scientific
validation, UQ, authorization truth, and cross-language conformance.
"""

from dataclasses import FrozenInstanceError, fields

import pytest

from ksdft2effmass.provenance import ExternalExecutionRequest

SUT = ExternalExecutionRequest
pytestmark = pytest.mark.software_verification


def _request(**changes: object) -> ExternalExecutionRequest:
    """Evidence ID
    Supports SV-PROV-037 through SV-PROV-039 and SV-PROV-078; owns no identifier.
    Requirement
    Provide explicit valid synthetic request fields.
    Method
    Merge named changes into visible safe defaults.
    Oracle
    Defaults independently satisfy the public corrected constructor.
    Acceptance
    Construction succeeds without I/O.
    Interpretation
    Helper failure is setup failure only.
    Limitations
    Identifiers convey no actual authorization.
    """
    values: dict[str, object] = {
        "request_id": "request-1",
        "correlation_id": "correlation-1",
        "attempt_id": "attempt-1",
        "retry_parent_request_id": None,
        "tool_id": "qe",
        "capability_id": "cap-1",
        "installation_id": "install-1",
        "authorization_id": "auth-1",
        "input_artifact_ids": ("input-a",),
        "expected_output_roles": ("output",),
        "provenance_id": "prov-1",
    }
    values.update(changes)
    return SUT(**values)  # type: ignore[arg-type]


def test_constructor__request_fields__maps_attempt_and_safe_immutable_payload() -> None:
    """Evidence ID
    SV-PROV-037
    Requirement
    Request, correlation, attempt, optional retry parent, tool, authorization,
    artifacts, roles, and provenance map exactly.
    Method
    Construct a root attempt, inspect correlation fields, and attempt reassignment.
    Oracle
    The corrected eleven-field request vocabulary fixes exact values.
    Acceptance
    Values equal inputs and reassignment raises FrozenInstanceError.
    Interpretation
    Failure indicates correlation mapping or immutability drift.
    Limitations
    No adapter or external operation is invoked.
    """
    value = _request()
    assert (
        value.request_id,
        value.correlation_id,
        value.attempt_id,
        value.retry_parent_request_id,
    ) == ("request-1", "correlation-1", "attempt-1", None)
    with pytest.raises(FrozenInstanceError):
        value.authorization_id = "other"  # type: ignore[misc]


def test_constructor__identifier_collections__rejects_noncanonical_forms() -> None:
    """Evidence ID
    SV-PROV-038
    Requirement
    Input artifacts and output roles are built-in sorted unique identifier tuples.
    Method
    Pass a list, unsorted tuple, and duplicate tuple.
    Oracle
    The canonical tuple contract fixes each invalid partition.
    Acceptance
    List raises TypeError; unsorted and duplicate tuples raise ValueError.
    Interpretation
    Failure indicates mutable or nondeterministic request payloads.
    Limitations
    Cross-record existence is excluded.
    """
    with pytest.raises(TypeError):
        _request(input_artifact_ids=["x"])
    with pytest.raises(ValueError):
        _request(expected_output_roles=("z", "a"))
    with pytest.raises(ValueError):
        _request(input_artifact_ids=("a", "a"))


def test_field__durable_payload__excludes_credentials_and_raw_runtime_channels() -> (
    None
):
    """Evidence ID
    SV-PROV-039
    Requirement
    Durable requests expose only stable identifiers/tuples, never credentials, commands,
    raw arguments/environment, clients, handles, schedulers, or backends.
    Method
    Compare the complete dataclass field inventory with the corrected fixed vocabulary
    and scan forbidden fragments.
    Oracle
    The human-approved durable-token boundary fixes all eleven allowed fields.
    Acceptance
    Field names match exactly and contain no forbidden fragment.
    Interpretation
    Failure indicates protected runtime responsibility leakage.
    Limitations
    Referenced authorization/provenance records are not dereferenced.
    """
    names = tuple(field.name for field in fields(SUT))
    assert names == (
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
    forbidden = (
        "credential",
        "password",
        "secret",
        "command",
        "argument",
        "environment",
        "client",
        "handle",
        "scheduler",
        "backend",
        "message",
        "detail",
    )
    assert not any(fragment in name for name in names for fragment in forbidden)


def test_constructor__retry_parent__requires_distinct_valid_request_identity() -> None:
    """Evidence ID
    SV-PROV-078
    Requirement
    A retry is a new request whose optional parent is a distinct portable request
    identity.
    Method
    Construct a valid child, then pass self-parent, empty, and wrong-type parent values.
    Oracle
    The accepted retry-lineage invariant fixes the valid/invalid partition.
    Acceptance
    Distinct parent is retained; self/empty raise ValueError and wrong type raises
    TypeError.
    Interpretation
    Failure indicates ambiguous retry lineage or unintended coercion.
    Limitations
    Parent existence, failure status, and authorization are relational concerns outside
    construction.
    """
    assert (
        _request(
            request_id="request-2",
            attempt_id="attempt-2",
            retry_parent_request_id="request-1",
        ).retry_parent_request_id
        == "request-1"
    )
    with pytest.raises(ValueError):
        _request(retry_parent_request_id="request-1")
    with pytest.raises(ValueError):
        _request(retry_parent_request_id="")
    with pytest.raises(TypeError):
        _request(retry_parent_request_id=1)
