#!/usr/bin/env python3
"""Produce the prospectively frozen local synthetic M3 evidence package."""

from __future__ import annotations

import csv
import json
import platform
import sys
from importlib.metadata import version
from pathlib import Path
from typing import Never, cast

import matplotlib.pyplot as plt
import numpy as np

from ksdft2effmass.operators import ComplexMatrixQuantity, ScalarQuantity, Unitless
from ksdft2effmass.periodic1d import (
    Periodic1DAdmissibleSetThresholds,
    Periodic1DBlockHamiltonianToyModel,
    Periodic1DConstrainedAdmissibleSetCalculationDefinition,
    Periodic1DConstrainedAdmissibleSetCalculationResult,
    Periodic1DConstrainedAdmissibleSetCalculator,
    Periodic1DConstrainedAdmissibleSetResultJsonSerializer,
    Periodic1DConstrainedAdmissibleSetResultVerifier,
    Periodic1DMultibandAlignmentCalculationDefinition,
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
    result = float(cast(int | float, value))
    if not np.isfinite(result):
        fail(f"{context} must be finite")
    return result


def numeric_pair(value: object, context: str) -> tuple[float, float]:
    """Decode a finite length-two array."""
    if type(value) is not list or len(value) != 2:
        fail(f"{context} must be a length-two array")
    return number(value[0], f"{context}[0]"), number(value[1], f"{context}[1]")


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


def decode_baseline(
    value: object,
) -> Periodic1DMultibandAlignmentCalculationDefinition:
    """Decode the exact nested M2 definition."""
    payload = mapping(value, "multiband_baseline")
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
        "multiband_baseline",
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
    parent = Periodic1DBlockHamiltonianToyModel(
        text(parent_payload["model_id"], "parent_model.model_id"),
        BlockHoppingModel1D(
            quantity(parent_payload["reciprocal_period"], "reciprocal_period"),
            tuple(
                integer(item, f"representatives[{index}]")
                for index, item in enumerate(representatives_raw)
            ),
            tuple(
                complex_matrix(item, f"hopping_blocks[{index}]")
                for index, item in enumerate(blocks_raw)
            ),
        ),
        quantity(
            parent_payload["hermiticity_absolute_tolerance"],
            "parent_model.hermiticity_absolute_tolerance",
        ),
    )
    attack = mapping(payload["attack"], "attack")
    exact_keys(attack, {"constant_angle", "sine_coefficients"}, "attack")
    coefficients = attack["sine_coefficients"]
    ranges = payload["hopping_ranges"]
    if type(coefficients) is not list or type(ranges) is not list:
        fail("attack coefficients and hopping ranges must be arrays")
    return Periodic1DMultibandAlignmentCalculationDefinition(
        text(payload["calculation_id"], "baseline.calculation_id"),
        parent,
        integer(payload["retained_rank"], "retained_rank"),
        integer(payload["reciprocal_mesh_size"], "reciprocal_mesh_size"),
        integer(payload["withheld_mesh_size"], "withheld_mesh_size"),
        tuple(
            integer(item, f"hopping_ranges[{index}]")
            for index, item in enumerate(ranges)
        ),
        number(attack["constant_angle"], "attack.constant_angle"),
        tuple(
            number(item, f"sine_coefficients[{index}]")
            for index, item in enumerate(coefficients)
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
            payload["coordinate_absolute_tolerance"], "coordinate_absolute_tolerance"
        ),
        number(
            payload["reconstruction_absolute_tolerance"],
            "reconstruction_absolute_tolerance",
        ),
        quantity(
            payload["hermiticity_absolute_tolerance"], "hermiticity_absolute_tolerance"
        ),
        number(
            payload["verification_absolute_tolerance"],
            "baseline.verification_absolute_tolerance",
        ),
    )


def decode_thresholds(value: object, context: str) -> Periodic1DAdmissibleSetThresholds:
    """Strictly decode one threshold pair."""
    payload = mapping(value, context)
    exact_keys(
        payload,
        {"case_id", "spectral_rms_threshold", "operator_rms_threshold"},
        context,
    )
    return Periodic1DAdmissibleSetThresholds(
        text(payload["case_id"], f"{context}.case_id"),
        number(payload["spectral_rms_threshold"], f"{context}.spectral"),
        number(payload["operator_rms_threshold"], f"{context}.operator"),
    )


def decode_definition(
    path: Path,
) -> Periodic1DConstrainedAdmissibleSetCalculationDefinition:
    """Strictly decode every prospectively frozen M3 control."""
    payload = mapping(json.loads(path.read_text(encoding="utf-8")), "root")
    exact_keys(
        payload,
        {
            "schema",
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
        },
        "root",
    )
    literal_expectations = {
        "schema": "ksdft2effmass.periodic1d.constrained-admissible-set-input.v1",
        "candidate_family": (
            "trace-plus-energy-shift-and-positive-traceless-splitting-v1"
        ),
        "alignment_family": "finite-one-global-real-rotation-v1",
        "loss_normalization": "sqrt(sum-frobenius-squared/(N*rank))/scale",
        "separation_metric": "euclidean-parameter-distance",
    }
    for name, expected in literal_expectations.items():
        if text(payload[name], name) != expected:
            fail(f"{name} must be {expected!r}")
    if payload["parameter_order"] != ["energy_shift_ratio", "splitting_scale"]:
        fail("parameter_order does not match the v1 contract")
    angles = payload["alignment_angles"]
    ranges = payload["locality_ranges"]
    if type(angles) is not list or type(ranges) is not list:
        fail("alignment_angles and locality_ranges must be arrays")
    return Periodic1DConstrainedAdmissibleSetCalculationDefinition(
        text(payload["calculation_id"], "calculation_id"),
        decode_baseline(payload["multiband_baseline"]),
        numeric_pair(payload["energy_shift_ratio_bounds"], "energy_shift_ratio_bounds"),
        numeric_pair(payload["splitting_scale_bounds"], "splitting_scale_bounds"),
        tuple(
            number(item, f"alignment_angles[{index}]")
            for index, item in enumerate(angles)
        ),
        quantity(payload["loss_energy_scale"], "loss_energy_scale"),
        decode_thresholds(payload["compatible_thresholds"], "compatible_thresholds"),
        decode_thresholds(payload["separated_thresholds"], "separated_thresholds"),
        numeric_pair(payload["compatible_witness"], "compatible_witness"),
        tuple(
            integer(item, f"locality_ranges[{index}]")
            for index, item in enumerate(ranges)
        ),
        number(payload["separation_resolution"], "separation_resolution"),
        number(payload["quadratic_absolute_tolerance"], "quadratic_absolute_tolerance"),
        number(
            payload["verification_absolute_tolerance"],
            "verification_absolute_tolerance",
        ),
    )


def write_figure_data(
    result: Periodic1DConstrainedAdmissibleSetCalculationResult,
) -> None:
    """Write retained boundary and witness rows used by the summary figure."""
    with (ROOT / "figure-data.csv").open("w", encoding="utf-8", newline="") as stream:
        writer = csv.writer(stream, lineterminator="\n")
        writer.writerow(
            (
                "case_id",
                "role",
                "energy_shift_ratio",
                "splitting_scale",
                "training_spectral_rms_loss",
                "training_operator_rms_loss",
                "withheld_spectral_rms_loss",
                "withheld_operator_rms_loss",
            )
        )
        for case in result.cases:
            evaluations = [
                case.spectral_certificate_point,
                case.operator_certificate_point,
            ]
            if case.common_witness is not None:
                evaluations = [case.common_witness]
            for item in evaluations:
                writer.writerow(
                    (
                        case.thresholds.case_id,
                        item.role,
                        *item.parameter,
                        item.training_spectral_rms_loss,
                        item.training_operator_rms_loss,
                        item.withheld_spectral_rms_loss,
                        item.withheld_operator_rms_loss,
                    )
                )


def write_figure(result: Periodic1DConstrainedAdmissibleSetCalculationResult) -> None:
    """Plot frozen training admissible boundaries in parameter space."""
    definition = result.definition
    shift = np.linspace(*definition.energy_shift_ratio_bounds, 401)
    splitting = np.linspace(*definition.splitting_scale_bounds, 401)
    xx, yy = np.meshgrid(shift, splitting)
    fig, axes = plt.subplots(1, 2, figsize=(9.2, 4.1), constrained_layout=True)
    for axis, case in zip(axes, result.cases, strict=True):
        spectral = np.asarray(
            [
                [result.spectral_loss.rms_loss((float(x), float(y))) for x in shift]
                for y in splitting
            ]
        )
        operator = np.minimum.reduce(
            [
                np.asarray(
                    [
                        [loss.rms_loss((float(x), float(y))) for x in shift]
                        for y in splitting
                    ]
                )
                for loss in result.operator_losses
            ]
        )
        axis.contour(
            xx,
            yy,
            spectral,
            levels=[case.thresholds.spectral_rms_threshold],
            colors=["#1f77b4"],
            linewidths=2.0,
        )
        axis.contour(
            xx,
            yy,
            operator,
            levels=[case.thresholds.operator_rms_threshold],
            colors=["#d62728"],
            linewidths=2.0,
        )
        if case.common_witness is not None:
            axis.scatter(
                *case.common_witness.parameter,
                marker="*",
                s=100,
                color="#2ca02c",
                label="common witness",
            )
        else:
            axis.scatter(
                *case.spectral_certificate_point.parameter,
                marker="o",
                color="#1f77b4",
                label="spectral boundary",
            )
            axis.scatter(
                *case.operator_certificate_point.parameter,
                marker="s",
                color="#d62728",
                label="operator boundary",
            )
        axis.set_title(case.thresholds.case_id)
        axis.set_xlabel("energy-shift ratio")
        axis.set_ylabel("splitting scale")
        axis.grid(alpha=0.2)
        axis.legend(fontsize=8)
    fig.suptitle("M3 frozen training admissible sets")
    fig.savefig(ROOT / "constrained-admissible-sets-summary.png", dpi=180)
    plt.close(fig)


def write_software_record() -> None:
    """Record the local software environment without claiming reproducibility."""
    document = {
        "schema": "ksdft2effmass.synthetic-calculation-software.v1",
        "python": platform.python_version(),
        "implementation": platform.python_implementation(),
        "platform": platform.platform(),
        "packages": {
            name: version(name)
            for name in ("ksdft2effmass", "numpy", "scipy", "matplotlib")
        },
        "executable": sys.executable,
        "execution_scope": "local-synthetic-no-external-calculator",
    }
    (ROOT / "software.json").write_text(
        json.dumps(document, sort_keys=True, separators=(",", ":")) + "\n",
        encoding="utf-8",
    )


def write_report(result: Periodic1DConstrainedAdmissibleSetCalculationResult) -> None:
    """Write a concise scope-bounded retained report."""
    compatible, separated = result.cases
    witness = compatible.common_witness
    witness_parameter = None if witness is None else witness.parameter
    lines = [
        "# Constrained admissible-set result",
        "",
        (
            "This is local synthetic evidence under frozen finite controls. It is "
            "not material validation, uncertainty quantification, continuum "
            "convergence, or a general alignment-optimizer result."
        ),
        "",
        "## Outcomes",
        "",
        (
            f"- compatible disposition: `{compatible.disposition.value}` at "
            f"witness `{witness_parameter}`;"
        ),
        f"- separated disposition: `{separated.disposition.value}`;",
        (
            "- certified Euclidean parameter separation: "
            f"`[{separated.separation_lower_bound:.17g}, "
            f"{separated.separation_upper_bound:.17g}]`;"
        ),
        f"- frozen separation resolution: `{separated.separation_resolution:.17g}`;",
        (
            "- feasible operator components in separated case: "
            f"`{separated.feasible_operator_component_angles}`."
        ),
        "",
        (
            "Training values define the quadratics, admissible sets, witness, and "
            "certificate. The 257 staggered evaluation coordinates are disjoint "
            "from training and do not alter those objects."
        ),
        "",
    ]
    (ROOT / "report.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    """Execute the frozen local synthetic calculation and write artifacts."""
    definition = decode_definition(ROOT / "input.json")
    result = Periodic1DConstrainedAdmissibleSetCalculator().execute(definition)
    (ROOT / "result.json").write_bytes(
        Periodic1DConstrainedAdmissibleSetResultJsonSerializer().serialize(result)
    )
    verification = Periodic1DConstrainedAdmissibleSetResultVerifier().execute(result)
    verification_document = {
        "schema": "ksdft2effmass.periodic1d.constrained-admissible-set-verification.v1",
        "dimensionless_maximum_absolute_defect": (
            verification.dimensionless_maximum_absolute_defect
        ),
        "energy_maximum_absolute_defect": {
            "magnitude": verification.energy_maximum_absolute_defect.magnitude,
            "unit": "1",
        },
        "absolute_tolerance": verification.absolute_tolerance,
        "passes": verification.passes,
    }
    (ROOT / "verification.json").write_text(
        json.dumps(verification_document, sort_keys=True, separators=(",", ":")) + "\n",
        encoding="utf-8",
    )
    write_figure_data(result)
    write_figure(result)
    write_report(result)
    write_software_record()
    if not verification.passes:
        fail("independent library verification did not pass")


if __name__ == "__main__":
    main()
