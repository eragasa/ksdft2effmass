"""Software verification for higher-rank D1 calculator failure dispositions."""

from __future__ import annotations

import pytest
from projectkoios.numerics.numpy.typing import Complex128Array
from workflow import (
    HigherRankD1A1NumericallyUnresolvedSelection,
    HigherRankD1A1Selection,
    HigherRankD1A2RankDeficientSelection,
    HigherRankD1A2SelectionResult,
    HigherRankD1AlignmentBackendError,
    HigherRankD1BackendExceptionCode,
    HigherRankD1CaseCalculator,
    HigherRankD1CaseDefinition,
    HigherRankD1ChannelMeshDiagnostics,
    HigherRankD1InapplicableChannelMeshDiagnostics,
    HigherRankD1TransportBackendError,
    HigherRankD1TransportNumericallyUnresolvedDiagnostics,
    HigherRankD1TransportResult,
)
from workflow import case_calculation as d1_case_calculation

pytestmark = pytest.mark.software_verification


class TestHigherRankD1CaseCalculatorFailureDispositions:
    """Establish invalid-case records without null completion or escaped failure."""

    def test_execute__retains_inapplicability_and_numerical_nonresolution(
        self,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """A2 deficiency and transport failure produce one bounded invalid result."""

        class ForcedAlignmentSelector:
            """Throw for A1 and return pointwise-deficient A2 evidence."""

            __slots__ = ()

            def select_a1(
                self,
                candidate_frames: Complex128Array,
                reference_frames: Complex128Array,
            ) -> HigherRankD1A1Selection:
                del candidate_frames, reference_frames
                raise HigherRankD1AlignmentBackendError(RuntimeError())

            def select_a2(
                self,
                candidate_frames: Complex128Array,
                reference_frames: Complex128Array,
            ) -> HigherRankD1A2SelectionResult:
                del reference_frames
                mesh_size = int(candidate_frames.shape[0])
                return HigherRankD1A2RankDeficientSelection(
                    mesh_size=mesh_size,
                    rank=int(candidate_frames.shape[-1]),
                    smallest_singular_values=(0.0,) * mesh_size,
                    applied_rank_cutoffs=(1.0e-12,) * mesh_size,
                    rank_margins=(-1.0e-12,) * mesh_size,
                    numerical_ranks=(0,) * mesh_size,
                    deficient_indices=tuple(range(mesh_size)),
                )

        class ForcedTransportAnalyzer:
            """Throw one backend failure with bounded route context."""

            __slots__ = ()

            def execute(
                self,
                frames: Complex128Array,
                endpoint_frame: Complex128Array,
            ) -> HigherRankD1TransportResult:
                del frames, endpoint_frame
                raise HigherRankD1TransportBackendError("link", 1, RuntimeError())

        monkeypatch.setattr(
            d1_case_calculation,
            "HigherRankD1AlignmentSelector",
            ForcedAlignmentSelector,
        )
        monkeypatch.setattr(
            d1_case_calculation,
            "HigherRankD1TransportAnalyzer",
            ForcedTransportAnalyzer,
        )

        result = HigherRankD1CaseCalculator().execute(HigherRankD1CaseDefinition(3, 1))

        assert result.qualification == "numerically-unresolved"
        assert result.failed_gate_paths
        assert isinstance(
            result.a1_selection, HigherRankD1A1NumericallyUnresolvedSelection
        )
        assert (
            result.a1_selection.exception_code
            is HigherRankD1BackendExceptionCode.NONCONVERGENCE
        )
        for mesh in result.meshes:
            assert isinstance(
                mesh.transport,
                HigherRankD1TransportNumericallyUnresolvedDiagnostics,
            )
            assert (
                mesh.transport.exception_code
                is HigherRankD1BackendExceptionCode.NONCONVERGENCE
            )
            assert isinstance(mesh.a2_selection, HigherRankD1A2RankDeficientSelection)
            a1_channel = mesh.channels[1]
            assert isinstance(
                a1_channel,
                HigherRankD1InapplicableChannelMeshDiagnostics,
            )
            assert a1_channel.downstream_applicability == (
                "inapplicable-alignment-numerically-unresolved"
            )
            a2_channel = mesh.channels[2]
            assert isinstance(
                a2_channel,
                HigherRankD1InapplicableChannelMeshDiagnostics,
            )
            assert a2_channel.downstream_applicability == (
                "inapplicable-pointwise-rank-deficient"
            )
        for channel in result.meshes[-1].channels:
            if isinstance(channel, HigherRankD1ChannelMeshDiagnostics):
                assert channel.pareto_points == ()
                assert channel.pareto_role == "inapplicable-technical-qualification"
