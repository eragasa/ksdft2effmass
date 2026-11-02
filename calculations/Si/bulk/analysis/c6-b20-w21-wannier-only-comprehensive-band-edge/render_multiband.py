from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parent
RESULT = ROOT / "multiband-result.json"
FIGURES = ROOT / "figures"
MODELS = ("full-source", "H-shell-05", "H-shell-10", "H-shell-16")
DISPLAY = ("Full source", "H-shell-05", "H-shell-10", "H-shell-16")
COLORS = ("#0072b2", "#cc79a7", "#d55e00")


def save(figure: plt.Figure, stem: str) -> None:
    pdf = FIGURES / f"{stem}.pdf"
    png = FIGURES / f"{stem}.png"
    if pdf.exists() or png.exists():
        raise FileExistsError(f"refusing to overwrite {stem}")
    figure.savefig(pdf, bbox_inches="tight")
    figure.savefig(png, bbox_inches="tight", dpi=220)
    plt.close(figure)


def main() -> None:
    result = json.loads(RESULT.read_text(encoding="utf-8"))
    models = result["models"]
    x = np.arange(len(MODELS))

    figure, axes = plt.subplots(1, 3, figsize=(11.5, 3.8), sharey=True)
    for axis, direction in zip(axes, ("100", "110", "111"), strict=True):
        for channel in range(3):
            masses = [
                models[model]["windows"]["0.01"]["directions"][direction][
                    "apparent_hole_masses_electron_for_negative_channels"
                ][channel]
                for model in MODELS
            ]
            axis.plot(
                x,
                masses,
                marker="o",
                linewidth=1.6,
                color=COLORS[channel],
                label=f"curvature channel {channel + 1}",
            )
        axis.set_yscale("log")
        axis.set_title(f"[{direction[0]}{direction[1]}{direction[2]}]")
        axis.set_xticks(x, DISPLAY, rotation=25, ha="right")
        axis.grid(alpha=0.25)
    axes[0].set_ylabel("Apparent non-SOC channel mass ($m_e$)")
    handles, labels = axes[0].get_legend_handles_labels()
    figure.legend(handles, labels, loc="upper center", ncol=3, frameon=False)
    figure.suptitle(
        "Degeneracy-aware three-band valence curvature channels", y=1.02
    )
    figure.tight_layout()
    save(figure, "multiband-valence-curvature-channels")

    source_directions = models["full-source"]["windows"]["0.01"]["directions"]
    maximum_mass_changes = []
    for model in MODELS:
        maximum = 0.0
        for direction in ("100", "110", "111"):
            candidate = models[model]["windows"]["0.01"]["directions"][direction][
                "apparent_hole_masses_electron_for_negative_channels"
            ]
            source = source_directions[direction][
                "apparent_hole_masses_electron_for_negative_channels"
            ]
            maximum = max(
                maximum,
                max(abs(left - right) / abs(right) for left, right in zip(candidate, source, strict=True)),
            )
        maximum_mass_changes.append(100.0 * maximum)
    splitting = [1000.0 * models[model]["gamma_cluster_splitting_ev"] for model in MODELS]
    coefficient_error = [
        100.0
        * models[model][
            "source_relative_aligned_quadratic_coefficient_frobenius_error"
        ]
        for model in MODELS
    ]
    bar_colors = ("#111111", "#d55e00", "#0072b2", "#009e73")
    figure, axes = plt.subplots(1, 3, figsize=(11.5, 3.8))
    axes[0].bar(x, splitting, color=bar_colors)
    axes[0].set_yscale("log")
    axes[0].set_ylabel("$\\Gamma$ cluster splitting (meV)")
    axes[1].bar(x, coefficient_error, color=bar_colors)
    axes[1].set_ylabel("Aligned quadratic-operator error (%)")
    axes[2].bar(x, maximum_mass_changes, color=bar_colors)
    axes[2].set_ylabel("Maximum channel-mass change (%)")
    for axis in axes:
        axis.set_xticks(x, DISPLAY, rotation=25, ha="right")
        axis.grid(axis="y", alpha=0.25)
    figure.suptitle("Non-SOC multiband valence fidelity separates three failure modes")
    figure.tight_layout()
    save(figure, "multiband-valence-fidelity-summary")


if __name__ == "__main__":
    main()
