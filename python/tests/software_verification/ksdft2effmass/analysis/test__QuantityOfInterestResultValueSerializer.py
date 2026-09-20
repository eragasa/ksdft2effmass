r"""Software verification of ``QuantityOfInterestResultValueSerializer``.

Bounded artifact scope: exact two-family scalar result-value codec version 1.

Evidence profile: claim_bearing

Facet and represented meaning

Complete scalar definitions, ordered requirements, nominal provenance and signed zero
are retained in canonical bytes. Synthetic fixture labels are not research results.

Intrinsic and cross-object scope

The codec alone owns canonical concrete representation and envelope correlation.
Independent literal wire and independently constructed records are the oracles.

VVUQ and scientific exclusions

Software verification only; no evaluation, unit conversion, scientific execution,
validation, uncertainty quantification, repository closure or human acceptance.
"""

import hashlib
from dataclasses import FrozenInstanceError, dataclass, replace
from pathlib import Path
from typing import Never

import pytest

from ksdft2effmass.analysis import (
    NormalizedObservationRequirementIdentity,
    QuantityOfInterestCompleteness,
    QuantityOfInterestConventionIdentity,
    QuantityOfInterestEvaluationFailureCode,
    QuantityOfInterestEvaluatorIdentity,
    QuantityOfInterestIdentity,
    QuantityOfInterestResultValueSerializer,
    QuantityOfInterestStateSpaceIdentity,
    QuantityOfInterestSubjectIdentity,
    ScalarQuantityOfInterestDefinition,
    ScalarQuantityOfInterestEvaluationFailure,
    ScalarQuantityOfInterestValue,
)
from ksdft2effmass.workflows import (
    ResultObjectContentIdentity,
    ResultObjectDomainIdentity,
    ResultObjectIdentity,
    ResultObjectTypeIdentity,
    WorkflowEncodedResultValue,
    WorkflowPersistenceFailureCode,
    WorkflowResultValueCodec,
)

pytestmark = pytest.mark.software_verification
SUT = QuantityOfInterestResultValueSerializer


