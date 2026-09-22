r"""Software verification of ``QuantumEspressoBundledExampleRunIdentity``.

Evidence profile: routine

Bounded artifact scope: the public Task-derived bundled-example run identity and
relative workspace hierarchy.

Facet and represented meaning

The class represents one explicit canonical simulation Task, QE release, and UTC
workspace-creation time as portable identity and path values.

Intrinsic and cross-object scope

Tests cover exact public export, immutable fields, lexical invariants, UTC precision,
canonical identity text, generic Workflow adaptation, and directory decomposition.
Filesystem creation, collision observation, and execution preparation are separate.

VVUQ and scientific exclusions

These tests establish exact software behavior only.  They perform no Quantum ESPRESSO
execution and establish no numerical verification, scientific validation, uncertainty
quantification, cross-version compatibility, or execution authority.
"""

from __future__ import annotations

from dataclasses import FrozenInstanceError
from datetime import UTC, datetime, timedelta, timezone
from pathlib import PurePosixPath

import pytest

import ksdft2effmass.simulations.quantumespresso as qe_simulations
from ksdft2effmass.integration.quantum_espresso import (
    LocalQuantumEspressoAttemptWorkspaceName,
)
from ksdft2effmass.simulations.quantumespresso import (
    QuantumEspressoBundledExampleRunIdentity,
)
from ksdft2effmass.workflows import WorkflowRunIdentity

pytestmark = pytest.mark.software_verification
SUT = QuantumEspressoBundledExampleRunIdentity


