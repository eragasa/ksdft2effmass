"""Complete QE result values at the injected Workflow persistence boundary.

The canonical ``qe-result-value:1`` wire retains the three exact supported result
families, not native file contents. Explicit tagged records preserve all operation
observations and source identities. The existing neutral schema-1 serializer owns
its nested JSON string, units, binary64 values and unchanged duality tolerance.
No parsing of native files, execution, normalization, registry or replay occurs.
Wire agreement is software evidence, not provenance authentication or science.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from typing import Literal, Never, cast

from ksdft2effmass.ksdft.pw import (
    KohnShamPlaneWaveCalculationRecord,
    KohnShamPlaneWaveCalculationRecordJsonSerializer,
)
from ksdft2effmass.ksdft.pw.serialization import JsonRepresentation
from ksdft2effmass.workflows import artifacts as a
from ksdft2effmass.workflows import model as m
from ksdft2effmass.workflows.persistence import (
    WorkflowEncodedResultValue,
    WorkflowPersistenceFailure,
    WorkflowPersistenceFailureCode,
    WorkflowResultValueDecodeResult,
    WorkflowResultValueEncodeResult,
)
from ksdft2effmass.workflows.runs.identities import (
    ResultObjectContentIdentity,
    ResultObjectDomainIdentity,
    ResultObjectTypeIdentity,
)

from . import contracts as c
from . import observation as o

type _Json = None | bool | str | list[_Json] | dict[str, _Json]
type _Result = (
    c.QuantumEspressoPwResult
    | c.QuantumEspressoBandsResult
    | o.QuantumEspressoExtractedObservationResult
)
type _Nominal = (
    m.ResultObjectIdentity
    | m.AttemptIdentity
    | m.OperationIdentity
    | m.TaskActivationIdentity
    | m.TaskDefinitionIdentity
    | m.TaskInstanceIdentity
    | a.ArtifactIdentity
    | a.ArtifactManifestIdentity
    | a.ArtifactManifestEntryIdentity
    | a.ArtifactProducerProvenanceIdentity
    | c.QuantumEspressoExecutionInputIdentity
    | c.QuantumEspressoExecutableConfigurationIdentity
    | c.QuantumEspressoPreparationIdentity
    | c.QuantumEspressoProcessObservationIdentity
    | c.QuantumEspressoDiagnosticClassifierIdentity
    | c.QuantumEspressoDiagnosticObservationIdentity
    | c.QuantumEspressoOutputMarkerObservationIdentity
    | c.QuantumEspressoDiagnosticReportIdentity
    | c.QuantumEspressoTerminalRecordIdentity
    | c.QuantumEspressoArtifactDestination
    | o.QuantumEspressoParsedDocumentIdentity
    | o.QuantumEspressoXsdParserIdentity
    | o.QuantumEspressoObservationNormalizationPolicyIdentity
)
type _Enum = (
    c.QuantumEspressoProgram
    | c.QuantumEspressoExecutableKind
    | c.QuantumEspressoDiagnosticChannel
    | c.QuantumEspressoDiagnosticDisposition
    | c.QuantumEspressoDiagnosticReportKind
    | c.QuantumEspressoProcessFailureKind
)
type _Record = (
    _Result
    | _Nominal
    | _Enum
    | a.ArtifactContentIdentity
    | c.QuantumEspressoFileArtifactContent
    | c.QuantumEspressoTreeArtifactContent
    | c.QuantumEspressoNativeInputArtifact
    | c.QuantumEspressoPseudopotentialArtifact
    | c.QuantumEspressoPredecessorNativeStateArtifact
    | c.QuantumEspressoExecutionInput
    | c.QuantumEspressoStreamObservation
    | c.QuantumEspressoProcessTermination
    | c.QuantumEspressoProcessObservation
    | c.QuantumEspressoDiagnosticObservation
    | c.QuantumEspressoOutputMarkerObservation
    | c.QuantumEspressoDiagnosticReport
    | c.QuantumEspressoCalculatorOutcome
    | c.QuantumEspressoOperationResultEvidence
    | o.QuantumEspressoObservationNormalizationPolicy
    | KohnShamPlaneWaveCalculationRecord
)
type _Node = None | bool | str | int | _Record | tuple[_Node, ...]


class _UnsupportedVersion(ValueError):
    """Internal distinction between a new owned version and malformed known wire."""


@dataclass(frozen=True, slots=True)
class QuantumEspressoResultValueSerializer:
    """Effect-free, closed three-family QE result codec, version 1.

    Notes
    -----
    There are no configurable fields or mutable dependencies. A fresh neutral
    serializer is constructed for each operation with its approved ``1.0e-12``
    absolute duality tolerance. The nested neutral JSON is retained exactly,
    including its final newline and represented tolerance; it is not reinterpreted
    as this codec's tagged scalar grammar.

    Supported public class labels end in ``:1`` under domain
    ``ksdft2effmass.integration.quantum_espresso``. PW and bands record versions
    are ``qe-pw-result:1`` and ``qe-bands-result:1``; execution inputs require
    ``qe-execution-input:1``. Parser and normalization policy require their
    constructor-supported identities and version ``1``. Observer, classifier and
    program version labels are provenance data, not executable implementations.

    Every declared field is a member of an explicit ``{type, fields}`` record.
    Nominal identities and enums have tagged ``value`` fields. Integers use tagged
    canonical Python ``hex`` strings without bool coercion or precision loss;
    tuples are ordered arrays. Strings, null and booleans retain JSON types.
    Canonical ASCII JSON has sorted keys, compact separators and no final newline.
    Content identity is ``qe-result-value:1:sha256:<digest>`` over those complete
    bytes; the separate payload digest binds the same bytes.

    Unknown versions are incompatible; malformed known records, noncanonical
    bytes, detached identities and constructor violations are corrupt. No partial
    value, native data access, arbitrary ResultObject support or aggregate repository
    capability is provided. Immutable reconstructed records retain scientific units
    and provenance but do not authenticate their external source.
    """

    def encode(self, value: m.ResultObject) -> WorkflowResultValueEncodeResult:
        """Encode an exact PW, bands or extracted-observation result.

        Parameters
        ----------
        value
            Workflow-facing result with exact nominal identity. Unsupported concrete
            types (including subclasses) return incompatible, not identity stand-ins.

        Returns
        -------
        WorkflowResultValueEncodeResult
            Complete encoded envelope or sanitized incompatible/invalid/error evidence.

        Raises
        ------
        TypeError
            The input does not expose an exact ResultObjectIdentity.
        """
        if (
            not isinstance(value, m.ResultObject)
            or type(value.identity) is not m.ResultObjectIdentity
        ):
            raise TypeError("value must expose an exact ResultObjectIdentity")
        if type(value) not in (
            c.QuantumEspressoPwResult,
            c.QuantumEspressoBandsResult,
            o.QuantumEspressoExtractedObservationResult,
        ):
            return WorkflowResultValueEncodeResult(
                status="incompatible",
                failure=self._failure(
                    "encode",
                    WorkflowPersistenceFailureCode.UNSUPPORTED_TYPE,
                    (value.identity.value,),
                ),
            )
        result = cast(_Result, value)
        try:
            payload = self._payload(result)
            # Constructor and nested identity checks apply equally on both sides.
            self._decode_result(payload, self._result_tag(result))
            digest = hashlib.sha256(payload).hexdigest()
            return WorkflowResultValueEncodeResult(
                status="encoded",
                encoded=WorkflowEncodedResultValue(
                    result_identity=result.identity,
                    concrete_type_identity=ResultObjectTypeIdentity(
                        "ksdft2effmass.integration.quantum_espresso."
                        + self._result_tag(result)
                        + ":1"
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
                ),
            )
        except _UnsupportedVersion:
            status: Literal["incompatible", "invalid", "error"] = "incompatible"
            code = WorkflowPersistenceFailureCode.UNSUPPORTED_VERSION
        except MemoryError, RecursionError:
            status = "error"
            code = WorkflowPersistenceFailureCode.REPRESENTATION_LIMIT
        except TypeError, ValueError, OverflowError, KeyError:
            status = "invalid"
            code = WorkflowPersistenceFailureCode.INVARIANT_VIOLATION
        except Exception:
            status = "error"
            code = WorkflowPersistenceFailureCode.CODEC_ERROR
        return WorkflowResultValueEncodeResult(
            status=status,
            failure=self._failure("encode", code, (value.identity.value,)),
        )

    def decode(
        self, value: WorkflowEncodedResultValue
    ) -> WorkflowResultValueDecodeResult:
        """Reconstruct a complete concrete value with exact envelope binding.

        Parameters
        ----------
        value
            Exact WorkflowEncodedResultValue with full bytes and identity metadata.

        Returns
        -------
        WorkflowResultValueDecodeResult
            Immutable concrete value only on decoded; otherwise incompatible, corrupt
            or error with sanitized diagnostics and no partial result.

        Raises
        ------
        TypeError
            The input is not an exact WorkflowEncodedResultValue.
        """
        if type(value) is not WorkflowEncodedResultValue:
            raise TypeError("value must be WorkflowEncodedResultValue")
        inputs = (
            value.result_identity.value,
            value.schema_identity,
            value.concrete_type_identity.value,
        )
        if value.schema_identity != "qe-result-value:1":
            return WorkflowResultValueDecodeResult(
                status="incompatible",
                failure=self._failure(
                    "decode", WorkflowPersistenceFailureCode.UNSUPPORTED_VERSION, inputs
                ),
            )
        label = value.concrete_type_identity.value
        if (
            label
            == "ksdft2effmass.integration.quantum_espresso.QuantumEspressoPwResult:1"
        ):
            tag = "QuantumEspressoPwResult"
        elif (
            label
            == "ksdft2effmass.integration.quantum_espresso.QuantumEspressoBandsResult:1"
        ):
            tag = "QuantumEspressoBandsResult"
        elif label == (
            "ksdft2effmass.integration.quantum_espresso."
            "QuantumEspressoExtractedObservationResult:1"
        ):
            tag = "QuantumEspressoExtractedObservationResult"
        else:
            return WorkflowResultValueDecodeResult(
                status="incompatible",
                failure=self._failure(
                    "decode", WorkflowPersistenceFailureCode.UNSUPPORTED_TYPE, inputs
                ),
            )
        try:
            if (
                value.owning_domain_identity.value
                != "ksdft2effmass.integration.quantum_espresso"
            ):
                return WorkflowResultValueDecodeResult(
                    status="corrupt",
                    failure=self._failure(
                        "decode",
                        WorkflowPersistenceFailureCode.IDENTITY_MISMATCH,
                        inputs,
                    ),
                )
            digest = hashlib.sha256(value.payload).hexdigest()
            if (
                value.payload_digest != digest
                or value.content_identity.value != f"qe-result-value:1:sha256:{digest}"
            ):
                return WorkflowResultValueDecodeResult(
                    status="corrupt",
                    failure=self._failure(
                        "decode",
                        WorkflowPersistenceFailureCode.CONTENT_MISMATCH,
                        inputs,
                    ),
                )
            result = self._decode_result(value.payload, tag)
            if result.identity != value.result_identity:
                return WorkflowResultValueDecodeResult(
                    status="corrupt",
                    failure=self._failure(
                        "decode",
                        WorkflowPersistenceFailureCode.IDENTITY_MISMATCH,
                        inputs,
                    ),
                )
            if self._payload(result) != value.payload:
                raise ValueError("noncanonical complete representation")
            return WorkflowResultValueDecodeResult(status="decoded", value=result)
        except _UnsupportedVersion:
            status: Literal["incompatible", "corrupt", "error"] = "incompatible"
            code = WorkflowPersistenceFailureCode.UNSUPPORTED_VERSION
        except MemoryError, RecursionError:
            status = "error"
            code = WorkflowPersistenceFailureCode.REPRESENTATION_LIMIT
        except TypeError, ValueError, OverflowError, KeyError:
            status = "corrupt"
            code = WorkflowPersistenceFailureCode.MALFORMED_REPRESENTATION
        except Exception:
            status = "error"
            code = WorkflowPersistenceFailureCode.CODEC_ERROR
        return WorkflowResultValueDecodeResult(
            status=status, failure=self._failure("decode", code, inputs)
        )

    @staticmethod
    def _failure(
        phase: str, code: WorkflowPersistenceFailureCode, inputs: tuple[str, ...]
    ) -> WorkflowPersistenceFailure:
        return WorkflowPersistenceFailure(
            implementation_identity="ksdft2effmass.integration.quantum_espresso.QuantumEspressoResultValueSerializer:1",
            phase=phase,
            code=code,
            input_identities=inputs,
            expected="complete canonical supported QE result and matching envelope",
            observed=code.value,
            diagnostic="QE result codec did not produce a complete value",
            claim_boundary=(
                "represented software failure only; no scientific or execution claim"
            ),
        )

    @staticmethod
    def _result_tag(value: _Result) -> str:
        if type(value) is c.QuantumEspressoPwResult:
            return "QuantumEspressoPwResult"
        if type(value) is c.QuantumEspressoBandsResult:
            return "QuantumEspressoBandsResult"
        if type(value) is o.QuantumEspressoExtractedObservationResult:
            return "QuantumEspressoExtractedObservationResult"
        raise TypeError("unsupported exact result")

    @classmethod
    def _payload(cls, value: _Result) -> bytes:
        return json.dumps(
            cls._encode_node(value),
            ensure_ascii=True,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        ).encode("ascii")

    @staticmethod
    def _unique_object(pairs: list[tuple[str, _Json]]) -> dict[str, _Json]:
        result: dict[str, _Json] = {}
        for key, value in pairs:
            if key in result:
                raise ValueError("duplicate member")
            result[key] = value
        return result

    @staticmethod
    def _reject_number(token: str) -> Never:
        raise ValueError("raw numbers are not QE tagged wire scalars")

    @classmethod
    def _decode_result(cls, payload: bytes, tag: str) -> _Result:
        wire = cast(
            _Json,
            json.loads(
                payload.decode("ascii"),
                object_pairs_hook=cls._unique_object,
                parse_int=cls._reject_number,
                parse_float=cls._reject_number,
                parse_constant=cls._reject_number,
            ),
        )
        if not isinstance(wire, dict) or wire.get("type") != tag:
            raise ValueError("result type does not match envelope")
        value = cls._decode_node(wire)
        if type(value) not in (
            c.QuantumEspressoPwResult,
            c.QuantumEspressoBandsResult,
            o.QuantumEspressoExtractedObservationResult,
        ):
            raise TypeError("not a supported result")
        return cast(_Result, value)

    @classmethod
    def _record(cls, tag: str, fields: dict[str, _Node]) -> _Json:
        return {
            "type": tag,
            "fields": {key: cls._encode_node(value) for key, value in fields.items()},
        }

    @classmethod
    def _encode_node(cls, value: _Node) -> _Json:
        if value is None or type(value) is bool or type(value) is str:
            return value
        if type(value) is int:
            return {"type": "int", "fields": {"value": hex(value)}}
        if type(value) is tuple:
            return [cls._encode_node(item) for item in value]
        if type(value) is m.ResultObjectIdentity:
            return cls._record("ResultObjectIdentity", {"value": value.value})
        if type(value) is m.AttemptIdentity:
            return cls._record("AttemptIdentity", {"value": value.value})
        if type(value) is m.OperationIdentity:
            return cls._record("OperationIdentity", {"value": value.value})
        if type(value) is m.TaskActivationIdentity:
            return cls._record("TaskActivationIdentity", {"value": value.value})
        if type(value) is m.TaskDefinitionIdentity:
            return cls._record("TaskDefinitionIdentity", {"value": value.value})
        if type(value) is m.TaskInstanceIdentity:
            return cls._record("TaskInstanceIdentity", {"value": value.value})
        if type(value) is a.ArtifactIdentity:
            return cls._record("ArtifactIdentity", {"value": value.value})
        if type(value) is a.ArtifactManifestIdentity:
            return cls._record("ArtifactManifestIdentity", {"value": value.value})
        if type(value) is a.ArtifactManifestEntryIdentity:
            return cls._record("ArtifactManifestEntryIdentity", {"value": value.value})
        if type(value) is a.ArtifactProducerProvenanceIdentity:
            return cls._record(
                "ArtifactProducerProvenanceIdentity", {"value": value.value}
            )
        if type(value) is c.QuantumEspressoExecutionInputIdentity:
            return cls._record(
                "QuantumEspressoExecutionInputIdentity", {"value": value.value}
            )
        if type(value) is c.QuantumEspressoExecutableConfigurationIdentity:
            return cls._record(
                "QuantumEspressoExecutableConfigurationIdentity", {"value": value.value}
            )
        if type(value) is c.QuantumEspressoPreparationIdentity:
            return cls._record(
                "QuantumEspressoPreparationIdentity", {"value": value.value}
            )
        if type(value) is c.QuantumEspressoProcessObservationIdentity:
            return cls._record(
                "QuantumEspressoProcessObservationIdentity", {"value": value.value}
            )
        if type(value) is c.QuantumEspressoDiagnosticClassifierIdentity:
            return cls._record(
                "QuantumEspressoDiagnosticClassifierIdentity", {"value": value.value}
            )
        if type(value) is c.QuantumEspressoDiagnosticObservationIdentity:
            return cls._record(
                "QuantumEspressoDiagnosticObservationIdentity", {"value": value.value}
            )
        if type(value) is c.QuantumEspressoOutputMarkerObservationIdentity:
            return cls._record(
                "QuantumEspressoOutputMarkerObservationIdentity", {"value": value.value}
            )
        if type(value) is c.QuantumEspressoDiagnosticReportIdentity:
            return cls._record(
                "QuantumEspressoDiagnosticReportIdentity", {"value": value.value}
            )
        if type(value) is c.QuantumEspressoTerminalRecordIdentity:
            return cls._record(
                "QuantumEspressoTerminalRecordIdentity", {"value": value.value}
            )
        if type(value) is c.QuantumEspressoArtifactDestination:
            return cls._record(
                "QuantumEspressoArtifactDestination", {"value": value.value}
            )
        if type(value) is o.QuantumEspressoParsedDocumentIdentity:
            return cls._record(
                "QuantumEspressoParsedDocumentIdentity", {"value": value.value}
            )
        if type(value) is o.QuantumEspressoXsdParserIdentity:
            return cls._record(
                "QuantumEspressoXsdParserIdentity", {"value": value.value}
            )
        if type(value) is o.QuantumEspressoObservationNormalizationPolicyIdentity:
            return cls._record(
                "QuantumEspressoObservationNormalizationPolicyIdentity",
                {"value": value.value},
            )
        if type(value) is c.QuantumEspressoProgram:
            return cls._record("QuantumEspressoProgram", {"value": value.value})
        if type(value) is c.QuantumEspressoExecutableKind:
            return cls._record("QuantumEspressoExecutableKind", {"value": value.value})
        if type(value) is c.QuantumEspressoDiagnosticChannel:
            return cls._record(
                "QuantumEspressoDiagnosticChannel", {"value": value.value}
            )
        if type(value) is c.QuantumEspressoDiagnosticDisposition:
            return cls._record(
                "QuantumEspressoDiagnosticDisposition", {"value": value.value}
            )
        if type(value) is c.QuantumEspressoDiagnosticReportKind:
            return cls._record(
                "QuantumEspressoDiagnosticReportKind", {"value": value.value}
            )
        if type(value) is c.QuantumEspressoProcessFailureKind:
            return cls._record(
                "QuantumEspressoProcessFailureKind", {"value": value.value}
            )
        if type(value) is a.ArtifactContentIdentity:
            return cls._record(
                "ArtifactContentIdentity",
                {
                    "algorithm": value.algorithm,
                    "digest": value.digest,
                    "byte_count": value.byte_count,
                },
            )
        if type(value) is c.QuantumEspressoFileArtifactContent:
            return cls._record(
                "QuantumEspressoFileArtifactContent",
                {"content_identity": value.content_identity},
            )
        if type(value) is c.QuantumEspressoTreeArtifactContent:
            return cls._record(
                "QuantumEspressoTreeArtifactContent",
                {
                    "manifest_identity": value.manifest_identity,
                    "manifest_entry_identities": value.manifest_entry_identities,
                },
            )
        if type(value) is c.QuantumEspressoNativeInputArtifact:
            return cls._record(
                "QuantumEspressoNativeInputArtifact",
                {
                    "identity": value.identity,
                    "content": value.content,
                    "destination": value.destination,
                },
            )
        if type(value) is c.QuantumEspressoPseudopotentialArtifact:
            return cls._record(
                "QuantumEspressoPseudopotentialArtifact",
                {
                    "identity": value.identity,
                    "content": value.content,
                    "destination": value.destination,
                },
            )
        if type(value) is c.QuantumEspressoPredecessorNativeStateArtifact:
            return cls._record(
                "QuantumEspressoPredecessorNativeStateArtifact",
                {
                    "identity": value.identity,
                    "content": value.content,
                    "destination": value.destination,
                    "predecessor_result_identity": value.predecessor_result_identity,
                    "predecessor_manifest_entry_identity": (
                        value.predecessor_manifest_entry_identity
                    ),
                },
            )
        if type(value) is c.QuantumEspressoExecutionInput:
            return cls._record(
                "QuantumEspressoExecutionInput",
                {
                    "identity": value.identity,
                    "program": value.program,
                    "native_input": value.native_input,
                    "pseudopotentials": value.pseudopotentials,
                    "predecessor_native_state": value.predecessor_native_state,
                    "task_definition_identity": value.task_definition_identity,
                    "task_instance_identity": value.task_instance_identity,
                    "activation_identity": value.activation_identity,
                    "operation_identity": value.operation_identity,
                    "attempt_identity": value.attempt_identity,
                    "contract_version": value.contract_version,
                },
            )
        if type(value) is c.QuantumEspressoStreamObservation:
            return cls._record(
                "QuantumEspressoStreamObservation",
                {
                    "channel": value.channel,
                    "artifact_identity": value.artifact_identity,
                    "content_identity": value.content_identity,
                },
            )
        if type(value) is c.QuantumEspressoNormalProcessExit:
            return cls._record(
                "QuantumEspressoNormalProcessExit", {"exit_code": value.exit_code}
            )
        if type(value) is c.QuantumEspressoProcessSignalTermination:
            return cls._record(
                "QuantumEspressoProcessSignalTermination",
                {"signal_number": value.signal_number},
            )
        if type(value) is c.QuantumEspressoProcessTimeout:
            return cls._record(
                "QuantumEspressoProcessTimeout",
                {
                    "timeout_milliseconds": value.timeout_milliseconds,
                    "termination_sent": value.termination_sent,
                    "kill_sent": value.kill_sent,
                },
            )
        if type(value) is c.QuantumEspressoProcessObservation:
            return cls._record(
                "QuantumEspressoProcessObservation",
                {
                    "identity": value.identity,
                    "execution_input_identity": value.execution_input_identity,
                    "executable_configuration_identity": (
                        value.executable_configuration_identity
                    ),
                    "preparation_identity": value.preparation_identity,
                    "attempt_identity": value.attempt_identity,
                    "argv_content_identity": value.argv_content_identity,
                    "termination": value.termination,
                    "wall_duration_nanoseconds": value.wall_duration_nanoseconds,
                    "stdout": value.stdout,
                    "stderr": value.stderr,
                    "before_snapshot_identity": value.before_snapshot_identity,
                    "after_snapshot_identity": value.after_snapshot_identity,
                    "created_entry_count": value.created_entry_count,
                    "created_total_bytes": value.created_total_bytes,
                    "peak_resident_bytes": value.peak_resident_bytes,
                    "observer_version": value.observer_version,
                },
            )
        if type(value) is c.QuantumEspressoDiagnosticObservation:
            return cls._record(
                "QuantumEspressoDiagnosticObservation",
                {
                    "identity": value.identity,
                    "channel": value.channel,
                    "byte_start": value.byte_start,
                    "byte_end": value.byte_end,
                    "stream_content_identity": value.stream_content_identity,
                    "span_content_identity": value.span_content_identity,
                    "signature_identity": value.signature_identity,
                    "disposition": value.disposition,
                    "sanitized_summary": value.sanitized_summary,
                    "claim_boundary": value.claim_boundary,
                },
            )
        if type(value) is c.QuantumEspressoOutputMarkerObservation:
            return cls._record(
                "QuantumEspressoOutputMarkerObservation",
                {
                    "identity": value.identity,
                    "channel": value.channel,
                    "byte_start": value.byte_start,
                    "byte_end": value.byte_end,
                    "stream_content_identity": value.stream_content_identity,
                    "span_content_identity": value.span_content_identity,
                    "signature_identity": value.signature_identity,
                },
            )
        if type(value) is c.QuantumEspressoDiagnosticReport:
            return cls._record(
                "QuantumEspressoDiagnosticReport",
                {
                    "identity": value.identity,
                    "classifier_identity": value.classifier_identity,
                    "executable_configuration_identity": (
                        value.executable_configuration_identity
                    ),
                    "executable_kind": value.executable_kind,
                    "program": value.program,
                    "program_version": value.program_version,
                    "stdout_content_identity": value.stdout_content_identity,
                    "stderr_content_identity": value.stderr_content_identity,
                    "observations": value.observations,
                    "completion_markers": value.completion_markers,
                    "kind": value.kind,
                    "claim_boundary": value.claim_boundary,
                },
            )
        if type(value) is c.QuantumEspressoCompletedOutcome:
            return cls._record(
                "QuantumEspressoCompletedOutcome",
                {"completion_marker_identities": value.completion_marker_identities},
            )
        if type(value) is c.QuantumEspressoCalculatorFailedOutcome:
            return cls._record(
                "QuantumEspressoCalculatorFailedOutcome",
                {"fatal_diagnostic_identities": value.fatal_diagnostic_identities},
            )
        if type(value) is c.QuantumEspressoProcessFailedOutcome:
            return cls._record(
                "QuantumEspressoProcessFailedOutcome", {"reason": value.reason}
            )
        if type(value) is c.QuantumEspressoDiagnosticUnresolvedOutcome:
            return cls._record(
                "QuantumEspressoDiagnosticUnresolvedOutcome",
                {
                    "diagnostic_identities": value.diagnostic_identities,
                    "reason_identities": value.reason_identities,
                },
            )
        if type(value) is c.QuantumEspressoOperationResultEvidence:
            return cls._record(
                "QuantumEspressoOperationResultEvidence",
                {
                    "execution_input": value.execution_input,
                    "process_observation": value.process_observation,
                    "diagnostic_report": value.diagnostic_report,
                    "calculator_outcome": value.calculator_outcome,
                    "native_output_manifest_identity": (
                        value.native_output_manifest_identity
                    ),
                    "native_output_entry_identities": (
                        value.native_output_entry_identities
                    ),
                    "terminal_record_identity": value.terminal_record_identity,
                },
            )
        if type(value) is c.QuantumEspressoPwResult:
            return cls._record(
                "QuantumEspressoPwResult",
                {
                    "identity": value.identity,
                    "evidence": value.evidence,
                    "contract_version": value.contract_version,
                },
            )
        if type(value) is c.QuantumEspressoBandsResult:
            return cls._record(
                "QuantumEspressoBandsResult",
                {
                    "identity": value.identity,
                    "evidence": value.evidence,
                    "contract_version": value.contract_version,
                },
            )
        if type(value) is o.QuantumEspressoObservationNormalizationPolicy:
            return cls._record(
                "QuantumEspressoObservationNormalizationPolicy",
                {"identity": value.identity, "version": value.version},
            )
        if type(value) is KohnShamPlaneWaveCalculationRecord:
            return cls._record(
                "KohnShamPlaneWaveCalculationRecord",
                {
                    "json": KohnShamPlaneWaveCalculationRecordJsonSerializer(
                        1.0e-12
                    ).serialize(value)
                },
            )
        if type(value) is o.QuantumEspressoExtractedObservationResult:
            return cls._record(
                "QuantumEspressoExtractedObservationResult",
                {
                    "identity": value.identity,
                    "observation": value.observation,
                    "source_manifest_identity": value.source_manifest_identity,
                    "source_manifest_entry_identity": (
                        value.source_manifest_entry_identity
                    ),
                    "source_artifact_identity": value.source_artifact_identity,
                    "source_content_identity": value.source_content_identity,
                    "source_producer_provenance_identity": (
                        value.source_producer_provenance_identity
                    ),
                    "parsed_document_identity": value.parsed_document_identity,
                    "parser_identity": value.parser_identity,
                    "parser_version": value.parser_version,
                    "normalization_policy": value.normalization_policy,
                    "limitation_values": value.limitation_values,
                },
            )
        raise TypeError("unsupported exact nested value")

    @staticmethod
    def _fields(value: _Json, names: tuple[str, ...]) -> dict[str, _Json]:
        if not isinstance(value, dict) or set(value) != {"type", "fields"}:
            raise ValueError("wrong record shape")
        fields = value["fields"]
        if not isinstance(fields, dict) or set(fields) != set(names):
            raise ValueError("wrong field inventory")
        return fields

    @staticmethod
    def _string(value: _Json) -> str:
        if type(value) is not str:
            raise TypeError("expected exact string")
        return value

    @classmethod
    def _as[T: _Node](cls, value: _Json, expected: type[T]) -> T:
        decoded = cls._decode_node(value)
        if type(decoded) is not expected:
            raise TypeError("wrong nominal or field type")
        return cast(T, decoded)

    @classmethod
    def _tuple_as[T: _Node](cls, value: _Json, expected: type[T]) -> tuple[T, ...]:
        if not isinstance(value, list):
            raise TypeError("expected ordered array")
        return tuple(cls._as(item, expected) for item in value)

    @classmethod
    def _termination(cls, value: _Json) -> c.QuantumEspressoProcessTermination:
        decoded = cls._decode_node(value)
        if type(decoded) not in (
            c.QuantumEspressoNormalProcessExit,
            c.QuantumEspressoProcessSignalTermination,
            c.QuantumEspressoProcessTimeout,
        ):
            raise TypeError("wrong termination variant")
        return cast(c.QuantumEspressoProcessTermination, decoded)

    @classmethod
    def _outcome(cls, value: _Json) -> c.QuantumEspressoCalculatorOutcome:
        decoded = cls._decode_node(value)
        if type(decoded) not in (
            c.QuantumEspressoCompletedOutcome,
            c.QuantumEspressoCalculatorFailedOutcome,
            c.QuantumEspressoProcessFailedOutcome,
            c.QuantumEspressoDiagnosticUnresolvedOutcome,
        ):
            raise TypeError("wrong outcome variant")
        return cast(c.QuantumEspressoCalculatorOutcome, decoded)

    @classmethod
    def _version(cls, value: _Json, expected: str) -> str:
        version = cls._string(value)
        if version != expected:
            raise _UnsupportedVersion("unsupported owned version")
        return version

    @classmethod
    def _decode_node(cls, value: _Json) -> _Node:
        if value is None or type(value) is bool or type(value) is str:
            return value
        if isinstance(value, list):
            return tuple(cls._decode_node(item) for item in value)
        if not isinstance(value, dict):
            raise TypeError("expected record")
        tag = cls._string(value.get("type"))
        if tag == "int":
            f = cls._fields(value, ("value",))
            text = cls._string(f["value"])
            number = int(text, 16)
            if hex(number) != text:
                raise ValueError("noncanonical integer")
            return number
        if tag in (
            "ResultObjectIdentity",
            "AttemptIdentity",
            "OperationIdentity",
            "TaskActivationIdentity",
            "TaskDefinitionIdentity",
            "TaskInstanceIdentity",
            "ArtifactIdentity",
            "ArtifactManifestIdentity",
            "ArtifactManifestEntryIdentity",
            "ArtifactProducerProvenanceIdentity",
            "QuantumEspressoExecutionInputIdentity",
            "QuantumEspressoExecutableConfigurationIdentity",
            "QuantumEspressoPreparationIdentity",
            "QuantumEspressoProcessObservationIdentity",
            "QuantumEspressoDiagnosticClassifierIdentity",
            "QuantumEspressoDiagnosticObservationIdentity",
            "QuantumEspressoOutputMarkerObservationIdentity",
            "QuantumEspressoDiagnosticReportIdentity",
            "QuantumEspressoTerminalRecordIdentity",
            "QuantumEspressoArtifactDestination",
            "QuantumEspressoParsedDocumentIdentity",
            "QuantumEspressoXsdParserIdentity",
            "QuantumEspressoObservationNormalizationPolicyIdentity",
            "QuantumEspressoProgram",
            "QuantumEspressoExecutableKind",
            "QuantumEspressoDiagnosticChannel",
            "QuantumEspressoDiagnosticDisposition",
            "QuantumEspressoDiagnosticReportKind",
            "QuantumEspressoProcessFailureKind",
        ):
            text = cls._string(cls._fields(value, ("value",))["value"])
            if tag == "ResultObjectIdentity":
                return m.ResultObjectIdentity(text)
            if tag == "AttemptIdentity":
                return m.AttemptIdentity(text)
            if tag == "OperationIdentity":
                return m.OperationIdentity(text)
            if tag == "TaskActivationIdentity":
                return m.TaskActivationIdentity(text)
            if tag == "TaskDefinitionIdentity":
                return m.TaskDefinitionIdentity(text)
            if tag == "TaskInstanceIdentity":
                return m.TaskInstanceIdentity(text)
            if tag == "ArtifactIdentity":
                return a.ArtifactIdentity(text)
            if tag == "ArtifactManifestIdentity":
                return a.ArtifactManifestIdentity(text)
            if tag == "ArtifactManifestEntryIdentity":
                return a.ArtifactManifestEntryIdentity(text)
            if tag == "ArtifactProducerProvenanceIdentity":
                return a.ArtifactProducerProvenanceIdentity(text)
            if tag == "QuantumEspressoExecutionInputIdentity":
                return c.QuantumEspressoExecutionInputIdentity(text)
            if tag == "QuantumEspressoExecutableConfigurationIdentity":
                return c.QuantumEspressoExecutableConfigurationIdentity(text)
            if tag == "QuantumEspressoPreparationIdentity":
                return c.QuantumEspressoPreparationIdentity(text)
            if tag == "QuantumEspressoProcessObservationIdentity":
                return c.QuantumEspressoProcessObservationIdentity(text)
            if tag == "QuantumEspressoDiagnosticClassifierIdentity":
                return c.QuantumEspressoDiagnosticClassifierIdentity(text)
            if tag == "QuantumEspressoDiagnosticObservationIdentity":
                return c.QuantumEspressoDiagnosticObservationIdentity(text)
            if tag == "QuantumEspressoOutputMarkerObservationIdentity":
                return c.QuantumEspressoOutputMarkerObservationIdentity(text)
            if tag == "QuantumEspressoDiagnosticReportIdentity":
                return c.QuantumEspressoDiagnosticReportIdentity(text)
            if tag == "QuantumEspressoTerminalRecordIdentity":
                return c.QuantumEspressoTerminalRecordIdentity(text)
            if tag == "QuantumEspressoArtifactDestination":
                return c.QuantumEspressoArtifactDestination(text)
            if tag == "QuantumEspressoParsedDocumentIdentity":
                return o.QuantumEspressoParsedDocumentIdentity(text)
            if tag == "QuantumEspressoXsdParserIdentity":
                return o.QuantumEspressoXsdParserIdentity(text)
            if tag == "QuantumEspressoObservationNormalizationPolicyIdentity":
                return o.QuantumEspressoObservationNormalizationPolicyIdentity(text)
            if tag == "QuantumEspressoProgram":
                return c.QuantumEspressoProgram(text)
            if tag == "QuantumEspressoExecutableKind":
                return c.QuantumEspressoExecutableKind(text)
            if tag == "QuantumEspressoDiagnosticChannel":
                return c.QuantumEspressoDiagnosticChannel(text)
            if tag == "QuantumEspressoDiagnosticDisposition":
                return c.QuantumEspressoDiagnosticDisposition(text)
            if tag == "QuantumEspressoDiagnosticReportKind":
                return c.QuantumEspressoDiagnosticReportKind(text)
            if tag == "QuantumEspressoProcessFailureKind":
                return c.QuantumEspressoProcessFailureKind(text)
        if tag == "ArtifactContentIdentity":
            f = cls._fields(value, ("algorithm", "digest", "byte_count"))
            return a.ArtifactContentIdentity(
                cls._string(f["algorithm"]),
                cls._string(f["digest"]),
                cls._as(f["byte_count"], int),
            )
        if tag == "QuantumEspressoFileArtifactContent":
            f = cls._fields(value, ("content_identity",))
            return c.QuantumEspressoFileArtifactContent(
                cls._as(f["content_identity"], a.ArtifactContentIdentity)
            )
        if tag == "QuantumEspressoTreeArtifactContent":
            f = cls._fields(value, ("manifest_identity", "manifest_entry_identities"))
            return c.QuantumEspressoTreeArtifactContent(
                cls._as(f["manifest_identity"], a.ArtifactManifestIdentity),
                cls._tuple_as(
                    f["manifest_entry_identities"], a.ArtifactManifestEntryIdentity
                ),
            )
        if tag == "QuantumEspressoNativeInputArtifact":
            f = cls._fields(value, ("identity", "content", "destination"))
            return c.QuantumEspressoNativeInputArtifact(
                cls._as(f["identity"], a.ArtifactIdentity),
                cls._as(f["content"], c.QuantumEspressoFileArtifactContent),
                cls._as(f["destination"], c.QuantumEspressoArtifactDestination),
            )
        if tag == "QuantumEspressoPseudopotentialArtifact":
            f = cls._fields(value, ("identity", "content", "destination"))
            return c.QuantumEspressoPseudopotentialArtifact(
                cls._as(f["identity"], a.ArtifactIdentity),
                cls._as(f["content"], c.QuantumEspressoFileArtifactContent),
                cls._as(f["destination"], c.QuantumEspressoArtifactDestination),
            )
        if tag == "QuantumEspressoPredecessorNativeStateArtifact":
            f = cls._fields(
                value,
                (
                    "identity",
                    "content",
                    "destination",
                    "predecessor_result_identity",
                    "predecessor_manifest_entry_identity",
                ),
            )
            return c.QuantumEspressoPredecessorNativeStateArtifact(
                cls._as(f["identity"], a.ArtifactIdentity),
                cls._as(f["content"], c.QuantumEspressoTreeArtifactContent),
                cls._as(f["destination"], c.QuantumEspressoArtifactDestination),
                cls._as(f["predecessor_result_identity"], m.ResultObjectIdentity),
                cls._as(
                    f["predecessor_manifest_entry_identity"],
                    a.ArtifactManifestEntryIdentity,
                ),
            )
        if tag == "QuantumEspressoExecutionInput":
            f = cls._fields(
                value,
                (
                    "identity",
                    "program",
                    "native_input",
                    "pseudopotentials",
                    "predecessor_native_state",
                    "task_definition_identity",
                    "task_instance_identity",
                    "activation_identity",
                    "operation_identity",
                    "attempt_identity",
                    "contract_version",
                ),
            )
            version = cls._version(f["contract_version"], "qe-execution-input:1")
            return c.QuantumEspressoExecutionInput(
                identity=cls._as(
                    f["identity"], c.QuantumEspressoExecutionInputIdentity
                ),
                program=cls._as(f["program"], c.QuantumEspressoProgram),
                native_input=cls._as(
                    f["native_input"], c.QuantumEspressoNativeInputArtifact
                ),
                pseudopotentials=cls._tuple_as(
                    f["pseudopotentials"], c.QuantumEspressoPseudopotentialArtifact
                ),
                predecessor_native_state=cls._tuple_as(
                    f["predecessor_native_state"],
                    c.QuantumEspressoPredecessorNativeStateArtifact,
                ),
                task_definition_identity=cls._as(
                    f["task_definition_identity"], m.TaskDefinitionIdentity
                ),
                task_instance_identity=cls._as(
                    f["task_instance_identity"], m.TaskInstanceIdentity
                ),
                activation_identity=cls._as(
                    f["activation_identity"], m.TaskActivationIdentity
                ),
                operation_identity=cls._as(
                    f["operation_identity"], m.OperationIdentity
                ),
                attempt_identity=cls._as(f["attempt_identity"], m.AttemptIdentity),
                contract_version=version,
            )
        if tag == "QuantumEspressoStreamObservation":
            f = cls._fields(value, ("channel", "artifact_identity", "content_identity"))
            return c.QuantumEspressoStreamObservation(
                channel=cls._as(f["channel"], c.QuantumEspressoDiagnosticChannel),
                artifact_identity=cls._as(f["artifact_identity"], a.ArtifactIdentity),
                content_identity=cls._as(
                    f["content_identity"], a.ArtifactContentIdentity
                ),
            )
        if tag == "QuantumEspressoNormalProcessExit":
            f = cls._fields(value, ("exit_code",))
            return c.QuantumEspressoNormalProcessExit(cls._as(f["exit_code"], int))
        if tag == "QuantumEspressoProcessSignalTermination":
            f = cls._fields(value, ("signal_number",))
            return c.QuantumEspressoProcessSignalTermination(
                cls._as(f["signal_number"], int)
            )
        if tag == "QuantumEspressoProcessTimeout":
            f = cls._fields(
                value, ("timeout_milliseconds", "termination_sent", "kill_sent")
            )
            return c.QuantumEspressoProcessTimeout(
                timeout_milliseconds=cls._as(f["timeout_milliseconds"], int),
                termination_sent=cls._as(f["termination_sent"], bool),
                kill_sent=cls._as(f["kill_sent"], bool),
            )
        if tag == "QuantumEspressoProcessObservation":
            f = cls._fields(
                value,
                (
                    "identity",
                    "execution_input_identity",
                    "executable_configuration_identity",
                    "preparation_identity",
                    "attempt_identity",
                    "argv_content_identity",
                    "termination",
                    "wall_duration_nanoseconds",
                    "stdout",
                    "stderr",
                    "before_snapshot_identity",
                    "after_snapshot_identity",
                    "created_entry_count",
                    "created_total_bytes",
                    "peak_resident_bytes",
                    "observer_version",
                ),
            )
            return c.QuantumEspressoProcessObservation(
                identity=cls._as(
                    f["identity"], c.QuantumEspressoProcessObservationIdentity
                ),
                execution_input_identity=cls._as(
                    f["execution_input_identity"],
                    c.QuantumEspressoExecutionInputIdentity,
                ),
                executable_configuration_identity=cls._as(
                    f["executable_configuration_identity"],
                    c.QuantumEspressoExecutableConfigurationIdentity,
                ),
                preparation_identity=cls._as(
                    f["preparation_identity"], c.QuantumEspressoPreparationIdentity
                ),
                attempt_identity=cls._as(f["attempt_identity"], m.AttemptIdentity),
                argv_content_identity=cls._as(
                    f["argv_content_identity"], a.ArtifactContentIdentity
                ),
                termination=cls._termination(f["termination"]),
                wall_duration_nanoseconds=cls._as(f["wall_duration_nanoseconds"], int),
                stdout=cls._as(f["stdout"], c.QuantumEspressoStreamObservation),
                stderr=cls._as(f["stderr"], c.QuantumEspressoStreamObservation),
                before_snapshot_identity=cls._as(
                    f["before_snapshot_identity"], a.ArtifactManifestIdentity
                ),
                after_snapshot_identity=cls._as(
                    f["after_snapshot_identity"], a.ArtifactManifestIdentity
                ),
                created_entry_count=cls._as(f["created_entry_count"], int),
                created_total_bytes=cls._as(f["created_total_bytes"], int),
                peak_resident_bytes=None
                if f["peak_resident_bytes"] is None
                else cls._as(f["peak_resident_bytes"], int),
                observer_version=cls._string(f["observer_version"]),
            )
        if tag == "QuantumEspressoDiagnosticObservation":
            f = cls._fields(
                value,
                (
                    "identity",
                    "channel",
                    "byte_start",
                    "byte_end",
                    "stream_content_identity",
                    "span_content_identity",
                    "signature_identity",
                    "disposition",
                    "sanitized_summary",
                    "claim_boundary",
                ),
            )
            return c.QuantumEspressoDiagnosticObservation(
                identity=cls._as(
                    f["identity"], c.QuantumEspressoDiagnosticObservationIdentity
                ),
                channel=cls._as(f["channel"], c.QuantumEspressoDiagnosticChannel),
                byte_start=cls._as(f["byte_start"], int),
                byte_end=cls._as(f["byte_end"], int),
                stream_content_identity=cls._as(
                    f["stream_content_identity"], a.ArtifactContentIdentity
                ),
                span_content_identity=cls._as(
                    f["span_content_identity"], a.ArtifactContentIdentity
                ),
                signature_identity=None
                if f["signature_identity"] is None
                else cls._string(f["signature_identity"]),
                disposition=cls._as(
                    f["disposition"], c.QuantumEspressoDiagnosticDisposition
                ),
                sanitized_summary=cls._string(f["sanitized_summary"]),
                claim_boundary=cls._tuple_as(f["claim_boundary"], str),
            )
        if tag == "QuantumEspressoOutputMarkerObservation":
            f = cls._fields(
                value,
                (
                    "identity",
                    "channel",
                    "byte_start",
                    "byte_end",
                    "stream_content_identity",
                    "span_content_identity",
                    "signature_identity",
                ),
            )
            return c.QuantumEspressoOutputMarkerObservation(
                identity=cls._as(
                    f["identity"], c.QuantumEspressoOutputMarkerObservationIdentity
                ),
                channel=cls._as(f["channel"], c.QuantumEspressoDiagnosticChannel),
                byte_start=cls._as(f["byte_start"], int),
                byte_end=cls._as(f["byte_end"], int),
                stream_content_identity=cls._as(
                    f["stream_content_identity"], a.ArtifactContentIdentity
                ),
                span_content_identity=cls._as(
                    f["span_content_identity"], a.ArtifactContentIdentity
                ),
                signature_identity=cls._string(f["signature_identity"]),
            )
        if tag == "QuantumEspressoDiagnosticReport":
            f = cls._fields(
                value,
                (
                    "identity",
                    "classifier_identity",
                    "executable_configuration_identity",
                    "executable_kind",
                    "program",
                    "program_version",
                    "stdout_content_identity",
                    "stderr_content_identity",
                    "observations",
                    "completion_markers",
                    "kind",
                    "claim_boundary",
                ),
            )
            return c.QuantumEspressoDiagnosticReport(
                identity=cls._as(
                    f["identity"], c.QuantumEspressoDiagnosticReportIdentity
                ),
                classifier_identity=cls._as(
                    f["classifier_identity"],
                    c.QuantumEspressoDiagnosticClassifierIdentity,
                ),
                executable_configuration_identity=cls._as(
                    f["executable_configuration_identity"],
                    c.QuantumEspressoExecutableConfigurationIdentity,
                ),
                executable_kind=cls._as(
                    f["executable_kind"], c.QuantumEspressoExecutableKind
                ),
                program=cls._as(f["program"], c.QuantumEspressoProgram),
                program_version=cls._string(f["program_version"]),
                stdout_content_identity=cls._as(
                    f["stdout_content_identity"], a.ArtifactContentIdentity
                ),
                stderr_content_identity=cls._as(
                    f["stderr_content_identity"], a.ArtifactContentIdentity
                ),
                observations=cls._tuple_as(
                    f["observations"], c.QuantumEspressoDiagnosticObservation
                ),
                completion_markers=cls._tuple_as(
                    f["completion_markers"], c.QuantumEspressoOutputMarkerObservation
                ),
                kind=cls._as(f["kind"], c.QuantumEspressoDiagnosticReportKind),
                claim_boundary=cls._tuple_as(f["claim_boundary"], str),
            )
        if tag == "QuantumEspressoCompletedOutcome":
            f = cls._fields(value, ("completion_marker_identities",))
            return c.QuantumEspressoCompletedOutcome(
                cls._tuple_as(
                    f["completion_marker_identities"],
                    c.QuantumEspressoOutputMarkerObservationIdentity,
                )
            )
        if tag == "QuantumEspressoCalculatorFailedOutcome":
            f = cls._fields(value, ("fatal_diagnostic_identities",))
            return c.QuantumEspressoCalculatorFailedOutcome(
                cls._tuple_as(
                    f["fatal_diagnostic_identities"],
                    c.QuantumEspressoDiagnosticObservationIdentity,
                )
            )
        if tag == "QuantumEspressoProcessFailedOutcome":
            f = cls._fields(value, ("reason",))
            return c.QuantumEspressoProcessFailedOutcome(
                cls._as(f["reason"], c.QuantumEspressoProcessFailureKind)
            )
        if tag == "QuantumEspressoDiagnosticUnresolvedOutcome":
            f = cls._fields(value, ("diagnostic_identities", "reason_identities"))
            return c.QuantumEspressoDiagnosticUnresolvedOutcome(
                cls._tuple_as(
                    f["diagnostic_identities"],
                    c.QuantumEspressoDiagnosticObservationIdentity,
                ),
                cls._tuple_as(f["reason_identities"], str),
            )
        if tag == "QuantumEspressoOperationResultEvidence":
            f = cls._fields(
                value,
                (
                    "execution_input",
                    "process_observation",
                    "diagnostic_report",
                    "calculator_outcome",
                    "native_output_manifest_identity",
                    "native_output_entry_identities",
                    "terminal_record_identity",
                ),
            )
            return c.QuantumEspressoOperationResultEvidence(
                execution_input=cls._as(
                    f["execution_input"], c.QuantumEspressoExecutionInput
                ),
                process_observation=cls._as(
                    f["process_observation"], c.QuantumEspressoProcessObservation
                ),
                diagnostic_report=cls._as(
                    f["diagnostic_report"], c.QuantumEspressoDiagnosticReport
                ),
                calculator_outcome=cls._outcome(f["calculator_outcome"]),
                native_output_manifest_identity=cls._as(
                    f["native_output_manifest_identity"], a.ArtifactManifestIdentity
                ),
                native_output_entry_identities=cls._tuple_as(
                    f["native_output_entry_identities"], a.ArtifactManifestEntryIdentity
                ),
                terminal_record_identity=cls._as(
                    f["terminal_record_identity"],
                    c.QuantumEspressoTerminalRecordIdentity,
                ),
            )
        if tag == "QuantumEspressoPwResult":
            f = cls._fields(value, ("identity", "evidence", "contract_version"))
            version = cls._version(f["contract_version"], "qe-pw-result:1")
            return c.QuantumEspressoPwResult(
                identity=cls._as(f["identity"], m.ResultObjectIdentity),
                evidence=cls._as(
                    f["evidence"], c.QuantumEspressoOperationResultEvidence
                ),
                contract_version=version,
            )
        if tag == "QuantumEspressoBandsResult":
            f = cls._fields(value, ("identity", "evidence", "contract_version"))
            version = cls._version(f["contract_version"], "qe-bands-result:1")
            return c.QuantumEspressoBandsResult(
                identity=cls._as(f["identity"], m.ResultObjectIdentity),
                evidence=cls._as(
                    f["evidence"], c.QuantumEspressoOperationResultEvidence
                ),
                contract_version=version,
            )
        if tag == "QuantumEspressoObservationNormalizationPolicy":
            f = cls._fields(value, ("identity", "version"))
            return o.QuantumEspressoObservationNormalizationPolicy(
                cls._as(
                    f["identity"],
                    o.QuantumEspressoObservationNormalizationPolicyIdentity,
                ),
                cls._version(f["version"], "1"),
            )
        if tag == "KohnShamPlaneWaveCalculationRecord":
            f = cls._fields(value, ("json",))
            text = cls._string(f["json"])
            # Only dispatch on the neutral owner's schema; its serializer performs
            # all representation, tolerance and scientific-record checks unchanged.
            neutral = cast(JsonRepresentation, json.loads(text))
            if (
                isinstance(neutral, dict)
                and type(neutral.get("schema_version")) is int
                and neutral["schema_version"] != 1
            ):
                raise _UnsupportedVersion("unsupported neutral schema")
            return KohnShamPlaneWaveCalculationRecordJsonSerializer(
                1.0e-12
            ).deserialize(text)
        if tag == "QuantumEspressoExtractedObservationResult":
            f = cls._fields(
                value,
                (
                    "identity",
                    "observation",
                    "source_manifest_identity",
                    "source_manifest_entry_identity",
                    "source_artifact_identity",
                    "source_content_identity",
                    "source_producer_provenance_identity",
                    "parsed_document_identity",
                    "parser_identity",
                    "parser_version",
                    "normalization_policy",
                    "limitation_values",
                ),
            )
            version = cls._version(f["parser_version"], "1")
            return o.QuantumEspressoExtractedObservationResult(
                identity=cls._as(f["identity"], m.ResultObjectIdentity),
                observation=cls._as(
                    f["observation"], KohnShamPlaneWaveCalculationRecord
                ),
                source_manifest_identity=cls._as(
                    f["source_manifest_identity"], a.ArtifactManifestIdentity
                ),
                source_manifest_entry_identity=cls._as(
                    f["source_manifest_entry_identity"], a.ArtifactManifestEntryIdentity
                ),
                source_artifact_identity=cls._as(
                    f["source_artifact_identity"], a.ArtifactIdentity
                ),
                source_content_identity=cls._as(
                    f["source_content_identity"], a.ArtifactContentIdentity
                ),
                source_producer_provenance_identity=cls._as(
                    f["source_producer_provenance_identity"],
                    a.ArtifactProducerProvenanceIdentity,
                ),
                parsed_document_identity=cls._as(
                    f["parsed_document_identity"],
                    o.QuantumEspressoParsedDocumentIdentity,
                ),
                parser_identity=cls._as(
                    f["parser_identity"], o.QuantumEspressoXsdParserIdentity
                ),
                parser_version=version,
                normalization_policy=cls._as(
                    f["normalization_policy"],
                    o.QuantumEspressoObservationNormalizationPolicy,
                ),
                limitation_values=cls._tuple_as(f["limitation_values"], str),
            )
        raise ValueError("unknown nested record tag")
