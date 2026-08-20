#!/usr/bin/env python3
"""Verify the retained particle-in-a-box grid-convergence series."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import numpy as np


def verify(payload: dict[str, Any]) -> None:
    """Raise ``AssertionError`` unless the convergence series meets its protocol."""
    assert payload["schema_version"] == 1
    assert payload["evidence_status"] == "illustrative numerical experiment"
    assert payload["calculation_status"] == "calculated illustrative result"

    refinements = payload["refinements"]
    point_counts = payload["input"]["grid_series"]["interior_points"]
    reported_modes = payload["input"]["grid_series"]["reported_modes"]
    order_modes = payload["input"]["grid_series"]["order_modes"]
    assert [item["interior_points"] for item in refinements] == point_counts

    errors_by_mode: dict[int, list[float]] = {mode: [] for mode in reported_modes}
    spacings: list[float] = []
    for item in refinements:
        points = item["interior_points"]
        spacing = float(item["spacing"])
        spacings.append(spacing)
        assert spacing == 1.0 / (points + 1)
        for record, mode in zip(item["modes"], reported_modes, strict=True):
            assert record["mode"] == mode
            z = mode * np.pi / (2.0 * (points + 1))
            expected_relative_error = 1.0 - (np.sin(z) / z) ** 2
            relative_oracle_tolerance = (
                2.0
                * record["discrete_closed_form_error"]
                / record["continuum_energy"]
                + 32.0 * np.finfo(np.float64).eps
            )
            assert (
                abs(record["relative_error"] - expected_relative_error)
                < relative_oracle_tolerance
            )
            assert record["discrete_closed_form_error"] < (
                128.0 * np.finfo(np.float64).eps / (spacing * spacing)
            )
            errors_by_mode[mode].append(record["relative_error"])

        diagnostics = item["diagnostic_residuals"]
        assert diagnostics["consistent_compression_frobenius_norm"] == 0.0
        assert diagnostics["unmatched_equals_discarded_relative_error"] < 1.0e-13

    for mode in reported_modes:
        errors = errors_by_mode[mode]
        assert all(
            finer < coarser
            for coarser, finer in zip(errors[:-1], errors[1:], strict=True)
        )

    for mode in order_modes:
        recorded = payload["observed_relative_error_orders"][str(mode)]
        assert recorded[0] is None
        independently_computed: list[float] = []
        for previous_h, current_h, previous_error, current_error in zip(
            spacings[:-1],
            spacings[1:],
            errors_by_mode[mode][:-1],
            errors_by_mode[mode][1:],
            strict=True,
        ):
            independently_computed.append(
                float(
                    np.log(previous_error / current_error)
                    / np.log(previous_h / current_h)
                )
            )
        np.testing.assert_allclose(
            recorded[1:],
            independently_computed,
            rtol=2.0e-10,
            atol=2.0e-10,
        )
        assert 1.99 < recorded[-1] < 2.01

    assert payload["limitations"] == [
        "Observed order concerns fixed-index eigenvalues only.",
        "The series does not establish uniform spectral convergence.",
        "Residual norms on different matrix spaces are not convergence metrics.",
        "The result is not semiconductor evidence or scientific validation.",
    ]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("result", type=Path)
    args = parser.parse_args()
    verify(json.loads(args.result.read_text(encoding="utf-8")))
    print("particle-in-box convergence series: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
