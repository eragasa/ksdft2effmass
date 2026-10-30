"""Development-only projections and figures for the higher-rank D1 study.

The projection consumes complete in-memory producer results.  It is intentionally not an
authenticated visualization projection: no verifier owns the source bytes yet.  Every
rendered figure therefore carries a visible development/unverified notice and must not
be used as publication evidence.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Literal, final

import matplotlib.pyplot as plt
import numpy as np
from ksdft2effmass.periodic1d.higher_rank_alignment import (
    Periodic1DHigherRankAlignmentCalculationResult,
    Periodic1DHigherRankAlignmentConfiguration,
    Periodic1DHigherRankAlignmentStatus,
)
from ksdft2effmass.periodic1d.higher_rank_alignment.gauge_alignment.definition import (
    GaugeAlignmentWireMapping,
    Periodic1DHigherRankGaugeAlignment,
)
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from matplotlib.lines import Line2D
from matplotlib.patches import Patch, Rectangle
from numpy.typing import NDArray

type FloatArray = NDArray[np.float64]
type IntArray = NDArray[np.int64]
type BoolArray = NDArray[np.bool_]
type LineStyle = Literal["-", "--", "-.", ":"]

_DEVELOPMENT_NOTICE = "DEVELOPMENT / UNVERIFIED — not publication evidence"
_S2_INDEX = 2
_S2_LOCALITY_EXTENSION_THRESHOLD = 1.0e-6
_S2_ORACLE_TAIL_THRESHOLD = 1.0e-10
_GLOBAL_RESIDUAL_THRESHOLD = 1.0e-6
_PLOT_FLOOR = 1.0e-18
_ANCHOR_RANK = 8
_ANCHOR_DEPTH = 4
_REFINEMENT_PATHS = (
    "/interpolation/normalized_operator_maximum",
    "/interpolation/normalized_spectrum_maximum",
    "/supports/2/tail_n",
    "/supports/2/truncation_operator_maximum",
    "/supports/2/truncation_spectrum_maximum",
    "/supports/2/total_operator_maximum",
    "/supports/2/total_spectrum_maximum",
)
_REFINEMENT_LABELS = (
    "interp. operator",
    "interp. spectrum",
    "S=2 tail",
    "S=2 trunc. operator",
    "S=2 trunc. spectrum",
    "S=2 total operator",
    "S=2 total spectrum",
)
_GAUGE_COLORS = ("#4C78A8", "#F58518", "#54A24B", "#B279A2")
_GAUGE_MARKERS = ("o", "s", "^", "D")
_DEPTH_COLORS = ("#4C78A8", "#F58518", "#54A24B", "#E45756")
_DEPTH_LINESTYLES: tuple[LineStyle, ...] = ("-", "--", "-.", ":")
_RANK_MARKERS = ("o", "s", "^", "D")
_STATUS_VALUES = tuple(Periodic1DHigherRankAlignmentStatus)
_STATUS_SHORT_LABELS = (
    "qualified",
    "aggregate\nrank deficient",
    "pointwise\nrank deficient",
    "numerically\nunresolved",
    "alignment\nintegrity failed",
    "oracle\nintegrity failed",
)
_STATUS_COLORS = (
    "#FFFFFF",
    "#B9A44C",
    "#8C6BB1",
    "#6B9AC4",
    "#C75D5D",
    "#A33D75",
)


class HigherRankDevelopmentPlot(Enum):
    """Closed filename inventory for the development figure suite."""

    ALIGNMENT_LOCALITY = "development-alignment-locality-s2.png"
    SUPPORT_LOCALITY = "development-support-locality-paths.png"
    BLOCK_LOCALITY = "development-fourier-block-locality.png"
    ERROR_CHANNELS = "development-error-channel-trajectories.png"
    CLAIM_RESOLUTION = "development-s2-claim-resolution.png"
    REFINEMENT = "development-mesh-refinement.png"
    RANK_DEPTH_SCALING = "development-rank-depth-scaling.png"
    RECOVERY_CONTROLS = "development-recovery-controls.png"
    PARETO = "development-support-error-pareto.png"


@dataclass(frozen=True, slots=True, eq=False)
class HigherRankDevelopmentFigureProjectionRequest:
    """Bind the complete ordered producer-result inventory to one projection."""

    calculation_results: tuple[Periodic1DHigherRankAlignmentCalculationResult, ...]

    def __post_init__(self) -> None:
        if type(self.calculation_results) is not tuple or any(
            type(result) is not Periodic1DHigherRankAlignmentCalculationResult
            for result in self.calculation_results
        ):
            raise TypeError("calculation_results must contain exact result records")
        configuration = Periodic1DHigherRankAlignmentConfiguration
        expected = tuple(
            (rank, depth)
            for rank in configuration.RETAINED_RANKS
            for depth in configuration.CIRCUIT_DEPTHS
        )
        actual = tuple(
            (result.request.retained_rank, result.request.circuit_depth)
            for result in self.calculation_results
        )
        if actual != expected:
            raise ValueError("calculation_results must match the complete case order")
        first_configuration = self.calculation_results[0].request.configuration
        if any(
            result.request.configuration != first_configuration
            for result in self.calculation_results[1:]
        ):
            raise ValueError("calculation_results must share one configuration")


@dataclass(frozen=True, slots=True, eq=False)
class HigherRankDevelopmentFigureData:
    """Own the immutable numeric projection drawn by development figures."""

    retained_ranks: tuple[int, ...]
    circuit_depths: tuple[int, ...]
    support_radii: tuple[int, ...]
    gauge_alignment_names: tuple[str, ...]
    refinement_labels: tuple[str, ...]
    block_translations: FloatArray
    qualified: BoolArray
    alignment_status_codes: IntArray
    frame_recovery: FloatArray
    operator_recovery: FloatArray
    support_two_tail: FloatArray
    support_two_total_spectrum: FloatArray
    support_tail: FloatArray
    interpolation_operator: FloatArray
    interpolation_spectrum: FloatArray
    truncation_operator: FloatArray
    truncation_spectrum: FloatArray
    total_operator: FloatArray
    total_spectrum: FloatArray
    decomposition_defect: FloatArray
    block_norms: FloatArray
    refinement_coarse: FloatArray
    refinement_fine: FloatArray
    refinement_change_over_tolerance: FloatArray
    pareto_efficient: BoolArray

    def __post_init__(self) -> None:
        expected_ranks = Periodic1DHigherRankAlignmentConfiguration.RETAINED_RANKS
        expected_depths = Periodic1DHigherRankAlignmentConfiguration.CIRCUIT_DEPTHS
        if self.retained_ranks != expected_ranks:
            raise ValueError("retained_ranks must match the frozen inventory")
        if self.circuit_depths != expected_depths:
            raise ValueError("circuit_depths must match the frozen inventory")
        if self.support_radii != (0, 1, 2, 4, 8, 16, 32, 64, 128):
            raise ValueError("support_radii must match the frozen inventory")
        expected_gauges = tuple(
            GaugeAlignmentWireMapping.to_wire(value)
            for value in Periodic1DHigherRankAlignmentConfiguration.GAUGE_ALIGNMENTS
        )
        if self.gauge_alignment_names != expected_gauges:
            raise ValueError("gauge_alignment_names must match the frozen order")
        if self.refinement_labels != _REFINEMENT_LABELS:
            raise ValueError("refinement_labels must match the fixed projection")
        nr = len(self.retained_ranks)
        nd = len(self.circuit_depths)
        ng = len(self.gauge_alignment_names)
        ns = len(self.support_radii)
        nm = 2
        npth = len(self.refinement_labels)
        shapes = {
            "block_translations": (257,),
            "qualified": (nr, nd, nm, ng),
            "alignment_status_codes": (nr, nd, nm, ng),
            "frame_recovery": (nr, nd, nm, ng),
            "operator_recovery": (nr, nd, nm, ng),
            "support_two_tail": (nr, nd, nm, ng),
            "support_two_total_spectrum": (nr, nd, nm, ng),
            "support_tail": (nr, nd, ng, ns),
            "interpolation_operator": (nr, nd, ng),
            "interpolation_spectrum": (nr, nd, ng),
            "truncation_operator": (nr, nd, ng, ns),
            "truncation_spectrum": (nr, nd, ng, ns),
            "total_operator": (nr, nd, ng, ns),
            "total_spectrum": (nr, nd, ng, ns),
            "decomposition_defect": (nr, nd, ng, ns),
            "block_norms": (nr, nd, ng, 257),
            "refinement_coarse": (nr, nd, ng, npth),
            "refinement_fine": (nr, nd, ng, npth),
            "refinement_change_over_tolerance": (nr, nd, ng, npth),
            "pareto_efficient": (nr, nd, ng, ns),
        }
        boolean_arrays = (
            ("qualified", self.qualified),
            ("pareto_efficient", self.pareto_efficient),
        )
        if self.alignment_status_codes.shape != shapes["alignment_status_codes"]:
            raise ValueError("alignment_status_codes has the wrong projection shape")
        if self.alignment_status_codes.dtype != np.dtype(np.int64):
            raise TypeError("alignment_status_codes must use int64 dtype")
        if self.alignment_status_codes.flags.writeable:
            raise ValueError("alignment_status_codes must be immutable")
        if not bool(
            np.all(
                (self.alignment_status_codes >= -1)
                & (self.alignment_status_codes < len(_STATUS_VALUES))
            )
        ):
            raise ValueError("alignment_status_codes contains an unknown status")
        float_arrays = (
            ("block_translations", self.block_translations),
            ("frame_recovery", self.frame_recovery),
            ("operator_recovery", self.operator_recovery),
            ("support_two_tail", self.support_two_tail),
            ("support_two_total_spectrum", self.support_two_total_spectrum),
            ("support_tail", self.support_tail),
            ("interpolation_operator", self.interpolation_operator),
            ("interpolation_spectrum", self.interpolation_spectrum),
            ("truncation_operator", self.truncation_operator),
            ("truncation_spectrum", self.truncation_spectrum),
            ("total_operator", self.total_operator),
            ("total_spectrum", self.total_spectrum),
            ("decomposition_defect", self.decomposition_defect),
            ("block_norms", self.block_norms),
            ("refinement_coarse", self.refinement_coarse),
            ("refinement_fine", self.refinement_fine),
            (
                "refinement_change_over_tolerance",
                self.refinement_change_over_tolerance,
            ),
        )
        for boolean_name, boolean_value in boolean_arrays:
            if boolean_value.shape != shapes[boolean_name]:
                raise ValueError(f"{boolean_name} has the wrong projection shape")
            if boolean_value.dtype != np.dtype(np.bool_):
                raise TypeError(f"{boolean_name} must use bool dtype")
            if boolean_value.flags.writeable:
                raise ValueError(f"{boolean_name} must be immutable")
        for float_name, float_value in float_arrays:
            if float_value.shape != shapes[float_name]:
                raise ValueError(f"{float_name} has the wrong projection shape")
            if float_value.dtype != np.dtype(np.float64):
                raise TypeError(f"{float_name} must use float64 dtype")
            if float_value.flags.writeable:
                raise ValueError(f"{float_name} must be immutable")


@final
class HigherRankDevelopmentFigureDataProjector:
    """Project complete producer results without authenticating their bytes."""

    __slots__ = ("_request",)

    def __init__(self, request: HigherRankDevelopmentFigureProjectionRequest) -> None:
        if type(request) is not HigherRankDevelopmentFigureProjectionRequest:
            raise TypeError("request must be the exact projection request")
        self._request = request

    @property
    def request(self) -> HigherRankDevelopmentFigureProjectionRequest:
        """Return the exact immutable request bound to this action."""
        return self._request

    def execute(self) -> HigherRankDevelopmentFigureData:
        """Return the complete development-only numeric figure projection."""
        results = self.request.calculation_results
        first = results[0]
        configuration = first.request.configuration
        controls = first.request.controls
        ranks = configuration.retained_ranks
        depths = configuration.circuit_depths
        gauges = configuration.gauge_alignments
        supports = controls.support_radii
        shape_mesh = (len(ranks), len(depths), 2, len(gauges))
        shape_support = (len(ranks), len(depths), len(gauges), len(supports))
        shape_scalar = (len(ranks), len(depths), len(gauges))
        shape_refinement = (*shape_scalar, len(_REFINEMENT_PATHS))
        qualified = np.zeros(shape_mesh, dtype=np.bool_)
        alignment_status_codes = np.full(shape_mesh, -1, dtype=np.int64)
        frame_recovery = np.full(shape_mesh, np.nan, dtype=np.float64)
        operator_recovery = np.full(shape_mesh, np.nan, dtype=np.float64)
        support_two_tail = np.full(shape_mesh, np.nan, dtype=np.float64)
        support_two_total_spectrum = np.full(shape_mesh, np.nan, dtype=np.float64)
        support_tail = np.full(shape_support, np.nan, dtype=np.float64)
        interpolation_operator = np.full(shape_scalar, np.nan, dtype=np.float64)
        interpolation_spectrum = np.full(shape_scalar, np.nan, dtype=np.float64)
        truncation_operator = np.full(shape_support, np.nan, dtype=np.float64)
        truncation_spectrum = np.full(shape_support, np.nan, dtype=np.float64)
        total_operator = np.full(shape_support, np.nan, dtype=np.float64)
        total_spectrum = np.full(shape_support, np.nan, dtype=np.float64)
        decomposition_defect = np.full(shape_support, np.nan, dtype=np.float64)
        block_norms = np.full((*shape_scalar, 257), np.nan, dtype=np.float64)
        refinement_coarse = np.full(shape_refinement, np.nan, dtype=np.float64)
        refinement_fine = np.full(shape_refinement, np.nan, dtype=np.float64)
        refinement_ratio = np.full(shape_refinement, np.nan, dtype=np.float64)
        pareto = np.zeros(shape_support, dtype=np.bool_)
        expected_translations = np.arange(-128, 129, dtype=np.int64)

        for result in results:
            rank_index = ranks.index(result.request.retained_rank)
            depth_index = depths.index(result.request.circuit_depth)
            selected_meshes = result.meshes[-2:]
            for mesh_index, mesh in enumerate(selected_meshes):
                for gauge_index, alignment in enumerate(mesh.gauge_alignment_results):
                    is_qualified = (
                        alignment.status.status
                        is Periodic1DHigherRankAlignmentStatus.QUALIFIED
                    )
                    qualified[rank_index, depth_index, mesh_index, gauge_index] = (
                        is_qualified
                    )
                    alignment_status_codes[
                        rank_index, depth_index, mesh_index, gauge_index
                    ] = _STATUS_VALUES.index(alignment.status.status)
                    if not is_qualified:
                        continue
                    if (
                        alignment.frame_recovery is None
                        or alignment.represented_operator_recovery is None
                    ):
                        raise ValueError(
                            "qualified alignment lacks recovery diagnostics"
                        )
                    frame_recovery[rank_index, depth_index, mesh_index, gauge_index] = (
                        alignment.frame_recovery.normalized_frobenius_maximum
                    )
                    operator_error = alignment.represented_operator_recovery
                    operator_recovery[
                        rank_index, depth_index, mesh_index, gauge_index
                    ] = operator_error.normalized_matrix_frobenius_maximum
                    support_two = alignment.supports[_S2_INDEX]
                    support_two_tail[
                        rank_index, depth_index, mesh_index, gauge_index
                    ] = support_two.normalized_omitted_frobenius_l2_norm
                    support_two_total_spectrum[
                        rank_index, depth_index, mesh_index, gauge_index
                    ] = support_two.total.errors.normalized_ordered_spectrum_maximum

            final_mesh = result.meshes[-1]
            for gauge_index, alignment in enumerate(final_mesh.gauge_alignment_results):
                if (
                    alignment.status.status
                    is not Periodic1DHigherRankAlignmentStatus.QUALIFIED
                ):
                    continue
                interpolation = alignment.interpolation
                if interpolation is None:
                    raise ValueError("qualified alignment lacks interpolation")
                interpolation_operator[rank_index, depth_index, gauge_index] = (
                    interpolation.errors.normalized_matrix_frobenius_maximum
                )
                interpolation_spectrum[rank_index, depth_index, gauge_index] = (
                    interpolation.errors.normalized_ordered_spectrum_maximum
                )
                if not np.array_equal(
                    alignment.coefficient_translations, expected_translations
                ):
                    raise ValueError("final block inventory differs from the protocol")
                block_norms[rank_index, depth_index, gauge_index] = (
                    alignment.block_normalized_frobenius_norms
                )
                for support_index, support in enumerate(alignment.supports):
                    key = (rank_index, depth_index, gauge_index, support_index)
                    support_tail[key] = support.normalized_omitted_frobenius_l2_norm
                    truncation_operator[key] = (
                        support.truncation.errors.normalized_matrix_frobenius_maximum
                    )
                    truncation_spectrum[key] = (
                        support.truncation.errors.normalized_ordered_spectrum_maximum
                    )
                    total_operator[key] = (
                        support.total.errors.normalized_matrix_frobenius_maximum
                    )
                    total_spectrum[key] = (
                        support.total.errors.normalized_ordered_spectrum_maximum
                    )
                    decomposition_defect[key] = (
                        support.normalized_error_decomposition_defect
                    )
                objectives = np.column_stack(
                    (
                        2.0 * np.asarray(supports, dtype=np.float64) + 1.0,
                        total_operator[rank_index, depth_index, gauge_index],
                        total_spectrum[rank_index, depth_index, gauge_index],
                    )
                )
                pareto[rank_index, depth_index, gauge_index] = (
                    _sampled_pareto_membership(objectives)
                )

            refinement_by_gauge: dict[
                Periodic1DHigherRankGaugeAlignment,
                dict[str, tuple[float, float, float, float]],
            ] = {gauge: {} for gauge in gauges}
            for refinement in result.scalar_refinements:
                refinement_by_gauge[refinement.gauge_alignment][
                    refinement.diagnostic_path
                ] = (
                    refinement.coarse_value,
                    refinement.fine_value,
                    refinement.absolute_change,
                    refinement.applied_tolerance,
                )
            for gauge_index, gauge in enumerate(gauges):
                if not qualified[rank_index, depth_index, 1, gauge_index]:
                    continue
                lookup = refinement_by_gauge[gauge]
                for path_index, path in enumerate(_REFINEMENT_PATHS):
                    if path not in lookup:
                        raise ValueError(f"missing scalar refinement path {path}")
                    coarse, fine, change, tolerance = lookup[path]
                    key = (rank_index, depth_index, gauge_index, path_index)
                    refinement_coarse[key] = coarse
                    refinement_fine[key] = fine
                    refinement_ratio[key] = change / tolerance

        arrays = (
            qualified,
            alignment_status_codes,
            frame_recovery,
            operator_recovery,
            support_two_tail,
            support_two_total_spectrum,
            support_tail,
            interpolation_operator,
            interpolation_spectrum,
            truncation_operator,
            truncation_spectrum,
            total_operator,
            total_spectrum,
            decomposition_defect,
            block_norms,
            refinement_coarse,
            refinement_fine,
            refinement_ratio,
            pareto,
        )
        for array in arrays:
            array.setflags(write=False)
        translations = np.asarray(expected_translations, dtype=np.float64)
        translations.setflags(write=False)
        return HigherRankDevelopmentFigureData(
            retained_ranks=ranks,
            circuit_depths=depths,
            support_radii=supports,
            gauge_alignment_names=tuple(
                GaugeAlignmentWireMapping.to_wire(value) for value in gauges
            ),
            refinement_labels=_REFINEMENT_LABELS,
            block_translations=translations,
            qualified=qualified,
            alignment_status_codes=alignment_status_codes,
            frame_recovery=frame_recovery,
            operator_recovery=operator_recovery,
            support_two_tail=support_two_tail,
            support_two_total_spectrum=support_two_total_spectrum,
            support_tail=support_tail,
            interpolation_operator=interpolation_operator,
            interpolation_spectrum=interpolation_spectrum,
            truncation_operator=truncation_operator,
            truncation_spectrum=truncation_spectrum,
            total_operator=total_operator,
            total_spectrum=total_spectrum,
            decomposition_defect=decomposition_defect,
            block_norms=block_norms,
            refinement_coarse=refinement_coarse,
            refinement_fine=refinement_fine,
            refinement_change_over_tolerance=refinement_ratio,
            pareto_efficient=pareto,
        )


@dataclass(frozen=True, slots=True, eq=False)
class HigherRankDevelopmentFigureRenderRequest:
    """Bind one development projection and destination to the renderer."""

    data: HigherRankDevelopmentFigureData
    output_directory: Path
    dpi: int = 180

    def __post_init__(self) -> None:
        if type(self.data) is not HigherRankDevelopmentFigureData:
            raise TypeError("data must be the exact development projection")
        if not isinstance(self.output_directory, Path):
            raise TypeError("output_directory must be pathlib.Path")
        if type(self.dpi) is not int or self.dpi <= 0:
            raise ValueError("dpi must be a positive built-in integer")


@final
class HigherRankDevelopmentFigureRenderer:
    """Render the closed unverified figure inventory without deriving science."""

    __slots__ = ("_request",)

    def __init__(self, request: HigherRankDevelopmentFigureRenderRequest) -> None:
        if type(request) is not HigherRankDevelopmentFigureRenderRequest:
            raise TypeError("request must be the exact render request")
        self._request = request

    @property
    def request(self) -> HigherRankDevelopmentFigureRenderRequest:
        """Return the exact immutable request bound to this action."""
        return self._request

    def execute(self) -> tuple[Path, ...]:
        """Render every fixed development plot and return its output path."""
        output = self.request.output_directory
        output.mkdir(parents=True, exist_ok=True)
        figures = (
            (HigherRankDevelopmentPlot.ALIGNMENT_LOCALITY, _alignment_locality_figure),
            (HigherRankDevelopmentPlot.SUPPORT_LOCALITY, _support_locality_figure),
            (HigherRankDevelopmentPlot.BLOCK_LOCALITY, _block_locality_figure),
            (HigherRankDevelopmentPlot.ERROR_CHANNELS, _error_channel_figure),
            (HigherRankDevelopmentPlot.CLAIM_RESOLUTION, _claim_resolution_figure),
            (HigherRankDevelopmentPlot.REFINEMENT, _refinement_figure),
            (HigherRankDevelopmentPlot.RANK_DEPTH_SCALING, _rank_depth_figure),
            (HigherRankDevelopmentPlot.RECOVERY_CONTROLS, _recovery_figure),
            (HigherRankDevelopmentPlot.PARETO, _pareto_figure),
        )
        destinations: list[Path] = []
        for plot, draw in figures:
            figure = draw(self.request.data)
            destination = output / plot.value
            figure.savefig(
                destination,
                dpi=self.request.dpi,
                bbox_inches="tight",
                metadata={"Software": "ksdft2effmass development renderer"},
            )
            plt.close(figure)
            destinations.append(destination)
        return tuple(destinations)


def _sampled_pareto_membership(objectives: FloatArray) -> BoolArray:
    if objectives.ndim != 2 or objectives.shape[1] != 3:
        raise ValueError("objectives must be a point-by-three matrix")
    if not bool(np.all(np.isfinite(objectives))):
        raise ValueError("objectives must be finite")
    efficient = np.ones(objectives.shape[0], dtype=np.bool_)
    for candidate_index, candidate in enumerate(objectives):
        for competitor_index, competitor in enumerate(objectives):
            if competitor_index == candidate_index:
                continue
            if bool(np.all(competitor <= candidate)) and bool(
                np.any(competitor < candidate)
            ):
                efficient[candidate_index] = False
                break
    efficient.setflags(write=False)
    return efficient


def _figure_grid(
    rows: int,
    columns: int,
    *,
    width: float,
    height: float,
) -> tuple[Figure, tuple[tuple[Axes, ...], ...]]:
    figure = plt.figure(figsize=(width, height), constrained_layout=True)
    axes = tuple(
        tuple(
            figure.add_subplot(rows, columns, row * columns + column + 1)
            for column in range(columns)
        )
        for row in range(rows)
    )
    return figure, axes


def _positive(values: FloatArray) -> FloatArray:
    return np.maximum(values, _PLOT_FLOOR)


def _claim_condition(
    value: np.float64,
    status_code: int,
    qualified_code: int,
    threshold: float,
    larger_is_resolved: bool,
) -> bool | None:
    if status_code != qualified_code or not np.isfinite(value):
        return None
    if larger_is_resolved:
        return bool(value >= threshold)
    return bool(value <= threshold)


def _finalize(figure: Figure, title: str) -> Figure:
    figure.suptitle(f"{title}\n{_DEVELOPMENT_NOTICE}", fontsize=14, fontweight="bold")
    figure.text(
        0.995,
        0.003,
        _DEVELOPMENT_NOTICE,
        ha="right",
        va="bottom",
        fontsize=8,
        color="#9C2F2F",
        alpha=0.9,
    )
    return figure


def _gauge_legend() -> tuple[Line2D, ...]:
    return tuple(
        Line2D(
            [0],
            [0],
            color=color,
            marker=marker,
            linestyle="none",
            label=name,
        )
        for name, color, marker in zip(
            (
                "identity",
                "global-unitary",
                "pointwise-unitary",
                "known-inverse-oracle",
            ),
            _GAUGE_COLORS,
            _GAUGE_MARKERS,
            strict=True,
        )
    )


def _alignment_locality_figure(data: HigherRankDevelopmentFigureData) -> Figure:
    figure, axes = _figure_grid(1, 4, width=17.0, height=5.6)
    for gauge_index, gauge in enumerate(data.gauge_alignment_names):
        axis = axes[0][gauge_index]
        for rank_index, marker in enumerate(_RANK_MARKERS):
            for depth_index, color in enumerate(_DEPTH_COLORS):
                x = _positive(
                    data.frame_recovery[rank_index, depth_index, :, gauge_index]
                )
                y = _positive(
                    data.support_two_tail[rank_index, depth_index, :, gauge_index]
                )
                axis.plot(x, y, color=color, linewidth=0.9, alpha=0.65)
                axis.scatter(
                    x[0],
                    y[0],
                    facecolors="none",
                    edgecolors=color,
                    marker=marker,
                    s=42,
                    linewidths=1.0,
                    zorder=3,
                )
                axis.scatter(
                    x[1],
                    y[1],
                    color=color,
                    marker=marker,
                    s=24,
                    zorder=4,
                )
        axis.set_xscale("log")
        axis.set_yscale("log")
        axis.axhline(
            _S2_LOCALITY_EXTENSION_THRESHOLD,
            color="#666666",
            linestyle=":",
            linewidth=0.8,
        )
        axis.set_xlabel("normalized frame-recovery defect")
        if gauge_index == 0:
            axis.set_ylabel("normalized omitted L2 tail at S=2")
        axis.set_title(gauge)
        axis.grid(True, which="both", alpha=0.18)
    rank_handles = tuple(
        Line2D(
            [0],
            [0],
            color="#333333",
            marker=marker,
            linestyle="none",
            label=f"r={rank}",
        )
        for rank, marker in zip(data.retained_ranks, _RANK_MARKERS, strict=True)
    )
    depth_handles = tuple(
        Line2D([0], [0], color=color, label=f"L={depth}")
        for depth, color in zip(data.circuit_depths, _DEPTH_COLORS, strict=True)
    )
    mesh_handles = (
        Line2D(
            [0],
            [0],
            marker="o",
            markerfacecolor="none",
            markeredgecolor="#333333",
            linestyle="none",
            label="M=1025",
        ),
        Line2D(
            [0],
            [0],
            marker="o",
            color="#333333",
            linestyle="none",
            label="M=2049",
        ),
    )
    figure.legend(
        handles=(*rank_handles, *depth_handles, *mesh_handles),
        loc="outside lower center",
        ncol=10,
    )
    return _finalize(figure, "S=2 alignment–locality plane")


def _support_locality_figure(data: HigherRankDevelopmentFigureData) -> Figure:
    figure, axes = _figure_grid(4, 4, width=16.5, height=14.5)
    x = np.arange(len(data.support_radii), dtype=np.float64)
    for rank_index, rank in enumerate(data.retained_ranks):
        for gauge_index, gauge in enumerate(data.gauge_alignment_names):
            axis = axes[rank_index][gauge_index]
            for depth_index, depth in enumerate(data.circuit_depths):
                axis.semilogy(
                    x,
                    _positive(data.support_tail[rank_index, depth_index, gauge_index]),
                    color=_DEPTH_COLORS[depth_index],
                    linestyle=_DEPTH_LINESTYLES[depth_index],
                    marker="o",
                    markersize=3,
                    label=f"L={depth}",
                )
            axis.axvline(_S2_INDEX, color="#666666", linestyle=":", linewidth=0.8)
            axis.set_title(f"r={rank}; {gauge}")
            axis.set_xticks(x, tuple(str(value) for value in data.support_radii))
            if rank_index == 3:
                axis.set_xlabel("support radius S")
            if gauge_index == 0:
                axis.set_ylabel("normalized omitted L2 tail")
            axis.grid(True, which="both", alpha=0.18)
    handles = tuple(
        Line2D(
            [0],
            [0],
            color=_DEPTH_COLORS[index],
            linestyle=_DEPTH_LINESTYLES[index],
            marker="o",
            label=f"L={depth}",
        )
        for index, depth in enumerate(data.circuit_depths)
    )
    figure.legend(handles=handles, loc="outside lower center", ncol=4)
    return _finalize(figure, "Complete support-path locality curves")


def _block_locality_figure(data: HigherRankDevelopmentFigureData) -> Figure:
    figure, axes = _figure_grid(2, 2, width=12.5, height=9.5)
    rank_index = data.retained_ranks.index(_ANCHOR_RANK)
    depth_index = data.circuit_depths.index(_ANCHOR_DEPTH)
    nonnegative = data.block_translations >= 0.0
    translations = data.block_translations[nonnegative]
    for gauge_index, gauge in enumerate(data.gauge_alignment_names):
        axis = axes[gauge_index // 2][gauge_index % 2]
        values = data.block_norms[rank_index, depth_index, gauge_index, nonnegative]
        axis.semilogy(
            translations,
            _positive(values),
            color=_GAUGE_COLORS[gauge_index],
            marker=".",
            markersize=3,
            linewidth=0.9,
        )
        axis.axvline(2.0, color="#333333", linestyle="--", linewidth=1.0)
        axis.set_xlim(-1.0, 128.0)
        axis.set_xlabel("nonnegative translation R")
        axis.set_ylabel("block Frobenius norm / (sqrt(r) E_ref)")
        axis.set_title(f"{gauge}; r={_ANCHOR_RANK}, L={_ANCHOR_DEPTH}")
        axis.grid(True, which="both", alpha=0.18)
    return _finalize(
        figure,
        "Final-mesh Fourier-block locality (fixed interior anchor)",
    )


def _error_channel_figure(data: HigherRankDevelopmentFigureData) -> Figure:
    figure, axes = _figure_grid(3, 4, width=17.0, height=11.5)
    rank_index = data.retained_ranks.index(_ANCHOR_RANK)
    depth_index = data.circuit_depths.index(_ANCHOR_DEPTH)
    x = np.arange(len(data.support_radii), dtype=np.float64)
    for gauge_index, gauge in enumerate(data.gauge_alignment_names):
        operator_axis = axes[0][gauge_index]
        spectrum_axis = axes[1][gauge_index]
        defect_axis = axes[2][gauge_index]
        operator_interpolation = np.full(
            x.shape,
            data.interpolation_operator[rank_index, depth_index, gauge_index],
            dtype=np.float64,
        )
        spectrum_interpolation = np.full(
            x.shape,
            data.interpolation_spectrum[rank_index, depth_index, gauge_index],
            dtype=np.float64,
        )
        for axis, interpolation, truncation, total in (
            (
                operator_axis,
                operator_interpolation,
                data.truncation_operator[rank_index, depth_index, gauge_index],
                data.total_operator[rank_index, depth_index, gauge_index],
            ),
            (
                spectrum_axis,
                spectrum_interpolation,
                data.truncation_spectrum[rank_index, depth_index, gauge_index],
                data.total_spectrum[rank_index, depth_index, gauge_index],
            ),
        ):
            axis.semilogy(
                x,
                _positive(total),
                color="#2CA02C",
                linestyle="-",
                marker="o",
                markersize=3,
                linewidth=1.4,
                label="total",
                zorder=2,
            )
            axis.semilogy(
                x,
                _positive(truncation),
                color="#FF7F0E",
                linestyle="--",
                marker="s",
                markerfacecolor="none",
                markeredgewidth=1.1,
                markersize=5,
                linewidth=2.2,
                label="truncation",
                zorder=3,
            )
            axis.semilogy(
                x,
                _positive(interpolation),
                color="#1F77B4",
                linestyle=":",
                linewidth=2.0,
                label="interpolation",
                zorder=4,
            )
            axis.axvline(_S2_INDEX, color="#666666", linestyle=":", linewidth=0.8)
            axis.set_xticks(x, tuple(str(value) for value in data.support_radii))
            axis.grid(True, which="both", alpha=0.18)
        operator_axis.set_title(gauge)
        operator_axis.set_ylabel("normalized max. Frobenius error")
        spectrum_axis.set_ylabel("normalized max. ordered-spectrum error")
        defect_axis.semilogy(
            x,
            _positive(data.decomposition_defect[rank_index, depth_index, gauge_index]),
            color=_GAUGE_COLORS[gauge_index],
            marker="o",
            markersize=3,
        )
        defect_axis.axhline(2.0e-11, color="#9C2F2F", linestyle="--", linewidth=1.0)
        defect_axis.set_xticks(x, tuple(str(value) for value in data.support_radii))
        defect_axis.set_xlabel("support radius S")
        defect_axis.set_ylabel("normalized decomposition-identity defect")
        defect_axis.grid(True, which="both", alpha=0.18)
    legend_axis = axes[0][0]
    handles, labels = legend_axis.get_legend_handles_labels()
    ordered_labels = ("interpolation", "truncation", "total")
    ordered_handles = tuple(handles[labels.index(label)] for label in ordered_labels)
    legend_axis.legend(ordered_handles, ordered_labels, loc="best", fontsize=8)
    return _finalize(
        figure,
        f"Three error channels at fixed r={_ANCHOR_RANK}, L={_ANCHOR_DEPTH}",
    )


def _claim_resolution_figure(data: HigherRankDevelopmentFigureData) -> Figure:
    figure, axes = _figure_grid(1, 4, width=17.0, height=5.8)
    identity = data.gauge_alignment_names.index("identity")
    oracle = data.gauge_alignment_names.index("known-inverse-oracle")
    global_unitary = data.gauge_alignment_names.index("global-unitary")
    metrics = (
        (
            data.support_two_tail[:, :, 1, identity],
            data.alignment_status_codes[:, :, 1, identity],
            _S2_LOCALITY_EXTENSION_THRESHOLD,
            "identity tail ≥ 1e-6",
            True,
        ),
        (
            data.support_two_tail[:, :, 1, oracle],
            data.alignment_status_codes[:, :, 1, oracle],
            _S2_ORACLE_TAIL_THRESHOLD,
            "oracle tail ≤ 1e-10",
            False,
        ),
        (
            data.support_two_total_spectrum[:, :, 1, identity],
            data.alignment_status_codes[:, :, 1, identity],
            _S2_LOCALITY_EXTENSION_THRESHOLD,
            "identity total spectrum ≥ 1e-6",
            True,
        ),
        (
            data.frame_recovery[:, :, 1, global_unitary],
            data.alignment_status_codes[:, :, 1, global_unitary],
            _GLOBAL_RESIDUAL_THRESHOLD,
            "global frame residual (supporting) ≥ 1e-6",
            True,
        ),
    )
    qualified_code = _STATUS_VALUES.index(Periodic1DHigherRankAlignmentStatus.QUALIFIED)
    for axis, (
        values,
        status_codes,
        threshold,
        title,
        larger_is_resolved,
    ) in zip(axes[0], metrics, strict=True):
        logs = np.log10(_positive(values))
        finite_logs = logs[np.isfinite(logs)]
        threshold_log = float(np.log10(threshold))
        low = min(float(np.min(finite_logs)), threshold_log)
        high = max(float(np.max(finite_logs)), threshold_log)
        if high - low < 1.0:
            low -= 0.5
            high += 0.5
        colormap = plt.get_cmap("viridis").copy()
        colormap.set_bad("#D9D9D9")
        image = axis.imshow(
            np.ma.masked_invalid(logs),
            origin="lower",
            vmin=low,
            vmax=high,
            cmap=colormap,
            aspect="auto",
        )
        for rank_index in range(len(data.retained_ranks)):
            for depth_index in range(len(data.circuit_depths)):
                status_code = int(status_codes[rank_index, depth_index])
                value = values[rank_index, depth_index]
                if status_code == -1:
                    label = "missing"
                    facecolor = "#D9D9D9"
                    edgecolor = "#555555"
                elif status_code != qualified_code:
                    label = _STATUS_SHORT_LABELS[status_code]
                    facecolor = _STATUS_COLORS[status_code]
                    edgecolor = "#333333"
                elif not np.isfinite(value):
                    label = "qualified\nvalue missing"
                    facecolor = "#D9D9D9"
                    edgecolor = "#C23B22"
                else:
                    condition_met = _claim_condition(
                        value,
                        status_code,
                        qualified_code,
                        threshold,
                        larger_is_resolved,
                    )
                    if condition_met is None:
                        raise RuntimeError(
                            "qualified finite claim cell must be decidable"
                        )
                    label = f"{value:.1e}"
                    facecolor = "none"
                    edgecolor = "#1B7837" if condition_met else "#B2182B"
                axis.add_patch(
                    Rectangle(
                        (depth_index - 0.5, rank_index - 0.5),
                        1.0,
                        1.0,
                        facecolor=facecolor,
                        edgecolor=edgecolor,
                        linewidth=2.0,
                    )
                )
                axis.text(
                    depth_index,
                    rank_index,
                    label,
                    ha="center",
                    va="center",
                    fontsize=6.5,
                    color="black",
                )
        axis.set_xticks(range(4), tuple(str(value) for value in data.circuit_depths))
        axis.set_yticks(range(4), tuple(str(value) for value in data.retained_ranks))
        axis.set_xlabel("circuit depth L")
        axis.set_ylabel("retained rank r")
        axis.set_title(title)
        figure.colorbar(image, ax=axis, label="log10 absolute normalized operand")
    status_handles = (
        Patch(
            facecolor="none", edgecolor="#1B7837", linewidth=2.0, label="condition met"
        ),
        Patch(
            facecolor="none",
            edgecolor="#B2182B",
            linewidth=2.0,
            label="condition not met",
        ),
        Patch(facecolor="#D9D9D9", edgecolor="#555555", label="missing"),
        *tuple(
            Patch(
                facecolor=_STATUS_COLORS[index],
                edgecolor="#333333",
                label=status.value,
            )
            for index, status in enumerate(_STATUS_VALUES)
            if status is not Periodic1DHigherRankAlignmentStatus.QUALIFIED
        ),
    )
    figure.legend(handles=status_handles, loc="outside lower center", ncol=4)
    return _finalize(
        figure,
        "S=2 claim operands and global supporting diagnostic",
    )


def _refinement_figure(data: HigherRankDevelopmentFigureData) -> Figure:
    figure, axes = _figure_grid(1, 2, width=13.5, height=5.8)
    path_colors = (
        "#1F77B4",
        "#FF7F0E",
        "#2CA02C",
        "#D62728",
        "#9467BD",
        "#8C564B",
        "#E377C2",
    )
    for path_index, label in enumerate(data.refinement_labels):
        coarse = data.refinement_coarse[:, :, :, path_index].reshape(-1)
        fine = data.refinement_fine[:, :, :, path_index].reshape(-1)
        finite = np.isfinite(coarse) & np.isfinite(fine)
        axes[0][0].loglog(
            _positive(coarse[finite]),
            _positive(fine[finite]),
            ".",
            alpha=0.45,
            color=path_colors[path_index],
            label=label,
        )
    all_coarse = data.refinement_coarse.reshape(-1)
    all_fine = data.refinement_fine.reshape(-1)
    finite = np.isfinite(all_coarse) & np.isfinite(all_fine)
    low = min(
        float(np.min(_positive(all_coarse[finite]))),
        float(np.min(_positive(all_fine[finite]))),
    )
    high = max(float(np.max(all_coarse[finite])), float(np.max(all_fine[finite])))
    axes[0][0].plot((low, high), (low, high), "--", color="#333333")
    axes[0][0].set_xlabel("M=1025 normalized diagnostic")
    axes[0][0].set_ylabel("M=2049 normalized diagnostic")
    axes[0][0].set_title("Paired coarse/final values")
    axes[0][0].grid(True, which="both", alpha=0.18)
    axes[0][0].legend(fontsize=6, loc="best")

    ratios = data.refinement_change_over_tolerance.reshape(
        (-1, len(data.refinement_labels))
    )
    positions = np.arange(len(data.refinement_labels), dtype=np.float64)
    for path_index, label in enumerate(data.refinement_labels):
        finite_values = ratios[:, path_index][np.isfinite(ratios[:, path_index])]
        jitter = np.linspace(-0.14, 0.14, finite_values.size, dtype=np.float64)
        axes[0][1].scatter(
            np.full(finite_values.shape, positions[path_index]) + jitter,
            _positive(finite_values),
            s=10,
            alpha=0.45,
            color=path_colors[path_index],
            label=label,
        )
    maximum_index = np.unravel_index(
        int(np.nanargmax(data.refinement_change_over_tolerance)),
        data.refinement_change_over_tolerance.shape,
    )
    rank_index = int(maximum_index[0])
    depth_index = int(maximum_index[1])
    gauge_index = int(maximum_index[2])
    path_index = int(maximum_index[3])
    maximum_value = data.refinement_change_over_tolerance[maximum_index]
    axes[0][1].scatter(
        positions[path_index],
        maximum_value,
        marker="*",
        s=85,
        color="#111111",
        zorder=5,
    )
    axes[0][1].annotate(
        (
            f"max: r={data.retained_ranks[rank_index]}, "
            f"L={data.circuit_depths[depth_index]}\n"
            f"{data.gauge_alignment_names[gauge_index]}"
        ),
        (positions[path_index], maximum_value),
        xytext=(8, 8),
        textcoords="offset points",
        fontsize=7,
    )
    axes[0][1].axhline(1.0, color="#9C2F2F", linestyle="--", linewidth=1.2)
    axes[0][1].set_yscale("log")
    axes[0][1].set_xticks(
        positions,
        data.refinement_labels,
        rotation=30,
        ha="right",
    )
    axes[0][1].set_ylabel("absolute change / applied tolerance")
    axes[0][1].set_title("Frozen refinement gate utilization")
    axes[0][1].grid(True, which="both", alpha=0.18)
    return _finalize(figure, "1025→2049 refinement diagnostics")


def _rank_depth_figure(data: HigherRankDevelopmentFigureData) -> Figure:
    support_index = data.support_radii.index(2)
    figure, axes = _figure_grid(4, 2, width=13.5, height=12.5)
    images = []
    for gauge_index, gauge in enumerate(data.gauge_alignment_names):
        for column, (values, metric) in enumerate(
            (
                (data.total_operator, "total operator error"),
                (data.total_spectrum, "total ordered-spectrum error"),
            )
        ):
            axis = axes[gauge_index][column]
            selected = values[:, :, gauge_index, support_index]
            image = axis.imshow(
                np.log10(_positive(selected)),
                origin="lower",
                cmap="viridis",
                aspect="auto",
                vmin=-18.0,
                vmax=0.0,
            )
            images.append(image)
            for rank_index in range(len(data.retained_ranks)):
                for depth_index in range(len(data.circuit_depths)):
                    value = selected[rank_index, depth_index]
                    label = "missing" if not np.isfinite(value) else f"{value:.1e}"
                    axis.text(
                        depth_index,
                        rank_index,
                        label,
                        ha="center",
                        va="center",
                        fontsize=7,
                        color="white" if value < 1.0e-6 else "black",
                    )
            axis.set_xticks(
                range(4), tuple(str(value) for value in data.circuit_depths)
            )
            axis.set_yticks(
                range(4), tuple(str(value) for value in data.retained_ranks)
            )
            axis.set_xlabel("circuit depth L")
            axis.set_ylabel("retained rank r")
            axis.set_title(f"{gauge}: {metric}")
    figure.colorbar(
        images[-1],
        ax=tuple(axis for row in axes for axis in row),
        label="log10 absolute normalized error (display floor 1e-18)",
    )
    return _finalize(figure, "Rank/depth scaling at S=2")


def _recovery_figure(data: HigherRankDevelopmentFigureData) -> Figure:
    figure, axes = _figure_grid(2, 4, width=16.5, height=8.2)
    images = []
    for gauge_index, gauge in enumerate(data.gauge_alignment_names):
        for row, (values, title) in enumerate(
            (
                (data.frame_recovery[:, :, 1, gauge_index], "frame"),
                (data.operator_recovery[:, :, 1, gauge_index], "operator"),
            )
        ):
            axis = axes[row][gauge_index]
            image = axis.imshow(
                np.log10(_positive(values)),
                origin="lower",
                cmap="viridis",
                aspect="auto",
                vmin=-18.0,
                vmax=0.0,
            )
            images.append(image)
            for rank_index in range(len(data.retained_ranks)):
                for depth_index in range(len(data.circuit_depths)):
                    value = values[rank_index, depth_index]
                    if value == 0.0:
                        axis.text(
                            depth_index,
                            rank_index,
                            "0",
                            ha="center",
                            va="center",
                            fontsize=7,
                            color="white",
                        )
            axis.set_xticks(
                range(4), tuple(str(value) for value in data.circuit_depths)
            )
            axis.set_yticks(
                range(4), tuple(str(value) for value in data.retained_ranks)
            )
            axis.set_xlabel("circuit depth L")
            axis.set_ylabel("retained rank r")
            axis.set_title(f"{gauge}: {title} recovery")
    figure.colorbar(
        images[-1],
        ax=tuple(axis for row in axes for axis in row),
        label="log10 max(defect, 1e-18); exact zeros marked 0",
    )
    return _finalize(figure, "Final-mesh gauge-recovery controls")


def _pareto_figure(data: HigherRankDevelopmentFigureData) -> Figure:
    figure, axes = _figure_grid(4, 2, width=13.5, height=14.5)
    block_counts = 2.0 * np.asarray(data.support_radii, dtype=np.float64) + 1.0
    for gauge_index, gauge in enumerate(data.gauge_alignment_names):
        for column, (values, label) in enumerate(
            (
                (data.total_operator, "total operator error"),
                (data.total_spectrum, "total spectrum error"),
            )
        ):
            axis = axes[gauge_index][column]
            for rank_index, _rank in enumerate(data.retained_ranks):
                for depth_index, _depth in enumerate(data.circuit_depths):
                    y = values[rank_index, depth_index, gauge_index]
                    finite = np.isfinite(y)
                    if not bool(np.any(finite)):
                        continue
                    color = _GAUGE_COLORS[rank_index]
                    linestyle = _DEPTH_LINESTYLES[depth_index]
                    axis.semilogy(
                        block_counts[finite],
                        _positive(y[finite]),
                        color=color,
                        linestyle=linestyle,
                        linewidth=0.8,
                        alpha=0.55,
                    )
                    efficient = (
                        data.pareto_efficient[rank_index, depth_index, gauge_index]
                        & finite
                    )
                    axis.scatter(
                        block_counts[efficient],
                        _positive(y[efficient]),
                        color=color,
                        marker="o",
                        s=12,
                        alpha=0.75,
                    )
            axis.set_xlabel("retained block count |Omega_S|=2S+1")
            axis.set_ylabel(label)
            axis.set_title(gauge)
            axis.grid(True, which="both", alpha=0.18)
    rank_handles = tuple(
        Line2D([0], [0], color=_GAUGE_COLORS[index], label=f"r={rank}")
        for index, rank in enumerate(data.retained_ranks)
    )
    depth_handles = tuple(
        Line2D(
            [0],
            [0],
            color="#333333",
            linestyle=_DEPTH_LINESTYLES[index],
            label=f"L={depth}",
        )
        for index, depth in enumerate(data.circuit_depths)
    )
    pareto_handle = Line2D(
        [0],
        [0],
        color="#333333",
        marker="o",
        linestyle="none",
        label="joint 3-objective nondominated support",
    )
    figure.legend(
        handles=(*rank_handles, *depth_handles, pareto_handle),
        loc="outside lower center",
        ncol=5,
    )
    return _finalize(figure, "Sampled support–error Pareto diagnostics")


__all__ = [
    "HigherRankDevelopmentFigureData",
    "HigherRankDevelopmentFigureDataProjector",
    "HigherRankDevelopmentFigureProjectionRequest",
    "HigherRankDevelopmentFigureRenderRequest",
    "HigherRankDevelopmentFigureRenderer",
    "HigherRankDevelopmentPlot",
]
