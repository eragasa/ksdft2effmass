"""Publication-oriented figures from one admitted complete five-scale record."""

from __future__ import annotations

import math
from dataclasses import dataclass

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import BoundaryNorm
from matplotlib.figure import Figure

from ksdft2effmass.periodic1d.band_equivalence_locality.embedded_subspace.rank2.parent_scale.results import (  # noqa: E501
    Periodic1DRank2QualifiedParent,
)
from ksdft2effmass.periodic1d.band_equivalence_locality.embedded_subspace.rank2.retention.complete_five_scale import (  # noqa: E501
    Periodic1DRank2CompleteFiveScaleCalculationRecord,
)
from ksdft2effmass.periodic1d.rank2.support_truncation.results import (
    Periodic1DRank2TruncationCompleted,
)
from ksdft2effmass.serialization import StringWireEnum
from ksdft2effmass.visualizations import (
    BaseFigure,
    PngFigureRenderer,
    PngVisualization,
)

_ERROR_FLOOR = 1.0e-18
_POWER_FLOOR = 1.0e-34
_RANGE_TARGETS = (1.0e-6, 1.0e-8, 1.0e-10, 1.0e-12)
_TAIL_RANGES = (0, 1, 2, 3, 4, 6, 8)
_BLACK = "#202020"


class Periodic1DRank2CompleteFiveScaleFigureEnum(StringWireEnum):
    """Identify the closed complete-five-scale publication figure inventory."""

    SCIENTIFIC_STORY = "band-equivalence-locality-scientific-story.png"
    RANGE_INFLATION = "range-inflation-preview.png"
    ERROR_CHANNEL_DECOMPOSITION = "truncation-error-channel-decomposition.png"


