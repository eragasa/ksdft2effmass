r"""Software verification of ``QeDiagnosticClassifier``.

Evidence profile: routine

Bounded artifact scope: fixture-only diagnostic classification by
``QeDiagnosticClassifier``.

Facet and represented meaning

The ActionObject classifies exact deterministic-fixture diagnostic lines and
completion markers from independently captured stdout and stderr bytes.

Intrinsic and cross-object scope

Tests cover fixture catalog binding, exact stream identities and spans, known
nonblocking and fatal diagnostics, unknown and contradictory output, and canonical
public API ownership. Process outcome resolution and scientific interpretation remain
separate.

VVUQ and scientific exclusions

This is software verification with synthetic bytes. The classifier supports no real
Quantum ESPRESSO version, invokes no executable, and establishes no numerical
verification, scientific validation, uncertainty quantification, or physical claim.
"""

import hashlib

import pytest

import ksdft2effmass.integration.quantum_espresso as quantum_espresso
from ksdft2effmass.integration.quantum_espresso import (
    QeDiagnosticCatalog,
    QeDiagnosticChannel,
    QeDiagnosticClassificationRequest,
    QeDiagnosticClassifier,
    QeDiagnosticClassifierIdentity,
    QeDiagnosticDisposition,
    QeDiagnosticReportIdentity,
    QeDiagnosticReportKind,
    QeExecutableConfiguration,
    QeExecutableConfigurationIdentity,
    QeExecutableKind,
    QeProgram,
)
from ksdft2effmass.workflows import ArtifactContentIdentity

pytestmark = pytest.mark.software_verification

SUT = QeDiagnosticClassifier


