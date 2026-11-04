"""Software verification of exact provider execution-record publication."""

from __future__ import annotations

import os
from pathlib import Path

import pytest
from projectkoios.simulations.execution import (
    CalculatorExecutionObservationAssembler,
    CalculatorExecutionRecordSerializer,
)

from ksdft2effmass.integration.quantum_espresso import (
    LocalQeCapturedProcess,
    QePwEvidenceAdapter,
    QePwEvidenceAdapterIdentity,
    QePwEvidenceFailureCode,
    QePwEvidencePublisher,
    QePwEvidencePublisherIdentity,
    QePwObservation,
    QePwPublicationFailure,
    QePwPublishedEvidence,
    QeWorkspaceSnapshotter,
)

from .test__LocalQeExecutionPreparer__preparation import (
    TestLocalQeExecutionPreparer as _PreparationScenario,
)

pytestmark = [pytest.mark.integration, pytest.mark.software_verification]


class TestQePwEvidencePublisher:
    """Own exact no-replace publication evidence for provider execution records."""

    def test_execute_publishes_exact_provider_bytes_and_manifest_entry(
        self, tmp_path: Path
    ) -> None:
        observation = self._observation(tmp_path.resolve())
        publisher = self._publisher()

        result = publisher.execute(observation)

        assert type(result) is QePwPublishedEvidence
        assert result.publisher_identity is publisher.identity
        assert result.observation_binding is observation
        assert (
            result.destination
            is observation.prepared_execution.execution_record_destination
        )
        provider_artifact = observation.provider_observation.record_artifact
        assert (
            result.destination.absolute_path.read_bytes() == provider_artifact.content
        )
        assert (
            result.content_identity.digest == provider_artifact.content_identity.sha256
        )
        assert result.publication_entry.identity in tuple(
            entry.identity for entry in result.publication_snapshot.entries
        )
        assert result.publication_entry.content_identity == result.content_identity

    def test_execute_rejects_preexisting_destination_without_replacement(
        self, tmp_path: Path
    ) -> None:
        observation = self._observation(tmp_path.resolve())
        target = (
            observation.prepared_execution.execution_record_destination.absolute_path
        )
        existing = b"preexisting execution record\n"
        target.write_bytes(existing)

        result = self._publisher().execute(observation)

        assert type(result) is QePwPublicationFailure
        assert result.code is QePwEvidenceFailureCode.DESTINATION_EXISTS
        assert result.publication_observed is True
        assert target.read_bytes() == existing

    def test_execute_rejects_symlink_destination_without_following_it(
        self, tmp_path: Path
    ) -> None:
        observation = self._observation(tmp_path.resolve())
        target = (
            observation.prepared_execution.execution_record_destination.absolute_path
        )
        external = tmp_path / "external-execution-record.json"
        external.write_bytes(b"external record\n")
        target.symlink_to(external)

        result = self._publisher().execute(observation)

        assert type(result) is QePwPublicationFailure
        assert result.code is QePwEvidenceFailureCode.DESTINATION_EXISTS
        assert result.publication_observed is True
        assert external.read_bytes() == b"external record\n"

    def test_execute_detects_content_replacement_after_publication(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        observation = self._observation(tmp_path.resolve())

        def replace_after_link(
            publisher: QePwEvidencePublisher,
            source: Path,
            destination: Path,
        ) -> None:
            del publisher
            os.link(source, destination, follow_symlinks=False)
            destination.write_bytes(b"replaced execution record\n")

        monkeypatch.setattr(QePwEvidencePublisher, "_link", replace_after_link)

        result = self._publisher().execute(observation)

        assert type(result) is QePwPublicationFailure
        assert result.code is QePwEvidenceFailureCode.VERIFICATION_FAILED
        assert result.publication_observed is True

    def test_execute_reports_durability_uncertainty_after_publication(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        observation = self._observation(tmp_path.resolve())
        fsync_calls = 0
        real_fsync = os.fsync

        def fail_directory_fsync(descriptor: int) -> None:
            nonlocal fsync_calls
            fsync_calls += 1
            if fsync_calls == 2:
                raise OSError("synthetic directory fsync failure")
            real_fsync(descriptor)

        monkeypatch.setattr(os, "fsync", fail_directory_fsync)

        result = self._publisher().execute(observation)

        assert type(result) is QePwPublicationFailure
        assert result.code is QePwEvidenceFailureCode.DURABILITY_UNCERTAIN
        assert result.publication_observed is True
        target = (
            observation.prepared_execution.execution_record_destination.absolute_path
        )
        assert target.exists()

    def _observation(self, root: Path) -> QePwObservation:
        prepared, _staged, process = _PreparationScenario.run_process(
            root, argument_suffix=("--fixture-empty-stderr",)
        )
        assert type(process) is LocalQeCapturedProcess
        result = QePwEvidenceAdapter(
            identity=QePwEvidenceAdapterIdentity(
                "qe-pw-evidence-adapter:publication-test"
            ),
            provider_assembler=CalculatorExecutionObservationAssembler(
                CalculatorExecutionRecordSerializer(schema_version=1)
            ),
        ).execute(prepared, process)
        assert type(result) is QePwObservation
        return result

    def _publisher(self) -> QePwEvidencePublisher:
        return QePwEvidencePublisher(
            identity=QePwEvidencePublisherIdentity(
                "qe-pw-evidence-publisher:publication-test"
            ),
            snapshotter=QeWorkspaceSnapshotter("qe-snapshotter:publication-test"),
        )
