"""Independently verify the retained direct admissible-set result."""

from __future__ import annotations

import csv
import hashlib
import json
import math
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parent
INPUT_PATH = ROOT / "input.json"
RESULT_PATH = ROOT / "result.json"
BOUNDARY_PATH = ROOT / "boundaries.csv"
FIGURE_PATH = ROOT / "admissible-sets.png"


def _fraction(value: str) -> Fraction:
    return Fraction(value)


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    digest.update(path.read_bytes())
    return digest.hexdigest()


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def _matrix_fraction(rows: list[list[str]]) -> tuple[tuple[Fraction, ...], ...]:
    return tuple(tuple(_fraction(value) for value in row) for row in rows)


def _quadratic(
    delta: tuple[Fraction, Fraction],
    matrix: tuple[tuple[Fraction, Fraction], tuple[Fraction, Fraction]],
) -> Fraction:
    return (
        matrix[0][0] * delta[0] * delta[0]
        + (matrix[0][1] + matrix[1][0]) * delta[0] * delta[1]
        + matrix[1][1] * delta[1] * delta[1]
    )


def _exact_least_squares(
    rows: tuple[tuple[Fraction, Fraction], ...],
    omitted_values: tuple[Fraction, ...],
) -> tuple[
    tuple[tuple[Fraction, Fraction], tuple[Fraction, Fraction]],
    tuple[Fraction, Fraction],
    Fraction,
]:
    count = Fraction(len(rows))
    q00 = sum(row[0] * row[0] for row in rows) / count
    q01 = sum(row[0] * row[1] for row in rows) / count
    q11 = sum(row[1] * row[1] for row in rows) / count
    g0 = (
        sum(row[0] * value for row, value in zip(rows, omitted_values, strict=True))
        / count
    )
    g1 = (
        sum(row[1] * value for row, value in zip(rows, omitted_values, strict=True))
        / count
    )
    determinant = q00 * q11 - q01 * q01
    shift = (
        (q11 * g0 - q01 * g1) / determinant,
        (-q01 * g0 + q00 * g1) / determinant,
    )
    mean_square = sum(value * value for value in omitted_values) / count
    minimum = mean_square - g0 * shift[0] - g1 * shift[1]
    return ((q00, q01), (q01, q11)), shift, minimum


