"""Campaign-owned plots for typed band-equivalence/locality diagnostics."""

from __future__ import annotations

import math
from dataclasses import dataclass
from pathlib import Path

import matplotlib
import numpy as np

from ksdft2effmass.analysis.model_adequacy.band_equivalence_locality.constrained_bessel import (  # noqa: E501
    ConstrainedBesselGeometry,
    ConstrainedBesselTailDiagnostic,
    ConstrainedBesselTailRequest,
)
from ksdft2effmass.analysis.model_adequacy.band_equivalence_locality.records import (
    BandEquivalenceLocalityDiagnostics,
)

matplotlib.use("Agg")
from matplotlib import pyplot as plt  # noqa: E402

_BLUE = "#0072B2"
_VERMILION = "#D55E00"
_GREEN = "#009E73"
_BLACK = "#202020"
_STYLE: dict[str, str | float | int | bool] = {
    "font.family": "DejaVu Sans",
    "font.size": 7.5,
    "axes.titlesize": 8.5,
    "axes.labelsize": 8,
    "axes.linewidth": 0.7,
    "xtick.labelsize": 7,
    "ytick.labelsize": 7,
    "legend.fontsize": 6.5,
    "lines.linewidth": 1.4,
    "pdf.fonttype": 42,
    "ps.fonttype": 42,
    "savefig.transparent": False,
}


@dataclass(frozen=True, slots=True)
class BandEquivalenceLocalityPlotRequest:
    """Supply typed diagnostics and output policy for one plot set."""

    mesh_results: tuple[BandEquivalenceLocalityDiagnostics, ...]
    output_directory: Path
    title: str
    constrained_geometry: ConstrainedBesselGeometry | None = None
    constrained_shell_cap: int | None = None
    constrained_kernel_cap: int | None = None

    def __post_init__(self) -> None:
        if type(self.mesh_results) is not tuple or len(self.mesh_results) < 2:
            raise ValueError("mesh_results must contain at least two diagnostics")
        if any(
            type(result) is not BandEquivalenceLocalityDiagnostics
            for result in self.mesh_results
        ):
            raise TypeError(
                "mesh_results must contain BandEquivalenceLocalityDiagnostics"
            )
        family = self.mesh_results[0].family
        if any(result.family is not family for result in self.mesh_results):
            raise ValueError("mesh_results must belong to one family")
        sizes = tuple(result.construction_size for result in self.mesh_results)
        if tuple(sorted(sizes)) != sizes or len(set(sizes)) != len(sizes):
            raise ValueError("mesh_results must have strictly increasing mesh sizes")
        case_names = tuple(case.name for case in self.mesh_results[0].cases)
        if any(
            tuple(case.name for case in result.cases) != case_names
            for result in self.mesh_results[1:]
        ):
            raise ValueError("mesh_results must have identical ordered cases")
        point_identities = tuple(
            tuple((point.parent_scale, point.amplitude) for point in case.points)
            for case in self.mesh_results[0].cases
        )
        if any(
            tuple(
                tuple((point.parent_scale, point.amplitude) for point in case.points)
                for case in result.cases
            )
            != point_identities
            for result in self.mesh_results[1:]
        ):
            raise ValueError(
                "mesh_results must have identical ordered point identities"
            )
        if not isinstance(self.output_directory, Path):
            raise TypeError("output_directory must be pathlib.Path")
        if type(self.title) is not str or not self.title:
            raise ValueError("title must be a nonempty string")
        constrained = (
            self.constrained_geometry,
            self.constrained_shell_cap,
            self.constrained_kernel_cap,
        )
        if any(value is not None for value in constrained) and any(
            value is None for value in constrained
        ):
            raise ValueError("all constrained-tail controls must be supplied together")
        if (
            self.constrained_geometry is not None
            and type(self.constrained_geometry) is not ConstrainedBesselGeometry
        ):
            raise TypeError("constrained_geometry must be ConstrainedBesselGeometry")
        for name, value in (
            ("constrained_shell_cap", self.constrained_shell_cap),
            ("constrained_kernel_cap", self.constrained_kernel_cap),
        ):
            if value is not None and (type(value) is not int or value < 0):
                raise ValueError(f"{name} must be a nonnegative built-in int")


