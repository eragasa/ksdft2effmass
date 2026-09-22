r"""Software verification of versioned production conformance ratchet integration.

Evidence profile: claim_bearing

Bounded artifact scope: versioned production conformance ratchet integration.

Facet and represented meaning

This module verifies exact subject, policy, profile, configuration, source, and
baseline identities; inherited-versus-new deterministic classification; bounded CLI
reporting; and aggregate composition of all four Phase 2 slices.

Intrinsic and cross-object scope

Frozen records own intrinsic identities and closed state. Serializers own exact text
representations, the Workflow owns cross-slice composition, and the command owns
explicit path reads and exit mapping. Maintained bytes and accepted prerequisite
contracts are the oracles.

VVUQ and scientific exclusions

Passing establishes bounded structural software behavior only. It does not approve an
inherited finding, classify any supported route, establish runtime-semantic
completeness, repair source, provide a mutable or permanent waiver, establish
numerical verification or scientific validation, human-accept a Task, or activate a
successor.
"""

from __future__ import annotations

import hashlib
from dataclasses import FrozenInstanceError, replace
from pathlib import Path, PurePosixPath
from typing import Literal

import pytest

from ksdft2effmass.harness.cli.main import run as harness_run
from ksdft2effmass.harness.cli.validate_production_conformance import (
    PythonProductionConformanceCommand,
)
from ksdft2effmass.harness.pi.conformance.python.callable_private import (
    PythonArchitectureRuleClassification,
)
from ksdft2effmass.harness.pi.conformance.python.dependency_graph import (
    PythonDependencyGraphView,
)
from ksdft2effmass.harness.pi.conformance.python.production import (
    PythonProductionSource,
)
from ksdft2effmass.harness.pi.conformance.python.ratchet import (
    PythonJsonStringSerializer,
    PythonProductionConformanceConfiguration,
    PythonProductionConformanceConfigurationSerializer,
    PythonProductionConformanceSubject,
    PythonProductionContentIdentity,
    PythonProductionInheritedBaseline,
    PythonProductionInheritedBaselineSerializer,
    PythonProductionRatchetReportSerializer,
    PythonProductionRatchetRequest,
    PythonProductionRatchetResult,
    PythonProductionRatchetStatus,
    PythonProductionRatchetWorkflow,
)

pytestmark = pytest.mark.software_verification
RESOURCE_ROOT = Path(__file__).parent / "resources/production_conformance_ratchet"


