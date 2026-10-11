#!/usr/bin/env python3
"""Standalone NumPy reconstruction of the frozen synthetic M3 result."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Never, cast

import numpy as np
from scipy.linalg import schur  # type: ignore[import-untyped]

ROOT = Path(__file__).resolve().parent


def fail(message: str) -> Never:
    """Reject malformed or inconsistent retained evidence."""
    raise ValueError(message)


def mapping(value: object, context: str) -> dict[str, object]:
    """Require a JSON object."""
    if type(value) is not dict:
        fail(f"{context} must be an object")
    return value


def exact(value: dict[str, object], keys: set[str], context: str) -> None:
    """Require exactly the declared fields."""
    if set(value) != keys:
        fail(f"{context} fields must be exactly {sorted(keys)}")


def array(value: object, context: str) -> list[object]:
    """Require a JSON array."""
    if type(value) is not list:
        fail(f"{context} must be an array")
    return value


def text(value: object, context: str) -> str:
    """Require a nonempty string."""
    if type(value) is not str or not value:
        fail(f"{context} must be a nonempty string")
    return value


def number(value: object, context: str) -> float:
    """Require a finite number and reject booleans."""
    if type(value) not in (int, float):
        fail(f"{context} must be numeric")
    result = float(cast(int | float, value))
    if not np.isfinite(result):
        fail(f"{context} must be finite")
    return result


def integer(value: object, context: str) -> int:
    """Require a built-in integer and reject booleans."""
    if type(value) is not int:
        fail(f"{context} must be an integer")
    return value


def quantity(value: object, context: str) -> float:
    """Decode a scalar quantity in the frozen model-energy unit."""
    payload = mapping(value, context)
    exact(payload, {"magnitude", "unit"}, context)
    if text(payload["unit"], f"{context}.unit") != "1":
        fail(f"{context}.unit must be '1'")
    return number(payload["magnitude"], f"{context}.magnitude")


def pair(value: object, context: str) -> tuple[float, float]:
    """Decode a finite length-two numeric array."""
    values = array(value, context)
    if len(values) != 2:
        fail(f"{context} must contain two values")
    return number(values[0], f"{context}[0]"), number(values[1], f"{context}[1]")


def complex_matrix(value: object, context: str) -> np.ndarray:
    """Decode a complex-pair matrix in the frozen model-energy unit."""
    payload = mapping(value, context)
    exact(payload, {"magnitude", "unit"}, context)
    if text(payload["unit"], f"{context}.unit") != "1":
        fail(f"{context}.unit must be '1'")
    rows = array(payload["magnitude"], f"{context}.magnitude")
    decoded: list[list[complex]] = []
    width: int | None = None
    for row_index, item in enumerate(rows):
        row = array(item, f"{context}[{row_index}]")
        if width is None:
            width = len(row)
        elif len(row) != width:
            fail(f"{context} must be rectangular")
        decoded_row: list[complex] = []
        for column_index, raw_pair in enumerate(row):
            values = array(raw_pair, f"{context}[{row_index},{column_index}]")
            if len(values) != 2:
                fail(f"{context} complex entries must have length two")
            decoded_row.append(
                complex(
                    number(values[0], f"{context}.real"),
                    number(values[1], f"{context}.imag"),
                )
            )
        decoded.append(decoded_row)
    result = np.asarray(decoded, dtype=np.complex128)
    if result.ndim != 2 or result.shape[0] != result.shape[1]:
        fail(f"{context} must be square")
    return result


def maximum(left: np.ndarray, right: np.ndarray) -> float:
    """Return a maximum absolute difference."""
    if left.shape != right.shape:
        return float("inf")
    return float(np.max(np.abs(left - right))) if left.size else 0.0


def rotation(angle: float) -> np.ndarray:
    """Return the declared rank-two real rotation."""
    return np.asarray(
        [[np.cos(angle), -np.sin(angle)], [np.sin(angle), np.cos(angle)]],
        dtype=np.complex128,
    )


def conjugate(matrices: np.ndarray, unitary: np.ndarray) -> np.ndarray:
    """Apply one global unitary to every represented operator."""
    return np.asarray(
        np.einsum(
            "ab,kbc,cd->kad",
            unitary.conj().T,
            matrices,
            unitary,
            optimize=True,
        )
    )


def transport(raw: np.ndarray) -> tuple[np.ndarray, float]:
    """Apply polar transport and distribute the periodic closure holonomy."""
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
    return np.asarray(frames, dtype=np.complex128), min(singular_values)


def transform(
    reduced: np.ndarray, matrices: np.ndarray
) -> tuple[np.ndarray, np.ndarray]:
    """Apply the centered complete discrete Fourier transform."""
    count = reduced.size
    representatives = np.arange(-(count // 2), count // 2, dtype=np.int64)
    blocks = np.asarray(
        [
            np.mean(
                matrices * np.exp(-2j * np.pi * reduced * int(item))[:, None, None],
                axis=0,
            )
            for item in representatives
        ]
    )
    return representatives, blocks


def interpolate(
    reduced: np.ndarray, representatives: np.ndarray, blocks: np.ndarray
) -> np.ndarray:
    """Reconstruct reciprocal matrices from hopping blocks."""
    phases = np.exp(2j * np.pi * np.outer(reduced, representatives))
    return np.asarray(np.einsum("kr,rij->kij", phases, blocks, optimize=True))


def candidate(
    reference: np.ndarray, parameter: tuple[float, float], scale: float
) -> np.ndarray:
    """Construct the declared trace-plus-traceless candidate family."""
    rank = reference.shape[1]
    identity = np.eye(rank, dtype=np.complex128)
    mean = np.trace(reference, axis1=1, axis2=2) / float(rank)
    base = mean[:, None, None] * identity
    return np.asarray(
        base + parameter[0] * scale * identity + parameter[1] * (reference - base)
    )


def spectral_rms(
    candidate_matrices: np.ndarray, target: np.ndarray, scale: float
) -> float:
    """Return the normalized spectral RMS loss."""
    return float(
        np.sqrt(np.mean(np.abs(np.linalg.eigvalsh(candidate_matrices) - target) ** 2))
        / scale
    )


def operator_rms(
    candidate_matrices: np.ndarray, target: np.ndarray, scale: float
) -> float:
    """Return the normalized represented-operator RMS loss."""
    rank = candidate_matrices.shape[1]
    return float(
        np.sqrt(
            np.sum(np.abs(candidate_matrices - target) ** 2)
            / float(candidate_matrices.shape[0] * rank)
        )
        / scale
    )


def quadratic(
    features: np.ndarray, offset: np.ndarray, scale: float
) -> tuple[np.ndarray, np.ndarray, float]:
    """Independently derive a centered squared-loss quadratic."""
    normalization = float(features.shape[0] * features.shape[1]) * scale**2
    matrix = np.asarray(
        [
            [
                np.vdot(features[..., row], features[..., column]).real / normalization
                for column in range(2)
            ]
            for row in range(2)
        ]
    )
    matrix = 0.5 * (matrix + matrix.T)
    linear = np.asarray(
        [np.vdot(features[..., row], offset).real / normalization for row in range(2)]
    )
    center = -np.linalg.solve(matrix, linear)
    minimum = float(
        np.vdot(offset, offset).real / normalization
        - linear @ np.linalg.solve(matrix, linear)
    )
    if minimum < 0.0 and abs(minimum) <= 1.0e-14:
        minimum = 0.0
    return center, matrix, minimum


def squared_loss(
    parameter: tuple[float, float],
    center: np.ndarray,
    matrix: np.ndarray,
    minimum: float,
) -> float:
    """Evaluate one reconstructed centered quadratic."""
    delta = np.asarray(parameter) - center
    return float(minimum + delta @ matrix @ delta)


def axis_extreme(
    center: np.ndarray,
    matrix: np.ndarray,
    minimum: float,
    threshold: float,
    direction: float,
) -> tuple[tuple[float, float], float]:
    """Return an unconstrained ellipsoid extreme along splitting scale."""
    inverse = np.linalg.inv(matrix)
    unit = np.asarray((0.0, direction))
    point = center + np.sqrt(
        (threshold**2 - minimum) / float(unit @ inverse @ unit)
    ) * (inverse @ unit)
    return (float(point[0]), float(point[1])), float(point[1])


def domain_minimum(
    bounds: tuple[tuple[float, float], tuple[float, float]],
    center: np.ndarray,
    matrix: np.ndarray,
    minimum: float,
) -> float:
    """Minimize a positive quadratic over the frozen rectangle."""
    lower = np.asarray((bounds[0][0], bounds[1][0]))
    upper = np.asarray((bounds[0][1], bounds[1][1]))
    candidates = [np.clip(center, lower, upper)]
    for axis in (0, 1):
        other = 1 - axis
        for bound in (lower[axis], upper[axis]):
            point = center.copy()
            point[axis] = bound
            point[other] = center[other] - matrix[other, axis] / matrix[
                other, other
            ] * (bound - center[axis])
            point[other] = np.clip(point[other], lower[other], upper[other])
            candidates.append(point)
    return min(
        squared_loss((float(point[0]), float(point[1])), center, matrix, minimum)
        for point in candidates
    )


def main() -> None:
    """Verify retained bytes against the frozen finite protocol."""
    source = mapping(json.loads((ROOT / "input.json").read_text()), "input")
    result = mapping(json.loads((ROOT / "result.json").read_text()), "result")
    exact(
        result,
        {
            "schema",
            "definition",
            "baseline_summary",
            "training_quadratic_losses",
            "cases",
            "scope",
        },
        "result",
    )
    if (
        result["schema"]
        != "ksdft2effmass.periodic1d.constrained-admissible-set-result.v1"
    ):
        fail("unexpected result schema")
    scope = mapping(result["scope"], "scope")
    expected_scope: dict[str, object] = {
        "training_defines_admissible_sets": True,
        "withheld_data_changes_models_or_certificates": False,
        "finite_global_alignment_family_only": True,
        "general_nonconvex_alignment_solution_included": False,
        "material_validation_included": False,
        "uncertainty_quantification_included": False,
        "external_calculator_execution_included": False,
        "scientific_acceptance_included": False,
    }
    exact(scope, set(expected_scope), "scope")
    if scope != expected_scope:
        fail("scope differs from the frozen evidence boundary")
    definition = mapping(result["definition"], "definition")
    baseline_input = mapping(source["multiband_baseline"], "input baseline")
    baseline_result = mapping(definition["multiband_baseline"], "result baseline")
    input_controls = {
        "calculation_id",
        "multiband_baseline",
        "candidate_family",
        "parameter_order",
        "energy_shift_ratio_bounds",
        "splitting_scale_bounds",
        "alignment_family",
        "alignment_angles",
        "loss_energy_scale",
        "loss_normalization",
        "compatible_thresholds",
        "separated_thresholds",
        "compatible_witness",
        "locality_ranges",
        "separation_metric",
        "separation_resolution",
        "quadratic_absolute_tolerance",
        "verification_absolute_tolerance",
        "schema",
    }
    exact(source, input_controls, "input")
    literal_controls = {
        "schema": "ksdft2effmass.periodic1d.constrained-admissible-set-input.v1",
        "candidate_family": (
            "trace-plus-energy-shift-and-positive-traceless-splitting-v1"
        ),
        "alignment_family": "finite-one-global-real-rotation-v1",
        "loss_normalization": "sqrt(sum-frobenius-squared/(N*rank))/scale",
        "separation_metric": "euclidean-parameter-distance",
    }
    for name, expected in literal_controls.items():
        if source[name] != expected:
            fail(f"input {name} differs from the v1 contract")
    if source["parameter_order"] != ["energy_shift_ratio", "splitting_scale"]:
        fail("input parameter order differs from the v1 contract")
    definition_controls = input_controls - {"schema"}
    exact(definition, definition_controls, "definition")
    for name in definition_controls - {"multiband_baseline"}:
        left = source[name]
        right = definition[name]
        if name == "loss_energy_scale":
            if quantity(left, "input loss scale") != quantity(
                right, "result loss scale"
            ):
                fail("loss scale differs from frozen input")
        elif left != right:
            fail(f"definition.{name} differs from frozen input")
    quadratic_tolerance = number(
        definition["quadratic_absolute_tolerance"],
        "quadratic tolerance",
    )
    if quadratic_tolerance <= 0.0:
        fail("quadratic tolerance must be positive")
    tolerance = number(
        definition["verification_absolute_tolerance"],
        "verification tolerance",
    )
    if tolerance <= 0.0:
        fail("verification tolerance must be positive")
    baseline_keys = {
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
    }
    exact(baseline_input, baseline_keys, "input baseline")
    exact(
        baseline_result,
        baseline_keys | {"withheld_mesh_rule"},
        "result baseline",
    )
    if baseline_result["withheld_mesh_rule"] != "staggered-uniform-disjoint-v1":
        fail("unexpected withheld mesh rule")
    quantity_fields = {
        "external_gap_lower_bound",
        "hermiticity_absolute_tolerance",
    }
    for name in baseline_keys - {"parent_model", "attack"}:
        if name in quantity_fields:
            if quantity(baseline_input[name], f"input baseline {name}") != quantity(
                baseline_result[name], f"result baseline {name}"
            ):
                fail(f"baseline definition field {name} differs from input")
        elif baseline_input[name] != baseline_result[name]:
            fail(f"baseline definition field {name} differs from input")
    attack_input = mapping(baseline_input["attack"], "input attack")
    attack_result = mapping(baseline_result["attack"], "result attack")
    exact(attack_input, {"constant_angle", "sine_coefficients"}, "input attack")
    exact(
        attack_result,
        {"family", "constant_angle", "sine_coefficients"},
        "result attack",
    )
    if attack_result["family"] != "rank-two-real-rotation-sine-series-v1":
        fail("unexpected attack family")
    for name in ("constant_angle", "sine_coefficients"):
        if attack_input[name] != attack_result[name]:
            fail(f"attack field {name} differs from input")
    parent_input = mapping(baseline_input["parent_model"], "input parent")
    parent_result = mapping(baseline_result["parent_model"], "result parent")
    exact(parent_result, set(parent_input) | {"model_role"}, "result parent")
    if parent_result["model_role"] != "toy":
        fail("unexpected parent model role")
    for name in set(parent_input) - {"hopping_blocks"}:
        if name in {"reciprocal_period", "hermiticity_absolute_tolerance"}:
            if quantity(parent_input[name], f"input parent {name}") != quantity(
                parent_result[name], f"result parent {name}"
            ):
                fail(f"parent {name} differs from input")
        elif parent_input[name] != parent_result[name]:
            fail(f"parent {name} differs from input")
    input_blocks = array(parent_input["hopping_blocks"], "input blocks")
    result_blocks = array(parent_result["hopping_blocks"], "result blocks")
    if len(input_blocks) != len(result_blocks):
        fail("parent block count differs from input")
    blocks = np.asarray(
        [
            complex_matrix(item, f"result block {index}")
            for index, item in enumerate(result_blocks)
        ]
    )
    for index, item in enumerate(input_blocks):
        if maximum(complex_matrix(item, f"input block {index}"), blocks[index]) != 0.0:
            fail("parent hopping blocks differ from input")
    if blocks.ndim != 3 or blocks.shape[1] != blocks.shape[2]:
        fail("parent hopping blocks must be common square matrices")
    representatives = np.asarray(
        [
            integer(item, "representative")
            for item in array(parent_result["representatives"], "representatives")
        ],
        dtype=np.int64,
    )
    mesh_size = integer(baseline_result["reciprocal_mesh_size"], "mesh size")
    withheld_size = integer(baseline_result["withheld_mesh_size"], "withheld size")
    rank = integer(baseline_result["retained_rank"], "retained rank")
    if mesh_size < 4 or withheld_size < 4:
        fail("training and withheld meshes must each contain at least four points")
    if rank != 2 or rank >= blocks.shape[1]:
        fail("M3 v1 requires a proper rank-two retained subspace")
    if len(representatives) != len(blocks):
        fail("parent representative and hopping-block counts must match")
    if quantity(parent_result["reciprocal_period"], "reciprocal period") <= 0.0:
        fail("parent reciprocal period must be positive")
    if tuple(representatives) != tuple(sorted(set(representatives))):
        fail("parent representatives must be unique and increasing")
    block_by_representative = {
        int(representative): block
        for representative, block in zip(representatives, blocks, strict=True)
    }
    parent_hermiticity = 0.0
    for representative, block in block_by_representative.items():
        partner = block_by_representative.get(-representative)
        if partner is None:
            fail("parent representatives must be inversion complete")
        parent_hermiticity = max(
            parent_hermiticity,
            float(np.linalg.norm(block - partner.conj().T)),
        )
    hermiticity_tolerance = quantity(
        baseline_result["hermiticity_absolute_tolerance"],
        "Hermiticity tolerance",
    )
    if parent_hermiticity > hermiticity_tolerance:
        fail("parent blocks violate the frozen Hermiticity tolerance")
    reduced = -0.5 + np.arange(mesh_size, dtype=np.float64) / float(mesh_size)
    withheld_offset = 1.0 / float(mesh_size + 1)
    withheld_reduced = -0.5 + (
        np.arange(withheld_size, dtype=np.float64) + withheld_offset
    ) / float(withheld_size)
    coordinate_tolerance = number(
        baseline_result["coordinate_absolute_tolerance"],
        "coordinate tolerance",
    )
    minimum_cross_mesh_distance = float(
        np.min(np.abs(reduced[:, None] - withheld_reduced[None, :]))
    )
    if minimum_cross_mesh_distance <= coordinate_tolerance:
        fail("training and withheld coordinate supports are not disjoint")
    phases = np.exp(2j * np.pi * np.outer(reduced, representatives))
    fibers = np.einsum("kr,rij->kij", phases, blocks, optimize=True)
    withheld_phases = np.exp(2j * np.pi * np.outer(withheld_reduced, representatives))
    withheld_fibers = np.einsum("kr,rij->kij", withheld_phases, blocks, optimize=True)
    fiber_hermiticity = max(
        float(
            np.max(
                np.linalg.norm(fibers - fibers.conj().transpose(0, 2, 1), axis=(1, 2))
            )
        ),
        float(
            np.max(
                np.linalg.norm(
                    withheld_fibers - withheld_fibers.conj().transpose(0, 2, 1),
                    axis=(1, 2),
                )
            )
        ),
    )
    if fiber_hermiticity > hermiticity_tolerance:
        fail("parent fibers violate the frozen Hermiticity tolerance")
    values, vectors = np.linalg.eigh(fibers)
    withheld_values = np.linalg.eigvalsh(withheld_fibers)
    target = values[:, :rank]
    withheld_target = withheld_values[:, :rank]
    external_gap = min(
        float(np.min(values[:, rank] - values[:, rank - 1])),
        float(np.min(withheld_values[:, rank] - withheld_values[:, rank - 1])),
    )
    raw_frames = vectors[:, :, :rank]
    orthonormality = float(
        np.max(
            [
                np.linalg.norm(frame.conj().T @ frame - np.eye(rank))
                for frame in raw_frames
            ]
        )
    )
    if orthonormality > number(
        baseline_result["orthonormality_absolute_tolerance"],
        "orthonormality tolerance",
    ):
        fail("raw frames violate the frozen orthonormality tolerance")
    frames, minimum_overlap = transport(raw_frames)
    reference = np.asarray(
        [
            frame.conj().T @ fiber @ frame
            for frame, fiber in zip(frames, fibers, strict=True)
        ]
    )
    attack = mapping(baseline_result["attack"], "attack")
    constant = number(attack["constant_angle"], "attack constant")
    coefficients = np.asarray(
        [
            number(item, "attack coefficient")
            for item in array(attack["sine_coefficients"], "attack coefficients")
        ]
    )
    attack_angles = np.full(mesh_size, constant)
    for harmonic, coefficient in enumerate(coefficients, start=1):
        attack_angles += coefficient * np.sin(2.0 * np.pi * harmonic * reduced)
    attack_rotations = np.asarray([rotation(float(angle)) for angle in attack_angles])
    attacked_frames = np.asarray(
        [
            frame @ unitary
            for frame, unitary in zip(frames, attack_rotations, strict=True)
        ]
    )
    attacked = np.asarray(
        [
            unitary.conj().T @ matrix @ unitary
            for unitary, matrix in zip(attack_rotations, reference, strict=True)
        ]
    )
    projector_defect = float(
        np.max(
            [
                np.linalg.norm(
                    frame @ frame.conj().T - attacked_frame @ attacked_frame.conj().T
                )
                for frame, attacked_frame in zip(frames, attacked_frames, strict=True)
            ]
        )
    )
    summary = mapping(result["baseline_summary"], "baseline_summary")
    exact(
        summary,
        {
            "external_gap_minimum",
            "minimum_neighbor_or_closure_overlap_singular_value",
            "projector_maximum_frobenius_defect",
        },
        "baseline_summary",
    )
    defects: list[float] = [
        abs(quantity(summary["external_gap_minimum"], "external gap") - external_gap),
        abs(
            number(
                summary["minimum_neighbor_or_closure_overlap_singular_value"],
                "minimum overlap",
            )
            - minimum_overlap
        ),
        abs(
            number(
                summary["projector_maximum_frobenius_defect"],
                "projector defect",
            )
            - projector_defect
        ),
    ]
    if external_gap < quantity(
        baseline_result["external_gap_lower_bound"], "gap bound"
    ):
        fail("reconstructed external gap violates its frozen bound")
    if minimum_overlap <= number(
        baseline_result["overlap_singular_value_threshold"],
        "overlap threshold",
    ):
        fail("reconstructed overlap violates its frozen strict threshold")
    scale = quantity(definition["loss_energy_scale"], "loss scale")
    if scale <= 0.0:
        fail("loss scale must be positive")
    mean = np.trace(reference, axis1=1, axis2=2).real / rank
    reference_values = np.linalg.eigvalsh(reference)
    spectral_base = np.repeat(mean[:, None], rank, axis=1)
    spectral_expected = quadratic(
        np.stack(
            (np.full_like(reference_values, scale), reference_values - spectral_base),
            axis=-1,
        ),
        spectral_base - target,
        scale,
    )
    loss_payload = mapping(result["training_quadratic_losses"], "losses")
    exact(loss_payload, {"spectral", "operator_components"}, "losses")
    spectral_retained = mapping(loss_payload["spectral"], "spectral loss")
    angles = tuple(
        number(item, "alignment angle")
        for item in array(definition["alignment_angles"], "alignment angles")
    )
    if angles != tuple(sorted(set(angles))):
        fail("alignment angles must be unique and increasing")
    identity = np.eye(rank, dtype=np.complex128)
    operator_base = (np.trace(reference, axis1=1, axis2=2) / rank)[
        :, None, None
    ] * identity
    operator_expected = []
    for angle in angles:
        features = np.stack(
            (
                np.broadcast_to(scale * identity, reference.shape),
                conjugate(reference - operator_base, rotation(angle)),
            ),
            axis=-1,
        )
        operator_expected.append(quadratic(features, operator_base - attacked, scale))
    operator_retained = array(loss_payload["operator_components"], "operator losses")
    if len(operator_retained) != len(operator_expected):
        fail("operator loss count differs from the alignment family")

    def check_loss(
        payload_value: object,
        expected: tuple[np.ndarray, np.ndarray, float],
        expected_angle: float | None,
        expected_channel_id: str,
        context: str,
    ) -> None:
        payload = mapping(payload_value, context)
        exact(
            payload,
            {
                "channel_id",
                "alignment_angle",
                "center",
                "quadratic_matrix",
                "minimum_squared_loss",
            },
            context,
        )
        if text(payload["channel_id"], f"{context}.channel_id") != expected_channel_id:
            fail(f"{context} channel identity differs")
        retained_angle = payload["alignment_angle"]
        if expected_angle is None:
            if retained_angle is not None:
                fail(f"{context} must be alignment-invariant")
        elif number(retained_angle, f"{context}.angle") != expected_angle:
            fail(f"{context} angle differs")
        center = np.asarray(pair(payload["center"], f"{context}.center"))
        matrix_rows = array(payload["quadratic_matrix"], f"{context}.matrix")
        matrix = np.asarray([pair(row, f"{context}.matrix row") for row in matrix_rows])
        loss_defects = (
            maximum(center, expected[0]),
            maximum(matrix, expected[1]),
            abs(
                number(payload["minimum_squared_loss"], f"{context}.minimum")
                - expected[2]
            ),
        )
        if max(loss_defects) > quadratic_tolerance:
            fail(f"{context} exceeds the frozen quadratic tolerance")
        defects.extend(loss_defects)

    check_loss(
        spectral_retained,
        spectral_expected,
        None,
        "spectral-training-rms-v1",
        "spectral loss",
    )
    for index, (payload_value, expected_loss, angle) in enumerate(
        zip(operator_retained, operator_expected, angles, strict=True)
    ):
        check_loss(
            payload_value,
            expected_loss,
            angle,
            f"operator-training-rms-angle-{angle:.17g}",
            f"operator loss {index}",
        )
    reference_representatives, reference_blocks = transform(reduced, reference)
    attacked_representatives, attacked_blocks = transform(reduced, attacked)
    if not np.array_equal(reference_representatives, attacked_representatives):
        fail("transform representative inventories differ")
    reconstruction_tolerance = number(
        baseline_result["reconstruction_absolute_tolerance"],
        "reconstruction tolerance",
    )
    reconstruction_defect = max(
        maximum(
            interpolate(reduced, reference_representatives, reference_blocks),
            reference,
        ),
        maximum(
            interpolate(reduced, attacked_representatives, attacked_blocks),
            attacked,
        ),
    )
    if reconstruction_defect > reconstruction_tolerance:
        fail("Fourier reconstruction violates the frozen tolerance")
    withheld_reference = interpolate(
        withheld_reduced, reference_representatives, reference_blocks
    )
    withheld_attacked = interpolate(
        withheld_reduced, attacked_representatives, attacked_blocks
    )
    locality_ranges = tuple(
        integer(item, "locality range")
        for item in array(definition["locality_ranges"], "locality ranges")
    )
    if locality_ranges != tuple(sorted(set(locality_ranges))) or locality_ranges[0] < 0:
        fail("locality ranges must be unique, increasing, and nonnegative")

    def check_evaluation(
        payload_value: object,
        expected_parameter: tuple[float, float],
        expected_angle: float,
        expected_role: str,
        context: str,
    ) -> None:
        payload = mapping(payload_value, context)
        exact(
            payload,
            {
                "role",
                "parameter",
                "selected_alignment_angle",
                "training_spectral_rms_loss",
                "training_operator_rms_loss",
                "withheld_spectral_rms_loss",
                "withheld_operator_rms_loss",
                "locality",
            },
            context,
        )
        if text(payload["role"], f"{context}.role") != expected_role:
            fail(f"{context} role differs")
        parameter = pair(payload["parameter"], f"{context}.parameter")
        defects.extend(
            (
                maximum(np.asarray(parameter), np.asarray(expected_parameter)),
                abs(
                    number(payload["selected_alignment_angle"], f"{context}.angle")
                    - expected_angle
                ),
            )
        )
        train_candidate = candidate(reference, expected_parameter, scale)
        withheld_candidate = candidate(withheld_reference, expected_parameter, scale)
        unitary = rotation(expected_angle)
        values_expected = (
            spectral_rms(train_candidate, target, scale),
            operator_rms(conjugate(train_candidate, unitary), attacked, scale),
            spectral_rms(withheld_candidate, withheld_target, scale),
            operator_rms(
                conjugate(withheld_candidate, unitary), withheld_attacked, scale
            ),
        )
        for name, expected_value in zip(
            (
                "training_spectral_rms_loss",
                "training_operator_rms_loss",
                "withheld_spectral_rms_loss",
                "withheld_operator_rms_loss",
            ),
            values_expected,
            strict=True,
        ):
            defects.append(
                abs(number(payload[name], f"{context}.{name}") - expected_value)
            )
        _, candidate_blocks = transform(reduced, conjugate(train_candidate, unitary))
        localities = array(payload["locality"], f"{context}.locality")
        if len(localities) != len(locality_ranges):
            fail(f"{context} locality count differs")
        for item_value, maximum_range in zip(localities, locality_ranges, strict=True):
            item = mapping(item_value, f"{context}.locality item")
            exact(
                item,
                {
                    "maximum_range",
                    "reference_omitted_block_l2_norm",
                    "attacked_omitted_block_l2_norm",
                    "candidate_omitted_block_l2_norm",
                },
                f"{context}.locality item",
            )
            if integer(item["maximum_range"], "maximum range") != maximum_range:
                fail(f"{context} locality range differs")
            keep = np.abs(reference_representatives) <= maximum_range
            for name, expected_value in (
                (
                    "reference_omitted_block_l2_norm",
                    float(np.linalg.norm(reference_blocks[~keep])),
                ),
                (
                    "attacked_omitted_block_l2_norm",
                    float(np.linalg.norm(attacked_blocks[~keep])),
                ),
                (
                    "candidate_omitted_block_l2_norm",
                    float(np.linalg.norm(candidate_blocks[~keep])),
                ),
            ):
                defects.append(
                    abs(number(item[name], f"{context}.{name}") - expected_value)
                )

    thresholds = []
    for name in ("compatible_thresholds", "separated_thresholds"):
        payload = mapping(definition[name], name)
        exact(
            payload,
            {"case_id", "spectral_rms_threshold", "operator_rms_threshold"},
            name,
        )
        thresholds.append(
            (
                text(payload["case_id"], f"{name}.case_id"),
                number(payload["spectral_rms_threshold"], f"{name}.spectral"),
                number(payload["operator_rms_threshold"], f"{name}.operator"),
            )
        )
    if thresholds[0][0] != "compatible" or thresholds[1][0] != "separated":
        fail("threshold case identities differ from the M3 v1 contract")
    if any(
        threshold <= 0.0
        for _, spectral_threshold, operator_threshold in thresholds
        for threshold in (spectral_threshold, operator_threshold)
    ):
        fail("thresholds must be positive")
    bounds = (
        pair(definition["energy_shift_ratio_bounds"], "shift bounds"),
        pair(definition["splitting_scale_bounds"], "splitting bounds"),
    )
    if any(lower >= upper for lower, upper in bounds) or bounds[1][0] <= 0.0:
        fail("parameter bounds must be ordered with positive splitting scale")
    feasible_by_case = []
    for _, _, operator_threshold in thresholds:
        feasible_by_case.append(
            tuple(
                angle
                for angle, expected in zip(angles, operator_expected, strict=True)
                if domain_minimum(bounds, *expected) <= operator_threshold**2
            )
        )
    if any(not components for components in feasible_by_case):
        fail("each operator admissible set must have a feasible alignment component")
    cases = array(result["cases"], "cases")
    if len(cases) != 2:
        fail("exactly two threshold cases are required")
    witness = pair(definition["compatible_witness"], "compatible witness")
    if any(
        coordinate < lower or coordinate > upper
        for coordinate, (lower, upper) in zip(witness, bounds, strict=True)
    ):
        fail("compatible witness lies outside the frozen domain")
    best_witness_index = min(
        range(len(operator_expected)),
        key=lambda index: squared_loss(witness, *operator_expected[index]),
    )
    compatible = mapping(cases[0], "compatible case")
    case_keys = {
        "thresholds",
        "disposition",
        "feasible_operator_component_angles",
        "common_witness",
        "spectral_certificate_point",
        "operator_certificate_point",
        "separation_lower_bound",
        "separation_upper_bound",
        "separation_resolution",
    }
    exact(compatible, case_keys, "compatible case")
    if compatible["thresholds"] != definition["compatible_thresholds"]:
        fail("compatible case thresholds differ from the definition")
    if compatible["disposition"] != "compatible-witness":
        fail("compatible case has the wrong disposition")
    if (
        tuple(
            number(item, "feasible angle")
            for item in array(
                compatible["feasible_operator_component_angles"], "compatible angles"
            )
        )
        != feasible_by_case[0]
    ):
        fail("compatible feasible component inventory differs")
    common = compatible["common_witness"]
    if common is None:
        fail("compatible case lacks its common witness")
    common_spectral = float(np.sqrt(squared_loss(witness, *spectral_expected)))
    common_operator = float(
        np.sqrt(squared_loss(witness, *operator_expected[best_witness_index]))
    )
    if common_spectral > thresholds[0][1] or common_operator > thresholds[0][2]:
        fail("declared common witness does not satisfy both thresholds")
    check_evaluation(
        common,
        witness,
        angles[best_witness_index],
        "compatible-common-witness",
        "common witness",
    )
    check_evaluation(
        compatible["spectral_certificate_point"],
        witness,
        angles[best_witness_index],
        "compatible-common-witness",
        "compatible spectral point",
    )
    check_evaluation(
        compatible["operator_certificate_point"],
        witness,
        angles[best_witness_index],
        "compatible-common-witness",
        "compatible operator point",
    )
    defects.extend(
        (
            abs(number(compatible["separation_lower_bound"], "compatible lower")),
            abs(number(compatible["separation_upper_bound"], "compatible upper")),
        )
    )
    spectral_point, spectral_lower = axis_extreme(
        *spectral_expected, thresholds[1][1], -1.0
    )
    feasible_indices = [
        index for index, angle in enumerate(angles) if angle in feasible_by_case[1]
    ]
    extrema = [
        (index, *axis_extreme(*operator_expected[index], thresholds[1][2], 1.0))
        for index in feasible_indices
    ]
    selected_index, operator_point, operator_upper = max(
        extrema, key=lambda item: item[2]
    )
    lower = max(0.0, spectral_lower - operator_upper)
    upper = float(
        np.linalg.norm(np.asarray(spectral_point) - np.asarray(operator_point))
    )
    separated = mapping(cases[1], "separated case")
    exact(separated, case_keys, "separated case")
    if separated["thresholds"] != definition["separated_thresholds"]:
        fail("separated case thresholds differ from the definition")
    expected_disposition = (
        "certified-separated"
        if lower > number(definition["separation_resolution"], "resolution")
        else "unresolved"
    )
    if (
        separated["disposition"] != expected_disposition
        or separated["common_witness"] is not None
    ):
        fail("separated case disposition is inconsistent")
    if (
        tuple(
            number(item, "feasible angle")
            for item in array(
                separated["feasible_operator_component_angles"], "separated angles"
            )
        )
        != feasible_by_case[1]
    ):
        fail("separated feasible component inventory differs")
    spectral_best = min(
        range(len(operator_expected)),
        key=lambda index: squared_loss(spectral_point, *operator_expected[index]),
    )
    check_evaluation(
        separated["spectral_certificate_point"],
        spectral_point,
        angles[spectral_best],
        "separated-spectral-boundary",
        "separated spectral point",
    )
    check_evaluation(
        separated["operator_certificate_point"],
        operator_point,
        angles[selected_index],
        "separated-operator-boundary",
        "separated operator point",
    )
    defects.extend(
        (
            abs(number(separated["separation_lower_bound"], "separated lower") - lower),
            abs(number(separated["separation_upper_bound"], "separated upper") - upper),
        )
    )
    resolution = number(definition["separation_resolution"], "resolution")
    for case in (compatible, separated):
        defects.append(
            abs(number(case["separation_resolution"], "case resolution") - resolution)
        )
    maximum_defect = max(defects, default=0.0)
    if maximum_defect > tolerance:
        fail(
            "verification failed: maximum defect "
            f"{maximum_defect:.17g} > {tolerance:.17g}"
        )
    verification_document = {
        "schema": (
            "ksdft2effmass.periodic1d.constrained-admissible-set-"
            "standalone-verification.v1"
        ),
        "passes": True,
        "maximum_absolute_defect": maximum_defect,
        "absolute_tolerance": tolerance,
        "reconstruction": "standalone-frozen-finite-protocol",
        "shared_numerical_dependencies": ["numpy", "scipy"],
    }
    (ROOT / "standalone-verification.json").write_text(
        json.dumps(
            verification_document,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        )
        + "\n",
        encoding="utf-8",
    )
    print(
        "periodic1d_constrained_admissible_set_verification=PASS "
        f"maximum_defect={maximum_defect:.17g} tolerance={tolerance:.17g}"
    )


if __name__ == "__main__":
    main()
