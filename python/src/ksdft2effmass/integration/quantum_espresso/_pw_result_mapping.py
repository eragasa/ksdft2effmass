"""Typed-mapping boundary for the ``QePwResult`` persistence payload."""

from __future__ import annotations

from collections.abc import Mapping

from projectkoios.simulations.execution import CalculatorExitCode

from ksdft2effmass.serialization import SerializableValue
from ksdft2effmass.workflows import (
    ArtifactContentIdentity,
    ArtifactIdentity,
    ArtifactManifestEntryIdentity,
    ArtifactManifestIdentity,
    AttemptIdentity,
    OperationIdentity,
    ResultObjectIdentity,
    TaskActivationIdentity,
    TaskDefinitionIdentity,
    TaskInstanceIdentity,
)

from .contracts import (
    QeArtifactDestination,
    QeCalculatorFailedOutcome,
    QeCalculatorOutcome,
    QeCompletedOutcome,
    QeDiagnosticChannel,
    QeDiagnosticClassifierIdentity,
    QeDiagnosticDisposition,
    QeDiagnosticObservation,
    QeDiagnosticObservationIdentity,
    QeDiagnosticReport,
    QeDiagnosticReportIdentity,
    QeDiagnosticReportKind,
    QeDiagnosticUnresolvedOutcome,
    QeExecutableConfigurationIdentity,
    QeExecutableKind,
    QeExecutionInput,
    QeExecutionInputIdentity,
    QeFileArtifactContent,
    QeNativeInputArtifact,
    QeNormalProcessExit,
    QeOutputMarkerObservation,
    QeOutputMarkerObservationIdentity,
    QePredecessorNativeStateArtifact,
    QePreparationIdentity,
    QeProcessFailedOutcome,
    QeProcessFailureKind,
    QeProcessObservation,
    QeProcessObservationIdentity,
    QeProcessSignalTermination,
    QeProcessTermination,
    QeProcessTimeout,
    QeProgram,
    QePseudopotentialArtifact,
    QePwResult,
    QeStreamObservation,
    QeTerminalRecordIdentity,
    QeTreeArtifactContent,
)


def string_record_mapping(value: str) -> Mapping[str, SerializableValue]:
    """Project one validated nominal string record."""
    if type(value) is not str:
        raise TypeError("value must be a built-in string")
    return {"value": value}


def string_record_from_mapping(
    values: Mapping[str, SerializableValue],
    owner: str,
) -> str:
    """Decode one exact nominal string-record mapping."""
    fields = _fields(values, {"value"}, owner)
    return _string(fields["value"], owner + ".value")


def qe_pw_result_mapping(value: QePwResult) -> Mapping[str, SerializableValue]:
    """Project one validated PW result into its typed persistence mapping."""
    if type(value) is not QePwResult:
        raise TypeError("value must be QePwResult")
    return {
        "identity": value.identity.value,
        "execution_input": value.execution_input,
        "process_observation": value.process_observation,
        "diagnostic_report": value.diagnostic_report,
        "calculator_outcome": value.calculator_outcome,
        "native_output_manifest_identity": (
            value.native_output_manifest_identity.value
        ),
        "native_output_entry_identities": tuple(
            item.value for item in value.native_output_entry_identities
        ),
        "execution_record_manifest_entry_identity": (
            value.execution_record_manifest_entry_identity.value
        ),
        "execution_record_content_identity": _content_identity_mapping(
            value.execution_record_content_identity
        ),
        "execution_record_publication_snapshot_identity": (
            value.execution_record_publication_snapshot_identity.value
        ),
        "terminal_record_identity": value.terminal_record_identity,
        "terminal_record_content_identity": _content_identity_mapping(
            value.terminal_record_content_identity
        ),
        "contract_version": value.contract_version,
    }


