from __future__ import annotations

import importlib.util
import json
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from types import ModuleType

import numpy as np
from numpy.typing import NDArray

RealArray = NDArray[np.float64]
ComplexArray = NDArray[np.complex128]
type JsonScalar = None | bool | int | float | str
type JsonValue = JsonScalar | list[JsonValue] | dict[str, JsonValue]
type JsonObject = dict[str, JsonValue]

ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "multiband-result.json"
WINDOWS = (0.005, 0.01, 0.02)
FEATURES = ("xx", "yy", "zz", "xy", "xz", "yz")
DIRECTIONS = {
    "100": np.asarray([1.0, 0.0, 0.0], dtype=np.float64),
    "110": np.asarray([1.0, 1.0, 0.0], dtype=np.float64) / np.sqrt(2.0),
    "111": np.asarray([1.0, 1.0, 1.0], dtype=np.float64) / np.sqrt(3.0),
}


@dataclass(frozen=True)
class Fit:
    gamma_basis: ComplexArray
    gamma_hamiltonian_ev: ComplexArray
    coefficients_ev_angstrom_squared: tuple[ComplexArray, ...]
    residual_rms_ev: float
    maximum_subspace_angle_radians: float


def load_module(path: Path) -> ModuleType:
    specification = importlib.util.spec_from_file_location(
        "c6_b20_w21_comprehensive_edge_multiband_source", path
    )
    if specification is None or specification.loader is None:
        raise RuntimeError("cannot load comprehensive edge producer")
    module = importlib.util.module_from_spec(specification)
    sys.modules[specification.name] = module
    specification.loader.exec_module(module)
    return module


def rays() -> tuple[RealArray, ...]:
    result: list[RealArray] = []
    for x in (-1.0, 0.0, 1.0):
        for y in (-1.0, 0.0, 1.0):
            for z in (-1.0, 0.0, 1.0):
                vector = np.asarray([x, y, z], dtype=np.float64)
                if not np.any(vector):
                    continue
                vector /= np.linalg.norm(vector)
                first = int(np.flatnonzero(vector)[0])
                if vector[first] > 0.0:
                    result.append(vector)
    return tuple(result)


def polar_unitary(matrix: ComplexArray) -> ComplexArray:
    left, _, right = np.linalg.svd(matrix)
    return np.asarray(left @ right, dtype=np.complex128)


def hermitian_json(matrix: ComplexArray) -> JsonObject:
    hermitian = 0.5 * (matrix + matrix.conj().T)
    return {
        "real": np.asarray(hermitian.real, dtype=np.float64).tolist(),
        "imaginary": np.asarray(hermitian.imag, dtype=np.float64).tolist(),
    }


def cluster_matrix(
    evaluator: object,
    model_index: int,
    fractional: RealArray,
    gamma_basis: ComplexArray,
) -> tuple[ComplexArray, float]:
    matrix = np.asarray(
        evaluator.matrices(fractional.reshape(1, 3))[0, model_index],
        dtype=np.complex128,
    )
    eigenvalues, eigenvectors = np.linalg.eigh(matrix)
    cluster_vectors = np.asarray(eigenvectors[:, 1:4], dtype=np.complex128)
    overlap = gamma_basis.conj().T @ cluster_vectors
    singular_values = np.linalg.svd(overlap, compute_uv=False)
    coordinates = polar_unitary(overlap)
    represented = coordinates @ np.diag(eigenvalues[1:4]) @ coordinates.conj().T
    maximum_angle = float(np.max(np.arccos(np.clip(singular_values, 0.0, 1.0))))
    return np.asarray(represented, dtype=np.complex128), maximum_angle


