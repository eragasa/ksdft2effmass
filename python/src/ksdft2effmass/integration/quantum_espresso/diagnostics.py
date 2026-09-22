"""Version-bound diagnostic classification for exact QE process streams.

The closed catalogs support the deterministic fixture and one exact real-QE ``pw``
version. Real-QE classification is deliberately conservative: every unrecognized
nonempty stderr line remains unresolved, and a completion marker is not a scientific
or numerical acceptance claim.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass

from ksdft2effmass.workflows import ArtifactContentIdentity

from .contracts import (
    QuantumEspressoDiagnosticChannel,
    QuantumEspressoDiagnosticClassifierIdentity,
    QuantumEspressoDiagnosticDisposition,
    QuantumEspressoDiagnosticObservation,
    QuantumEspressoDiagnosticObservationIdentity,
    QuantumEspressoDiagnosticReport,
    QuantumEspressoDiagnosticReportIdentity,
    QuantumEspressoDiagnosticReportKind,
    QuantumEspressoExecutableConfiguration,
    QuantumEspressoExecutableKind,
    QuantumEspressoOutputMarkerObservation,
    QuantumEspressoOutputMarkerObservationIdentity,
    QuantumEspressoProgram,
)


@dataclass(frozen=True, slots=True, kw_only=True)
class QuantumEspressoDiagnosticSignature:
    """Represent one exact version-bound diagnostic-line signature.

    Attributes
    ----------
    identity
        Exact nominal identity retained for cross-record correlation.
    channel
        Independent stdout or stderr channel.
    exact_line
        Exact complete line admitted by this versioned signature.
    disposition
        Closed admission disposition for this result.
    sanitized_summary
        Bounded diagnostic meaning without raw-path or scientific claims.
    """

    identity: str
    channel: QuantumEspressoDiagnosticChannel
    exact_line: bytes
    disposition: QuantumEspressoDiagnosticDisposition
    sanitized_summary: str

    def __post_init__(self) -> None:
        if type(self.identity) is not str:
            raise TypeError("identity must be a built-in str")
        if not self.identity:
            raise ValueError("identity must not be empty")
        if type(self.channel) is not QuantumEspressoDiagnosticChannel:
            raise TypeError("channel must be QuantumEspressoDiagnosticChannel")
        if type(self.exact_line) is not bytes:
            raise TypeError("exact_line must be built-in bytes")
        if not self.exact_line or b"\n" in self.exact_line or b"\r" in self.exact_line:
            raise ValueError("exact_line must be one nonempty line without terminator")
        if type(self.disposition) is not QuantumEspressoDiagnosticDisposition:
            raise TypeError("disposition must be QuantumEspressoDiagnosticDisposition")
        if self.disposition is QuantumEspressoDiagnosticDisposition.UNRESOLVED:
            raise ValueError("catalog signatures must have a known disposition")
        if type(self.sanitized_summary) is not str:
            raise TypeError("sanitized_summary must be a built-in str")
        if not self.sanitized_summary:
            raise ValueError("sanitized_summary must not be empty")


@dataclass(frozen=True, slots=True, kw_only=True)
class QuantumEspressoOutputMarkerSignature:
    """Represent one exact version-bound completion-marker line signature.

    Attributes
    ----------
    identity
        Exact nominal identity retained for cross-record correlation.
    channel
        Independent stdout or stderr channel.
    exact_line
        Exact complete line admitted as a completion marker.
    """

    identity: str
    channel: QuantumEspressoDiagnosticChannel
    exact_line: bytes

    def __post_init__(self) -> None:
        if type(self.identity) is not str:
            raise TypeError("identity must be a built-in str")
        if not self.identity:
            raise ValueError("identity must not be empty")
        if type(self.channel) is not QuantumEspressoDiagnosticChannel:
            raise TypeError("channel must be QuantumEspressoDiagnosticChannel")
        if type(self.exact_line) is not bytes:
            raise TypeError("exact_line must be built-in bytes")
        if not self.exact_line or b"\n" in self.exact_line or b"\r" in self.exact_line:
            raise ValueError("exact_line must be one nonempty line without terminator")


@dataclass(frozen=True, slots=True, kw_only=True)
class QuantumEspressoDiagnosticCatalog:
    """Bind one immutable classifier catalog to an exact executable configuration.

    Attributes
    ----------
    classifier_identity
        Exact nominal identity retained for cross-record correlation.
    executable_kind
        Closed real-executable or deterministic-fixture namespace.
    program
        Closed Quantum ESPRESSO program role.
    program_version
        Exact admitted executable program version string.
    diagnostic_signatures
        Canonical immutable exact diagnostic-signature catalog.
    marker_signatures
        Canonical immutable exact completion-marker catalog.
    unresolved_line_channels
        Canonical channels whose unrecognized nonempty lines fail closed.
    observation_claim_boundary
        Nonempty limits attached to every classified diagnostic observation.
    """

    classifier_identity: QuantumEspressoDiagnosticClassifierIdentity
    executable_kind: QuantumEspressoExecutableKind
    program: QuantumEspressoProgram
    program_version: str
    diagnostic_signatures: tuple[QuantumEspressoDiagnosticSignature, ...]
    marker_signatures: tuple[QuantumEspressoOutputMarkerSignature, ...]
    unresolved_line_channels: tuple[QuantumEspressoDiagnosticChannel, ...]
    observation_claim_boundary: tuple[str, ...]

    def __post_init__(self) -> None:
        if type(self.classifier_identity) is not (
            QuantumEspressoDiagnosticClassifierIdentity
        ):
            raise TypeError(
                "classifier_identity must be "
                "QuantumEspressoDiagnosticClassifierIdentity"
            )
        if type(self.executable_kind) is not QuantumEspressoExecutableKind:
            raise TypeError("executable_kind must be QuantumEspressoExecutableKind")
        if type(self.program) is not QuantumEspressoProgram:
            raise TypeError("program must be QuantumEspressoProgram")
        if type(self.program_version) is not str:
            raise TypeError("program_version must be a built-in str")
        supported = (
            self.executable_kind is QuantumEspressoExecutableKind.DETERMINISTIC_FIXTURE
            and self.program is QuantumEspressoProgram.PW
            and self.program_version == "fixture-pw-v1"
        ) or (
            self.executable_kind is QuantumEspressoExecutableKind.QUANTUM_ESPRESSO
            and self.program is QuantumEspressoProgram.PW
            and self.program_version == "7.2"
        )
        if not supported:
            raise ValueError("diagnostic catalog executable binding is unsupported")
        signatures = self.diagnostic_signatures
        if type(signatures) is not tuple or any(
            type(value) is not QuantumEspressoDiagnosticSignature
            for value in signatures
        ):
            raise TypeError(
                "diagnostic_signatures must contain "
                "QuantumEspressoDiagnosticSignature values"
            )
        if signatures != tuple(sorted(signatures, key=lambda value: value.identity)):
            raise ValueError("diagnostic_signatures must be lexically ordered")
        if len({value.identity for value in signatures}) != len(signatures) or len(
            {(value.channel, value.exact_line) for value in signatures}
        ) != len(signatures):
            raise ValueError("diagnostic signatures must be unique")
        markers = self.marker_signatures
        if type(markers) is not tuple or any(
            type(value) is not QuantumEspressoOutputMarkerSignature for value in markers
        ):
            raise TypeError(
                "marker_signatures must contain "
                "QuantumEspressoOutputMarkerSignature values"
            )
        if markers != tuple(sorted(markers, key=lambda value: value.identity)):
            raise ValueError("marker_signatures must be lexically ordered")
        if len({value.identity for value in markers}) != len(markers) or len(
            {(value.channel, value.exact_line) for value in markers}
        ) != len(markers):
            raise ValueError("marker signatures must be unique")
        channels = self.unresolved_line_channels
        if type(channels) is not tuple or any(
            type(value) is not QuantumEspressoDiagnosticChannel for value in channels
        ):
            raise TypeError(
                "unresolved_line_channels must contain "
                "QuantumEspressoDiagnosticChannel values"
            )
        if channels != tuple(sorted(set(channels), key=lambda value: value.value)):
            raise ValueError("unresolved_line_channels must be unique and ordered")
        boundary = self.observation_claim_boundary
        if type(boundary) is not tuple or any(
            type(value) is not str for value in boundary
        ):
            raise TypeError(
                "observation_claim_boundary must contain built-in str values"
            )
        if not boundary or any(not value for value in boundary):
            raise ValueError("observation_claim_boundary must contain nonempty strings")
        if self.executable_kind is QuantumEspressoExecutableKind.DETERMINISTIC_FIXTURE:
            if any(
                not value.exact_line.startswith(b"DIAGNOSTIC: ") for value in signatures
            ):
                raise ValueError(
                    "fixture diagnostic signatures must use the fixture line prefix"
                )
        else:
            expected_boundary = (
                "text classification does not establish numerical convergence",
                "text classification does not establish scientific validity",
            )
            marker = markers[0] if len(markers) == 1 else None
            if (
                self.classifier_identity.value != "qe-diagnostic-classifier.pw-7.2:1"
                or signatures
                or marker is None
                or marker.identity != "qe.pw-7.2.job-done.v1"
                or marker.channel is not QuantumEspressoDiagnosticChannel.STDOUT
                or marker.exact_line != b"JOB DONE."
                or channels != (QuantumEspressoDiagnosticChannel.STDERR,)
                or boundary != expected_boundary
            ):
                raise ValueError("real-QE catalog must equal the closed pw 7.2 catalog")

    @classmethod
    def fixture_pw_v1(cls) -> QuantumEspressoDiagnosticCatalog:
        """Return the exact deterministic fixture ``pw`` catalog."""
        return cls(
            classifier_identity=QuantumEspressoDiagnosticClassifierIdentity(
                "qe-diagnostic-classifier.fixture-pw:1"
            ),
            executable_kind=QuantumEspressoExecutableKind.DETERMINISTIC_FIXTURE,
            program=QuantumEspressoProgram.PW,
            program_version="fixture-pw-v1",
            diagnostic_signatures=(
                QuantumEspressoDiagnosticSignature(
                    identity="fixture.pw.fatal-c-bands.v1",
                    channel=QuantumEspressoDiagnosticChannel.STDOUT,
                    exact_line=(
                        b"DIAGNOSTIC: FATAL c_bands too many bands are not converged"
                    ),
                    disposition=QuantumEspressoDiagnosticDisposition.FATAL,
                    sanitized_summary="fixture calculator fatal diagnostic",
                ),
                QuantumEspressoDiagnosticSignature(
                    identity="fixture.pw.nonblocking-floating-point.v1",
                    channel=QuantumEspressoDiagnosticChannel.STDERR,
                    exact_line=(
                        b"DIAGNOSTIC: NONBLOCKING synthetic floating-point notice"
                    ),
                    disposition=QuantumEspressoDiagnosticDisposition.NONBLOCKING,
                    sanitized_summary="fixture nonblocking diagnostic",
                ),
                QuantumEspressoDiagnosticSignature(
                    identity="fixture.pw.secondary-mpi-abort.v1",
                    channel=QuantumEspressoDiagnosticChannel.STDERR,
                    exact_line=b"DIAGNOSTIC: SECONDARY synthetic MPI_ABORT",
                    disposition=QuantumEspressoDiagnosticDisposition.SECONDARY_FATAL,
                    sanitized_summary="fixture secondary fatal diagnostic",
                ),
            ),
            marker_signatures=(
                QuantumEspressoOutputMarkerSignature(
                    identity="fixture.pw.job-done.v1",
                    channel=QuantumEspressoDiagnosticChannel.STDOUT,
                    exact_line=b"JOB DONE.",
                ),
            ),
            unresolved_line_channels=(),
            observation_claim_boundary=(
                "fixture-only diagnostic classification; no real QE claim",
            ),
        )

    @classmethod
    def qe_pw_7_2_v1(cls) -> QuantumEspressoDiagnosticCatalog:
        """Return the conservative catalog for the exact real-QE ``pw`` 7.2 version."""
        return cls(
            classifier_identity=QuantumEspressoDiagnosticClassifierIdentity(
                "qe-diagnostic-classifier.pw-7.2:1"
            ),
            executable_kind=QuantumEspressoExecutableKind.QUANTUM_ESPRESSO,
            program=QuantumEspressoProgram.PW,
            program_version="7.2",
            diagnostic_signatures=(),
            marker_signatures=(
                QuantumEspressoOutputMarkerSignature(
                    identity="qe.pw-7.2.job-done.v1",
                    channel=QuantumEspressoDiagnosticChannel.STDOUT,
                    exact_line=b"JOB DONE.",
                ),
            ),
            unresolved_line_channels=(QuantumEspressoDiagnosticChannel.STDERR,),
            observation_claim_boundary=(
                "text classification does not establish numerical convergence",
                "text classification does not establish scientific validity",
            ),
        )


@dataclass(frozen=True, slots=True, kw_only=True)
class QuantumEspressoDiagnosticClassificationRequest:
    """Supply exact captured streams and configuration for classification.

    Attributes
    ----------
    report_identity
        Exact nominal identity retained for cross-record correlation.
    configuration
        Exact executable configuration governing classification.
    stdout
        Exact standard-output bytes to classify.
    stderr
        Exact standard-error bytes to classify.
    stdout_content_identity
        Exact nominal identity retained for cross-record correlation.
    stderr_content_identity
        Exact nominal identity retained for cross-record correlation.
    claim_boundary
        Nonempty immutable statements limiting evidentiary interpretation.
    """

    report_identity: QuantumEspressoDiagnosticReportIdentity
    configuration: QuantumEspressoExecutableConfiguration
    stdout: bytes
    stderr: bytes
    stdout_content_identity: ArtifactContentIdentity
    stderr_content_identity: ArtifactContentIdentity
    claim_boundary: tuple[str, ...]

    def __post_init__(self) -> None:
        if type(self.report_identity) is not QuantumEspressoDiagnosticReportIdentity:
            raise TypeError(
                "report_identity must be QuantumEspressoDiagnosticReportIdentity"
            )
        if type(self.configuration) is not QuantumEspressoExecutableConfiguration:
            raise TypeError(
                "configuration must be QuantumEspressoExecutableConfiguration"
            )
        if type(self.stdout) is not bytes:
            raise TypeError("stdout must be built-in bytes")
        if type(self.stderr) is not bytes:
            raise TypeError("stderr must be built-in bytes")
        if type(self.stdout_content_identity) is not ArtifactContentIdentity:
            raise TypeError("stdout_content_identity must be ArtifactContentIdentity")
        if type(self.stderr_content_identity) is not ArtifactContentIdentity:
            raise TypeError("stderr_content_identity must be ArtifactContentIdentity")
        if type(self.claim_boundary) is not tuple or any(
            type(value) is not str for value in self.claim_boundary
        ):
            raise TypeError("claim_boundary must contain built-in str values")
        if not self.claim_boundary or any(not value for value in self.claim_boundary):
            raise ValueError("claim_boundary must contain nonempty strings")


@dataclass(frozen=True, slots=True)
class QuantumEspressoDiagnosticClassifier:
    """Classify version-bound diagnostics from stdout and stderr independently.

    Attributes
    ----------
    catalog
        Immutable executable- and version-bound diagnostic catalog.
    """

    catalog: QuantumEspressoDiagnosticCatalog

    def __post_init__(self) -> None:
        if type(self.catalog) is not QuantumEspressoDiagnosticCatalog:
            raise TypeError("catalog must be QuantumEspressoDiagnosticCatalog")

    def execute(
        self,
        request: QuantumEspressoDiagnosticClassificationRequest,
    ) -> QuantumEspressoDiagnosticReport:
        """Return one closed report or raise for integration identity mismatch."""
        if type(request) is not QuantumEspressoDiagnosticClassificationRequest:
            raise TypeError(
                "request must be QuantumEspressoDiagnosticClassificationRequest"
            )
        self._require_configuration(request.configuration)
        self._require_content_identity(
            request.stdout, request.stdout_content_identity, "stdout"
        )
        self._require_content_identity(
            request.stderr, request.stderr_content_identity, "stderr"
        )
        observations = tuple(
            sorted(
                (
                    *self._diagnostics(
                        QuantumEspressoDiagnosticChannel.STDOUT,
                        request.stdout,
                        request.stdout_content_identity,
                    ),
                    *self._diagnostics(
                        QuantumEspressoDiagnosticChannel.STDERR,
                        request.stderr,
                        request.stderr_content_identity,
                    ),
                ),
                key=lambda value: (
                    value.channel.value,
                    value.byte_start,
                    value.byte_end,
                    value.identity.value,
                ),
            )
        )
        markers = tuple(
            sorted(
                (
                    *self._markers(
                        QuantumEspressoDiagnosticChannel.STDOUT,
                        request.stdout,
                        request.stdout_content_identity,
                    ),
                    *self._markers(
                        QuantumEspressoDiagnosticChannel.STDERR,
                        request.stderr,
                        request.stderr_content_identity,
                    ),
                ),
                key=lambda value: (
                    value.channel.value,
                    value.byte_start,
                    value.byte_end,
                    value.identity.value,
                ),
            )
        )
        return QuantumEspressoDiagnosticReport(
            identity=request.report_identity,
            classifier_identity=self.catalog.classifier_identity,
            executable_configuration_identity=request.configuration.identity,
            executable_kind=request.configuration.executable_kind,
            program=request.configuration.program,
            program_version=request.configuration.program_version,
            stdout_content_identity=request.stdout_content_identity,
            stderr_content_identity=request.stderr_content_identity,
            observations=observations,
            completion_markers=markers,
            kind=self._report_kind(observations, markers),
            claim_boundary=request.claim_boundary,
        )

    def _require_configuration(
        self, configuration: QuantumEspressoExecutableConfiguration
    ) -> None:
        catalog = self.catalog
        if (
            configuration.classifier_identity != catalog.classifier_identity
            or configuration.executable_kind is not catalog.executable_kind
            or configuration.program is not catalog.program
            or configuration.program_version != catalog.program_version
        ):
            raise ValueError(
                "executable configuration does not match the classifier catalog"
            )

    @staticmethod
    def _require_content_identity(
        content: bytes,
        identity: ArtifactContentIdentity,
        channel: str,
    ) -> None:
        digest = hashlib.sha256(content).hexdigest()
        if identity.digest != digest or identity.byte_count != len(content):
            raise ValueError(f"{channel} bytes do not match their content identity")

    def _diagnostics(
        self,
        channel: QuantumEspressoDiagnosticChannel,
        content: bytes,
        content_identity: ArtifactContentIdentity,
    ) -> tuple[QuantumEspressoDiagnosticObservation, ...]:
        signatures = {
            value.exact_line: value
            for value in self.catalog.diagnostic_signatures
            if value.channel is channel
        }
        observations: list[QuantumEspressoDiagnosticObservation] = []
        for start, end, line in self._lines(content):
            signature = signatures.get(line)
            fixture_diagnostic = line.startswith(b"DIAGNOSTIC: ")
            fail_closed_channel = channel in self.catalog.unresolved_line_channels
            if signature is None and not fixture_diagnostic and not fail_closed_channel:
                continue
            disposition = (
                QuantumEspressoDiagnosticDisposition.UNRESOLVED
                if signature is None
                else signature.disposition
            )
            signature_identity = None if signature is None else signature.identity
            summary = (
                "unrecognized version-bound diagnostic line"
                if signature is None
                else signature.sanitized_summary
            )
            identity_value = self._derived_identity(
                "diagnostic",
                channel,
                content_identity,
                start,
                end,
                signature_identity or "unresolved",
            )
            observations.append(
                QuantumEspressoDiagnosticObservation(
                    identity=QuantumEspressoDiagnosticObservationIdentity(
                        identity_value
                    ),
                    channel=channel,
                    byte_start=start,
                    byte_end=end,
                    stream_content_identity=content_identity,
                    span_content_identity=self._content_identity(line),
                    signature_identity=signature_identity,
                    disposition=disposition,
                    sanitized_summary=summary,
                    claim_boundary=self.catalog.observation_claim_boundary,
                )
            )
        return tuple(observations)

    def _markers(
        self,
        channel: QuantumEspressoDiagnosticChannel,
        content: bytes,
        content_identity: ArtifactContentIdentity,
    ) -> tuple[QuantumEspressoOutputMarkerObservation, ...]:
        signatures = {
            value.exact_line: value
            for value in self.catalog.marker_signatures
            if value.channel is channel
        }
        observations: list[QuantumEspressoOutputMarkerObservation] = []
        for start, end, line in self._lines(content):
            signature = signatures.get(line)
            if signature is None:
                continue
            identity_value = self._derived_identity(
                "marker",
                channel,
                content_identity,
                start,
                end,
                signature.identity,
            )
            observations.append(
                QuantumEspressoOutputMarkerObservation(
                    identity=QuantumEspressoOutputMarkerObservationIdentity(
                        identity_value
                    ),
                    channel=channel,
                    byte_start=start,
                    byte_end=end,
                    stream_content_identity=content_identity,
                    span_content_identity=self._content_identity(line),
                    signature_identity=signature.identity,
                )
            )
        return tuple(observations)

    @staticmethod
    def _lines(content: bytes) -> tuple[tuple[int, int, bytes], ...]:
        lines: list[tuple[int, int, bytes]] = []
        cursor = 0
        for terminated in content.splitlines(keepends=True):
            line = terminated.rstrip(b"\r\n")
            end = cursor + len(line)
            if line:
                lines.append((cursor, end, line))
            cursor += len(terminated)
        return tuple(lines)

    @staticmethod
    def _content_identity(content: bytes) -> ArtifactContentIdentity:
        return ArtifactContentIdentity(
            "sha256",
            hashlib.sha256(content).hexdigest(),
            len(content),
        )

    @staticmethod
    def _derived_identity(
        role: str,
        channel: QuantumEspressoDiagnosticChannel,
        stream_identity: ArtifactContentIdentity,
        start: int,
        end: int,
        signature_identity: str,
    ) -> str:
        payload = (
            f"{role}\n{channel.value}\n{stream_identity.digest}\n"
            f"{start}\n{end}\n{signature_identity}"
        ).encode()
        return f"qe-{role}:{hashlib.sha256(payload).hexdigest()}"

    @staticmethod
    def _report_kind(
        observations: tuple[QuantumEspressoDiagnosticObservation, ...],
        markers: tuple[QuantumEspressoOutputMarkerObservation, ...],
    ) -> QuantumEspressoDiagnosticReportKind:
        dispositions = {value.disposition for value in observations}
        fatal = QuantumEspressoDiagnosticDisposition.FATAL in dispositions
        secondary = QuantumEspressoDiagnosticDisposition.SECONDARY_FATAL in dispositions
        unresolved = QuantumEspressoDiagnosticDisposition.UNRESOLVED in dispositions
        if (fatal and markers) or (secondary and not fatal):
            return QuantumEspressoDiagnosticReportKind.CONTRADICTORY
        if unresolved:
            return QuantumEspressoDiagnosticReportKind.UNRESOLVED
        if fatal:
            return QuantumEspressoDiagnosticReportKind.FATAL
        return QuantumEspressoDiagnosticReportKind.CLEAR
