"""Rank-two composite-alignment scientific figures."""

from __future__ import annotations

from dataclasses import dataclass

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure

from ksdft2effmass.visualizations import BaseFigure

from .data import Periodic1DCompositeBandAlignmentVisualizationData


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
        axes[0].set_ylabel("energy / E_ref")
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
        axes[0].set_xlabel("maximum hopping range")
        axes[0].set_ylabel("evaluation spectral maximum error / E_ref")
        axes[0].set_title("Finite-range spectral errors")
        axes[0].legend()
        axes[1].set_xlabel("lattice representative")
        axes[1].set_ylabel("block Frobenius norm / E_ref")
        axes[1].set_title("Complete block-hopping decay")
        axes[1].legend()
        figure.suptitle("Rank-two composite-band block locality")
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
        axes[0].set_ylabel("conversion power / E_ref²")
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
        axes[1].set_xlabel("maximum hopping range")
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
        axes[2].set_xlabel("maximum hopping range")
        axes[2].set_ylabel("maximum sorted-band error / E_ref")
        axes[2].set_title("Attacked spectral channels")
        axes[2].legend()
        figure.suptitle("Rank-two composite-band error-channel decomposition")
        return figure
