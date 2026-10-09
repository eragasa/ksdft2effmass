"""Portable evidence for the periodic-2D Wannier90 study."""

import ast
import inspect
from pathlib import Path

import pytest

from ksdft2effmass.periodic2d import (
    Periodic2DWannier90StudyCampaign,
    Periodic2DWannier90StudyEncodedDocuments,
)
from ksdft2effmass.periodic2d.run import wannier90

Verifier = wannier90.study.verify.Periodic2DWannier90StudyCampaignVerifier
pytestmark = [
    pytest.mark.integration,
    pytest.mark.numerical_verification,
    pytest.mark.expensive,
]


class TestPeriodic2DWannier90StudyCampaign:
    """Own repository-portable convergence-study evidence."""

    @staticmethod
    def root() -> Path:
        """Return the repository root."""
        return Path(__file__).resolve().parents[7]

    def campaign(self, result: bytes | None = None) -> Periodic2DWannier90StudyCampaign:
        """Construct a campaign from exact retained study documents."""
        base = self.root() / "calculations/research-monograph/periodic-2d"
        retained = (base / "wannier90-study-result.json").read_bytes()
        return Periodic2DWannier90StudyCampaign(
            Periodic2DWannier90StudyEncodedDocuments(
                (base / "wannier90-study-input.json").read_bytes(),
                retained if result is None else result,
            )
        )

    @staticmethod
    def require(condition: bool, message: str) -> None:
        """Raise an optimization-stable failure."""
        if not condition:
            raise AssertionError(message)

    def test_method__verify__reconstructs_all_six_portable_cases(self) -> None:
        """Evidence ID: NV-CAMPAIGN-PERIODIC-TWO-D-011.

        Requirement: Independent portable verification covers all six study cases.
        Method: Authenticate fixtures and reconstruct each balanced comparison.
        Oracle: Independent loop-based parent, gauge, hopping, and spread routes.
        Acceptance: Six cases pass with the exact retained study identity.
        Interpretation: This verifies bounded synthetic sensitivity evidence.
        Limitations: It does not establish convergence or embedding independence.
        """
        result = self.campaign().verify(repository_root=self.root())
        self.require(result.passes, "portable study verification failed")
        self.require(result.case_count == 6, "unexpected study case count")
        self.require(
            result.retained_result_sha256
            == "a4a400f7610520d75f42af991b5b0eacaaaca53ac5dfd0736f072b918d092e11",
            "retained identity mismatch",
        )

    def test_contract__verifier__avoids_extractors_and_rejects_corruption(self) -> None:
        """Evidence ID: NV-CAMPAIGN-PERIODIC-TWO-D-012.

        Requirement: Verification is extractor-independent and corruption-sensitive.
        Method: Inspect imports and mutate one retained native spread summary.
        Oracle: Independent portable case reconstruction.
        Acceptance: No extractor import and mutation is rejected.
        Interpretation: This verifies route separation and sensitivity.
        Limitations: Portable evidence does not authenticate native run files.
        """
        tree = ast.parse(Path(inspect.getfile(Verifier)).read_text())
        modules = tuple(
            node.module
            for node in ast.walk(tree)
            if isinstance(node, ast.ImportFrom) and node.module
        )
        self.require(
            not any("extract" in module for module in modules),
            "verifier imports extractor",
        )
        retained = self.campaign().encoded_documents.result_payload
        marker = b'"native_total_spread_cell_squared": '
        start = retained.find(marker)
        begin = start + len(marker)
        end = retained.find(b"\n", begin)
        mutated = retained[:begin] + b"99.0," + retained[end:]
        with pytest.raises(AssertionError):
            self.campaign(mutated).verify(repository_root=self.root())

    def test_contract__portable_decoder_and_retained_paths__fail_closed(self) -> None:
        """Evidence ID: SV-CAMPAIGN-PERIODIC-TWO-D-018.

        Requirement: Study verification must reject duplicate/nonfinite JSON and any
        retained case path outside its explicit repository root.

        Method: Mutate the result schema key and first portable-result path.

        Oracle: Shared strict JSON and exact repository-confinement contracts.

        Acceptance: Each invalid result raises ``ValueError`` before source use.

        Interpretation: A pass establishes strict adaptation and path confinement.

        Limitations: It does not establish native-file presence or execution provenance.
        """
        payload = self.campaign().encoded_documents.result_payload
        duplicate = payload[:-2] + b',\n  "schema_version": 1\n}\n'
        nonfinite = payload.replace(b'"schema_version": 1', b'"schema_version": NaN', 1)
        escaping = payload.replace(
            b'"portable_result_path": "calculations/research-monograph/periodic-2d/'
            b'wannier90-study-results/mesh_n11.json"',
            b'"portable_result_path": "../../outside.json"',
            1,
        )
        with pytest.raises(ValueError, match="duplicate JSON key"):
            self.campaign(duplicate).verify(repository_root=self.root())
        with pytest.raises(ValueError, match="non-finite JSON constant"):
            self.campaign(nonfinite).verify(repository_root=self.root())
        with pytest.raises(ValueError, match="confined"):
            self.campaign(escaping).verify(repository_root=self.root())
