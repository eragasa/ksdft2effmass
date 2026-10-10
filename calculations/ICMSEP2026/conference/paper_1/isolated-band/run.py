#!/usr/bin/env python3
"""Produce the frozen Conference Paper 1 isolated-band result and figure."""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import cast

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

from ksdft2effmass.analysis.model_systems import PeriodicFourierPotential1D
from ksdft2effmass.operators import ScalarQuantity, Unitless, VectorQuantity
from ksdft2effmass.periodic1d import (
    Periodic1DFourierHamiltonianToyModel,
    Periodic1DIsolatedBandCalculationDefinition,
    Periodic1DIsolatedBandCalculationResult,
    Periodic1DIsolatedBandCalculator,
    Periodic1DIsolatedBandResultJsonSerializer,
    Periodic1DIsolatedBandResultVerifier,
)

type JsonScalar = None | bool | int | float | str
type JsonValue = JsonScalar | list[JsonValue] | dict[str, JsonValue]

HERE = Path(__file__).resolve().parent
INPUT_PATH = HERE / "input.json"
RESULT_PATH = HERE / "result.json"
FIGURE_DATA_PATH = HERE / "figure-data.csv"
FIGURE_PATH = HERE / "isolated-band-summary.png"
INPUT_SCHEMA = "ksdft2effmass.periodic1d.isolated-band-calculation-input.v1"


def _object(value: JsonValue, context: str) -> dict[str, JsonValue]:
    if type(value) is not dict:
        raise TypeError(f"{context} must be an object")
    return value


def _array(value: JsonValue, context: str) -> list[JsonValue]:
    if type(value) is not list:
        raise TypeError(f"{context} must be an array")
    return value


def _keys(value: dict[str, JsonValue], expected: set[str], context: str) -> None:
    if set(value) != expected:
        raise ValueError(f"{context} fields do not match schema")


def _string(value: JsonValue, context: str) -> str:
    if type(value) is not str or not value:
        raise TypeError(f"{context} must be a nonempty string")
    return value


def _float(value: JsonValue, context: str) -> float:
    if type(value) is not float or not np.isfinite(value):
        raise TypeError(f"{context} must be a finite JSON float")
    return value


def _integer(value: JsonValue, context: str) -> int:
    if type(value) is not int:
        raise TypeError(f"{context} must be a JSON integer")
    return value


def _float_tuple(value: JsonValue, context: str) -> tuple[float, ...]:
    values = _array(value, context)
    return tuple(_float(item, f"{context} item") for item in values)


def _integer_tuple(value: JsonValue, context: str) -> tuple[int, ...]:
    values = _array(value, context)
    return tuple(_integer(item, f"{context} item") for item in values)


def _load_input() -> dict[str, JsonValue]:
    decoded = cast(JsonValue, json.loads(INPUT_PATH.read_text(encoding="utf-8")))
    root = _object(decoded, "input")
    _keys(
        root,
        {
            "schema",
            "calculation_id",
            "evidence_class",
            "model",
            "parent_representation",
            "reduction",
            "tolerances",
            "scope",
            "figure",
        },
        "input",
    )
    if _string(root["schema"], "schema") != INPUT_SCHEMA:
        raise ValueError("unsupported input schema")
    _string(root["evidence_class"], "evidence_class")
    scope = _object(root["scope"], "scope")
    _keys(scope, {"included", "excluded"}, "scope")
    for name in ("included", "excluded"):
        for item in _array(scope[name], f"scope.{name}"):
            _string(item, f"scope.{name} item")
    figure = _object(root["figure"], "figure")
    _keys(figure, {"filename", "dpi"}, "figure")
    if _string(figure["filename"], "figure.filename") != FIGURE_PATH.name:
        raise ValueError("figure filename must match the retained path")
    if _integer(figure["dpi"], "figure.dpi") <= 0:
        raise ValueError("figure.dpi must be positive")
    return root


