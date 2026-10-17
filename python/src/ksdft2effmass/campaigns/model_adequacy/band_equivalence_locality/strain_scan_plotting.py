"""Campaign-owned rendering for sampled synthetic-strain witness scans."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import matplotlib

from ksdft2effmass.analysis.model_adequacy.band_equivalence_locality.strain import (
    SyntheticStrainResult,
)
from ksdft2effmass.analysis.model_adequacy.band_equivalence_locality.strain_response import (  # noqa: E501
    StrainResponseModel,
    StrainWitnessControl,
    SyntheticStrainResponseResult,
    SyntheticStrainWitnessScanResult,
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
    "legend.fontsize": 6.5,
    "lines.linewidth": 1.4,
    "pdf.fonttype": 42,
    "ps.fonttype": 42,
}
_CONTROL_PRESENTATION = {
    StrainWitnessControl.GEOMETRY_ONLY: ("geometry-only", _BLUE),
    StrainWitnessControl.FROZEN_PARENT: ("frozen-parent null", _GREEN),
    StrainWitnessControl.RADIAL_RESPONSE: ("synthetic radial response", _VERMILION),
}


@dataclass(frozen=True, slots=True)
class SyntheticStrainScanPlotRequest:
    """Supply typed scan diagnostics and publication-neutral output policy."""

    witness_results: tuple[SyntheticStrainWitnessScanResult, ...]
    geometry_result: SyntheticStrainResult
    frozen_response: SyntheticStrainResponseResult
    radial_response: SyntheticStrainResponseResult
    output_directory: Path
    title: str

    def __post_init__(self) -> None:
        expected_controls = set(StrainWitnessControl)
        if type(self.witness_results) is not tuple or len(self.witness_results) != len(
            expected_controls
        ):
            raise ValueError("witness_results must contain all three controls")
        if any(
            type(result) is not SyntheticStrainWitnessScanResult
            for result in self.witness_results
        ):
            raise TypeError(
                "witness_results must contain SyntheticStrainWitnessScanResult"
            )
        controls = {result.control for result in self.witness_results}
        if controls != expected_controls:
            raise ValueError("witness_results must contain each control exactly once")
        if type(self.geometry_result) is not SyntheticStrainResult:
            raise TypeError("geometry_result must be SyntheticStrainResult")
        if type(self.frozen_response) is not SyntheticStrainResponseResult:
            raise TypeError("frozen_response must be SyntheticStrainResponseResult")
        if type(self.radial_response) is not SyntheticStrainResponseResult:
            raise TypeError("radial_response must be SyntheticStrainResponseResult")
        if self.frozen_response.model is not StrainResponseModel.M1_FROZEN:
            raise ValueError("frozen_response must use the frozen-parent model")
        if self.radial_response.model is not StrainResponseModel.M2_RADIAL:
            raise ValueError("radial_response must use the radial-response model")
        path = self.geometry_result.path
        if any(result.path is not path for result in self.witness_results) or (
            self.frozen_response.path is not path
            or self.radial_response.path is not path
        ):
            raise ValueError("all scan diagnostics must use the same strain path")
        fractions = tuple(
            point.strain_fraction for point in self.geometry_result.points
        )
        inventories = (
            *(
                tuple(point.strain_fraction for point in result.points)
                for result in self.witness_results
            ),
            tuple(point.strain_fraction for point in self.frozen_response.points),
            tuple(point.strain_fraction for point in self.radial_response.points),
        )
        if any(inventory != fractions for inventory in inventories):
            raise ValueError("all scan diagnostics must use identical strain fractions")
        if not isinstance(self.output_directory, Path):
            raise TypeError("output_directory must be pathlib.Path")
        if type(self.title) is not str or not self.title:
            raise ValueError("title must be a nonempty string")


@dataclass(frozen=True, slots=True)
class SyntheticStrainScanPlotResult:
    """Identify the sampled scan plots written by one request."""

    paths: tuple[Path, ...]


class SyntheticStrainScanPlotWriter:
    """Render witness, locality, and response scan channels without accepting them."""

    __slots__ = ()

    def execute(
        self, request: SyntheticStrainScanPlotRequest
    ) -> SyntheticStrainScanPlotResult:
        """Write PDF and PNG views of one sampled strain scan."""
        if type(request) is not SyntheticStrainScanPlotRequest:
            raise TypeError("request must be SyntheticStrainScanPlotRequest")
        request.output_directory.mkdir(parents=True, exist_ok=True)
        fractions = tuple(
            point.strain_fraction for point in request.geometry_result.points
        )
        witness_by_control = {
            result.control: result for result in request.witness_results
        }
        with matplotlib.rc_context(_STYLE):  # type: ignore[arg-type]
            figure, axes = plt.subplots(
                3,
                2,
                figsize=(8.2, 9.2),
                constrained_layout=True,
            )
            for control in StrainWitnessControl:
                result = witness_by_control[control]
                label, color = _CONTROL_PRESENTATION[control]
                axes[0, 0].plot(
                    fractions,
                    tuple(
                        point.pointwise_optimized_operator_threshold
                        for point in result.points
                    ),
                    color=color,
                    label=label,
                )
                axes[0, 1].plot(
                    fractions,
                    tuple(
                        point.fixed_candidate_operator_threshold
                        for point in result.points
                    ),
                    color=color,
                    label=label,
                )
            axes[0, 0].set_title("(a) pointwise optimized requirement")
            axes[0, 0].set_ylabel("operator threshold")
            axes[0, 1].set_title("(b) fixed $p_0=(0,1)$ candidate requirement")
            axes[0, 1].set_ylabel("operator threshold")
            axes[0, 0].legend(frameon=False)

            for tolerance_index, tolerance in enumerate(
                request.geometry_result.tail_tolerances
            ):
                label = rf"tail $\leq {tolerance:.0e}$"
                axes[1, 0].plot(
                    fractions,
                    tuple(
                        point.first_passing_radius[tolerance_index]
                        for point in request.geometry_result.points
                    ),
                    marker=".",
                    label=label,
                )
                axes[1, 1].step(
                    fractions,
                    tuple(
                        point.first_passing_blocks[tolerance_index]
                        for point in request.geometry_result.points
                    ),
                    where="mid",
                    label=label,
                )
            axes[1, 0].set_title("(c) geometry-only physical range")
            axes[1, 0].set_ylabel("first-passing radius")
            axes[1, 1].set_title("(d) geometry-only representation size")
            axes[1, 1].set_ylabel("retained blocks")
            axes[1, 0].legend(frameon=False)

            axes[2, 0].semilogy(
                fractions,
                tuple(
                    point.aligned_strain_perturbation.maximum_hamiltonian
                    for point in request.frozen_response.points
                ),
                color=_GREEN,
                label="frozen-parent null",
            )
            axes[2, 0].semilogy(
                fractions,
                tuple(
                    point.aligned_strain_perturbation.maximum_hamiltonian
                    for point in request.radial_response.points
                ),
                color=_VERMILION,
                label="synthetic radial response",
            )
            axes[2, 0].set_title("(e) aligned strain response")
            axes[2, 0].set_ylabel("maximum Hamiltonian defect")
            axes[2, 0].legend(frameon=False)

            axes[2, 1].plot(
                fractions,
                tuple(
                    point.minimum_hopping_response
                    for point in request.radial_response.points
                ),
                color=_BLUE,
                label="minimum response",
            )
            axes[2, 1].plot(
                fractions,
                tuple(
                    point.maximum_hopping_response
                    for point in request.radial_response.points
                ),
                color=_VERMILION,
                label="maximum response",
            )
            axes[2, 1].axhline(1.0, color=_BLACK, linestyle=":", linewidth=0.8)
            axes[2, 1].set_title("(f) prescribed radial factors")
            axes[2, 1].set_ylabel(r"$t_j(t)/t_j(0)$")
            axes[2, 1].legend(frameon=False)

            for axis in axes.flat:
                axis.set_xlabel("strain fraction")
                axis.grid(alpha=0.22)
            figure.suptitle(
                request.title
                + "\nSampled development scan; not a continuum certificate",
                fontsize=10.5,
            )
            stem = request.output_directory / "strain-witness-locality-scan"
            figure.savefig(stem.with_suffix(".pdf"), bbox_inches="tight")
            figure.savefig(stem.with_suffix(".png"), dpi=400, bbox_inches="tight")
            plt.close(figure)
        return SyntheticStrainScanPlotResult(
            (stem.with_suffix(".pdf"), stem.with_suffix(".png"))
        )


__all__ = [
    "SyntheticStrainScanPlotRequest",
    "SyntheticStrainScanPlotResult",
    "SyntheticStrainScanPlotWriter",
]