def main() -> None:
    source = json.loads(INPUT_PATH.read_text(encoding="utf-8"))
    result = json.loads(RESULT_PATH.read_text(encoding="utf-8"))

    _require(
        result["schema"] == "icmsep2026.paper1.admissible-set-result.v1",
        "unexpected result schema",
    )
    _require(result["input_sha256"] == _sha256(INPUT_PATH), "input identity mismatch")
    _require(
        result["evidence_class"] == "controlled illustrative numerical verification",
        "evidence class changed",
    )

    hoppings = source["parent_hoppings"]
    a = _fraction(hoppings["R=0"])
    b = _fraction(hoppings["R=+1"])
    c = _fraction(hoppings["R=+2"])
    epsilon = _fraction(source["loss_contract"]["excess_loss_budget"])
    _require(
        (a, b, c) == (Fraction(1), Fraction(-1, 4), Fraction(1, 10)), "parent changed"
    )
    _require(epsilon == Fraction(1, 10000), "excess budget changed")

    denominator = a * a + 2 * b * b + 2 * c * c
    operator_floor = 2 * c * c / denominator
    operator_threshold = operator_floor + epsilon
    retained_operator = result["operator_loss"]
    _require(
        denominator == Fraction(229, 200), "operator denominator derivation failed"
    )
    _require(
        _fraction(retained_operator["normalization_denominator"]) == denominator,
        "operator denominator mismatch",
    )
    _require(
        _fraction(retained_operator["analytic_minimum"]) == operator_floor,
        "operator floor mismatch",
    )
    _require(
        _fraction(retained_operator["threshold"]) == operator_threshold,
        "operator threshold mismatch",
    )
    _require(
        _matrix_fraction(retained_operator["quadratic_about_center"])
        == ((Fraction(200, 229), Fraction(0)), (Fraction(0), Fraction(400, 229))),
        "operator quadratic mismatch",
    )

    compatible = result["compatible_complete_mesh"]
    compatible_center = tuple(
        _fraction(value) for value in compatible["spectral_center"]
    )
    compatible_q = _matrix_fraction(compatible["spectral_quadratic_about_center"])
    derived_compatible_q, compatible_shift, compatible_floor = _exact_least_squares(
        (
            (Fraction(1), Fraction(2)),
            (Fraction(1), Fraction(1)),
            (Fraction(1), Fraction(-1)),
            (Fraction(1), Fraction(-2)),
            (Fraction(1), Fraction(-1)),
            (Fraction(1), Fraction(1)),
        ),
        (
            Fraction(1, 5),
            Fraction(-1, 10),
            Fraction(-1, 10),
            Fraction(1, 5),
            Fraction(-1, 10),
            Fraction(-1, 10),
        ),
    )
    _require(compatible_shift == (0, 0), "compatible least-squares center shifted")
    _require(compatible_center == (a, b), "compatible spectral center mismatch")
    _require(
        compatible_q == derived_compatible_q, "compatible spectral quadratic mismatch"
    )
    _require(
        _fraction(compatible["spectral_analytic_minimum"]) == compatible_floor,
        "compatible floor mismatch",
    )
    _require(
        _fraction(compatible["spectral_threshold"]) == compatible_floor + epsilon,
        "compatible threshold mismatch",
    )
    witness = tuple(_fraction(value) for value in compatible["common_witness"])
    _require(witness == (a, b), "common witness mismatch")
    _require(
        _fraction(compatible["witness_spectral_loss"])
        <= _fraction(compatible["spectral_threshold"]),
        "witness is not spectrally feasible",
    )
    _require(
        _fraction(compatible["witness_operator_loss"]) <= operator_threshold,
        "witness is not operator feasible",
    )
    _require(compatible["set_separation"] == "0", "compatible separation must be zero")
    _require(
        compatible["disposition"] == "COMPATIBLE_COMMON_WITNESS",
        "compatible disposition mismatch",
    )

    separated = result["separated_restricted_training"]
    spectral_center = tuple(_fraction(value) for value in separated["spectral_center"])
    spectral_q = _matrix_fraction(separated["spectral_quadratic_about_center"])
    derived_separated_q, separated_shift, separated_floor = _exact_least_squares(
        (
            (Fraction(1), Fraction(1)),
            (Fraction(1), Fraction(2)),
            (Fraction(1), Fraction(1)),
        ),
        (Fraction(-1, 10), Fraction(1, 5), Fraction(-1, 10)),
    )
    derived_separated_center = (a + separated_shift[0], b + separated_shift[1])
    _require(
        spectral_center == derived_separated_center,
        "restricted spectral center mismatch",
    )
    _require(
        spectral_q == derived_separated_q, "restricted spectral quadratic mismatch"
    )
    _require(separated_floor == 0, "restricted exact fit derivation failed")
    _require(
        _fraction(separated["spectral_analytic_minimum"]) == separated_floor,
        "restricted spectral floor mismatch",
    )
    _require(
        _fraction(separated["spectral_threshold"]) == epsilon,
        "restricted threshold mismatch",
    )

    center_delta = (spectral_center[0] - a, spectral_center[1] - b)
    center_distance_squared = center_delta[0] ** 2 + center_delta[1] ** 2
    _require(
        center_distance_squared == Fraction(1, 4), "center distance derivation failed"
    )
    _require(
        _fraction(separated["center_distance_squared"]) == center_distance_squared,
        "center distance squared mismatch",
    )
    _require(
        _fraction(separated["center_distance"]) == Fraction(1, 2),
        "center distance mismatch",
    )

    certificate = separated["certificate"]
    sqrt_upper = _fraction(certificate["sqrt_73_upper_bound"])
    lambda_e_lower = _fraction(certificate["spectral_minimum_eigenvalue_lower_bound"])
    radius_e_upper = _fraction(certificate["spectral_radius_upper_bound"])
    lambda_h = _fraction(certificate["operator_minimum_eigenvalue"])
    radius_h_upper = _fraction(certificate["operator_radius_upper_bound"])

    _require(sqrt_upper * sqrt_upper > 73, "sqrt(73) upper bound is invalid")
    _require(
        lambda_e_lower == Fraction(91, 1200), "spectral eigenvalue lower bound changed"
    )
    _require(
        (Fraction(9) - sqrt_upper) / 6 == lambda_e_lower,
        "spectral eigenvalue bound derivation failed",
    )
    _require(radius_e_upper == Fraction(37, 1000), "spectral radius bound changed")
    _require(
        epsilon / lambda_e_lower < radius_e_upper * radius_e_upper,
        "spectral radius certificate failed",
    )
    _require(
        lambda_h == Fraction(1, 1) / denominator, "operator minimum eigenvalue mismatch"
    )
    _require(radius_h_upper == Fraction(11, 1000), "operator radius bound changed")
    _require(
        epsilon / lambda_h < radius_h_upper * radius_h_upper,
        "operator radius certificate failed",
    )

    lower_bound = Fraction(1, 2) - radius_e_upper - radius_h_upper
    upper_bound = Fraction(1, 2)
    _require(
        lower_bound == Fraction(113, 250), "separation lower-bound derivation failed"
    )
    _require(
        _fraction(separated["certified_lower_bound"]) == lower_bound,
        "retained lower bound mismatch",
    )
    _require(
        _fraction(separated["feasible_upper_bound"]) == upper_bound,
        "retained upper bound mismatch",
    )
    _require(lower_bound > 0, "separation is not positive")
    _require(
        separated["disposition"] == "INCOMPATIBLE_CERTIFIED_SEPARATION",
        "separated disposition mismatch",
    )

    spectral_center_loss = _quadratic((Fraction(0), Fraction(0)), spectral_q)
    operator_center_loss = operator_floor
    _require(spectral_center_loss <= epsilon, "spectral center is not feasible")
    _require(
        operator_center_loss <= operator_threshold, "operator center is not feasible"
    )

    _require(
        BOUNDARY_PATH.is_file() and BOUNDARY_PATH.stat().st_size > 0,
        "boundary samples missing",
    )
    _require(FIGURE_PATH.is_file() and FIGURE_PATH.stat().st_size > 0, "figure missing")
    expected_samples = int(source["visualization"]["boundary_samples_per_set"])
    with BOUNDARY_PATH.open(encoding="utf-8", newline="") as stream:
        rows = list(csv.DictReader(stream))
    _require(len(rows) == 4 * expected_samples, "boundary sample count mismatch")
    _require(
        math.isfinite(float(separated["spectral_center_withheld_rms"])),
        "withheld RMS is not finite",
    )
    _require(
        float(separated["spectral_center_withheld_rms"])
        > float(separated["spectral_center_training_rms"]),
        "restricted-training control did not worsen on withheld points",
    )

    print("verified: exact common witness and certified separated admissible sets")
    print("compatible separation: 0")
    print(f"separated bounds: [{float(lower_bound):.3f}, {float(upper_bound):.3f}]")


if __name__ == "__main__":
    main()