def qe_pw_result_from_mapping(
    values: Mapping[str, SerializableValue],
) -> QePwResult:
    """Reconstruct one validated PW result from its typed persistence mapping."""
    fields = _fields(
        values,
        {
            "identity",
            "execution_input",
            "process_observation",
            "diagnostic_report",
            "calculator_outcome",
            "native_output_manifest_identity",
            "native_output_entry_identities",
            "execution_record_manifest_entry_identity",
            "execution_record_content_identity",
            "execution_record_publication_snapshot_identity",
            "terminal_record_identity",
            "terminal_record_content_identity",
            "contract_version",
        },
        "QePwResult",
    )
    return QePwResult(
        identity=ResultObjectIdentity(_string(fields["identity"], "identity")),
        execution_input=QeExecutionInput.from_dict(
            _mapping(fields["execution_input"], "execution_input")
        ),
        process_observation=QeProcessObservation.from_dict(
            _mapping(fields["process_observation"], "process_observation")
        ),
        diagnostic_report=QeDiagnosticReport.from_dict(
            _mapping(fields["diagnostic_report"], "diagnostic_report")
        ),
        calculator_outcome=_calculator_outcome(fields["calculator_outcome"]),
        native_output_manifest_identity=ArtifactManifestIdentity(
            _string(
                fields["native_output_manifest_identity"],
                "native_output_manifest_identity",
            )
        ),
        native_output_entry_identities=tuple(
            ArtifactManifestEntryIdentity(item)
            for item in _string_tuple(
                fields["native_output_entry_identities"],
                "native_output_entry_identities",
            )
        ),
        execution_record_manifest_entry_identity=ArtifactManifestEntryIdentity(
            _string(
                fields["execution_record_manifest_entry_identity"],
                "execution_record_manifest_entry_identity",
            )
        ),
        execution_record_content_identity=_content_identity(
            fields["execution_record_content_identity"],
            "execution_record_content_identity",
        ),
        execution_record_publication_snapshot_identity=ArtifactManifestIdentity(
            _string(
                fields["execution_record_publication_snapshot_identity"],
                "execution_record_publication_snapshot_identity",
            )
        ),
        terminal_record_identity=QeTerminalRecordIdentity.from_dict(
            _mapping(fields["terminal_record_identity"], "terminal_record_identity")
        ),
        terminal_record_content_identity=_content_identity(
            fields["terminal_record_content_identity"],
            "terminal_record_content_identity",
        ),
        contract_version=_string(fields["contract_version"], "contract_version"),
    )


def _content_identity_mapping(
    value: ArtifactContentIdentity,
) -> Mapping[str, SerializableValue]:
    return {
        "algorithm": value.algorithm,
        "digest": value.digest,
        "byte_count": value.byte_count,
    }


def _content_identity(
    value: SerializableValue,
    owner: str,
) -> ArtifactContentIdentity:
    fields = _fields(value, {"algorithm", "digest", "byte_count"}, owner)
    return ArtifactContentIdentity(
        algorithm=_string(fields["algorithm"], owner + ".algorithm"),
        digest=_string(fields["digest"], owner + ".digest"),
        byte_count=_integer(fields["byte_count"], owner + ".byte_count"),
    )


def _file_content_mapping(
    value: QeFileArtifactContent,
) -> Mapping[str, SerializableValue]:
    return {"content_identity": _content_identity_mapping(value.content_identity)}


def _file_content(value: SerializableValue, owner: str) -> QeFileArtifactContent:
    fields = _fields(value, {"content_identity"}, owner)
    return QeFileArtifactContent(
        _content_identity(fields["content_identity"], owner + ".content_identity")
    )


def _tree_content_mapping(
    value: QeTreeArtifactContent,
) -> Mapping[str, SerializableValue]:
    return {
        "manifest_identity": value.manifest_identity.value,
        "manifest_entry_identities": tuple(
            item.value for item in value.manifest_entry_identities
        ),
    }


def _tree_content(value: SerializableValue, owner: str) -> QeTreeArtifactContent:
    fields = _fields(
        value,
        {"manifest_identity", "manifest_entry_identities"},
        owner,
    )
    return QeTreeArtifactContent(
        manifest_identity=ArtifactManifestIdentity(
            _string(fields["manifest_identity"], owner + ".manifest_identity")
        ),
        manifest_entry_identities=tuple(
            ArtifactManifestEntryIdentity(item)
            for item in _string_tuple(
                fields["manifest_entry_identities"],
                owner + ".manifest_entry_identities",
            )
        ),
    )


