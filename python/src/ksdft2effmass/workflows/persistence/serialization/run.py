"""Public WorkflowRun serializer composed from bounded wire-value facets."""

from __future__ import annotations

import base64
import hashlib
import json
import math
from dataclasses import dataclass, replace
from datetime import UTC, datetime, timedelta
from typing import Never, cast

from ...model import (
    ResultObject,
    ResultObjectIdentity,
)
from ...runs.aggregate import WorkflowRun
from ...runs.identities import (
    ResultObjectContentIdentity,
    ResultObjectDomainIdentity,
    ResultObjectTypeIdentity,
)
from ..records import (
    WorkflowEncodedResultValue,
    WorkflowEncodedRun,
    WorkflowPersistenceFailure,
    WorkflowPersistenceFailureCode,
    WorkflowResultValueCodec,
    WorkflowRunCommitBinding,
    WorkflowRunDecodeResult,
    WorkflowRunEncodeResult,
)
from ._base import (
    _ResultJson,
    _RunValue,
    _WorkflowRunCodecFailure,
    _WorkflowRunWireUnsupported,
)
from .aggregate import _WorkflowRunAggregateWireSerializer
from .authority import _WorkflowRunAuthorityWireSerializer
from .dispatch import _WorkflowRunDispatchWireSerializer
from .history import _WorkflowRunHistoryWireSerializer
from .petrinet import _WorkflowRunPetrinetWireSerializer
from .task import _WorkflowRunTaskWireSerializer


