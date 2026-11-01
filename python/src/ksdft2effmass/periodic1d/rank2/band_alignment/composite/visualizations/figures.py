"""Rank-two composite-alignment scientific figures."""

from __future__ import annotations

from dataclasses import dataclass

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure

from ksdft2effmass.visualizations import BaseFigure

from .data import Periodic1DCompositeBandAlignmentVisualizationData

_PLOT_FLOOR = 1.0e-18


def _positive(values: np.ndarray) -> np.ndarray:
    """Return positive display coordinates without changing retained data."""
    return np.asarray(np.maximum(values, _PLOT_FLOOR), dtype=np.float64)


@dataclass(frozen=True, slots=True)
class _AlignmentFigure(BaseFigure):
    data: Periodic1DCompositeBandAlignmentVisualizationData

    def draw(self) -> Figure:
        figure, axes = plt.subplots(1, 2, figsize=(12.0, 4.6), constrained_layout=True)
        coordinates = self.data.evaluation_reduced_momenta.magnitude
        spectrum = self.data.evaluation_parent_spectrum.magnitude
        axes[0].plot(coordinates, spectrum[:, 0], label="retained band 1")
        axes[0].plot(coordinates, spectrum[:, 1], label="retained band 2")
        axes[0].set_xlabel("reduced momentum")
        axes[0].set_ylabel("energy / $E_{\\mathrm{ref}}$")
        axes[0].set_title("Parent retained spectrum")
        axes[0].legend()
        positions = np.arange(len(self.data.diagnostic_names), dtype=np.float64)
        axes[1].bar(positions, self.data.diagnostic_values.magnitude)
        axes[1].set_xticks(
            positions, self.data.diagnostic_names, rotation=25, ha="right"
        )
        axes[1].set_yscale("log")
        axes[1].set_ylabel("dimensionless defect")
        axes[1].set_title("Alignment diagnostics")
        figure.suptitle("Rank-two composite-band alignment")
        return figure


@dataclass(frozen=True, slots=True)
class _LocalityFigure(BaseFigure):
    data: Periodic1DCompositeBandAlignmentVisualizationData

    def draw(self) -> Figure:
        figure, axes = plt.subplots(1, 2, figsize=(12.0, 4.6), constrained_layout=True)
        ranges = np.asarray(self.data.maximum_ranges, dtype=np.int64)
        for index, channel in enumerate(self.data.channel_names):
            axes[0].semilogy(
                ranges,
                self.data.evaluation_total_spectral_maximum_errors.magnitude[:, index],
                marker="o",
                label=channel,
            )
            axes[1].semilogy(
                self.data.transform_representatives,
                self.data.hopping_block_frobenius_norms.magnitude[index],
                marker=".",
                label=channel,
            )
        axes[0].set_xlabel("retained support radius S")
        axes[0].set_ylabel("evaluation spectral maximum error / $E_{\\mathrm{ref}}$")
        axes[0].set_title("Finite-support spectral error")
        axes[0].legend()
        axes[1].set_xlabel("ordinary translation index n")
        axes[1].set_ylabel("block Frobenius norm / $E_{\\mathrm{ref}}$")
        axes[1].set_title("Hopping-block norm by translation")
        axes[1].legend()
        figure.suptitle("Rank-two composite-band block locality")
        return figure


@dataclass(frozen=True, slots=True)
class _HoppingDiagnosticFigure(BaseFigure):
    data: Periodic1DCompositeBandAlignmentVisualizationData

    def draw(self) -> Figure:
        figure, axis = plt.subplots(figsize=(7.8, 5.2), constrained_layout=True)
        ranges = np.asarray(
            self.data.hopping_diagnostic_range_inventory.maximum_ranges,
            dtype=np.int64,
        )
        for channel_index, channel in enumerate(self.data.channel_names):
            axis.semilogy(
                ranges,
                _positive(
                    self.data.ordinary_omitted_block_l2_norms.magnitude[
                        :, channel_index
                    ]
                ),
                marker="o",
                label=channel,
            )
        axis.set_xlabel("hopping-diagnostic cutoff S")
        axis.set_ylabel("ordinary omitted-block L2 norm / $E_{\\mathrm{ref}}$")
        axis.set_title("Hopping-tail diagnostics from unchanged coefficients")
        axis.grid(True, which="both", alpha=0.2)
        axis.legend()
        return figure


