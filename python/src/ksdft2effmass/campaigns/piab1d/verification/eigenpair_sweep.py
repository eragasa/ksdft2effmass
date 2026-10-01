"""Independent verification of the PIAB1D higher-eigenpair sweep."""

from __future__ import annotations

from pathlib import Path

import numpy as np

from .decoder import ParticleInBoxCampaignResultDecoder


class ParticleInBoxEigenpairSweepVerifier(ParticleInBoxCampaignResultDecoder):
    """Independently verify the retained higher-eigenpair campaign."""

    def execute(self, path: Path) -> None:
        """Raise unless one result satisfies the declared eigenpair identities."""
        payload = self.decode(path)
        assert self.integer(payload["schema_version"], "schema_version") == 1
        input_payload = self.mapping(payload["input"], "input")
        series = self.mapping(input_payload["grid_series"], "grid_series")
        point_counts = self.integer_sequence(
            series["interior_points"], "interior_points"
        )
        fixed_modes = self.integer_sequence(
            series["fixed_higher_modes"], "fixed_higher_modes"
        )
        fixed_errors: dict[int, list[float]] = {mode: [] for mode in fixed_modes}
        fixed_spacings: dict[int, list[float]] = {mode: [] for mode in fixed_modes}
        fixed_points: dict[int, list[int]] = {mode: [] for mode in fixed_modes}
        grids = self.sequence(payload["grids"], "grids")
        for value, expected_points in zip(grids, point_counts, strict=True):
            grid = self.mapping(value, "grid")
            points = self.integer(grid["interior_points"], "interior_points")
            assert points == expected_points
            spacing = self.real(grid["spacing"], "spacing")
            assert spacing == 1.0 / (points + 1)
            records = self.sequence(grid["eigenpairs"], "eigenpairs")
            assert len(records) == points
            for item, mode in zip(records, range(1, points + 1), strict=True):
                record = self.mapping(item, "eigenpair")
                assert self.integer(record["mode"], "mode") == mode
                assert self.real(
                    record["fractional_mode_index"], "fractional_mode_index"
                ) == mode / (points + 1)
                continuum = self.real(record["continuum_energy"], "continuum_energy")
                observed = self.real(
                    record["relative_energy_error"], "relative_energy_error"
                )
                z = mode * np.pi / (2.0 * (points + 1))
                expected = 1.0 - (np.sin(z) / z) ** 2
                allowance = (
                    128.0 * np.finfo(np.float64).eps / (spacing * spacing * continuum)
                )
                assert abs(observed - expected) < allowance
                assert (
                    self.real(record["nodal_overlap_defect"], "overlap defect")
                    < 1.0e-13
                )
                assert (
                    self.real(record["scaled_eigenpair_residual"], "scaled residual")
                    < 1.0e-13
                )
                if mode in fixed_errors:
                    fixed_errors[mode].append(observed)
                    fixed_spacings[mode].append(spacing)
                    fixed_points[mode].append(points)
            assert (
                self.real(
                    grid["maximum_nodal_overlap_defect"], "maximum overlap defect"
                )
                < 1.0e-13
            )
            assert (
                self.real(grid["maximum_scaled_eigenpair_residual"], "maximum residual")
                < 1.0e-13
            )
            first = self.mapping(records[0], "first eigenpair")
            last = self.mapping(records[-1], "last eigenpair")
            assert self.real(first["relative_energy_error"], "first error") < 0.02
            assert self.real(last["relative_energy_error"], "last error") > 0.5
        all_series = self.mapping(
            payload["fixed_higher_mode_series"], "fixed_higher_mode_series"
        )
        for mode in fixed_modes:
            mode_series = self.mapping(all_series[str(mode)], "mode series")
            assert self.integer_sequence(
                mode_series["interior_points"], "interior_points"
            ) == tuple(fixed_points[mode])
            np.testing.assert_array_equal(
                self.real_sequence(mode_series["spacings"], "spacings"),
                fixed_spacings[mode],
            )
            np.testing.assert_array_equal(
                self.real_sequence(
                    mode_series["relative_energy_errors"], "relative errors"
                ),
                fixed_errors[mode],
            )
            recorded = self.sequence(mode_series["observed_orders"], "orders")
            assert recorded[0] is None
            independent = tuple(
                np.log(a / b) / np.log(h_a / h_b)
                for h_a, h_b, a, b in zip(
                    fixed_spacings[mode][:-1],
                    fixed_spacings[mode][1:],
                    fixed_errors[mode][:-1],
                    fixed_errors[mode][1:],
                    strict=True,
                )
            )
            np.testing.assert_allclose(
                self.real_sequence(recorded[1:], "orders"),
                independent,
                rtol=2.0e-10,
                atol=2.0e-10,
            )
            assert 1.95 < self.real(recorded[-1], "last order") < 2.01
        assert payload["limitations"] == [
            "Fixed-mode convergence does not imply uniform spectral convergence.",
            "Nodal overlap does not measure continuum interpolation error.",
            "High-index eigenvalues probe finite-difference dispersion.",
            "The result is not semiconductor evidence or scientific validation.",
        ]
