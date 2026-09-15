"""Calculator-independent assembly of normalized Kohn--Sham observations.

This module owns the Workflow stage that follows a concrete integration's exact
observation extraction. It retains immutable extracted ResultObjects through a
read-only structural protocol, validates their neutral plane-wave Kohn--Sham payload
and exact source correlations, and assembles one Workflow-owned result without
importing a calculator or integration package.

The records and ActionObject perform no parsing, unit conversion, numerical
transformation, persistence, artifact lookup, calculator execution, scientific
analysis, scientific validation, acceptance, or uncertainty quantification. The retained
schema-version-1 neutral observation is not copied or changed.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Protocol, runtime_checkable

from ksdft2effmass.ksdft.pw import KohnShamPlaneWaveCalculationRecord

from .artifacts import (
    ArtifactContentIdentity,
    ArtifactIdentity,
    ArtifactManifestEntryIdentity,
    ArtifactManifestIdentity,
    ArtifactProducerProvenanceIdentity,
)
from .model import ResultObject, ResultObjectIdentity


@runtime_checkable
class ObservationCorrelationIdentity(Protocol):
    """Read-only structural identity retained from an observation source domain.

    Concrete integrations own the nominal identity class and its meaning. Workflow
    reads only its exact nonempty lexical value and does not replace it with a
    Workflow-owned nominal identity.
    """

    @property
    def value(self) -> str:
        """Return the exact nonempty source-domain identity value."""
        ...


@runtime_checkable
class ObservationNormalizationPolicySource(Protocol):
    """Read-only identity and version of an applied integration normalization policy.

    The concrete integration owns policy interpretation and support. Workflow retains
    the exact policy object and validates only its structural identity/version
    representation.
    """

    @property
    def identity(self) -> ObservationCorrelationIdentity:
        """Return the exact source-domain normalization-policy identity."""
        ...

    @property
    def version(self) -> str:
        """Return the exact nonempty source-domain policy version."""
        ...


@runtime_checkable
class NormalizedObservationSource(ResultObject, Protocol):
    """Immutable extracted Kohn--Sham observation accepted by Workflow assembly.

    Concrete integration ResultObjects satisfy this calculator-independent protocol
    structurally. Implementations must be operationally immutable. The protocol
    exposes the unchanged neutral record, exact Workflow artifact identities,
    source-domain parser and policy identities, and explicit limitations; it does not
    interpret a native format or grant scientific acceptance.
    """

    @property
    def observation(self) -> KohnShamPlaneWaveCalculationRecord:
        """Return the unchanged schema-version-1 neutral observation."""
        ...

    @property
    def source_manifest_identity(self) -> ArtifactManifestIdentity:
        """Return the exact source artifact-manifest revision identity."""
        ...

    @property
    def source_manifest_entry_identity(self) -> ArtifactManifestEntryIdentity:
        """Return the exact admitted source-manifest entry identity."""
        ...

    @property
    def source_artifact_identity(self) -> ArtifactIdentity:
        """Return the exact nominal source-artifact identity."""
        ...

    @property
    def source_content_identity(self) -> ArtifactContentIdentity:
        """Return the represented SHA-256 and byte-count source identity."""
        ...

    @property
    def source_producer_provenance_identity(
        self,
    ) -> ArtifactProducerProvenanceIdentity:
        """Return the exact source producer-provenance identity."""
        ...

    @property
    def parsed_document_identity(self) -> ObservationCorrelationIdentity:
        """Return the exact source-domain parsed-document identity."""
        ...

    @property
    def parser_identity(self) -> ObservationCorrelationIdentity:
        """Return the exact source-domain parser implementation identity."""
        ...

    @property
    def parser_version(self) -> str:
        """Return the exact nonempty source-domain parser version."""
        ...

    @property
    def normalization_policy(self) -> ObservationNormalizationPolicySource:
        """Return the exact applied source-domain policy identity and version."""
        ...

    @property
    def limitation_values(self) -> tuple[str, ...]:
        """Return unique lexically ordered explicit source limitations."""
        ...


@dataclass(frozen=True, slots=True, kw_only=True)
class NormalizedObservationAssemblyRequest:
    """Request assembly of one Workflow-owned normalized-observation set.

    Parameters
    ----------
    result_identity
        Exact Workflow-facing identity reserved for the intended successful set.
    sources
        Built-in tuple of immutable extracted ResultObjects. An empty tuple is admitted
        so that the assembler can return a closed ``NO_SOURCES`` failure.

    Notes
    -----
    Construction validates only the request's local types. Complete source correlation
    and unique membership are invariants of :class:`NormalizedObservationSet` and are
    mapped to closed failures by :class:`NormalizedObservationAssembler`.
    """

    result_identity: ResultObjectIdentity
    sources: tuple[NormalizedObservationSource, ...]

    def __post_init__(self) -> None:
        """Validate the exact request boundary types."""
        if type(self.result_identity) is not ResultObjectIdentity:
            raise TypeError("result_identity must be ResultObjectIdentity")
        if type(self.sources) is not tuple:
            raise TypeError("sources must be a built-in tuple")
        if any(
            not isinstance(source, NormalizedObservationSource)
            for source in self.sources
        ):
            raise TypeError("sources must contain NormalizedObservationSource")


@dataclass(frozen=True, slots=True, kw_only=True)
class NormalizedObservationSet:
    """Workflow-owned set retaining exact extracted Kohn--Sham ResultObjects.

    Parameters
    ----------
    identity
        Exact Workflow-facing identity of this normalized-observation result.
    sources
        Nonempty tuple of exact immutable source ResultObjects. Source-result
        identities and manifest-revision/entry pairs must each be unique, and this
        set's identity must differ from every source identity. Every source
        must contain an exact schema-version-1 neutral plane-wave record whose
        provenance agrees with
        its represented content identity, nonempty parser and policy identities and
        versions, and canonical explicit limitations.

    Notes
    -----
    The set retains, rather than copies, each exact immutable source. Construction and
    assembly establish software-contract correlation only. They do not establish that
    represented bytes exist, that provenance statements are true, or that an
    observation is numerically verified, scientifically valid, converged, accepted, or
    suitable for an intended use.
    """

    identity: ResultObjectIdentity
    sources: tuple[NormalizedObservationSource, ...]

    def __post_init__(self) -> None:
        """Validate membership, source fields, and neutral provenance agreement."""
        if type(self.identity) is not ResultObjectIdentity:
            raise TypeError("identity must be ResultObjectIdentity")
        if type(self.sources) is not tuple or any(
            not isinstance(source, NormalizedObservationSource)
            for source in self.sources
        ):
            raise TypeError("sources must be a tuple of NormalizedObservationSource")
        if not self.sources:
            raise ValueError("sources must not be empty")

        result_identities = tuple(source.identity for source in self.sources)
        if len(set(result_identities)) != len(result_identities):
            raise ValueError("source result identities must be unique")
        if self.identity in result_identities:
            raise ValueError(
                "normalized observation set identity must differ from source result "
                "identities"
            )
        entry_references = tuple(
            (
                source.source_manifest_identity,
                source.source_manifest_entry_identity,
            )
            for source in self.sources
        )
        if len(set(entry_references)) != len(entry_references):
            raise ValueError("source manifest revision and entry pairs must be unique")

        for source in self.sources:
            self._require_source(source)

    @staticmethod
    def _require_source(source: NormalizedObservationSource) -> None:
        """Validate one retained source's exact represented correlation fields."""
        if type(source.identity) is not ResultObjectIdentity:
            raise TypeError("source identity must be ResultObjectIdentity")
        if type(source.observation) is not KohnShamPlaneWaveCalculationRecord:
            raise TypeError(
                "source observation must be KohnShamPlaneWaveCalculationRecord"
            )
        if type(source.source_manifest_identity) is not ArtifactManifestIdentity:
            raise TypeError("source_manifest_identity must be ArtifactManifestIdentity")
        if (
            type(source.source_manifest_entry_identity)
            is not ArtifactManifestEntryIdentity
        ):
            raise TypeError(
                "source_manifest_entry_identity must be ArtifactManifestEntryIdentity"
            )
        if type(source.source_artifact_identity) is not ArtifactIdentity:
            raise TypeError("source_artifact_identity must be ArtifactIdentity")
        if type(source.source_content_identity) is not ArtifactContentIdentity:
            raise TypeError("source_content_identity must be ArtifactContentIdentity")
        if (
            type(source.source_producer_provenance_identity)
            is not ArtifactProducerProvenanceIdentity
        ):
            raise TypeError(
                "source_producer_provenance_identity must be "
                "ArtifactProducerProvenanceIdentity"
            )
        for name, identity in (
            ("parsed_document_identity", source.parsed_document_identity),
            ("parser_identity", source.parser_identity),
        ):
            if not isinstance(identity, ObservationCorrelationIdentity):
                raise TypeError(f"{name} must implement ObservationCorrelationIdentity")
            if type(identity.value) is not str:
                raise TypeError(f"{name} value must be a built-in str")
            if not identity.value:
                raise ValueError(f"{name} value must not be empty")
        if type(source.parser_version) is not str:
            raise TypeError("parser_version must be a built-in str")
        if not source.parser_version:
            raise ValueError("parser_version must not be empty")

        policy = source.normalization_policy
        if not isinstance(policy, ObservationNormalizationPolicySource):
            raise TypeError(
                "normalization_policy must implement "
                "ObservationNormalizationPolicySource"
            )
        if not isinstance(policy.identity, ObservationCorrelationIdentity):
            raise TypeError(
                "normalization policy identity must implement "
                "ObservationCorrelationIdentity"
            )
        if type(policy.identity.value) is not str:
            raise TypeError(
                "normalization policy identity value must be a built-in str"
            )
        if not policy.identity.value:
            raise ValueError("normalization policy identity value must not be empty")
        if type(policy.version) is not str:
            raise TypeError("normalization policy version must be a built-in str")
        if not policy.version:
            raise ValueError("normalization policy version must not be empty")

        limitations = source.limitation_values
        if type(limitations) is not tuple:
            raise TypeError("limitation_values must be a built-in tuple")
        if not limitations or any(
            type(value) is not str or not value for value in limitations
        ):
            raise ValueError("limitation_values must contain nonempty built-in strings")
        if limitations != tuple(sorted(set(limitations))):
            raise ValueError("limitation_values must be unique and lexically sorted")

        provenance = source.observation.provenance
        if (
            provenance.source_sha256 != source.source_content_identity.digest
            or provenance.source_byte_count != source.source_content_identity.byte_count
        ):
            raise ValueError(
                "source observation provenance must equal source content identity"
            )