def _native_input_mapping(
    value: QeNativeInputArtifact,
) -> Mapping[str, SerializableValue]:
    return {
        "identity": value.identity.value,
        "content": value.content,
        "destination": value.destination,
    }


def _native_input(value: SerializableValue) -> QeNativeInputArtifact:
    fields = _fields(value, {"identity", "content", "destination"}, "native_input")
    return QeNativeInputArtifact(
        identity=ArtifactIdentity(_string(fields["identity"], "native_input.identity")),
        content=QeFileArtifactContent.from_dict(
            _mapping(fields["content"], "native_input.content")
        ),
        destination=QeArtifactDestination.from_dict(
            _mapping(fields["destination"], "native_input.destination")
        ),
    )


def _pseudopotential_mapping(
    value: QePseudopotentialArtifact,
) -> Mapping[str, SerializableValue]:
    return {
        "identity": value.identity.value,
        "content": value.content,
        "destination": value.destination,
    }


def _pseudopotential(
    value: SerializableValue,
    index: int,
) -> QePseudopotentialArtifact:
    owner = f"pseudopotentials[{index}]"
    fields = _fields(value, {"identity", "content", "destination"}, owner)
    return QePseudopotentialArtifact(
        identity=ArtifactIdentity(_string(fields["identity"], owner + ".identity")),
        content=QeFileArtifactContent.from_dict(
            _mapping(fields["content"], owner + ".content")
        ),
        destination=QeArtifactDestination.from_dict(
            _mapping(fields["destination"], owner + ".destination")
        ),
    )


def _predecessor_mapping(
    value: QePredecessorNativeStateArtifact,
) -> Mapping[str, SerializableValue]:
    return {
        "identity": value.identity.value,
        "content": value.content,
        "destination": value.destination,
        "predecessor_result_identity": value.predecessor_result_identity.value,
        "predecessor_manifest_entry_identity": (
            value.predecessor_manifest_entry_identity.value
        ),
    }


def _predecessor(
    value: SerializableValue,
    index: int,
) -> QePredecessorNativeStateArtifact:
    owner = f"predecessor_native_state[{index}]"
    fields = _fields(
        value,
        {
            "identity",
            "content",
            "destination",
            "predecessor_result_identity",
            "predecessor_manifest_entry_identity",
        },
        owner,
    )
    return QePredecessorNativeStateArtifact(
        identity=ArtifactIdentity(_string(fields["identity"], owner + ".identity")),
        content=QeTreeArtifactContent.from_dict(
            _mapping(fields["content"], owner + ".content")
        ),
        destination=QeArtifactDestination.from_dict(
            _mapping(fields["destination"], owner + ".destination")
        ),
        predecessor_result_identity=ResultObjectIdentity(
            _string(
                fields["predecessor_result_identity"],
                owner + ".predecessor_result_identity",
            )
        ),
        predecessor_manifest_entry_identity=ArtifactManifestEntryIdentity(
            _string(
                fields["predecessor_manifest_entry_identity"],
                owner + ".predecessor_manifest_entry_identity",
            )
        ),
    )


def _execution_input_mapping(
    value: QeExecutionInput,
) -> Mapping[str, SerializableValue]:
    return {
        "identity": value.identity,
        "program": value.program.to_wire(),
        "native_input": value.native_input,
        "pseudopotentials": value.pseudopotentials,
        "predecessor_native_state": value.predecessor_native_state,
        "task_definition_identity": value.task_definition_identity.value,
        "task_instance_identity": value.task_instance_identity.value,
        "activation_identity": value.activation_identity.value,
        "operation_identity": value.operation_identity.value,
        "attempt_identity": value.attempt_identity.value,
        "contract_version": value.contract_version,
    }


