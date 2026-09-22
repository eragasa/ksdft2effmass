"""Two-stage QE observation adaptation: integration-owned extraction stage.

This module owns the first stage selected by the human-resolved Option C architecture.
It correlates one mechanically parsed QEXSD document with one exact Workflow artifact
manifest entry and constructs the retained neutral plane-wave Kohn--Sham observation.
A separately authorized Workflow owner must assemble a Workflow-owned normalized
observation set; this module neither defines nor fabricates that second-stage result.

The records and action perform no filesystem access, parsing, execution, persistence,
scientific acceptance, numerical validation, or uncertainty quantification.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from ksdft2effmass.ksdft import Availability
from ksdft2effmass.ksdft.pw import KohnShamPlaneWaveCalculationRecord
from ksdft2effmass.workflows import ResultObjectIdentity
from ksdft2effmass.workflows.artifacts import (
    ArtifactContentIdentity,
    ArtifactIdentity,
    ArtifactManifest,
    ArtifactManifestEntryIdentity,
    ArtifactManifestIdentity,
    ArtifactProducerProvenanceIdentity,
)

from .qexsd import ConstructQexsdKohnShamPlaneWaveRecord, QexsdDocument

_SUPPORTED_NATIVE_FORMAT = "quantum-espresso.qexsd"
_SUPPORTED_SEMANTIC_ROLE = "electronic-structure.qexsd-native-output"
_SUPPORTED_POLICY_IDENTITY = (
    "ksdft2effmass.quantum-espresso.qexsd-plane-wave-observation"
)
_SUPPORTED_POLICY_VERSION = "1"
_SUPPORTED_PARSER_IDENTITY = "ksdft2effmass.quantum-espresso.qexsd-parser"
_SUPPORTED_PARSER_VERSION = "1"
_LIMITATION_VALUES = (
    "basis_identity.not_represented",
    "energy_reference.not_represented",
    "gauge.not_represented",
    "phase_convention.not_represented",
    "retained_subspace.no_retained_subspace",
    "spin_resolved_arrays.not_represented",
)


@dataclass(frozen=True, slots=True)
class QuantumEspressoParsedDocumentIdentity:
    """Nominal identity of one mechanically parsed QE-native document.

    Parameters
    ----------
    value
        Nonempty integration-owned identity. It is not a path, content digest,
        parser-version claim, or assertion that parsing was scientifically valid.
    """

    value: str

    def __post_init__(self) -> None:
        """Validate the exact identity value."""
        if type(self.value) is not str:
            raise TypeError("parsed document identity value must be a built-in str")
        if not self.value:
            raise ValueError("parsed document identity value must not be empty")


@dataclass(frozen=True, slots=True)
class QuantumEspressoXsdParserIdentity:
    """Nominal identity of one QEXSD parser implementation family.

    Parameters
    ----------
    value
        Nonempty integration-owned identity. The separately represented parser version
        selects one implementation revision within this family.
    """

    value: str

    def __post_init__(self) -> None:
        """Validate the exact identity value."""
        if type(self.value) is not str:
            raise TypeError("QEXSD parser identity value must be a built-in str")
        if not self.value:
            raise ValueError("QEXSD parser identity value must not be empty")


@dataclass(frozen=True, slots=True, kw_only=True)
class QuantumEspressoParsedDocumentRecord:
    """Bind one parsed QEXSD document to parser and source-content identity.

    Parameters
    ----------
    identity
        Exact identity of this mechanically parsed document record.
    parser_identity, parser_version
        Exact integration-owned parser implementation family and version.
    source_content_identity
        SHA-256 and byte count of the bytes supplied to the parser.
    document
        Mechanically faithful QEXSD document whose source fields must equal the
        supplied content identity.

    Notes
    -----
    This correlation record does not parse bytes, prove external identity existence,
    or establish scientific validity.
    """

    identity: QuantumEspressoParsedDocumentIdentity
    parser_identity: QuantumEspressoXsdParserIdentity
    parser_version: str
    source_content_identity: ArtifactContentIdentity
    document: QexsdDocument

    def __post_init__(self) -> None:
        """Validate exact parser, source-content, and document correlation."""
        if type(self.identity) is not QuantumEspressoParsedDocumentIdentity:
            raise TypeError("identity must be QuantumEspressoParsedDocumentIdentity")
        if type(self.parser_identity) is not QuantumEspressoXsdParserIdentity:
            raise TypeError("parser_identity must be QuantumEspressoXsdParserIdentity")
        if type(self.parser_version) is not str:
            raise TypeError("parser_version must be a built-in str")
        if not self.parser_version:
            raise ValueError("parser_version must not be empty")
        if type(self.source_content_identity) is not ArtifactContentIdentity:
            raise TypeError("source_content_identity must be ArtifactContentIdentity")
        if type(self.document) is not QexsdDocument:
            raise TypeError("document must be QexsdDocument")
        if (
            self.source_content_identity.digest != self.document.source_sha256
            or self.source_content_identity.byte_count
            != self.document.source_byte_count
        ):
            raise ValueError(
                "parsed document source must equal parser source content identity"
            )


@dataclass(frozen=True, slots=True)
class QuantumEspressoObservationNormalizationPolicyIdentity:
    """Nominal identity of one QE observation-normalization policy family.

    Parameters
    ----------
    value
        Nonempty integration-owned identity. It does not itself select or execute a
        policy version.
    """

    value: str

    def __post_init__(self) -> None:
        """Validate the exact identity value."""
        if type(self.value) is not str:
            raise TypeError(
                "observation normalization policy identity value must be a built-in str"
            )
        if not self.value:
            raise ValueError(
                "observation normalization policy identity value must not be empty"
            )


@dataclass(frozen=True, slots=True)
class QuantumEspressoObservationNormalizationPolicy:
    """Identify the exact integration-owned normalization policy and version.

    Parameters
    ----------
    identity
        Nominal integration-owned policy-family identity.
    version
        Nonempty owner-local version. The current adapter accepts only its documented
        schema-version-1 QEXSD plane-wave policy.
    """

    identity: QuantumEspressoObservationNormalizationPolicyIdentity
    version: str

    def __post_init__(self) -> None:
        """Validate exact policy identity and version types."""
        if (
            type(self.identity)
            is not QuantumEspressoObservationNormalizationPolicyIdentity
        ):
            raise TypeError(
                "identity must be QuantumEspressoObservationNormalizationPolicyIdentity"
            )
        if type(self.version) is not str:
            raise TypeError("normalization policy version must be a built-in str")
        if not self.version:
            raise ValueError("normalization policy version must not be empty")


@dataclass(frozen=True, slots=True, kw_only=True)
class QuantumEspressoObservationExtractionRequest:
    """Bind one parsed QEXSD document to admitted Workflow artifact lineage.

    Parameters
    ----------
    result_identity
        Identity reserved by the caller for the intended extracted-observation result
        and retained by every expected failure for exact correlation.
    parsed_document
        Mechanically faithful QEXSD document bound to exact parser implementation,
        parser version, and source-content identities.
    source_manifest
        Exact immutable Workflow artifact-manifest revision admitting the native bytes.
    source_manifest_entry_identity
        Exact entry expected to identify the QEXSD source bytes.
    normalization_policy
        Explicit normalization policy and version requested for the extraction.

    Notes
    -----
    Construction validates local types only. Manifest membership, byte identity,
    native format, policy support, and neutral semantic construction are owned by
    :class:`QuantumEspressoObservationAdapter`.
    """

    result_identity: ResultObjectIdentity
    parsed_document: QuantumEspressoParsedDocumentRecord
    source_manifest: ArtifactManifest
    source_manifest_entry_identity: ArtifactManifestEntryIdentity
    normalization_policy: QuantumEspressoObservationNormalizationPolicy

    def __post_init__(self) -> None:
        """Validate the exact request boundary types."""
        if type(self.result_identity) is not ResultObjectIdentity:
            raise TypeError("result_identity must be ResultObjectIdentity")
        if type(self.parsed_document) is not QuantumEspressoParsedDocumentRecord:
            raise TypeError(
                "parsed_document must be QuantumEspressoParsedDocumentRecord"
            )
        if type(self.source_manifest) is not ArtifactManifest:
            raise TypeError("source_manifest must be ArtifactManifest")
        if (
            type(self.source_manifest_entry_identity)
            is not ArtifactManifestEntryIdentity
        ):
            raise TypeError(
                "source_manifest_entry_identity must be ArtifactManifestEntryIdentity"
            )
        if (
            type(self.normalization_policy)
            is not QuantumEspressoObservationNormalizationPolicy
        ):
            raise TypeError(
                "normalization_policy must be "
                "QuantumEspressoObservationNormalizationPolicy"
            )


@dataclass(frozen=True, slots=True, kw_only=True)
class QuantumEspressoExtractedObservationResult:
    """One integration-owned neutral observation with exact source correlation.

    Attributes
    ----------
    identity
        Exact Workflow-facing identity of this first-stage result.
    observation
        Retained schema-version-1 neutral plane-wave Kohn--Sham record.
    source_manifest_identity, source_manifest_entry_identity
        Exact Workflow manifest revision and entry admitting the source artifact.
    source_artifact_identity, source_content_identity
        Nominal artifact and exact SHA-256/byte-count source identities.
    source_producer_provenance_identity
        Exact producer-provenance record identity retained by the manifest entry.
    parsed_document_identity
        Exact integration-owned parsed-document record identity.
    parser_identity, parser_version
        Exact QEXSD parser implementation family and version bound by that record.
    normalization_policy
        Explicit policy and version applied by the adapter.
    limitation_values
        Canonically ordered explicit limitations of the retained neutral observation.

    Notes
    -----
    This is a concrete Workflow ``ResultObject`` by structural conformance. It is not
    the Workflow-owned normalized-observation set selected as Option C's second stage.
    Exact construction establishes software-contract agreement only.
    """

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
    normalization_policy: QuantumEspressoObservationNormalizationPolicy
    limitation_values: tuple[str, ...]

    def __post_init__(self) -> None:
        """Validate result types, source agreement, and canonical limitations."""
        if type(self.identity) is not ResultObjectIdentity:
            raise TypeError("identity must be ResultObjectIdentity")
        if type(self.observation) is not KohnShamPlaneWaveCalculationRecord:
            raise TypeError("observation must be KohnShamPlaneWaveCalculationRecord")
        if type(self.source_manifest_identity) is not ArtifactManifestIdentity:
            raise TypeError("source_manifest_identity must be ArtifactManifestIdentity")
        if (
            type(self.source_manifest_entry_identity)
            is not ArtifactManifestEntryIdentity
        ):
            raise TypeError(
                "source_manifest_entry_identity must be ArtifactManifestEntryIdentity"
            )
        if type(self.source_artifact_identity) is not ArtifactIdentity:
            raise TypeError("source_artifact_identity must be ArtifactIdentity")
        if type(self.source_content_identity) is not ArtifactContentIdentity:
            raise TypeError("source_content_identity must be ArtifactContentIdentity")
        if (
            type(self.source_producer_provenance_identity)
            is not ArtifactProducerProvenanceIdentity
        ):
            raise TypeError(
                "source_producer_provenance_identity must be "
                "ArtifactProducerProvenanceIdentity"
            )
        if (
            type(self.parsed_document_identity)
            is not QuantumEspressoParsedDocumentIdentity
        ):
            raise TypeError(
                "parsed_document_identity must be QuantumEspressoParsedDocumentIdentity"
            )
        if type(self.parser_identity) is not QuantumEspressoXsdParserIdentity:
            raise TypeError("parser_identity must be QuantumEspressoXsdParserIdentity")
        if type(self.parser_version) is not str:
            raise TypeError("parser_version must be a built-in str")
        if not self.parser_version:
            raise ValueError("parser_version must not be empty")
        if (
            type(self.normalization_policy)
            is not QuantumEspressoObservationNormalizationPolicy
        ):
            raise TypeError(
                "normalization_policy must be "
                "QuantumEspressoObservationNormalizationPolicy"
            )
        if type(self.limitation_values) is not tuple:
            raise TypeError("limitation_values must be a built-in tuple")
        if not self.limitation_values or any(
            type(value) is not str or not value for value in self.limitation_values
        ):
            raise ValueError("limitation_values must contain nonempty built-in strings")
        if self.limitation_values != tuple(sorted(set(self.limitation_values))):
            raise ValueError("limitation_values must be unique and lexically sorted")
        if self.limitation_values != _LIMITATION_VALUES:
            raise ValueError(
                "limitation_values must equal the supported extraction limitations"
            )
        if (
            self.normalization_policy.identity.value != _SUPPORTED_POLICY_IDENTITY
            or self.normalization_policy.version != _SUPPORTED_POLICY_VERSION
        ):
            raise ValueError("normalization_policy must equal the supported policy")
        if (
            self.parser_identity.value != _SUPPORTED_PARSER_IDENTITY
            or self.parser_version != _SUPPORTED_PARSER_VERSION
        ):
            raise ValueError(
                "parser identity and version must equal the supported parser"
            )
        if (
            self.observation.spectrum.energy_reference_availability
            is not Availability.NOT_REPRESENTED
            or self.observation.total_energy.reference_availability
            is not Availability.NOT_REPRESENTED
            or self.observation.spectrum.spin_channel_availability
            is not Availability.NO_SPIN_RESOLVED_ARRAYS
        ):
            raise ValueError(
                "neutral observation availability must agree with limitations"
            )
        provenance = self.observation.provenance
        if (
            provenance.source_sha256 != self.source_content_identity.digest
            or provenance.source_byte_count != self.source_content_identity.byte_count
        ):
            raise ValueError(
                "neutral observation provenance must equal source content identity"
            )
        if provenance.source_format != "QEXSD":
            raise ValueError(
                "neutral observation provenance source format must be QEXSD"
            )


class QuantumEspressoObservationAdaptationFailureCode(StrEnum):
    """Closed expected failure classification for first-stage adaptation.

    Attributes
    ----------
    POLICY_UNSUPPORTED
        Requested normalization policy identity or version is unsupported.
    PARSER_UNSUPPORTED
        Parsed-document parser identity or version is unsupported.
    SOURCE_ENTRY_NOT_FOUND
        Selected manifest entry is absent.
    SOURCE_FORMAT_UNSUPPORTED
        Selected entry does not declare the supported QEXSD native format.
    SOURCE_ROLE_UNSUPPORTED
        Selected entry does not declare the supported QEXSD semantic role.
    SOURCE_CONTENT_MISMATCH
        Parsed-document and manifest-entry content identities disagree.
    OBSERVATION_INCOMPATIBLE
        Parsed values cannot construct the retained neutral observation contract.
    """

    POLICY_UNSUPPORTED = "policy_unsupported"
    PARSER_UNSUPPORTED = "parser_unsupported"
    SOURCE_ENTRY_NOT_FOUND = "source_entry_not_found"
    SOURCE_FORMAT_UNSUPPORTED = "source_format_unsupported"
    SOURCE_ROLE_UNSUPPORTED = "source_role_unsupported"
    SOURCE_CONTENT_MISMATCH = "source_content_mismatch"
    OBSERVATION_INCOMPATIBLE = "observation_incompatible"


@dataclass(frozen=True, slots=True, kw_only=True)
class QuantumEspressoObservationAdaptationFailure:
    """One deterministic first-stage adaptation failure without partial output.

    Parameters
    ----------
    code
        Closed expected failure classification.
    result_identity
        Exact caller-reserved identity of the intended successful result, retained for
        failure correlation without representing that result as existing.
    source_manifest_identity, source_manifest_entry_identity
        Exact source manifest revision and selected entry identity.
    parsed_document_identity, source_content_identity
        Exact correlated parsed-document record and parsed source-byte identities.
    parser_identity, parser_version
        Exact requested QEXSD parser implementation family and version.
    normalization_policy
        Exact requested policy identity and version.
    detail
        Nonempty deterministic explanation. It is not a scientific conclusion.
    """

    code: QuantumEspressoObservationAdaptationFailureCode
    result_identity: ResultObjectIdentity
    source_manifest_identity: ArtifactManifestIdentity
    source_manifest_entry_identity: ArtifactManifestEntryIdentity
    parsed_document_identity: QuantumEspressoParsedDocumentIdentity
    source_content_identity: ArtifactContentIdentity
    parser_identity: QuantumEspressoXsdParserIdentity
    parser_version: str
    normalization_policy: QuantumEspressoObservationNormalizationPolicy
    detail: str

    def __post_init__(self) -> None:
        """Validate exact failure fields."""
        if not isinstance(self.code, QuantumEspressoObservationAdaptationFailureCode):
            raise TypeError(
                "code must be QuantumEspressoObservationAdaptationFailureCode"
            )
        if type(self.result_identity) is not ResultObjectIdentity:
            raise TypeError("result_identity must be ResultObjectIdentity")
        if type(self.source_manifest_identity) is not ArtifactManifestIdentity:
            raise TypeError("source_manifest_identity must be ArtifactManifestIdentity")
        if (
            type(self.source_manifest_entry_identity)
            is not ArtifactManifestEntryIdentity
        ):
            raise TypeError(
                "source_manifest_entry_identity must be ArtifactManifestEntryIdentity"
            )
        if (
            type(self.parsed_document_identity)
            is not QuantumEspressoParsedDocumentIdentity
        ):
            raise TypeError(
                "parsed_document_identity must be QuantumEspressoParsedDocumentIdentity"
            )
        if type(self.source_content_identity) is not ArtifactContentIdentity:
            raise TypeError("source_content_identity must be ArtifactContentIdentity")
        if type(self.parser_identity) is not QuantumEspressoXsdParserIdentity:
            raise TypeError("parser_identity must be QuantumEspressoXsdParserIdentity")
        if type(self.parser_version) is not str:
            raise TypeError("parser_version must be a built-in str")
        if not self.parser_version:
            raise ValueError("parser_version must not be empty")
        if (
            type(self.normalization_policy)
            is not QuantumEspressoObservationNormalizationPolicy
        ):
            raise TypeError(
                "normalization_policy must be "
                "QuantumEspressoObservationNormalizationPolicy"
            )
        if type(self.detail) is not str:
            raise TypeError("detail must be a built-in str")
        if not self.detail:
            raise ValueError("detail must not be empty")


type QuantumEspressoObservationAdaptationResult = (
    QuantumEspressoExtractedObservationResult
    | QuantumEspressoObservationAdaptationFailure
)
"""Closed success-or-failure union for first-stage adaptation.

