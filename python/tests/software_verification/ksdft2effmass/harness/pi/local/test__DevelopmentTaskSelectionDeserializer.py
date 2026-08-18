r"""Software verification of ``DevelopmentTaskSelectionDeserializer``.

Evidence profile: claim_bearing

Bounded artifact scope: the module's declared evidence owner.

Facet and represented meaning

The module verifies strict decoding of version-1 Task selection JSON.

Intrinsic and cross-object scope

The sole primary SUT is ``DevelopmentTaskSelectionDeserializer``. UTF-8, JSON,
closed-key, array, and intrinsic selection-state validation are covered.

VVUQ and scientific exclusions

Passing establishes deserialization software behavior only. It grants no Task or
protected authority and interprets no scientific workflow state.
"""

import pytest

from ksdft2effmass.harness import (
    DevelopmentTaskSelection,
    DevelopmentTaskSelectionDeserializer,
    DevelopmentTaskSelectionSerializer,
)

pytestmark = pytest.mark.software_verification
SUT = DevelopmentTaskSelectionDeserializer


def test_method__execute__round_trips_canonical_state() -> None:
    """Evidence ID: SV-HT-109

    Requirement: Strict deserialization reconstructs the exact canonical selection
    value.

    Method: Serialize then deserialize one active-reference value.

    Oracle: Public DataObject equality and serializer bytes independently fix the
    represented state.

    Acceptance: The decoded value equals the original exact DataObject.

    Interpretation: Failure identifies field mapping or type drift.

    Limitations: Round-trip agreement does not validate referenced identities.
    """
    expected = DevelopmentTaskSelection(
        1, "task.active", ("receipt.a", "receipt.b"), False
    )
    payload = DevelopmentTaskSelectionSerializer().execute(expected)
    assert SUT().execute(payload) == expected


@pytest.mark.parametrize(
    "payload",
    (
        pytest.param(b"\xff", id="invalid_utf8"),
        pytest.param(b"{", id="invalid_json"),
        pytest.param(
            b'{"schema_version":1,"schema_version":1}',
            id="duplicate_object_key",
        ),
        pytest.param(b'{"schema_version":1}', id="missing_required_fields"),
        pytest.param(
            b'{"schema_version":1,"active_task_id":null,'
            b'"explicit_activation_receipt_ids":[],'
            b'"automatic_successor_activation":false,"task_sequence":[]}',
            id="unknown_topology_field",
        ),
    ),
)
def test_method__execute__rejects_malformed_duplicate_and_unknown_keys(
    payload: bytes,
) -> None:
    """Evidence ID: SV-HT-110

    Requirement: Invalid UTF-8/JSON, duplicate keys, missing fields, and unknown fields
    fail closed.

    Method: Decode one independently malformed payload per closed-wire boundary.

    Oracle: The strict deserializer contract fixes complete key closure and unique JSON
    object members.

    Acceptance: Every payload raises ``ValueError`` and produces no DataObject.

    Interpretation: Failure identifies permissive or ambiguous decoding.

    Limitations: JSON Schema behavior is separately covered by artifact evidence.
    """
    with pytest.raises(ValueError):
        SUT().execute(payload)


def test_method__execute__rejects_wrong_array_and_intrinsic_values() -> None:
    """Evidence ID: SV-HT-111

    Requirement: Receipt arrays retain exact JSON type and intrinsic ordering while
    automatic successor activation remains disabled.

    Method: Decode a non-array receipt value, unordered receipts, and enabled policy.

    Oracle: The schema and DataObject constructor contracts fix these independent
    boundaries.

    Acceptance: Wrong JSON type raises ``TypeError``; ordering and policy raise
    ``ValueError``.

    Interpretation: Failure identifies wire coercion or invariant bypass.

    Limitations: Receipt existence and authority are not interpreted.
    """
    with pytest.raises(TypeError, match="JSON array"):
        SUT().execute(
            b'{"schema_version":1,"active_task_id":null,'
            b'"explicit_activation_receipt_ids":{},'
            b'"automatic_successor_activation":false}'
        )
    with pytest.raises(ValueError, match="unique and strictly sorted"):
        SUT().execute(
            b'{"schema_version":1,"active_task_id":null,'
            b'"explicit_activation_receipt_ids":["receipt.b","receipt.a"],'
            b'"automatic_successor_activation":false}'
        )
    with pytest.raises(ValueError, match="must be false"):
        SUT().execute(
            b'{"schema_version":1,"active_task_id":null,'
            b'"explicit_activation_receipt_ids":[],'
            b'"automatic_successor_activation":true}'
        )
