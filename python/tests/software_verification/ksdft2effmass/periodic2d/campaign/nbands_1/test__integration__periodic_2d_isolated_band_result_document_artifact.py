r"""Artifact-owned evidence for the isolated-band encoded result document.

Evidence profile: claim_bearing

This module binds exact maintained bytes to their checksum-catalog identity and reviews
public ownership routes. SHA-256 equality establishes content identity only; it does not
establish execution provenance, decoded correctness, numerical reproduction,
convergence, scientific validity, uncertainty quantification, or acceptance.
"""

import hashlib
from pathlib import Path

import pytest

import ksdft2effmass.periodic2d as periodic2d_facade
import ksdft2effmass.periodic2d.campaign as campaign_facade
from ksdft2effmass.periodic2d.campaign import nbands_1 as nbands_1_facade
from ksdft2effmass.periodic2d.campaign.nbands_1 import definition
from ksdft2effmass.periodic2d.campaign.nbands_1.encoded_documents import (
    Periodic2DIsolatedBandEncodedDocuments,
)
from ksdft2effmass.periodic2d.campaign.nbands_1.result_documents import (
    Periodic2DIsolatedBandResultDocument,
)

pytestmark = [pytest.mark.software_verification, pytest.mark.integration]
SUT = Periodic2DIsolatedBandResultDocument
_RESULT_SHA256 = "4eb55bde9d456d86bad1d65c8ac60267c07873c6936f8af876b07fd3e1d27be6"


class TestPeriodic2DIsolatedBandResultDocumentArtifact:
    """Own retained-artifact and route evidence for crosswalk row 056."""

    def repository_root(self) -> Path:
        """Return the repository root containing maintained campaign documents.

        Returns
        -------
        pathlib.Path
            Absolute repository root derived from this maintained test location.
        """
        return Path(__file__).resolve().parents[7]

    def checksum_catalog(self, directory: Path) -> dict[str, str]:
        """Decode unique logical-name to SHA-256 entries from one retained catalog.

        Parameters
        ----------
        directory
            Maintained artifact directory containing ``SHA256SUMS``.

        Returns
        -------
        dict[str, str]
            Mutable test-local lookup from exact logical names to digest strings.

        Raises
        ------
        ValueError
            If a logical name occurs more than once or a nonempty line cannot be split
            into a digest and logical name.
        OSError
            If the maintained catalog cannot be read.
        """
        entries: dict[str, str] = {}
        for line in (
            directory.joinpath("SHA256SUMS").read_text(encoding="utf-8").splitlines()
        ):
            if not line:
                continue
            digest, logical_name = line.split(maxsplit=1)
            if logical_name in entries:
                raise ValueError(f"duplicate checksum-catalog name: {logical_name}")
            entries[logical_name] = digest
        return entries

    def test_retained_result__preserves_exact_bytes_and_catalog_identity(self) -> None:
        """Evidence ID: SV-PERIODIC-TWO-D-ROW-056-ARTIFACT-001.

        Requirement: Row 056 must preserve the exact retained result bytes while moving
        their owner out of the scientific-definition module.

        Method: Read maintained input/result bytes and ``SHA256SUMS``, compose the
        existing two-document owner with the result-document owner, and hash the exact
        result bytes independently.

        Oracle: The reviewed result digest literal and maintained ``SHA256SUMS`` entry.

        Acceptance: Both owners retain the same result byte object and its digest equals
        the reviewed and catalog identities.

        Interpretation: A pass establishes content preservation across the ownership
        correction.

        Limitations: Content identity does not prove calculation execution, provenance,
        decoding, convergence, scientific validation, UQ, or acceptance.
        """
        retained = (
            self.repository_root() / "calculations/research-monograph/periodic-2d"
        )
        input_payload = retained.joinpath("input.json").read_bytes()
        result_payload = retained.joinpath("result.json").read_bytes()
        catalog = self.checksum_catalog(retained)
        encoded_documents = Periodic2DIsolatedBandEncodedDocuments(
            input_payload, result_payload
        )

        document = SUT(encoded_documents.result_payload)
        digest = hashlib.sha256(document.payload).hexdigest()

        assert document.payload is result_payload
        assert document.payload is encoded_documents.result_payload
        assert document.sha256 == digest == _RESULT_SHA256
        assert catalog["result.json"] == _RESULT_SHA256

    def test_public_routes__share_result_document_without_definition_alias(
        self,
    ) -> None:
        """Evidence ID: SV-PERIODIC-TWO-D-ROW-056-ROUTE-001.

        Requirement: Reviewed facades expose the defining result-document class while
        the scientific-definition module no longer owns or aliases that class.

        Method: Compare facade objects with the class defined in ``result_documents``
        and inspect the former definition owner.

        Oracle: The documented three-facade route and no-compatibility-alias policy.

        Acceptance: Every facade exposes the exact defining class object, its module is
        ``result_documents``, and ``definition`` has no retired ownership attribute.

        Interpretation: A pass establishes corrected source ownership without an alias
        or forwarding class.

        Limitations: Import identity does not authenticate or decode any payload.
        """
        assert nbands_1_facade.Periodic2DIsolatedBandResultDocument is SUT
        assert campaign_facade.Periodic2DIsolatedBandResultDocument is SUT
        assert periodic2d_facade.Periodic2DIsolatedBandResultDocument is SUT
        assert SUT.__module__ == (
            "ksdft2effmass.periodic2d.campaign.nbands_1.result_documents"
        )
        assert not hasattr(definition, "Periodic2DIsolatedBandResultDocument")
