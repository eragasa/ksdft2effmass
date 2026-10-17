"""Campaign-owned rendering for sampled shell--scale decision landscapes."""

from __future__ import annotations

import math
import re
from dataclasses import dataclass
from pathlib import Path
from typing import cast

import matplotlib
from matplotlib import colormaps
from matplotlib.cm import ScalarMappable
from matplotlib.colors import Normalize

from ksdft2effmass.analysis.model_adequacy.band_equivalence_locality.decision_landscape import (  # noqa: E501
    ShellScaleCaseDecisionLandscape,
    ShellScaleDecisionLandscapeResult,
)

matplotlib.use("Agg")
from matplotlib import pyplot as plt  # noqa: E402
from mpl_toolkits.mplot3d.art3d import (  # type: ignore[import-untyped]  # noqa: E402
    Poly3DCollection,
)
from mpl_toolkits.mplot3d.axes3d import (  # type: ignore[import-untyped]  # noqa: E402
    Axes3D,
)

_STYLE: dict[str, str | float | int | bool] = {
    "font.family": "DejaVu Sans",
    "font.size": 7.5,
    "axes.titlesize": 8.5,
    "axes.labelsize": 8,
    "legend.fontsize": 6.5,
    "pdf.fonttype": 42,
    "ps.fonttype": 42,
}
_CASE_PRESENTATION = {
    "square-directed-parent": "Square directed parent",
    "matched-square-bravais-control": "Matched square Bravais control",
    "triangular-bravais-control": "Triangular Bravais control",
    "graphene-inspired-honeycomb": "Graphene-inspired honeycomb",
    "simple-cubic-directed-parent": "Simple-cubic directed parent",
    "matched-simple-cubic-bravais-control": "Matched simple-cubic Bravais control",
    "fcc-bravais-control": "FCC Bravais control",
    "silicon-inspired-diamond": "Silicon-inspired diamond",
}
_PRINCIPAL_CASES = (
    "square-directed-parent",
    "graphene-inspired-honeycomb",
    "simple-cubic-directed-parent",
    "silicon-inspired-diamond",
)


@dataclass(frozen=True, slots=True)
class ShellScaleDecisionLandscapePlotRequest:
    """Supply typed family landscapes and output policy."""

    family_results: tuple[ShellScaleDecisionLandscapeResult, ...]
    output_directory: Path

    def __post_init__(self) -> None:
        if type(self.family_results) is not tuple or not self.family_results:
            raise TypeError("family_results must be a nonempty tuple")
        if any(
            type(result) is not ShellScaleDecisionLandscapeResult
            for result in self.family_results
        ):
            raise TypeError(
                "family_results must contain ShellScaleDecisionLandscapeResult values"
            )
        families = tuple(result.family for result in self.family_results)
        if len(families) != len(set(families)):
            raise ValueError("family_results must contain each family at most once")
        case_names = tuple(
            case.name for result in self.family_results for case in result.cases
        )
        if len(case_names) != len(set(case_names)):
            raise ValueError("case names must be unique across family_results")
        if not isinstance(self.output_directory, Path):
            raise TypeError("output_directory must be pathlib.Path")


@dataclass(frozen=True, slots=True)
class ShellScaleDecisionLandscapePlotResult:
    """Identify all written individual and composite figures."""

    individual_paths: tuple[Path, ...]
    principal_composite_paths: tuple[Path, ...]

    @property
    def paths(self) -> tuple[Path, ...]:
        """Return every written path in deterministic order."""
        return self.individual_paths + self.principal_composite_paths


def _slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


