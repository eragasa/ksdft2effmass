"""Independent verification of the PIAB1D grid-convergence campaign."""

from __future__ import annotations

from pathlib import Path

import numpy as np

from .decoder import ParticleInBoxCampaignResultDecoder


class ParticleInBoxConvergenceVerifier(ParticleInBoxCampaignResultDecoder):
    """Independently verify the retained grid-convergence campaign."""

    def execute(self, path: Path) -> None:
        """Raise unless one result satisfies the declared convergence identities."""
        payload = self.decode(path)
        assert self.integer(payload["schema_version"], "schema_version") == 1
        assert payload["evidence_status"] == "illustrative numerical experiment"
        assert payload["calculation_status"] == "calculated illustrative result"
        input_payload = self.mapping(payload["input"], "input")
        series = self.mapping(input_payload["grid_series"], "grid_series")
        point_counts = self.integer_sequence(
            series["interior_points"], "interior_points"
        )
        reported_modes = self.integer_sequence(
            series["reported_modes"], "reported_modes"
        )
        order_modes = self.integer_sequence(series["order_modes"], "order_modes")
        refinements = self.sequence(payload["refinements"], "refinements")
        assert (
            tuple(
                self.integer(
                    self.mapping(item, "refinement")["interior_points"], "points"
                )
                for item in refinements
            )
            == point_counts
        )
        errors_by_mode: dict[int, list[float]] = {mode: [] for mode in reported_modes}
        spacings: list[float] = []
        for item in refinements:
            refinement = self.mapping(item, "refinement")
            points = self.integer(refinement["interior_points"], "interior_points")
            spacing = self.real(refinement["spacing"], "spacing")
            spacings.append(spacing)
            assert spacing == 1.0 / (points + 1)
            modes = self.sequence(refinement["modes"], "modes")
            for value, mode in zip(modes, reported_modes, strict=True):
                record = self.mapping(value, "mode record")
                assert self.integer(record["mode"], "mode") == mode
                continuum = self.real(record["continuum_energy"], "continuum_energy")
                closed_error = self.real(
                    record["discrete_closed_form_error"], "closed-form error"
                )
                observed = self.real(record["relative_error"], "relative_error")
                z = mode * np.pi / (2.0 * (points + 1))
                expected = 1.0 - (np.sin(z) / z) ** 2
                allowance = (
                    2.0 * closed_error / continuum + 32.0 * np.finfo(np.float64).eps
                )
                assert abs(observed - expected) < allowance
                assert closed_error < (
                    128.0 * np.finfo(np.float64).eps / (spacing * spacing)
                )
                errors_by_mode[mode].append(observed)
            diagnostics = self.mapping(
                refinement["diagnostic_residuals"], "diagnostic_residuals"
            )
            assert (
                self.real(
                    diagnostics["consistent_compression_frobenius_norm"],
                    "consistent norm",
                )
                == 0.0
            )
            assert (
                self.real(
                    diagnostics["unmatched_equals_discarded_relative_error"],
                    "discarded relative error",
                )
                < 1.0e-13
            )
        for mode in reported_modes:
            assert all(
                fine < coarse
                for coarse, fine in zip(
                    errors_by_mode[mode][:-1], errors_by_mode[mode][1:], strict=True
                )
            )
        recorded_orders = self.mapping(
            payload["observed_relative_error_orders"], "observed orders"
        )
        for mode in order_modes:
            recorded = self.sequence(recorded_orders[str(mode)], "mode orders")
            assert recorded[0] is None
            independent = tuple(
                float(np.log(a / b) / np.log(h_a / h_b))
                for h_a, h_b, a, b in zip(
                    spacings[:-1],
                    spacings[1:],
                    errors_by_mode[mode][:-1],
                    errors_by_mode[mode][1:],
                    strict=True,
                )
            )
            np.testing.assert_allclose(
                self.real_sequence(recorded[1:], "orders"),
                independent,
                rtol=2.0e-10,
                atol=2.0e-10,
            )
            assert 1.99 < self.real(recorded[-1], "last order") < 2.01
        assert payload["limitations"] == [
            "Observed order concerns fixed-index eigenvalues only.",
            "The series does not establish uniform spectral convergence.",
            "Residual norms on different matrix spaces are not convergence metrics.",
            "The result is not semiconductor evidence or scientific validation.",
        ]