def _execution_input(value: SerializableValue) -> QeExecutionInput:
    fields = _fields(
        value,
        {
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
        },
        "execution_input",
    )
    pseudopotentials = _tuple(fields["pseudopotentials"], "pseudopotentials")
    predecessors = _tuple(
        fields["predecessor_native_state"], "predecessor_native_state"
    )
    return QeExecutionInput(
        identity=QeExecutionInputIdentity.from_dict(
            _mapping(fields["identity"], "execution_input.identity")
        ),
        program=QeProgram.from_wire(
            _string(fields["program"], "execution_input.program")
        ),
        native_input=QeNativeInputArtifact.from_dict(
            _mapping(fields["native_input"], "execution_input.native_input")
        ),
        pseudopotentials=tuple(
            QePseudopotentialArtifact.from_dict(
                _mapping(item, f"execution_input.pseudopotentials[{index}]")
            )
            for index, item in enumerate(pseudopotentials)
        ),
        predecessor_native_state=tuple(
            QePredecessorNativeStateArtifact.from_dict(
                _mapping(item, f"execution_input.predecessor_native_state[{index}]")
            )
            for index, item in enumerate(predecessors)
        ),
        task_definition_identity=TaskDefinitionIdentity(
            _string(
                fields["task_definition_identity"],
                "execution_input.task_definition_identity",
            )
        ),
        task_instance_identity=TaskInstanceIdentity(
            _string(
                fields["task_instance_identity"],
                "execution_input.task_instance_identity",
            )
        ),
        activation_identity=TaskActivationIdentity(
            _string(
                fields["activation_identity"],
                "execution_input.activation_identity",
            )
        ),
        operation_identity=OperationIdentity(
            _string(
                fields["operation_identity"],
                "execution_input.operation_identity",
            )
        ),
        attempt_identity=AttemptIdentity(
            _string(fields["attempt_identity"], "execution_input.attempt_identity")
        ),
        contract_version=_string(
            fields["contract_version"], "execution_input.contract_version"
        ),
    )


def _stream_mapping(value: QeStreamObservation) -> Mapping[str, SerializableValue]:
    return {
        "channel": value.channel.to_wire(),
        "artifact_identity": value.artifact_identity.value,
        "content_identity": _content_identity_mapping(value.content_identity),
    }


def _stream(value: SerializableValue, owner: str) -> QeStreamObservation:
    fields = _fields(
        value,
        {"channel", "artifact_identity", "content_identity"},
        owner,
    )
    return QeStreamObservation(
        channel=QeDiagnosticChannel.from_wire(
            _string(fields["channel"], owner + ".channel")
        ),
        artifact_identity=ArtifactIdentity(
            _string(fields["artifact_identity"], owner + ".artifact_identity")
        ),
        content_identity=_content_identity(
            fields["content_identity"], owner + ".content_identity"
        ),
    )


def _termination_mapping(
    value: QeProcessTermination,
) -> Mapping[str, SerializableValue]:
    if type(value) is QeNormalProcessExit:
        return {"kind": "normal_exit", "exit_code": value.exit_code.value}
    if type(value) is QeProcessSignalTermination:
        return {"kind": "signal", "signal_number": value.signal_number}
    if type(value) is QeProcessTimeout:
        return {
            "kind": "timeout",
            "timeout_milliseconds": value.timeout_milliseconds,
            "termination_sent": value.termination_sent,
            "kill_sent": value.kill_sent,
        }
    raise TypeError("termination must be a closed QE process termination")


