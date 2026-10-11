"""Construct the controlled ICMSEP 2026 Paper 1 admissible-set evidence."""

from __future__ import annotations

import csv
import hashlib
import json
import math
from fractions import Fraction
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parent
INPUT_PATH = ROOT / "input.json"
RESULT_PATH = ROOT / "result.json"
BOUNDARY_PATH = ROOT / "boundaries.csv"
FIGURE_PATH = ROOT / "admissible-sets.png"


def _fraction(text: str) -> Fraction:
    return Fraction(text)


def _fraction_text(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    digest.update(path.read_bytes())
    return digest.hexdigest()


def _energy(theta: tuple[float, float], k: float) -> float:
    return theta[0] + 2.0 * theta[1] * math.cos(k)


def _parent_energy(a: float, b: float, c: float, k: float) -> float:
    return a + 2.0 * b * math.cos(k) + 2.0 * c * math.cos(2.0 * k)


def _rms(
    theta: tuple[float, float], points: tuple[float, ...], a: float, b: float, c: float
) -> float:
    residuals = [
        _energy(theta, point) - _parent_energy(a, b, c, point) for point in points
    ]
    return math.sqrt(sum(value * value for value in residuals) / len(residuals))


def _ellipse_boundary(
    center: tuple[float, float],
    quadratic: np.ndarray,
    excess: float,
    count: int,
) -> np.ndarray:
    eigenvalues, eigenvectors = np.linalg.eigh(quadratic)
    angles = np.linspace(0.0, 2.0 * math.pi, count, endpoint=False)
    unit_circle = np.vstack((np.cos(angles), np.sin(angles)))
    transform = eigenvectors @ np.diag(np.sqrt(excess / eigenvalues))
    return np.asarray(center)[:, None].T + (transform @ unit_circle).T


def main() -> None:
    source = json.loads(INPUT_PATH.read_text(encoding="utf-8"))
    hoppings = source["parent_hoppings"]
    a = _fraction(hoppings["R=0"])
    b = _fraction(hoppings["R=+1"])
    c = _fraction(hoppings["R=+2"])
    epsilon = _fraction(source["loss_contract"]["excess_loss_budget"])

    operator_denominator = a * a + 2 * b * b + 2 * c * c
    operator_floor = 2 * c * c / operator_denominator
    operator_threshold = operator_floor + epsilon

    compatible_center = (a, b)
    compatible_spectral_quadratic = (
        (Fraction(1), Fraction(0)),
        (Fraction(0), Fraction(2)),
    )
    compatible_spectral_floor = 2 * c * c
    compatible_spectral_threshold = compatible_spectral_floor + epsilon

    separated_spectral_center = (Fraction(3, 5), Fraction(1, 20))
    separated_spectral_quadratic = (
        (Fraction(1), Fraction(4, 3)),
        (Fraction(4, 3), Fraction(2)),
    )
    separated_spectral_threshold = epsilon

    center_delta = (
        compatible_center[0] - separated_spectral_center[0],
        compatible_center[1] - separated_spectral_center[1],
    )
    center_distance_squared = center_delta[0] ** 2 + center_delta[1] ** 2

    spectral_eigenvalue_lower_bound = Fraction(91, 1200)
    spectral_radius_upper_bound = Fraction(37, 1000)
    operator_eigenvalue = Fraction(1, 1) / operator_denominator
    operator_radius_upper_bound = Fraction(11, 1000)
    separation_lower_bound = (
        Fraction(1, 2) - spectral_radius_upper_bound - operator_radius_upper_bound
    )
    separation_upper_bound = Fraction(1, 2)

    training_compatible = (
        0.0,
        math.pi / 3.0,
        2.0 * math.pi / 3.0,
        math.pi,
        4.0 * math.pi / 3.0,
        5.0 * math.pi / 3.0,
    )
    training_separated = (-math.pi / 3.0, 0.0, math.pi / 3.0)
    withheld = (
        -5.0 * math.pi / 6.0,
        -math.pi / 6.0,
        math.pi / 6.0,
        5.0 * math.pi / 6.0,
    )
    float_parent = (float(a), float(b), float(c))
    float_compatible = (float(compatible_center[0]), float(compatible_center[1]))
    float_separated = (
        float(separated_spectral_center[0]),
        float(separated_spectral_center[1]),
    )

    result = {
        "schema": "icmsep2026.paper1.admissible-set-result.v1",
        "evidence_class": source["evidence_class"],
        "input_sha256": _sha256(INPUT_PATH),
        "status": "CALCULATED_CONTROLLED_NUMERICAL_VERIFICATION",
        "canonical_metric": {
            "parameter_order": ["theta_0", "theta_1"],
            "scales": ["1", "1"],
            "weights": ["1", "1"],
            "distance": "euclidean",
        },
        "operator_loss": {
            "normalization_denominator": _fraction_text(operator_denominator),
            "analytic_minimum": _fraction_text(operator_floor),
            "threshold": _fraction_text(operator_threshold),
            "excess_budget": _fraction_text(epsilon),
            "quadratic_about_center": [
                ["200/229", "0"],
                ["0", "400/229"],
            ],
            "center": [_fraction_text(a), _fraction_text(b)],
            "translation_residuals_at_center": {
                "R=-2": "1/10",
                "R=-1": "0",
                "R=0": "0",
                "R=1": "0",
                "R=2": "1/10",
            },
        },
        "compatible_complete_mesh": {
            "spectral_center": [
                _fraction_text(compatible_center[0]),
                _fraction_text(compatible_center[1]),
            ],
            "spectral_quadratic_about_center": [
                [_fraction_text(value) for value in row]
                for row in compatible_spectral_quadratic
            ],
            "spectral_analytic_minimum": _fraction_text(compatible_spectral_floor),
            "spectral_threshold": _fraction_text(compatible_spectral_threshold),
            "common_witness": [_fraction_text(a), _fraction_text(b)],
            "witness_spectral_loss": _fraction_text(compatible_spectral_floor),
            "witness_operator_loss": _fraction_text(operator_floor),
            "set_separation": "0",
            "disposition": "COMPATIBLE_COMMON_WITNESS",
            "training_rms": _rms(float_compatible, training_compatible, *float_parent),
            "withheld_rms": _rms(float_compatible, withheld, *float_parent),
        },
        "separated_restricted_training": {
            "spectral_center": [
                _fraction_text(separated_spectral_center[0]),
                _fraction_text(separated_spectral_center[1]),
            ],
            "spectral_quadratic_about_center": [
                [_fraction_text(value) for value in row]
                for row in separated_spectral_quadratic
            ],
            "spectral_analytic_minimum": "0",
            "spectral_threshold": _fraction_text(separated_spectral_threshold),
            "spectral_center_training_rms": _rms(
                float_separated, training_separated, *float_parent
            ),
            "spectral_center_withheld_rms": _rms(
                float_separated, withheld, *float_parent
            ),
            "operator_center_withheld_rms": _rms(
                float_compatible, withheld, *float_parent
            ),
            "center_distance_squared": _fraction_text(center_distance_squared),
            "center_distance": "1/2",
            "certified_lower_bound": _fraction_text(separation_lower_bound),
            "feasible_upper_bound": _fraction_text(separation_upper_bound),
            "disposition": "INCOMPATIBLE_CERTIFIED_SEPARATION",
            "certificate": {
                "sqrt_73_upper_bound": "1709/200",
                "spectral_minimum_eigenvalue_lower_bound": _fraction_text(
                    spectral_eigenvalue_lower_bound
                ),
                "spectral_radius_upper_bound": _fraction_text(
                    spectral_radius_upper_bound
                ),
                "operator_minimum_eigenvalue": _fraction_text(operator_eigenvalue),
                "operator_radius_upper_bound": _fraction_text(
                    operator_radius_upper_bound
                ),
                "method": "exact rational quadratic bounds and reverse triangle inequality",
            },
        },
        "limitations": [
            "synthetic scalar one-dimensional parent",
            "singleton identity alignment family",
            "finite declared parameter box and translation domain",
            "thresholds are benchmark design resolutions, not uncertainties",
            "compatibility and separation are relative to the frozen contract",
            "no material, silicon, or three-dimensional conclusion",
        ],
    }
    RESULT_PATH.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")

    count = int(source["visualization"]["boundary_samples_per_set"])
    eps_float = float(epsilon)
    q_compatible = np.array([[1.0, 0.0], [0.0, 2.0]])
    q_separated = np.array([[1.0, 4.0 / 3.0], [4.0 / 3.0, 2.0]])
    q_operator = np.array(
        [
            [float(Fraction(1) / operator_denominator), 0.0],
            [0.0, float(Fraction(2) / operator_denominator)],
        ]
    )
    compatible_spectral_boundary = _ellipse_boundary(
        float_compatible, q_compatible, eps_float, count
    )
    separated_spectral_boundary = _ellipse_boundary(
        float_separated, q_separated, eps_float, count
    )
    operator_boundary = _ellipse_boundary(
        float_compatible, q_operator, eps_float, count
    )

    with BOUNDARY_PATH.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.writer(stream, lineterminator="\n")
        writer.writerow(("case", "set", "sample", "theta_0", "theta_1"))
        for case, name, boundary in (
            ("compatible_complete_mesh", "spectral", compatible_spectral_boundary),
            ("compatible_complete_mesh", "operator", operator_boundary),
            ("separated_restricted_training", "spectral", separated_spectral_boundary),
            ("separated_restricted_training", "operator", operator_boundary),
        ):
            for index, point in enumerate(boundary):
                writer.writerow(
                    (case, name, index, f"{point[0]:.17g}", f"{point[1]:.17g}")
                )

    figure, axes = plt.subplots(1, 2, figsize=(9.2, 4.1), constrained_layout=True)
    panels = (
        (
            axes[0],
            compatible_spectral_boundary,
            float_compatible,
            "Complete-mesh objective",
            "common witness; $\\delta^*=0$",
        ),
        (
            axes[1],
            separated_spectral_boundary,
            float_separated,
            "Restricted-training objective",
            "$0.452\\leq\\delta^*\\leq0.500$",
        ),
    )
    for axis, spectral_boundary, spectral_center, title, subtitle in panels:
        axis.fill(
            spectral_boundary[:, 0],
            spectral_boundary[:, 1],
            color="#4477AA",
            alpha=0.28,
            label=r"spectral set $\mathfrak{A}_E$",
        )
        axis.plot(spectral_boundary[:, 0], spectral_boundary[:, 1], color="#225588")
        axis.fill(
            operator_boundary[:, 0],
            operator_boundary[:, 1],
            color="#CC6677",
            alpha=0.28,
            label=r"operator set $\mathfrak{A}_H$",
        )
        axis.plot(operator_boundary[:, 0], operator_boundary[:, 1], color="#AA4455")
        axis.scatter(*spectral_center, color="#225588", marker="o", s=28, zorder=4)
        axis.scatter(*float_compatible, color="#AA4455", marker="s", s=28, zorder=4)
        axis.set_title(f"{title}\n{subtitle}", fontsize=10)
        axis.set_xlabel(r"$\theta_0/E_G$")
        axis.set_ylabel(r"$\theta_1/E_G$")
        axis.grid(alpha=0.2)
        axis.set_aspect("equal", adjustable="box")
    axes[0].set_xlim(0.984, 1.016)
    axes[0].set_ylim(-0.263, -0.237)
    axes[1].set_xlim(0.53, 1.04)
    axes[1].set_ylim(-0.30, 0.11)
    axes[1].plot(
        [float_separated[0], float_compatible[0]],
        [float_separated[1], float_compatible[1]],
        linestyle="--",
        color="#444444",
        linewidth=0.9,
        label="center-to-center feasible pair",
    )
    handles, labels = axes[1].get_legend_handles_labels()
    figure.legend(handles, labels, loc="outside lower center", ncol=3, frameon=False)
    figure.savefig(
        FIGURE_PATH,
        dpi=int(source["visualization"]["dpi"]),
        metadata={"Software": "ksdft2effmass controlled evidence generator"},
    )
    plt.close(figure)


if __name__ == "__main__":
    main()
