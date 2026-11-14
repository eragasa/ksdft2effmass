#!/usr/bin/env python3
"""Render protocol figures from authenticated retained and planning evidence only."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
from typing import cast

import matplotlib
import numpy as np
from matplotlib.axes import Axes
from matplotlib.colors import Normalize
from matplotlib.figure import Figure
from matplotlib.patches import Patch, Rectangle

type JsonScalar = None | bool | int | float | str
type JsonValue = JsonScalar | list[JsonValue] | dict[str, JsonValue]
type JsonObject = dict[str, JsonValue]
type IntegerPoint = tuple[int, int]
type NumericMap = dict[str, float]

CALCULATION_ROOT = Path(__file__).resolve().parent
FOLDING_RESULT = (
    CALCULATION_ROOT / "executions/folding-null-controls-v1/results/result.json"
)
FINITE_DOMAIN_RESULT = (
    CALCULATION_ROOT
    / "executions/finite-domain-defect-planning-v2/results/case-inventory.json"
)
PARENT_QUALIFICATION_ROOT = CALCULATION_ROOT / "executions/parent-qualification-v1"
PARENT_QUALIFICATION_RESULT = PARENT_QUALIFICATION_ROOT / "results/result.json"
PARENT_QUALIFICATION_VERIFICATION = (
    PARENT_QUALIFICATION_ROOT / "verification/verification.json"
)
PARENT_QUALIFICATION_EXECUTION = PARENT_QUALIFICATION_ROOT / "execution.json"
FOLDING_TOLERANCE = 1.0e-11
FOLDING_RESULT_SHA256 = (
    "8c771b58a135f4ea16412cfbaa825efa9ab1d26f0365a83de10d1d4af1d9b44c"
)
FINITE_DOMAIN_RESULT_SHA256 = (
    "da722ec9042b232162c46fe49e228c14c714665cae35f6043e475d3d3d9a88d5"
)
PARENT_QUALIFICATION_RESULT_SHA256 = (
    "e5626e48ce844e215306fa03630a1faa89519075918032af986727f57ecf9ca5"
)
PARENT_QUALIFICATION_VERIFICATION_SHA256 = (
    "decb9d370ebf2e50b875ab4bb510324c6c708816b9aaa10a637d92748e2145e4"
)
PARENT_QUALIFICATION_EXECUTION_SHA256 = (
    "7bf71907ab39001534c7dd8f25a2180ad27d166f74bbc43f12442002ac4ca77c"
)
SQUARE_EXTENTS = (1, 2, 3, 4, 5, 6, 8, 10, 12, 16)
PARENT_SUPPORT_RADIUS_SQUARED = 18
CORE_RADIUS_SQUARED = 4
FIGURE_STEMS = (
    "folding-null-residuals",
    "folding-null-metric-atlas",
    "finite-domain-inventory",
    "parent-support-collisions",
    "parent-support-equivalence-maps",
    "radius-two-core-equivalence-maps",
    "boundary-twist-mesh",
    "shape-orientation-gallery",
    "evaluation-accounting",
    "seam-oracle-phases",
    "parent-qualification-metric-atlas",
    "parent-truncation-losses",
    "parent-gauge-bridge-residuals",
    "parent-independent-reconstruction",
    "parent-resource-observation",
)


def read_object(path: Path, expected_sha256: str) -> JsonObject:
    """Authenticate and read one retained JSON object."""
    source = path.read_bytes()
    if hashlib.sha256(source).hexdigest() != expected_sha256:
        raise ValueError(f"{path} does not match its retained SHA-256 identity")
    decoded = cast(JsonValue, json.loads(source))
    if type(decoded) is not dict:
        raise ValueError(f"{path} must contain one JSON object")
    return decoded


def require_object(value: JsonValue, name: str) -> JsonObject:
    """Return one exact JSON object."""
    if type(value) is not dict:
        raise ValueError(f"{name} must be an object")
    return value


def require_list(value: JsonValue, name: str) -> list[JsonValue]:
    """Return one exact JSON list."""
    if type(value) is not list:
        raise ValueError(f"{name} must be a list")
    return value


def require_string(value: JsonValue, name: str) -> str:
    """Return one nonempty JSON string."""
    if type(value) is not str or not value:
        raise ValueError(f"{name} must be a nonempty string")
    return value


def require_int(value: JsonValue, name: str) -> int:
    """Return one built-in JSON integer without admitting booleans."""
    if type(value) is not int:
        raise ValueError(f"{name} must be an integer")
    return value


def require_bool(value: JsonValue, name: str) -> bool:
    """Return one exact JSON boolean."""
    if type(value) is not bool:
        raise ValueError(f"{name} must be a boolean")
    return value


def require_float(value: JsonValue, name: str) -> float:
    """Return one finite built-in JSON float."""
    if type(value) is not float or not np.isfinite(value):
        raise ValueError(f"{name} must be a finite float")
    return value


def numeric_map(value: JsonValue, name: str) -> NumericMap:
    """Return one JSON object whose values are exact finite floats."""
    payload = require_object(value, name)
    return {
        key: require_float(metric, f"{name}.{key}") for key, metric in payload.items()
    }


def folding_case_data() -> tuple[
    tuple[str, ...], tuple[NumericMap, ...], tuple[NumericMap, ...]
]:
    """Authenticate and extract labels and metrics for eight folding/null cases."""
    payload = read_object(FOLDING_RESULT, FOLDING_RESULT_SHA256)
    if require_string(payload.get("record_type"), "record_type") != (
        "periodic2d_rank_defect_folding_null_result"
    ):
        raise ValueError("folding/null record_type is not supported")
    if require_list(payload.get("failed_criteria"), "failed_criteria"):
        raise ValueError("the retained folding/null result must preserve a pass")
    definition = require_object(payload.get("definition"), "definition")
    definition_cases = require_list(definition.get("cases"), "definition.cases")
    result_cases = require_list(payload.get("cases"), "cases")
    if len(definition_cases) != 8 or len(result_cases) != 8:
        raise ValueError("the retained folding/null inventory must contain eight cases")

    labels: list[str] = []
    folding_metrics: list[NumericMap] = []
    null_metrics: list[NumericMap] = []
    for index, (definition_value, result_value) in enumerate(
        zip(definition_cases, result_cases, strict=True)
    ):
        case_definition = require_object(definition_value, f"definition.cases[{index}]")
        result_case = require_object(result_value, f"cases[{index}]")
        shape = require_list(case_definition.get("shape"), f"shape[{index}]")
        twist = require_list(
            case_definition.get("twist_turns"), f"twist_turns[{index}]"
        )
        if len(shape) != 2 or len(twist) != 2:
            raise ValueError("each plotting case must remain two-dimensional")
        nx = require_int(shape[0], f"shape[{index}][0]")
        ny = require_int(shape[1], f"shape[{index}][1]")
        phi_x = require_float(twist[0], f"twist[{index}][0]")
        phi_y = require_float(twist[1], f"twist[{index}][1]")
        labels.append(f"{nx}×{ny}\n({phi_x:g},{phi_y:g})")
        folding_metrics.append(
            numeric_map(result_case.get("folding"), f"folding[{index}]")
        )
        null_metrics.append(
            numeric_map(result_case.get("null_extraction"), f"null[{index}]")
        )
    return tuple(labels), tuple(folding_metrics), tuple(null_metrics)


def finite_domain_data() -> tuple[
    JsonObject, tuple[IntegerPoint, ...], tuple[IntegerPoint, ...]
]:
    """Authenticate and extract the version-2 finite-domain geometry inventory."""
    payload = read_object(FINITE_DOMAIN_RESULT, FINITE_DOMAIN_RESULT_SHA256)
    if require_string(payload.get("record_type"), "record_type") != (
        "finite_domain_effects_case_inventory"
    ):
        raise ValueError("finite-domain record_type is not supported")
    if require_string(payload.get("execution_status"), "execution_status") != (
        "not_executed"
    ):
        raise ValueError("finite-domain inventory must remain unexecuted")
    definition = require_object(payload.get("definition"), "definition")

    def shapes(key: str) -> tuple[IntegerPoint, ...]:
        values = require_list(definition.get(key), f"definition.{key}")
        result: list[IntegerPoint] = []
        for index, value in enumerate(values):
            shape = require_list(value, f"definition.{key}[{index}]")
            if len(shape) != 2:
                raise ValueError(f"{key} must remain two-dimensional")
            result.append(
                (
                    require_int(shape[0], f"{key}[{index}][0]"),
                    require_int(shape[1], f"{key}[{index}][1]"),
                )
            )
        return tuple(result)

    area_shapes = shapes("area_shapes")
    shape_shapes = shapes("shape_shapes")
    if area_shapes != tuple((extent, extent) for extent in SQUARE_EXTENTS):
        raise ValueError("square area-control inventory changed")
    if shape_shapes != ((8, 18), (9, 16), (12, 12), (16, 9), (18, 8)):
        raise ValueError("fixed-area shape inventory changed")
    return payload, area_shapes, shape_shapes


def parent_qualification_data() -> tuple[JsonObject, JsonObject, JsonObject]:
    """Authenticate and extract the retained synthetic parent qualification package."""
    result = read_object(
        PARENT_QUALIFICATION_RESULT, PARENT_QUALIFICATION_RESULT_SHA256
    )
    verification = read_object(
        PARENT_QUALIFICATION_VERIFICATION,
        PARENT_QUALIFICATION_VERIFICATION_SHA256,
    )
    execution = read_object(
        PARENT_QUALIFICATION_EXECUTION, PARENT_QUALIFICATION_EXECUTION_SHA256
    )
    if require_string(result.get("record_type"), "parent result record_type") != (
        "periodic2d_rank_defect_parent_qualification_result"
    ):
        raise ValueError("parent qualification result record_type is not supported")
    if require_list(result.get("failed_criteria"), "parent failed_criteria"):
        raise ValueError("the retained parent qualification must preserve a pass")
    if (
        require_string(verification.get("record_type"), "verification record_type")
        != "periodic2d_rank_defect_parent_qualification_verification"
    ):
        raise ValueError("parent verification record_type is not supported")
    if require_string(verification.get("outcome"), "verification outcome") != "passed":
        raise ValueError("the retained parent verification must preserve a pass")
    if not require_bool(
        verification.get("reconstruction_passed"), "reconstruction_passed"
    ):
        raise ValueError("the retained independent reconstruction must preserve a pass")
    if require_string(execution.get("record_type"), "execution record_type") != (
        "periodic2d_rank_defect_parent_qualification_execution"
    ):
        raise ValueError("parent execution record_type is not supported")
    if require_bool(execution.get("defect_campaign_executed"), "defect campaign"):
        raise ValueError("the retained defect campaign must remain unexecuted")
    if require_string(execution.get("result_sha256"), "execution result_sha256") != (
        PARENT_QUALIFICATION_RESULT_SHA256
    ):
        raise ValueError("execution result identity changed")
    if (
        require_string(verification.get("result_sha256"), "verification result_sha256")
        != PARENT_QUALIFICATION_RESULT_SHA256
    ):
        raise ValueError("verification result identity changed")
    return result, verification, execution


def parent_short_label(identifier: str) -> str:
    """Return one compact displayed identity without weakening the wire identity."""
    labels = {
        "isotropic_lambda_0p5_0p5_0": r"isotropic $(0.5,0.5)$",
        "anisotropic_lambda_0p3_0p7_0": r"anisotropic $(0.3,0.7)$",
        "anisotropic_lambda_0p7_0p3_0": r"axis-swapped $(0.7,0.3)$",
        "directional_nearest_neighbor": "directional nearest-neighbor",
        "finite_range_diagonal_nonlocal": "finite-range diagonal",
    }
    try:
        return labels[identifier]
    except KeyError as error:
        raise ValueError(
            f"unsupported parent qualification identity: {identifier}"
        ) from error


def parent_qualification_metric_atlas_figure() -> Figure:
    """Render every retained dimensionless qualification metric by exact identity."""
    result, _, _ = parent_qualification_data()
    definition = require_object(result.get("definition"), "parent definition")
    tolerances = require_object(definition.get("tolerances"), "parent tolerances")
    parent_specs = (
        (
            "hopping_hermiticity_maximum_absolute",
            "coefficient Hermiticity",
            "hopping_hermiticity_absolute",
        ),
        (
            "hopping_symmetry_maximum_absolute",
            "coefficient inversion",
            "hopping_symmetry_absolute",
        ),
        (
            "represented_hermiticity_maximum_absolute",
            "represented Hermiticity",
            "represented_hermiticity_absolute",
        ),
        (
            "gauge_bridge_maximum_absolute",
            "uniform/seam bridge",
            "gauge_bridge_absolute",
        ),
    )
    parent_records = tuple(
        require_object(value, f"parents[{index}]")
        for index, value in enumerate(require_list(result.get("parents"), "parents"))
    )
    perturbation_records = tuple(
        require_object(value, f"perturbations[{index}]")
        for index, value in enumerate(
            require_list(result.get("perturbations"), "perturbations")
        )
    )
    parent_values = np.asarray(
        [
            [
                require_float(record.get(metric), metric)
                / require_float(tolerances.get(tolerance), tolerance)
                for metric, _, tolerance in parent_specs
            ]
            for record in parent_records
        ],
        dtype=np.float64,
    )
    perturbation_specs = (
        (
            "represented_hermiticity_maximum_absolute",
            "represented Hermiticity",
            "represented_hermiticity_absolute",
        ),
        (
            "gauge_bridge_maximum_absolute",
            "uniform/seam bridge",
            "gauge_bridge_absolute",
        ),
    )
    perturbation_values = np.asarray(
        [
            [
                require_float(record.get(metric), metric)
                / require_float(tolerances.get(tolerance), tolerance)
                for metric, _, tolerance in perturbation_specs
            ]
            for record in perturbation_records
        ],
        dtype=np.float64,
    )

    def logarithmic(values: np.ndarray) -> np.ndarray:
        return np.asarray(np.log10(np.maximum(values, 1.0e-16)), dtype=np.float64)

    figure = Figure(figsize=(10.2, 7.4), layout="constrained")
    parent_axes, perturbation_axes = figure.subplots(2, 1)
    normalization = Normalize(vmin=-16.0, vmax=0.0)
    parent_image = parent_axes.imshow(
        logarithmic(parent_values).T,
        aspect="auto",
        cmap="viridis",
        norm=normalization,
    )
    parent_axes.set_xticks(
        np.arange(len(parent_records)),
        [
            parent_short_label(
                require_string(record.get("parent_identifier"), "parent identifier")
            )
            for record in parent_records
        ],
        rotation=12,
        ha="right",
    )
    parent_axes.set_yticks(
        np.arange(len(parent_specs)), [label for _, label, _ in parent_specs]
    )
    parent_axes.set_title("Qualified parent metrics")
    perturbation_axes.imshow(
        logarithmic(perturbation_values).T,
        aspect="auto",
        cmap="viridis",
        norm=normalization,
    )
    perturbation_axes.set_xticks(
        np.arange(len(perturbation_records)),
        [
            parent_short_label(
                require_string(
                    record.get("perturbation_identifier"), "perturbation identifier"
                )
            )
            for record in perturbation_records
        ],
        rotation=8,
        ha="right",
    )
    perturbation_axes.set_yticks(
        np.arange(len(perturbation_specs)),
        [label for _, label, _ in perturbation_specs],
    )
    perturbation_axes.set_title("Frozen perturbation metrics")
    colorbar = figure.colorbar(
        parent_image, ax=[parent_axes, perturbation_axes], pad=0.02
    )
    colorbar.set_label(r"$\log_{10}$(metric / prospective criterion)")
    separability = require_float(
        result.get("maximum_plane_wave_separability_absolute"), "separability"
    )
    separability_tolerance = require_float(
        tolerances.get("separability_absolute"), "separability tolerance"
    )
    separability_ratio = separability / separability_tolerance
    figure.suptitle(
        "Accepted Historical Synthetic Parent Qualification\n"
        f"maximum plane-wave separability ratio: {separability_ratio:.3e}"
    )
    return figure


def parent_truncation_losses_figure() -> Figure:
    """Render inherited radius-18 losses without calling them route defects."""
    result, _, _ = parent_qualification_data()
    records = tuple(
        require_object(value, f"parents[{index}]")
        for index, value in enumerate(require_list(result.get("parents"), "parents"))
    )
    labels = tuple(
        parent_short_label(
            require_string(record.get("parent_identifier"), "parent identifier")
        )
        for record in records
    )
    maximum = tuple(
        require_float(
            record.get("inherited_truncation_maximum_absolute"), "maximum loss"
        )
        for record in records
    )
    frobenius = tuple(
        require_float(record.get("inherited_truncation_frobenius"), "Frobenius loss")
        for record in records
    )
    figure = Figure(figsize=(9.4, 5.8), layout="constrained")
    axes = figure.subplots()
    positions = np.arange(len(labels), dtype=np.float64)
    width = 0.36
    axes.bar(
        positions - width / 2.0,
        maximum,
        width,
        label="Maximum absolute loss",
        color="#2563eb",
    )
    axes.bar(
        positions + width / 2.0,
        frobenius,
        width,
        label="Frobenius loss",
        color="#ea580c",
    )
    axes.set_yscale("log")
    axes.set_xticks(positions, labels, rotation=12, ha="right")
    axes.set_ylabel("inherited represented loss (unitless energy)")
    axes.set_title("Inherited Radius-18 Parent Truncation Losses")
    axes.grid(axis="y", which="both", color="#d1d5db", linewidth=0.6)
    axes.legend(frameon=False)
    return figure


def parent_gauge_bridge_figure() -> Figure:
    """Render retained uniform-link to quotient-seam bridge residuals."""
    result, _, _ = parent_qualification_data()
    definition = require_object(result.get("definition"), "parent definition")
    tolerances = require_object(definition.get("tolerances"), "parent tolerances")
    tolerance = require_float(
        tolerances.get("gauge_bridge_absolute"), "gauge tolerance"
    )
    records = [
        *[
            require_object(value, f"parents[{index}]")
            for index, value in enumerate(
                require_list(result.get("parents"), "parents")
            )
        ],
        *[
            require_object(value, f"perturbations[{index}]")
            for index, value in enumerate(
                require_list(result.get("perturbations"), "perturbations")
            )
        ],
    ]
    labels: list[str] = []
    values: list[float] = []
    for record in records:
        identity = record.get(
            "parent_identifier", record.get("perturbation_identifier")
        )
        labels.append(
            parent_short_label(require_string(identity, "qualified identity"))
        )
        values.append(
            require_float(record.get("gauge_bridge_maximum_absolute"), "gauge bridge")
            / tolerance
        )
    figure = Figure(figsize=(10.0, 5.8), layout="constrained")
    axes = figure.subplots()
    positions = np.arange(len(labels), dtype=np.float64)
    colors = ("#2563eb", "#2563eb", "#2563eb", "#ea580c", "#ea580c")
    axes.bar(positions, values, color=colors)
    axes.axhline(1.0, color="#111827", linestyle="--", label="Prospective criterion")
    axes.set_yscale("log")
    axes.set_xticks(positions, labels, rotation=15, ha="right")
    axes.set_ylabel("maximum bridge residual / criterion")
    axes.set_title("Uniform-Link to Quotient-Seam Gauge Bridge")
    axes.grid(axis="y", which="both", color="#d1d5db", linewidth=0.6)
    axes.legend(frameon=False)
    return figure


def parent_independent_reconstruction_figure() -> Figure:
    """Render the retained aggregate independent-reconstruction comparison."""
    result, verification, _ = parent_qualification_data()
    definition = require_object(result.get("definition"), "parent definition")
    tolerances = require_object(definition.get("tolerances"), "parent tolerances")
    tolerance = require_float(
        tolerances.get("reconstruction_absolute"), "reconstruction tolerance"
    )
    difference = require_float(
        verification.get("maximum_metric_absolute_difference"), "metric difference"
    )
    parent_routes = require_int(
        verification.get("reconstructed_parent_route_evaluations"), "parent routes"
    )
    defect_routes = require_int(
        verification.get("reconstructed_defect_route_evaluations"), "defect routes"
    )
    figure = Figure(figsize=(7.4, 5.6), layout="constrained")
    axes = figure.subplots()
    ratio = difference / tolerance
    axes.bar((0,), (ratio,), width=0.5, color="#059669")
    axes.axhline(1.0, color="#111827", linestyle="--", label="Prospective criterion")
    axes.set_yscale("log")
    axes.set_ylim(max(ratio / 20.0, 1.0e-6), 2.0)
    axes.set_xticks((0,), ("maximum retained metric difference",))
    axes.set_ylabel("independent difference / criterion")
    axes.set_title(
        "Production versus Independent Reconstruction\n"
        f"{parent_routes:,} parent and {defect_routes:,} perturbation routes"
    )
    axes.text(0.0, ratio * 1.25, f"{difference:.3e}", ha="center", va="bottom")
    axes.grid(axis="y", which="both", color="#d1d5db", linewidth=0.6)
    axes.legend(frameon=False)
    return figure


def parent_resource_observation_figure() -> Figure:
    """Render measured calculation and verification resources without a scaling fit."""
    _, verification, execution = parent_qualification_data()
    calculation = require_object(
        execution.get("resource_observation"), "calculation resources"
    )
    independent = require_object(
        verification.get("resource_observation"), "verification resources"
    )
    labels = ("calculation", "independent verification")
    runtimes = (
        require_float(calculation.get("runtime_seconds"), "calculation runtime"),
        require_float(independent.get("runtime_seconds"), "verification runtime"),
    )
    memory_mib = (
        require_int(calculation.get("peak_memory_bytes"), "calculation memory")
        / (1024.0**2),
        require_int(independent.get("peak_memory_bytes"), "verification memory")
        / (1024.0**2),
    )
    figure = Figure(figsize=(9.4, 5.8), layout="constrained")
    runtime_axes, memory_axes = figure.subplots(1, 2)
    positions = np.arange(len(labels), dtype=np.float64)
    runtime_axes.bar(positions, runtimes, color=("#2563eb", "#059669"))
    runtime_axes.set_xticks(positions, labels, rotation=12, ha="right")
    runtime_axes.set_ylabel("measured runtime (s)")
    runtime_axes.set_title("Runtime")
    runtime_axes.grid(axis="y", color="#d1d5db", linewidth=0.6)
    memory_axes.bar(positions, memory_mib, color=("#2563eb", "#059669"))
    memory_axes.set_xticks(positions, labels, rotation=12, ha="right")
    memory_axes.set_ylabel("peak resident memory (MiB)")
    memory_axes.set_title("Peak memory")
    memory_axes.grid(axis="y", color="#d1d5db", linewidth=0.6)
    figure.suptitle(
        "Observed Parent-Qualification Resources\n"
        "complete inventory; maximum represented dimension 256; no scaling fit"
    )
    return figure


def lattice_disk(radius_squared: int) -> tuple[IntegerPoint, ...]:
    """Return ordered integer displacements inside one squared-radius disk."""
    radius = math.isqrt(radius_squared)
    return tuple(
        (x, y)
        for x in range(-radius, radius + 1)
        for y in range(-radius, radius + 1)
        if x * x + y * y <= radius_squared
    )


def quotient_multiplicity(points: tuple[IntegerPoint, ...], extent: int) -> np.ndarray:
    """Count declared integer points in every finite quotient residue."""
    result = np.zeros((extent, extent), dtype=np.int64)
    for x, y in points:
        result[y % extent, x % extent] += 1
    return result


def folding_figure() -> Figure:
    """Render maximum normalized residuals from retained folding/null evidence."""
    labels, folding_metrics, null_metrics = folding_case_data()
    folding_values = tuple(
        max(metrics.values()) / FOLDING_TOLERANCE for metrics in folding_metrics
    )
    null_values = tuple(
        max(metrics.values()) / FOLDING_TOLERANCE for metrics in null_metrics
    )

    figure = Figure(figsize=(9.2, 6.2), layout="constrained")
    axes = figure.subplots()
    positions = np.arange(len(labels), dtype=np.float64)
    width = 0.36
    axes.bar(
        positions - width / 2.0,
        folding_values,
        width,
        label="Maximum folding metric",
        color="#2563eb",
    )
    axes.bar(
        positions + width / 2.0,
        null_values,
        width,
        label="Maximum null-alignment metric",
        color="#ea580c",
    )
    axes.axhline(1.0, color="#111827", linestyle="--", linewidth=1.2, label="Criterion")
    axes.set_yscale("log")
    axes.set_ylim(1.0e-6, 2.0)
    axes.set_xticks(positions, labels)
    axes.set_ylabel(r"maximum residual / $10^{-11}$ criterion")
    axes.set_xlabel("finite shape and boundary twist (turns)")
    axes.set_title("Authored Folding and Null-Alignment Controls")
    axes.grid(axis="y", which="both", color="#d1d5db", linewidth=0.6)
    axes.legend(loc="upper right", frameon=False)
    return figure


def folding_metric_atlas_figure() -> Figure:
    """Render every retained folding and null metric without maximum pooling."""
    labels, folding_metrics, null_metrics = folding_case_data()
    folding_names = (
        "unitarity_maximum_absolute_defect",
        "hermiticity_maximum_absolute_defect",
        "off_diagonal_maximum_absolute",
        "primitive_energy_maximum_absolute_defect",
        "eigenvalue_maximum_absolute_defect",
    )
    null_names = (
        "transform_unitarity_maximum_absolute_defect",
        "recovered_maximum_absolute_defect",
        "recovered_frobenius_defect",
    )
    folding_short = (
        "unitarity",
        "Hermiticity",
        "off diagonal",
        "primitive energy",
        "spectrum",
    )
    null_short = ("transform unitarity", "maximum recovery", "Frobenius recovery")

    def matrix(metrics: tuple[NumericMap, ...], names: tuple[str, ...]) -> np.ndarray:
        values = np.asarray(
            [[case[name] / FOLDING_TOLERANCE for name in names] for case in metrics],
            dtype=np.float64,
        ).transpose()
        return np.log10(np.maximum(values, 1.0e-8))

    figure = Figure(figsize=(10.5, 7.2), layout="constrained")
    folding_axes, null_axes = figure.subplots(2, 1)
    image = folding_axes.imshow(
        matrix(folding_metrics, folding_names),
        aspect="auto",
        cmap="viridis",
        vmin=-8.0,
        vmax=0.0,
    )
    null_axes.imshow(
        matrix(null_metrics, null_names),
        aspect="auto",
        cmap="viridis",
        vmin=-8.0,
        vmax=0.0,
    )
    for axes, names, title in (
        (folding_axes, folding_short, "Folding metrics"),
        (null_axes, null_short, "Null-alignment metrics"),
    ):
        axes.set_yticks(np.arange(len(names)), names)
        axes.set_xticks(np.arange(len(labels)), labels)
        axes.set_title(title)
    figure.colorbar(
        image,
        ax=(folding_axes, null_axes),
        label=r"$\log_{10}($metric / $10^{-11})$; zeros shown at $10^{-8}$",
        shrink=0.86,
    )
    figure.suptitle("Retained Folding/Null Metric Atlas")
    return figure


def finite_domain_figure() -> Figure:
    """Render the retained unexecuted finite-domain inventory."""
    payload, area_shapes, _ = finite_domain_data()
    summary = require_object(payload.get("inventory_summary"), "inventory_summary")
    isotropic_cases = require_int(
        summary.get("isotropic_case_count"), "isotropic_case_count"
    )
    orientation_records = require_int(
        summary.get("orientation_case_count"), "orientation_case_count"
    )
    total_evaluations = require_int(
        summary.get("operator_evaluation_count"), "operator_evaluation_count"
    )
    orientation_evaluations = 3 * orientation_records
    if (isotropic_cases, orientation_records, total_evaluations) != (2268, 324, 3240):
        raise ValueError("finite-domain inventory counts changed")
    if isotropic_cases + orientation_evaluations != total_evaluations:
        raise ValueError("finite-domain operator accounting is inconsistent")

    square_extents = tuple(shape[0] for shape in area_shapes)
    figure = Figure(figsize=(9.2, 5.8), layout="constrained")
    extent_axes, stack_axes = figure.subplots(
        1,
        2,
        gridspec_kw={"width_ratios": (1.25, 1.0)},
    )
    positions = np.arange(len(square_extents), dtype=np.float64)
    colors = ("#7c3aed",) * 4 + ("#ea580c",) * 3 + ("#2563eb",) * 3
    bars = extent_axes.bar(positions, square_extents, color=colors)
    extent_axes.bar_label(bars, fmt="%.0f", padding=2)
    extent_axes.set_xticks(
        positions, tuple(f"{value}×{value}" for value in square_extents)
    )
    extent_axes.tick_params(axis="x", labelrotation=45)
    extent_axes.set_ylim(0.0, 17.5)
    extent_axes.set_ylabel("linear extent in lattice cells")
    extent_axes.set_title("Square area controls")
    extent_axes.grid(axis="y", color="#d1d5db", linewidth=0.6)
    extent_axes.legend(
        handles=(
            Patch(color="#7c3aed", label="1–4: defect-support aliasing"),
            Patch(color="#ea580c", label="5, 6, 8: parent-support aliasing"),
            Patch(color="#2563eb", label="10+: parent support unaliased"),
        ),
        loc="upper left",
        frameon=False,
        fontsize=8,
    )

    stack_axes.barh(
        ("Proposed operator evaluations",),
        (isotropic_cases,),
        color="#2563eb",
        label=f"Isotropic: {isotropic_cases}",
    )
    stack_axes.barh(
        ("Proposed operator evaluations",),
        (orientation_evaluations,),
        left=(isotropic_cases,),
        color="#ea580c",
        label=f"Orientation: {orientation_records} records → {orientation_evaluations}",
    )
    stack_axes.set_xlim(0.0, 3450.0)
    stack_axes.set_xlabel("proposed operator evaluations")
    stack_axes.set_yticks(())
    stack_axes.set_title(f"Unexecuted total: {total_evaluations}")
    stack_axes.text(
        isotropic_cases / 2.0,
        0.0,
        str(isotropic_cases),
        ha="center",
        va="center",
        color="white",
        weight="bold",
    )
    stack_axes.text(
        isotropic_cases + orientation_evaluations / 2.0,
        0.0,
        str(orientation_evaluations),
        ha="center",
        va="center",
        color="white",
        weight="bold",
    )
    stack_axes.legend(loc="upper center", frameon=False, fontsize=8)
    stack_axes.grid(axis="x", color="#d1d5db", linewidth=0.6)
    figure.suptitle("Finite-Domain Sensitivity Planning Inventory", fontsize=15)
    return figure


def parent_support_collisions_figure() -> Figure:
    """Render quotient collision counts for the declared radius-18 support disk."""
    support = lattice_disk(PARENT_SUPPORT_RADIUS_SQUARED)
    if len(support) != 61:
        raise ValueError("declared radius-18 parent support must contain 61 points")
    extents = np.arange(1, 17, dtype=np.int64)
    distinct = np.asarray(
        [np.count_nonzero(quotient_multiplicity(support, int(n))) for n in extents],
        dtype=np.int64,
    )
    collisions = len(support) - distinct

    figure = Figure(figsize=(9.2, 5.8), layout="constrained")
    axes = figure.subplots()
    axes.plot(extents, distinct, marker="o", color="#2563eb", label="distinct residues")
    axes.plot(extents, collisions, marker="s", color="#dc2626", label="collided terms")
    axes.axvline(9.0, color="#111827", linestyle="--", label="first unaliased extent")
    for extent in SQUARE_EXTENTS:
        axes.axvspan(extent - 0.08, extent + 0.08, color="#7c3aed", alpha=0.25)
    axes.set_xticks(extents)
    axes.set_xlabel("square extent N")
    axes.set_ylabel("count from 61 declared support displacements")
    axes.set_title(r"Quotient Aliasing of the Declared $R_x^2+R_y^2\leq18$ Support")
    axes.grid(color="#d1d5db", linewidth=0.6)
    axes.legend(frameon=False)
    return figure


def equivalence_maps_figure(
    points: tuple[IntegerPoint, ...], title: str, colorbar_label: str
) -> Figure:
    """Render residue multiplicities for extents one through eight."""
    figure = Figure(figsize=(11.0, 6.5), layout="constrained")
    axes_grid = np.asarray(figure.subplots(2, 4), dtype=object)
    normalization = Normalize(vmin=0.0, vmax=float(len(points)))
    image = None
    for axes_value, extent in zip(axes_grid.flat, range(1, 9), strict=True):
        axes = cast(Axes, axes_value)
        counts = quotient_multiplicity(points, extent)
        image = axes.imshow(
            counts,
            origin="lower",
            cmap="magma",
            norm=normalization,
            interpolation="nearest",
        )
        axes.set_title(f"{extent}×{extent}")
        axes.set_xticks(range(extent))
        axes.set_yticks(range(extent))
        axes.tick_params(labelsize=6)
        for y in range(extent):
            for x in range(extent):
                value = int(counts[y, x])
                if value > 1:
                    axes.text(
                        x,
                        y,
                        str(value),
                        ha="center",
                        va="center",
                        color="white",
                        fontsize=6,
                        weight="bold",
                    )
    if image is None:
        raise AssertionError("equivalence map inventory cannot be empty")
    figure.colorbar(image, ax=tuple(axes_grid.flat), label=colorbar_label, shrink=0.82)
    figure.suptitle(title, fontsize=15)
    return figure


def boundary_twist_mesh_figure() -> Figure:
    """Render the complete execution-free 9x9 twist mesh."""
    values = np.arange(9, dtype=np.float64) / 9.0
    phi_x, phi_y = np.meshgrid(values, values, indexing="ij")
    indices = np.arange(81, dtype=np.int64).reshape((9, 9))
    figure = Figure(figsize=(7.2, 6.2), layout="constrained")
    axes = figure.subplots()
    scatter = axes.scatter(
        phi_x.ravel(),
        phi_y.ravel(),
        c=indices.ravel(),
        cmap="viridis",
        s=52,
        edgecolor="white",
        linewidth=0.5,
    )
    axes.scatter((0.0,), (0.0,), marker="*", s=180, color="#dc2626", label="Gamma")
    axes.set_xticks(values)
    axes.set_yticks(values)
    axes.set_xticklabels(tuple(f"{index}/9" for index in range(9)), rotation=45)
    axes.set_yticklabels(tuple(f"{index}/9" for index in range(9)))
    axes.set_xlabel(r"$\phi_x$ (turns)")
    axes.set_ylabel(r"$\phi_y$ (turns)")
    axes.set_title("Complete Boundary-Twist Mesh")
    axes.set_aspect("equal")
    axes.grid(color="#d1d5db", linewidth=0.6)
    axes.legend(frameon=False)
    figure.colorbar(scatter, ax=axes, label="canonical twist index")
    return figure


def shape_orientation_gallery_figure() -> Figure:
    """Render fixed-area shapes and the two adopted orientation pairs."""
    _, _, shape_shapes = finite_domain_data()
    figure = Figure(figsize=(10.5, 6.0), layout="constrained")
    shape_axes, orientation_axes = figure.subplots(2, 1)

    for index, (nx, ny) in enumerate(shape_shapes):
        scale = 2.2 / math.sqrt(float(nx * ny))
        width = float(nx) * scale
        height = float(ny) * scale
        center = float(index) * 3.7
        shape_axes.add_patch(
            Rectangle(
                (center - width / 2.0, -height / 2.0),
                width,
                height,
                facecolor="#dbeafe",
                edgecolor="#2563eb",
                linewidth=1.5,
            )
        )
        shape_axes.text(center, -1.55, f"{nx}×{ny}", ha="center", va="top")
    shape_axes.set_xlim(-2.0, 16.8)
    shape_axes.set_ylim(-2.1, 2.1)
    shape_axes.set_aspect("equal")
    shape_axes.set_title("Fixed-area-144 shape controls")
    shape_axes.axis("off")

    pairs = (((8, 18), (18, 8)), ((9, 16), (16, 9)))
    for row, (source, target) in enumerate(pairs):
        y_center = 1.4 - 2.8 * float(row)
        for x_center, shape, color in (
            (1.7, source, "#7c3aed"),
            (7.2, target, "#ea580c"),
        ):
            nx, ny = shape
            scale = 2.0 / math.sqrt(float(nx * ny))
            width = float(nx) * scale
            height = float(ny) * scale
            orientation_axes.add_patch(
                Rectangle(
                    (x_center - width / 2.0, y_center - height / 2.0),
                    width,
                    height,
                    facecolor=f"{color}20",
                    edgecolor=color,
                    linewidth=1.5,
                )
            )
            orientation_axes.text(
                x_center, y_center - 1.35, f"{nx}×{ny}", ha="center", va="top"
            )
        orientation_axes.annotate(
            r"$x\leftrightarrow y$",
            xy=(6.0, y_center),
            xytext=(3.0, y_center),
            ha="center",
            va="center",
            arrowprops={"arrowstyle": "<->", "color": "#111827"},
        )
    orientation_axes.set_xlim(-0.2, 9.2)
    orientation_axes.set_ylim(-2.6, 2.6)
    orientation_axes.set_aspect("equal")
    orientation_axes.set_title("Adopted orientation pairs")
    orientation_axes.axis("off")
    figure.suptitle("Shape and Orientation Planning Gallery", fontsize=15)
    return figure


def evaluation_accounting_figure() -> Figure:
    """Render exact multiplicative accounting for the version-2 inventory."""
    figure = Figure(figsize=(9.2, 5.8), layout="constrained")
    axes = figure.subplots()
    labels = (
        "Isotropic\ngeometry–defect pairs",
        "Isotropic\nevaluations",
        "Orientation\nrecords",
        "Orientation\nevaluations",
        "Total proposed\nevaluations",
    )
    values = (28, 2268, 324, 972, 3240)
    colors = ("#7c3aed", "#2563eb", "#9333ea", "#ea580c", "#111827")
    bars = axes.bar(labels, values, color=colors)
    axes.bar_label(bars, labels=tuple(f"{value:,}" for value in values), padding=3)
    axes.set_ylim(0.0, 3500.0)
    axes.set_ylabel("retained planning count")
    axes.set_title("Version-2 Evaluation Accounting")
    axes.grid(axis="y", color="#d1d5db", linewidth=0.6)
    axes.text(0.0, 410.0, "14 geometries × 2 defects", ha="center", fontsize=9)
    axes.text(1.0, 2450.0, "28 × 81 twists", ha="center", fontsize=9)
    axes.text(2.0, 520.0, "2 pairs × 2 defects × 81", ha="center", fontsize=9)
    axes.text(3.0, 1160.0, "324 records × 3", ha="center", fontsize=9)
    axes.text(4.0, 3400.0, "2268 + 972", ha="center", fontsize=9)
    return figure


def seam_oracle_figure() -> Figure:
    """Render the pending size-six seam oracle without executing an operator."""
    twist = 0.37
    phase_positive = np.exp(2.0j * np.pi * twist)
    phase_negative = np.exp(-2.0j * np.pi * twist)
    figure = Figure(figsize=(10.0, 5.4), layout="constrained")
    phase_axes, ring_axes = figure.subplots(1, 2)

    angles = np.linspace(0.0, 2.0 * np.pi, 500)
    phase_axes.plot(np.cos(angles), np.sin(angles), color="#9ca3af")
    for value, label, color in (
        (1.0 + 0.0j, "noncrossing: 1", "#2563eb"),
        (phase_positive, r"$+1$ seam: $e^{2\pi i0.37}$", "#ea580c"),
        (phase_negative, r"$-1$ seam: $e^{-2\pi i0.37}$", "#7c3aed"),
    ):
        phase_axes.annotate(
            "",
            xy=(value.real, value.imag),
            xytext=(0.0, 0.0),
            arrowprops={"arrowstyle": "->", "color": color, "linewidth": 2.0},
        )
        phase_axes.scatter((value.real,), (value.imag,), color=color, label=label)
    phase_axes.axhline(0.0, color="#d1d5db", linewidth=0.6)
    phase_axes.axvline(0.0, color="#d1d5db", linewidth=0.6)
    phase_axes.set_aspect("equal")
    phase_axes.set_xlim(-1.15, 1.15)
    phase_axes.set_ylim(-1.15, 1.15)
    phase_axes.set_xlabel("real phase")
    phase_axes.set_ylabel("imaginary phase")
    phase_axes.set_title("Oracle phases")
    phase_axes.legend(frameon=False, fontsize=8, loc="lower left")

    site_angles = 2.0 * np.pi * np.arange(6, dtype=np.float64) / 6.0
    x_values = np.cos(site_angles)
    y_values = np.sin(site_angles)
    ring_axes.plot(
        np.append(x_values, x_values[0]),
        np.append(y_values, y_values[0]),
        color="#9ca3af",
    )
    ring_axes.scatter(x_values, y_values, color="#111827", s=45)
    for site, (x_value, y_value) in enumerate(zip(x_values, y_values, strict=True)):
        ring_axes.text(
            x_value * 1.18, y_value * 1.18, str(site), ha="center", va="center"
        )
    ring_axes.annotate(
        "+1 crossing",
        xy=(x_values[0], y_values[0]),
        xytext=(x_values[5], y_values[5]),
        arrowprops={"arrowstyle": "->", "color": "#ea580c", "linewidth": 2.0},
        color="#ea580c",
    )
    ring_axes.annotate(
        "−1 crossing",
        xy=(x_values[5], y_values[5]),
        xytext=(x_values[0], y_values[0]),
        arrowprops={"arrowstyle": "->", "color": "#7c3aed", "linewidth": 2.0},
        color="#7c3aed",
    )
    ring_axes.set_aspect("equal")
    ring_axes.set_xlim(-1.45, 1.45)
    ring_axes.set_ylim(-1.45, 1.45)
    ring_axes.set_title("Size-six quotient seam")
    ring_axes.axis("off")
    figure.suptitle("Pending Exact Seam Oracle at Twist 0.37 Turns", fontsize=15)
    return figure


def write_figure(figure: Figure, output_root: Path, stem: str) -> None:
    """Write deterministic PDF and PNG renderings without replacement."""
    pdf_path = output_root / f"{stem}.pdf"
    png_path = output_root / f"{stem}.png"
    if pdf_path.exists() or png_path.exists():
        raise FileExistsError(f"refusing to overwrite retained figure {stem}")
    with pdf_path.open("xb") as stream:
        figure.savefig(
            stream,
            format="pdf",
            metadata={
                "Creator": "ksdft2effmass periodic2d_rank_defect",
                "Producer": "Matplotlib",
                "CreationDate": None,
                "ModDate": None,
            },
        )
    with png_path.open("xb") as stream:
        figure.savefig(
            stream,
            format="png",
            dpi=180,
            metadata={"Software": "ksdft2effmass periodic2d_rank_defect"},
        )
    figure.clear()


def execute(output_root: Path) -> None:
    """Render all currently supportable retained and planning protocol figures."""
    output_root = output_root.resolve()
    output_root.mkdir(parents=True, exist_ok=True)
    for stem in FIGURE_STEMS:
        if (output_root / f"{stem}.pdf").exists() or (
            output_root / f"{stem}.png"
        ).exists():
            raise FileExistsError(f"refusing to overwrite retained figure {stem}")

    parent_support = lattice_disk(PARENT_SUPPORT_RADIUS_SQUARED)
    radius_two_core = lattice_disk(CORE_RADIUS_SQUARED)
    renderings = (
        (folding_figure(), "folding-null-residuals"),
        (folding_metric_atlas_figure(), "folding-null-metric-atlas"),
        (finite_domain_figure(), "finite-domain-inventory"),
        (parent_support_collisions_figure(), "parent-support-collisions"),
        (
            equivalence_maps_figure(
                parent_support,
                r"Declared Parent-Support Quotient Multiplicity ($R_x^2+R_y^2\leq18$)",
                "primitive support displacements per residue",
            ),
            "parent-support-equivalence-maps",
        ),
        (
            equivalence_maps_figure(
                radius_two_core,
                r"Radius-Two Core Quotient Multiplicity ($R_x^2+R_y^2\leq4$)",
                "core displacements per residue",
            ),
            "radius-two-core-equivalence-maps",
        ),
        (boundary_twist_mesh_figure(), "boundary-twist-mesh"),
        (shape_orientation_gallery_figure(), "shape-orientation-gallery"),
        (evaluation_accounting_figure(), "evaluation-accounting"),
        (seam_oracle_figure(), "seam-oracle-phases"),
        (
            parent_qualification_metric_atlas_figure(),
            "parent-qualification-metric-atlas",
        ),
        (parent_truncation_losses_figure(), "parent-truncation-losses"),
        (parent_gauge_bridge_figure(), "parent-gauge-bridge-residuals"),
        (
            parent_independent_reconstruction_figure(),
            "parent-independent-reconstruction",
        ),
        (parent_resource_observation_figure(), "parent-resource-observation"),
    )
    with matplotlib.rc_context(
        {
            "font.family": "DejaVu Sans",
            "axes.spines.top": False,
            "axes.spines.right": False,
            "figure.facecolor": "white",
            "axes.facecolor": "white",
        }
    ):
        for figure, stem in renderings:
            write_figure(figure, output_root, stem)


def main() -> None:
    """Parse an explicit output directory and render the current protocol atlas."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-root", type=Path, required=True)
    arguments = parser.parse_args()
    execute(arguments.output_root)


if __name__ == "__main__":
    main()