def _termination(value: SerializableValue) -> QeProcessTermination:
    values = _mapping(value, "process_observation.termination")
    kind = _string(
        values.get("kind"),
        "process_observation.termination.kind",
    )
    if kind == "normal_exit":
        fields = _fields(
            values,
            {"kind", "exit_code"},
            "process_observation.termination",
        )
        return QeNormalProcessExit(
            CalculatorExitCode(
                _integer(
                    fields["exit_code"],
                    "process_observation.termination.exit_code",
                )
            )
        )
    if kind == "signal":
        fields = _fields(
            values,
            {"kind", "signal_number"},
            "process_observation.termination",
        )
        return QeProcessSignalTermination(
            _integer(
                fields["signal_number"],
                "process_observation.termination.signal_number",
            )
        )
    if kind == "timeout":
        fields = _fields(
            values,
            {"kind", "timeout_milliseconds", "termination_sent", "kill_sent"},
            "process_observation.termination",
        )
        return QeProcessTimeout(
            timeout_milliseconds=_integer(
                fields["timeout_milliseconds"],
                "process_observation.termination.timeout_milliseconds",
            ),
            termination_sent=_boolean(
                fields["termination_sent"],
                "process_observation.termination.termination_sent",
            ),
            kill_sent=_boolean(
                fields["kill_sent"],
                "process_observation.termination.kill_sent",
            ),
        )
    raise ValueError("process_observation.termination kind is unsupported")


def _process_observation_mapping(
    value: QeProcessObservation,
) -> Mapping[str, SerializableValue]:
    return {
        "identity": value.identity,
        "execution_input_identity": value.execution_input_identity,
        "executable_configuration_identity": value.executable_configuration_identity,
        "preparation_identity": value.preparation_identity,
        "attempt_identity": value.attempt_identity.value,
        "argv_content_identity": _content_identity_mapping(value.argv_content_identity),
        "termination": value.termination,
        "wall_duration_nanoseconds": value.wall_duration_nanoseconds,
        "stdout": value.stdout,
        "stderr": value.stderr,
        "before_snapshot_identity": value.before_snapshot_identity.value,
        "after_snapshot_identity": value.after_snapshot_identity.value,
        "created_entry_count": value.created_entry_count,
        "created_total_bytes": value.created_total_bytes,
        "peak_resident_bytes": value.peak_resident_bytes,
        "observer_version": value.observer_version,
    }


def _process_observation(value: SerializableValue) -> QeProcessObservation:
    fields = _fields(
        value,
        {
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
        },
        "process_observation",
    )
    peak = fields["peak_resident_bytes"]
    if peak is not None:
        peak_value: int | None = _integer(
            peak, "process_observation.peak_resident_bytes"
        )
    else:
        peak_value = None
    return QeProcessObservation(
        identity=QeProcessObservationIdentity.from_dict(
            _mapping(fields["identity"], "process_observation.identity")
        ),
        execution_input_identity=QeExecutionInputIdentity.from_dict(
            _mapping(
                fields["execution_input_identity"],
                "process_observation.execution_input_identity",
            )
        ),
        executable_configuration_identity=QeExecutableConfigurationIdentity.from_dict(
            _mapping(
                fields["executable_configuration_identity"],
                "process_observation.executable_configuration_identity",
            )
        ),
        preparation_identity=QePreparationIdentity.from_dict(
            _mapping(
                fields["preparation_identity"],
                "process_observation.preparation_identity",
            )
        ),
        attempt_identity=AttemptIdentity(
            _string(
                fields["attempt_identity"],
                "process_observation.attempt_identity",
            )
        ),
        argv_content_identity=_content_identity(
            fields["argv_content_identity"],
            "process_observation.argv_content_identity",
        ),
        termination=_termination(fields["termination"]),
        wall_duration_nanoseconds=_integer(
            fields["wall_duration_nanoseconds"],
            "process_observation.wall_duration_nanoseconds",
        ),
        stdout=QeStreamObservation.from_dict(
            _mapping(fields["stdout"], "process_observation.stdout")
        ),
        stderr=QeStreamObservation.from_dict(
            _mapping(fields["stderr"], "process_observation.stderr")
        ),
        before_snapshot_identity=ArtifactManifestIdentity(
            _string(
                fields["before_snapshot_identity"],
                "process_observation.before_snapshot_identity",
            )
        ),
        after_snapshot_identity=ArtifactManifestIdentity(
            _string(
                fields["after_snapshot_identity"],
                "process_observation.after_snapshot_identity",
            )
        ),
        created_entry_count=_integer(
            fields["created_entry_count"],
            "process_observation.created_entry_count",
        ),
        created_total_bytes=_integer(
            fields["created_total_bytes"],
            "process_observation.created_total_bytes",
        ),
        peak_resident_bytes=peak_value,
        observer_version=_string(
            fields["observer_version"], "process_observation.observer_version"
        ),
    )


