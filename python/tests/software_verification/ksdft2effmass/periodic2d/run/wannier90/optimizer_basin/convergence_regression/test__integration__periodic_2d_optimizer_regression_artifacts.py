r"""Artifact-owned identity and bounded verification evidence for row 054.

Evidence profile: claim_bearing

These tests bind compact repository bytes and reproduce retained finite diagnostics.
They do not rerun Wannier90, prove optimizer convergence or causality, define population
or physical uncertainty, predict DFT behavior, establish scientific validation, or
record acceptance.
"""

import hashlib
from pathlib import Path

import pytest

from ksdft2effmass import periodic2d
from ksdft2effmass.periodic2d.run import wannier90
from ksdft2effmass.periodic2d.run.wannier90 import optimizer_basin
from ksdft2effmass.periodic2d.run.wannier90.optimizer_basin import (
    convergence_regression,
)

pytestmark = [pytest.mark.software_verification, pytest.mark.integration]
SOURCE_DIGEST = "add349df1cccd95fc35c1984a21f58d4d5b49b62ba528377ea0f4245e5d5ce9a"
ANALYZER_DIGEST = "e80c16ab7fd11d86e6c51a344e01790306982f1a628b962611dfd0291d16fe46"
RESULT_DIGEST = "572b5ca7fe73ebb1cee6d9334e9ad6cddddea446fad3d02dfaf88202096ced22"


class TestPeriodic2DOptimizerRegressionArtifacts:
    """Own retained artifact, route, and numerical evidence for row 054."""

    def repository_root(self) -> Path:
        """Return the repository root containing compact retained evidence."""
        return Path(__file__).resolve().parents[9]

    def retained_documents(
        self,
    ) -> convergence_regression.Periodic2DOptimizerRegressionEncodedDocuments:
        """Load the three exact maintained row-054 documents."""
        base = (
            self.repository_root()
            / "calculations/research-monograph/periodic-2d-optimizer-basin"
        )
        return convergence_regression.Periodic2DOptimizerRegressionEncodedDocuments(
            base.joinpath("standalone-result.json").read_bytes(),
            base.joinpath("analyze_standalone_convergence_regression.py").read_bytes(),
            base.joinpath("standalone-convergence-regression.json").read_bytes(),
        )

    def test_retained_artifacts__preserve_bytes_and_catalog_identities(self) -> None:
        """Evidence ID: SV-PERIODIC-TWO-D-ROW-054-ARTIFACT-001.

        Requirement: Exact source, analyzer, and result bytes equal independently
        calculated and checksum-catalog identities.

        Acceptance: All three byte digests and catalog entries match fixed values;
        digests establish content identity only.
        """
        base = (
            self.repository_root()
            / "calculations/research-monograph/periodic-2d-optimizer-basin"
        )
        documents = self.retained_documents()
        catalog = {
            line.split(maxsplit=1)[1]: line.split(maxsplit=1)[0]
            for line in base.joinpath("SHA256SUMS").read_text().splitlines()
            if line.strip()
        }
        assert (
            hashlib.sha256(documents.standalone_result_payload).hexdigest()
            == SOURCE_DIGEST
        )
        assert hashlib.sha256(documents.analyzer_payload).hexdigest() == ANALYZER_DIGEST
        assert hashlib.sha256(documents.regression_payload).hexdigest() == RESULT_DIGEST
        assert catalog["standalone-result.json"] == SOURCE_DIGEST
        assert (
            catalog["analyze_standalone_convergence_regression.py"] == ANALYZER_DIGEST
        )
        assert catalog["standalone-convergence-regression.json"] == RESULT_DIGEST

    def test_retained_campaign__passes_bounded_independent_reconstruction(self) -> None:
        """Evidence ID: SV-PERIODIC-TWO-D-ROW-054-VERIFICATION-001.

        Requirement: Portable verification authenticates compact sources and
        independently reconstructs the declared finite right-censored log-normal
        diagnostics.

        Acceptance: Exact counts are 256 observations, 196 events, 60 right-censored
        observations, and 32 parameters; both bounded pass flags are true.
        """
        campaign = convergence_regression.Periodic2DOptimizerRegressionCampaign(
            self.retained_documents()
        )
        result = campaign.verify(repository_root=self.repository_root())
        assert result.source_authentication_passed
        assert result.numerical_reconstruction_passed
        assert result.observation_count == 256
        assert result.converged_count == 196
        assert result.right_censored_count == 60
        assert result.parameter_count == 32
        assert result.retained_result_sha256 == RESULT_DIGEST
        assert result.passes

    def test_public_routes__share_identity_and_retired_model_is_absent(self) -> None:
        """Evidence ID: SV-PERIODIC-TWO-D-ROW-054-ROUTE-002.

        Requirement: Reviewed facades expose one defining encoded-document class and no
        former retained-model compatibility alias or module remains.

        Acceptance: Class identity is shared across four facades and retired ownership
        is absent.
        """
        sut = convergence_regression.Periodic2DOptimizerRegressionEncodedDocuments
        assert periodic2d.Periodic2DOptimizerRegressionEncodedDocuments is sut
        assert wannier90.Periodic2DOptimizerRegressionEncodedDocuments is sut
        assert optimizer_basin.Periodic2DOptimizerRegressionEncodedDocuments is sut
        assert not hasattr(
            convergence_regression, "Periodic2DOptimizerConvergenceRegressionModel"
        )
        retired = (
            self.repository_root()
            / "python/src/ksdft2effmass/periodic2d/model/retained/"
            "optimizer_regression.py"
        )
        assert not retired.exists()
