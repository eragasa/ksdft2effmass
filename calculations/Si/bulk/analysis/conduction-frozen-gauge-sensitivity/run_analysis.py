from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path

import numpy as np
from numpy.typing import NDArray
from projectkoios.physkit import units as _physkit_units
from projectkoios.physkit.units import PhysicalUnit
from scipy import constants  # type: ignore[import-untyped]
from scipy.optimize import minimize  # type: ignore[import-untyped]

if not hasattr(_physkit_units, "ModelSystemUnitConverter"):
    _physkit_units.ModelSystemUnitConverter = (  # type: ignore[attr-defined]
        _physkit_units.MODEL_SYSTEM_UNIT_CONVERTER
    )

from projectkoios.integrations.wannier90 import (
    Wannier90EigenvalueParser,
    Wannier90HamiltonianBlockParser,
)

ROOT = Path(__file__).resolve().parent
BULK = ROOT.parents[1]
SIMULATION_EVIDENCE = BULK / "simulations" / "evidence"
STRUCTURE = (
    BULK
    / "simulations"
    / "structures"
    / "Si.PrimitiveUnitCell.RightHanded.RelaxedS1.json"
)
EIG = (
    SIMULATION_EVIDENCE
    / "sssp-1.3.0-pbe-efficiency-qe-7.5-accepted-s1-pw2wannier90-sp3sstar"
    / "result"
    / "silicon.eig"
)
HR_500 = (
    SIMULATION_EVIDENCE
    / "sssp-1.3.0-pbe-efficiency-qe-7.5-accepted-s1-wannier90-localization-"
    "conduction-frozen-blocked" / "result" / "silicon_hr.dat"
)
HR_1000 = (
    SIMULATION_EVIDENCE
    / "sssp-1.3.0-pbe-efficiency-qe-7.5-accepted-s1-wannier90-localization-"
    "conduction-frozen-iter1000-blocked" / "result" / "silicon_hr.dat"
)
EXPECTED_IDENTITIES = {
    "structure": (
        758,
        "d131107753512c53dc0a32b9e07e0081f8277d8eeafcb9fad5f1fc7f153ded03",
    ),
    "eig": (29952, "e2a86cbab7f14a607987fe5d965449541703ebece16db8500b2b1cb74ecb743a"),
    "hr_500": (
        465533,
        "f3988f96a8c12615c0fda9d2e259df869b76fbdac1d804b8e780b5f9453a1d2f",
    ),
    "hr_1000": (
        465533,
        "9233921c5888ea731c00aa0f447f33a3e8001f4187863d18497c470de9b9b60d",
    ),
}
ENERGY_UNIT = PhysicalUnit("eV")
DENSE_GRID_SIZE = 41
EDGE_WINDOW_EV = 0.5
PRIMARY_HESSIAN_STEP_INVERSE_ANGSTROM = 0.002
HESSIAN_STEPS_INVERSE_ANGSTROM = (0.001, 0.002, 0.005, 0.010)
SOURCE_GRID_SIZE = 4
OPTIMIZATION_START_COUNT = 20
ELECTRON_MASS_CURVATURE_EV_ANGSTROM2 = (
    constants.hbar**2 / constants.m_e / constants.electron_volt * 1.0e20
)

RealArray = NDArray[np.float64]
ComplexArray = NDArray[np.complex128]


@dataclass(frozen=True, slots=True)
class FiniteHamiltonian:
    representatives: NDArray[np.int64]
    degeneracies: NDArray[np.float64]
    blocks_ev: ComplexArray

    def matrices(self, kpoints: RealArray) -> ComplexArray:
        phase = np.exp(2.0j * np.pi * (kpoints @ self.representatives.T))
        weighted = phase / self.degeneracies
        matrices = np.einsum("kr,rij->kij", weighted, self.blocks_ev, optimize=True)
        return 0.5 * (matrices + matrices.conj().transpose(0, 2, 1))

    def eigenvalues(self, kpoints: RealArray, chunk_size: int = 4096) -> RealArray:
        chunks = []
        for start in range(0, len(kpoints), chunk_size):
            matrices = self.matrices(kpoints[start : start + chunk_size])
            chunks.append(np.linalg.eigvalsh(matrices))
        return np.concatenate(chunks, axis=0)

    def eigenvalue(self, kpoint: RealArray, index: int) -> float:
        values = np.linalg.eigvalsh(self.matrices(kpoint[np.newaxis, :])[0])
        return float(values[index])


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def authenticate(name: str, path: Path) -> dict[str, int | str]:
    expected_size, expected_sha256 = EXPECTED_IDENTITIES[name]
    observed_size = path.stat().st_size
    observed_sha256 = sha256(path)
    if observed_size != expected_size or observed_sha256 != expected_sha256:
        raise RuntimeError(f"{name} artifact identity mismatch")
    return {
        "path": str(path.relative_to(BULK)),
        "byte_size": observed_size,
        "sha256": observed_sha256,
    }


