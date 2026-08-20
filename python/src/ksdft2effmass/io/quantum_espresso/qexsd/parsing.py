"""Compatibility import for the canonical QEXSD parser ActionObject.

New code imports :class:`QexsdDocumentParser` from
:mod:`ksdft2effmass.integration.quantumespresso.qexsd`. The historical
``ParseQexsdDocument`` name remains an identity-preserving transitional alias.
"""

from ksdft2effmass.integration.quantumespresso.qexsd.parsing import (
    QexsdDocumentParser,
)

ParseQexsdDocument = QexsdDocumentParser

__all__ = ["ParseQexsdDocument", "QexsdDocumentParser"]
