"""Canonical workflow-owned result-value serialization."""

from __future__ import annotations

import base64
import hashlib
import json
from dataclasses import dataclass
from typing import Literal, Never, cast

from ...model import (
    ResultObject,
    ResultObjectIdentity,
    WorkflowIdentity,
    WorkflowRunIdentity,
)
from ...observations import NormalizedObservationSet, NormalizedObservationSource
from ...runs.identities import (
    AuthorityContextIdentity,
    BoundaryReceiptIdentity,
    ResponseSourceIdentity,
    ResultObjectContentIdentity,
    ResultObjectDomainIdentity,
    ResultObjectTypeIdentity,
    ResultProducerProvenanceIdentity,
    ScientificDecisionOptionIdentity,
    ScientificDecisionRecorderIdentity,
    ScientificDecisionRequestIdentity,
    ScientificDecisionTransitionRecordIdentity,
)
from ...runs.records import (
    RepresentedScientificDecisionIngressProducer,
    ScientificDecisionResolution,
)
from ..records import (
    WorkflowEncodedResultValue,
    WorkflowPersistenceFailure,
    WorkflowPersistenceFailureCode,
    WorkflowResultValueCodec,
    WorkflowResultValueDecodeResult,
    WorkflowResultValueEncodeResult,
)

type _ResultJson = None | bool | str | list[_ResultJson] | dict[str, _ResultJson]
type _WorkflowValue = ScientificDecisionResolution | NormalizedObservationSet


class _WorkflowSourceCodecFailure(Exception):
    """Carry a complete nested codec failure across local wire traversal only."""

    def __init__(
        self,
        failure: WorkflowPersistenceFailure,
        status: Literal["incompatible", "invalid", "corrupt", "error"] = "corrupt",
    ) -> None:
        super().__init__("nested source codec did not produce a complete value")
        self.failure = failure
        self.status = status


