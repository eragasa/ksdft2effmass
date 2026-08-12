r"""Software verification of ``ConstructPeriodicCalculationRecord``.

Evidence profile: routine

Bounded artifact scope: native-QEXSD to semantic periodic-record construction.

Facet and represented meaning

The ActionObject preserves values and makes absent semantics explicit.

Intrinsic and cross-object scope

This is the semantic cross-object boundary; XML behavior is excluded.

VVUQ and scientific exclusions

Exact mapping establishes no numerical or scientific validation.
"""

import inspect

import pytest
from qexsd_fixtures import CONTROLLED_QEXSD, controlled_source_bytes

from ksdft2effmass.periodic import (
    ConstructPeriodicCalculationRecord,
    ParseQexsdDocument,
    QexsdSource,
    UnavailableReason,
)

SUT = ConstructPeriodicCalculationRecord
pytestmark = pytest.mark.software_verification


def test_method__execute__preserves_values_and_unavailable_semantics() -> None:
    """Evidence ID: SV-PERIODIC-009

    Requirement: Semantic construction preserves order, units, provenance, and typed
    absence.

    Acceptance: Every represented mapping and required unavailable field is exact.
    """
    digest, count = controlled_source_bytes()
    document = ParseQexsdDocument().execute(
        QexsdSource("/controlled/source.xml", digest, count, CONTROLLED_QEXSD)
    )
    record = ConstructPeriodicCalculationRecord().execute(document)
    assert record.source_sha256 == document.source_sha256
    assert record.direct_lattice_vectors == document.direct_lattice_vectors
    assert record.k_points == document.k_points
    assert record.k_point_weights == document.k_point_weights
    assert record.eigenvalues == document.eigenvalues
    assert record.total_energy == -1.25
    assert record.energy_unit == "Hartree atomic units"
    assert (
        record.absolute_energy_reference is UnavailableReason.NOT_REPRESENTED_IN_QEXSD
    )
    assert record.retained_subspace is UnavailableReason.NO_RETAINED_SUBSPACE
    assert record.spin_convention is UnavailableReason.NO_SPIN_RESOLVED_ARRAYS


def test_artifact__semantic_dependency__contains_no_xml_behavior() -> None:
    """Evidence ID: SV-PERIODIC-010

    Requirement: Semantic construction contains no XML parser types or imports.

    Acceptance: Defining source contains neither ElementTree nor XML element references.
    """
    module = inspect.getmodule(ConstructPeriodicCalculationRecord)
    assert module is not None
    source = inspect.getsource(module)
    assert "ElementTree" not in source
    assert "xml.etree" not in source


def test_method__execute__rejects_wrong_input_type() -> None:
    """Evidence ID: SV-PERIODIC-011

    Requirement: The semantic boundary accepts only immutable QexsdDocument inputs.

    Acceptance: Bytes are rejected with TypeError rather than parsed implicitly.
    """
    with pytest.raises(TypeError):
        ConstructPeriodicCalculationRecord().execute(CONTROLLED_QEXSD)  # type: ignore[arg-type]
