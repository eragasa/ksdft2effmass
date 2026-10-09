r"""Strict-wire evidence for the portable optimizer-reanalysis verifier.

Evidence profile: routine

Malformed synthetic wires establish parser rejection only. They do not exercise retained
artifacts, numerical reconstruction, native execution, or scientific acceptance.
"""

from pathlib import Path

import pytest

from ksdft2effmass.periodic2d.run.wannier90.optimizer_basin.reanalysis import (
    Periodic2DOptimizerReanalysisEncodedDocuments,
)
from ksdft2effmass.periodic2d.run.wannier90.optimizer_basin.reanalysis.verify import (
    Periodic2DOptimizerReanalysisCampaignVerificationRequest,
    Periodic2DOptimizerReanalysisCampaignVerifier,
)

pytestmark = pytest.mark.software_verification
SUT = Periodic2DOptimizerReanalysisCampaignVerifier


class TestPeriodic2DOptimizerReanalysisCampaignVerifierStrictDecoding:
    """Own malformed-wire rejection evidence for crosswalk row 053."""

    @pytest.mark.parametrize(
        "payload,exception",
        [
            (b'{"schema_version":1,"schema_version":1}', ValueError),
            (b'{"schema_version":NaN}', ValueError),
            (b"\xff", ValueError),
            (b"[]", TypeError),
        ],
    )
    def test_execute__rejects_ambiguous_or_nonstandard_source_wires(
        self, payload: bytes, exception: type[Exception]
    ) -> None:
        """Evidence ID: SV-PERIODIC-TWO-D-ROW-053-STRICT-001.

        Requirement: Shared strict decoding rejects duplicate keys, nonstandard
        nonfinite constants, invalid UTF-8, and non-object roots before schema use.

        Acceptance: Each malformed source wire raises its documented exception class.
        """
        request = Periodic2DOptimizerReanalysisCampaignVerificationRequest(
            Periodic2DOptimizerReanalysisEncodedDocuments(payload, b"{}"),
            Path("/tmp").resolve(),
        )

        with pytest.raises(exception):
            SUT().execute(request)

    def test_execute__rejects_schema_before_schema_specific_field_access(self) -> None:
        """Evidence ID: SV-PERIODIC-TWO-D-ROW-053-STRICT-002.

        Requirement: Schema selection precedes schema-specific adaptation so an
        unsupported version cannot be interpreted through the version-one field layout.

        Acceptance: A version-two object lacking version-one fields fails on schema
        identity rather than through a later missing-field error.
        """
        request = Periodic2DOptimizerReanalysisCampaignVerificationRequest(
            Periodic2DOptimizerReanalysisEncodedDocuments(
                b'{"schema_version":2}', b"{}"
            ),
            Path("/tmp").resolve(),
        )

        with pytest.raises(AssertionError, match="source schema changed"):
            SUT().execute(request)
