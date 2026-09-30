# ruff: noqa: E501
r"""Numerical verification for ``BlindAlignmentCampaignVerifier``.

Evidence profile: claim_bearing

Facet and represented meaning
-----------------------------
The module owns independent source authentication, structural checks, and numerical
reconstruction of all retained blind-alignment case families.

Intrinsic and cross-object scope
--------------------------------
The verifier reads direct and transitive retained artifacts and is therefore marked as
integration evidence. Its import graph excludes maintained calculation algorithms.

VVUQ and scientific exclusions
------------------------------
A pass establishes independent numerical reconstruction of the bounded synthetic
campaign. It does not validate silicon, transferability, or uncertainty quantification.
"""

import ast
import inspect
from pathlib import Path

import pytest

from ksdft2effmass.campaigns.research_monograph.periodic_1d.defects.blind_alignment.model import (
    BlindAlignmentCampaignModel,
)
from ksdft2effmass.campaigns.research_monograph.periodic_1d.defects.blind_alignment.verification import (
    BlindAlignmentCampaignVerificationRequest,
    BlindAlignmentCampaignVerifier,
)

pytestmark = [pytest.mark.integration, pytest.mark.numerical_verification]
SUT = BlindAlignmentCampaignVerifier


class TestBlindAlignmentCampaignVerifier:
    """Own independent retained-result verification evidence."""

    @staticmethod
    def repository_root() -> Path:
        """Return the repository containing retained campaign artifacts."""
        return Path(__file__).resolve().parents[8]

    def model(
        self, result_document: bytes | None = None
    ) -> BlindAlignmentCampaignModel:
        """Build an encapsulated model, optionally replacing retained result bytes."""
        root = self.repository_root()
        calculation = root / (
            "calculations/research-monograph/impurity-defect-1d-blind-alignment"
        )
        retained = (calculation / "result.json").read_bytes()
        return BlindAlignmentCampaignModel(
            input_document=(calculation / "input.json").read_bytes(),
            retained_result_document=(
                retained if result_document is None else result_document
            ),
            repository_root=root,
        )

    def test_method__execute__independently_verifies_all_retained_cases(self) -> None:
        """Evidence ID: NV-CAMPAIGN-PERIODIC-ONE-D-DEFECT-003.

        Requirement: Independent verification must authenticate sources, check the
        structural contract, and reconstruct every retained numerical case.

        Method: Execute the verifier through only its model-bound request.

        Oracle: Independently implemented matrix construction, SVD/polar inference,
        energy anchoring, extraction, and diagnostic formulas.

        Acceptance: All three verification channels pass; 34 records and three direct
        source identities are reported; the retained digest is lowercase SHA-256.

        Interpretation: A pass establishes independent numerical reconstruction under
        the retained synthetic controls.

        Limitations: This does not establish material validation or uncertainty.
        """
        result = SUT().execute(BlindAlignmentCampaignVerificationRequest(self.model()))

        assert result.passed
        assert result.source_authentication_passed
        assert result.structural_contract_passed
        assert result.numerical_reconstruction_passed
        assert result.verified_case_count == 34
        assert result.source_identity_count == 3
        assert len(result.retained_result_sha256) == 64

    def test_method__execute__rejects_a_mutated_numerical_diagnostic(self) -> None:
        """Evidence ID: NV-CAMPAIGN-PERIODIC-ONE-D-DEFECT-004.

        Requirement: The verifier must compare reconstructed numbers rather than trust
        structurally valid retained fields.

        Method: Change one exact-case energy-shift error while preserving valid JSON and
        every source artifact.

        Oracle: The independent inferred scalar shift and authored hidden shift.

        Acceptance: Verification raises ``ValueError`` for the mismatched field.

        Interpretation: A pass establishes sensitivity to numerical-result corruption.

        Limitations: This mutation samples one of the many checked diagnostics.
        """
        retained = self.model().retained_result_document
        mutated = retained.replace(
            b'"energy_shift_error": 5.551115123125783e-17',
            b'"energy_shift_error": 0.25',
            1,
        )
        if mutated == retained:
            raise ValueError("test mutation target was absent")

        with pytest.raises(
            ValueError, match="retained field mismatch: energy_shift_error"
        ):
            SUT().execute(
                BlindAlignmentCampaignVerificationRequest(self.model(mutated))
            )

    def test_source__verifier__excludes_maintained_calculation_algorithms(self) -> None:
        """Evidence ID: SV-CAMPAIGN-PERIODIC-ONE-D-DEFECT-021.

        Requirement: The independent verifier must not import maintained Workflow,
        construction, inference, case-execution, or evaluation implementations.

        Method: Parse the verifier source and inspect all relative import module names.

        Oracle: The declared independence boundary.

        Acceptance: None of the five prohibited defining modules occurs in imports.

        Interpretation: A pass establishes static implementation separation.

        Limitations: Import separation complements but cannot alone prove algorithmic
        independence.
        """
        source_path = Path(inspect.getfile(SUT))
        tree = ast.parse(source_path.read_text(encoding="utf-8"))
        imported_modules = tuple(
            node.module
            for node in ast.walk(tree)
            if isinstance(node, ast.ImportFrom) and node.module is not None
        )

        for prohibited in (
            "workflow",
            "construction",
            "inference",
            "case_execution",
            "evaluation",
        ):
            assert prohibited not in imported_modules
