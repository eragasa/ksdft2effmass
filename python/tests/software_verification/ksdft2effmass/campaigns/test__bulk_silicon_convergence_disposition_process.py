r"""Software verification of the bulk-silicon convergence disposition compiler.

Evidence profile: routine

Bounded artifact scope: typed decoding of the retained finite-setting analysis,
analysis-owned recalculation of its frozen pass flags, sequential cutoff-first then
conditional-mesh selection, recommendation generation, and packet serialization.

Facet and represented meaning

The code-driven disposition process is the primary artifact.  Its source is retained
calculated evidence, but these tests verify software behavior only.

Intrinsic and cross-object scope

The decoder owns exact wire adaptation, the analysis-owned guard analyzer owns
threshold and two-sided-guard policy, the campaign planner owns material-specific
composition, and the serializer owns the generated packet. Their composition is
checked against the maintained generated artifact.

VVUQ and scientific exclusions

No scientific executable is invoked. Passing tests do not select a parameter,
classify the IEEE warning, authorize downstream execution, establish an
infinite-setting or cutoff-mesh interaction bound, provide scientific validation, or
provide uncertainty quantification.
"""

from pathlib import Path

import pytest

from ksdft2effmass.campaigns._bulk_silicon_convergence_disposition import (
    BULK_SILICON_SEQUENTIAL_SCAN_CONFIGURATION,
    BulkSiliconConvergenceDispositionJsonSerializer,
    BulkSiliconConvergenceDispositionPlanner,
    BulkSiliconConvergenceSetting,
    BulkSiliconFiniteSettingAnalysis,
    BulkSiliconFiniteSettingAnalysisJsonDecoder,
)
from ksdft2effmass.units import UnitIdentity, UnitScalar

pytestmark = pytest.mark.software_verification


class TestBulkSiliconConvergenceDispositionProcess:
    """Own maintained evidence for the code-driven disposition artifact."""

    @staticmethod
    def repository_root() -> Path:
        """Return the checkout root containing the retained evidence."""
        return Path(__file__).resolve().parents[5]

    @classmethod
    def source_path(cls) -> Path:
        """Return the exact retained finite-setting analysis path."""
        return cls.repository_root() / (
            "calculations/bulk-silicon/production-convergence-preflight/"
            "finite-setting-analysis.json"
        )

    @classmethod
    def decoded(cls) -> BulkSiliconFiniteSettingAnalysis:
        """Decode the exact maintained evidence through the production adapter."""
        path = cls.source_path()
        return BulkSiliconFiniteSettingAnalysisJsonDecoder().execute(
            (
                "calculations/bulk-silicon/production-convergence-preflight/"
                "finite-setting-analysis.json"
            ),
            path.read_bytes(),
        )

    @staticmethod
    def planner() -> BulkSiliconConvergenceDispositionPlanner:
        """Return the production planner with explicit metal-unit scan inputs."""
        return BulkSiliconConvergenceDispositionPlanner(
            BULK_SILICON_SEQUENTIAL_SCAN_CONFIGURATION
        )

    def test_artifact__analysis__rechecks_all_eight_frozen_comparisons(self) -> None:
        """Evidence ID: SV-BULK-SI-CONVERGENCE-DISPOSITION-001

        Requirement: The process must decode all retained adjacent-setting evidence
        and have the analysis owner recompute every pass flag from frozen criteria.

        Acceptance: Five cutoff and three mesh comparisons decode, every retained
        pass record equals its recomputed value, and deliberate flag drift fails.
        """
        analysis = self.decoded()

        assert len(analysis.cutoff.comparisons) == 5
        assert len(analysis.mesh.comparisons) == 3
        assert tuple(
            value.passes.all_pass
            for value in analysis.cutoff.comparisons + analysis.mesh.comparisons
        ) == (False, False, True, True, True, True, True, True)
        self.planner().execute(analysis)
        drifted = (
            self.source_path()
            .read_bytes()
            .replace(b'"energy_pass": false', b'"energy_pass": true', 1)
        )
        drifted_analysis = BulkSiliconFiniteSettingAnalysisJsonDecoder().execute(
            "synthetic-drifted-analysis.json", drifted
        )
        with pytest.raises(ValueError, match="criteria flags disagree"):
            self.planner().execute(drifted_analysis)

    def test_artifact__planner__enforces_cutoff_then_conditional_mesh_order(
        self,
    ) -> None:
        """Evidence ID: SV-BULK-SI-CONVERGENCE-DISPOSITION-002

        Requirement: The process first recommends ENCUT from its guarded scan and
        only then evaluates the k-point scan performed at that recommended ENCUT.

        Acceptance: The C48/C54 evidence maps to guarded canonical eV cutoffs and
        653.073269903544 eV is selected by the smallest-setting policy; the mesh scan
        is fixed at that cutoff, K8/K10 are guarded, and the resulting setting remains
        proposed rather than accepted.
        """
        packet = self.planner().execute(self.decoded())

        assert tuple(value.value for value in packet.plan.cutoff_eligible) == (
            653.073269903544,
            734.707428641487,
        )
        assert packet.plan.recommended_cutoff == UnitScalar(
            653.073269903544, UnitIdentity.ELECTRON_VOLT
        )
        assert packet.plan.cutoff_lower_guard == UnitScalar(
            571.439111165601, UnitIdentity.ELECTRON_VOLT
        )
        assert packet.plan.cutoff_upper_guard == UnitScalar(
            734.707428641487, UnitIdentity.ELECTRON_VOLT
        )
        assert packet.plan.mesh_scan_cutoff == packet.plan.recommended_cutoff
        assert packet.plan.mesh_eligible == (8, 10)
        assert packet.plan.recommended_mesh == 8
        assert packet.plan.mesh_lower_guard == 6
        assert packet.plan.mesh_upper_guard == 10
        assert packet.plan.recommended_setting == BulkSiliconConvergenceSetting(
            UnitScalar(653.073269903544, UnitIdentity.ELECTRON_VOLT), 8
        )

    def test_artifact__serialization__matches_generated_decision_packet(self) -> None:
        """Evidence ID: SV-BULK-SI-CONVERGENCE-DISPOSITION-003

        Requirement: The maintained human-decision packet is generated
        deterministically from the retained evidence rather than assembled by hand.

        Acceptance: Fresh serialization is byte-identical to the maintained packet,
        with no selected setting, warning disposition, or execution authority.
        """
        packet = self.planner().execute(self.decoded())
        observed = BulkSiliconConvergenceDispositionJsonSerializer().execute(packet)
        expected = (
            self.repository_root()
            / (
                "calculations/bulk-silicon/production-convergence-preflight/"
                "direct-results-decision-packet.json"
            )
        ).read_bytes()

        assert observed == expected
        assert b'"unit_system": "lammps_metal"' in observed
        assert b'"unit": "electron_volt"' in observed
        assert b'"energy_ry_atom"' not in observed
        assert b'"pressure_change_kbar"' not in observed
        assert b'"setting_selected": null' in observed
        assert b'"selected": null' in observed
        assert b'"protected_execution_authorized": false' in observed