class NormalizedObservationAssemblyFailureCode(StrEnum):
    """Closed expected failure classification for Workflow normalization assembly.

    Attributes
    ----------
    NO_SOURCES
        The request contains no extracted observation source.
    SOURCE_SET_INVALID
        Source membership, identity, limitation, or neutral provenance correlation is
        invalid.
    """

    NO_SOURCES = "no_sources"
    SOURCE_SET_INVALID = "source_set_invalid"


@dataclass(frozen=True, slots=True, kw_only=True)
class NormalizedObservationAssemblyFailure:
    """One closed assembly failure retaining the exact original request.

    Parameters
    ----------
    code
        Closed expected failure classification.
    request
        Exact immutable request, including the reserved result identity and every
        supplied source ResultObject with its complete correlation fields.
    detail
        Nonempty deterministic explanation. It is not a scientific conclusion.
    """

    code: NormalizedObservationAssemblyFailureCode
    request: NormalizedObservationAssemblyRequest
    detail: str

    def __post_init__(self) -> None:
        """Validate exact failure fields."""
        if not isinstance(self.code, NormalizedObservationAssemblyFailureCode):
            raise TypeError("code must be NormalizedObservationAssemblyFailureCode")
        if type(self.request) is not NormalizedObservationAssemblyRequest:
            raise TypeError("request must be NormalizedObservationAssemblyRequest")
        if type(self.detail) is not str:
            raise TypeError("detail must be a built-in str")
        if not self.detail:
            raise ValueError("detail must not be empty")