def _definition(
    root: dict[str, JsonValue],
) -> Periodic1DIsolatedBandCalculationDefinition:
    model_data = _object(root["model"], "model")
    _keys(
        model_data,
        {
            "model_id",
            "lattice_period",
            "reciprocal_vector",
            "recoil_energy",
            "constant_coefficient",
            "cosine_coefficients",
            "sine_coefficients",
            "unit",
            "duality_absolute_tolerance",
        },
        "model",
    )
    if _string(model_data["unit"], "model.unit") != "dimensionless":
        raise ValueError("this protocol requires dimensionless model quantities")
    unit = Unitless()
    potential = PeriodicFourierPotential1D(
        period=ScalarQuantity(
            _float(model_data["lattice_period"], "model.lattice_period"), unit
        ),
        constant_coefficient=ScalarQuantity(
            _float(model_data["constant_coefficient"], "model.constant_coefficient"),
            unit,
        ),
        cosine_coefficients=VectorQuantity(
            np.asarray(
                _float_tuple(
                    model_data["cosine_coefficients"],
                    "model.cosine_coefficients",
                ),
                dtype=np.float64,
            ),
            unit,
        ),
        sine_coefficients=VectorQuantity(
            np.asarray(
                _float_tuple(
                    model_data["sine_coefficients"], "model.sine_coefficients"
                ),
                dtype=np.float64,
            ),
            unit,
        ),
    )
    model = Periodic1DFourierHamiltonianToyModel(
        identity=_string(model_data["model_id"], "model.model_id"),
        potential=potential,
        reciprocal_vector=ScalarQuantity(
            _float(model_data["reciprocal_vector"], "model.reciprocal_vector"),
            unit,
        ),
        recoil_energy=ScalarQuantity(
            _float(model_data["recoil_energy"], "model.recoil_energy"), unit
        ),
        duality_absolute_tolerance=_float(
            model_data["duality_absolute_tolerance"],
            "model.duality_absolute_tolerance",
        ),
    )

    parent = _object(root["parent_representation"], "parent_representation")
    _keys(
        parent,
        {
            "plane_wave_cutoffs",
            "plane_wave_reference_cutoff",
            "production_plane_wave_cutoff",
            "finite_difference_points",
            "sample_reduced_momenta",
            "compared_band_count",
        },
        "parent_representation",
    )
    reduction = _object(root["reduction"], "reduction")
    _keys(
        reduction,
        {
            "reciprocal_training_mesh_size",
            "hopping_ranges",
            "withheld_mesh_size",
            "withheld_mesh_rule",
        },
        "reduction",
    )
    if (
        _string(reduction["withheld_mesh_rule"], "reduction.withheld_mesh_rule")
        != "staggered-uniform-disjoint-v1"
    ):
        raise ValueError("unsupported withheld mesh rule")
    tolerances = _object(root["tolerances"], "tolerances")
    _keys(
        tolerances,
        {
            "coordinate_absolute",
            "reconstruction_absolute",
            "hermiticity_absolute",
            "parseval_absolute",
            "imaginary_absolute",
        },
        "tolerances",
    )
    return Periodic1DIsolatedBandCalculationDefinition(
        calculation_id=_string(root["calculation_id"], "calculation_id"),
        parent_model=model,
        plane_wave_cutoffs=_integer_tuple(
            parent["plane_wave_cutoffs"], "parent_representation.plane_wave_cutoffs"
        ),
        plane_wave_reference_cutoff=_integer(
            parent["plane_wave_reference_cutoff"],
            "parent_representation.plane_wave_reference_cutoff",
        ),
        production_plane_wave_cutoff=_integer(
            parent["production_plane_wave_cutoff"],
            "parent_representation.production_plane_wave_cutoff",
        ),
        finite_difference_points=_integer_tuple(
            parent["finite_difference_points"],
            "parent_representation.finite_difference_points",
        ),
        parent_sample_reduced_momenta=_float_tuple(
            parent["sample_reduced_momenta"],
            "parent_representation.sample_reduced_momenta",
        ),
        compared_band_count=_integer(
            parent["compared_band_count"],
            "parent_representation.compared_band_count",
        ),
        reciprocal_mesh_size=_integer(
            reduction["reciprocal_training_mesh_size"],
            "reduction.reciprocal_training_mesh_size",
        ),
        hopping_ranges=_integer_tuple(
            reduction["hopping_ranges"], "reduction.hopping_ranges"
        ),
        withheld_mesh_size=_integer(
            reduction["withheld_mesh_size"], "reduction.withheld_mesh_size"
        ),
        coordinate_absolute_tolerance=_float(
            tolerances["coordinate_absolute"], "tolerances.coordinate_absolute"
        ),
        reconstruction_absolute_tolerance=_float(
            tolerances["reconstruction_absolute"],
            "tolerances.reconstruction_absolute",
        ),
        hermiticity_absolute_tolerance=ScalarQuantity(
            _float(
                tolerances["hermiticity_absolute"],
                "tolerances.hermiticity_absolute",
            ),
            unit,
        ),
        parseval_absolute_tolerance=ScalarQuantity(
            _float(tolerances["parseval_absolute"], "tolerances.parseval_absolute"),
            unit,
        ),
        imaginary_absolute_tolerance=ScalarQuantity(
            _float(
                tolerances["imaginary_absolute"],
                "tolerances.imaginary_absolute",
            ),
            unit,
        ),
    )


