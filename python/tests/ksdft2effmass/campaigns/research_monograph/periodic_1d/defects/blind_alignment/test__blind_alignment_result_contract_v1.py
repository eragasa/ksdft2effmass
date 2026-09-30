# ruff: noqa: E501
r"""Software verification for the blind-alignment version-one result artifact.

Evidence profile: claim_bearing

Facet and represented meaning
-----------------------------
The module owns strict typed decoding, canonical encoding, and identity-only
correlation of the retained version-one blind-alignment result.

Intrinsic and cross-object scope
--------------------------------
The retained JSON file is the primary artifact under test, so the module is marked as
integration evidence. Serialization uses the public result records but does not execute
the numerical campaign.

VVUQ and scientific exclusions
------------------------------
A pass establishes wire-contract and identity behavior. It does not independently
recompute the matrices or numerically verify, scientifically validate, or quantify
uncertainty in the retained result.
"""

from collections.abc import Callable
from pathlib import Path

import pytest

from ksdft2effmass.campaigns.research_monograph.periodic_1d.defects.blind_alignment.result_encoding import (
    BlindAlignmentResultSerializer,
    BlindAlignmentRetainedResultCorrelator,
)
from ksdft2effmass.campaigns.research_monograph.periodic_1d.defects.blind_alignment.result_records import (
    BlindAlignmentResultCorrelationRequest,
)
from ksdft2effmass.campaigns.research_monograph.periodic_1d.defects.blind_alignment.result_serialization import (
    BlindAlignmentResultDeserializer,
)

pytestmark = [pytest.mark.integration, pytest.mark.software_verification]
type ResultPayloadMutation = Callable[[bytes], bytes]


class TestBlindAlignmentResultContractV1:
    """Own retained version-one result wire-contract evidence."""

    @staticmethod
    def retained_payload() -> bytes:
        """Read the retained result from its authoritative calculation package."""
        repository_root = Path(__file__).resolve().parents[8]
        return (
            repository_root / "calculations/research-monograph/"
            "impurity-defect-1d-blind-alignment/result.json"
        ).read_bytes()

    def test_artifact__retained_result__decodes_complete_typed_contract(self) -> None:
        """Evidence ID: SV-CAMPAIGN-PERIODIC-ONE-D-DEFECT-017.

        Requirement: Every retained version-one result section must decode into closed
        immutable records rather than erased JSON mappings.

        Method: Decode the retained artifact and inspect all ordered family counts and
        representative boundary dispositions.

        Oracle: The authored version-one result contract and retained artifact.

        Acceptance: Exact, noise, stop, conditioning, principal-angle, and energy-anchor
        counts are respectively 2, 6, 5, 6, 5, and 7; gauge and rank cases are partial;
        the spin-lift case is full.

        Interpretation: A pass establishes complete typed consumption of the retained
        document.

        Limitations: Decoding does not recompute or verify retained numerical values.
        """
        result = BlindAlignmentResultDeserializer().deserialize(self.retained_payload())

        assert len(result.exact_full_rank_cases) == 2
        assert len(result.noise_sweep) == 6
        assert len(result.stopping_cases) == 5
        assert len(result.debugging_diagnostics.conditioning_boundary) == 6
        assert len(result.debugging_diagnostics.principal_angle_boundary) == 5
        assert len(result.debugging_diagnostics.energy_anchor_boundary) == 7
        assert result.gauge_equivalent_case.case.status == "aligned_partial"
        assert result.debugging_diagnostics.rank_reconciliation.case.status == (
            "aligned_partial"
        )
        assert (
            result.debugging_diagnostics.spin_reconciliation.lifted_alignment.status
            == ("aligned_full")
        )

    def test_artifact__retained_result__round_trips_canonical_bytes(self) -> None:
        """Evidence ID: SV-CAMPAIGN-PERIODIC-ONE-D-DEFECT-018.

        Requirement: Canonical typed serialization must reproduce the retained
        version-one bytes and expose correlation separately from verification.

        Method: Decode, encode, and correlate the retained artifact against itself.

        Oracle: Exact retained bytes and their SHA-256 identity.

        Acceptance: Encoded bytes are identical; semantic and canonical-byte channels
        are true; calculated and retained digests agree.

        Interpretation: A pass establishes canonical compatibility and identity-only
        correlation.

        Limitations: Byte identity is not numerical or scientific verification.
        """
        payload = self.retained_payload()
        decoded = BlindAlignmentResultDeserializer().deserialize(payload)
        encoded = BlindAlignmentResultSerializer().serialize(decoded)
        correlation = BlindAlignmentRetainedResultCorrelator().execute(
            BlindAlignmentResultCorrelationRequest(decoded, payload)
        )

        assert encoded == payload
        assert correlation.semantic_equal
        assert correlation.canonical_bytes_equal
        assert correlation.calculated_sha256 == correlation.retained_sha256

    @pytest.mark.parametrize(
        ("mutation", "message"),
        (
            pytest.param(
                lambda payload: payload.replace(
                    b'  "schema_version": 1,',
                    b'  "schema_version": 1,\n  "schema_version": 1,',
                    1,
                ),
                "duplicate JSON key",
                id="duplicate-key",
            ),
            pytest.param(
                lambda payload: payload.replace(
                    b'"calculation_status": "calculated synthetic '
                    b'numerical-verification result"',
                    b'"calculation_status": "validated material result"',
                    1,
                ),
                "calculation_status",
                id="unsupported-evidence-status",
            ),
        ),
    )
    def test_artifact__invalid_result__is_rejected(
        self, mutation: ResultPayloadMutation, message: str
    ) -> None:
        """Evidence ID: SV-CAMPAIGN-PERIODIC-ONE-D-DEFECT-019.

        Requirement: Duplicate members and unsupported evidentiary declarations must
        be rejected even when JSON remains syntactically parseable.

        Method: Mutate only one structural or fixed-declaration channel.

        Oracle: Closed version-one member and evidence-status contracts.

        Acceptance: Decoding raises ``ValueError`` containing the expected diagnostic.

        Interpretation: A pass establishes fail-closed result parsing.

        Limitations: These cases do not enumerate every invalid nested scalar.
        """
        with pytest.raises(ValueError, match=message):
            BlindAlignmentResultDeserializer().deserialize(
                mutation(self.retained_payload())
            )
