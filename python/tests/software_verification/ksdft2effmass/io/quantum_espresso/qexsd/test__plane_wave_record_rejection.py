r"""Software verification of strict plane-wave record rejection.

Evidence profile: routine

Bounded artifact scope: closed serializer and composed record invariants.

Facet and represented meaning

The artifact rejects malformed wire state and inconsistent domain composition.

Intrinsic and cross-object scope

Duplicate/unknown fields, types, values, and reciprocal scales are covered.

VVUQ and scientific exclusions

Rejection behavior is software verification, not scientific validation or UQ.
"""

from __future__ import annotations

import json
from dataclasses import replace

import pytest
from qexsd_fixtures import CONTROLLED_QEXSD, controlled_source_bytes

from ksdft2effmass.io.quantum_espresso.qexsd import (
    ConstructQexsdKohnShamPlaneWaveRecord,
    ParseQexsdDocument,
    QexsdSource,
)
from ksdft2effmass.ksdft.pw import KohnShamPlaneWaveCalculationRecordJsonSerializer

pytestmark = pytest.mark.software_verification


def make_record_text() -> str:
    """Return canonical support text; this helper owns no identifier.

    Evidence ID: Helper owns no identifier.

    Requirement: Support strict rejection tests without owning evidence.

    Acceptance: Return deterministic canonical text.
    """
    digest, count = controlled_source_bytes()
    document = ParseQexsdDocument().execute(
        QexsdSource("/controlled/source.xml", digest, count, CONTROLLED_QEXSD)
    )
    record = ConstructQexsdKohnShamPlaneWaveRecord().execute(document)
    return KohnShamPlaneWaveCalculationRecordJsonSerializer().serialize(record)


def test_artifact__serialization__rejects_duplicate_and_unknown_fields() -> None:
    """Evidence ID: SV-PERIODIC-021

    Requirement: The closed wire contract rejects duplicate and unknown keys.

    Acceptance: Both independently malformed payloads raise ValueError.
    """
    serializer = KohnShamPlaneWaveCalculationRecordJsonSerializer()
    canonical = make_record_text()
    duplicate = canonical.replace(
        '{"exit_status":0', '{"exit_status":0,"exit_status":0', 1
    )
    payload = json.loads(canonical)
    payload["unknown"] = 1
    with pytest.raises(ValueError):
        serializer.deserialize(duplicate)
    with pytest.raises(ValueError):
        serializer.deserialize(json.dumps(payload))


def test_artifact__serialization__rejects_invalid_types_units_and_scales() -> None:
    """Evidence ID: SV-PERIODIC-022

    Requirement: Wrong JSON types, concrete units, and scale flags are rejected.

    Acceptance: Every independently malformed payload raises TypeError or ValueError.
    """
    serializer = KohnShamPlaneWaveCalculationRecordJsonSerializer()
    original = json.loads(make_record_text())
    wrong_type = json.loads(json.dumps(original))
    wrong_type["exit_status"] = True
    wrong_unit = json.loads(json.dumps(original))
    wrong_unit["total_energy"]["unit"] = "rydberg"
    wrong_scale = json.loads(json.dumps(original))
    wrong_scale["reciprocal_lattice"]["incorporates_two_pi"] = False
    with pytest.raises((TypeError, ValueError)):
        serializer.deserialize(json.dumps(wrong_type))
    with pytest.raises((TypeError, ValueError)):
        serializer.deserialize(json.dumps(wrong_unit))
    with pytest.raises((TypeError, ValueError)):
        serializer.deserialize(json.dumps(wrong_scale))


def test_artifact__record_invariants__reject_inconsistent_reciprocal_scale() -> None:
    """Evidence ID: SV-PERIODIC-023

    Requirement: Physical reciprocal vectors must match raw coefficients and scale.

    Acceptance: Replacing one physical vector with a wrong scale raises ValueError.
    """
    serializer = KohnShamPlaneWaveCalculationRecordJsonSerializer()
    record = serializer.deserialize(make_record_text())
    with pytest.raises(ValueError):
        replace(
            record.reciprocal_lattice,
            physical_vectors=((1.0, 0.0, 0.0),)
            + record.reciprocal_lattice.physical_vectors[1:],
        )
