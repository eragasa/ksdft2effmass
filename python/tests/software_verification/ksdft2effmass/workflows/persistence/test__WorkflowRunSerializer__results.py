r"""Software verification of ``WorkflowRunSerializer``.

Bounded artifact scope: seven complete concrete families in nonempty aggregate wires.

Evidence profile: claim_bearing

Facet and represented meaning

Independent literal aggregate bytes and direct concrete constructors fix the expected
values. Result envelopes occur in result references and invocation outcomes.

Intrinsic and cross-object scope

The serializer owns lossless traversal and cross-occurrence agreement, not structural
history validation, native execution, receipt derivation or scientific policy.

VVUQ and scientific exclusions

Synthetic software verification only; no scientific or historical authority claim.
"""

import json
from dataclasses import replace
from pathlib import Path
from typing import Literal, cast

import pytest

from ksdft2effmass import analysis as q
from ksdft2effmass import workflows as w
from ksdft2effmass.application import ApplicationResultValueSerializer
from ksdft2effmass.electronic_structure import KPointSampling, KPointWeightNormalization
from ksdft2effmass.integration import quantum_espresso as qe
from ksdft2effmass.ksdft import (
    Availability,
    EnergyUnit,
    KohnShamSpectralObservations,
    TotalEnergyObservation,
)
from ksdft2effmass.ksdft.pw import (
    ArtifactProvenance,
    KohnShamPlaneWaveCalculationRecord,
    KohnShamPlaneWaveCalculationRecordJsonSerializer,
    PlaneWaveMetadataAvailability,
    PlaneWaveRepresentationMetadata,
)
from ksdft2effmass.structures.periodic import (
    AtomicSpecies,
    CoordinateConvention,
    DirectLattice,
    InverseLengthUnit,
    LengthUnit,
    PeriodicSite,
    PeriodicStructure,
    PhysicalDimension,
    ReciprocalLattice,
    ReciprocalScaleConvention,
    UnitSystem,
)
from ksdft2effmass.workflows import (
    AttemptIdentity,
    OperationIdentity,
    ResultObjectIdentity,
    TaskActivationIdentity,
    TaskDefinitionIdentity,
    TaskInstanceIdentity,
    WorkflowRunSerializer,
)
from ksdft2effmass.workflows import artifacts as a

type _QeFamily = Literal["pw", "bands", "observation"]
type _QeValue = (
    qe.QuantumEspressoPwResult
    | qe.QuantumEspressoBandsResult
    | qe.QuantumEspressoExtractedObservationResult
)
type JsonValue = None | bool | str | list[JsonValue] | dict[str, JsonValue]
type Family = Literal[
    "pw", "bands", "observation", "scalar", "failure", "decision", "set"
]

pytestmark = pytest.mark.software_verification
SUT = WorkflowRunSerializer


