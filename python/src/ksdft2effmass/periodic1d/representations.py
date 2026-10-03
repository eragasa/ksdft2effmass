"""Gauge-qualified one-dimensional retained-operator representations.

The records in this module bind exact retained operators to complete reciprocal-mesh
or hopping-family data.  They do not construct a retained space, choose a gauge,
perform a Fourier transform, truncate coefficients, or infer an effective model.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass

import numpy as np

from ksdft2effmass.operators import (
    MODEL_SYSTEM_UNIT_CONVERTER,
    Basis,
    EnergyReference,
)
from ksdft2effmass.periodic import PeriodicRetainedOperator
from ksdft2effmass.solid_state import (
    BlockHoppingModel1D,
    CenteredUniformReciprocalMesh1D,
    ReciprocalOperatorSamples1D,
)


@dataclass(frozen=True, slots=True, eq=False)
class Periodic1DRetainedOperatorReciprocalRepresentation:
    """Bind reciprocal-mesh matrices to one exact retained operator and gauge.

    Parameters
    ----------
    representation_id
        Stable nonempty identity of this reciprocal representation.
    retained_operator
        Exact retained operator represented by every sampled matrix.
    reciprocal_mesh
        Complete ordered one-dimensional reciprocal mesh.
    samples
        Square represented matrices at every mesh coordinate.
    basis
        Ordered orthonormal basis metadata. Its ordering must equal the retained
        state-label ordering.
    energy_reference
        Represented energy-zero and unit metadata. It must exactly equal the exact
        retained operator's energy reference, and its unit label must equal every
        sampled matrix unit expression.
    representation_map_id
        Nonempty identity of the map into reciprocal matrix coordinates.
    gauge_id
        Nonempty identity of the represented gauge convention.
    content_sha256
        Lowercase SHA-256 identity of the contiguous little-endian ``complex128``
        matrix array. Construction authenticates this identity against ``samples``.
    provenance_id
        Nonempty identity of the representation provenance.

    Raises
    ------
    TypeError
        If a field has the wrong exact semantic type.
    ValueError
        If identities, retained basis ordering, energy metadata, rank, mesh
        coordinates, reciprocal period, or content identity disagree.

    Notes
    -----
    The gauge and basis qualify this finite representation, not the exact retained
    operator. Successful construction authenticates represented array bytes and
    structural correlations only; it does not validate a parent model, gauge quality,
    or scientific adequacy.
    """

    representation_id: str
    retained_operator: PeriodicRetainedOperator
    reciprocal_mesh: CenteredUniformReciprocalMesh1D
    samples: ReciprocalOperatorSamples1D
    basis: Basis
    energy_reference: EnergyReference
    representation_map_id: str
    gauge_id: str
    content_sha256: str
    provenance_id: str

    def __post_init__(self) -> None:
        """Check identities, exact component types, mesh, rank, and content bytes."""
        self._check_args_identities()
        self._check_args_components()
        self._check_args_mesh_and_rank()
        self._check_args_content_identity()

    def _check_args_identities(self) -> None:
        """Require exact nonempty representation identities."""
        for name, value in (
            ("representation_id", self.representation_id),
            ("representation_map_id", self.representation_map_id),
            ("gauge_id", self.gauge_id),
            ("provenance_id", self.provenance_id),
        ):
            if type(value) is not str:
                raise TypeError(f"{name} must be a built-in str")
            if value == "":
                raise ValueError(f"{name} must be nonempty")
        self._require_sha256(self.content_sha256)

    def _check_args_components(self) -> None:
        """Require exact retained-operator and reciprocal-metadata types."""
        if type(self.retained_operator) is not PeriodicRetainedOperator:
            raise TypeError("retained_operator must be PeriodicRetainedOperator")
        if type(self.reciprocal_mesh) is not CenteredUniformReciprocalMesh1D:
            raise TypeError("reciprocal_mesh must be CenteredUniformReciprocalMesh1D")
        if type(self.samples) is not ReciprocalOperatorSamples1D:
            raise TypeError("samples must be ReciprocalOperatorSamples1D")
        if type(self.basis) is not Basis:
            raise TypeError("basis must be Basis")
        if type(self.energy_reference) is not EnergyReference:
            raise TypeError("energy_reference must be EnergyReference")

    def _check_args_mesh_and_rank(self) -> None:
        """Require complete mesh, retained basis, rank, and energy metadata."""
        if self.retained_operator.retained_subspace.spatial_dimension != 1:
            raise ValueError("retained operator must be one-dimensional")
        retained_subspace = self.retained_operator.retained_subspace
        if self.samples.matrix_dimension != retained_subspace.rank:
            raise ValueError("sample dimension must equal retained rank")
        if self.basis.ordering != retained_subspace.definition.ordered_state_labels:
            raise ValueError("basis ordering must equal retained state labels")
        if not self.basis.orthonormal:
            raise ValueError("represented basis must be orthonormal")
        if self.energy_reference != self.retained_operator.energy_reference:
            raise ValueError("energy reference must equal the retained operator")
        if any(
            matrix.unit.expression != self.energy_reference.unit
            for matrix in self.samples.matrices
        ):
            raise ValueError("sample units must equal the represented energy unit")
        expected_period = MODEL_SYSTEM_UNIT_CONVERTER.convert_scalar(
            self.reciprocal_mesh.reciprocal_period,
            self.samples.reciprocal_period.unit,
        )
        if expected_period.magnitude != self.samples.reciprocal_period.magnitude:
            raise ValueError("sample and mesh reciprocal periods must agree")
        expected_coordinates = MODEL_SYSTEM_UNIT_CONVERTER.convert_vector(
            self.reciprocal_mesh.coordinates,
            self.samples.coordinates.unit,
        )
        if not np.array_equal(
            expected_coordinates.magnitude,
            self.samples.coordinates.magnitude,
        ):
            raise ValueError("samples must contain every ordered mesh coordinate")

    def _check_args_content_identity(self) -> None:
        """Authenticate the canonical represented matrix-array bytes."""
        values = np.asarray(
            [matrix.magnitude for matrix in self.samples.matrices],
            dtype=np.complex128,
        )
        canonical = np.ascontiguousarray(values, dtype="<c16")
        measured = hashlib.sha256(canonical.tobytes(order="C")).hexdigest()
        if measured != self.content_sha256:
            raise ValueError("content_sha256 must authenticate reciprocal matrices")

    @staticmethod
    def _require_sha256(value: str) -> None:
        """Require canonical lowercase SHA-256 syntax."""
        if type(value) is not str:
            raise TypeError("content_sha256 must be a built-in str")
        if len(value) != 64 or any(
            character not in "0123456789abcdef" for character in value
        ):
            raise ValueError("content_sha256 must be lowercase SHA-256 hexadecimal")


@dataclass(frozen=True, slots=True, eq=False)
class Periodic1DRetainedOperatorHoppingRepresentation:
    """Bind complete finite-mesh hopping blocks to a retained operator and gauge.

    Parameters
    ----------
    representation_id
        Stable nonempty identity of this hopping representation.
    retained_operator
        Exact retained operator represented by the hopping family.
    reciprocal_mesh
        Complete Born--von Karman mesh whose centered cell representatives are kept.
    hopping_model
        Ordered hopping blocks for every centered mesh representative.
    basis
        Ordered orthonormal basis metadata. Its ordering must equal the retained
        state-label ordering.
    energy_reference
        Represented energy-zero and unit metadata. It must exactly equal the exact
        retained operator's energy reference, and its unit label must equal every
        hopping-block unit expression.
    representation_map_id
        Nonempty identity of the complete reciprocal-to-cell representation map.
    gauge_id
        Nonempty identity of the represented gauge convention.
    content_sha256
        Lowercase SHA-256 identity of the contiguous little-endian ``complex128``
        hopping-block array. Construction authenticates it against ``hopping_model``.
    provenance_id
        Nonempty identity of the representation provenance.

    Raises
    ------
    TypeError
        If a field has the wrong exact semantic type.
    ValueError
        If identities, retained basis ordering, energy metadata, rank, complete
        representative inventory, reciprocal period, or content identity disagree.

    Notes
    -----
    This complete finite-mesh coefficient family is an operator representation, not a
    finite-range effective model. Construction does not claim Fourier reconstruction,
    gauge quality, model adequacy, scientific validation, or uncertainty
    quantification.

    See Also
    --------
    Periodic1DCompleteHoppingRepresentationResult
        Construction ResultObject that additionally owns a reciprocal-to-hopping
        transform, its source and reconstruction, and numerical diagnostics. This
        binding does not require those unavailable route artifacts.
    """

    representation_id: str
    retained_operator: PeriodicRetainedOperator
    reciprocal_mesh: CenteredUniformReciprocalMesh1D
    hopping_model: BlockHoppingModel1D
    basis: Basis
    energy_reference: EnergyReference
    representation_map_id: str
    gauge_id: str
    content_sha256: str
    provenance_id: str

    def __post_init__(self) -> None:
        """Check identities, exact component types, completeness, rank, and bytes."""
        self._check_args_identities()
        self._check_args_components()
        self._check_args_mesh_and_rank()
        self._check_args_content_identity()

    def _check_args_identities(self) -> None:
        """Require exact nonempty representation identities."""
        for name, value in (
            ("representation_id", self.representation_id),
            ("representation_map_id", self.representation_map_id),
            ("gauge_id", self.gauge_id),
            ("provenance_id", self.provenance_id),
        ):
            if type(value) is not str:
                raise TypeError(f"{name} must be a built-in str")
            if value == "":
                raise ValueError(f"{name} must be nonempty")
        self._require_sha256(self.content_sha256)

    def _check_args_components(self) -> None:
        """Require exact retained-operator, mesh, and hopping-metadata types."""
        if type(self.retained_operator) is not PeriodicRetainedOperator:
            raise TypeError("retained_operator must be PeriodicRetainedOperator")
        if type(self.reciprocal_mesh) is not CenteredUniformReciprocalMesh1D:
            raise TypeError("reciprocal_mesh must be CenteredUniformReciprocalMesh1D")
        if type(self.hopping_model) is not BlockHoppingModel1D:
            raise TypeError("hopping_model must be BlockHoppingModel1D")
        if type(self.basis) is not Basis:
            raise TypeError("basis must be Basis")
        if type(self.energy_reference) is not EnergyReference:
            raise TypeError("energy_reference must be EnergyReference")

    def _check_args_mesh_and_rank(self) -> None:
        """Require complete representatives, retained basis, rank, and energy."""
        if self.retained_operator.retained_subspace.spatial_dimension != 1:
            raise ValueError("retained operator must be one-dimensional")
        retained_subspace = self.retained_operator.retained_subspace
        if self.hopping_model.matrix_dimension != retained_subspace.rank:
            raise ValueError("hopping dimension must equal retained rank")
        if self.basis.ordering != retained_subspace.definition.ordered_state_labels:
            raise ValueError("basis ordering must equal retained state labels")
        if not self.basis.orthonormal:
            raise ValueError("represented basis must be orthonormal")
        if self.energy_reference != self.retained_operator.energy_reference:
            raise ValueError("energy reference must equal the retained operator")
        if any(
            block.unit.expression != self.energy_reference.unit
            for block in self.hopping_model.hopping_blocks
        ):
            raise ValueError("hopping units must equal the represented energy unit")
        if self.hopping_model.representatives != (
            self.reciprocal_mesh.centered_cell_representatives
        ):
            raise ValueError("hopping representation must retain the complete mesh")
        expected_period = MODEL_SYSTEM_UNIT_CONVERTER.convert_scalar(
            self.reciprocal_mesh.reciprocal_period,
            self.hopping_model.reciprocal_period.unit,
        )
        if expected_period.magnitude != self.hopping_model.reciprocal_period.magnitude:
            raise ValueError("hopping and mesh reciprocal periods must agree")

    def _check_args_content_identity(self) -> None:
        """Authenticate the canonical represented hopping-array bytes."""
        values = np.asarray(
            [block.magnitude for block in self.hopping_model.hopping_blocks],
            dtype=np.complex128,
        )
        canonical = np.ascontiguousarray(values, dtype="<c16")
        measured = hashlib.sha256(canonical.tobytes(order="C")).hexdigest()
        if measured != self.content_sha256:
            raise ValueError("content_sha256 must authenticate hopping blocks")

    @staticmethod
    def _require_sha256(value: str) -> None:
        """Require canonical lowercase SHA-256 syntax."""
        if type(value) is not str:
            raise TypeError("content_sha256 must be a built-in str")
        if len(value) != 64 or any(
            character not in "0123456789abcdef" for character in value
        ):
            raise ValueError("content_sha256 must be lowercase SHA-256 hexadecimal")


__all__ = [
    "Periodic1DRetainedOperatorHoppingRepresentation",
    "Periodic1DRetainedOperatorReciprocalRepresentation",
]