@dataclass(frozen=True, slots=True)
class _ErrorChannelFigure(BaseFigure):
    data: Periodic1DCompositeBandAlignmentVisualizationData

    def draw(self) -> Figure:
        figure, axes = plt.subplots(1, 3, figsize=(15.0, 4.6), constrained_layout=True)
        ranges = np.asarray(self.data.maximum_ranges, dtype=np.int64)
        attacked_index = self.data.channel_names.index("attacked")
        positions = np.arange(len(self.data.channel_names), dtype=np.float64)
        axes[0].bar(positions, self.data.cyclic_conversion_powers.magnitude)
        axes[0].set_xticks(positions, self.data.channel_names, rotation=20, ha="right")
        axes[0].set_yscale("log")
        axes[0].set_ylabel("conversion power / $E_{\\mathrm{ref}}^2$")
        axes[0].set_title("Cyclic Nyquist conversion")
        interpolation_hamiltonian = (
            self.data.evaluation_interpolation_hamiltonian_maximum_errors.magnitude[
                attacked_index
            ]
        )
        axes[1].semilogy(
            ranges,
            np.full(ranges.shape, interpolation_hamiltonian),
            marker="o",
            label="interpolation",
        )
        axes[1].semilogy(
            ranges,
            self.data.evaluation_truncation_hamiltonian_maximum_errors.magnitude[
                :, attacked_index
            ],
            marker="o",
            label="truncation",
        )
        axes[1].semilogy(
            ranges,
            self.data.evaluation_total_hamiltonian_maximum_errors.magnitude[
                :, attacked_index
            ],
            marker="o",
            label="total",
        )
        axes[1].set_xlabel("retained support radius S")
        axes[1].set_ylabel("normalized maximum Frobenius error")
        axes[1].set_title("Attacked Hamiltonian channels")
        axes[1].legend()
        interpolation_spectral = (
            self.data.evaluation_interpolation_spectral_maximum_errors.magnitude[
                attacked_index
            ]
        )
        axes[2].semilogy(
            ranges,
            np.full(ranges.shape, interpolation_spectral),
            marker="o",
            label="interpolation",
        )
        axes[2].semilogy(
            ranges,
            self.data.evaluation_truncation_spectral_maximum_errors.magnitude[
                :, attacked_index
            ],
            marker="o",
            label="truncation",
        )
        axes[2].semilogy(
            ranges,
            self.data.evaluation_total_spectral_maximum_errors.magnitude[
                :, attacked_index
            ],
            marker="o",
            label="total",
        )
        axes[2].set_xlabel("retained support radius S")
        axes[2].set_ylabel("maximum ordered-spectrum error / $E_{\\mathrm{ref}}$")
        axes[2].set_title("Attacked spectral channels")
        axes[2].legend()
        figure.suptitle("Rank-two composite-band error-channel decomposition")
        return figure


