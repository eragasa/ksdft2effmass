r"""Software verification of ``QuantumEspressoObservationAdapter``.

Evidence profile: routine

Bounded artifact scope: Integration-owned first-stage QEXSD observation extraction.

Facet and represented meaning

The ActionObject correlates exact admitted artifact bytes with a parsed QEXSD document
and constructs one explicitly limited neutral plane-wave Kohn--Sham observation.

Intrinsic and cross-object scope

The evidence covers manifest membership, exact byte identity, native-format and policy
rejection, retained neutral semantics, lineage retention, and nonmutation.

VVUQ and scientific exclusions

The controlled QEXSD bytes are synthetic test data. Exact adaptation establishes
software verification only, not numerical verification, scientific validation, UQ,
physical correctness, convergence, or acceptance.
"""

from copy import deepcopy
from dataclasses import FrozenInstanceError, replace

import pytest

from ksdft2effmass.integration.quantum_espresso import (
    QuantumEspressoExtractedObservationResult,
    QuantumEspressoObservationAdaptationFailure,
    QuantumEspressoObservationAdaptationFailureCode,
    QuantumEspressoObservationAdapter,
    QuantumEspressoObservationExtractionRequest,
    QuantumEspressoObservationNormalizationPolicy,
    QuantumEspressoObservationNormalizationPolicyIdentity,
    QuantumEspressoParsedDocumentIdentity,
    QuantumEspressoParsedDocumentRecord,
    QuantumEspressoXsdParserIdentity,
)
from ksdft2effmass.integration.quantum_espresso.qexsd import (
    ConstructQexsdKohnShamPlaneWaveRecord,
    QexsdDocument,
    QexsdSource,
    QuantumEspressoXsdDocumentParser,
)
from ksdft2effmass.ksdft import Availability, EnergyUnit
from ksdft2effmass.workflows import (
    AttemptIdentity,
    ResultObject,
    ResultObjectIdentity,
    TaskActivationIdentity,
    TaskInstanceIdentity,
)
from ksdft2effmass.workflows.artifacts import (
    ArtifactContentIdentity,
    ArtifactIdentity,
    ArtifactLineageKind,
    ArtifactLineageRelation,
    ArtifactLineageRelationIdentity,
    ArtifactLineageSourceIdentity,
    ArtifactManifest,
    ArtifactManifestEntry,
    ArtifactManifestEntryIdentity,
    ArtifactManifestIdentity,
    ArtifactProducerKind,
    ArtifactProducerProvenanceIdentity,
    RepresentedWorkflowProducer,
    ResultArtifactRelationIdentity,
    UnknownLegacyProducer,
)
from ksdft2effmass.workflows.model import WorkflowIdentity, WorkflowRunIdentity

from .resources.qexsd_fixtures import CONTROLLED_QEXSD, QexsdFixtureResources

SUT = QuantumEspressoObservationAdapter
pytestmark = pytest.mark.software_verification


