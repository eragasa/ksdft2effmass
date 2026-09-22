r"""Software verification of ``NormalizedObservationAssembler``.

Evidence profile: routine

Bounded artifact scope: Workflow-owned normalized-observation assembly.

Facet and represented meaning

The ActionObject consumes exact immutable extracted Kohn--Sham ResultObjects through a
calculator-independent protocol and returns one Workflow-owned set or closed failure.

Intrinsic and cross-object scope

The evidence covers structural conformance of the accepted QE extraction result,
identity and membership correlation, output/source identity separation, exact source
retention, order, nonmutation, closed empty, malformed-policy, and duplicate-source
failures, public imports, and dependency direction.

VVUQ and scientific exclusions

All QEXSD bytes and identities are synthetic test data. Assembly establishes software
verification only, not parsing provenance, numerical verification, scientific
validation, UQ, physical correctness, convergence, or acceptance.
"""

import ast
import hashlib
import importlib.util
from copy import deepcopy
from dataclasses import FrozenInstanceError, dataclass, replace
from pathlib import Path

import pytest

import ksdft2effmass.workflows as workflows
import ksdft2effmass.workflows.observations as workflow_observations
from ksdft2effmass.integration.quantum_espresso import (
    QuantumEspressoExtractedObservationResult,
    QuantumEspressoObservationAdapter,
    QuantumEspressoObservationExtractionRequest,
    QuantumEspressoObservationNormalizationPolicy,
    QuantumEspressoObservationNormalizationPolicyIdentity,
    QuantumEspressoParsedDocumentIdentity,
    QuantumEspressoParsedDocumentRecord,
    QuantumEspressoXsdParserIdentity,
)
from ksdft2effmass.integration.quantum_espresso.qexsd import (
    QexsdSource,
    QuantumEspressoXsdDocumentParser,
)
from ksdft2effmass.ksdft.pw import KohnShamPlaneWaveCalculationRecord
from ksdft2effmass.workflows import (
    NormalizedObservationAssembler,
    NormalizedObservationAssemblyFailure,
    NormalizedObservationAssemblyFailureCode,
    NormalizedObservationAssemblyRequest,
    NormalizedObservationAssemblyResult,
    NormalizedObservationSet,
    NormalizedObservationSource,
    ObservationCorrelationIdentity,
    ObservationNormalizationPolicySource,
    ResultObject,
    ResultObjectIdentity,
)
from ksdft2effmass.workflows.artifacts import (
    ArtifactContentIdentity,
    ArtifactIdentity,
    ArtifactManifest,
    ArtifactManifestEntry,
    ArtifactManifestEntryIdentity,
    ArtifactManifestIdentity,
    ArtifactProducerKind,
    ArtifactProducerProvenanceIdentity,
    UnknownLegacyProducer,
)
from ksdft2effmass.workflows.model import WorkflowIdentity, WorkflowRunIdentity

SUT = NormalizedObservationAssembler
pytestmark = pytest.mark.software_verification


