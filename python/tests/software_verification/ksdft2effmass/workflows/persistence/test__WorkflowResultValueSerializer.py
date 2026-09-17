r"""Software verification of ``WorkflowResultValueSerializer``.

Bounded artifact scope: complete Workflow decision and normalized-set wires.

Evidence profile: claim_bearing

Facet and represented meaning

Synthetic decisions and ordered complete QE sources have fixed independent wires.
Opaque decision content labels retain their represented meaning, not a hash claim.

Intrinsic and cross-object scope

The serializer owns field closure, canonical bytes and nested envelope agreement;
source constructors and the injected QE owner retain neutral provenance invariants.

VVUQ and scientific exclusions

Software verification only, not decision authentication, scientific validity,
aggregate persistence, execution authority, numerical verification or acceptance.
"""

import hashlib
import json
from dataclasses import FrozenInstanceError, dataclass, replace
from pathlib import Path
from typing import Literal, cast
from unittest.mock import patch

import pytest
from ksdft2effmass.integration.quantum_espresso import (
    QuantumEspressoExtractedObservationResult,
    QuantumEspressoResultValueSerializer,
)
from ksdft2effmass.workflows import (
    ArtifactManifestEntryIdentity,
    AuthorityContextIdentity,
    BoundaryReceiptIdentity,
    NormalizedObservationSet,
    RepresentedScientificDecisionIngressProducer,
    ResponseSourceIdentity,
    ResultObjectContentIdentity,
    ResultObjectDomainIdentity,
    ResultObjectIdentity,
    ResultObjectTypeIdentity,
    ResultProducerProvenanceIdentity,
    ScientificDecisionOptionIdentity,
    ScientificDecisionRecorderIdentity,
    ScientificDecisionRequestIdentity,
    ScientificDecisionResolution,
    ScientificDecisionTransitionRecordIdentity,
    WorkflowEncodedResultValue,
    WorkflowIdentity,
    WorkflowPersistenceFailure,
    WorkflowPersistenceFailureCode,
    WorkflowResultValueCodec,
    WorkflowResultValueDecodeResult,
    WorkflowResultValueEncodeResult,
    WorkflowResultValueSerializer,
    WorkflowRunIdentity,
)

pytestmark = pytest.mark.software_verification
SUT = WorkflowResultValueSerializer
type JsonValue = None | bool | str | list[JsonValue] | dict[str, JsonValue]


