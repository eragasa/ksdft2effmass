r"""Artifact-owned adversarial evidence for row-055 standalone verification.

Evidence profile: claim_bearing

These mutations test source and reconstruction sensitivity only. They do not validate
native execution, optimizer assumptions, or scientific conclusions.
"""

from dataclasses import replace
from pathlib import Path

import pytest

from ksdft2effmass.periodic2d.run.wannier90.optimizer_basin import standalone
from ksdft2effmass.periodic2d.run.wannier90.optimizer_basin.standalone.authentication import (  # noqa: E501
    Periodic2DOptimizerStandaloneSourceAuthenticator,
)
from ksdft2effmass.periodic2d.run.wannier90.optimizer_basin.standalone.correlation import (  # noqa: E501
    Periodic2DOptimizerStandaloneCorrelator,
)
from ksdft2effmass.periodic2d.run.wannier90.optimizer_basin.standalone.decode import (
    Periodic2DOptimizerStandaloneDocumentDecoder,
)

pytestmark = [pytest.mark.software_verification, pytest.mark.integration]


class TestPeriodic2DOptimizerStandaloneFailClosed:
    """Own artifact-aware fail-closed evidence for crosswalk row 055."""

    def repository_root(self) -> Path:
        """Return the repository root containing exact retained documents."""
        return Path(__file__).resolve().parents[9]

    def retained_documents(
        self,
    ) -> standalone.Periodic2DOptimizerStandaloneEncodedDocuments:
        """Return exact maintained row-055 wires."""
        base = (
            self.repository_root()
            / "calculations/research-monograph/periodic-2d-optimizer-basin"
        )
        return standalone.Periodic2DOptimizerStandaloneEncodedDocuments(
            base.joinpath("standalone-study-proposal.json").read_bytes(),
            base.joinpath("standalone-initial-gauges.json").read_bytes(),
            base.joinpath("standalone-result.json").read_bytes(),
        )

    def test_authenticator__rejects_declared_and_coordinated_identity_changes(
        self, tmp_path: Path
    ) -> None:
        """Evidence ID: SV-PERIODIC-TWO-D-ROW-055-AUTHENTICATION-001.

        Requirement: Repository equality, declared proposal identity, and frozen wire
        identity are distinct checks.

        Acceptance: A forged declaration, repository mismatch, and coordinated
        repository-plus-encoded result change each fail closed.
        """
        documents = self.retained_documents()
        decoded = Periodic2DOptimizerStandaloneDocumentDecoder().execute(documents)
        authenticator = Periodic2DOptimizerStandaloneSourceAuthenticator()
        forged = replace(
            decoded.result,
            provenance=replace(decoded.result.provenance, proposal_sha256="0" * 64),
        )
        with pytest.raises(AssertionError, match="result proposal identity mismatch"):
            authenticator.execute(
                documents, decoded.gauge_design, forged, self.repository_root()
            )
        changed = standalone.Periodic2DOptimizerStandaloneEncodedDocuments(
            documents.proposal_payload + b"\n",
            documents.initial_gauges_payload,
            documents.result_payload,
        )
        with pytest.raises(AssertionError, match="proposal repository bytes changed"):
            authenticator.execute(
                changed,
                decoded.gauge_design,
                decoded.result,
                self.repository_root(),
            )

        changed_result = documents.result_payload.replace(
            b'"effective_native_converged_count": 196',
            b'"effective_native_converged_count": 195',
            1,
        )
        coordinated = standalone.Periodic2DOptimizerStandaloneEncodedDocuments(
            documents.proposal_payload,
            documents.initial_gauges_payload,
            changed_result,
        )
        mirrored = (
            tmp_path / "calculations/research-monograph/periodic-2d-optimizer-basin"
        )
        mirrored.mkdir(parents=True)
        mirrored.joinpath("standalone-study-proposal.json").write_bytes(
            coordinated.proposal_payload
        )
        mirrored.joinpath("standalone-initial-gauges.json").write_bytes(
            coordinated.initial_gauges_payload
        )
        mirrored.joinpath("standalone-result.json").write_bytes(
            coordinated.result_payload
        )
        source_extractor = (
            self.repository_root()
            / "calculations/research-monograph/periodic-2d-optimizer-basin"
            / "extract_standalone_results.py"
        )
        mirrored.joinpath("extract_standalone_results.py").write_bytes(
            source_extractor.read_bytes()
        )
        coordinated_decoded = Periodic2DOptimizerStandaloneDocumentDecoder().execute(
            coordinated
        )
        with pytest.raises(AssertionError, match="result identity mismatch"):
            authenticator.execute(
                coordinated,
                coordinated_decoded.gauge_design,
                coordinated_decoded.result,
                tmp_path,
            )

    def test_correlator__rejects_reassigned_basin_membership(self) -> None:
        """Evidence ID: SV-PERIODIC-TWO-D-ROW-055-CORRELATION-002.

        Requirement: Basin membership is tied to its representative, ordered endpoint,
        threshold diagnostics, rejected comparisons, and derived start block.

        Acceptance: Swapping two singleton member identities while preserving the
        partition and occupancies fails independent basin correlation.
        """
        decoded = Periodic2DOptimizerStandaloneDocumentDecoder().execute(
            self.retained_documents()
        )
        group = decoded.result.groups[0]
        first, second = group.basins[:2]
        changed_basins = (
            replace(first, start_ids=(second.representative_start_id,)),
            replace(second, start_ids=(first.representative_start_id,)),
            *group.basins[2:],
        )
        changed = replace(
            decoded,
            result=replace(
                decoded.result,
                groups=(
                    replace(group, basins=changed_basins),
                    *decoded.result.groups[1:],
                ),
            ),
        )
        with pytest.raises(AssertionError, match="basin representative"):
            Periodic2DOptimizerStandaloneCorrelator().execute(changed)

    def test_correlator__rejects_changed_aggregate_and_claim_boundary(self) -> None:
        """Evidence ID: SV-PERIODIC-TWO-D-ROW-055-CORRELATION-001.

        Requirement: Aggregate reconstruction and the exact negative disposition are
        both independently enforced after typed decoding.

        Acceptance: A changed endpoint count and changed disposition each fail.
        """
        decoded = Periodic2DOptimizerStandaloneDocumentDecoder().execute(
            self.retained_documents()
        )
        changed_count = replace(
            decoded,
            result=replace(
                decoded.result,
                summary=replace(
                    decoded.result.summary,
                    effective_native_converged_count=195,
                ),
            ),
        )
        with pytest.raises(AssertionError, match="execution summary counts disagree"):
            Periodic2DOptimizerStandaloneCorrelator().execute(changed_count)
        changed_disposition = replace(
            decoded,
            result=replace(
                decoded.result,
                convergence_disposition="supports convergence",
            ),
        )
        with pytest.raises(AssertionError, match="disposition text changed"):
            Periodic2DOptimizerStandaloneCorrelator().execute(changed_disposition)