class TestQuantumEspressoObservationAdapter:
    """Own this module's maintained software-verification evidence."""

    @staticmethod
    def document() -> QexsdDocument:
        """Return one mechanically parsed synthetic QEXSD document.

        Evidence ID: Helper owns no identifier.

        Requirement: Support adapter evidence with one deterministic parsed document.

        Method: Parse the maintained synthetic QEXSD bytes through the public parser.

        Oracle: Consuming test methods own all assertions.

        Acceptance: Return one intrinsically valid QexsdDocument.

        Interpretation: Failure blocks the consuming software-verification evidence.

        Limitations: The bytes are synthetic test data, not physical evidence.
        """
        digest, count = QexsdFixtureResources.controlled_source_bytes()
        return QuantumEspressoXsdDocumentParser().execute(
            QexsdSource("/controlled/source.xml", digest, count, CONTROLLED_QEXSD)
        )

    @staticmethod
    def parsed_document(
        document: QexsdDocument,
    ) -> QuantumEspressoParsedDocumentRecord:
        """Return one parser record exactly correlated to the supplied document.

        Evidence ID: Helper owns no identifier.

        Requirement: Support exact parser-record correlation inputs.

        Method: Bind the supplied document to its represented content and parser IDs.

        Oracle: Consuming test methods own all assertions.

        Acceptance: Return one intrinsically valid parsed-document record.

        Interpretation: Failure blocks the consuming software-verification evidence.

        Limitations: Construction does not prove an external parser execution.
        """
        return QuantumEspressoParsedDocumentRecord(
            identity=QuantumEspressoParsedDocumentIdentity(
                "parsed-document.synthetic.qexsd"
            ),
            parser_identity=QuantumEspressoXsdParserIdentity(
                QuantumEspressoObservationAdapter.SUPPORTED_PARSER_IDENTITY
            ),
            parser_version=QuantumEspressoObservationAdapter.SUPPORTED_PARSER_VERSION,
            source_content_identity=ArtifactContentIdentity(
                "sha256", document.source_sha256, document.source_byte_count
            ),
            document=document,
        )

    @staticmethod
    def policy(
        *,
        identity: str = QuantumEspressoObservationAdapter.SUPPORTED_POLICY_IDENTITY,
        version: str = QuantumEspressoObservationAdapter.SUPPORTED_POLICY_VERSION,
    ) -> QuantumEspressoObservationNormalizationPolicy:
        """Return the supported policy identity with one caller-selected version.

        Evidence ID: Helper owns no identifier.

        Requirement: Support explicit policy identity/version test inputs.

        Method: Construct the public immutable policy DataObject.

        Oracle: Consuming test methods own all assertions.

        Acceptance: Return the requested intrinsically valid policy value.

        Interpretation: Failure blocks the consuming software-verification evidence.

        Limitations: Construction alone does not establish adapter support.
        """
        return QuantumEspressoObservationNormalizationPolicy(
            QuantumEspressoObservationNormalizationPolicyIdentity(identity),
            version,
        )

    @staticmethod
    def manifest(
        content: ArtifactContentIdentity,
        *,
        native_format: str = QuantumEspressoObservationAdapter.SUPPORTED_NATIVE_FORMAT,
        semantic_role: str = QuantumEspressoObservationAdapter.SUPPORTED_SEMANTIC_ROLE,
    ) -> ArtifactManifest:
        """Return one synthetic admitted manifest with exact producer correlation.

        Evidence ID: Helper owns no identifier.

        Requirement: Support admitted legacy-lineage artifact test inputs.

        Method: Construct one internally closed immutable synthetic manifest.

        Oracle: Consuming test methods own all assertions.

        Acceptance: Return one manifest containing the selected artifact entry.

        Interpretation: Failure blocks the consuming software-verification evidence.

        Limitations: Unknown-legacy provenance is synthetic and explicitly limited.
        """
        artifact = ArtifactIdentity("artifact.synthetic.qexsd")
        producer = UnknownLegacyProducer(
            ArtifactProducerProvenanceIdentity("producer.synthetic.qexsd"),
            1,
            ArtifactProducerKind.UNKNOWN_LEGACY,
            artifact,
            content,
            ("evidence.synthetic.qexsd",),
            ("claim.synthetic-test-data-only",),
            "synthetic source has no represented Workflow producer",
            ("producer lineage intentionally unavailable",),
            "synthetic_test_data",
        )
        entry = ArtifactManifestEntry(
            ArtifactManifestEntryIdentity("entry.synthetic.qexsd"),
            artifact,
            content,
            native_format,
            semantic_role,
            "retained-software-verification-fixture",
            (),
            "synthetic/qexsd/source.xml",
            (),
            producer,
        )
        return ArtifactManifest(
            ArtifactManifestIdentity("manifest.synthetic.qexsd.r1"),
            1,
            None,
            None,
            WorkflowIdentity("workflow.synthetic.qexsd"),
            WorkflowRunIdentity("workflow-run.synthetic.qexsd"),
            ("evidence.synthetic.qexsd",),
            (entry,),
        )

    @staticmethod
    def represented_manifest(content: ArtifactContentIdentity) -> ArtifactManifest:
        """Return one manifest with exact represented-Workflow producer lineage.

        Evidence ID: Helper owns no identifier.

        Requirement: Support exact represented-Workflow lineage test inputs.

        Method: Construct one closed manifest with required production relations.

        Oracle: Consuming test methods own all assertions.

        Acceptance: Return one intrinsically valid represented-Workflow manifest.

        Interpretation: Failure blocks the consuming software-verification evidence.

        Limitations: All identities and content are synthetic test data.
        """
        artifact = ArtifactIdentity("artifact.represented.qexsd")
        workflow = WorkflowIdentity("workflow.represented.qexsd")
        workflow_run = WorkflowRunIdentity("workflow-run.represented.qexsd")
        task = TaskInstanceIdentity("task.represented.qexsd")
        activation = TaskActivationIdentity("activation.represented.qexsd")
        attempt = AttemptIdentity("attempt.represented.qexsd")
        result_identity = ResultObjectIdentity("result.represented.qe-pw")
        result_artifact_relation = ResultArtifactRelationIdentity(
            "relation.represented.qexsd-result"
        )
        producer = RepresentedWorkflowProducer(
            ArtifactProducerProvenanceIdentity("producer.represented.qexsd"),
            1,
            ArtifactProducerKind.REPRESENTED_WORKFLOW,
            artifact,
            content,
            ("evidence.represented.producer",),
            ("claim.software-correlation-only",),
            workflow,
            workflow_run,
            task,
            activation,
            attempt,
            result_identity,
            result_artifact_relation,
        )
        relations = (
            ArtifactLineageRelation(
                ArtifactLineageRelationIdentity("lineage.1.cpn-selection"),
                ArtifactLineageKind.CPN_SELECTION,
                ArtifactLineageSourceIdentity(activation.value),
                artifact,
                workflow_run,
                attempt,
                ("evidence.represented.cpn",),
                ("claim.software-correlation-only",),
            ),
            ArtifactLineageRelation(
                ArtifactLineageRelationIdentity("lineage.2.result-production"),
                ArtifactLineageKind.RESULT_PRODUCTION,
                ArtifactLineageSourceIdentity(result_artifact_relation.value),
                artifact,
                workflow_run,
                attempt,
                ("evidence.represented.result",),
                ("claim.software-correlation-only",),
            ),
        )
        entry = ArtifactManifestEntry(
            ArtifactManifestEntryIdentity("entry.synthetic.qexsd"),
            artifact,
            content,
            SUT.SUPPORTED_NATIVE_FORMAT,
            SUT.SUPPORTED_SEMANTIC_ROLE,
            "retained-software-verification-fixture",
            (),
            "synthetic/qexsd/source.xml",
            relations,
            producer,
        )
        return ArtifactManifest(
            ArtifactManifestIdentity("manifest.represented.qexsd.r1"),
            1,
            None,
            None,
            workflow,
            workflow_run,
            (
                "evidence.represented.cpn",
                "evidence.represented.producer",
                "evidence.represented.result",
            ),
            (entry,),
        )

    @classmethod
    def request(
        cls,
        *,
        document: QexsdDocument | None = None,
        manifest: ArtifactManifest | None = None,
        entry_identity: ArtifactManifestEntryIdentity | None = None,
        policy: QuantumEspressoObservationNormalizationPolicy | None = None,
    ) -> QuantumEspressoObservationExtractionRequest:
        """Return one exact synthetic first-stage extraction request.

        Evidence ID: Helper owns no identifier.

        Requirement: Support exact first-stage adapter request inputs.

        Method: Compose caller overrides with immutable synthetic defaults.

        Oracle: Consuming test methods own all assertions.

        Acceptance: Return one intrinsically valid extraction request.

        Interpretation: Failure blocks the consuming software-verification evidence.

        Limitations: Defaults represent synthetic test data only.
        """
        selected_document = cls.document() if document is None else document
        selected_manifest = (
            cls.manifest(
                ArtifactContentIdentity(
                    "sha256",
                    selected_document.source_sha256,
                    selected_document.source_byte_count,
                )
            )
            if manifest is None
            else manifest
        )
        return QuantumEspressoObservationExtractionRequest(
            result_identity=ResultObjectIdentity("result.synthetic.qexsd-extraction"),
            parsed_document=cls.parsed_document(selected_document),
            source_manifest=selected_manifest,
            source_manifest_entry_identity=(
                ArtifactManifestEntryIdentity("entry.synthetic.qexsd")
                if entry_identity is None
                else entry_identity
            ),
            normalization_policy=cls.policy() if policy is None else policy,
        )

    def test_method__execute__returns_correlated_neutral_observation(self) -> None:
        """Evidence ID: SV-QE-ADAPT-001

        Requirement: Exact QEXSD bytes and admitted manifest membership produce one
        integration-owned neutral observation with explicit lineage and limitations.

        Acceptance: Result identity, source identities, policy, units, unavailable
        metadata, and canonical limitation values all agree exactly.
        """
        request = self.request()

        result = SUT().execute(request)

        assert type(result) is QuantumEspressoExtractedObservationResult
        assert isinstance(result, ResultObject)
        assert result.identity == request.result_identity
        assert result.source_manifest_identity == request.source_manifest.identity
        assert (
            result.source_manifest_entry_identity
            == request.source_manifest_entry_identity
        )
        assert (
            result.source_content_identity.digest
            == request.parsed_document.document.source_sha256
        )
        assert (
            result.source_content_identity.byte_count
            == request.parsed_document.document.source_byte_count
        )
        assert (
            result.source_producer_provenance_identity
            == request.source_manifest.entries[0].producer_provenance.identity
        )
        assert result.parsed_document_identity == request.parsed_document.identity
        assert result.parser_identity == request.parsed_document.parser_identity
        assert result.parser_version == request.parsed_document.parser_version
        assert result.normalization_policy == request.normalization_policy
        assert result.observation == ConstructQexsdKohnShamPlaneWaveRecord().execute(
            request.parsed_document.document
        )
        assert result.observation.spectrum.eigenvalue_unit is EnergyUnit.HARTREE
        assert (
            result.observation.spectrum.energy_reference_availability
            is Availability.NOT_REPRESENTED
        )
        assert result.limitation_values == SUT.LIMITATION_VALUES

    def test_method__execute__does_not_mutate_inputs_or_result(self) -> None:
        """Evidence ID: SV-QE-ADAPT-002

        Requirement: Adaptation is a pure transformation over immutable input records.

        Acceptance: Inputs remain equal to their snapshots and result mutation fails.
        """
        request = self.request()
        parsed_document_before = deepcopy(request.parsed_document)
        manifest_before = deepcopy(request.source_manifest)

        result = SUT().execute(request)

        assert type(result) is QuantumEspressoExtractedObservationResult
        assert request.parsed_document == parsed_document_before
        assert request.source_manifest == manifest_before
        with pytest.raises(FrozenInstanceError):
            result.identity = ResultObjectIdentity("result.changed")  # type: ignore[misc]

    def test_method__execute__rejects_missing_manifest_entry(self) -> None:
        """Evidence ID: SV-QE-ADAPT-003

        Requirement: A parser result cannot bypass exact manifest-entry admission.

        Acceptance: Unknown entry identity returns SOURCE_ENTRY_NOT_FOUND and no
        partial neutral observation.
        """
        request = self.request(
            entry_identity=ArtifactManifestEntryIdentity("entry.not-present")
        )

        result = SUT().execute(request)
        other_result = SUT().execute(
            replace(
                request,
                result_identity=ResultObjectIdentity(
                    "result.synthetic.qexsd-extraction.other"
                ),
            )
        )

        assert type(result) is QuantumEspressoObservationAdaptationFailure
        assert type(other_result) is QuantumEspressoObservationAdaptationFailure
        assert (
            result.code
            is QuantumEspressoObservationAdaptationFailureCode.SOURCE_ENTRY_NOT_FOUND
        )
        assert result.result_identity == request.result_identity
        assert result.source_manifest_identity == request.source_manifest.identity
        assert (
            result.source_manifest_entry_identity
            == request.source_manifest_entry_identity
        )
        assert result.parsed_document_identity == request.parsed_document.identity
        assert (
            result.source_content_identity
            == request.parsed_document.source_content_identity
        )
        assert result.parser_identity == request.parsed_document.parser_identity
        assert result.parser_version == request.parsed_document.parser_version
        assert result.normalization_policy == request.normalization_policy
        assert result != other_result

    def test_method__execute__rejects_mismatched_source_content(self) -> None:
        """Evidence ID: SV-QE-ADAPT-004

        Requirement: Parsed and admitted artifact byte identities must agree exactly.

        Acceptance: A different SHA-256 identity returns SOURCE_CONTENT_MISMATCH.
        """
        document = self.document()
        manifest = self.manifest(
            ArtifactContentIdentity("sha256", "0" * 64, document.source_byte_count)
        )

        result = SUT().execute(self.request(document=document, manifest=manifest))

        assert type(result) is QuantumEspressoObservationAdaptationFailure
        assert (
            result.code
            is QuantumEspressoObservationAdaptationFailureCode.SOURCE_CONTENT_MISMATCH
        )

    def test_method__execute__rejects_unsupported_native_format(self) -> None:
        """Evidence ID: SV-QE-ADAPT-005

        Requirement: QEXSD semantics cannot be assigned to another declared format.

        Acceptance: A non-QEXSD manifest format returns SOURCE_FORMAT_UNSUPPORTED.
        """
        document = self.document()
        manifest = self.manifest(
            ArtifactContentIdentity(
                "sha256", document.source_sha256, document.source_byte_count
            ),
            native_format="quantum-espresso.stdout-text",
        )

        result = SUT().execute(self.request(document=document, manifest=manifest))

        assert type(result) is QuantumEspressoObservationAdaptationFailure
        assert (
            result.code
            is QuantumEspressoObservationAdaptationFailureCode.SOURCE_FORMAT_UNSUPPORTED
        )

    def test_method__execute__rejects_unsupported_semantic_role(self) -> None:
        """Evidence ID: SV-QE-ADAPT-006

        Requirement: Adaptation requires the admitted artifact's exact QEXSD role.

        Acceptance: An unrelated role returns SOURCE_ROLE_UNSUPPORTED.
        """
        document = self.document()
        manifest = self.manifest(
            ArtifactContentIdentity(
                "sha256", document.source_sha256, document.source_byte_count
            ),
            semantic_role="electronic-structure.standard-output",
        )

        result = SUT().execute(self.request(document=document, manifest=manifest))

        assert type(result) is QuantumEspressoObservationAdaptationFailure
        assert (
            result.code
            is QuantumEspressoObservationAdaptationFailureCode.SOURCE_ROLE_UNSUPPORTED
        )

    @pytest.mark.parametrize(
        ("identity", "version"),
        (
            ("unsupported.policy", SUT.SUPPORTED_POLICY_VERSION),
            (SUT.SUPPORTED_POLICY_IDENTITY, "2"),
        ),
        ids=("identity", "version"),
    )
    def test_method__execute__rejects_unsupported_policy(
        self, identity: str, version: str
    ) -> None:
        """Evidence ID: SV-QE-ADAPT-007

        Requirement: Adaptation uses only an explicit supported policy and version.

        Acceptance: An unrecognized identity or version returns POLICY_UNSUPPORTED
        before output.
        """
        result = SUT().execute(
            self.request(policy=self.policy(identity=identity, version=version))
        )

        assert type(result) is QuantumEspressoObservationAdaptationFailure
        assert (
            result.code
            is QuantumEspressoObservationAdaptationFailureCode.POLICY_UNSUPPORTED
        )

    def test_method__execute__maps_neutral_incompatibility_without_partial_result(
        self,
    ) -> None:
        """Evidence ID: SV-QE-ADAPT-008

        Requirement: Unsupported QEXSD semantics fail as a closed adaptation result.

        Acceptance: An unsupported unit declaration returns OBSERVATION_INCOMPATIBLE
        and contains no neutral observation field.
        """
        document = replace(
            self.document(), declared_unit_system_label="unsupported-unit-system"
        )

        result = SUT().execute(self.request(document=document))

        assert type(result) is QuantumEspressoObservationAdaptationFailure
        assert (
            result.code
            is QuantumEspressoObservationAdaptationFailureCode.OBSERVATION_INCOMPATIBLE
        )
        assert not hasattr(result, "observation")

    def test_method__execute__rejects_mismatched_source_byte_count(self) -> None:
        """Evidence ID: SV-QE-ADAPT-009

        Requirement: Parsed and admitted artifact byte counts must agree exactly.

        Acceptance: A different byte count with the same digest returns
        SOURCE_CONTENT_MISMATCH.
        """
        document = self.document()
        manifest = self.manifest(
            ArtifactContentIdentity(
                "sha256", document.source_sha256, document.source_byte_count + 1
            )
        )

        result = SUT().execute(self.request(document=document, manifest=manifest))

        assert type(result) is QuantumEspressoObservationAdaptationFailure
        assert (
            result.code
            is QuantumEspressoObservationAdaptationFailureCode.SOURCE_CONTENT_MISMATCH
        )

    @pytest.mark.parametrize(
        ("identity", "version"),
        (
            ("unsupported.qexsd-parser", SUT.SUPPORTED_PARSER_VERSION),
            (SUT.SUPPORTED_PARSER_IDENTITY, "2"),
        ),
        ids=("identity", "version"),
    )
    def test_method__execute__rejects_unsupported_parser(
        self, identity: str, version: str
    ) -> None:
        """Evidence ID: SV-QE-ADAPT-011

        Requirement: The adapter accepts only its explicit parser identity and version.

        Acceptance: An unrecognized identity or version returns PARSER_UNSUPPORTED.
        """
        request = self.request()
        request = replace(
            request,
            parsed_document=replace(
                request.parsed_document,
                parser_identity=QuantumEspressoXsdParserIdentity(identity),
                parser_version=version,
            ),
        )

        result = SUT().execute(request)

        assert type(result) is QuantumEspressoObservationAdaptationFailure
        assert (
            result.code
            is QuantumEspressoObservationAdaptationFailureCode.PARSER_UNSUPPORTED
        )
        assert result.result_identity == request.result_identity
        assert result.parsed_document_identity == request.parsed_document.identity
        assert result.parser_identity == request.parsed_document.parser_identity
        assert result.parser_version == request.parsed_document.parser_version

    def test_method__execute__retains_represented_workflow_lineage_references(
        self,
    ) -> None:
        """Evidence ID: SV-QE-ADAPT-012

        Requirement: First-stage output preserves exact references to a represented
        Workflow artifact manifest and producer provenance.

        Acceptance: Manifest, entry, artifact, content, and producer identities agree
        with the represented-Workflow entry exactly.
        """
        document = self.document()
        manifest = self.represented_manifest(
            ArtifactContentIdentity(
                "sha256", document.source_sha256, document.source_byte_count
            )
        )

        result = SUT().execute(self.request(document=document, manifest=manifest))

        assert type(result) is QuantumEspressoExtractedObservationResult
        entry = manifest.entries[0]
        assert type(entry.producer_provenance) is RepresentedWorkflowProducer
        assert result.source_manifest_identity == manifest.identity
        assert result.source_manifest_entry_identity == entry.identity
        assert result.source_artifact_identity == entry.artifact_identity
        assert result.source_content_identity == entry.content_identity
        assert (
            result.source_producer_provenance_identity
            == entry.producer_provenance.identity
        )

    def test_method__execute__rejects_wrong_request_type(self) -> None:
        """Evidence ID: SV-QE-ADAPT-013

        Requirement: The public ActionObject accepts only its exact request DataObject.

        Acceptance: A raw parsed document raises TypeError at the call boundary.
        """
        with pytest.raises(TypeError):
            SUT().execute(self.document())  # type: ignore[arg-type]
