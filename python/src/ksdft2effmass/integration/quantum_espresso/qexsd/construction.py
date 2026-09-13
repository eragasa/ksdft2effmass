"""Source-backed translation from raw QEXSD values to plane-wave KS semantics."""

from __future__ import annotations

import math

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
    ReciprocalLatticeCompatibilityValidator,
    ReciprocalScaleConvention,
    UnitSystem,
)

from .records import QexsdDocument


class ConstructQexsdKohnShamPlaneWaveRecord:
    """Translate one mechanically faithful QEXSD document into target semantics.

    The ActionObject owns the QEXSD-specific facts that output cell vectors and
    Cartesian atomic positions are in bohr, reciprocal vectors and k points are
    Cartesian coefficients in units of ``2*pi/alat``, and QEXSD energies are in
    hartree for the supported global ``Hartree atomic units`` declaration.
    """

    DUALITY_ABSOLUTE_TOLERANCE = 1.0e-12

    def execute(self, document: QexsdDocument) -> KohnShamPlaneWaveCalculationRecord:
        """Return a complete immutable plane-wave Kohn--Sham record."""
        if not isinstance(document, QexsdDocument):
            raise TypeError("document must be a QexsdDocument")
        if document.declared_unit_system_label != "Hartree atomic units":
            raise ValueError("unsupported QEXSD declared unit system")

        direct = DirectLattice(
            vectors=document.direct_lattice_vectors,
            unit_system=UnitSystem.HARTREE_ATOMIC,
            dimension=PhysicalDimension.LENGTH,
            unit=LengthUnit.BOHR,
            coordinate_convention=CoordinateConvention.CARTESIAN,
            vector_order="source_order_a1_a2_a3",
        )
        structure = PeriodicStructure(
            direct_lattice=direct,
            species=tuple(
                AtomicSpecies(
                    name=name,
                    mass=mass,
                    mass_dimension=PhysicalDimension.MASS,
                    mass_unit="unified_atomic_mass_unit",
                    pseudopotential_label=pseudo,
                )
                for name, mass, pseudo in document.species
            ),
            sites=tuple(
                PeriodicSite(
                    index=index,
                    species_name=species,
                    coordinates=position,
                    coordinate_convention=CoordinateConvention.CARTESIAN,
                    coordinate_dimension=PhysicalDimension.LENGTH,
                    coordinate_unit=LengthUnit.BOHR,
                )
                for index, species, position in document.atoms
            ),
        )
        scale = 2.0 * math.pi / document.atomic_structure_alat
        physical_reciprocal = tuple(
            tuple(value * scale for value in vector)
            for vector in document.reciprocal_lattice_coefficients
        )
        reciprocal = ReciprocalLattice(
            raw_coefficients=document.reciprocal_lattice_coefficients,
            raw_dimension=PhysicalDimension.DIMENSIONLESS,
            raw_coordinate_convention=CoordinateConvention.CARTESIAN,
            scale_convention=ReciprocalScaleConvention.TWO_PI_OVER_ALAT,
            scale_alat=document.atomic_structure_alat,
            scale_alat_unit=LengthUnit.BOHR,
            incorporates_two_pi=True,
            physical_vectors=physical_reciprocal,  # type: ignore[arg-type]
            physical_dimension=PhysicalDimension.INVERSE_LENGTH,
            physical_unit=InverseLengthUnit.PER_BOHR,
            physical_coordinate_convention=CoordinateConvention.CARTESIAN,
        )
        ReciprocalLatticeCompatibilityValidator().execute(
            direct,
            reciprocal,
            absolute_tolerance=self.DUALITY_ABSOLUTE_TOLERANCE,
        )
        physical_k_points = tuple(
            tuple(value * scale for value in vector) for vector in document.k_points
        )
        weight_normalization = (
            KPointWeightNormalization.SUM_TO_TWO
            if math.fsum(document.k_point_weights) == 2.0
            else KPointWeightNormalization.UNAVAILABLE
        )
        sampling = KPointSampling(
            raw_coordinates=document.k_points,
            raw_dimension=PhysicalDimension.DIMENSIONLESS,
            coordinate_convention=CoordinateConvention.CARTESIAN,
            scale_convention=ReciprocalScaleConvention.TWO_PI_OVER_ALAT,
            scale_alat=document.atomic_structure_alat,
            scale_alat_unit=LengthUnit.BOHR,
            incorporates_two_pi=True,
            physical_coordinates=physical_k_points,  # type: ignore[arg-type]
            physical_dimension=PhysicalDimension.INVERSE_LENGTH,
            physical_unit=InverseLengthUnit.PER_BOHR,
            weights=document.k_point_weights,
            weight_normalization=weight_normalization,
        )
        spectrum = KohnShamSpectralObservations(
            eigenvalues=document.eigenvalues,
            eigenvalue_unit=EnergyUnit.HARTREE,
            occupations=document.occupations,
            band_count=document.band_count,
            spin_channel_availability=Availability.NO_SPIN_RESOLVED_ARRAYS,
            energy_reference_availability=Availability.NOT_REPRESENTED,
        )
        record = KohnShamPlaneWaveCalculationRecord(
            schema_version=1,
            structure=structure,
            reciprocal_lattice=reciprocal,
            k_point_sampling=sampling,
            spectrum=spectrum,
            total_energy=TotalEnergyObservation(
                value=document.total_energy,
                unit=EnergyUnit.HARTREE,
                reference_availability=Availability.NOT_REPRESENTED,
            ),
            plane_wave=PlaneWaveRepresentationMetadata(
                representation="plane_wave",
                fft_grid=document.fft_grid,
                fft_smooth=document.fft_smooth,
                fft_box=document.fft_box,
                basis_identity=PlaneWaveMetadataAvailability.NOT_REPRESENTED,
                retained_subspace=PlaneWaveMetadataAvailability.NO_RETAINED_SUBSPACE,
                gauge=PlaneWaveMetadataAvailability.NOT_REPRESENTED,
                phase_convention=PlaneWaveMetadataAvailability.NOT_REPRESENTED,
            ),
            provenance=ArtifactProvenance(
                source_path=document.source_path,
                source_sha256=document.source_sha256,
                source_byte_count=document.source_byte_count,
                source_format="QEXSD",
                source_format_version=document.qexsd_version,
                producing_application=document.producing_application,
                producing_application_version=document.producing_application_version,
                transformation=(
                    "QEXSD raw values; direct vectors and Cartesian sites in bohr; "
                    "reciprocal coefficients and k points scaled by 2*pi/alat"
                ),
            ),
            exit_status=document.exit_status,
        )
        KohnShamPlaneWaveCalculationRecordValidator().execute(record)
        return record
