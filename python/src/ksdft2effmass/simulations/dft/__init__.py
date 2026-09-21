"""Public backend-neutral DFT simulation composition contracts.

The subpackage owns pseudopotential source identities, native-format artifact
metadata, content-addressed external storage layout, and the compact SQLite catalog
boundary shared by calculator-specific simulation packages.  It performs no download,
format conversion, calculator execution, or scientific validation.
"""

from .pseudopotentials import (
    PseudopotentialArtifact,
    PseudopotentialArtifactFormat,
    PseudopotentialArtifactPathResolver,
    PseudopotentialArtifactVerificationResult,
    PseudopotentialArtifactVerifier,
    PseudopotentialCatalogEntry,
    PseudopotentialCatalogInitializer,
    PseudopotentialCatalogRecorder,
    PseudopotentialCatalogResolver,
    PseudopotentialCutoffHints,
    PseudopotentialFormalism,
    PseudopotentialLibraryLayout,
    PseudopotentialRelativity,
    PseudopotentialSha256,
    PseudopotentialSourceEntry,
    PseudopotentialVerificationStatus,
)

__all__ = [
    "PseudopotentialArtifact",
    "PseudopotentialArtifactFormat",
    "PseudopotentialArtifactPathResolver",
    "PseudopotentialArtifactVerificationResult",
    "PseudopotentialArtifactVerifier",
    "PseudopotentialCatalogEntry",
    "PseudopotentialCatalogInitializer",
    "PseudopotentialCatalogRecorder",
    "PseudopotentialCatalogResolver",
    "PseudopotentialCutoffHints",
    "PseudopotentialFormalism",
    "PseudopotentialLibraryLayout",
    "PseudopotentialRelativity",
    "PseudopotentialSha256",
    "PseudopotentialSourceEntry",
    "PseudopotentialVerificationStatus",
]