def _diagnostic_observation_mapping(
    value: QeDiagnosticObservation,
) -> Mapping[str, SerializableValue]:
    return {
        "identity": value.identity,
        "channel": value.channel.to_wire(),
        "byte_start": value.byte_start,
        "byte_end": value.byte_end,
        "stream_content_identity": _content_identity_mapping(
            value.stream_content_identity
        ),
        "span_content_identity": _content_identity_mapping(value.span_content_identity),
        "signature_identity": value.signature_identity,
        "disposition": value.disposition.to_wire(),
        "sanitized_summary": value.sanitized_summary,
        "claim_boundary": value.claim_boundary,
    }


def _diagnostic_observation(
    value: SerializableValue,
    index: int,
) -> QeDiagnosticObservation:
    owner = f"diagnostic_report.observations[{index}]"
    fields = _fields(
        value,
        {
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
        },
        owner,
    )
    signature = fields["signature_identity"]
    if signature is not None:
        signature_value: str | None = _string(signature, owner + ".signature_identity")
    else:
        signature_value = None
    return QeDiagnosticObservation(
        identity=QeDiagnosticObservationIdentity.from_dict(
            _mapping(fields["identity"], owner + ".identity")
        ),
        channel=QeDiagnosticChannel.from_wire(
            _string(fields["channel"], owner + ".channel")
        ),
        byte_start=_integer(fields["byte_start"], owner + ".byte_start"),
        byte_end=_integer(fields["byte_end"], owner + ".byte_end"),
        stream_content_identity=_content_identity(
            fields["stream_content_identity"], owner + ".stream_content_identity"
        ),
        span_content_identity=_content_identity(
            fields["span_content_identity"], owner + ".span_content_identity"
        ),
        signature_identity=signature_value,
        disposition=QeDiagnosticDisposition.from_wire(
            _string(fields["disposition"], owner + ".disposition")
        ),
        sanitized_summary=_string(
            fields["sanitized_summary"], owner + ".sanitized_summary"
        ),
        claim_boundary=_string_tuple(
            fields["claim_boundary"], owner + ".claim_boundary"
        ),
    )


def _marker_mapping(
    value: QeOutputMarkerObservation,
) -> Mapping[str, SerializableValue]:
    return {
        "identity": value.identity,
        "channel": value.channel.to_wire(),
        "byte_start": value.byte_start,
        "byte_end": value.byte_end,
        "stream_content_identity": _content_identity_mapping(
            value.stream_content_identity
        ),
        "span_content_identity": _content_identity_mapping(value.span_content_identity),
        "signature_identity": value.signature_identity,
    }


def _marker(value: SerializableValue, index: int) -> QeOutputMarkerObservation:
    owner = f"diagnostic_report.completion_markers[{index}]"
    fields = _fields(
        value,
        {
            "identity",
            "channel",
            "byte_start",
            "byte_end",
            "stream_content_identity",
            "span_content_identity",
            "signature_identity",
        },
        owner,
    )
    return QeOutputMarkerObservation(
        identity=QeOutputMarkerObservationIdentity.from_dict(
            _mapping(fields["identity"], owner + ".identity")
        ),
        channel=QeDiagnosticChannel.from_wire(
            _string(fields["channel"], owner + ".channel")
        ),
        byte_start=_integer(fields["byte_start"], owner + ".byte_start"),
        byte_end=_integer(fields["byte_end"], owner + ".byte_end"),
        stream_content_identity=_content_identity(
            fields["stream_content_identity"], owner + ".stream_content_identity"
        ),
        span_content_identity=_content_identity(
            fields["span_content_identity"], owner + ".span_content_identity"
        ),
        signature_identity=_string(
            fields["signature_identity"], owner + ".signature_identity"
        ),
    )


