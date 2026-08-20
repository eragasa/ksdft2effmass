"""Compatibility imports for canonical QEXSD native records.

New code imports from :mod:`ksdft2effmass.integration.quantumespresso.qexsd`.
This module retains the accepted v1 import path without duplicating record policy.
"""

from ksdft2effmass.integration.quantumespresso.qexsd.records import (
    AtomDeclaration,
    QexsdDocument,
    QexsdSource,
    SpeciesDeclaration,
    Spectrum,
    Vector3,
    Vector3Sequence,
)

__all__ = [
    "AtomDeclaration",
    "QexsdDocument",
    "QexsdSource",
    "SpeciesDeclaration",
    "Spectrum",
    "Vector3",
    "Vector3Sequence",
]
