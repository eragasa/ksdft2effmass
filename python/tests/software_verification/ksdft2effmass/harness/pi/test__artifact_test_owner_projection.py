r"""Software verification of artifact-owned Test-class projection.

Evidence profile: claim_bearing

Bounded artifact scope: owner-qualified evidence extraction and collected-node
projection from one explicitly selected pytest owner class.

Facet and represented meaning

The artifact represents the parser-to-evidence-to-node path used by maintained
repository projections.

Intrinsic and cross-object scope

Direct owner selection, evidence identity, class-qualified node identity, and static
parameter identity are covered. Database publication remains outside this module.

VVUQ and scientific exclusions

This is software verification only. It establishes no numerical verification,
scientific validation, uncertainty quantification, or human acceptance.
"""

from pathlib import Path

import pytest
from ksdft2effmass.harness.pi.conformance.python.corpus import (
    _PythonTestModuleCorpusBuilder,
    _PythonTestModuleInput,
)
from ksdft2effmass.harness.pi.conformance.python.evidence import (
    _PythonEvidenceFactExtractor,
)
from ksdft2effmass.harness.pi.conformance.python.migration import (
    _PythonEvidenceMigrationRule,
)
from ksdft2effmass.harness.pi.conformance.python.nodes import (
    _PythonTestNodeProjector,
)
from ksdft2effmass.harness.pi.conformance.python.parser import PythonTestModuleParser
from ksdft2effmass.harness.pi.local.conformance_inputs import (
    _PythonConformanceInputResolver,
    _PythonConformanceInputs,
)
from ksdft2effmass.harness.pi.local.control.configuration_inputs import (
    _HarnessConfigurationInputResolver,
)
from ksdft2effmass.harness.pi.local.evidence_repository_conformance import (
    _EvidenceRepositoryConformanceValidator,
)
from ksdft2effmass.harness.pi.local.validation import (
    HarnessValidationCheck,
    HarnessValidationRequest,
    HarnessValidationResult,
    HarnessValidator,
    _PythonConformanceRepositoryValidator,
)

_RESOURCE_ROOT = Path(__file__).with_name("resources")
_SOURCE_PATH = "python/tests/software_verification/synthetic/test__artifact.py"
_SOURCE = (_RESOURCE_ROOT / "artifact_test_owner_source.py").read_bytes()
_LEGACY_SOURCE = (_RESOURCE_ROOT / "legacy_module_level_source.py").read_bytes()
_MIGRATION = (_RESOURCE_ROOT / "artifact_test_owner_migration_v2.json").read_bytes()
_SCHEMA_V1_MIGRATION = (
    _RESOURCE_ROOT / "legacy_module_level_migration_v1.json"
).read_bytes()


