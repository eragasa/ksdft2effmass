r"""Software verification of ``ConstructQexsdKohnShamPlaneWaveRecord``.

Evidence profile: routine

Bounded artifact scope: QEXSD-to-plane-wave semantic translation.

Facet and represented meaning

The ActionObject translates source-backed units, coordinates, scales, and absence.

Intrinsic and cross-object scope

This owns QEXSD knowledge crossing into backend-neutral composed objects.

VVUQ and scientific exclusions

Exact translation and duality checks establish no scientific validation or UQ.
"""

import math

import pytest
from qexsd_fixtures import CONTROLLED_QEXSD, controlled_source_bytes

from ksdft2effmass.io.quantum_espresso.qexsd import (
    ConstructQexsdKohnShamPlaneWaveRecord,
    ParseQexsdDocument,
    QexsdSource,
)
from ksdft2effmass.ksdft import Availability, EnergyUnit
from ksdft2effmass.periodic import KPointWeightNormalization, LengthUnit

SUT = ConstructQexsdKohnShamPlaneWaveRecord
pytestmark = pytest.mark.software_verification


def test_method__execute__constructs_quantity_specific_semantics() -> None:
    """Evidence ID: SV-PERIODIC-009

    Requirement: Construction assigns explicit quantity-specific units and conventions.

    Acceptance: Every asserted semantic field and unavailable state is exact.
    """
    digest, count = controlled_source_bytes()
    document = ParseQexsdDocument().execute(
        QexsdSource("/controlled/source.xml", digest, count, CONTROLLED_QEXSD)
    )
    record = SUT().execute(document)
    assert record.structure.direct_lattice.unit is LengthUnit.BOHR
    assert record.structure.sites[0].coordinate_unit is LengthUnit.BOHR
    assert record.spectrum.eigenvalue_unit is EnergyUnit.HARTREE
    assert record.total_energy.unit is EnergyUnit.HARTREE
    assert (
        record.spectrum.spin_channel_availability
        is Availability.NO_SPIN_RESOLVED_ARRAYS
    )
    assert record.spectrum.energy_reference_availability is Availability.NOT_REPRESENTED
    assert (
        record.k_point_sampling.weight_normalization
        is KPointWeightNormalization.UNAVAILABLE
    )
    assert record.reciprocal_lattice.incorporates_two_pi is True
    assert record.provenance.source_sha256 == digest


def test_method__execute__enforces_direct_reciprocal_duality() -> None:
    """Evidence ID: SV-PERIODIC-010

    Requirement: The physical reciprocal lattice obeys A B^T = 2*pi I.

    Acceptance: Independently evaluated components match 2*pi I within 1e-12.
    """
    digest, count = controlled_source_bytes()
    record = SUT().execute(
        ParseQexsdDocument().execute(
            QexsdSource("/controlled/source.xml", digest, count, CONTROLLED_QEXSD)
        )
    )
    a1, a2, a3 = record.structure.direct_lattice.vectors
    b1, b2, b3 = record.reciprocal_lattice.physical_vectors
    assert math.fsum((a1[0] * b1[0], a1[1] * b1[1], a1[2] * b1[2])) == pytest.approx(
        2.0 * math.pi, abs=1.0e-12, rel=0.0
    )
    assert math.fsum((a1[0] * b2[0], a1[1] * b2[1], a1[2] * b2[2])) == pytest.approx(
        0.0, abs=1.0e-12, rel=0.0
    )
    assert math.fsum((a1[0] * b3[0], a1[1] * b3[1], a1[2] * b3[2])) == pytest.approx(
        0.0, abs=1.0e-12, rel=0.0
    )
    assert math.fsum((a2[0] * b1[0], a2[1] * b1[1], a2[2] * b1[2])) == pytest.approx(
        0.0, abs=1.0e-12, rel=0.0
    )
    assert math.fsum((a2[0] * b2[0], a2[1] * b2[1], a2[2] * b2[2])) == pytest.approx(
        2.0 * math.pi, abs=1.0e-12, rel=0.0
    )
    assert math.fsum((a2[0] * b3[0], a2[1] * b3[1], a2[2] * b3[2])) == pytest.approx(
        0.0, abs=1.0e-12, rel=0.0
    )
    assert math.fsum((a3[0] * b1[0], a3[1] * b1[1], a3[2] * b1[2])) == pytest.approx(
        0.0, abs=1.0e-12, rel=0.0
    )
    assert math.fsum((a3[0] * b2[0], a3[1] * b2[1], a3[2] * b2[2])) == pytest.approx(
        0.0, abs=1.0e-12, rel=0.0
    )
    assert math.fsum((a3[0] * b3[0], a3[1] * b3[1], a3[2] * b3[2])) == pytest.approx(
        2.0 * math.pi, abs=1.0e-12, rel=0.0
    )


def test_method__execute__rejects_wrong_input_type() -> None:
    """Evidence ID: SV-PERIODIC-011

    Requirement: Construction accepts only QexsdDocument.

    Acceptance: Raw bytes raise TypeError and are not parsed implicitly.
    """
    with pytest.raises(TypeError):
        SUT().execute(CONTROLLED_QEXSD)  # type: ignore[arg-type]