def fit_model(
    analysis: ModuleType,
    evaluator: object,
    model_index: int,
    inverse_reciprocal: RealArray,
    window: float,
) -> Fit:
    gamma_matrix = np.asarray(
        evaluator.matrices(np.zeros((1, 3), dtype=np.float64))[0, model_index],
        dtype=np.complex128,
    )
    gamma_values, gamma_vectors = np.linalg.eigh(gamma_matrix)
    gamma_basis = np.asarray(gamma_vectors[:, 1:4], dtype=np.complex128)
    gamma_hamiltonian = np.asarray(
        np.diag(gamma_values[1:4]), dtype=np.complex128
    )
    designs: list[list[float]] = []
    responses: list[ComplexArray] = []
    maximum_angle = 0.0
    for direction in rays():
        for radius in np.linspace(window / 4.0, window, 4, dtype=np.float64):
            represented: list[ComplexArray] = []
            for sign in (-1.0, 1.0):
                fractional = analysis.cartesian_point(
                    np.zeros(3, dtype=np.float64),
                    sign * radius * direction,
                    inverse_reciprocal,
                )
                matrix, angle = cluster_matrix(
                    evaluator, model_index, fractional, gamma_basis
                )
                represented.append(matrix)
                maximum_angle = max(maximum_angle, angle)
            even_delta = 0.5 * (represented[0] + represented[1]) - gamma_hamiltonian
            x, y, z = radius * direction
            designs.append([x * x, y * y, z * z, 2.0 * x * y, 2.0 * x * z, 2.0 * y * z])
            responses.append(even_delta.reshape(9))
    design = np.asarray(designs, dtype=np.float64)
    response = np.asarray(responses, dtype=np.complex128)
    coefficients_flat, *_ = np.linalg.lstsq(design, response, rcond=None)
    predicted = design @ coefficients_flat
    residual = float(
        np.sqrt(np.mean(np.sum(np.abs(predicted - response) ** 2, axis=1) / 3.0))
    )
    coefficients = tuple(
        np.asarray(
            0.5
            * (
                coefficient.reshape(3, 3)
                + coefficient.reshape(3, 3).conj().T
            ),
            dtype=np.complex128,
        )
        for coefficient in coefficients_flat
    )
    return Fit(
        gamma_basis=gamma_basis,
        gamma_hamiltonian_ev=gamma_hamiltonian,
        coefficients_ev_angstrom_squared=coefficients,
        residual_rms_ev=residual,
        maximum_subspace_angle_radians=maximum_angle,
    )


def directional_curvature(
    coefficients: tuple[ComplexArray, ...], direction: RealArray
) -> RealArray:
    x, y, z = direction
    quadratic = (
        x * x * coefficients[0]
        + y * y * coefficients[1]
        + z * z * coefficients[2]
        + 2.0 * x * y * coefficients[3]
        + 2.0 * x * z * coefficients[4]
        + 2.0 * y * z * coefficients[5]
    )
    return np.asarray(2.0 * np.linalg.eigvalsh(quadratic), dtype=np.float64)


def coefficient_norm(coefficients: tuple[ComplexArray, ...]) -> float:
    return float(
        np.sqrt(sum(np.linalg.norm(coefficient) ** 2 for coefficient in coefficients))
    )