@dataclass(frozen=True, slots=True)
class _ErrorTrajectoryFigure(BaseFigure):
    data: Periodic1DCompositeBandAlignmentVisualizationData

    def draw(self) -> Figure:
        figure, axes = plt.subplots(
            2,
            3,
            figsize=(14.5, 8.0),
            constrained_layout=True,
            sharex=True,
        )
        ranges = np.asarray(
            self.data.support_range_inventory.maximum_ranges,
            dtype=np.int64,
        )
        for channel_index, channel in enumerate(self.data.channel_names):
            operator_interpolation = np.full(
                ranges.shape,
                self.data.evaluation_interpolation_hamiltonian_maximum_errors.magnitude[
                    channel_index
                ],
                dtype=np.float64,
            )
            spectrum_interpolation = np.full(
                ranges.shape,
                self.data.evaluation_interpolation_spectral_maximum_errors.magnitude[
                    channel_index
                ],
                dtype=np.float64,
            )
            for axis, interpolation, truncation, total in (
                (
                    axes[0, channel_index],
                    operator_interpolation,
                    self.data.evaluation_truncation_hamiltonian_maximum_errors.magnitude[
                        :, channel_index
                    ],
                    self.data.evaluation_total_hamiltonian_maximum_errors.magnitude[
                        :, channel_index
                    ],
                ),
                (
                    axes[1, channel_index],
                    spectrum_interpolation,
                    self.data.evaluation_truncation_spectral_maximum_errors.magnitude[
                        :, channel_index
                    ],
                    self.data.evaluation_total_spectral_maximum_errors.magnitude[
                        :, channel_index
                    ],
                ),
            ):
                axis.semilogy(
                    ranges,
                    _positive(total),
                    color="#2CA02C",
                    marker="o",
                    linewidth=1.4,
                    label="total",
                    zorder=2,
                )
                axis.semilogy(
                    ranges,
                    _positive(truncation),
                    color="#FF7F0E",
                    linestyle="--",
                    marker="s",
                    markerfacecolor="none",
                    markeredgewidth=1.1,
                    linewidth=2.0,
                    label="truncation",
                    zorder=3,
                )
                axis.semilogy(
                    ranges,
                    _positive(interpolation),
                    color="#1F77B4",
                    linestyle=":",
                    linewidth=2.0,
                    label="interpolation",
                    zorder=4,
                )
                axis.grid(True, which="both", alpha=0.2)
            axes[0, channel_index].set_title(channel)
            axes[1, channel_index].set_xlabel("retained support radius S")
        axes[0, 0].set_ylabel("normalized maximum Frobenius error")
        axes[1, 0].set_ylabel("maximum ordered-spectrum error / $E_{\\mathrm{ref}}$")
        handles, labels = axes[0, 0].get_legend_handles_labels()
        ordered_labels = ("interpolation", "truncation", "total")
        axes[0, 0].legend(
            tuple(handles[labels.index(label)] for label in ordered_labels),
            ordered_labels,
            loc="best",
        )
        figure.suptitle("Rank-two support-truncation error trajectories")
        return figure


@dataclass(frozen=True, slots=True)
class _RecoveryControlFigure(BaseFigure):
    data: Periodic1DCompositeBandAlignmentVisualizationData

    def draw(self) -> Figure:
        figure, axis = plt.subplots(figsize=(8.0, 5.2), constrained_layout=True)
        labels = ("attacked", "pointwise", "global unitary")
        frame_names = ("attack frame", "pointwise frame", "global frame")
        operator_names = (
            "attack operator",
            "pointwise operator",
            "global operator",
        )
        values = self.data.diagnostic_values.magnitude
        frame_values = np.asarray(
            [values[self.data.diagnostic_names.index(name)] for name in frame_names],
            dtype=np.float64,
        )
        operator_values = np.asarray(
            [values[self.data.diagnostic_names.index(name)] for name in operator_names],
            dtype=np.float64,
        )
        positions = np.arange(len(labels), dtype=np.float64)
        width = 0.36
        axis.bar(
            positions - width / 2.0,
            _positive(frame_values),
            width,
            label="frame defect",
        )
        axis.bar(
            positions + width / 2.0,
            _positive(operator_values),
            width,
            label="represented-operator defect",
        )
        axis.set_xticks(positions, labels)
        axis.set_yscale("log")
        axis.set_ylabel("dimensionless maximum defect")
        axis.set_title("Frame and represented-operator controls")
        axis.grid(True, which="both", axis="y", alpha=0.2)
        axis.legend()
        return figure