class TestWorkflowResultValueSerializer:
    """One codec and its complete source-envelope boundary, without store effects."""

    @staticmethod
    def make_codec() -> WorkflowResultValueSerializer:
        return WorkflowResultValueSerializer(
            source_codec=QuantumEspressoResultValueSerializer()
        )

    @staticmethod
    def make_decision() -> ScientificDecisionResolution:
        return ScientificDecisionResolution(
            identity=ResultObjectIdentity("decision-correction"),
            content_identity=ResultObjectContentIdentity("opaque:historical-content"),
            request_identity=ScientificDecisionRequestIdentity("request"),
            verbatim_response="  yes — retain\nverbatim\tΩ  ",
            normalized_option_identity=ScientificDecisionOptionIdentity("option-yes"),
            response_source_identity=ResponseSourceIdentity("source"),
            authority_context_identity=AuthorityContextIdentity("context"),
            boundary_receipt_identity=BoundaryReceiptIdentity("boundary-receipt"),
            predecessor_resolution_identity=ResultObjectIdentity("decision-initial"),
            supersedes_resolution_identity=ResultObjectIdentity("decision-initial"),
            producer_provenance=RepresentedScientificDecisionIngressProducer(
                identity=ResultProducerProvenanceIdentity("producer"),
                workflow_identity=WorkflowIdentity("workflow"),
                workflow_run_identity=WorkflowRunIdentity("run"),
                request_identity=ScientificDecisionRequestIdentity("request"),
                transition_record_identity=ScientificDecisionTransitionRecordIdentity(
                    "transition"
                ),
                recorder_identity=ScientificDecisionRecorderIdentity("recorder:7"),
                response_source_identity=ResponseSourceIdentity("source"),
                authority_context_identity=AuthorityContextIdentity("context"),
                resolution_identity=ResultObjectIdentity("decision-correction"),
            ),
        )

    @staticmethod
    def fixture_bytes(name: str) -> bytes:
        return Path(__file__).with_name("resources").joinpath(name).read_bytes()

    @staticmethod
    def make_envelope(
        payload: bytes, family: str = "ScientificDecisionResolution"
    ) -> WorkflowEncodedResultValue:
        digest = hashlib.sha256(payload).hexdigest()
        return WorkflowEncodedResultValue(
            result_identity=ResultObjectIdentity(
                "decision-correction"
                if family == "ScientificDecisionResolution"
                else "observation-set"
            ),
            concrete_type_identity=ResultObjectTypeIdentity(
                f"ksdft2effmass.workflows.{family}:1"
            ),
            owning_domain_identity=ResultObjectDomainIdentity(
                "ksdft2effmass.workflows"
            ),
            schema_identity="workflow-result:1",
            content_identity=ResultObjectContentIdentity(
                "opaque:historical-content"
                if family == "ScientificDecisionResolution"
                else f"workflow-result:1:sha256:{digest}"
            ),
            payload=payload,
            payload_digest=digest,
        )

    @staticmethod
    def make_source() -> QuantumEspressoExtractedObservationResult:
        payload = (
            Path(__file__)
            .parents[2]
            .joinpath(
                "integration/quantum_espresso/resources/result-observation-v1.json"
            )
            .read_bytes()
        )
        digest = hashlib.sha256(payload).hexdigest()
        decoded = QuantumEspressoResultValueSerializer().decode(
            WorkflowEncodedResultValue(
                result_identity=ResultObjectIdentity("synthetic-result"),
                concrete_type_identity=ResultObjectTypeIdentity(
                    "ksdft2effmass.integration.quantum_espresso.QuantumEspressoExtractedObservationResult:1"
                ),
                owning_domain_identity=ResultObjectDomainIdentity(
                    "ksdft2effmass.integration.quantum_espresso"
                ),
                schema_identity="qe-result-value:1",
                content_identity=ResultObjectContentIdentity(
                    f"qe-result-value:1:sha256:{digest}"
                ),
                payload=payload,
                payload_digest=digest,
            )
        )
        assert type(decoded.value) is QuantumEspressoExtractedObservationResult
        return decoded.value

    def make_set(self) -> NormalizedObservationSet:
        source = self.make_source()
        return NormalizedObservationSet(
            identity=ResultObjectIdentity("observation-set"),
            sources=(
                replace(
                    source,
                    identity=ResultObjectIdentity("source-z"),
                    source_manifest_entry_identity=ArtifactManifestEntryIdentity(
                        "entry-z"
                    ),
                ),
                replace(
                    source,
                    identity=ResultObjectIdentity("source-a"),
                    source_manifest_entry_identity=ArtifactManifestEntryIdentity(
                        "entry-a"
                    ),
                ),
            ),
        )

    def test_method__encode__matches_complete_decision_literal(self) -> None:
        """Evidence ID: SV-WORKFLOW-RESULT-CODEC-001

        Requirement: Every decision field and opaque content label survives encoding.

        Method: Compare separately constructed correction against hand-authored bytes.

        Oracle: result-decision-v1.json fixes all eleven fields and complete producer.

        Acceptance: Exact complete envelope equals the independent expected envelope.

        Interpretation: No response normalization or historical hash reinterpretation.

        Limitations: Synthetic represented decisions are not authenticated responses.
        """
        result = self.make_codec().encode(self.make_decision())
        assert result.status == "encoded"
        assert result.encoded == self.make_envelope(
            self.fixture_bytes("result-decision-v1.json")
        )

    def test_method__decode__reconstructs_complete_decision_literal(self) -> None:
        """Evidence ID: SV-WORKFLOW-RESULT-CODEC-002

        Requirement: Decision decoding restores the exact complete immutable record.

        Method: Decode independent literal bytes and compare independent constructors.

        Oracle: Explicit correction fields including Unicode, whitespace and provenance.

        Acceptance: Exact concrete type and every field equal the independently
        built record.

        Interpretation: Decoder does not rely on an encode-generated oracle.

        Limitations: Constructor agreement establishes no scientific decision authority.
        """
        decoded = self.make_codec().decode(
            self.make_envelope(self.fixture_bytes("result-decision-v1.json"))
        )
        assert decoded.status == "decoded"
        assert type(decoded.value) is ScientificDecisionResolution
        assert decoded.value == self.make_decision()

    def test_method__encode__retains_absent_correction_fields(self) -> None:
        """Evidence ID: SV-WORKFLOW-RESULT-CODEC-003

        Requirement: Initial resolutions retain all three explicit null fields.

        Method: Encode a constructor-defined initial decision and compare fixed
        null substitutions.

        Oracle: Independent correction literal with receipt and both predecessor
        tags replaced by null.

        Acceptance: Exact payload and independently constructed decoded initial
        record agree.

        Interpretation: Nulls are represented, never omitted or inferred.

        Limitations: This does not validate a request or transition history.
        """
        value = replace(
            self.make_decision(),
            boundary_receipt_identity=None,
            predecessor_resolution_identity=None,
            supersedes_resolution_identity=None,
        )
        payload = (
            self.fixture_bytes("result-decision-v1.json")
            .replace(
                b'{"fields":{"value":"boundary-receipt"},"type":"BoundaryReceiptIdentity"}',
                b"null",
            )
            .replace(
                b'{"fields":{"value":"decision-initial"},"type":"ResultObjectIdentity"}',
                b"null",
            )
        )
        encoded = self.make_codec().encode(value)
        assert encoded.encoded == self.make_envelope(payload)
        assert self.make_codec().decode(self.make_envelope(payload)).value == value

    def test_method__encode__matches_ordered_nested_source_literal(self) -> None:
        """Evidence ID: SV-WORKFLOW-RESULT-CODEC-004

        Requirement: Normalized sets contain every complete ordered source envelope.

        Method: Encode two actual QE sources with reversed lexical identity order.

        Oracle: Independently authored result-observation-set-v1.json embeds
        fixed QE bytes.

        Acceptance: Exact set envelope and bytes match the literal without
        sorting sources.

        Interpretation: Source bytes, digest, type, schema, domain and content
        remain present.

        Limitations: QE input is synthetic neutral data, not a native calculation.
        """
        encoded = self.make_codec().encode(self.make_set())
        assert encoded.status == "encoded"
        assert encoded.encoded == self.make_envelope(
            self.fixture_bytes("result-observation-set-v1.json"),
            "NormalizedObservationSet",
        )

    def test_method__decode__retains_concrete_nested_provenance(self) -> None:
        """Evidence ID: SV-WORKFLOW-RESULT-CODEC-005

        Requirement: Set decoding restores exact concrete sources and unchanged
        neutral content.

        Method: Decode the independently composed literal and inspect sources
        through public fields.

        Oracle: Fixed source-z/source-a order, entry labels and the literal QE
        source record.

        Acceptance: Both exact source types, ordered identities, provenance and
        neutral values agree.

        Interpretation: No identity-only or anonymous protocol adapter replaces
        a source.

        Limitations: QE codec owns its internal complete field and precision evidence.
        """
        decoded = self.make_codec().decode(
            self.make_envelope(
                self.fixture_bytes("result-observation-set-v1.json"),
                "NormalizedObservationSet",
            )
        )
        assert decoded.status == "decoded"
        assert type(decoded.value) is NormalizedObservationSet
        first, second = decoded.value.sources
        assert type(first) is QuantumEspressoExtractedObservationResult
        assert type(second) is QuantumEspressoExtractedObservationResult
        assert (first.identity.value, second.identity.value) == ("source-z", "source-a")
        assert (
            first.source_manifest_entry_identity.value,
            second.source_manifest_entry_identity.value,
        ) == ("entry-z", "entry-a")
        original = self.make_source()
        assert first.observation == original.observation
        assert second.observation == original.observation
        assert first.normalization_policy == original.normalization_policy
        assert first.parser_identity == original.parser_identity
        assert first.parsed_document_identity == original.parsed_document_identity
        assert first.source_content_identity == original.source_content_identity
        assert first.limitation_values == original.limitation_values

    @pytest.mark.parametrize(
        "payload",
        [
            pytest.param(
                b'{"fields":{},"type":"ScientificDecisionResolution"}',
                id="missing_fields",
            ),
            pytest.param(
                b'{"fields":{},"fields":{},"type":"ScientificDecisionResolution"}',
                id="duplicate_members",
            ),
            pytest.param(b"1", id="raw_number"),
            pytest.param(b"NaN", id="nonfinite_token"),
            pytest.param(b"\xff", id="non_ascii"),
        ],
    )
    def test_method__decode__rejects_malformed_wire(self, payload: bytes) -> None:
        """Evidence ID: SV-WORKFLOW-RESULT-CODEC-006

        Requirement: Invalid known representations never become complete decisions.

        Method: Decode explicitly byte-bound grammar violations.

        Oracle: Closed record grammar requires unique complete fields and ASCII
        tagged values.

        Acceptance: Corrupt outcome contains failure and no value for every case.

        Interpretation: Byte digest agreement alone is insufficient for reconstruction.

        Limitations: Cases establish grammar rejection, not hostile-input
        resource bounds.
        """
        decoded = self.make_codec().decode(self.make_envelope(payload))
        assert decoded.status == "corrupt"
        assert decoded.value is None
        assert decoded.failure is not None
        assert (
            decoded.failure.code
            == WorkflowPersistenceFailureCode.MALFORMED_REPRESENTATION
        )

    @pytest.mark.parametrize(
        "old,new",
        [
            pytest.param(
                b'"verbatim_response":',
                b'"extra":null,"verbatim_response":',
                id="extra_field",
            ),
            pytest.param(b'"recorder:7"', b'""', id="empty_producer_label"),
            pytest.param(
                b'"supersedes_resolution_identity":{"fields":{"value":"decision-initial"}',
                b'"supersedes_resolution_identity":{"fields":{"value":"other"}',
                id="detached_predecessor",
            ),
            pytest.param(
                b'"resolution_identity":{"fields":{"value":"decision-correction"}',
                b'"resolution_identity":{"fields":{"value":"other"}',
                id="detached_producer",
            ),
            pytest.param(
                b'"type":"BoundaryReceiptIdentity"',
                b'"type":"ResultObjectIdentity"',
                id="wrong_nominal_tag",
            ),
            pytest.param(b'"fields":{', b'"fields": {', id="noncanonical_spacing"),
        ],
    )
    def test_method__decode__rejects_decision_field_faults(
        self, old: bytes, new: bytes
    ) -> None:
        """Evidence ID: SV-WORKFLOW-RESULT-CODEC-007

        Requirement: Complete decision field grammar and constructor invariants
        remain binding.

        Method: Apply explicit independent single-facet mutations to the literal
        payload.

        Oracle: Exact nominal tags, correlated producer and equal
        predecessor/supersession contract.

        Acceptance: Every mutation yields corrupt without a partial record.

        Interpretation: Canonical and intrinsic checks are applied on reconstruction.

        Limitations: Aggregate references and request-option membership are
        outside this codec.
        """
        payload = self.fixture_bytes("result-decision-v1.json")
        assert old in payload
        decoded = self.make_codec().decode(
            self.make_envelope(payload.replace(old, new, 1))
        )
        assert decoded.status == "corrupt"
        assert decoded.value is None

    @pytest.mark.parametrize(
        "field",
        [
            pytest.param("identity", id="detached_result_identity"),
            pytest.param("domain", id="detached_domain"),
            pytest.param("content", id="detached_opaque_content"),
        ],
    )
    def test_method__decode__rejects_detached_envelope(self, field: str) -> None:
        """Evidence ID: SV-WORKFLOW-RESULT-CODEC-008

        Requirement: Envelope metadata must agree with complete decoded content.

        Method: Replace one nominal envelope label while retaining exact payload digest.

        Oracle: Literal decision identity/domain/content labels fix binding
        independently.

        Acceptance: Corrupt outcome carries no value for each detached metadata field.

        Interpretation: An opaque content label is compared, not recomputed as a hash.

        Limitations: Digests do not authenticate historical provenance statements.
        """
        envelope = self.make_envelope(self.fixture_bytes("result-decision-v1.json"))
        if field == "identity":
            envelope = replace(envelope, result_identity=ResultObjectIdentity("other"))
        elif field == "domain":
            envelope = replace(
                envelope, owning_domain_identity=ResultObjectDomainIdentity("other")
            )
        else:
            envelope = replace(
                envelope, content_identity=ResultObjectContentIdentity("other")
            )
        decoded = self.make_codec().decode(envelope)
        assert decoded.status == "corrupt"
        assert decoded.value is None

    @pytest.mark.parametrize(
        "field",
        [
            pytest.param("schema", id="future_wire_schema"),
            pytest.param("type", id="future_concrete_type"),
        ],
    )
    def test_method__decode__rejects_unknown_versions(self, field: str) -> None:
        """Evidence ID: SV-WORKFLOW-RESULT-CODEC-009

        Requirement: Unknown schemas and concrete type versions remain incompatible.

        Method: Replace a known envelope's schema or concrete type version.

        Oracle: Only workflow-result:1 and the two explicit version-one labels
        are supported.

        Acceptance: Incompatible outcome contains failure and no reconstructed value.

        Interpretation: No dynamic discovery or legacy inference occurs.

        Limitations: Future implementations require an explicitly revised contract.
        """
        envelope = self.make_envelope(self.fixture_bytes("result-decision-v1.json"))
        envelope = (
            replace(envelope, schema_identity="workflow-result:2")
            if field == "schema"
            else replace(
                envelope,
                concrete_type_identity=ResultObjectTypeIdentity(
                    "ksdft2effmass.workflows.ScientificDecisionResolution:2"
                ),
            )
        )
        decoded = self.make_codec().decode(envelope)
        assert decoded.status == "incompatible"
        assert decoded.value is None

    @pytest.mark.parametrize(
        "fault",
        [
            pytest.param("identity", id="detached_nested_identity"),
            pytest.param("digest", id="detached_nested_digest"),
            pytest.param("base64", id="noncanonical_nested_bytes"),
            pytest.param("duplicate", id="duplicate_source_identity"),
            pytest.param("empty", id="empty_source_set"),
        ],
    )
    def test_method__decode__rejects_nested_envelope_faults(self, fault: str) -> None:
        """Evidence ID: SV-WORKFLOW-RESULT-CODEC-010

        Requirement: Complete nested envelopes and source membership must agree.

        Method: Mutate a literal source envelope or its ordered membership
        before decoding.

        Oracle: Exact base64/digest and unique nonempty source contracts.

        Acceptance: Every malformed nested value is corrupt without a result.

        Interpretation: Outer rehashing cannot bless a malformed or detached
        nested envelope.

        Limitations: This is source closure, not full WorkflowRun
        repeated-occurrence validation.
        """
        wire = cast(
            dict[str, JsonValue],
            json.loads(self.fixture_bytes("result-observation-set-v1.json")),
        )
        fields = wire["fields"]
        assert isinstance(fields, dict)
        sources = fields["sources"]
        assert isinstance(sources, list)
        first = sources[0]
        assert isinstance(first, dict)
        nested = first["fields"]
        assert isinstance(nested, dict)
        if fault == "identity":
            nested["result_identity"] = {
                "type": "ResultObjectIdentity",
                "fields": {"value": "detached"},
            }
        elif fault == "digest":
            nested["payload_digest"] = "0" * 64
        elif fault == "base64":
            nested["payload"] = {"type": "bytes", "fields": {"value": "Zh=="}}
        elif fault == "duplicate":
            sources[1] = sources[0]
        else:
            fields["sources"] = []
        payload = json.dumps(
            wire, ensure_ascii=True, sort_keys=True, separators=(",", ":")
        ).encode("ascii")
        decoded = self.make_codec().decode(
            self.make_envelope(payload, "NormalizedObservationSet")
        )
        assert decoded.status == "corrupt"
        assert decoded.value is None

    def test_method__decode__retains_nested_version_incompatibility(self) -> None:
        """Evidence ID: SV-WORKFLOW-RESULT-CODEC-017

        Requirement: Unsupported nested schemas remain incompatible at the set boundary.

        Method: Substitute a future source schema in the literal complete set.

        Oracle: Only qe-result-value:1 is supported by the actual injected source owner.

        Acceptance: Incompatible failure retains the source owner and no set value.

        Interpretation: An outer supported schema cannot mask nested incompatibility.

        Limitations: No future-schema migration is selected or attempted.
        """
        payload = self.fixture_bytes("result-observation-set-v1.json").replace(
            b'"schema_identity":"qe-result-value:1"',
            b'"schema_identity":"qe-result-value:2"',
            1,
        )
        decoded = self.make_codec().decode(
            self.make_envelope(payload, "NormalizedObservationSet")
        )
        assert decoded.status == "incompatible"
        assert decoded.value is None
        assert decoded.failure is not None
        assert (
            decoded.failure.code == WorkflowPersistenceFailureCode.UNSUPPORTED_VERSION
        )
        assert decoded.failure.implementation_identity == (
            "ksdft2effmass.integration.quantum_espresso."
            "QuantumEspressoResultValueSerializer:1"
        )

    def test_method__decode__checks_source_reencoding_agreement(self) -> None:
        """Evidence ID: SV-WORKFLOW-RESULT-CODEC-011

        Requirement: A nested decode success must re-encode to the exact
        original envelope.

        Method: Substitute an actual source with equal identity but different
        parsed-document provenance.

        Oracle: Literal source bytes bind the original document label, not
        identity alone.

        Acceptance: Corrupt content mismatch has no set value despite successful
        source decoding.

        Interpretation: Codec return-value substitution cannot silently change
        represented content.

        Limitations: This controlled collaborator fault does not claim arbitrary
        codec authentication.
        """
        source = self.make_set().sources[0]
        assert type(source) is QuantumEspressoExtractedObservationResult
        altered = replace(
            source,
            parser_version="1",
            parsed_document_identity=type(source.parsed_document_identity)(
                "different-document"
            ),
        )
        with patch.object(
            QuantumEspressoResultValueSerializer,
            "decode",
            return_value=WorkflowResultValueDecodeResult(
                status="decoded", value=altered
            ),
        ):
            decoded = self.make_codec().decode(
                self.make_envelope(
                    self.fixture_bytes("result-observation-set-v1.json"),
                    "NormalizedObservationSet",
                )
            )
        assert decoded.status == "corrupt"
        assert decoded.value is None
        assert decoded.failure is not None
        assert decoded.failure.code == WorkflowPersistenceFailureCode.CONTENT_MISMATCH

    def test_method__encode__rejects_identity_only_standins(self) -> None:
        """Evidence ID: SV-WORKFLOW-RESULT-CODEC-012

        Requirement: Protocol identity alone and subclasses do not establish
        codec support.

        Method: Encode a local identity-only result and a decision subclass.

        Oracle: The selected codec admits exact classes only.

        Acceptance: Both return incompatible without an encoded envelope.

        Interpretation: No arbitrary ResultObject or subclass reconstruction is
        promised.

        Limitations: Unsupported future families require separate owning
        implementations.
        """

        @dataclass(frozen=True)
        class IdentityOnly:
            identity: ResultObjectIdentity

        class DecisionSubclass(ScientificDecisionResolution):
            pass

        assert (
            self.make_codec()
            .encode(IdentityOnly(ResultObjectIdentity("standin")))
            .status
            == "incompatible"
        )
        decision = self.make_decision()
        value = DecisionSubclass(
            identity=decision.identity,
            content_identity=decision.content_identity,
            request_identity=decision.request_identity,
            verbatim_response=decision.verbatim_response,
            normalized_option_identity=decision.normalized_option_identity,
            response_source_identity=decision.response_source_identity,
            authority_context_identity=decision.authority_context_identity,
            boundary_receipt_identity=decision.boundary_receipt_identity,
            predecessor_resolution_identity=decision.predecessor_resolution_identity,
            supersedes_resolution_identity=decision.supersedes_resolution_identity,
            producer_provenance=decision.producer_provenance,
        )
        assert self.make_codec().encode(value).status == "incompatible"

    def test_field__dependencies__remain_immutable(self) -> None:
        """Evidence ID: SV-WORKFLOW-RESULT-CODEC-013

        Requirement: Codec binding and reconstructed nested state remain
        operationally immutable.

        Method: Attempt ordinary mutation of the codec, decision and retained
        set sources.

        Oracle: Frozen dataclass and tuple contracts reject mutation through
        public state.

        Acceptance: Assignments fail and source observations remain unchanged.

        Interpretation: Serialization does not introduce mutable result wrappers
        or caches.

        Limitations: Deliberate low-level Python object mutation is outside
        ordinary APIs.
        """
        codec = self.make_codec()
        assert isinstance(codec, WorkflowResultValueCodec)
        with pytest.raises(FrozenInstanceError):
            codec.source_codec = QuantumEspressoResultValueSerializer()  # type: ignore[misc]
        decoded = codec.decode(
            self.make_envelope(self.fixture_bytes("result-decision-v1.json"))
        )
        assert type(decoded.value) is ScientificDecisionResolution
        with pytest.raises(FrozenInstanceError):
            decoded.value.verbatim_response = "changed"  # type: ignore[misc]
        normalized = codec.decode(
            self.make_envelope(
                self.fixture_bytes("result-observation-set-v1.json"),
                "NormalizedObservationSet",
            )
        )
        assert type(normalized.value) is NormalizedObservationSet
        with pytest.raises(FrozenInstanceError):
            normalized.value.sources = ()  # type: ignore[misc]

    @pytest.mark.parametrize(
        "error",
        [
            pytest.param(MemoryError("private"), id="allocation_limit"),
            pytest.param(RuntimeError("private"), id="operational_error"),
        ],
    )
    def test_method__decode__sanitizes_operational_failures(
        self, error: MemoryError | RuntimeError
    ) -> None:
        """Evidence ID: SV-WORKFLOW-RESULT-CODEC-014

        Requirement: Codec operational failures are closed sanitized errors
        without partial values.

        Method: Inject allocation or operational failure at the JSON decoding boundary.

        Oracle: Operational errors differ from corrupt data and never copy
        exception details.

        Acceptance: Error status, no value and sanitized diagnostic for each fault.

        Interpretation: Representation failure does not create a successful
        empty result.

        Limitations: Controlled exceptions do not establish actual resource
        exhaustion bounds.
        """
        with patch.object(json, "loads", side_effect=error):
            decoded = self.make_codec().decode(
                self.make_envelope(self.fixture_bytes("result-decision-v1.json"))
            )
        assert decoded.status == "error"
        assert decoded.value is None
        assert decoded.failure is not None
        assert "private" not in decoded.failure.diagnostic

    @pytest.mark.parametrize(
        "status,code",
        [
            pytest.param(
                "incompatible",
                WorkflowPersistenceFailureCode.UNSUPPORTED_VERSION,
                id="unsupported_source_version",
            ),
            pytest.param(
                "invalid",
                WorkflowPersistenceFailureCode.INVARIANT_VIOLATION,
                id="invalid_source_value",
            ),
            pytest.param(
                "error",
                WorkflowPersistenceFailureCode.CODEC_ERROR,
                id="source_operation_error",
            ),
        ],
    )
    def test_method__encode__preserves_nested_failure_evidence(
        self,
        status: Literal["incompatible", "invalid", "error"],
        code: WorkflowPersistenceFailureCode,
    ) -> None:
        """Evidence ID: SV-WORKFLOW-RESULT-CODEC-015

        Requirement: Nested failure diagnostics survive without a partial source
        set envelope.

        Method: Supply each closed nonsuccess QE source encode outcome.

        Oracle: Exact injected failure record, including implementation and
        input identity.

        Acceptance: Exact source status and full failure return without an envelope.

        Interpretation: Workflow composition does not hide source-domain
        incompatibility.

        Limitations: This represents a collaborator failure rather than a
        scientific conclusion.
        """
        value = self.make_set()
        failure = WorkflowPersistenceFailure(
            implementation_identity="synthetic-source:1",
            phase="encode",
            code=code,
            input_identities=("source-z",),
            expected="supported source",
            observed="unknown version",
            diagnostic="source incompatible",
            claim_boundary="software only",
        )
        with patch.object(
            QuantumEspressoResultValueSerializer,
            "encode",
            return_value=WorkflowResultValueEncodeResult(
                status=status, failure=failure
            ),
        ):
            result = self.make_codec().encode(value)
        assert result.status == status
        assert result.failure is failure
        assert result.encoded is None

    @pytest.mark.parametrize(
        "invalid",
        [
            pytest.param(None, id="null"),
            pytest.param("wire", id="text"),
            pytest.param(True, id="boolean"),
        ],
    )
    def test_method__codec__rejects_wrong_direct_types(
        self, invalid: None | str | bool
    ) -> None:
        """Evidence ID: SV-WORKFLOW-RESULT-CODEC-016

        Requirement: Wrong semantic direct API types raise TypeError, not
        represented success.

        Method: Call the constructor and both codec operations with closed
        invalid inputs.

        Oracle: Exact port, ResultObject identity and envelope Python contracts.

        Acceptance: Each direct misuse raises TypeError without coercion.

        Interpretation: Wire strings are not silently accepted as domain inputs.

        Limitations: Invalid types are intentionally isolated at suppressed call sites.
        """
        with pytest.raises(TypeError):
            WorkflowResultValueSerializer(source_codec=invalid)  # type: ignore[arg-type]
        with pytest.raises(TypeError):
            self.make_codec().encode(invalid)  # type: ignore[arg-type]
        with pytest.raises(TypeError):
            self.make_codec().decode(invalid)  # type: ignore[arg-type]

    def test_method__encode__rejects_nested_source_subclass(self) -> None:
        """Evidence ID: SV-WORKFLOW-RESULT-CODEC-018

        Requirement: Source protocol membership does not extend exact codec support.

        Method: Retain a constructor-valid QE subclass in a normalized set.

        Oracle: Actual QE codec supports its exact extracted-result class only.

        Acceptance: Set encode is incompatible and contains no partial envelope.

        Interpretation: Inward Workflow code delegates concrete support outward.

        Limitations: This does not claim arbitrary protocols are immutable.
        """

        class SourceSubclass(QuantumEspressoExtractedObservationResult):
            pass

        source = self.make_source()
        subclass = SourceSubclass(
            identity=source.identity,
            observation=source.observation,
            source_manifest_identity=source.source_manifest_identity,
            source_manifest_entry_identity=source.source_manifest_entry_identity,
            source_artifact_identity=source.source_artifact_identity,
            source_content_identity=source.source_content_identity,
            source_producer_provenance_identity=source.source_producer_provenance_identity,
            parsed_document_identity=source.parsed_document_identity,
            parser_identity=source.parser_identity,
            parser_version=source.parser_version,
            normalization_policy=source.normalization_policy,
            limitation_values=source.limitation_values,
        )
        value = NormalizedObservationSet(
            identity=ResultObjectIdentity("set"), sources=(subclass,)
        )
        result = self.make_codec().encode(value)
        assert result.status == "incompatible"
        assert result.encoded is None

    @pytest.mark.parametrize(
        "error",
        [
            pytest.param(MemoryError("private"), id="allocation_limit"),
            pytest.param(RuntimeError("private"), id="operation_failure"),
        ],
    )
    def test_method__encode__sanitizes_operational_failures(
        self, error: MemoryError | RuntimeError
    ) -> None:
        """Evidence ID: SV-WORKFLOW-RESULT-CODEC-019

        Requirement: Failed encode operations never produce partial envelopes.

        Method: Inject allocation and operational exceptions at JSON encoding.

        Oracle: Errors remain distinct from invalid values and omit exception text.

        Acceptance: Error with no envelope and a sanitized diagnostic in both cases.

        Interpretation: No successful empty value masks an encoding failure.

        Limitations: Controlled faults do not measure actual resource limits.
        """
        with patch.object(json, "dumps", side_effect=error):
            result = self.make_codec().encode(self.make_decision())
        assert result.status == "error"
        assert result.encoded is None
        assert result.failure is not None
        assert "private" not in result.failure.diagnostic

    @pytest.mark.parametrize(
        "status,code",
        [
            pytest.param(
                "incompatible",
                WorkflowPersistenceFailureCode.UNSUPPORTED_VERSION,
                id="source_incompatible",
            ),
            pytest.param(
                "corrupt",
                WorkflowPersistenceFailureCode.MALFORMED_REPRESENTATION,
                id="source_corrupt",
            ),
            pytest.param(
                "error", WorkflowPersistenceFailureCode.CODEC_ERROR, id="source_error"
            ),
        ],
    )
    def test_method__decode__preserves_nested_failure_evidence(
        self,
        status: Literal["incompatible", "corrupt", "error"],
        code: WorkflowPersistenceFailureCode,
    ) -> None:
        """Evidence ID: SV-WORKFLOW-RESULT-CODEC-020

        Requirement: Closed source decode failures remain explicit through Workflow.

        Method: Inject each source nonsuccess result into a valid set decode.

        Oracle: Independently constructed status and complete source diagnostic.

        Acceptance: Exact status and same failure survive without a set value.

        Interpretation: Nested failure is not converted into a partial success.

        Limitations: Synthetic collaborator faults establish software behavior only.
        """
        failure = WorkflowPersistenceFailure(
            implementation_identity="synthetic-source:1",
            phase="decode",
            code=code,
            input_identities=("source-z",),
            expected="complete source",
            observed=status,
            diagnostic="source did not decode",
            claim_boundary="software only",
        )
        with patch.object(
            QuantumEspressoResultValueSerializer,
            "decode",
            return_value=WorkflowResultValueDecodeResult(
                status=status, failure=failure
            ),
        ):
            result = self.make_codec().decode(
                self.make_envelope(
                    self.fixture_bytes("result-observation-set-v1.json"),
                    "NormalizedObservationSet",
                )
            )
        assert result.status == status
        assert result.failure is failure
        assert result.value is None

    def test_method__encode__binds_opaque_label_and_changed_response(self) -> None:
        """Evidence ID: SV-WORKFLOW-RESULT-CODEC-021

        Requirement: Equal opaque labels cannot hide different represented responses.

        Method: Encode a changed response under the same result and content identities.

        Oracle: Original literal payload independently fixes the original response.

        Acceptance: Labels agree but exact bytes and payload digests differ.

        Interpretation: Opaque content is preserved; separate byte binding is required.

        Limitations: Future aggregate checks must reject the conflicting pair.
        """
        codec = self.make_codec()
        original = self.make_envelope(self.fixture_bytes("result-decision-v1.json"))
        altered = codec.encode(replace(self.make_decision(), verbatim_response="no"))
        assert altered.encoded is not None
        assert altered.encoded.result_identity == original.result_identity
        assert altered.encoded.content_identity == original.content_identity
        assert altered.encoded.payload != original.payload
        assert altered.encoded.payload_digest != original.payload_digest
