r"""Software verification of ``QuantumEspressoDiagnosticClassifier``.

Evidence profile: routine

Bounded artifact scope: deterministic-fixture and exact real-QE ``pw`` 7.2
diagnostic classification by ``QuantumEspressoDiagnosticClassifier``.

Facet and represented meaning

The ActionObject classifies exact version-bound diagnostic lines and completion
markers from independently captured stdout and stderr bytes. The real-QE catalog
fails closed on every unrecognized nonempty stderr line.

Intrinsic and cross-object scope

Tests cover fixture and real-QE catalog binding, exact stream identities and spans,
known nonblocking, unresolved, and fatal diagnostics, unknown and contradictory
output, and canonical public API ownership. Process outcome resolution and scientific
interpretation remain separate.

VVUQ and scientific exclusions

This is software verification with authored bytes reproducing an already retained
observed warning. The classifier invokes no executable and establishes no numerical
verification, scientific validation, uncertainty quantification, or physical claim.
"""

import hashlib
from dataclasses import replace

import pytest

import ksdft2effmass.integration.quantum_espresso as quantum_espresso
from ksdft2effmass.integration.quantum_espresso import (
    QuantumEspressoDiagnosticCatalog,
    QuantumEspressoDiagnosticChannel,
    QuantumEspressoDiagnosticClassificationRequest,
    QuantumEspressoDiagnosticClassifier,
    QuantumEspressoDiagnosticClassifierIdentity,
    QuantumEspressoDiagnosticDisposition,
    QuantumEspressoDiagnosticReportIdentity,
    QuantumEspressoDiagnosticReportKind,
    QuantumEspressoExecutableConfiguration,
    QuantumEspressoExecutableConfigurationIdentity,
    QuantumEspressoExecutableKind,
    QuantumEspressoProgram,
)
from ksdft2effmass.workflows import ArtifactContentIdentity

pytestmark = pytest.mark.software_verification

SUT = QuantumEspressoDiagnosticClassifier


