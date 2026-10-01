"""Independent verification of the PIAB1D multi-norm sweep."""

from __future__ import annotations

from pathlib import Path

import numpy as np

from .decoder import ParticleInBoxCampaignResultDecoder


class ParticleInBoxNormSweepVerifier(ParticleInBoxCampaignResultDecoder):
    """Independently verify the retained multi-norm campaign."""

    def execute(self, path: Path) -> None:
        """Raise unless one result satisfies the declared norm identities."""
        payload = self.decode(path)
        assert self.integer(payload["schema_version"], "schema_version") == 1
        input_payload = self.mapping(payload["input"], "input")
        series = self.mapping(input_payload["grid_series"], "grid_series")
        point_counts = self.integer_sequence(
            series["interior_points"], "interior_points"
        )
        retained = self.integer(series["retained_dimension"], "retained_dimension")
        grids = self.sequence(payload["grids"], "grids")
        boundary_ratios: list[float] = []
        unmatched_ratios: list[float] = []
        for value, expected_points in zip(grids, point_counts, strict=True):
            grid = self.mapping(value, "grid")
            points = self.integer(grid["interior_points"], "interior_points")
            assert points == expected_points
            spacing = self.real(grid["spacing"], "spacing")
            prefactor = 1.0 / (2.0 * spacing * spacing)
            indices = np.arange(1, points + 1, dtype=np.float64)
            eigenvalues = (
                4.0 * prefactor * np.sin(indices * np.pi / (2.0 * (points + 1))) ** 2
            )
            expected_hamiltonian = {
                "frobenius": prefactor * np.sqrt(6.0 * points - 2.0),
                "spectral": float(eigenvalues[-1]),
                "maximum_entry": 2.0 * prefactor,
            }
            hamiltonian_norms = self.mapping(
                grid["hamiltonian_norms"], "hamiltonian_norms"
            )
            for name, expected in expected_hamiltonian.items():
                np.testing.assert_allclose(
                    self.real(hamiltonian_norms[name], name),
                    expected,
                    rtol=2.0e-13,
                    atol=2.0e-12,
                )
            residuals = self.mapping(grid["operator_residuals"], "residuals")
            consistent = self.mapping(
                residuals["consistent_compression"], "consistent compression"
            )
            for section in ("raw", "relative_to_hamiltonian"):
                values = self.mapping(consistent[section], section)
                assert all(
                    self.real(item, name) == 0.0 for name, item in values.items()
                )
            boundary = self.mapping(residuals["boundary_realization"], "boundary")
            boundary_raw = self.mapping(boundary["raw"], "boundary raw")
            boundary_relative = self.mapping(
                boundary["relative_to_hamiltonian"], "boundary relative"
            )
            expected_boundary = {
                "frobenius": np.sqrt(2.0) * prefactor,
                "spectral": prefactor,
                "maximum_entry": prefactor,
            }
            for name, expected in expected_boundary.items():
                np.testing.assert_allclose(
                    self.real(boundary_raw[name], name),
                    expected,
                    rtol=2.0e-13,
                    atol=2.0e-12,
                )
                np.testing.assert_allclose(
                    self.real(boundary_relative[name], name),
                    expected / expected_hamiltonian[name],
                    rtol=2.0e-13,
                    atol=2.0e-13,
                )
            unmatched = self.mapping(residuals["unmatched_compression"], "unmatched")
            unmatched_raw = self.mapping(unmatched["raw"], "unmatched raw")
            expected_frobenius = float(
                np.sqrt(np.sum(np.square(eigenvalues[retained:])))
            )
            np.testing.assert_allclose(
                self.real(unmatched_raw["frobenius"], "unmatched frobenius"),
                expected_frobenius,
                rtol=2.0e-13,
                atol=2.0e-11,
            )
            np.testing.assert_allclose(
                self.real(unmatched_raw["spectral"], "unmatched spectral"),
                eigenvalues[-1],
                rtol=2.0e-13,
                atol=2.0e-11,
            )
            boundary_ratios.append(
                self.real(boundary_relative["frobenius"], "boundary ratio")
            )
            unmatched_relative = self.mapping(
                unmatched["relative_to_hamiltonian"], "unmatched relative"
            )
            unmatched_ratios.append(
                self.real(unmatched_relative["frobenius"], "unmatched ratio")
            )
            algebraic = self.mapping(
                grid["full_eigenpair_algebraic_residual"], "algebraic residual"
            )
            algebraic_relative = self.mapping(
                algebraic["relative_to_hamiltonian"], "algebraic relative"
            )
            assert all(
                self.real(item, name) < 1.0e-13
                for name, item in algebraic_relative.items()
            )
        assert all(
            fine < coarse
            for coarse, fine in zip(
                boundary_ratios[:-1], boundary_ratios[1:], strict=True
            )
        )
        assert all(
            fine > coarse
            for coarse, fine in zip(
                unmatched_ratios[:-1], unmatched_ratios[1:], strict=True
            )
        )
        assert payload["limitations"] == [
            "Raw matrix norms are dimension- and discretization-scale-dependent.",
            (
                "Normalized norms compare each residual only with its same-grid "
                "Hamiltonian."
            ),
            "Maximum-entry norms are basis-dependent.",
            "Algebraic eigenpair residuals do not measure continuum error.",
            "The result is not semiconductor evidence or scientific validation.",
        ]
