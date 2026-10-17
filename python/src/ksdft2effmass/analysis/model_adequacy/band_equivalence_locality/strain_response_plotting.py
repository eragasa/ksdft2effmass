"""Plot bounded M1/M2 synthetic strain-response diagnostics."""

from __future__ import annotations

from pathlib import Path

import matplotlib
import numpy as np

from .strain_response import StrainErrorChannels, SyntheticStrainResponseResult

matplotlib.use("Agg")
from matplotlib import pyplot as plt  # noqa: E402

_BLUE = "#0072B2"
_VERMILION = "#D55E00"
_GREEN = "#009E73"
_PURPLE = "#CC79A7"
_BLACK = "#202020"


def _positive(value: float) -> float:
    return max(value, np.finfo(np.float64).tiny)


def _maximum_or_zero(channels: StrainErrorChannels | None) -> float:
    return 0.0 if channels is None else channels.maximum_hamiltonian


def _panel(axis: plt.Axes, label: str) -> None:
    axis.text(
        -0.13,
        1.04,
        label,
        transform=axis.transAxes,
        fontsize=9,
        fontweight="bold",
        ha="left",
        va="bottom",
    )


def write_strain_response_plots(
    frozen: SyntheticStrainResponseResult,
    radial: SyntheticStrainResponseResult,
    output: Path,
    title: str,
) -> tuple[Path, Path]:
    """Write one vector PDF and 600-dpi PNG M1/M2 comparison."""
    if type(frozen) is not SyntheticStrainResponseResult:
        raise TypeError("frozen must be SyntheticStrainResponseResult")
    if type(radial) is not SyntheticStrainResponseResult:
        raise TypeError("radial must be SyntheticStrainResponseResult")
    if frozen.path is not radial.path:
        raise ValueError("M1 and M2 paths must match")
    if frozen.tail_tolerances != radial.tail_tolerances:
        raise ValueError("M1 and M2 tail tolerances must match")
    if len(radial.tail_tolerances) != 2:
        raise ValueError("the maintained plot requires exactly two tail tolerances")
    if not isinstance(output, Path):
        raise TypeError("output must be pathlib.Path")
    if type(title) is not str or not title:
        raise ValueError("title must be a nonempty string")
    output.mkdir(parents=True, exist_ok=True)

    style = {
        "font.family": "DejaVu Sans",
        "font.size": 7.5,
        "axes.titlesize": 8.5,
        "axes.labelsize": 8,
        "legend.fontsize": 6.5,
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
    }
    with matplotlib.rc_context(style):  # type: ignore[arg-type]
        figure, axes = plt.subplots(2, 2, figsize=(7.4, 6.2), constrained_layout=True)
        strain = [point.strain_fraction for point in radial.points]
        axes[0, 0].plot(
            strain,
            [point.minimum_hopping_response for point in radial.points],
            "o-",
            color=_BLUE,
            label="M2 minimum",
        )
        axes[0, 0].plot(
            strain,
            [point.maximum_hopping_response for point in radial.points],
            "s--",
            color=_VERMILION,
            label="M2 maximum",
        )
        axes[0, 0].axhline(1.0, color=_BLACK, linestyle=":", label="M1 frozen")
        axes[0, 0].set_ylabel("bond hopping response $t_j(s)/t_j(0)$")
        axes[0, 0].set_title("Fixed radial response")
        axes[0, 0].legend(frameon=False)

        axes[0, 1].semilogy(
            strain,
            [
                _positive(point.aligned_strain_perturbation.maximum_hamiltonian)
                for point in frozen.points
            ],
            "o-",
            color=_BLACK,
            label="M1 aligned $\\Delta H$",
        )
        axes[0, 1].semilogy(
            strain,
            [
                _positive(point.aligned_strain_perturbation.maximum_hamiltonian)
                for point in radial.points
            ],
            "o-",
            color=_VERMILION,
            label="M2 full $\\Delta H$",
        )
        axes[0, 1].semilogy(
            strain,
            [
                _positive(point.maximum_scalar_strain_component)
                for point in radial.points
            ],
            "^--",
            color=_GREEN,
            label="M2 scalar",
        )
        axes[0, 1].semilogy(
            strain,
            [
                _positive(point.maximum_traceless_strain_component)
                for point in radial.points
            ],
            "s--",
            color=_PURPLE,
            label="M2 traceless",
        )
        axes[0, 1].set_ylabel("maximum channel / $E_{\\mathrm{ref}}$")
        axes[0, 1].set_title("Gauge-aligned strain perturbation")
        axes[0, 1].legend(frameon=False)

        colors = (_BLUE, _VERMILION)
        for index, tolerance in enumerate(radial.tail_tolerances):
            axes[1, 0].plot(
                strain,
                [point.cutoffs[index].physical_radius for point in frozen.points],
                "o:",
                color=colors[index],
                label=rf"M1 tail $\leq {tolerance:.0e}$",
            )
            axes[1, 0].plot(
                strain,
                [point.cutoffs[index].physical_radius for point in radial.points],
                "s-",
                color=colors[index],
                label=rf"M2 tail $\leq {tolerance:.0e}$",
            )
        axes[1, 0].set_ylabel("first-passing physical radius")
        axes[1, 0].set_title("Locality cost")
        axes[1, 0].legend(frameon=False, ncol=2)

        strict_index = len(radial.tail_tolerances) - 1
        axes[1, 1].semilogy(
            strain,
            [
                _positive(point.delta_interpolation.maximum_hamiltonian)
                for point in radial.points
            ],
            color=_BLACK,
            linestyle=":",
            label="interpolation",
        )
        axes[1, 1].semilogy(
            strain,
            [
                _positive(
                    _maximum_or_zero(point.cutoffs[strict_index].delta_truncation)
                )
                for point in radial.points
            ],
            color=_BLUE,
            marker="o",
            label="deliberate truncation",
        )
        axes[1, 1].semilogy(
            strain,
            [
                _positive(_maximum_or_zero(point.cutoffs[strict_index].delta_total))
                for point in radial.points
            ],
            color=_VERMILION,
            linestyle="--",
            label="total versus direct",
        )
        axes[1, 1].set_ylabel("M2 $\\Delta H$ error / $E_{\\mathrm{ref}}$")
        axes[1, 1].set_title(
            rf"Three channels at tail $\leq {radial.tail_tolerances[-1]:.0e}$"
        )
        axes[1, 1].legend(frameon=False)

        for label, axis in zip(("(a)", "(b)", "(c)", "(d)"), axes.flat, strict=True):
            _panel(axis, label)
            axis.set_xlabel("strain fraction")
            axis.grid(True, which="both", alpha=0.22, linewidth=0.5)
        figure.suptitle(
            f"{title}: bounded M1/M2 synthetic strain controls", fontsize=11
        )
        stem = output / "m1-m2-strain-response"
        metadata = {
            "Title": f"{title}: M1/M2 synthetic strain controls",
            "Subject": "Replaceable bounded synthetic development diagnostics",
        }
        figure.savefig(stem.with_suffix(".pdf"), bbox_inches="tight", metadata=metadata)
        figure.savefig(
            stem.with_suffix(".png"),
            dpi=600,
            bbox_inches="tight",
            metadata=metadata,
        )
        plt.close(figure)
    return stem.with_suffix(".pdf"), stem.with_suffix(".png")


__all__ = ["write_strain_response_plots"]
