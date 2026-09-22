#!/usr/bin/env python3
"""Independently verify the periodic-2D composite-band result."""

from __future__ import annotations

import argparse
import hashlib
import json
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


class CompositeResultVerifier:
    """Reconstruct the composite parent, gauges, topology, and localization."""

    __slots__ = ()

    def execute(self, result_path: Path, repository_root: Path) -> None:
        result = self._mapping(
            cast(JsonValue, json.loads(result_path.read_text())), "result"
        )
        provenance = self._mapping(result["provenance"], "provenance")
        input_path = repository_root / self._string(provenance["input_path"])
        script_path = repository_root / self._string(provenance["script_path"])
        assert (
            hashlib.sha256(input_path.read_bytes()).hexdigest()
            == provenance["input_sha256"]
        )
        assert (
            hashlib.sha256(script_path.read_bytes()).hexdigest()
            == provenance["script_sha256"]
        )
        source = self._mapping(
            cast(JsonValue, json.loads(input_path.read_text())), "input"
        )
        potential = self._mapping(source["potential"], "potential")
        trials = self._mapping(source["trial_orbitals"], "trials")
        cutoff = self._integer(source["plane_wave_cutoff"])
        mesh_size = self._integer(source["reciprocal_mesh_size"])
        rank = len(self._integers(source["retained_band_indices"]))
        lx = self._real(potential["lambda_x"])
        ly = self._real(potential["lambda_y"])
        lxy = self._real(potential["lambda_xy"])
        center_values = self._reals(trials["center_fractional"])
        center = (center_values[0], center_values[1])
        width = self._real(trials["momentum_width"])
        fft_size = self._integer(source["localization_fft_size"])
        shell_radii = self._integers(source["hopping_shell_squared_radii"])
        mesh = self._mesh(mesh_size)
        dimension = (2 * cutoff + 1) ** 2
        raw = np.empty((mesh_size, mesh_size, dimension, rank), complex)
        smooth = np.empty_like(raw)
        hamiltonians = np.empty((mesh_size, mesh_size, rank, rank), complex)
        energies = np.empty((mesh_size, mesh_size, rank), float)
        minimum_projection = np.inf
        minimum_gap = np.inf
        projector_defect = 0.0
        for ix, kx in enumerate(mesh):
            for iy, ky in enumerate(mesh):
                operator = self._operator(float(kx), float(ky), cutoff, lx, ly, lxy)
                spectrum, vectors = np.linalg.eigh(operator)
                frame = vectors[:, :rank]
                trial = self._trials(float(kx), float(ky), cutoff, center, width)
                overlap = frame.conj().T @ trial
                singular = np.linalg.svd(overlap, compute_uv=False)
                gram = overlap.conj().T @ overlap
                gram_values, gram_vectors = np.linalg.eigh(gram)
                inverse_root = (
                    gram_vectors
                    @ np.diag(1.0 / np.sqrt(gram_values))
                    @ gram_vectors.conj().T
                )
                projected = frame @ overlap @ inverse_root
                raw[ix, iy] = frame
                smooth[ix, iy] = projected
                energies[ix, iy] = spectrum[:rank]
                hamiltonians[ix, iy] = projected.conj().T @ operator @ projected
                minimum_projection = min(minimum_projection, float(singular[-1]))
                minimum_gap = min(
                    minimum_gap, float(spectrum[rank] - spectrum[rank - 1])
                )
                projector_defect = max(
                    projector_defect,
                    float(
                        np.linalg.norm(
                            frame @ frame.conj().T - projected @ projected.conj().T
                        )
                    ),
                )
        parent = self._mapping(result["parent"], "parent")
        stored_energies = np.asarray(self._tensor_reals(parent["mesh_energies"]))
        np.testing.assert_allclose(stored_energies, energies, atol=2.0e-14)
        np.testing.assert_allclose(
            self._real(parent["minimum_composite_to_exterior_gap"]),
            minimum_gap,
            atol=2.0e-14,
        )
        np.testing.assert_allclose(
            self._real(parent["minimum_projection_singular_value"]),
            minimum_projection,
            atol=2.0e-14,
        )
        np.testing.assert_allclose(
            self._real(parent["maximum_raw_smooth_projector_frobenius_defect"]),
            projector_defect,
            atol=2.0e-14,
        )
        assert minimum_gap > 0.03
        assert minimum_projection > 0.88

        attacked = np.empty_like(smooth)
        attacked_hamiltonians = np.empty_like(hamiltonians)
        for ix in range(mesh_size):
            for iy in range(mesh_size):
                rotation = self._attack(ix, iy, mesh_size)
                attacked[ix, iy] = smooth[ix, iy] @ rotation
                attacked_hamiltonians[ix, iy] = (
                    rotation.conj().T @ hamiltonians[ix, iy] @ rotation
                )
        smooth_topology = self._topology(smooth, cutoff)
        attacked_topology = self._topology(attacked, cutoff)
        smooth_record = self._mapping(result["smooth_projected_gauge"], "smooth")
        rough_record = self._mapping(result["controlled_rough_gauge"], "rough")
        self._verify_topology(
            self._mapping(smooth_record["topology"], "smooth topology"),
            smooth_topology,
        )
        self._verify_topology(
            self._mapping(rough_record["topology"], "rough topology"),
            attacked_topology,
        )
        assert smooth_topology[0] > 0.78
        assert abs(smooth_topology[1]) < 1.0e-12

        smooth_hopping_defect = self._verify_reduction(
            self._mapping(smooth_record["reduction"], "smooth reduction"),
            hamiltonians,
            mesh,
            shell_radii,
        )
        rough_hopping_defect = self._verify_reduction(
            self._mapping(rough_record["reduction"], "rough reduction"),
            attacked_hamiltonians,
            mesh,
            shell_radii,
        )
        smooth_spreads = self._verify_localization(
            self._records(smooth_record["localization"]),
            smooth,
            cutoff,
            fft_size,
        )
        rough_spreads = self._verify_localization(
            self._records(rough_record["localization"]),
            attacked,
            cutoff,
            fft_size,
        )
        comparison = self._mapping(result["gauge_invariant_comparison"], "comparison")
        np.testing.assert_allclose(
            self._real(comparison["chern_difference"]),
            abs(smooth_topology[1] - attacked_topology[1]),
            atol=1.0e-15,
        )
        np.testing.assert_allclose(
            self._real(comparison["maximum_wilson_eigenphase_set_defect"]),
            max(
                self._wilson_defect(smooth_topology[2], attacked_topology[2]),
                self._wilson_defect(smooth_topology[3], attacked_topology[3]),
            ),
            atol=2.0e-14,
        )
        np.testing.assert_allclose(
            self._real(comparison["smooth_to_rough_total_spread_ratio"]),
            sum(smooth_spreads) / sum(rough_spreads),
            atol=2.0e-14,
        )
        assert smooth_record["reduction"] is not None
        assert rough_record["reduction"] is not None
        assert smooth_hopping_defect < 2.0e-14
        assert rough_hopping_defect < 2.0e-14
        print("periodic_2d_composite_verification=PASS")
        print(f"minimum_composite_gap={minimum_gap:.12e}")
        print(f"minimum_projection_singular_value={minimum_projection:.12e}")
        print(f"smooth_total_spread={sum(smooth_spreads):.12e}")
        print(f"rough_total_spread={sum(rough_spreads):.12e}")

    def _verify_reduction(
        self,
        record: dict[str, JsonValue],
        hamiltonians: npt.NDArray[np.complex128],
        mesh: RealVector,
        shell_radii: tuple[int, ...],
    ) -> float:
        reps = self._representatives(mesh.size)
        points = tuple((float(kx), float(ky)) for kx in mesh for ky in mesh)
        rank = hamiltonians.shape[-1]
        flat = hamiltonians.reshape(len(points), rank * rank)
        inverse = np.exp(
            -2j
            * np.pi
            * np.asarray([[kx * rx + ky * ry for kx, ky in points] for rx, ry in reps])
        )
        coefficients = (inverse @ flat / len(points)).reshape(len(reps), rank, rank)
        stored_blocks = self._records(record["hopping_blocks"])
        stored = np.asarray(
            [self._complex_matrix(item["matrix"]) for item in stored_blocks]
        )
        maximum_defect = float(np.max(np.abs(stored - coefficients)))
        design = np.exp(
            2j
            * np.pi
            * np.asarray([[kx * rx + ky * ry for rx, ry in reps] for kx, ky in points])
        )
        shell_records = self._records(record["shell_study"])
        for observed, radius in zip(shell_records, shell_radii, strict=True):
            retained = np.asarray([rx * rx + ry * ry <= radius for rx, ry in reps])
            mediated = (
                design[:, retained]
                @ coefficients[retained].reshape(int(np.sum(retained)), -1)
            ).reshape(hamiltonians.shape)
            residual = hamiltonians - mediated
            omitted = float(np.linalg.norm(coefficients[~retained]))
            np.testing.assert_allclose(
                self._real(observed["omitted_block_frobenius_l2_norm"]),
                omitted,
                atol=2.0e-14,
            )
            np.testing.assert_allclose(
                self._real(observed["mesh_operator_root_mean_square_frobenius_error"]),
                np.sqrt(np.mean(np.square(np.linalg.norm(residual, axis=(-2, -1))))),
                atol=2.0e-14,
            )
            direct = np.linalg.lstsq(design[:, retained], flat, rcond=None)[0]
            np.testing.assert_allclose(
                self._real(observed["direct_mediated_coefficient_frobenius_defect"]),
                np.linalg.norm(
                    direct - coefficients[retained].reshape(int(np.sum(retained)), -1)
                ),
                atol=2.0e-14,
            )
        assert (
            self._real(record["full_mesh_reconstruction_maximum_frobenius_error"])
            < 1.0e-13
        )
        return maximum_defect

    def _verify_localization(
        self,
        records: tuple[dict[str, JsonValue], ...],
        frames: ComplexFrames,
        cutoff: int,
        fft_size: int,
    ) -> list[float]:
        size = frames.shape[0]
        half = size // 2
        side = 2 * cutoff + 1
        spreads: list[float] = []
        for orbital, record in enumerate(records):
            coefficients = np.zeros((fft_size, fft_size), complex)
            for ix, sx in enumerate(range(-half, half + 1)):
                for iy, sy in enumerate(range(-half, half + 1)):
                    frame = frames[ix, iy, :, orbital].reshape(side, side)
                    for ip, p in enumerate(range(-cutoff, cutoff + 1)):
                        for iq, q in enumerate(range(-cutoff, cutoff + 1)):
                            coefficients[
                                (p * size + sx) % fft_size, (q * size + sy) % fft_size
                            ] += frame[ip, iq] / size
            coefficient_norm = float(np.sum(np.square(np.abs(coefficients))))
            wave = np.fft.ifft2(coefficients) * fft_size**2
            probability = np.square(np.abs(wave))
            probability /= np.sum(probability)
            coordinate = np.arange(fft_size, dtype=float) * size / fft_size
            marginal_x = np.sum(probability, axis=1)
            marginal_y = np.sum(probability, axis=0)
            center_x = self._center(marginal_x, coordinate, size)
            center_y = self._center(marginal_y, coordinate, size)
            dx = (coordinate - center_x + size / 2.0) % size - size / 2.0
            dy = (coordinate - center_y + size / 2.0) % size - size / 2.0
            spread = float(np.sum(probability * (dx[:, None] ** 2 + dy[None, :] ** 2)))
            digest = hashlib.sha256(
                np.round(probability, 12).astype("<f8", copy=False).tobytes(order="C")
            ).hexdigest()
            np.testing.assert_allclose(
                self._real(record["coefficient_norm"]), coefficient_norm, atol=2.0e-14
            )
            np.testing.assert_allclose(
                self._real(record["spread_cell_squared"]), spread, atol=2.0e-13
            )
            assert record["density_content_sha256"] == digest
            spreads.append(spread)
        return spreads

    def _topology(
        self, frames: ComplexFrames, cutoff: int
    ) -> tuple[float, float, list[list[float]], list[list[float]], float]:
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
                    else self._sew(frames[0, iy], cutoff, True)
                )
                up = (
                    frames[ix, iy + 1]
                    if iy + 1 < size
                    else self._sew(frames[ix, 0], cutoff, False)
                )
                for target, links in ((right, links_x), (up, links_y)):
                    overlap = frames[ix, iy].conj().T @ target
                    left, singular, right_h = np.linalg.svd(overlap)
                    minimum = min(minimum, float(singular[-1]))
                    links[ix, iy] = left @ right_h
        phases: list[float] = []
        for ix in range(size):
            for iy in range(size):
                loop = (
                    links_x[ix, iy]
                    @ links_y[(ix + 1) % size, iy]
                    @ links_x[ix, (iy + 1) % size].conj().T
                    @ links_y[ix, iy].conj().T
                )
                phases.append(float(np.angle(np.linalg.det(loop))))
        wilson_x: list[list[float]] = []
        wilson_y: list[list[float]] = []
        for iy in range(size):
            product = np.eye(rank, dtype=complex)
            for ix in range(size):
                product = product @ links_x[ix, iy]
            wilson_x.append(
                sorted(float(value) for value in np.angle(np.linalg.eigvals(product)))
            )
        for ix in range(size):
            product = np.eye(rank, dtype=complex)
            for iy in range(size):
                product = product @ links_y[ix, iy]
            wilson_y.append(
                sorted(float(value) for value in np.angle(np.linalg.eigvals(product)))
            )
        return (
            minimum,
            float(sum(phases) / (2.0 * np.pi)),
            wilson_x,
            wilson_y,
            max(abs(value) for value in phases),
        )

    def _verify_topology(
        self,
        record: dict[str, JsonValue],
        topology: tuple[float, float, list[list[float]], list[list[float]], float],
    ) -> None:
        np.testing.assert_allclose(
            self._real(record["minimum_neighbor_singular_value"]),
            topology[0],
            atol=2.0e-14,
        )
        np.testing.assert_allclose(
            self._real(record["chern_number"]), topology[1], atol=2.0e-14
        )
        np.testing.assert_allclose(
            self._real(record["maximum_absolute_determinant_plaquette_phase"]),
            topology[4],
            atol=2.0e-14,
        )

    @staticmethod
    def _wilson_defect(first: list[list[float]], second: list[list[float]]) -> float:
        maximum = 0.0
        for left, right in zip(first, second, strict=True):
            minimum = np.inf
            for order in permutations(range(len(right))):
                defect = np.max(
                    np.abs(
                        np.angle(
                            np.exp(
                                1j
                                * (
                                    np.asarray(left)
                                    - np.asarray(right)[np.asarray(order)]
                                )
                            )
                        )
                    )
                )
                minimum = min(minimum, float(defect))
            maximum = max(maximum, minimum)
        return maximum

    @staticmethod
    def _operator(
        kx: float,
        ky: float,
        cutoff: int,
        lx: float,
        ly: float,
        lxy: float,
    ) -> ComplexMatrix:
        pairs = tuple(
            (p, q)
            for p in range(-cutoff, cutoff + 1)
            for q in range(-cutoff, cutoff + 1)
        )
        lookup = {pair: index for index, pair in enumerate(pairs)}
        matrix = np.zeros((len(pairs), len(pairs)), complex)
        for row, (p, q) in enumerate(pairs):
            matrix[row, row] = (kx + p) ** 2 + (ky + q) ** 2
            for dp, dq, value in (
                (1, 0, lx / 2.0),
                (-1, 0, lx / 2.0),
                (0, 1, ly / 2.0),
                (0, -1, ly / 2.0),
                (1, 1, lxy / 4.0),
                (1, -1, lxy / 4.0),
                (-1, 1, lxy / 4.0),
                (-1, -1, lxy / 4.0),
            ):
                column = lookup.get((p + dp, q + dq))
                if column is not None:
                    matrix[row, column] += value
        return matrix

    @staticmethod
    def _trials(
        kx: float,
        ky: float,
        cutoff: int,
        center: tuple[float, float],
        width: float,
    ) -> ComplexMatrix:
        columns: list[ComplexVector] = []
        for character in range(3):
            values: list[complex] = []
            for p in range(-cutoff, cutoff + 1):
                for q in range(-cutoff, cutoff + 1):
                    x = kx + p
                    y = ky + q
                    base = np.exp(-0.5 * width**2 * (x**2 + y**2))
                    phase = np.exp(-2j * np.pi * (center[0] * x + center[1] * y))
                    factor = (
                        1.0 if character == 0 else 1j * (x if character == 1 else y)
                    )
                    values.append(complex(factor * base * phase))
            vector = np.asarray(values)
            vector /= np.linalg.norm(vector)
            columns.append(vector)
        return np.linalg.qr(np.column_stack(columns))[0]

    @staticmethod
    def _attack(ix: int, iy: int, size: int) -> ComplexMatrix:
        a = 1.7 * np.sin(2.0 * np.pi * (3 * ix + iy) / size)
        b = 1.3 * np.cos(2.0 * np.pi * (ix + 4 * iy) / size)
        first = np.asarray(
            [
                [np.cos(a), -np.sin(a), 0.0],
                [np.sin(a), np.cos(a), 0.0],
                [0.0, 0.0, 1.0],
            ],
            complex,
        )
        second = np.asarray(
            [
                [1.0, 0.0, 0.0],
                [0.0, np.cos(b), -np.sin(b)],
                [0.0, np.sin(b), np.cos(b)],
            ],
            complex,
        )
        return first @ second

    @staticmethod
    def _sew(frame: ComplexMatrix, cutoff: int, x_direction: bool) -> ComplexMatrix:
        side = 2 * cutoff + 1
        source = frame.reshape(side, side, frame.shape[1])
        result = np.zeros_like(source)
        if x_direction:
            result[:-1] = source[1:]
        else:
            result[:, :-1] = source[:, 1:]
        return result.reshape(frame.shape)

    @staticmethod
    def _center(
        probability: RealVector, coordinate: RealVector, period: float
    ) -> float:
        phase = np.sum(probability * np.exp(2j * np.pi * coordinate / period))
        return float(np.angle(phase) % (2.0 * np.pi) * period / (2.0 * np.pi))

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

    @staticmethod
    def _mapping(value: JsonValue, name: str) -> dict[str, JsonValue]:
        if not isinstance(value, dict):
            raise TypeError(f"{name} must be an object")
        return value

    def _records(self, value: JsonValue) -> tuple[dict[str, JsonValue], ...]:
        if not isinstance(value, list):
            raise TypeError("value must be an array")
        return tuple(self._mapping(item, "record") for item in value)

    @staticmethod
    def _string(value: JsonValue) -> str:
        if not isinstance(value, str) or not value:
            raise TypeError("value must be a nonempty string")
        return value

    @staticmethod
    def _real(value: JsonValue) -> float:
        if isinstance(value, bool) or not isinstance(value, int | float):
            raise TypeError("value must be numeric")
        return float(value)

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

    def _tensor_reals(self, value: JsonValue) -> list[list[list[float]]]:
        if not isinstance(value, list):
            raise TypeError("tensor must be an array")
        result: list[list[list[float]]] = []
        for matrix in value:
            if not isinstance(matrix, list):
                raise TypeError("tensor matrix must be an array")
            rows: list[list[float]] = []
            for row in matrix:
                if not isinstance(row, list):
                    raise TypeError("tensor row must be an array")
                rows.append([self._real(item) for item in row])
            result.append(rows)
        return result

    def _complex_matrix(self, value: JsonValue) -> ComplexMatrix:
        if not isinstance(value, list):
            raise TypeError("complex matrix must be an array")
        rows: list[list[complex]] = []
        for row in value:
            if not isinstance(row, list):
                raise TypeError("complex matrix row must be an array")
            values: list[complex] = []
            for item in row:
                if not isinstance(item, list) or len(item) != 2:
                    raise TypeError("complex value must be a pair")
                values.append(complex(self._real(item[0]), self._real(item[1])))
            rows.append(values)
        return np.asarray(rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("result", type=Path)
    arguments = parser.parse_args()
    repository_root = Path(__file__).resolve().parents[3]
    CompositeResultVerifier().execute(arguments.result.resolve(), repository_root)


if __name__ == "__main__":
    main()