def shell_scale_sampled_cell_triangles(
    case: ShellScaleCaseDecisionLandscape,
) -> tuple[tuple[int, int, int], ...]:
    """Triangulate adjacent calculated cells without objective-space interpolation."""
    if type(case) is not ShellScaleCaseDecisionLandscape:
        raise TypeError("case must be ShellScaleCaseDecisionLandscape")
    shell_count = len(case.shell_indices)
    scale_count = len(case.scale_path_coordinates)
    triangles: list[tuple[int, int, int]] = []
    for scale_index in range(scale_count - 1):
        for shell_index in range(shell_count - 1):
            lower_left = scale_index * shell_count + shell_index
            lower_right = lower_left + 1
            upper_left = (scale_index + 1) * shell_count + shell_index
            upper_right = upper_left + 1
            triangles.extend(
                (
                    (lower_left, lower_right, upper_right),
                    (lower_left, upper_right, upper_left),
                )
            )
    return tuple(triangles)


def _vertices(
    case: ShellScaleCaseDecisionLandscape,
) -> tuple[tuple[float, float, float], ...]:
    tiny = float.fromhex("0x1.0p-1022")
    return tuple(
        (
            float(point.retained_blocks),
            math.log10(max(point.maximum_hamiltonian_error, tiny)),
            math.log10(max(point.maximum_sorted_band_error, tiny)),
        )
        for point in case.points
    )


def render_shell_scale_decision_landscape(
    axis: Axes3D,
    case: ShellScaleCaseDecisionLandscape,
    *,
    title: str,
) -> None:
    """Render one case onto a supplied three-dimensional axis."""
    if not isinstance(axis, Axes3D):
        raise TypeError("axis must be a three-dimensional matplotlib axis")
    if type(case) is not ShellScaleCaseDecisionLandscape:
        raise TypeError("case must be ShellScaleCaseDecisionLandscape")
    if type(title) is not str or not title:
        raise ValueError("title must be a nonempty built-in str")
    vertices = _vertices(case)
    triangles = shell_scale_sampled_cell_triangles(case)
    faces = tuple(tuple(vertices[index] for index in indices) for indices in triangles)
    face_coordinates = tuple(
        sum(case.points[index].scale_path_coordinate for index in indices) / 3.0
        for indices in triangles
    )
    color_map = colormaps["viridis"]
    normalization = Normalize(0.0, 1.0)
    axis.add_collection3d(
        Poly3DCollection(
            faces,
            facecolors=[color_map(normalization(value)) for value in face_coordinates],
            edgecolors=(0.1, 0.1, 0.1, 0.24),
            linewidths=0.3,
            alpha=0.84,
        )
    )
    efficient_indices = tuple(
        index for index, point in enumerate(case.points) if point.pareto_efficient
    )
    axis.scatter(
        [vertices[index][0] for index in efficient_indices],
        [vertices[index][1] for index in efficient_indices],
        [vertices[index][2] for index in efficient_indices],
        s=20,
        color="#D55E00",
        edgecolor="black",
        linewidth=0.35,
        label="nondominated calculated vertices",
        depthshade=False,
    )
    axis.set_xlim(
        min(value[0] for value in vertices), max(value[0] for value in vertices)
    )
    axis.set_ylim(
        min(value[1] for value in vertices), max(value[1] for value in vertices)
    )
    axis.set_zlim(
        min(value[2] for value in vertices), max(value[2] for value in vertices)
    )
    axis.set_xlabel("retained hopping blocks")
    axis.set_ylabel(r"$\log_{10}$ max Hamiltonian error")
    axis.set_zlabel(r"$\log_{10}$ max sorted-band error")
    axis.set_title(title)
    axis.view_init(elev=24, azim=-58)
    axis.legend(frameon=False, fontsize=5.8, loc="upper left")
    axis.text2D(
        0.98,
        0.015,
        (
            f"{case.calculated_vertex_count} calculated; "
            f"{case.pareto_efficient_vertex_count} nondominated"
        ),
        transform=axis.transAxes,
        ha="right",
        fontsize=5.8,
        color="#666666",
        weight="bold",
    )


