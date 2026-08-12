r"""Software verification of ``PeriodicCalculationRecordJsonSerializer``.

Evidence profile: routine

Bounded artifact scope: closed canonical periodic-record JSON version 1.

Facet and represented meaning

The serializer owns canonical wire bytes, strict decoding, and round trips.

Intrinsic and cross-object scope

Wire behavior and record invariants are covered separately from XML.

VVUQ and scientific exclusions

Serialization success establishes no physical or scientific validity.
"""

import json

import pytest
from qexsd_fixtures import CONTROLLED_QEXSD, controlled_source_bytes

from ksdft2effmass.periodic import (
    ConstructPeriodicCalculationRecord,
    ParseQexsdDocument,
    PeriodicCalculationRecordJsonSerializer,
    QexsdSource,
)

SUT = PeriodicCalculationRecordJsonSerializer
pytestmark = pytest.mark.software_verification


def make_record():
    """Construct controlled valid semantic state for wire evidence.

    Evidence ID: Helper owns no identifier.

    Requirement: Support the named tests without owning evidence.

    Acceptance: Return deterministic controlled support data.
    """
    digest, count = controlled_source_bytes()
    document = ParseQexsdDocument().execute(
        QexsdSource("/controlled/source.xml", digest, count, CONTROLLED_QEXSD)
    )
    return ConstructPeriodicCalculationRecord().execute(document)


def test_method__serialize__is_canonical_exact_and_deterministic() -> None:
    """Evidence ID: SV-PERIODIC-015

    Requirement: Canonical JSON has sorted compact keys, one newline, and exact
    round trip.

    Acceptance: Repeated text is byte-identical, canonical, and reconstructs equal
    immutable state.
    """
    serializer = PeriodicCalculationRecordJsonSerializer()
    record = make_record()
    first = serializer.serialize(record)
    second = serializer.serialize(record)
    assert first == second
    assert first.endswith("\n") and not first.endswith("\n\n")
    assert (
        json.dumps(json.loads(first), separators=(",", ":"), sort_keys=True) + "\n"
        == first
    )
    assert serializer.deserialize(first) == record
    assert serializer.serialize(serializer.deserialize(first)) == first


@pytest.mark.parametrize(
    "text",
    [
        pytest.param('{"schema_version":1,"schema_version":1}', id="duplicate_key"),
        pytest.param('{"schema_version":1,"unknown":0}', id="unknown_field"),
        pytest.param('{"schema_version":NaN}', id="nonfinite_constant"),
        pytest.param("[]", id="nonobject_root"),
    ],
)
def test_method__deserialize__rejects_noncanonical_or_open_payloads(text: str) -> None:
    """Evidence ID: SV-PERIODIC-016

    Requirement: Duplicate, unknown, nonfinite, and wrong-root JSON fails closed.

    Acceptance: Every named invalid wire partition raises TypeError or ValueError.
    """
    with pytest.raises((TypeError, ValueError)):
        PeriodicCalculationRecordJsonSerializer().deserialize(text)


def test_method__deserialize__rejects_unknown_nested_semantics() -> None:
    """Evidence ID: SV-PERIODIC-017

    Requirement: The closed schema rejects invalid typed unavailable values.

    Acceptance: Replacing a valid reason with unknown text raises ValueError.
    """
    serializer = PeriodicCalculationRecordJsonSerializer()
    payload = json.loads(serializer.serialize(make_record()))
    payload["gauge"] = "unknown"
    with pytest.raises(ValueError):
        serializer.deserialize(json.dumps(payload))
