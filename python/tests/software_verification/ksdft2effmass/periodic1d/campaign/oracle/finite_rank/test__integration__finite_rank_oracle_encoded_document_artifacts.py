r"""Artifact-owned integration evidence for row-043 finite-rank-oracle documents.

Evidence profile: claim_bearing

Bounded artifact, route, and ownership scope
-------------------------------------------
The maintained analytical-oracle ``input.json`` and ``result.json`` files, their
``SHA256SUMS`` entries, the curated leaf-package route, removal of the former
``FiniteRankOracleCampaignModel`` route, and separation of repository location from
encoded bytes at calculation, retained-correlation, and verification boundaries.

Runtime and scientific boundary
-------------------------------
The tests perform bounded local reads of compact maintained files and inspect typed
Python structure. They do not decode campaign payloads, authenticate source results,
resolve a secular equation, construct an operator, execute an eigensolve, invoke a
calculator, or run retained correlation or verification.

Scientific exclusions
---------------------
A pass establishes retained content identity and software ownership only. It does not
establish execution provenance, infinite-volume or continuum convergence, material
adequacy, transferability, oracle qualification, uncertainty quantification, or
acceptance.
"""

import ast
import hashlib
import inspect
from dataclasses import fields
from pathlib import Path

import pytest

from ksdft2effmass.periodic1d.campaign.oracle import (
    finite_rank as finite_rank_oracle_package,
)
from ksdft2effmass.periodic1d.campaign.oracle.finite_rank import (
    FiniteRankOracleEncodedDocuments as PublicEncodedDocuments,
)
from ksdft2effmass.periodic1d.campaign.oracle.finite_rank import (
    campaign as campaign_module,
)
from ksdft2effmass.periodic1d.campaign.oracle.finite_rank import (
    comparison as comparison_module,
)
from ksdft2effmass.periodic1d.campaign.oracle.finite_rank import (
    contracts as contracts_module,
)
from ksdft2effmass.periodic1d.campaign.oracle.finite_rank import (
    encoded_documents as encoded_documents_module,
)
from ksdft2effmass.periodic1d.campaign.oracle.finite_rank import (
    independent_reconstruction as independent_reconstruction_module,
)
from ksdft2effmass.periodic1d.campaign.oracle.finite_rank import (
    input_decoding as input_decoding_module,
)
from ksdft2effmass.periodic1d.campaign.oracle.finite_rank import (
    numerical_actions as numerical_actions_module,
)
from ksdft2effmass.periodic1d.campaign.oracle.finite_rank import (
    parent_data as parent_data_module,
)
from ksdft2effmass.periodic1d.campaign.oracle.finite_rank import (
    verification as verification_module,
)
from ksdft2effmass.periodic1d.campaign.oracle.finite_rank import (
    workflow as workflow_module,
)

pytestmark = [pytest.mark.integration, pytest.mark.software_verification]
SUT = encoded_documents_module.FiniteRankOracleEncodedDocuments
CAMPAIGN = campaign_module.FiniteRankOracleCampaign
VERIFICATION_REQUEST = verification_module.FiniteRankOracleVerificationRequest


