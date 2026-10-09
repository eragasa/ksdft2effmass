"""Explicit represented-supercell metadata authoring for blind alignment."""

from __future__ import annotations

from ksdft2effmass.periodic1d import (
    Periodic1DSupercellOperatorMetadata,
    Periodic1DSupercellOperatorProvenance,
)


class BlindAlignmentSupercellMetadataAuthor:
    """Author the closed synthetic supercell convention used by blind alignment.

    This Action is deliberately campaign-specific.  It does not adapt unknown or
    historical scientific artifacts and must not be used to infer their cell vectors,
    state labels, identities, or provenance.
    """

    __slots__ = ()

    def execute(
        self,
        *,
        state_space_id: str,
        cell_count: int,
        orbital_count: int,
        spin_count: int,
        site_ordering: str,
        orbital_ordering: str,
        spin_ordering: str,
        coordinate_frame: str,
        energy_reference: str,
        geometry_id: str,
    ) -> Periodic1DSupercellOperatorMetadata:
        """Return explicit metadata for one synthetic blind-alignment basis.

        Parameters
        ----------
        state_space_id
            Stable finite-state-space identity supplied by the campaign case.
        cell_count, orbital_count, spin_count
            Positive exact factors of the maintained synthetic tensor-product
            convention.
        site_ordering, orbital_ordering, spin_ordering, coordinate_frame
            Nonempty exact semantic conventions used to author every state label
            and the basis identity.
        energy_reference
            Nonempty exact energy-zero convention in units of ``E_G``.
        geometry_id
            Nonempty exact identity of the embedded supercell geometry.

        Returns
        -------
        Periodic1DSupercellOperatorMetadata
            Complete cell vectors, ordered state labels, conventions, and
            structured provenance for the synthetic campaign case.

        Raises
        ------
        TypeError
            If a count is not an exact built-in integer or a textual field is not
            an exact built-in string.
        ValueError
            If a count is nonpositive or a textual field is empty.
        OverflowError
            If ``cell_count`` is not representable as binary64 for the explicit
            embedded first cell vector.
        MemoryError
            If the exact ordered label inventory cannot be allocated.

        Notes
        -----
        The operation creates ``cell_count * orbital_count * spin_count`` labels
        and therefore uses linear time and storage in represented dimension.  It
        imposes no arbitrary size cap.  The conventions are synthetic campaign
        definitions, not recovered material metadata or scientific validation.
        """
        values = (
            ("state_space_id", state_space_id),
            ("site_ordering", site_ordering),
            ("orbital_ordering", orbital_ordering),
            ("spin_ordering", spin_ordering),
            ("coordinate_frame", coordinate_frame),
            ("energy_reference", energy_reference),
            ("geometry_id", geometry_id),
        )
        for text_name, text_value in values:
            if type(text_value) is not str:
                raise TypeError(f"{text_name} must be a built-in str")
            if text_value == "":
                raise ValueError(f"{text_name} must be nonempty")
        for count_name, count_value in (
            ("cell_count", cell_count),
            ("orbital_count", orbital_count),
            ("spin_count", spin_count),
        ):
            if type(count_value) is not int:
                raise TypeError(f"{count_name} must be a built-in int")
            if count_value <= 0:
                raise ValueError(f"{count_name} must be positive")
        first_cell_length = float(cell_count)
        if not first_cell_length < float("inf"):
            raise OverflowError("cell_count is not representable in binary64")
        labels = tuple(
            f"{site_ordering}:site-{site}/{orbital_ordering}:orbital-{orbital}/"
            f"{spin_ordering}:spin-{spin}"
            for site in range(cell_count)
            for orbital in range(orbital_count)
            for spin in range(spin_count)
        )
        return Periodic1DSupercellOperatorMetadata(
            state_space_id=state_space_id,
            state_space_kind="periodic-1d synthetic blind-alignment supercell fiber",
            basis_id=(
                f"{geometry_id}/{site_ordering}/{orbital_ordering}/{spin_ordering}/"
                f"{coordinate_frame}"
            ),
            basis_kind="site-major orbital-middle spin-fast orthonormal basis",
            ordered_state_labels=labels,
            cell_vectors=(
                (first_cell_length, 0.0, 0.0),
                (0.0, 1.0, 0.0),
                (0.0, 0.0, 1.0),
            ),
            geometry_id=geometry_id,
            boundary_conditions="periodic along first embedded cell vector",
            coordinate_convention="dimensionless Cartesian row lattice vectors",
            length_unit="primitive_cell_length",
            energy_reference=energy_reference,
            energy_unit="E_G",
            provenance=Periodic1DSupercellOperatorProvenance(
                parent_model_id="periodic1d.blind-alignment-parent.v1",
                source_record_id="authenticated blind-alignment baseline",
                construction_record_id="blind-alignment-v1 synthetic supercell",
                producer_id="BlindAlignmentSupercellMetadataAuthor",
            ),
        )


__all__ = ["BlindAlignmentSupercellMetadataAuthor"]
