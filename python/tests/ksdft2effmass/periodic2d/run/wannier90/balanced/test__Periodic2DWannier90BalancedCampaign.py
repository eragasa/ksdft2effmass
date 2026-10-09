"""Portable evidence for the balanced periodic-2D Wannier90 comparison."""

import ast
import inspect
from pathlib import Path

import pytest

from ksdft2effmass.periodic2d import (
    Periodic2DWannier90BalancedCampaign,
    Periodic2DWannier90BalancedEncodedDocuments,
)
from ksdft2effmass.periodic2d.run import wannier90

Reconstructor = wannier90.balanced.verify.Periodic2DWannier90BalancedReconstructor
Verifier = wannier90.balanced.verify.Periodic2DWannier90BalancedCampaignVerifier
pytestmark = [
    pytest.mark.integration,
    pytest.mark.numerical_verification,
    pytest.mark.expensive,
]


class TestPeriodic2DWannier90BalancedCampaign:
    """Own repository-portable balanced comparison evidence."""

    @staticmethod
    def root() -> Path:
        """Return the repository root."""
        return Path(__file__).resolve().parents[7]

    def campaign(
        self, result: bytes | None = None
    ) -> Periodic2DWannier90BalancedCampaign:
        """Construct a campaign from retained exact result bytes."""
        path = self.root() / (
            "calculations/research-monograph/periodic-2d/wannier90-balanced-result.json"
        )
        retained = path.read_bytes()
        return Periodic2DWannier90BalancedCampaign(
            Periodic2DWannier90BalancedEncodedDocuments(
                retained if result is None else result
            )
        )

    @staticmethod
    def require(condition: bool, message: str) -> None:
        """Raise an optimization-stable failure."""
        if not condition:
            raise AssertionError(message)

    def test_method__verify__reconstructs_portable_balanced_comparison(self) -> None:
        """Evidence ID: NV-CAMPAIGN-PERIODIC-TWO-D-009.

        Requirement: Repository evidence reconstructs the balanced comparison.
        Method: Authenticate sources and rebuild parent, gauges, hopping, and spreads.
        Oracle: Independent loop-based Hamiltonian and Hermitian polar routes.
        Acceptance: Portable reconstruction passes with the retained result identity.
        Interpretation: This verifies one bounded synthetic external-tool result.
        Limitations: It does not rerun Wannier90 or establish convergence.
        """
        result = self.campaign().verify(repository_root=self.root())
        self.require(result.passes, "portable Wannier90 verification failed")
        self.require(
            result.retained_result_sha256
            == "422e53b012fb824164e3f03e67eeef6f5a013ce6f17da942ddc3f2d477b06e93",
            "retained identity mismatch",
        )

    def test_contract__verifier__does_not_import_extractor_and_rejects_corruption(
        self,
    ) -> None:
        """Evidence ID: NV-CAMPAIGN-PERIODIC-TWO-D-010.

        Requirement: Verification is extractor-independent and corruption-sensitive.
        Method: Inspect imports and mutate one retained represented quantity.
        Oracle: Independent portable reconstruction.
        Acceptance: No extractor import and mutation is rejected.
        Interpretation: This verifies route separation and sensitivity.
        Limitations: Portable evidence does not authenticate absent native files.
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
        marker = b'"direct_w90_projector_maximum_frobenius_defect": '
        start = retained.find(marker)
        begin = start + len(marker)
        end = retained.find(b"\n", begin)
        mutated = retained[:begin] + b"0.5," + retained[end:]
        with pytest.raises(AssertionError):
            self.campaign(mutated).verify(repository_root=self.root())

    def test_contract__portable_decoder_and_paths__fail_closed(
        self, tmp_path: Path
    ) -> None:
        """Evidence ID: SV-CAMPAIGN-PERIODIC-TWO-D-017.

        Requirement: Portable verification must reject duplicate/nonfinite JSON and
        explicit or symlinked source paths outside its repository root.

        Method: Mutate the retained root key, use an escaping extractor path, and place
        the fixed composite-result route behind an escaping symlink.

        Oracle: Shared strict JSON and exact repository-confinement contracts.

        Acceptance: All four invalid inputs raise ``ValueError`` before reading an
        unauthenticated source outside the repository root.

        Interpretation: A pass establishes strict adaptation and source confinement.

        Limitations: It does not authenticate any unavailable native artifact.
        """
        payload = self.campaign().encoded_documents.result_payload
        duplicate = payload[:-2] + b',\n  "schema_version": 1\n}\n'
        nonfinite = payload.replace(b'"schema_version": 1', b'"schema_version": NaN', 1)
        root = self.root()
        extractor = (
            root / "calculations/research-monograph/periodic-2d/extract_wannier90.py"
        )
        with pytest.raises(ValueError, match="duplicate JSON key"):
            Reconstructor().execute_portable(
                duplicate, repository_root=root, extractor_path=extractor
            )
        with pytest.raises(ValueError, match="non-finite JSON constant"):
            Reconstructor().execute_portable(
                nonfinite, repository_root=root, extractor_path=extractor
            )
        with pytest.raises(ValueError, match="confined"):
            Reconstructor().execute_portable(
                payload,
                repository_root=root,
                extractor_path=root.parent / "outside.py",
            )

        temporary_root = tmp_path / "repository"
        temporary_calculation = temporary_root / (
            "calculations/research-monograph/periodic-2d"
        )
        temporary_calculation.mkdir(parents=True)
        temporary_extractor = temporary_calculation / "extract_wannier90.py"
        temporary_extractor.write_bytes(extractor.read_bytes())
        outside_composite = tmp_path / "outside-composite-result.json"
        outside_composite.write_bytes(
            (
                root
                / "calculations/research-monograph/periodic-2d/composite-result.json"
            ).read_bytes()
        )
        (temporary_calculation / "composite-result.json").symlink_to(outside_composite)
        with pytest.raises(ValueError, match="composite result path must be confined"):
            Reconstructor().execute_portable(
                payload,
                repository_root=temporary_root,
                extractor_path=temporary_extractor,
            )
