r"""Artifact-owned adversarial evidence for row-054 verification.

Evidence profile: claim_bearing

These mutations test sensitivity and authentication boundaries only. They do not prove
the retained statistical assumptions or any scientific conclusion.
"""

from dataclasses import replace
from pathlib import Path

import pytest

from ksdft2effmass.periodic2d.run.wannier90.optimizer_basin import (
    convergence_regression as regression,
)
from ksdft2effmass.periodic2d.run.wannier90.optimizer_basin.convergence_regression.authentication import (  # noqa: E501
    Periodic2DOptimizerRegressionSourceAuthenticator,
)
from ksdft2effmass.periodic2d.run.wannier90.optimizer_basin.convergence_regression.correlation import (  # noqa: E501
    Periodic2DOptimizerRegressionCorrelator,
)
from ksdft2effmass.periodic2d.run.wannier90.optimizer_basin.convergence_regression.decode import (  # noqa: E501
    Periodic2DOptimizerRegressionDocumentDecoder,
)

Periodic2DOptimizerRegressionEncodedDocuments = (
    regression.Periodic2DOptimizerRegressionEncodedDocuments
)

pytestmark = [pytest.mark.software_verification, pytest.mark.integration]


class TestPeriodic2DOptimizerRegressionFailClosed:
    """Own artifact-aware fail-closed evidence for row 054."""

    def repository_root(self) -> Path:
        """Return the repository root containing exact retained documents."""
        return Path(__file__).resolve().parents[9]

    def retained_documents(self) -> Periodic2DOptimizerRegressionEncodedDocuments:
        """Return exact maintained row-054 wires."""
        base = (
            self.repository_root()
            / "calculations/research-monograph/periodic-2d-optimizer-basin"
        )
        return Periodic2DOptimizerRegressionEncodedDocuments(
            base.joinpath("standalone-result.json").read_bytes(),
            base.joinpath("analyze_standalone_convergence_regression.py").read_bytes(),
            base.joinpath("standalone-convergence-regression.json").read_bytes(),
        )

    def test_authenticator__rejects_forged_digest_and_changed_analyzer(
        self, tmp_path: Path
    ) -> None:
        """Evidence ID: SV-PERIODIC-TWO-D-ROW-054-AUTHENTICATION-001.

        Requirement: Repository equality, declared source identity, and frozen analyzer
        identity are separate checks.

        Acceptance: A forged source digest, an encoded/repository byte mismatch, and a
        coordinated repository-plus-encoded analyzer change each fail at their distinct
        checks.
        """
        documents = self.retained_documents()
        decoded = Periodic2DOptimizerRegressionDocumentDecoder().execute(documents)
        forged = replace(decoded.regression_result, source_result_sha256="0" * 64)
        authenticator = Periodic2DOptimizerRegressionSourceAuthenticator()
        with pytest.raises(AssertionError, match="source result identity mismatch"):
            authenticator.execute(documents, forged, self.repository_root())
        changed_documents = Periodic2DOptimizerRegressionEncodedDocuments(
            documents.standalone_result_payload,
            documents.analyzer_payload + b"\n# changed",
            documents.regression_payload,
        )
        with pytest.raises(AssertionError, match="analyzer repository bytes changed"):
            authenticator.execute(
                changed_documents, decoded.regression_result, self.repository_root()
            )

        # Mirror all encapsulated bytes so repository equality passes; the independent
        # frozen analyzer identity must still reject the coordinated modification.
        mirrored = (
            tmp_path / "calculations/research-monograph/periodic-2d-optimizer-basin"
        )
        mirrored.mkdir(parents=True)
        mirrored.joinpath("standalone-result.json").write_bytes(
            changed_documents.standalone_result_payload
        )
        mirrored.joinpath("analyze_standalone_convergence_regression.py").write_bytes(
            changed_documents.analyzer_payload
        )
        mirrored.joinpath("standalone-convergence-regression.json").write_bytes(
            changed_documents.regression_payload
        )
        with pytest.raises(AssertionError, match="analyzer identity mismatch"):
            authenticator.execute(
                changed_documents, decoded.regression_result, tmp_path
            )

    def test_correlator__rejects_changed_counts_and_parameter_values(self) -> None:
        """Evidence ID: SV-PERIODIC-TWO-D-ROW-054-NUMERICS-001.

        Requirement: Independent reconstruction is sensitive to aggregate and fitted
        parameter corruption after typed decoding.

        Acceptance: A changed right-censored count and intercept each fail correlation.
        """
        decoded = Periodic2DOptimizerRegressionDocumentDecoder().execute(
            self.retained_documents()
        )
        changed_count = replace(
            decoded,
            regression_result=replace(
                decoded.regression_result, right_censored_count=59
            ),
        )
        with pytest.raises(AssertionError, match="aggregate counts changed"):
            Periodic2DOptimizerRegressionCorrelator().execute(changed_count)
        first, *remaining = decoded.regression_result.parameters
        changed_parameters = (replace(first, value=first.value + 0.1), *remaining)
        changed_parameter = replace(
            decoded,
            regression_result=replace(
                decoded.regression_result, parameters=changed_parameters
            ),
        )
        with pytest.raises(AssertionError):
            Periodic2DOptimizerRegressionCorrelator().execute(changed_parameter)