class TestQeDiagnosticClassifier:
    """Own software verification of the fixture-only diagnostic classifier."""

    @staticmethod
    def content_identity(content: bytes) -> ArtifactContentIdentity:
        """Evidence ID: This helper owns no identifier.

        Requirement: Provide deterministic typed support for this module's test owners.

        Acceptance: Behavior remains exact and confined to the calling test.
        """
        return ArtifactContentIdentity(
            "sha256", hashlib.sha256(content).hexdigest(), len(content)
        )

    @classmethod
    def configuration(cls) -> QeExecutableConfiguration:
        """Evidence ID: This helper owns no identifier.

        Requirement: Provide deterministic typed support for this module's test owners.

        Acceptance: Behavior remains exact and confined to the calling test.
        """
        catalog = QeDiagnosticCatalog.fixture_pw_v1()
        return QeExecutableConfiguration(
            identity=QeExecutableConfigurationIdentity("fixture.pw"),
            program=QeProgram.PW,
            executable_kind=QeExecutableKind.DETERMINISTIC_FIXTURE,
            executable_content_identity=cls.content_identity(b"fixture executable"),
            program_version="fixture-pw-v1",
            argument_suffix=(),
            environment_additions=(),
            classifier_identity=catalog.classifier_identity,
            contract_version="qe-executable-configuration:1",
        )

    @classmethod
    def request(
        cls,
        stdout: bytes,
        stderr: bytes,
        *,
        identity: str,
    ) -> QeDiagnosticClassificationRequest:
        """Evidence ID: This helper owns no identifier.

        Requirement: Provide deterministic typed support for this module's test owners.

        Acceptance: Behavior remains exact and confined to the calling test.
        """
        return QeDiagnosticClassificationRequest(
            report_identity=QeDiagnosticReportIdentity(identity),
            configuration=cls.configuration(),
            stdout=stdout,
            stderr=stderr,
            stdout_content_identity=cls.content_identity(stdout),
            stderr_content_identity=cls.content_identity(stderr),
            claim_boundary=("synthetic fixture diagnostic classification",),
        )

    def test_classmethod__fixture_pw_v1__binds_only_fixture_configuration(
        self,
    ) -> None:
        """Evidence ID: SV-QE-DIAGNOSTIC-001

        Requirement: The initial catalog is bound to one deterministic fixture kind,
        ``pw`` role, version, and classifier identity without claiming real QE support.

        Acceptance: Exact fixture fields are retained and constructing a real-QE
        catalog raises ``ValueError``.
        """
        catalog = QeDiagnosticCatalog.fixture_pw_v1()

        assert catalog.executable_kind is (QeExecutableKind.DETERMINISTIC_FIXTURE)
        assert catalog.program is QeProgram.PW
        assert catalog.program_version == "fixture-pw-v1"
        with pytest.raises(ValueError):
            QeDiagnosticCatalog(
                classifier_identity=catalog.classifier_identity,
                executable_kind=QeExecutableKind.QUANTUM_ESPRESSO,
                program=catalog.program,
                program_version="7.5",
                diagnostic_signatures=catalog.diagnostic_signatures,
                marker_signatures=catalog.marker_signatures,
            )

    def test_method__execute__accepts_known_nonblocking_stderr_independently(
        self,
    ) -> None:
        """Evidence ID: SV-QE-DIAGNOSTIC-002

        Requirement: A recognized nonblocking stderr diagnostic does not override an
        independently recognized stdout completion marker.

        Acceptance: The report is exactly ``clear`` with one stderr nonblocking
        observation, one stdout marker, and exact stream identities.
        """
        stdout = b"fixture output\nJOB DONE.\n"
        stderr = b"DIAGNOSTIC: NONBLOCKING synthetic floating-point notice\n"
        report = QeDiagnosticClassifier(QeDiagnosticCatalog.fixture_pw_v1()).execute(
            self.request(stdout, stderr, identity="report.clear")
        )

        assert report.kind is QeDiagnosticReportKind.CLEAR
        assert len(report.observations) == 1
        assert report.observations[0].channel is (QeDiagnosticChannel.STDERR)
        assert report.observations[0].disposition is (
            QeDiagnosticDisposition.NONBLOCKING
        )
        assert report.stderr_content_identity == self.content_identity(stderr)
        assert len(report.completion_markers) == 1
        assert report.completion_markers[0].channel is (QeDiagnosticChannel.STDOUT)

    def test_method__execute__joins_known_stdout_fatal_and_secondary_stderr(
        self,
    ) -> None:
        """Evidence ID: SV-QE-DIAGNOSTIC-003

        Requirement: Fatal primary stdout and secondary stderr diagnostics are
        classified together without treating stderr as the sole error channel.

        Acceptance: The report is ``fatal`` and preserves one observation from each
        channel with fatal and secondary-fatal dispositions.
        """
        stdout = b"DIAGNOSTIC: FATAL c_bands too many bands are not converged\n"
        stderr = b"DIAGNOSTIC: SECONDARY synthetic MPI_ABORT\n"
        report = QeDiagnosticClassifier(QeDiagnosticCatalog.fixture_pw_v1()).execute(
            self.request(stdout, stderr, identity="report.fatal")
        )

        assert report.kind is QeDiagnosticReportKind.FATAL
        assert {value.channel for value in report.observations} == {
            QeDiagnosticChannel.STDOUT,
            QeDiagnosticChannel.STDERR,
        }
        assert {value.disposition for value in report.observations} == {
            QeDiagnosticDisposition.FATAL,
            QeDiagnosticDisposition.SECONDARY_FATAL,
        }

    @pytest.mark.parametrize(
        ("stderr", "report_identity"),
        [
            pytest.param(
                b"DIAGNOSTIC: UNKNOWN synthetic condition\n",
                "report.unknown",
                id="unknown_signature",
            ),
            pytest.param(
                b"DIAGNOSTIC: NONBLOCKING synthetic floating-point notice!\n",
                "report.near_miss",
                id="one_character_near_miss",
            ),
        ],
    )
    def test_method__execute__fails_closed_for_unknown_and_near_miss_lines(
        self,
        stderr: bytes,
        report_identity: str,
    ) -> None:
        """Evidence ID: SV-QE-DIAGNOSTIC-004

        Requirement: Every fixture diagnostic-prefixed line without an exact catalog
        signature remains explicitly unresolved.

        Acceptance: Unknown and one-character near-miss lines each produce an
        ``unresolved`` report with no signature identity.
        """
        classifier = QeDiagnosticClassifier(QeDiagnosticCatalog.fixture_pw_v1())
        report = classifier.execute(
            self.request(b"JOB DONE.\n", stderr, identity=report_identity)
        )

        assert report.kind is QeDiagnosticReportKind.UNRESOLVED
        assert report.observations[0].disposition is (
            QeDiagnosticDisposition.UNRESOLVED
        )
        assert report.observations[0].signature_identity is None

    def test_method__execute__reports_contradictory_fatal_completion_or_secondary(
        self,
    ) -> None:
        """Evidence ID: SV-QE-DIAGNOSTIC-005

        Requirement: A fatal diagnostic combined with a completion marker, or a
        secondary-fatal diagnostic without its primary fatal, is not silently resolved.

        Acceptance: Both exact combinations produce ``contradictory`` reports.
        """
        classifier = QeDiagnosticClassifier(QeDiagnosticCatalog.fixture_pw_v1())
        fatal_with_completion = classifier.execute(
            self.request(
                b"DIAGNOSTIC: FATAL c_bands too many bands are not converged\n"
                b"JOB DONE.\n",
                b"DIAGNOSTIC: SECONDARY synthetic MPI_ABORT\n",
                identity="report.contradictory.fatal",
            )
        )
        secondary_alone = classifier.execute(
            self.request(
                b"ordinary output\n",
                b"DIAGNOSTIC: SECONDARY synthetic MPI_ABORT\n",
                identity="report.contradictory.secondary",
            )
        )

        assert fatal_with_completion.kind is (QeDiagnosticReportKind.CONTRADICTORY)
        assert secondary_alone.kind is (QeDiagnosticReportKind.CONTRADICTORY)

    def test_method__execute__rejects_stream_or_catalog_identity_mismatch(
        self,
    ) -> None:
        """Evidence ID: SV-QE-DIAGNOSTIC-006

        Requirement: Classification requires exact stream content identities and the
        exact classifier/program/version binding.

        Acceptance: A changed stream and a changed classifier identity each raise
        ``ValueError`` rather than returning a diagnostic report.
        """
        catalog = QeDiagnosticCatalog.fixture_pw_v1()
        classifier = QeDiagnosticClassifier(catalog)
        request = self.request(b"JOB DONE.\n", b"", identity="report.identity")
        with pytest.raises(ValueError):
            classifier.execute(
                QeDiagnosticClassificationRequest(
                    report_identity=request.report_identity,
                    configuration=request.configuration,
                    stdout=request.stdout + b"changed",
                    stderr=request.stderr,
                    stdout_content_identity=request.stdout_content_identity,
                    stderr_content_identity=request.stderr_content_identity,
                    claim_boundary=request.claim_boundary,
                )
            )
        wrong_configuration = QeExecutableConfiguration(
            identity=request.configuration.identity,
            program=request.configuration.program,
            executable_kind=request.configuration.executable_kind,
            executable_content_identity=(
                request.configuration.executable_content_identity
            ),
            program_version=request.configuration.program_version,
            argument_suffix=(),
            environment_additions=(),
            classifier_identity=QeDiagnosticClassifierIdentity("other-classifier"),
            contract_version=request.configuration.contract_version,
        )
        with pytest.raises(ValueError):
            classifier.execute(
                QeDiagnosticClassificationRequest(
                    report_identity=request.report_identity,
                    configuration=wrong_configuration,
                    stdout=request.stdout,
                    stderr=request.stderr,
                    stdout_content_identity=request.stdout_content_identity,
                    stderr_content_identity=request.stderr_content_identity,
                    claim_boundary=request.claim_boundary,
                )
            )

    def test_method__execute__retains_exact_byte_spans_without_cross_stream_order(
        self,
    ) -> None:
        """Evidence ID: SV-QE-DIAGNOSTIC-007

        Requirement: Every diagnostic and marker identifies a zero-based half-open
        byte span within its own exact stream without claiming temporal stream order.

        Acceptance: Independently counted offsets and span bytes reproduce every
        observation's retained content identity exactly.
        """
        stdout = b"prefix\nDIAGNOSTIC: FATAL c_bands too many bands are not converged\n"
        stderr = b"prefix\nDIAGNOSTIC: SECONDARY synthetic MPI_ABORT\n"
        report = QeDiagnosticClassifier(QeDiagnosticCatalog.fixture_pw_v1()).execute(
            self.request(stdout, stderr, identity="report.spans")
        )

        stderr_observation, stdout_observation = report.observations
        assert stdout_observation.channel is QeDiagnosticChannel.STDOUT
        assert stderr_observation.channel is QeDiagnosticChannel.STDERR
        stdout_span = stdout[
            stdout_observation.byte_start : stdout_observation.byte_end
        ]
        stderr_span = stderr[
            stderr_observation.byte_start : stderr_observation.byte_end
        ]
        assert (
            self.content_identity(stdout_span)
            == stdout_observation.span_content_identity
        )
        assert (
            self.content_identity(stderr_span)
            == stderr_observation.span_content_identity
        )

    def test_public_api__package__owns_classifier_canonically(self) -> None:
        """Evidence ID: SV-QE-DIAGNOSTIC-008

        Requirement: The canonical underscored Quantum ESPRESSO package owns and
        exports the public classifier.

        Acceptance: The canonical root exports the exact SUT.
        """
        assert quantum_espresso.QeDiagnosticClassifier is SUT
        assert "QeDiagnosticClassifier" in quantum_espresso.__all__
