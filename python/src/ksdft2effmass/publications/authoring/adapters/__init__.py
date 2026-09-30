"""Exact Project Koios owner adapters for local manuscript authoring."""

from .ad_hoc import AuthorSuppliedPublisherAbstractAdapter
from .ingestion import ProjectKoiosIngestionAdapter
from .ollama import OllamaLoopbackManuscriptInferenceAdapter
from .ollama_retention import OllamaRawResponseArtifact, OllamaResponseRetention
from .references import ProjectedCitationIdentity, ProjectKoiosReferencesAdapter
from .search import ProjectKoiosSearchAdapter

__all__ = (
    "AuthorSuppliedPublisherAbstractAdapter",
    "OllamaLoopbackManuscriptInferenceAdapter",
    "OllamaRawResponseArtifact",
    "OllamaResponseRetention",
    "ProjectedCitationIdentity",
    "ProjectKoiosIngestionAdapter",
    "ProjectKoiosReferencesAdapter",
    "ProjectKoiosSearchAdapter",
)
