"""Closed PIAB1D figure inventory."""

from enum import Enum


class Piab1dVisualizationPlotEnum(Enum):
    """Enumerate the complete maintained PIAB1D plot migration target."""

    spectrum_and_states = "spectrum-and-states.png"
    residual_matrices = "residual-matrices.png"
    continuum_wavefunction_ladder = "figure_01a_continuum_wavefunction_ladder.png"
    discrete_wavefunction_ladder = "figure_01b_discrete_wavefunction_ladder.png"
    retained_dimension_selection = "figure_02_retained_dimension_selection.png"
    convergence_series = "convergence-series.png"
    convergence_mode_sweep = "convergence-mode-sweep.png"
    higher_eigenpair_sweep = "higher-eigenpair-sweep.png"
    higher_mode_convergence = "higher-mode-convergence.png"
    operator_residual_norms = "operator-residual-norms.png"
    eigensolver_residual_norms = "eigensolver-residual-norms.png"
    finite_algebraic_diagnostics = "finite-algebraic-diagnostics.png"
    kinetic_potential_decomposition = "kinetic-potential-decomposition.png"