``QuantumEspressoExtractedObservationResult`` is the sole success variant;
``QuantumEspressoObservationAdaptationFailure`` is the sole expected-failure variant.
Neither variant is the separately owned Workflow normalized-observation set.
"""


class QuantumEspressoObservationAdapter:
    """Correlate QEXSD source identity and construct one neutral observation.

    The fieldless ActionObject supports exactly the retained QEXSD plane-wave
    normalization policy. It performs no artifact lookup outside the supplied manifest,
    parser invocation, Workflow normalization assembly, persistence, or execution.
    """

    SUPPORTED_NATIVE_FORMAT = _SUPPORTED_NATIVE_FORMAT
    SUPPORTED_SEMANTIC_ROLE = _SUPPORTED_SEMANTIC_ROLE
    SUPPORTED_POLICY_IDENTITY = _SUPPORTED_POLICY_IDENTITY
    SUPPORTED_POLICY_VERSION = _SUPPORTED_POLICY_VERSION
    SUPPORTED_PARSER_IDENTITY = _SUPPORTED_PARSER_IDENTITY
    SUPPORTED_PARSER_VERSION = _SUPPORTED_PARSER_VERSION
    LIMITATION_VALUES = _LIMITATION_VALUES

    __slots__ = ()

    def execute(
        self, request: QuantumEspressoObservationExtractionRequest
    ) -> QuantumEspressoObservationAdaptationResult:
        """Return one correlated extracted observation or closed expected failure.

        Parameters
        ----------
        request
            Exact parsed document, manifest revision, entry identity, result identity,
            parser identity, and normalization policy.

        Returns
        -------
        QuantumEspressoObservationAdaptationResult
            Immutable extracted observation on exact agreement, otherwise one closed
            failure without a partial observation.

        Raises
        ------
        TypeError
            If ``request`` is not exactly
            :class:`QuantumEspressoObservationExtractionRequest`.
        """
        if type(request) is not QuantumEspressoObservationExtractionRequest:
            raise TypeError(
                "request must be QuantumEspressoObservationExtractionRequest"
            )

        policy = request.normalization_policy
        if (
            policy.identity.value != self.SUPPORTED_POLICY_IDENTITY
            or policy.version != self.SUPPORTED_POLICY_VERSION
        ):
            return self._failure(
                request,
                QuantumEspressoObservationAdaptationFailureCode.POLICY_UNSUPPORTED,
                "normalization policy identity and version are unsupported",
            )

        parsed_document = request.parsed_document
        if (
            parsed_document.parser_identity.value != self.SUPPORTED_PARSER_IDENTITY
            or parsed_document.parser_version != self.SUPPORTED_PARSER_VERSION
        ):
            return self._failure(
                request,
                QuantumEspressoObservationAdaptationFailureCode.PARSER_UNSUPPORTED,
                "QEXSD parser identity and version are unsupported",
            )

        entry = next(
            (
                candidate
                for candidate in request.source_manifest.entries
                if candidate.identity == request.source_manifest_entry_identity
            ),
            None,
        )
        if entry is None:
            return self._failure(
                request,
                QuantumEspressoObservationAdaptationFailureCode.SOURCE_ENTRY_NOT_FOUND,
                "source manifest does not contain the selected entry identity",
            )
        if entry.native_format != self.SUPPORTED_NATIVE_FORMAT:
            return self._failure(
                request,
                QuantumEspressoObservationAdaptationFailureCode.SOURCE_FORMAT_UNSUPPORTED,
                "source manifest entry native format is not quantum-espresso.qexsd",
            )
        if entry.semantic_role != self.SUPPORTED_SEMANTIC_ROLE:
            return self._failure(
                request,
                QuantumEspressoObservationAdaptationFailureCode.SOURCE_ROLE_UNSUPPORTED,
                "source manifest entry role is not QEXSD native output",
            )

        document = parsed_document.document
        if entry.content_identity != parsed_document.source_content_identity:
            return self._failure(
                request,
                QuantumEspressoObservationAdaptationFailureCode.SOURCE_CONTENT_MISMATCH,
                "QEXSD document source identity does not equal manifest entry content",
            )

        try:
            observation = ConstructQexsdKohnShamPlaneWaveRecord().execute(document)
        except ValueError as error:
            return self._failure(
                request,
                QuantumEspressoObservationAdaptationFailureCode.OBSERVATION_INCOMPATIBLE,
                str(error),
            )

        return QuantumEspressoExtractedObservationResult(
            identity=request.result_identity,
            observation=observation,
            source_manifest_identity=request.source_manifest.identity,
            source_manifest_entry_identity=entry.identity,
            source_artifact_identity=entry.artifact_identity,
            source_content_identity=entry.content_identity,
            source_producer_provenance_identity=entry.producer_provenance.identity,
            parsed_document_identity=parsed_document.identity,
            parser_identity=parsed_document.parser_identity,
            parser_version=parsed_document.parser_version,
            normalization_policy=policy,
            limitation_values=self.LIMITATION_VALUES,
        )

    @staticmethod
    def _failure(
        request: QuantumEspressoObservationExtractionRequest,
        code: QuantumEspressoObservationAdaptationFailureCode,
        detail: str,
    ) -> QuantumEspressoObservationAdaptationFailure:
        """Construct one correlated expected failure without partial output."""
        return QuantumEspressoObservationAdaptationFailure(
            code=code,
            result_identity=request.result_identity,
            source_manifest_identity=request.source_manifest.identity,
            source_manifest_entry_identity=request.source_manifest_entry_identity,
            parsed_document_identity=request.parsed_document.identity,
            source_content_identity=request.parsed_document.source_content_identity,
            parser_identity=request.parsed_document.parser_identity,
            parser_version=request.parsed_document.parser_version,
            normalization_policy=request.normalization_policy,
            detail=detail,
        )
