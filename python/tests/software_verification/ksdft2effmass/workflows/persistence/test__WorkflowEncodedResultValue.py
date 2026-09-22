r"""Software verification of ``WorkflowEncodedResultValue``.

Bounded artifact scope: nominal concrete-result envelope and exact-byte SHA-256.

Evidence profile: claim_bearing

Facet and represented meaning

An immutable envelope binds complete payload bytes independently of content labels.

Intrinsic and cross-object scope

Only nominal fields and byte-digest invariants are owned here; no codec is implied.

VVUQ and scientific exclusions

Software verification only; no science, authority, complete run or store evidence.
"""

from dataclasses import FrozenInstanceError, replace

import pytest

from ksdft2effmass.workflows import (
    ResultObjectContentIdentity,
    ResultObjectDomainIdentity,
    ResultObjectIdentity,
    ResultObjectTypeIdentity,
    WorkflowEncodedResultValue,
)

pytestmark = pytest.mark.software_verification
SUT = WorkflowEncodedResultValue


class TestWorkflowEncodedResultValue:
    """Exact bytes with independent published SHA-256 empty-input test vector."""

    @staticmethod
    def make_envelope() -> WorkflowEncodedResultValue:
        return WorkflowEncodedResultValue(
            result_identity=ResultObjectIdentity("synthetic-result"),
            concrete_type_identity=ResultObjectTypeIdentity("synthetic-type:1"),
            owning_domain_identity=ResultObjectDomainIdentity("synthetic-domain"),
            schema_identity="synthetic-wire:1",
            content_identity=ResultObjectContentIdentity("opaque-owner-label"),
            payload=b"",
            payload_digest="e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
        )

    def test_constructor__payload__retains_opaque_content_label(self) -> None:
        """Evidence ID: SV-WFR-ENVELOPE-001

        Requirement: Byte digest is separate from owner-defined content identity.

        Method: Construct directly using the independent SHA256 empty-input vector.

        Oracle: SHA256 empty-input digest and literal independently supplied labels.

        Acceptance: Empty byte test vector and opaque content label remain exact.

        Interpretation: Intrinsic binding does not pretend to understand the payload.

        Limitations: This envelope is not a supported complete concrete result wire.
        """
        value = self.make_envelope()
        assert value.payload == b""
        assert value.content_identity.value == "opaque-owner-label"
        assert value.result_identity == ResultObjectIdentity("synthetic-result")

    @pytest.mark.parametrize(
        "digest",
        [
            pytest.param("0" * 64, id="wrong_digest"),
            pytest.param(
                "E3B0C44298FC1C149AFBF4C8996FB92427AE41E4649B934CA495991B7852B855",
                id="uppercase_digest",
            ),
            pytest.param("sha256:empty", id="opaque_digest"),
        ],
    )
    def test_constructor__payload__rejects_digest_mismatch(self, digest: str) -> None:
        """Evidence ID: SV-WFR-ENVELOPE-002

        Requirement: Envelope payload digest must equal the exact byte digest.

        Method: Substitute a digest around fixed independent empty-input bytes.

        Oracle: Exact lowercase SHA256 empty-input vector.

        Acceptance: Each digest not exactly matching SHA256 raises ValueError.

        Interpretation: Wrong or noncanonical digest labels never bind bytes.

        Limitations: Digest agreement is not authentication or scientific validation.
        """
        with pytest.raises(ValueError):
            replace(self.make_envelope(), payload_digest=digest)

    @pytest.mark.parametrize(
        "invalid",
        [
            pytest.param(bytearray(), id="mutable_bytes"),
            pytest.param("", id="text"),
        ],
    )
    def test_constructor__payload__rejects_nonbytes(
        self, invalid: bytearray | str
    ) -> None:
        """Evidence ID: SV-WFR-ENVELOPE-003

        Requirement: Envelopes cannot retain mutable or implicitly encoded payloads.

        Method: Replace the payload with explicit closed invalid semantic types.

        Oracle: The exact bytes constructor field contract.

        Acceptance: Mutable byte buffer or text input raises TypeError.

        Interpretation: Exact immutable byte ownership is required at the boundary.

        Limitations: No payload schema decoding is performed by the envelope.
        """
        value = self.make_envelope()
        with pytest.raises(TypeError):
            WorkflowEncodedResultValue(
                result_identity=value.result_identity,
                concrete_type_identity=value.concrete_type_identity,
                owning_domain_identity=value.owning_domain_identity,
                schema_identity=value.schema_identity,
                content_identity=value.content_identity,
                payload=invalid,  # type: ignore[arg-type]
                payload_digest=value.payload_digest,
            )

    def test_field__payload__is_immutable(self) -> None:
        """Evidence ID: SV-WFR-ENVELOPE-004

        Requirement: Encoded result envelopes are operationally immutable.

        Method: Attempt to overwrite one frozen payload field.

        Oracle: Frozen dataclass semantics and independent original bytes.

        Acceptance: Direct assignment raises and original bytes remain empty.

        Interpretation: Maintained envelope content cannot drift by normal assignment.

        Limitations: No hostile reflection or memory mutation guarantee is asserted.
        """
        value = self.make_envelope()
        with pytest.raises(FrozenInstanceError):
            value.payload = b"replacement"  # type: ignore[misc]
        assert value.payload == b""
