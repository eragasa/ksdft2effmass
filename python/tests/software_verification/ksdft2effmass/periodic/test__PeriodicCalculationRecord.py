r"""Software verification of ``PeriodicCalculationRecord``.

Evidence profile: routine

Bounded artifact scope: immutable semantic periodic calculation observation.

Facet and represented meaning

The record owns dimensions, ordering, provenance, units, and typed absence.

Intrinsic and cross-object scope

Only record construction and immutable value semantics are verified.

VVUQ and scientific exclusions

A valid record establishes no convergence or scientific acceptance.
"""

from dataclasses import FrozenInstanceError, replace

import pytest
from qexsd_fixtures import CONTROLLED_QEXSD, controlled_source_bytes

from ksdft2effmass.periodic import (
    ConstructPeriodicCalculationRecord,
    ParseQexsdDocument,
    PeriodicCalculationRecord,
    QexsdSource,
)

SUT = PeriodicCalculationRecord
pytestmark = pytest.mark.software_verification


def make_record() -> PeriodicCalculationRecord:
    """Construct a semantic record from controlled mechanical input.

    Evidence ID: Helper owns no identifier.

    Requirement: Support the named tests without owning evidence.

    Acceptance: Return deterministic controlled support data.
    """
    digest, count = controlled_source_bytes()
    document = ParseQexsdDocument().execute(
        QexsdSource("/controlled/source.xml", digest, count, CONTROLLED_QEXSD)
    )
    return ConstructPeriodicCalculationRecord().execute(document)


def test_constructor__complete_state__is_deeply_immutable_and_xml_free() -> None:
    """Evidence ID: SV-PERIODIC-012

    Requirement: Semantic state is tuple-backed, frozen, and exposes no XML values.

    Acceptance: Nested arrays are tuples, reassignment fails, and field values have
    no XML types.
    """
    record = make_record()
    assert type(record.k_points) is tuple and type(record.k_points[0]) is tuple
    assert type(record.eigenvalues) is tuple
    assert (
        all("Element" not in type(value).__name__ for value in record.__dict__.values())
        if hasattr(record, "__dict__")
        else True
    )
    with pytest.raises(FrozenInstanceError):
        record.total_energy = 0.0  # type: ignore[misc]


@pytest.mark.parametrize(
    "changes",
    [
        pytest.param({"schema_version": 2}, id="unsupported_schema"),
        pytest.param({"atom_count": 3}, id="atom_count"),
        pytest.param({"band_count": 3}, id="band_count"),
        pytest.param({"k_point_count": 3}, id="kpoint_count"),
        pytest.param({"fft_box": (0, 5, 6)}, id="fft_grid"),
        pytest.param(
            {"absolute_energy_reference": "unknown"}, id="untyped_unavailable"
        ),
    ],
)
def test_constructor__semantic_invariants__rejects_invalid_state(
    changes: dict[str, object],
) -> None:
    """Evidence ID: SV-PERIODIC-013

    Requirement: Schema, cardinality, grid, and unavailable-state contracts are closed.

    Acceptance: Every invalid named replacement raises TypeError or ValueError.
    """
    with pytest.raises((TypeError, ValueError)):
        replace(make_record(), **changes)  # type: ignore[arg-type]
