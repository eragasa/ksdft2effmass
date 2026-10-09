r"""Artifact-owned integration evidence for the reduction-challenge family.

Evidence profile: claim_bearing

Bounded artifact and route scope
--------------------------------
The maintained ``stress-input.json`` and ``stress-result.json`` files, their
``SHA256SUMS`` entries, canonical facade identity, removal of former source routes and
names, and fresh-interpreter import independence.

Runtime and terminology boundary
--------------------------------
``ReductionChallenge`` names adversarial tests of reduction assumptions, not
mechanical stress. Historical filenames, schema keys, evidence-status text, result-kind
identity, experiment identity, and wire bytes remain unchanged. These tests perform
bounded local reads and imports only; they invoke no calculator.

Scientific exclusions
---------------------
A pass establishes retained content identity and migration-route behavior only. It does
not prove authorship, execution provenance, decoded correctness, numerical
reconstruction, convergence, validation, UQ, transferability, or acceptance.
"""

import hashlib
import os
import subprocess
import sys
from pathlib import Path

import pytest

from ksdft2effmass.periodic1d.campaign import (
    Periodic1DReductionChallengeEncodedDocuments as CampaignEncodedDocuments,
)
from ksdft2effmass.periodic1d.campaign.reduction_challenge import (
    Periodic1DReductionChallengeEncodedDocuments,
)

pytestmark = [pytest.mark.integration, pytest.mark.software_verification]
SUT = Periodic1DReductionChallengeEncodedDocuments


class TestPeriodic1DReductionChallengeEncodedDocumentArtifacts:
    """Own retained-wire and canonical-route evidence for rows 039 and 060."""

    repository_root = Path(__file__).resolve().parents[7]
    artifact_directory = repository_root / "calculations/research-monograph/periodic-1d"
    input_digest = "3be86c6ee7cb08c1c194aa97e856c89458907c23428bed19f6b38cdb437d987a"
    result_digest = "5897e16570609f3b2ad2fb5cdefb39b8da9df6395e42796d8c5af77734cba394"

    @classmethod
    def _retained_payloads(cls) -> tuple[bytes, bytes]:
        """Read the two maintained historical payloads as exact bytes."""
        return (
            (cls.artifact_directory / "stress-input.json").read_bytes(),
            (cls.artifact_directory / "stress-result.json").read_bytes(),
        )

    @classmethod
    def _catalog_digests(cls) -> dict[str, str]:
        """Read the maintained checksum catalog without decoding campaign payloads."""
        return {
            path: digest
            for digest, path in (
                line.split(maxsplit=1)
                for line in (cls.artifact_directory / "SHA256SUMS")
                .read_text(encoding="utf-8")
                .splitlines()
                if line
            )
        }

    def test_retained_artifacts__preserve_exact_bytes_and_catalog_identities(
        self,
    ) -> None:
        """Evidence ID: SV-CAMPAIGN-PERIODIC-ONE-D-ROW-060-ARTIFACT-001.

        Requirement: Canonical ownership preserves both exact historical wire
        representations and reviewed SHA-256 content identities.

        Method: Read both compact artifacts, construct the encoded-document DataObject,
        and compare object identity, computed digests, catalog entries, and historical
        key presence.

        Oracle: Reviewed digests and the maintained ``SHA256SUMS`` catalog.

        Acceptance: Supplied byte objects are retained unchanged; computed and catalog
        digests match; and representative historical ``stress`` keys remain present.

        Interpretation: A pass establishes exact wire preservation across the move.

        Limitations: Digest equality establishes content identity only, not provenance,
        semantics, numerical correctness, scientific validity, UQ, or acceptance.
        """
        input_payload, result_payload = self._retained_payloads()
        documents = SUT(input_payload, result_payload)
        catalog = self._catalog_digests()

        assert documents.input_payload is input_payload
        assert documents.result_payload is result_payload
        assert hashlib.sha256(documents.input_payload).hexdigest() == self.input_digest
        assert (
            hashlib.sha256(documents.result_payload).hexdigest() == self.result_digest
        )
        assert catalog["stress-input.json"] == self.input_digest
        assert catalog["stress-result.json"] == self.result_digest
        # Historical schema spellings are immutable wire identities, not canonical API
        # names and not mechanical-stress semantics.
        assert b'"stress_band_indices"' in input_payload
        assert b'"route_assumption_stress"' in result_payload

    def test_public_routes__expose_one_canonical_owner_and_remove_former_routes(
        self,
    ) -> None:
        """Evidence ID: SV-CAMPAIGN-PERIODIC-ONE-D-ROW-060-ROUTE-001.

        Requirement: The canonical leaf and campaign facade expose one implementation,
        while transitional/publication exports and former implementation modules are
        absent without compatibility aliases.

        Method: Compare canonical facade identity, inspect former facades, and inspect
        every former source path owned by the migrated family.

        Oracle: Row-060 package ownership and no-alias migration policy.

        Acceptance: Canonical identities agree; former facades expose no reduction-
        challenge or ``Periodic1DStress*`` name; and former implementation paths do not
        exist.

        Interpretation: A pass establishes one canonical implementation owner.

        Limitations: Route identity does not validate payload meaning or numerics.
        """
        import ksdft2effmass.campaigns.periodic_1d as transitional
        import ksdft2effmass.campaigns.research_monograph as publication

        assert CampaignEncodedDocuments is SUT
        former_names = {
            name
            for name in (*transitional.__all__, *publication.__all__)
            if name.startswith("Periodic1DStress")
            or name.startswith("Periodic1DReductionChallenge")
        }
        assert former_names == set()
        former_paths = (
            "stress.py",
            "stress_results.py",
            "stress_verification.py",
            "stress_verified_workflows.py",
            "serialization/stress.py",
            "run/stress",
        )
        former_root = (
            self.repository_root / "python/src/ksdft2effmass/campaigns/periodic_1d"
        )
        assert all(not (former_root / path).exists() for path in former_paths)

    def test_fresh_interpreter__canonical_import_is_independent_of_former_package(
        self,
    ) -> None:
        """Evidence ID: SV-CAMPAIGN-PERIODIC-ONE-D-ROW-060-ROUTE-002.

        Requirement: Canonical campaign imports must not initialize or depend on the
        former underscored campaign package.

        Method: Import the canonical leaf in a fresh interpreter with the source tree
        prepended to ``PYTHONPATH`` and inspect loaded module names.

        Oracle: Canonical-to-transitional dependency-direction policy.

        Acceptance: Import succeeds and no ``ksdft2effmass.campaigns.periodic_1d``
        module is loaded.

        Interpretation: A pass excludes hidden forwarding through the former package.

        Limitations: Import independence does not establish scientific correctness.
        """
        source_root = self.repository_root / "python/src"
        environment = os.environ.copy()
        environment["PYTHONPATH"] = os.pathsep.join(
            (str(source_root), environment.get("PYTHONPATH", ""))
        )
        code = """
import sys
from ksdft2effmass.periodic1d.campaign.reduction_challenge import (
    Periodic1DReductionChallengeCampaign,
)
assert Periodic1DReductionChallengeCampaign.__module__.endswith(
    'periodic1d.campaign.reduction_challenge.campaign'
)
assert not any(
    name == 'ksdft2effmass.campaigns.periodic_1d'
    or name.startswith('ksdft2effmass.campaigns.periodic_1d.')
    for name in sys.modules
)
"""
        completed = subprocess.run(
            [sys.executable, "-c", code],
            cwd=self.repository_root,
            env=environment,
            check=False,
            capture_output=True,
            text=True,
            timeout=30,
        )
        assert completed.returncode == 0, completed.stderr
