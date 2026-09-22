r"""Software verification of the versioned Task catalog configuration wire contract.

Evidence profile: routine

Bounded artifact scope: exact source/resolved schema-2 bytes, retired schema-1
refusal, aggregate invariants and independent resolver version boundaries.

Facet and represented meaning

Four literal resource documents independently specify current and retired bytes.
Schema-1 fixtures are rejection evidence, not compatibility promises. Categorized
roots differ from project locations; no fixture is emitted by production encoding.

Intrinsic and cross-object scope

This artifact owns agreement across source/resolved values, both serializer pairs
and source resolution, not the intrinsic lexical root cases owned separately.

VVUQ and scientific exclusions

Software verification only. No catalog discovery, relocation, filesystem validity,
Task authority or scientific claim follows from accepted configuration bytes.
"""

import hashlib
from dataclasses import replace
from pathlib import Path

import pytest

import ksdft2effmass.harness as api
from ksdft2effmass.harness.pi import PiHarnessConfiguration

pytestmark = pytest.mark.software_verification
RESOURCE_ROOT = Path(__file__).parent / "resources"
PI_BYTES = b'{"subagents":{"agentOverrides":{}}}'


class TestTaskCatalogConfigurationWire:
    """Own source/resolved wire and version-boundary agreement."""

    @staticmethod
    def make_source(version: int) -> api.HarnessConfigurationSource:
        return api.HarnessConfigurationSource(
            version,
            ".pi/settings.json",
            api.HumanReviewConfiguration(
                ".pi/reviews/packets", ".pi/reviews/decisions"
            ),
            api.HarnessPersistenceConfiguration(
                "harness/state/harness-control.sqlite3",
                "harness/state/harness-control.sql",
                "harness/state/projection-manifest.json",
            ),
            api.PythonConformanceConfiguration(
                "python/pyproject.toml",
                "python/tests",
                "harness/pi/evidence/python-test-evidence-profile-matrix-v1.json",
                ".pi/evidence/python-conformance/r2.3-private-owner-migration.json",
            ),
            api.HarnessResourceConfiguration(
                "harness/local/profiles/ksdft2effmass-v2.json",
                "harness/pi/resource-manifest.json",
                "harness/pi",
                "harness/local/resource-manifest.json",
                "harness/local",
            ),
            api.HarnessCatalogConfiguration(
                api.TaskCatalogConfiguration(
                    "catalogs/questions", "catalogs/calculations", "catalogs/code"
                ),
                (".pi/agents",),
                (".pi/checkpoints",),
                (".agents/skills", ".pi/skills"),
            ),
        )

    @staticmethod
    def make_configuration(
        source: api.HarnessConfigurationSource,
    ) -> api.HarnessConfiguration:
        return api.HarnessConfiguration(
            source.schema_version,
            PiHarnessConfiguration(1, ()),
            source.human_review,
            source.persistence,
            source.python_conformance,
            source.resources,
            source.catalogs,
        )

    def test_artifact__canonical_bytes__agrees_with_literal_fixtures(
        self,
    ) -> None:
        """Evidence ID: software-verification.task-catalog.wire.literal-bytes

        Requirement: Schema 2 preserves exact source and resolved canonical bytes.

        Oracle: Independently authored literal files and explicit domain values.

        Acceptance: Both encoders equal fixtures; both decoders equal expected values.
        """
        version = 2
        source = self.make_source(version)
        configuration = self.make_configuration(source)
        source_bytes = (
            RESOURCE_ROOT / f"configuration-source-v{version}.json"
        ).read_bytes()
        resolved_bytes = (
            RESOURCE_ROOT / f"configuration-resolved-v{version}.json"
        ).read_bytes()
        assert (
            api.HarnessConfigurationSourceJsonSerializer().execute(source)
            == source_bytes
        )
        assert (
            api.HarnessConfigurationSourceJsonDeserializer().execute(source_bytes)
            == source
        )
        assert (
            api.HarnessConfigurationJsonSerializer().execute(configuration)
            == resolved_bytes
        )
        assert (
            api.HarnessConfigurationJsonDeserializer().execute(resolved_bytes)
            == configuration
        )

    @pytest.mark.parametrize(
        "before,after,error",
        (
            pytest.param(
                b'"schema_version": 2',
                b'"schema_version": 3',
                ValueError,
                id="unsupported_version",
            ),
            pytest.param(
                b'"schema_version": 2',
                b'"schema_version": 1',
                ValueError,
                id="categorized_in_legacy",
            ),
            pytest.param(
                b'"task_catalog": {',
                b'"task_root": {',
                ValueError,
                id="flat_member_in_categorized",
            ),
            pytest.param(
                b'"task_catalog": {',
                b'"task_root": "tasks",\n    "task_catalog": {',
                ValueError,
                id="mixed_layout",
            ),
            pytest.param(
                b'"research_root": "catalogs/questions",',
                b"",
                ValueError,
                id="missing_category",
            ),
            pytest.param(
                b'"research_root": "catalogs/questions",',
                b'"research_root": "catalogs/questions", "extra": "root",',
                ValueError,
                id="unknown_category",
            ),
            pytest.param(
                b'"research_root": "catalogs/questions",',
                b'"research_root": "catalogs/questions", '
                b'"research_root": "catalogs/other",',
                ValueError,
                id="duplicate_category",
            ),
            pytest.param(
                b'"catalogs/questions"', b"NaN", ValueError, id="nonfinite_root"
            ),
            pytest.param(
                b'"catalogs/questions"',
                b'"catalogs/code"',
                ValueError,
                id="aliased_roots",
            ),
            pytest.param(
                b'"catalogs/questions"', b'"catalogs"', ValueError, id="nested_roots"
            ),
            pytest.param(
                b'"research_root": "catalogs/questions",\n'
                b'      "simulation_root": "catalogs/calculations",',
                b'"simulation_root": "catalogs/calculations",\n'
                b'      "research_root": "catalogs/questions",',
                ValueError,
                id="member_order",
            ),
            pytest.param(
                b'  "schema_version": 2',
                b' "schema_version": 2',
                ValueError,
                id="noncanonical_spacing",
            ),
            pytest.param(b"{", b"\xef\xbb\xbf{", ValueError, id="bom"),
            pytest.param(
                b'"catalogs/questions"',
                b'"catalogs/caf\\u00e9"',
                ValueError,
                id="noncanonical_unicode_escape",
            ),
        ),
    )
    def test_artifact__strict_grammar__rejects_malformed_both_forms(
        self, before: bytes, after: bytes, error: type[ValueError]
    ) -> None:
        """Evidence ID: software-verification.task-catalog.wire.rejections

        Requirement: Both wire forms reject malformed or noncanonical versioned layouts.

        Oracle: Explicit single-mutation partitions of independently authored fixtures.

        Acceptance: Each source and resolved decode raises the named error family.
        """
        source = (RESOURCE_ROOT / "configuration-source-v2.json").read_bytes()
        resolved = (RESOURCE_ROOT / "configuration-resolved-v2.json").read_bytes()
        assert before in source and before in resolved
        with pytest.raises(error):
            api.HarnessConfigurationSourceJsonDeserializer().execute(
                source.replace(before, after, 1)
            )
        with pytest.raises(error):
            api.HarnessConfigurationJsonDeserializer().execute(
                resolved.replace(before, after, 1)
            )

    @pytest.mark.parametrize(
        "before,after",
        (
            pytest.param(
                b'"schema_version": 2', b'"schema_version": true', id="boolean_version"
            ),
            pytest.param(
                b'"schema_version": 2', b'"schema_version": 2.0', id="float_version"
            ),
            pytest.param(
                b'"schema_version": 2', b'"schema_version": "2"', id="string_version"
            ),
            pytest.param(b'"catalogs/questions"', b"null", id="null_root"),
            pytest.param(b'"catalogs/questions"', b"42", id="numeric_root"),
            pytest.param(b'"catalogs/questions"', b"[]", id="array_root"),
        ),
    )
    def test_artifact__field_types__rejects_wrong_semantic_types(
        self, before: bytes, after: bytes
    ) -> None:
        """Evidence ID: software-verification.task-catalog.wire.wrong-field-types

        Requirement: Wrong semantic field types are rejected without coercion.

        Oracle: Explicit type-substitution partitions of the literal v2 fixtures.

        Acceptance: Source and resolved decoding both raise TypeError.
        """
        source = (RESOURCE_ROOT / "configuration-source-v2.json").read_bytes()
        resolved = (RESOURCE_ROOT / "configuration-resolved-v2.json").read_bytes()
        assert before in source and before in resolved
        with pytest.raises(TypeError):
            api.HarnessConfigurationSourceJsonDeserializer().execute(
                source.replace(before, after, 1)
            )
        with pytest.raises(TypeError):
            api.HarnessConfigurationJsonDeserializer().execute(
                resolved.replace(before, after, 1)
            )

    @pytest.mark.parametrize(
        "version",
        (
            pytest.param(1, id="retired_version"),
            pytest.param(3, id="unknown_version"),
        ),
    )
    def test_artifact__aggregate_version__rejects_retired_or_unknown_versions(
        self, version: int
    ) -> None:
        """Evidence ID: software-verification.task-catalog.wire.layout-version

        Requirement: Current components cannot reactivate retired or unknown versions.

        Acceptance: Both source and resolved constructors reject noncurrent versions.
        """
        source = self.make_source(2)
        with pytest.raises(ValueError, match="schema_version must equal 2"):
            replace(source, schema_version=version)
        with pytest.raises(ValueError, match="schema_version must equal 2"):
            replace(self.make_configuration(source), schema_version=version)

    def test_artifact__resolution__preserves_format_and_exact_source_bindings(
        self,
    ) -> None:
        """Evidence ID: software-verification.task-catalog.wire.resolution

        Requirement: Resolution preserves the configuration version and exact inputs.

        Oracle: Literal expected configuration and standard SHA-256 of fixture bytes.

        Acceptance: Resolved value and ordered source digests agree; result and
        framing versions stay at 1.
        """
        version = 2
        payload = (RESOURCE_ROOT / f"configuration-source-v{version}.json").read_bytes()
        result = api.HarnessConfigurationResolver().execute(
            "harness/configuration.json", payload, ".pi/settings.json", PI_BYTES
        )
        assert result.status == "resolved"
        assert result.configuration == self.make_configuration(
            self.make_source(version)
        )
        assert result.schema_version == 1
        assert result.snapshot_identity is not None
        assert result.snapshot_identity.schema_version == 1
        assert tuple(
            binding.content_identity.digest for binding in result.source_bindings
        ) == (hashlib.sha256(payload).hexdigest(), hashlib.sha256(PI_BYTES).hexdigest())
        assert tuple(binding.path for binding in result.source_bindings) == (
            "harness/configuration.json",
            ".pi/settings.json",
        )

    def test_artifact__legacy_bytes__rejects_without_upgrade(self) -> None:
        """Evidence ID: software-verification.task-catalog.wire.retired-schema

        Requirement: Retained schema-1 bytes are historical inputs, not a supported
        runtime format or an implicit migration instruction.

        Acceptance: Both decoders reject the literal historical fixtures.
        """
        with pytest.raises(ValueError, match="schema_version must equal 2"):
            api.HarnessConfigurationSourceJsonDeserializer().execute(
                (RESOURCE_ROOT / "configuration-source-v1.json").read_bytes()
            )
        with pytest.raises(ValueError, match="schema_version must equal 2"):
            api.HarnessConfigurationJsonDeserializer().execute(
                (RESOURCE_ROOT / "configuration-resolved-v1.json").read_bytes()
            )

    def test_artifact__resolution_result__does_not_accept_configuration_version(
        self,
    ) -> None:
        """Evidence ID: software-verification.task-catalog.wire.result-version

        Requirement: Supporting configuration v2 must not widen the result schema.

        Acceptance: Replacing the result's version with 2 raises ValueError.
        """
        payload = (RESOURCE_ROOT / "configuration-source-v2.json").read_bytes()
        result = api.HarnessConfigurationResolver().execute(
            "harness/configuration.json", payload, ".pi/settings.json", PI_BYTES
        )
        with pytest.raises(ValueError, match="result schema_version"):
            replace(result, schema_version=2)

    def test_artifact__pi_version__remains_independently_owned(self) -> None:
        """Evidence ID: software-verification.task-catalog.wire.pi-version

        Requirement: Configuration v2 does not widen Pi's normalized schema.

        Acceptance: A resolved fixture with Pi version 2 raises ValueError.
        """
        payload = (RESOURCE_ROOT / "configuration-resolved-v2.json").read_bytes()
        with pytest.raises(ValueError):
            api.HarnessConfigurationJsonDeserializer().execute(
                payload.replace(b'"schema_version": 1', b'"schema_version": 2')
            )

    def test_artifact__invalid_source__returns_closed_failure(self) -> None:
        """Evidence ID: software-verification.task-catalog.wire.closed-failure

        Requirement: Invalid categorized source yields no resolved configuration.

        Acceptance: Resolver reports SOURCE_INVALID with neither configuration
        nor snapshot.
        """
        payload = (
            (RESOURCE_ROOT / "configuration-source-v2.json")
            .read_bytes()
            .replace(b'"catalogs/questions"', b'"catalogs/code"')
        )
        result = api.HarnessConfigurationResolver().execute(
            "harness/configuration.json", payload, ".pi/settings.json", PI_BYTES
        )
        assert result.status == "failed"
        assert result.configuration is None
        assert result.snapshot_identity is None
        assert tuple(finding.code for finding in result.findings) == (
            "HARNESS_CONFIGURATION.SOURCE_INVALID",
        )
