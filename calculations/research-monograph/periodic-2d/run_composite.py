#!/usr/bin/env python3
"""Run the direct composite-band gauge and localization comparison."""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
from dataclasses import dataclass
from itertools import permutations
from pathlib import Path
from typing import cast

import numpy as np
import numpy.typing as npt

type JsonValue = (
    None | bool | int | float | str | list[JsonValue] | dict[str, JsonValue]
)
type RealVector = npt.NDArray[np.float64]
type ComplexVector = npt.NDArray[np.complex128]
type ComplexMatrix = npt.NDArray[np.complex128]
type ComplexFrames = npt.NDArray[np.complex128]


@dataclass(frozen=True, slots=True)
class CompositeInput:
    """Frozen controls for the lowest-three-band composite experiment."""

    experiment_id: str
    period: float
    lambda_x: float
    lambda_y: float
    lambda_xy: float
    cutoff: int
    mesh_size: int
    retained_bands: tuple[int, ...]
    center: tuple[float, float]
    momentum_width: float
    characters: tuple[str, ...]
    shell_radii: tuple[int, ...]
    fft_size: int
    minimum_projection_singular_value: float
    minimum_neighbor_singular_value: float
    chern_integer_defect: float

    def __post_init__(self) -> None:
        if not self.experiment_id:
            raise ValueError("experiment_id must be nonempty")
        if self.retained_bands != tuple(range(len(self.retained_bands))):
            raise ValueError("retained bands must be the contiguous lowest group")
        if len(self.retained_bands) != len(self.characters):
            raise ValueError("trial character count must equal retained rank")
        if self.characters != ("s", "px", "py"):
            raise ValueError("the version-1 trial characters must be s, px, py")
        if self.cutoff < 1 or self.mesh_size < 5 or self.mesh_size % 2 == 0:
            raise ValueError("cutoff and odd mesh must be valid")
        if self.fft_size <= 2 * (self.cutoff * self.mesh_size + self.mesh_size // 2):
            raise ValueError("localization FFT aliases retained global Fourier modes")
        if tuple(sorted(set(self.shell_radii))) != self.shell_radii:
            raise ValueError("shell radii must be strictly increasing")
        half = self.mesh_size // 2
        if self.shell_radii[-1] != 2 * half * half:
            raise ValueError("final shell must contain every representative")
        for value in (
            self.period,
            self.momentum_width,
            self.minimum_projection_singular_value,
            self.minimum_neighbor_singular_value,
            self.chern_integer_defect,
        ):
            if not np.isfinite(value) or value <= 0.0:
                raise ValueError("positive controls must be finite")


class CompositeInputDeserializer:
    """Deserialize the closed composite input record."""

    __slots__ = ()

    def execute(self, payload: bytes) -> CompositeInput:
        root = self._mapping(cast(JsonValue, json.loads(payload.decode("utf-8"))))
        if self._integer(root["schema_version"]) != 1:
            raise ValueError("unsupported input schema version")
        if root["evidence_status"] != "illustrative numerical experiment":
            raise ValueError("unexpected evidence status")
        convention = self._mapping(root["dimensionless_convention"])
        potential = self._mapping(root["potential"])
        trials = self._mapping(root["trial_orbitals"])
        center_values = self._reals(trials["center_fractional"])
        if len(center_values) != 2:
            raise ValueError("trial center must have two coordinates")
        characters_value = trials["characters"]
        if not isinstance(characters_value, list):
            raise TypeError("characters must be an array")
        characters = tuple(self._string(value) for value in characters_value)
        return CompositeInput(
            experiment_id=self._string(root["experiment_id"]),
            period=self._real(convention["lattice_period"]),
            lambda_x=self._real(potential["lambda_x"]),
            lambda_y=self._real(potential["lambda_y"]),
            lambda_xy=self._real(potential["lambda_xy"]),
            cutoff=self._integer(root["plane_wave_cutoff"]),
            mesh_size=self._integer(root["reciprocal_mesh_size"]),
            retained_bands=self._integers(root["retained_band_indices"]),
            center=(center_values[0], center_values[1]),
            momentum_width=self._real(trials["momentum_width"]),
            characters=characters,
            shell_radii=self._integers(root["hopping_shell_squared_radii"]),
            fft_size=self._integer(root["localization_fft_size"]),
            minimum_projection_singular_value=self._real(
                root["minimum_projection_singular_value"]
            ),
            minimum_neighbor_singular_value=self._real(
                root["minimum_neighbor_singular_value"]
            ),
            chern_integer_defect=self._real(root["chern_integer_defect"]),
        )

    @staticmethod
    def _mapping(value: JsonValue) -> dict[str, JsonValue]:
        if not isinstance(value, dict):
            raise TypeError("value must be an object")
        return value

    @staticmethod
    def _string(value: JsonValue) -> str:
        if not isinstance(value, str) or not value:
            raise TypeError("value must be a nonempty string")
        return value

    @staticmethod
    def _real(value: JsonValue) -> float:
        if isinstance(value, bool) or not isinstance(value, int | float):
            raise TypeError("value must be a number")
        result = float(value)
        if not np.isfinite(result):
            raise ValueError("value must be finite")
        return result

    @staticmethod
    def _integer(value: JsonValue) -> int:
        if isinstance(value, bool) or not isinstance(value, int):
            raise TypeError("value must be an integer")
        return value

    def _reals(self, value: JsonValue) -> tuple[float, ...]:
        if not isinstance(value, list):
            raise TypeError("value must be an array")
        return tuple(self._real(item) for item in value)

    def _integers(self, value: JsonValue) -> tuple[int, ...]:
        if not isinstance(value, list):
            raise TypeError("value must be an array")
        return tuple(self._integer(item) for item in value)


class CompositeExperiment:
    """Construct smooth and attacked composite frames and their reductions."""

    __slots__ = ()

    def execute(
        self, source: CompositeInput, input_path: Path, script_path: Path
    ) -> bytes:
        mesh = self._mesh(source.mesh_size)
        rank = len(source.retained_bands)
        dimension = (2 * source.cutoff + 1) ** 2
        raw_frames = np.empty(
            (source.mesh_size, source.mesh_size, dimension, rank), complex
        )
        smooth_frames = np.empty_like(raw_frames)
        values = np.empty((source.mesh_size, source.mesh_size, rank), float)
        smooth_hamiltonians = np.empty(
            (source.mesh_size, source.mesh_size, rank, rank), complex
        )
        projection_minimum = np.inf
        gap_minimum = np.inf
        projector_defect = 0.0
        for ix, kx in enumerate(mesh):
            for iy, ky in enumerate(mesh):
                operator = self._plane_wave(source, float(kx), float(ky))
                spectrum, vectors = np.linalg.eigh(operator)
                raw = vectors[:, :rank]
                trials = self._trial_frame(source, float(kx), float(ky))
                overlap = raw.conj().T @ trials
                left, singular, right_h = np.linalg.svd(overlap, full_matrices=False)
                projection_minimum = min(projection_minimum, float(singular[-1]))
                smooth = raw @ left @ right_h
                raw_frames[ix, iy] = raw
                smooth_frames[ix, iy] = smooth
                values[ix, iy] = spectrum[:rank]
                smooth_hamiltonians[ix, iy] = smooth.conj().T @ operator @ smooth
                gap_minimum = min(
                    gap_minimum, float(spectrum[rank] - spectrum[rank - 1])
                )
                projector_defect = max(
                    projector_defect,
                    float(
                        np.linalg.norm(raw @ raw.conj().T - smooth @ smooth.conj().T)
                    ),
                )
        if projection_minimum < source.minimum_projection_singular_value:
            raise RuntimeError("PERIODIC_2D.COMPOSITE_PROJECTION_RANK_LOSS")

        attacked_frames = np.empty_like(smooth_frames)
        attacked_hamiltonians = np.empty_like(smooth_hamiltonians)
        for ix in range(source.mesh_size):
            for iy in range(source.mesh_size):
                attack = self._attack(ix, iy, source.mesh_size)
                attacked_frames[ix, iy] = smooth_frames[ix, iy] @ attack
                attacked_hamiltonians[ix, iy] = (
                    attack.conj().T @ smooth_hamiltonians[ix, iy] @ attack
                )

        smooth_topology = self._topology(smooth_frames, source.cutoff)
        attacked_topology = self._topology(attacked_frames, source.cutoff)
        if (
            smooth_topology["minimum_neighbor_singular_value"]
            < source.minimum_neighbor_singular_value
        ):
            raise RuntimeError("PERIODIC_2D.COMPOSITE_NEIGHBOR_RANK_LOSS")
        if (
            abs(
                smooth_topology["chern_number"] - round(smooth_topology["chern_number"])
            )
            > source.chern_integer_defect
        ):
            raise RuntimeError("PERIODIC_2D.COMPOSITE_CHERN_NOT_QUANTIZED")

        smooth_reduction = self._reduction(source, mesh, smooth_hamiltonians)
        attacked_reduction = self._reduction(source, mesh, attacked_hamiltonians)
        smooth_localization = self._localization(source, mesh, smooth_frames)
        attacked_localization = self._localization(source, mesh, attacked_frames)
        maximum_wilson_defect = self._wilson_defect(
            smooth_topology["wilson_x_phases"],
            attacked_topology["wilson_x_phases"],
        )
        maximum_wilson_defect = max(
            maximum_wilson_defect,
            self._wilson_defect(
                smooth_topology["wilson_y_phases"],
                attacked_topology["wilson_y_phases"],
            ),
        )
        repository_root = script_path.parents[3]
        result: dict[str, JsonValue] = {
            "schema_version": 1,
            "experiment_id": source.experiment_id,
            "evidence_status": "illustrative numerical experiment",
            "calculation_status": "calculated illustrative result",
            "represented_space": {
                "dimension": dimension,
                "basis_order": "p outer, q inner, each increasing",
                "units": "E_G=1, G=1, a=2*pi",
                "geometry": "square primitive cell with Bloch boundary sewing",
                "energy_reference": "common parent Hamiltonian zero",
                "spin_convention": "spinless scalar",
                "retained_rank": rank,
                "retained_bands": list(source.retained_bands),
            },
            "parent": {
                "minimum_composite_to_exterior_gap": gap_minimum,
                "minimum_projection_singular_value": projection_minimum,
                "maximum_raw_smooth_projector_frobenius_defect": projector_defect,
                "mesh_energies": values.tolist(),
            },
            "smooth_projected_gauge": {
                "topology": self._topology_json(smooth_topology),
                "localization": smooth_localization,
                "reduction": smooth_reduction,
            },
            "controlled_rough_gauge": {
                "attack": (
                    "deterministic momentum-dependent real orthogonal rotations "
                    "within the retained rank-three subspace"
                ),
                "topology": self._topology_json(attacked_topology),
                "localization": attacked_localization,
                "reduction": attacked_reduction,
            },
            "gauge_invariant_comparison": {
                "chern_difference": abs(
                    smooth_topology["chern_number"] - attacked_topology["chern_number"]
                ),
                "maximum_wilson_eigenphase_set_defect": maximum_wilson_defect,
                "maximum_mesh_spectrum_defect": self._spectrum_defect(
                    smooth_hamiltonians, attacked_hamiltonians
                ),
                "smooth_to_rough_total_spread_ratio": (
                    sum(item["spread_cell_squared"] for item in smooth_localization)
                    / sum(item["spread_cell_squared"] for item in attacked_localization)
                ),
            },
            "structured_stops": {
                "projection_rank_loss": "PERIODIC_2D.COMPOSITE_PROJECTION_RANK_LOSS",
                "neighbor_rank_loss": "PERIODIC_2D.COMPOSITE_NEIGHBOR_RANK_LOSS",
                "chern_not_quantized": "PERIODIC_2D.COMPOSITE_CHERN_NOT_QUANTIZED",
            },
            "provenance": {
                "input_path": input_path.relative_to(repository_root).as_posix(),
                "input_sha256": hashlib.sha256(input_path.read_bytes()).hexdigest(),
                "script_path": script_path.relative_to(repository_root).as_posix(),
                "script_sha256": hashlib.sha256(script_path.read_bytes()).hexdigest(),
                "python_version": platform.python_version(),
                "numpy_version": np.__version__,
                "floating_point": "IEEE-754 binary64",
            },
            "limitations": [
                (
                    "The retained rank-three group is isolated only for the frozen "
                    "lambda_xy=0.15 case and declared finite representation."
                ),
                (
                    "The projection gauge uses declared synthetic s, px, and py "
                    "trial functions rather than material orbitals."
                ),
                (
                    "Finite-supercell density moments are localization diagnostics, "
                    "not an infinite-mesh localization theorem."
                ),
                (
                    "Wannier90 comparison and a topologically obstructed model remain "
                    "separate extensions."
                ),
            ],
        }
        return (json.dumps(result, indent=2, sort_keys=True) + "\n").encode()

    def _reduction(
        self,
        source: CompositeInput,
        mesh: RealVector,
        hamiltonians: npt.NDArray[np.complex128],
    ) -> dict[str, JsonValue]:
        reps = self._representatives(source.mesh_size)
        points = tuple((float(kx), float(ky)) for kx in mesh for ky in mesh)
        rank = hamiltonians.shape[-1]
        flat = hamiltonians.reshape(len(points), rank * rank)
        inverse = np.exp(
            -2j
            * np.pi
            * np.asarray([[kx * rx + ky * ry for kx, ky in points] for rx, ry in reps])
        )
        coefficients = (inverse @ flat / len(points)).reshape(len(reps), rank, rank)
        design = np.exp(
            2j
            * np.pi
            * np.asarray([[kx * rx + ky * ry for rx, ry in reps] for kx, ky in points])
        )
        reconstruction = (design @ coefficients.reshape(len(reps), -1)).reshape(
            hamiltonians.shape
        )
        hermiticity = 0.0
        coefficient_lookup = {rep: index for index, rep in enumerate(reps)}
        for index, (rx, ry) in enumerate(reps):
            opposite = coefficient_lookup[(-rx, -ry)]
            hermiticity = max(
                hermiticity,
                float(
                    np.linalg.norm(
                        coefficients[index] - coefficients[opposite].conj().T
                    )
                ),
            )
        shells: list[JsonValue] = []
        for radius in source.shell_radii:
            retained = np.asarray([rx * rx + ry * ry <= radius for rx, ry in reps])
            retained_design = design[:, retained]
            mediated = (
                retained_design
                @ coefficients[retained].reshape(int(np.sum(retained)), -1)
            ).reshape(hamiltonians.shape)
            direct = np.linalg.lstsq(retained_design, flat, rcond=None)[0]
            residual = hamiltonians - mediated
            omitted = float(np.linalg.norm(coefficients[~retained]))
            shells.append(
                {
                    "maximum_squared_radius": radius,
                    "retained_block_count": int(np.sum(retained)),
                    "omitted_block_frobenius_l2_norm": omitted,
                    "mesh_operator_root_mean_square_frobenius_error": float(
                        np.sqrt(
                            np.mean(np.square(np.linalg.norm(residual, axis=(-2, -1))))
                        )
                    ),
                    "mesh_operator_maximum_frobenius_error": float(
                        np.max(np.linalg.norm(residual, axis=(-2, -1)))
                    ),
                    "direct_mediated_coefficient_frobenius_defect": float(
                        np.linalg.norm(
                            direct
                            - coefficients[retained].reshape(int(np.sum(retained)), -1)
                        )
                    ),
                    "parseval_absolute_residual": abs(
                        float(np.sum(np.square(np.abs(residual))))
                        - len(points) * omitted * omitted
                    ),
                }
            )
        return {
            "hopping_blocks": [
                {
                    "rx": rx,
                    "ry": ry,
                    "matrix": self._complex_matrix(coefficients[index]),
                    "frobenius_norm": float(np.linalg.norm(coefficients[index])),
                }
                for index, (rx, ry) in enumerate(reps)
            ],
            "shell_study": shells,
            "full_mesh_reconstruction_maximum_frobenius_error": float(
                np.max(np.linalg.norm(reconstruction - hamiltonians, axis=(-2, -1)))
            ),
            "hopping_hermiticity_maximum_frobenius_defect": hermiticity,
        }

    def _localization(
        self, source: CompositeInput, mesh: RealVector, frames: ComplexFrames
    ) -> list[JsonValue]:
        rank = frames.shape[-1]
        side = 2 * source.cutoff + 1
        half = source.mesh_size // 2
        k_indices = range(-half, half + 1)
        period_cells = source.mesh_size
        records: list[JsonValue] = []
        for orbital in range(rank):
            coefficients = np.zeros((source.fft_size, source.fft_size), complex)
            for ix, sx in enumerate(k_indices):
                for iy, sy in enumerate(k_indices):
                    frame = frames[ix, iy, :, orbital].reshape(side, side)
                    for ip, p in enumerate(range(-source.cutoff, source.cutoff + 1)):
                        for iq, q in enumerate(
                            range(-source.cutoff, source.cutoff + 1)
                        ):
                            mx = p * source.mesh_size + sx
                            my = q * source.mesh_size + sy
                            coefficients[
                                mx % source.fft_size, my % source.fft_size
                            ] += frame[ip, iq] / source.mesh_size
            coefficient_norm = float(np.sum(np.square(np.abs(coefficients))))
            wave = np.fft.ifft2(coefficients) * source.fft_size**2
            probability = np.square(np.abs(wave))
            probability /= np.sum(probability)
            coordinate = (
                np.arange(source.fft_size, dtype=float) * period_cells / source.fft_size
            )
            marginal_x = np.sum(probability, axis=1)
            marginal_y = np.sum(probability, axis=0)
            center_x = self._circular_center(marginal_x, coordinate, period_cells)
            center_y = self._circular_center(marginal_y, coordinate, period_cells)
            dx = (coordinate - center_x + period_cells / 2.0) % period_cells
            dx -= period_cells / 2.0
            dy = (coordinate - center_y + period_cells / 2.0) % period_cells
            dy -= period_cells / 2.0
            spread = float(np.sum(probability * (dx[:, None] ** 2 + dy[None, :] ** 2)))
            digest_values = np.round(probability, 12).astype("<f8", copy=False)
            records.append(
                {
                    "orbital": orbital,
                    "coefficient_norm": coefficient_norm,
                    "center_cells": [center_x, center_y],
                    "spread_cell_squared": spread,
                    "density_content_sha256": hashlib.sha256(
                        digest_values.tobytes(order="C")
                    ).hexdigest(),
                }
            )
        return records

    def _topology(
        self, frames: ComplexFrames, cutoff: int
    ) -> dict[str, float | list[list[float]]]:
        size = frames.shape[0]
        rank = frames.shape[-1]
        links_x = np.empty((size, size, rank, rank), complex)
        links_y = np.empty_like(links_x)
        minimum = np.inf
        for ix in range(size):
            for iy in range(size):
                right = (
                    frames[ix + 1, iy]
                    if ix + 1 < size
                    else self._sew(frames[0, iy], cutoff, 1, 0)
                )
                up = (
                    frames[ix, iy + 1]
                    if iy + 1 < size
                    else self._sew(frames[ix, 0], cutoff, 0, 1)
                )
                for target, store in ((right, links_x), (up, links_y)):
                    overlap = frames[ix, iy].conj().T @ target
                    left, singular, right_h = np.linalg.svd(overlap)
                    minimum = min(minimum, float(singular[-1]))
                    store[ix, iy] = left @ right_h
        plaquette_phases = np.empty((size, size), float)
        for ix in range(size):
            for iy in range(size):
                loop = (
                    links_x[ix, iy]
                    @ links_y[(ix + 1) % size, iy]
                    @ links_x[ix, (iy + 1) % size].conj().T
                    @ links_y[ix, iy].conj().T
                )
                plaquette_phases[ix, iy] = np.angle(np.linalg.det(loop))
        wilson_x: list[list[float]] = []
        wilson_y: list[list[float]] = []
        for iy in range(size):
            loop = np.eye(rank, dtype=complex)
            for ix in range(size):
                loop = loop @ links_x[ix, iy]
            wilson_x.append(
                sorted(float(value) for value in np.angle(np.linalg.eigvals(loop)))
            )
        for ix in range(size):
            loop = np.eye(rank, dtype=complex)
            for iy in range(size):
                loop = loop @ links_y[ix, iy]
            wilson_y.append(
                sorted(float(value) for value in np.angle(np.linalg.eigvals(loop)))
            )
        return {
            "minimum_neighbor_singular_value": minimum,
            "chern_number": float(np.sum(plaquette_phases) / (2.0 * np.pi)),
            "maximum_absolute_determinant_plaquette_phase": float(
                np.max(np.abs(plaquette_phases))
            ),
            "wilson_x_phases": wilson_x,
            "wilson_y_phases": wilson_y,
        }

    @staticmethod
    def _topology_json(
        topology: dict[str, float | list[list[float]]],
    ) -> dict[str, JsonValue]:
        return {
            "minimum_neighbor_singular_value": cast(
                float, topology["minimum_neighbor_singular_value"]
            ),
            "chern_number": cast(float, topology["chern_number"]),
            "maximum_absolute_determinant_plaquette_phase": cast(
                float, topology["maximum_absolute_determinant_plaquette_phase"]
            ),
            "wilson_x_phases": cast(list[JsonValue], topology["wilson_x_phases"]),
            "wilson_y_phases": cast(list[JsonValue], topology["wilson_y_phases"]),
        }

    @staticmethod
    def _wilson_defect(
        first_value: float | list[list[float]],
        second_value: float | list[list[float]],
    ) -> float:
        if not isinstance(first_value, list) or not isinstance(second_value, list):
            raise TypeError("Wilson values must be nested arrays")
        maximum = 0.0
        for first, second in zip(first_value, second_value, strict=True):
            first_array = np.asarray(first)
            second_array = np.asarray(second)
            loop_minimum = np.inf
            for permutation in permutations(range(len(second))):
                difference = np.angle(
                    np.exp(
                        1j
                        * (
                            first_array
                            - second_array[np.asarray(permutation, dtype=np.int64)]
                        )
                    )
                )
                loop_minimum = min(loop_minimum, float(np.max(np.abs(difference))))
            maximum = max(maximum, loop_minimum)
        return maximum

    @staticmethod
    def _spectrum_defect(
        first: npt.NDArray[np.complex128], second: npt.NDArray[np.complex128]
    ) -> float:
        return float(
            np.max(np.abs(np.linalg.eigvalsh(first) - np.linalg.eigvalsh(second)))
        )

    @staticmethod
    def _circular_center(
        probability: RealVector, coordinate: RealVector, period: float
    ) -> float:
        phase = np.sum(probability * np.exp(2j * np.pi * coordinate / period))
        return float((np.angle(phase) % (2.0 * np.pi)) * period / (2.0 * np.pi))

    @staticmethod
    def _attack(ix: int, iy: int, size: int) -> ComplexMatrix:
        x_angle = 1.7 * np.sin(2.0 * np.pi * (3 * ix + iy) / size)
        y_angle = 1.3 * np.cos(2.0 * np.pi * (ix + 4 * iy) / size)
        first = np.asarray(
            [
                [np.cos(x_angle), -np.sin(x_angle), 0.0],
                [np.sin(x_angle), np.cos(x_angle), 0.0],
                [0.0, 0.0, 1.0],
            ],
            complex,
        )
        second = np.asarray(
            [
                [1.0, 0.0, 0.0],
                [0.0, np.cos(y_angle), -np.sin(y_angle)],
                [0.0, np.sin(y_angle), np.cos(y_angle)],
            ],
            complex,
        )
        return first @ second

    @staticmethod
    def _trial_frame(source: CompositeInput, kx: float, ky: float) -> ComplexMatrix:
        vectors: list[ComplexVector] = []
        for character in source.characters:
            values: list[complex] = []
            for p in range(-source.cutoff, source.cutoff + 1):
                for q in range(-source.cutoff, source.cutoff + 1):
                    momentum_x = kx + p
                    momentum_y = ky + q
                    gaussian = np.exp(
                        -0.5
                        * source.momentum_width**2
                        * (momentum_x**2 + momentum_y**2)
                    )
                    center_phase = np.exp(
                        -2j
                        * np.pi
                        * (
                            source.center[0] * momentum_x
                            + source.center[1] * momentum_y
                        )
                    )
                    if character == "s":
                        factor = 1.0
                    elif character == "px":
                        factor = 1j * momentum_x
                    elif character == "py":
                        factor = 1j * momentum_y
                    else:
                        raise ValueError("unsupported trial character")
                    values.append(complex(factor * gaussian * center_phase))
            vector = np.asarray(values)
            vector /= np.linalg.norm(vector)
            vectors.append(vector)
        frame, _ = np.linalg.qr(np.column_stack(vectors))
        return frame

    @staticmethod
    def _plane_wave(source: CompositeInput, kx: float, ky: float) -> ComplexMatrix:
        indices = np.arange(-source.cutoff, source.cutoff + 1)
        p, q = np.meshgrid(indices, indices, indexing="ij")
        flat_p = p.ravel()
        flat_q = q.ravel()
        delta_p = flat_p[:, None] - flat_p[None, :]
        delta_q = flat_q[:, None] - flat_q[None, :]
        matrix = np.diag((kx + flat_p) ** 2 + (ky + flat_q) ** 2).astype(complex)
        matrix += (source.lambda_x / 2.0) * ((np.abs(delta_p) == 1) & (delta_q == 0))
        matrix += (source.lambda_y / 2.0) * ((delta_p == 0) & (np.abs(delta_q) == 1))
        matrix += (source.lambda_xy / 4.0) * (
            (np.abs(delta_p) == 1) & (np.abs(delta_q) == 1)
        )
        return matrix

    @staticmethod
    def _sew(
        frame: ComplexMatrix, cutoff: int, shift_x: int, shift_y: int
    ) -> ComplexMatrix:
        side = 2 * cutoff + 1
        rank = frame.shape[1]
        source = frame.reshape(side, side, rank)
        result = np.zeros_like(source)
        if shift_x == 1 and shift_y == 0:
            result[:-1, :, :] = source[1:, :, :]
        elif shift_x == 0 and shift_y == 1:
            result[:, :-1, :] = source[:, 1:, :]
        else:
            raise ValueError("only positive unit sewing is supported")
        return result.reshape(side * side, rank)

    @staticmethod
    def _complex_matrix(matrix: ComplexMatrix) -> list[list[list[float]]]:
        return [
            [[float(value.real), float(value.imag)] for value in row] for row in matrix
        ]

    @staticmethod
    def _mesh(size: int) -> RealVector:
        half = size // 2
        return np.arange(-half, half + 1, dtype=float) / size

    @staticmethod
    def _representatives(size: int) -> tuple[tuple[int, int], ...]:
        half = size // 2
        return tuple(
            (rx, ry) for rx in range(-half, half + 1) for ry in range(-half, half + 1)
        )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    arguments = parser.parse_args()
    source = CompositeInputDeserializer().execute(arguments.input.read_bytes())
    output = CompositeExperiment().execute(
        source, arguments.input.resolve(), Path(__file__).resolve()
    )
    arguments.output.write_bytes(output)


if __name__ == "__main__":
    main()
