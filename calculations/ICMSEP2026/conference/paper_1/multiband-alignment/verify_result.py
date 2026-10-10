#!/usr/bin/env python3
"""Independently reconstruct and verify the retained M2 JSON result."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Never

import numpy as np
from scipy.linalg import schur  # type: ignore[import-untyped]

ROOT = Path(__file__).resolve().parent


def fail(message: str) -> Never:
    """Reject malformed retained evidence."""
    raise ValueError(message)


def mapping(value: object, context: str) -> dict[str, object]:
    """Require a JSON object."""
    if type(value) is not dict:
        fail(f"{context} must be an object")
    return value


def exact_keys(value: dict[str, object], expected: set[str], context: str) -> None:
    """Fail closed on missing or unknown fields."""
    if set(value) != expected:
        fail(f"{context} fields must be exactly {sorted(expected)}")


def array(value: object, context: str) -> list[object]:
    """Require a JSON array."""
    if type(value) is not list:
        fail(f"{context} must be an array")
    return value


def integer(value: object, context: str) -> int:
    """Require a built-in integer."""
    if type(value) is not int:
        fail(f"{context} must be an integer")
    return value


def number(value: object, context: str) -> float:
    """Require a finite built-in JSON number and reject booleans."""
    if type(value) not in (int, float):
        fail(f"{context} must be numeric")
    result = float(value)
    if not np.isfinite(result):
        fail(f"{context} must be finite")
    return result


def quantity(value: object, context: str) -> float:
    """Decode a scalar quantity with a dimensionless spelling."""
    payload = mapping(value, context)
    exact_keys(payload, {"magnitude", "unit"}, context)
    if payload["unit"] not in ("1", "dimensionless"):
        fail(f"{context}.unit must be dimensionless")
    return number(payload["magnitude"], f"{context}.magnitude")


def complex_matrix(value: object, context: str) -> np.ndarray:
    """Strictly decode a dimensionless complex-pair matrix."""
    payload = mapping(value, context)
    exact_keys(payload, {"magnitude", "unit"}, context)
    if payload["unit"] not in ("1", "dimensionless"):
        fail(f"{context}.unit must be dimensionless")
    rows = array(payload["magnitude"], f"{context}.magnitude")
    decoded: list[list[complex]] = []
    width: int | None = None
    for row_index, row_value in enumerate(rows):
        row = array(row_value, f"{context}.magnitude[{row_index}]")
        if width is None:
            width = len(row)
        elif len(row) != width:
            fail(f"{context}.magnitude must be rectangular")
        decoded_row: list[complex] = []
        for column_index, pair_value in enumerate(row):
            pair = array(pair_value, f"{context}[{row_index},{column_index}]")
            if len(pair) != 2:
                fail(f"{context}[{row_index},{column_index}] must have length two")
            decoded_row.append(
                complex(
                    number(pair[0], f"{context}[{row_index},{column_index}].real"),
                    number(pair[1], f"{context}[{row_index},{column_index}].imag"),
                )
            )
        decoded.append(decoded_row)
    result = np.asarray(decoded, dtype=np.complex128)
    if result.ndim != 2 or result.size == 0:
        fail(f"{context} must be a nonempty matrix")
    return result


def spectrum(value: object, context: str) -> tuple[np.ndarray, np.ndarray]:
    """Strictly decode retained spectrum coordinates and values."""
    payload = mapping(value, context)
    exact_keys(payload, {"coordinates", "reciprocal_period", "eigenvalues"}, context)
    coordinates_payload = mapping(payload["coordinates"], f"{context}.coordinates")
    eigenvalues_payload = mapping(payload["eigenvalues"], f"{context}.eigenvalues")
    exact_keys(coordinates_payload, {"magnitude", "unit"}, f"{context}.coordinates")
    exact_keys(eigenvalues_payload, {"magnitude", "unit"}, f"{context}.eigenvalues")
    quantity(payload["reciprocal_period"], f"{context}.reciprocal_period")
    if coordinates_payload["unit"] != "dimensionless" or (
        eigenvalues_payload["unit"] != "dimensionless"
    ):
        fail(f"{context} must use the encoded dimensionless units")
    coordinates = np.asarray(
        [
            number(item, f"{context}.coordinates")
            for item in array(
                coordinates_payload["magnitude"], f"{context}.coordinates"
            )
        ],
        dtype=np.float64,
    )
    eigenvalues = np.asarray(
        [
            [
                number(item, f"{context}.eigenvalues")
                for item in array(row, f"{context}.eigenvalues")
            ]
            for row in array(eigenvalues_payload["magnitude"], f"{context}.eigenvalues")
        ],
        dtype=np.float64,
    )
    if eigenvalues.shape[0] != coordinates.size:
        fail(f"{context} coordinate/eigenvalue lengths disagree")
    return coordinates, eigenvalues


def interpolate(
    reduced: np.ndarray, representatives: np.ndarray, blocks: np.ndarray
) -> np.ndarray:
    """Independently evaluate a block-hopping polynomial."""
    phases = np.exp(2j * np.pi * np.outer(reduced, representatives))
    return np.asarray(
        np.einsum("kr,rij->kij", phases, blocks, optimize=True), dtype=np.complex128
    )


def fourier(
    reduced: np.ndarray, matrices: np.ndarray, representatives: np.ndarray
) -> np.ndarray:
    """Independently compute complete discrete block hoppings."""
    return np.asarray(
        [
            np.mean(
                matrices
                * np.exp(-2j * np.pi * reduced * int(representative))[:, None, None],
                axis=0,
            )
            for representative in representatives
        ],
        dtype=np.complex128,
    )


def transport(raw: np.ndarray) -> tuple[np.ndarray, float, np.ndarray]:
    """Independently apply polar transport and periodic closure."""
    frames = [raw[0].copy()]
    singular_values: list[float] = []
    for index in range(raw.shape[0] - 1):
        overlap = frames[index].conj().T @ raw[index + 1]
        left, values, right_h = np.linalg.svd(overlap)
        singular_values.extend(float(item) for item in values)
        frames.append(raw[index + 1] @ right_h.conj().T @ left.conj().T)
    closure = frames[-1].conj().T @ frames[0]
    left, values, right_h = np.linalg.svd(closure)
    singular_values.extend(float(item) for item in values)
    triangular, eigenvectors = schur(left @ right_h, output="complex")
    phases = np.angle(np.diag(triangular)).astype(np.float64)
    order = np.argsort(phases)
    phases = phases[order]
    eigenvectors = eigenvectors[:, order]
    for index in range(len(frames)):
        fraction = float(index) / float(len(frames))
        root = (
            eigenvectors
            @ np.diag(np.exp(1j * phases * fraction))
            @ eigenvectors.conj().T
        )
        frames[index] = frames[index] @ root
    return np.asarray(frames, dtype=np.complex128), min(singular_values), phases


def frame_defect(left: np.ndarray, right: np.ndarray) -> float:
    """Return maximum pointwise Frobenius defect."""
    return float(max(np.linalg.norm(a - b) for a, b in zip(left, right, strict=True)))


def projector_defect(left: np.ndarray, right: np.ndarray) -> float:
    """Return maximum projector Frobenius defect."""
    return float(
        max(
            np.linalg.norm(a @ a.conj().T - b @ b.conj().T)
            for a, b in zip(left, right, strict=True)
        )
    )


def spectral_error(matrices: np.ndarray, target: np.ndarray) -> float:
    """Return maximum absolute eigenvalue error."""
    values = np.asarray([np.linalg.eigvalsh(matrix) for matrix in matrices])
    return float(np.max(np.abs(values - target)))


def maximum(left: np.ndarray, right: np.ndarray) -> float:
    """Return a maximum elementwise absolute defect."""
    return float(np.max(np.abs(left - right)))


def main() -> None:
    """Strictly decode, reconstruct, compare, and retain verification."""
    input_payload = mapping(json.loads((ROOT / "input.json").read_text()), "input")
    exact_keys(
        input_payload,
        {
            "calculation_id",
            "parent_model",
            "retained_rank",
            "reciprocal_mesh_size",
            "withheld_mesh_size",
            "hopping_ranges",
            "attack",
            "external_gap_lower_bound",
            "overlap_singular_value_threshold",
            "orthonormality_absolute_tolerance",
            "coordinate_absolute_tolerance",
            "reconstruction_absolute_tolerance",
            "hermiticity_absolute_tolerance",
            "verification_absolute_tolerance",
        },
        "input",
    )
    result = mapping(json.loads((ROOT / "result.json").read_text()), "result")
    exact_keys(
        result,
        {
            "schema",
            "definition",
            "training_target",
            "withheld_target",
            "alignment_diagnostics",
            "complete_transforms",
            "range_study",
            "scope",
        },
        "result",
    )
    if (
        result["schema"]
        != "ksdft2effmass.periodic1d.multiband-alignment-calculation-result.v1"
    ):
        fail("unexpected result schema")
    definition = mapping(result["definition"], "definition")
    exact_keys(
        definition,
        {
            "calculation_id",
            "parent_model",
            "retained_rank",
            "reciprocal_mesh_size",
            "withheld_mesh_size",
            "withheld_mesh_rule",
            "withheld_reduced_momenta",
            "hopping_ranges",
            "attack",
            "external_gap_lower_bound",
            "overlap_singular_value_threshold",
            "orthonormality_absolute_tolerance",
            "coordinate_absolute_tolerance",
            "reconstruction_absolute_tolerance",
            "hermiticity_absolute_tolerance",
            "verification_absolute_tolerance",
        },
        "definition",
    )
    if definition["calculation_id"] != input_payload["calculation_id"]:
        fail("calculation identity differs from frozen input")
    if definition["withheld_mesh_rule"] != "staggered-uniform-disjoint-v1":
        fail("unexpected withheld mesh rule")
    parent_result = mapping(definition["parent_model"], "definition.parent_model")
    exact_keys(
        parent_result,
        {
            "model_id",
            "model_role",
            "reciprocal_period",
            "representatives",
            "hopping_blocks",
            "hermiticity_absolute_tolerance",
        },
        "definition.parent_model",
    )
    parent_input = mapping(input_payload["parent_model"], "input.parent_model")
    exact_keys(
        parent_input,
        {
            "model_id",
            "reciprocal_period",
            "representatives",
            "hopping_blocks",
            "hermiticity_absolute_tolerance",
        },
        "input.parent_model",
    )
    if (
        parent_result["model_id"] != parent_input["model_id"]
        or parent_result["model_role"] != "toy"
    ):
        fail("parent identity or role differs from frozen input")
    reciprocal_period = quantity(
        parent_result["reciprocal_period"], "reciprocal_period"
    )
    representatives = np.asarray(
        [
            integer(item, "representative")
            for item in array(parent_result["representatives"], "representatives")
        ],
        dtype=np.int64,
    )
    blocks = np.asarray(
        [
            complex_matrix(item, "parent block")
            for item in array(parent_result["hopping_blocks"], "parent blocks")
        ],
        dtype=np.complex128,
    )
    if representatives.tolist() != parent_input["representatives"]:
        fail("parent representatives differ from frozen input")
    input_blocks = np.asarray(
        [
            complex_matrix(item, "input parent block")
            for item in array(parent_input["hopping_blocks"], "input parent blocks")
        ]
    )
    if maximum(blocks, input_blocks) != 0.0 or reciprocal_period != quantity(
        parent_input["reciprocal_period"], "input reciprocal_period"
    ):
        fail("parent payload differs from frozen input")
    if quantity(
        parent_result["hermiticity_absolute_tolerance"],
        "definition.parent_model.hermiticity_absolute_tolerance",
    ) != quantity(
        parent_input["hermiticity_absolute_tolerance"],
        "input.parent_model.hermiticity_absolute_tolerance",
    ):
        fail("parent Hermiticity tolerance differs from frozen input")
    rank = integer(definition["retained_rank"], "retained_rank")
    mesh_size = integer(definition["reciprocal_mesh_size"], "reciprocal_mesh_size")
    withheld_size = integer(definition["withheld_mesh_size"], "withheld_mesh_size")
    if rank != integer(input_payload["retained_rank"], "input.retained_rank"):
        fail("retained rank differs from frozen input")
    if mesh_size != integer(
        input_payload["reciprocal_mesh_size"], "input.reciprocal_mesh_size"
    ):
        fail("training mesh size differs from frozen input")
    if withheld_size != integer(
        input_payload["withheld_mesh_size"], "input.withheld_mesh_size"
    ):
        fail("withheld mesh size differs from frozen input")
    for field in (
        "overlap_singular_value_threshold",
        "orthonormality_absolute_tolerance",
        "coordinate_absolute_tolerance",
        "reconstruction_absolute_tolerance",
        "verification_absolute_tolerance",
    ):
        if number(definition[field], f"definition.{field}") != number(
            input_payload[field], f"input.{field}"
        ):
            fail(f"{field} differs from frozen input")
    for field in (
        "external_gap_lower_bound",
        "hermiticity_absolute_tolerance",
    ):
        if quantity(definition[field], f"definition.{field}") != quantity(
            input_payload[field], f"input.{field}"
        ):
            fail(f"{field} differs from frozen input")
    frozen_ranges_from_input = [
        integer(item, "input frozen range")
        for item in array(input_payload["hopping_ranges"], "input.hopping_ranges")
    ]
    frozen_ranges_from_result = [
        integer(item, "result frozen range")
        for item in array(definition["hopping_ranges"], "definition.hopping_ranges")
    ]
    if frozen_ranges_from_result != frozen_ranges_from_input:
        fail("hopping ranges differ from frozen input")
    training_coordinates, retained_training = spectrum(
        result["training_target"], "training_target"
    )
    withheld_coordinates, retained_withheld = spectrum(
        result["withheld_target"], "withheld_target"
    )
    expected_training_reduced = np.arange(-mesh_size // 2, mesh_size // 2) / float(
        mesh_size
    )
    expected_withheld_reduced = np.asarray(
        [
            -0.5 + (float(index) + 1.0 / float(mesh_size + 1)) / float(withheld_size)
            for index in range(withheld_size)
        ]
    )
    dimensionless_defects = [
        maximum(training_coordinates / reciprocal_period, expected_training_reduced),
        maximum(withheld_coordinates / reciprocal_period, expected_withheld_reduced),
        maximum(
            np.asarray(
                array(definition["withheld_reduced_momenta"], "withheld points"),
                dtype=float,
            ),
            expected_withheld_reduced,
        ),
    ]
    parent_training = interpolate(expected_training_reduced, representatives, blocks)
    parent_withheld = interpolate(expected_withheld_reduced, representatives, blocks)
    training_values: list[np.ndarray] = []
    raw_frames: list[np.ndarray] = []
    for matrix in parent_training:
        values, vectors = np.linalg.eigh(matrix)
        training_values.append(values[:rank])
        raw_frames.append(vectors[:, :rank])
    expected_training = np.asarray(training_values)
    expected_withheld = np.asarray(
        [np.linalg.eigvalsh(matrix)[:rank] for matrix in parent_withheld]
    )
    energy_defects = [
        maximum(retained_training, expected_training),
        maximum(retained_withheld, expected_withheld),
    ]
    reference_frames, minimum_overlap, closure_phases = transport(
        np.asarray(raw_frames)
    )
    attack_result = mapping(definition["attack"], "definition.attack")
    exact_keys(
        attack_result,
        {"family", "constant_angle", "sine_coefficients"},
        "definition.attack",
    )
    if attack_result["family"] != "rank-two-real-rotation-sine-series-v1":
        fail("unexpected attack family")
    constant = number(attack_result["constant_angle"], "attack.constant_angle")
    input_attack = mapping(input_payload["attack"], "input.attack")
    exact_keys(
        input_attack,
        {"constant_angle", "sine_coefficients"},
        "input.attack",
    )
    input_constant = number(
        input_attack["constant_angle"], "input.attack.constant_angle"
    )
    if constant != input_constant:
        fail("attack constant angle differs from frozen input")
    coefficients = [
        number(item, "attack coefficient")
        for item in array(attack_result["sine_coefficients"], "attack coefficients")
    ]
    input_coefficient_values = array(
        input_attack["sine_coefficients"], "input attack coefficients"
    )
    input_coefficients = [
        number(item, "input attack coefficient")
        for item in input_coefficient_values
    ]
    if coefficients != input_coefficients:
        fail("attack sine coefficients differ from frozen input")
    attacks = []
    for momentum in expected_training_reduced:
        angle = constant + sum(
            value * np.sin(2.0 * np.pi * harmonic * momentum)
            for harmonic, value in enumerate(coefficients, start=1)
        )
        attacks.append(
            np.asarray(
                [[np.cos(angle), -np.sin(angle)], [np.sin(angle), np.cos(angle)]],
                dtype=np.complex128,
            )
        )
    attacks_array = np.asarray(attacks)
    attacked_frames = np.asarray(
        [
            frame @ attack
            for frame, attack in zip(reference_frames, attacks_array, strict=True)
        ]
    )
    rotations: list[np.ndarray] = []
    aligned_frames: list[np.ndarray] = []
    for reference, candidate in zip(reference_frames, attacked_frames, strict=True):
        left, _, right_h = np.linalg.svd(candidate.conj().T @ reference)
        rotation = left @ right_h
        rotations.append(rotation)
        aligned_frames.append(candidate @ rotation)
    rotations_array = np.asarray(rotations)
    aligned_frames_array = np.asarray(aligned_frames)
    aggregate = np.sum(
        np.einsum("kji,kjl->kil", attacked_frames.conj(), reference_frames), axis=0
    )
    left, _, right_h = np.linalg.svd(aggregate)
    global_rotation = left @ right_h
    constrained_frames = np.asarray(
        [frame @ global_rotation for frame in attacked_frames]
    )
    reference_operators = np.asarray(
        [
            frame.conj().T @ matrix @ frame
            for matrix, frame in zip(parent_training, reference_frames, strict=True)
        ]
    )
    attacked_operators = np.asarray(
        [
            frame.conj().T @ matrix @ frame
            for matrix, frame in zip(parent_training, attacked_frames, strict=True)
        ]
    )
    aligned_operators = np.asarray(
        [
            frame.conj().T @ matrix @ frame
            for matrix, frame in zip(parent_training, aligned_frames_array, strict=True)
        ]
    )
    constrained_operators = np.asarray(
        [
            frame.conj().T @ matrix @ frame
            for matrix, frame in zip(parent_training, constrained_frames, strict=True)
        ]
    )
    diagnostics = mapping(result["alignment_diagnostics"], "alignment_diagnostics")
    exact_keys(
        diagnostics,
        {
            "external_gap_minimum",
            "minimum_neighbor_or_closure_overlap_singular_value",
            "closure_eigenphases",
            "projector_maximum_frobenius_defect",
            "attack_frame_maximum_frobenius_defect",
            "pointwise_frame_maximum_frobenius_defect",
            "pointwise_rotation_recovery_maximum_frobenius_defect",
            "constrained_global_rotation",
            "constrained_frame_maximum_frobenius_defect",
            "attacked_operator_maximum_frobenius_defect",
            "pointwise_operator_maximum_frobenius_defect",
            "constrained_operator_maximum_frobenius_defect",
        },
        "alignment_diagnostics",
    )
    expected_gap = min(
        float(np.linalg.eigvalsh(matrix)[rank] - np.linalg.eigvalsh(matrix)[rank - 1])
        for matrix in np.concatenate((parent_training, parent_withheld))
    )
    if expected_gap < quantity(
        definition["external_gap_lower_bound"], "external gap lower bound"
    ):
        fail("reconstructed external gap violates the frozen lower bound")
    if minimum_overlap < number(
        definition["overlap_singular_value_threshold"], "overlap threshold"
    ):
        fail("reconstructed overlap violates the frozen threshold")
    energy_defects.extend(
        [
            abs(
                quantity(diagnostics["external_gap_minimum"], "external gap")
                - expected_gap
            ),
            abs(
                quantity(
                    diagnostics["attacked_operator_maximum_frobenius_defect"],
                    "attacked operator",
                )
                - frame_defect(reference_operators, attacked_operators)
            ),
            abs(
                quantity(
                    diagnostics["pointwise_operator_maximum_frobenius_defect"],
                    "pointwise operator",
                )
                - frame_defect(reference_operators, aligned_operators)
            ),
            abs(
                quantity(
                    diagnostics["constrained_operator_maximum_frobenius_defect"],
                    "constrained operator",
                )
                - frame_defect(reference_operators, constrained_operators)
            ),
        ]
    )
    dimensionless_defects.extend(
        [
            abs(
                number(
                    diagnostics["minimum_neighbor_or_closure_overlap_singular_value"],
                    "minimum overlap",
                )
                - minimum_overlap
            ),
            maximum(
                np.asarray(
                    array(diagnostics["closure_eigenphases"], "closure phases"),
                    dtype=float,
                ),
                closure_phases,
            ),
            abs(
                number(
                    diagnostics["projector_maximum_frobenius_defect"],
                    "projector defect",
                )
                - projector_defect(reference_frames, attacked_frames)
            ),
            abs(
                number(
                    diagnostics["attack_frame_maximum_frobenius_defect"],
                    "attack frame defect",
                )
                - frame_defect(reference_frames, attacked_frames)
            ),
            abs(
                number(
                    diagnostics["pointwise_frame_maximum_frobenius_defect"],
                    "pointwise frame defect",
                )
                - frame_defect(reference_frames, aligned_frames_array)
            ),
            abs(
                number(
                    diagnostics["pointwise_rotation_recovery_maximum_frobenius_defect"],
                    "rotation recovery",
                )
                - frame_defect(rotations_array, attacks_array.conj().transpose(0, 2, 1))
            ),
            maximum(
                complex_matrix(
                    diagnostics["constrained_global_rotation"], "global rotation"
                ),
                global_rotation,
            ),
            abs(
                number(
                    diagnostics["constrained_frame_maximum_frobenius_defect"],
                    "global frame defect",
                )
                - frame_defect(reference_frames, constrained_frames)
            ),
        ]
    )
    complete_representatives = np.arange(
        -mesh_size // 2, mesh_size // 2, dtype=np.int64
    )
    expected_blocks = {
        "reference": fourier(
            expected_training_reduced, reference_operators, complete_representatives
        ),
        "attacked": fourier(
            expected_training_reduced, attacked_operators, complete_representatives
        ),
        "pointwise_aligned": fourier(
            expected_training_reduced, aligned_operators, complete_representatives
        ),
    }
    transforms = mapping(result["complete_transforms"], "complete_transforms")
    exact_keys(transforms, set(expected_blocks), "complete_transforms")
    for name, blocks_expected in expected_blocks.items():
        transform = mapping(transforms[name], f"complete_transforms.{name}")
        exact_keys(
            transform,
            {
                "representatives",
                "hopping_blocks",
                "reconstruction_maximum_frobenius_error",
                "reconstruction_absolute_tolerance",
                "reconstruction_passes",
                "hermiticity",
            },
            f"complete_transforms.{name}",
        )
        retained_representatives = np.asarray(
            [
                integer(item, "transform representative")
                for item in array(
                    transform["representatives"], "transform representatives"
                )
            ]
        )
        if not np.array_equal(retained_representatives, complete_representatives):
            fail(f"{name} transform representatives differ")
        retained_blocks = np.asarray(
            [
                complex_matrix(item, f"{name} block")
                for item in array(transform["hopping_blocks"], f"{name} blocks")
            ]
        )
        energy_defects.append(maximum(retained_blocks, blocks_expected))
        reconstructed = interpolate(
            expected_training_reduced, complete_representatives, blocks_expected
        )
        expected_reconstruction = frame_defect(
            reconstructed,
            {
                "reference": reference_operators,
                "attacked": attacked_operators,
                "pointwise_aligned": aligned_operators,
            }[name],
        )
        energy_defects.append(
            abs(
                quantity(
                    transform["reconstruction_maximum_frobenius_error"],
                    f"{name} reconstruction",
                )
                - expected_reconstruction
            )
        )
        reconstruction_tolerance = quantity(
            transform["reconstruction_absolute_tolerance"],
            f"{name} reconstruction tolerance",
        )
        if reconstruction_tolerance != number(
            definition["reconstruction_absolute_tolerance"],
            "definition reconstruction tolerance",
        ):
            fail(f"{name} reconstruction tolerance differs from frozen input")
        if transform["reconstruction_passes"] is not (
            expected_reconstruction <= reconstruction_tolerance
        ):
            fail(f"{name} reconstruction disposition is inconsistent")
        hermiticity = mapping(transform["hermiticity"], f"{name}.hermiticity")
        exact_keys(
            hermiticity,
            {"maximum_frobenius_defect", "absolute_tolerance", "passes"},
            f"{name}.hermiticity",
        )
        defects = [
            np.linalg.norm(
                blocks_expected[index]
                - blocks_expected[
                    np.where(
                        complete_representatives
                        == ((-int(representative) + mesh_size // 2) % mesh_size)
                        - mesh_size // 2
                    )[0][0]
                ]
                .conj()
                .T
            )
            for index, representative in enumerate(complete_representatives)
        ]
        expected_hermiticity = max(defects)
        retained_hermiticity = quantity(
            hermiticity["maximum_frobenius_defect"], f"{name} Hermiticity"
        )
        retained_hermiticity_tolerance = quantity(
            hermiticity["absolute_tolerance"], f"{name} Hermiticity tolerance"
        )
        energy_defects.append(abs(retained_hermiticity - expected_hermiticity))
        if retained_hermiticity_tolerance != quantity(
            definition["hermiticity_absolute_tolerance"],
            "definition Hermiticity tolerance",
        ):
            fail(f"{name} Hermiticity tolerance differs from frozen input")
        expected_hermiticity_passes = bool(
            expected_hermiticity <= retained_hermiticity_tolerance
        )
        if hermiticity["passes"] is not expected_hermiticity_passes:
            fail(f"{name} Hermiticity disposition is inconsistent")
    ranges = array(result["range_study"], "range_study")
    frozen_ranges = [
        integer(item, "frozen range")
        for item in array(definition["hopping_ranges"], "hopping_ranges")
    ]
    if len(ranges) != len(frozen_ranges):
        fail("range-study length differs from frozen inventory")
    for raw_range, maximum_range in zip(ranges, frozen_ranges, strict=True):
        range_result = mapping(raw_range, "range result")
        exact_keys(
            range_result,
            {"maximum_range", "reference", "attacked", "pointwise_aligned"},
            "range result",
        )
        if range_result["maximum_range"] != maximum_range:
            fail("range-study ordering differs from frozen inventory")
        keep = np.abs(complete_representatives) <= maximum_range
        for name, blocks_full in expected_blocks.items():
            channel = mapping(range_result[name], f"range.{name}")
            exact_keys(
                channel,
                {
                    "omitted_block_l2_norm",
                    "training_maximum_absolute_spectral_error",
                    "withheld_maximum_absolute_spectral_error",
                },
                f"range.{name}",
            )
            expected_omitted = float(np.linalg.norm(blocks_full[~keep]))
            training_model = interpolate(
                expected_training_reduced,
                complete_representatives[keep],
                blocks_full[keep],
            )
            withheld_model = interpolate(
                expected_withheld_reduced,
                complete_representatives[keep],
                blocks_full[keep],
            )
            energy_defects.extend(
                [
                    abs(
                        quantity(channel["omitted_block_l2_norm"], f"{name} omitted")
                        - expected_omitted
                    ),
                    abs(
                        quantity(
                            channel["training_maximum_absolute_spectral_error"],
                            f"{name} training error",
                        )
                        - spectral_error(training_model, expected_training)
                    ),
                    abs(
                        quantity(
                            channel["withheld_maximum_absolute_spectral_error"],
                            f"{name} withheld error",
                        )
                        - spectral_error(withheld_model, expected_withheld)
                    ),
                ]
            )
    scope = mapping(result["scope"], "scope")
    exact_keys(
        scope,
        {
            "pointwise_procrustes_included",
            "global_unitary_constraint_included",
            "general_nonconvex_alignment_solution_included",
            "material_validation_included",
            "uncertainty_quantification_included",
            "external_calculator_execution_included",
            "scientific_acceptance_included",
        },
        "scope",
    )
    expected_scope = {
        "pointwise_procrustes_included": True,
        "global_unitary_constraint_included": True,
        "general_nonconvex_alignment_solution_included": False,
        "material_validation_included": False,
        "uncertainty_quantification_included": False,
        "external_calculator_execution_included": False,
        "scientific_acceptance_included": False,
    }
    if scope != expected_scope:
        fail("scope flags differ from the frozen evidence boundary")
    tolerance = number(
        definition["verification_absolute_tolerance"], "verification tolerance"
    )
    maximum_dimensionless = float(max(dimensionless_defects))
    maximum_energy = float(max(energy_defects))
    passes = bool(maximum_dimensionless <= tolerance and maximum_energy <= tolerance)
    verification = {
        "schema": "ksdft2effmass.periodic1d.multiband-alignment-verification.v1",
        "result_schema": result["schema"],
        "dimensionless_maximum_absolute_defect": maximum_dimensionless,
        "energy_maximum_absolute_defect": {"magnitude": maximum_energy, "unit": "1"},
        "absolute_tolerance": tolerance,
        "passes": passes,
        "scope": {
            "independent_reconstruction": True,
            "producer_action_called": False,
            "material_validation": False,
            "scientific_acceptance": False,
        },
    }
    (ROOT / "verification.json").write_text(
        json.dumps(verification, sort_keys=True, separators=(",", ":"), allow_nan=False)
        + "\n",
        encoding="utf-8",
    )
    if not verification["passes"]:
        fail("independent reconstruction exceeded the frozen tolerance")


if __name__ == "__main__":
    main()
