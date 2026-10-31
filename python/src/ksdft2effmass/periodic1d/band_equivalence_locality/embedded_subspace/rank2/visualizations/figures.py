"""Scientific figures for authenticated embedded rank-two projections."""

from __future__ import annotations

from dataclasses import dataclass

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure

from ksdft2effmass.visualizations import BaseFigure

from ..retention.visualization_data import (
    Periodic1DRank2CalculationVisualizationData,
    Periodic1DRank2ParentFamilyVisualizationData,
    Periodic1DRank2VisualizationData,
)


@dataclass(frozen=True, slots=True)
class _MomentumRefinementFigure(BaseFigure):
    data: Periodic1DRank2CalculationVisualizationData

    def draw(self) -> Figure:
        """Plot each independently retained mesh-refinement channel."""
        figure, axis = plt.subplots(figsize=(9.0, 5.2), constrained_layout=True)
        for label, values in zip(
            self.data.MOMENTUM_CHANNELS,
            self.data.momentum_defects,
            strict=True,
        ):
            axis.plot(self.data.momentum_fine_mesh_sizes, values, "o-", label=label)
        failed = tuple(
            size
            for size, passed in zip(
                self.data.momentum_fine_mesh_sizes,
                self.data.momentum_within_tolerances,
                strict=True,
            )
            if not passed
        )
        for size in failed:
            axis.axvline(size, color="black", alpha=0.12, linewidth=5.0)
        axis.set(
            xlabel="fine reciprocal-mesh size",
            ylabel="separate maximum defect or change",
            xscale="log",
            yscale="symlog",
            title="Embedded rank-two momentum refinement",
        )
        axis.grid(True, alpha=0.25)
        axis.legend(frameon=False, fontsize=7, ncol=2)
        return figure


@dataclass(frozen=True, slots=True)
class _AdaptiveAmplitudeRefinementFigure(BaseFigure):
    data: Periodic1DRank2CalculationVisualizationData

    def draw(self) -> Figure:
        """Plot midpoint and disjoint quarter-point defects separately."""
        figure, axes = plt.subplots(1, 2, figsize=(12.0, 4.8), constrained_layout=True)
        for label, midpoint in zip(
            self.data.AMPLITUDE_CHANNELS,
            self.data.adaptive_midpoint_defects,
            strict=True,
        ):
            axes[0].plot(
                self.data.adaptive_level_indices,
                midpoint,
                "o-",
                label=label,
            )
        if self.data.adaptive_validation_level_indices:
            for label, validation in zip(
                self.data.AMPLITUDE_CHANNELS,
                self.data.adaptive_validation_defects,
                strict=True,
            ):
                axes[1].plot(
                    self.data.adaptive_validation_level_indices,
                    validation,
                    "s--",
                    label=label,
                )
        else:
            axes[1].text(
                0.5,
                0.5,
                "No disjoint validation retained",
                ha="center",
                va="center",
                transform=axes[1].transAxes,
            )
        axes[0].set(title="Midpoint refinement")
        axes[1].set(title="Disjoint quarter-point validation")
        for axis in axes:
            axis.set(
                xlabel="adaptive level",
                ylabel="separate maximum interpolation defect",
                yscale="symlog",
            )
            axis.grid(True, alpha=0.25)
        axes[0].legend(frameon=False, fontsize=7)
        if self.data.adaptive_validation_level_indices:
            axes[1].legend(frameon=False, fontsize=7)
        figure.suptitle("Embedded rank-two adaptive-amplitude refinement")
        return figure


