"""Independent verification for particle-in-a-box auxiliary campaigns."""

from __future__ import annotations

import json
from pathlib import Path
from typing import cast

import numpy as np
import numpy.typing as npt

type JsonValue = (
    None | bool | int | float | str | list[JsonValue] | dict[str, JsonValue]
)
type RealMatrix = npt.NDArray[np.float64]


class ParticleInBoxCampaignResultDecoder:
    """Own strict JSON mechanics shared only by independent campaign verifiers."""

    __slots__ = ()

    def decode(self, path: Path) -> dict[str, JsonValue]:
        """Decode one UTF-8 JSON result object."""
        if not isinstance(path, Path):
            raise TypeError("path must be pathlib.Path")
        return self.mapping(
            cast(JsonValue, json.loads(path.read_text(encoding="utf-8"))), "result"
        )

    @staticmethod
    def mapping(value: JsonValue, name: str) -> dict[str, JsonValue]:
        """Return one JSON object with string keys."""
        if not isinstance(value, dict) or not all(type(key) is str for key in value):
            raise TypeError(f"{name} must be a JSON object")
        return value

    @staticmethod
    def sequence(value: JsonValue, name: str) -> list[JsonValue]:
        """Return one JSON array."""
        if not isinstance(value, list):
            raise TypeError(f"{name} must be a JSON array")
        return value

    @staticmethod
    def integer(value: JsonValue, name: str) -> int:
        """Return one built-in JSON integer excluding booleans."""
        if isinstance(value, bool) or not isinstance(value, int):
            raise TypeError(f"{name} must be a JSON integer")
        return value

    @staticmethod
    def real(value: JsonValue, name: str) -> float:
        """Return one finite JSON real excluding booleans."""
        if isinstance(value, bool) or not isinstance(value, int | float):
            raise TypeError(f"{name} must be a JSON real")
        result = float(value)
        if not np.isfinite(result):
            raise ValueError(f"{name} must be finite")
        return result

    @classmethod
    def integer_sequence(cls, value: JsonValue, name: str) -> tuple[int, ...]:
        """Return one JSON integer sequence."""
        return tuple(cls.integer(item, name) for item in cls.sequence(value, name))

    @classmethod
    def real_sequence(cls, value: JsonValue, name: str) -> tuple[float, ...]:
        """Return one JSON real sequence."""
        return tuple(cls.real(item, name) for item in cls.sequence(value, name))

    @classmethod
    def matrix(cls, value: JsonValue, name: str) -> RealMatrix:
        """Return one finite binary64 matrix from nested JSON arrays."""
        rows = cls.sequence(value, name)
        matrix = np.asarray(rows, dtype=np.float64)
        if matrix.ndim != 2 or not np.all(np.isfinite(matrix)):
            raise ValueError(f"{name} must be a finite matrix")
        return matrix


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


class ParticleInBoxIdentifiabilityVerifier(ParticleInBoxCampaignResultDecoder):
    """Independently verify the retained identifiability campaign."""

    def execute(self, path: Path) -> None:
        """Raise unless one result satisfies decomposition and fit identities."""
        payload = self.decode(path)
        assert self.integer(payload["schema_version"], "schema_version") == 1
        retained = self.mapping(payload["retained_space"], "retained_space")
        hamiltonian = self.matrix(retained["reduced_hamiltonian"], "Hamiltonian")
        assert hamiltonian.shape == (3, 3)
        assert self.integer(retained["dimension"], "dimension") == 3
        shift = self.matrix(payload["illustrative_shift"], "shift")
        np.testing.assert_array_equal(shift, shift.T)
        decompositions = self.mapping(payload["decompositions"], "decompositions")
        physical = self.mapping(
            decompositions["consistently_reduced_dirichlet"], "physical"
        )
        shifted = self.mapping(decompositions["illustratively_shifted"], "shifted")
        physical_kinetic = self.matrix(physical["kinetic"], "physical kinetic")
        physical_potential = self.matrix(physical["potential"], "physical potential")
        shifted_kinetic = self.matrix(shifted["kinetic"], "shifted kinetic")
        shifted_potential = self.matrix(shifted["potential"], "shifted potential")
        np.testing.assert_allclose(
            physical_kinetic + physical_potential,
            hamiltonian,
            rtol=0.0,
            atol=2.0e-14,
        )
        np.testing.assert_allclose(
            shifted_kinetic + shifted_potential,
            hamiltonian,
            rtol=0.0,
            atol=2.0e-14,
        )
        np.testing.assert_array_equal(physical_potential, np.zeros((3, 3)))
        np.testing.assert_array_equal(shifted_potential, shift)
        dimension = shift.shape[0]
        rows, columns = np.indices(shift.shape)
        independent = {
            "scalar_identity": np.eye(dimension) * np.trace(shift) / dimension,
            "diagonal_in_retained_basis": np.diag(np.diag(shift)),
            "real_symmetric_tridiagonal": np.where(
                np.abs(rows - columns) <= 1, shift, 0.0
            ),
            "arbitrary_real_symmetric": shift,
        }
        fits = self.mapping(payload["model_class_fits"], "model_class_fits")
        input_payload = self.mapping(payload["input"], "input")
        classes = self.sequence(
            input_payload["admissible_model_classes"], "admissible_model_classes"
        )
        norms: list[float] = []
        for value in classes:
            if not isinstance(value, str):
                raise TypeError("model class names must be strings")
            candidate = independent[value]
            unexplained = shift - candidate
            record = self.mapping(fits[value], "fit")
            np.testing.assert_array_equal(
                self.matrix(record["best_fit"], "best_fit"), candidate
            )
            np.testing.assert_array_equal(
                self.matrix(record["unexplained_residual"], "unexplained residual"),
                unexplained,
            )
            observed = self.real(
                record["unexplained_frobenius_norm"], "unexplained norm"
            )
            np.testing.assert_allclose(
                observed,
                np.linalg.norm(unexplained, ord="fro"),
                rtol=0.0,
                atol=2.0e-15,
            )
            norms.append(observed)
        assert norms[0] > norms[1] > norms[2] > norms[3]
        assert norms[-1] == 0.0
        assert payload["limitations"] == [
            "The alternative shift is illustrative and has no physical assignment.",
            (
                "Model-class fits depend on the declared retained basis and "
                "Frobenius metric."
            ),
            "Algebraic reconstructability does not establish physical identifiability.",
            "The result is not semiconductor evidence or scientific validation.",
        ]
