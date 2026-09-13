"""Fail-closed calculator-outcome resolution for Quantum ESPRESSO observations."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass

from .contracts import (
    QuantumEspressoCalculatorFailedOutcome,
    QuantumEspressoCalculatorOutcome,
    QuantumEspressoCompletedOutcome,
    QuantumEspressoDiagnosticDisposition,
    QuantumEspressoDiagnosticReport,
    QuantumEspressoDiagnosticReportKind,
    QuantumEspressoDiagnosticUnresolvedOutcome,
    QuantumEspressoFileArtifactContent,
    QuantumEspressoNormalProcessExit,
    QuantumEspressoProcessFailedOutcome,
    QuantumEspressoProcessFailureKind,
    QuantumEspressoProcessObservation,
    QuantumEspressoProcessSignalTermination,
    QuantumEspressoProcessTimeout,
)
from .effects import (
    QuantumEspressoNativeOutputExtractionSpecification,
    QuantumEspressoNativeOutputManifest,
    QuantumEspressoNativeOutputRole,
)


@dataclass(frozen=True, slots=True)
class QuantumEspressoCalculatorOutcomeResolver:
    """Resolve compatible process, diagnostic, and artifact facts by precedence.

        The resolver performs no parsing, filesystem access, retry, or scientific
        acceptance. Identity mismatch and every unsupported combination fail closed as a
        diagnostic-unresolved outcome with a deterministic reason identity.

    Attributes
    ----------
    resolver_version
        Nonempty identity of the outcome-resolution implementation.
    """

    resolver_version: str

    def __post_init__(self) -> None:
        if type(self.resolver_version) is not str:
            raise TypeError("resolver_version must be a built-in str")
        if not self.resolver_version:
            raise ValueError("resolver_version must not be empty")

    def execute(
        self,
        process: QuantumEspressoProcessObservation,
        report: QuantumEspressoDiagnosticReport,
        manifest: QuantumEspressoNativeOutputManifest,
        specification: QuantumEspressoNativeOutputExtractionSpecification,
    ) -> QuantumEspressoCalculatorOutcome:
        """Return one closed calculator outcome without changing any input."""
        if type(process) is not QuantumEspressoProcessObservation:
            raise TypeError("process must be QuantumEspressoProcessObservation")
        if type(report) is not QuantumEspressoDiagnosticReport:
            raise TypeError("report must be QuantumEspressoDiagnosticReport")
        if type(manifest) is not QuantumEspressoNativeOutputManifest:
            raise TypeError("manifest must be QuantumEspressoNativeOutputManifest")
        if (
            type(specification)
            is not QuantumEspressoNativeOutputExtractionSpecification
        ):
            raise TypeError(
                "specification must be "
                "QuantumEspressoNativeOutputExtractionSpecification"
            )
        mismatch = self._compatibility_mismatch(
            process, report, manifest, specification
        )
        if mismatch is not None:
            return self._unresolved(report, mismatch)
        if report.kind in (
            QuantumEspressoDiagnosticReportKind.UNRESOLVED,
            QuantumEspressoDiagnosticReportKind.CONTRADICTORY,
        ):
            return self._unresolved(report, "report:" + report.kind.value)
        termination = process.termination
        if type(termination) is QuantumEspressoProcessSignalTermination:
            return QuantumEspressoProcessFailedOutcome(
                QuantumEspressoProcessFailureKind.SIGNAL
            )
        if type(termination) is QuantumEspressoProcessTimeout:
            return QuantumEspressoProcessFailedOutcome(
                QuantumEspressoProcessFailureKind.TIMEOUT
            )
        assert type(termination) is QuantumEspressoNormalProcessExit
        if report.kind is QuantumEspressoDiagnosticReportKind.FATAL:
            fatal = tuple(
                sorted(
                    (
                        observation.identity
                        for observation in report.observations
                        if observation.disposition
                        is QuantumEspressoDiagnosticDisposition.FATAL
                    ),
                    key=lambda value: value.value,
                )
            )
            if not fatal:
                return self._unresolved(
                    report, "fatal-report-without-fatal-observation"
                )
            return QuantumEspressoCalculatorFailedOutcome(fatal)
        if termination.exit_code != 0:
            return QuantumEspressoProcessFailedOutcome(
                QuantumEspressoProcessFailureKind.NONZERO_EXIT
            )
        if report.kind is not QuantumEspressoDiagnosticReportKind.CLEAR:
            return self._unresolved(report, "unsupported-report-kind")
        if not report.completion_markers:
            return self._unresolved(report, "missing-completion-marker")
        if not self._required_candidates_present(manifest, specification):
            return self._unresolved(report, "required-native-output-missing")
        return QuantumEspressoCompletedOutcome(
            tuple(
                sorted(
                    (value.identity for value in report.completion_markers),
                    key=lambda value: value.value,
                )
            )
        )

    def _compatibility_mismatch(
        self,
        process: QuantumEspressoProcessObservation,
        report: QuantumEspressoDiagnosticReport,
        manifest: QuantumEspressoNativeOutputManifest,
        specification: QuantumEspressoNativeOutputExtractionSpecification,
    ) -> str | None:
        configuration = process.executable_configuration_identity
        if (
            report.executable_configuration_identity != configuration
            or specification.executable_configuration_identity != configuration
        ):
            return "executable-configuration-mismatch"
        if (
            report.program is not specification.program
            or report.executable_kind is not specification.executable_kind
            or report.program_version != specification.program_version
        ):
            return "program-version-binding-mismatch"
        if (
            report.stdout_content_identity != process.stdout.content_identity
            or report.stderr_content_identity != process.stderr.content_identity
        ):
            return "stream-content-mismatch"
        if (
            manifest.preparation_identity != process.preparation_identity
            or manifest.after_snapshot_identity != process.after_snapshot_identity
            or manifest.extraction_specification_identity != specification.identity
        ):
            return "observation-lineage-mismatch"
        manifest_by_role = {entry.role: entry for entry in manifest.entries}
        stdout = manifest_by_role.get(QuantumEspressoNativeOutputRole.STDOUT)
        stderr = manifest_by_role.get(QuantumEspressoNativeOutputRole.STDERR)
        if stdout is None or stderr is None:
            return "stream-manifest-entry-missing"
        if (
            stdout.artifact_identity != process.stdout.artifact_identity
            or stderr.artifact_identity != process.stderr.artifact_identity
            or type(stdout.content) is not QuantumEspressoFileArtifactContent
            or type(stderr.content) is not QuantumEspressoFileArtifactContent
        ):
            return "stream-manifest-identity-mismatch"
        if (
            stdout.content.content_identity != process.stdout.content_identity
            or stderr.content.content_identity != process.stderr.content_identity
        ):
            return "stream-manifest-content-mismatch"
        return None

    @staticmethod
    def _required_candidates_present(
        manifest: QuantumEspressoNativeOutputManifest,
        specification: QuantumEspressoNativeOutputExtractionSpecification,
    ) -> bool:
        entries = {entry.artifact_identity: entry for entry in manifest.entries}
        for candidate in specification.candidates:
            if not candidate.required:
                continue
            entry = entries.get(candidate.artifact_identity)
            if entry is None:
                return False
            if (
                entry.role is not candidate.role
                or entry.relative_path != candidate.relative_path
                or entry.entry_type is not candidate.entry_type
            ):
                return False
        return True

    def _unresolved(
        self,
        report: QuantumEspressoDiagnosticReport,
        reason: str,
    ) -> QuantumEspressoDiagnosticUnresolvedOutcome:
        diagnostics = tuple(
            sorted(
                (value.identity for value in report.observations),
                key=lambda value: value.value,
            )
        )
        payload = (
            self.resolver_version + "\n" + report.identity.value + "\n" + reason
        ).encode("utf-8")
        reason_identity = (
            "qe-outcome-unresolved-v1:" + hashlib.sha256(payload).hexdigest()
        )
        return QuantumEspressoDiagnosticUnresolvedOutcome(
            diagnostic_identities=diagnostics,
            reason_identities=(reason_identity,),
        )
