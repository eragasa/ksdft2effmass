"""Reusable authored and protected accepted-parent Stage C Workflows."""

from __future__ import annotations

import hashlib
import os
from pathlib import Path
from typing import cast

from .authorization import (
    AcceptedParentStageCAuthorityValidator,
    AcceptedParentStageCExecutionAuthorizationDeserializer,
    StageCOperationPaths,
)
from .context import StageCResultContextPreparer
from .evaluation import AcceptedParentStageCEvaluator
from .model import (
    ArtifactBinding,
    JsonValue,
    StageCAcceptedParentExecutionAuthorization,
)
from .records import (
    AcceptedParentStageCArtifactAdapter,
    AcceptedParentStageCDesignDeserializer,
    AuthoredAcceptedParentAdapterFixtureDeserializer,
    AuthoredParentFixtureDeserializer,
    ParentJsonReader,
)
from .retention import (
    AcceptedParentStageCResultSerializer,
    StageCAttemptJournal,
    StageCProtectedOperationFinalizer,
)

STAGE_DIRECTORY = Path(__file__).resolve(strict=True).parent.parent
REPOSITORY_ROOT = STAGE_DIRECTORY.parents[2]


class AcceptedParentStageCToyWorkflow:
    """Compose adopted design, authored fixture, schedules, and serialization."""

    __slots__ = ()

    def execute(
        self, design: Path, fixture: Path, output: Path
    ) -> dict[str, JsonValue]:
        controls, design_sha256 = AcceptedParentStageCDesignDeserializer().execute(
            design
        )
        fixture_record = AuthoredParentFixtureDeserializer().execute(fixture)
        repository_root = REPOSITORY_ROOT
        identities = (
            ArtifactBinding(
                "authored_parent_fixture",
                fixture.resolve(strict=True).relative_to(repository_root).as_posix(),
                hashlib.sha256(fixture.read_bytes()).hexdigest(),
            ),
        )
        context = StageCResultContextPreparer.authored(
            (
                "research-monograph.impurity-defect-2d.stage-c."
                "accepted-parent-authored-fixture.v1"
            ),
            "authored_parent_fixture",
            identities,
        )
        result = AcceptedParentStageCEvaluator().execute(
            controls, fixture_record, design_sha256, context
        )
        AcceptedParentStageCResultSerializer.execute(result, output)
        return result


class AcceptedParentStageCAdapterFixtureWorkflow:
    """Exercise the accepted-artifact adapter with authored records only."""

    __slots__ = ()

    def execute(
        self, design: Path, fixture: Path, output: Path
    ) -> dict[str, JsonValue]:
        controls, design_sha256 = AcceptedParentStageCDesignDeserializer().execute(
            design
        )
        fixture_record, identities = (
            AuthoredAcceptedParentAdapterFixtureDeserializer().execute(fixture)
        )
        context = StageCResultContextPreparer.authored(
            (
                "research-monograph.impurity-defect-2d.stage-c."
                "accepted-parent-adapter-authored-fixture.v1"
            ),
            "authored_accepted_parent_adapter_fixture",
            identities,
        )
        result = AcceptedParentStageCEvaluator().execute(
            controls, fixture_record, design_sha256, context
        )
        AcceptedParentStageCResultSerializer.execute(result, output)
        return result


class AuthoredStageCOperationWorkflow:
    """Exercise the complete protected operation using authored records only."""

    __slots__ = ()

    def execute(
        self, design: Path, fixture: Path, output_directory: Path
    ) -> dict[str, JsonValue]:
        output_directory.mkdir(parents=True, exist_ok=True)
        outputs = StageCOperationPaths.authored(output_directory.resolve(strict=True))
        inventory = (
            AcceptedParentStageCExecutionAuthorizationDeserializer.OPERATION_INVENTORY
        )
        authorization_sha256 = hashlib.sha256(
            str(fixture.resolve(strict=True)).encode("utf-8")
        ).hexdigest()
        started = StageCAttemptJournal.start(
            outputs.attempt_record,
            "authored.nonexecuting.stage-c.complete-operation.v1",
            authorization_sha256,
            inventory,
            "authored synthetic operation fixture; not execution authority",
        )
        try:
            controls, design_sha256 = AcceptedParentStageCDesignDeserializer().execute(
                design
            )
            fixture_record, identities = (
                AuthoredAcceptedParentAdapterFixtureDeserializer().execute(fixture)
            )
            context = StageCResultContextPreparer.authored_operation(
                identities, outputs
            )
            result = AcceptedParentStageCEvaluator().execute(
                controls, fixture_record, design_sha256, context
            )
            maximum_bytes = 20 * 1024 * 1024
            AcceptedParentStageCResultSerializer.execute(
                result, outputs.result, maximum_bytes
            )
            root = REPOSITORY_ROOT
            StageCProtectedOperationFinalizer.verify_authored(
                design, fixture, outputs.result, outputs.verification_log, root
            )
            StageCProtectedOperationFinalizer.plot(
                outputs.result, outputs.summary_svg, root
            )
            StageCProtectedOperationFinalizer.report(
                outputs.result, outputs.verification_log, outputs.report
            )
            StageCProtectedOperationFinalizer.manifest(
                outputs.result,
                outputs.verification_log,
                outputs.summary_svg,
                outputs.report,
                outputs.native_evidence_manifest,
                "authored synthetic complete-operation evidence; not "
                "accepted-parent evidence",
            )
            StageCProtectedOperationFinalizer.checksums(outputs)
            StageCProtectedOperationFinalizer.validate_total_size(
                outputs, maximum_bytes
            )
            StageCAttemptJournal.succeed(
                outputs.attempt_record,
                started,
                outputs.produced_outputs()
                + (("checksum_catalog", outputs.checksum_catalog),),
            )
            return result
        except BaseException as error:
            StageCAttemptJournal.fail(outputs.attempt_record, started, error)
            raise


