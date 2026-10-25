"""Verify KSD consumption of owner-provided batched Procrustes transport."""

from __future__ import annotations

from dataclasses import replace
from typing import ClassVar

import numpy as np
import pytest
from band_equivalence_workflow import application, schemas
from jsonschema import ValidationError  # type: ignore[import-untyped]
from numpy.typing import NDArray
from projectkoios.optimization.alignment.numpy.batched_procrustes import (
    NumpyBatchedComplexUnitaryProcrustesDefinition,
    NumpyBatchedComplexUnitaryProcrustesResult,
    NumpyBatchedComplexUnitaryProcrustesSolver,
)
from projectkoios.physkit.periodic.lattice import DirectLattice2D, DirectLatticeMetric

from ksdft2effmass.analysis.model_adequacy.band_equivalence_locality import (
    alignment,
    definitions,
)

type ComplexArray = NDArray[np.complex128]


def _rotation(angle: float) -> ComplexArray:
    cosine = np.cos(angle)
    sine = np.sin(angle)
    return np.asarray([[cosine, -sine], [sine, cosine]], dtype=np.complex128)


def _full_rank_frame(dimension: int, size: int = 3) -> ComplexArray:
    shape = (size,) * dimension
    frame = np.zeros((*shape, 4, 2), dtype=np.complex128)
    coordinates = np.indices(shape, dtype=np.float64)
    angle = np.sum(coordinates, axis=0) * (0.17 / float(size))
    for index in np.ndindex(shape):
        frame[index][:2, :] = _rotation(float(angle[index]))
    return frame


def _deficient_frame(dimension: int) -> ComplexArray:
    shape = (2,) * dimension
    frame = np.zeros((*shape, 4, 2), dtype=np.complex128)
    for index in np.ndindex(shape):
        frame[index][0, 0] = 1.0
        frame[index][1 if index[0] == 0 else 2, 1] = 1.0
    return frame


def _local_full_rank_reference(
    frame: ComplexArray, dimension: int
) -> tuple[float, float, float, tuple[float, float], float, float]:
    identity = np.eye(2, dtype=np.complex128)
    minimum_singular = 1.0
    maximum_residual = 0.0
    maximum_unitarity = 0.0
    maximum_phase = np.zeros(2, dtype=np.float64)
    maximum_closure_unitarity = 0.0
    links_by_axis: list[ComplexArray] = []
    for axis in range(dimension):
        neighbor = np.roll(frame, shift=-1, axis=axis)
        overlap = np.swapaxes(frame.conjugate(), -1, -2) @ neighbor
        left, singular_values, right_adjoint = np.linalg.svd(overlap)
        links = left @ right_adjoint
        links_by_axis.append(links)
        minimum_singular = min(minimum_singular, float(np.min(singular_values)))
        residual = np.linalg.norm(frame @ links - neighbor, axis=(-2, -1))
        maximum_residual = max(maximum_residual, float(np.max(residual)))
        unitarity = np.linalg.norm(
            np.swapaxes(links.conjugate(), -1, -2) @ links
            - np.broadcast_to(identity, links.shape),
            axis=(-2, -1),
        )
        maximum_unitarity = max(maximum_unitarity, float(np.max(unitarity)))
        ordered = np.moveaxis(links, axis, 0).reshape(links.shape[axis], -1, 2, 2)
        holonomy = np.broadcast_to(identity, (ordered.shape[1], 2, 2)).copy()
        for link in ordered:
            holonomy = holonomy @ link
        closure_unitarity = np.linalg.norm(
            np.swapaxes(holonomy.conjugate(), -1, -2) @ holonomy
            - np.broadcast_to(identity, holonomy.shape),
            axis=(-2, -1),
        )
        maximum_closure_unitarity = max(
            maximum_closure_unitarity, float(np.max(closure_unitarity))
        )
        phases = np.sort(np.angle(np.linalg.eigvals(holonomy)), axis=-1)
        maximum_phase = np.maximum(maximum_phase, np.max(np.abs(phases), axis=0))
    maximum_plaquette = 0.0
    for first_axis in range(dimension):
        for second_axis in range(first_axis + 1, dimension):
            first = links_by_axis[first_axis]
            second = links_by_axis[second_axis]
            plaquette = (
                first
                @ np.roll(second, shift=-1, axis=first_axis)
                @ np.swapaxes(
                    np.roll(first, shift=-1, axis=second_axis).conjugate(), -1, -2
                )
                @ np.swapaxes(second.conjugate(), -1, -2)
            )
            maximum_plaquette = max(
                maximum_plaquette,
                float(np.max(np.abs(np.angle(np.linalg.eigvals(plaquette))))),
            )
    return (
        minimum_singular,
        maximum_residual,
        maximum_unitarity,
        (float(maximum_phase[0]), float(maximum_phase[1])),
        maximum_closure_unitarity,
        maximum_plaquette,
    )