class TestQuantumEspressoDiagnosticClassifier:
    """Own software verification of version-bound diagnostic classification."""

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
    def configuration(cls) -> QuantumEspressoExecutableConfiguration:
        """Evidence ID: This helper owns no identifier.

        Requirement: Provide deterministic typed support for this module's test owners.

        Acceptance: Behavior remains exact and confined to the calling test.
        """
        catalog = QuantumEspressoDiagnosticCatalog.fixture_pw_v1()
        return QuantumEspressoExecutableConfiguration(
            identity=QuantumEspressoExecutableConfigurationIdentity("fixture.pw"),
            program=QuantumEspressoProgram.PW,
            executable_kind=QuantumEspressoExecutableKind.DETERMINISTIC_FIXTURE,
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
    ) -> QuantumEspressoDiagnosticClassificationRequest:
        """Evidence ID: This helper owns no identifier.

        Requirement: Provide deterministic typed support for this module's test owners.

        Acceptance: Behavior remains exact and confined to the calling test.
        """
        return QuantumEspressoDiagnosticClassificationRequest(
            report_identity=QuantumEspressoDiagnosticReportIdentity(identity),
            configuration=cls.configuration(),
            stdout=stdout,
            stderr=stderr,
            stdout_content_identity=cls.content_identity(stdout),
            stderr_content_identity=cls.content_identity(stderr),
            claim_boundary=("synthetic fixture diagnostic classification",),
        )

    @classmethod
    def qe72_configuration(cls) -> QuantumEspressoExecutableConfiguration:
        """Evidence ID: This helper owns no identifier.

        Requirement: Provide the exact real-QE catalog binding with synthetic content.

        Acceptance: The configuration agrees with the QE ``pw`` 7.2 catalog.
        """
        catalog = QuantumEspressoDiagnosticCatalog.qe_pw_7_2_v1()
        return QuantumEspressoExecutableConfiguration(
            identity=QuantumEspressoExecutableConfigurationIdentity("qe.pw.7.2"),
            program=QuantumEspressoProgram.PW,
            executable_kind=QuantumEspressoExecutableKind.QUANTUM_ESPRESSO,
            executable_content_identity=cls.content_identity(
                b"synthetic QE 7.2 executable identity"
            ),
            program_version="7.2",
            argument_suffix=(),
            environment_additions=(),
            classifier_identity=catalog.classifier_identity,
            contract_version="qe-executable-configuration:1",
        )

    @classmethod
    def qe72_request(
        cls,
        stdout: bytes,
        stderr: bytes,
        *,
        identity: str,
    ) -> QuantumEspressoDiagnosticClassificationRequest:
        """Evidence ID: This helper owns no identifier.

        Requirement: Provide typed authored streams for real-QE catalog verification.

        Acceptance: Both exact stream identities agree with their authored bytes.
        """
        return QuantumEspressoDiagnosticClassificationRequest(
            report_identity=QuantumEspressoDiagnosticReportIdentity(identity),
            configuration=cls.qe72_configuration(),
            stdout=stdout,
            stderr=stderr,
            stdout_content_identity=cls.content_identity(stdout),
            stderr_content_identity=cls.content_identity(stderr),
            claim_boundary=(
                "authored diagnostic bytes; no numerical or scientific claim",
            ),
        )

    def test_classmethod__fixture_pw_v1__binds_exact_fixture_configuration(
        self,
    ) -> None:
        """Evidence ID: SV-QE-DIAGNOSTIC-001

        Requirement: The fixture catalog is bound to one deterministic fixture kind,
        ``pw`` role, version, and classifier identity.

        Acceptance: Exact fixture fields are retained and an unsupported real-QE
        version raises ``ValueError``.
        """
        catalog = QuantumEspressoDiagnosticCatalog.fixture_pw_v1()

        assert catalog.executable_kind is (
            QuantumEspressoExecutableKind.DETERMINISTIC_FIXTURE
        )
        assert catalog.program is QuantumEspressoProgram.PW
        assert catalog.program_version == "fixture-pw-v1"
        with pytest.raises(ValueError):
            QuantumEspressoDiagnosticCatalog(
                classifier_identity=catalog.classifier_identity,
                executable_kind=QuantumEspressoExecutableKind.QUANTUM_ESPRESSO,
                program=catalog.program,
                program_version="7.5",
                diagnostic_signatures=catalog.diagnostic_signatures,
                marker_signatures=catalog.marker_signatures,
                unresolved_line_channels=(QuantumEspressoDiagnosticChannel.STDERR,),
                observation_claim_boundary=("synthetic unsupported catalog",),
            )

    def test_classmethod__qe_pw_7_2_v1__binds_conservative_real_catalog(
        self,
    ) -> None:
        """Evidence ID: SV-QE-DIAGNOSTIC-009

        Requirement: Real-QE support must be exact to ``pw`` 7.2 and fail closed on
        every unrecognized nonempty stderr line.

        Acceptance: Program, version, executable kind, classifier identity, and
        unresolved channel policy are exact.
        """
        catalog = QuantumEspressoDiagnosticCatalog.qe_pw_7_2_v1()

        assert catalog.executable_kind is (
            QuantumEspressoExecutableKind.QUANTUM_ESPRESSO
        )
        assert catalog.program is QuantumEspressoProgram.PW
        assert catalog.program_version == "7.2"
        assert catalog.classifier_identity == (
            QuantumEspressoDiagnosticClassifierIdentity(
                "qe-diagnostic-classifier.pw-7.2:1"
            )
        )
        assert catalog.unresolved_line_channels == (
            QuantumEspressoDiagnosticChannel.STDERR,
        )
        with pytest.raises(ValueError):
            replace(
                catalog,
                classifier_identity=QuantumEspressoDiagnosticClassifierIdentity(
                    "qe-diagnostic-classifier.pw-7.2:substituted"
                ),
            )

    @pytest.mark.parametrize(
        "stderr",
        [
            pytest.param(
                b"Note: The following floating-point exceptions are signalling: "
                b"IEEE_INVALID_FLAG IEEE_DIVIDE_BY_ZERO IEEE_OVERFLOW_FLAG "
                b"IEEE_UNDERFLOW_FLAG\n",
                id="retained_ieee_notice",
            ),
            pytest.param(
                b"unrecognized authored stderr line\n",
                id="unrecognized_stderr",
            ),
        ],
    )
    def test_method__execute__fails_closed_for_real_qe_stderr(
        self,
        stderr: bytes,
    ) -> None:
        """Evidence ID: SV-QE-DIAGNOSTIC-010

        Requirement: The retained QE 7.2 IEEE notice and every unknown stderr line
        remain unresolved rather than being treated as harmless or successful.

        Acceptance: Both produce an unresolved report without assigning a known
        diagnostic signature or nonblocking disposition.
        """
        report = QuantumEspressoDiagnosticClassifier(
            QuantumEspressoDiagnosticCatalog.qe_pw_7_2_v1()
        ).execute(
            self.qe72_request(
                b"authored output\nJOB DONE.\n",
                stderr,
                identity="report.qe72.unresolved",
            )
        )

        assert report.kind is QuantumEspressoDiagnosticReportKind.UNRESOLVED
        assert len(report.observations) == 1
        assert report.observations[0].disposition is (
            QuantumEspressoDiagnosticDisposition.UNRESOLVED
        )
        assert report.observations[0].signature_identity is None
        assert len(report.completion_markers) == 1

    def test_method__execute__accepts_empty_real_qe_stderr_with_marker(
        self,
    ) -> None:
        """Evidence ID: SV-QE-DIAGNOSTIC-011

        Requirement: The exact QE 7.2 completion marker with empty stderr must remain
        eligible for separate process/artifact outcome resolution.

        Acceptance: Classification is clear with one marker and no diagnostics,
        without making a convergence or scientific claim.
        """
        report = QuantumEspressoDiagnosticClassifier(
            QuantumEspressoDiagnosticCatalog.qe_pw_7_2_v1()
        ).execute(
            self.qe72_request(
                b"authored output\nJOB DONE.\n",
                b"",
                identity="report.qe72.clear",
            )
        )

        assert report.kind is QuantumEspressoDiagnosticReportKind.CLEAR
        assert report.observations == ()
        assert len(report.completion_markers) == 1

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
        report = QuantumEspressoDiagnosticClassifier(
            QuantumEspressoDiagnosticCatalog.fixture_pw_v1()
        ).execute(self.request(stdout, stderr, identity="report.clear"))

        assert report.kind is QuantumEspressoDiagnosticReportKind.CLEAR
        assert len(report.observations) == 1
        assert report.observations[0].channel is (
            QuantumEspressoDiagnosticChannel.STDERR
        )
        assert report.observations[0].disposition is (
            QuantumEspressoDiagnosticDisposition.NONBLOCKING
        )
        assert report.stderr_content_identity == self.content_identity(stderr)
        assert len(report.completion_markers) == 1
        assert report.completion_markers[0].channel is (
            QuantumEspressoDiagnosticChannel.STDOUT
        )

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
        report = QuantumEspressoDiagnosticClassifier(
            QuantumEspressoDiagnosticCatalog.fixture_pw_v1()
        ).execute(self.request(stdout, stderr, identity="report.fatal"))

        assert report.kind is QuantumEspressoDiagnosticReportKind.FATAL
        assert {value.channel for value in report.observations} == {
            QuantumEspressoDiagnosticChannel.STDOUT,
            QuantumEspressoDiagnosticChannel.STDERR,
        }
        assert {value.disposition for value in report.observations} == {
            QuantumEspressoDiagnosticDisposition.FATAL,
            QuantumEspressoDiagnosticDisposition.SECONDARY_FATAL,
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
        classifier = QuantumEspressoDiagnosticClassifier(
            QuantumEspressoDiagnosticCatalog.fixture_pw_v1()
        )
        report = classifier.execute(
            self.request(b"JOB DONE.\n", stderr, identity=report_identity)
        )

        assert report.kind is QuantumEspressoDiagnosticReportKind.UNRESOLVED
        assert report.observations[0].disposition is (
            QuantumEspressoDiagnosticDisposition.UNRESOLVED
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
        classifier = QuantumEspressoDiagnosticClassifier(
            QuantumEspressoDiagnosticCatalog.fixture_pw_v1()
        )
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

        assert fatal_with_completion.kind is (
            QuantumEspressoDiagnosticReportKind.CONTRADICTORY
        )
        assert secondary_alone.kind is (
            QuantumEspressoDiagnosticReportKind.CONTRADICTORY
        )

    def test_method__execute__rejects_stream_or_catalog_identity_mismatch(
        self,
    ) -> None:
        """Evidence ID: SV-QE-DIAGNOSTIC-006

        Requirement: Classification requires exact stream content identities and the
        exact classifier/program/version binding.

        Acceptance: A changed stream and a changed classifier identity each raise
        ``ValueError`` rather than returning a diagnostic report.
        """
        catalog = QuantumEspressoDiagnosticCatalog.fixture_pw_v1()
        classifier = QuantumEspressoDiagnosticClassifier(catalog)
        request = self.request(b"JOB DONE.\n", b"", identity="report.identity")
        with pytest.raises(ValueError):
            classifier.execute(
                QuantumEspressoDiagnosticClassificationRequest(
                    report_identity=request.report_identity,
                    configuration=request.configuration,
                    stdout=request.stdout + b"changed",
                    stderr=request.stderr,
                    stdout_content_identity=request.stdout_content_identity,
                    stderr_content_identity=request.stderr_content_identity,
                    claim_boundary=request.claim_boundary,
                )
            )
        wrong_configuration = QuantumEspressoExecutableConfiguration(
            identity=request.configuration.identity,
            program=request.configuration.program,
            executable_kind=request.configuration.executable_kind,
            executable_content_identity=(
                request.configuration.executable_content_identity
            ),
            program_version=request.configuration.program_version,
            argument_suffix=(),
            environment_additions=(),
            classifier_identity=QuantumEspressoDiagnosticClassifierIdentity(
                "other-classifier"
            ),
            contract_version=request.configuration.contract_version,
        )
        with pytest.raises(ValueError):
            classifier.execute(
                QuantumEspressoDiagnosticClassificationRequest(
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
        report = QuantumEspressoDiagnosticClassifier(
            QuantumEspressoDiagnosticCatalog.fixture_pw_v1()
        ).execute(self.request(stdout, stderr, identity="report.spans"))

        stderr_observation, stdout_observation = report.observations
        assert stdout_observation.channel is QuantumEspressoDiagnosticChannel.STDOUT
        assert stderr_observation.channel is QuantumEspressoDiagnosticChannel.STDERR
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
        assert quantum_espresso.QuantumEspressoDiagnosticClassifier is SUT
        assert "QuantumEspressoDiagnosticClassifier" in quantum_espresso.__all__
