"""Tests for the maintained rank-N composite-band alignment public surface."""

import ast
import importlib
from pathlib import Path

import pytest

from ksdft2effmass.periodic1d.rankN import gauge_alignment
from ksdft2effmass.periodic1d.rankN.band_alignment import (
    composite as rankn_composite_band_alignment,
)
from ksdft2effmass.periodic1d.rankN.gauge_alignment.status import (
    Periodic1DRankNAlignmentStatusResult,
)

pytestmark = [pytest.mark.unit, pytest.mark.software_verification]


class TestPeriodic1DRankNAlignmentStatusResult:
    """Establish explicit exports and isolate calculation-local donor code."""

    def test__package__is_a_non_eager_orchestration_namespace(self) -> None:
        assert not hasattr(rankn_composite_band_alignment, "__all__")
        assert not any(
            name.startswith("Periodic1D")
            for name in vars(rankn_composite_band_alignment)
        )

    def test__status_result__belongs_to_the_rankN_alignment_partition(self) -> None:
        assert Periodic1DRankNAlignmentStatusResult.__module__ == (
            "ksdft2effmass.periodic1d.rankN.gauge_alignment.status"
        )

    def test__gauge_alignment_package__is_a_non_eager_namespace(self) -> None:
        assert not hasattr(gauge_alignment, "__all__")
        assert not any(
            name.startswith("Periodic1DRankN") for name in vars(gauge_alignment)
        )

    def test__package__does_not_reexport_internal_analysis_actions(self) -> None:
        internal_names = (
            "Periodic1DRankNGaugeAlignmentAnalysisRequest",
            "Periodic1DRankNCompositeGaugeCaseAnalyzer",
            "Periodic1DRankNEvaluationIndependenceAnalyzer",
            "Periodic1DRankNEvaluationIndependenceResult",
            "Periodic1DRankNRefinementAnalysis",
            "Periodic1DRankNRefinementAnalysisRequest",
            "Periodic1DRankNRefinementAnalyzer",
            "Periodic1DRankNCoreInvariantReference",
            "Periodic1DRankNCoreInvariantReferenceAnalyzer",
            "Periodic1DRankNCoreInvariantReferenceRequest",
            "Periodic1DRankNFourierReference",
            "Periodic1DRankNFourierReferenceAnalyzer",
            "Periodic1DRankNFourierReferenceRequest",
            "Periodic1DRankNProcrustesReference",
            "Periodic1DRankNProcrustesReferenceAnalyzer",
            "Periodic1DRankNProcrustesReferenceRequest",
            "Periodic1DRankNTransportReference",
            "Periodic1DRankNTransportReferenceAnalyzer",
            "Periodic1DRankNTransportReferenceRequest",
            "Periodic1DRankNAlignmentTransportBackendFailureResult",
            "Periodic1DRankNAlignmentTransportLinkResult",
            "Periodic1DRankNAlignmentTransportOwnerResult",
            "Periodic1DRankNAlignmentTransportRequest",
            "Periodic1DRankNTransportBackendExceptionCode",
        )

        assert all(
            not hasattr(rankn_composite_band_alignment, name) for name in internal_names
        )

    def test__records__belong_to_their_partitioned_owner_modules(self) -> None:
        expected_modules = {
            "Periodic1DRankNAlignmentCalculationControls": (
                "band_alignment.calculation"
            ),
            "Periodic1DRankNAlignmentCalculationRequest": (
                "band_alignment.calculation"
            ),
            "Periodic1DRankNAlignmentCalculationResult": (
                "band_alignment.calculation_result"
            ),
            "Periodic1DRankNAlignmentStatusResult": "gauge_alignment.status",
            "Periodic1DRankNGaugeAlignmentMeshResult": (
                "band_alignment.gauge_case_result"
            ),
            "Periodic1DRankNMeshCalculationResult": (
                "band_alignment.construction_mesh_result"
            ),
            "Periodic1DRankNSupportResult": "support_truncation.result",
            "Periodic1DRankNModelDiagnostics": "band_alignment.model_diagnostics",
            "Periodic1DRankNProcrustesDiagnostics": (
                "gauge_alignment.procrustes.result"
            ),
            "Periodic1DRankNBlockRefinementResult": (
                "band_alignment.refinement_result"
            ),
            "Periodic1DRankNScalarRefinementResult": (
                "band_alignment.refinement_result"
            ),
        }

        for name, module_suffix in expected_modules.items():
            module = importlib.import_module(
                f"ksdft2effmass.periodic1d.rankN.{module_suffix}"
            )
            record = getattr(module, name)
            assert record.__module__.endswith(f".{module_suffix}")

        analyzer_module = importlib.import_module(
            "ksdft2effmass.periodic1d.rankN.band_alignment.composite.calculation"
        )
        assert analyzer_module.Periodic1DRankNAlignmentAnalyzer.__module__.endswith(
            ".composite.calculation"
        )

        transport_failure_module = importlib.import_module(
            "ksdft2effmass.periodic1d.rankN.band_alignment.frame_transport.failure"
        )
        for name in (
            "Periodic1DRankNAlignmentTransportBackendFailureResult",
            "Periodic1DRankNTransportBackendExceptionCode",
        ):
            record = getattr(transport_failure_module, name)
            assert record.__module__.endswith(".band_alignment.frame_transport.failure")

        transport_link_module = importlib.import_module(
            "ksdft2effmass.periodic1d.rankN.band_alignment.frame_transport.link"
        )
        link_record = transport_link_module.Periodic1DRankNAlignmentTransportLinkResult
        assert link_record.__module__.endswith(".band_alignment.frame_transport.link")

        transport_result_module = importlib.import_module(
            "ksdft2effmass.periodic1d.rankN.band_alignment.frame_transport.result"
        )
        owner_record = (
            transport_result_module.Periodic1DRankNAlignmentTransportOwnerResult
        )
        assert owner_record.__module__.endswith(
            ".band_alignment.frame_transport.result"
        )

        calculation_module = importlib.import_module(
            "ksdft2effmass.periodic1d.rankN.band_alignment.calculation"
        )
        moved_names = expected_modules.keys() - {
            "Periodic1DRankNAlignmentCalculationControls",
            "Periodic1DRankNAlignmentCalculationRequest",
        }
        assert all(not hasattr(calculation_module, name) for name in moved_names)

    def test__obsolete_owner_modules__are_absent(self) -> None:
        for module_name in (
            "ksdft2effmass.periodic1d.rankN.band_alignment.request",
            "ksdft2effmass.periodic1d.rankN.band_alignment.composite.transport",
            "ksdft2effmass.periodic1d.rankN.band_alignment.composite.result",
            (
                "ksdft2effmass.periodic1d.rankN.band_alignment.composite."
                "gauge_alignment_result"
            ),
            (
                "ksdft2effmass.periodic1d.rankN.band_alignment.composite."
                "construction_mesh_result"
            ),
            (
                "ksdft2effmass.periodic1d.rankN.band_alignment.composite."
                "calculation_result"
            ),
            (
                "ksdft2effmass.periodic1d.rankN.band_alignment.composite."
                "refinement_results"
            ),
            ("ksdft2effmass.periodic1d.rankN.band_alignment.composite.provenance"),
            (
                "ksdft2effmass.periodic1d.rankN.band_alignment.composite."
                "scalar_diagnostics"
            ),
            (
                "ksdft2effmass.periodic1d.rankN.band_alignment.composite.result."
                "gauge_alignment"
            ),
            "ksdft2effmass.periodic1d.rankN.band_alignment.composite.result.mesh",
            (
                "ksdft2effmass.periodic1d.rankN.band_alignment.composite.result."
                "frame_transport"
            ),
        ):
            with pytest.raises(ModuleNotFoundError):
                importlib.import_module(module_name)

    def test__source__does_not_import_calculation_workflow_material(self) -> None:
        package = Path(rankn_composite_band_alignment.__file__).resolve().parent

        for path in package.rglob("*.py"):
            source = path.read_text(encoding="utf-8")
            tree = ast.parse(source, filename=str(path))
            imported_modules = {
                node.module
                for node in ast.walk(tree)
                if isinstance(node, ast.ImportFrom) and node.module is not None
            } | {
                alias.name
                for node in ast.walk(tree)
                if isinstance(node, ast.Import)
                for alias in node.names
            }
            assert all("workflow" not in module for module in imported_modules)
            assert "HigherRankD1" not in source
