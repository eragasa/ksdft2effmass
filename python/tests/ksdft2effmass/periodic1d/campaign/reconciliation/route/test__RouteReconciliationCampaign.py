# ruff: noqa: E501
r"""Integration evidence for ``RouteReconciliationCampaign``.

Evidence profile: claim_bearing

Facet and represented meaning
-----------------------------
The campaign authenticates retained matched-extraction and periodic-parent sources,
executes independent site-space and Bloch-fiber routes, correlates canonical retained
bytes, and delegates to a separately implemented verifier.

Intrinsic and cross-object scope
--------------------------------
This is integration evidence because it reads retained repository artifacts and composes
source loading, two route Actionizers, campaign comparison, serialization, correlation,
and independent verification.

VVUQ and scientific exclusions
------------------------------
Passing establishes software and numerical verification for one finite synthetic model.
It does not validate silicon, a continuum limit, transferability, or uncertainty.
"""

import ast
import hashlib
import inspect
from pathlib import Path

import pytest

import ksdft2effmass.periodic1d.campaign.reconciliation.route as public_package
from ksdft2effmass.periodic1d.campaign.reconciliation.route import (
    RouteReconciliationCampaign,
    RouteReconciliationEncodedDocuments,
)
from ksdft2effmass.periodic1d.campaign.reconciliation.route.verification import (
    RouteReconciliationCampaignVerifier,
)
from ksdft2effmass.periodic1d.campaign.reconciliation.route.workflow import (
    BlochFiberExtractor,
    RealSpaceExtractor,
)

pytestmark = [pytest.mark.integration, pytest.mark.numerical_verification]
SUT = RouteReconciliationCampaign


