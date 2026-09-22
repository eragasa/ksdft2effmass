"""Exact authored and accepted result-context preparation for Stage C."""

from __future__ import annotations

import hashlib
import platform
import time
from pathlib import Path

from .authorization import (
    AcceptedParentStageCAuthorityValidator,
    AcceptedParentStageCExecutionAuthorizationDeserializer,
    StageCOperationPaths,
    ValidatedStageCExecution,
)
from .model import ArtifactBinding, StageCResultContext

STAGE_DIRECTORY = Path(__file__).resolve(strict=True).parent.parent
REPOSITORY_ROOT = STAGE_DIRECTORY.parents[2]


class StageCResultContextPreparer:
    """Prepare exact authored or accepted result contexts."""

    __slots__ = ()

    _ATTEMPT = (
        "calculations/research-monograph/impurity-defect-2d/"
        "stage-c-accepted-parent-attempt.jsonl"
    )
    _RESULT = (
        "calculations/research-monograph/impurity-defect-2d/"
        "stage-c-accepted-parent-result.json"
    )
    _VERIFICATION = (
        "calculations/research-monograph/impurity-defect-2d/"
        "stage-c-accepted-parent-verification.log"
    )
    _SVG = (
        "calculations/research-monograph/impurity-defect-2d/"
        "stage-c-accepted-parent-summary.svg"
    )
    _REPORT = (
        "calculations/research-monograph/impurity-defect-2d/"
        "stage-c-accepted-parent-report.md"
    )
    _MANIFEST = (
        "calculations/research-monograph/impurity-defect-2d/"
        "stage-c-accepted-parent-native-evidence-manifest.json"
    )
    _CHECKSUM = (
        "calculations/research-monograph/impurity-defect-2d/"
        "stage-c-accepted-parent-SHA256SUMS"
    )

    @classmethod
    def authored(
        cls,
        result_id: str,
        source_mode: str,
        identities: tuple[ArtifactBinding, ...],
    ) -> StageCResultContext:
        root = REPOSITORY_ROOT
        return StageCResultContext(
            result_id=result_id,
            evidence_status=(
                "authored synthetic execution-free software-verification behavior; "
                "not accepted-parent evidence"
            ),
            accepted_parent_read=False,
            source_mode=source_mode,
            operation_inventory=("evaluate_stage_c", "serialize_result"),
            input_identities=identities,
            authorization_id=None,
            authorization_path=None,
            authorization_sha256=None,
            checkpoint_path=None,
            checkpoint_sha256=None,
            human_response_verbatim=None,
            repository_root=str(root),
            repository_revision=AcceptedParentStageCAuthorityValidator.repository_revision(
                root
            ),
            machine_identity=platform.node(),
            native_artifact_root="/Users/eugene/projects/ksdft2effmass",
            attempt_record_path=cls._ATTEMPT,
            result_path=cls._RESULT,
            verification_log_path=cls._VERIFICATION,
            summary_svg_path=cls._SVG,
            report_path=cls._REPORT,
            native_evidence_manifest_path=cls._MANIFEST,
            checksum_catalog_path=cls._CHECKSUM,
            maximum_runtime_seconds=600,
            maximum_peak_memory_gib=2.0,
            maximum_retained_output_mib=20.0,
            maximum_attempts=0,
            retry_authorized=False,
            overwrite_existing=False,
            started_at=None,
        )

    @staticmethod
    def authored_operation(
        identities: tuple[ArtifactBinding, ...], outputs: StageCOperationPaths
    ) -> StageCResultContext:
        """Prepare a complete nonexecuting authored-operation context."""

        root = REPOSITORY_ROOT
        return StageCResultContext(
            result_id=(
                "research-monograph.impurity-defect-2d.stage-c."
                "accepted-parent-operation-authored-fixture.v1"
            ),
            evidence_status=(
                "authored synthetic complete-operation software-verification "
                "behavior; not accepted-parent evidence"
            ),
            accepted_parent_read=False,
            source_mode="authored_complete_operation_fixture",
            operation_inventory=(
                AcceptedParentStageCExecutionAuthorizationDeserializer.OPERATION_INVENTORY
            ),
            input_identities=identities,
            authorization_id=None,
            authorization_path=None,
            authorization_sha256=None,
            checkpoint_path=None,
            checkpoint_sha256=None,
            human_response_verbatim=None,
            repository_root=str(root),
            repository_revision=AcceptedParentStageCAuthorityValidator.repository_revision(
                root
            ),
            machine_identity=platform.node(),
            native_artifact_root="/Users/eugene/projects/ksdft2effmass",
            attempt_record_path=str(outputs.attempt_record),
            result_path=str(outputs.result),
            verification_log_path=str(outputs.verification_log),
            summary_svg_path=str(outputs.summary_svg),
            report_path=str(outputs.report),
            native_evidence_manifest_path=str(outputs.native_evidence_manifest),
            checksum_catalog_path=str(outputs.checksum_catalog),
            maximum_runtime_seconds=600,
            maximum_peak_memory_gib=2.0,
            maximum_retained_output_mib=20.0,
            maximum_attempts=1,
            retry_authorized=False,
            overwrite_existing=False,
            started_at=None,
        )

    @staticmethod
    def accepted(execution: ValidatedStageCExecution) -> StageCResultContext:
        authorization = execution.authorization
        data_roles = AcceptedParentStageCAuthorityValidator.DATA_ROLES
        identities = tuple(
            value for value in authorization.artifacts if value.role in data_roles
        )
        return StageCResultContext(
            result_id=(
                "research-monograph.impurity-defect-2d.stage-c.accepted-parent.v1"
            ),
            evidence_status=(
                "calculated result from one explicitly authorized accepted-parent "
                "Stage C execution; numerical-verification evidence only, not "
                "material or scientific-validation evidence"
            ),
            accepted_parent_read=True,
            source_mode="accepted_parent_execution",
            operation_inventory=authorization.operation_inventory,
            input_identities=identities,
            authorization_id=authorization.authorization_id,
            authorization_path=execution.authorization_path.relative_to(
                Path(authorization.repository_root)
            ).as_posix(),
            authorization_sha256=hashlib.sha256(
                execution.authorization_path.read_bytes()
            ).hexdigest(),
            checkpoint_path=authorization.checkpoint_path,
            checkpoint_sha256=authorization.checkpoint_sha256,
            human_response_verbatim=authorization.human_response_verbatim,
            repository_root=authorization.repository_root,
            repository_revision=authorization.repository_revision,
            machine_identity=authorization.machine_identity,
            native_artifact_root=authorization.native_artifact_root,
            attempt_record_path=authorization.attempt_record_path,
            result_path=authorization.result_path,
            verification_log_path=authorization.verification_log_path,
            summary_svg_path=authorization.summary_svg_path,
            report_path=authorization.report_path,
            native_evidence_manifest_path=authorization.native_evidence_manifest_path,
            checksum_catalog_path=authorization.checksum_catalog_path,
            maximum_runtime_seconds=authorization.maximum_runtime_seconds,
            maximum_peak_memory_gib=authorization.maximum_peak_memory_gib,
            maximum_retained_output_mib=authorization.maximum_retained_output_mib,
            maximum_attempts=authorization.maximum_attempts,
            retry_authorized=authorization.retry_authorized,
            overwrite_existing=authorization.overwrite_existing,
            started_at=time.perf_counter(),
        )
