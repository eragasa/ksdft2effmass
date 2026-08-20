#!/usr/bin/env python3
"""Verify the retained higher-index particle-in-a-box eigenpair sweep."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import numpy as np


def verify(payload: dict[str, Any]) -> None:
    """Raise ``AssertionError`` unless the eigenpair sweep meets its protocol."""
    assert payload["schema_version"] == 1
    assert payload["evidence_status"] == "illustrative numerical experiment"
    assert payload["calculation_status"] == "calculated illustrative result"

    grids = payload["grids"]
    point_counts = payload["input"]["grid_series"]["interior_points"]
    fixed_modes = payload["input"]["grid_series"]["fixed_higher_modes"]
    assert [grid["interior_points"] for grid in grids] == point_counts
    fixed_errors: dict[int, list[float]] = {mode: [] for mode in fixed_modes}
    fixed_spacings: dict[int, list[float]] = {mode: [] for mode in fixed_modes}
    fixed_point_counts: dict[int, list[int]] = {mode: [] for mode in fixed_modes}

    for grid in grids:
        points = grid["interior_points"]
        spacing = float(grid["spacing"])
        assert spacing == 1.0 / (points + 1)
        assert len(grid["eigenpairs"]) == points
        for record, mode in zip(grid["eigenpairs"], range(1, points + 1), strict=True):
            assert record["mode"] == mode
            assert record["fractional_mode_index"] == mode / (points + 1)
            z = mode * np.pi / (2.0 * (points + 1))
            expected_error = 1.0 - (np.sin(z) / z) ** 2
            oracle_tolerance = (
                128.0
                * np.finfo(np.float64).eps
                / (spacing * spacing * record["continuum_energy"])
            )
            assert (
                abs(record["relative_energy_error"] - expected_error) < oracle_tolerance
            )
            assert record["nodal_overlap_defect"] < 1.0e-13
            assert record["scaled_eigenpair_residual"] < 1.0e-13
            if mode in fixed_errors:
                fixed_errors[mode].append(record["relative_energy_error"])
                fixed_spacings[mode].append(spacing)
                fixed_point_counts[mode].append(points)

        assert grid["maximum_nodal_overlap_defect"] < 1.0e-13
        assert grid["maximum_scaled_eigenpair_residual"] < 1.0e-13
        assert grid["eigenpairs"][0]["relative_energy_error"] < 0.02
        assert grid["eigenpairs"][-1]["relative_energy_error"] > 0.5

    for mode in fixed_modes:
        series = payload["fixed_higher_mode_series"][str(mode)]
        np.testing.assert_array_equal(
            series["interior_points"], fixed_point_counts[mode]
        )
        np.testing.assert_array_equal(series["spacings"], fixed_spacings[mode])
        np.testing.assert_array_equal(
            series["relative_energy_errors"], fixed_errors[mode]
        )
        assert all(
            finer < coarser
            for coarser, finer in zip(
                fixed_errors[mode][:-1], fixed_errors[mode][1:], strict=True
            )
        )
        recorded_orders = series["observed_orders"]
        assert recorded_orders[0] is None
        independent_orders = []
        for previous_h, current_h, previous_error, current_error in zip(
            fixed_spacings[mode][:-1],
            fixed_spacings[mode][1:],
            fixed_errors[mode][:-1],
            fixed_errors[mode][1:],
            strict=True,
        ):
            independent_orders.append(
                np.log(previous_error / current_error) / np.log(previous_h / current_h)
            )
        np.testing.assert_allclose(
            recorded_orders[1:], independent_orders, rtol=2.0e-10, atol=2.0e-10
        )
        assert 1.95 < recorded_orders[-1] < 2.01

    assert payload["limitations"] == [
        "Fixed-mode convergence does not imply uniform spectral convergence.",
        "Nodal overlap does not measure continuum interpolation error.",
        "High-index eigenvalues probe finite-difference dispersion.",
        "The result is not semiconductor evidence or scientific validation.",
    ]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("result", type=Path)
    args = parser.parse_args()
    verify(json.loads(args.result.read_text(encoding="utf-8")))
    print("particle-in-box higher eigenpair sweep: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
