r"""Software verification of ``WorkflowRunSnapshot``.

Bounded artifact scope: complete immutable run, binding and revision record retention.

Evidence profile: claim_bearing

Facet and represented meaning

Snapshots retain the complete supplied records rather than identity-only stand-ins.

Intrinsic and cross-object scope

Only constructor typing and immutability; repositories must verify all correlations.

VVUQ and scientific exclusions

Software verification only; synthetic genesis does not establish stored presence.
"""

from dataclasses import FrozenInstanceError, replace

import pytest
from ksdft2effmass.workflows import WorkflowRun, WorkflowRunSnapshot

pytestmark = pytest.mark.software_verification
SUT = WorkflowRunSnapshot


class TestWorkflowRunSnapshot:
    """Intrinsic immutable snapshot container, not a repository or replay engine."""

    def test_constructor__fields__retains_complete_records(
        self, genesis_run: WorkflowRun, genesis_snapshot: WorkflowRunSnapshot
    ) -> None:
        """Evidence ID: SV-WFR-SNAPSHOT-001

        Requirement: A snapshot retains full run, binding and exact revision bytes.

        Method: Inspect the hand-constructed complete genesis snapshot.

        Oracle: Fixed genesis records and independent complete envelope resource.

        Acceptance: Exact run, transaction label, revision labels and bytes remain.

        Interpretation: Record construction is not evidence that a store found it.

        Limitations: Structural closure and replay equality are separate operations.
        """
        value = genesis_snapshot
        assert value.run is genesis_run
        assert value.binding.transaction_identity == "genesis-transaction"
        assert value.revision.stream_id == "run"
        assert value.revision.revision_id == "genesis"
        assert value.revision.predecessor_revision_id is None
        assert value.revision.payload.startswith(b'{"commit_binding":')
        assert value.revision.payload.endswith(
            b'"schema":"ksdft2effmass.workflow-run:1"}'
        )

    @pytest.mark.parametrize(
        "field",
        [
            pytest.param("run", id="identity_only_run"),
            pytest.param("binding", id="binding_label_only"),
            pytest.param("revision", id="revision_label_only"),
        ],
    )
    def test_constructor__types__rejects_partial_standins(
        self, genesis_snapshot: WorkflowRunSnapshot, field: str
    ) -> None:
        """Evidence ID: SV-WFR-SNAPSHOT-002

        Requirement: Snapshot fields require exact complete concrete records.

        Method: Replace each field with only its identifying string.

        Oracle: Exact declared WorkflowRun, binding and Revision types.

        Acceptance: Each identity-only stand-in raises TypeError.

        Interpretation: A snapshot cannot ordinarily be constructed from bare labels.

        Limitations: This record does not decode or verify the supplied payload.
        """
        with pytest.raises(TypeError):
            if field == "run":
                replace(genesis_snapshot, run="run")  # type: ignore[arg-type]
            elif field == "binding":
                replace(genesis_snapshot, binding="binding")  # type: ignore[arg-type]
            else:
                replace(genesis_snapshot, revision="revision")  # type: ignore[arg-type]

    @pytest.mark.parametrize(
        "field",
        [
            pytest.param("snapshot", id="snapshot_assignment"),
            pytest.param("run", id="nested_run_assignment"),
            pytest.param("binding", id="nested_binding_assignment"),
            pytest.param("revision", id="nested_revision_assignment"),
        ],
    )
    def test_field__retained_state__is_operationally_immutable(
        self, genesis_snapshot: WorkflowRunSnapshot, field: str
    ) -> None:
        """Evidence ID: SV-WFR-SNAPSHOT-003

        Requirement: Retained snapshot state cannot be rewritten through public fields.

        Method: Attempt assignment on snapshot or nested immutable records.

        Oracle: Frozen dataclass semantics on complete supplied records.

        Acceptance: Every assignment raises FrozenInstanceError.

        Interpretation: Nested retained records do not expose mutable field state.

        Limitations: Genesis has no NumPy-backed concrete result arrays.
        """
        with pytest.raises(FrozenInstanceError):
            if field == "snapshot":
                genesis_snapshot.run = genesis_snapshot.run  # type: ignore[misc]
            elif field == "run":
                genesis_snapshot.run.schema_version = 2  # type: ignore[misc]
            elif field == "binding":
                genesis_snapshot.binding.transaction_identity = "changed"  # type: ignore[misc]
            else:
                genesis_snapshot.revision.payload = b"changed"  # type: ignore[misc]