def _diagnostic_report_mapping(
    value: QeDiagnosticReport,
) -> Mapping[str, SerializableValue]:
    return {
        "identity": value.identity,
        "classifier_identity": value.classifier_identity,
        "executable_configuration_identity": value.executable_configuration_identity,
        "executable_kind": value.executable_kind.to_wire(),
        "program": value.program.to_wire(),
        "program_version": value.program_version,
        "stdout_content_identity": _content_identity_mapping(
            value.stdout_content_identity
        ),
        "stderr_content_identity": _content_identity_mapping(
            value.stderr_content_identity
        ),
        "observations": value.observations,
        "completion_markers": value.completion_markers,
        "kind": value.kind.to_wire(),
        "claim_boundary": value.claim_boundary,
    }


def _diagnostic_report(value: SerializableValue) -> QeDiagnosticReport:
    fields = _fields(
        value,
        {
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
        },
        "diagnostic_report",
    )
    observations = _tuple(fields["observations"], "diagnostic_report.observations")
    markers = _tuple(
        fields["completion_markers"], "diagnostic_report.completion_markers"
    )
    return QeDiagnosticReport(
        identity=QeDiagnosticReportIdentity.from_dict(
            _mapping(fields["identity"], "diagnostic_report.identity")
        ),
        classifier_identity=QeDiagnosticClassifierIdentity.from_dict(
            _mapping(
                fields["classifier_identity"],
                "diagnostic_report.classifier_identity",
            )
        ),
        executable_configuration_identity=QeExecutableConfigurationIdentity.from_dict(
            _mapping(
                fields["executable_configuration_identity"],
                "diagnostic_report.executable_configuration_identity",
            )
        ),
        executable_kind=QeExecutableKind.from_wire(
            _string(fields["executable_kind"], "diagnostic_report.executable_kind")
        ),
        program=QeProgram.from_wire(
            _string(fields["program"], "diagnostic_report.program")
        ),
        program_version=_string(
            fields["program_version"], "diagnostic_report.program_version"
        ),
        stdout_content_identity=_content_identity(
            fields["stdout_content_identity"],
            "diagnostic_report.stdout_content_identity",
        ),
        stderr_content_identity=_content_identity(
            fields["stderr_content_identity"],
            "diagnostic_report.stderr_content_identity",
        ),
        observations=tuple(
            QeDiagnosticObservation.from_dict(
                _mapping(item, f"diagnostic_report.observations[{index}]")
            )
            for index, item in enumerate(observations)
        ),
        completion_markers=tuple(
            QeOutputMarkerObservation.from_dict(
                _mapping(item, f"diagnostic_report.completion_markers[{index}]")
            )
            for index, item in enumerate(markers)
        ),
        kind=QeDiagnosticReportKind.from_wire(
            _string(fields["kind"], "diagnostic_report.kind")
        ),
        claim_boundary=_string_tuple(
            fields["claim_boundary"], "diagnostic_report.claim_boundary"
        ),
    )


def _calculator_outcome_mapping(
    value: QeCalculatorOutcome,
) -> Mapping[str, SerializableValue]:
    if type(value) is QeCompletedOutcome:
        return {
            "kind": "completed",
            "completion_marker_identities": value.completion_marker_identities,
        }
    if type(value) is QeCalculatorFailedOutcome:
        return {
            "kind": "calculator_failed",
            "fatal_diagnostic_identities": value.fatal_diagnostic_identities,
        }
    if type(value) is QeProcessFailedOutcome:
        return {"kind": "process_failed", "reason": value.reason.to_wire()}
    if type(value) is QeDiagnosticUnresolvedOutcome:
        return {
            "kind": "diagnostic_unresolved",
            "diagnostic_identities": value.diagnostic_identities,
            "reason_identities": value.reason_identities,
        }
    raise TypeError("calculator_outcome must be a closed QE outcome variant")