type NormalizedObservationAssemblyResult = (
    NormalizedObservationSet | NormalizedObservationAssemblyFailure
)
"""Closed success-or-failure union for Workflow normalization assembly."""


class NormalizedObservationAssembler:
    """Assemble exact extracted sources into one Workflow normalized-observation set.

    This fieldless ActionObject applies no scientific or numerical normalization. The
    concrete integration has already produced the neutral record under its explicit
    policy. Assembly validates calculator-independent structural correlation and
    retains each exact immutable source without copying or mutation.
    """

    __slots__ = ()

    def execute(
        self, request: NormalizedObservationAssemblyRequest
    ) -> NormalizedObservationAssemblyResult:
        """Return one normalized-observation set or a closed correlated failure.

        Parameters
        ----------
        request
            Reserved result identity and exact immutable extracted sources.

        Returns
        -------
        NormalizedObservationAssemblyResult
            Workflow-owned set on complete correlation, otherwise a failure retaining
            the exact request and no partial set.

        Raises
        ------
        TypeError
            If ``request`` is not exactly
            :class:`NormalizedObservationAssemblyRequest`.
        """
        if type(request) is not NormalizedObservationAssemblyRequest:
            raise TypeError("request must be NormalizedObservationAssemblyRequest")
        if not request.sources:
            return NormalizedObservationAssemblyFailure(
                code=NormalizedObservationAssemblyFailureCode.NO_SOURCES,
                request=request,
                detail="normalization assembly requires at least one source",
            )
        try:
            return NormalizedObservationSet(
                identity=request.result_identity,
                sources=request.sources,
            )
        except (TypeError, ValueError) as error:
            return NormalizedObservationAssemblyFailure(
                code=NormalizedObservationAssemblyFailureCode.SOURCE_SET_INVALID,
                request=request,
                detail=str(error),
            )
