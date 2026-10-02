# ruff: noqa: E501
"""Integration and numerical-verification evidence for the finite-rank oracle."""

import ast
import inspect
from pathlib import Path

import pytest

import ksdft2effmass.campaigns.periodic_1d.defects.finite_rank_oracle as public_package
from ksdft2effmass.campaigns.periodic_1d.defects.finite_rank_oracle import (
    FiniteRankOracleCampaign,
    FiniteRankOracleEncodedDocuments,
)
from ksdft2effmass.campaigns.periodic_1d.defects.finite_rank_oracle.verification import (
    FiniteRankOracleCampaignVerifier,
)
from ksdft2effmass.campaigns.periodic_1d.defects.finite_rank_oracle.workflow import (
    FiniteRankOracleCampaignInputDeserializer,
)

pytestmark = [pytest.mark.integration, pytest.mark.numerical_verification]
SUT = FiniteRankOracleCampaign


class TestFiniteRankOracleCampaign:
    """Own retained composition, verification, and encapsulation evidence."""

    @staticmethod
    def root() -> Path:
        """Return the repository containing retained oracle artifacts."""
        return Path(__file__).resolve().parents[7]

    def campaign(self, result: bytes | None = None) -> SUT:
        """Build the campaign from exact retained documents."""
        root = self.root()
        retained = (
            root
            / "calculations/research-monograph/impurity-defect-1d-analytical-oracle"
        )
        original = (retained / "result.json").read_bytes()
        return SUT(
            FiniteRankOracleEncodedDocuments(
                (retained / "input.json").read_bytes(),
                original if result is None else result,
            )
        )

    @pytest.mark.expensive
    def test_method__correlate_and_verify_retained__reproduces_oracle(self) -> None:
        """Evidence ID: NV-CAMPAIGN-PERIODIC-ONE-D-DEFECT-007.

        Requirement: Maintained composition and an independent implementation must
        agree with every retained finite-rank oracle record.

        Method: Correlate canonical bytes and execute independent reconstruction.

        Oracle: Bloch-resolvent bisection versus a separate dense site-space eigensolve.

        Acceptance: Exact digest identity and all channels pass for 24 records and three
        authenticated sources.

        Interpretation: A pass establishes bounded finite-system synthetic verification.

        Limitations: It establishes no infinite-system, continuum, or material claim.
        """
        campaign = self.campaign()
        root = self.root()
        correlation = campaign.correlate_retained(root)
        verification = campaign.verify_retained(root)

        assert correlation.semantic_identity
        assert correlation.canonical_byte_identity
        assert (
            correlation.retained_sha256
            == "64ab16a279d5f8ca18f725dadb15860811a45ea12758a91a7cd7166f6074dae0"
        )
        assert verification.passed
        assert verification.verified_record_count == 24
        assert verification.source_identity_count == 3

    def test_method__verify_retained__rejects_energy_corruption(self) -> None:
        """Evidence ID: NV-CAMPAIGN-PERIODIC-ONE-D-DEFECT-008.

        Requirement: Independent verification must reject changed oracle diagnostics.

        Method: Mutate one retained energy discrepancy without changing source inputs.

        Oracle: Independently resolved root and site-space lowest eigenvalue.

        Acceptance: Verification raises ``ValueError`` at the changed field.

        Interpretation: A pass establishes sensitivity to numerical corruption.

        Limitations: This samples one retained scalar channel.
        """
        retained = self.campaign().encoded_documents.retained_result_document
        marker = b'"energy_absolute_discrepancy": '
        start = retained.find(marker)
        if start < 0:
            raise ValueError("test mutation target was absent")
        value_start = start + len(marker)
        value_end = retained.find(b",", value_start)
        mutated = retained[:value_start] + b"0.25" + retained[value_end:]

        with pytest.raises(ValueError, match="value mismatch"):
            self.campaign(mutated).verify_retained(self.root())

    def test_contract__input_and_imports__remain_closed_and_independent(self) -> None:
        """Evidence ID: SV-CAMPAIGN-PERIODIC-ONE-D-DEFECT-028.

        Requirement: Input JSON must be strict, the package surface narrow, and the
        independent verifier separated from the maintained Workflow.

        Method: Decode malformed JSON and inspect package exports and verifier imports.

        Oracle: Version-one wire and implementation-independence contracts.

        Acceptance: Duplicate keys are rejected, two façade names are exported, and the
        verifier imports no ``workflow`` module.

        Interpretation: A pass establishes structural software boundaries.

        Limitations: Static import separation does not prove independent physical data.
        """
        with pytest.raises(ValueError, match="duplicate JSON key"):
            FiniteRankOracleCampaignInputDeserializer().execute(
                b'{"schema_version":1,"schema_version":1}'
            )
        assert public_package.__all__ == [
            "FiniteRankOracleCampaign",
            "FiniteRankOracleEncodedDocuments",
        ]
        tree = ast.parse(
            Path(inspect.getfile(FiniteRankOracleCampaignVerifier)).read_text()
        )
        modules = tuple(
            node.module
            for node in ast.walk(tree)
            if isinstance(node, ast.ImportFrom) and node.module is not None
        )
        assert "workflow" not in modules
