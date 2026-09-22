r"""Software verification of ``QuantumEspressoPlanner``.

Evidence profile: routine

Bounded artifact scope: schema-v2 manifest decoding and project composition over
existing QE integration ActionObjects.

Facet and represented meaning

The planner maps one exact JSON manifest into a nonexecuting integration-backed
``QuantumEspressoExecution``.

Intrinsic and cross-object scope

Tests cover the curated public route and complete control of selected run, source,
destination, resource, environment, and correlation values by the manifest.

VVUQ and scientific exclusions

The manifest is synthetic test data. Tests invoke no executable and establish no
numerical verification, scientific validation, production readiness, execution
authority, or human acceptance.
"""

from __future__ import annotations

from pathlib import Path

import pytest

import ksdft2effmass.simulations.quantumespresso as qe_simulations
from ksdft2effmass.simulations.quantumespresso import (
    QuantumEspressoExecution,
    QuantumEspressoExecutionRequest,
    QuantumEspressoPlanner,
)

pytestmark = pytest.mark.software_verification
SUT = QuantumEspressoPlanner


class TestQuantumEspressoPlanner:
    """Own maintained software evidence for manifest-driven QE composition."""

    @staticmethod
    def manifest() -> Path:
        """Return the exact maintained synthetic schema-v2 manifest."""
        return (
            Path(__file__).parent / "resources" / "execution-manifest-v2.json"
        ).resolve()

    def test_public_api__package__exports_only_generic_execution_names(self) -> None:
        """Evidence ID: SV-QE-PLANNER-001

        Requirement: The supported execution surface uses generic QE names rather
        than one public type family per example and scientific setting.

        Method: Inspect the curated ``simulations.quantumespresso`` package route.

        Oracle: The three exact public classes selected by the operator.

        Acceptance: The package attributes are the imported classes and the replaced
        example01-specific names are absent.

        Interpretation: Example details are data rather than public Python types.

        Limitations: Other established build, identity, and pseudopotential exports
        remain outside this execution-surface assertion.
        """
        assert qe_simulations.QuantumEspressoExecution is QuantumEspressoExecution
        assert (
            qe_simulations.QuantumEspressoExecutionRequest
            is QuantumEspressoExecutionRequest
        )
        assert qe_simulations.QuantumEspressoPlanner is SUT
        assert not hasattr(
            qe_simulations, "QuantumEspressoExample01SiliconScfExecution"
        )
        assert not hasattr(
            qe_simulations, "QuantumEspressoExample01SiliconScfExecutionPlanner"
        )
        assert not hasattr(
            qe_simulations, "QuantumEspressoExample01SiliconScfExecutionRequest"
        )

    def test_method__execute__maps_manifest_to_integration_composition(self) -> None:
        """Evidence ID: SV-QE-PLANNER-002

        Requirement: One JSON manifest controls the complete selected composition
        while native mechanics remain integration-owned.

        Method: Plan the maintained synthetic manifest without invoking its Workflow.

        Oracle: Literal manifest values and exact integration owner types.

        Acceptance: Decision evidence, generic Workflow authority reference, run,
        path, arguments, environment, limits, and destinations equal their
        manifest-defined values; direct Workflow execution is blocked.

        Interpretation: The planner represents composition without creating an
        authority-bypassing path to staging or process entry.

        Limitations: Generic Workflow authorization, claim, dispatch, and effect-port
        behavior remain outside this planner test.
        """
        execution = SUT().execute(
            QuantumEspressoExecutionRequest(manifest_path=self.manifest())
        )
        request = execution.plan.preparation_request
        local_plan = execution.local_execution_plan

        assert type(execution) is QuantumEspressoExecution
        assert execution.plan.manifest_schema_identity == (
            "quantum-espresso-execution-manifest:v2.20260921T155105Z"
        )
        assert execution.plan.run_identity.task_id == (
            "quantumespresso.simulations.qe_examples.pw.example01"
        )
        assert execution.plan.run_identity.release == "7.2"
        assert execution.plan.development_decision_id == (
            "QE-7-2-EXAMPLE01-SI-SCF-HC01"
        )
        assert execution.plan.authority_reference.grant_identity.value == (
            "grant.example01.001"
        )
        assert execution.plan.authority_reference.snapshot_identity.value == (
            "authority.snapshot.example01.001"
        )
        assert local_plan.preparation_request is request
        assert local_plan.workflow_run_identity.value == "workflow-run.example01"
        assert local_plan.obligation_identity.value == "obligation.example01"
        assert local_plan.dispatch_entry_identity.value == "dispatch-entry.example01"
        assert local_plan.dispatch_outcome_identity.value == (
            "dispatch-outcome.example01"
        )
        assert tuple(
            candidate.role.value
            for candidate in local_plan.extraction_specification.candidates
        ) == ("stderr", "stdout")
        assert execution.plan.workspace == Path(
            "/synthetic/ksdft2effmass-runs/simulations/quantumespresso/"
            "qe_examples/pw/example01/v7-2/20260921T120325Z"
        )
        assert request.executable_configuration.argument_suffix == (
            "-in",
            "input/si.scf.david.in",
        )
        assert request.executable_configuration.environment_additions == (
            ("OMP_NUM_THREADS", "1"),
        )
        assert request.limits.wall_time_milliseconds == 360_000
        assert request.stdout_destination.value == "streams/si.scf.david.out"
        with pytest.raises(RuntimeError, match="authorized Workflow dispatch"):
            execution.workflow.execute(execution.plan)

    def test_method__execute__rejects_legacy_manifest_without_authority_binding(
        self, tmp_path: Path
    ) -> None:
        """Evidence ID: SV-QE-PLANNER-003

        Requirement: New execution planning requires explicit decision evidence and a
        generic Workflow grant reference rather than a legacy correlation string alone.

        Method: Change only the maintained synthetic manifest version to one.

        Oracle: The accepted schema-v2 manifest contract.

        Acceptance: Planning rejects the legacy version before constructing execution
        composition or performing an external effect.

        Interpretation: Future manifests cannot silently omit the authority binding.

        Limitations: Rejection does not authenticate or issue the referenced grant.
        """
        path = tmp_path / "legacy-manifest.json"
        path.write_bytes(
            self.manifest()
            .read_bytes()
            .replace(b'"schema_version": 2', b'"schema_version": 1', 1)
        )

        with pytest.raises(ValueError, match="schema_version must equal 2"):
            SUT().execute(QuantumEspressoExecutionRequest(manifest_path=path))

    def test_method__execute__missing_authority_performs_no_effect(
        self, tmp_path: Path
    ) -> None:
        """Evidence ID: SV-QE-PLANNER-004

        Requirement: A manifest missing authority correlation must fail before any
        external workspace or process effect.

        Method: Remove the complete authority member from the maintained synthetic
        manifest and redirect its external root into the isolated test directory.

        Oracle: Schema-v2 requires the exact authority member before composition.

        Acceptance: Planning rejects the manifest and the named external root does
        not exist afterward.

        Interpretation: Missing authority cannot reach QE preparation or process
        entry through the planning boundary.

        Limitations: This verifies structural presence, not grant authentication.
        """
        external_root = tmp_path / "external-runs"
        authority = b"""  "authority": {
    "development_decision_id": "QE-7-2-EXAMPLE01-SI-SCF-HC01",
    "grant_identity": "grant.example01.001",
    "grant_revision_identity": "grant.example01.001.revision.001",
    "snapshot_identity": "authority.snapshot.example01.001",
    "state_identity": "authority.state.example01.unused"
  },
"""
        payload = self.manifest().read_bytes()
        assert authority in payload
        payload = payload.replace(
            b"/synthetic/ksdft2effmass-runs", str(external_root).encode("utf-8"), 1
        ).replace(authority, b"", 1)
        path = tmp_path / "missing-authority.json"
        path.write_bytes(payload)

        with pytest.raises(ValueError, match="manifest must contain exactly"):
            SUT().execute(QuantumEspressoExecutionRequest(manifest_path=path))

        assert not external_root.exists()

    def test_method__execute__rejects_unknown_dated_v2_identity(
        self, tmp_path: Path
    ) -> None:
        """Evidence ID: SV-QE-PLANNER-005

        Requirement: The major schema number must not admit an unidentified dated
        revision of the execution-manifest contract.

        Method: Replace only the accepted dated schema identity in the maintained
        synthetic manifest.

        Oracle: The exact human-authorized ``v2.YYYYMMDDTHHMMSSZ`` identity.

        Acceptance: Planning rejects the unknown identity before composition.

        Interpretation: Dated v2 revisions remain explicit closed contracts.

        Limitations: This does not define compatibility with any future revision.
        """
        path = tmp_path / "unknown-dated-schema.json"
        path.write_bytes(
            self.manifest()
            .read_bytes()
            .replace(
                b"v2.20260921T155105Z",
                b"v2.20260921T155106Z",
                1,
            )
        )

        with pytest.raises(ValueError, match="schema_identity must equal"):
            SUT().execute(QuantumEspressoExecutionRequest(manifest_path=path))
