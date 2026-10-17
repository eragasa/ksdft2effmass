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
    calculation,
    definitions,
)
from ksdft2effmass.analysis.model_adequacy.band_equivalence_locality.records import (
    ErrorChannels,
)
from ksdft2effmass.analysis.model_adequacy.band_equivalence_locality.refinement import (
    BandEquivalenceLocalityRefinementAnalyzer,
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


def _case(
    family: definitions.BandEquivalenceLocalityFamily,
) -> definitions.BandEquivalenceLocalityCase:
    if family is definitions.BandEquivalenceLocalityFamily.SQUARE:
        return definitions.BandEquivalenceLocalityCase(
            name="square-directed-parent",
            dimension=2,
            parent_kind=definitions.ParentKind.DIRECTED_AXIS,
            gauge_normalization=definitions.GaugeNormalization.AXIS_MAXIMUM,
            positive_bonds=((1, 0), (0, 1)),
            direct_metric=DirectLatticeMetric(
                DirectLattice2D(
                    a1=np.array((1.0, 0.0), dtype=np.float64),
                    a2=np.array((0.0, 1.0), dtype=np.float64),
                )
            ),
            shell_metric_scale=1.0,
        )
    if family is definitions.BandEquivalenceLocalityFamily.SIMPLE_CUBIC:
        return definitions.BandEquivalenceLocalityCase(
            name="simple-cubic-directed-parent",
            dimension=3,
            parent_kind=definitions.ParentKind.DIRECTED_AXIS,
            gauge_normalization=definitions.GaugeNormalization.AXIS_MAXIMUM,
            positive_bonds=((1, 0, 0), (0, 1, 0), (0, 0, 1)),
            direct_metric=DirectLatticeMetric(
                BravaisLattice.cubic_primitive().direct_lattice
            ),
            shell_metric_scale=1.0,
        )
    if family is definitions.BandEquivalenceLocalityFamily.GRAPHENE_INSPIRED:
        return definitions.BandEquivalenceLocalityCase(
            name="graphene-inspired-honeycomb",
            dimension=2,
            parent_kind=definitions.ParentKind.BIPARTITE_INSPIRED,
            gauge_normalization=definitions.GaugeNormalization.BOND_RMS,
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
        parent_kind=definitions.ParentKind.BIPARTITE_INSPIRED,
        gauge_normalization=definitions.GaugeNormalization.BOND_RMS,
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
    if case.parent_kind is definitions.ParentKind.DIRECTED_AXIS:
        phase_average = np.mean(np.exp(2.0j * np.pi * coordinates), axis=-1)
        scaled = parent_scale * phase_average
        result += scaled[..., None, None] * _DIRECTED
        result += scaled.conjugate()[..., None, None] * _DIRECTED.conjugate().T
        return result
    if case.parent_kind is definitions.ParentKind.HERMITIAN_BRAVAIS:
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
    if case.gauge_normalization is definitions.GaugeNormalization.AXIS_MAXIMUM:
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


_FAMILIES = tuple(definitions.BandEquivalenceLocalityFamily)


class TestFourierLocalityParity:
    """Reconstruct power, omission, identity, and refinement channels directly."""

    @pytest.mark.parametrize("family", _FAMILIES)
    def test_all_point_channels_match_independent_finite_sums(
        self,
        family: definitions.BandEquivalenceLocalityFamily,
    ) -> None:
        case = _case(family)
        size = 6
        evaluation_size = 7
        parent_scale = 1.0
        amplitude = math.pi / 8.0
        shell_cap = 5
        request = definitions.BandEquivalenceLocalityRequest(
            family=family,
            cases=(case,),
            construction_size=size,
            evaluation_size=evaluation_size,
            evaluation_shift=1.0 / 3.0,
            parent_scales=(parent_scale,),
            amplitudes=(amplitude,),
            band_tolerances=(1.0e-3,),
            shell_cap=shell_cap,
            amplitude_resolution_intervals=(1, 2),
        )
        diagnostics = calculation.BandEquivalenceLocalityCalculator().execute(request)
        verification = calculation.BandEquivalenceLocalityVerifier().execute(
            request, diagnostics
        )
        point = diagnostics.cases[0].points[0]
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

        discrepancies: list[float] = []

        def compare(observed: float, expected: float) -> None:
            discrepancies.append(abs(observed - expected))

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
        compare(
            point.reference_fourier_reconstruction_defect,
            _maximum_matrix_defect(reconstructed_reference, reference),
        )
        compare(
            point.comparison_fourier_reconstruction_defect,
            _maximum_matrix_defect(reconstructed_comparison, comparison),
        )
        compare(
            point.reference_parseval_defect,
            abs(
                float(np.mean(np.sum(np.abs(reference) ** 2, axis=(-2, -1))))
                - float(np.sum(np.abs(reference_blocks) ** 2))
            ),
        )
        compare(
            point.comparison_parseval_defect,
            abs(
                float(np.mean(np.sum(np.abs(comparison) ** 2, axis=(-2, -1))))
                - float(np.sum(np.abs(comparison_blocks) ** 2))
            ),
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
            expected_channel_sets = (
                (
                    shell_diagnostic.reference_truncation,
                    _error_channels(reference_evaluation, full_reference_evaluation),
                ),
                (
                    shell_diagnostic.comparison_truncation,
                    _error_channels(comparison_evaluation, full_comparison_evaluation),
                ),
                (
                    shell_diagnostic.reference_total,
                    _error_channels(reference_evaluation, direct_reference),
                ),
                (
                    shell_diagnostic.comparison_total,
                    _error_channels(comparison_evaluation, direct_comparison),
                ),
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

        assert verification.passes
        assert max(discrepancies, default=0.0) < 5.0e-13

    @pytest.mark.parametrize("family", _FAMILIES)
    def test_refinement_and_midpoint_power_changes_match_direct_sums(
        self,
        family: definitions.BandEquivalenceLocalityFamily,
    ) -> None:
        case = _case(family)
        sizes = (4, 8, 16)
        amplitudes = (0.0, math.pi / 16.0, math.pi / 8.0)
        shell_cap = 3
        requests = tuple(
            definitions.BandEquivalenceLocalityRequest(
                family=family,
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
            calculation.BandEquivalenceLocalityCalculator().execute(request)
            for request in requests
        )
        assessment = BandEquivalenceLocalityRefinementAnalyzer().execute(results)
        summaries = tuple(
            tuple(
                _direct_power_summary(case, size, 1.0, amplitude, shell_cap)
                for amplitude in amplitudes
            )
            for size in sizes
        )

        for result, level in zip(results, summaries, strict=True):
            points = result.cases[0].points
            for point, expected in zip(points, level, strict=True):
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
        assert midpoint_diagnostic.maximum_nonzero_hopping_weight_midpoint_defect == (
            pytest.approx(expected_nononsite_midpoint, abs=5.0e-13)
        )
        assert midpoint_diagnostic.maximum_hopping_block_power_midpoint_defect == (
            pytest.approx(max(shell_midpoint_defects, default=0.0), abs=5.0e-13)
        )
