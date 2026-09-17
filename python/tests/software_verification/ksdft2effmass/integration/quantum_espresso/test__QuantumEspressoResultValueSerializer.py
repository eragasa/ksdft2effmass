r"""Software verification of ``QuantumEspressoResultValueSerializer``.

Bounded artifact scope: complete three-family QE result-value wire version 1.

Evidence profile: claim_bearing

Facet and represented meaning

Literal synthetic wires independently specify complete operation evidence and neutral
observations. No fixture is a calculated physical result or native executable input.

Intrinsic and cross-object scope

The codec owns canonical representation and envelope binding; existing constructors
own correlations and the neutral serializer retains its approved tolerance policy.

VVUQ and scientific exclusions

Software verification only, not scientific execution, provenance authentication,
numerical verification, validation, uncertainty quantification or aggregate closure.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import FrozenInstanceError, dataclass, replace
from pathlib import Path
from typing import Literal, Never, cast

import pytest
from ksdft2effmass.electronic_structure import KPointSampling, KPointWeightNormalization
from ksdft2effmass.integration import quantum_espresso as qe
from ksdft2effmass.integration.quantum_espresso import (
    QuantumEspressoResultValueSerializer,
)
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
    ResultObjectContentIdentity,
    ResultObjectDomainIdentity,
    ResultObjectIdentity,
    ResultObjectTypeIdentity,
    TaskActivationIdentity,
    TaskDefinitionIdentity,
    TaskInstanceIdentity,
    WorkflowEncodedResultValue,
    WorkflowPersistenceFailureCode,
    WorkflowResultValueCodec,
)
from ksdft2effmass.workflows import artifacts as a

type _Wire = None | bool | str | list[_Wire] | dict[str, _Wire]
type _Family = Literal["pw", "bands", "observation"]
type _Value = (
    qe.QuantumEspressoPwResult
    | qe.QuantumEspressoBandsResult
    | qe.QuantumEspressoExtractedObservationResult
)

pytestmark = pytest.mark.software_verification
SUT = QuantumEspressoResultValueSerializer


class TestQuantumEspressoResultValueSerializer:
    """One concrete serializer with independent wires and exact field oracles."""

    @staticmethod
    def fixture_bytes(family: _Family) -> bytes:
        name = {
            "pw": "result-values-v1.json",
            "bands": "result-bands-v1.json",
            "observation": "result-observation-v1.json",
        }[family]
        return Path(__file__).with_name("resources").joinpath(name).read_bytes()

    @staticmethod
    def make_envelope(
        payload: bytes, family: _Family = "pw"
    ) -> WorkflowEncodedResultValue:
        tag = {
            "pw": "QuantumEspressoPwResult",
            "bands": "QuantumEspressoBandsResult",
            "observation": "QuantumEspressoExtractedObservationResult",
        }[family]
        digest = hashlib.sha256(payload).hexdigest()
        return WorkflowEncodedResultValue(
            result_identity=ResultObjectIdentity("synthetic-result"),
            concrete_type_identity=ResultObjectTypeIdentity(
                "ksdft2effmass.integration.quantum_espresso." + tag + ":1"
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
        )

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
    def make_value(cls, family: _Family) -> _Value:
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

    @pytest.mark.parametrize(
        "family",
        [
            pytest.param("pw", id="pw"),
            pytest.param("bands", id="bands"),
            pytest.param("observation", id="extracted_observation"),
        ],
    )
    def test_method__encode__matches_independent_complete_wire(
        self, family: _Family
    ) -> None:
        """Evidence ID: SV-QE-CODEC-001

        Requirement: Each supported family retains every field in canonical bytes.

        Method: Encode independently constructed values against fixed literal wires.

        Oracle: Authored version-one resources, independent of the production codec.

        Acceptance: The entire envelope equals the byte-bound literal expectation.

        Interpretation: Complete field mapping is verified, not merely round trip.

        Limitations: Synthetic data establish no external provenance truth.
        """
        encoded = QuantumEspressoResultValueSerializer().encode(self.make_value(family))
        assert encoded.status == "encoded"
        assert encoded.failure is None
        assert encoded.encoded == self.make_envelope(self.fixture_bytes(family), family)

    @pytest.mark.parametrize(
        "family",
        [
            pytest.param("pw", id="pw"),
            pytest.param("bands", id="bands"),
            pytest.param("observation", id="extracted_observation"),
        ],
    )
    def test_method__decode__reconstructs_literal_complete_fields(
        self, family: _Family
    ) -> None:
        """Evidence ID: SV-QE-CODEC-002

        Requirement: Literal envelopes reconstruct complete exact concrete records.

        Method: Decode authored wires and compare independent constructor values.

        Oracle: Separate immutable domain constructors specify every retained field.

        Acceptance: Concrete type and all nested fields agree exactly without failure.

        Interpretation: Decoder expectations do not originate in encoder output.

        Limitations: This does not reconstruct a complete WorkflowRun.
        """
        decoded = QuantumEspressoResultValueSerializer().decode(
            self.make_envelope(self.fixture_bytes(family), family)
        )
        expected = self.make_value(family)
        assert decoded.status == "decoded"
        assert type(decoded.value) is type(expected)
        assert decoded.value == expected
        assert decoded.failure is None

    def test_method__decode__preserves_neutral_precision_and_immutability(self) -> None:
        """Evidence ID: SV-QE-CODEC-003

        Requirement: Neutral precision, units, tolerance and immutable state survive.

        Method: Decode a literal observation and challenge its nested tuple state.

        Oracle: Fixed binary64 hex values, Hartree/bohr units and neutral literal JSON.

        Acceptance: Signed zero, subnormal, total energy and delegated bytes are exact.

        Interpretation: No tolerance change, normalization or precision loss occurs.

        Limitations: Exact representation is not scientific validation.
        """
        decoded = QuantumEspressoResultValueSerializer().decode(
            self.make_envelope(self.fixture_bytes("observation"), "observation")
        )
        assert type(decoded.value) is qe.QuantumEspressoExtractedObservationResult
        record = decoded.value.observation
        assert record.spectrum.eigenvalues[0][0].hex() == "-0x0.0p+0"
        assert record.spectrum.eigenvalues[0][1].hex() == "0x0.0000000000001p-1022"
        assert record.total_energy.value.hex() == "-0x1.0000000000001p+0"
        assert record.spectrum.eigenvalue_unit is EnergyUnit.HARTREE
        assert record.structure.direct_lattice.unit is LengthUnit.BOHR
        literal = (
            Path(__file__)
            .with_name("resources")
            .joinpath("result-neutral-v1.json")
            .read_text()
        )
        assert (
            KohnShamPlaneWaveCalculationRecordJsonSerializer().serialize(record)
            == literal
        )
        assert '"duality_absolute_tolerance":1e-12' in literal
        with pytest.raises(TypeError):
            record.spectrum.eigenvalues[0][0] = 1.0  # type: ignore[index]
        with pytest.raises(FrozenInstanceError):
            decoded.value.parser_version = "2"  # type: ignore[misc]

    @classmethod
    def make_variant(cls, variant: str) -> qe.QuantumEspressoPwResult:
        evidence = cls.make_evidence()
        report = evidence.diagnostic_report
        process = evidence.process_observation
        notice = report.observations[0]
        outcome: qe.QuantumEspressoCalculatorOutcome
        if variant == "signal":
            process = replace(
                process,
                termination=qe.QuantumEspressoProcessSignalTermination(9),
                peak_resident_bytes=None,
            )
            outcome = qe.QuantumEspressoProcessFailedOutcome(
                qe.QuantumEspressoProcessFailureKind.SIGNAL
            )
        elif variant == "timeout":
            process = replace(
                process,
                termination=qe.QuantumEspressoProcessTimeout(
                    timeout_milliseconds=123, termination_sent=True, kill_sent=True
                ),
            )
            outcome = qe.QuantumEspressoProcessFailedOutcome(
                qe.QuantumEspressoProcessFailureKind.TIMEOUT
            )
        elif variant == "nonzero":
            process = replace(
                process, termination=qe.QuantumEspressoNormalProcessExit(17)
            )
            outcome = qe.QuantumEspressoProcessFailedOutcome(
                qe.QuantumEspressoProcessFailureKind.NONZERO_EXIT
            )
        elif variant == "fatal":
            report = replace(
                report,
                observations=(
                    replace(
                        notice,
                        disposition=qe.QuantumEspressoDiagnosticDisposition.FATAL,
                    ),
                ),
                completion_markers=(),
                kind=qe.QuantumEspressoDiagnosticReportKind.FATAL,
            )
            outcome = qe.QuantumEspressoCalculatorFailedOutcome((notice.identity,))
        elif variant == "contradictory":
            report = replace(
                report,
                observations=(
                    replace(
                        notice,
                        disposition=qe.QuantumEspressoDiagnosticDisposition.SECONDARY_FATAL,
                    ),
                ),
                kind=qe.QuantumEspressoDiagnosticReportKind.CONTRADICTORY,
            )
            outcome = qe.QuantumEspressoDiagnosticUnresolvedOutcome(
                (notice.identity,), ("synthetic-contradiction",)
            )
        else:
            report = replace(
                report,
                observations=(
                    replace(
                        notice,
                        disposition=qe.QuantumEspressoDiagnosticDisposition.UNRESOLVED,
                        signature_identity=None,
                    ),
                ),
                kind=qe.QuantumEspressoDiagnosticReportKind.UNRESOLVED,
            )
            outcome = qe.QuantumEspressoDiagnosticUnresolvedOutcome(
                (notice.identity,), ("synthetic-unresolved",)
            )
        return qe.QuantumEspressoPwResult(
            identity=ResultObjectIdentity("synthetic-result"),
            evidence=replace(
                evidence,
                process_observation=process,
                diagnostic_report=report,
                calculator_outcome=outcome,
            ),
            contract_version="qe-pw-result:1",
        )

    @pytest.mark.parametrize(
        "variant,termination,outcome",
        [
            pytest.param(
                "signal",
                b'{"fields":{"signal_number":{"fields":{"value":"0x9"},"type":"int"}},"type":"QuantumEspressoProcessSignalTermination"}',
                b'{"fields":{"reason":{"fields":{"value":"signal"},"type":"QuantumEspressoProcessFailureKind"}},"type":"QuantumEspressoProcessFailedOutcome"}',
                id="signal",
            ),
            pytest.param(
                "timeout",
                b'{"fields":{"kill_sent":true,"termination_sent":true,"timeout_milliseconds":{"fields":{"value":"0x7b"},"type":"int"}},"type":"QuantumEspressoProcessTimeout"}',
                b'{"fields":{"reason":{"fields":{"value":"timeout"},"type":"QuantumEspressoProcessFailureKind"}},"type":"QuantumEspressoProcessFailedOutcome"}',
                id="timeout",
            ),
            pytest.param(
                "nonzero",
                b'{"fields":{"exit_code":{"fields":{"value":"0x11"},"type":"int"}},"type":"QuantumEspressoNormalProcessExit"}',
                b'{"fields":{"reason":{"fields":{"value":"nonzero_exit"},"type":"QuantumEspressoProcessFailureKind"}},"type":"QuantumEspressoProcessFailedOutcome"}',
                id="nonzero_exit",
            ),
            pytest.param(
                "fatal",
                b'{"fields":{"exit_code":{"fields":{"value":"0x0"},"type":"int"}},"type":"QuantumEspressoNormalProcessExit"}',
                b'{"fields":{"fatal_diagnostic_identities":[{"fields":{"value":"notice"},"type":"QuantumEspressoDiagnosticObservationIdentity"}]},"type":"QuantumEspressoCalculatorFailedOutcome"}',
                id="calculator_fatal",
            ),
            pytest.param(
                "unresolved",
                b'{"fields":{"exit_code":{"fields":{"value":"0x0"},"type":"int"}},"type":"QuantumEspressoNormalProcessExit"}',
                b'{"fields":{"diagnostic_identities":[{"fields":{"value":"notice"},"type":"QuantumEspressoDiagnosticObservationIdentity"}],"reason_identities":["synthetic-unresolved"]},"type":"QuantumEspressoDiagnosticUnresolvedOutcome"}',
                id="unresolved",
            ),
            pytest.param(
                "contradictory",
                b'{"fields":{"exit_code":{"fields":{"value":"0x0"},"type":"int"}},"type":"QuantumEspressoNormalProcessExit"}',
                b'{"fields":{"diagnostic_identities":[{"fields":{"value":"notice"},"type":"QuantumEspressoDiagnosticObservationIdentity"}],"reason_identities":["synthetic-contradiction"]},"type":"QuantumEspressoDiagnosticUnresolvedOutcome"}',
                id="contradictory",
            ),
        ],
    )
    def test_method__encode__retains_closed_operation_variants(
        self, variant: str, termination: bytes, outcome: bytes
    ) -> None:
        """Evidence ID: SV-QE-CODEC-004

        Requirement: Closed termination, diagnostic and outcome variants remain data.

        Method: Encode explicit variants against literal wire fragments and decode.

        Oracle: Independent exact fragments and complete constructed variant records.

        Acceptance: Exact fragments and complete reconstructed fields agree.

        Interpretation: Failure and uncertainty are not replaced by successful output.

        Limitations: No process, diagnostic classifier or scientific tool is invoked.
        """
        value = self.make_variant(variant)
        codec = QuantumEspressoResultValueSerializer()
        encoded = codec.encode(value)
        assert encoded.encoded is not None
        assert b'"termination":' + termination in encoded.encoded.payload
        assert b'"calculator_outcome":' + outcome in encoded.encoded.payload
        decoded = codec.decode(encoded.encoded)
        assert decoded.status == "decoded"
        assert decoded.value == value

    @pytest.mark.parametrize(
        "family,old,new",
        [
            pytest.param(
                "pw",
                b'"0xffffffffffffffff"',
                b'"0x10000000000000000"',
                id="integer_overflow",
            ),
            pytest.param(
                "pw",
                b'"0xffffffffffffffff"',
                b'"0x0ffffffffffffffff"',
                id="noncanonical_integer",
            ),
            pytest.param("pw", b'"0xffffffffffffffff"', b"true", id="boolean_integer"),
            pytest.param("pw", b'"0xffffffffffffffff"', b"123", id="raw_integer"),
            pytest.param("pw", b'"0xffffffffffffffff"', b"NaN", id="nonfinite_token"),
            pytest.param(
                "pw",
                b'"value":"attempt"',
                b'"value":"detached-attempt"',
                id="nested_attempt_correlation",
            ),
            pytest.param(
                "pw",
                b'"value":"marker"',
                b'"value":"detached-marker"',
                id="outcome_marker_correlation",
            ),
            pytest.param(
                "pw",
                b'"type":"OperationIdentity"',
                b'"type":"AttemptIdentity"',
                id="wrong_nominal_type",
            ),
            pytest.param(
                "pw",
                b'"observer_version":"synthetic-observer:99",',
                b"",
                id="missing_field",
            ),
            pytest.param(
                "pw",
                b'"observer_version":"synthetic-observer:99"',
                b'"observer_version":"synthetic-observer:99","extra":null',
                id="extra_field",
            ),
            pytest.param(
                "pw",
                b'"observer_version":"synthetic-observer:99"',
                b'"observer_version":"synthetic-observer:99","observer_version":"duplicate"',
                id="duplicate_member",
            ),
            pytest.param(
                "pw",
                b'"value":"output-b"',
                b'"value":"output-a"',
                id="duplicate_manifest_entry",
            ),
            pytest.param(
                "pw",
                b'"value":"input.in"',
                b'"value":"../input.in"',
                id="unsafe_destination",
            ),
            pytest.param(
                "observation",
                b'"value":"0x13"',
                b'"value":"0x14"',
                id="neutral_source_count_mismatch",
            ),
            pytest.param(
                "observation",
                b'"type":"QuantumEspressoParsedDocumentIdentity"',
                b'"type":"ArtifactIdentity"',
                id="parsed_document_nominal_mismatch",
            ),
            pytest.param(
                "observation",
                b"ksdft2effmass.quantum-espresso.qexsd-parser",
                b"other-parser",
                id="parser_identity_mismatch",
            ),
            pytest.param(
                "observation",
                b"ksdft2effmass.quantum-espresso.qexsd-plane-wave-observation",
                b"other-policy",
                id="policy_identity_mismatch",
            ),
            pytest.param(
                "observation",
                b"basis_identity.not_represented",
                b"basis_identity.available",
                id="limitations_mismatch",
            ),
            pytest.param(
                "observation", b"1e-12", b"1e-11", id="neutral_tolerance_mismatch"
            ),
            pytest.param(
                "observation",
                b'\\"source_format\\":\\"QEXSD\\"',
                b'\\"source_format\\":\\"OTHER\\"',
                id="neutral_source_format_mismatch",
            ),
        ],
    )
    def test_method__decode__rejects_known_wire_corruption(
        self, family: _Family, old: bytes, new: bytes
    ) -> None:
        """Evidence ID: SV-QE-CODEC-005

        Requirement: Malformed wires and detached nested identity links fail closed.

        Method: Rebind checksums after one explicit literal corruption.

        Oracle: Independent field grammar and owning constructor correlations.

        Acceptance: Every case returns corrupt with no reconstructed value.

        Interpretation: A matching payload checksum cannot hide malformed content.

        Limitations: Identity labels are not externally authenticated.
        """
        original = self.fixture_bytes(family)
        assert old in original
        mutated = original.replace(old, new, 1)
        result = QuantumEspressoResultValueSerializer().decode(
            self.make_envelope(mutated, family)
        )
        assert result.status == "corrupt"
        assert result.value is None
        assert result.failure is not None

    @pytest.mark.parametrize(
        "family,old,new",
        [
            pytest.param("pw", b"qe-pw-result:1", b"qe-pw-result:2", id="pw_version"),
            pytest.param(
                "bands", b"qe-bands-result:1", b"qe-bands-result:2", id="bands_version"
            ),
            pytest.param(
                "pw",
                b"qe-execution-input:1",
                b"qe-execution-input:2",
                id="input_version",
            ),
            pytest.param(
                "observation",
                b'"parser_version":"1"',
                b'"parser_version":"2"',
                id="parser_version",
            ),
            pytest.param(
                "observation", b'"version":"1"', b'"version":"2"', id="policy_version"
            ),
            pytest.param(
                "observation",
                b'\\"schema_version\\":1',
                b'\\"schema_version\\":2',
                id="neutral_schema",
            ),
        ],
    )
    def test_method__decode__rejects_unknown_nested_versions(
        self, family: _Family, old: bytes, new: bytes
    ) -> None:
        """Evidence ID: SV-QE-CODEC-006

        Requirement: Unknown owning versions are incompatible, not success.

        Method: Decode re-bound literal wires with one unsupported nested version.

        Oracle: Exact supported QE input/result, parser, policy and neutral versions.

        Acceptance: Incompatible with unsupported-version evidence and no value.

        Interpretation: Provenance labels differ from supported wire versions.

        Limitations: No migration of unknown versions is attempted.
        """
        payload = self.fixture_bytes(family)
        assert old in payload
        result = QuantumEspressoResultValueSerializer().decode(
            self.make_envelope(payload.replace(old, new, 1), family)
        )
        assert result.status == "incompatible"
        assert result.value is None
        assert result.failure is not None
        assert result.failure.code is WorkflowPersistenceFailureCode.UNSUPPORTED_VERSION

    @pytest.mark.parametrize(
        "boundary",
        [
            pytest.param("schema", id="schema"),
            pytest.param("type", id="concrete_type"),
            pytest.param("domain", id="domain"),
            pytest.param("content", id="content"),
            pytest.param("identity", id="result_identity"),
        ],
    )
    def test_method__decode__binds_all_envelope_metadata(self, boundary: str) -> None:
        """Evidence ID: SV-QE-CODEC-007

        Requirement: All concrete envelope identities constrain reconstruction.

        Method: Substitute one metadata field while retaining a valid literal payload.

        Oracle: Known schema and concrete labels, domain, content and result identity.

        Acceptance: Unknown schema/type is incompatible; detached metadata is corrupt.

        Interpretation: Byte binding alone does not identify a concrete domain value.

        Limitations: Intrinsic envelope digest validation has its own evidence owner.
        """
        envelope = self.make_envelope(self.fixture_bytes("pw"))
        if boundary == "schema":
            envelope = replace(envelope, schema_identity="qe-result-value:2")
        elif boundary == "type":
            envelope = replace(
                envelope,
                concrete_type_identity=ResultObjectTypeIdentity(
                    "ksdft2effmass.integration.quantum_espresso.QuantumEspressoPwResult:2"
                ),
            )
        elif boundary == "domain":
            envelope = replace(
                envelope, owning_domain_identity=ResultObjectDomainIdentity("other")
            )
        elif boundary == "content":
            envelope = replace(
                envelope, content_identity=ResultObjectContentIdentity("other")
            )
        else:
            envelope = replace(envelope, result_identity=ResultObjectIdentity("other"))
        result = QuantumEspressoResultValueSerializer().decode(envelope)
        assert result.status == (
            "incompatible" if boundary in ("schema", "type") else "corrupt"
        )
        assert result.value is None
        assert result.failure is not None

    def test_method__encode__rejects_unsupported_input_versions(self) -> None:
        """Evidence ID: SV-QE-CODEC-008

        Requirement: Encode cannot emit an unsupported nested execution-input version.

        Method: Construct a valid result carrying a future execution-input contract.

        Oracle: Only qe-execution-input:1 is supported by this codec version.

        Acceptance: Incompatible unsupported-version evidence with no envelope.

        Interpretation: Nonempty domain labels alone do not establish codec support.

        Limitations: Future contract semantics are not interpreted.
        """
        evidence = self.make_evidence()
        value = qe.QuantumEspressoPwResult(
            identity=ResultObjectIdentity("synthetic-result"),
            evidence=replace(
                evidence,
                execution_input=replace(
                    evidence.execution_input, contract_version="qe-execution-input:2"
                ),
            ),
            contract_version="qe-pw-result:1",
        )
        result = QuantumEspressoResultValueSerializer().encode(value)
        assert result.status == "incompatible"
        assert result.encoded is None
        assert result.failure is not None
        assert result.failure.code is WorkflowPersistenceFailureCode.UNSUPPORTED_VERSION

    def test_method__encode__rejects_identity_only_standins(self) -> None:
        """Evidence ID: SV-QE-CODEC-009

        Requirement: ResultObject conformance alone does not supply concrete content.

        Method: Encode an immutable identity-only protocol implementation.

        Oracle: Exactly three supported concrete result classes.

        Acceptance: Incompatible unsupported-type evidence and no encoded value.

        Interpretation: No dynamic registry or arbitrary-result reflection is used.

        Limitations: Complete aggregate codec injection is outside this test.
        """

        @dataclass(frozen=True)
        class IdentityOnly:
            identity: ResultObjectIdentity

        result = QuantumEspressoResultValueSerializer().encode(
            IdentityOnly(ResultObjectIdentity("synthetic-result"))
        )
        assert result.status == "incompatible"
        assert result.encoded is None
        assert result.failure is not None
        assert result.failure.code is WorkflowPersistenceFailureCode.UNSUPPORTED_TYPE

    def test_method__decode__rejects_noncanonical_bytes(self) -> None:
        """Evidence ID: SV-QE-CODEC-010

        Requirement: Equivalent JSON with noncanonical whitespace is corrupt.

        Method: Add a newline to a valid literal and rebind the envelope checksum.

        Oracle: Version one has exactly canonical compact bytes without final newline.

        Acceptance: Corrupt with no decoded value.

        Interpretation: Re-encoding checks exact represented bytes rather than equality.

        Limitations: The nested neutral serializer retains its own newline.
        """
        result = QuantumEspressoResultValueSerializer().decode(
            self.make_envelope(self.fixture_bytes("pw") + b"\n")
        )
        assert result.status == "corrupt"
        assert result.value is None

    def test_method__encode__distinguishes_equal_identity_different_content(
        self,
    ) -> None:
        """Evidence ID: SV-QE-CODEC-011

        Requirement: Identical result labels cannot collapse different complete content.

        Method: Encode two values differing only by retained observer provenance.

        Oracle: Literal field difference requires different content-bound bytes.

        Acceptance: Result identity agrees but bytes, content and digests differ.

        Interpretation: A later aggregate can detect conflicting repeated occurrences.

        Limitations: This codec does not itself own the aggregate identity map.
        """
        first = self.make_value("pw")
        assert type(first) is qe.QuantumEspressoPwResult
        second = replace(
            first,
            evidence=replace(
                first.evidence,
                process_observation=replace(
                    first.evidence.process_observation,
                    observer_version="synthetic-observer:100",
                ),
            ),
        )
        codec = QuantumEspressoResultValueSerializer()
        left, right = codec.encode(first).encoded, codec.encode(second).encoded
        assert left is not None and right is not None
        assert left.result_identity == right.result_identity
        assert left.payload != right.payload
        assert left.content_identity != right.content_identity
        assert left.payload_digest != right.payload_digest

    def test_public_api__package__supports_injected_immutable_codec(self) -> None:
        """Evidence ID: SV-QE-CODEC-012

        Requirement: The outward codec satisfies the injected typed port immutably.

        Method: Import from the supported package and inspect nominal protocol behavior.

        Oracle: Explicit public export and WorkflowResultValueCodec interface.

        Acceptance: Correct owner, export and protocol membership; no state fields.

        Interpretation: Dependency composition requires no inward integration import.

        Limitations: Application composition and aggregate persistence remain separate.
        """
        codec: WorkflowResultValueCodec = QuantumEspressoResultValueSerializer()
        assert isinstance(codec, WorkflowResultValueCodec)
        assert "QuantumEspressoResultValueSerializer" in qe.__all__
        assert (
            QuantumEspressoResultValueSerializer.__module__
            == "ksdft2effmass.integration.quantum_espresso.result_values"
        )
        assert QuantumEspressoResultValueSerializer.__slots__ == ()

    def test_method__decode__rejects_unknown_report_kind(self) -> None:
        """Evidence ID: SV-QE-CODEC-016

        Requirement: Unknown values of the known diagnostic enum are corrupt.

        Method: Replace the literal clear kind with an unknown string.

        Oracle: Closed diagnostic-report enum rather than a new schema version.

        Acceptance: Corrupt with no decoded value.

        Interpretation: Unknown enum values do not introduce new result families.

        Limitations: This does not classify native output.
        """
        payload = self.fixture_bytes("pw").replace(
            b'"value":"clear"', b'"value":"not-a-report"', 1
        )
        result = QuantumEspressoResultValueSerializer().decode(
            self.make_envelope(payload)
        )
        assert result.status == "corrupt"
        assert result.value is None

    def test_method__codec__retains_optional_absence(self) -> None:
        """Evidence ID: SV-QE-CODEC-017

        Requirement: Optional neutral arrays and producer versions remain absent.

        Method: Encode a source with absent occupations and producing version.

        Oracle: Explicit null fields and unchanged independently constructed record.

        Acceptance: Nulls appear in the nested wire and decode equals the input.

        Interpretation: Absence is retained rather than filled from ambient data.

        Limitations: Missing physical information is not inferred.
        """
        value = self.make_value("observation")
        assert type(value) is qe.QuantumEspressoExtractedObservationResult
        record = value.observation
        value = replace(
            value,
            observation=replace(
                record,
                spectrum=replace(record.spectrum, occupations=None),
                provenance=replace(
                    record.provenance, producing_application_version=None
                ),
            ),
        )
        codec = QuantumEspressoResultValueSerializer()
        encoded = codec.encode(value)
        assert encoded.encoded is not None
        assert b'\\"occupations\\":null' in encoded.encoded.payload
        assert b'\\"producing_application_version\\":null' in encoded.encoded.payload
        assert codec.decode(encoded.encoded).value == value

    def test_method__encode__rejects_invalid_neutral_cross_record_state(self) -> None:
        """Evidence ID: SV-QE-CODEC-018

        Requirement: Invalid neutral cross-record state cannot produce an envelope.

        Method: Supply two spectrum rows for one sampled point in synthetic data.

        Oracle: The existing neutral serializer owns exact sample-count agreement.

        Acceptance: Invalid invariant-violation evidence and no envelope.

        Interpretation: Delegation retains the neutral owner's existing checks.

        Limitations: No scientific setting or neutral algorithm is changed.
        """
        value = self.make_value("observation")
        assert type(value) is qe.QuantumEspressoExtractedObservationResult
        record = value.observation
        spectrum = replace(
            record.spectrum,
            eigenvalues=((-0.0, 5e-324), (-0.0, 5e-324)),
            occupations=((1.0, 0.0), (1.0, 0.0)),
        )
        value = replace(value, observation=replace(record, spectrum=spectrum))
        encoded = QuantumEspressoResultValueSerializer().encode(value)
        assert encoded.status == "invalid"
        assert encoded.encoded is None
        assert encoded.failure is not None
        assert (
            encoded.failure.code is WorkflowPersistenceFailureCode.INVARIANT_VIOLATION
        )

    def test_method__encode__rejects_concrete_subclasses(self) -> None:
        """Evidence ID: SV-QE-CODEC-019

        Requirement: Subclasses cannot silently lose additional concrete content.

        Method: Encode a subclass inheriting an otherwise valid PW result.

        Oracle: Exact concrete class support, not nominal inheritance acceptance.

        Acceptance: Incompatible unsupported-type evidence without an envelope.

        Interpretation: The serializer does not promise arbitrary subtype support.

        Limitations: Future supported types require their own explicit contract.
        """

        class DerivedPwResult(qe.QuantumEspressoPwResult):
            pass

        value = DerivedPwResult(
            identity=ResultObjectIdentity("synthetic-result"),
            evidence=self.make_evidence(),
            contract_version="qe-pw-result:1",
        )
        encoded = QuantumEspressoResultValueSerializer().encode(value)
        assert encoded.status == "incompatible"
        assert encoded.encoded is None
        assert encoded.failure is not None
        assert encoded.failure.code is WorkflowPersistenceFailureCode.UNSUPPORTED_TYPE

    @staticmethod
    def fail_memory(*args: _Wire, **kwargs: _Wire) -> Never:
        raise MemoryError("must-not-leak-synthetic-detail")

    @staticmethod
    def fail_operation(*args: _Wire, **kwargs: _Wire) -> Never:
        raise RuntimeError("must-not-leak-synthetic-detail")

    @pytest.mark.parametrize(
        "phase,fault",
        [
            pytest.param("encode", "memory", id="encode_memory"),
            pytest.param("decode", "memory", id="decode_memory"),
            pytest.param("encode", "operation", id="encode_operation"),
            pytest.param("decode", "operation", id="decode_operation"),
        ],
    )
    def test_method__codec__represents_operational_failures(
        self, monkeypatch: pytest.MonkeyPatch, phase: str, fault: str
    ) -> None:
        """Evidence ID: SV-QE-CODEC-013

        Requirement: Operational failure yields sanitized error without partial data.

        Method: Inject a controlled JSON allocation or operational exception.

        Oracle: Closed error status and stable representation-limit/codec-error codes.

        Acceptance: Error, no success data and no raw exception detail in diagnostics.

        Interpretation: Mechanical failure cannot masquerade as corrupt or success.

        Limitations: Controlled faults are not hardware reliability evidence.
        """
        value = self.make_value("pw")
        envelope = self.make_envelope(self.fixture_bytes("pw"))
        monkeypatch.setattr(
            json,
            "dumps" if phase == "encode" else "loads",
            self.fail_memory if fault == "memory" else self.fail_operation,
        )
        codec = QuantumEspressoResultValueSerializer()
        if phase == "encode":
            encoded = codec.encode(value)
            assert encoded.status == "error" and encoded.encoded is None
            failure = encoded.failure
        else:
            decoded = codec.decode(envelope)
            assert decoded.status == "error" and decoded.value is None
            failure = decoded.failure
        assert failure is not None
        assert failure.code is (
            WorkflowPersistenceFailureCode.REPRESENTATION_LIMIT
            if fault == "memory"
            else WorkflowPersistenceFailureCode.CODEC_ERROR
        )
        assert "must-not-leak" not in failure.diagnostic

    def test_method__codec__rejects_wrong_direct_types(self) -> None:
        """Evidence ID: SV-QE-CODEC-014

        Requirement: Wrong direct Python semantic types raise TypeError.

        Method: Supply an integer to encode and bytes instead of an envelope to decode.

        Oracle: Exact typed public API rather than permissive scalar coercion.

        Acceptance: Both invalid calls raise TypeError.

        Interpretation: Wrong direct types differ from represented codec failures.

        Limitations: Closed invalid cases do not widen the production signatures.
        """
        codec = QuantumEspressoResultValueSerializer()
        with pytest.raises(TypeError):
            codec.encode(1)  # type: ignore[arg-type]
        with pytest.raises(TypeError):
            codec.decode(b"{}")  # type: ignore[arg-type]

    def test_method__decode__does_not_retain_mutable_wire_containers(self) -> None:
        """Evidence ID: SV-QE-CODEC-015

        Requirement: Decode reconstructs immutable tuples, not mutable wire lists.

        Method: Decode, mutate a separately parsed JSON tree and re-encode.

        Oracle: Original fixed bytes and immutable nested tuple contracts.

        Acceptance: Mutation cannot alter decoded content or re-encoded bytes.

        Interpretation: No mutable parsed-container cache or aliased state is retained.

        Limitations: This is operational immutability, not cryptographic authentication.
        """
        payload = self.fixture_bytes("pw")
        codec = QuantumEspressoResultValueSerializer()
        decoded = codec.decode(self.make_envelope(payload))
        assert type(decoded.value) is qe.QuantumEspressoPwResult
        assert type(decoded.value.evidence.execution_input.pseudopotentials) is tuple
        wire = cast(dict[str, _Wire], json.loads(payload))
        wire.clear()
        encoded = codec.encode(decoded.value)
        assert encoded.encoded is not None
        assert encoded.encoded.payload == payload