@dataclass(frozen=True, slots=True)
class Periodic1DRank2CompleteFiveScaleFigureData:
    """Bind admitted values needed by the complete-five-scale figure inventory."""

    source_sha256: str
    record: Periodic1DRank2CompleteFiveScaleCalculationRecord

    def __post_init__(self) -> None:
        if (
            type(self.source_sha256) is not str
            or len(self.source_sha256) != 64
            or any(
                character not in "0123456789abcdef"
                for character in self.source_sha256
            )
        ):
            raise ValueError("source_sha256 must be a lowercase SHA-256 digest")
        if type(self.record) is not Periodic1DRank2CompleteFiveScaleCalculationRecord:
            raise TypeError("record must be a complete-five-scale calculation record")
        parent_request = self.record.parent_family.request
        if parent_request.parent_hopping_scales != (0.0, 0.25, 0.5, 0.75, 1.0):
            raise ValueError(
                "figures require the declared complete five-scale inventory"
            )
        amplitudes = parent_request.template_request.amplitudes
        selected_amplitudes = (
            amplitudes[0],
            amplitudes[len(amplitudes) // 2],
            amplitudes[-1],
        )
        if selected_amplitudes != (0.0, math.pi / 8.0, math.pi / 4.0):
            raise ValueError("figures require amplitudes spanning 0 through pi/4")
        if any(
            type(member.qualification) is not Periodic1DRank2QualifiedParent
            for member in self.record.parent_family.members
        ):
            raise ValueError("figures require a fully qualified parent family")
        if any(
            type(member) is not Periodic1DRank2TruncationCompleted
            for member in self.record.principal_truncation_family.members
        ):
            raise ValueError("figures require complete principal truncation outcomes")

    @classmethod
    def from_record(
        cls,
        record: Periodic1DRank2CompleteFiveScaleCalculationRecord,
        *,
        source_sha256: str,
    ) -> Periodic1DRank2CompleteFiveScaleFigureData:
        """Construct figure data without rerunning any scientific analysis."""
        return cls(source_sha256=source_sha256, record=record)


@dataclass(frozen=True, slots=True)
class _ScientificStoryFigure(BaseFigure):
    data: Periodic1DRank2CompleteFiveScaleFigureData

    def draw(self) -> Figure:
        record = self.data.record
        family = record.parent_family
        scales = family.request.parent_hopping_scales
        colors = plt.get_cmap("viridis")(np.linspace(0.08, 0.92, len(scales)))
        style = {
            "font.family": "DejaVu Sans",
            "font.size": 7.2,
            "axes.titlesize": 8.2,
            "axes.labelsize": 7.7,
            "axes.linewidth": 0.7,
            "xtick.labelsize": 6.8,
            "ytick.labelsize": 6.8,
            "legend.fontsize": 5.9,
            "lines.linewidth": 1.3,
        }
        with mpl.rc_context(style):  # type: ignore[arg-type]
            figure, axes = plt.subplots(
                2, 3, figsize=(7.2, 5.15), constrained_layout=True
            )
            flat_axes = axes.ravel()
            for scale, color, member in zip(
                scales, colors, family.members, strict=True
            ):
                amplitudes = tuple(point.amplitude for point in member.points)
                label = rf"$\rho={scale:g}$"
                flat_axes[0].semilogy(
                    amplitudes,
                    np.maximum(
                        tuple(point.maximum_band_defect for point in member.points),
                        _ERROR_FLOOR,
                    ),
                    color=color,
                    marker="o",
                    markevery=4,
                    markersize=2.2,
                    label=label,
                )
                thresholds = tuple(
                    point.minimum_operator_threshold
                    / math.sqrt(point.splitting_scale)
                    for point in member.points
                )
                excess = tuple(
                    (
                        point.comparison_nonzero_hopping_weight
                        - point.reference_nonzero_hopping_weight
                    )
                    / point.splitting_scale
                    for point in member.points
                )
                squared_residuals = tuple(value * value for value in thresholds)
                flat_axes[1].plot(
                    amplitudes,
                    thresholds,
                    color=color,
                    marker="o",
                    markevery=4,
                    markersize=2.2,
                    label=label,
                )
                flat_axes[2].plot(
                    amplitudes,
                    excess,
                    color=color,
                    marker="o",
                    markevery=4,
                    markersize=2.2,
                    label=label,
                )
                flat_axes[3].plot(
                    squared_residuals,
                    excess,
                    color=color,
                    marker="o",
                    markevery=4,
                    markersize=2.2,
                    label="_nolegend_",
                )

            flat_member = family.members[0]
            flat_amplitudes = tuple(point.amplitude for point in flat_member.points)
            flat_thresholds = tuple(
                point.minimum_operator_threshold / math.sqrt(point.splitting_scale)
                for point in flat_member.points
            )
            flat_axes[1].plot(
                flat_amplitudes,
                flat_thresholds,
                color=_BLACK,
                linestyle="--",
                linewidth=1.0,
                label="sampled flat control",
            )
            flat_axes[2].plot(
                flat_amplitudes,
                tuple(value * value for value in flat_thresholds),
                color=_BLACK,
                linestyle="--",
                linewidth=1.0,
                label="sampled flat identity",
            )
            maximum_relation = max(value * value for value in flat_thresholds)
            diagonal = np.linspace(0.0, maximum_relation, 101)
            flat_axes[3].plot(
                diagonal,
                diagonal,
                color=_BLACK,
                linestyle="--",
                linewidth=1.0,
                label="flat identity $y=x$",
            )

            amplitudes = family.request.template_request.amplitudes
            departure = np.asarray(
                [
                    [
                        (
                            point.comparison_nonzero_hopping_weight
                            - point.reference_nonzero_hopping_weight
                        )
                        / point.splitting_scale
                        - (
                            point.minimum_operator_threshold
                            / math.sqrt(point.splitting_scale)
                        )
                        ** 2
                        for point in member.points
                    ]
                    for member in family.members
                ],
                dtype=np.float64,
            )
            image = flat_axes[4].pcolormesh(
                amplitudes,
                scales,
                departure,
                shading="nearest",
                cmap="magma",
                vmin=float(np.min(departure)),
                vmax=max(0.0, float(np.max(departure))),
            )
            colorbar = figure.colorbar(image, ax=flat_axes[4], pad=0.02)
            colorbar.set_label("normalized departure", fontsize=7)
            colorbar.ax.tick_params(labelsize=6.3)

            full_parent = family.members[-1]
            selected_indices = (
                0,
                len(full_parent.points) // 2,
                len(full_parent.points) - 1,
            )
            selected = tuple(full_parent.points[index] for index in selected_indices)
            tail_styles = (
                (selected[0], True, "reference", _BLACK, "^"),
                (selected[1], False, r"comparison, $a=\pi/8$", colors[2], "o"),
                (selected[2], False, r"comparison, $a=\pi/4$", colors[-1], "s"),
            )
            for point, reference, label, color, marker in tail_styles:
                tails = tuple(
                    math.fsum(
                        (
                            power.reference_normalized_squared_frobenius_norm
                            if reference
                            else power.comparison_normalized_squared_frobenius_norm
                        )
                        for power in point.hopping_powers
                        if abs(power.displacement) > maximum_range
                    )
                    for maximum_range in _TAIL_RANGES
                )
                flat_axes[5].semilogy(
                    _TAIL_RANGES,
                    np.maximum(tails, _POWER_FLOOR),
                    color=color,
                    marker=marker,
                    markersize=2.8,
                    label=label,
                )

            flat_axes[0].set_ylabel("maximum band defect")
            flat_axes[0].set_title("Band blindness")
            flat_axes[0].legend(frameon=False, ncol=2)
            flat_axes[1].set_ylabel(r"$\epsilon_{\min}/\sqrt{\kappa}$")
            flat_axes[1].set_title("Restricted mismatch")
            flat_axes[2].set_ylabel(r"$(P_{>0}^{A}-P_{>0}^{H})/\kappa$")
            flat_axes[2].set_title("Excess hopping")
            flat_axes[3].set_xlabel(r"$x=\epsilon_{\min}^2/\kappa$")
            flat_axes[3].set_ylabel(r"$y=(P_{>0}^{A}-P_{>0}^{H})/\kappa$")
            flat_axes[3].set_title("Residual--locality relation")
            flat_axes[3].legend(frameon=False, loc="upper left")
            flat_axes[4].set_yticks(scales)
            flat_axes[4].set_xlabel("rotation amplitude $a$")
            flat_axes[4].set_ylabel(r"parent hopping scale $\rho$")
            flat_axes[4].set_title("Departure from flat identity")
            flat_axes[5].set_xlabel(r"retained range $R_{\max}$")
            flat_axes[5].set_ylabel(r"weight outside $|R|\leq R_{\max}$")
            flat_axes[5].set_title(r"Full-parent tails ($\rho=1$)")
            flat_axes[5].legend(frameon=False)

            for axis in flat_axes[:3]:
                axis.set_xlabel("rotation amplitude $a$")
            for axis in (*flat_axes[:3], flat_axes[4]):
                axis.set_xticks(
                    (0.0, math.pi / 8.0, math.pi / 4.0),
                    ("0", r"$\pi/8$", r"$\pi/4$"),
                )
            for index, axis in enumerate(flat_axes):
                axis.grid(which="both", alpha=0.2, linewidth=0.5)
                axis.text(
                    -0.13,
                    1.08,
                    f"({chr(ord('a') + index)})",
                    transform=axis.transAxes,
                    fontsize=9,
                    fontweight="bold",
                    va="bottom",
                )
            return figure


@dataclass(frozen=True, slots=True)
class _RangeInflationFigure(BaseFigure):
    data: Periodic1DRank2CompleteFiveScaleFigureData

    @staticmethod
    def _first_passing(
        values: tuple[float, ...], ranges: tuple[int, ...], target: float
    ) -> int | None:
        for maximum_range, value in zip(ranges, values, strict=True):
            if value <= target:
                return maximum_range
        return None

    @staticmethod
    def _edges(values: tuple[float, ...]) -> np.ndarray:
        array = np.asarray(values, dtype=np.float64)
        if array.size < 2:
            raise ValueError("at least two sampled values are required")
        midpoints = 0.5 * (array[:-1] + array[1:])
        return np.concatenate(
            (
                np.asarray([array[0] - 0.5 * (array[1] - array[0])]),
                midpoints,
                np.asarray([array[-1] + 0.5 * (array[-1] - array[-2])]),
            )
        )

    def _grid(self, target: float) -> np.ndarray:
        family = self.data.record.principal_truncation_family
        grid = np.full(
            (
                len(family.request.parent_family_request.parent_hopping_scales),
                len(family.request.parent_family_request.template_request.amplitudes),
            ),
            np.nan,
            dtype=np.float64,
        )
        for scale_index, member in enumerate(family.members):
            if type(member) is not Periodic1DRank2TruncationCompleted:
                raise TypeError("figure data admitted a non-complete truncation member")
            for amplitude_index, point in enumerate(member.points):
                ranges = tuple(item.maximum_range for item in point.ranges)
                reference = self._first_passing(
                    tuple(
                        item.reference_truncation_spectral_maximum_error
                        for item in point.ranges
                    ),
                    ranges,
                    target,
                )
                comparison = self._first_passing(
                    tuple(
                        item.comparison_total_spectral_maximum_error
                        for item in point.ranges
                    ),
                    ranges,
                    target,
                )
                if reference is not None and comparison is not None:
                    grid[scale_index, amplitude_index] = comparison - reference
        return grid

    def draw(self) -> Figure:
        family = self.data.record.principal_truncation_family
        scales = family.request.parent_family_request.parent_hopping_scales
        amplitudes = family.request.parent_family_request.template_request.amplitudes
        grids = tuple(self._grid(target) for target in _RANGE_TARGETS)
        finite_values = np.concatenate(
            tuple(grid[np.isfinite(grid)] for grid in grids)
        )
        maximum = (
            int(max(0.0, float(np.max(finite_values))))
            if finite_values.size
            else 0
        )
        boundaries = np.arange(-0.5, maximum + 1.5, 1.0)
        normalization = BoundaryNorm(boundaries, ncolors=256)
        figure, axes = plt.subplots(
            2,
            2,
            figsize=(10.8, 7.8),
            sharex=True,
            sharey=True,
            constrained_layout=True,
        )
        image = None
        normalized_amplitudes = tuple(4.0 * value / math.pi for value in amplitudes)
        for axis, target, grid in zip(axes.flat, _RANGE_TARGETS, grids, strict=True):
            image = axis.pcolormesh(
                self._edges(normalized_amplitudes),
                self._edges(scales),
                grid,
                cmap="viridis",
                norm=normalization,
                shading="flat",
            )
            endpoint = grid[-1, -1]
            endpoint_text = (
                rf"endpoint $\Delta\widehat{{R}}_c^\star={int(endpoint)}$"
                if math.isfinite(float(endpoint))
                else "endpoint unresolved"
            )
            axis.text(
                0.97,
                0.93,
                endpoint_text,
                transform=axis.transAxes,
                ha="right",
                va="top",
                color="black",
                fontsize=9,
                bbox={"facecolor": "white", "edgecolor": "none", "alpha": 0.82},
            )
            exponent = round(math.log10(target))
            axis.set_title(rf"sampled target $\tau=10^{{{exponent}}}$")
            axis.set_xticks((0.0, 0.5, 1.0), ("0", r"$\pi/8$", r"$\pi/4$"))
            axis.set_yticks(scales)
        if image is None:
            raise RuntimeError("no range-inflation panels were constructed")
        for axis in axes[-1, :]:
            axis.set_xlabel(r"rotation amplitude $a$")
        for axis in axes[:, 0]:
            axis.set_ylabel(r"sampled parent scale $\rho$")
        colorbar = figure.colorbar(
            image,
            ax=axes,
            ticks=np.arange(0, maximum + 1, max(1, 2 if maximum > 1 else 1)),
            shrink=0.94,
        )
        colorbar.set_label(
            r"additional range $\Delta\widehat{R}_c^\star$ "
            "(first sampled passing cutoff)"
        )
        figure.suptitle(
            "Exploratory sampled range inflation for equal band-error targets",
            fontsize=15,
        )
        return figure


@dataclass(frozen=True, slots=True)
class _ErrorChannelDecompositionFigure(BaseFigure):
    data: Periodic1DRank2CompleteFiveScaleFigureData

    def draw(self) -> Figure:
        family = self.data.record.principal_truncation_family
        scales = family.request.parent_family_request.parent_hopping_scales
        colors = plt.get_cmap("viridis")(np.linspace(0.05, 0.95, len(scales)))
        figure, axes = plt.subplots(
            2, 2, figsize=(11.2, 8.0), constrained_layout=True
        )
        reference_powers: list[float] = []
        for color, scale, member in zip(colors, scales, family.members, strict=True):
            if type(member) is not Periodic1DRank2TruncationCompleted:
                raise TypeError("figure data admitted a non-complete truncation member")
            amplitudes = tuple(point.amplitude for point in member.points)
            axes[0, 0].semilogy(
                amplitudes,
                np.maximum(
                    tuple(point.comparison_nyquist_power for point in member.points),
                    _POWER_FLOOR,
                ),
                "o-",
                color=color,
                markersize=3.0,
                linewidth=1.1,
                label=rf"$\rho={scale:g}$",
            )
            reference_powers.extend(
                point.reference_nyquist_power for point in member.points
            )
            axes[0, 1].semilogy(
                amplitudes,
                np.maximum(
                    tuple(
                        point.comparison_interpolation_spectral_maximum_error
                        for point in member.points
                    ),
                    _ERROR_FLOOR,
                ),
                "o-",
                color=color,
                markersize=3.0,
                linewidth=1.1,
                label=rf"$\rho={scale:g}$",
            )
            endpoint = member.points[-1]
            maximum_ranges = tuple(item.maximum_range for item in endpoint.ranges)
            axes[1, 0].semilogy(
                maximum_ranges,
                np.maximum(
                    tuple(
                        item.comparison_truncation_spectral_maximum_error
                        for item in endpoint.ranges
                    ),
                    _ERROR_FLOOR,
                ),
                "o-",
                color=color,
                markersize=4.0,
                linewidth=1.2,
                label=rf"$\rho={scale:g}$",
            )
            axes[1, 1].semilogy(
                maximum_ranges,
                np.maximum(
                    tuple(
                        item.comparison_total_spectral_maximum_error
                        for item in endpoint.ranges
                    ),
                    _ERROR_FLOOR,
                ),
                "o-",
                color=color,
                markersize=4.0,
                linewidth=1.2,
                label=rf"$\rho={scale:g}$",
            )
        axes[0, 0].axhspan(
            min(reference_powers),
            max(reference_powers),
            color="0.35",
            alpha=0.22,
            label="reference span",
        )
        full_parent = family.members[-1]
        if type(full_parent) is not Periodic1DRank2TruncationCompleted:
            raise TypeError("figure data admitted a non-complete truncation member")
        interpolation_floor = full_parent.points[
            -1
        ].comparison_interpolation_spectral_maximum_error
        axes[1, 1].axhline(
            interpolation_floor,
            linestyle="--",
            color="0.25",
            linewidth=1.0,
            label=r"$\rho=1$ interpolation discrepancy",
        )
        axes[0, 0].set_title("(a) centered-Nyquist conversion power")
        axes[0, 0].set_ylabel(r"$P_{\mathrm{Nyq}}/E_{\mathrm{ref}}^2$")
        axes[0, 1].set_title("(b) finite-interpolant spectral discrepancy")
        axes[0, 1].set_ylabel(r"maximum interpolation error / $E_{\mathrm{ref}}$")
        axes[1, 0].set_title(r"(c) deliberate truncation, $a=\pi/4$")
        axes[1, 0].set_xlabel(r"cutoff $R_c$")
        axes[1, 0].set_ylabel(r"maximum truncation error / $E_{\mathrm{ref}}$")
        axes[1, 1].set_title(r"(d) total spectral consequence, $a=\pi/4$")
        axes[1, 1].set_xlabel(r"cutoff $R_c$")
        axes[1, 1].set_ylabel(r"maximum total band error / $E_{\mathrm{ref}}$")
        for axis in axes[0, :]:
            axis.set_xlabel(r"rotation amplitude $a$")
            axis.set_xticks(
                (0.0, math.pi / 8.0, math.pi / 4.0),
                ("0", r"$\pi/8$", r"$\pi/4$"),
            )
        for axis in axes.flat:
            axis.grid(alpha=0.22)
            axis.legend(frameon=False, fontsize=7, ncol=2)
        figure.suptitle(
            "Separated conversion, interpolation, truncation, and total-error channels",
            fontsize=14,
        )
        return figure


@dataclass(frozen=True, slots=True)
class Periodic1DRank2CompleteFiveScaleFigureRenderer:
    """Render the complete-five-scale closed figure inventory as PNG values."""

    data: Periodic1DRank2CompleteFiveScaleFigureData
    dpi: int = 220

    def __post_init__(self) -> None:
        if type(self.data) is not Periodic1DRank2CompleteFiveScaleFigureData:
            raise TypeError("data must be complete-five-scale figure data")
        if type(self.dpi) is not int:
            raise TypeError("dpi must be a built-in integer")
        if self.dpi <= 0:
            raise ValueError("dpi must be positive")

    def execute(
        self,
    ) -> tuple[PngVisualization[Periodic1DRank2CompleteFiveScaleFigureEnum], ...]:
        """Render every figure exactly once in enumeration order."""
        figures: tuple[
            tuple[Periodic1DRank2CompleteFiveScaleFigureEnum, BaseFigure], ...
        ] = (
            (
                Periodic1DRank2CompleteFiveScaleFigureEnum.SCIENTIFIC_STORY,
                _ScientificStoryFigure(self.data),
            ),
            (
                Periodic1DRank2CompleteFiveScaleFigureEnum.RANGE_INFLATION,
                _RangeInflationFigure(self.data),
            ),
            (
                Periodic1DRank2CompleteFiveScaleFigureEnum.ERROR_CHANNEL_DECOMPOSITION,
                _ErrorChannelDecompositionFigure(self.data),
            ),
        )
        return tuple(
            PngFigureRenderer(plot=plot, figure=figure, dpi=self.dpi).visualize()
            for plot, figure in figures
        )


__all__ = [
    "Periodic1DRank2CompleteFiveScaleFigureData",
    "Periodic1DRank2CompleteFiveScaleFigureEnum",
    "Periodic1DRank2CompleteFiveScaleFigureRenderer",
]