def load_hamiltonian(path: Path) -> FiniteHamiltonian:
    parsed = Wannier90HamiltonianBlockParser().execute(path.read_bytes(), ENERGY_UNIT)
    if parsed.wannier_count != 10 or len(parsed.representatives) != 93:
        raise RuntimeError("unexpected Hamiltonian dimensions")
    return FiniteHamiltonian(
        np.asarray(parsed.representatives, dtype=np.int64),
        np.asarray(parsed.degeneracies, dtype=np.float64),
        np.asarray(tuple(block.magnitude for block in parsed.blocks)),
    )


def regular_grid(size: int) -> RealArray:
    values = np.arange(size, dtype=np.float64) / size
    return np.asarray(
        [(i, j, k) for i in values for j in values for k in values],
        dtype=np.float64,
    )


def error_summary(difference: RealArray) -> dict[str, float]:
    return {
        "maximum_absolute_ev": float(np.max(np.abs(difference))),
        "rms_ev": float(np.sqrt(np.mean(np.square(difference)))),
        "percentile_95_absolute_ev": float(np.percentile(np.abs(difference), 95.0)),
    }


def direct_lattice_angstrom() -> RealArray:
    record = json.loads(STRUCTURE.read_text(encoding="utf-8"))
    vectors = np.asarray(
        [
            record["lattice"]["A"]["a1"],
            record["lattice"]["A"]["a2"],
            record["lattice"]["A"]["a3"],
        ],
        dtype=np.float64,
    ).T
    return vectors * float(record["lattice"]["lattice_parameter"]["magnitude"])


def optimize_conduction_minimum(
    model: FiniteHamiltonian,
    dense_kpoints: RealArray,
    dense_eigenvalues: RealArray,
) -> tuple[float, RealArray, bool, int]:
    lowest_conduction = dense_eigenvalues[:, 2]
    starts = np.argpartition(lowest_conduction, OPTIMIZATION_START_COUNT)[
        :OPTIMIZATION_START_COUNT
    ]
    candidates: list[tuple[float, RealArray, bool, int]] = []
    for index in starts:
        result = minimize(
            lambda point: model.eigenvalue(np.asarray(point) % 1.0, 2),
            dense_kpoints[index],
            method="Nelder-Mead",
            options={"xatol": 1.0e-11, "fatol": 1.0e-12, "maxiter": 2000},
        )
        candidates.append(
            (
                float(result.fun),
                np.asarray(result.x, dtype=np.float64) % 1.0,
                bool(result.success),
                int(result.nit),
            )
        )
    return min(candidates, key=lambda candidate: candidate[0])


def curvature_diagnostics(
    model: FiniteHamiltonian,
    minimum_fractional: RealArray,
    reciprocal_lattice_inverse_angstrom: RealArray,
) -> list[dict[str, float | list[float]]]:
    inverse_reciprocal = np.linalg.inv(reciprocal_lattice_inverse_angstrom)
    origin = model.eigenvalue(minimum_fractional, 2)
    diagnostics: list[dict[str, float | list[float]]] = []
    for step in HESSIAN_STEPS_INVERSE_ANGSTROM:
        hessian = np.empty((3, 3), dtype=np.float64)
        for row in range(3):
            delta_row = inverse_reciprocal[:, row] * step
            hessian[row, row] = (
                model.eigenvalue(minimum_fractional + delta_row, 2)
                - 2.0 * origin
                + model.eigenvalue(minimum_fractional - delta_row, 2)
            ) / step**2
            for column in range(row):
                delta_column = inverse_reciprocal[:, column] * step
                value = (
                    model.eigenvalue(minimum_fractional + delta_row + delta_column, 2)
                    - model.eigenvalue(minimum_fractional + delta_row - delta_column, 2)
                    - model.eigenvalue(minimum_fractional - delta_row + delta_column, 2)
                    + model.eigenvalue(minimum_fractional - delta_row - delta_column, 2)
                ) / (4.0 * step**2)
                hessian[row, column] = value
                hessian[column, row] = value
        curvatures = np.linalg.eigvalsh(hessian)
        masses = ELECTRON_MASS_CURVATURE_EV_ANGSTROM2 / curvatures
        diagnostics.append(
            {
                "step_inverse_angstrom": step,
                "principal_curvatures_ev_angstrom_squared": curvatures.tolist(),
                "curvature_derived_mass_ratios_to_electron_mass": masses.tolist(),
            }
        )
    return diagnostics


