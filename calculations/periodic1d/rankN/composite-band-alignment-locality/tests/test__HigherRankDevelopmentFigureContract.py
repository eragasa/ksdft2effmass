"""Contracts for explicitly unverified higher-rank development figures."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pytest
from analysis.development import (
    HigherRankDevelopmentCacheAdmission,
    HigherRankDevelopmentCacheEntry,
    HigherRankDevelopmentCacheManifest,
    HigherRankDevelopmentPlot,
)
from analysis.development.plots import (
    _DEVELOPMENT_NOTICE,
    _PLOT_FLOOR,
    _claim_condition,
    _positive,
    _sampled_pareto_membership,
)
from ksdft2effmass.periodic1d.higher_rank_alignment import (
    Periodic1DHigherRankAlignmentConfiguration,
)

pytestmark = pytest.mark.software_verification


class TestHigherRankDevelopmentFigureContract:
    """Establish the closed inventory, disclaimers, and sampled Pareto rule."""

    def test__plot_inventory__contains_every_predeclared_view(self) -> None:
        assert tuple(plot.value for plot in HigherRankDevelopmentPlot) == (
            "development-alignment-locality-s2.png",
            "development-support-locality-paths.png",
            "development-fourier-block-locality.png",
            "development-error-channel-trajectories.png",
            "development-s2-claim-resolution.png",
            "development-mesh-refinement.png",
            "development-rank-depth-scaling.png",
            "development-recovery-controls.png",
            "development-support-error-pareto.png",
        )
        assert _DEVELOPMENT_NOTICE == (
            "DEVELOPMENT / UNVERIFIED — not publication evidence"
        )

    def test__sampled_pareto_membership__uses_joint_three_objective_dominance(
        self,
    ) -> None:
        objectives = np.asarray(
            (
                (1.0, 3.0, 3.0),
                (3.0, 2.0, 2.0),
                (5.0, 2.0, 2.0),
            ),
            dtype=np.float64,
        )

        efficient = _sampled_pareto_membership(objectives)

        assert np.array_equal(efficient, np.asarray((True, True, False)))
        assert not efficient.flags.writeable

    def test__claim_condition__preserves_missing_and_failed_states(self) -> None:
        assert (
            _claim_condition(
                np.float64("nan"),
                status_code=0,
                qualified_code=0,
                threshold=1.0e-6,
                larger_is_resolved=True,
            )
            is None
        )
        assert (
            _claim_condition(
                np.float64(1.0),
                status_code=1,
                qualified_code=0,
                threshold=1.0e-6,
                larger_is_resolved=True,
            )
            is None
        )

    def test__log_display_floor__does_not_change_exact_zero_source_value(self) -> None:
        values = np.asarray((0.0, _PLOT_FLOOR / 10.0, _PLOT_FLOOR * 2.0))

        displayed = _positive(values)

        assert values[0] == 0.0
        assert np.array_equal(
            displayed,
            np.asarray((_PLOT_FLOOR, _PLOT_FLOOR, _PLOT_FLOOR * 2.0)),
        )

    def test__technical_report__uses_descriptive_terms_not_internal_shorthand(
        self,
    ) -> None:
        report = (
            Path(__file__).resolve().parents[1]
            / "technical-report"
            / "technical_report.tex"
        ).read_text(encoding="utf-8")

        for shorthand in ("D1", "P0", "P1", "G0", "G1", "A0", "A1", "A2", "A3"):
            assert shorthand not in report

    def test__render_entrypoint__declares_non_evidence_lifecycle(self) -> None:
        entrypoint = Path(__file__).resolve().parents[1] / "run_03_render.py"
        source = entrypoint.read_text(encoding="utf-8")

        assert "scientific_evidence=false" in source
        assert "HigherRankDevelopmentAdmittedCacheReader" in source
        assert "HigherRankDevelopmentFigureDataProjector" in source
        assert "HigherRankDevelopmentFigureRenderer" in source
        assert "_calculation_results" not in source
        assert "workflow" not in source

    def test__cache_manifest__is_canonical_and_explicitly_not_evidence(self) -> None:
        configuration = Periodic1DHigherRankAlignmentConfiguration
        entries = tuple(
            HigherRankDevelopmentCacheEntry(
                case_identity=f"case-r{rank}-l{depth}",
                retained_rank=rank,
                circuit_depth=depth,
                file_name=f"result-r{rank}-l{depth}.json",
                result_sha256="0" * 64,
                byte_count=1,
            )
            for rank in configuration.RETAINED_RANKS
            for depth in configuration.CIRCUIT_DEPTHS
        )
        manifest = HigherRankDevelopmentCacheManifest(
            artifact_role="replaceable-development-result-cache",
            scientific_evidence=False,
            cache_format=("ksdft2effmass.higher-rank-development-result-cache.v1"),
            family_identity=configuration.FAMILY_IDENTITY,
            version_identity=configuration.VERSION_IDENTITY,
            calculation_infrastructure_sha256="1" * 64,
            entries=entries,
        )

        wire = manifest.to_json()

        assert HigherRankDevelopmentCacheManifest.from_json(wire).to_json() == wire
        assert manifest.scientific_evidence is False
        assert manifest.calculation_infrastructure_sha256 == "1" * 64

    def test__cache_admission__cannot_claim_scientific_verification(self) -> None:
        with pytest.raises(
            ValueError,
            match="not independent scientific verification",
        ):
            HigherRankDevelopmentCacheAdmission(
                artifact_role=("replaceable-development-cache-integrity-admission"),
                scientific_evidence=False,
                independent_scientific_verification=True,
                cache_format=("ksdft2effmass.higher-rank-development-result-cache.v1"),
                admission_method=("canonical-typed-byte-integrity-and-inventory.v1"),
                manifest_sha256="0" * 64,
                canonical_manifest_pass=True,
                entry_digest_pass=True,
                exact_result_round_trip_pass=True,
                complete_case_inventory_pass=True,
            )
