r"""Artifact-owned fail-closed evidence for row-053 portable verification.

Evidence profile: claim_bearing

Mutations affect in-memory copies of compact retained wires only. The tests access no
external native tree and make no convergence, validation, uncertainty, or acceptance
claim.
"""

import copy
import json
from collections.abc import Callable
from pathlib import Path

import pytest

from ksdft2effmass.periodic2d.run.wannier90.optimizer_basin.reanalysis import (
    Periodic2DOptimizerReanalysisEncodedDocuments,
)
from ksdft2effmass.periodic2d.run.wannier90.optimizer_basin.reanalysis.verify import (
    Periodic2DOptimizerReanalysisCampaignVerificationRequest,
    Periodic2DOptimizerReanalysisCampaignVerifier,
)
from ksdft2effmass.serialization.json import JsonValue

pytestmark = [pytest.mark.software_verification, pytest.mark.integration]
SUT = Periodic2DOptimizerReanalysisCampaignVerifier


class TestPeriodic2DOptimizerReanalysisVerifierFailClosed:
    """Own adversarial structural evidence for crosswalk row 053."""

    def repository_root(self) -> Path:
        """Return the repository root containing maintained compact evidence."""
        return Path(__file__).resolve().parents[9]

    def retained_documents(self) -> tuple[bytes, bytes]:
        """Read exact source-result and reanalysis-result wires."""
        base = (
            self.repository_root()
            / "calculations/research-monograph/periodic-2d-optimizer-basin"
        )
        return base.joinpath("result.json").read_bytes(), base.joinpath(
            "reanalysis-result.json"
        ).read_bytes()

    def mutated_result(self, mutation: Callable[[dict[str, JsonValue]], None]) -> bytes:
        """Return a deterministic test-only result wire after one mutation."""
        _, payload = self.retained_documents()
        decoded = json.loads(payload)
        if type(decoded) is not dict:
            raise TypeError("retained reanalysis result must be an object")
        mutation(decoded)
        return json.dumps(decoded, allow_nan=False, separators=(",", ":")).encode(
            "utf-8"
        )

    def request(
        self, result_payload: bytes
    ) -> Periodic2DOptimizerReanalysisCampaignVerificationRequest:
        """Build one request from exact source bytes and a supplied result wire."""
        source_payload, _ = self.retained_documents()
        return Periodic2DOptimizerReanalysisCampaignVerificationRequest(
            Periodic2DOptimizerReanalysisEncodedDocuments(
                source_payload, result_payload
            ),
            self.repository_root(),
        )

    def test_execute__rejects_duplicate_configuration_identity(self) -> None:
        """Evidence ID: SV-PERIODIC-TWO-D-ROW-053-STRUCTURE-001.

        Requirement: Configuration identities are unique before dictionary construction.

        Acceptance: Replacing one configuration with a duplicate fails explicitly.
        """

        def duplicate_configuration(result: dict[str, JsonValue]) -> None:
            """Replace the last configuration with a copy of the first."""
            configurations = result["configurations"]
            assert type(configurations) is list
            configurations[-1] = copy.deepcopy(configurations[0])

        with pytest.raises(AssertionError, match="unique identities"):
            SUT().execute(self.request(self.mutated_result(duplicate_configuration)))

    def test_execute__rejects_duplicate_endpoint_identity(self) -> None:
        """Evidence ID: SV-PERIODIC-TWO-D-ROW-053-STRUCTURE-002.

        Requirement: Endpoint identities are unique before gauge lookup construction.

        Acceptance: Replacing one endpoint with a duplicate fails explicitly.
        """

        def duplicate_endpoint(result: dict[str, JsonValue]) -> None:
            """Replace one endpoint with a copy sharing another gauge identity."""
            configurations = result["configurations"]
            assert type(configurations) is list
            configuration = configurations[0]
            assert type(configuration) is dict
            starts = configuration["starts"]
            assert type(starts) is list
            starts[-1] = copy.deepcopy(starts[0])

        with pytest.raises(AssertionError, match="unique identities"):
            SUT().execute(self.request(self.mutated_result(duplicate_endpoint)))

    @pytest.mark.parametrize(
        "declared_path",
        ["/tmp/outside-row-053.py", "../outside-row-053.py"],
    )
    def test_execute__rejects_compact_source_escape(self, declared_path: str) -> None:
        """Evidence ID: SV-PERIODIC-TWO-D-ROW-053-CONFINEMENT-001.

        Requirement: Directly declared compact source paths resolve within the explicit
        repository root before bytes are read.

        Acceptance: Absolute and parent-traversal escapes raise the confinement error.
        """

        def escape(result: dict[str, JsonValue]) -> None:
            """Replace the reanalyzer declaration with one escaping path."""
            provenance = result["provenance"]
            assert type(provenance) is dict
            provenance["reanalyzer_path"] = declared_path

        with pytest.raises(ValueError, match="must resolve within repository_root"):
            SUT().execute(self.request(self.mutated_result(escape)))

    def test_execute__rejects_malformed_provenance_digest(self) -> None:
        """Evidence ID: SV-PERIODIC-TWO-D-ROW-053-PROVENANCE-001.

        Requirement: Declared provenance identities use strict lowercase SHA-256 syntax.

        Acceptance: Uppercase hexadecimal fails at the digest boundary.
        """

        def uppercase_digest(result: dict[str, JsonValue]) -> None:
            """Uppercase one otherwise valid compact-source digest."""
            provenance = result["provenance"]
            assert type(provenance) is dict
            digest = provenance["reanalyzer_sha256"]
            assert type(digest) is str
            provenance["reanalyzer_sha256"] = digest.upper()

        with pytest.raises(ValueError, match="lowercase SHA-256 digest"):
            SUT().execute(self.request(self.mutated_result(uppercase_digest)))

    def test_execute__rejects_incomplete_best_endpoint_copy(self) -> None:
        """Evidence ID: SV-PERIODIC-TWO-D-ROW-053-STRUCTURE-003.

        Requirement: The retained best-by-Omega-tilde object exactly copies the complete
        minimum reported Omega-tilde converged endpoint.

        Acceptance: Changing a copied field while retaining the gauge identity fails.
        """

        def change_best(result: dict[str, JsonValue]) -> None:
            """Change one field in a copied best endpoint."""
            configurations = result["configurations"]
            assert type(configurations) is list
            configuration = configurations[0]
            assert type(configuration) is dict
            best = configuration["best_observed_converged_by_omega_tilde"]
            assert type(best) is dict
            source_path = best["source_analysis_result_path"]
            assert type(source_path) is str
            best["source_analysis_result_path"] = f"{source_path}.changed"

        with pytest.raises(AssertionError, match="best Omega_tilde endpoint changed"):
            SUT().execute(self.request(self.mutated_result(change_best)))

    def test_execute__rejects_duplicate_refinement_case(self) -> None:
        """Evidence ID: SV-PERIODIC-TWO-D-ROW-053-REFINEMENT-001.

        Requirement: Refinement case identities are unique before case-map construction.

        Acceptance: Replacing one case with a duplicate fails explicitly.
        """

        def duplicate_case(result: dict[str, JsonValue]) -> None:
            """Replace the final refinement with a copy of the first."""
            refinements = result["common_estimator_refinement"]
            assert type(refinements) is list
            refinements[-1] = copy.deepcopy(refinements[0])

        with pytest.raises(AssertionError, match="refinement cases must have unique"):
            SUT().execute(self.request(self.mutated_result(duplicate_case)))
