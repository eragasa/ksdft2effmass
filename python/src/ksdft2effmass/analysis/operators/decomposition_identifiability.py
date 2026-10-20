"""Reusable retained-space decomposition identifiability analysis."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from ksdft2effmass.operators import MatrixQuantity, ScalarQuantity

from .model_fitting import RetainedModelClassFitResult, RetainedModelClassFitter


@dataclass(frozen=True, slots=True, eq=False)
class DecompositionIdentifiabilityResult:
    """Retain two exact decompositions and declared model-class fits."""

    physical_kinetic: MatrixQuantity
    physical_potential: MatrixQuantity
    alternative_kinetic: MatrixQuantity
    alternative_potential: MatrixQuantity
    physical_reconstruction_error: ScalarQuantity
    alternative_reconstruction_error: ScalarQuantity
    model_class_fits: tuple[RetainedModelClassFitResult, ...]


class DecompositionIdentifiabilityAnalyzer:
    """Compare exact decomposition freedom with restricted model-class fits."""

    __slots__ = ("model_fitter",)

    def __init__(self, model_fitter: RetainedModelClassFitter | None = None) -> None:
        """Construct with an explicit or default retained model-class fitter."""
        if model_fitter is not None and not isinstance(
            model_fitter, RetainedModelClassFitter
        ):
            raise TypeError("model_fitter must be RetainedModelClassFitter or None")
        self.model_fitter = model_fitter or RetainedModelClassFitter()

    def execute(
        self, reduced_hamiltonian: MatrixQuantity, shift: MatrixQuantity
    ) -> DecompositionIdentifiabilityResult:
        """Return exact decompositions and fits of the declared shift."""
        if not isinstance(reduced_hamiltonian, MatrixQuantity):
            raise TypeError("reduced_hamiltonian must be MatrixQuantity")
        if not isinstance(shift, MatrixQuantity):
            raise TypeError("shift must be MatrixQuantity")
        hamiltonian = reduced_hamiltonian.magnitude
        shift_matrix = shift.magnitude
        if hamiltonian.shape != shift_matrix.shape:
            raise ValueError("reduced_hamiltonian and shift dimensions must match")
        dimension = hamiltonian.shape[0]
        if hamiltonian.shape != (dimension, dimension):
            raise ValueError("reduced_hamiltonian and shift must be square")
        if reduced_hamiltonian.unit != shift.unit:
            raise ValueError("reduced_hamiltonian and shift units must match")
        physical_kinetic = hamiltonian.copy()
        physical_potential = np.zeros_like(hamiltonian)
        alternative_kinetic = hamiltonian - shift_matrix
        alternative_potential = shift_matrix.copy()
        physical_residual = hamiltonian - physical_kinetic - physical_potential
        alternative_residual = (
            hamiltonian - alternative_kinetic - alternative_potential
        )
        unit = reduced_hamiltonian.unit
        return DecompositionIdentifiabilityResult(
            physical_kinetic=MatrixQuantity(physical_kinetic, unit),
            physical_potential=MatrixQuantity(physical_potential, unit),
            alternative_kinetic=MatrixQuantity(alternative_kinetic, unit),
            alternative_potential=MatrixQuantity(alternative_potential, unit),
            physical_reconstruction_error=ScalarQuantity(
                float(np.linalg.norm(physical_residual, ord="fro")), unit
            ),
            alternative_reconstruction_error=ScalarQuantity(
                float(np.linalg.norm(alternative_residual, ord="fro")), unit
            ),
            model_class_fits=self.model_fitter.execute(shift),
        )