def locality_diagnostics(
    model: FiniteHamiltonian,
    direct_lattice: RealArray,
    dense_kpoints: RealArray,
) -> dict[str, list[dict[str, float | int]] | float]:
    radii = np.linalg.norm(
        (direct_lattice @ model.representatives.astype(np.float64).T).T,
        axis=1,
    )
    effective_blocks = model.blocks_ev / model.degeneracies[:, np.newaxis, np.newaxis]
    spectral_norms = np.linalg.svd(effective_blocks, compute_uv=False)[:, 0]
    frobenius_norms = np.linalg.norm(effective_blocks, axis=(1, 2))
    shells = sorted(float(value) for value in np.unique(np.round(radii, decimals=9)))
    records: list[dict[str, float | int]] = []
    for radius in shells:
        tail = radii > radius + 5.0e-9
        if np.any(tail):
            tail_model = FiniteHamiltonian(
                model.representatives[tail],
                model.degeneracies[tail],
                model.blocks_ev[tail],
            )
            maximum_direct_error = 0.0
            for start in range(0, len(dense_kpoints), 4096):
                matrices = tail_model.matrices(dense_kpoints[start : start + 4096])
                maximum_direct_error = max(
                    maximum_direct_error,
                    float(np.max(np.abs(np.linalg.eigvalsh(matrices)))),
                )
        else:
            maximum_direct_error = 0.0
        records.append(
            {
                "radius_angstrom": radius,
                "excluded_representative_count": int(np.count_nonzero(tail)),
                "spectral_tail_bound_ev": float(np.sum(spectral_norms[tail])),
                "frobenius_tail_rms_ev": float(
                    np.sqrt(np.sum(np.square(frobenius_norms[tail])))
                ),
                "dense_grid_maximum_direct_operator_error_ev": maximum_direct_error,
            }
        )
    return {
        "maximum_representative_radius_angstrom": float(np.max(radii)),
        "frobenius_squared_weighted_mean_radius_angstrom": float(
            np.sum(radii * np.square(frobenius_norms))
            / np.sum(np.square(frobenius_norms))
        ),
        "shells": records,
    }


def candidate_diagnostics(
    label: str,
    model: FiniteHamiltonian,
    dense_kpoints: RealArray,
    dense_eigenvalues: RealArray,
    direct_lattice: RealArray,
    reciprocal_lattice: RealArray,
) -> tuple[dict[str, object], RealArray]:
    energy, fractional, success, iterations = optimize_conduction_minimum(
        model, dense_kpoints, dense_eigenvalues
    )
    return (
        {
            "label": label,
            "optimized_lowest_conduction_minimum": {
                "energy_ev_native_reference": energy,
                "fractional_reciprocal_coordinates": fractional.tolist(),
                "optimizer_success": success,
                "optimizer_iterations": iterations,
            },
            "curvature_diagnostics": curvature_diagnostics(
                model, fractional, reciprocal_lattice
            ),
            "locality": locality_diagnostics(model, direct_lattice, dense_kpoints),
        },
        fractional,
    )


