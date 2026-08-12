"""Semantic construction of backend-neutral periodic calculation records.

This module contains no XML parsing.  ``ConstructPeriodicCalculationRecord``
translates an already validated native :class:`QexsdDocument` into the minimal
backend-neutral semantic record while preserving provenance, source order, and
native units and making unavailable interpretation explicit.
"""

from __future__ import annotations

from .records import PeriodicCalculationRecord, QexsdDocument, UnavailableReason


class ConstructPeriodicCalculationRecord:
    """Construct backend-neutral semantics from one immutable QEXSD document.

    Notes
    -----
    This deliberately verb-first public name is the explicit task contract for
    ``QexsdDocument -> PeriodicCalculationRecord``.  The transformation performs
    no XML parsing, filesystem access, sorting, normalization, or unit conversion.
    """

    def execute(self, document: QexsdDocument) -> PeriodicCalculationRecord:
        """Return the minimal semantic record preserving native represented state.

        Parameters
        ----------
        document
            Mechanically parsed native QEXSD values.

        Returns
        -------
        PeriodicCalculationRecord
            Immutable schema-version-1 semantic observation.

        Raises
        ------
        TypeError
            If ``document`` is not a :class:`QexsdDocument`.
        """
        if not isinstance(document, QexsdDocument):
            raise TypeError("document must be a QexsdDocument")
        unavailable = UnavailableReason.NOT_REPRESENTED_IN_QEXSD
        return PeriodicCalculationRecord(
            schema_version=1,
            source_path=document.source_path,
            source_sha256=document.source_sha256,
            source_byte_count=document.source_byte_count,
            qexsd_namespace=document.namespace,
            qexsd_version=document.qexsd_version,
            producing_application=document.producing_application,
            producing_application_version=document.producing_application_version,
            direct_lattice_vectors=document.direct_lattice_vectors,
            direct_lattice_unit=document.direct_lattice_unit,
            direct_lattice_convention=document.direct_lattice_convention,
            reciprocal_lattice_vectors=document.reciprocal_lattice_vectors,
            reciprocal_lattice_unit=document.reciprocal_lattice_unit,
            reciprocal_lattice_convention=document.reciprocal_lattice_convention,
            species=document.species,
            atoms=document.atoms,
            atom_count=document.declared_atom_count,
            position_unit=document.position_unit,
            position_convention=document.position_convention,
            k_points=document.k_points,
            k_point_weights=document.k_point_weights,
            k_point_count=document.sampled_k_point_count,
            k_point_convention=document.k_point_convention,
            eigenvalues=document.eigenvalues,
            occupations=document.occupations,
            energy_unit=document.energy_unit,
            band_count=document.band_count,
            spin_channels=document.spin_channels,
            total_energy=document.total_energy,
            total_energy_unit=document.total_energy_unit,
            fft_grid=document.fft_grid,
            fft_smooth=document.fft_smooth,
            fft_box=document.fft_box,
            exit_status=document.exit_status,
            absolute_energy_reference=unavailable,
            fermi_alignment_convention=unavailable,
            retained_subspace=UnavailableReason.NO_RETAINED_SUBSPACE,
            gauge=unavailable,
            phase_convention=unavailable,
            basis_identity=unavailable,
            spin_convention=UnavailableReason.NO_SPIN_RESOLVED_ARRAYS,
        )
