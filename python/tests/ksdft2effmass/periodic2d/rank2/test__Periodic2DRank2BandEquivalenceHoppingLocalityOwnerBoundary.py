"""Periodic-2D rank-two ownership for ``BandEquivalenceHoppingLocalityCalculationResult``."""  # noqa: E501

from __future__ import annotations

from pathlib import Path

import pytest

pytestmark = [pytest.mark.integration, pytest.mark.software_verification]


class TestPeriodic2DRank2BandEquivalenceHoppingLocalityOwnerBoundary:
    """Keep donor responsibilities and child evidence boundaries explicit."""

    @staticmethod
    def _root(repository_root: Path) -> Path:
        return repository_root / "calculations" / "periodic2d" / "rank2"

    def test_declares_periodic1d_rank_two_lifecycle_donor(
        self, repository_root: Path
    ) -> None:
        root = self._root(repository_root)
        readme = (root / "README.md").read_text(encoding="utf-8")
        controls = (root / "scientific-controls.md").read_text(encoding="utf-8")

        donor = "periodic1d/rank2/band-equivalence-versus-hopping-locality"
        assert donor in readme
        assert donor in controls
        for responsibility in (
            "calculation",
            "independent verification",
            "authenticated rendering",
            "immutable execution",
            "claim boundaries",
        ):
            assert responsibility in controls

    def test_keeps_current_child_family_lifecycle_dispositions_separate(
        self, repository_root: Path
    ) -> None:
        calculations = repository_root / "calculations"
        expected = {
            "periodic2d/rank2/orthogonal/band-equivalence-locality/README.md": (
                "direct-square-rank2-n16",
                "CALCULATED RESULT",
            ),
            "periodic2d_rank2_hexagonal/README.md": (
                "no retained execution",
                "two-basis metric",
            ),
            "periodic2d_rank2_rhombic_path/README.md": (
                "development calculation",
                "M0 geometry/frozen-response",
            ),
        }

        for relative_path, phrases in expected.items():
            record = (calculations / relative_path).read_text(encoding="utf-8")
            for phrase in phrases:
                assert phrase in record

        for retired in (
            "periodic2d/rank2/nonorthogonal/band-equivalence-locality",
            "periodic2d/rank2/strain-locality",
        ):
            assert not (calculations / retired).exists()

    def test_declares_two_dimensional_nontransfer_boundaries(
        self, repository_root: Path
    ) -> None:
        controls = (self._root(repository_root) / "scientific-controls.md").read_text(
            encoding="utf-8"
        )

        for phrase in (
            "tensor nyquist classes",
            "complete physical-metric shells",
            "equal-radius shells are never split",
            "no shared nodes",
            "momentum disposition remains unresolved",
            "not retroactively inserted",
            "sha-256 establishes byte identity only",
        ):
            assert phrase in controls.casefold()

    def test_accounts_for_every_donor_diagnostic_family(
        self, repository_root: Path
    ) -> None:
        inventory = " ".join(
            (self._root(repository_root) / "diagnostic-parity.md")
            .read_text(encoding="utf-8")
            .split()
        )

        for heading in (
            "Parent and retained-subspace qualification",
            "Frame transport and topology",
            "Representation equivalence and restricted alignment",
            "Fourier, Nyquist, and locality diagnostics",
            "Support-selection diagnostics",
            "Parent-family diagnostics",
            "Amplitude diagnostics",
            "Momentum-refinement diagnostics",
            "Independent verification and retained projection",
            "Strain-family extension",
        ):
            assert heading in inventory

        for diagnostic in (
            "minimum_sampled_external_gap",
            "maximum_projector_reconstruction_defect",
            "minimum_sampled_transport_singular_value",
            "maximum_plaquette_holonomy_phase",
            "maximum_direct_band_defect",
            "normalized_squared_operator_residual",
            "BandEquivalenceHoppingLocalityLoss",
            "reference_twisted_nyquist_defect",
            "reference_truncation_parseval_defect",
            "BandEquivalenceHoppingLocalityFirstPassingDecision",
            "maximum_correlation_midpoint_defect",
            "maximum_shared_parent_eigenvalue_defect",
            "maximum_shared_projector_defect",
            "RealSpaceSupportTruncationToleranceSelector",
        ):
            assert diagnostic in inventory

        for boundary in (
            "no shared nodes",
            "momentum disposition is `unresolved`",
            "rather than `converged`",
            "equal-radius displacements are never split",
            "not a calculated result",
            "explicit human authorization",
        ):
            assert boundary in inventory.casefold()

    def test_context_first_owners_keep_capabilities_and_aggregate_separate(
        self, repository_root: Path
    ) -> None:
        calculations = repository_root / "calculations"
        contexts = (
            calculations / "periodic2d_rank2_hexagonal",
            calculations / "periodic2d_rank2_rhombic_path",
        )

        for context in contexts:
            readme = (context / "README.md").read_text(encoding="utf-8")
            for capability in (
                "gauge_alignment",
                "band_equivalence",
                "hopping_locality",
                "support_truncation",
                "band_equivalence_hopping_locality",
            ):
                assert (context / capability / "README.md").is_file()
                assert capability in readme

        parent = (self._root(repository_root) / "README.md").read_text(encoding="utf-8")
        assert "periodic2d_rank2_hexagonal" in parent
        assert "periodic2d_rank2_rhombic_path" in parent