class TestArtifactTestOwnerProjection:
    """Own the artifact-level agreement evidence for class-qualified projection."""

    def test_artifact__owner_qualified_evidence__preserves_method_identity(
        self,
    ) -> None:
        """Evidence ID: software-verification.harness.test-owner.evidence.qualified

        Requirement: Evidence extraction preserves the selected Test owner together
        with the evidence-owning method name.

        Method: Parse exact synthetic artifact-owned source and extract its evidence
        facts.

        Oracle: The unique top-level ``TestSyntheticArtifact`` declaration fixes the
        owner-qualified suffix, and the method docstring fixes the semantic evidence
        identifier.

        Acceptance: The parsed function and extracted evidence pair equal the exact
        owner-qualified literals.

        Interpretation: Failure would permit class methods to disappear or collide
        with same-named module or peer-class callables.

        Limitations: The synthetic source does not exercise repository discovery.
        """
        model = PythonTestModuleParser.execute_with_test_owner(_SOURCE_PATH, _SOURCE)

        assert len(model.functions) == 1
        assert model.functions[0].owner_class_name == "TestSyntheticArtifact"
        assert model.functions[0].owner_node_name == (
            "TestSyntheticArtifact::test_artifact__literal__equals_itself"
        )
        assert _PythonEvidenceFactExtractor().execute(model) == (
            (
                "TestSyntheticArtifact::test_artifact__literal__equals_itself",
                "software-verification.synthetic.artifact.literal.equals-itself",
            ),
        )

    def test_artifact__helper_nonownership__projects_only_actual_tests(self) -> None:
        """Evidence ID: software-verification.harness.test-owner.helpers.excluded

        Requirement: ID-free helpers remain absent from evidence and node projections.

        Method: Parse a literal fixture with one actual test and one short helper,
        then project both evidence facts and collected nodes.

        Oracle: The fixture's sole Test owner and test declaration fix the exact
        qualified node; its helper has no evidence declaration.

        Acceptance: Exactly the literal class-qualified test and its evidence ID
        appear, never the support method.

        Interpretation: Failure fabricates helper evidence or loses class identity.

        Limitations: Static source projection does not execute the synthetic test.
        """
        source = (_RESOURCE_ROOT / "helper-evidence-source.py.txt").read_bytes()
        path = "test__helper_evidence_fixture.py"
        model = PythonTestModuleParser.execute_with_test_owner(path, source)
        assert _PythonEvidenceFactExtractor().execute(model) == (
            (
                "TestHelperEvidenceFixture::test_artifact__literal__retains_value",
                "SV-HELPER-FIXTURE-001",
            ),
        )
        nodes = _PythonTestNodeProjector().execute((model,))
        assert tuple(node.node_id for node in nodes) == (
            "test__helper_evidence_fixture.py::TestHelperEvidenceFixture::"
            "test_artifact__literal__retains_value",
        )

    def test_artifact__collected_nodes__uses_class_qualified_pytest_identity(
        self,
    ) -> None:
        """Evidence ID: software-verification.harness.test-owner.nodes.qualified

        Requirement: Static collected-node projection includes the selected Test owner
        before the evidence method and preserves explicit parameter IDs.

        Method: Project nodes from the exact parsed synthetic artifact-owned source.

        Oracle: Pytest's class-method node syntax and the literal parameter ID ``one``
        define the exact expected node.

        Acceptance: Projection returns one node whose identity, owner suffix, and
        parameter identity equal the independent literals.

        Interpretation: Failure would create a database node that does not identify
        the pytest-collected class method.

        Limitations: This static check does not execute pytest collection itself.
        """
        model = PythonTestModuleParser.execute_with_test_owner(_SOURCE_PATH, _SOURCE)
        nodes = _PythonTestNodeProjector().execute((model,))

        assert len(nodes) == 1
        assert nodes[0].node_id == (
            f"{_SOURCE_PATH}::TestSyntheticArtifact::"
            "test_artifact__literal__equals_itself[one]"
        )
        assert nodes[0].owner_node_name == (
            "TestSyntheticArtifact::test_artifact__literal__equals_itself"
        )
        assert nodes[0].parameter_id == "one"

    def test_artifact__migration_selection__exempts_only_declared_legacy_owner(
        self,
    ) -> None:
        """Evidence ID: software-verification.harness.test-owner.activation.bounded

        Requirement: Ordinary class-method discovery is the default, schema version 2
        activates only explicitly inventoried legacy paths, and schema version 1 retains
        whole-corpus compatibility.

        Method: Resolve exact schema-version-1 and schema-version-2 migration resources
        and build the same source corpus with and without the version-2 exemption.

        Oracle: The version-1 contract selects all supplied paths, while the version-2
        literal inventories exactly one legacy module path.

        Acceptance: Default parsing exposes the exact owner-qualified method,
        compatibility parsing for the inventoried path exposes no class methods,
        schema version 1 resolves all supplied paths, mismatched prebuilt modes are
        rejected, and a nonrelative debt path fails closed.

        Interpretation: Failure would either omit ordinary new evidence or silently
        reinterpret declared migration debt.

        Limitations: The synthetic resource covers one legacy module without
        predecessor mappings.
        """
        migration = _PythonEvidenceMigrationRule().execute(
            "synthetic-migration.json", _MIGRATION, None
        )
        source = _PythonTestModuleInput(_SOURCE_PATH, _SOURCE)
        default_corpus = _PythonTestModuleCorpusBuilder().execute(
            (source,), legacy_test_owner_paths=()
        )
        assert migration.findings == ()
        assert migration.legacy_test_owner_paths == (_SOURCE_PATH,)
        assert migration.activated_legacy_test_owner_paths((_SOURCE_PATH,)) == (
            _SOURCE_PATH,
        )
        schema_v1 = _PythonEvidenceMigrationRule().execute(
            "schema-v1-migration.json", _SCHEMA_V1_MIGRATION, None
        )
        assert schema_v1.findings == ()
        assert schema_v1.legacy_test_owner_paths is None
        assert schema_v1.activated_legacy_test_owner_paths(
            ("z.py", _SOURCE_PATH, "z.py")
        ) == (_SOURCE_PATH, "z.py")
        compatibility_corpus = _PythonTestModuleCorpusBuilder().execute(
            (source,),
            legacy_test_owner_paths=migration.legacy_test_owner_paths,
        )

        assert default_corpus.models[0].functions[0].owner_node_name == (
            "TestSyntheticArtifact::test_artifact__literal__equals_itself"
        )
        assert compatibility_corpus.models[0].functions == ()
        invalid_migration = _PythonEvidenceMigrationRule().execute(
            "invalid-migration.json",
            _MIGRATION.replace(_SOURCE_PATH.encode(), b"../outside.py"),
            None,
        )
        assert tuple(item[0] for item in invalid_migration.findings) == (
            "TE.MIGRATION_LEGACY_OWNER_PATHS",
        )
        with pytest.raises(ValueError, match="source snapshots and owner mode"):
            _PythonTestModuleCorpusBuilder().execute(
                (source,),
                legacy_test_owner_paths=migration.legacy_test_owner_paths,
                prebuilt=default_corpus,
            )
        with pytest.raises(ValueError, match="source snapshots and owner mode"):
            _PythonTestModuleCorpusBuilder().execute(
                (source,), legacy_test_owner_paths=(), prebuilt=compatibility_corpus
            )

    def test_artifact__schema_v1_adapters__retain_whole_corpus_compatibility(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        """Evidence ID: software-verification.harness.test-owner.activation.schema-v1-adapters

        Requirement: Local repository validation and evidence-summary adapters retain
        whole-corpus module-level discovery for schema-version-1 migration resources.

        Method: Redirect both adapters to one synthetic module-level source and an exact
        schema-version-1 migration resource while retaining the repository's profile and
        remaining structural checks.

        Oracle: Schema version 1 predates per-path debt and therefore selects every
        supplied source for compatibility parsing.

        Acceptance: Repository conformance passes and reports exactly one discovered
        module, classless module-level test node, and unique evidence owner.

        Interpretation: Failure identifies an adapter that collapses schema-version-1
        ``None`` into the schema-version-2 empty-debt meaning.

        Limitations: The schema-version-2 repository path is covered by maintained
        harness validation and projection checks.
        """  # noqa: E501
        repository = Path(__file__).resolve().parents[6]
        source_path = Path("python/tests/test__legacy_artifact.py")
        profile_path = Path("harness/pi/evidence/profile.json")
        migration_path = Path("harness/pi/evidence/migration.json")
        (tmp_path / source_path).parent.mkdir(parents=True)
        (tmp_path / source_path).write_bytes(_LEGACY_SOURCE)
        (tmp_path / profile_path).parent.mkdir(parents=True)
        (tmp_path / profile_path).write_bytes(
            (
                repository
                / "harness/pi/evidence/python-test-evidence-profile-matrix-v1.json"
            ).read_bytes()
        )
        (tmp_path / migration_path).write_bytes(_SCHEMA_V1_MIGRATION)
        inputs = _PythonConformanceInputs(
            tmp_path.resolve(), profile_path, (source_path,), migration_path
        )

        def resolve_inputs(
            resolver: _PythonConformanceInputResolver,
            repository_root: Path,
            *,
            pyproject_path: Path,
            test_root_path: Path,
            profile_path: Path,
            migration_path: Path,
        ) -> _PythonConformanceInputs:
            del resolver, repository_root, pyproject_path, test_root_path
            del profile_path, migration_path
            return inputs

        monkeypatch.setattr(_PythonConformanceInputResolver, "execute", resolve_inputs)
        configuration = (
            _HarnessConfigurationInputResolver()
            .execute(repository)
            .configuration.python_conformance
        )
        local_check = _PythonConformanceRepositoryValidator().execute(
            tmp_path.resolve(), configuration
        )
        passing_checks = tuple(
            HarnessValidationCheck(name, "PASS", ())
            for name in (
                "python_conformance",
                "resources",
                "task_graph",
                "checkpoints",
                "skills",
                "control_state",
            )
        )
        passing_validation = HarnessValidationResult("PASS", passing_checks)

        def validate_harness(
            validator: HarnessValidator, request: HarnessValidationRequest
        ) -> HarnessValidationResult:
            del validator, request
            return passing_validation

        monkeypatch.setattr(HarnessValidator, "execute", validate_harness)
        result = _EvidenceRepositoryConformanceValidator().execute(
            HarnessValidationRequest(repository)
        )

        assert local_check.status == "PASS"
        assert local_check.findings == ()
        assert result.status == "PASS"
        assert result.discovered_modules == 1
        assert result.collected_nodes == 1
        assert result.unique_evidence_owners == 1
        assert result.findings == ()
