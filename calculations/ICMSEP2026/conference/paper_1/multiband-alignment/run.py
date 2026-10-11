#!/usr/bin/env python3
"""Produce the frozen local synthetic M2 result and presentation artifacts."""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Never

import matplotlib.pyplot as plt
import numpy as np

from ksdft2effmass.operators import ComplexMatrixQuantity, ScalarQuantity, Unitless
from ksdft2effmass.periodic1d import (
    Periodic1DBlockHamiltonianToyModel,
    Periodic1DMultibandAlignmentCalculationDefinition,
    Periodic1DMultibandAlignmentCalculationResult,
    Periodic1DMultibandAlignmentCalculator,
    Periodic1DMultibandAlignmentResultJsonSerializer,
)
from ksdft2effmass.solid_state import BlockHoppingModel1D

ROOT = Path(__file__).resolve().parent


def fail(message: str) -> Never:
    """Reject malformed frozen input without structural fallbacks."""
    raise ValueError(message)


def exact_keys(value: dict[str, object], expected: set[str], context: str) -> None:
    """Require exactly the declared fields."""
    if set(value) != expected:
        fail(f"{context} fields must be exactly {sorted(expected)}")


def mapping(value: object, context: str) -> dict[str, object]:
    """Require a JSON object."""
    if type(value) is not dict:
        fail(f"{context} must be an object")
    return value


def text(value: object, context: str) -> str:
    """Require a nonempty built-in string."""
    if type(value) is not str or not value:
        fail(f"{context} must be a nonempty string")
    return value


def integer(value: object, context: str) -> int:
    """Require a built-in integer and reject booleans."""
    if type(value) is not int:
        fail(f"{context} must be an integer")
    return value


def number(value: object, context: str) -> float:
    """Require a finite JSON number and reject booleans."""
    if type(value) not in (int, float):
        fail(f"{context} must be numeric")
    result = float(value)
    if not np.isfinite(result):
        fail(f"{context} must be finite")
    return result


def quantity(value: object, context: str) -> ScalarQuantity:
    """Decode a scalar unitless quantity."""
    payload = mapping(value, context)
    exact_keys(payload, {"magnitude", "unit"}, context)
    if text(payload["unit"], f"{context}.unit") != "1":
        fail(f"{context}.unit must be '1'")
    return ScalarQuantity(
        number(payload["magnitude"], f"{context}.magnitude"), Unitless()
    )


def complex_matrix(value: object, context: str) -> ComplexMatrixQuantity:
    """Decode a rectangular complex-pair matrix with unit `1`."""
    payload = mapping(value, context)
    exact_keys(payload, {"magnitude", "unit"}, context)
    if text(payload["unit"], f"{context}.unit") != "1":
        fail(f"{context}.unit must be '1'")
    raw = payload["magnitude"]
    if type(raw) is not list or not raw:
        fail(f"{context}.magnitude must be a nonempty matrix")
    rows: list[list[complex]] = []
    width: int | None = None
    for row_index, raw_row in enumerate(raw):
        if type(raw_row) is not list or not raw_row:
            fail(f"{context}.magnitude[{row_index}] must be a nonempty row")
        if width is None:
            width = len(raw_row)
        elif len(raw_row) != width:
            fail(f"{context}.magnitude must be rectangular")
        row: list[complex] = []
        for column_index, pair in enumerate(raw_row):
            if type(pair) is not list or len(pair) != 2:
                fail(f"{context}[{row_index},{column_index}] must be [real,imag]")
            row.append(
                complex(
                    number(pair[0], f"{context}[{row_index},{column_index}].real"),
                    number(pair[1], f"{context}[{row_index},{column_index}].imag"),
                )
            )
        rows.append(row)
    return ComplexMatrixQuantity(np.asarray(rows, dtype=np.complex128), Unitless())


