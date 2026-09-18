r"""Software verification of defect-2D Stage A execution contract.

Evidence profile: routine

Bounded artifact scope: the fail-closed Stage A runner, exact authorization and
provenance binding, result overwrite protection, design-owned folding inventory,
criterion disposition, and independent-verifier command agreement.

Facet and represented meaning

The artifact represents one local synthetic Stage A command boundary and its
retained JSON result. Tests use temporary toy parent records and never invoke the
accepted periodic-2D scientific parent.

Intrinsic and cross-object scope

The cases cover authorization rejection, canonical paths, runner/verifier command
composition, design-case enforcement, negative criterion retention, and output
immutability.

VVUQ and scientific exclusions

This is software verification with synthetic toy data. It establishes no numerical
verification of the accepted parent, scientific validation, uncertainty
quantification, material claim, resource measurement, or Stage A execution authority.
"""

from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path
from typing import cast

import pytest

type JsonValue = (
    None | bool | int | float | str | list[JsonValue] | dict[str, JsonValue]
)

pytestmark = pytest.mark.software_verification


class TestStageAExecutionContract:
    """Own software verification of the Stage A command artifact."""

    @staticmethod
    def repository_source_root() -> Path:
        """Return the repository containing the maintained Stage A scripts.

        Evidence ID: Helper owns no identifier.

        Requirement: Locate immutable source inputs for temporary command copies.

        Acceptance: Return the repository root derived from this maintained module.
        """
        return Path(__file__).resolve().parents[6]

    @staticmethod
    def sha256(path: Path) -> str:
        """Return one file's SHA-256 identity for test-owned bindings.

        Evidence ID: Helper owns no identifier.

        Requirement: Support exact temporary authorization identities.

        Acceptance: Return the lowercase hexadecimal SHA-256 digest.
        """
        return hashlib.sha256(path.read_bytes()).hexdigest()

    @staticmethod
    def write_json(path: Path, payload: dict[str, JsonValue]) -> None:
        """Write one deterministic test-owned JSON resource.

        Evidence ID: Helper owns no identifier.

        Requirement: Support canonical temporary command inputs.

        Acceptance: Write sorted, indented UTF-8 JSON with one final newline.
        """
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )

    @staticmethod
    def read_json(path: Path) -> dict[str, JsonValue]:
        """Read a temporary JSON record through the closed test representation.

        Evidence ID: Helper owns no identifier.

        Requirement: Avoid erased JSON values in maintained tests.

        Acceptance: Return a JSON object or fail at the exact representation boundary.
        """
        value = cast(JsonValue, json.loads(path.read_text(encoding="utf-8")))
        if not isinstance(value, dict):
            raise TypeError("test JSON root must be an object")
        return value

    @classmethod
    def make_toy_repository(
        cls, tmp_path: Path, *, algebraic_tolerance: float = 1.0e-11
    ) -> tuple[Path, Path, Path, Path, Path]:
        """Create an isolated toy command repository without accepted parent data.

        Evidence ID: Helper owns no identifier.

        Requirement: Supply deterministic software-only command inputs.

        Acceptance: Return root, runner, verifier, authorization, and result paths.
        """
        root = (tmp_path / "toy-repository").resolve()
        stage_relative = Path("calculations/research-monograph/impurity-defect-2d")
        stage = root / stage_relative
        stage.mkdir(parents=True)
        source_stage = (
            cls.repository_source_root()
            / "calculations/research-monograph/impurity-defect-2d"
        )
        runner = stage / "run_stage_a.py"
        verifier = stage / "verify_stage_a.py"
        shutil.copy2(source_stage / "run_stage_a.py", runner)
        shutil.copy2(source_stage / "verify_stage_a.py", verifier)
        (stage / "protocol.md").write_text("synthetic protocol\n", encoding="utf-8")
        (stage / "preflight.md").write_text("synthetic preflight\n", encoding="utf-8")

        parent_relative = Path(
            "calculations/research-monograph/periodic-2d/result.json"
        )
        parent = root / parent_relative
        cls.write_json(
            parent,
            {
                "coupling_continuation": [
                    {
                        "lambda_xy": 0.0,
                        "hopping_coefficients": [
                            {"rx": 0, "ry": 0, "real": 0.2, "imag": 0.0},
                            {"rx": 1, "ry": 0, "real": -0.1, "imag": 0.0},
                            {"rx": -1, "ry": 0, "real": -0.1, "imag": 0.0},
                            {"rx": 0, "ry": 1, "real": -0.08, "imag": 0.0},
                            {"rx": 0, "ry": -1, "real": -0.08, "imag": 0.0},
                        ],
                    }
                ]
            },
        )
        design = stage / "study-design.json"
        pristine: dict[str, JsonValue] = {
            "geometry": [2, 2],
            "boundary_phase_turns": [0.0, 0.0],
            "site_map_known": True,
            "energy_reference_relation_known": True,
        }
        incompatible: list[JsonValue] = [
            {
                "control": "incorrect_supercell_geometry",
                "pristine": pristine,
                "candidate": {
                    **pristine,
                    "geometry": [3, 2],
                    "boundary_phase_turns": [0.5, 0.0],
                },
                "expected_issue_code": "DEFECT_2D.GEOMETRY_MISMATCH",
            },
            {
                "control": "incorrect_boundary_phase",
                "pristine": pristine,
                "candidate": {
                    **pristine,
                    "boundary_phase_turns": [0.5, 0.0],
                },
                "expected_issue_code": "DEFECT_2D.BOUNDARY_PHASE_MISMATCH",
            },
            {
                "control": "lost_site_correspondence",
                "pristine": pristine,
                "candidate": {**pristine, "site_map_known": False},
                "expected_issue_code": "DEFECT_2D.SITE_MAP_UNRESOLVED",
            },
            {
                "control": "unknown_energy_reference",
                "pristine": pristine,
                "candidate": {
                    **pristine,
                    "energy_reference_relation_known": False,
                },
                "expected_issue_code": "DEFECT_2D.ENERGY_REFERENCE_UNKNOWN",
            },
        ]
        cls.write_json(
            design,
            {
                "schema_version": 1,
                "study_id": "synthetic.defect-2d.stage-a.software-test",
                "design_status": "frozen_human_accepted_for_implementation",
                "execution_authorized_by_this_record": False,
                "parent_sources": {
                    "periodic_2d_scalar_result_path": parent_relative.as_posix(),
                    "periodic_2d_scalar_result_sha256": cls.sha256(parent),
                },
                "represented_spaces": {
                    "scalar_parent": {"hopping_maximum_squared_radius": 1}
                },
                "folding_controls": {
                    "supercell_shapes": [[2, 2]],
                    "boundary_phase_turns": [[0.0, 0.0], [0.37, -0.23]],
                    "seam_phase_oracle": {
                        "size": 6,
                        "twist_turns": 0.37,
                        "noncrossing_source": 0,
                        "positive_crossing_source": 5,
                        "positive_displacement": 1,
                        "negative_crossing_source": 0,
                        "negative_displacement": -1,
                    },
                },
                "alignment_attacks": {
                    "translation_cells": [1, 1],
                    "site_phase_steps_radians": [0.137, -0.191],
                    "energy_reference_shift": 0.137,
                },
                "tolerances": {
                    "algebraic_absolute": algebraic_tolerance,
                    "folding_unitarity": algebraic_tolerance,
                    "independent_reconstruction_relative": 1.0e-10,
                },
                "stage_a_incompatible_controls": incompatible,
            },
        )
        checkpoint_relative = Path(
            ".pi/checkpoints/synthetic-defect-2d-stage-a-execution.json"
        )
        checkpoint = root / checkpoint_relative
        human_response = "synthetic software-test execution only"
        cls.write_json(
            checkpoint,
            {
                "status": "resolved",
                "task_id": "research-monograph.exercises.impurity.defect-2d",
                "human_response": human_response,
                "authorized_scope": "Run only the temporary synthetic toy command.",
                "blocked_scope": "Accepted parent and scientific execution excluded.",
                "authoritative_files": [
                    (stage_relative / "preflight.md").as_posix(),
                    (stage_relative / "protocol.md").as_posix(),
                    (stage_relative / "run_stage_a.py").as_posix(),
                    (stage_relative / "study-design.json").as_posix(),
                ],
            },
        )
        authorization = stage / "synthetic-execution-authorization.json"
        result = stage / "synthetic-stage-a-result.json"
        cls.write_json(
            authorization,
            {
                "schema_version": 2,
                "authorization_kind": "defect-2d-stage-execution",
                "authorization_id": "synthetic-test-stage-a",
                "stage_id": "A_null_and_folding",
                "execution_authorized": True,
                "checkpoint_path": checkpoint_relative.as_posix(),
                "checkpoint_sha256": cls.sha256(checkpoint),
                "repository_root": str(root),
                "design_path": (stage_relative / "study-design.json").as_posix(),
                "design_sha256": cls.sha256(design),
                "runner_path": (stage_relative / "run_stage_a.py").as_posix(),
                "runner_sha256": cls.sha256(runner),
                "parent_path": parent_relative.as_posix(),
                "parent_sha256": cls.sha256(parent),
                "output_path": (stage_relative / result.name).as_posix(),
                "resource_envelope": {
                    "maximum_matrix_dimension": 4,
                    "maximum_runtime_seconds": 30,
                    "maximum_peak_memory_gib": 0.25,
                    "network_access": False,
                },
                "human_response_verbatim": human_response,
            },
        )
        return root, runner, verifier, authorization, result

    @staticmethod
    def assert_canonical_relative_path(value: JsonValue) -> None:
        """Assert one retained path uses canonical repository-relative spelling.

        Evidence ID: Helper owns no identifier.

        Requirement: Support explicit provenance assertions without hidden cases.

        Acceptance: The value is a relative string without parent traversal.
        """
        assert isinstance(value, str)
        assert not Path(value).is_absolute()
        assert ".." not in Path(value).parts

    @staticmethod
    def run_command(*arguments: str) -> subprocess.CompletedProcess[str]:
        """Run one temporary Python command and capture deterministic streams.

        Evidence ID: Helper owns no identifier.

        Requirement: Keep process effects explicit and local to ``tmp_path``.

        Acceptance: Return the completed process without implicit success checking.
        """
        return subprocess.run(
            (sys.executable, *arguments),
            check=False,
            capture_output=True,
            text=True,
        )

    @classmethod
    def run_stage_a(
        cls,
        root: Path,
        runner: Path,
        authorization: Path,
        result: Path,
    ) -> subprocess.CompletedProcess[str]:
        """Invoke the temporary toy runner through its public CLI.

        Evidence ID: Helper owns no identifier.

        Requirement: Exercise the exact command boundary used by evidence owners.

        Acceptance: Return the process outcome for caller-owned assertions.
        """
        return cls.run_command(
            str(runner),
            "--design",
            "calculations/research-monograph/impurity-defect-2d/study-design.json",
            "--execution-authorization",
            str(authorization.relative_to(root)),
            "--repository-root",
            str(root),
            "--output",
            str(result.relative_to(root)),
        )

    def test_artifact__authorization__rejects_unbound_design_digest(
        self, tmp_path: Path
    ) -> None:
        """Evidence ID: SV-RM-D2A-001

        Requirement: Stage A refuses an authorization that does not bind the exact
        accepted design bytes.

        Acceptance: The command exits nonzero, reports the digest mismatch, and writes
        no result.
        """
        root, runner, _, authorization, result = self.make_toy_repository(tmp_path)
        payload = self.read_json(authorization)
        payload["design_sha256"] = "0" * 64
        self.write_json(authorization, payload)
        completed = self.run_stage_a(root, runner, authorization, result)
        assert completed.returncode != 0
        assert "authorization digest binding differs" in completed.stderr
        assert not result.exists()

    def test_artifact__authorization__rejects_malformed_record(
        self, tmp_path: Path
    ) -> None:
        """Evidence ID: SV-RM-D2A-002

        Requirement: Stage A refuses an authorization missing one mandatory immutable
        binding rather than supplying a default.

        Acceptance: Removing the checkpoint digest produces a nonzero exit and no
        result.
        """
        root, runner, _, authorization, result = self.make_toy_repository(tmp_path)
        payload = self.read_json(authorization)
        del payload["checkpoint_sha256"]
        self.write_json(authorization, payload)
        completed = self.run_stage_a(root, runner, authorization, result)
        assert completed.returncode != 0
        assert not result.exists()

    def test_artifact__paths__rejects_parent_traversal(self, tmp_path: Path) -> None:
        """Evidence ID: SV-RM-D2A-003

        Requirement: Authorization paths cannot escape or traverse the canonical
        repository root even when a target could otherwise resolve.

        Acceptance: A traversing design binding produces a nonzero exit and no result.
        """
        root, runner, _, authorization, result = self.make_toy_repository(tmp_path)
        payload = self.read_json(authorization)
        payload["design_path"] = (
            "calculations/research-monograph/impurity-defect-2d/../"
            "impurity-defect-2d/study-design.json"
        )
        self.write_json(authorization, payload)
        completed = self.run_stage_a(root, runner, authorization, result)
        assert completed.returncode != 0
        assert "must be canonical repository-relative" in completed.stderr
        assert not result.exists()

    def test_artifact__provenance__retains_canonical_paths_and_verifies_toy_result(
        self, tmp_path: Path
    ) -> None:
        """Evidence ID: SV-RM-D2A-004

        Requirement: A fully bound toy execution retains canonical repository-relative
        provenance and is consumable by the independently implemented verifier.

        Acceptance: Both commands succeed, retained paths contain neither absolute nor
        parent traversal syntax, and reconstruction and criteria report PASS.
        """
        root, runner, verifier, authorization, result = self.make_toy_repository(
            tmp_path
        )
        executed = self.run_stage_a(root, runner, authorization, result)
        assert executed.returncode == 0, executed.stderr
        payload = self.read_json(result)
        provenance = payload["provenance"]
        assert isinstance(provenance, dict)
        self.assert_canonical_relative_path(provenance["design_path"])
        self.assert_canonical_relative_path(provenance["parent_path"])
        self.assert_canonical_relative_path(provenance["authorization_path"])
        self.assert_canonical_relative_path(provenance["checkpoint_path"])
        self.assert_canonical_relative_path(provenance["script_path"])
        stops = payload["structured_stops"]
        assert isinstance(stops, list) and stops
        first_stop = stops[0]
        assert isinstance(first_stop, dict)
        assert first_stop["issue_code"] == "DEFECT_2D.GEOMETRY_MISMATCH"
        verified = self.run_command(
            str(verifier),
            "--result",
            str(result.relative_to(root)),
            "--repository-root",
            str(root),
        )
        assert verified.returncode == 0, verified.stderr
        assert "defect_2d_stage_a_reconstruction=PASS" in verified.stdout
        assert "defect_2d_stage_a_criteria=PASS" in verified.stdout

    def test_artifact__verification__rejects_substituted_folding_case(
        self, tmp_path: Path
    ) -> None:
        """Evidence ID: SV-RM-D2A-005

        Requirement: Verification enforces the exact design-owned folding case order,
        shapes, and twists rather than accepting any equal-sized result inventory.

        Acceptance: Mutating one retained twist causes a nonzero verifier exit with the
        exact design-mismatch diagnostic.
        """
        root, runner, verifier, authorization, result = self.make_toy_repository(
            tmp_path
        )
        executed = self.run_stage_a(root, runner, authorization, result)
        assert executed.returncode == 0, executed.stderr
        payload = self.read_json(result)
        cases = payload["cases"]
        assert isinstance(cases, list) and cases
        first = cases[0]
        assert isinstance(first, dict)
        first["boundary_phase_turns"] = [0.125, 0.0]
        self.write_json(result, payload)
        verified = self.run_command(
            str(verifier),
            "--result",
            str(result.relative_to(root)),
            "--repository-root",
            str(root),
        )
        assert verified.returncode != 0
        assert "differs from the accepted design" in verified.stderr

    def test_artifact__verification__rejects_mutated_seam_sign(
        self, tmp_path: Path
    ) -> None:
        """Evidence ID: SV-RM-D2A-006

        Requirement: Verification independently enforces the positive- and
        negative-crossing seam-phase signs.

        Acceptance: Reversing the retained positive-crossing imaginary sign causes a
        nonzero independent-verifier exit.
        """
        root, runner, verifier, authorization, result = self.make_toy_repository(
            tmp_path
        )
        executed = self.run_stage_a(root, runner, authorization, result)
        assert executed.returncode == 0, executed.stderr
        payload = self.read_json(result)
        seam = payload["seam_phase_oracle"]
        assert isinstance(seam, dict)
        cases = seam["cases"]
        assert isinstance(cases, list)
        positive = cases[1]
        assert isinstance(positive, dict)
        imaginary = positive["imag"]
        assert isinstance(imaginary, int | float) and not isinstance(imaginary, bool)
        positive["imag"] = -float(imaginary)
        self.write_json(result, payload)
        verified = self.run_command(
            str(verifier),
            "--result",
            str(result.relative_to(root)),
            "--repository-root",
            str(root),
        )
        assert verified.returncode != 0
        assert "Not equal to tolerance" in verified.stderr

    def test_artifact__criteria__retains_reconstructed_failure(
        self, tmp_path: Path
    ) -> None:
        """Evidence ID: SV-RM-D2A-007

        Requirement: Independently reproduced criterion failure remains a verified
        negative result rather than becoming a reconstruction error.

        Acceptance: With a deliberately sub-roundoff tolerance, runner and verifier
        succeed, the result status is ``fail``, and verifier reports reconstruction
        PASS with criteria FAIL.
        """
        root, runner, verifier, authorization, result = self.make_toy_repository(
            tmp_path, algebraic_tolerance=1.0e-30
        )
        executed = self.run_stage_a(root, runner, authorization, result)
        assert executed.returncode == 0, executed.stderr
        payload = self.read_json(result)
        criterion = payload["criterion_evaluation"]
        assert isinstance(criterion, dict)
        assert criterion["status"] == "fail"
        failures = criterion["failed_criteria"]
        assert isinstance(failures, list) and failures
        verified = self.run_command(
            str(verifier),
            "--result",
            str(result.relative_to(root)),
            "--repository-root",
            str(root),
        )
        assert verified.returncode == 0, verified.stderr
        assert "defect_2d_stage_a_reconstruction=PASS" in verified.stdout
        assert "defect_2d_stage_a_criteria=FAIL" in verified.stdout

    def test_artifact__persistence__refuses_result_overwrite(
        self, tmp_path: Path
    ) -> None:
        """Evidence ID: SV-RM-D2A-008

        Requirement: Stage A never overwrites an existing result path.

        Acceptance: The first toy command succeeds; the second exits nonzero with the
        overwrite diagnostic and leaves result bytes unchanged.
        """
        root, runner, _, authorization, result = self.make_toy_repository(tmp_path)
        first = self.run_stage_a(root, runner, authorization, result)
        assert first.returncode == 0, first.stderr
        retained = result.read_bytes()
        second = self.run_stage_a(root, runner, authorization, result)
        assert second.returncode != 0
        assert "refusing to overwrite" in second.stderr
        assert result.read_bytes() == retained
