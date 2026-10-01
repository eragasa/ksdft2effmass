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
        if type(self.interior_points) is not int:
            raise TypeError("interior_points must be a built-in int")
        if self.interior_points <= 0:
            raise ValueError("interior_points must be positive")
        if type(self.retained_dimension) is not int:
            raise TypeError("retained_dimension must be a built-in int")
        if self.retained_dimension <= 0:
            raise ValueError("retained_dimension must be positive")
        if self.retained_dimension > self.interior_points:
            raise ValueError("retained_dimension must not exceed interior_points")
        if type(self.boundary_kind) is not str:
            raise TypeError("boundary_kind must be a string")
        if self.boundary_kind != "cyclic closure on the same finite coordinate space":
            raise ValueError("boundary_kind must identify the version-one reference")
        if type(self.boundary_interpretation) is not str:
            raise TypeError("boundary_interpretation must be a string")
        if self.boundary_interpretation != (
            "Declared comparison reference only; not a "
            "representation-independent continuum potential."
        ):
            raise ValueError(
                "boundary_interpretation must identify the version-one interpretation"
            )


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
        full_dimension = self.definition.interior_points
        retained_dimension = self.definition.retained_dimension
        full_shape = (full_dimension, full_dimension)
        retained_shape = (retained_dimension, retained_dimension)
        if self.hamiltonian.shape != full_shape:
            raise ValueError("hamiltonian shape must match the full state space")
        if self.eigenvalues.magnitude.shape != (full_dimension,):
            raise ValueError("eigenvalues must span the full state space")
        if self.eigenvectors.magnitude.shape != full_shape:
            raise ValueError("eigenvectors must span the full state space")
        if self.retained_vectors.magnitude.shape != (
            full_dimension,
            retained_dimension,
        ):
            raise ValueError("retained_vectors must map retained to full coordinates")
        for name, quantity in (
            ("projector", self.projector),
            ("retained_embedded", self.retained_embedded),
            ("cyclic_reference", self.cyclic_reference),
            ("consistently_compressed", self.consistently_compressed),
            ("unmatched_compression", self.unmatched_compression),
            ("discarded_sector", self.discarded_sector),
            ("boundary_realization", self.boundary_realization),
        ):
            if quantity.magnitude.shape != full_shape:
                raise ValueError(f"{name} shape must match the full state space")
        if self.retained_coordinates.magnitude.shape != retained_shape:
            raise ValueError(
                "retained_coordinates shape must match the retained state space"
            )
        for name, vector_quantity in (
            ("discrete_closed_form", self.discrete_closed_form),
            ("continuum_closed_form", self.continuum_closed_form),
        ):
            if vector_quantity.magnitude.shape != (full_dimension,):
                raise ValueError(f"{name} must span the full state space")
        diagnostic_names = tuple(name for name, _ in self.diagnostics)
        if len(set(diagnostic_names)) != len(diagnostic_names):
            raise ValueError("diagnostic names must be unique")