class TestQuantumEspressoBundledExampleRunIdentity:
    """Own this class's maintained software-verification evidence."""

    @staticmethod
    def valid_timestamp() -> datetime:
        """Return one exact UTC timestamp for this module's tests."""
        return datetime(2026, 9, 21, 1, 40, 18, tzinfo=UTC)

    def test_public_api__package__exports_run_identity(self) -> None:
        """Evidence ID: SV-QE-BUNDLED-RUN-001

        Requirement: The QE Workflow simulation package exports the canonical run
        identity.

        Acceptance: The package export is the exact class defined by the simulation
        run-identity module.
        """
        assert qe_simulations.QuantumEspressoBundledExampleRunIdentity is SUT
        assert SUT.__module__ == (
            "ksdft2effmass.simulations.quantumespresso.run_identity"
        )

    def test_property__canonical_identity__maps_task_release_and_timestamp(
        self,
    ) -> None:
        """Evidence ID: SV-QE-BUNDLED-RUN-002

        Requirement: One valid Task, release, and UTC timestamp map exactly to the
        approved portable identity and nested relative workspace hierarchy.

        Acceptance: All derived public values equal their explicit contract literals.
        """
        value = SUT(
            task_id="quantumespresso.simulations.qe_examples.pw.example01",
            release="7.2",
            workspace_created_at=self.valid_timestamp(),
        )
        expected = (
            "quantumespresso.simulations.qe_examples.pw.example01.v7-2.20260921T014018Z"
        )

        assert value.version_segment == "v7-2"
        assert value.timestamp_segment == "20260921T014018Z"
        assert value.value == expected
        assert value.workflow_run_identity == WorkflowRunIdentity(expected)
        assert value.relative_parent_path == PurePosixPath(
            "simulations/quantumespresso/qe_examples/pw/example01/v7-2"
        )
        assert value.attempt_workspace_name == (
            LocalQuantumEspressoAttemptWorkspaceName("20260921T014018Z")
        )
        assert value.relative_workspace_path == PurePosixPath(
            "simulations/quantumespresso/qe_examples/pw/example01/v7-2/20260921T014018Z"
        )

    def test_property__release_regression__creates_sibling_version_hierarchies(
        self,
    ) -> None:
        """Evidence ID: SV-QE-BUNDLED-RUN-003

        Requirement: Distinct QE releases of one example retain the same Task path and
        distinct release segments without merging the runs.

        Acceptance: QE 7.2, 7.2.1, and 7.5 identities differ exactly at their version
        segment and produce distinct sibling parent paths.
        """
        task_id = "quantumespresso.simulations.qe_examples.pw.example01"
        version_7_2 = SUT(task_id, "7.2", self.valid_timestamp())
        version_7_2_1 = SUT(task_id, "7.2.1", self.valid_timestamp())
        version_7_5 = SUT(task_id, "7.5", self.valid_timestamp())

        assert version_7_2.value == f"{task_id}.v7-2.20260921T014018Z"
        assert version_7_2_1.value == f"{task_id}.v7-2-1.20260921T014018Z"
        assert version_7_5.value == f"{task_id}.v7-5.20260921T014018Z"
        assert version_7_2.relative_parent_path.parent == (
            version_7_5.relative_parent_path.parent
        )
        assert version_7_2.relative_parent_path.name == "v7-2"
        assert version_7_2_1.relative_parent_path.name == "v7-2-1"
        assert version_7_5.relative_parent_path.name == "v7-5"

    def test_constructor__immutability__rejects_field_assignment(self) -> None:
        """Evidence ID: SV-QE-BUNDLED-RUN-004

        Requirement: Run-identity inputs remain immutable after construction.

        Acceptance: Ordinary assignment raises ``FrozenInstanceError``.
        """
        value = SUT(
            "quantumespresso.simulations.qe_examples.pw.example01",
            "7.2",
            self.valid_timestamp(),
        )
        with pytest.raises(FrozenInstanceError):
            value.release = "7.5"  # type: ignore[misc]

    def test_constructor__semantic_types__rejects_wrong_field_types(self) -> None:
        """Evidence ID: SV-QE-BUNDLED-RUN-005

        Requirement: Task identity, release, and timestamp reject implicit coercion.

        Acceptance: Each wrong semantic type raises ``TypeError`` at construction.
        """
        with pytest.raises(TypeError):
            SUT(7, "7.2", self.valid_timestamp())  # type: ignore[arg-type]
        with pytest.raises(TypeError):
            SUT(
                "quantumespresso.simulations.qe_examples.pw.example01",
                7.2,  # type: ignore[arg-type]
                self.valid_timestamp(),
            )
        with pytest.raises(TypeError):
            SUT(
                "quantumespresso.simulations.qe_examples.pw.example01",
                "7.2",
                "20260921T014018Z",  # type: ignore[arg-type]
            )

    @pytest.mark.parametrize(
        "task_id",
        [
            pytest.param(
                "quantumespresso.simulations.qe_examples.pw",
                id="missing_example",
            ),
            pytest.param(
                "quantumespresso.simulations.qe_examples.review",
                id="campaign_review",
            ),
            pytest.param(
                "quantumespresso.simulations.qe_examples.pw.example01.extra",
                id="extra_segment",
            ),
            pytest.param(
                "wannier90.tutorials.v3_1_0.example01",
                id="different_campaign",
            ),
            pytest.param(
                "quantumespresso.simulations.qe_examples.PW.example01",
                id="uppercase_component",
            ),
            pytest.param(
                "quantumespresso.simulations.qe_examples.pw.example/01",
                id="path_separator",
            ),
        ],
    )
    def test_constructor__task_id__rejects_non_example_identities(
        self, task_id: str
    ) -> None:
        """Evidence ID: SV-QE-BUNDLED-RUN-006

        Requirement: The naming contract accepts only one canonical bundled-example
        Task identity with exact campaign, component, and example segments.

        Acceptance: Every named non-example identity raises ``ValueError``.
        """
        with pytest.raises(ValueError):
            SUT(task_id, "7.2", self.valid_timestamp())

    @pytest.mark.parametrize(
        "release",
        [
            pytest.param("", id="empty"),
            pytest.param("7", id="missing_minor"),
            pytest.param("v7.2", id="prefixed"),
            pytest.param("07.2", id="major_leading_zero"),
            pytest.param("7.02", id="minor_leading_zero"),
            pytest.param("7-2", id="preformatted"),
            pytest.param("7.2.0.1", id="too_many_components"),
        ],
    )
    def test_constructor__release__rejects_noncanonical_versions(
        self, release: str
    ) -> None:
        """Evidence ID: SV-QE-BUNDLED-RUN-007

        Requirement: QE releases use canonical two- or three-component decimal text.

        Acceptance: Every named malformed release raises ``ValueError``.
        """
        with pytest.raises(ValueError):
            SUT(
                "quantumespresso.simulations.qe_examples.pw.example01",
                release,
                self.valid_timestamp(),
            )

    @pytest.mark.parametrize(
        "workspace_created_at",
        [
            pytest.param(
                datetime(2026, 9, 21, 1, 40, 18),
                id="naive",
            ),
            pytest.param(
                datetime(
                    2026,
                    9,
                    21,
                    1,
                    40,
                    18,
                    tzinfo=timezone(timedelta(hours=8)),
                ),
                id="nonzero_offset",
            ),
            pytest.param(
                datetime(2026, 9, 21, 1, 40, 18, 1, tzinfo=UTC),
                id="subsecond",
            ),
        ],
    )
    def test_constructor__timestamp__rejects_noncanonical_utc_precision(
        self, workspace_created_at: datetime
    ) -> None:
        """Evidence ID: SV-QE-BUNDLED-RUN-008

        Requirement: The workspace timestamp is explicit UTC at whole-second
        precision.

        Acceptance: Naive, non-UTC, and subsecond values each raise ``ValueError``.
        """
        with pytest.raises(ValueError):
            SUT(
                "quantumespresso.simulations.qe_examples.pw.example01",
                "7.2",
                workspace_created_at,
            )