class TestNormalizedObservationAssembler:
    """Own this module's maintained software-verification evidence."""

    @dataclass(frozen=True, slots=True)
    class SyntheticNormalizedObservationSource:
        """Represent an immutable source with selected negative-test fields."""

        identity: ResultObjectIdentity
        observation: KohnShamPlaneWaveCalculationRecord
        source_manifest_identity: ArtifactManifestIdentity
        source_manifest_entry_identity: ArtifactManifestEntryIdentity
        source_artifact_identity: ArtifactIdentity
        source_content_identity: ArtifactContentIdentity
        source_producer_provenance_identity: ArtifactProducerProvenanceIdentity
        parsed_document_identity: QuantumEspressoParsedDocumentIdentity
        parser_identity: QuantumEspressoXsdParserIdentity
        parser_version: str
        normalization_policy: ObservationNormalizationPolicySource
        limitation_values: tuple[str, ...]

    @dataclass(frozen=True, slots=True)
    class SyntheticMalformedNormalizationPolicy:
        """Represent a structurally present but wrongly typed policy identity."""

        identity: int
        version: str

    @staticmethod
    def source(suffix: str = "one") -> QuantumEspressoExtractedObservationResult:
        """Return one exact synthetic integration-owned extracted observation.

        Evidence ID: Helper owns no identifier.

        Requirement: Support Workflow assembly with one real structural source.

        Method: Parse maintained synthetic QEXSD bytes and execute the public adapter.

        Oracle: Consuming test methods own all assertions.

        Acceptance: Return one successful immutable QE extraction result.

        Interpretation: Failure blocks the consuming software-verification evidence.

        Limitations: The source bytes and all identities are synthetic test data.
        """
        fixture_path = (
            Path(__file__).parents[1]
            / "integration/quantum_espresso/resources/qexsd/qexsd-23.03.10.xml"
        )
        fixture_bytes = fixture_path.read_bytes()
        digest = hashlib.sha256(fixture_bytes).hexdigest()
        document = QuantumEspressoXsdDocumentParser().execute(
            QexsdSource(
                "/controlled/source.xml",
                digest,
                len(fixture_bytes),
                fixture_bytes,
            )
        )
        content = ArtifactContentIdentity(
            "sha256", document.source_sha256, document.source_byte_count
        )
        artifact = ArtifactIdentity(f"artifact.synthetic.qexsd.{suffix}")
        producer = UnknownLegacyProducer(
            ArtifactProducerProvenanceIdentity(f"producer.synthetic.qexsd.{suffix}"),
            1,
            ArtifactProducerKind.UNKNOWN_LEGACY,
            artifact,
            content,
            (f"evidence.synthetic.qexsd.{suffix}",),
            ("claim.synthetic-test-data-only",),
            "synthetic source has no represented Workflow producer",
            ("producer lineage intentionally unavailable",),
            "synthetic_test_data",
        )
        entry_identity = ArtifactManifestEntryIdentity(
            f"entry.synthetic.qexsd.{suffix}"
        )
        manifest = ArtifactManifest(
            ArtifactManifestIdentity(f"manifest.synthetic.qexsd.{suffix}.r1"),
            1,
            None,
            None,
            WorkflowIdentity("workflow.synthetic.qexsd"),
            WorkflowRunIdentity("workflow-run.synthetic.qexsd"),
            (f"evidence.synthetic.qexsd.{suffix}",),
            (
                ArtifactManifestEntry(
                    entry_identity,
                    artifact,
                    content,
                    QuantumEspressoObservationAdapter.SUPPORTED_NATIVE_FORMAT,
                    QuantumEspressoObservationAdapter.SUPPORTED_SEMANTIC_ROLE,
                    "retained-software-verification-fixture",
                    (),
                    f"synthetic/qexsd/{suffix}.xml",
                    (),
                    producer,
                ),
            ),
        )
        parsed_document = QuantumEspressoParsedDocumentRecord(
            identity=QuantumEspressoParsedDocumentIdentity(
                f"parsed-document.synthetic.qexsd.{suffix}"
            ),
            parser_identity=QuantumEspressoXsdParserIdentity(
                QuantumEspressoObservationAdapter.SUPPORTED_PARSER_IDENTITY
            ),
            parser_version=QuantumEspressoObservationAdapter.SUPPORTED_PARSER_VERSION,
            source_content_identity=content,
            document=document,
        )
        request = QuantumEspressoObservationExtractionRequest(
            result_identity=ResultObjectIdentity(
                f"result.synthetic.qexsd-extraction.{suffix}"
            ),
            parsed_document=parsed_document,
            source_manifest=manifest,
            source_manifest_entry_identity=entry_identity,
            normalization_policy=QuantumEspressoObservationNormalizationPolicy(
                QuantumEspressoObservationNormalizationPolicyIdentity(
                    QuantumEspressoObservationAdapter.SUPPORTED_POLICY_IDENTITY
                ),
                QuantumEspressoObservationAdapter.SUPPORTED_POLICY_VERSION,
            ),
        )
        result = QuantumEspressoObservationAdapter().execute(request)
        if type(result) is not QuantumEspressoExtractedObservationResult:
            raise AssertionError("synthetic extraction source must succeed")
        return result

    @staticmethod
    def request(
        sources: tuple[NormalizedObservationSource, ...],
    ) -> NormalizedObservationAssemblyRequest:
        """Return one exact assembly request for supplied immutable sources.

        Evidence ID: Helper owns no identifier.

        Requirement: Support explicit source-membership assembly cases.

        Method: Bind sources to one deterministic reserved result identity.

        Oracle: Consuming test methods own all assertions.

        Acceptance: Return one intrinsically valid assembly request.

        Interpretation: Failure blocks the consuming software-verification evidence.

        Limitations: Construction alone establishes no source correlation.
        """
        return NormalizedObservationAssemblyRequest(
            result_identity=ResultObjectIdentity(
                "result.synthetic.normalized-observation-set"
            ),
            sources=sources,
        )

    def test_method__execute__retains_exact_source_in_workflow_result(self) -> None:
        """Evidence ID: SV-WNO-001

        Requirement: One structurally conforming extracted ResultObject produces one
        Workflow ResultObject retaining that exact immutable source.

        Acceptance: The result identity and source object agree by identity and value,
        and both public structural protocols are satisfied.
        """
        source: NormalizedObservationSource = self.source()
        request = self.request((source,))

        result = SUT().execute(request)

        assert type(result) is NormalizedObservationSet
        assert isinstance(result, ResultObject)
        assert result.identity == request.result_identity
        assert result.sources == (source,)
        assert result.sources[0] is source

    def test_method__execute__preserves_distinct_source_order(self) -> None:
        """Evidence ID: SV-WNO-002

        Requirement: Assembly preserves caller-declared order for distinct sources.

        Acceptance: Two exact sources remain in the original tuple order.
        """
        first: NormalizedObservationSource = self.source("first")
        second: NormalizedObservationSource = self.source("second")

        result = SUT().execute(self.request((second, first)))

        assert type(result) is NormalizedObservationSet
        assert result.sources == (second, first)

    def test_method__execute__returns_closed_empty_source_failure(self) -> None:
        """Evidence ID: SV-WNO-003

        Requirement: An empty request cannot create a normalized observation set.

        Acceptance: NO_SOURCES retains the exact request and exposes no partial set.
        """
        request = self.request(())

        result = SUT().execute(request)

        assert type(result) is NormalizedObservationAssemblyFailure
        assert result.code is NormalizedObservationAssemblyFailureCode.NO_SOURCES
        assert result.request is request
        assert not hasattr(result, "sources")

    def test_method__execute__rejects_duplicate_source_result_identity(self) -> None:
        """Evidence ID: SV-WNO-004

        Requirement: One source ResultObject identity occurs at most once in a set.

        Acceptance: Duplicate result identity returns SOURCE_SET_INVALID and retains
        both exact requested sources.
        """
        first = self.source("first")
        second = replace(self.source("second"), identity=first.identity)
        request = self.request((first, second))

        result = SUT().execute(request)

        assert type(result) is NormalizedObservationAssemblyFailure
        assert (
            result.code is NormalizedObservationAssemblyFailureCode.SOURCE_SET_INVALID
        )
        assert result.request is request
        assert result.request.sources == (first, second)

    def test_method__execute__rejects_output_identity_matching_source(self) -> None:
        """Evidence ID: SV-WNO-012

        Requirement: A new Workflow result cannot reuse a retained source identity.

        Acceptance: An output/source identity collision returns SOURCE_SET_INVALID,
        retains the exact request, and exposes no partial set.
        """
        source = self.source()
        request = NormalizedObservationAssemblyRequest(
            result_identity=source.identity,
            sources=(source,),
        )

        result = SUT().execute(request)

        assert type(result) is NormalizedObservationAssemblyFailure
        assert (
            result.code is NormalizedObservationAssemblyFailureCode.SOURCE_SET_INVALID
        )
        assert result.request is request
        assert not hasattr(result, "sources")

    def test_method__execute__rejects_duplicate_manifest_entry_reference(self) -> None:
        """Evidence ID: SV-WNO-005

        Requirement: One exact manifest-revision/entry pair occurs at most once.

        Acceptance: A duplicate manifest and entry pair returns SOURCE_SET_INVALID
        without a partial set.
        """
        first = self.source("first")
        second = replace(
            self.source("second"),
            source_manifest_identity=first.source_manifest_identity,
            source_manifest_entry_identity=first.source_manifest_entry_identity,
        )

        result = SUT().execute(self.request((first, second)))

        assert type(result) is NormalizedObservationAssemblyFailure
        assert (
            result.code is NormalizedObservationAssemblyFailureCode.SOURCE_SET_INVALID
        )
        assert not hasattr(result, "sources")

    def test_method__execute__allows_entry_identity_in_distinct_manifests(self) -> None:
        """Evidence ID: SV-WNO-011

        Requirement: Manifest-entry identity is scoped by its manifest revision.

        Acceptance: Equal entry identities under different manifests remain distinct
        admissible source references.
        """
        first = self.source("first")
        second = replace(
            self.source("second"),
            source_manifest_entry_identity=first.source_manifest_entry_identity,
        )

        result = SUT().execute(self.request((first, second)))

        assert type(result) is NormalizedObservationSet
        assert result.sources == (first, second)

    def test_method__execute__rejects_mismatched_neutral_provenance(self) -> None:
        """Evidence ID: SV-WNO-010

        Requirement: A source neutral record must agree with represented source bytes.

        Acceptance: A different observation digest returns SOURCE_SET_INVALID while
        retaining the exact request and no partial set.
        """
        source = self.source()
        invalid_source = self.SyntheticNormalizedObservationSource(
            identity=source.identity,
            observation=replace(
                source.observation,
                provenance=replace(
                    source.observation.provenance,
                    source_sha256="0" * 64,
                ),
            ),
            source_manifest_identity=source.source_manifest_identity,
            source_manifest_entry_identity=source.source_manifest_entry_identity,
            source_artifact_identity=source.source_artifact_identity,
            source_content_identity=source.source_content_identity,
            source_producer_provenance_identity=(
                source.source_producer_provenance_identity
            ),
            parsed_document_identity=source.parsed_document_identity,
            parser_identity=source.parser_identity,
            parser_version=source.parser_version,
            normalization_policy=source.normalization_policy,
            limitation_values=source.limitation_values,
        )
        request = self.request((invalid_source,))

        result = SUT().execute(request)

        assert type(result) is NormalizedObservationAssemblyFailure
        assert (
            result.code is NormalizedObservationAssemblyFailureCode.SOURCE_SET_INVALID
        )
        assert result.request is request
        assert not hasattr(result, "sources")

    def test_method__execute__closes_malformed_policy_identity_as_failure(self) -> None:
        """Evidence ID: SV-WNO-013

        Requirement: A structurally present policy with a wrongly typed identity does
        not escape the closed assembly-result boundary.

        Acceptance: The malformed nested identity returns SOURCE_SET_INVALID with the
        exact request and no partial set.
        """
        source = self.source()
        invalid_source = self.SyntheticNormalizedObservationSource(
            identity=source.identity,
            observation=source.observation,
            source_manifest_identity=source.source_manifest_identity,
            source_manifest_entry_identity=source.source_manifest_entry_identity,
            source_artifact_identity=source.source_artifact_identity,
            source_content_identity=source.source_content_identity,
            source_producer_provenance_identity=(
                source.source_producer_provenance_identity
            ),
            parsed_document_identity=source.parsed_document_identity,
            parser_identity=source.parser_identity,
            parser_version=source.parser_version,
            normalization_policy=self.SyntheticMalformedNormalizationPolicy(
                identity=7,
                version="1",
            ),  # type: ignore[arg-type]
            limitation_values=source.limitation_values,
        )
        request = self.request((invalid_source,))

        result = SUT().execute(request)

        assert type(result) is NormalizedObservationAssemblyFailure
        assert (
            result.code is NormalizedObservationAssemblyFailureCode.SOURCE_SET_INVALID
        )
        assert result.request is request
        assert not hasattr(result, "sources")

    def test_method__execute__does_not_mutate_sources_and_returns_frozen_set(
        self,
    ) -> None:
        """Evidence ID: SV-WNO-006

        Requirement: Assembly is pure and its Workflow result is immutable.

        Acceptance: The source remains equal to its snapshot and set mutation fails.
        """
        source = self.source()
        source_before = deepcopy(source)
        result = SUT().execute(self.request((source,)))

        assert type(result) is NormalizedObservationSet
        assert source == source_before
        with pytest.raises(FrozenInstanceError):
            result.identity = ResultObjectIdentity("result.changed")  # type: ignore[misc]

    def test_method__execute__rejects_wrong_request_type(self) -> None:
        """Evidence ID: SV-WNO-007

        Requirement: The public ActionObject accepts only its exact request DataObject.

        Acceptance: A raw source tuple raises TypeError at the call boundary.
        """
        with pytest.raises(TypeError):
            SUT().execute((self.source(),))  # type: ignore[arg-type]

    def test_public_api__package__exports_normalized_observation_contract(self) -> None:
        """Evidence ID: SV-WNO-008

        Requirement: Workflow publishes the complete selected normalization contract.

        Acceptance: Every required public name resolves to its documented object.
        """
        expected = {
            "NormalizedObservationAssembler": NormalizedObservationAssembler,
            "NormalizedObservationAssemblyFailure": (
                NormalizedObservationAssemblyFailure
            ),
            "NormalizedObservationAssemblyFailureCode": (
                NormalizedObservationAssemblyFailureCode
            ),
            "NormalizedObservationAssemblyRequest": (
                NormalizedObservationAssemblyRequest
            ),
            "NormalizedObservationAssemblyResult": (
                NormalizedObservationAssemblyResult
            ),
            "NormalizedObservationSet": NormalizedObservationSet,
            "NormalizedObservationSource": NormalizedObservationSource,
            "ObservationCorrelationIdentity": ObservationCorrelationIdentity,
            "ObservationNormalizationPolicySource": (
                ObservationNormalizationPolicySource
            ),
        }

        assert {name: getattr(workflows, name) for name in expected} == expected
        assert set(expected) <= set(workflows.__all__)

    def test_artifact__dependency__does_not_import_calculator_packages(self) -> None:
        """Evidence ID: SV-WNO-009

        Requirement: The Workflow implementation imports no calculator or concrete
        integration package.

        Acceptance: Parsed import statements contain no integration or calculator
        package reference.
        """
        source_path = Path(workflow_observations.__file__)
        syntax = ast.parse(source_path.read_text(encoding="utf-8"))
        package_name = workflow_observations.__package__
        if package_name is None:
            raise AssertionError("Workflow observation module must have a package")
        imported_modules = tuple(
            alias.name
            for node in ast.walk(syntax)
            if isinstance(node, ast.Import)
            for alias in node.names
        ) + tuple(
            f"{resolved_module}.{alias.name}"
            for node in ast.walk(syntax)
            if isinstance(node, ast.ImportFrom)
            for resolved_module in (
                importlib.util.resolve_name(
                    f"{'.' * node.level}{node.module or ''}", package_name
                )
                if node.level
                else (node.module or ""),
            )
            for alias in node.names
        )

        assert not any(
            module.startswith(
                ("ksdft2effmass.calculators", "ksdft2effmass.integration")
            )
            for module in imported_modules
        )