def decode_definition(path: Path) -> Periodic1DMultibandAlignmentCalculationDefinition:
    """Strictly decode the prospectively frozen calculation definition."""
    raw = json.loads(path.read_text(encoding="utf-8"))
    payload = mapping(raw, "root")
    exact_keys(
        payload,
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
        "root",
    )
    parent_payload = mapping(payload["parent_model"], "parent_model")
    exact_keys(
        parent_payload,
        {
            "model_id",
            "reciprocal_period",
            "representatives",
            "hopping_blocks",
            "hermiticity_absolute_tolerance",
        },
        "parent_model",
    )
    representatives_raw = parent_payload["representatives"]
    blocks_raw = parent_payload["hopping_blocks"]
    if type(representatives_raw) is not list or type(blocks_raw) is not list:
        fail("parent representatives and hopping_blocks must be arrays")
    representatives = tuple(
        integer(value, f"representatives[{index}]")
        for index, value in enumerate(representatives_raw)
    )
    blocks = tuple(
        complex_matrix(value, f"hopping_blocks[{index}]")
        for index, value in enumerate(blocks_raw)
    )
    hopping_model = BlockHoppingModel1D(
        quantity(parent_payload["reciprocal_period"], "reciprocal_period"),
        representatives,
        blocks,
    )
    parent = Periodic1DBlockHamiltonianToyModel(
        text(parent_payload["model_id"], "parent_model.model_id"),
        hopping_model,
        quantity(
            parent_payload["hermiticity_absolute_tolerance"],
            "parent_model.hermiticity_absolute_tolerance",
        ),
    )
    attack = mapping(payload["attack"], "attack")
    exact_keys(attack, {"constant_angle", "sine_coefficients"}, "attack")
    sine_raw = attack["sine_coefficients"]
    ranges_raw = payload["hopping_ranges"]
    if type(sine_raw) is not list or type(ranges_raw) is not list:
        fail("attack coefficients and hopping ranges must be arrays")
    return Periodic1DMultibandAlignmentCalculationDefinition(
        text(payload["calculation_id"], "calculation_id"),
        parent,
        integer(payload["retained_rank"], "retained_rank"),
        integer(payload["reciprocal_mesh_size"], "reciprocal_mesh_size"),
        integer(payload["withheld_mesh_size"], "withheld_mesh_size"),
        tuple(
            integer(value, f"hopping_ranges[{index}]")
            for index, value in enumerate(ranges_raw)
        ),
        number(attack["constant_angle"], "attack.constant_angle"),
        tuple(
            number(value, f"attack.sine_coefficients[{index}]")
            for index, value in enumerate(sine_raw)
        ),
        quantity(payload["external_gap_lower_bound"], "external_gap_lower_bound"),
        number(
            payload["overlap_singular_value_threshold"],
            "overlap_singular_value_threshold",
        ),
        number(
            payload["orthonormality_absolute_tolerance"],
            "orthonormality_absolute_tolerance",
        ),
        number(
            payload["coordinate_absolute_tolerance"],
            "coordinate_absolute_tolerance",
        ),
        number(
            payload["reconstruction_absolute_tolerance"],
            "reconstruction_absolute_tolerance",
        ),
        quantity(
            payload["hermiticity_absolute_tolerance"],
            "hermiticity_absolute_tolerance",
        ),
        number(
            payload["verification_absolute_tolerance"],
            "verification_absolute_tolerance",
        ),
    )


def write_figure_data(
    result: Periodic1DMultibandAlignmentCalculationResult,
) -> None:
    """Write the finite-range values used by the summary figure."""
    if type(result) is not Periodic1DMultibandAlignmentCalculationResult:
        fail("result has the wrong type")
    with (ROOT / "figure-data.csv").open("w", encoding="utf-8", newline="") as stream:
        writer = csv.writer(stream, lineterminator="\n")
        writer.writerow(
            (
                "maximum_range",
                "reference_omitted_block_l2_norm",
                "attacked_omitted_block_l2_norm",
                "aligned_omitted_block_l2_norm",
                "reference_withheld_maximum_absolute_spectral_error",
                "attacked_withheld_maximum_absolute_spectral_error",
                "aligned_withheld_maximum_absolute_spectral_error",
            )
        )
        for item in result.range_study:
            writer.writerow(
                (
                    item.maximum_range,
                    item.reference_truncation.omitted_block_l2_norm,
                    item.attacked_truncation.omitted_block_l2_norm,
                    item.aligned_truncation.omitted_block_l2_norm,
                    item.reference_withheld_error.maximum_absolute_error.magnitude,
                    item.attacked_withheld_error.maximum_absolute_error.magnitude,
                    item.aligned_withheld_error.maximum_absolute_error.magnitude,
                )
            )