@dataclass(frozen=True, slots=True, kw_only=True)
class WorkflowRunSerializer(
    _WorkflowRunPetrinetWireSerializer,
    _WorkflowRunTaskWireSerializer,
    _WorkflowRunAuthorityWireSerializer,
    _WorkflowRunDispatchWireSerializer,
    _WorkflowRunHistoryWireSerializer,
    _WorkflowRunAggregateWireSerializer,
):
    """Explicit complete version-one WorkflowRun wire serializer.

    Parameters
    ----------
    result_codec
        Explicit effect-free, operationally immutable outward result codec. Application
        composition supplies the selected seven-family codec; protocol membership
        alone does not establish concrete support. No registry or inward domain import
        is used.

    Notes
    -----
    The root has exactly ``schema``, ``run`` and ``commit_binding``. Schema is
    ``ksdft2effmass.workflow-run:1``; the historical writer is explicitly recognized as
    ``ksdft2effmass.workflows.WorkflowRunAtomicRepository:1``. Unknown versions are
    incompatible, not inferred legacy representations. Declared reachable fields
    (including null/default/derived fields) use literal field/constructor branches,
    subject to the exact empty-collection omission rule below.
    Records, nominal identities and enums use ``{type, fields}``; tuples are ordered
    arrays. Canonical bytes are sorted compact ASCII JSON without newline. Integers
    use tagged ``hex(int)`` strings (no Boolean coercion or decimal size limit), finite
    floats tagged ``float.hex()`` (preserving binary64 signed zero), bytes canonical
    base64, and UTC timestamps ISO-8601 with six fractional digits and ``+00:00``.

    Within v1, both empty ``nested_invocation_intents`` and
    ``nested_terminal_observations`` are omitted, preserving the original 34-field
    aggregate bytes. If either is nonempty, both keys are required in the 36-field
    extension. Single-key, unknown-field and explicitly both-empty extensions are
    corrupt; no second schema, writer or migration is introduced. A terminal intent
    reference retains its exact new-intent or combined-invocation nominal tag.

    Every result occurrence contains a complete injected-codec envelope. A local
    operation map checks repeated identities, including normalized sources, against
    every envelope field; it is not a type registry or persistent cache. References
    must agree with envelope type/domain/content metadata. Constructor-derived
    identities are reconstructed and compared, never overwritten. Exact re-encoding
    rejects constructor normalization of malformed wire. Allocation/recursion and
    operational failures are sanitized errors without partial values.

    This serializer performs no structural-history validation, replay, authorization,
    native I/O, store operation or receipt derivation. Successful reconstruction proves
    representation only, not scientific validity, provenance truth or effect permission.

    Raises
    ------
    TypeError
        The supplied dependency does not implement the explicit codec port.
    """

    result_codec: WorkflowResultValueCodec

    def __post_init__(self) -> None:
        """Require the explicitly supplied codec without discovering implementations."""
        if not isinstance(self.result_codec, WorkflowResultValueCodec):
            raise TypeError("result_codec must implement WorkflowResultValueCodec")

    def serialize(
        self, run: WorkflowRun, binding: WorkflowRunCommitBinding
    ) -> WorkflowRunEncodeResult:
        """Encode a complete run and its durable transaction/key/writer binding.

        Parameters
        ----------
        run
            Exact immutable WorkflowRun; only schema version one is supported.
        binding
            Exact immutable historical binding included in the content-bound payload.

        Returns
        -------
        WorkflowRunEncodeResult
            Complete bytes/content identity on encoded; incompatible, invalid or
            error with structured evidence and no partial bytes otherwise.

        Raises
        ------
        TypeError
            A direct argument has the wrong exact semantic type.
        """
        if (
            type(run) is not WorkflowRun
            or type(binding) is not WorkflowRunCommitBinding
        ):
            raise TypeError("serialize requires exact WorkflowRun and commit binding")
        inputs = (
            run.identity.value,
            run.revision_identity.value,
            binding.transaction_identity,
        )
        try:
            self._versions(run, binding, "encode")
            wire = self._encode(run, {})
            payload = self._json(self._root(wire, binding))
            reconstructed = self._exact(self._decode(wire, {}), WorkflowRun)
            if (
                self._json(self._root(self._encode(reconstructed, {}), binding))
                != payload
            ):
                raise self._failure(
                    "encode", WorkflowPersistenceFailureCode.CONTENT_MISMATCH
                )
            return WorkflowRunEncodeResult(
                status="encoded",
                encoded=WorkflowEncodedRun(
                    schema_identity="ksdft2effmass.workflow-run:1",
                    content_identity="ksdft2effmass.workflow-run:1:sha256:"
                    + hashlib.sha256(payload).hexdigest(),
                    payload=payload,
                ),
            )
        except _WorkflowRunCodecFailure as error:
            return WorkflowRunEncodeResult(
                status="invalid" if error.status == "corrupt" else error.status,
                failure=self._annotate_failure(error.failure, inputs, "encode"),
            )
        except MemoryError, RecursionError:
            failure = self._failure(
                "encode", WorkflowPersistenceFailureCode.REPRESENTATION_LIMIT
            )
        except TypeError, ValueError, OverflowError, KeyError:
            failure = self._failure(
                "encode", WorkflowPersistenceFailureCode.INVARIANT_VIOLATION
            )
        except Exception:
            failure = self._failure(
                "encode", WorkflowPersistenceFailureCode.CODEC_ERROR
            )
        return WorkflowRunEncodeResult(
            status="invalid" if failure.status == "corrupt" else failure.status,
            failure=self._annotate_failure(failure.failure, inputs, "encode"),
        )

    def deserialize(self, payload: bytes) -> WorkflowRunDecodeResult:
        """Decode canonical complete run bytes without checking stored presence.

        Parameters
        ----------
        payload
            Exact immutable ASCII JSON bytes, including the persisted commit binding.

        Returns
        -------
        WorkflowRunDecodeResult
            Complete run/binding on decoded only; incompatible, corrupt or error
            otherwise. Known malformed fields, tags, canonicality and derived identity
            mismatches never yield a partial run.

        Raises
        ------
        TypeError
            Payload is not exact bytes (mutable buffers and text are rejected).
        """
        if type(payload) is not bytes:
            raise TypeError("payload must be exact bytes")
        inputs: tuple[str, ...] = ()
        try:
            inputs = ("sha256:" + hashlib.sha256(payload).hexdigest(),)
            wire = cast(
                _ResultJson,
                json.loads(
                    payload.decode("ascii"),
                    object_pairs_hook=self._unique_object,
                    parse_int=self._reject_number,
                    parse_float=self._reject_number,
                    parse_constant=self._reject_number,
                ),
            )
            if not isinstance(wire, dict) or set(wire) != {
                "schema",
                "run",
                "commit_binding",
            }:
                raise ValueError("wrong complete root fields")
            schema = self._string(wire["schema"])
            if schema != "ksdft2effmass.workflow-run:1":
                raise self._failure(
                    "decode", WorkflowPersistenceFailureCode.UNSUPPORTED_VERSION
                )
            raw_binding = wire["commit_binding"]
            if not isinstance(raw_binding, dict) or set(raw_binding) != {
                "transaction_identity",
                "commit_idempotency_identity",
                "persistence_implementation_identity",
            }:
                raise ValueError("wrong durable binding fields")
            binding = WorkflowRunCommitBinding(
                transaction_identity=self._string(raw_binding["transaction_identity"]),
                commit_idempotency_identity=self._string(
                    raw_binding["commit_idempotency_identity"]
                ),
                persistence_implementation_identity=self._string(
                    raw_binding["persistence_implementation_identity"]
                ),
            )
            # Known schema canonicality is checked before constructing any domain run.
            if self._json(wire) != payload:
                raise ValueError("noncanonical aggregate bytes")
            run = self._exact(self._decode(wire["run"], {}), WorkflowRun)
            self._versions(run, binding, "decode")
            if self._json(self._root(self._encode(run, {}), binding)) != payload:
                raise self._failure(
                    "decode", WorkflowPersistenceFailureCode.CONTENT_MISMATCH
                )
            return WorkflowRunDecodeResult(status="decoded", run=run, binding=binding)
        except _WorkflowRunCodecFailure as error:
            return WorkflowRunDecodeResult(
                status="corrupt" if error.status == "invalid" else error.status,
                failure=self._annotate_failure(error.failure, inputs, "decode"),
            )
        except MemoryError, RecursionError:
            failure = self._failure(
                "decode", WorkflowPersistenceFailureCode.REPRESENTATION_LIMIT
            )
        except TypeError, ValueError, OverflowError, KeyError:
            failure = self._failure(
                "decode", WorkflowPersistenceFailureCode.MALFORMED_REPRESENTATION
            )
        except Exception:
            failure = self._failure(
                "decode", WorkflowPersistenceFailureCode.CODEC_ERROR
            )
        return WorkflowRunDecodeResult(
            status="corrupt" if failure.status == "invalid" else failure.status,
            failure=self._annotate_failure(failure.failure, inputs, "decode"),
        )

    @staticmethod
    def _annotate_failure(
        failure: WorkflowPersistenceFailure, inputs: tuple[str, ...], phase: str
    ) -> WorkflowPersistenceFailure:
        if (
            failure.implementation_identity
            == "ksdft2effmass.workflows.WorkflowRunSerializer:1"
        ):
            return replace(failure, input_identities=inputs, phase=phase)
        return failure

    def _versions(
        self, run: WorkflowRun, binding: WorkflowRunCommitBinding, phase: str
    ) -> None:
        if (
            run.schema_version != 1
            or binding.persistence_implementation_identity
            != "ksdft2effmass.workflows.WorkflowRunAtomicRepository:1"
        ):
            raise self._failure(
                phase, WorkflowPersistenceFailureCode.UNSUPPORTED_VERSION
            )

    @staticmethod
    def _root(run: _ResultJson, binding: WorkflowRunCommitBinding) -> _ResultJson:
        return {
            "schema": "ksdft2effmass.workflow-run:1",
            "run": run,
            "commit_binding": {
                "transaction_identity": binding.transaction_identity,
                "commit_idempotency_identity": binding.commit_idempotency_identity,
                "persistence_implementation_identity": (
                    binding.persistence_implementation_identity
                ),
            },
        }

    @staticmethod
    def _json(value: _ResultJson) -> bytes:
        return json.dumps(
            value,
            ensure_ascii=True,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        ).encode("ascii")

    @staticmethod
    def _unique_object(pairs: list[tuple[str, _ResultJson]]) -> dict[str, _ResultJson]:
        """Own json's exact object-pairs hook with duplicate-member rejection."""
        result: dict[str, _ResultJson] = {}
        for key, value in pairs:
            if key in result:
                raise ValueError("duplicate member")
            result[key] = value
        return result

    @staticmethod
    def _reject_number(token: str) -> Never:
        """Own json's numeric hooks; numbers must use the explicit scalar grammar."""
        raise ValueError("raw numeric token")

    def _encode(
        self, value: _RunValue, seen: dict[str, WorkflowEncodedResultValue]
    ) -> _ResultJson:
        if value is None:
            return None
        if type(value) is bool:
            return value
        if type(value) is str:
            return value
        if type(value) is int:
            return self._record("int", {"value": hex(value)})
        if type(value) is float:
            if not math.isfinite(value):
                raise ValueError("nonfinite float")
            return self._record("float", {"value": value.hex()})
        if type(value) is bytes:
            return self._record(
                "bytes", {"value": base64.b64encode(value).decode("ascii")}
            )
        if type(value) is datetime:
            if value.tzinfo is None or value.utcoffset() != timedelta(0):
                raise ValueError("timestamp must be UTC")
            return self._record(
                "datetime",
                {"value": value.astimezone(UTC).isoformat(timespec="microseconds")},
            )
        if type(value) is tuple:
            return [self._encode(item, seen) for item in value]
        try:
            return self._encode_petrinet(value, seen)
        except _WorkflowRunWireUnsupported:
            pass
        try:
            return self._encode_task(value, seen)
        except _WorkflowRunWireUnsupported:
            pass
        try:
            return self._encode_authority(value, seen)
        except _WorkflowRunWireUnsupported:
            pass
        try:
            return self._encode_dispatch(value, seen)
        except _WorkflowRunWireUnsupported:
            pass
        try:
            return self._encode_history(value, seen)
        except _WorkflowRunWireUnsupported:
            pass
        try:
            return self._encode_aggregate(value, seen)
        except _WorkflowRunWireUnsupported:
            pass
        if (
            isinstance(value, ResultObject)
            and type(value.identity) is ResultObjectIdentity
        ):
            return self._result_wire(self._encode_result(value, seen))
        raise self._failure("encode", WorkflowPersistenceFailureCode.UNSUPPORTED_TYPE)

    def _decode(
        self, wire: _ResultJson, seen: dict[str, WorkflowEncodedResultValue]
    ) -> _RunValue:
        if wire is None:
            return None
        if type(wire) is bool:
            return wire
        if type(wire) is str:
            return wire
        if isinstance(wire, list):
            return tuple(self._decode(item, seen) for item in wire)
        if not isinstance(wire, dict) or set(wire) != {"type", "fields"}:
            raise ValueError("wrong tagged value shape")
        tag = self._string(wire["type"])
        if tag == "int":
            text = self._string(self._fields(wire, "int", ("value",))["value"])
            number = int(text, 16)
            if hex(number) != text:
                raise ValueError("noncanonical signed hexadecimal integer")
            return number
        if tag == "float":
            text = self._string(self._fields(wire, "float", ("value",))["value"])
            real = float.fromhex(text)
            if not math.isfinite(real) or real.hex() != text:
                raise ValueError("noncanonical finite binary64")
            return real
        if tag == "bytes":
            text = self._string(self._fields(wire, "bytes", ("value",))["value"])
            payload = base64.b64decode(text, validate=True)
            if base64.b64encode(payload).decode("ascii") != text:
                raise ValueError("noncanonical base64")
            return payload
        if tag == "datetime":
            text = self._string(self._fields(wire, "datetime", ("value",))["value"])
            instant = datetime.fromisoformat(text)
            if (
                instant.tzinfo is None
                or instant.utcoffset() != timedelta(0)
                or instant.isoformat(timespec="microseconds") != text
            ):
                raise ValueError("noncanonical UTC microsecond timestamp")
            return instant
        if tag == "WorkflowEncodedResultValue":
            fields = self._fields(
                wire,
                tag,
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
            envelope = WorkflowEncodedResultValue(
                result_identity=self._exact(
                    self._decode(fields["result_identity"], seen), ResultObjectIdentity
                ),
                concrete_type_identity=self._exact(
                    self._decode(fields["concrete_type_identity"], seen),
                    ResultObjectTypeIdentity,
                ),
                owning_domain_identity=self._exact(
                    self._decode(fields["owning_domain_identity"], seen),
                    ResultObjectDomainIdentity,
                ),
                schema_identity=self._string(fields["schema_identity"]),
                content_identity=self._exact(
                    self._decode(fields["content_identity"], seen),
                    ResultObjectContentIdentity,
                ),
                payload=self._exact(self._decode(fields["payload"], seen), bytes),
                payload_digest=self._string(fields["payload_digest"]),
            )
            return self._decode_result(envelope, seen)
        try:
            return self._decode_petrinet(tag, wire, seen)
        except _WorkflowRunWireUnsupported:
            pass
        try:
            return self._decode_task(tag, wire, seen)
        except _WorkflowRunWireUnsupported:
            pass
        try:
            return self._decode_authority(tag, wire, seen)
        except _WorkflowRunWireUnsupported:
            pass
        try:
            return self._decode_dispatch(tag, wire, seen)
        except _WorkflowRunWireUnsupported:
            pass
        try:
            return self._decode_history(tag, wire, seen)
        except _WorkflowRunWireUnsupported:
            pass
        try:
            return self._decode_aggregate(tag, wire, seen)
        except _WorkflowRunWireUnsupported:
            pass
        raise self._failure("decode", WorkflowPersistenceFailureCode.UNSUPPORTED_TYPE)