class TestRouteReconciliationCampaign:
    """Own campaign composition, correlation, and independence evidence."""

    @staticmethod
    def repository_root() -> Path:
        """Return the repository containing retained campaign artifacts."""
        return Path(__file__).resolve().parents[7]

    def campaign(self, result_document: bytes | None = None) -> SUT:
        """Build the façade with exact retained documents."""
        root = self.repository_root()
        retained = root / (
            "calculations/research-monograph/impurity-defect-1d-independent-route"
        )
        result = (retained / "result.json").read_bytes()
        return SUT(
            RouteReconciliationEncodedDocuments(
                input_document=(retained / "input.json").read_bytes(),
                retained_result_document=(
                    result if result_document is None else result_document
                ),
            )
        )

    @pytest.mark.expensive
    def test_method__correlate_and_verify_retained__reproduces_campaign(self) -> None:
        """Evidence ID: NV-CAMPAIGN-PERIODIC-ONE-D-DEFECT-005.

        Requirement: Maintained composition must reproduce the retained version-one
        document, while independent verification must separately authenticate sources,
        check structure, and reconstruct every numerical record.

        Method: Correlate under retained provenance and execute the independent verifier.

        Oracle: Exact canonical bytes plus independent site/fiber reconstruction.

        Acceptance: Semantic and byte identity hold at the retained digest; all three
        verifier channels pass for 15 records and three source identities.

        Interpretation: A pass establishes retained compatibility and independent
        numerical verification for the bounded synthetic campaign.

        Limitations: Correlation alone is identity evidence; neither channel establishes
        material validation or uncertainty quantification.
        """
        campaign = self.campaign()
        root = self.repository_root()
        correlation = campaign.correlate_retained(root)
        verification = campaign.verify_retained(root)

        assert correlation.semantic_identity
        assert correlation.canonical_byte_identity
        assert correlation.calculated_sha256 == (
            "861097a6156999b615edd27cf68dcf36fd110248b9d24dc1b862eff5eeec3bdc"
        )
        assert correlation.calculated_sha256 == correlation.retained_sha256
        assert verification.passed
        assert verification.verified_record_count == 15
        assert verification.source_identity_count == 3
        assert verification.retained_result_sha256 == correlation.retained_sha256

    def test_method__verify_retained__authenticates_nonlegacy_implementation(
        self, tmp_path: Path
    ) -> None:
        """Evidence ID: SV-CAMPAIGN-PERIODIC-ONE-D-DEFECT-030.

        Requirement: A nonlegacy result must authenticate both its current runner and
        its separately identified implementation source rather than receiving the
        bounded historical-runner exception.

        Method: Extend a retained-result copy with current runner and implementation
        identities, verify it, then alter only the implementation digest.

        Oracle: Independently computed SHA-256 content identities for both files.

        Acceptance: Exact identities pass; a changed digest fails with an identity
        mismatch; and absolute, parent-traversal, and symlink escapes fail before source
        bytes are read.

        Interpretation: The nonlegacy provenance branch checks exact source content.

        Limitations: SHA-256 identity does not prove execution, correctness, scientific
        validity, uncertainty quantification, or acceptance.
        """
        root = self.repository_root()
        retained = root / (
            "calculations/research-monograph/impurity-defect-1d-independent-route"
        )
        runner = retained / "run_experiment.py"
        implementation = root / (
            "python/src/ksdft2effmass/periodic1d/campaign/reconciliation/"
            "route/workflow.py"
        )
        historical = (
            b'    "script_sha256": '
            b'"9ec2c391e4b49d859abef52249d17699173b6e7844387b3eda47e016d487839c"\n'
        )
        implementation_digest = hashlib.sha256(implementation.read_bytes()).hexdigest()
        current = (
            b'    "implementation_path": '
            b'"python/src/ksdft2effmass/periodic1d/campaign/reconciliation/'
            b'route/workflow.py",\n'
            b'    "implementation_sha256": "'
            + implementation_digest.encode("ascii")
            + b'",\n'
            b'    "script_sha256": "'
            + hashlib.sha256(runner.read_bytes()).hexdigest().encode("ascii")
            + b'"\n'
        )
        result_document = (
            (retained / "result.json").read_bytes().replace(historical, current, 1)
        )
        if historical in result_document:
            raise AssertionError("historical provenance replacement was incomplete")

        verification = self.campaign(result_document).verify_retained(root)

        assert verification.passed
        changed_digest = result_document.replace(
            implementation_digest.encode("ascii"), b"0" * 64, 1
        )
        with pytest.raises(ValueError, match="implementation sha256 mismatch"):
            self.campaign(changed_digest).verify_retained(root)

        declared_implementation = (
            b"python/src/ksdft2effmass/periodic1d/campaign/reconciliation/"
            b"route/workflow.py"
        )
        outside = tmp_path / "outside-workflow.py"
        outside.write_bytes(implementation.read_bytes())
        absolute_escape = result_document.replace(
            declared_implementation, str(outside).encode("utf-8"), 1
        )
        traversal_escape = result_document.replace(
            declared_implementation, b"../outside-workflow.py", 1
        )
        with pytest.raises(ValueError, match="implementation path escapes"):
            self.campaign(absolute_escape).verify_retained(root)
        with pytest.raises(ValueError, match="implementation path escapes"):
            self.campaign(traversal_escape).verify_retained(root)

        temporary_root = tmp_path / "repository"
        temporary_retained = temporary_root / (
            "calculations/research-monograph/impurity-defect-1d-independent-route"
        )
        temporary_retained.mkdir(parents=True)
        (temporary_retained / "input.json").write_bytes(
            (retained / "input.json").read_bytes()
        )
        (temporary_retained / "run_experiment.py").write_bytes(runner.read_bytes())
        linked_implementation = temporary_root / declared_implementation.decode("ascii")
        linked_implementation.parent.mkdir(parents=True)
        linked_implementation.symlink_to(outside)
        with pytest.raises(ValueError, match="implementation path escapes"):
            self.campaign(result_document).verify_retained(temporary_root)

    def test_source__implementation_routes__remain_separate(self) -> None:
        """Evidence ID: SV-CAMPAIGN-PERIODIC-ONE-D-DEFECT-022.

        Requirement: Neither extraction route may invoke or instantiate the other.

        Method: Parse the two Actionizer class bodies from their defining source.

        Oracle: The declared implementation-independence contract.

        Acceptance: Each class body excludes the other class name.

        Interpretation: A pass establishes static route separation while permitting
        shared immutable inputs.

        Limitations: Static separation does not imply independent physical input data.
        """
        real_source = Path(inspect.getfile(RealSpaceExtractor))
        bloch_source = Path(inspect.getfile(BlochFiberExtractor))
        if real_source != bloch_source:
            raise ValueError("route Actionizers must share one audited defining module")
        source = ast.parse(real_source.read_text())
        classes = {
            node.name: ast.unparse(node)
            for node in source.body
            if isinstance(node, ast.ClassDef)
        }

        assert "BlochFiberExtractor" not in classes["RealSpaceExtractor"]
        assert "RealSpaceExtractor" not in classes["BlochFiberExtractor"]

    def test_source__independent_verifier__does_not_import_workflow(self) -> None:
        """Evidence ID: SV-CAMPAIGN-PERIODIC-ONE-D-DEFECT-023.

        Requirement: Independent verification must not import the maintained Workflow
        or either maintained route Actionizer.

        Method: Parse every import in the verifier defining module.

        Oracle: The campaign's independent-verification boundary.

        Acceptance: No import targets ``workflow``.

        Interpretation: A pass establishes a static implementation boundary.

        Limitations: Static imports complement but cannot alone prove algorithmic
        independence.
        """
        source = ast.parse(
            Path(inspect.getfile(RouteReconciliationCampaignVerifier)).read_text()
        )
        modules = tuple(
            node.module
            for node in ast.walk(source)
            if isinstance(node, ast.ImportFrom) and node.module is not None
        )

        assert "workflow" not in modules

    def test_package__exports__remain_encapsulated(self) -> None:
        """Evidence ID: SV-CAMPAIGN-PERIODIC-ONE-D-DEFECT-024.

        Requirement: The package boundary exposes only the facade and document owners.

        Method: Inspect the declared package export list.

        Oracle: The curated package contract.

        Acceptance: Exactly the campaign, result-document, and paired-document names
        are exported.

        Interpretation: A pass establishes the narrow aggregation boundary.

        Limitations: Defining-module implementation imports remain intentionally usable.
        """
        assert public_package.__all__ == [
            "RouteReconciliationCampaign",
            "RouteReconciliationCampaignResultDocument",
            "RouteReconciliationEncodedDocuments",
        ]

    def test_method__verify_retained__rejects_numerical_corruption(self) -> None:
        """Evidence ID: NV-CAMPAIGN-PERIODIC-ONE-D-DEFECT-006.

        Requirement: Independent verification must detect a retained route diagnostic
        changed without changing its authenticated sources.

        Method: Replace one exact route-noncommutativity value in otherwise valid JSON.

        Oracle: Independent site-space and Bloch-fiber reconstruction.

        Acceptance: Verification raises ``ValueError`` naming the changed field.

        Interpretation: A pass establishes sensitivity to numerical corruption.

        Limitations: The mutation samples one of the checked scalar channels.
        """
        retained = self.campaign().encoded_documents.retained_result_document
        mutated = retained.replace(
            b'"route_noncommutativity_frobenius": 6.8247125479935086e-15',
            b'"route_noncommutativity_frobenius": 0.25',
            1,
        )
        if mutated == retained:
            raise ValueError("test mutation target was absent")

        with pytest.raises(
            ValueError, match="record mismatch: route_noncommutativity_frobenius"
        ):
            self.campaign(mutated).verify_retained(self.repository_root())

    def test_method__retained_result__preserves_exact_digest(self) -> None:
        """Evidence ID: SV-CAMPAIGN-PERIODIC-ONE-D-DEFECT-025.

        Requirement: Reading the retained result must preserve its exact bytes.

        Method: Hash the encapsulated result returned by the façade.

        Oracle: The retained SHA-256 content identity.

        Acceptance: The digest equals the frozen retained identity.

        Interpretation: A pass establishes byte-preserving encapsulation only.

        Limitations: Content identity is not numerical verification.
        """
        payload = self.campaign().retained_result().payload
        assert hashlib.sha256(payload).hexdigest() == (
            "861097a6156999b615edd27cf68dcf36fd110248b9d24dc1b862eff5eeec3bdc"
        )
