r"""Software verification of periodic-2D parent capability qualification.

Evidence profile: routine

These tests exercise accepted historical dimensionless synthetic parent projections.
They perform no external calculation and do not establish material validation,
finite-domain convergence, isolated-defect behavior, or execution authority for the
3,240-evaluation defect campaign.
"""

from __future__ import annotations

import hashlib
import json
import platform
import subprocess
import sys
from dataclasses import replace
from pathlib import Path
from typing import cast

import pytest

from ksdft2effmass.campaigns.research_monograph.impurity_defect_2d import (
    ParentQualificationCalculationWorkflow,
    ParentQualificationIndependentVerificationWorkflow,
    ParentQualificationIndependentVerifier,
    ParentQualificationRequestJsonSerializer,
    ParentQualificationResourceEnvelope,
    ParentQualificationResult,
    ParentQualificationResultJsonSerializer,
    ParentQualificationTolerances,
    QualifiedParentMetrics,
)
from ksdft2effmass.solidstate import (
    BoundaryTwistMesh,
    FiniteLatticeShape,
    LatticeDimension,
)

pytestmark = [pytest.mark.integration, pytest.mark.software_verification]

type JsonValue = (
    None | bool | int | float | str | list[JsonValue] | dict[str, JsonValue]
)


class TestParentQualification:
    """Own software verification of maintained parent qualification."""

    @staticmethod
    def repository_root() -> Path:
        """Return the repository root containing retained qualification evidence."""
        return Path(__file__).resolve().parents[7]

    @classmethod
    def execution_root(cls) -> Path:
        """Return the retained version-one parent qualification root."""
        return (
            cls.repository_root()
            / "calculations/periodic2d_rank_defect/executions/parent-qualification-v1"
        )

    def test__ParentQualification__method__workflows__qualify_compact_parent_inventory(
        self,
    ) -> None:
        """Evidence ID: SV-P2D-RANK-DEFECT-PARENT-001.

        Requirement: Separate public Workflows calculate and independently reconstruct
        the exact parent, perturbation, gauge, and route contracts.

        Acceptance: A compact shape/twist inventory binds its exact platform-local
        binary64 hopping identities, passes prospective criteria, and passes independent
        arithmetic within its declared reconstruction tolerance.
        """
        request = self.compact_request()
        calculation = ParentQualificationCalculationWorkflow().execute(request)
        verification = ParentQualificationIndependentVerificationWorkflow().execute(
            calculation.serialized_result,
            verification_absolute_tolerance=(
                calculation.result.definition.tolerances.reconstruction_absolute
            ),
        )

        assert calculation.result.passes
        assert verification.verification.passes
        assert len(calculation.result.parents) == 3
        assert len(calculation.result.perturbations) == 2
        assert verification.verification.reconstructed_parent_route_evaluations == 48
        assert verification.verification.reconstructed_defect_route_evaluations == 32

    def test__ParentQualification__artifact__retained_package__authenticates_all_manifest_entries(  # noqa: E501
        self,
    ) -> None:
        """Evidence ID: SV-P2D-RANK-DEFECT-PARENT-002.

        Requirement: The retained package binds request, result, execution, scripts,
        software versions, and independent verification without dense matrices.

        Acceptance: Every manifest artifact has the retained byte count and SHA-256,
        and the typed result records a passing complete inventory.
        """
        root = self.execution_root()
        manifest = self.read_object(root / "manifest.json")
        assert manifest["dense_matrices_retained"] is False
        artifacts = cast(list[JsonValue], manifest["artifacts"])
        for value in artifacts:
            record = cast(dict[str, JsonValue], value)
            represented = cast(str, record["path"])
            path = (
                root / represented
                if not represented.startswith("calculations/")
                else self.repository_root() / represented
            )
            content = path.read_bytes()
            assert len(content) == record["bytes"]
            assert hashlib.sha256(content).hexdigest() == record["sha256"]

        result = ParentQualificationResultJsonSerializer().deserialize(
            (root / "results/result.json").read_bytes()
        )
        verification = self.read_object(root / "verification/verification.json")
        assert result.passes
        assert sum(value.route_evaluations for value in result.parents) == 6804
        assert sum(value.route_evaluations for value in result.perturbations) == 4536
        assert verification["outcome"] == "passed"
        assert verification["criteria_match"] is True
        assert verification["reconstruction_passed"] is True

    def test__ParentQualification__artifact__source_audit__replays_and_refuses_overwrite(  # noqa: E501
        self, tmp_path: Path
    ) -> None:
        """Evidence ID: SV-P2D-RANK-DEFECT-PARENT-003.

        Requirement: The retained request projection is authenticated against exact
        historical Git objects and implementation identities are additively bound.

        Acceptance: A fresh read-only audit is byte-identical to both retained
        amendment records, every added artifact authenticates, and overwrite is
        refused.
        """
        retained = self.execution_root()
        generated = tmp_path / "parent-qualification-v1"
        (generated / "inputs").mkdir(parents=True)
        (generated / "inputs/request.json").write_bytes(
            (retained / "inputs/request.json").read_bytes()
        )
        (generated / "manifest.json").write_bytes(
            (retained / "manifest.json").read_bytes()
        )
        script = (
            self.repository_root() / "calculations/periodic2d_rank_defect/"
            "run_09_audit_parent_qualification_source.py"
        )
        command = (
            sys.executable,
            str(script),
            "--execution-root",
            str(generated),
        )
        subprocess.run(command, check=True, capture_output=True, text=True)
        for name in (
            "source-projection-audit.json",
            "manifest-amendment-v1.json",
        ):
            assert (generated / name).read_bytes() == (retained / name).read_bytes()

        amendment = self.read_object(retained / "manifest-amendment-v1.json")
        assert amendment["additive_only"] is True
        assert (
            amendment["original_manifest_sha256"]
            == hashlib.sha256((retained / "manifest.json").read_bytes()).hexdigest()
        )
        for value in cast(list[JsonValue], amendment["added_artifacts"]):
            record = cast(dict[str, JsonValue], value)
            represented = cast(str, record["path"])
            path = (
                retained / represented
                if represented == "source-projection-audit.json"
                else self.repository_root() / represented
            )
            content = path.read_bytes()
            assert len(content) == record["bytes"]
            assert hashlib.sha256(content).hexdigest() == record["sha256"]

        repeated = subprocess.run(command, check=False, capture_output=True, text=True)
        assert repeated.returncode != 0
        assert "refusing to overwrite" in repeated.stderr

    def test__ParentQualification__method__independent_verifier__detects_metric_substitution(  # noqa: E501
        self,
    ) -> None:
        """Evidence ID: SV-P2D-RANK-DEFECT-PARENT-004.

        Requirement: Independent reconstruction detects a retained metric mutation
        even when the mutation remains within deliberately relaxed campaign criteria.

        Acceptance: Criterion correlation remains exact while arithmetic
        reconstruction fails.
        """
        definition = ParentQualificationRequestJsonSerializer().deserialize(
            self.compact_request()
        )
        relaxed = replace(
            definition,
            tolerances=replace(
                definition.tolerances,
                gauge_bridge_absolute=1.0e-3,
            ),
        )
        retained = (
            ParentQualificationCalculationWorkflow()
            .execute(ParentQualificationRequestJsonSerializer().serialize(relaxed))
            .result
        )
        first = retained.parents[0]
        substituted = QualifiedParentMetrics(
            first.parent_identifier,
            first.hopping_count,
            first.hopping_digest,
            first.hopping_hermiticity_maximum_absolute,
            first.hopping_symmetry_maximum_absolute,
            first.represented_hermiticity_maximum_absolute,
            first.gauge_bridge_maximum_absolute + 1.0e-6,
            first.route_evaluations,
            first.inherited_truncation_maximum_absolute,
            first.inherited_truncation_frobenius,
        )
        mutated = ParentQualificationResult(
            retained.definition,
            (substituted, *retained.parents[1:]),
            retained.perturbations,
            retained.maximum_plane_wave_separability_absolute,
            retained.failed_criteria,
        )

        verification = ParentQualificationIndependentVerifier().execute(
            mutated,
            absolute_tolerance=relaxed.tolerances.reconstruction_absolute,
        )

        assert verification.criteria_match
        assert not verification.reconstruction_passed
        assert not verification.passes

    def test__ParentQualification__artifact__request_serialization__rejects_identity_mutation(  # noqa: E501
        self,
    ) -> None:
        """Evidence ID: SV-P2D-RANK-DEFECT-PARENT-005.

        Requirement: Parent qualification requests have one closed canonical wire
        identity.

        Acceptance: Canonical bytes round-trip exactly and an unsupported record type
        is rejected before parent reconstruction.
        """
        payload = self.compact_request()
        serializer = ParentQualificationRequestJsonSerializer()
        assert serializer.serialize(serializer.deserialize(payload)) == payload
        mutated = payload.replace(
            b'"record_type": "periodic2d_rank_defect_parent_qualification_request"',
            b'"record_type": "unsupported_parent_qualification_request"',
            1,
        )
        with pytest.raises(ValueError, match="record_type"):
            serializer.deserialize(mutated)

    @classmethod
    def compact_request(cls) -> bytes:
        """Return a compact request with exact platform-local hopping identities."""
        serializer = ParentQualificationRequestJsonSerializer()
        retained = serializer.deserialize(
            (cls.execution_root() / "inputs/request.json").read_bytes()
        )
        definition = replace(
            retained,
            shapes=(
                FiniteLatticeShape(LatticeDimension.TWO, (1, 1)),
                FiniteLatticeShape(LatticeDimension.TWO, (3, 4)),
            ),
            twist_mesh=BoundaryTwistMesh(LatticeDimension.TWO, (2, 2)),
            tolerances=ParentQualificationTolerances(
                retained.tolerances.hopping_hermiticity_absolute,
                retained.tolerances.hopping_symmetry_absolute,
                retained.tolerances.represented_hermiticity_absolute,
                retained.tolerances.gauge_bridge_absolute,
                retained.tolerances.reconstruction_absolute,
                retained.tolerances.separability_absolute,
            ),
            resource_envelope=ParentQualificationResourceEnvelope(
                maximum_matrix_dimension=12,
                maximum_parent_route_evaluations=48,
                maximum_defect_route_evaluations=32,
                maximum_runtime_seconds=120,
                maximum_peak_memory_gib=2.0,
                maximum_retained_output_mib=5.0,
                network_access=False,
                external_executables=(),
                new_dependencies=(),
            ),
        )
        observed = ParentQualificationCalculationWorkflow().execute(
            serializer.serialize(definition)
        )
        digest_failures = tuple(
            f"parent.{value.parent_identifier}.historical_digest"
            for value in observed.result.parents
            if value.hopping_digest
            != dict(definition.expected_parent_digests)[value.parent_identifier]
        )
        versions = cls.read_object(cls.execution_root() / "software-versions.json")
        retained_platform = versions["platform"]
        if type(retained_platform) is not str or not retained_platform:
            raise AssertionError("retained platform identity must be a string")
        if platform.platform() == retained_platform:
            assert not digest_failures
        assert observed.result.failed_criteria == digest_failures
        platform_definition = replace(
            definition,
            expected_parent_digests=tuple(
                (value.parent_identifier, value.hopping_digest)
                for value in observed.result.parents
            ),
        )
        return serializer.serialize(platform_definition)

    @staticmethod
    def read_object(path: Path) -> dict[str, JsonValue]:
        """Read one retained JSON object for package authentication."""
        decoded = cast(JsonValue, json.loads(path.read_text(encoding="utf-8")))
        if type(decoded) is not dict:
            raise ValueError(f"{path} must contain one JSON object")
        return decoded