class TestProductionConformanceRatchet:
    """Verify the integration artifact through exact unsupported implementation APIs."""

    @staticmethod
    def identity(path: Path) -> PythonProductionContentIdentity:
        """Return the independently computed SHA-256 and size of one resource."""
        payload = path.read_bytes()
        return PythonProductionContentIdentity(
            sha256=hashlib.sha256(payload).hexdigest(), byte_count=len(payload)
        )

    @classmethod
    def configuration(cls) -> PythonProductionConformanceConfiguration:
        """Decode the maintained configuration under its exact content identity."""
        path = RESOURCE_ROOT / "configuration-v1.txt"
        return PythonProductionConformanceConfigurationSerializer().execute(
            path.read_bytes(), cls.identity(path)
        )

    @classmethod
    def baseline(cls) -> PythonProductionInheritedBaseline:
        """Decode the maintained inherited baseline under exact content identity."""
        path = RESOURCE_ROOT / "baseline-v1.txt"
        return PythonProductionInheritedBaselineSerializer().execute(
            path.read_bytes(), cls.identity(path)
        )

    @staticmethod
    def source(resource_name: str) -> PythonProductionSource:
        """Create one explicit source input from the named maintained bytes."""
        return PythonProductionSource.from_payload(
            input_identity="fixture-input",
            path=PurePosixPath("controlled/fixture.py"),
            payload=(RESOURCE_ROOT / resource_name).read_bytes(),
        )

    @classmethod
    def execute(
        cls, resource_name: str = "inherited.py.txt"
    ) -> PythonProductionRatchetResult:
        """Execute the complete ratchet for one exact maintained source resource."""
        return PythonProductionRatchetWorkflow().execute(
            PythonProductionRatchetRequest(
                configuration=cls.configuration(),
                baseline=cls.baseline(),
                sources=(cls.source(resource_name),),
            )
        )

    @classmethod
    def cli_arguments(
        cls,
        source_name: str = "inherited.py.txt",
        *,
        limit: int = 20,
        source_sha256: str | None = None,
    ) -> tuple[str, ...]:
        """Build exact command arguments without hiding expected report values."""
        configuration = RESOURCE_ROOT / "configuration-v1.txt"
        baseline = RESOURCE_ROOT / "baseline-v1.txt"
        source = RESOURCE_ROOT / source_name
        configuration_identity = cls.identity(configuration)
        baseline_identity = cls.identity(baseline)
        source_identity = cls.identity(source)
        return (
            "--configuration",
            str(configuration),
            configuration_identity.sha256,
            str(configuration_identity.byte_count),
            "--baseline",
            str(baseline),
            baseline_identity.sha256,
            str(baseline_identity.byte_count),
            "--source",
            "fixture-input",
            "controlled/fixture.py",
            str(source),
            source_identity.sha256 if source_sha256 is None else source_sha256,
            str(source_identity.byte_count),
            "--limit",
            str(limit),
        )

    def test_artifact__ratchet_classification__keeps_inherited_visible_and_fails_new(
        self,
    ) -> None:
        """Evidence ID: software-verification.harness.production-ratchet.classification

        Requirement: An inherited deterministic finding remains visible without being
        treated as approval or waiver, while a newly introduced deterministic finding
        fails the versioned ratchet.

        Method: Run the same identified configuration and immutable baseline against
        authored source containing only the inherited class-name finding and against a
        second source that adds one module-level callable.

        Oracle: The exact accepted callable/private rule identities, authored source
        lines, and maintained baseline finding key.

        Acceptance: The first result passes with both inherited findings and no new
        finding; the second fails with both inherited findings still present and the
        exact hook-integrity plus module-callable findings introduced by changed bytes.

        Interpretation: Failure identifies baseline suppression, waiver semantics, or
        failure to ratchet a new deterministic violation.

        Limitations: Passing does not approve the inherited finding or establish
        repository-wide conformance.
        """
        inherited = self.execute()
        changed = self.execute("new.py.txt")
        assert inherited.status is PythonProductionRatchetStatus.PASS
        assert len(inherited.inherited_present) == 2
        assert not inherited.inherited_absent
        assert not inherited.new_findings
        assert changed.status is PythonProductionRatchetStatus.FAIL_NEW_VIOLATIONS
        assert len(changed.inherited_present) == 2
        assert tuple(item.key.rule_identity for item in changed.new_findings) == (
            "python.callable-private.hook-exception-integrity.v1",
            "python.callable-private.module-callable-owner.v1",
            "python.callable-private.module-callable-owner.v1",
        )
        assert not hasattr(changed, "waivers")
        assert not hasattr(changed, "approved_findings")

    def test_artifact__phase_two_aggregate__composes_all_slices_without_v1_mutation(
        self,
    ) -> None:
        """Evidence ID: software-verification.harness.production-ratchet.aggregate

        Requirement: One run composes production facts, callable/private rules, all
        three named dependency views, and ratchet classification under a distinct
        production subject/profile.

        Method: Execute the inherited fixture and inspect every retained prerequisite
        result plus the final identity-bearing comparison.

        Oracle: Accepted Phase 2a-2c result types and exact versioned Phase 2d subject
        and profile identities documented by the architecture contract.

        Acceptance: Source facts retain one successful module, callable rules retain
        the deterministic class-name finding and canonical classifications, graph
        output retains the exact three views, and the distinct production profile is
        version one without using ``python.test-evidence``.

        Interpretation: Failure identifies omitted prerequisite output, view
        conflation, or mutation of the accepted test-evidence subject.

        Limitations: Dedicated prerequisite suites remain the detailed evidence for
        each accepted slice.
        """
        result = self.execute()
        assert len(result.production_facts.modules) == 1
        assert result.production_facts.modules[0].facts is not None
        assert any(
            finding.rule.rule_identity
            == "python.callable-private.top-level-class-name.v1"
            for finding in result.callable_rules
        )
        assert all(
            finding.rule.classification in tuple(PythonArchitectureRuleClassification)
            for finding in result.callable_rules
        )
        assert tuple(view.view for view in result.dependency_graph.views) == tuple(
            PythonDependencyGraphView
        )
        assert (
            result.subject.subject_family,
            result.subject.subject_version,
        ) == ("python.production-source", "1")
        assert result.profile.profile_identity == (
            "ksdft2effmass.python.production-ratchet"
        )
        assert "test-evidence" not in result.profile.profile_identity

    def test_artifact__owner_boundaries__contain_no_reported_private_cross_calls(
        self,
    ) -> None:
        """Evidence ID: software-verification.harness.production-ratchet.ownership

        Requirement: DataObjects own intrinsic field checks and serializers share wire
        decoding only through an explicit non-private serializer contract.

        Method: Inspect the exact ratchet source for the two reported cross-owner
        private-call forms.

        Oracle: The object model prohibits calls to another owner's private methods;
        the configuration serializer's ``decode_text`` method is the shared wire
        decoding contract.

        Acceptance: Neither reported private call exists and the explicit decoding
        contract is present.

        Interpretation: Failure identifies recurrence of cross-owner private coupling.

        Limitations: This focused regression assertion covers the reported call forms,
        not a repository-wide semantic ownership analysis.
        """
        source_path = (
            Path(__file__).parents[4]
            / "src/ksdft2effmass/harness/pi/conformance/python/ratchet.py"
        )
        source = source_path.read_text(encoding="utf-8")
        assert (
            "PythonProductionConformanceSubject._require_text(" not in source
            and "PythonProductionConformanceConfigurationSerializer._decode("
            not in source
            and "def decode_text(value: str) -> str:" in source
        )

    @pytest.mark.parametrize(
        "case",
        (
            pytest.param("configuration_content", id="configuration_digest_mismatch"),
            pytest.param("configuration_profile", id="configuration_profile_mismatch"),
            pytest.param("baseline_content", id="baseline_digest_mismatch"),
            pytest.param(
                "baseline_configuration", id="baseline_configuration_mismatch"
            ),
            pytest.param("source_content", id="source_digest_mismatch"),
        ),
    )
    def test_artifact__identified_inputs__fail_closed_on_every_identity_mismatch(
        self,
        case: Literal[
            "configuration_content",
            "configuration_profile",
            "baseline_content",
            "baseline_configuration",
            "source_content",
        ],
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        """Evidence ID: software-verification.harness.production-ratchet.identities

        Requirement: Configuration, subject/profile binding, baseline content,
        baseline-to-configuration binding, and source content identities each fail
        closed rather than falling back to ambient or latest inputs.

        Method: Alter exactly one identity dimension per semantic parameter case at
        the serializer, Workflow, or command boundary.

        Oracle: SHA-256/byte-count equality and exact versioned identity tuples.

        Acceptance: Every mismatch raises ``ValueError`` or returns CLI status 2 with
        ``invalid_input``; no ratchet result is emitted.

        Interpretation: Failure identifies implicit discovery, identity substitution,
        or profile fallback.

        Limitations: SHA-256 collision resistance is assumed rather than tested.
        """
        configuration_path = RESOURCE_ROOT / "configuration-v1.txt"
        baseline_path = RESOURCE_ROOT / "baseline-v1.txt"
        if case == "configuration_content":
            identity = self.identity(configuration_path)
            with pytest.raises(ValueError, match="configuration content identity"):
                PythonProductionConformanceConfigurationSerializer().execute(
                    configuration_path.read_bytes(),
                    replace(identity, sha256="0" * 64),
                )
        elif case == "configuration_profile":
            payload = configuration_path.read_bytes().replace(
                b"a3NkZnQyZWZmbWFzcy5weXRob24ucHJvZHVjdGlvbi1yYXRjaGV0",
                b"aW1wb3N0b3IucHJvZmlsZQ",
            )
            with pytest.raises(ValueError, match="profile binding"):
                PythonProductionConformanceConfigurationSerializer().execute(
                    payload, PythonProductionContentIdentity.from_bytes(payload)
                )
        elif case == "baseline_content":
            identity = self.identity(baseline_path)
            with pytest.raises(ValueError, match="baseline content identity"):
                PythonProductionInheritedBaselineSerializer().execute(
                    baseline_path.read_bytes(), replace(identity, sha256="0" * 64)
                )
        elif case == "baseline_configuration":
            baseline = replace(
                self.baseline(),
                configuration_identity=PythonProductionContentIdentity(
                    sha256="0" * 64, byte_count=0
                ),
            )
            with pytest.raises(ValueError, match="baseline fields disagree"):
                PythonProductionRatchetWorkflow().execute(
                    PythonProductionRatchetRequest(
                        configuration=self.configuration(),
                        baseline=baseline,
                        sources=(self.source("inherited.py.txt"),),
                    )
                )
        else:
            status = PythonProductionConformanceCommand().execute(
                self.cli_arguments(source_sha256="0" * 64)
            )
            report = capsys.readouterr().out
            assert status == 2
            assert '"status":"invalid_input"' in report
            assert "SHA-256 mismatch" in report

    @pytest.mark.parametrize(
        "case",
        (
            pytest.param("configuration_subject", id="same_digest_changed_subject"),
            pytest.param("configuration_hook", id="same_digest_changed_hook"),
            pytest.param("configuration_direction", id="same_digest_changed_direction"),
            pytest.param(
                "baseline_identity", id="same_digest_changed_baseline_identity"
            ),
            pytest.param(
                "baseline_findings", id="same_digest_changed_baseline_findings"
            ),
        ),
    )
    def test_artifact__content_identity__rejects_same_digest_changed_fields(
        self,
        case: Literal[
            "configuration_subject",
            "configuration_hook",
            "configuration_direction",
            "baseline_identity",
            "baseline_findings",
        ],
    ) -> None:
        """Evidence ID: software-verification.harness.production-ratchet.field-closure

        Requirement: Direct typed configuration and baseline values cannot change a
        consumed field while retaining the content identity of different bytes.

        Method: Replace the subject identity, baseline logical identity, or baseline
        findings while preserving the maintained SHA-256 and byte count.

        Oracle: Canonical complete version-one encodings and SHA-256/byte-count
        equality for every field consumed by the Workflow.

        Acceptance: Every same-digest changed-field impostor fails before inspection
        or classification with a content-identity disagreement.

        Interpretation: Failure would permit false identity attribution or
        waiver-equivalent baseline suppression.

        Limitations: SHA-256 collision resistance remains assumed.
        """
        configuration = self.configuration()
        baseline = self.baseline()
        if case == "configuration_subject":
            configuration = replace(
                configuration,
                subject=replace(
                    configuration.subject, subject_identity="changed-subject"
                ),
            )
            match = "configuration fields disagree"
        elif case == "configuration_hook":
            configuration = replace(
                configuration,
                hook_exceptions=(
                    replace(
                        configuration.hook_exceptions[0],
                        hook_owner="changed-framework",
                    ),
                ),
            )
            match = "configuration fields disagree"
        elif case == "configuration_direction":
            configuration = replace(
                configuration,
                direction_checks=(
                    replace(
                        configuration.direction_checks[0],
                        source_module="controlled.other",
                    ),
                ),
            )
            match = "configuration fields disagree"
        elif case == "baseline_identity":
            baseline = replace(baseline, baseline_identity="changed-baseline")
            match = "baseline fields disagree"
        else:
            additional = self.execute("new.py.txt").new_findings[0].key
            baseline = replace(
                baseline,
                findings=tuple(sorted((*baseline.findings, additional))),
            )
            match = "baseline fields disagree"
        with pytest.raises(ValueError, match=match):
            PythonProductionRatchetWorkflow().execute(
                PythonProductionRatchetRequest(
                    configuration=configuration,
                    baseline=baseline,
                    sources=(self.source("inherited.py.txt"),),
                )
            )

    @pytest.mark.parametrize(
        "case",
        (
            pytest.param("omit_new", id="new_partition_omitted_false_pass"),
            pytest.param("misclassify_new", id="new_finding_marked_inherited"),
            pytest.param("omit_baseline", id="baseline_partition_omitted"),
            pytest.param("duplicate_absent", id="inherited_absent_duplicate"),
        ),
    )
    def test_artifact__result_partition__rejects_false_or_ambiguous_results(
        self,
        case: Literal[
            "omit_new", "misclassify_new", "omit_baseline", "duplicate_absent"
        ],
    ) -> None:
        """Evidence ID: software-verification.harness.production-ratchet.partition

        Requirement: Current findings partition exactly into inherited-present and
        new, while baseline keys partition exactly into inherited-present and absent;
        every group is canonical and unique.

        Method: Directly construct omission, misclassification, baseline-erasure, and
        duplicate-absent variants from genuine Workflow results.

        Oracle: Exact finding-key set intersection and difference.

        Acceptance: Every false or ambiguous ResultObject raises ``ValueError``;
        specifically, erasing new findings cannot construct a ``pass`` result.

        Interpretation: Failure would allow report or exit-status falsification.

        Limitations: Finding semantics remain owned by the versioned policy.
        """
        failed = self.execute("new.py.txt")
        if case == "omit_new":
            with pytest.raises(ValueError, match="exact current/baseline difference"):
                replace(
                    failed,
                    new_findings=(),
                    status=PythonProductionRatchetStatus.PASS,
                )
        elif case == "misclassify_new":
            inherited = tuple(
                sorted((*failed.inherited_present, failed.new_findings[0]))
            )
            with pytest.raises(ValueError, match="exact current/baseline intersection"):
                replace(failed, inherited_present=inherited)
        elif case == "omit_baseline":
            with pytest.raises(ValueError, match="exact current/baseline intersection"):
                replace(failed, baseline_findings=())
        else:
            absent_result = PythonProductionRatchetWorkflow().execute(
                PythonProductionRatchetRequest(
                    configuration=self.configuration(),
                    baseline=self.baseline(),
                    sources=(
                        PythonProductionSource.from_payload(
                            input_identity="fixture-input",
                            path=PurePosixPath("controlled/fixture.py"),
                            payload=b"class Good:\n    pass\n",
                        ),
                    ),
                )
            )
            absent = absent_result.inherited_absent[0]
            with pytest.raises(ValueError, match="unique finding keys"):
                replace(absent_result, inherited_absent=(absent, absent))

    @pytest.mark.parametrize(
        ("case", "source"),
        (
            pytest.param(
                "decode",
                PythonProductionSource.from_payload(
                    input_identity="fixture-input",
                    path=PurePosixPath("controlled/fixture.py"),
                    payload=b"\xff",
                ),
                id="configured_invalid_utf8",
            ),
            pytest.param(
                "syntax",
                PythonProductionSource.from_payload(
                    input_identity="fixture-input",
                    path=PurePosixPath("controlled/fixture.py"),
                    payload=b"def broken(",
                ),
                id="configured_invalid_python",
            ),
            pytest.param(
                "read",
                PythonProductionSource(
                    input_identity="fixture-input",
                    path=PurePosixPath("controlled/fixture.py"),
                    payload=None,
                    read_error="represented read failure",
                ),
                id="configured_represented_read_failure",
            ),
        ),
    )
    def test_artifact__source_failures__become_new_deterministic_violations(
        self,
        case: Literal["decode", "syntax", "read"],
        source: PythonProductionSource,
        tmp_path: Path,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        """Evidence ID: software-verification.harness.production-ratchet.failures

        Requirement: Configured decode, syntax, and represented read failures reach
        the production source-failure policy instead of becoming invalid graph input.

        Method: Execute each accepted failure partition through the complete Workflow;
        additionally invoke the CLI over syntax-invalid bytes.

        Oracle: Accepted production-fact failure kinds and the policy's exact
        ``python.production-source.input-failure.v1`` identity.

        Acceptance: Every partition returns ``fail_new_violations`` with the exact
        source-failure rule; the configured syntax CLI exits one, not two.

        Interpretation: Failure identifies loss of represented failure outcomes at
        graph integration.

        Limitations: CLI cannot originate a represented read failure because OS read
        failure remains an invalid external input.
        """
        result = PythonProductionRatchetWorkflow().execute(
            PythonProductionRatchetRequest(
                configuration=self.configuration(),
                baseline=self.baseline(),
                sources=(source,),
            )
        )
        assert result.status is PythonProductionRatchetStatus.FAIL_NEW_VIOLATIONS
        assert any(
            finding.key.rule_identity == "python.production-source.input-failure.v1"
            for finding in result.new_findings
        )
        if case == "syntax":
            source_path = tmp_path / "invalid.py"
            source_payload = source.payload
            assert source_payload is not None
            source_path.write_bytes(source_payload)
            arguments = list(self.cli_arguments())
            identity = PythonProductionContentIdentity.from_bytes(source_payload)
            arguments[11] = str(source_path)
            arguments[12] = identity.sha256
            arguments[13] = str(identity.byte_count)
            assert PythonProductionConformanceCommand().execute(tuple(arguments)) == 1
            assert '"status":"fail_new_violations"' in capsys.readouterr().out

    @pytest.mark.parametrize(
        "case",
        (
            pytest.param("duplicate_sources", id="ambiguous_duplicate_source_identity"),
            pytest.param("duplicate_baseline", id="ambiguous_duplicate_baseline_key"),
            pytest.param("request_impostor", id="nominal_request_impostor"),
        ),
    )
    def test_artifact__closed_inputs__rejects_ambiguous_duplicates_and_impostors(
        self,
        case: Literal["duplicate_sources", "duplicate_baseline", "request_impostor"],
    ) -> None:
        """Evidence ID: software-verification.harness.production-ratchet.rejection

        Requirement: Ambiguous duplicate source/finding identities and nominal request
        impostors fail before deterministic classification.

        Method: Duplicate one input identity across different paths, duplicate an
        inherited key through direct record construction, or subclass the exact
        Workflow request.

        Oracle: Exact source identity, baseline finding-key uniqueness, and closed
        operation-boundary type semantics.

        Acceptance: Each semantic partition raises ``ValueError`` for ambiguity or
        ``TypeError`` for the nominal impostor.

        Interpretation: Failure identifies order-dependent duplicate collapse or an
        open erased request boundary.

        Limitations: Distinct findings at distinct exact locations remain valid.
        """
        if case == "duplicate_sources":
            source = self.source("inherited.py.txt")
            duplicate_identity = replace(
                source, path=PurePosixPath("controlled/different.py")
            )
            with pytest.raises(ValueError, match="identities must be unique"):
                PythonProductionRatchetWorkflow().execute(
                    PythonProductionRatchetRequest(
                        configuration=self.configuration(),
                        baseline=self.baseline(),
                        sources=(source, duplicate_identity),
                    )
                )
        elif case == "duplicate_baseline":
            baseline = self.baseline()
            with pytest.raises(ValueError, match="unique"):
                replace(baseline, findings=(baseline.findings[0], baseline.findings[0]))
        else:

            class ImpostorRequest(PythonProductionRatchetRequest):
                """Nominal impostor for the exact Workflow operation boundary."""

            request = ImpostorRequest(
                configuration=self.configuration(),
                baseline=self.baseline(),
                sources=(self.source("inherited.py.txt"),),
            )
            with pytest.raises(
                TypeError, match="must be PythonProductionRatchetRequest"
            ):
                PythonProductionRatchetWorkflow().execute(request)

    def test_artifact__report__is_deterministic_bounded_and_identity_complete(
        self,
    ) -> None:
        """Evidence ID: software-verification.harness.production-ratchet.report

        Requirement: Report projection is deterministic, bounded, and retains exact
        subject, policy, profile, configuration, source, and baseline identities plus
        total/truncation metadata.

        Method: Serialize one failed result twice with a zero-item limit and parse the
        canonical JSON projection.

        Oracle: Exact result identities, configured limit, and JSON value equality.

        Acceptance: Both bytes-equivalent strings match; no finding item is emitted;
        each total remains exact with truncation true where applicable; and every
        required identity agrees with the source ResultObject.

        Interpretation: Failure identifies nondeterminism, unbounded output, or lost
        identity provenance.

        Limitations: The report is a derived view and not source authority or a durable
        approval record.
        """
        result = self.execute("new.py.txt")
        serializer = PythonProductionRatchetReportSerializer()
        first = serializer.execute(result, 0)
        second = serializer.execute(result, 0)
        assert first == second
        assert '"new":{"items":[],"total":3,"truncated":true}' in first
        assert '"inherited_present":{"items":[],"total":2,"truncated":true}' in first
        assert f'"family":"{result.subject.subject_family}"' in first
        assert f'"identity":"{result.policy.policy_identity}"' in first
        assert f'"identity":"{result.profile.profile_identity}"' in first
        assert result.configuration_identity.sha256 in first
        assert result.source_identity.sha256 in first
        assert result.baseline_identity.sha256 in first
        assert "not approvals or waivers" in first

    def test_artifact__cli__is_bounded_nonmutating_and_dispatcher_integrated(
        self,
        tmp_path: Path,
        monkeypatch: pytest.MonkeyPatch,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        """Evidence ID: software-verification.harness.production-ratchet.cli

        Requirement: The dispatcher reaches one explicit nonmutating command whose
        result and exit status agree and whose output honors the requested bound.

        Method: Snapshot every authored input, change to an unrelated empty directory,
        invoke the Harness dispatcher using only absolute explicit paths with limit
        zero, and compare all bytes afterward.

        Oracle: Exact file bytes, dispatcher command inventory, ratchet status, and
        requested report bound.

        Acceptance: Exit status is zero for the inherited-only fixture, the report is
        ``pass`` with a visible inherited total and zero emitted items, and every input
        byte sequence is unchanged despite an unrelated current directory.

        Interpretation: Failure identifies ambient discovery, mutation/repair, lost
        CLI integration, unbounded reporting, or exit/report disagreement.

        Limitations: OS-level read access and stdout transport are assumed.
        """
        paths = tuple(sorted(RESOURCE_ROOT.iterdir()))
        before = tuple((path, path.read_bytes()) for path in paths)
        absolute_arguments = tuple(
            str(Path(argument).resolve())
            if argument.startswith(str(RESOURCE_ROOT))
            else argument
            for argument in self.cli_arguments(limit=0)
        )
        monkeypatch.chdir(tmp_path)
        status = harness_run(("validate-production-conformance", *absolute_arguments))
        report = capsys.readouterr().out
        assert status == 0
        assert '"status":"pass"' in report
        assert '"inherited_present":{"items":[],"total":2,"truncated":true}' in report
        assert tuple((path, path.read_bytes()) for path in paths) == before

    def test_artifact__cli__rejects_duplicate_limit_as_invalid_input(
        self, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """Evidence ID: software-verification.harness.production-ratchet.cli-limit

        Requirement: The optional bounded report limit may be supplied at most once.

        Method: Append a second valid in-range ``--limit`` to an otherwise complete
        explicit command request.

        Oracle: The closed command grammar and invalid-input exit mapping.

        Acceptance: The command exits two and emits the exact deterministic JSON error
        rather than applying last-one-wins behavior or reading inputs.

        Interpretation: Failure identifies ambiguous duplicate option handling.

        Limitations: Existing focused evidence retains the independent zero-item report
        behavior; the request record continues to enforce the zero-through-one-hundred
        bound.
        """
        status = PythonProductionConformanceCommand().execute(
            (*self.cli_arguments(limit=0), "--limit", "100")
        )
        assert status == 2
        assert capsys.readouterr().out == (
            '{"error":"--limit may be supplied at most once",'
            '"status":"invalid_input"}\n'
        )

    def test_artifact__values__are_immutable_and_leave_source_unrepaired(self) -> None:
        """Evidence ID: software-verification.harness.production-ratchet.nonmutation

        Requirement: Configuration, baseline, and result records are immutable and
        execution neither repairs nor rewrites violating source bytes.

        Method: Snapshot the new-violation fixture, execute a failing ratchet, attempt
        field assignment on each principal value, and compare fixture bytes afterward.

        Oracle: Frozen dataclass semantics and exact authored resource bytes.

        Acceptance: Every assignment raises ``FrozenInstanceError`` and source bytes
        remain identical after failed classification.

        Interpretation: Failure identifies mutable waiver-like state or source repair.

        Limitations: This checks ordinary public mutation and file bytes, not hostile
        process-level memory manipulation.
        """
        path = RESOURCE_ROOT / "new.py.txt"
        before = path.read_bytes()
        configuration = self.configuration()
        baseline = self.baseline()
        result = self.execute("new.py.txt")
        with pytest.raises(FrozenInstanceError):
            configuration.subject = PythonProductionConformanceSubject(  # type: ignore[misc]
                subject_family="python.production-source",
                subject_version="1",
                subject_identity="changed",
            )
        with pytest.raises(FrozenInstanceError):
            baseline.findings = ()  # type: ignore[misc]
        with pytest.raises(FrozenInstanceError):
            result.status = PythonProductionRatchetStatus.PASS  # type: ignore[misc]
        assert path.read_bytes() == before

    def test_artifact__configuration_wire__covers_hooks_and_direction_contracts(
        self,
    ) -> None:
        """Evidence ID: software-verification.harness.production-ratchet.configuration

        Requirement: Version-one configuration bytes completely bind module, hook,
        direction-check, and accepted-contract state consumed by the Workflow.

        Method: Decode and re-encode the maintained nonempty configuration, then run
        its exact hook and direction check end to end.

        Oracle: Exact maintained bytes, hook callable span/source digest, and explicit
        lexical edge contract fields.

        Acceptance: Re-encoding is byte-exact; one hook and one contracted direction
        check survive decoding; the hook exempts its exact callable; and the absent
        contracted edge remains an identified inherited deterministic result.

        Interpretation: Failure identifies omitted prerequisite configuration state or
        a content identity that does not cover consumed fields.

        Limitations: The fixture exercises an absent allowed edge, not every accepted
        dependency status already covered by the prerequisite suite.
        """
        path = RESOURCE_ROOT / "configuration-v1.txt"
        configuration = self.configuration()
        result = self.execute()
        assert (
            PythonProductionConformanceConfigurationSerializer().encode(configuration)
            == path.read_bytes()
        )
        assert len(configuration.hook_exceptions) == 1
        assert len(configuration.direction_checks) == 1
        assert configuration.direction_checks[0].accepted_contract is not None
        assert not any(
            finding.owner_identity == "framework_hook"
            for finding in result.callable_rules
        )
        assert (
            result.dependency_graph.direction_results[0].status.value == "edge_absent"
        )

    def test_artifact__json_strings__escape_all_control_characters(
        self, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """Evidence ID: software-verification.harness.production-ratchet.json

        Requirement: Success and invalid-input JSON string rendering completely escapes
        every C0 control accepted from represented values or command arguments.

        Method: Encode one string containing all C0 controls and inject the same text
        into an unknown command argument.

        Oracle: RFC 8259 prohibits raw U+0000 through U+001F inside JSON strings.

        Acceptance: Rendering is deterministic and neither success-string nor bounded
        command-error JSON contains any raw C0 control except the command's final
        output newline.

        Interpretation: Failure identifies malformed JSON for a legal represented
        value or external error text.

        Limitations: Unicode scalar escaping outside C0 follows the standard-library
        encoder contract.
        """
        controls = "".join(chr(value) for value in range(32))
        serializer = PythonJsonStringSerializer()
        first = serializer.execute(controls)
        assert first == serializer.execute(controls)
        assert not any(character in first for character in controls)
        assert (
            PythonProductionConformanceCommand().execute((f"--unknown{controls}",)) == 2
        )
        output = capsys.readouterr().out
        assert output.endswith("\n")
        assert not any(character in output[:-1] for character in controls)

    def test_artifact__empty_baseline__round_trips_canonically(self) -> None:
        """Evidence ID: software-verification.harness.production-ratchet.empty-baseline

        Requirement: A canonical inherited baseline may contain zero findings.

        Method: Remove findings from the maintained baseline, derive its new canonical
        content identity, then decode and re-encode it.

        Oracle: The baseline contract declares a sorted unique tuple without a
        nonempty invariant.

        Acceptance: The empty baseline round-trips byte-for-byte with an exact content
        identity and remains empty.

        Interpretation: Failure prevents establishment of a clean initial ratchet.

        Limitations: Historical source bytes remain external provenance.
        """
        serializer = PythonProductionInheritedBaselineSerializer()
        placeholder = PythonProductionContentIdentity(sha256="0" * 64, byte_count=0)
        baseline = replace(self.baseline(), content_identity=placeholder, findings=())
        payload = serializer.encode(baseline, include_content_identity=False)
        identity = PythonProductionContentIdentity.from_bytes(payload)
        baseline = replace(baseline, content_identity=identity)
        assert serializer.execute(payload, identity) == baseline
        assert serializer.encode(baseline) == payload

    def test_artifact__baseline_serialization__round_trips_canonically(self) -> None:
        """Evidence ID: software-verification.harness.production-ratchet.baseline

        Requirement: The inherited baseline is immutable, content identified, exact,
        canonical, and does not encode mutable waiver or approval semantics.

        Method: Decode and re-encode the maintained baseline with its independently
        computed content identity.

        Oracle: Exact maintained bytes, SHA-256, canonical Base64 fields, and the
        closed baseline DataObject field inventory.

        Acceptance: Re-encoding is byte-for-byte exact; the historical source identity
        remains present; and no waiver, approval, expiration, or mutation field exists.

        Interpretation: Failure identifies unstable baseline identity or unauthorized
        approval/waiver semantics.

        Limitations: The baseline records structural findings, not repository-wide
        conformance or human acceptance.
        """
        path = RESOURCE_ROOT / "baseline-v1.txt"
        baseline = self.baseline()
        assert PythonProductionInheritedBaselineSerializer().encode(baseline) == (
            path.read_bytes()
        )
        assert baseline.content_identity == self.identity(path)
        assert baseline.source_identity.byte_count > 0
        assert not hasattr(baseline, "waivers")
        assert not hasattr(baseline, "approved")
        assert not hasattr(baseline, "expires_at")
