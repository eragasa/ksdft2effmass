# ruff: noqa: E501
"""Integration and numerical evidence for separated continuum refinement."""

import ast
import inspect
from pathlib import Path

import pytest

import ksdft2effmass.campaigns.research_monograph.periodic_1d.defects.continuum_refinement as public_package
from ksdft2effmass.campaigns.research_monograph.periodic_1d.defects.continuum_refinement import (
    ContinuumRefinementCampaign,
    ContinuumRefinementCampaignModel,
)
from ksdft2effmass.campaigns.research_monograph.periodic_1d.defects.continuum_refinement.verification import (
    ContinuumRefinementCampaignVerifier,
)
from ksdft2effmass.campaigns.research_monograph.periodic_1d.defects.continuum_refinement.workflow import (
    ContinuumRefinementInputDeserializer,
)

pytestmark = [pytest.mark.integration, pytest.mark.numerical_verification]


class TestContinuumRefinementCampaign:
    """Own retained composition, verification, and boundary evidence."""

    @staticmethod
    def root() -> Path:
        """Return the repository containing retained refinement artifacts."""
        return Path(__file__).resolve().parents[8]

    def campaign(self, result: bytes | None = None) -> ContinuumRefinementCampaign:
        """Build the campaign from exact retained documents."""
        root = self.root()
        retained = (
            root
            / "calculations/research-monograph/impurity-defect-1d-continuum-refinement"
        )
        original = (retained / "result.json").read_bytes()
        return ContinuumRefinementCampaign(
            ContinuumRefinementCampaignModel(
                (retained / "input.json").read_bytes(),
                original if result is None else result,
                root,
            )
        )

    @pytest.mark.expensive
    def test_method__correlate_and_verify_retained__reproduces_all_axes(self) -> None:
        """Evidence ID: NV-CAMPAIGN-PERIODIC-ONE-D-DEFECT-009.

        Requirement: Maintained calculation and an independent implementation must
        reproduce every separated refinement-axis record and retained conclusion.

        Method: Correlate canonical bytes and independently reconstruct all operators.

        Oracle: Independent site-space lattice and entrywise continuum assembly.

        Acceptance: Exact digest identity and all channels pass for 31 records and three
        authenticated sources; the result retains no profile-defined crossover.

        Interpretation: A pass establishes bounded synthetic refinement verification.

        Limitations: It proves no asymptotic, infinite-system, or material result.
        """
        campaign = self.campaign()
        correlation = campaign.correlate_retained()
        verification = campaign.verify_retained()
        retained = campaign.model.retained_result_document

        assert correlation.semantic_identity
        assert correlation.canonical_byte_identity
        assert (
            correlation.retained_sha256
            == "1f4029cc953e78eb8231e5a651676401b20d5b74f09ecb8cb38d72aa2e92c2dc"
        )
        assert verification.passed
        assert verification.verified_record_count == 31
        assert verification.source_identity_count == 3
        assert b'"profile_defined_crossover_established": false' in retained
        assert b'"lattice_scale_persistent_pass_spacing": 0.5' in retained

    def test_method__verify_retained__rejects_metric_corruption(self) -> None:
        """Evidence ID: NV-CAMPAIGN-PERIODIC-ONE-D-DEFECT-010.

        Requirement: Independent verification must reject changed refinement metrics.

        Method: Mutate the first retained binding energy without changing sources.

        Oracle: Independently reconstructed represented Hamiltonian spectrum.

        Acceptance: Verification raises ``ValueError`` for the changed channel.

        Interpretation: A pass establishes sensitivity to numerical corruption.

        Limitations: The mutation samples one of the checked numerical fields.
        """
        retained = self.campaign().model.retained_result_document
        marker = b'"binding_energy": '
        start = retained.find(marker)
        if start < 0:
            raise ValueError("test mutation target was absent")
        begin = start + len(marker)
        end = retained.find(b",", begin)
        mutated = retained[:begin] + b"0.25" + retained[end:]

        with pytest.raises((ValueError, AssertionError)):
            self.campaign(mutated).verify_retained()

    def test_contract__wire_surface_and_imports__remain_closed(self) -> None:
        """Evidence ID: SV-CAMPAIGN-PERIODIC-ONE-D-DEFECT-029.

        Requirement: Input JSON must be strict, package exports narrow, and independent
        verification separated from maintained construction.

        Method: Exercise duplicate-key rejection and inspect exports and imports.

        Oracle: Version-one wire and implementation-independence contracts.

        Acceptance: Duplicate keys fail, exactly two names export, and the verifier
        imports no maintained ``workflow`` module.

        Interpretation: A pass establishes structural software boundaries.

        Limitations: Static separation does not establish independent physical data.
        """
        with pytest.raises(ValueError, match="duplicate JSON key"):
            ContinuumRefinementInputDeserializer().execute(
                b'{"schema_version":1,"schema_version":1}'
            )
        assert public_package.__all__ == [
            "ContinuumRefinementCampaign",
            "ContinuumRefinementCampaignModel",
        ]
        tree = ast.parse(
            Path(inspect.getfile(ContinuumRefinementCampaignVerifier)).read_text()
        )
        modules = tuple(
            node.module
            for node in ast.walk(tree)
            if isinstance(node, ast.ImportFrom) and node.module is not None
        )
        assert "workflow" not in modules
