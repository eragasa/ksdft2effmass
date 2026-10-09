"""Explicit metadata adaptation for represented periodic-1D supercell operators.

This module provides the lossless route from caller-authored supercell metadata and a
dense matrix to the general :class:`ksdft2effmass.operators.OperatorRecord`.  It does
not reconstruct cell vectors, basis labels, provenance, or scientific identity from a
matrix, dimension, path, file name, digest, or descriptive ordering string.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray

from ksdft2effmass.operators import (
    Basis,
    EnergyReference,
    Geometry,
    OperatorRecord,
    StateSpace,
)

type ComplexMatrix = NDArray[np.complex128]
type CellVectors = tuple[
    tuple[float, float, float],
    tuple[float, float, float],
    tuple[float, float, float],
]


@dataclass(frozen=True, slots=True)
class Periodic1DSupercellOperatorProvenance:
    """Retain structured provenance identities for one supercell representation.

    Parameters
    ----------
    parent_model_id
        Stable nonempty identity of the represented scientific parent model.
    source_record_id
        Stable nonempty identity of the authenticated source record.
    construction_record_id
        Stable nonempty identity of the numerical construction record.
    producer_id
        Stable nonempty identity of the producing software operation or campaign.

    Raises
    ------
    TypeError
        If any field is not an exact built-in string.
    ValueError
        If any field is empty.

    Notes
    -----
    These are caller-supplied identities, not identities inferred from paths or
    hashes.  The record does not authenticate any referenced artifact.
    """

    parent_model_id: str
    source_record_id: str
    construction_record_id: str
    producer_id: str

    def __post_init__(self) -> None:
        """Require exact nonempty provenance identities."""
        for name, value in (
            ("parent_model_id", self.parent_model_id),
            ("source_record_id", self.source_record_id),
            ("construction_record_id", self.construction_record_id),
            ("producer_id", self.producer_id),
        ):
            if type(value) is not str:
                raise TypeError(f"{name} must be a built-in str")
            if value == "":
                raise ValueError(f"{name} must be nonempty")

    def as_operator_record_mapping(self) -> dict[str, str]:
        """Return a new exact-key mapping for ``OperatorRecord`` provenance.

        Returns
        -------
        dict[str, str]
            Four provenance identities under closed, descriptive keys.
        """
        return {
            "parent_model_id": self.parent_model_id,
            "source_record_id": self.source_record_id,
            "construction_record_id": self.construction_record_id,
            "producer_id": self.producer_id,
        }


@dataclass(frozen=True, slots=True)
class Periodic1DSupercellOperatorMetadata:
    """Supply complete interpreting metadata for one dense supercell operator.

    Parameters
    ----------
    state_space_id, state_space_kind
        Stable nonempty finite-state-space identity and state-space-kind metadata.
    basis_id, basis_kind
        Stable nonempty ordered-basis identity and convention.
    ordered_state_labels
        Exact unique nonempty label for every matrix row and column, in semantic
        order.  Labels are never generated from dimensions.
    cell_vectors
        Three explicit finite linearly independent row cell vectors.
    geometry_id, boundary_conditions, coordinate_convention, length_unit
        Exact interpreting geometry identity and conventions.
    energy_reference, energy_unit
        Exact matrix energy-zero and unit conventions.
    provenance
        Structured caller-supplied provenance identities.

    Raises
    ------
    TypeError
        If a textual field, labels tuple, cell tuple, or provenance object has
        the wrong exact type.
    ValueError
        If metadata are empty, labels repeat, or the cell is nonfinite or not
        linearly independent.
    OverflowError
        If finite cell values cannot be represented in binary64.

    Notes
    -----
    The constructor deliberately requires information absent from historical
    matched-extraction artifacts.  Those artifacts remain unmigrated unless a
    caller supplies authenticated metadata; this class never guesses it.
    """

    state_space_id: str
    state_space_kind: str
    basis_id: str
    basis_kind: str
    ordered_state_labels: tuple[str, ...]
    cell_vectors: CellVectors
    geometry_id: str
    boundary_conditions: str
    coordinate_convention: str
    length_unit: str
    energy_reference: str
    energy_unit: str
    provenance: Periodic1DSupercellOperatorProvenance

    def __post_init__(self) -> None:
        """Validate exact metadata through its canonical nested record owners."""
        self._check_args_exact_containers()
        self._construct_nested_metadata()

    def _check_args_exact_containers(self) -> None:
        """Reject erased or coercible containers before nested validation."""
        if type(self.ordered_state_labels) is not tuple:
            raise TypeError("ordered_state_labels must be an exact tuple")
        if type(self.cell_vectors) is not tuple or any(
            type(row) is not tuple for row in self.cell_vectors
        ):
            raise TypeError("cell_vectors must be an exact tuple of exact tuples")
        if type(self.provenance) is not Periodic1DSupercellOperatorProvenance:
            raise TypeError("provenance must be Periodic1DSupercellOperatorProvenance")

    def _construct_nested_metadata(
        self,
    ) -> tuple[StateSpace, Basis, Geometry, EnergyReference]:
        """Construct canonical metadata owners and thereby validate correlations."""
        state_space = StateSpace(
            self.state_space_id,
            self.state_space_kind,
            len(self.ordered_state_labels),
        )
        basis = Basis(
            self.basis_id,
            self.basis_kind,
            self.ordered_state_labels,
            True,
        )
        geometry = Geometry(
            self.geometry_id,
            self.cell_vectors,
            self.boundary_conditions,
            self.coordinate_convention,
            self.length_unit,
        )
        energy_reference = EnergyReference(self.energy_reference, self.energy_unit)
        # OperatorRecord owns the final cross-object dimension check once a matrix
        # is supplied; all metadata-only invariants are closed here.
        return state_space, basis, geometry, energy_reference


class Periodic1DSupercellOperatorConstructor:
    """Construct a general represented operator from explicit supercell metadata."""

    __slots__ = ()

    def execute(
        self,
        identifier: str,
        operator_kind: str,
        metadata: Periodic1DSupercellOperatorMetadata,
        matrix: ComplexMatrix,
    ) -> OperatorRecord:
        """Build an immutable ``OperatorRecord`` without inferring metadata.

        Parameters
        ----------
        identifier
            Exact nonempty represented-record identity.
        operator_kind
            Exact nonempty mathematical operator-kind description.
        metadata
            Complete caller-supplied cell, ordered-state, convention, identity,
            and structured-provenance metadata.
        matrix
            Dense finite represented matrix.  Its exact row and column order is
            ``metadata.ordered_state_labels``.

        Returns
        -------
        OperatorRecord
            General immutable represented-operator record.

        Raises
        ------
        TypeError
            If ``metadata`` is not the exact metadata type or ``matrix`` is not
            an approved numeric NumPy matrix for ``OperatorRecord``.
        ValueError
            If matrix rank, shape, finiteness, or dimension conflicts with the
            explicit metadata.
        OverflowError
            If accepted finite values cannot be represented in complex128.
        MemoryError
            If defensive dense-matrix storage cannot be allocated.

        Notes
        -----
        Construction requires ``O(N^2)`` time and storage for an ``N``-state
        dense operator.  No arbitrary size cap is imposed.  SHA-256 and other
        digests establish content identity only and are not accepted as metadata
        substitutes.  Successful construction is software evidence, not proof of
        provenance authenticity, convergence, or scientific validation.
        """
        for name, value in (
            ("identifier", identifier),
            ("operator_kind", operator_kind),
        ):
            if type(value) is not str:
                raise TypeError(f"{name} must be a built-in str")
            if value == "":
                raise ValueError(f"{name} must be nonempty")
        if type(metadata) is not Periodic1DSupercellOperatorMetadata:
            raise TypeError("metadata must be Periodic1DSupercellOperatorMetadata")
        state_space, basis, geometry, energy_reference = (
            metadata._construct_nested_metadata()
        )
        return OperatorRecord(
            identifier=identifier,
            operator_kind=operator_kind,
            matrix=matrix,
            state_space=state_space,
            basis=basis,
            geometry=geometry,
            energy_reference=energy_reference,
            provenance=metadata.provenance.as_operator_record_mapping(),
        )


__all__ = [
    "Periodic1DSupercellOperatorConstructor",
    "Periodic1DSupercellOperatorMetadata",
    "Periodic1DSupercellOperatorProvenance",
]