@dataclass(frozen=True, slots=True)
class _TruncationConsequencesFigure(BaseFigure):
    data: Periodic1DRank2CalculationVisualizationData

    def draw(self) -> Figure:
        """Plot omitted power, finite-range error, and interpolation channels."""
        figure, axes = plt.subplots(1, 3, figsize=(16.0, 4.8), constrained_layout=True)
        for label, values in zip(
            self.data.TRUNCATION_POWER_CHANNELS,
            self.data.truncation_omitted_powers,
            strict=True,
        ):
            axes[0].plot(
                self.data.truncation_maximum_ranges,
                values,
                "o-",
                label=label,
            )
        for label, values in zip(
            self.data.TRUNCATION_ERROR_CHANNELS,
            self.data.truncation_maximum_errors,
            strict=True,
        ):
            axes[1].plot(
                self.data.truncation_maximum_ranges,
                values,
                "o-",
                label=label,
            )
        for label, values in zip(
            self.data.INTERPOLATION_CHANNELS,
            self.data.truncation_interpolation_maximum_errors,
            strict=True,
        ):
            axes[2].plot(
                self.data.truncation_amplitudes,
                values,
                "o-",
                label=label,
            )
        axes[0].set(title="Omitted hopping power", xlabel="maximum ordinary range")
        axes[1].set(title="Finite-range consequences", xlabel="maximum ordinary range")
        axes[2].set(title="Interpolation controls", xlabel="gauge amplitude / rad")
        for axis in axes:
            axis.set(yscale="symlog", ylabel="separate maximum channel")
            axis.grid(True, alpha=0.25)
            axis.legend(frameon=False, fontsize=6)
        figure.suptitle("Embedded rank-two truncation consequences")
        return figure


@dataclass(frozen=True, slots=True)
class _BandAndAlignmentFigure(BaseFigure):
    data: Periodic1DRank2VisualizationData

    def draw(self) -> Figure:
        """Plot the band-equivalence and restricted-alignment channels."""
        figure, axes = plt.subplots(1, 3, figsize=(14.0, 4.2), constrained_layout=True)
        axes[0].plot(self.data.amplitudes, self.data.band_defects, "o-")
        axes[0].set(
            xlabel="gauge-attack amplitude / rad",
            ylabel="maximum sorted-band defect / E_ref",
            yscale="symlog",
            title="Retained-band equivalence",
        )
        axes[1].plot(self.data.amplitudes, self.data.correlations, "o-")
        axes[1].set(
            xlabel="gauge-attack amplitude / rad",
            ylabel="maximum correlation",
            title="Restricted global alignment",
        )
        axes[2].plot(
            self.data.amplitudes,
            self.data.operator_thresholds,
            "s--",
            label="operator threshold",
        )
        axes[2].plot(
            self.data.amplitudes,
            self.data.joint_thresholds,
            "^--",
            label="exact-spectrum joint threshold",
        )
        axes[2].set(
            xlabel="gauge-attack amplitude / rad",
            ylabel="normalized squared loss",
            title="Separated decision thresholds",
        )
        for axis in axes:
            axis.grid(True, alpha=0.25)
        axes[2].legend(frameon=False)
        figure.suptitle("Embedded rank-two band and alignment channels")
        return figure


@dataclass(frozen=True, slots=True)
class _LocalityFigure(BaseFigure):
    data: Periodic1DRank2VisualizationData

    def draw(self) -> Figure:
        """Plot reference and attacked ordinary-lattice hopping power."""
        figure, axes = plt.subplots(1, 2, figsize=(11.0, 4.2), constrained_layout=True)
        for amplitude, reference, comparison in zip(
            self.data.amplitudes,
            self.data.reference_hopping_powers,
            self.data.comparison_hopping_powers,
            strict=True,
        ):
            axes[0].plot(
                self.data.hopping_displacements,
                reference,
                "o-",
                label=f"a={amplitude:.3f}",
            )
            axes[1].plot(
                self.data.hopping_displacements,
                comparison,
                "o-",
                label=f"a={amplitude:.3f}",
            )
        axes[0].set(title="Reference represented operator")
        axes[1].set(title="Gauge-attacked represented operator")
        for axis in axes:
            axis.set(
                xlabel="ordinary displacement",
                ylabel="normalized squared Frobenius power",
                yscale="symlog",
            )
            axis.grid(True, alpha=0.25)
            axis.legend(frameon=False, fontsize=8)
        figure.suptitle("Embedded rank-two hopping locality")
        return figure