def main() -> None:
    if OUTPUT.exists():
        raise FileExistsError(f"refusing to overwrite retained result: {OUTPUT}")
    start = time.perf_counter()
    analysis = load_module(ROOT / "run_analysis.py")
    _, evaluator, _, reciprocal, _ = analysis.reconstruct()
    inverse_reciprocal = np.linalg.inv(reciprocal)
    fits: dict[str, dict[float, Fit]] = {}
    for model_index, model_name in enumerate(analysis.MODEL_NAMES):
        fits[model_name] = {
            window: fit_model(
                analysis, evaluator, model_index, inverse_reciprocal, window
            )
            for window in WINDOWS
        }
    source_primary = fits["full-source"][0.01]
    source_norm = coefficient_norm(source_primary.coefficients_ev_angstrom_squared)
    models: JsonObject = {}
    for model_name in analysis.MODEL_NAMES:
        model_fits = fits[model_name]
        primary = model_fits[0.01]
        overlap = source_primary.gamma_basis.conj().T @ primary.gamma_basis
        alignment = polar_unitary(overlap)
        aligned = tuple(
            np.asarray(alignment @ coefficient @ alignment.conj().T, dtype=np.complex128)
            for coefficient in primary.coefficients_ev_angstrom_squared
        )
        coefficient_error = float(
            np.sqrt(
                sum(
                    np.linalg.norm(candidate - source) ** 2
                    for candidate, source in zip(
                        aligned,
                        source_primary.coefficients_ev_angstrom_squared,
                        strict=True,
                    )
                )
            )
            / source_norm
        )
        windows: JsonObject = {}
        for window, fit in model_fits.items():
            direction_records: JsonObject = {}
            for direction_name, direction in DIRECTIONS.items():
                curvatures = directional_curvature(
                    fit.coefficients_ev_angstrom_squared, direction
                )
                masses: list[JsonValue] = [
                    (
                        float(
                            -analysis.ELECTRON_MASS_CURVATURE_EV_ANGSTROM2
                            / curvature
                        )
                        if curvature < 0.0
                        else None
                    )
                    for curvature in curvatures
                ]
                direction_records[direction_name] = {
                    "unit_cartesian_direction": direction.tolist(),
                    "curvature_channel_eigenvalues_ev_angstrom_squared": (
                        curvatures.tolist()
                    ),
                    "apparent_hole_masses_electron_for_negative_channels": masses,
                }
            windows[str(window)] = {
                "fit_residual_rms_ev": fit.residual_rms_ev,
                "maximum_sampled_cluster_subspace_angle_radians": (
                    fit.maximum_subspace_angle_radians
                ),
                "quadratic_coefficient_matrices": {
                    name: hermitian_json(coefficient)
                    for name, coefficient in zip(
                        FEATURES,
                        fit.coefficients_ev_angstrom_squared,
                        strict=True,
                    )
                },
                "directions": direction_records,
            }
        primary_coefficients = primary.coefficients_ev_angstrom_squared
        window_sensitivity: JsonObject = {}
        primary_norm = coefficient_norm(primary_coefficients)
        for window, fit in model_fits.items():
            window_sensitivity[str(window)] = float(
                np.sqrt(
                    sum(
                        np.linalg.norm(candidate - reference) ** 2
                        for candidate, reference in zip(
                            fit.coefficients_ev_angstrom_squared,
                            primary_coefficients,
                            strict=True,
                        )
                    )
                )
                / primary_norm
            )
        models[model_name] = {
            "gamma_cluster_hamiltonian_ev": hermitian_json(
                primary.gamma_hamiltonian_ev
            ),
            "gamma_cluster_splitting_ev": float(
                np.ptp(np.diag(primary.gamma_hamiltonian_ev).real)
            ),
            "source_cluster_alignment_unitary": {
                "real": alignment.real.tolist(),
                "imaginary": alignment.imag.tolist(),
            },
            "primary_window_inverse_angstrom": 0.01,
            "source_relative_aligned_quadratic_coefficient_frobenius_error": (
                coefficient_error
            ),
            "coefficient_window_relative_changes_from_primary": window_sensitivity,
            "windows": windows,
        }
    result: JsonObject = {
        "schema_version": 1,
        "status": "degeneracy-aware-nonsoc-valence-subspace-producer-checked-development-not-independently-verified",
        "method": {
            "cluster_band_indices_zero_based": [1, 2, 3],
            "sample_ray_count": len(rays()),
            "positive_radii_per_ray": 4,
            "fit_windows_inverse_angstrom": list(WINDOWS),
            "even_field": "average of transported +q and -q three-band represented Hamiltonians",
            "transport": "polar unitary of the Gamma-cluster to displaced-cluster overlap",
            "quadratic_form": "H_eff(q)=H_eff(0)+q_x^2 B_xx+q_y^2 B_yy+q_z^2 B_zz+2q_xq_y B_xy+2q_xq_z B_xz+2q_yq_z B_yz",
            "directional_channels": "eigenvalues of twice the direction-contracted quadratic coefficient matrix",
            "claim_boundary": "degeneracy-aware non-SOC multiband curvature channels, not physical SOC HH/LH/split-off masses or individual-band Hessians",
        },
        "models": models,
        "execution": {
            "elapsed_seconds": float(time.perf_counter() - start),
            "producer_path": str(Path(__file__)),
            "output_path": str(OUTPUT),
            "calculator_invocations": 0,
        },
        "limitations": [
            "Curvature-channel eigenvalues describe the fitted three-band quadratic operator; when truncation splits H_eff(0), they are not Hessians of independently nondegenerate branches.",
            "The source itself is scalar-relativistic and non-SOC, so standard physical HH, LH, and split-off labels are not assigned.",
            "Polar transport controls basis freedom but does not make the candidate and source cluster subspaces identical; principal-angle evidence remains separate.",
            "No DFT, Wannier90, refitting, independent reconstruction, or experimental validation was performed."
        ],
    }
    OUTPUT.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
