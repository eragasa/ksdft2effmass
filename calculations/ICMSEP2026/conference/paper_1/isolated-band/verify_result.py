#!/usr/bin/env python3
"""Independently reconstruct the retained isolated-band result document."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import cast

import numpy as np
from scipy import sparse  # type: ignore[import-untyped]
from scipy.sparse.linalg import eigsh  # type: ignore[import-untyped]

type JsonScalar = None | bool | int | float | str
type JsonValue = JsonScalar | list[JsonValue] | dict[str, JsonValue]

HERE = Path(__file__).resolve().parent
INPUT_PATH = HERE / "input.json"
RESULT_PATH = HERE / "result.json"
VERIFICATION_PATH = HERE / "verification.json"
INPUT_SCHEMA = "ksdft2effmass.periodic1d.isolated-band-calculation-input.v1"
RESULT_SCHEMA = "ksdft2effmass.periodic1d.isolated-band-calculation-result.v1"
VERIFICATION_SCHEMA = (
    "ksdft2effmass.periodic1d.isolated-band-calculation-verification.v1"
)


@dataclass(frozen=True, slots=True)
class Controls:
    """Hold strictly decoded defining controls for independent reconstruction."""

    calculation_id: str
    model_id: str
    period: float
    reciprocal_vector: float
    recoil_energy: float
    constant: float
    cosine: tuple[float, ...]
    sine: tuple[float, ...]
    duality_tolerance: float
    plane_wave_cutoffs: tuple[int, ...]
    reference_cutoff: int
    production_cutoff: int
    finite_difference_points: tuple[int, ...]
    parent_momenta: tuple[float, ...]
    band_count: int
    training_size: int
    hopping_ranges: tuple[int, ...]
    withheld_size: int
    coordinate_tolerance: float
    tolerance: float
    hermiticity_tolerance: float
    parseval_tolerance: float
    imaginary_tolerance: float

    @property
    def training_momenta(self) -> np.ndarray:
        representatives = np.arange(
            -self.training_size // 2,
            self.training_size // 2,
            dtype=np.float64,
        )
        return representatives / float(self.training_size)

    @property
    def withheld_momenta(self) -> np.ndarray:
        offset = 1.0 / float(self.training_size + 1)
        return -0.5 + (
            np.arange(self.withheld_size, dtype=np.float64) + offset
        ) / float(self.withheld_size)

    @property
    def representatives(self) -> np.ndarray:
        return np.arange(
            -self.training_size // 2,
            self.training_size // 2,
            dtype=np.int64,
        )


def _load(path: Path) -> dict[str, JsonValue]:
    decoded = cast(JsonValue, json.loads(path.read_text(encoding="utf-8")))
    return _object(decoded, path.name)


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


def _integer(value: JsonValue, context: str) -> int:
    if type(value) is not int:
        raise TypeError(f"{context} must be an integer")
    return value


def _real(value: JsonValue, context: str) -> float:
    if type(value) is int:
        result = float(value)
    elif type(value) is float:
        result = value
    else:
        raise TypeError(f"{context} must be a real number")
    if not np.isfinite(result):
        raise ValueError(f"{context} must be finite")
    return result


def _boolean(value: JsonValue, context: str) -> bool:
    if type(value) is not bool:
        raise TypeError(f"{context} must be a boolean")
    return value


def _integer_tuple(value: JsonValue, context: str) -> tuple[int, ...]:
    return tuple(_integer(item, f"{context} item") for item in _array(value, context))


def _real_tuple(value: JsonValue, context: str) -> tuple[float, ...]:
    return tuple(_real(item, f"{context} item") for item in _array(value, context))


def _quantity(value: JsonValue, context: str, unit: str = "dimensionless") -> float:
    quantity = _object(value, context)
    _keys(quantity, {"magnitude", "unit"}, context)
    if _string(quantity["unit"], f"{context}.unit") != unit:
        raise ValueError(f"{context} uses an unexpected unit")
    return _real(quantity["magnitude"], f"{context}.magnitude")


def _vector_quantity(value: JsonValue, context: str) -> np.ndarray:
    quantity = _object(value, context)
    _keys(quantity, {"magnitude", "unit"}, context)
    if _string(quantity["unit"], f"{context}.unit") != "dimensionless":
        raise ValueError(f"{context} must be dimensionless")
    return np.asarray(
        _real_tuple(quantity["magnitude"], f"{context}.magnitude"),
        dtype=np.float64,
    )


def _matrix_quantity(value: JsonValue, context: str) -> np.ndarray:
    quantity = _object(value, context)
    _keys(quantity, {"magnitude", "unit"}, context)
    if _string(quantity["unit"], f"{context}.unit") != "dimensionless":
        raise ValueError(f"{context} must be dimensionless")
    rows = _array(quantity["magnitude"], f"{context}.magnitude")
    matrix = np.asarray(
        [
            [_real(item, f"{context} item") for item in _array(row, context)]
            for row in rows
        ],
        dtype=np.float64,
    )
    if matrix.ndim != 2:
        raise ValueError(f"{context} must contain a matrix")
    return matrix


def _complex_matrix(value: JsonValue, context: str) -> np.ndarray:
    quantity = _object(value, context)
    _keys(quantity, {"magnitude", "unit"}, context)
    if _string(quantity["unit"], f"{context}.unit") != "dimensionless":
        raise ValueError(f"{context} must be dimensionless")
    rows = _array(quantity["magnitude"], f"{context}.magnitude")
    decoded_rows: list[list[complex]] = []
    for row in rows:
        decoded_row: list[complex] = []
        for pair_value in _array(row, context):
            pair = _array(pair_value, f"{context} complex pair")
            if len(pair) != 2:
                raise ValueError(f"{context} complex pairs must have length two")
            decoded_row.append(
                complex(
                    _real(pair[0], f"{context} real part"),
                    _real(pair[1], f"{context} imaginary part"),
                )
            )
        decoded_rows.append(decoded_row)
    matrix = np.asarray(decoded_rows, dtype=np.complex128)
    if matrix.ndim != 2:
        raise ValueError(f"{context} must contain a complex matrix")
    return matrix


def _spectrum(value: JsonValue, context: str) -> tuple[np.ndarray, np.ndarray]:
    spectrum = _object(value, context)
    _keys(spectrum, {"coordinates", "reciprocal_period", "eigenvalues"}, context)
    coordinates = _vector_quantity(spectrum["coordinates"], f"{context}.coordinates")
    reciprocal_period = _quantity(
        spectrum["reciprocal_period"], f"{context}.reciprocal_period"
    )
    if reciprocal_period <= 0.0:
        raise ValueError(f"{context}.reciprocal_period must be positive")
    eigenvalues = _matrix_quantity(spectrum["eigenvalues"], f"{context}.eigenvalues")
    if eigenvalues.shape[0] != coordinates.size:
        raise ValueError(f"{context} sample counts do not agree")
    return coordinates / reciprocal_period, eigenvalues


def _decode_controls(input_document: dict[str, JsonValue]) -> Controls:
    _keys(
        input_document,
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
    if _string(input_document["schema"], "input.schema") != INPUT_SCHEMA:
        raise ValueError("unsupported input schema")
    model = _object(input_document["model"], "input.model")
    _keys(
        model,
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
        "input.model",
    )
    if _string(model["unit"], "input.model.unit") != "dimensionless":
        raise ValueError("input model must be dimensionless")
    _string(model["model_id"], "input.model.model_id")
    _real(model["duality_absolute_tolerance"], "input.model.duality_tolerance")
    parent = _object(input_document["parent_representation"], "input.parent")
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
        "input.parent",
    )
    reduction = _object(input_document["reduction"], "input.reduction")
    _keys(
        reduction,
        {
            "reciprocal_training_mesh_size",
            "hopping_ranges",
            "withheld_mesh_size",
            "withheld_mesh_rule",
        },
        "input.reduction",
    )
    if (
        _string(reduction["withheld_mesh_rule"], "input.reduction.mesh_rule")
        != "staggered-uniform-disjoint-v1"
    ):
        raise ValueError("unsupported withheld mesh rule")
    tolerances = _object(input_document["tolerances"], "input.tolerances")
    _keys(
        tolerances,
        {
            "coordinate_absolute",
            "reconstruction_absolute",
            "hermiticity_absolute",
            "parseval_absolute",
            "imaginary_absolute",
        },
        "input.tolerances",
    )
    scope = _object(input_document["scope"], "input.scope")
    _keys(scope, {"included", "excluded"}, "input.scope")
    for name in ("included", "excluded"):
        for value in _array(scope[name], f"input.scope.{name}"):
            _string(value, f"input.scope.{name} item")
    figure = _object(input_document["figure"], "input.figure")
    _keys(figure, {"filename", "dpi"}, "input.figure")
    if _string(figure["filename"], "input.figure.filename") != (
        "isolated-band-summary.png"
    ):
        raise ValueError("input figure filename does not match retained figure")
    if _integer(figure["dpi"], "input.figure.dpi") <= 0:
        raise ValueError("input figure dpi must be positive")
    return Controls(
        calculation_id=_string(
            input_document["calculation_id"], "input.calculation_id"
        ),
        model_id=_string(model["model_id"], "input.model.model_id"),
        period=_real(model["lattice_period"], "input.model.lattice_period"),
        reciprocal_vector=_real(
            model["reciprocal_vector"], "input.model.reciprocal_vector"
        ),
        recoil_energy=_real(model["recoil_energy"], "input.model.recoil_energy"),
        constant=_real(
            model["constant_coefficient"], "input.model.constant_coefficient"
        ),
        cosine=_real_tuple(
            model["cosine_coefficients"], "input.model.cosine_coefficients"
        ),
        sine=_real_tuple(model["sine_coefficients"], "input.model.sine_coefficients"),
        duality_tolerance=_real(
            model["duality_absolute_tolerance"], "input.model.duality_tolerance"
        ),
        plane_wave_cutoffs=_integer_tuple(
            parent["plane_wave_cutoffs"], "input.parent.plane_wave_cutoffs"
        ),
        reference_cutoff=_integer(
            parent["plane_wave_reference_cutoff"], "input.parent.reference_cutoff"
        ),
        production_cutoff=_integer(
            parent["production_plane_wave_cutoff"],
            "input.parent.production_cutoff",
        ),
        finite_difference_points=_integer_tuple(
            parent["finite_difference_points"], "input.parent.fd_points"
        ),
        parent_momenta=_real_tuple(
            parent["sample_reduced_momenta"], "input.parent.sample_momenta"
        ),
        band_count=_integer(parent["compared_band_count"], "input.parent.band_count"),
        training_size=_integer(
            reduction["reciprocal_training_mesh_size"],
            "input.reduction.training_size",
        ),
        hopping_ranges=_integer_tuple(
            reduction["hopping_ranges"], "input.reduction.hopping_ranges"
        ),
        withheld_size=_integer(
            reduction["withheld_mesh_size"], "input.reduction.withheld_size"
        ),
        coordinate_tolerance=_real(
            tolerances["coordinate_absolute"], "input.tolerances.coordinate"
        ),
        tolerance=_real(
            tolerances["reconstruction_absolute"], "input.tolerances.reconstruction"
        ),
        hermiticity_tolerance=_real(
            tolerances["hermiticity_absolute"], "input.tolerances.hermiticity"
        ),
        parseval_tolerance=_real(
            tolerances["parseval_absolute"], "input.tolerances.parseval"
        ),
        imaginary_tolerance=_real(
            tolerances["imaginary_absolute"], "input.tolerances.imaginary"
        ),
    )


def _plane_wave(
    controls: Controls, cutoff: int, momenta: np.ndarray, bands: int
) -> np.ndarray:
    indices = np.arange(-cutoff, cutoff + 1, dtype=np.float64)
    values: list[np.ndarray] = []
    for momentum in momenta:
        matrix = np.diag(
            controls.recoil_energy * np.square(float(momentum) + indices)
            + controls.constant
        ).astype(np.complex128)
        for harmonic, (cosine, sine) in enumerate(
            zip(controls.cosine, controls.sine, strict=True), start=1
        ):
            size = matrix.shape[0] - harmonic
            if size <= 0:
                continue
            matrix += np.diag(np.full(size, 0.5 * (cosine + 1j * sine)), harmonic)
            matrix += np.diag(np.full(size, 0.5 * (cosine - 1j * sine)), -harmonic)
        values.append(np.linalg.eigvalsh(matrix)[:bands])
    return np.asarray(values, dtype=np.float64)


def _finite_difference(
    controls: Controls, points: int, momenta: np.ndarray, bands: int
) -> np.ndarray:
    coordinates = controls.period * np.arange(points, dtype=np.float64) / float(points)
    potential = np.full(points, controls.constant, dtype=np.float64)
    for harmonic, (cosine, sine) in enumerate(
        zip(controls.cosine, controls.sine, strict=True), start=1
    ):
        angle = 2.0 * np.pi * harmonic * coordinates / controls.period
        potential += cosine * np.cos(angle) + sine * np.sin(angle)
    reciprocal_spacing = 2.0 * np.pi / float(points)
    link = controls.recoil_energy / reciprocal_spacing**2
    values: list[np.ndarray] = []
    for momentum in momenta:
        matrix = sparse.diags(
            (
                np.full(points - 1, -link, dtype=np.complex128),
                (2.0 * link + potential).astype(np.complex128),
                np.full(points - 1, -link, dtype=np.complex128),
            ),
            offsets=(-1, 0, 1),
            shape=(points, points),
            format="lil",
            dtype=np.complex128,
        )
        seam = -link * np.exp(-2j * np.pi * float(momentum))
        matrix[0, points - 1] = seam
        matrix[points - 1, 0] = np.conjugate(seam)
        eigenvalues = eigsh(
            matrix.tocsr(),
            k=bands,
            which="SA",
            return_eigenvectors=False,
            v0=np.full(
                points,
                1.0 / np.sqrt(float(points)),
                dtype=np.float64,
            ),
        )
        values.append(np.sort(np.asarray(eigenvalues, dtype=np.float64)))
    return np.asarray(values, dtype=np.float64)


def _direct_fourier(
    momenta: np.ndarray, values: np.ndarray, representatives: np.ndarray
) -> np.ndarray:
    return np.asarray(
        [
            np.mean(values * np.exp(-2j * np.pi * momenta * int(representative)))
            for representative in representatives
        ],
        dtype=np.complex128,
    )


def _interpolate(
    momenta: np.ndarray, representatives: np.ndarray, blocks: np.ndarray
) -> np.ndarray:
    return np.asarray(
        np.exp(2j * np.pi * np.outer(momenta, representatives)) @ blocks,
        dtype=np.complex128,
    )


def _maximum_defect(candidate: np.ndarray, reference: np.ndarray) -> float:
    return float(np.max(np.abs(candidate - reference)))


def _definition_matches(
    controls: Controls, result_document: dict[str, JsonValue]
) -> bool:
    definition = _object(result_document["definition"], "result.definition")
    _keys(
        definition,
        {
            "calculation_id",
            "parent_model",
            "plane_wave_cutoffs",
            "plane_wave_reference_cutoff",
            "production_plane_wave_cutoff",
            "finite_difference_points",
            "parent_sample_reduced_momenta",
            "compared_band_count",
            "reciprocal_mesh_size",
            "hopping_ranges",
            "withheld_mesh_size",
            "withheld_mesh_rule",
            "withheld_reduced_momenta",
            "coordinate_absolute_tolerance",
            "reconstruction_absolute_tolerance",
            "hermiticity_absolute_tolerance",
            "parseval_absolute_tolerance",
            "imaginary_absolute_tolerance",
        },
        "result.definition",
    )
    model = _object(definition["parent_model"], "result.definition.parent_model")
    _keys(
        model,
        {
            "model_id",
            "model_role",
            "period",
            "constant_coefficient",
            "cosine_coefficients",
            "sine_coefficients",
            "reciprocal_vector",
            "recoil_energy",
            "duality_absolute_tolerance",
        },
        "result.definition.parent_model",
    )
    if (
        _string(definition["calculation_id"], "result.calculation_id")
        != controls.calculation_id
    ):
        return False
    return (
        _string(model["model_id"], "result.model_id") == controls.model_id
        and _string(model["model_role"], "result.model_role") == "toy"
        and _quantity(model["period"], "result.model.period") == controls.period
        and _quantity(model["constant_coefficient"], "result.model.constant")
        == controls.constant
        and tuple(_vector_quantity(model["cosine_coefficients"], "result.model.cosine"))
        == controls.cosine
        and tuple(_vector_quantity(model["sine_coefficients"], "result.model.sine"))
        == controls.sine
        and _quantity(model["reciprocal_vector"], "result.model.reciprocal")
        == controls.reciprocal_vector
        and _quantity(model["recoil_energy"], "result.model.recoil")
        == controls.recoil_energy
        and _real(model["duality_absolute_tolerance"], "result.model.duality_tolerance")
        == controls.duality_tolerance
        and _integer_tuple(definition["plane_wave_cutoffs"], "result.cutoffs")
        == controls.plane_wave_cutoffs
        and _integer(definition["plane_wave_reference_cutoff"], "result.reference")
        == controls.reference_cutoff
        and _integer(definition["production_plane_wave_cutoff"], "result.production")
        == controls.production_cutoff
        and _integer_tuple(definition["finite_difference_points"], "result.fd")
        == controls.finite_difference_points
        and _real_tuple(definition["parent_sample_reduced_momenta"], "result.momenta")
        == controls.parent_momenta
        and _integer(definition["compared_band_count"], "result.band_count")
        == controls.band_count
        and _integer(definition["reciprocal_mesh_size"], "result.training_size")
        == controls.training_size
        and _integer_tuple(definition["hopping_ranges"], "result.ranges")
        == controls.hopping_ranges
        and _integer(definition["withheld_mesh_size"], "result.withheld_size")
        == controls.withheld_size
        and _string(definition["withheld_mesh_rule"], "result.withheld_rule")
        == "staggered-uniform-disjoint-v1"
        and _real_tuple(
            definition["withheld_reduced_momenta"], "result.withheld_momenta"
        )
        == tuple(float(value) for value in controls.withheld_momenta)
        and _real(
            definition["coordinate_absolute_tolerance"],
            "result.coordinate_tolerance",
        )
        == controls.coordinate_tolerance
        and _real(
            definition["reconstruction_absolute_tolerance"],
            "result.reconstruction_tolerance",
        )
        == controls.tolerance
        and _quantity(
            definition["hermiticity_absolute_tolerance"],
            "result.hermiticity_tolerance",
        )
        == controls.hermiticity_tolerance
        and _quantity(
            definition["parseval_absolute_tolerance"], "result.parseval_tolerance"
        )
        == controls.parseval_tolerance
        and _quantity(
            definition["imaginary_absolute_tolerance"],
            "result.imaginary_tolerance",
        )
        == controls.imaginary_tolerance
    )


def _verify(
    controls: Controls, result_document: dict[str, JsonValue]
) -> dict[str, JsonValue]:
    expected_root_keys = {
        "schema",
        "definition",
        "parent_reference",
        "plane_wave_convergence",
        "finite_difference_convergence",
        "training_target",
        "withheld_target",
        "complete_transform",
        "hopping_hermiticity",
        "range_study",
        "scope",
    }
    _keys(result_document, expected_root_keys, "result")
    if _string(result_document["schema"], "result.schema") != RESULT_SCHEMA:
        raise ValueError("unsupported result schema")
    definition_matches = _definition_matches(controls, result_document)
    scope = _object(result_document["scope"], "result.scope")
    _keys(
        scope,
        {
            "localization_included",
            "external_calculator_execution_included",
            "scientific_acceptance_included",
        },
        "result.scope",
    )
    scope_matches = all(
        not _boolean(scope[name], f"result.scope.{name}")
        for name in (
            "localization_included",
            "external_calculator_execution_included",
            "scientific_acceptance_included",
        )
    )
    parent_momenta = np.asarray(controls.parent_momenta, dtype=np.float64)
    reference = _plane_wave(
        controls, controls.reference_cutoff, parent_momenta, controls.band_count
    )
    retained_parent_momenta, retained_reference = _spectrum(
        result_document["parent_reference"], "result.parent_reference"
    )
    spectral_defects = [
        _maximum_defect(retained_parent_momenta, parent_momenta),
        _maximum_defect(retained_reference, reference),
    ]

    plane_wave_items = _array(
        result_document["plane_wave_convergence"], "result.plane_wave_convergence"
    )
    if len(plane_wave_items) != len(controls.plane_wave_cutoffs):
        raise ValueError("plane-wave observation count does not match input")
    for value, cutoff in zip(
        plane_wave_items, controls.plane_wave_cutoffs, strict=True
    ):
        item = _object(value, "plane-wave observation")
        _keys(item, {"cutoff", "maximum_absolute_error"}, "plane-wave observation")
        if _integer(item["cutoff"], "plane-wave cutoff") != cutoff:
            raise ValueError("plane-wave cutoff order does not match input")
        expected = _maximum_defect(
            _plane_wave(controls, cutoff, parent_momenta, controls.band_count),
            reference,
        )
        spectral_defects.append(
            abs(
                _quantity(item["maximum_absolute_error"], "plane-wave error") - expected
            )
        )

    finite_difference_items = _array(
        result_document["finite_difference_convergence"],
        "result.finite_difference_convergence",
    )
    if len(finite_difference_items) != len(controls.finite_difference_points):
        raise ValueError("finite-difference observation count does not match input")
    for value, points in zip(
        finite_difference_items, controls.finite_difference_points, strict=True
    ):
        item = _object(value, "finite-difference observation")
        _keys(
            item,
            {"point_count", "maximum_absolute_error"},
            "finite-difference observation",
        )
        if _integer(item["point_count"], "finite-difference points") != points:
            raise ValueError("finite-difference point order does not match input")
        expected = _maximum_defect(
            _finite_difference(controls, points, parent_momenta, controls.band_count),
            reference,
        )
        spectral_defects.append(
            abs(
                _quantity(item["maximum_absolute_error"], "finite-difference error")
                - expected
            )
        )

    retained_training_momenta, retained_training = _spectrum(
        result_document["training_target"], "result.training_target"
    )
    retained_withheld_momenta, retained_withheld = _spectrum(
        result_document["withheld_target"], "result.withheld_target"
    )
    training_momenta = controls.training_momenta
    withheld_momenta = controls.withheld_momenta
    training = _plane_wave(controls, controls.production_cutoff, training_momenta, 1)[
        :, 0
    ]
    withheld = _plane_wave(controls, controls.production_cutoff, withheld_momenta, 1)[
        :, 0
    ]
    spectral_defects.extend(
        (
            _maximum_defect(retained_training_momenta, training_momenta),
            _maximum_defect(retained_training[:, 0], training),
            _maximum_defect(retained_withheld_momenta, withheld_momenta),
            _maximum_defect(retained_withheld[:, 0], withheld),
        )
    )
    disjoint_sampling = not np.any(
        np.isclose(
            training_momenta[:, None],
            withheld_momenta[None, :],
            rtol=0.0,
            atol=0.0,
        )
    )

    transform = _object(result_document["complete_transform"], "result.transform")
    _keys(
        transform,
        {
            "representatives",
            "hopping_blocks",
            "reconstruction_maximum_frobenius_error",
            "reconstruction_absolute_tolerance",
            "reconstruction_passes",
        },
        "result.transform",
    )
    retained_representatives = np.asarray(
        _integer_tuple(transform["representatives"], "result.representatives"),
        dtype=np.int64,
    )
    expected_representatives = controls.representatives
    representatives_match = np.array_equal(
        retained_representatives, expected_representatives
    )
    retained_blocks = np.asarray(
        [
            _complex_matrix(value, "result.complete hopping block")[0, 0]
            for value in _array(transform["hopping_blocks"], "result.hopping_blocks")
        ],
        dtype=np.complex128,
    )
    expected_blocks = _direct_fourier(
        training_momenta, training, expected_representatives
    )
    hopping_defects = [_maximum_defect(retained_blocks, expected_blocks)]
    reconstructed_training = _interpolate(
        training_momenta, expected_representatives, expected_blocks
    )
    expected_reconstruction_error = _maximum_defect(reconstructed_training, training)
    reconstruction_scalar_defect = abs(
        _quantity(
            transform["reconstruction_maximum_frobenius_error"],
            "result.reconstruction_error",
        )
        - expected_reconstruction_error
    )
    reconstruction_tolerance = _quantity(
        transform["reconstruction_absolute_tolerance"],
        "result.reconstruction_tolerance",
    )
    reconstruction_disposition_match = (
        reconstruction_tolerance == controls.tolerance
        and _boolean(transform["reconstruction_passes"], "result.reconstruction_passes")
        is (expected_reconstruction_error <= reconstruction_tolerance)
    )

    hermiticity = _object(result_document["hopping_hermiticity"], "result.hermiticity")
    _keys(
        hermiticity,
        {
            "representative_modulus",
            "paired_representatives",
            "missing_opposite_representatives",
            "maximum_frobenius_defect",
            "absolute_tolerance",
            "passes",
        },
        "result.hermiticity",
    )
    lookup = {
        int(representative): value
        for representative, value in zip(
            expected_representatives, expected_blocks, strict=True
        )
    }
    expected_hermiticity = max(
        abs(
            value
            - np.conjugate(
                lookup[
                    next(
                        candidate
                        for candidate in lookup
                        if (candidate + representative) % controls.training_size == 0
                    )
                ]
            )
        )
        for representative, value in lookup.items()
    )
    hermiticity_defect = abs(
        _quantity(hermiticity["maximum_frobenius_defect"], "result.hermiticity.defect")
        - expected_hermiticity
    )
    hermiticity_inventory_match = (
        _integer(hermiticity["representative_modulus"], "hermiticity modulus")
        == controls.training_size
        and _integer_tuple(hermiticity["paired_representatives"], "hermiticity paired")
        == tuple(int(value) for value in expected_representatives)
        and not _array(
            hermiticity["missing_opposite_representatives"], "hermiticity missing"
        )
        and _quantity(hermiticity["absolute_tolerance"], "hermiticity tolerance")
        == controls.hermiticity_tolerance
        and _boolean(hermiticity["passes"], "hermiticity passes")
        == bool(expected_hermiticity <= controls.hermiticity_tolerance)
    )

    range_items = _array(result_document["range_study"], "result.range_study")
    if len(range_items) != len(controls.hopping_ranges):
        raise ValueError("range-study count does not match input")
    diagnostic_defects: list[float] = []
    diagnostic_dispositions_match = True
    for value, maximum_range in zip(range_items, controls.hopping_ranges, strict=True):
        item = _object(value, "range result")
        _keys(
            item,
            {
                "maximum_range",
                "retained_representatives",
                "retained_hopping_blocks",
                "omitted_block_l2_norm",
                "training_maximum_absolute_error",
                "withheld_maximum_absolute_error",
                "parseval",
                "direct_fit",
                "direct_mediated_comparison",
                "band_shape",
            },
            "range result",
        )
        if _integer(item["maximum_range"], "range maximum") != maximum_range:
            raise ValueError("range-study order does not match input")
        retained_mask = np.abs(expected_representatives) <= maximum_range
        range_representatives = expected_representatives[retained_mask]
        range_blocks = expected_blocks[retained_mask]
        if _integer_tuple(
            item["retained_representatives"], "range representatives"
        ) != tuple(int(entry) for entry in range_representatives):
            diagnostic_dispositions_match = False
        retained_range_blocks = np.asarray(
            [
                _complex_matrix(block, "range hopping block")[0, 0]
                for block in _array(item["retained_hopping_blocks"], "range blocks")
            ],
            dtype=np.complex128,
        )
        hopping_defects.append(_maximum_defect(retained_range_blocks, range_blocks))
        omitted_norm = float(np.linalg.norm(expected_blocks[~retained_mask]))
        diagnostic_defects.append(
            abs(
                _quantity(item["omitted_block_l2_norm"], "range omitted norm")
                - omitted_norm
            )
        )
        training_candidate = _interpolate(
            training_momenta, range_representatives, range_blocks
        )
        withheld_candidate = _interpolate(
            withheld_momenta, range_representatives, range_blocks
        )
        diagnostic_defects.extend(
            (
                abs(
                    _quantity(
                        item["training_maximum_absolute_error"], "range training error"
                    )
                    - float(np.max(np.abs(training_candidate.real - training)))
                ),
                abs(
                    _quantity(
                        item["withheld_maximum_absolute_error"], "range withheld error"
                    )
                    - float(np.max(np.abs(withheld_candidate.real - withheld)))
                ),
            )
        )
        parseval = _object(item["parseval"], "range parseval")
        _keys(
            parseval,
            {
                "training_squared_frobenius_residual",
                "expected_squared_frobenius_residual",
                "parseval_absolute_residual",
                "absolute_tolerance",
                "passes",
            },
            "range parseval",
        )
        training_squared = float(
            np.sum(np.square(np.abs(training_candidate - training)))
        )
        expected_squared = controls.training_size * omitted_norm**2
        parseval_residual = abs(training_squared - expected_squared)
        diagnostic_defects.extend(
            (
                abs(
                    _quantity(
                        parseval["training_squared_frobenius_residual"],
                        "parseval training squared",
                    )
                    - training_squared
                ),
                abs(
                    _quantity(
                        parseval["expected_squared_frobenius_residual"],
                        "parseval expected squared",
                    )
                    - expected_squared
                ),
                abs(
                    _quantity(
                        parseval["parseval_absolute_residual"],
                        "parseval residual",
                    )
                    - parseval_residual
                ),
            )
        )
        diagnostic_dispositions_match = diagnostic_dispositions_match and (
            _quantity(parseval["absolute_tolerance"], "parseval tolerance")
            == controls.parseval_tolerance
            and _boolean(parseval["passes"], "parseval passes")
            is (parseval_residual <= controls.parseval_tolerance)
        )

        direct = _object(item["direct_fit"], "range direct fit")
        _keys(
            direct,
            {
                "representatives",
                "hopping_blocks",
                "design_rank",
                "design_condition_number",
                "is_identified",
                "training_l2_frobenius_residual",
                "training_maximum_frobenius_residual",
            },
            "range direct fit",
        )
        design = np.exp(2j * np.pi * np.outer(training_momenta, range_representatives))
        fitted, _, rank, singular_values = np.linalg.lstsq(
            design, training.astype(np.complex128)[:, None], rcond=None
        )
        fitted_blocks = fitted[:, 0]
        retained_fitted_blocks = np.asarray(
            [
                _complex_matrix(block, "direct hopping block")[0, 0]
                for block in _array(direct["hopping_blocks"], "direct blocks")
            ],
            dtype=np.complex128,
        )
        hopping_defects.append(_maximum_defect(retained_fitted_blocks, fitted_blocks))
        direct_residuals = design @ fitted_blocks - training
        expected_condition = float(singular_values[0] / singular_values[-1])
        diagnostic_defects.extend(
            (
                abs(
                    _real(direct["design_condition_number"], "direct condition")
                    - expected_condition
                ),
                abs(
                    _quantity(
                        direct["training_l2_frobenius_residual"],
                        "direct l2 residual",
                    )
                    - float(np.linalg.norm(direct_residuals))
                ),
                abs(
                    _quantity(
                        direct["training_maximum_frobenius_residual"],
                        "direct maximum residual",
                    )
                    - float(np.max(np.abs(direct_residuals)))
                ),
            )
        )
        diagnostic_dispositions_match = diagnostic_dispositions_match and (
            _integer_tuple(direct["representatives"], "direct representatives")
            == tuple(int(entry) for entry in range_representatives)
            and _integer(direct["design_rank"], "direct rank") == int(rank)
            and _boolean(direct["is_identified"], "direct identified")
            is (int(rank) == len(range_representatives))
        )

        route = _object(item["direct_mediated_comparison"], "range route")
        _keys(
            route,
            {
                "coefficient_l2_frobenius_defect",
                "sampled_l2_frobenius_defect",
                "sampled_maximum_frobenius_defect",
            },
            "range route",
        )
        direct_samples = _interpolate(
            training_momenta, range_representatives, fitted_blocks
        )
        sampled_difference = direct_samples - training_candidate
        diagnostic_defects.extend(
            (
                abs(
                    _quantity(
                        route["coefficient_l2_frobenius_defect"],
                        "route coefficient defect",
                    )
                    - float(np.linalg.norm(fitted_blocks - range_blocks))
                ),
                abs(
                    _quantity(
                        route["sampled_l2_frobenius_defect"],
                        "route sampled l2 defect",
                    )
                    - float(np.linalg.norm(sampled_difference))
                ),
                abs(
                    _quantity(
                        route["sampled_maximum_frobenius_defect"],
                        "route sampled maximum defect",
                    )
                    - float(np.max(np.abs(sampled_difference)))
                ),
            )
        )

        band_shape = _object(item["band_shape"], "range band shape")
        _keys(
            band_shape,
            {
                "bandwidth",
                "zone_center_curvature",
                "maximum_imaginary_residual",
                "imaginary_absolute_tolerance",
                "passes",
            },
            "range band shape",
        )
        curvature = np.sum(
            -np.square(2.0 * np.pi * range_representatives) * range_blocks
        )
        maximum_imaginary = max(
            float(np.max(np.abs(withheld_candidate.imag))), abs(float(curvature.imag))
        )
        diagnostic_defects.extend(
            (
                abs(
                    _quantity(band_shape["bandwidth"], "bandwidth")
                    - float(np.ptp(withheld_candidate.real))
                ),
                abs(
                    _quantity(band_shape["zone_center_curvature"], "curvature")
                    - float(curvature.real)
                ),
                abs(
                    _quantity(
                        band_shape["maximum_imaginary_residual"],
                        "maximum imaginary residual",
                    )
                    - maximum_imaginary
                ),
            )
        )
        diagnostic_dispositions_match = diagnostic_dispositions_match and (
            _quantity(
                band_shape["imaginary_absolute_tolerance"],
                "band-shape imaginary tolerance",
            )
            == controls.imaginary_tolerance
            and _boolean(band_shape["passes"], "band-shape passes")
            is (maximum_imaginary <= controls.imaginary_tolerance)
        )

    maximum_spectral_defect = max(spectral_defects)
    maximum_hopping_defect = max(hopping_defects)
    maximum_diagnostic_defect = max(
        diagnostic_defects + [reconstruction_scalar_defect, hermiticity_defect]
    )
    passes = (
        definition_matches
        and scope_matches
        and disjoint_sampling
        and representatives_match
        and reconstruction_disposition_match
        and hermiticity_inventory_match
        and diagnostic_dispositions_match
        and maximum_spectral_defect <= controls.tolerance
        and maximum_hopping_defect <= controls.tolerance
        and maximum_diagnostic_defect <= controls.tolerance
    )
    return {
        "schema": VERIFICATION_SCHEMA,
        "calculation_id": controls.calculation_id,
        "input_schema": INPUT_SCHEMA,
        "result_schema": RESULT_SCHEMA,
        "checks": {
            "definition_matches_input": definition_matches,
            "scope_matches_protocol": scope_matches,
            "training_and_withheld_are_disjoint": disjoint_sampling,
            "representatives_match": representatives_match,
            "reconstruction_disposition_matches": reconstruction_disposition_match,
            "hermiticity_inventory_matches": hermiticity_inventory_match,
            "diagnostic_dispositions_match": diagnostic_dispositions_match,
        },
        "maximum_spectral_absolute_defect": maximum_spectral_defect,
        "maximum_hopping_absolute_defect": maximum_hopping_defect,
        "maximum_diagnostic_absolute_defect": maximum_diagnostic_defect,
        "absolute_tolerance": controls.tolerance,
        "passes": passes,
        "claim_boundary": (
            "Passing establishes bounded numerical consistency only; it does not "
            "establish material validity, uncertainty quantification, or scientific "
            "acceptance."
        ),
    }


def main() -> None:
    """Verify the retained document and write a deterministic verification record."""
    controls = _decode_controls(_load(INPUT_PATH))
    verification = _verify(controls, _load(RESULT_PATH))
    VERIFICATION_PATH.write_text(
        json.dumps(
            verification,
            sort_keys=True,
            indent=2,
            ensure_ascii=False,
            allow_nan=False,
        )
        + "\n",
        encoding="utf-8",
    )
    if verification["passes"] is not True:
        raise SystemExit("independent verification failed")
    print(f"verified {RESULT_PATH.name}; wrote {VERIFICATION_PATH.name}")


if __name__ == "__main__":
    main()
