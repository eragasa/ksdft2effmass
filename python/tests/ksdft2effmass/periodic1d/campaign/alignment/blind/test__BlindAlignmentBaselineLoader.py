# ruff: noqa: E501
r"""Software verification for ``BlindAlignmentBaselineLoader``.

Evidence profile: claim_bearing

Facet and represented meaning
-----------------------------
The module owns authenticated adaptation of matched-extraction artifacts into the
pristine matrix, hidden construction maps, and planted perturbations needed to create
blind observations.

Intrinsic and cross-object scope
--------------------------------
The retained blind input, matched input, matched result, and transitive periodic parent
are filesystem artifacts, so this module is marked as integration evidence. The test
does not import either historical runner.

VVUQ and scientific exclusions
------------------------------
A pass establishes source authentication and represented software invariants. It does
not independently verify every matrix entry, validate silicon, establish physical
alignment, or perform uncertainty quantification.
"""

from dataclasses import replace
from pathlib import Path

import numpy as np
import pytest

from ksdft2effmass.periodic1d.campaign.alignment.blind.baseline import (
    BlindAlignmentBaselineLoader,
)
from ksdft2effmass.periodic1d.campaign.alignment.blind.input_records import (
    BlindAlignmentCampaignInput,
    BlindAlignmentSourceIdentity,
)
from ksdft2effmass.periodic1d.campaign.alignment.blind.serialization import (
    BlindAlignmentInputDeserializer,
)

pytestmark = [pytest.mark.integration, pytest.mark.software_verification]
SUT = BlindAlignmentBaselineLoader


class TestBlindAlignmentBaselineLoader:
    """Own authenticated blind-alignment baseline adaptation evidence."""

    @staticmethod
    def repository_root() -> Path:
        """Return the repository containing retained campaign artifacts."""
        return Path(__file__).resolve().parents[7]

    def specification(self) -> BlindAlignmentCampaignInput:
        """Decode the retained blind-alignment input."""
        path = self.repository_root() / (
            "calculations/research-monograph/"
            "impurity-defect-1d-blind-alignment/input.json"
        )
        return BlindAlignmentInputDeserializer().execute(path.read_bytes())

    def test_method__execute__authenticates_and_adapts_matched_baseline(self) -> None:
        """Evidence ID: SV-CAMPAIGN-PERIODIC-ONE-D-DEFECT-012.

        Requirement: The baseline loader must authenticate direct and transitive
        retained sources before exposing immutable reference, map, and defect records.

        Method: Load the retained blind specification against the repository and
        inspect dimensions, identities, Hermiticity, unitarity, ordering, and
        operational immutability.

        Oracle: Retained source identities and exact finite-space contracts inherited
        from matched extraction.

        Acceptance: Source order and defect inventory agree exactly; matrix dimensions
        agree with spin factors; reference Hermiticity and map unitarity residuals are
        at most ``1e-12``; arrays are read-only.

        Interpretation: A pass establishes authenticated baseline adaptation for later
        observation construction.

        Limitations: These structural and algebraic checks are not an independent
        entrywise reconstruction of the retained parent.
        """
        result = SUT().execute(self.specification(), self.repository_root())

        assert result.cell_count == 16
        assert result.reduced_momentum == pytest.approx(0.010625, abs=0.0)
        assert result.energy_shift == pytest.approx(0.137, abs=0.0)
        assert result.pristine_spinless.shape == (32, 32)
        assert result.candidate_to_reference_spinless.shape == (32, 32)
        assert result.candidate_to_reference_spinor.shape == (64, 64)
        assert tuple(value.identifier for value in result.defects) == (
            "collinear-spin",
            "nearest-neighbor",
            "null",
            "orbital-onsite",
            "range-two-nonlocal",
            "scalar-onsite",
            "spin-mixing",
        )
        assert tuple(value.path for value in result.source_identities) == (
            "calculations/research-monograph/impurity-defect-1d/input.json",
            "calculations/research-monograph/impurity-defect-1d/result.json",
            "calculations/research-monograph/periodic-1d/composite-result.json",
        )
        np.testing.assert_allclose(
            result.pristine_spinless,
            result.pristine_spinless.conj().T,
            rtol=0.0,
            atol=1e-12,
        )
        for matrix in (
            result.candidate_to_reference_spinless,
            result.candidate_to_reference_spinor,
        ):
            np.testing.assert_allclose(
                matrix @ matrix.conj().T,
                np.eye(matrix.shape[0]),
                rtol=0.0,
                atol=1e-12,
            )
            assert not matrix.flags.writeable
        assert result.defect("orbital-onsite").matrix.shape == (32, 32)
        assert result.defect("spin-mixing").matrix.shape == (64, 64)
        assert not result.pristine_spinless.flags.writeable
        assert all(not value.matrix.flags.writeable for value in result.defects)

    def test_method__execute__rejects_direct_source_identity_mismatch(self) -> None:
        """Evidence ID: SV-CAMPAIGN-PERIODIC-ONE-D-DEFECT-013.

        Requirement: Baseline bytes must not be parsed after a direct source identity
        mismatch.

        Method: Replace only the expected matched-input digest with a validly shaped
        but incorrect SHA-256 value.

        Oracle: Exact cryptographic identity gate before deserialization.

        Acceptance: Loading raises ``ValueError`` naming a source identity mismatch.

        Interpretation: A pass establishes fail-closed direct-source authentication.

        Limitations: It does not establish authorship or correctness of bytes whose
        digest does match.
        """
        specification = self.specification()
        corrupted = replace(
            specification,
            baseline_input=BlindAlignmentSourceIdentity(
                specification.baseline_input.path, "0" * 64
            ),
        )

        with pytest.raises(ValueError, match="source identity mismatch"):
            SUT().execute(corrupted, self.repository_root())