class AcceptedParentStageCExecutionWorkflow:
    """Compose one separately authorized accepted-parent operation."""

    __slots__ = ("_adapter", "_authority", "_json")

    def __init__(self) -> None:
        self._adapter = AcceptedParentStageCArtifactAdapter()
        self._authority = AcceptedParentStageCAuthorityValidator()
        self._json = ParentJsonReader()

    def execute(
        self,
        design: Path,
        authorization: Path,
        repository_root: Path,
        output: Path,
    ) -> dict[str, JsonValue]:
        execution = self._authority.execute(
            design, authorization, repository_root, output
        )
        authorization_sha256 = hashlib.sha256(
            execution.authorization_path.read_bytes()
        ).hexdigest()
        started = StageCAttemptJournal.start(
            execution.outputs.attempt_record,
            execution.authorization.authorization_id,
            authorization_sha256,
            execution.authorization.operation_inventory,
            "one protected accepted-parent Stage C attempt consumed",
        )
        try:
            self._authority.validate_accepted_input_identities(execution)
            context = StageCResultContextPreparer.accepted(execution)
            controls, design_sha256 = AcceptedParentStageCDesignDeserializer().execute(
                self._authority.path(execution, "accepted_parent_design")
            )
            source_roles = (
                "accepted_periodic_parent_input",
                "accepted_periodic_parent_result",
                "accepted_stage_a_prerequisite",
                "accepted_stage_b_parent_and_route_evidence",
                "accepted_execution_free_stage_c_contract",
            )
            records = tuple(
                self._json.read(self._authority.path(execution, role))
                for role in source_roles
            )
            digest = hashlib.sha256(
                "".join(
                    value.sha256
                    for value in execution.authorization.artifacts
                    if value.role in source_roles
                ).encode("ascii")
            ).hexdigest()
            fixture = self._adapter.execute(
                records[0], records[1], records[2], records[3], records[4], digest
            )
            original_directory = Path.cwd()
            try:
                os.chdir(execution.authorization.native_artifact_root)
                result = AcceptedParentStageCEvaluator().execute(
                    controls, fixture, design_sha256, context
                )
            finally:
                os.chdir(original_directory)
            self._validate_observed_resources(result, execution.authorization)
            maximum_bytes = int(
                execution.authorization.maximum_retained_output_mib * 1024.0 * 1024.0
            )
            AcceptedParentStageCResultSerializer.execute(
                result, execution.outputs.result, maximum_bytes
            )
            StageCProtectedOperationFinalizer.verify_accepted(
                execution, repository_root
            )
            StageCProtectedOperationFinalizer.plot(
                execution.outputs.result,
                execution.outputs.summary_svg,
                repository_root,
            )
            StageCProtectedOperationFinalizer.report(
                execution.outputs.result,
                execution.outputs.verification_log,
                execution.outputs.report,
            )
            StageCProtectedOperationFinalizer.manifest(
                execution.outputs.result,
                execution.outputs.verification_log,
                execution.outputs.summary_svg,
                execution.outputs.report,
                execution.outputs.native_evidence_manifest,
                "calculated numerical-verification evidence; not scientific validation",
            )
            StageCProtectedOperationFinalizer.checksums(execution.outputs)
            StageCProtectedOperationFinalizer.validate_total_size(
                execution.outputs, maximum_bytes
            )
            StageCAttemptJournal.succeed(
                execution.outputs.attempt_record,
                started,
                execution.outputs.produced_outputs()
                + (("checksum_catalog", execution.outputs.checksum_catalog),),
            )
            return result
        except BaseException as error:
            StageCAttemptJournal.fail(execution.outputs.attempt_record, started, error)
            raise

    @staticmethod
    def _validate_observed_resources(
        result: dict[str, JsonValue],
        authorization: StageCAcceptedParentExecutionAuthorization,
    ) -> None:
        provenance = cast(dict[str, JsonValue], result["provenance"])
        observation = cast(dict[str, JsonValue], provenance["execution_observation"])
        runtime = cast(float, observation["runtime_seconds"])
        peak_memory = cast(int, observation["peak_memory_bytes"])
        if runtime > authorization.maximum_runtime_seconds:
            raise TimeoutError("accepted-parent Stage C exceeded authorized runtime")
        maximum_memory = int(
            authorization.maximum_peak_memory_gib * 1024.0 * 1024.0 * 1024.0
        )
        if peak_memory > maximum_memory:
            raise MemoryError("accepted-parent Stage C exceeded authorized memory")