def _write_figure_data(result: Periodic1DIsolatedBandCalculationResult) -> None:
    if type(result) is not Periodic1DIsolatedBandCalculationResult:
        raise TypeError("result must be Periodic1DIsolatedBandCalculationResult")
    with FIGURE_DATA_PATH.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.writer(stream, lineterminator="\n")
        writer.writerow(
            (
                "hopping_range_cells",
                "training_maximum_absolute_error",
                "withheld_maximum_absolute_error",
                "direct_mediated_coefficient_l2_defect",
                "omitted_hopping_l2_norm",
            )
        )
        for item in result.range_study:
            writer.writerow(
                (
                    item.maximum_range,
                    format(
                        item.training_error.maximum_absolute_error.magnitude, ".17g"
                    ),
                    format(
                        item.withheld_error.maximum_absolute_error.magnitude, ".17g"
                    ),
                    format(
                        item.direct_mediated_comparison.coefficient_l2_frobenius_defect.magnitude,
                        ".17g",
                    ),
                    format(item.truncation.omitted_block_l2_norm, ".17g"),
                )
            )


def _write_figure(result: Periodic1DIsolatedBandCalculationResult, dpi: int) -> None:
    if type(result) is not Periodic1DIsolatedBandCalculationResult:
        raise TypeError("result must be Periodic1DIsolatedBandCalculationResult")
    figure, axes = plt.subplots(2, 2, figsize=(10.0, 7.2), constrained_layout=True)
    plane_wave = axes[0, 0]
    plane_wave.semilogy(
        [item.cutoff for item in result.plane_wave_convergence],
        [
            item.maximum_absolute_error.magnitude
            for item in result.plane_wave_convergence
        ],
        "o-",
    )
    plane_wave.set(
        xlabel="Plane-wave cutoff P",
        ylabel="Maximum error / $E_G$",
        title="(a) Plane-wave refinement",
    )
    plane_wave.grid(True, alpha=0.3)

    finite_difference = axes[0, 1]
    finite_difference.loglog(
        [item.point_count for item in result.finite_difference_convergence],
        [
            item.maximum_absolute_error.magnitude
            for item in result.finite_difference_convergence
        ],
        "o-",
    )
    finite_difference.set(
        xlabel="Grid points",
        ylabel="Maximum error / $E_G$",
        title="(b) Finite-difference refinement",
    )
    finite_difference.grid(True, alpha=0.3)

    hopping = axes[1, 0]
    complete = result.complete_transform.hopping_model
    hopping.semilogy(
        complete.representatives,
        [abs(block.magnitude[0, 0]) for block in complete.hopping_blocks],
        "o",
        markersize=3,
    )
    hopping.set(
        xlabel="Cell displacement R",
        ylabel="$|t_R|/E_G$",
        title="(c) Complete hopping decay",
    )
    hopping.grid(True, alpha=0.3)

    ranges = axes[1, 1]
    range_values = [item.maximum_range for item in result.range_study]
    ranges.semilogy(
        range_values,
        [
            item.training_error.maximum_absolute_error.magnitude
            for item in result.range_study
        ],
        "o-",
        label="training",
    )
    ranges.semilogy(
        range_values,
        [
            item.withheld_error.maximum_absolute_error.magnitude
            for item in result.range_study
        ],
        "s-",
        label="withheld",
    )
    ranges.semilogy(
        range_values,
        [
            item.direct_mediated_comparison.coefficient_l2_frobenius_defect.magnitude
            for item in result.range_study
        ],
        "^-",
        label="route coefficient defect",
    )
    ranges.set(
        xlabel="Hopping range",
        ylabel="Diagnostic / $E_G$",
        title="(d) Finite-range diagnostics",
    )
    ranges.grid(True, alpha=0.3)
    ranges.legend(fontsize="small")

    figure.savefig(
        FIGURE_PATH,
        dpi=dpi,
        metadata={"Software": "ksdft2effmass"},
    )
    plt.close(figure)


def main() -> None:
    """Run the frozen calculation and retain deterministic data products."""
    root = _load_input()
    definition = _definition(root)
    result = Periodic1DIsolatedBandCalculator().execute(definition)
    verification = Periodic1DIsolatedBandResultVerifier().execute(result)
    if not verification.passes:
        raise RuntimeError("in-memory independent verification did not pass")
    RESULT_PATH.write_bytes(
        Periodic1DIsolatedBandResultJsonSerializer().serialize(result)
    )
    _write_figure_data(result)
    figure = _object(root["figure"], "figure")
    _write_figure(result, _integer(figure["dpi"], "figure.dpi"))
    print(f"wrote {RESULT_PATH.relative_to(HERE.parent.parent.parent.parent.parent)}")
    print(
        f"wrote {FIGURE_DATA_PATH.relative_to(HERE.parent.parent.parent.parent.parent)}"
    )
    print(f"wrote {FIGURE_PATH.relative_to(HERE.parent.parent.parent.parent.parent)}")


if __name__ == "__main__":
    main()