class TestFiniteRankOracleEncodedDocumentArtifacts:
    """Own row-043 retained-file, route, and location-split evidence."""

    repository_root = Path(__file__).resolve().parents[8]
    artifact_directory = repository_root / (
        "calculations/research-monograph/impurity-defect-1d-analytical-oracle"
    )
    input_digest = "ab653338be4f1733c8dd39878526b3293e603f2f0b0e7b8241577db2406c5840"
    result_digest = "64ab16a279d5f8ca18f725dadb15860811a45ea12758a91a7cd7166f6074dae0"

    @classmethod
    def _retained_payloads(cls) -> tuple[bytes, bytes]:
        """Read the two maintained row-043 payloads as exact bytes."""
        return (
            (cls.artifact_directory / "input.json").read_bytes(),
            (cls.artifact_directory / "result.json").read_bytes(),
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
        """Evidence ID: SV-CAMPAIGN-PERIODIC-ONE-D-ROW-043-ARTIFACT-001.

        Requirement: The renamed encoded owner preserves exact maintained input and
        retained-result objects plus reviewed SHA-256 content identities.

        Method: Read both compact artifacts, construct the DataObject, and compare
        object identity and computed digests with the maintained checksum catalog.

        Oracle: The two reviewed SHA-256 values and their ``SHA256SUMS`` entries.

        Acceptance: Both fields retain supplied objects and both computed and catalog
        digests equal the reviewed values.

        Interpretation: A pass establishes exact retained-byte and content-identity
        preservation across the row-043 split.

        Limitations: Digest equality establishes content identity only, not provenance,
        decoded oracle semantics, numerical correctness, qualification, UQ, or
        acceptance.
        """
        input_document, result_document = self._retained_payloads()
        documents = SUT(input_document, result_document)
        catalog = self._catalog_digests()

        assert documents.input_document is input_document
        assert documents.retained_result_document is result_document
        assert hashlib.sha256(documents.input_document).hexdigest() == self.input_digest
        assert (
            hashlib.sha256(documents.retained_result_document).hexdigest()
            == self.result_digest
        )
        assert catalog["input.json"] == self.input_digest
        assert catalog["result.json"] == self.result_digest

    def test_operations__reject_input_bytes_outside_declared_provenance(self) -> None:
        """Evidence ID: SV-CAMPAIGN-PERIODIC-ONE-D-ROW-043-INPUT-001.

        Requirement: Calculation and verification must bind exact encapsulated input
        bytes to provenance before assigning a model unit or reconstructing records.

        Method: Change only the encoded parent energy unit while retaining the original
        result and original input provenance identity.

        Oracle: The reviewed retained-input SHA-256 identity.

        Acceptance: Both paths reject the encapsulated-input mismatch before parent
        adaptation or numerical reconstruction.

        Interpretation: A pass prevents authenticated hopping coefficients from being
        relabeled by unauthenticated input metadata.

        Limitations: This samples one mutation and establishes neither transitive
        provenance nor scientific validity.
        """
        input_document, result_document = self._retained_payloads()
        altered = input_document.replace(
            b'"energy_unit": "E_G"', b'"energy_unit": "forged-unit"', 1
        )
        if altered == input_document:
            raise ValueError("test mutation target was absent")
        campaign = CAMPAIGN(SUT(altered, result_document))

        with pytest.raises(ValueError, match="encapsulated input sha256"):
            campaign.verify_retained(self.repository_root)
        with pytest.raises(ValueError, match="encapsulated input sha256 mismatch"):
            campaign.calculate(
                repository_root=self.repository_root,
                input_path=(
                    "calculations/research-monograph/"
                    "impurity-defect-1d-analytical-oracle/input.json"
                ),
                input_sha256=self.input_digest,
                script_path="unused-runner.py",
                script_sha256="b" * 64,
                python_version="test-python",
                numpy_version="test-numpy",
            )

    def test_routes_and_operation_roots__preserve_repository_location_split(
        self,
        tmp_path: Path,
    ) -> None:
        """Evidence ID: SV-CAMPAIGN-PERIODIC-ONE-D-ROW-043-ROUTE-001.

        Requirement: The curated facade exposes the defining byte-only class,
        calculation and correlation receive explicit roots, verification owns its root
        in a typed request, campaign, Workflow, and verifier behavior is instance-owned,
        and the former aggregate model and source module are absent.

        Method: Compare facade identity, inspect fields and operation signatures,
        exercise lexical root validation without source access, inspect ``__all__``,
        and check retired paths.

        Oracle: The documented row-043 ownership and actual operation-boundary split.

        Acceptance: Documents have no root; verification requests accept a nonexistent
        absolute root without access and reject relative roots; campaign operations
        reject unsupported or relative roots before payload decoding or provenance
        validation; the campaign, Workflow, and verifier modules contain no
        static/class-method namespace behavior; retired routes are absent.

        Interpretation: A pass establishes explicit location ownership without
        authenticating sources or executing finite-rank calculations.

        Limitations: Structural boundaries do not prove source authentication,
        numerical reconstruction, oracle qualification, or physical adequacy.
        """
        assert PublicEncodedDocuments is SUT
        assert finite_rank_oracle_package.FiniteRankOracleEncodedDocuments is SUT
        assert finite_rank_oracle_package.__all__ == [
            "FiniteRankOracleCampaign",
            "FiniteRankOracleCampaignResultDocument",
            "FiniteRankOracleEncodedDocuments",
        ]
        assert [field.name for field in fields(SUT)] == [
            "input_document",
            "retained_result_document",
        ]
        assert [field.name for field in fields(VERIFICATION_REQUEST)] == [
            "encoded_documents",
            "repository_root",
        ]
        assert "repository_root" in inspect.signature(CAMPAIGN.calculate).parameters
        assert list(inspect.signature(CAMPAIGN.correlate_retained).parameters) == [
            "self",
            "repository_root",
        ]
        class_owners = (
            (
                campaign_module,
                ("FiniteRankOracleResultCorrelation", "FiniteRankOracleCampaign"),
            ),
            (comparison_module, ("FiniteRankOracleComparisonCalculator",)),
            (
                contracts_module,
                (
                    "FiniteRankOracleSourceIdentity",
                    "FiniteRankParentContract",
                    "RankOneOracleContract",
                    "FiniteRankSpecialControls",
                    "FiniteRankOracleTolerances",
                    "FiniteRankOracleCampaignInput",
                    "FiniteRankOracleParentData",
                    "RankOneRootResult",
                    "FiniteRankOracleProvenance",
                ),
            ),
            (
                independent_reconstruction_module,
                ("FiniteRankOracleIndependentReconstructor",),
            ),
            (input_decoding_module, ("FiniteRankOracleCampaignInputDeserializer",)),
            (
                numerical_actions_module,
                (
                    "FiniteRankSiteSpaceOperatorConstructor",
                    "FiniteRankResolventOracle",
                ),
            ),
            (
                parent_data_module,
                (
                    "FiniteRankOracleParentModelAdapter",
                    "FiniteRankOracleParentDataLoader",
                ),
            ),
            (workflow_module, ("FiniteRankOracleCampaignWorkflow",)),
            (
                verification_module,
                (
                    "FiniteRankOracleVerificationRequest",
                    "FiniteRankOracleVerificationResult",
                    "FiniteRankOracleCampaignVerifier",
                ),
            ),
        )
        for module, expected_classes in class_owners:
            tree = ast.parse(Path(inspect.getfile(module)).read_text(encoding="utf-8"))
            assert (
                tuple(node.name for node in tree.body if isinstance(node, ast.ClassDef))
                == expected_classes
            )
            namespace_methods = [
                f"{node.name}.{method.name}"
                for node in tree.body
                if isinstance(node, ast.ClassDef)
                for method in node.body
                if isinstance(method, ast.FunctionDef)
                and any(
                    isinstance(decorator, ast.Name)
                    and decorator.id in {"staticmethod", "classmethod"}
                    for decorator in method.decorator_list
                )
            ]
            assert namespace_methods == []

        documents = SUT(b"synthetic input", b"synthetic result")
        campaign = CAMPAIGN(documents)
        absent_absolute_root = tmp_path / "absent-repository-root"
        assert not absent_absolute_root.exists()
        request = VERIFICATION_REQUEST(documents, absent_absolute_root)
        assert request.repository_root is absent_absolute_root

        with pytest.raises(ValueError, match="repository_root must be absolute"):
            VERIFICATION_REQUEST(documents, Path("relative-root"))
        with pytest.raises(ValueError, match="repository_root must be absolute"):
            campaign.correlate_retained(Path("relative-root"))
        with pytest.raises(TypeError, match="repository_root must be pathlib.Path"):
            campaign.correlate_retained("relative-root")  # type: ignore[arg-type]
        with pytest.raises(ValueError, match="repository_root must be absolute"):
            campaign.calculate(
                repository_root=Path("relative-root"),
                input_path="",
                input_sha256="",
                script_path="",
                script_sha256="",
                python_version="",
                numpy_version="",
            )
        with pytest.raises(ValueError, match="repository_root must be absolute"):
            campaign.verify_retained(Path("relative-root"))

        retired_name = "FiniteRankOracleCampaignModel"
        assert not hasattr(finite_rank_oracle_package, retired_name)
        retired_package = self.repository_root / (
            "python/src/ksdft2effmass/campaigns/periodic_1d/defects/finite_rank_oracle"
        )
        assert not retired_package.exists()
