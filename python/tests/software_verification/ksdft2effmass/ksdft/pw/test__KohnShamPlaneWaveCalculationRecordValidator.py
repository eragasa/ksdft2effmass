r"""Software verification of ``KohnShamPlaneWaveCalculationRecordValidator``.

Evidence profile: routine

Bounded artifact scope: cross-object scale and sampled-point-count compatibility.

Facet and represented meaning

The ActionObject validates compatibility among independently valid periodic and
Kohn--Sham components of one aggregate plane-wave record.

Intrinsic and cross-object scope

Exact reciprocal/k-point scale and spectrum/k-point count agreement are covered;
intrinsic component invariants remain with their DataObjects.

VVUQ and scientific exclusions

Validation is software verification only and establishes no physical adequacy,
numerical verification, scientific validation, or uncertainty quantification.
"""

from __future__ import annotations

import math
from dataclasses import replace

import pytest

from ksdft2effmass.ksdft import (
    Availability,
    EnergyUnit,
    KohnShamSpectralObservations,
    TotalEnergyObservation,
)
from ksdft2effmass.ksdft.pw import (
    ArtifactProvenance,
    KohnShamPlaneWaveCalculationRecord,
    KohnShamPlaneWaveCalculationRecordValidator,
    PlaneWaveMetadataAvailability,
    PlaneWaveRepresentationMetadata,
)
from ksdft2effmass.periodic import (
    AtomicSpecies,
    CoordinateConvention,
    DirectLattice,
    InverseLengthUnit,
    KPointSampling,
    KPointWeightNormalization,
    LengthUnit,
    PeriodicSite,
    PeriodicStructure,
    PhysicalDimension,
    ReciprocalLattice,
    ReciprocalScaleConvention,
    UnitSystem,
)

pytestmark = pytest.mark.software_verification
SUT = KohnShamPlaneWaveCalculationRecordValidator


def make_record() -> KohnShamPlaneWaveCalculationRecord:
    """Return one compatible aggregate record; this helper owns no identifier.

    Evidence ID: Helper owns no identifier.

    Requirement: Support validator tests without an independent evidence claim.

    Acceptance: Return independently valid components with one matching sample.
    """
    direct = DirectLattice(
        ((2.0, 0.0, 0.0), (0.0, 2.0, 0.0), (0.0, 0.0, 2.0)),
        UnitSystem.HARTREE_ATOMIC,
        PhysicalDimension.LENGTH,
        LengthUnit.BOHR,
        CoordinateConvention.CARTESIAN,
        "source order",
    )
    species = AtomicSpecies(
        "Si", 28.085, PhysicalDimension.MASS, "unified_atomic_mass_unit", "Si.upf"
    )
    site = PeriodicSite(
        1,
        "Si",
        (0.0, 0.0, 0.0),
        CoordinateConvention.CARTESIAN,
        PhysicalDimension.LENGTH,
        LengthUnit.BOHR,
    )
    reciprocal = ReciprocalLattice(
        ((1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, 1.0)),
        PhysicalDimension.DIMENSIONLESS,
        CoordinateConvention.CARTESIAN,
        ReciprocalScaleConvention.TWO_PI_OVER_ALAT,
        2.0,
        LengthUnit.BOHR,
        True,
        ((math.pi, 0.0, 0.0), (0.0, math.pi, 0.0), (0.0, 0.0, math.pi)),
        PhysicalDimension.INVERSE_LENGTH,
        InverseLengthUnit.PER_BOHR,
        CoordinateConvention.CARTESIAN,
    )
    sampling = KPointSampling(
        ((0.0, 0.0, 0.0),),
        PhysicalDimension.DIMENSIONLESS,
        CoordinateConvention.CARTESIAN,
        ReciprocalScaleConvention.TWO_PI_OVER_ALAT,
        2.0,
        LengthUnit.BOHR,
        True,
        ((0.0, 0.0, 0.0),),
        PhysicalDimension.INVERSE_LENGTH,
        InverseLengthUnit.PER_BOHR,
        (2.0,),
        KPointWeightNormalization.SUM_TO_TWO,
    )
    spectrum = KohnShamSpectralObservations(
        ((-0.5,),),
        EnergyUnit.HARTREE,
        ((1.0,),),
        1,
        Availability.NO_SPIN_RESOLVED_ARRAYS,
        Availability.NOT_REPRESENTED,
    )
    return KohnShamPlaneWaveCalculationRecord(
        1,
        PeriodicStructure(direct, (species,), (site,)),
        reciprocal,
        sampling,
        spectrum,
        TotalEnergyObservation(
            -1.0, EnergyUnit.HARTREE, Availability.NOT_REPRESENTED
        ),
        PlaneWaveRepresentationMetadata(
            "plane_wave",
            (2, 2, 2),
            (2, 2, 2),
            (2, 2, 2),
            PlaneWaveMetadataAvailability.NOT_REPRESENTED,
            PlaneWaveMetadataAvailability.NO_RETAINED_SUBSPACE,
            PlaneWaveMetadataAvailability.NOT_REPRESENTED,
            PlaneWaveMetadataAvailability.NOT_REPRESENTED,
        ),
        ArtifactProvenance(
            "/source.xml", "a" * 64, 1, "QEXSD", "1", "PWSCF", "7.2", "test"
        ),
        0,
    )


def test_method__execute__accepts_compatible_record_components() -> None:
    """Evidence ID: SV-KSDFT-005

    Requirement: The validator accepts equal reciprocal/k-point scales and equal
    sampled-point/spectrum counts.

    Acceptance: ``execute`` returns ``None`` without mutating the record.
    """
    record = make_record()
    before = record
    KohnShamPlaneWaveCalculationRecordValidator().execute(record)
    assert record == before


def test_method__execute__rejects_scale_disagreement() -> None:
    """Evidence ID: SV-KSDFT-006

    Requirement: Reciprocal and k-point scale disagreement is rejected by the
    ActionObject rather than aggregate DataObject construction.

    Acceptance: The aggregate constructs and ``execute`` raises ``ValueError``.
    """
    record = make_record()
    sampling = replace(record.k_point_sampling, scale_alat=3.0)
    incompatible = replace(record, k_point_sampling=sampling)
    with pytest.raises(ValueError, match="scales must agree"):
        KohnShamPlaneWaveCalculationRecordValidator().execute(incompatible)


def test_method__execute__rejects_sample_count_disagreement() -> None:
    """Evidence ID: SV-KSDFT-007

    Requirement: Spectrum-row and sampled-k-point count disagreement is rejected by
    the ActionObject rather than aggregate DataObject construction.

    Acceptance: The aggregate constructs and ``execute`` raises ``ValueError``.
    """
    record = make_record()
    spectrum = replace(
        record.spectrum,
        eigenvalues=((-0.5,), (-0.4,)),
        occupations=((1.0,), (1.0,)),
    )
    incompatible = replace(record, spectrum=spectrum)
    with pytest.raises(ValueError, match="counts must agree"):
        KohnShamPlaneWaveCalculationRecordValidator().execute(incompatible)
