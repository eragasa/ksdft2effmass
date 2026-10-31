"""Scientific figures for the flat-parent band-equivalence control."""

from __future__ import annotations

from dataclasses import dataclass

import matplotlib.pyplot as plt
from matplotlib.figure import Figure

from ksdft2effmass.visualizations import BaseFigure

from .data import Periodic1DBandEquivalenceLocalityVisualizationData


@dataclass(frozen=True, slots=True)
class _AlignmentFigure(BaseFigure):
    data: Periodic1DBandEquivalenceLocalityVisualizationData

    def draw(self) -> Figure:
        """Plot finite/analytic alignment and separated operator thresholds."""
        figure, axes = plt.subplots(1, 2, figsize=(11.0, 4.2), constrained_layout=True)
        amplitudes = self.data.amplitudes
        axes[0].plot(
            amplitudes,
            self.data.discrete_correlations,
            "o-",
            label="finite harmonic maximum",
        )
        axes[0].plot(
            amplitudes,
            self.data.analytic_correlations,
            "s--",
            label=r"analytic $|J_0(2a)|$ comparator",
        )
        axes[0].set(
            xlabel="gauge-attack amplitude / rad",
            ylabel="maximum correlation",
            title="Restricted global alignment",
        )
        axes[1].plot(
            amplitudes,
            self.data.operator_thresholds,
            "o-",
            label="operator-only threshold",
        )
        axes[1].plot(
            amplitudes,
            self.data.joint_thresholds,
            "s--",
            label="exact-spectrum joint threshold",
        )
        axes[1].set(
            xlabel="gauge-attack amplitude / rad",
            ylabel="normalized squared loss",
            title="Separated decision thresholds",
        )
        for axis in axes:
            axis.grid(True, alpha=0.25)
            axis.legend(frameon=False)
        figure.suptitle("Flat rank-two band equivalence — authenticated data")
        return figure


@dataclass(frozen=True, slots=True)
class _LocalityFigure(BaseFigure):
    data: Periodic1DBandEquivalenceLocalityVisualizationData

    def draw(self) -> Figure:
        """Plot ordinary-lattice hopping power and cyclic Nyquist power."""
        figure, axes = plt.subplots(1, 2, figsize=(11.0, 4.2), constrained_layout=True)
        for amplitude, powers in zip(
            self.data.amplitudes,
            self.data.hopping_powers,
            strict=True,
        ):
            axes[0].plot(
                self.data.hopping_displacements,
                powers,
                "o-",
                label=f"a={amplitude:.3f}",
            )
        axes[0].set(
            xlabel="ordinary displacement",
            ylabel="normalized squared Frobenius power",
            yscale="symlog",
            title="Ordinary-lattice hopping inventory",
        )
        axes[0].legend(frameon=False, fontsize=8)
        axes[1].plot(self.data.amplitudes, self.data.nyquist_powers, "o-")
        axes[1].set(
            xlabel="gauge-attack amplitude / rad",
            ylabel="normalized cyclic Nyquist power",
            yscale="symlog",
            title="Discarded self-inverse cyclic class",
        )
        for axis in axes:
            axis.grid(True, alpha=0.25)
        figure.suptitle("Gauge-induced hopping locality — authenticated data")
        return figure


@dataclass(frozen=True, slots=True)
class _ErrorChannelFigure(BaseFigure):
    data: Periodic1DBandEquivalenceLocalityVisualizationData

    def draw(self) -> Figure:
        """Plot total Hamiltonian and sorted-band consequences by range."""
        figure, axes = plt.subplots(1, 2, figsize=(11.0, 4.2), constrained_layout=True)
        for amplitude, hamiltonian, spectral in zip(
            self.data.amplitudes,
            self.data.total_hamiltonian_errors,
            self.data.total_spectral_errors,
            strict=True,
        ):
            label = f"a={amplitude:.3f}"
            axes[0].plot(self.data.maximum_ranges, hamiltonian, "o-", label=label)
            axes[1].plot(self.data.maximum_ranges, spectral, "o-", label=label)
        axes[0].set(
            xlabel="maximum ordinary range",
            ylabel="total Hamiltonian maximum error / E_ref",
            yscale="symlog",
            title="Total represented-Hamiltonian consequence",
        )
        axes[1].set(
            xlabel="maximum ordinary range",
            ylabel="total sorted-band maximum error / E_ref",
            yscale="symlog",
            title="Total spectral consequence",
        )
        for axis in axes:
            axis.grid(True, alpha=0.25)
            axis.legend(frameon=False, fontsize=8)
        figure.suptitle(
            "Interpolation and truncation consequences — authenticated data"
        )
        return figure
