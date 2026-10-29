"""Scientific figures for authenticated constrained-admissible-set data."""

from __future__ import annotations

from dataclasses import dataclass

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure

from ksdft2effmass.visualizations import BaseFigure

from .data import Periodic1DConstrainedAdmissibleSetVisualizationData


@dataclass(frozen=True, slots=True)
class _AdmissibilityFigure(BaseFigure):
    data: Periodic1DConstrainedAdmissibleSetVisualizationData

    def draw(self) -> Figure:
        figure, axes = plt.subplots(1, 2, figsize=(12.0, 4.8), constrained_layout=True)
        for point in self.data.proof_points:
            parameters = point.evaluation.parameter
            axes[0].scatter(
                parameters[0],
                parameters[1],
                label=f"{point.thresholds.case_id}: {point.disposition.value}",
            )
            axes[0].annotate(
                f"{point.evaluation.role}\n"
                f"angle={point.evaluation.selected_alignment_angle:.3g}",
                (parameters[0], parameters[1]),
                xytext=(4, 4),
                textcoords="offset points",
                fontsize="x-small",
            )
        bounds = self.data.parameter_bounds.magnitude
        axes[0].set_xlim(bounds[0, 0], bounds[0, 1])
        axes[0].set_ylim(bounds[1, 0], bounds[1, 1])
        axes[0].set_xlabel(self.data.parameter_names[0].replace("_", " "))
        axes[0].set_ylabel(self.data.parameter_names[1].replace("_", " "))
        axes[0].set_title("Witness and certificate points")
        axes[0].legend(fontsize="small")

        positions = np.arange(len(self.data.proof_points), dtype=np.float64)
        width = 0.35
        for channel_index, channel in enumerate(self.data.loss_channel_names):
            horizontal = positions + width * (channel_index - 0.5)
            training = np.asarray(
                [
                    (
                        point.evaluation.training_spectral_rms_loss,
                        point.evaluation.training_operator_rms_loss,
                    )[channel_index]
                    for point in self.data.proof_points
                ]
            )
            evaluation = np.asarray(
                [
                    (
                        point.evaluation.evaluation_spectral_rms_loss,
                        point.evaluation.evaluation_operator_rms_loss,
                    )[channel_index]
                    for point in self.data.proof_points
                ]
            )
            thresholds = np.asarray(
                [
                    (
                        point.thresholds.spectral_rms_threshold,
                        point.thresholds.operator_rms_threshold,
                    )[channel_index]
                    for point in self.data.proof_points
                ]
            )
            axes[1].bar(horizontal, training, width, label=f"training {channel}")
            axes[1].scatter(
                horizontal,
                evaluation,
                marker="x",
                color="black",
                label=f"evaluation {channel}",
            )
            axes[1].scatter(
                horizontal,
                thresholds,
                marker="_",
                s=160,
                label=f"threshold {channel}",
            )
        tick_labels = tuple(
            f"{point.evaluation.role}\nseparation "
            f"[{point.separation_bounds.magnitude[0]:.2g}, "
            f"{point.separation_bounds.magnitude[1]:.2g}]"
            for point in self.data.proof_points
        )
        axes[1].set_xticks(positions, tick_labels, rotation=20, ha="right")
        axes[1].set_ylabel("dimensionless RMS loss")
        axes[1].set_title("Training, evaluation, and threshold diagnostics")
        axes[1].legend(fontsize="x-small")
        figure.suptitle("Constrained rank-two admissible-set proof points")
        return figure


@dataclass(frozen=True, slots=True)
class _LocalityChannelsFigure(BaseFigure):
    data: Periodic1DConstrainedAdmissibleSetVisualizationData

    def draw(self) -> Figure:
        figure, axes = plt.subplots(1, 2, figsize=(12.0, 4.8), constrained_layout=True)
        for point in self.data.proof_points:
            locality = point.evaluation.locality
            ranges = np.asarray(
                [value.maximum_range for value in locality], dtype=np.int64
            )
            ordinary_channels = (
                [value.reference_ordinary_omitted_block_l2_norm for value in locality],
                [value.attacked_ordinary_omitted_block_l2_norm for value in locality],
                [value.candidate_ordinary_omitted_block_l2_norm for value in locality],
            )
            for channel_index, channel in enumerate(self.data.locality_channel_names):
                axes[0].semilogy(
                    ranges,
                    ordinary_channels[channel_index],
                    marker="o",
                    label=f"{point.evaluation.role}: {channel}",
                )
        axes[0].set_xlabel("maximum ordinary hopping range")
        axes[0].set_ylabel("ordinary omitted-block L2 norm / E_ref")
        axes[0].set_title("Deliberate ordinary-tail truncation")
        axes[0].legend(fontsize="x-small")

        positions = np.arange(len(self.data.proof_points), dtype=np.float64)
        for channel_index, channel in enumerate(self.data.locality_channel_names):
            axes[1].bar(
                positions + 0.24 * (channel_index - 1),
                [
                    (
                        point.evaluation.locality[0].reference_cyclic_conversion_power,
                        point.evaluation.locality[0].attacked_cyclic_conversion_power,
                        point.evaluation.locality[0].candidate_cyclic_conversion_power,
                    )[channel_index]
                    for point in self.data.proof_points
                ],
                0.24,
                label=channel,
            )
        axes[1].set_xticks(
            positions,
            tuple(point.evaluation.role for point in self.data.proof_points),
            rotation=20,
            ha="right",
        )
        axes[1].set_yscale("log")
        axes[1].set_ylabel("removed cyclic class power / E_ref^2")
        axes[1].set_title("Cyclic-to-ordinary conversion")
        axes[1].legend()
        figure.suptitle("Separate constrained-admissible-set locality channels")
        return figure


__all__: list[str] = []
