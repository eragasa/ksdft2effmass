"""Independent Fourier-locality accounting for every dimensional family."""

from __future__ import annotations

import math
from collections.abc import Mapping
from dataclasses import dataclass

import numpy as np
import pytest
from numpy.typing import NDArray
from projectkoios.physkit.periodic.lattice import (
    BravaisLattice,
    DirectLattice2D,
    DirectLatticeMetric,
)

from ksdft2effmass.analysis.model_adequacy.band_equivalence_locality import (
    analysis,
    calculation,
    definitions,
)
from ksdft2effmass.analysis.model_adequacy.band_equivalence_locality.records import (
    ErrorChannels,
)
from ksdft2effmass.analysis.model_adequacy.band_equivalence_locality.refinement import (
    BandEquivalenceLocalityRefinementAnalyzer,
)
from ksdft2effmass.analysis.model_adequacy.band_equivalence_locality.result import (
    BandEquivalenceLocalityAnalysisRecorder,
)

pytestmark = [pytest.mark.unit, pytest.mark.software_verification]

type ComplexArray = NDArray[np.complex128]
type FloatArray = NDArray[np.float64]
type IntArray = NDArray[np.int64]

_ONSITE = np.array(
    [
        [-1.20, 0.06, 0.0, 0.0],
        [0.06, -0.35, 0.0, 0.0],
        [0.0, 0.0, 1.00, 0.04],
        [0.0, 0.0, 0.04, 1.75],
    ],
    dtype=np.complex128,
)
_DIRECTED = np.array(
    [
        [0.15, 0.0, 0.12, 0.0],
        [0.0, -0.10, 0.0, 0.10],
        [0.0, 0.0, 0.05, 0.0],
        [0.0, 0.0, 0.0, -0.04],
    ],
    dtype=np.complex128,
)
_HERMITIAN_BOND = _DIRECTED + _DIRECTED.conjugate().T
_SEED = np.eye(4, 2, dtype=np.complex128)


@dataclass(frozen=True, slots=True)
class _PowerSummary:
    """Hold direct finite-sum powers used only by this test oracle."""

    reference_nononsite: float
    comparison_nononsite: float
    reference_shells: Mapping[int, float]
    comparison_shells: Mapping[int, float]


@dataclass(frozen=True, slots=True)
class _ShellErrorSummary:
    """Hold independently evaluated errors at one complete metric shell."""

    shell_index: int
    reference_truncation: tuple[float, float, float, float]
    comparison_truncation: tuple[float, float, float, float]
    reference_total: tuple[float, float, float, float]
    comparison_total: tuple[float, float, float, float]


@dataclass(frozen=True, slots=True)
class _RestrictedAlignmentSummary:
    """Hold an independent closed-form restricted-alignment solution."""

    splitting_scale: float
    maximum_correlation: float
    minimum_threshold: float
    exact_spectrum_threshold: float
    normalized_squared_residual: float


def _case(
    family: definitions.BandEquivalenceLocalityFamilyEnum,
) -> definitions.BandEquivalenceLocalityCase:
    if family is definitions.BandEquivalenceLocalityFamilyEnum.SQUARE:
        return definitions.BandEquivalenceLocalityCase(
            name="square-directed-parent",
            dimension=2,
            parent_kind=definitions.ParentEnum.DIRECTED_AXIS,
            gauge_normalization=definitions.GaugeNormalizationEnum.AXIS_MAXIMUM,
            positive_bonds=((1, 0), (0, 1)),
            direct_metric=DirectLatticeMetric(
                DirectLattice2D(
                    a1=np.array((1.0, 0.0), dtype=np.float64),
                    a2=np.array((0.0, 1.0), dtype=np.float64),
                )
            ),
            shell_metric_scale=1.0,
        )
    if family is definitions.BandEquivalenceLocalityFamilyEnum.SIMPLE_CUBIC:
        return definitions.BandEquivalenceLocalityCase(
            name="simple-cubic-directed-parent",
            dimension=3,
            parent_kind=definitions.ParentEnum.DIRECTED_AXIS,
            gauge_normalization=definitions.GaugeNormalizationEnum.AXIS_MAXIMUM,
            positive_bonds=((1, 0, 0), (0, 1, 0), (0, 0, 1)),
            direct_metric=DirectLatticeMetric(
                BravaisLattice.cubic_primitive().direct_lattice
            ),
            shell_metric_scale=1.0,
        )
    if family is definitions.BandEquivalenceLocalityFamilyEnum.GRAPHENE_INSPIRED:
        return definitions.BandEquivalenceLocalityCase(
            name="graphene-inspired-honeycomb",
            dimension=2,
            parent_kind=definitions.ParentEnum.BIPARTITE_INSPIRED,
            gauge_normalization=definitions.GaugeNormalizationEnum.BOND_RMS,
            positive_bonds=((1, 0), (0, 1), (1, -1)),
            direct_metric=DirectLatticeMetric(
                DirectLattice2D(
                    a1=np.array((1.0, 0.0), dtype=np.float64),
                    a2=np.array((0.5, math.sqrt(3.0) / 2.0), dtype=np.float64),
                )
            ),
            shell_metric_scale=1.0,
            basis_offsets=((0.0, 0.0), (1.0 / 3.0, 1.0 / 3.0)),
        )
    return definitions.BandEquivalenceLocalityCase(
        name="silicon-inspired-diamond",
        dimension=3,
        parent_kind=definitions.ParentEnum.BIPARTITE_INSPIRED,
        gauge_normalization=definitions.GaugeNormalizationEnum.BOND_RMS,
        positive_bonds=(
            (1, 0, 0),
            (0, 1, 0),
            (0, 0, 1),
            (-1, 1, 0),
            (-1, 0, 1),
            (0, -1, 1),
        ),
        direct_metric=DirectLatticeMetric(
            BravaisLattice.cubic_face_centered().direct_lattice
        ),
        shell_metric_scale=2.0,
        basis_offsets=(
            (0.0, 0.0, 0.0),
            (1.0 / 4.0, 1.0 / 4.0, 1.0 / 4.0),
        ),
    )


def _coordinates(size: int, dimension: int, offset: float) -> FloatArray:
    axis = -0.5 + (np.arange(size, dtype=np.float64) + offset) / float(size)
    return np.stack(np.meshgrid(*(axis,) * dimension, indexing="ij"), axis=-1)


