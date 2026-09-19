"""Immutable records for particle-in-a-box research-monograph campaigns."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from ksdft2effmass.analysis.model_systems import ScalarQuantity, VectorQuantity
from ksdft2effmass.operators import MatrixQuantity, SparseMatrixQuantity


@dataclass(frozen=True, slots=True)
class ParticleInBoxStudyDefinition:
    """Retain one validated version-one residual-study definition."""

    schema_version: int
    experiment_id: str
    evidence_status: str
    length: float
    mass: float
    hbar: float
    interior_points: int
    retained_dimension: int
    boundary_kind: str
    boundary_interpretation: str

    def __post_init__(self) -> None:
        if self.schema_version != 1:
            raise ValueError("schema_version must equal one")
        if type(self.experiment_id) is not str or not self.experiment_id:
            raise TypeError("experiment_id must be a nonempty string")
        if self.evidence_status != "illustrative numerical experiment":
            raise ValueError("evidence_status must identify an illustrative experiment")
        for value, name in (
            (self.length, "length"),
            (self.mass, "mass"),
            (self.hbar, "hbar"),
        ):
            if type(value) is not float:
                raise TypeError(f"{name} must be a built-in float")
            if not np.isfinite(value) or value <= 0.0:
                raise ValueError(f"{name} must be positive and finite")
        if type(self.interior_points) is not int or self.interior_points <= 0:
            raise ValueError("interior_points must be a positive built-in int")
        if type(self.retained_dimension) is not int or self.retained_dimension <= 0:
            raise ValueError("retained_dimension must be a positive built-in int")
        if self.retained_dimension > self.interior_points:
            raise ValueError("retained_dimension must not exceed interior_points")
        if type(self.boundary_kind) is not str or not self.boundary_kind:
            raise TypeError("boundary_kind must be a nonempty string")
        if (
            type(self.boundary_interpretation) is not str
            or not self.boundary_interpretation
        ):
            raise TypeError("boundary_interpretation must be a nonempty string")


@dataclass(frozen=True, slots=True, eq=False)
class ParticleInBoxResidualStudyResult:
    """Retain represented matrices, spectra, residuals, and scalar diagnostics."""

    definition: ParticleInBoxStudyDefinition
    hamiltonian: SparseMatrixQuantity
    eigenvalues: VectorQuantity
    eigenvectors: MatrixQuantity
    retained_vectors: MatrixQuantity
    projector: MatrixQuantity
    retained_embedded: MatrixQuantity
    retained_coordinates: MatrixQuantity
    cyclic_reference: MatrixQuantity
    consistently_compressed: MatrixQuantity
    unmatched_compression: MatrixQuantity
    discarded_sector: MatrixQuantity
    boundary_realization: MatrixQuantity
    discrete_closed_form: VectorQuantity
    continuum_closed_form: VectorQuantity
    diagnostics: tuple[tuple[str, ScalarQuantity], ...]

    def __post_init__(self) -> None:
        if not isinstance(self.definition, ParticleInBoxStudyDefinition):
            raise TypeError("definition must be ParticleInBoxStudyDefinition")
        if not isinstance(self.hamiltonian, SparseMatrixQuantity):
            raise TypeError("hamiltonian must be SparseMatrixQuantity")
        if not isinstance(self.eigenvalues, VectorQuantity):
            raise TypeError("eigenvalues must be VectorQuantity")
        if not isinstance(self.eigenvectors, MatrixQuantity):
            raise TypeError("eigenvectors must be MatrixQuantity")
        for quantity in (
            self.retained_vectors,
            self.projector,
            self.retained_embedded,
            self.retained_coordinates,
            self.cyclic_reference,
            self.consistently_compressed,
            self.unmatched_compression,
            self.discarded_sector,
            self.boundary_realization,
        ):
            if not isinstance(quantity, MatrixQuantity):
                raise TypeError("represented result matrices must be MatrixQuantity")
        if not isinstance(self.discrete_closed_form, VectorQuantity):
            raise TypeError("discrete_closed_form must be VectorQuantity")
        if not isinstance(self.continuum_closed_form, VectorQuantity):
            raise TypeError("continuum_closed_form must be VectorQuantity")
        if not isinstance(self.diagnostics, tuple) or not all(
            isinstance(item, tuple)
            and len(item) == 2
            and type(item[0]) is str
            and isinstance(item[1], ScalarQuantity)
            for item in self.diagnostics
        ):
            raise TypeError("diagnostics must be immutable named scalar quantities")
