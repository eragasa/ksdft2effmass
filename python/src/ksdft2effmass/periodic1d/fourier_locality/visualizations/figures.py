"""Rank-one Fourier-locality scientific figures."""

from __future__ import annotations

from dataclasses import dataclass

import matplotlib.pyplot as plt
from matplotlib.figure import Figure

from ksdft2effmass.visualizations import BaseFigure

from .data import Periodic1DFourierLocalityVisualizationData


@dataclass(frozen=True, slots=True)
class Periodic1DFourierLocalityFigure(BaseFigure):
    """Compose parent, coefficient, error-channel, and refinement panels."""

    data: Periodic1DFourierLocalityVisualizationData

    def draw(self) -> Figure:
        """Return the complete eight-panel scientific figure."""
        figure, axes = plt.subplots(4, 2, figsize=(12.0, 14.0), constrained_layout=True)
        momenta = self.data.evaluation_reduced_momenta.magnitude
        axes[0, 0].plot(
            momenta, self.data.evaluation_lowest_energies.magnitude, label="lowest"
        )
        axes[0, 0].plot(
            momenta, self.data.evaluation_adjacent_energies.magnitude, label="adjacent"
        )
        axes[0, 0].set(
            xlabel="reduced momentum",
            ylabel="energy / E_ref",
            title="Sampled parent bands",
        )
        axes[0, 0].legend(frameon=False)
        axes[0, 1].plot(
            momenta,
            self.data.evaluation_sampled_gaps.magnitude,
            label="evaluation",
        )
        axes[0, 1].plot(
            self.data.production_reduced_momenta.magnitude,
            self.data.production_sampled_gaps.magnitude,
            label="production construction",
        )
        axes[0, 1].axhline(
            self.data.sampled_gap_threshold.magnitude,
            color="black",
            linestyle="--",
            label="sampled-gap threshold",
        )
        axes[0, 1].axhline(
            self.data.minimum_sampled_gap.magnitude,
            color="tab:red",
            linestyle=":",
            label="sampled minimum",
        )
        axes[0, 1].set(
            xlabel="reduced momentum",
            ylabel="first-to-second gap / E_ref",
            title="Finite sampled-gap qualification",
        )
        axes[0, 1].legend(frameon=False, fontsize=8)
        axes[1, 0].plot(
            self.data.production_complete_representatives,
            self.data.production_complete_coefficient_magnitudes.magnitude,
            "o-",
        )
        axes[1, 0].set(
            xlabel="cell representative",
            ylabel="coefficient magnitude / E_ref",
            yscale="log",
            title="Production complete transform",
        )
        axes[1, 1].plot(
            self.data.construction_sizes,
            self.data.interpolation_maximum_errors.magnitude,
            "o-",
            label="interpolation maximum",
        )
        axes[1, 1].plot(
            self.data.construction_sizes[1:],
            self.data.refinement_maximum_changes.magnitude,
            "s--",
            label="adjacent-mesh maximum change",
        )
        axes[1, 1].set(
            xlabel="fine construction size",
            ylabel="recorded magnitude / E_ref",
            xscale="log",
            yscale="log",
            title="Mesh and refinement diagnostics",
        )
        axes[1, 1].legend(frameon=False, fontsize=8)
        production_index = len(self.data.construction_sizes) - 1
        ranges = self.data.maximum_ranges
        axes[2, 0].plot(
            ranges,
            self.data.truncation_maximum_errors.magnitude[production_index],
            "o-",
            label="truncation",
        )
        axes[2, 0].plot(
            ranges,
            self.data.mediated_total_maximum_errors.magnitude[production_index],
            "s--",
            label="mediated total",
        )
        axes[2, 0].plot(
            ranges,
            self.data.direct_total_maximum_errors.magnitude[production_index],
            "^:",
            label="direct total",
        )
        axes[2, 0].axhline(
            self.data.application_threshold.magnitude,
            color="black",
            linestyle="--",
            label="application threshold",
        )
        axes[2, 0].set(
            xlabel="maximum range",
            ylabel="maximum error / E_ref",
            yscale="log",
            title="Production finite-range errors",
        )
        axes[2, 0].legend(frameon=False, fontsize=8)
        for mesh_index, mesh_size in enumerate(self.data.construction_sizes):
            axes[2, 1].plot(
                ranges,
                self.data.omitted_coefficient_l2_norms.magnitude[mesh_index],
                "o-",
                label=f"N={mesh_size}",
            )
        axes[2, 1].set(
            xlabel="maximum range",
            ylabel="omitted coefficient L2 norm / E_ref",
            yscale="log",
            title="Omitted finite-transform norm",
        )
        axes[2, 1].legend(frameon=False, fontsize=8)
        production_errors = self.data.mediated_total_maximum_errors.magnitude[
            production_index
        ]
        axes[3, 0].plot(ranges, production_errors, "o-", label="attained table")
        nondominated = self.data.nondominated_masks[production_index]
        near_tie = self.data.near_tie_masks[production_index]
        axes[3, 0].scatter(
            [
                value
                for value, retained in zip(ranges, nondominated, strict=True)
                if retained
            ],
            [
                value
                for value, retained in zip(production_errors, nondominated, strict=True)
                if retained
            ],
            marker="D",
            label="nondominated",
        )
        axes[3, 0].scatter(
            [
                value
                for value, retained in zip(ranges, near_tie, strict=True)
                if retained
            ],
            [
                value
                for value, retained in zip(production_errors, near_tie, strict=True)
                if retained
            ],
            marker="x",
            label="near tie",
        )
        axes[3, 0].axhline(
            self.data.application_threshold.magnitude,
            color="black",
            linestyle="--",
        )
        axes[3, 0].set(
            xlabel="maximum range",
            ylabel="mediated total maximum error / E_ref",
            yscale="log",
            title="Attained support/error locality",
        )
        axes[3, 0].legend(frameon=False, fontsize=8)
        passage_values = [
            float("nan") if value is None else float(value)
            for value in self.data.first_joint_passes
        ]
        for mesh_size, passage, sustained in zip(
            self.data.construction_sizes,
            passage_values,
            self.data.sustained_after_first_passes,
            strict=True,
        ):
            axes[3, 1].scatter(
                mesh_size,
                passage,
                marker="o" if sustained else "x",
                color="tab:green" if sustained else "tab:red",
            )
        axes[3, 1].plot(self.data.construction_sizes, passage_values, color="0.5")
        axes[3, 1].set(
            xlabel="construction size",
            ylabel="first jointly passing maximum range",
            title="Threshold passage and sustained status",
        )
        for axis in axes.flat:
            axis.grid(True, alpha=0.25)
        figure.suptitle("Rank-one Fourier locality — authenticated data")
        return figure