def main() -> None:
    sources = {
        "structure": authenticate("structure", STRUCTURE),
        "eig": authenticate("eig", EIG),
        "hr_500": authenticate("hr_500", HR_500),
        "hr_1000": authenticate("hr_1000", HR_1000),
    }
    model_500 = load_hamiltonian(HR_500)
    model_1000 = load_hamiltonian(HR_1000)
    if not np.array_equal(model_500.representatives, model_1000.representatives):
        raise RuntimeError("candidate representative inventories disagree")
    if not np.array_equal(model_500.degeneracies, model_1000.degeneracies):
        raise RuntimeError("candidate degeneracy inventories disagree")
    parent = (
        Wannier90EigenvalueParser()
        .execute(EIG.read_bytes(), ENERGY_UNIT)
        .eigenvalues.magnitude
    )
    if parent.shape != (64, 12):
        raise RuntimeError("unexpected parent eigenvalue shape")
    source_kpoints = regular_grid(SOURCE_GRID_SIZE)
    source_500 = model_500.eigenvalues(source_kpoints)
    source_1000 = model_1000.eigenvalues(source_kpoints)
    dense_kpoints = regular_grid(DENSE_GRID_SIZE)
    dense_500 = model_500.eigenvalues(dense_kpoints)
    dense_1000 = model_1000.eigenvalues(dense_kpoints)
    dense_difference = dense_1000 - dense_500
    edge_500 = float(np.min(dense_500[:, 2]))
    edge_1000 = float(np.min(dense_1000[:, 2]))
    edge_mask = (dense_500[:, 2] <= edge_500 + EDGE_WINDOW_EV) | (
        dense_1000[:, 2] <= edge_1000 + EDGE_WINDOW_EV
    )
    direct_lattice = direct_lattice_angstrom()
    reciprocal_lattice = 2.0 * np.pi * np.linalg.inv(direct_lattice).T
    candidate_500, minimum_500 = candidate_diagnostics(
        "num_iter_500",
        model_500,
        dense_kpoints,
        dense_500,
        direct_lattice,
        reciprocal_lattice,
    )
    candidate_1000, minimum_1000 = candidate_diagnostics(
        "num_iter_1000",
        model_1000,
        dense_kpoints,
        dense_1000,
        direct_lattice,
        reciprocal_lattice,
    )
    result = {
        "schema_version": 1,
        "status": "exploratory-diagnostic-complete",
        "calculator_invocations": 0,
        "sources": sources,
        "comparison_contract": {
            "source_grid": "Gamma-origin 4 x 4 x 4",
            "dense_grid": "Gamma-origin 41 x 41 x 41",
            "dense_grid_point_count": len(dense_kpoints),
            "conduction_candidate_band_indices_one_based": [3, 10],
            "parent_conduction_band_indices_one_based": [5, 12],
            "edge_union_window_ev": EDGE_WINDOW_EV,
            "optimization_start_count": OPTIMIZATION_START_COUNT,
            "primary_hessian_step_inverse_angstrom": (
                PRIMARY_HESSIAN_STEP_INVERSE_ANGSTROM
            ),
            "operator_comparison": "spectral only; unaligned matrices not subtracted",
        },
        "source_mesh": {
            "num_iter_500_vs_parent_conduction": error_summary(
                source_500[:, 2:] - parent[:, 4:]
            ),
            "num_iter_1000_vs_parent_conduction": error_summary(
                source_1000[:, 2:] - parent[:, 4:]
            ),
            "num_iter_500_vs_1000_all_bands": error_summary(source_1000 - source_500),
            "num_iter_500_vs_1000_conduction_bands": error_summary(
                source_1000[:, 2:] - source_500[:, 2:]
            ),
        },
        "dense_finite_representation": {
            "all_bands": error_summary(dense_difference),
            "conduction_bands": error_summary(dense_difference[:, 2:]),
            "lowest_conduction_band": error_summary(dense_difference[:, 2]),
            "edge_union": {
                "point_count": int(np.count_nonzero(edge_mask)),
                "lowest_conduction_band": error_summary(dense_difference[edge_mask, 2]),
                "all_conduction_bands": error_summary(dense_difference[edge_mask, 2:]),
            },
        },
        "candidates": [candidate_500, candidate_1000],
        "cross_evaluation_at_optimized_minima": {
            "at_num_iter_500_minimum": {
                "num_iter_500_ev": model_500.eigenvalue(minimum_500, 2),
                "num_iter_1000_ev": model_1000.eigenvalue(minimum_500, 2),
            },
            "at_num_iter_1000_minimum": {
                "num_iter_500_ev": model_500.eigenvalue(minimum_1000, 2),
                "num_iter_1000_ev": model_1000.eigenvalue(minimum_1000, 2),
            },
        },
        "disposition": (
            "diagnostic comparison only; neither blocked operator is accepted and "
            "curvature-derived masses are not validated material results"
        ),
    }
    output = ROOT / "gauge-sensitivity-result.json"
    output.write_text(
        json.dumps(result, allow_nan=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
