r"""Software verification of ``QuantumEspressoParsedDocumentRecord``.

Evidence profile: routine

Bounded artifact scope: Parsed QEXSD document and source-content correlation.

Facet and represented meaning

The DataObject binds one mechanically parsed QEXSD document to its exact represented
source-byte identity and explicit parser implementation identity and version.

Intrinsic and cross-object scope

The evidence covers the intrinsic agreement between document and source-content
identity. Parser support and manifest compatibility remain adapter-owned behavior.

VVUQ and scientific exclusions

The controlled QEXSD bytes are synthetic test data. Construction establishes software
verification only, not parser execution, provenance truth, numerical verification,
scientific validation, UQ, physical correctness, convergence, or acceptance.
"""

from dataclasses import replace

import pytest

from ksdft2effmass.integration.quantum_espresso import (
    QuantumEspressoParsedDocumentIdentity,
    QuantumEspressoParsedDocumentRecord,
    QuantumEspressoXsdParserIdentity,
)
from ksdft2effmass.integration.quantum_espresso.qexsd import (
    QexsdDocument,
    QexsdSource,
    QuantumEspressoXsdDocumentParser,
)
from ksdft2effmass.workflows.artifacts import ArtifactContentIdentity

from .resources.qexsd_fixtures import CONTROLLED_QEXSD, QexsdFixtureResources

SUT = QuantumEspressoParsedDocumentRecord
pytestmark = pytest.mark.software_verification


class TestQuantumEspressoParsedDocumentRecord:
    """Own this module's maintained software-verification evidence."""

    @staticmethod
    def parsed_document() -> QuantumEspressoParsedDocumentRecord:
        """Return one exactly correlated synthetic parsed-document record.

        Evidence ID: Helper owns no identifier.

        Requirement: Support intrinsic source-correlation evidence.

        Method: Parse maintained synthetic QEXSD bytes and bind their exact identity.

        Oracle: Consuming test methods own all assertions.

        Acceptance: Return one intrinsically valid parsed-document record.

        Interpretation: Failure blocks the consuming software-verification evidence.

        Limitations: The bytes are synthetic test data, not physical evidence.
        """
        digest, count = QexsdFixtureResources.controlled_source_bytes()
        document: QexsdDocument = QuantumEspressoXsdDocumentParser().execute(
            QexsdSource("/controlled/source.xml", digest, count, CONTROLLED_QEXSD)
        )
        return SUT(
            identity=QuantumEspressoParsedDocumentIdentity(
                "parsed-document.synthetic.qexsd"
            ),
            parser_identity=QuantumEspressoXsdParserIdentity(
                "ksdft2effmass.quantum-espresso.qexsd-parser"
            ),
            parser_version="1",
            source_content_identity=ArtifactContentIdentity(
                "sha256", document.source_sha256, document.source_byte_count
            ),
            document=document,
        )

    def test_constructor__source_correlation__rejects_mismatch(self) -> None:
        """Evidence ID: SV-QE-PARSED-DOC-001

        Requirement: A parsed-document record binds its exact document to source bytes.

        Acceptance: Replacing its content identity with a different digest fails.
        """
        parsed_document = self.parsed_document()

        with pytest.raises(ValueError, match="parser source content identity"):
            replace(
                parsed_document,
                source_content_identity=ArtifactContentIdentity(
                    "sha256",
                    "0" * 64,
                    parsed_document.document.source_byte_count,
                ),
            )