class TestFrameTransportDiagnostics:
    """Establish the KSD boundary around the owner batched solver."""

    dimensions: ClassVar[tuple[int, ...]] = (2, 3)

    @staticmethod
    def analysis_request() -> definitions.BandEquivalenceLocalityRequest:
        """Return one bounded square-family serialization fixture."""
        return definitions.BandEquivalenceLocalityRequest(
            family=definitions.BandEquivalenceLocalityFamily.SQUARE,
            cases=(
                definitions.BandEquivalenceLocalityCase(
                    name="square-directed",
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
                ),
            ),
            construction_size=4,
            evaluation_size=9,
            evaluation_shift=1.0 / 3.0,
            parent_scales=(0.0,),
            amplitudes=(0.0,),
            band_tolerances=(1.0e-3,),
            shell_cap=3,
        )

    @pytest.mark.parametrize("dimension", dimensions)
    def test_full_rank_transport_matches_local_reference(self, dimension: int) -> None:
        frame = _full_rank_frame(dimension)
        observed = alignment.frame_transport_diagnostics(
            frame, dimension, 1.0e-10, 1.0e-12
        )
        expected = _local_full_rank_reference(frame, dimension)

        assert observed.minimum_singular_value == pytest.approx(expected[0], abs=1e-15)
        assert observed.maximum_procrustes_residual == pytest.approx(
            expected[1], abs=3e-14
        )
        assert observed.maximum_unitarity_defect == pytest.approx(
            expected[2], abs=1e-15
        )
        assert observed.maximum_absolute_closure_phases == pytest.approx(
            expected[3], abs=1e-15
        )
        assert observed.maximum_closure_unitarity_defect == pytest.approx(
            expected[4], abs=1e-15
        )
        assert observed.maximum_plaquette_phase == pytest.approx(expected[5], abs=1e-15)
        assert observed.maximum_squared_residual_roundoff_cutoff >= 0.0
        assert observed.rank_deficient_link_count == 0
        assert observed.closure_and_plaquette_applicable
        assert observed.closure_and_plaquette_inapplicable_reason is None

    def test_owner_right_action_aligns_each_captured_axis(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        frame = _full_rank_frame(2)
        captured: list[
            tuple[
                NumpyBatchedComplexUnitaryProcrustesDefinition,
                ComplexArray,
            ]
        ] = []
        owner = NumpyBatchedComplexUnitaryProcrustesSolver()

        class CapturingSolver:
            def solve(
                self, definition: NumpyBatchedComplexUnitaryProcrustesDefinition
            ) -> NumpyBatchedComplexUnitaryProcrustesResult:
                result = owner.solve(definition)
                captured.append((definition, result.right_unitary_completions))
                return result

        monkeypatch.setattr(
            "ksdft2effmass.analysis.model_adequacy.band_equivalence_locality."
            "alignment.NumpyBatchedComplexUnitaryProcrustesSolver",
            CapturingSolver,
        )
        alignment.frame_transport_diagnostics(frame, 2, 1.0e-10, 1.0e-12)

        assert len(captured) == 2
        for definition, completions in captured:
            aligned = definition.source_matrices @ completions
            residuals = np.linalg.norm(
                aligned - definition.target_matrices, axis=(-2, -1)
            )
            assert float(np.max(residuals)) < 3.0e-14

    def test_additive_cutoff_equality_is_rank_deficient(self) -> None:
        frame = np.zeros((2, 2, 4, 2), dtype=np.complex128)
        frame[0, ..., 0, 0] = 1.0
        frame[0, ..., 1, 1] = 1.0
        frame[1, ..., 0, 0] = 1.0
        frame[1, ..., 1, 1] = 0.5
        frame[1, ..., 2, 1] = np.sqrt(0.75)

        observed = alignment.frame_transport_diagnostics(frame, 2, 0.2, 0.3)

        assert observed.maximum_rank_cutoff == pytest.approx(0.5)
        assert observed.rank_deficient_link_count > 0
        assert not observed.closure_and_plaquette_applicable
        assert (
            observed.closure_and_plaquette_inapplicable_reason
            == definitions.TRANSPORT_RANK_DEFICIENT_REASON
        )

    @pytest.mark.parametrize("dimension", dimensions)
    def test_rank_deficiency_fails_closed_before_topology(
        self, dimension: int, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        def prohibited_eigenvalues(_: ComplexArray) -> ComplexArray:
            raise AssertionError("topology must not use deficient completions")

        monkeypatch.setattr(
            "ksdft2effmass.analysis.model_adequacy.band_equivalence_locality."
            "alignment.np.linalg.eigvals",
            prohibited_eigenvalues,
        )
        observed = alignment.frame_transport_diagnostics(
            _deficient_frame(dimension), dimension, 1.0e-10, 1.0e-12
        )

        assert observed.rank_deficient_link_count > 0
        assert not observed.closure_and_plaquette_applicable
        assert observed.maximum_absolute_closure_phases is None
        assert observed.maximum_closure_unitarity_defect is None
        assert observed.maximum_plaquette_phase is None

    def test_owner_failure_propagates_without_fabricated_diagnostic(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        class FailingSolver:
            def solve(
                self, definition: NumpyBatchedComplexUnitaryProcrustesDefinition
            ) -> NumpyBatchedComplexUnitaryProcrustesResult:
                del definition
                raise np.linalg.LinAlgError("synthetic owner failure")

        monkeypatch.setattr(
            "ksdft2effmass.analysis.model_adequacy.band_equivalence_locality."
            "alignment.NumpyBatchedComplexUnitaryProcrustesSolver",
            FailingSolver,
        )
        with pytest.raises(np.linalg.LinAlgError, match="synthetic owner failure"):
            alignment.frame_transport_diagnostics(
                _full_rank_frame(2), 2, 1.0e-10, 1.0e-12
            )

    def test_roundoff_cutoff_and_v1_schema_are_joint_evidence(self) -> None:
        definition = self.analysis_request()
        result = application.BandEquivalenceLocalityResultConstructor().execute(
            definition
        )
        point = result.diagnostics.cases[0].points[0]

        assert point.maximum_transport_procrustes_residual == 0.0
        assert point.maximum_transport_squared_residual_roundoff_cutoff > 0.0
        document = result.document
        schemas.BandEquivalenceLocalitySchema(
            result.diagnostics.family,
            schemas.BandEquivalenceLocalitySchemaKind.ANALYSIS_RESULT,
        ).validate(document.canonical_bytes())
        assert b'"schema":"' in document.canonical_bytes()
        assert b'.v1"' in document.canonical_bytes()

    def test_record_and_schema_reject_zero_filled_inapplicable_topology(self) -> None:
        definition = self.analysis_request()
        result = application.BandEquivalenceLocalityResultConstructor().execute(
            definition
        )
        point = result.diagnostics.cases[0].points[0]
        with pytest.raises(ValueError, match="prohibits topology diagnostics"):
            replace(
                point,
                transport_rank_deficient_link_count=1,
                transport_closure_and_plaquette_applicable=False,
                transport_closure_and_plaquette_inapplicable_reason=(
                    definitions.TRANSPORT_RANK_DEFICIENT_REASON
                ),
                maximum_absolute_closure_holonomy_phases=(0.0, 0.0),
                maximum_closure_holonomy_unitarity_defect=0.0,
                maximum_plaquette_holonomy_phase=0.0,
            )

        document = result.document
        malformed = document.canonical_bytes().replace(
            b'"transport_rank_deficient_link_count":0',
            b'"transport_rank_deficient_link_count":1',
        )
        malformed = malformed.replace(
            b'"transport_closure_and_plaquette_applicable":true',
            b'"transport_closure_and_plaquette_applicable":false',
        )
        malformed = malformed.replace(
            b'"transport_closure_and_plaquette_inapplicable_reason":null',
            b'"transport_closure_and_plaquette_inapplicable_reason":'
            b'"rank-deficient neighbor overlap does not identify unique transport"',
        )
        with pytest.raises(ValidationError):
            schemas.BandEquivalenceLocalitySchema(
                result.diagnostics.family,
                schemas.BandEquivalenceLocalitySchemaKind.ANALYSIS_RESULT,
            ).validate(malformed)