class TestWorkflowRunSerializer:
    """Seven-family aggregate traversal using independent concrete expected values."""

    @staticmethod
    def make_evidence(
        program: qe.QuantumEspressoProgram = qe.QuantumEspressoProgram.PW,
    ) -> qe.QuantumEspressoOperationResultEvidence:
        stdout = a.ArtifactContentIdentity("sha256", "a" * 64, 8)
        stderr = a.ArtifactContentIdentity("sha256", "b" * 64, 3)
        span = a.ArtifactContentIdentity("sha256", "c" * 64, 4)
        execution = qe.QuantumEspressoExecutionInput(
            identity=qe.QuantumEspressoExecutionInputIdentity("input"),
            program=program,
            native_input=qe.QuantumEspressoNativeInputArtifact(
                a.ArtifactIdentity("native"),
                qe.QuantumEspressoFileArtifactContent(stdout),
                qe.QuantumEspressoArtifactDestination("input.in"),
            ),
            pseudopotentials=(
                qe.QuantumEspressoPseudopotentialArtifact(
                    a.ArtifactIdentity("pseudo"),
                    qe.QuantumEspressoFileArtifactContent(stderr),
                    qe.QuantumEspressoArtifactDestination("pseudo/Si.upf"),
                ),
            ),
            predecessor_native_state=(
                qe.QuantumEspressoPredecessorNativeStateArtifact(
                    a.ArtifactIdentity("state"),
                    qe.QuantumEspressoTreeArtifactContent(
                        a.ArtifactManifestIdentity("previous-manifest"),
                        (
                            a.ArtifactManifestEntryIdentity("previous-a"),
                            a.ArtifactManifestEntryIdentity("previous-b"),
                        ),
                    ),
                    qe.QuantumEspressoArtifactDestination("out/si.save"),
                    ResultObjectIdentity("previous-result"),
                    a.ArtifactManifestEntryIdentity("previous-a"),
                ),
            ),
            task_definition_identity=TaskDefinitionIdentity("definition"),
            task_instance_identity=TaskInstanceIdentity("task"),
            activation_identity=TaskActivationIdentity("activation"),
            operation_identity=OperationIdentity("operation"),
            attempt_identity=AttemptIdentity("attempt"),
            contract_version="qe-execution-input:1",
        )
        process = qe.QuantumEspressoProcessObservation(
            identity=qe.QuantumEspressoProcessObservationIdentity("process"),
            execution_input_identity=execution.identity,
            executable_configuration_identity=qe.QuantumEspressoExecutableConfigurationIdentity(
                "configuration"
            ),
            preparation_identity=qe.QuantumEspressoPreparationIdentity("preparation"),
            attempt_identity=execution.attempt_identity,
            argv_content_identity=span,
            termination=qe.QuantumEspressoNormalProcessExit(0),
            wall_duration_nanoseconds=18_446_744_073_709_551_615,
            stdout=qe.QuantumEspressoStreamObservation(
                channel=qe.QuantumEspressoDiagnosticChannel.STDOUT,
                artifact_identity=a.ArtifactIdentity("stdout-artifact"),
                content_identity=stdout,
            ),
            stderr=qe.QuantumEspressoStreamObservation(
                channel=qe.QuantumEspressoDiagnosticChannel.STDERR,
                artifact_identity=a.ArtifactIdentity("stderr-artifact"),
                content_identity=stderr,
            ),
            before_snapshot_identity=a.ArtifactManifestIdentity("before"),
            after_snapshot_identity=a.ArtifactManifestIdentity("after"),
            created_entry_count=2,
            created_total_bytes=11,
            peak_resident_bytes=4096,
            observer_version="synthetic-observer:99",
        )
        notice = qe.QuantumEspressoDiagnosticObservation(
            identity=qe.QuantumEspressoDiagnosticObservationIdentity("notice"),
            channel=qe.QuantumEspressoDiagnosticChannel.STDOUT,
            byte_start=0,
            byte_end=4,
            stream_content_identity=stdout,
            span_content_identity=span,
            signature_identity="notice-signature:2",
            disposition=qe.QuantumEspressoDiagnosticDisposition.NONBLOCKING,
            sanitized_summary="synthetic notice α",
            claim_boundary=("synthetic-only", "not-convergence"),
        )
        marker = qe.QuantumEspressoOutputMarkerObservation(
            identity=qe.QuantumEspressoOutputMarkerObservationIdentity("marker"),
            channel=qe.QuantumEspressoDiagnosticChannel.STDOUT,
            byte_start=4,
            byte_end=8,
            stream_content_identity=stdout,
            span_content_identity=a.ArtifactContentIdentity("sha256", "d" * 64, 4),
            signature_identity="completion:5",
        )
        report = qe.QuantumEspressoDiagnosticReport(
            identity=qe.QuantumEspressoDiagnosticReportIdentity("report"),
            classifier_identity=qe.QuantumEspressoDiagnosticClassifierIdentity(
                "classifier:17"
            ),
            executable_configuration_identity=process.executable_configuration_identity,
            executable_kind=qe.QuantumEspressoExecutableKind.DETERMINISTIC_FIXTURE,
            program=program,
            program_version="fixture-synthetic:23",
            stdout_content_identity=stdout,
            stderr_content_identity=stderr,
            observations=(notice,),
            completion_markers=(marker,),
            kind=qe.QuantumEspressoDiagnosticReportKind.CLEAR,
            claim_boundary=("synthetic-only", "not-acceptance"),
        )
        return qe.QuantumEspressoOperationResultEvidence(
            execution_input=execution,
            process_observation=process,
            diagnostic_report=report,
            calculator_outcome=qe.QuantumEspressoCompletedOutcome((marker.identity,)),
            native_output_manifest_identity=a.ArtifactManifestIdentity("outputs"),
            native_output_entry_identities=(
                a.ArtifactManifestEntryIdentity("output-a"),
                a.ArtifactManifestEntryIdentity("output-b"),
            ),
            terminal_record_identity=qe.QuantumEspressoTerminalRecordIdentity(
                "terminal"
            ),
        )

    @staticmethod
    def make_neutral() -> KohnShamPlaneWaveCalculationRecord:
        direct = DirectLattice(
            ((2.0, 0.0, 0.0), (0.0, 2.0, 0.0), (0.0, 0.0, 2.0)),
            UnitSystem.HARTREE_ATOMIC,
            PhysicalDimension.LENGTH,
            LengthUnit.BOHR,
            CoordinateConvention.CARTESIAN,
            "synthetic order",
        )
        reciprocal = ReciprocalLattice(
            ((1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, 1.0)),
            PhysicalDimension.DIMENSIONLESS,
            CoordinateConvention.CARTESIAN,
            ReciprocalScaleConvention.TWO_PI_OVER_ALAT,
            2.0,
            LengthUnit.BOHR,
            True,
            (
                (3.141592653589793, 0.0, 0.0),
                (0.0, 3.141592653589793, 0.0),
                (0.0, 0.0, 3.141592653589793),
            ),
            PhysicalDimension.INVERSE_LENGTH,
            InverseLengthUnit.PER_BOHR,
            CoordinateConvention.CARTESIAN,
        )
        points = KPointSampling(
            ((0.0, 0.0, 0.0),),
            PhysicalDimension.DIMENSIONLESS,
            CoordinateConvention.CARTESIAN,
            ReciprocalScaleConvention.TWO_PI_OVER_ALAT,
            2.0,
            LengthUnit.BOHR,
            True,
            ((0.0, 0.0, 0.0),),
            PhysicalDimension.INVERSE_LENGTH,
            InverseLengthUnit.PER_BOHR,
            (2.0,),
            KPointWeightNormalization.SUM_TO_TWO,
        )
        return KohnShamPlaneWaveCalculationRecord(
            1,
            PeriodicStructure(
                direct,
                (
                    AtomicSpecies(
                        "Si",
                        28.085,
                        PhysicalDimension.MASS,
                        "unified_atomic_mass_unit",
                        "synthetic-Si.upf",
                    ),
                ),
                (
                    PeriodicSite(
                        1,
                        "Si",
                        (0.0, 0.0, 0.0),
                        CoordinateConvention.CARTESIAN,
                        PhysicalDimension.LENGTH,
                        LengthUnit.BOHR,
                    ),
                ),
            ),
            reciprocal,
            points,
            KohnShamSpectralObservations(
                ((-0.0, 5e-324),),
                EnergyUnit.HARTREE,
                ((1.0, 0.0),),
                2,
                Availability.NO_SPIN_RESOLVED_ARRAYS,
                Availability.NOT_REPRESENTED,
            ),
            TotalEnergyObservation(
                -1.0000000000000002, EnergyUnit.HARTREE, Availability.NOT_REPRESENTED
            ),
            PlaneWaveRepresentationMetadata(
                "plane_wave",
                (2, 3, 4),
                (5, 6, 7),
                (8, 9, 10),
                PlaneWaveMetadataAvailability.NOT_REPRESENTED,
                PlaneWaveMetadataAvailability.NO_RETAINED_SUBSPACE,
                PlaneWaveMetadataAvailability.NOT_REPRESENTED,
                PlaneWaveMetadataAvailability.NOT_REPRESENTED,
            ),
            ArtifactProvenance(
                "/synthetic/qexsd.xml",
                "e" * 64,
                19,
                "QEXSD",
                "synthetic-schema:5",
                "synthetic-PWSCF",
                "fixture:31",
                "synthetic-only",
            ),
            0,
        )

    @classmethod
    def make_qe_value(cls, family: _QeFamily) -> _QeValue:
        if family == "pw":
            return qe.QuantumEspressoPwResult(
                identity=ResultObjectIdentity("synthetic-result"),
                evidence=cls.make_evidence(),
                contract_version="qe-pw-result:1",
            )
        if family == "bands":
            return qe.QuantumEspressoBandsResult(
                identity=ResultObjectIdentity("synthetic-result"),
                evidence=cls.make_evidence(qe.QuantumEspressoProgram.BANDS),
                contract_version="qe-bands-result:1",
            )
        return qe.QuantumEspressoExtractedObservationResult(
            identity=ResultObjectIdentity("synthetic-result"),
            observation=cls.make_neutral(),
            source_manifest_identity=a.ArtifactManifestIdentity("source-manifest"),
            source_manifest_entry_identity=a.ArtifactManifestEntryIdentity(
                "source-entry"
            ),
            source_artifact_identity=a.ArtifactIdentity("source-artifact"),
            source_content_identity=a.ArtifactContentIdentity("sha256", "e" * 64, 19),
            source_producer_provenance_identity=a.ArtifactProducerProvenanceIdentity(
                "source-producer"
            ),
            parsed_document_identity=qe.QuantumEspressoParsedDocumentIdentity(
                "parsed-document"
            ),
            parser_identity=qe.QuantumEspressoXsdParserIdentity(
                "ksdft2effmass.quantum-espresso.qexsd-parser"
            ),
            parser_version="1",
            normalization_policy=qe.QuantumEspressoObservationNormalizationPolicy(
                qe.QuantumEspressoObservationNormalizationPolicyIdentity(
                    "ksdft2effmass.quantum-espresso.qexsd-plane-wave-observation"
                ),
                "1",
            ),
            limitation_values=(
                "basis_identity.not_represented",
                "energy_reference.not_represented",
                "gauge.not_represented",
                "phase_convention.not_represented",
                "retained_subspace.no_retained_subspace",
                "spin_resolved_arrays.not_represented",
            ),
        )

    @staticmethod
    def make_scalar() -> q.ScalarQuantityOfInterestValue:
        evaluator = q.QuantityOfInterestEvaluatorIdentity("synthetic-evaluator:7")
        return q.ScalarQuantityOfInterestValue(
            ResultObjectIdentity("synthetic-result"),
            q.ScalarQuantityOfInterestDefinition(
                q.QuantityOfInterestIdentity("synthetic-qoi"),
                q.QuantityOfInterestSubjectIdentity("synthetic-subject"),
                q.QuantityOfInterestStateSpaceIdentity("synthetic-space"),
                q.QuantityOfInterestConventionIdentity("synthetic-convention"),
                evaluator,
                (
                    q.NormalizedObservationRequirementIdentity("second"),
                    q.NormalizedObservationRequirementIdentity("first"),
                ),
                q.QuantityOfInterestCompleteness.COMPLETE,
                "synthetic-unit",
            ),
            ResultObjectIdentity("synthetic-observations"),
            evaluator,
            -0.0,
        )

    @staticmethod
    def make_decision() -> w.ScientificDecisionResolution:
        return w.ScientificDecisionResolution(
            identity=ResultObjectIdentity("decision-correction"),
            content_identity=w.ResultObjectContentIdentity("opaque:historical-content"),
            request_identity=w.ScientificDecisionRequestIdentity("request"),
            verbatim_response="  yes — retain\nverbatim\tΩ  ",
            normalized_option_identity=w.ScientificDecisionOptionIdentity("option-yes"),
            response_source_identity=w.ResponseSourceIdentity("source"),
            authority_context_identity=w.AuthorityContextIdentity("context"),
            boundary_receipt_identity=w.BoundaryReceiptIdentity("boundary-receipt"),
            predecessor_resolution_identity=ResultObjectIdentity("decision-initial"),
            supersedes_resolution_identity=ResultObjectIdentity("decision-initial"),
            producer_provenance=w.RepresentedScientificDecisionIngressProducer(
                identity=w.ResultProducerProvenanceIdentity("producer"),
                workflow_identity=w.WorkflowIdentity("workflow"),
                workflow_run_identity=w.WorkflowRunIdentity("run"),
                request_identity=w.ScientificDecisionRequestIdentity("request"),
                transition_record_identity=w.ScientificDecisionTransitionRecordIdentity(
                    "transition"
                ),
                recorder_identity=w.ScientificDecisionRecorderIdentity("recorder:7"),
                response_source_identity=w.ResponseSourceIdentity("source"),
                authority_context_identity=w.AuthorityContextIdentity("context"),
                resolution_identity=ResultObjectIdentity("decision-correction"),
            ),
        )

    @classmethod
    def make_value(cls, family: Family) -> w.ResultObject:
        if family in ("pw", "bands", "observation"):
            return cls.make_qe_value(family)
        if family == "decision":
            return cls.make_decision()
        if family == "set":
            source = cls.make_qe_value("observation")
            assert type(source) is qe.QuantumEspressoExtractedObservationResult
            return w.NormalizedObservationSet(
                identity=w.ResultObjectIdentity("observation-set"),
                sources=(
                    replace(
                        source,
                        identity=w.ResultObjectIdentity("source-z"),
                        source_manifest_entry_identity=a.ArtifactManifestEntryIdentity(
                            "entry-z"
                        ),
                    ),
                    replace(
                        source,
                        identity=w.ResultObjectIdentity("source-a"),
                        source_manifest_entry_identity=a.ArtifactManifestEntryIdentity(
                            "entry-a"
                        ),
                    ),
                ),
            )
        scalar = cls.make_scalar()
        if family == "scalar":
            return scalar
        return q.ScalarQuantityOfInterestEvaluationFailure(
            scalar.identity,
            scalar.quantity,
            scalar.source_observation_set_result_identity,
            scalar.evaluator_identity,
            q.QuantityOfInterestEvaluationFailureCode.UNAVAILABLE,
            "synthetic unavailable observation",
        )

    @staticmethod
    def make_serializer() -> w.WorkflowRunSerializer:
        qe_codec = qe.QuantumEspressoResultValueSerializer()
        return w.WorkflowRunSerializer(
            result_codec=ApplicationResultValueSerializer(
                workflow_codec=w.WorkflowResultValueSerializer(source_codec=qe_codec),
                quantum_espresso_codec=qe_codec,
                quantity_of_interest_codec=q.QuantityOfInterestResultValueSerializer(),
            )
        )

    @staticmethod
    def metadata(family: Family) -> dict[str, str]:
        manifest = cast(
            dict[str, dict[str, str]],
            json.loads(
                Path(__file__)
                .parents[2]
                .joinpath("application/resources/result-values-v1.json")
                .read_bytes()
            ),
        )
        return manifest[family]

    @staticmethod
    def wire(family: Family) -> bytes:
        return (
            Path(__file__)
            .with_name("resources")
            .joinpath(f"workflow-run-{family}-v1.json")
            .read_bytes()
        )

    @classmethod
    def make_run(cls, genesis: w.WorkflowRun, family: Family) -> w.WorkflowRun:
        metadata = cls.metadata(family)
        reference = w.ResultObjectReference(
            identity=w.ResultObjectReferenceIdentity("reference"),
            result=cls.make_value(family),
            concrete_type_identity=w.ResultObjectTypeIdentity(
                metadata["concrete_type_identity"]
            ),
            owning_domain_identity=w.ResultObjectDomainIdentity(
                metadata["owning_domain_identity"]
            ),
            content_identity=w.ResultObjectContentIdentity(
                metadata["content_identity"]
            ),
            producer_provenance=w.UnknownLegacyResultProducer(
                identity=w.ResultProducerProvenanceIdentity("legacy-producer"),
                source_identity=w.RetainedResultSourceIdentity("synthetic-source"),
                evidence_identities=(
                    w.ResultProducerEvidenceIdentity("synthetic-evidence"),
                ),
                limitations=("synthetic software fixture; not historical evidence",),
            ),
        )
        outcome = w.TaskInvocationOutcome(
            identity=w.TaskInvocationOutcomeIdentity("outcome"),
            workflow_run_identity=genesis.identity,
            activation_identity=w.TaskActivationIdentity("activation"),
            operation_identity=w.OperationIdentity("operation"),
            attempt_identity=w.AttemptIdentity("attempt"),
            terminal_attempt_record_identity=w.TaskAttemptRecordIdentity("terminal"),
            kind=w.TaskInvocationOutcomeKind.CONFIRMED,
            results=(reference,),
            production_record_identities=(
                w.ResultProductionRecordIdentity("production"),
            ),
        )
        return replace(genesis, result_references=(reference,), outcomes=(outcome,))

    @classmethod
    def assert_result(cls, actual: w.ResultObject, expected: w.ResultObject) -> None:
        """Compare all concrete fields without NumPy's ambiguous dataclass equality."""
        assert type(actual) is type(expected)
        if type(actual) is w.NormalizedObservationSet:
            assert type(expected) is w.NormalizedObservationSet
            assert actual.identity == expected.identity
            assert len(actual.sources) == 2
            cls.assert_result(actual.sources[0], expected.sources[0])
            cls.assert_result(actual.sources[1], expected.sources[1])
        elif type(actual) is qe.QuantumEspressoExtractedObservationResult:
            assert type(expected) is qe.QuantumEspressoExtractedObservationResult
            # Neutral wire mechanics are independent of aggregate traversal.
            neutral = KohnShamPlaneWaveCalculationRecordJsonSerializer()
            assert neutral.serialize(actual.observation) == neutral.serialize(
                expected.observation
            )
            assert replace(actual, observation=expected.observation) == expected
        else:
            assert actual == expected
            if type(actual) is q.ScalarQuantityOfInterestValue:
                assert actual.value.hex() == "-0x0.0p+0"

    @pytest.mark.parametrize(
        "family",
        [
            pytest.param("pw", id="plane_wave_operation"),
            pytest.param("bands", id="bands_operation"),
            pytest.param("observation", id="parsed_neutral_observation"),
            pytest.param("scalar", id="scalar_success"),
            pytest.param("failure", id="scalar_failure"),
            pytest.param("decision", id="decision_correction"),
            pytest.param("set", id="ordered_concrete_sources"),
        ],
    )
    def test_method__serialize__matches_seven_family_aggregate_wires(
        self,
        genesis_snapshot: w.WorkflowRunSnapshot,
        family: Family,
    ) -> None:
        """Evidence ID: SV-WFR-SERIALIZER-RESULTS-001

        Requirement: Complete concrete values survive every represented occurrence.

        Method: Serialize direct constructor values under references and outcomes.

        Oracle: Independently authored aggregate wires embedding fixed concrete bytes.

        Acceptance: Complete aggregate bytes equal the fixed resource exactly.

        Interpretation: Seven supported concrete families traverse without substitution.

        Limitations: These synthetic runs do not assert structural link closure.
        """
        result = self.make_serializer().serialize(
            self.make_run(genesis_snapshot.run, family),
            genesis_snapshot.binding,
        )
        assert result.status == "encoded", result.failure
        assert result.encoded is not None
        assert result.encoded.payload == self.wire(family)

    @pytest.mark.parametrize(
        "family",
        [
            pytest.param("pw", id="plane_wave_operation"),
            pytest.param("bands", id="bands_operation"),
            pytest.param("observation", id="parsed_neutral_observation"),
            pytest.param("scalar", id="scalar_success"),
            pytest.param("failure", id="scalar_failure"),
            pytest.param("decision", id="decision_correction"),
            pytest.param("set", id="ordered_concrete_sources"),
        ],
    )
    def test_method__deserialize__restores_all_concrete_and_aggregate_fields(
        self,
        genesis_snapshot: w.WorkflowRunSnapshot,
        family: Family,
    ) -> None:
        """Evidence ID: SV-WFR-SERIALIZER-RESULTS-002

        Requirement: Decode restores all aggregate and concrete fields exactly.

        Method: Decode independent bytes and compare direct public constructors.

        Oracle: Separately authored values; neutral arrays use their existing owner.

        Acceptance: Both concrete occurrences and every remaining run field agree.

        Interpretation: Neither a round trip nor identity equality is the oracle.

        Limitations: Representation is not scientific or historical validation.
        """
        result = self.make_serializer().deserialize(self.wire(family))
        assert result.status == "decoded", result.failure
        assert result.run is not None
        expected = self.make_run(genesis_snapshot.run, family)
        actual_reference = result.run.result_references[0]
        expected_reference = expected.result_references[0]
        self.assert_result(actual_reference.result, expected_reference.result)
        self.assert_result(
            result.run.outcomes[0].results[0].result, expected_reference.result
        )
        assert (
            replace(actual_reference, result=expected_reference.result)
            == expected_reference
        )
        assert (
            replace(result.run.outcomes[0].results[0], result=expected_reference.result)
            == expected_reference
        )
        assert (
            replace(result.run.outcomes[0], results=expected.outcomes[0].results)
            == expected.outcomes[0]
        )
        assert (
            replace(
                result.run,
                result_references=expected.result_references,
                outcomes=expected.outcomes,
            )
            == expected
        )
        assert result.binding == genesis_snapshot.binding

    @pytest.mark.parametrize(
        "family",
        [
            pytest.param("pw", id="plane_wave_operation"),
            pytest.param("bands", id="bands_operation"),
            pytest.param("observation", id="parsed_neutral_observation"),
            pytest.param("scalar", id="scalar_success"),
            pytest.param("failure", id="scalar_failure"),
            pytest.param("decision", id="decision_correction"),
            pytest.param("set", id="ordered_concrete_sources"),
        ],
    )
    def test_method__deserialize__retains_concrete_version_failure(
        self,
        family: Family,
    ) -> None:
        """Evidence ID: SV-WFR-SERIALIZER-RESULTS-003

        Requirement: Unsupported concrete versions remain incompatible in aggregates.

        Method: Change only the concrete schema label in independently fixed bytes.

        Oracle: Seven explicitly supported version-one concrete classes only.

        Acceptance: Incompatible with unsupported-version evidence and no run.

        Interpretation: Aggregate decoding cannot bypass outward codec version checks.

        Limitations: Future compatibility policy is not specified here.
        """
        original = self.metadata(family)["schema_identity"].encode()
        wire = self.wire(family).replace(original, original[:-1] + b"2")
        result = self.make_serializer().deserialize(wire)
        assert result.status == "incompatible"
        assert result.failure is not None
        assert (
            result.failure.code is w.WorkflowPersistenceFailureCode.UNSUPPORTED_VERSION
        )
        assert result.run is None and result.binding is None

    @pytest.mark.parametrize(
        "field,replacement",
        [
            pytest.param(
                "concrete_type_identity", "wrong-type", id="reference_concrete_type"
            ),
            pytest.param(
                "owning_domain_identity", "wrong-domain", id="reference_owning_domain"
            ),
            pytest.param("content_identity", "wrong-content", id="reference_content"),
        ],
    )
    def test_method__deserialize__rejects_detached_reference_metadata(
        self,
        field: str,
        replacement: str,
    ) -> None:
        """Evidence ID: SV-WFR-SERIALIZER-RESULTS-004

        Requirement: Every reference metadata field binds its complete concrete value.

        Method: Change one outer reference label while leaving its envelope intact.

        Oracle: Fixed envelope metadata from the independent scalar aggregate.

        Acceptance: Corrupt content mismatch with no run or binding.

        Interpretation: A plausible concrete payload cannot validate detached metadata.

        Limitations: No structural producer-link validity is asserted.
        """
        wire = cast(dict[str, JsonValue], json.loads(self.wire("scalar")))
        run = self.fields(wire["run"])
        references = run["result_references"]
        assert isinstance(references, list)
        reference = self.fields(references[0])
        self.fields(reference[field])["value"] = replacement
        result = self.make_serializer().deserialize(
            json.dumps(
                wire, ensure_ascii=True, sort_keys=True, separators=(",", ":")
            ).encode("ascii")
        )
        assert result.status == "corrupt"
        assert result.failure is not None
        assert result.failure.code is w.WorkflowPersistenceFailureCode.CONTENT_MISMATCH
        assert result.run is None and result.binding is None

    @staticmethod
    def fields(value: JsonValue) -> dict[str, JsonValue]:
        """Select an explicit test wire record for a targeted negative mutation."""
        assert isinstance(value, dict)
        fields = value["fields"]
        assert isinstance(fields, dict)
        return fields

    @pytest.mark.parametrize(
        "direction",
        [
            pytest.param("encode", id="candidate_nested_source_conflict"),
            pytest.param("decode", id="wire_nested_source_conflict"),
        ],
    )
    def test_method__codec__rejects_conflicts_hidden_inside_observation_sets(
        self,
        genesis_snapshot: w.WorkflowRunSnapshot,
        direction: str,
    ) -> None:
        """Evidence ID: SV-WFR-SERIALIZER-RESULTS-005

        Requirement: Nested and standalone occurrences with the same identity agree.

        Method: Add a changed source-z standalone beside its fixed set occurrence.

        Oracle: The fixed source-z payload plus one explicit manifest-entry change.

        Acceptance: Content mismatch excludes encoded bytes and reconstructed run.

        Interpretation: Observation-set boundaries cannot hide identity conflicts.

        Limitations: Manifest labels are represented data, not authenticated sources.
        """
        import base64
        import hashlib

        run = self.make_run(genesis_snapshot.run, "set")
        value = run.result_references[0].result
        assert type(value) is w.NormalizedObservationSet
        source = value.sources[0]
        assert type(source) is qe.QuantumEspressoExtractedObservationResult
        changed = replace(
            source,
            source_manifest_entry_identity=a.ArtifactManifestEntryIdentity(
                "entry-other"
            ),
        )
        set_payload = (
            Path(__file__)
            .with_name("resources")
            .joinpath("result-observation-set-v1.json")
            .read_bytes()
        )
        set_fields = self.fields(cast(JsonValue, json.loads(set_payload)))
        sources = set_fields["sources"]
        assert isinstance(sources, list)
        envelope = self.fields(sources[0])
        payload_fields = self.fields(envelope["payload"])
        encoded_payload = payload_fields["value"]
        assert isinstance(encoded_payload, str)
        payload = base64.b64decode(encoded_payload, validate=True).replace(
            b"entry-z", b"entry-other"
        )
        digest = hashlib.sha256(payload).hexdigest()
        content = "qe-result-value:1:sha256:" + digest
        payload_fields["value"] = base64.b64encode(payload).decode("ascii")
        envelope["payload_digest"] = digest
        self.fields(envelope["content_identity"])["value"] = content
        reference = w.ResultObjectReference(
            identity=w.ResultObjectReferenceIdentity("source-reference"),
            result=changed,
            concrete_type_identity=w.ResultObjectTypeIdentity(
                "ksdft2effmass.integration.quantum_espresso.QuantumEspressoExtractedObservationResult:1"
            ),
            owning_domain_identity=w.ResultObjectDomainIdentity(
                "ksdft2effmass.integration.quantum_espresso"
            ),
            content_identity=w.ResultObjectContentIdentity(content),
            producer_provenance=run.result_references[0].producer_provenance,
        )
        if direction == "encode":
            result = self.make_serializer().serialize(
                replace(run, result_references=(*run.result_references, reference)),
                genesis_snapshot.binding,
            )
            assert result.status == "invalid" and result.encoded is None
            failure = result.failure
        else:
            wire = cast(dict[str, JsonValue], json.loads(self.wire("set")))
            references = self.fields(wire["run"])["result_references"]
            assert isinstance(references, list)
            original_reference = self.fields(references[0])
            references.append(
                {
                    "type": "ResultObjectReference",
                    "fields": {
                        "identity": {
                            "type": "ResultObjectReferenceIdentity",
                            "fields": {"value": "source-reference"},
                        },
                        "result": sources[0],
                        "concrete_type_identity": envelope["concrete_type_identity"],
                        "owning_domain_identity": envelope["owning_domain_identity"],
                        "content_identity": envelope["content_identity"],
                        "producer_provenance": original_reference[
                            "producer_provenance"
                        ],
                    },
                }
            )
            decoded = self.make_serializer().deserialize(
                json.dumps(
                    wire, ensure_ascii=True, sort_keys=True, separators=(",", ":")
                ).encode("ascii")
            )
            assert (
                decoded.status == "corrupt"
                and decoded.run is None
                and decoded.binding is None
            )
            failure = decoded.failure
        assert failure is not None
        assert failure.code is w.WorkflowPersistenceFailureCode.CONTENT_MISMATCH
