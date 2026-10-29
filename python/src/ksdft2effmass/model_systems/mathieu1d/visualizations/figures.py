"""Mathieu1D scientific figure composition."""

from __future__ import annotations

from dataclasses import dataclass

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from ksdft2effmass.visualizations import BaseFigure, BasePlot, BaseSubplot

from .data import Mathieu1dVisualizationData


@dataclass(frozen=True, slots=True)
class Mathieu1dRefinementPlot(BasePlot):
    """Draw represented plane-wave and finite-difference refinement errors."""

    data: Mathieu1dVisualizationData

    def draw(self, axis: Axes) -> None:
        """Draw both finite-refinement inventories on one logarithmic axis."""
        axis.plot(
            self.data.plane_wave_cutoffs,
            self.data.plane_wave_maximum_errors.magnitude,
            "o-",
            label="plane-wave cutoff",
        )
        axis.plot(
            np.arange(len(self.data.finite_difference_points)),
            self.data.finite_difference_maximum_errors.magnitude,
            "s--",
            label="finite-difference grid",
        )


@dataclass(frozen=True, slots=True)
class Mathieu1dBandPlot(BasePlot):
    """Draw the evaluation band and recorded finite-range reconstructions."""

    data: Mathieu1dVisualizationData

    def draw(self, axis: Axes) -> None:
        """Draw explicitly ordered evaluation samples without interpolation claims."""
        coordinates = self.data.evaluation_reduced_momenta.magnitude
        axis.plot(
            coordinates,
            self.data.evaluation_selected_energies.magnitude,
            color="black",
            linewidth=2.0,
            label="finite parent band",
        )
        # The overview intentionally displays the first, middle, and last authored
        # ranges. This is a presentation selection, not a scientific acceptance rule.
        selected_indices = sorted(
            {0, len(self.data.hopping_ranges) // 2, len(self.data.hopping_ranges) - 1}
        )
        for index in selected_indices:
            axis.plot(
                coordinates,
                self.data.evaluation_candidates.magnitude[index],
                linewidth=1.0,
                label=f"range {self.data.hopping_ranges[index]}",
            )


@dataclass(frozen=True, slots=True)
class Mathieu1dHoppingPlot(BasePlot):
    """Draw complete finite-mesh hopping magnitudes."""

    data: Mathieu1dVisualizationData

    def draw(self, axis: Axes) -> None:
        """Draw the complete recorded representative inventory."""
        axis.plot(
            self.data.complete_representatives,
            self.data.complete_hopping_magnitudes.magnitude,
            "o",
            markersize=3,
            label="complete transform",
        )


@dataclass(frozen=True, slots=True)
class Mathieu1dRangePlot(BasePlot):
    """Draw finite range errors, omitted norm, and route defect."""

    data: Mathieu1dVisualizationData

    def draw(self, axis: Axes) -> None:
        """Draw only recorded range-indexed diagnostics."""
        ranges = self.data.hopping_ranges
        for values, marker, label in (
            (self.data.training_maximum_errors.magnitude, "o-", "training error"),
            (self.data.evaluation_maximum_errors.magnitude, "s-", "evaluation error"),
            (self.data.omitted_block_l2_norms.magnitude, "^-", "omitted norm"),
            (
                self.data.route_coefficient_l2_defects.magnitude,
                "d--",
                "route defect",
            ),
        ):
            axis.plot(ranges, values, marker, label=label)


@dataclass(frozen=True, slots=True)
class Mathieu1dRefinementSubplot(BaseSubplot):
    """Compose the finite representation-refinement subplot."""

    plot: Mathieu1dRefinementPlot

    def draw(self, axis: Axes) -> None:
        """Draw and label finite refinement errors."""
        self.plot.draw(axis)
        axis.set_title("Finite representation refinement")
        axis.set_xlabel("cutoff or ordered grid index")
        axis.set_ylabel("maximum absolute energy defect")
        axis.set_yscale("symlog", linthresh=1.0e-18)
        axis.grid(True, alpha=0.25)
        axis.legend(fontsize=8)


@dataclass(frozen=True, slots=True)
class Mathieu1dBandSubplot(BaseSubplot):
    """Compose the finite band-reconstruction subplot."""

    plot: Mathieu1dBandPlot

    def draw(self, axis: Axes) -> None:
        """Draw and label parent and range-reconstructed bands."""
        self.plot.draw(axis)
        axis.set_title("Finite evaluation inventory")
        axis.set_xlabel("reduced momentum")
        axis.set_ylabel("dimensionless energy")
        axis.grid(True, alpha=0.25)
        axis.legend(fontsize=8)


@dataclass(frozen=True, slots=True)
class Mathieu1dHoppingSubplot(BaseSubplot):
    """Compose the complete hopping-magnitude subplot."""

    plot: Mathieu1dHoppingPlot

    def draw(self, axis: Axes) -> None:
        """Draw and label complete finite-transform magnitudes."""
        self.plot.draw(axis)
        axis.set_title("Complete finite transform")
        axis.set_xlabel("cell representative")
        axis.set_ylabel("hopping magnitude")
        axis.set_yscale("symlog", linthresh=1.0e-18)
        axis.grid(True, alpha=0.25)
        axis.legend(fontsize=8)


@dataclass(frozen=True, slots=True)
class Mathieu1dRangeSubplot(BaseSubplot):
    """Compose the range-diagnostic subplot."""

    plot: Mathieu1dRangePlot

    def draw(self, axis: Axes) -> None:
        """Draw and label the explicit finite range inventory."""
        self.plot.draw(axis)
        axis.set_title("Finite-range diagnostics")
        axis.set_xlabel("maximum range")
        axis.set_ylabel("recorded magnitude")
        axis.set_yscale("symlog", linthresh=1.0e-18)
        axis.grid(True, alpha=0.25)
        axis.legend(fontsize=8)


@dataclass(frozen=True, slots=True)
class Mathieu1dFiniteReductionFigure(BaseFigure):
    """Compose the four-panel native Mathieu1D figure."""

    refinement: Mathieu1dRefinementSubplot
    bands: Mathieu1dBandSubplot
    hoppings: Mathieu1dHoppingSubplot
    ranges: Mathieu1dRangeSubplot

    def draw(self) -> Figure:
        """Return the complete in-memory figure."""
        figure, axes = plt.subplots(2, 2, figsize=(12.0, 8.0), constrained_layout=True)
        self.refinement.draw(axes[0, 0])
        self.bands.draw(axes[0, 1])
        self.hoppings.draw(axes[1, 0])
        self.ranges.draw(axes[1, 1])
        figure.suptitle("Mathieu1D finite reduction — authenticated data")
        return figure


@dataclass(frozen=True, slots=True)
class Mathieu1dPublicationSummaryFigure(BaseFigure):
    """Compose the compact publication-facing finite-range summary."""

    data: Mathieu1dVisualizationData

    def draw(self) -> Figure:
        """Return the two-panel summary using authenticated recorded values only."""
        ranges = self.data.hopping_ranges
        figure, axes = plt.subplots(
            1,
            2,
            figsize=(8.4, 3.4),
            constrained_layout=True,
        )
        axes[0].plot(
            ranges,
            self.data.training_maximum_errors.magnitude,
            "o-",
            label="training maximum",
        )
        axes[0].plot(
            ranges,
            self.data.evaluation_maximum_errors.magnitude,
            "s--",
            label="evaluation maximum",
        )
        axes[0].set(
            xlabel="maximum hopping range",
            ylabel="absolute error (dimensionless)",
            yscale="log",
        )
        axes[0].grid(True, alpha=0.25)
        axes[0].legend(frameon=False)
        axes[1].plot(
            ranges,
            self.data.omitted_block_l2_norms.magnitude,
            "o-",
            color="tab:purple",
        )
        axes[1].set(
            xlabel="maximum hopping range",
            ylabel="omitted-block norm (dimensionless)",
            yscale="log",
        )
        axes[1].grid(True, alpha=0.25)
        figure.suptitle("Mathieu1D finite-range reduction — authenticated data")
        return figure
