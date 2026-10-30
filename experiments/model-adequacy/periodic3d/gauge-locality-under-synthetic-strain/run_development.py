"""Run and plot the bounded 3-D frozen-gauge Bain-strain control."""

from __future__ import annotations

import math
from pathlib import Path

import matplotlib.pyplot as plt
from ksdft2effmass.analysis.model_adequacy.band_equivalence_locality.strain import (
    SyntheticStrainCalculator,
    SyntheticStrainPathEnum,
)

FRACTIONS = tuple(float(index) / 8.0 for index in range(9))


def main() -> int:
    """Write replaceable typed JSON, PDF, and PNG development diagnostics."""
    result = SyntheticStrainCalculator(
        path=SyntheticStrainPathEnum.BAIN_3D,
        construction_size=24,
        strain_fractions=FRACTIONS,
        maximum_rotation_amplitude=math.pi / 4.0,
        tail_tolerances=(1.0e-3, 1.0e-5),
    ).execute()
    output = Path(__file__).resolve().parent / "analysis" / "development"
    output.mkdir(parents=True, exist_ok=True)
    typed_result_path = output / "development-result.json"
    typed_result_path.write_bytes(result.to_json())
    with plt.rc_context(
        {
            "font.family": "DejaVu Sans",
            "font.size": 7.5,
            "axes.titlesize": 8.5,
            "axes.labelsize": 8,
            "legend.fontsize": 6.5,
            "pdf.fonttype": 42,
        }
    ):
        figure, axes = plt.subplots(2, 2, figsize=(7.2, 6.2), constrained_layout=True)
        points = result.points
        strain = [point.strain_fraction for point in points]
        axes[0, 0].plot(
            strain,
            [point.minimum_bond_length for point in points],
            "o-",
            label="minimum",
        )
        axes[0, 0].plot(
            strain,
            [point.maximum_bond_length for point in points],
            "s--",
            label="maximum",
        )
        axes[0, 0].set_ylabel("bond length at unit primitive volume")
        axes[0, 0].set_title("(a) strained FCC bond orbit")
        axes[0, 0].legend(frameon=False)
        axes[0, 1].plot(
            strain, [point.restricted_alignment_residual for point in points], "o-"
        )
        axes[0, 1].set_ylabel("normalized restricted residual")
        axes[0, 1].set_title("(b) gauge-cost invariant")
        for tolerance_index, tolerance in enumerate(result.tail_tolerances):
            axes[1, 0].plot(
                strain,
                [point.first_passing_radius[tolerance_index] for point in points],
                "o-",
                label=rf"tail $\leq {tolerance:.0e}$",
            )
            axes[1, 1].plot(
                strain,
                [point.first_passing_blocks[tolerance_index] for point in points],
                "o-",
                label=rf"tail $\leq {tolerance:.0e}$",
            )
        axes[1, 0].set_ylabel("first-passing physical radius")
        axes[1, 0].set_title("(c) fidelity cost in range")
        axes[1, 1].set_ylabel("retained hopping blocks")
        axes[1, 1].set_title("(d) fidelity cost in block count")
        for axis in axes.flat:
            axis.set_xlabel("strain fraction (FCC → BCC Bain endpoint)")
            axis.grid(alpha=0.22)
        axes[1, 0].legend(frameon=False)
        figure.suptitle("3-D frozen-gauge synthetic Bain control", fontsize=11)
        stem = output / "gauge-locality-under-synthetic-strain"
        figure.savefig(stem.with_suffix(".pdf"), bbox_inches="tight")
        figure.savefig(stem.with_suffix(".png"), dpi=600, bbox_inches="tight")
        plt.close(figure)
    print(f"output={typed_result_path}")
    print(f"output={stem.with_suffix('.pdf')}")
    print(f"output={stem.with_suffix('.png')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