def write_figure(result: Periodic1DMultibandAlignmentCalculationResult) -> None:
    """Render the retained summary directly from the typed result."""
    if type(result) is not Periodic1DMultibandAlignmentCalculationResult:
        fail("result has the wrong type")
    figure, axes = plt.subplots(2, 2, figsize=(9.4, 6.8), constrained_layout=True)
    coordinates = result.training_target.coordinates.magnitude
    for band in range(result.training_target.band_count):
        axes[0, 0].plot(
            coordinates, result.training_target.eigenvalues.magnitude[:, band]
        )
    axes[0, 0].set(
        xlabel="reduced momentum", ylabel="energy", title="Retained parent spectrum"
    )
    diagnostics = result.diagnostics
    labels = ("attack", "pointwise", "global")
    frame_values = (
        diagnostics.attack_frame_maximum_frobenius_defect,
        diagnostics.pointwise_alignment.frame_maximum_frobenius_defect,
        diagnostics.constrained_frame_maximum_frobenius_defect,
    )
    axes[0, 1].bar(labels, frame_values)
    axes[0, 1].set_yscale("log")
    axes[0, 1].set(ylabel="maximum frame defect", title="Alignment channels")
    ranges = [item.maximum_range for item in result.range_study]
    for label, values in (
        (
            "transported",
            [
                item.reference_truncation.omitted_block_l2_norm
                for item in result.range_study
            ],
        ),
        (
            "attacked",
            [
                item.attacked_truncation.omitted_block_l2_norm
                for item in result.range_study
            ],
        ),
        (
            "pointwise aligned",
            [
                item.aligned_truncation.omitted_block_l2_norm
                for item in result.range_study
            ],
        ),
    ):
        axes[1, 0].semilogy(ranges, values, marker="o", label=label)
    axes[1, 0].set(
        xlabel="hopping range",
        ylabel="omitted block norm",
        title="Gauge-dependent locality",
    )
    axes[1, 0].legend()
    for label, values in (
        (
            "transported",
            [
                item.reference_withheld_error.maximum_absolute_error.magnitude
                for item in result.range_study
            ],
        ),
        (
            "attacked",
            [
                item.attacked_withheld_error.maximum_absolute_error.magnitude
                for item in result.range_study
            ],
        ),
        (
            "pointwise aligned",
            [
                item.aligned_withheld_error.maximum_absolute_error.magnitude
                for item in result.range_study
            ],
        ),
    ):
        axes[1, 1].semilogy(ranges, values, marker="o", label=label)
    axes[1, 1].set(
        xlabel="hopping range",
        ylabel="withheld maximum spectral error",
        title="Disjoint withheld diagnostics",
    )
    axes[1, 1].legend()
    figure.savefig(ROOT / "multiband-alignment-summary.png", dpi=180)
    plt.close(figure)


def write_report(result: Periodic1DMultibandAlignmentCalculationResult) -> None:
    """Write a bounded human-readable result report."""
    if type(result) is not Periodic1DMultibandAlignmentCalculationResult:
        fail("result has the wrong type")
    diagnostics = result.diagnostics
    last = result.range_study[-1]
    reference_error = last.reference_withheld_error.maximum_absolute_error.magnitude
    attacked_error = last.attacked_withheld_error.maximum_absolute_error.magnitude
    aligned_error = last.aligned_withheld_error.maximum_absolute_error.magnitude
    lines = [
        "# M2 multiband-alignment result",
        "",
        "The frozen local synthetic calculation completed. This is bounded "
        "numerical evidence, not material validation or uncertainty quantification.",
        "",
        f"- minimum external gap: `{diagnostics.external_gap_minimum.magnitude:.17g}`",
        "- minimum neighboring/closure overlap singular value: "
        f"`{diagnostics.transport.minimum_overlap_singular_value:.17g}`",
        "- attacked-frame maximum Frobenius defect: "
        f"`{diagnostics.attack_frame_maximum_frobenius_defect:.17g}`",
        "- pointwise-aligned frame maximum Frobenius defect: "
        f"`{diagnostics.pointwise_alignment.frame_maximum_frobenius_defect:.17g}`",
        "- one-global-unitary frame maximum Frobenius defect: "
        f"`{diagnostics.constrained_frame_maximum_frobenius_defect:.17g}`",
        "- attacked operator maximum Frobenius defect: "
        f"`{diagnostics.attacked_operator_maximum_frobenius_defect.magnitude:.17g}`",
        "- pointwise-aligned operator maximum Frobenius defect: "
        f"`{diagnostics.pointwise_operator_maximum_frobenius_defect.magnitude:.17g}`",
        "- one-global-unitary operator maximum Frobenius defect: "
        f"`{diagnostics.constrained_operator_maximum_frobenius_defect.magnitude:.17g}`",
        f"- range-{last.maximum_range} transported withheld maximum spectral "
        f"error: `{reference_error:.17g}`",
        f"- range-{last.maximum_range} attacked withheld maximum spectral "
        f"error: `{attacked_error:.17g}`",
        f"- range-{last.maximum_range} pointwise-aligned withheld maximum spectral "
        f"error: `{aligned_error:.17g}`",
        "",
        "Independent reconstruction is retained separately in `verification.json`.",
        "",
    ]
    report = "\n".join(lines)
    (ROOT / "report.md").write_text(report, encoding="utf-8")


def main() -> None:
    """Decode, calculate, and retain the frozen local synthetic package."""
    definition = decode_definition(ROOT / "input.json")
    result = Periodic1DMultibandAlignmentCalculator().execute(definition)
    encoded = Periodic1DMultibandAlignmentResultJsonSerializer().serialize(result)
    (ROOT / "result.json").write_bytes(encoded)
    write_figure_data(result)
    write_figure(result)
    write_report(result)


if __name__ == "__main__":
    main()
