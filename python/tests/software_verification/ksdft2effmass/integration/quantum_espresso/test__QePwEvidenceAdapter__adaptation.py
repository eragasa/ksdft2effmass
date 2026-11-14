"""Software verification for exact provider execution-evidence adaptation."""

from __future__ import annotations

import dataclasses
import json
from dataclasses import replace
from pathlib import Path

import pytest
from projectkoios.simulations.execution import (
    CalculatorExecutionObservationAssembler,
    CalculatorExecutionRecordSerializer,
    CalculatorExitDisposition,
    CalculatorNormalExit,
    CalculatorSignalTermination,
    CalculatorTimeout,
    ExecutionStatus,
)

from ksdft2effmass.integration.quantum_espresso import (
    LocalQeCapturedProcess,
    QePwEvidenceAdapter,
    QePwEvidenceAdapterIdentity,
    QePwEvidenceFailureCode,
    QePwObservation,
    QePwObservationFailure,
)
from ksdft2effmass.integration.quantum_espresso.contracts import (
    QePreparationIdentity,
)

from .test__LocalQeExecutionPreparer__preparation import (
    TestLocalQeExecutionPreparer as _PreparationScenario,
)

pytestmark = [pytest.mark.integration, pytest.mark.software_verification]


class TestQePwEvidenceAdapter:
    def test_adapts_object_owned_process_facts_without_reconstructing_bytes(
        self, tmp_path: Path
    ) -> None:
        prepared, _staged, process = _PreparationScenario.run_process(
            tmp_path.resolve(), argument_suffix=("--fixture-empty-stderr",)
        )
        assert type(process) is LocalQeCapturedProcess
        adapter = self._adapter()

        result = adapter.execute(prepared, process)

        assert type(result) is QePwObservation
        assert result.prepared_execution is prepared
        assert result.captured_process is process
        provider = result.provider_observation
        assert provider.record.command == prepared.argv
        assert provider.record.working_directory == str(prepared.workspace)
        assert provider.record.status is ExecutionStatus.succeeded
        assert provider.record.returncode == 0
        assert provider.stdout is not None
        assert provider.stderr is not None
        assert provider.stdout.content is process.stdout_bytes
        assert provider.stderr.content is process.stderr_bytes
        assert provider.stdout.content_identity.sha256 == (
            process.observation.stdout.content_identity.digest
        )
        assert provider.stderr.content_identity.sha256 == (
            process.observation.stderr.content_identity.digest
        )
        assert provider.wall_duration_nanoseconds == (
            process.observation.wall_duration_nanoseconds
        )
        assert json.loads(provider.record_artifact.content)["schema_version"] == 1
        with pytest.raises(dataclasses.FrozenInstanceError):
            result.provider_observation = provider  # type: ignore[misc]

    def test_retains_nonzero_normal_exit(self, tmp_path: Path) -> None:
        prepared, _staged, process = _PreparationScenario.run_process(
            tmp_path.resolve(), argument_suffix=("--fixture-fail",)
        )
        assert type(process) is LocalQeCapturedProcess

        result = self._adapter().execute(prepared, process)

        assert type(result) is QePwObservation
        termination = result.provider_observation.termination
        assert type(termination) is CalculatorNormalExit
        assert termination.exit_code.disposition is CalculatorExitDisposition.failed
        assert result.provider_observation.record.status is ExecutionStatus.failed
        assert (
            result.provider_observation.record.returncode == termination.exit_code.value
        )

    def test_retains_explicit_signal_and_timeout_variants(self, tmp_path: Path) -> None:
        signal_root = tmp_path.resolve() / "signal"
        timeout_root = tmp_path.resolve() / "timeout"
        signal_root.mkdir()
        timeout_root.mkdir()
        signal_prepared, _signal_staged, signal_process = (
            _PreparationScenario.run_process(
                signal_root,
                argument_suffix=("--fixture-signal",),
            )
        )
        timeout_prepared, _timeout_staged, timeout_process = (
            _PreparationScenario.run_process(
                timeout_root,
                argument_suffix=("--fixture-timeout",),
                wall_time_milliseconds=2_000,
                termination_grace_milliseconds=100,
            )
        )
        assert type(signal_process) is LocalQeCapturedProcess
        assert type(timeout_process) is LocalQeCapturedProcess
        adapter = self._adapter()

        signal_result = adapter.execute(signal_prepared, signal_process)
        timeout_result = adapter.execute(timeout_prepared, timeout_process)

        assert type(signal_result) is QePwObservation
        assert type(timeout_result) is QePwObservation
        assert type(signal_result.provider_observation.termination) is (
            CalculatorSignalTermination
        )
        assert signal_result.provider_observation.record.returncode == (
            -signal_result.provider_observation.termination.signal_number
        )
        assert (
            type(timeout_result.provider_observation.termination) is CalculatorTimeout
        )
        assert timeout_result.provider_observation.record.status is (
            ExecutionStatus.timed_out
        )
        assert timeout_result.provider_observation.record.returncode is None

    def test_rejects_copied_process_with_different_preparation_identity(
        self, tmp_path: Path
    ) -> None:
        prepared, _staged, process = _PreparationScenario.run_process(
            tmp_path.resolve(), argument_suffix=("--fixture-empty-stderr",)
        )
        assert type(process) is LocalQeCapturedProcess
        mismatched_observation = replace(
            process.observation,
            preparation_identity=QePreparationIdentity("preparation.other"),
        )
        mismatched_process = replace(process, observation=mismatched_observation)

        result = self._adapter().execute(prepared, mismatched_process)

        assert type(result) is QePwObservationFailure
        assert result.code is (QePwEvidenceFailureCode.PREPARATION_CORRELATION_MISMATCH)
        assert result.prepared_execution is prepared
        assert result.captured_process is mismatched_process

    def _adapter(self) -> QePwEvidenceAdapter:
        return QePwEvidenceAdapter(
            identity=QePwEvidenceAdapterIdentity("qe-pw-evidence-adapter:1"),
            provider_assembler=CalculatorExecutionObservationAssembler(
                CalculatorExecutionRecordSerializer(schema_version=1)
            ),
        )