@dataclass(frozen=True, slots=True)
class _NumericalResidualFigure(BaseFigure):
    data: Periodic1DRank2VisualizationData

    def draw(self) -> Figure:
        """Plot reconstruction and Parseval diagnostics separately."""
        figure, axes = plt.subplots(1, 2, figsize=(11.0, 4.2), constrained_layout=True)
        axes[0].plot(
            self.data.amplitudes,
            self.data.reconstruction_defects,
            "o-",
        )
        axes[0].set(title="Minimum-loss reconstruction defect")
        axes[1].plot(
            self.data.amplitudes,
            self.data.reference_parseval_defects,
            "o-",
            label="reference",
        )
        axes[1].plot(
            self.data.amplitudes,
            self.data.comparison_parseval_defects,
            "s--",
            label="comparison",
        )
        axes[1].set(title="Parseval defects")
        for axis in axes:
            axis.set(
                xlabel="gauge-attack amplitude / rad",
                ylabel="absolute numerical defect",
                yscale="symlog",
            )
            axis.grid(True, alpha=0.25)
        axes[1].legend(frameon=False)
        figure.suptitle("Embedded rank-two numerical residual channels")
        return figure


def _landscape(
    data: Periodic1DRank2ParentFamilyVisualizationData,
    values: tuple[tuple[float, ...], ...],
    *,
    title: str,
    colorbar_label: str,
) -> Figure:
    figure, axis = plt.subplots(figsize=(7.2, 4.8), constrained_layout=True)
    image = axis.imshow(
        np.asarray(values, dtype=np.float64),
        origin="lower",
        aspect="auto",
        extent=(
            data.amplitudes[0],
            data.amplitudes[-1],
            data.parent_hopping_scales[0],
            data.parent_hopping_scales[-1],
        ),
    )
    axis.set(
        xlabel="gauge-attack amplitude / rad",
        ylabel="parent hopping scale",
        title=title,
    )
    figure.colorbar(image, ax=axis, label=colorbar_label)
    return figure


@dataclass(frozen=True, slots=True)
class _FamilyAlignmentLandscapeFigure(BaseFigure):
    data: Periodic1DRank2ParentFamilyVisualizationData

    def draw(self) -> Figure:
        """Plot restricted-alignment correlation over the bounded family."""
        return _landscape(
            self.data,
            self.data.correlations,
            title="Embedded rank-two family alignment",
            colorbar_label="maximum correlation",
        )


@dataclass(frozen=True, slots=True)
class _FamilyLocalityLandscapeFigure(BaseFigure):
    data: Periodic1DRank2ParentFamilyVisualizationData

    def draw(self) -> Figure:
        """Plot attacked nonzero hopping weight over the bounded family."""
        return _landscape(
            self.data,
            self.data.comparison_nonzero_weights,
            title="Embedded rank-two family locality",
            colorbar_label="nonzero hopping weight",
        )


@dataclass(frozen=True, slots=True)
class _FamilyQualificationFigure(BaseFigure):
    data: Periodic1DRank2ParentFamilyVisualizationData

    def draw(self) -> Figure:
        """Plot the distinct external-gap and transport qualification channels."""
        figure, axes = plt.subplots(1, 2, figsize=(11.0, 4.2), constrained_layout=True)
        axes[0].plot(
            self.data.parent_hopping_scales,
            self.data.minimum_external_gaps,
            "o-",
        )
        axes[0].set(title="Sampled minimum external gap", ylabel="gap / E_ref")
        axes[1].plot(
            self.data.parent_hopping_scales,
            self.data.minimum_transport_singular_values,
            "o-",
        )
        axes[1].set(
            title="Minimum transport singular value",
            ylabel="singular value",
        )
        for axis in axes:
            axis.set(xlabel="parent hopping scale", yscale="symlog")
            axis.grid(True, alpha=0.25)
        figure.suptitle("Embedded rank-two family qualification channels")
        return figure
