"""Retained correlation and verification for the isolated periodic-2D campaign."""

import ast
import inspect
from pathlib import Path

import pytest

from ksdft2effmass.periodic2d.campaign.nbands_1 import (
    Periodic2DIsolatedBandCampaign,
    Periodic2DIsolatedBandCampaignJsonSerializer,
    Periodic2DIsolatedBandCampaignVerifier,
    Periodic2DIsolatedBandEncodedDocuments,
)

pytestmark = [
    pytest.mark.integration,
    pytest.mark.numerical_verification,
    pytest.mark.expensive,
]


class TestPeriodic2DIsolatedBandCampaign:
    """Own retained composition, verification, and independence evidence."""

    @staticmethod
    def root() -> Path:
        """Return the repository containing retained periodic-2D artifacts."""
        return Path(__file__).resolve().parents[6]

    def campaign(
        self, result_payload: bytes | None = None
    ) -> Periodic2DIsolatedBandCampaign:
        """Build the campaign from exact retained documents."""
        retained = self.root() / "calculations/research-monograph/periodic-2d"
        original = (retained / "result.json").read_bytes()
        return Periodic2DIsolatedBandCampaign(
            Periodic2DIsolatedBandEncodedDocuments(
                (retained / "input.json").read_bytes(),
                original if result_payload is None else result_payload,
            )
        )

    @staticmethod
    def require(condition: bool, message: str) -> None:
        """Raise an optimization-stable test failure when a condition is false."""
        if not condition:
            raise AssertionError(message)

    def test_method__correlate_and_verify__reproduces_retained_scalar_campaign(
        self,
    ) -> None:
        """Evidence ID: NV-CAMPAIGN-PERIODIC-TWO-D-001.

        Requirement: Maintained and independent routes must reproduce the retained
        scalar periodic-2D campaign without modifying its version-one artifact.

        Method: Recalculate under retained provenance and independently reconstruct
        parent, separability, topology, hopping, mass, and anisotropy channels.

        Oracle: Independent vectorized Fourier and finite-difference reconstruction.

        Acceptance: Canonical SHA-256 identity agrees, all independent channels pass,
        and all four coupling cases are reconstructed.

        Interpretation: A pass is bounded synthetic numerical verification.

        Limitations: It proves no material behavior or continuum convergence.
        """
        campaign = self.campaign()
        correlation = campaign.correlate()
        verification = campaign.verify(repository_root=self.root())

        self.require(correlation.passes, "retained correlation failed")
        self.require(
            correlation.retained_sha256
            == "4eb55bde9d456d86bad1d65c8ac60267c07873c6936f8af876b07fd3e1d27be6",
            "retained identity mismatch",
        )
        self.require(verification.passes, "independent verification failed")
        self.require(
            verification.coupling_case_count == 4,
            "coupling inventory mismatch",
        )

    def test_method__verify__rejects_numerical_corruption(self) -> None:
        """Evidence ID: NV-CAMPAIGN-PERIODIC-TWO-D-002.

        Requirement: Independent verification must reject changed retained metrics.

        Method: Replace the first retained plane-wave cutoff error.

        Oracle: Independent finite plane-wave reconstruction.

        Acceptance: Verification raises ``ValueError`` or a NumPy comparison failure.

        Interpretation: A pass establishes sensitivity to numerical corruption.

        Limitations: One representative scalar channel is mutated.
        """
        retained = self.campaign().encoded_documents.result_payload
        marker = b'"maximum_low_band_absolute_error": '
        start = retained.find(marker)
        if start < 0:
            raise ValueError("test mutation target was absent")
        begin = start + len(marker)
        end = retained.find(b"\n", begin)
        mutated = retained[:begin] + b"0.25," + retained[end:]
        with pytest.raises((ValueError, AssertionError)):
            self.campaign(mutated).verify(repository_root=self.root())

    def test_contract__wire_and_import_boundaries__remain_explicit(self) -> None:
        """Evidence ID: SV-CAMPAIGN-PERIODIC-TWO-D-008.

        Requirement: Version-one input is strict and independent verification imports
        neither maintained calculation nor reusable toy-model implementations.

        Method: Exercise duplicate-key rejection and inspect verifier imports.

        Oracle: Closed wire and independent-route ownership contracts.

        Acceptance: Duplicate keys fail and prohibited implementation modules are
        absent.

        Interpretation: A pass establishes structural software boundaries.

        Limitations: Import separation is not independent physical evidence.
        """
        with pytest.raises(ValueError, match="duplicate JSON key"):
            Periodic2DIsolatedBandCampaignJsonSerializer().deserialize(
                b'{"schema_version":1,"schema_version":1}'
            )
        tree = ast.parse(
            Path(inspect.getfile(Periodic2DIsolatedBandCampaignVerifier)).read_text()
        )
        modules = tuple(
            node.module
            for node in ast.walk(tree)
            if isinstance(node, ast.ImportFrom) and node.module is not None
        )
        self.require("calculate" not in modules, "verifier imports calculation route")
        self.require(
            not any("toy_models" in module for module in modules),
            "verifier imports maintained toy-model constructor",
        )