class TestQuantityOfInterestResultValueSerializer:
    """One exact public codec, independently specified complete scalar values."""

    @staticmethod
    def make_value() -> ScalarQuantityOfInterestValue:
        evaluator = QuantityOfInterestEvaluatorIdentity("synthetic-evaluator:7")
        return ScalarQuantityOfInterestValue(
            ResultObjectIdentity("synthetic-result"),
            ScalarQuantityOfInterestDefinition(
                QuantityOfInterestIdentity("synthetic-qoi"),
                QuantityOfInterestSubjectIdentity("synthetic-subject"),
                QuantityOfInterestStateSpaceIdentity("synthetic-space"),
                QuantityOfInterestConventionIdentity("synthetic-convention"),
                evaluator,
                (
                    NormalizedObservationRequirementIdentity("second"),
                    NormalizedObservationRequirementIdentity("first"),
                ),
                QuantityOfInterestCompleteness.COMPLETE,
                "synthetic-unit",
            ),
            ResultObjectIdentity("synthetic-observations"),
            evaluator,
            -0.0,
        )

    @staticmethod
    def fixture_bytes() -> bytes:
        return (
            Path(__file__)
            .with_name("resources")
            .joinpath("result-values-v1.json")
            .read_bytes()
        )

    @staticmethod
    def make_envelope(payload: bytes) -> WorkflowEncodedResultValue:
        digest = hashlib.sha256(payload).hexdigest()
        return WorkflowEncodedResultValue(
            result_identity=ResultObjectIdentity("synthetic-result"),
            concrete_type_identity=ResultObjectTypeIdentity(
                "ksdft2effmass.analysis.ScalarQuantityOfInterestValue:1"
            ),
            owning_domain_identity=ResultObjectDomainIdentity("ksdft2effmass.analysis"),
            schema_identity="qoi-result-value:1",
            content_identity=ResultObjectContentIdentity(
                f"qoi-result-value:1:sha256:{digest}"
            ),
            payload=payload,
            payload_digest=digest,
        )

    def test_method__encode__matches_independent_complete_wire(self) -> None:
        """Evidence ID: SV-QOI-CODEC-001

        Requirement: Encoding preserves complete concrete scalar content canonically.

        Method: Encode independently constructed records and compare a literal wire.

        Oracle: Hand-authored result-values-v1.json with explicit tags and field order.

        Acceptance: Exact literal bytes and independently bound envelope agree.

        Interpretation: All declared scalar and definition fields are encoded.

        Limitations: This synthetic wire is not a calculated physical value.
        """
        result = QuantityOfInterestResultValueSerializer().encode(self.make_value())
        assert result.status == "encoded"
        assert result.failure is None
        assert result.encoded == self.make_envelope(self.fixture_bytes())

    def test_method__decode__reconstructs_independent_wire(self) -> None:
        """Evidence ID: SV-QOI-CODEC-002

        Requirement: Decode reconstructs complete nominal provenance without coercion.

        Method: Decode the literal wire and compare separately constructed records.

        Oracle: Exact source constructor fields and binary64 negative-zero hex form.

        Acceptance: Concrete type, complete fields and negative zero agree exactly.

        Interpretation: Decode does not rely on an encode-generated expected value.

        Limitations: No numerical evaluation or scientific interpretation is tested.
        """
        result = QuantityOfInterestResultValueSerializer().decode(
            self.make_envelope(self.fixture_bytes())
        )
        assert result.status == "decoded"
        assert type(result.value) is ScalarQuantityOfInterestValue
        assert result.value == self.make_value()
        assert result.value.value.hex() == "-0x0.0p+0"
        assert result.failure is None

    @pytest.mark.parametrize(
        "code",
        [
            pytest.param(
                QuantityOfInterestEvaluationFailureCode.UNAVAILABLE, id="unavailable"
            ),
            pytest.param(
                QuantityOfInterestEvaluationFailureCode.INCOMPLETE, id="incomplete"
            ),
            pytest.param(
                QuantityOfInterestEvaluationFailureCode.INCOMPATIBLE, id="incompatible"
            ),
            pytest.param(QuantityOfInterestEvaluationFailureCode.INVALID, id="invalid"),
            pytest.param(QuantityOfInterestEvaluationFailureCode.ERROR, id="error"),
        ],
    )
    def test_method__decode__retains_closed_failure(
        self, code: QuantityOfInterestEvaluationFailureCode
    ) -> None:
        """Evidence ID: SV-QOI-CODEC-003

        Requirement: Failure serialization never substitutes a successful scalar.

        Method: Encode and decode explicit failures with the complete quantity.

        Oracle: Independent input records and the closed scalar-failure contract.

        Acceptance: Exact failure record returns with no fabricated scalar field.

        Interpretation: All five evaluation-failure variants remain distinct data.

        Limitations: Round trip alone does not establish an independent wire oracle.
        """
        source = self.make_value()
        value = ScalarQuantityOfInterestEvaluationFailure(
            source.identity,
            source.quantity,
            source.source_observation_set_result_identity,
            source.evaluator_identity,
            code,
            "synthetic unavailable observation",
        )
        codec = QuantityOfInterestResultValueSerializer()
        encoded = codec.encode(value)
        assert encoded.encoded is not None
        decoded = codec.decode(encoded.encoded)
        assert decoded.status == "decoded"
        assert type(decoded.value) is ScalarQuantityOfInterestEvaluationFailure
        assert decoded.value == value
        assert b'"value":{"fields"' not in encoded.encoded.payload

    @pytest.mark.parametrize(
        "old,new",
        [
            pytest.param(b'"-0x0.0p+0"', b'"nan"', id="nonfinite_float"),
            pytest.param(b'"-0x0.0p+0"', b"0", id="untagged_integer"),
            pytest.param(b'"-0x0.0p+0"', b"true", id="boolean_float"),
            pytest.param(b'"-0x0.0p+0"', b'"-0x0p+0"', id="noncanonical_hex"),
            pytest.param(
                b'"unit":"synthetic-unit"',
                b'"unit":"synthetic-unit","extra":null',
                id="extra_field",
            ),
            pytest.param(
                b'"unit":"synthetic-unit"',
                b'"unit":"synthetic-unit","unit":"synthetic-unit"',
                id="duplicate_member",
            ),
            pytest.param(
                b'"unit":"synthetic-unit"', b'"unit":null', id="wrong_field_type"
            ),
            pytest.param(
                b'"QuantityOfInterestStateSpaceIdentity"',
                b'"QuantityOfInterestSubjectIdentity"',
                id="wrong_nominal_tag",
            ),
            pytest.param(b'"second"', b'"first"', id="duplicate_requirements"),
        ],
    )
    def test_method__decode__rejects_known_wire_corruption(
        self, old: bytes, new: bytes
    ) -> None:
        """Evidence ID: SV-QOI-CODEC-004

        Requirement: A matching digest cannot legitimize malformed known content.

        Method: Mutate one literal fixture member and update envelope byte binding.

        Oracle: Explicit known-wire grammar and owning constructor invariants.

        Acceptance: Corrupt outcome has failure evidence and no concrete value.

        Interpretation: Digest-valid bytes still require canonical domain closure.

        Limitations: Cases establish only the named deterministic wire partitions.
        """
        result = QuantityOfInterestResultValueSerializer().decode(
            self.make_envelope(self.fixture_bytes().replace(old, new))
        )
        assert result.status == "corrupt"
        assert result.value is None
        assert result.failure is not None

    @pytest.mark.parametrize(
        "suffix",
        [
            pytest.param(b"\n", id="trailing_newline"),
            pytest.param(b" ", id="trailing_space"),
            pytest.param(b"{}", id="trailing_record"),
        ],
    )
    def test_method__decode__requires_exact_canonical_bytes(
        self, suffix: bytes
    ) -> None:
        """Evidence ID: SV-QOI-CODEC-005

        Requirement: Complete decode and re-encode must agree byte for byte.

        Method: Append named byte suffixes to a literal complete representation.

        Oracle: The version-one no-trailing-bytes canonical grammar.

        Acceptance: Any named trailing data yields corrupt without a value.

        Interpretation: JSON parser acceptance does not define canonical bytes.

        Limitations: Does not claim arbitrary text format compatibility.
        """
        result = QuantityOfInterestResultValueSerializer().decode(
            self.make_envelope(self.fixture_bytes() + suffix)
        )
        assert result.status == "corrupt"
        assert result.value is None

    @pytest.mark.parametrize(
        "field,label,status,code",
        [
            pytest.param(
                "schema",
                "qoi-result-value:2",
                "incompatible",
                WorkflowPersistenceFailureCode.UNSUPPORTED_VERSION,
                id="unknown_schema",
            ),
            pytest.param(
                "type",
                "ksdft2effmass.analysis.ScalarQuantityOfInterestValue:2",
                "incompatible",
                WorkflowPersistenceFailureCode.UNSUPPORTED_TYPE,
                id="unknown_type_version",
            ),
            pytest.param(
                "domain",
                "other-domain",
                "corrupt",
                WorkflowPersistenceFailureCode.IDENTITY_MISMATCH,
                id="detached_domain",
            ),
            pytest.param(
                "identity",
                "other-result",
                "corrupt",
                WorkflowPersistenceFailureCode.IDENTITY_MISMATCH,
                id="detached_identity",
            ),
            pytest.param(
                "content",
                "opaque-other-content",
                "corrupt",
                WorkflowPersistenceFailureCode.CONTENT_MISMATCH,
                id="detached_content",
            ),
        ],
    )
    def test_method__decode__rejects_detached_envelope(
        self, field: str, label: str, status: str, code: WorkflowPersistenceFailureCode
    ) -> None:
        """Evidence ID: SV-QOI-CODEC-006

        Requirement: Detached or unsupported metadata cannot reconstruct success.

        Method: Substitute one field around otherwise identical literal bytes.

        Oracle: Version-one domain, type and content binding contract.

        Acceptance: Expected closed category/code returns without a result value.

        Interpretation: Every outward envelope identity participates in decoding.

        Limitations: Labels and hashes provide consistency, not authentication.
        """
        envelope = self.make_envelope(self.fixture_bytes())
        if field == "schema":
            envelope = replace(envelope, schema_identity=label)
        elif field == "type":
            envelope = replace(
                envelope, concrete_type_identity=ResultObjectTypeIdentity(label)
            )
        elif field == "domain":
            envelope = replace(
                envelope, owning_domain_identity=ResultObjectDomainIdentity(label)
            )
        elif field == "identity":
            envelope = replace(envelope, result_identity=ResultObjectIdentity(label))
        else:
            envelope = replace(
                envelope, content_identity=ResultObjectContentIdentity(label)
            )
        result = QuantityOfInterestResultValueSerializer().decode(envelope)
        assert result.status == status
        assert result.value is None
        assert result.failure is not None and result.failure.code is code

    def test_method__encode__rejects_identity_only_protocol(self) -> None:
        """Evidence ID: SV-QOI-CODEC-007

        Requirement: Codec coverage must not silently widen to identity substitutes.

        Method: Supply an immutable synthetic implementation of only the protocol.

        Oracle: The two exact supported concrete families, not protocol membership.

        Acceptance: An identity-only result is incompatible with no envelope.

        Interpretation: Structural protocol conformance is not serializability.

        Limitations: This does not audit arbitrary third-party codec implementations.
        """

        @dataclass(frozen=True)
        class IdentityOnly:
            identity: ResultObjectIdentity

        result = QuantityOfInterestResultValueSerializer().encode(
            IdentityOnly(ResultObjectIdentity("synthetic-result"))
        )
        assert result.status == "incompatible"
        assert result.encoded is None
        assert result.failure is not None
        assert result.failure.code is WorkflowPersistenceFailureCode.UNSUPPORTED_TYPE

    def test_method__encode__distinguishes_same_identity_different_content(
        self,
    ) -> None:
        """Evidence ID: SV-QOI-CODEC-008

        Requirement: The complete content digest binds the scalar, not just identity.

        Method: Encode signed-zero variants with all nominal identities unchanged.

        Oracle: Binary64 signed-zero hex strings are distinct exact representations.

        Acceptance: Equal logical identities retain different bytes/content labels.

        Interpretation: A logical identity does not collapse distinct scalar values.

        Limitations: Aggregate-level repeated-occurrence checking is not implemented.
        """
        codec = QuantityOfInterestResultValueSerializer()
        first = codec.encode(self.make_value()).encoded
        second = codec.encode(replace(self.make_value(), value=0.0)).encoded
        assert first is not None and second is not None
        assert first.result_identity == second.result_identity
        assert first.payload != second.payload
        assert first.content_identity != second.content_identity

    def test_method__decode__retains_optional_definition_state(self) -> None:
        """Evidence ID: SV-QOI-CODEC-009

        Requirement: The codec preserves null fields and legal completeness variants.

        Method: Encode and decode an explicit alternate legal definition.

        Oracle: The independent complete input definition and optional-field contract.

        Acceptance: Null state and declared-subset completeness survive exactly.

        Interpretation: Optional state does not invent shared-state compatibility.

        Limitations: This is represented state preservation, not evaluator validation.
        """
        value = self.make_value()
        value = replace(
            value,
            quantity=replace(
                value.quantity,
                state_space_identity=None,
                completeness=QuantityOfInterestCompleteness.DECLARED_SUBSET,
            ),
        )
        codec = QuantityOfInterestResultValueSerializer()
        encoded = codec.encode(value).encoded
        assert encoded is not None
        result = codec.decode(encoded)
        assert result.status == "decoded"
        assert result.value == value

    def test_method__decode__reconstructs_independent_failure_wire(self) -> None:
        """Evidence ID: SV-QOI-CODEC-011

        Requirement: Complete failure values reconstruct without a scalar substitute.

        Method: Decode the authored failure fixture with an independently bound tag.

        Oracle: Literal result-failure-v1.json and exact input failure fields.

        Acceptance: Literal failure wire yields the independently declared failure.

        Interpretation: Failure reconstruction has an oracle independent of encoding.

        Limitations: Synthetic observation absence is not a calculated result.
        """
        payload = (
            Path(__file__)
            .with_name("resources")
            .joinpath("result-failure-v1.json")
            .read_bytes()
        )
        envelope = replace(
            self.make_envelope(payload),
            concrete_type_identity=ResultObjectTypeIdentity(
                "ksdft2effmass.analysis.ScalarQuantityOfInterestEvaluationFailure:1"
            ),
        )
        source = self.make_value()
        expected = ScalarQuantityOfInterestEvaluationFailure(
            source.identity,
            source.quantity,
            source.source_observation_set_result_identity,
            source.evaluator_identity,
            QuantityOfInterestEvaluationFailureCode.UNAVAILABLE,
            "synthetic unavailable observation",
        )
        result = QuantityOfInterestResultValueSerializer().decode(envelope)
        assert result.status == "decoded"
        assert type(result.value) is ScalarQuantityOfInterestEvaluationFailure
        assert result.value == expected

    def test_method__decode__rejects_unknown_closed_variant(self) -> None:
        """Evidence ID: SV-QOI-CODEC-013

        Requirement: A known scalar schema admits only its closed completeness enum.

        Method: Substitute an unknown enum label in an otherwise literal valid wire.

        Oracle: The two exact QuantityOfInterestCompleteness variants.

        Acceptance: Decode returns corrupt with no reconstructed value.

        Interpretation: Unknown enum labels are not silently mapped to a default.

        Limitations: This is a known-schema invariant, not a future schema parser.
        """
        envelope = self.make_envelope(
            self.fixture_bytes().replace(b'"complete"', b'"future-completeness"')
        )
        result = QuantityOfInterestResultValueSerializer().decode(envelope)
        assert result.status == "corrupt"
        assert result.value is None

    @staticmethod
    def raise_digest_error(payload: bytes) -> Never:
        raise RuntimeError("synthetic exception text must not escape")

    @staticmethod
    def raise_digest_limit(payload: bytes) -> Never:
        raise MemoryError("synthetic allocation limit must not escape")

    @pytest.mark.parametrize(
        "phase,limit,code",
        [
            pytest.param(
                "encode",
                False,
                WorkflowPersistenceFailureCode.CODEC_ERROR,
                id="encoding_operational_error",
            ),
            pytest.param(
                "decode",
                False,
                WorkflowPersistenceFailureCode.CODEC_ERROR,
                id="decoding_operational_error",
            ),
            pytest.param(
                "encode",
                True,
                WorkflowPersistenceFailureCode.REPRESENTATION_LIMIT,
                id="encoding_allocation_limit",
            ),
            pytest.param(
                "decode",
                True,
                WorkflowPersistenceFailureCode.REPRESENTATION_LIMIT,
                id="decoding_allocation_limit",
            ),
        ],
    )
    def test_method__codec__represents_sanitized_operational_failure(
        self,
        monkeypatch: pytest.MonkeyPatch,
        phase: str,
        limit: bool,
        code: WorkflowPersistenceFailureCode,
    ) -> None:
        """Evidence ID: SV-QOI-CODEC-012

        Requirement: Operational/representation errors are represented without payloads.

        Method: Replace the standard-library digest seam for one isolated operation.

        Oracle: Closed failure vocabulary and literal sanitized diagnostic contract.

        Acceptance: Error has the exact closed code and no value or exception text.

        Interpretation: Failed operations cannot return empty encoded/decoded success.

        Limitations: These are controlled local digest faults, not hardware failures.
        """
        envelope = self.make_envelope(self.fixture_bytes())
        value = self.make_value()
        monkeypatch.setattr(
            hashlib,
            "sha256",
            self.raise_digest_limit if limit else self.raise_digest_error,
        )
        codec = QuantityOfInterestResultValueSerializer()
        if phase == "encode":
            encoded = codec.encode(value)
            assert encoded.status == "error" and encoded.encoded is None
            failure = encoded.failure
        else:
            decoded = codec.decode(envelope)
            assert decoded.status == "error" and decoded.value is None
            failure = decoded.failure
        assert failure is not None and failure.code is code
        assert failure.phase == phase
        assert (
            failure.diagnostic == "scalar result codec did not produce a complete value"
        )
        assert "must not escape" not in repr(failure)

    def test_protocol__codec__is_immutable_explicit_dependency(self) -> None:
        """Evidence ID: SV-QOI-CODEC-010

        Requirement: The codec exposes no mutable dependency or ambient registry.

        Method: Check the public port and ordinary assignment on the serializer.

        Oracle: The explicit protocol and frozen dataclass language contract.

        Acceptance: Public codec satisfies the port and rejects field assignment.

        Interpretation: Composition can inject this stateless concrete serializer.

        Limitations: No application composer or complete Workflow repository exists.
        """
        codec = QuantityOfInterestResultValueSerializer()
        assert isinstance(codec, WorkflowResultValueCodec)
        with pytest.raises((FrozenInstanceError, TypeError, AttributeError)):
            codec.registry = ()  # type: ignore[attr-defined]