@dataclass(frozen=True, slots=True)
class Periodic1DFourierRouteAgreementFigure(BaseFigure):
    """Compose coefficient-space and sampled route-agreement panels."""

    data: Periodic1DFourierLocalityVisualizationData

    def draw(self) -> Figure:
        """Return the complete four-panel route-agreement figure."""
        figure, axes = plt.subplots(2, 2, figsize=(11.0, 8.0), constrained_layout=True)
        ranges = self.data.maximum_ranges
        for mesh_index, mesh_size in enumerate(self.data.construction_sizes):
            label = f"N={mesh_size}"
            axes[0, 0].plot(
                ranges,
                self.data.coefficient_l2_defects.magnitude[mesh_index],
                "o-",
                label=label,
            )
            axes[0, 1].plot(
                ranges,
                self.data.sampled_maximum_defects.magnitude[mesh_index],
                "o-",
                label=label,
            )
            axes[1, 0].plot(
                ranges,
                self.data.mediated_total_maximum_errors.magnitude[mesh_index],
                "o-",
                label=label,
            )
            axes[1, 1].plot(
                ranges,
                self.data.direct_total_maximum_errors.magnitude[mesh_index],
                "o-",
                label=label,
            )
        axes[0, 0].set(
            xlabel="maximum range",
            ylabel="coefficient L2 defect / E_ref",
            yscale="symlog",
            title="Mediated versus direct coefficients",
        )
        axes[0, 1].set(
            xlabel="maximum range",
            ylabel="sampled maximum defect / E_ref",
            yscale="symlog",
            title="Construction-mesh route agreement",
        )
        axes[1, 0].set(
            xlabel="maximum range",
            ylabel="mediated total maximum error / E_ref",
            yscale="log",
            title="Transform-mediated total error",
        )
        axes[1, 1].set(
            xlabel="maximum range",
            ylabel="direct total maximum error / E_ref",
            yscale="log",
            title="Direct-fit total error",
        )
        for axis in axes[1]:
            axis.axhline(
                self.data.application_threshold.magnitude,
                color="black",
                linestyle="--",
            )
        for axis in axes.flat:
            axis.grid(True, alpha=0.25)
            axis.legend(frameon=False, fontsize=8)
        figure.suptitle("Rank-one Fourier route agreement — authenticated data")
        return figure
