"""Independent verification of particle-in-a-box residual-study results."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import cast

import numpy as np
import numpy.typing as npt

type JsonValue = (
    None | bool | int | float | str | list[JsonValue] | dict[str, JsonValue]
)
type RealMatrix = npt.NDArray[np.float64]

HISTORICAL_RUNNER_SHA256 = (
    "e945c0a6320f84b3b32e938e5cf7cd6f779ecf3261846abd67a2ae192a08252d"
)


class ParticleInBoxResultVerifier:
    """Verify retained or currently authored results without importing producers."""

    __slots__ = ()

    def execute(self, path: Path, repository_root: Path) -> None:
        """Raise unless one version-one result satisfies independent identities."""
        if not isinstance(path, Path):
            raise TypeError("path must be pathlib.Path")
        if not isinstance(repository_root, Path):
            raise TypeError("repository_root must be pathlib.Path")
        payload = self.mapping(
            cast(JsonValue, json.loads(path.read_text(encoding="utf-8"))), "result"
        )
        assert self.integer(payload["schema_version"], "schema_version") == 1
        assert payload["evidence_status"] == "illustrative numerical experiment"
        assert payload["calculation_status"] == "calculated illustrative result"
        input_payload = self.mapping(payload["input"], "input")
        parameters = self.mapping(
            input_payload["dimensionless_parameters"], "dimensionless_parameters"
        )
        length = self.real(parameters["length"], "length")
        mass = self.real(parameters["mass"], "mass")
        hbar = self.real(parameters["hbar"], "hbar")
        points = self.integer(parameters["interior_points"], "interior_points")
        retained = self.integer(parameters["retained_dimension"], "retained_dimension")
        spacing = length / (points + 1)
        prefactor = hbar * hbar / (2.0 * mass * spacing * spacing)
        expected_hamiltonian = np.diag(np.full(points, 2.0 * prefactor))
        expected_hamiltonian += np.diag(np.full(points - 1, -prefactor), 1)
        expected_hamiltonian += np.diag(np.full(points - 1, -prefactor), -1)
        hamiltonian = self.matrix(payload, "matrices", "dirichlet_hamiltonian_full")
        np.testing.assert_array_equal(hamiltonian, expected_hamiltonian)

        indices = np.arange(1, points + 1, dtype=np.float64)
        z = indices * np.pi / (2.0 * (points + 1))
        expected_discrete = 4.0 * prefactor * np.sin(z) ** 2
        expected_continuum = (
            hbar
            * hbar
            * np.pi
            * np.pi
            * indices
            * indices
            / (2.0 * mass * length * length)
        )
        spectra = self.mapping(payload["spectra"], "spectra")
        computed = self.vector(spectra["computed_discrete"], "computed_discrete")
        recorded_discrete = self.vector(
            spectra["discrete_closed_form"], "discrete_closed_form"
        )
        recorded_continuum = self.vector(
            spectra["continuum_closed_form"], "continuum_closed_form"
        )
        recorded_ratio = self.vector(
            spectra["discrete_to_continuum_ratio"], "discrete_to_continuum_ratio"
        )
        np.testing.assert_array_equal(recorded_discrete, expected_discrete)
        np.testing.assert_array_equal(recorded_continuum, expected_continuum)
        np.testing.assert_allclose(
            recorded_ratio,
            (np.sin(z) / z) ** 2,
            rtol=16.0 * np.finfo(np.float64).eps,
            atol=0.0,
        )
        scale = float(np.max(expected_discrete))
        np.testing.assert_allclose(
            computed,
            expected_discrete,
            rtol=64.0 * np.finfo(np.float64).eps,
            atol=64.0 * np.finfo(np.float64).eps * scale,
        )

        vectors = self.matrix(payload, "matrices", "retained_eigenvectors")
        projector = self.matrix(payload, "matrices", "spectral_projector_full")
        embedded = self.matrix(
            payload, "matrices", "retained_hamiltonian_embedded_full"
        )
        coordinates = self.matrix(
            payload, "matrices", "retained_hamiltonian_coordinates"
        )
        tolerance = (
            256.0
            * np.finfo(np.float64).eps
            * float(np.linalg.norm(hamiltonian, ord="fro"))
        )
        np.testing.assert_allclose(
            vectors.T @ vectors, np.eye(retained), atol=tolerance
        )
        np.testing.assert_allclose(projector, vectors @ vectors.T, atol=tolerance)
        np.testing.assert_allclose(projector @ projector, projector, atol=tolerance)
        np.testing.assert_allclose(
            embedded, projector @ hamiltonian @ projector, atol=tolerance
        )
        np.testing.assert_allclose(
            coordinates, vectors.T @ hamiltonian @ vectors, atol=tolerance
        )
        np.testing.assert_allclose(
            coordinates, np.diag(expected_discrete[:retained]), atol=tolerance
        )

        compressed = self.residual(
            payload, "consistently_compressed_physical_potential", "matrix"
        )
        np.testing.assert_array_equal(compressed, np.zeros((points, points)))
        unmatched = self.residual(
            payload, "projected_hamiltonian_minus_unprojected_kinetic", "matrix"
        )
        discarded = self.residual(
            payload,
            "projected_hamiltonian_minus_unprojected_kinetic",
            "discarded_sector_reference",
        )
        np.testing.assert_allclose(unmatched, embedded - hamiltonian, atol=tolerance)
        np.testing.assert_allclose(unmatched, discarded, atol=tolerance)
        assert float(np.linalg.norm(unmatched, ord="fro")) > tolerance
        boundary = self.residual(payload, "dirichlet_minus_cyclic_reference", "matrix")
        expected_boundary = np.zeros((points, points))
        expected_boundary[0, -1] = prefactor
        expected_boundary[-1, 0] = prefactor
        np.testing.assert_array_equal(boundary, expected_boundary)
        assert payload["limitations"] == [
            "The finite matrix is not the continuum differential operator.",
            (
                "The cyclic-reference residual is not a "
                "representation-independent potential."
            ),
            "The result is not semiconductor evidence or scientific validation.",
        ]
        self.verify_provenance(payload, repository_root.resolve())

    def verify_provenance(
        self, payload: dict[str, JsonValue], repository_root: Path
    ) -> None:
        """Verify historical or current implementation identities explicitly."""
        provenance = self.mapping(payload["provenance"], "provenance")
        input_path = repository_root / self.string(
            provenance["input_path"], "input_path"
        )
        assert hashlib.sha256(input_path.read_bytes()).hexdigest() == self.string(
            provenance["input_sha256"], "input_sha256"
        )
        recorded_runner = self.string(provenance["script_sha256"], "script_sha256")
        identities = provenance.get("implementation_identities")
        if identities is None:
            if recorded_runner != HISTORICAL_RUNNER_SHA256:
                raise ValueError("unrecognized historical runner identity")
            return
        if not isinstance(identities, list):
            raise TypeError("implementation_identities must be a JSON array")
        expected = {
            "python/src/ksdft2effmass/analysis/model_systems/intervals.py",
            "python/src/ksdft2effmass/analysis/model_systems/particle_in_box/model.py",
            "python/src/ksdft2effmass/operators/eigenpairs.py",
            "python/src/ksdft2effmass/operators/finite_differences.py",
            "python/src/ksdft2effmass/operators/quantities.py",
            (
                "python/src/ksdft2effmass/campaigns/research_monograph/"
                "particle_in_box/records.py"
            ),
            (
                "python/src/ksdft2effmass/campaigns/research_monograph/"
                "particle_in_box/input.py"
            ),
            (
                "python/src/ksdft2effmass/campaigns/research_monograph/"
                "particle_in_box/residual_study.py"
            ),
            (
                "python/src/ksdft2effmass/campaigns/research_monograph/"
                "particle_in_box/serialization.py"
            ),
        }
        observed: set[str] = set()
        for value in identities:
            identity = self.mapping(value, "implementation identity")
            relative = self.string(identity["path"], "implementation path")
            observed.add(relative)
            source = repository_root / relative
            assert hashlib.sha256(source.read_bytes()).hexdigest() == self.string(
                identity["sha256"], "implementation sha256"
            )
        if observed != expected:
            raise ValueError("implementation identity paths do not match")
        script_path = repository_root / self.string(
            provenance["script_path"], "script_path"
        )
        assert hashlib.sha256(script_path.read_bytes()).hexdigest() == recorded_runner

    @staticmethod
    def mapping(value: JsonValue, name: str) -> dict[str, JsonValue]:
        """Return one JSON object with string keys."""
        if not isinstance(value, dict) or not all(
            isinstance(key, str) for key in value
        ):
            raise TypeError(f"{name} must be a JSON object")
        return value

    @staticmethod
    def string(value: JsonValue, name: str) -> str:
        """Return one nonempty JSON string."""
        if not isinstance(value, str) or not value:
            raise TypeError(f"{name} must be a nonempty string")
        return value

    @staticmethod
    def integer(value: JsonValue, name: str) -> int:
        """Return one built-in integer excluding booleans."""
        if isinstance(value, bool) or not isinstance(value, int):
            raise TypeError(f"{name} must be an integer")
        return value

    @staticmethod
    def real(value: JsonValue, name: str) -> float:
        """Return one built-in finite JSON real excluding booleans."""
        if isinstance(value, bool) or not isinstance(value, int | float):
            raise TypeError(f"{name} must be a JSON real")
        result = float(value)
        if not np.isfinite(result):
            raise ValueError(f"{name} must be finite")
        return result

    @staticmethod
    def vector(value: JsonValue, name: str) -> npt.NDArray[np.float64]:
        """Decode one binary64 vector."""
        if not isinstance(value, list):
            raise TypeError(f"{name} must be a JSON array")
        return np.asarray(value, dtype=np.float64)

    def matrix(
        self, payload: dict[str, JsonValue], section: str, name: str
    ) -> RealMatrix:
        """Decode one matrix from a named result section."""
        values = self.mapping(payload[section], section)[name]
        if not isinstance(values, list):
            raise TypeError(f"{name} must be a JSON array")
        return np.asarray(values, dtype=np.float64)

    def residual(
        self, payload: dict[str, JsonValue], name: str, field: str
    ) -> RealMatrix:
        """Decode one residual matrix field."""
        residuals = self.mapping(payload["residuals"], "residuals")
        record = self.mapping(residuals[name], name)
        values = record[field]
        if not isinstance(values, list):
            raise TypeError(f"{name}.{field} must be a JSON array")
        return np.asarray(values, dtype=np.float64)