class ShellScaleDecisionLandscapePlotWriter:
    """Write one plot per case and one four-case principal composite."""

    __slots__ = ()

    def execute(
        self, request: ShellScaleDecisionLandscapePlotRequest
    ) -> ShellScaleDecisionLandscapePlotResult:
        """Render deterministic PDF and PNG development figures."""
        if type(request) is not ShellScaleDecisionLandscapePlotRequest:
            raise TypeError("request must be ShellScaleDecisionLandscapePlotRequest")
        request.output_directory.mkdir(parents=True, exist_ok=True)
        cases = tuple(
            case for result in request.family_results for case in result.cases
        )
        individual_paths: list[Path] = []
        color_map = colormaps["viridis"]
        normalization = Normalize(0.0, 1.0)
        with matplotlib.rc_context(_STYLE):  # type: ignore[arg-type]
            for case in cases:
                figure = plt.figure(figsize=(8.5, 6.6), constrained_layout=True)
                axis = cast(Axes3D, figure.add_subplot(111, projection="3d"))
                render_shell_scale_decision_landscape(
                    axis,
                    case,
                    title=(
                        f"{_CASE_PRESENTATION.get(case.name, case.name)}\n"
                        r"sampled $\lambda$--shell decision landscape"
                    ),
                )
                colorbar = figure.colorbar(
                    ScalarMappable(norm=normalization, cmap=color_map),
                    ax=axis,
                    shrink=0.62,
                    pad=0.08,
                )
                colorbar.set_label(r"scale path $u$ ($0=\lambda_*$, $1=1$)")
                stem = request.output_directory / (
                    f"{_slug(case.name)}-shell-scale-decision-landscape"
                )
                figure.savefig(stem.with_suffix(".pdf"), bbox_inches="tight")
                figure.savefig(stem.with_suffix(".png"), dpi=400, bbox_inches="tight")
                plt.close(figure)
                individual_paths.extend(
                    (stem.with_suffix(".pdf"), stem.with_suffix(".png"))
                )

            case_by_name = {case.name: case for case in cases}
            composite_paths: tuple[Path, ...]
            if all(name in case_by_name for name in _PRINCIPAL_CASES):
                composite = plt.figure(figsize=(11.5, 10.0), constrained_layout=True)
                composite_axes: list[Axes3D] = []
                for index, name in enumerate(_PRINCIPAL_CASES, start=1):
                    axis = cast(
                        Axes3D,
                        composite.add_subplot(2, 2, index, projection="3d"),
                    )
                    render_shell_scale_decision_landscape(
                        axis,
                        case_by_name[name],
                        title=_CASE_PRESENTATION[name],
                    )
                    composite_axes.append(axis)
                composite.colorbar(
                    ScalarMappable(norm=normalization, cmap=color_map),
                    ax=composite_axes,
                    shrink=0.54,
                    pad=0.04,
                    label=r"scale path $u$ ($0=\lambda_*$, $1=1$)",
                )
                composite.suptitle(
                    "Principal sampled shell--scale decision landscapes\n"
                    "Tessellation connects adjacent calculated samples only",
                    fontsize=11,
                )
                composite_stem = (
                    request.output_directory
                    / "principal-shell-scale-decision-landscapes"
                )
                composite.savefig(
                    composite_stem.with_suffix(".pdf"), bbox_inches="tight"
                )
                composite.savefig(
                    composite_stem.with_suffix(".png"),
                    dpi=400,
                    bbox_inches="tight",
                )
                plt.close(composite)
                composite_paths = (
                    composite_stem.with_suffix(".pdf"),
                    composite_stem.with_suffix(".png"),
                )
            else:
                composite_paths = ()
        return ShellScaleDecisionLandscapePlotResult(
            individual_paths=tuple(individual_paths),
            principal_composite_paths=composite_paths,
        )


__all__ = [
    "ShellScaleDecisionLandscapePlotRequest",
    "ShellScaleDecisionLandscapePlotResult",
    "ShellScaleDecisionLandscapePlotWriter",
    "render_shell_scale_decision_landscape",
    "shell_scale_sampled_cell_triangles",
]