@dataclass(frozen=True, slots=True, kw_only=True)
class WorkflowResultValueSerializer:
    """Lossless version-one codec for two exact Workflow-owned result families.

    Parameters
    ----------
    source_codec
        Explicit effect-free, operationally immutable source codec implementing
        ``WorkflowResultValueCodec``. Application composition supplies the QE codec.
        It must support only exact concrete sources, never protocol stand-ins.
        The dependency is retained without a registry, discovery or inward import.

    Notes
    -----
    ``workflow-result:1`` uses canonical sorted compact ASCII JSON without newline,
    explicit ``type``/``fields`` records and nominal tags. Decisions retain every
    field, including verbatim Unicode response and opaque owning content identity;
    that label is compared, not reinterpreted as a hash. Sets retain ordered complete
    source envelopes with canonical base64 payload bytes. Their content identity is
    ``workflow-result:1:sha256:<digest>`` over the complete payload. A separate SHA-256
    digest always binds bytes. Nested decode/re-encode must agree on every envelope
    field. Unknown schemas/types are incompatible; invalid known wire is corrupt.
    No native I/O, scientific transformation, authority interpretation or replay occurs.
    This codec does not serialize a complete WorkflowRun or retain an identity cache.

    Raises
    ------
    TypeError
        ``source_codec`` does not implement the explicit codec port.
    """

    source_codec: WorkflowResultValueCodec

    def __post_init__(self) -> None:
        """Require the explicit source port without discovering its implementation."""
        if not isinstance(self.source_codec, WorkflowResultValueCodec):
            raise TypeError("source_codec must implement WorkflowResultValueCodec")

    def encode(self, value: ResultObject) -> WorkflowResultValueEncodeResult:
        """Encode a complete decision or normalized set with exact source envelopes.

        Parameters
        ----------
        value
            Workflow-facing result; only the two exact supported classes encode.

        Returns
        -------
        WorkflowResultValueEncodeResult
            Complete envelope or incompatible/invalid/error without a partial value.
            Nested codec failures retain their complete diagnostic evidence.

        Raises
        ------
        TypeError
            Input does not expose an exact nominal ResultObject identity.
        """
        if (
            not isinstance(value, ResultObject)
            or type(value.identity) is not ResultObjectIdentity
        ):
            raise TypeError("value must expose an exact ResultObjectIdentity")
        if (
            type(value) is not ScientificDecisionResolution
            and type(value) is not NormalizedObservationSet
        ):
            return WorkflowResultValueEncodeResult(
                status="incompatible",
                failure=self._failure(
                    "encode",
                    WorkflowPersistenceFailureCode.UNSUPPORTED_TYPE,
                    (value.identity.value,),
                ),
            )
        try:
            payload = self._payload(value)
            digest = hashlib.sha256(payload).hexdigest()
            tag = (
                "ScientificDecisionResolution"
                if type(value) is ScientificDecisionResolution
                else "NormalizedObservationSet"
            )
            content = (
                value.content_identity
                if type(value) is ScientificDecisionResolution
                else ResultObjectContentIdentity(f"workflow-result:1:sha256:{digest}")
            )
            return WorkflowResultValueEncodeResult(
                status="encoded",
                encoded=WorkflowEncodedResultValue(
                    result_identity=value.identity,
                    concrete_type_identity=ResultObjectTypeIdentity(
                        f"ksdft2effmass.workflows.{tag}:1"
                    ),
                    owning_domain_identity=ResultObjectDomainIdentity(
                        "ksdft2effmass.workflows"
                    ),
                    schema_identity="workflow-result:1",
                    content_identity=content,
                    payload=payload,
                    payload_digest=digest,
                ),
            )
        except _WorkflowSourceCodecFailure as error:
            return WorkflowResultValueEncodeResult(
                status="invalid" if error.status == "corrupt" else error.status,
                failure=error.failure,
            )
        except MemoryError, RecursionError:
            failure = self._failure(
                "encode",
                WorkflowPersistenceFailureCode.REPRESENTATION_LIMIT,
                (value.identity.value,),
            )
        except TypeError, ValueError, OverflowError:
            failure = self._failure(
                "encode",
                WorkflowPersistenceFailureCode.INVARIANT_VIOLATION,
                (value.identity.value,),
            )
        except Exception:
            failure = self._failure(
                "encode",
                WorkflowPersistenceFailureCode.CODEC_ERROR,
                (value.identity.value,),
            )
        status: Literal["incompatible", "invalid", "error"] = "invalid"
        if failure.code in (
            WorkflowPersistenceFailureCode.UNSUPPORTED_TYPE,
            WorkflowPersistenceFailureCode.UNSUPPORTED_VERSION,
        ):
            status = "incompatible"
        elif failure.code in (
            WorkflowPersistenceFailureCode.CODEC_ERROR,
            WorkflowPersistenceFailureCode.REPRESENTATION_LIMIT,
        ):
            status = "error"
        return WorkflowResultValueEncodeResult(status=status, failure=failure)

    def decode(
        self, value: WorkflowEncodedResultValue
    ) -> WorkflowResultValueDecodeResult:
        """Reconstruct complete immutable values after exact envelope agreement.

        Parameters
        ----------
        value
            Exact complete content-bound envelope in a supported schema and type.

        Returns
        -------
        WorkflowResultValueDecodeResult
            Concrete value or incompatible/corrupt/error evidence. Missing, extra or
            duplicate fields, noncanonical bytes, wrong tags and constructor invariant
            failures never return a partial result. Nested failures are preserved.

        Raises
        ------
        TypeError
            Input is not an exact WorkflowEncodedResultValue.
        """
        if type(value) is not WorkflowEncodedResultValue:
            raise TypeError("value must be WorkflowEncodedResultValue")
        inputs = (
            value.result_identity.value,
            value.schema_identity,
            value.concrete_type_identity.value,
        )
        if value.schema_identity != "workflow-result:1":
            return WorkflowResultValueDecodeResult(
                status="incompatible",
                failure=self._failure(
                    "decode", WorkflowPersistenceFailureCode.UNSUPPORTED_VERSION, inputs
                ),
            )
        label = value.concrete_type_identity.value
        if label not in (
            "ksdft2effmass.workflows.ScientificDecisionResolution:1",
            "ksdft2effmass.workflows.NormalizedObservationSet:1",
        ):
            return WorkflowResultValueDecodeResult(
                status="incompatible",
                failure=self._failure(
                    "decode", WorkflowPersistenceFailureCode.UNSUPPORTED_TYPE, inputs
                ),
            )
        try:
            if value.owning_domain_identity.value != "ksdft2effmass.workflows":
                raise _WorkflowSourceCodecFailure(
                    self._failure(
                        "decode",
                        WorkflowPersistenceFailureCode.IDENTITY_MISMATCH,
                        inputs,
                    )
                )
            # Exact json callbacks close the representation union before typed parsing.
            wire = cast(
                _ResultJson,
                json.loads(
                    value.payload.decode("ascii"),
                    object_pairs_hook=self._unique_object,
                    parse_int=self._reject_number,
                    parse_float=self._reject_number,
                    parse_constant=self._reject_number,
                ),
            )
            result: _WorkflowValue
            if label == "ksdft2effmass.workflows.ScientificDecisionResolution:1":
                result = self._decode_decision(wire)
                content = result.content_identity
            else:
                fields = self._fields(
                    wire, "NormalizedObservationSet", ("identity", "sources")
                )
                sources = fields["sources"]
                if not isinstance(sources, list):
                    raise TypeError("sources must be an ordered array")
                result = NormalizedObservationSet(
                    identity=ResultObjectIdentity(
                        self._label(fields["identity"], "ResultObjectIdentity")
                    ),
                    sources=tuple(self._decode_source(item) for item in sources),
                )
                content = ResultObjectContentIdentity(
                    f"workflow-result:1:sha256:{hashlib.sha256(value.payload).hexdigest()}"
                )
            if result.identity != value.result_identity:
                raise _WorkflowSourceCodecFailure(
                    self._failure(
                        "decode",
                        WorkflowPersistenceFailureCode.IDENTITY_MISMATCH,
                        inputs,
                    )
                )
            if (
                content != value.content_identity
                or hashlib.sha256(value.payload).hexdigest() != value.payload_digest
            ):
                raise _WorkflowSourceCodecFailure(
                    self._failure(
                        "decode",
                        WorkflowPersistenceFailureCode.CONTENT_MISMATCH,
                        inputs,
                    )
                )
            if self._payload(result) != value.payload:
                raise ValueError("noncanonical complete payload")
            return WorkflowResultValueDecodeResult(status="decoded", value=result)
        except _WorkflowSourceCodecFailure as error:
            return WorkflowResultValueDecodeResult(
                status="corrupt" if error.status == "invalid" else error.status,
                failure=error.failure,
            )
        except MemoryError, RecursionError:
            failure = self._failure(
                "decode", WorkflowPersistenceFailureCode.REPRESENTATION_LIMIT, inputs
            )
        except TypeError, ValueError, OverflowError, KeyError:
            failure = self._failure(
                "decode",
                WorkflowPersistenceFailureCode.MALFORMED_REPRESENTATION,
                inputs,
            )
        except Exception:
            failure = self._failure(
                "decode", WorkflowPersistenceFailureCode.CODEC_ERROR, inputs
            )
        status: Literal["incompatible", "corrupt", "error"] = "corrupt"
        if failure.code in (
            WorkflowPersistenceFailureCode.UNSUPPORTED_TYPE,
            WorkflowPersistenceFailureCode.UNSUPPORTED_VERSION,
        ):
            status = "incompatible"
        elif failure.code in (
            WorkflowPersistenceFailureCode.CODEC_ERROR,
            WorkflowPersistenceFailureCode.REPRESENTATION_LIMIT,
        ):
            status = "error"
        return WorkflowResultValueDecodeResult(status=status, failure=failure)

    @staticmethod
    def _failure(
        phase: str, code: WorkflowPersistenceFailureCode, identities: tuple[str, ...]
    ) -> WorkflowPersistenceFailure:
        return WorkflowPersistenceFailure(
            implementation_identity="ksdft2effmass.workflows.WorkflowResultValueSerializer:1",
            phase=phase,
            code=code,
            input_identities=identities,
            expected="complete canonical Workflow value and matching envelope",
            observed=code.value,
            diagnostic="Workflow result codec did not produce a complete value",
            claim_boundary="software representation only; no authority or science",
        )

    @staticmethod
    def _unique_object(pairs: list[tuple[str, _ResultJson]]) -> dict[str, _ResultJson]:
        """Own json's exact object-pairs hook, rejecting duplicate members."""
        result: dict[str, _ResultJson] = {}
        for key, value in pairs:
            if key in result:
                raise ValueError("duplicate member")
            result[key] = value
        return result

    @staticmethod
    def _reject_number(token: str) -> Never:
        """Own json numeric hooks; raw numeric tokens are outside this wire."""
        raise ValueError("untagged numeric token")

    @staticmethod
    def _record(tag: str, fields: dict[str, _ResultJson]) -> _ResultJson:
        return {"type": tag, "fields": fields}

    @classmethod
    def _nominal(cls, tag: str, value: str) -> _ResultJson:
        return cls._record(tag, {"value": value})

    @staticmethod
    def _fields(
        value: _ResultJson, tag: str, names: tuple[str, ...]
    ) -> dict[str, _ResultJson]:
        if (
            not isinstance(value, dict)
            or set(value) != {"type", "fields"}
            or value["type"] != tag
        ):
            raise ValueError("wrong record shape or tag")
        fields = value["fields"]
        if not isinstance(fields, dict) or set(fields) != set(names):
            raise ValueError("wrong field inventory")
        return fields

    @staticmethod
    def _string(value: _ResultJson) -> str:
        if type(value) is not str:
            raise TypeError("expected exact string")
        return value

    @classmethod
    def _label(cls, value: _ResultJson, tag: str) -> str:
        return cls._string(cls._fields(value, tag, ("value",))["value"])

    def _payload(self, value: _WorkflowValue) -> bytes:
        if type(value) is ScientificDecisionResolution:
            wire = self._decision(value)
        elif type(value) is NormalizedObservationSet:
            # Reconstruct the set to recheck membership/provenance before encoding.
            checked = NormalizedObservationSet(
                identity=value.identity, sources=value.sources
            )
            wire = self._record(
                "NormalizedObservationSet",
                {
                    "identity": self._nominal(
                        "ResultObjectIdentity", checked.identity.value
                    ),
                    "sources": [
                        self._encode_source(source) for source in checked.sources
                    ],
                },
            )
        else:
            raise TypeError("unsupported exact Workflow result type")
        return json.dumps(
            wire,
            ensure_ascii=True,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        ).encode("ascii")

    def _encode_source(self, source: NormalizedObservationSource) -> _ResultJson:
        result = self.source_codec.encode(source)
        if result.encoded is None:
            assert result.failure is not None
            if result.status == "encoded":
                raise ValueError("successful source codec omitted its envelope")
            raise _WorkflowSourceCodecFailure(result.failure, result.status)
        envelope = result.encoded
        if envelope.result_identity != source.identity:
            raise _WorkflowSourceCodecFailure(
                self._failure(
                    "encode",
                    WorkflowPersistenceFailureCode.IDENTITY_MISMATCH,
                    (source.identity.value,),
                )
            )
        wire = self._record(
            "WorkflowEncodedResultValue",
            {
                "result_identity": self._nominal(
                    "ResultObjectIdentity", envelope.result_identity.value
                ),
                "concrete_type_identity": self._nominal(
                    "ResultObjectTypeIdentity", envelope.concrete_type_identity.value
                ),
                "owning_domain_identity": self._nominal(
                    "ResultObjectDomainIdentity", envelope.owning_domain_identity.value
                ),
                "schema_identity": envelope.schema_identity,
                "content_identity": self._nominal(
                    "ResultObjectContentIdentity", envelope.content_identity.value
                ),
                "payload": self._nominal(
                    "bytes", base64.b64encode(envelope.payload).decode("ascii")
                ),
                "payload_digest": envelope.payload_digest,
            },
        )
        # A source success must reconstruct as a source and bind identical bytes.
        self._decode_source(wire)
        return wire

    def _decode_source(self, wire: _ResultJson) -> NormalizedObservationSource:
        fields = self._fields(
            wire,
            "WorkflowEncodedResultValue",
            (
                "result_identity",
                "concrete_type_identity",
                "owning_domain_identity",
                "schema_identity",
                "content_identity",
                "payload",
                "payload_digest",
            ),
        )
        text = self._label(fields["payload"], "bytes")
        payload = base64.b64decode(text, validate=True)
        if base64.b64encode(payload).decode("ascii") != text:
            raise ValueError("noncanonical base64")
        envelope = WorkflowEncodedResultValue(
            result_identity=ResultObjectIdentity(
                self._label(fields["result_identity"], "ResultObjectIdentity")
            ),
            concrete_type_identity=ResultObjectTypeIdentity(
                self._label(
                    fields["concrete_type_identity"], "ResultObjectTypeIdentity"
                )
            ),
            owning_domain_identity=ResultObjectDomainIdentity(
                self._label(
                    fields["owning_domain_identity"], "ResultObjectDomainIdentity"
                )
            ),
            schema_identity=self._string(fields["schema_identity"]),
            content_identity=ResultObjectContentIdentity(
                self._label(fields["content_identity"], "ResultObjectContentIdentity")
            ),
            payload=payload,
            payload_digest=self._string(fields["payload_digest"]),
        )
        decoded = self.source_codec.decode(envelope)
        if decoded.value is None:
            assert decoded.failure is not None
            if decoded.status == "decoded":
                raise ValueError("successful source codec omitted its value")
            raise _WorkflowSourceCodecFailure(decoded.failure, decoded.status)
        source = decoded.value
        if (
            not isinstance(source, NormalizedObservationSource)
            or source.identity != envelope.result_identity
        ):
            raise _WorkflowSourceCodecFailure(
                self._failure(
                    "decode",
                    WorkflowPersistenceFailureCode.IDENTITY_MISMATCH,
                    (envelope.result_identity.value,),
                )
            )
        encoded = self.source_codec.encode(source)
        if encoded.encoded is None:
            assert encoded.failure is not None
            if encoded.status == "encoded":
                raise ValueError("successful source codec omitted its envelope")
            raise _WorkflowSourceCodecFailure(encoded.failure, encoded.status)
        if encoded.encoded != envelope:
            raise _WorkflowSourceCodecFailure(
                self._failure(
                    "decode",
                    WorkflowPersistenceFailureCode.CONTENT_MISMATCH,
                    (source.identity.value,),
                )
            )
        return source

    @classmethod
    def _decision(cls, value: ScientificDecisionResolution) -> _ResultJson:
        producer = value.producer_provenance
        wire = cls._record(
            "ScientificDecisionResolution",
            {
                "identity": cls._nominal("ResultObjectIdentity", value.identity.value),
                "content_identity": cls._nominal(
                    "ResultObjectContentIdentity", value.content_identity.value
                ),
                "request_identity": cls._nominal(
                    "ScientificDecisionRequestIdentity", value.request_identity.value
                ),
                "verbatim_response": value.verbatim_response,
                "normalized_option_identity": cls._nominal(
                    "ScientificDecisionOptionIdentity",
                    value.normalized_option_identity.value,
                ),
                "response_source_identity": cls._nominal(
                    "ResponseSourceIdentity", value.response_source_identity.value
                ),
                "authority_context_identity": cls._nominal(
                    "AuthorityContextIdentity", value.authority_context_identity.value
                ),
                "boundary_receipt_identity": None
                if value.boundary_receipt_identity is None
                else cls._nominal(
                    "BoundaryReceiptIdentity", value.boundary_receipt_identity.value
                ),
                "predecessor_resolution_identity": None
                if value.predecessor_resolution_identity is None
                else cls._nominal(
                    "ResultObjectIdentity", value.predecessor_resolution_identity.value
                ),
                "supersedes_resolution_identity": None
                if value.supersedes_resolution_identity is None
                else cls._nominal(
                    "ResultObjectIdentity", value.supersedes_resolution_identity.value
                ),
                "producer_provenance": cls._record(
                    "RepresentedScientificDecisionIngressProducer",
                    {
                        "identity": cls._nominal(
                            "ResultProducerProvenanceIdentity", producer.identity.value
                        ),
                        "workflow_identity": cls._nominal(
                            "WorkflowIdentity", producer.workflow_identity.value
                        ),
                        "workflow_run_identity": cls._nominal(
                            "WorkflowRunIdentity", producer.workflow_run_identity.value
                        ),
                        "request_identity": cls._nominal(
                            "ScientificDecisionRequestIdentity",
                            producer.request_identity.value,
                        ),
                        "transition_record_identity": cls._nominal(
                            "ScientificDecisionTransitionRecordIdentity",
                            producer.transition_record_identity.value,
                        ),
                        "recorder_identity": cls._nominal(
                            "ScientificDecisionRecorderIdentity",
                            producer.recorder_identity.value,
                        ),
                        "response_source_identity": cls._nominal(
                            "ResponseSourceIdentity",
                            producer.response_source_identity.value,
                        ),
                        "authority_context_identity": cls._nominal(
                            "AuthorityContextIdentity",
                            producer.authority_context_identity.value,
                        ),
                        "resolution_identity": cls._nominal(
                            "ResultObjectIdentity", producer.resolution_identity.value
                        ),
                    },
                ),
            },
        )
        cls._decode_decision(wire)
        return wire

    @classmethod
    def _decode_decision(cls, wire: _ResultJson) -> ScientificDecisionResolution:
        fields = cls._fields(
            wire,
            "ScientificDecisionResolution",
            (
                "identity",
                "content_identity",
                "request_identity",
                "verbatim_response",
                "normalized_option_identity",
                "response_source_identity",
                "authority_context_identity",
                "boundary_receipt_identity",
                "predecessor_resolution_identity",
                "supersedes_resolution_identity",
                "producer_provenance",
            ),
        )
        producer = cls._fields(
            fields["producer_provenance"],
            "RepresentedScientificDecisionIngressProducer",
            (
                "identity",
                "workflow_identity",
                "workflow_run_identity",
                "request_identity",
                "transition_record_identity",
                "recorder_identity",
                "response_source_identity",
                "authority_context_identity",
                "resolution_identity",
            ),
        )
        receipt = fields["boundary_receipt_identity"]
        predecessor = fields["predecessor_resolution_identity"]
        supersedes = fields["supersedes_resolution_identity"]
        return ScientificDecisionResolution(
            identity=ResultObjectIdentity(
                cls._label(fields["identity"], "ResultObjectIdentity")
            ),
            content_identity=ResultObjectContentIdentity(
                cls._label(fields["content_identity"], "ResultObjectContentIdentity")
            ),
            request_identity=ScientificDecisionRequestIdentity(
                cls._label(
                    fields["request_identity"], "ScientificDecisionRequestIdentity"
                )
            ),
            verbatim_response=cls._string(fields["verbatim_response"]),
            normalized_option_identity=ScientificDecisionOptionIdentity(
                cls._label(
                    fields["normalized_option_identity"],
                    "ScientificDecisionOptionIdentity",
                )
            ),
            response_source_identity=ResponseSourceIdentity(
                cls._label(fields["response_source_identity"], "ResponseSourceIdentity")
            ),
            authority_context_identity=AuthorityContextIdentity(
                cls._label(
                    fields["authority_context_identity"], "AuthorityContextIdentity"
                )
            ),
            boundary_receipt_identity=None
            if receipt is None
            else BoundaryReceiptIdentity(
                cls._label(receipt, "BoundaryReceiptIdentity")
            ),
            predecessor_resolution_identity=None
            if predecessor is None
            else ResultObjectIdentity(cls._label(predecessor, "ResultObjectIdentity")),
            supersedes_resolution_identity=None
            if supersedes is None
            else ResultObjectIdentity(cls._label(supersedes, "ResultObjectIdentity")),
            producer_provenance=RepresentedScientificDecisionIngressProducer(
                identity=ResultProducerProvenanceIdentity(
                    cls._label(producer["identity"], "ResultProducerProvenanceIdentity")
                ),
                workflow_identity=WorkflowIdentity(
                    cls._label(producer["workflow_identity"], "WorkflowIdentity")
                ),
                workflow_run_identity=WorkflowRunIdentity(
                    cls._label(producer["workflow_run_identity"], "WorkflowRunIdentity")
                ),
                request_identity=ScientificDecisionRequestIdentity(
                    cls._label(
                        producer["request_identity"],
                        "ScientificDecisionRequestIdentity",
                    )
                ),
                transition_record_identity=ScientificDecisionTransitionRecordIdentity(
                    cls._label(
                        producer["transition_record_identity"],
                        "ScientificDecisionTransitionRecordIdentity",
                    )
                ),
                recorder_identity=ScientificDecisionRecorderIdentity(
                    cls._label(
                        producer["recorder_identity"],
                        "ScientificDecisionRecorderIdentity",
                    )
                ),
                response_source_identity=ResponseSourceIdentity(
                    cls._label(
                        producer["response_source_identity"], "ResponseSourceIdentity"
                    )
                ),
                authority_context_identity=AuthorityContextIdentity(
                    cls._label(
                        producer["authority_context_identity"],
                        "AuthorityContextIdentity",
                    )
                ),
                resolution_identity=ResultObjectIdentity(
                    cls._label(producer["resolution_identity"], "ResultObjectIdentity")
                ),
            ),
        )