@dataclass(frozen=True, slots=True)
class BandEquivalenceLocalityPlotResult:
    """Identify every plot artifact written by one request."""

    paths: tuple[Path, ...]


class BandEquivalenceLocalityPlotWriter:
    """Write the maintained campaign plot set from typed diagnostics."""

    __slots__ = ()

    def execute(
        self, request: BandEquivalenceLocalityPlotRequest
    ) -> BandEquivalenceLocalityPlotResult:
        if type(request) is not BandEquivalenceLocalityPlotRequest:
            raise TypeError("request must be BandEquivalenceLocalityPlotRequest")
        request.output_directory.mkdir(parents=True, exist_ok=True)
        smoke = request.mesh_results[0]
        refined = request.mesh_results[-1]
        stems: list[Path] = []
        with matplotlib.rc_context(_STYLE):  # type: ignore[arg-type]
            stems.append(self._write_scientific_story(request, smoke, refined))
            stems.append(self._write_mesh_summary(request))
            stems.append(self._write_error_decomposition(request, refined))
            stems.append(self._write_shell_profiles(request, smoke, refined))
            stems.append(self._write_first_passing_stability(request, smoke, refined))
            if request.constrained_geometry is not None:
                stems.append(self._write_constrained_tail(request))
        return BandEquivalenceLocalityPlotResult(
            tuple(
                path
                for stem in stems
                for path in (stem.with_suffix(".pdf"), stem.with_suffix(".png"))
            )
        )

    def _write_scientific_story(
        self,
        request: BandEquivalenceLocalityPlotRequest,
        smoke: BandEquivalenceLocalityDiagnostics,
        refined: BandEquivalenceLocalityDiagnostics,
    ) -> Path:
        figure, axes = plt.subplots(2, 2, figsize=(10.5, 7.0), constrained_layout=True)
        for case_index, (smoke_case, refined_case) in enumerate(
            zip(smoke.cases, refined.cases, strict=True)
        ):
            color = (_BLUE, _VERMILION, _GREEN)[case_index % 3]
            interpolation = (
                max(
                    max(
                        point.reference_interpolation.maximum_hamiltonian,
                        point.comparison_interpolation.maximum_hamiltonian,
                    )
                    for point in smoke_case.points
                ),
                max(
                    max(
                        point.reference_interpolation.maximum_hamiltonian,
                        point.comparison_interpolation.maximum_hamiltonian,
                    )
                    for point in refined_case.points
                ),
            )
            axes[0, 0].plot(
                (smoke.construction_size, refined.construction_size),
                interpolation,
                color=color,
                marker="o",
                label=smoke_case.name,
            )
            point = max(
                refined_case.points,
                key=lambda item: (item.parent_scale, item.amplitude),
            )
            axes[0, 1].plot(
                [shell.shell_index for shell in point.shell_diagnostics],
                [
                    max(
                        shell.comparison_total.maximum_hamiltonian,
                        np.finfo(np.float64).tiny,
                    )
                    for shell in point.shell_diagnostics
                ],
                color=color,
                marker=".",
                label=refined_case.name,
            )
            unit_scale_points = tuple(
                point
                for point in refined_case.points
                if point.parent_scale
                == max(item.parent_scale for item in refined_case.points)
            )
            axes[1, 0].plot(
                [point.amplitude for point in unit_scale_points],
                [
                    point.finite_mesh_maximum_correlation
                    if point.finite_mesh_maximum_correlation is not None
                    else float("nan")
                    for point in unit_scale_points
                ],
                color=color,
                marker="o",
                label=refined_case.name,
            )
            axes[1, 1].plot(
                [point.amplitude for point in unit_scale_points],
                [point.minimum_operator_threshold for point in unit_scale_points],
                color=color,
                marker="o",
                label=refined_case.name,
            )
        axes[0, 0].set_yscale("log")
        axes[0, 0].set_xlabel("construction mesh size per coordinate, N")
        axes[0, 0].set_ylabel(
            "maximum interpolation matrix error / $E_{\\mathrm{ref}}$"
        )
        axes[0, 0].set_title("Withheld-mesh interpolation")
        axes[0, 1].set_yscale("log")
        axes[0, 1].set_xlabel("complete physical-metric shell index")
        axes[0, 1].set_ylabel("comparison total matrix error / $E_{\\mathrm{ref}}$")
        axes[0, 1].set_title("Endpoint hopping locality")
        axes[1, 0].set_xlabel("gauge amplitude")
        axes[1, 0].set_ylabel("finite-mesh maximum correlation")
        axes[1, 0].set_title("Gauge-correlation response")
        axes[1, 1].set_xlabel("gauge amplitude")
        axes[1, 1].set_ylabel("minimum operator threshold / $E_{\\mathrm{ref}}$")
        axes[1, 1].set_title("Threshold response")
        for index, axis in enumerate(axes.flat):
            axis.grid(True, alpha=0.25)
            axis.text(
                -0.13,
                1.04,
                f"({chr(97 + index)})",
                transform=axis.transAxes,
                fontsize=9,
                fontweight="bold",
            )
            axis.legend(frameon=False)
        figure.suptitle(f"{request.title}: band equivalence and hopping locality")
        stem = request.output_directory / "band-equivalence-locality-scientific-story"
        metadata = {
            "Title": f"{request.title}: scientific story",
            "Subject": "Replaceable development diagnostics; not retained evidence",
        }
        figure.savefig(stem.with_suffix(".pdf"), bbox_inches="tight", metadata=metadata)
        figure.savefig(
            stem.with_suffix(".png"),
            dpi=600,
            bbox_inches="tight",
            metadata=metadata,
        )
        plt.close(figure)
        return stem

    def _write_mesh_summary(self, request: BandEquivalenceLocalityPlotRequest) -> Path:
        sizes = tuple(result.construction_size for result in request.mesh_results)
        case_levels = tuple(result.cases for result in request.mesh_results)
        figure, axes = plt.subplots(1, 2, figsize=(11.0, 4.2), constrained_layout=True)
        for case_index, first_case in enumerate(case_levels[0]):
            cases = tuple(level[case_index] for level in case_levels)
            interpolation = tuple(
                max(
                    max(
                        point.reference_interpolation.maximum_hamiltonian,
                        point.comparison_interpolation.maximum_hamiltonian,
                    )
                    for point in case.points
                )
                for case in cases
            )
            isolation = tuple(
                min(point.minimum_sampled_external_gap for point in case.points)
                for case in cases
            )
            axes[0].plot(sizes, interpolation, marker="o", label=first_case.name)
            axes[1].plot(sizes, isolation, marker="o", label=first_case.name)
        axes[0].set_yscale("log")
        axes[0].set_xlabel("construction mesh size per coordinate, N")
        axes[0].set_ylabel("maximum interpolation matrix error / $E_{\\mathrm{ref}}$")
        axes[0].set_title("Withheld-mesh interpolation")
        axes[1].set_xlabel("construction mesh size per coordinate, N")
        axes[1].set_ylabel("sampled external isolation gap / $E_{\\mathrm{ref}}$")
        axes[1].set_title("External retained-subspace isolation")
        for index, axis in enumerate(axes):
            axis.set_xticks(sizes)
            axis.grid(True, alpha=0.25)
            axis.text(
                -0.13,
                1.04,
                f"({chr(97 + index)})",
                transform=axis.transAxes,
                fontsize=9,
                fontweight="bold",
            )
        axes[1].legend(frameon=False)
        figure.suptitle(f"{request.title}: bounded mesh refinement", fontsize=11)
        stem = request.output_directory / "mesh-refinement-summary"
        metadata = {
            "Title": f"{request.title}: bounded mesh refinement",
            "Subject": "Replaceable development diagnostics; not convergence evidence",
        }
        figure.savefig(stem.with_suffix(".pdf"), bbox_inches="tight", metadata=metadata)
        figure.savefig(
            stem.with_suffix(".png"),
            dpi=600,
            bbox_inches="tight",
            metadata=metadata,
        )
        plt.close(figure)
        return stem

    def _write_error_decomposition(
        self,
        request: BandEquivalenceLocalityPlotRequest,
        refined: BandEquivalenceLocalityDiagnostics,
    ) -> Path:
        figure, axes = plt.subplots(
            len(refined.cases),
            2,
            figsize=(10.5, 3.1 * len(refined.cases)),
            squeeze=False,
            constrained_layout=True,
        )
        for row, case in enumerate(refined.cases):
            point = max(
                case.points, key=lambda item: (item.parent_scale, item.amplitude)
            )
            shells = point.shell_diagnostics
            shell_indices = [shell.shell_index for shell in shells]
            channel_rows = (
                (
                    [
                        max(
                            shell.comparison_truncation.maximum_hamiltonian,
                            np.finfo(np.float64).tiny,
                        )
                        for shell in shells
                    ],
                    [
                        max(
                            shell.comparison_total.maximum_hamiltonian,
                            np.finfo(np.float64).tiny,
                        )
                        for shell in shells
                    ],
                    max(
                        point.comparison_interpolation.maximum_hamiltonian,
                        np.finfo(np.float64).tiny,
                    ),
                ),
                (
                    [
                        max(
                            shell.comparison_truncation.maximum_band,
                            np.finfo(np.float64).tiny,
                        )
                        for shell in shells
                    ],
                    [
                        max(
                            shell.comparison_total.maximum_band,
                            np.finfo(np.float64).tiny,
                        )
                        for shell in shells
                    ],
                    max(
                        point.comparison_interpolation.maximum_band,
                        np.finfo(np.float64).tiny,
                    ),
                ),
            )
            for column, (truncation, total, interpolation) in enumerate(channel_rows):
                axis = axes[row, column]
                axis.axhline(
                    interpolation,
                    color=_BLACK,
                    linestyle=":",
                    label="interpolation",
                )
                axis.plot(
                    shell_indices,
                    truncation,
                    color=_BLUE,
                    marker="o",
                    label="deliberate truncation",
                )
                axis.plot(
                    shell_indices,
                    total,
                    color=_VERMILION,
                    linestyle="--",
                    label="total versus direct",
                )
                axis.set_yscale("log")
                axis.set_xlabel("complete physical-metric shell index")
                axis.set_ylabel(f"{case.name}\nerror / $E_{{\\mathrm{{ref}}}}$")
                axis.grid(True, which="both", alpha=0.22)
                axis.legend(frameon=False)
        axes[0, 0].set_title("Maximum Hamiltonian error", fontweight="bold")
        axes[0, 1].set_title("Maximum sorted-band error", fontweight="bold")
        figure.suptitle(f"{request.title}: three-channel error decomposition")
        stem = request.output_directory / "three-channel-error-decomposition"
        metadata = {
            "Title": f"{request.title}: three-channel error decomposition",
            "Subject": "Interpolation, truncation, and total error remain separate",
        }
        figure.savefig(stem.with_suffix(".pdf"), bbox_inches="tight", metadata=metadata)
        figure.savefig(
            stem.with_suffix(".png"),
            dpi=600,
            bbox_inches="tight",
            metadata=metadata,
        )
        plt.close(figure)
        return stem

    def _write_shell_profiles(
        self,
        request: BandEquivalenceLocalityPlotRequest,
        smoke: BandEquivalenceLocalityDiagnostics,
        refined: BandEquivalenceLocalityDiagnostics,
    ) -> Path:
        figure, axes = plt.subplots(
            len(smoke.cases),
            2,
            figsize=(11.0, 3.1 * len(smoke.cases)),
            squeeze=False,
            constrained_layout=True,
        )
        for row, (smoke_case, refined_case) in enumerate(
            zip(smoke.cases, refined.cases, strict=True)
        ):
            for case, mesh_label, color in (
                (smoke_case, "smoke mesh", _VERMILION),
                (refined_case, "refined mesh", _GREEN),
            ):
                point = max(
                    case.points,
                    key=lambda item: (item.parent_scale, item.amplitude),
                )
                shells = point.shell_diagnostics
                shell_indices = [shell.shell_index for shell in shells]
                axes[row, 0].plot(
                    shell_indices,
                    [
                        max(
                            shell.comparison_total.maximum_hamiltonian,
                            np.finfo(np.float64).tiny,
                        )
                        for shell in shells
                    ],
                    color=color,
                    label=f"{mesh_label}: matrix",
                )
                axes[row, 0].plot(
                    shell_indices,
                    [
                        max(
                            shell.comparison_total.maximum_band,
                            np.finfo(np.float64).tiny,
                        )
                        for shell in shells
                    ],
                    color=color,
                    linestyle="--",
                    label=f"{mesh_label}: band",
                )
                axes[row, 1].plot(
                    shell_indices,
                    [
                        max(
                            shell.comparison_omitted_power,
                            np.finfo(np.float64).tiny,
                        )
                        for shell in shells
                    ],
                    color=color,
                    marker=".",
                    label=mesh_label,
                )
            axes[row, 0].set_yscale("log")
            axes[row, 1].set_yscale("log")
            axes[row, 0].set_ylabel(
                f"{smoke_case.name}\nerror / $E_{{\\mathrm{{ref}}}}$"
            )
            axes[row, 1].set_ylabel("omitted block power / $E_{\\mathrm{ref}}^2$")
            for axis in axes[row]:
                axis.set_xlabel("complete physical-metric shell index")
                axis.grid(True, alpha=0.25)
                axis.legend(frameon=False)
        axes[0, 0].set_title("Endpoint total reconstruction errors")
        axes[0, 1].set_title("Endpoint comparison omitted power")
        stem = request.output_directory / "shell-locality-profiles"
        metadata = {
            "Title": f"{request.title}: hopping-locality profiles",
            "Subject": "Separated matrix, spectral, and omitted-power channels",
        }
        figure.savefig(stem.with_suffix(".pdf"), bbox_inches="tight", metadata=metadata)
        figure.savefig(
            stem.with_suffix(".png"),
            dpi=600,
            bbox_inches="tight",
            metadata=metadata,
        )
        plt.close(figure)
        return stem

    def _write_first_passing_stability(
        self,
        request: BandEquivalenceLocalityPlotRequest,
        smoke: BandEquivalenceLocalityDiagnostics,
        refined: BandEquivalenceLocalityDiagnostics,
    ) -> Path:
        rows: list[list[float]] = []
        annotations: list[list[str]] = []
        labels: list[str] = []
        for smoke_case, refined_case in zip(smoke.cases, refined.cases, strict=True):
            for smoke_point, refined_point in zip(
                smoke_case.points,
                refined_case.points,
                strict=True,
            ):
                for before, after in zip(
                    smoke_point.first_passing,
                    refined_point.first_passing,
                    strict=True,
                ):
                    before_values = (
                        before.reference_hamiltonian_shell,
                        before.reference_band_shell,
                        before.comparison_hamiltonian_shell,
                        before.comparison_band_shell,
                    )
                    after_values = (
                        after.reference_hamiltonian_shell,
                        after.reference_band_shell,
                        after.comparison_hamiltonian_shell,
                        after.comparison_band_shell,
                    )
                    row: list[float] = []
                    text_row: list[str] = []
                    for left, right in zip(before_values, after_values, strict=True):
                        left_text = "U" if left is None else str(left)
                        right_text = "U" if right is None else str(right)
                        text_row.append(f"{left_text}→{right_text}")
                        row.append(
                            float("nan")
                            if left is None or right is None
                            else float(right - left)
                        )
                    rows.append(row)
                    annotations.append(text_row)
                    labels.append(
                        f"{smoke_case.name} | ρ={smoke_point.parent_scale:.0f}"
                        f" | a={smoke_point.amplitude:.3g}"
                        f" | τ={before.tolerance:.0e}"
                    )
        matrix = np.asarray(rows, dtype=np.float64)
        finite_differences = np.abs(matrix[np.isfinite(matrix)])
        limit = (
            max(1.0, float(np.max(finite_differences)))
            if finite_differences.size
            else 1.0
        )
        masked = np.ma.masked_invalid(matrix)
        colormap = matplotlib.colormaps["coolwarm"].with_extremes(bad="#d9d9d9")
        figure, axis = plt.subplots(
            figsize=(10.5, max(5.0, 0.31 * len(labels) + 1.8)),
            constrained_layout=True,
        )
        image = axis.imshow(
            masked,
            cmap=colormap,
            vmin=-limit,
            vmax=limit,
            aspect="auto",
        )
        axis.set_xticks(
            range(4),
            labels=("ref H", "ref bands", "comparison H", "comparison bands"),
        )
        axis.set_yticks(range(len(labels)), labels=labels, fontsize=7)
        for row_index, text_row in enumerate(annotations):
            for column_index, text in enumerate(text_row):
                axis.text(column_index, row_index, text, ha="center", va="center")
        colorbar = figure.colorbar(image, ax=axis, shrink=0.7)
        colorbar.set_label("refinement shell minus smoke shell")
        stem = request.output_directory / "first-passing-shell-stability"
        metadata = {
            "Title": f"{request.title}: first-passing shell stability",
            "Subject": "Smoke-to-refinement sampled decision comparison",
        }
        figure.savefig(stem.with_suffix(".pdf"), bbox_inches="tight", metadata=metadata)
        figure.savefig(
            stem.with_suffix(".png"),
            dpi=600,
            bbox_inches="tight",
            metadata=metadata,
        )
        plt.close(figure)
        return stem

    def _write_constrained_tail(
        self, request: BandEquivalenceLocalityPlotRequest
    ) -> Path:
        geometry = request.constrained_geometry
        shell_cap = request.constrained_shell_cap
        kernel_cap = request.constrained_kernel_cap
        assert geometry is not None
        assert shell_cap is not None
        assert kernel_cap is not None
        shells = tuple(range(shell_cap + 1))
        diagnostic = ConstrainedBesselTailDiagnostic()
        bounds = tuple(
            diagnostic.execute(
                ConstrainedBesselTailRequest(
                    geometry=geometry,
                    maximum_rotation_amplitude=math.pi / 4.0,
                    shell_cap=shell,
                    kernel_cap=kernel_cap,
                    numerical_margin=1.0e-13,
                )
            ).tail_power_upper_bound
            for shell in shells
        )
        figure, axis = plt.subplots(figsize=(7.2, 4.4), constrained_layout=True)
        axis.semilogy(
            shells,
            [max(value, np.finfo(np.float64).tiny) for value in bounds],
            color=_BLUE,
            marker="o",
        )
        axis.set_xlabel("complete physical-metric shell cap")
        axis.set_ylabel("certified normalized scalar-tail upper bound")
        axis.grid(True, which="both", alpha=0.2)
        stem = request.output_directory / "constrained-bessel-tail-certificate"
        metadata = {
            "Title": f"{request.title}: constrained-Bessel tail",
            "Subject": "Replaceable binary64 development certificate",
        }
        figure.savefig(stem.with_suffix(".pdf"), bbox_inches="tight", metadata=metadata)
        figure.savefig(
            stem.with_suffix(".png"),
            dpi=600,
            bbox_inches="tight",
            metadata=metadata,
        )
        plt.close(figure)
        return stem


__all__ = [
    "BandEquivalenceLocalityPlotRequest",
    "BandEquivalenceLocalityPlotResult",
    "BandEquivalenceLocalityPlotWriter",
]