def _calculator_outcome(value: SerializableValue) -> QeCalculatorOutcome:
    values = _mapping(value, "calculator_outcome")
    kind = _string(values.get("kind"), "calculator_outcome.kind")
    if kind == "completed":
        fields = _fields(
            values,
            {"kind", "completion_marker_identities"},
            "calculator_outcome",
        )
        return QeCompletedOutcome(
            tuple(
                QeOutputMarkerObservationIdentity.from_dict(
                    _mapping(
                        item,
                        f"calculator_outcome.completion_marker_identities[{index}]",
                    )
                )
                for index, item in enumerate(
                    _tuple(
                        fields["completion_marker_identities"],
                        "calculator_outcome.completion_marker_identities",
                    )
                )
            )
        )
    if kind == "calculator_failed":
        fields = _fields(
            values,
            {"kind", "fatal_diagnostic_identities"},
            "calculator_outcome",
        )
        return QeCalculatorFailedOutcome(
            tuple(
                QeDiagnosticObservationIdentity.from_dict(
                    _mapping(
                        item,
                        f"calculator_outcome.fatal_diagnostic_identities[{index}]",
                    )
                )
                for index, item in enumerate(
                    _tuple(
                        fields["fatal_diagnostic_identities"],
                        "calculator_outcome.fatal_diagnostic_identities",
                    )
                )
            )
        )
    if kind == "process_failed":
        fields = _fields(
            values,
            {"kind", "reason"},
            "calculator_outcome",
        )
        return QeProcessFailedOutcome(
            QeProcessFailureKind.from_wire(
                _string(fields["reason"], "calculator_outcome.reason")
            )
        )
    if kind == "diagnostic_unresolved":
        fields = _fields(
            values,
            {"kind", "diagnostic_identities", "reason_identities"},
            "calculator_outcome",
        )
        return QeDiagnosticUnresolvedOutcome(
            diagnostic_identities=tuple(
                QeDiagnosticObservationIdentity.from_dict(
                    _mapping(
                        item,
                        f"calculator_outcome.diagnostic_identities[{index}]",
                    )
                )
                for index, item in enumerate(
                    _tuple(
                        fields["diagnostic_identities"],
                        "calculator_outcome.diagnostic_identities",
                    )
                )
            ),
            reason_identities=_string_tuple(
                fields["reason_identities"],
                "calculator_outcome.reason_identities",
            ),
        )
    raise ValueError("calculator_outcome kind is unsupported")


def _mapping(
    value: SerializableValue,
    owner: str,
) -> Mapping[str, SerializableValue]:
    if not isinstance(value, Mapping):
        raise TypeError(f"{owner} must decode to a mapping")
    for key in value:
        if type(key) is not str:
            raise TypeError(f"{owner} keys must be built-in strings")
    return value


def _fields(
    value: SerializableValue | Mapping[str, SerializableValue],
    expected: set[str],
    owner: str,
) -> Mapping[str, SerializableValue]:
    if not isinstance(value, Mapping):
        raise TypeError(f"{owner} must decode to a mapping")
    if set(value) != expected:
        raise ValueError(f"{owner} fields do not match the exact schema")
    return value


def _string(value: SerializableValue | None, owner: str) -> str:
    if type(value) is not str:
        raise TypeError(f"{owner} must decode to a built-in string")
    return value


def _integer(value: SerializableValue, owner: str) -> int:
    if type(value) is not int:
        raise TypeError(f"{owner} must decode to a built-in integer")
    return value


def _boolean(value: SerializableValue, owner: str) -> bool:
    if type(value) is not bool:
        raise TypeError(f"{owner} must decode to a built-in boolean")
    return value


def _tuple(value: SerializableValue, owner: str) -> tuple[SerializableValue, ...]:
    if type(value) is not tuple:
        raise TypeError(f"{owner} must decode to a tuple")
    return value


def _string_tuple(value: SerializableValue, owner: str) -> tuple[str, ...]:
    items = _tuple(value, owner)
    if any(type(item) is not str for item in items):
        raise TypeError(f"{owner} must decode to a tuple of built-in strings")
    return tuple(item for item in items if type(item) is str)
