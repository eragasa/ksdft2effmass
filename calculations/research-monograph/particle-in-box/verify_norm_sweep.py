#!/usr/bin/env python3
"""Verify retained particle-in-a-box multi-norm diagnostics."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import numpy as np


def verify(payload: dict[str, Any]) -> None:
    """Raise ``AssertionError`` unless the norm sweep satisfies its protocol."""
    assert payload["schema_version"] == 1
    assert payload["evidence_status"] == "illustrative numerical experiment"
    assert payload["calculation_status"] == "calculated illustrative result"
    point_counts = payload["input"]["grid_series"]["interior_points"]
    retained = payload["input"]["grid_series"]["retained_dimension"]
    grids = payload["grids"]
    assert [grid["interior_points"] for grid in grids] == point_counts

    boundary_frobenius_ratios = []
    unmatched_frobenius_ratios = []
    for grid in grids:
        points = grid["interior_points"]
        spacing = float(grid["spacing"])
        assert spacing == 1.0 / (points + 1)
        prefactor = 1.0 / (2.0 * spacing * spacing)
        mode_indices = np.arange(1, points + 1, dtype=np.float64)
        eigenvalues = (
            4.0 * prefactor * np.sin(mode_indices * np.pi / (2.0 * (points + 1))) ** 2
        )
        expected_hamiltonian = {
            "frobenius": prefactor * np.sqrt(6.0 * points - 2.0),
            "spectral": float(eigenvalues[-1]),
            "maximum_entry": 2.0 * prefactor,
        }
        for norm_name, expected in expected_hamiltonian.items():
            np.testing.assert_allclose(
                grid["hamiltonian_norms"][norm_name],
                expected,
                rtol=2.0e-13,
                atol=2.0e-12,
            )

        consistent = grid["operator_residuals"]["consistent_compression"]
        assert all(value == 0.0 for value in consistent["raw"].values())
        assert all(
            value == 0.0 for value in consistent["relative_to_hamiltonian"].values()
        )

        boundary = grid["operator_residuals"]["boundary_realization"]
        expected_boundary = {
            "frobenius": np.sqrt(2.0) * prefactor,
            "spectral": prefactor,
            "maximum_entry": prefactor,
        }
        for norm_name, expected in expected_boundary.items():
            np.testing.assert_allclose(
                boundary["raw"][norm_name], expected, rtol=2.0e-13, atol=2.0e-12
            )
            np.testing.assert_allclose(
                boundary["relative_to_hamiltonian"][norm_name],
                expected / expected_hamiltonian[norm_name],
                rtol=2.0e-13,
                atol=2.0e-13,
            )

        unmatched = grid["operator_residuals"]["unmatched_compression"]
        expected_unmatched_frobenius = float(
            np.sqrt(np.sum(np.square(eigenvalues[retained:])))
        )
        np.testing.assert_allclose(
            unmatched["raw"]["frobenius"],
            expected_unmatched_frobenius,
            rtol=2.0e-13,
            atol=2.0e-11,
        )
        np.testing.assert_allclose(
            unmatched["raw"]["spectral"],
            eigenvalues[-1],
            rtol=2.0e-13,
            atol=2.0e-11,
        )
        boundary_frobenius_ratios.append(
            boundary["relative_to_hamiltonian"]["frobenius"]
        )
        unmatched_frobenius_ratios.append(
            unmatched["relative_to_hamiltonian"]["frobenius"]
        )

        algebraic = grid["full_eigenpair_algebraic_residual"]
        assert all(
            value < 1.0e-13 for value in algebraic["relative_to_hamiltonian"].values()
        )

    assert all(
        finer < coarser
        for coarser, finer in zip(
            boundary_frobenius_ratios[:-1],
            boundary_frobenius_ratios[1:],
            strict=True,
        )
    )
    assert all(
        finer > coarser
        for coarser, finer in zip(
            unmatched_frobenius_ratios[:-1],
            unmatched_frobenius_ratios[1:],
            strict=True,
        )
    )

    assert payload["limitations"] == [
        "Raw matrix norms are dimension- and discretization-scale-dependent.",
        "Normalized norms compare each residual only with its same-grid Hamiltonian.",
        "Maximum-entry norms are basis-dependent.",
        "Algebraic eigenpair residuals do not measure continuum error.",
        "The result is not semiconductor evidence or scientific validation.",
    ]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("result", type=Path)
    args = parser.parse_args()
    verify(json.loads(args.result.read_text(encoding="utf-8")))
    print("particle-in-box norm sweep: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
