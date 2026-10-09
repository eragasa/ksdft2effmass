r"""Routine decoder-boundary evidence for row-055 standalone documents.

Evidence profile: routine

Synthetic wires test parser mechanics only. They do not authenticate retained artifacts,
reconstruct endpoints, or establish scientific validity.
"""

import pytest

from ksdft2effmass.periodic2d.run.wannier90.optimizer_basin.standalone.decode import (
    OptimizerStandaloneLegacyResultDecoder,
    Periodic2DOptimizerStandaloneDocumentDecoder,
)

pytestmark = pytest.mark.software_verification


class TestPeriodic2DOptimizerStandaloneDocumentDecoder:
    """Own strict and historical-wire decoder evidence for row 055."""

    @pytest.mark.parametrize("token", (b"NaN", b"-Infinity"))
    def test_legacy_decoder__rejects_unsupported_nonfinite_tokens(
        self, token: bytes
    ) -> None:
        """Evidence ID: SV-PERIODIC-TWO-D-ROW-055-DECODE-001.

        Requirement: The historical exception recognizes positive infinity only.

        Acceptance: ``NaN`` and negative infinity fail before schema adaptation.
        """
        with pytest.raises(ValueError, match="unsupported historical constant"):
            OptimizerStandaloneLegacyResultDecoder().execute(
                b'{"value":' + token + b"}"
            )

    def test_legacy_decoder__confines_infinity_to_rejected_mismatch_fields(
        self,
    ) -> None:
        """Evidence ID: SV-PERIODIC-TWO-D-ROW-055-DECODE-002.

        Requirement: Positive infinity is an extended-real value only for the two exact
        rejected-equivalence mismatch fields.

        Acceptance: Both declared paths decode; another root path fails closed.
        """
        valid = (
            b'{"groups":[{"observed_density_d4_basins":['
            b'{"rejected_equivalence_candidates":['
            b'{"center_set_periodic_distance":Infinity,'
            b'"maximum_density_l2_mismatch":Infinity}]}]}]}'
        )
        decoded = OptimizerStandaloneLegacyResultDecoder().execute(valid)
        assert "groups" in decoded
        with pytest.raises(ValueError, match="outside the historical contract"):
            OptimizerStandaloneLegacyResultDecoder().execute(
                b'{"omega_total_cell_squared":Infinity}'
            )

    @pytest.mark.parametrize(
        "payload",
        (
            (
                b'{"groups":[{"observed_density_d4_basins":['
                b'{"rejected_equivalence_candidates":['
                b'{"extra":{"center_set_periodic_distance":Infinity}}]}]}]}'
            ),
            (
                b'{"groups":{"observed_density_d4_basins":['
                b'{"rejected_equivalence_candidates":['
                b'{"center_set_periodic_distance":Infinity}]}]}}'
            ),
            (
                b'{"groups":[{"lookalike_observed_density_d4_basins":['
                b'{"rejected_equivalence_candidates":['
                b'{"maximum_density_l2_mismatch":Infinity}]}]}]}'
            ),
        ),
    )
    def test_legacy_decoder__rejects_near_miss_extended_real_paths(
        self, payload: bytes
    ) -> None:
        """Evidence ID: SV-PERIODIC-TWO-D-ROW-055-DECODE-005.

        Requirement: Historical positive infinity requires the complete seven-part path
        with array indices and exact object-field names.

        Acceptance: Extra nesting, a missing group index, and a look-alike ancestor name
        each fail closed.
        """
        with pytest.raises(ValueError, match="outside the historical contract"):
            OptimizerStandaloneLegacyResultDecoder().execute(payload)

    def test_legacy_decoder__rejects_duplicate_keys(self) -> None:
        """Evidence ID: SV-PERIODIC-TWO-D-ROW-055-DECODE-003.

        Requirement: The historical adapter must not weaken duplicate-key rejection.

        Acceptance: A repeated object key raises ``ValueError``.
        """
        with pytest.raises(ValueError, match="duplicate JSON key"):
            OptimizerStandaloneLegacyResultDecoder().execute(b'{"x":1,"x":2}')

    def test_document_decoder__requires_exact_document_owner(self) -> None:
        """Evidence ID: SV-PERIODIC-TWO-D-ROW-055-DECODE-004.

        Requirement: Schema adaptation begins only after exact owner selection.

        Acceptance: A structural substitute fails without parsing.
        """
        with pytest.raises(TypeError, match="documents must be"):
            Periodic2DOptimizerStandaloneDocumentDecoder().execute(
                (b"{}", b"{}", b"{}")  # type: ignore[arg-type]
            )