def _direct_blocks(
    coordinates: FloatArray,
    field: ComplexArray,
) -> tuple[IntArray, ComplexArray]:
    """Evaluate the finite Fourier sums by separable explicit contractions."""
    dimension = coordinates.shape[-1]
    size = field.shape[0]
    integer_axis = np.arange(-size // 2, size // 2, dtype=np.int64)
    transformed = np.asarray(field, dtype=np.complex128)
    for axis in range(dimension):
        coordinate_index: list[int | slice] = [0] * dimension
        coordinate_index[axis] = slice(None)
        coordinate_axis = coordinates[tuple(coordinate_index)][..., axis]
        phases = np.exp(
            -2.0j * np.pi * np.einsum("r,q->rq", integer_axis, coordinate_axis)
        )
        transformed = np.tensordot(phases, transformed, axes=((1,), (axis,)))
        transformed = np.moveaxis(transformed, 0, axis)
    transformed /= float(size**dimension)
    displacements = np.stack(
        np.meshgrid(*(integer_axis,) * dimension, indexing="ij"), axis=-1
    ).reshape((-1, dimension))
    return displacements, transformed.reshape((-1, 2, 2))


def _direct_evaluation(
    displacements: IntArray,
    blocks: ComplexArray,
    coordinates: FloatArray,
) -> ComplexArray:
    phases = np.exp(
        2.0j * np.pi * np.einsum("...d,rd->...r", coordinates, displacements)
    )
    return np.asarray(
        np.einsum("...r,rij->...ij", phases, blocks, optimize=True),
        dtype=np.complex128,
    )


def _oracle_parent_field(
    case: definitions.BandEquivalenceLocalityCase,
    coordinates: FloatArray,
    parent_scale: float,
) -> ComplexArray:
    """Construct the declared synthetic parent independently of production code."""
    shape = coordinates.shape[:-1]
    result = np.broadcast_to(_ONSITE, (*shape, 4, 4)).copy()
    if case.parent_kind is definitions.ParentEnum.DIRECTED_AXIS:
        phase_average = np.mean(np.exp(2.0j * np.pi * coordinates), axis=-1)
        scaled = parent_scale * phase_average
        result += scaled[..., None, None] * _DIRECTED
        result += scaled.conjugate()[..., None, None] * _DIRECTED.conjugate().T
        return result
    if case.parent_kind is definitions.ParentEnum.HERMITIAN_BRAVAIS:
        bonds = np.asarray(case.positive_bonds, dtype=np.float64)
        arguments = np.einsum("...d,bd->...b", coordinates, bonds)
        structure = np.mean(np.cos(2.0 * np.pi * arguments), axis=-1)
        result += parent_scale * structure[..., None, None] * _HERMITIAN_BOND
        return result

    exponentials = np.exp(-2.0j * np.pi * coordinates)
    gamma = (1.0 + np.sum(exponentials, axis=-1)) / float(case.dimension + 1)
    sublattice = np.empty((*shape, 2, 2), dtype=np.complex128)
    sublattice[..., 0, 0] = 0.0
    sublattice[..., 0, 1] = gamma
    sublattice[..., 1, 0] = gamma.conjugate()
    sublattice[..., 1, 1] = 0.0
    result = np.zeros((*shape, 4, 4), dtype=np.complex128)
    identity = np.eye(2, dtype=np.complex128)
    result[..., :2, :2] = -1.20 * identity + parent_scale * 0.30 * sublattice
    result[..., 2:, 2:] = 1.20 * identity + parent_scale * 0.10 * sublattice
    result[..., :2, 2:] = 0.08 * identity
    result[..., 2:, :2] = 0.08 * identity
    return result


def _oracle_retained_field(parent: ComplexArray) -> ComplexArray:
    """Project the parent through an independently assembled seed-polar frame."""
    _, eigenvectors = np.linalg.eigh(parent)
    low = eigenvectors[..., :, :2]
    projector = low @ np.swapaxes(low.conjugate(), -1, -2)
    projected_seed = projector @ _SEED
    seed_gram = np.swapaxes(projected_seed.conjugate(), -1, -2) @ projected_seed
    gram_values, gram_vectors = np.linalg.eigh(seed_gram)
    inverse_root = (
        gram_vectors * (1.0 / np.sqrt(gram_values))[..., None, :]
    ) @ np.swapaxes(gram_vectors.conjugate(), -1, -2)
    frame = projected_seed @ inverse_root
    return np.swapaxes(frame.conjugate(), -1, -2) @ parent @ frame


def _oracle_gauge_angles(
    case: definitions.BandEquivalenceLocalityCase,
    coordinates: FloatArray,
    amplitude: float,
) -> FloatArray:
    """Evaluate the declared multidimensional gauge law directly."""
    bonds = np.asarray(case.positive_bonds, dtype=np.float64)
    arguments = np.einsum("...d,bd->...b", coordinates, bonds)
    sine_sum = np.sum(np.sin(2.0 * np.pi * arguments), axis=-1)
    if case.gauge_normalization is definitions.GaugeNormalizationEnum.AXIS_MAXIMUM:
        return amplitude * sine_sum / float(case.dimension)
    return amplitude * math.sqrt(2.0 / float(len(case.positive_bonds))) * sine_sum


def _oracle_rotation_field(angles: FloatArray) -> ComplexArray:
    """Construct the real rank-two rotation field explicitly."""
    rotations = np.empty((*angles.shape, 2, 2), dtype=np.complex128)
    cosine = np.cos(angles)
    sine = np.sin(angles)
    rotations[..., 0, 0] = cosine
    rotations[..., 0, 1] = -sine
    rotations[..., 1, 0] = sine
    rotations[..., 1, 1] = cosine
    return rotations


def _fields(
    case: definitions.BandEquivalenceLocalityCase,
    coordinates: FloatArray,
    parent_scale: float,
    amplitude: float,
) -> tuple[ComplexArray, ComplexArray]:
    """Construct both scientific fields without calling production calculations."""
    parent = _oracle_parent_field(case, coordinates, parent_scale)
    reference = _oracle_retained_field(parent)
    rotation = _oracle_rotation_field(
        _oracle_gauge_angles(case, coordinates, amplitude)
    )
    comparison = np.swapaxes(rotation.conjugate(), -1, -2) @ reference @ rotation
    return reference, comparison


def _block_powers(blocks: ComplexArray) -> FloatArray:
    return np.asarray(
        np.sum(np.abs(blocks) ** 2, axis=(-2, -1)) / 2.0,
        dtype=np.float64,
    )


def _restricted_alignment_summary(
    reference: ComplexArray, comparison: ComplexArray
) -> _RestrictedAlignmentSummary:
    """Solve the rank-two restricted alignment without production actions."""
    identity = np.eye(2, dtype=np.complex128)
    reference_trace = np.trace(reference, axis1=-2, axis2=-1).real / 2.0
    comparison_trace = np.trace(comparison, axis1=-2, axis2=-1).real / 2.0
    reference_traceless = reference - reference_trace[..., None, None] * identity
    comparison_traceless = comparison - comparison_trace[..., None, None] * identity
    splitting_scale = float(
        np.mean(np.sum(np.abs(reference_traceless) ** 2, axis=(-2, -1))) / 2.0
    )
    assert splitting_scale > 0.0

    def numerator(angle: float) -> float:
        rotation = _oracle_rotation_field(np.asarray(angle, dtype=np.float64))
        aligned = (
            np.swapaxes(rotation.conjugate(), -1, -2) @ reference_traceless @ rotation
        )
        products = np.einsum(
            "...ij,...ij->...",
            aligned.conjugate(),
            comparison_traceless,
            optimize=True,
        )
        return float(np.mean(products.real) / 2.0)

    positive_quarter = numerator(math.pi / 4.0)
    negative_quarter = numerator(-math.pi / 4.0)
    constant = 0.5 * (positive_quarter + negative_quarter)
    cosine_coefficient = numerator(0.0) - constant
    sine_coefficient = 0.5 * (positive_quarter - negative_quarter)
    angle = 0.5 * math.atan2(sine_coefficient, cosine_coefficient)
    maximum_correlation = (
        constant + math.hypot(cosine_coefficient, sine_coefficient)
    ) / splitting_scale
    positive_scale = max(0.0, maximum_correlation)
    rotation = _oracle_rotation_field(np.asarray(angle, dtype=np.float64))
    aligned = np.swapaxes(rotation.conjugate(), -1, -2) @ reference_traceless @ rotation
    minimum_squared = float(
        np.mean(
            np.sum(
                np.abs(positive_scale * aligned - comparison_traceless) ** 2,
                axis=(-2, -1),
            )
        )
        / 2.0
    )
    exact_squared = float(
        np.mean(
            np.sum(
                np.abs(aligned - comparison_traceless) ** 2,
                axis=(-2, -1),
            )
        )
        / 2.0
    )
    return _RestrictedAlignmentSummary(
        splitting_scale=splitting_scale,
        maximum_correlation=maximum_correlation,
        minimum_threshold=math.sqrt(max(0.0, minimum_squared)),
        exact_spectrum_threshold=math.sqrt(max(0.0, exact_squared)),
        normalized_squared_residual=minimum_squared / splitting_scale,
    )


def _metric_indices(
    case: definitions.BandEquivalenceLocalityCase,
    displacements: IntArray,
) -> IntArray:
    values = case.shell_metric_scale * np.einsum(
        "ri,ij,rj->r",
        displacements,
        case.direct_metric.metric_tensor,
        displacements,
    )
    assert float(np.max(np.abs(values - np.rint(values)))) < 1.0e-12
    return np.asarray(np.rint(values), dtype=np.int64)


def _error_channels(
    approximation: ComplexArray,
    direct: ComplexArray,
) -> tuple[float, float, float, float]:
    difference = approximation - direct
    matrix_norms = np.linalg.norm(difference, axis=(-2, -1)) / math.sqrt(2.0)
    band_difference = np.abs(
        np.linalg.eigvalsh(approximation) - np.linalg.eigvalsh(direct)
    )
    return (
        float(np.max(matrix_norms)),
        float(np.sqrt(np.mean(matrix_norms**2))),
        float(np.max(band_difference)),
        float(np.sqrt(np.mean(band_difference**2))),
    )


def _channel_values(channels: ErrorChannels) -> tuple[float, float, float, float]:
    return (
        channels.maximum_hamiltonian,
        channels.rms_hamiltonian,
        channels.maximum_band,
        channels.rms_band,
    )


def _hermiticity_defects(
    size: int,
    displacements: IntArray,
    blocks: ComplexArray,
) -> tuple[float, float]:
    lookup = {
        tuple(int(value) for value in displacement): block
        for displacement, block in zip(displacements, blocks, strict=True)
    }
    lower = -size // 2
    upper = size // 2 - 1
    twisted = 0.0
    ordinary = 0.0
    for displacement, block in zip(displacements, blocks, strict=True):
        target: list[int] = []
        wraps = 0
        boundary = False
        for value in displacement:
            negative = -int(value)
            if negative > upper:
                negative -= size
                wraps += 1
                boundary = True
            elif negative < lower:
                negative += size
                wraps += 1
                boundary = True
            target.append(negative)
        defect = float(
            np.linalg.norm(
                lookup[tuple(target)] - ((-1.0) ** wraps) * block.conjugate().T
            )
        )
        twisted = max(twisted, defect)
        if not boundary and not np.any(displacement == lower):
            ordinary = max(ordinary, defect)
    return twisted, ordinary


def _maximum_matrix_defect(left: ComplexArray, right: ComplexArray) -> float:
    return float(np.max(np.linalg.norm(left - right, axis=(-2, -1))))


def _relative_maximum_matrix_defect(left: ComplexArray, right: ComplexArray) -> float:
    scale = float(np.max(np.linalg.norm(right, axis=(-2, -1))))
    assert scale > 0.0
    return _maximum_matrix_defect(left, right) / scale


def _brute_minimum_mesh_separation(
    construction: FloatArray, evaluation: FloatArray
) -> float:
    """Evaluate the torus separation from every explicit point pair."""
    dimension = construction.shape[-1]
    construction_points = construction.reshape((-1, dimension))
    evaluation_points = evaluation.reshape((-1, dimension))
    deltas = evaluation_points[:, None, :] - construction_points[None, :, :]
    deltas -= np.rint(deltas)
    return float(np.min(np.linalg.norm(deltas, axis=-1)))


def _select_first_passing(
    values: tuple[tuple[int, float], ...], tolerance: float
) -> tuple[int | None, float | None, float | None]:
    """Select a first-passing shell without using production decision code."""
    previous: float | None = None
    for shell_index, value in values:
        if value <= tolerance:
            return shell_index, value, previous
        previous = value
    return None, None, None


def _direct_alignment_summary(
    case: definitions.BandEquivalenceLocalityCase,
    size: int,
    parent_scale: float,
    amplitude: float,
) -> _RestrictedAlignmentSummary:
    coordinates = _coordinates(size, case.dimension, 0.5)
    reference, comparison = _fields(case, coordinates, parent_scale, amplitude)
    return _restricted_alignment_summary(reference, comparison)


def _direct_integrated_values(
    case: definitions.BandEquivalenceLocalityCase,
    size: int,
    parent_scale: float,
    amplitude: float,
    shell_cap: int,
) -> tuple[float, ...]:
    """Return every bounded integrated alignment and Fourier-power channel."""
    coordinates = _coordinates(size, case.dimension, 0.5)
    reference, comparison = _fields(case, coordinates, parent_scale, amplitude)
    alignment = _restricted_alignment_summary(reference, comparison)
    displacements, reference_blocks = _direct_blocks(coordinates, reference)
    comparison_displacements, comparison_blocks = _direct_blocks(
        coordinates, comparison
    )
    assert np.array_equal(displacements, comparison_displacements)
    reference_powers = _block_powers(reference_blocks)
    comparison_powers = _block_powers(comparison_blocks)
    onsite = np.all(displacements == 0, axis=1)
    nyquist = np.any(displacements == -size // 2, axis=1)
    ordinary_metric_indices = _metric_indices(case, displacements[~nyquist])
    reference_ordinary = reference_powers[~nyquist]
    comparison_ordinary = comparison_powers[~nyquist]
    reference_nyquist = float(np.sum(reference_powers[nyquist]))
    comparison_nyquist = float(np.sum(comparison_powers[nyquist]))
    values = [
        alignment.splitting_scale,
        alignment.maximum_correlation,
        alignment.minimum_threshold,
        alignment.exact_spectrum_threshold,
        alignment.normalized_squared_residual,
        float(np.sum(reference_powers)),
        float(np.sum(comparison_powers)),
        float(np.sum(reference_powers[onsite])),
        float(np.sum(comparison_powers[onsite])),
        float(np.sum(reference_powers[~onsite])),
        float(np.sum(comparison_powers[~onsite])),
        reference_nyquist,
        comparison_nyquist,
    ]
    shells = tuple(
        int(value)
        for value in sorted(set(ordinary_metric_indices.tolist()))
        if value <= shell_cap
    )
    for shell in shells:
        retained = ordinary_metric_indices <= shell
        shell_mask = ordinary_metric_indices == shell
        reference_omitted = float(np.sum(reference_ordinary[~retained]))
        comparison_omitted = float(np.sum(comparison_ordinary[~retained]))
        values.extend(
            (
                float(np.sum(reference_ordinary[shell_mask])),
                float(np.sum(comparison_ordinary[shell_mask])),
                reference_omitted,
                comparison_omitted,
                reference_omitted + reference_nyquist,
                comparison_omitted + comparison_nyquist,
            )
        )
    return tuple(values)


def _direct_power_summary(
    case: definitions.BandEquivalenceLocalityCase,
    size: int,
    parent_scale: float,
    amplitude: float,
    shell_cap: int,
) -> _PowerSummary:
    coordinates = _coordinates(size, case.dimension, 0.5)
    reference, comparison = _fields(case, coordinates, parent_scale, amplitude)
    displacements, reference_blocks = _direct_blocks(coordinates, reference)
    comparison_displacements, comparison_blocks = _direct_blocks(
        coordinates, comparison
    )
    assert np.array_equal(displacements, comparison_displacements)
    reference_powers = _block_powers(reference_blocks)
    comparison_powers = _block_powers(comparison_blocks)
    onsite = np.all(displacements == 0, axis=1)
    nyquist = np.any(displacements == -size // 2, axis=1)
    ordinary_displacements = displacements[~nyquist]
    metric_indices = _metric_indices(case, ordinary_displacements)
    reference_ordinary = reference_powers[~nyquist]
    comparison_ordinary = comparison_powers[~nyquist]
    shells = tuple(
        int(value)
        for value in sorted(set(metric_indices.tolist()))
        if value <= shell_cap
    )
    return _PowerSummary(
        reference_nononsite=float(np.sum(reference_powers[~onsite])),
        comparison_nononsite=float(np.sum(comparison_powers[~onsite])),
        reference_shells={
            shell: float(np.sum(reference_ordinary[metric_indices == shell]))
            for shell in shells
        },
        comparison_shells={
            shell: float(np.sum(comparison_ordinary[metric_indices == shell]))
            for shell in shells
        },
    )


_FAMILIES = tuple(definitions.BandEquivalenceLocalityFamilyEnum)


class TestFourierLocalityParity:
    """Reconstruct power, omission, identity, and refinement channels directly."""

    @pytest.mark.parametrize("family", _FAMILIES)
    def test_all_point_channels_match_independent_finite_sums(
        self,
        family: definitions.BandEquivalenceLocalityFamilyEnum,
    ) -> None:
        case = _case(family)
        size = 6
        evaluation_size = 7
        parent_scale = 1.0
        amplitude = math.pi / 8.0
        shell_cap = 5
        request = definitions.BandEquivalenceLocalityRequest(
            family=family,
            synthetic_model=definitions.FOUR_STATE_LOCALITY_DEVELOPMENT_MODEL_V1,
            cases=(case,),
            construction_size=size,
            evaluation_size=evaluation_size,
            evaluation_shift=1.0 / 3.0,
            parent_scales=(parent_scale,),
            amplitudes=(amplitude,),
            band_tolerances=(1.0e-1,),
            shell_cap=shell_cap,
            amplitude_resolution_intervals=(1, 2),
        )
        scientific_analysis = analysis.BandEquivalenceLocalityAnalyzer(
            request=request
        ).execute()
        retained = BandEquivalenceLocalityAnalysisRecorder(scientific_analysis).result()
        verification = calculation.BandEquivalenceLocalityVerifier(
            request=request,
            result=retained.diagnostics,
        ).execute()
        point = scientific_analysis.cases[0].points[0]
        construction = _coordinates(size, case.dimension, 0.5)
        evaluation = _coordinates(
            evaluation_size,
            case.dimension,
            0.5 + request.evaluation_shift,
        )
        reference, comparison = _fields(case, construction, parent_scale, amplitude)
        direct_reference, direct_comparison = _fields(
            case, evaluation, parent_scale, amplitude
        )
        assert scientific_analysis.construction_size == size
        assert scientific_analysis.evaluation_size == evaluation_size
        assert construction.shape == (size,) * case.dimension + (case.dimension,)
        assert evaluation.shape == (evaluation_size,) * case.dimension + (
            case.dimension,
        )
        expected_construction_axis = -0.5 + (
            np.arange(size, dtype=np.float64) + 0.5
        ) / float(size)
        expected_evaluation_axis = -0.5 + (
            np.arange(evaluation_size, dtype=np.float64)
            + 0.5
            + request.evaluation_shift
        ) / float(evaluation_size)
        for axis in range(case.dimension):
            construction_index: list[int | slice] = [0] * case.dimension
            evaluation_index: list[int | slice] = [0] * case.dimension
            construction_index[axis] = slice(None)
            evaluation_index[axis] = slice(None)
            np.testing.assert_allclose(
                construction[tuple(construction_index)][..., axis],
                expected_construction_axis,
                rtol=0.0,
                atol=2.0e-16,
            )
            np.testing.assert_allclose(
                evaluation[tuple(evaluation_index)][..., axis],
                expected_evaluation_axis,
                rtol=0.0,
                atol=2.0e-16,
            )
        expected_separation = _brute_minimum_mesh_separation(construction, evaluation)
        assert expected_separation > 0.0
        assert scientific_analysis.cases[
            0
        ].construction_evaluation_minimum_separation == pytest.approx(
            expected_separation, abs=5.0e-15
        )

        displacements, reference_blocks = _direct_blocks(construction, reference)
        comparison_displacements, comparison_blocks = _direct_blocks(
            construction, comparison
        )
        assert np.array_equal(displacements, comparison_displacements)

        reference_powers = _block_powers(reference_blocks)
        comparison_powers = _block_powers(comparison_blocks)
        onsite = np.all(displacements == 0, axis=1)
        nyquist = np.any(displacements == -size // 2, axis=1)
        ordinary = ~nyquist
        ordinary_displacements = displacements[ordinary]
        ordinary_reference = reference_blocks[ordinary]
        ordinary_comparison = comparison_blocks[ordinary]
        ordinary_reference_powers = reference_powers[ordinary]
        ordinary_comparison_powers = comparison_powers[ordinary]
        metric_indices = _metric_indices(case, ordinary_displacements)

        comparisons: list[tuple[float, float]] = []

        def compare(observed: float, expected: float) -> None:
            comparisons.append((observed, expected))

        def compare_optional(observed: float | None, expected: float | None) -> None:
            if expected is None:
                assert observed is None
            else:
                assert observed is not None
                compare(observed, expected)

        alignment = _restricted_alignment_summary(reference, comparison)
        equivalence = point.representation_equivalence
        assert equivalence.spatial_dimension == case.dimension
        assert equivalence.retained_rank == 2
        assert (
            point.maximum_direct_band_defect == equivalence.maximum_direct_band_defect
        )
        assert point.maximum_covariant_defect == equivalence.maximum_covariant_defect
        assert (
            point.minimum_operator_threshold == equivalence.minimum_operator_threshold
        )
        retained_point_mapping = retained.diagnostics.cases[0].points[0].to_dict()
        assert "representation_equivalence" not in retained_point_mapping
        assert (
            retained_point_mapping["maximum_direct_band_defect"]
            == equivalence.maximum_direct_band_defect
        )
        parent = _oracle_parent_field(case, construction, parent_scale)
        parent_eigenvalues = np.linalg.eigvalsh(parent)
        compare(
            point.minimum_sampled_external_gap,
            float(np.min(parent_eigenvalues[..., 2] - parent_eigenvalues[..., 1])),
        )
        compare(
            point.maximum_direct_band_defect,
            float(
                np.max(
                    np.abs(
                        np.linalg.eigvalsh(reference) - np.linalg.eigvalsh(comparison)
                    )
                )
            ),
        )
        assert point.finite_mesh_maximum_correlation is not None
        assert point.normalized_squared_operator_residual is not None
        compare(point.splitting_scale, alignment.splitting_scale)
        compare(point.finite_mesh_maximum_correlation, alignment.maximum_correlation)
        compare(point.minimum_operator_threshold, alignment.minimum_threshold)
        compare(
            point.exact_spectrum_joint_operator_threshold,
            alignment.exact_spectrum_threshold,
        )
        compare(
            point.normalized_squared_operator_residual,
            alignment.normalized_squared_residual,
        )
        compare(point.restricted_global_rotation_residual, alignment.minimum_threshold)
        comparisons.extend(
            (
                (
                    _relative_maximum_matrix_defect(
                        reference, np.swapaxes(reference.conjugate(), -1, -2)
                    ),
                    0.0,
                ),
                (
                    _relative_maximum_matrix_defect(
                        comparison, np.swapaxes(comparison.conjugate(), -1, -2)
                    ),
                    0.0,
                ),
            )
        )

        compare(point.reference_total_power, float(np.sum(reference_powers)))
        compare(point.comparison_total_power, float(np.sum(comparison_powers)))
        compare(point.reference_onsite_power, float(np.sum(reference_powers[onsite])))
        compare(
            point.comparison_onsite_power,
            float(np.sum(comparison_powers[onsite])),
        )
        reference_nononsite = float(np.sum(reference_powers[~onsite]))
        comparison_nononsite = float(np.sum(comparison_powers[~onsite]))
        compare(point.reference_nononsite_power, reference_nononsite)
        compare(point.comparison_nononsite_power, comparison_nononsite)
        compare(
            point.excess_nonzero_hopping_weight,
            comparison_nononsite - reference_nononsite,
        )
        assert point.normalized_excess_nonzero_hopping_weight is not None
        compare(
            point.normalized_excess_nonzero_hopping_weight,
            (comparison_nononsite - reference_nononsite) / point.splitting_scale,
        )
        reference_nyquist = float(np.sum(reference_powers[nyquist]))
        comparison_nyquist = float(np.sum(comparison_powers[nyquist]))
        compare(point.reference_nyquist_power, reference_nyquist)
        compare(point.comparison_nyquist_power, comparison_nyquist)

        reconstructed_reference = _direct_evaluation(
            displacements, reference_blocks, construction
        )
        reconstructed_comparison = _direct_evaluation(
            displacements, comparison_blocks, construction
        )
        reference_reconstruction_defect = _maximum_matrix_defect(
            reconstructed_reference, reference
        )
        comparison_reconstruction_defect = _maximum_matrix_defect(
            reconstructed_comparison, comparison
        )
        compare(
            point.reference_fourier_reconstruction_defect,
            reference_reconstruction_defect,
        )
        compare(
            point.comparison_fourier_reconstruction_defect,
            comparison_reconstruction_defect,
        )
        comparisons.extend(
            (
                (
                    _relative_maximum_matrix_defect(reconstructed_reference, reference),
                    0.0,
                ),
                (
                    _relative_maximum_matrix_defect(
                        reconstructed_comparison, comparison
                    ),
                    0.0,
                ),
            )
        )
        reference_momentum_weight = float(
            np.mean(np.sum(np.abs(reference) ** 2, axis=(-2, -1)))
        )
        comparison_momentum_weight = float(
            np.mean(np.sum(np.abs(comparison) ** 2, axis=(-2, -1)))
        )
        reference_parseval_defect = abs(
            reference_momentum_weight - float(np.sum(np.abs(reference_blocks) ** 2))
        )
        comparison_parseval_defect = abs(
            comparison_momentum_weight - float(np.sum(np.abs(comparison_blocks) ** 2))
        )
        compare(point.reference_parseval_defect, reference_parseval_defect)
        compare(point.comparison_parseval_defect, comparison_parseval_defect)
        comparisons.extend(
            (
                (reference_parseval_defect / reference_momentum_weight, 0.0),
                (comparison_parseval_defect / comparison_momentum_weight, 0.0),
            )
        )
        reference_twisted, reference_ordinary = _hermiticity_defects(
            size, displacements, reference_blocks
        )
        comparison_twisted, comparison_ordinary = _hermiticity_defects(
            size, displacements, comparison_blocks
        )
        compare(point.reference_twisted_nyquist_defect, reference_twisted)
        compare(point.reference_ordinary_hermiticity_defect, reference_ordinary)
        compare(point.comparison_twisted_nyquist_defect, comparison_twisted)
        compare(point.comparison_ordinary_hermiticity_defect, comparison_ordinary)

        full_reference_source = _direct_evaluation(
            ordinary_displacements, ordinary_reference, construction
        )
        full_comparison_source = _direct_evaluation(
            ordinary_displacements, ordinary_comparison, construction
        )
        full_reference_evaluation = _direct_evaluation(
            ordinary_displacements, ordinary_reference, evaluation
        )
        full_comparison_evaluation = _direct_evaluation(
            ordinary_displacements, ordinary_comparison, evaluation
        )
        for observed_value, expected_value in zip(
            _channel_values(point.reference_interpolation),
            _error_channels(full_reference_evaluation, direct_reference),
            strict=True,
        ):
            compare(observed_value, expected_value)
        for observed_value, expected_value in zip(
            _channel_values(point.comparison_interpolation),
            _error_channels(full_comparison_evaluation, direct_comparison),
            strict=True,
        ):
            compare(observed_value, expected_value)

        expected_shells = tuple(
            int(value)
            for value in sorted(set(metric_indices.tolist()))
            if value <= shell_cap
        )
        assert tuple(value.shell_index for value in point.shell_diagnostics) == (
            expected_shells
        )
        assert (
            tuple(value.metric_shell_value for value in point.shell_diagnostics)
            == expected_shells
        )
        expected_shell_errors: list[_ShellErrorSummary] = []
        for shell_index, shell_diagnostic in zip(
            expected_shells, point.shell_diagnostics, strict=True
        ):
            retained = metric_indices <= shell_index
            shell_mask = metric_indices == shell_index
            reference_source = _direct_evaluation(
                ordinary_displacements[retained],
                ordinary_reference[retained],
                construction,
            )
            comparison_source = _direct_evaluation(
                ordinary_displacements[retained],
                ordinary_comparison[retained],
                construction,
            )
            reference_evaluation = _direct_evaluation(
                ordinary_displacements[retained],
                ordinary_reference[retained],
                evaluation,
            )
            comparison_evaluation = _direct_evaluation(
                ordinary_displacements[retained],
                ordinary_comparison[retained],
                evaluation,
            )
            reference_omitted = float(np.sum(ordinary_reference_powers[~retained]))
            comparison_omitted = float(np.sum(ordinary_comparison_powers[~retained]))
            assert shell_diagnostic.retained_blocks == int(np.count_nonzero(retained))
            compare(
                shell_diagnostic.reference_shell_power,
                float(np.sum(ordinary_reference_powers[shell_mask])),
            )
            compare(
                shell_diagnostic.comparison_shell_power,
                float(np.sum(ordinary_comparison_powers[shell_mask])),
            )
            compare(shell_diagnostic.reference_omitted_power, reference_omitted)
            compare(shell_diagnostic.comparison_omitted_power, comparison_omitted)
            compare(
                shell_diagnostic.reference_total_omitted_power,
                reference_omitted + reference_nyquist,
            )
            compare(
                shell_diagnostic.comparison_total_omitted_power,
                comparison_omitted + comparison_nyquist,
            )
            expected_reference_truncation = _error_channels(
                reference_evaluation, full_reference_evaluation
            )
            expected_comparison_truncation = _error_channels(
                comparison_evaluation, full_comparison_evaluation
            )
            expected_reference_total = _error_channels(
                reference_evaluation, direct_reference
            )
            expected_comparison_total = _error_channels(
                comparison_evaluation, direct_comparison
            )
            expected_shell_errors.append(
                _ShellErrorSummary(
                    shell_index=shell_index,
                    reference_truncation=expected_reference_truncation,
                    comparison_truncation=expected_comparison_truncation,
                    reference_total=expected_reference_total,
                    comparison_total=expected_comparison_total,
                )
            )
            expected_channel_sets = (
                (
                    shell_diagnostic.reference_truncation,
                    expected_reference_truncation,
                ),
                (
                    shell_diagnostic.comparison_truncation,
                    expected_comparison_truncation,
                ),
                (shell_diagnostic.reference_total, expected_reference_total),
                (shell_diagnostic.comparison_total, expected_comparison_total),
            )
            for observed_channels, expected_channels in expected_channel_sets:
                for observed_value, expected_value in zip(
                    _channel_values(observed_channels),
                    expected_channels,
                    strict=True,
                ):
                    compare(observed_value, expected_value)
            reference_source_rms = _error_channels(
                reference_source, full_reference_source
            )[1]
            comparison_source_rms = _error_channels(
                comparison_source, full_comparison_source
            )[1]
            compare(
                shell_diagnostic.reference_truncation_parseval_defect,
                abs(reference_source_rms**2 - reference_omitted),
            )
            compare(
                shell_diagnostic.comparison_truncation_parseval_defect,
                abs(comparison_source_rms**2 - comparison_omitted),
            )

        assert len(point.first_passing) == 1
        decision = point.first_passing[0]
        tolerance = request.band_tolerances[0]
        expected_reference_band = _select_first_passing(
            tuple(
                (shell.shell_index, shell.reference_total[2])
                for shell in expected_shell_errors
            ),
            tolerance,
        )
        expected_comparison_band = _select_first_passing(
            tuple(
                (shell.shell_index, shell.comparison_total[2])
                for shell in expected_shell_errors
            ),
            tolerance,
        )
        expected_reference_hamiltonian = _select_first_passing(
            tuple(
                (shell.shell_index, shell.reference_total[0])
                for shell in expected_shell_errors
            ),
            tolerance,
        )
        expected_comparison_hamiltonian = _select_first_passing(
            tuple(
                (shell.shell_index, shell.comparison_total[0])
                for shell in expected_shell_errors
            ),
            tolerance,
        )
        assert decision.tolerance == tolerance
        assert decision.reference_band_shell == expected_reference_band[0]
        assert decision.comparison_band_shell == expected_comparison_band[0]
        assert decision.reference_hamiltonian_shell == expected_reference_hamiltonian[0]
        assert (
            decision.comparison_hamiltonian_shell == expected_comparison_hamiltonian[0]
        )
        compare_optional(
            decision.reference_band_passing_error, expected_reference_band[1]
        )
        compare_optional(
            decision.reference_band_preceding_error, expected_reference_band[2]
        )
        compare_optional(
            decision.comparison_band_passing_error, expected_comparison_band[1]
        )
        compare_optional(
            decision.comparison_band_preceding_error, expected_comparison_band[2]
        )
        compare_optional(
            decision.reference_hamiltonian_passing_error,
            expected_reference_hamiltonian[1],
        )
        compare_optional(
            decision.reference_hamiltonian_preceding_error,
            expected_reference_hamiltonian[2],
        )
        compare_optional(
            decision.comparison_hamiltonian_passing_error,
            expected_comparison_hamiltonian[1],
        )
        compare_optional(
            decision.comparison_hamiltonian_preceding_error,
            expected_comparison_hamiltonian[2],
        )

        normalized_defects = tuple(
            abs(primary - independent) / max(1.0, abs(independent))
            for primary, independent in comparisons
        )
        assert verification.passes
        assert normalized_defects
        assert max(normalized_defects) < 5.0e-13

    @pytest.mark.parametrize("family", _FAMILIES)
    def test_flat_residual_locality_identities_match_direct_sums(
        self,
        family: definitions.BandEquivalenceLocalityFamilyEnum,
    ) -> None:
        case = _case(family)
        amplitude = math.pi / 8.0
        request = definitions.BandEquivalenceLocalityRequest(
            family=family,
            synthetic_model=definitions.FOUR_STATE_LOCALITY_DEVELOPMENT_MODEL_V1,
            cases=(case,),
            construction_size=6,
            evaluation_size=7,
            evaluation_shift=1.0 / 3.0,
            parent_scales=(0.0,),
            amplitudes=(amplitude,),
            band_tolerances=(1.0e-1,),
            shell_cap=5,
            amplitude_resolution_intervals=(1, 2),
        )
        scientific_analysis = analysis.BandEquivalenceLocalityAnalyzer(
            request=request
        ).execute()
        point = scientific_analysis.cases[0].points[0]
        coordinates = _coordinates(6, case.dimension, 0.5)
        reference, comparison = _fields(case, coordinates, 0.0, amplitude)
        identity = np.eye(2, dtype=np.complex128)
        reference_trace = np.trace(reference, axis1=-2, axis2=-1).real / 2.0
        reference_traceless = reference - reference_trace[..., None, None] * identity
        splitting_scale = float(
            np.mean(np.sum(np.abs(reference_traceless) ** 2, axis=(-2, -1))) / 2.0
        )
        if splitting_scale <= 1.0e-30:
            assert not point.alignment_applicable
            assert point.normalized_excess_nonzero_hopping_weight is None
            assert point.normalized_squared_operator_residual is None
            assert point.flat_identity_departure is None
            assert point.flat_residual_tail_identity_defect is None
            return
        alignment = _restricted_alignment_summary(reference, comparison)
        displacements, reference_blocks = _direct_blocks(coordinates, reference)
        comparison_displacements, comparison_blocks = _direct_blocks(
            coordinates, comparison
        )
        assert np.array_equal(displacements, comparison_displacements)
        onsite = np.all(displacements == 0, axis=1)
        reference_nononsite = float(np.sum(_block_powers(reference_blocks)[~onsite]))
        comparison_nononsite = float(np.sum(_block_powers(comparison_blocks)[~onsite]))
        identity_defect = abs(alignment.minimum_threshold**2 - comparison_nononsite)
        normalized_excess = (
            comparison_nononsite - reference_nononsite
        ) / alignment.splitting_scale
        normalized_residual = alignment.minimum_threshold**2 / alignment.splitting_scale

        assert point.flat_residual_tail_identity_defect == pytest.approx(
            identity_defect, abs=5.0e-13
        )
        assert identity_defect < 5.0e-13
        assert point.normalized_excess_nonzero_hopping_weight == pytest.approx(
            normalized_excess, abs=5.0e-13
        )
        assert point.normalized_squared_operator_residual == pytest.approx(
            normalized_residual, abs=5.0e-13
        )
        assert point.flat_identity_departure == pytest.approx(
            normalized_excess - normalized_residual, abs=5.0e-13
        )
        assert abs(normalized_excess - normalized_residual) < 5.0e-13

    @pytest.mark.parametrize("family", _FAMILIES)
    def test_refinement_and_midpoint_power_changes_match_direct_sums(
        self,
        family: definitions.BandEquivalenceLocalityFamilyEnum,
    ) -> None:
        case = _case(family)
        sizes = (4, 8, 16)
        amplitudes = (0.0, math.pi / 16.0, math.pi / 8.0)
        shell_cap = 3
        requests = tuple(
            definitions.BandEquivalenceLocalityRequest(
                family=family,
                synthetic_model=definitions.FOUR_STATE_LOCALITY_DEVELOPMENT_MODEL_V1,
                cases=(case,),
                construction_size=size,
                evaluation_size=size + 1,
                evaluation_shift=1.0 / 3.0,
                parent_scales=(1.0,),
                amplitudes=amplitudes,
                band_tolerances=(1.0e-3,),
                shell_cap=shell_cap,
                amplitude_resolution_intervals=(1, 2),
            )
            for size in sizes
        )
        results = tuple(
            analysis.BandEquivalenceLocalityAnalyzer(request=request).execute()
            for request in requests
        )
        assessment = BandEquivalenceLocalityRefinementAnalyzer(
            results=results
        ).execute()
        summaries = tuple(
            tuple(
                _direct_power_summary(case, size, 1.0, amplitude, shell_cap)
                for amplitude in amplitudes
            )
            for size in sizes
        )
        alignment_summaries = tuple(
            tuple(
                _direct_alignment_summary(case, size, 1.0, amplitude)
                for amplitude in amplitudes
            )
            for size in sizes
        )

        for result, level, alignment_level in zip(
            results, summaries, alignment_summaries, strict=True
        ):
            points = result.cases[0].points
            assert tuple(point.amplitude for point in points) == amplitudes
            for point, expected, expected_alignment in zip(
                points, level, alignment_level, strict=True
            ):
                assert point.reference_nononsite_power == pytest.approx(
                    expected.reference_nononsite, abs=5.0e-13
                )
                assert point.comparison_nononsite_power == pytest.approx(
                    expected.comparison_nononsite, abs=5.0e-13
                )
                assert point.excess_nonzero_hopping_weight == pytest.approx(
                    expected.comparison_nononsite - expected.reference_nononsite,
                    abs=5.0e-13,
                )
                assert point.finite_mesh_maximum_correlation == pytest.approx(
                    expected_alignment.maximum_correlation, abs=5.0e-13
                )
                assert point.minimum_operator_threshold == pytest.approx(
                    expected_alignment.minimum_threshold, abs=5.0e-13
                )
                assert point.exact_spectrum_joint_operator_threshold == pytest.approx(
                    expected_alignment.exact_spectrum_threshold, abs=5.0e-13
                )
                assert point.normalized_squared_operator_residual == pytest.approx(
                    expected_alignment.normalized_squared_residual, abs=5.0e-13
                )
                for shell_diagnostic in point.shell_diagnostics:
                    assert shell_diagnostic.reference_shell_power == pytest.approx(
                        expected.reference_shells[shell_diagnostic.shell_index],
                        abs=5.0e-13,
                    )
                    assert shell_diagnostic.comparison_shell_power == pytest.approx(
                        expected.comparison_shells[shell_diagnostic.shell_index],
                        abs=5.0e-13,
                    )

        for observed, coarse, fine in zip(
            assessment.refinements,
            summaries[:-1],
            summaries[1:],
            strict=True,
        ):
            expected_hopping_change = max(
                max(
                    abs(left.reference_nononsite - right.reference_nononsite),
                    abs(left.comparison_nononsite - right.comparison_nononsite),
                )
                for left, right in zip(coarse, fine, strict=True)
            )
            block_changes: list[float] = []
            for left, right in zip(coarse, fine, strict=True):
                common_shells = set(left.reference_shells) & set(right.reference_shells)
                for shell_index in common_shells:
                    block_changes.extend(
                        (
                            abs(
                                left.reference_shells[shell_index]
                                - right.reference_shells[shell_index]
                            ),
                            abs(
                                left.comparison_shells[shell_index]
                                - right.comparison_shells[shell_index]
                            ),
                        )
                    )
            assert observed.maximum_hopping_weight_change == pytest.approx(
                expected_hopping_change, abs=5.0e-13
            )
            assert observed.maximum_hopping_block_power_change == pytest.approx(
                max(block_changes, default=0.0), abs=5.0e-13
            )

        left, midpoint, right = summaries[-1]
        left_alignment, midpoint_alignment, right_alignment = alignment_summaries[-1]
        expected_nononsite_midpoint = abs(
            midpoint.comparison_nononsite
            - 0.5 * (left.comparison_nononsite + right.comparison_nononsite)
        )
        shell_midpoint_defects = tuple(
            abs(
                midpoint.comparison_shells[shell_index]
                - 0.5
                * (
                    left.comparison_shells[shell_index]
                    + right.comparison_shells[shell_index]
                )
            )
            for shell_index in (
                set(left.comparison_shells)
                & set(midpoint.comparison_shells)
                & set(right.comparison_shells)
            )
        )
        midpoint_diagnostic = results[-1].cases[0].amplitude_midpoint
        assert midpoint_diagnostic.applicable
        assert midpoint_diagnostic.amplitude_nodes == len(amplitudes)
        assert midpoint_diagnostic.maximum_operator_threshold_midpoint_defect == (
            pytest.approx(
                abs(
                    midpoint_alignment.minimum_threshold
                    - 0.5
                    * (
                        left_alignment.minimum_threshold
                        + right_alignment.minimum_threshold
                    )
                ),
                abs=5.0e-13,
            )
        )
        assert midpoint_diagnostic.maximum_joint_threshold_midpoint_defect == (
            pytest.approx(
                abs(
                    midpoint_alignment.exact_spectrum_threshold
                    - 0.5
                    * (
                        left_alignment.exact_spectrum_threshold
                        + right_alignment.exact_spectrum_threshold
                    )
                ),
                abs=5.0e-13,
            )
        )
        normalized_thresholds = tuple(
            value.minimum_threshold / math.sqrt(value.splitting_scale)
            for value in alignment_summaries[-1]
        )
        assert normalized_thresholds[0] == pytest.approx(0.0, abs=5.0e-13)
        assert 0.0 <= normalized_thresholds[0] <= normalized_thresholds[1]
        assert normalized_thresholds[1] <= normalized_thresholds[2]
        integrated_values = tuple(
            tuple(
                _direct_integrated_values(case, size, 1.0, amplitude, shell_cap)
                for amplitude in amplitudes
            )
            for size in sizes
        )
        coarse_integrated = tuple(
            value for point_values in integrated_values[-2] for value in point_values
        )
        fine_integrated = tuple(
            value for point_values in integrated_values[-1] for value in point_values
        )
        assert len(coarse_integrated) == len(fine_integrated)
        maximum_normalized_quadrature_change = max(
            abs(coarse - fine) / max(1.0, abs(fine))
            for coarse, fine in zip(coarse_integrated, fine_integrated, strict=True)
        )
        assert maximum_normalized_quadrature_change < 1.0e-5

        for resolution, intervals in zip(
            results[-1].cases[0].flat_amplitude_resolution,
            requests[-1].amplitude_resolution_intervals,
            strict=True,
        ):
            analytic_nodes = tuple(
                amplitudes[-1] * index / intervals for index in range(intervals + 1)
            )
            assert resolution.amplitude_intervals == intervals
            assert resolution.amplitude_nodes == len(analytic_nodes)
            assert analytic_nodes[0] == 0.0
            assert analytic_nodes[-1] == amplitudes[-1]
        assert midpoint_diagnostic.maximum_nonzero_hopping_weight_midpoint_defect == (
            pytest.approx(expected_nononsite_midpoint, abs=5.0e-13)
        )
        assert midpoint_diagnostic.maximum_hopping_block_power_midpoint_defect == (
            pytest.approx(max(shell_midpoint_defects, default=0.0), abs=5.0e-13)
        )
