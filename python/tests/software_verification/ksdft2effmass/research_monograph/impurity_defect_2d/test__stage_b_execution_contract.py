r"""Software verification of defect-2D Stage B multi-route execution contract.

Evidence profile: routine

Bounded artifact scope: the execution-free multi-route toy path, retained
route/schedule/candidate data, independent verifier, deterministic SVG plotter,
mutation detection, overwrite refusal, and accepted-parent execution gate.

Facet and represented meaning

The artifact represents two finite-matrix gauge routes, one explicit bridge,
two execution orders, and their data-complete retained JSON form. Every test uses
authored nearest-neighbour toy coefficients and never reads the accepted parent.

Intrinsic and cross-object scope

The artifact owns command boundaries, retained data, independent reconstruction,
plot serialization, and their cross-script agreement. It excludes production
scientific inputs and external execution.

VVUQ and scientific exclusions

This is software verification using synthetic test data. It establishes no
accepted-parent numerical result, physical order effect, material validation,
uncertainty quantification, execution authority, publication, or release status.
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


class TestStageBExecutionContract:
    """Own software verification of the multi-route Stage B artifacts."""

    @staticmethod
    def repository_root() -> Path:
        """Return the repository containing the maintained Stage B scripts.

        Evidence ID: Helper owns no identifier.

        Requirement: Locate immutable script inputs.

        Method: Exercise the maintained artifact with authored toy data and compare
        the retained or process behavior with the declared contract.

        Oracle: The frozen multi-route inventory, exact mutation, or independent
        command behavior stated by the requirement.

        Acceptance: Return the canonical repository root.
        """
        return Path(__file__).resolve().parents[6]

    @classmethod
    def scripts(cls) -> tuple[Path, Path, Path]:
        """Return runner, verifier, and plotter paths.

        Evidence ID: Helper owns no identifier.

        Requirement: Use maintained artifacts rather than copied algorithms.

        Method: Exercise the maintained artifact with authored toy data and compare
        the retained or process behavior with the declared contract.

        Oracle: The frozen multi-route inventory, exact mutation, or independent
        command behavior stated by the requirement.

        Acceptance: Return three existing paths in artifact order.
        """
        stage = (
            cls.repository_root() / "calculations/research-monograph/impurity-defect-2d"
        )
        result = (
            stage / "run_stage_b.py",
            stage / "verify_stage_b.py",
            stage / "plot_stage_b.py",
        )
        if not all(path.is_file() for path in result):
            raise FileNotFoundError("maintained Stage B script is absent")
        return result

    @staticmethod
    def sha256(path: Path) -> str:
        """Return one fixture identity.

        Evidence ID: Helper owns no identifier.
        """
        return hashlib.sha256(path.read_bytes()).hexdigest()

    @classmethod
    def make_execution_fixture(
        cls, tmp_path: Path
    ) -> tuple[Path, Path, Path, dict[str, JsonValue]]:
        """Create an isolated exact-authority fixture without accepted inputs.

        Evidence ID: Helper owns no identifier.
        """
        root = tmp_path.resolve() / "repository"
        study = root / "calculations/research-monograph/impurity-defect-2d"
        study.mkdir(parents=True)
        source_study = (
            cls.repository_root() / "calculations/research-monograph/impurity-defect-2d"
        )
        shutil.copyfile(
            source_study / "stage-b-multiroute-design.json",
            study / "stage-b-multiroute-design.json",
        )
        shutil.copyfile(source_study / "run_stage_b.py", study / "run_stage_b.py")
        shutil.copyfile(source_study / "verify_stage_b.py", study / "verify_stage_b.py")
        shutil.copyfile(source_study / "plot_stage_b.py", study / "plot_stage_b.py")
        shutil.copyfile(
            source_study / "stage-b-result.schema.json",
            study / "stage-b-result.schema.json",
        )
        shutil.copyfile(
            source_study / "stage-b-native-evidence-manifest.json",
            study / "stage-b-native-evidence-manifest.json",
        )
        (study / "parent-input.json").write_text("{}\n", encoding="utf-8")
        (study / "parent-result.json").write_text("{}\n", encoding="utf-8")
        (study / "stage-a-result.json").write_text("{}\n", encoding="utf-8")
        checkpoint = root / ".pi/checkpoints/stage-b-execution.json"
        checkpoint.parent.mkdir(parents=True)
        checkpoint.write_text(
            json.dumps(
                {
                    "status": "resolved",
                    "task_id": "research-monograph.exercises.impurity.defect-2d",
                    "normalized_decision": "WRONG_STAGE_DECISION",
                    "human_response": "fixture response",
                },
                sort_keys=True,
            )
            + "\n",
            encoding="utf-8",
        )

        relative = "calculations/research-monograph/impurity-defect-2d/"
        authorization: dict[str, JsonValue] = {
            "schema_version": 2,
            "authorization_kind": "defect-2d-stage-execution",
            "stage_id": "B_scalar_onsite_and_D4_multiroute",
            "execution_authorized": True,
            "authorization_id": "execution-free-negative-fixture",
            "checkpoint_path": ".pi/checkpoints/stage-b-execution.json",
            "checkpoint_sha256": cls.sha256(checkpoint),
            "repository_root": str(root),
            "design_path": relative + "stage-b-multiroute-design.json",
            "design_sha256": cls.sha256(study / "stage-b-multiroute-design.json"),
            "runner_path": relative + "run_stage_b.py",
            "runner_sha256": cls.sha256(study / "run_stage_b.py"),
            "verifier_path": relative + "verify_stage_b.py",
            "verifier_sha256": cls.sha256(study / "verify_stage_b.py"),
            "plotter_path": relative + "plot_stage_b.py",
            "plotter_sha256": cls.sha256(study / "plot_stage_b.py"),
            "result_schema_path": relative + "stage-b-result.schema.json",
            "result_schema_sha256": cls.sha256(study / "stage-b-result.schema.json"),
            "native_manifest_path": relative + "stage-b-native-evidence-manifest.json",
            "native_manifest_sha256": cls.sha256(
                study / "stage-b-native-evidence-manifest.json"
            ),
            "parent_input_path": relative + "parent-input.json",
            "parent_input_sha256": cls.sha256(study / "parent-input.json"),
            "parent_path": relative + "parent-result.json",
            "parent_sha256": cls.sha256(study / "parent-result.json"),
            "stage_a_result_path": relative + "stage-a-result.json",
            "stage_a_result_sha256": cls.sha256(study / "stage-a-result.json"),
            "output_path": relative + "stage-b-result.json",
            "resource_envelope": {
                "maximum_matrix_dimension": 64,
                "maximum_execution_schedules": 2,
                "maximum_known_map_route_evaluations": 72,
                "maximum_total_blind_candidate_evaluations": 2304,
                "maximum_runtime_seconds": 600,
                "maximum_peak_memory_gib": 2.0,
                "maximum_retained_output_mib": 30.0,
                "network_access": False,
            },
            "human_response_verbatim": "fixture response",
        }
        authorization_path = study / "authorization.json"
        authorization_path.write_text(
            json.dumps(authorization, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        return root, study / "run_stage_b.py", authorization_path, authorization

    @staticmethod
    def run_execution_fixture(
        root: Path, runner: Path, authorization: Path
    ) -> subprocess.CompletedProcess[str]:
        """Invoke one isolated future-execution refusal fixture.

        Evidence ID: Helper owns no identifier.
        """
        return subprocess.run(
            [
                sys.executable,
                str(runner),
                "--design",
                str(
                    root
                    / "calculations/research-monograph/impurity-defect-2d"
                    / "stage-b-multiroute-design.json"
                ),
                "--execution-authorization",
                str(authorization),
                "--repository-root",
                str(root),
                "--output",
                str(
                    root
                    / "calculations/research-monograph/impurity-defect-2d"
                    / "stage-b-result.json"
                ),
            ],
            check=False,
            capture_output=True,
            text=True,
        )

    @staticmethod
    def read_json(path: Path) -> dict[str, JsonValue]:
        """Read one closed test-owned JSON object.

        Evidence ID: Helper owns no identifier.

        Requirement: Avoid erased representations in maintained tests.

        Method: Exercise the maintained artifact with authored toy data and compare
        the retained or process behavior with the declared contract.

        Oracle: The frozen multi-route inventory, exact mutation, or independent
        command behavior stated by the requirement.

        Acceptance: Return an object or fail at the boundary.
        """
        value = cast(JsonValue, json.loads(path.read_text(encoding="utf-8")))
        if not isinstance(value, dict):
            raise TypeError("test JSON root must be an object")
        return value

    @staticmethod
    def write_json(path: Path, payload: dict[str, JsonValue]) -> None:
        """Write one deterministic mutated result.

        Evidence ID: Helper owns no identifier.

        Requirement: Support narrow verifier mutations.

        Method: Exercise the maintained artifact with authored toy data and compare
        the retained or process behavior with the declared contract.

        Oracle: The frozen multi-route inventory, exact mutation, or independent
        command behavior stated by the requirement.

        Acceptance: Write sorted UTF-8 JSON with one final newline.
        """
        path.write_text(
            json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )

    @classmethod
    def make_toy_result(cls, tmp_path: Path) -> Path:
        """Execute the maintained authored-toy path.

        Evidence ID: Helper owns no identifier.

        Requirement: Generate behavior without accepted-parent inputs.

        Method: Exercise the maintained artifact with authored toy data and compare
        the retained or process behavior with the declared contract.

        Oracle: The frozen multi-route inventory, exact mutation, or independent
        command behavior stated by the requirement.

        Acceptance: Return a new retained toy result from a successful process.
        """
        runner, _, _ = cls.scripts()
        result = tmp_path / "stage-b-toy.json"
        subprocess.run(
            [
                sys.executable,
                str(runner),
                "--execution-free-toy-output",
                str(result),
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        return result

    @classmethod
    def verify(cls, result: Path) -> subprocess.CompletedProcess[str]:
        """Run the independent verifier against a temporary result.

        Evidence ID: Helper owns no identifier.

        Requirement: Exercise the maintained verifier command boundary.

        Method: Exercise the maintained artifact with authored toy data and compare
        the retained or process behavior with the declared contract.

        Oracle: The frozen multi-route inventory, exact mutation, or independent
        command behavior stated by the requirement.

        Acceptance: Return the completed process without imposing pass status.
        """
        _, verifier, _ = cls.scripts()
        return subprocess.run(
            [
                sys.executable,
                str(verifier),
                "--result",
                str(result.resolve()),
                "--repository-root",
                str(result.parent.resolve()),
            ],
            check=False,
            capture_output=True,
            text=True,
        )

    @staticmethod
    def assert_blind_route(route_value: JsonValue) -> None:
        """Assert one route's exact two-case blind stop contract.

        Evidence ID: Helper owns no identifier.

        Requirement: Support explicit route/schedule assertions without hidden cases.

        Method: Inspect the two frozen blind records directly.

        Acceptance: Require 512/64 ambiguities and null extraction payloads.
        """
        route = cast(dict[str, JsonValue], route_value)
        blind = cast(list[JsonValue], route["blind_cases"])
        gamma = cast(dict[str, JsonValue], blind[0])
        generic = cast(dict[str, JsonValue], blind[1])
        assert gamma["ambiguity_count"] == 512
        assert generic["ambiguity_count"] == 64
        assert gamma["selected_map"] is None
        assert gamma["extracted_operator"] is None
        assert generic["selected_map"] is None
        assert generic["extracted_operator"] is None

    def test_artifact__inventory__retains_exact_data_complete_counts(
        self, tmp_path: Path
    ) -> None:
        """Retain both routes, schedules, bridges, and every blind candidate.

        Evidence ID: SV-RM-DEFECT2D-B-001

        Requirement: Data-complete output preserves the frozen inventory.

        Method: Exercise the maintained artifact with authored toy data and compare
        the retained or process behavior with the declared contract.

        Oracle: The frozen multi-route inventory, exact mutation, or independent
        command behavior stated by the requirement.

        Acceptance: Observe 72 known evaluations, 36 bridges, 2,304 candidates,
        54 known/bridge order comparisons, and six blind order comparisons.

        Interpretation: Passing establishes only the stated synthetic software
        behavior; failure identifies an artifact, oracle, or contract discrepancy.

        Limitations: The case does not execute the accepted parent or establish
        numerical verification, scientific validation, UQ, or execution authority.
        """
        payload = self.read_json(self.make_toy_result(tmp_path))
        inventory = cast(dict[str, JsonValue], payload["inventory"])
        assert inventory == {
            "execution_schedules": 2,
            "matrix_routes": 2,
            "known_map_route_evaluations": 72,
            "matched_bridge_records": 36,
            "blind_candidate_evaluations": 2304,
            "known_case_order_comparisons": 36,
            "bridge_order_comparisons": 18,
            "blind_summary_order_comparisons": 6,
        }

    def test_artifact__blind_alignment__preserves_route_and_order_dispositions(
        self, tmp_path: Path
    ) -> None:
        """Preserve exact blind ambiguity and clean order agreement.

        Evidence ID: SV-RM-DEFECT2D-B-002

        Requirement: Neither route nor schedule may select a favorable map.

        Method: Exercise the maintained artifact with authored toy data and compare
        the retained or process behavior with the declared contract.

        Oracle: The frozen multi-route inventory, exact mutation, or independent
        command behavior stated by the requirement.

        Acceptance: Both schedules retain 512/64 ambiguities, null extraction,
        and a passing overall criterion disposition.

        Interpretation: Passing establishes only the stated synthetic software
        behavior; failure identifies an artifact, oracle, or contract discrepancy.

        Limitations: The case does not execute the accepted parent or establish
        numerical verification, scientific validation, UQ, or execution authority.
        """
        payload = self.read_json(self.make_toy_result(tmp_path))
        schedules = cast(list[JsonValue], payload["schedules"])
        first = cast(dict[str, JsonValue], schedules[0])
        second = cast(dict[str, JsonValue], schedules[1])
        first_routes = cast(dict[str, JsonValue], first["routes"])
        second_routes = cast(dict[str, JsonValue], second["routes"])
        self.assert_blind_route(first_routes["A_centered_uniform"])
        self.assert_blind_route(first_routes["B_reduced_seam"])
        self.assert_blind_route(second_routes["A_centered_uniform"])
        self.assert_blind_route(second_routes["B_reduced_seam"])
        criterion = cast(dict[str, JsonValue], payload["criterion_evaluation"])
        assert criterion == {"failed_criteria": [], "status": "pass"}

    def test_artifact__independent_verification__reconstructs_toy_result(
        self, tmp_path: Path
    ) -> None:
        """Reconstruct the complete toy result through the independent script.

        Evidence ID: SV-RM-DEFECT2D-B-003

        Requirement: Verification must not trust retained metrics alone.

        Method: Exercise the maintained artifact with authored toy data and compare
        the retained or process behavior with the declared contract.

        Oracle: The frozen multi-route inventory, exact mutation, or independent
        command behavior stated by the requirement.

        Acceptance: The verifier reports reconstruction and criteria PASS.

        Interpretation: Passing establishes only the stated synthetic software
        behavior; failure identifies an artifact, oracle, or contract discrepancy.

        Limitations: The case does not execute the accepted parent or establish
        numerical verification, scientific validation, UQ, or execution authority.
        """
        completed = self.verify(self.make_toy_result(tmp_path))
        assert completed.returncode == 0, completed.stderr
        assert "defect_2d_stage_b_reconstruction=PASS" in completed.stdout
        assert "defect_2d_stage_b_criteria=PASS" in completed.stdout

    def test_artifact__bridge_mutation__is_rejected_by_verifier(
        self, tmp_path: Path
    ) -> None:
        """Reject a favorable retained bridge value after mutation.

        Evidence ID: SV-RM-DEFECT2D-B-004

        Requirement: Operator bridge values are independently reconstructed.

        Method: Exercise the maintained artifact with authored toy data and compare
        the retained or process behavior with the declared contract.

        Oracle: The frozen multi-route inventory, exact mutation, or independent
        command behavior stated by the requirement.

        Acceptance: A changed canonical bridge maximum makes verification fail.

        Interpretation: Passing establishes only the stated synthetic software
        behavior; failure identifies an artifact, oracle, or contract discrepancy.

        Limitations: The case does not execute the accepted parent or establish
        numerical verification, scientific validation, UQ, or execution authority.
        """
        payload = self.read_json(self.make_toy_result(tmp_path))
        schedules = cast(list[JsonValue], payload["schedules"])
        first = cast(dict[str, JsonValue], schedules[0])
        bridges = cast(list[JsonValue], first["bridges"])
        bridge = cast(dict[str, JsonValue], bridges[0])
        bridge["canonical_maximum_absolute"] = 0.25
        mutated = tmp_path / "mutated-bridge.json"
        self.write_json(mutated, payload)
        completed = self.verify(mutated)
        assert completed.returncode == 1
        assert "defect_2d_stage_b_reconstruction=FAIL" in completed.stdout

    def test_artifact__ambiguity_mutation__is_rejected_by_verifier(
        self, tmp_path: Path
    ) -> None:
        """Reject a changed blind map even when its count is unchanged.

        Evidence ID: SV-RM-DEFECT2D-B-005

        Requirement: Complete ambiguity identities, not only counts, are evidence.

        Method: Exercise the maintained artifact with authored toy data and compare
        the retained or process behavior with the declared contract.

        Oracle: The frozen multi-route inventory, exact mutation, or independent
        command behavior stated by the requirement.

        Acceptance: Mutating one operation name makes verification fail.

        Interpretation: Passing establishes only the stated synthetic software
        behavior; failure identifies an artifact, oracle, or contract discrepancy.

        Limitations: The case does not execute the accepted parent or establish
        numerical verification, scientific validation, UQ, or execution authority.
        """
        payload = self.read_json(self.make_toy_result(tmp_path))
        schedules = cast(list[JsonValue], payload["schedules"])
        first = cast(dict[str, JsonValue], schedules[0])
        routes = cast(dict[str, JsonValue], first["routes"])
        route = cast(dict[str, JsonValue], routes["A_centered_uniform"])
        blind = cast(
            dict[str, JsonValue], cast(list[JsonValue], route["blind_cases"])[0]
        )
        ambiguity = cast(list[JsonValue], blind["ambiguity_set"])
        first_map = cast(dict[str, JsonValue], ambiguity[0])
        first_map["operation"] = "mutated_identity"
        mutated = tmp_path / "mutated-ambiguity.json"
        self.write_json(mutated, payload)
        completed = self.verify(mutated)
        assert completed.returncode == 1
        assert "ambiguity identities" in completed.stdout

    def test_artifact__order_mutation__is_rejected_by_verifier(
        self, tmp_path: Path
    ) -> None:
        """Reject a route-order comparison relabeled as agreement.

        Evidence ID: SV-RM-DEFECT2D-B-006

        Requirement: Schedule comparison is retained independently of route passes.

        Method: Exercise the maintained artifact with authored toy data and compare
        the retained or process behavior with the declared contract.

        Oracle: The frozen multi-route inventory, exact mutation, or independent
        command behavior stated by the requirement.

        Acceptance: A false recovered-digest agreement makes verification fail.

        Interpretation: Passing establishes only the stated synthetic software
        behavior; failure identifies an artifact, oracle, or contract discrepancy.

        Limitations: The case does not execute the accepted parent or establish
        numerical verification, scientific validation, UQ, or execution authority.
        """
        payload = self.read_json(self.make_toy_result(tmp_path))
        comparison = cast(dict[str, JsonValue], payload["order_comparison"])
        known = cast(list[JsonValue], comparison["known_case_comparisons"])
        cast(dict[str, JsonValue], known[0])["same_recovered_sha256"] = False
        mutated = tmp_path / "mutated-order.json"
        self.write_json(mutated, payload)
        completed = self.verify(mutated)
        assert completed.returncode == 1
        assert "order.known[0]" in completed.stdout

    def test_artifact__svg_plot__is_deterministic_and_refuses_overwrite(
        self, tmp_path: Path
    ) -> None:
        """Render presentation data deterministically without recalculation.

        Evidence ID: SV-RM-DEFECT2D-B-007

        Requirement: The plotter reads only retained data and preserves output.

        Method: Exercise the maintained artifact with authored toy data and compare
        the retained or process behavior with the declared contract.

        Oracle: The frozen multi-route inventory, exact mutation, or independent
        command behavior stated by the requirement.

        Acceptance: Fresh outputs are byte-identical and overwrite exits nonzero.

        Interpretation: Passing establishes only the stated synthetic software
        behavior; failure identifies an artifact, oracle, or contract discrepancy.

        Limitations: The case does not execute the accepted parent or establish
        numerical verification, scientific validation, UQ, or execution authority.
        """
        result = self.make_toy_result(tmp_path)
        _, _, plotter = self.scripts()
        first = tmp_path / "first.svg"
        second = tmp_path / "second.svg"
        command = [sys.executable, str(plotter), "--result", str(result), "--output"]
        subprocess.run(
            [*command, str(first)], check=True, capture_output=True, text=True
        )
        subprocess.run(
            [*command, str(second)], check=True, capture_output=True, text=True
        )
        assert first.read_bytes() == second.read_bytes()
        assert b"Blind objective distributions" in first.read_bytes()
        refused = subprocess.run(
            [*command, str(first)], check=False, capture_output=True, text=True
        )
        assert refused.returncode != 0
        assert "refusing to overwrite" in refused.stderr

    def test_artifact__toy_output__refuses_overwrite(self, tmp_path: Path) -> None:
        """Protect retained execution-free toy evidence from replacement.

        Evidence ID: SV-RM-DEFECT2D-B-008

        Requirement: No result path may be silently overwritten.

        Method: Exercise the maintained artifact with authored toy data and compare
        the retained or process behavior with the declared contract.

        Oracle: The frozen multi-route inventory, exact mutation, or independent
        command behavior stated by the requirement.

        Acceptance: A second toy invocation fails and preserves exact bytes.

        Interpretation: Passing establishes only the stated synthetic software
        behavior; failure identifies an artifact, oracle, or contract discrepancy.

        Limitations: The case does not execute the accepted parent or establish
        numerical verification, scientific validation, UQ, or execution authority.
        """
        result = self.make_toy_result(tmp_path)
        original = result.read_bytes()
        runner, _, _ = self.scripts()
        completed = subprocess.run(
            [
                sys.executable,
                str(runner),
                "--execution-free-toy-output",
                str(result),
            ],
            check=False,
            capture_output=True,
            text=True,
        )
        assert completed.returncode != 0
        assert result.read_bytes() == original

    def test_artifact__order_adverse__detects_shared_twist_cache(
        self, tmp_path: Path
    ) -> None:
        """Detect the deliberately stateful route-order mutation.

        Evidence ID: SV-RM-DEFECT2D-B-009

        Requirement: The order control must discriminate shared twist state while
        clean schedules remain invariant.

        Method: Read the maintained authored adverse record from the toy result.

        Oracle: Clean route schedule differences are exact zero; the declared
        mutation exceeds the frozen adverse floor in Route A and the bridge.

        Acceptance: Clean differences are zero, while mutated Route A and bridge
        differences exceed ``1e-6``.

        Interpretation: Passing shows that the schedule control detects this
        software mutation without claiming a physical order effect.

        Limitations: One synthetic mutation does not exhaust shared-state failures
        or establish accepted-parent numerical behavior.
        """
        payload = self.read_json(self.make_toy_result(tmp_path))
        adverse = cast(dict[str, JsonValue], payload["execution_free_order_adverse"])
        assert adverse["clean_schedule_route_A_maximum_absolute"] == 0.0
        assert adverse["clean_schedule_route_B_maximum_absolute"] == 0.0
        assert (
            cast(float, adverse["mutated_schedule_route_A_maximum_absolute"]) > 1.0e-6
        )
        assert cast(float, adverse["mutated_B_then_A_bridge_maximum_absolute"]) > 1.0e-6

    def test_artifact__execution_gate__requires_exact_authorization_arguments(
        self, tmp_path: Path
    ) -> None:
        """Fail closed before any accepted-parent path can be read.

        Evidence ID: SV-RM-DEFECT2D-B-010

        Requirement: Toy authority must not imply calculation execution authority.

        Method: Exercise the maintained artifact with authored toy data and compare
        the retained or process behavior with the declared contract.

        Oracle: The frozen multi-route inventory, exact mutation, or independent
        command behavior stated by the requirement.

        Acceptance: An incomplete execution command fails and creates no output.

        Interpretation: Passing establishes only the stated synthetic software
        behavior; failure identifies an artifact, oracle, or contract discrepancy.

        Limitations: The case does not execute the accepted parent or establish
        numerical verification, scientific validation, UQ, or execution authority.
        """
        runner, _, _ = self.scripts()
        output = tmp_path / "forbidden-result.json"
        completed = subprocess.run(
            [sys.executable, str(runner), "--output", str(output)],
            check=False,
            capture_output=True,
            text=True,
        )
        assert completed.returncode != 0
        assert "execution requires" in completed.stderr
        assert not output.exists()

    def test_artifact__execution_gate__rejects_stale_source_digest(
        self, tmp_path: Path
    ) -> None:
        """Reject a stale exact runner identity before parent parsing.

        Evidence ID: SV-RM-DEFECT2D-B-011

        Requirement: Future execution authority must bind final source identities.

        Method: Replace the bound runner digest in an isolated complete fixture.

        Oracle: The copied runner bytes define their SHA-256 identity.

        Acceptance: Execution fails, reports a digest difference, and writes no result.

        Interpretation: Passing establishes fail-closed source binding only.

        Limitations: The fixture contains no accepted scientific input.
        """
        root, runner, auth_path, authorization = self.make_execution_fixture(tmp_path)
        authorization["runner_sha256"] = "0" * 64
        auth_path.write_text(
            json.dumps(authorization, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        completed = self.run_execution_fixture(root, runner, auth_path)
        assert completed.returncode != 0
        assert "digest differs" in completed.stderr
        assert not (auth_path.parent / "stage-b-result.json").exists()

    def test_artifact__execution_gate__rejects_path_escape(
        self, tmp_path: Path
    ) -> None:
        """Reject an authorization binding outside the canonical repository.

        Evidence ID: SV-RM-DEFECT2D-B-012

        Requirement: Every represented provenance path must remain below root.

        Method: Replace the verifier binding with the absolute ``/etc/hosts`` path.

        Oracle: Canonical ``Path.is_relative_to`` confinement.

        Acceptance: Execution fails with a path-escape diagnostic and no result.

        Interpretation: Passing establishes this traversal refusal only.

        Limitations: It does not enumerate every filesystem alias or race.
        """
        root, runner, auth_path, authorization = self.make_execution_fixture(tmp_path)
        authorization["verifier_path"] = "/etc/hosts"
        auth_path.write_text(
            json.dumps(authorization, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        completed = self.run_execution_fixture(root, runner, auth_path)
        assert completed.returncode != 0
        assert "must be canonical repository-relative" in completed.stderr
        assert not (auth_path.parent / "stage-b-result.json").exists()

    def test_artifact__execution_gate__rejects_wrong_checkpoint_decision(
        self, tmp_path: Path
    ) -> None:
        """Reject a resolved checkpoint that authorizes another boundary.

        Evidence ID: SV-RM-DEFECT2D-B-013

        Requirement: Resolved status alone must not authorize Stage B execution.

        Method: Use a digest-matched checkpoint with a wrong normalized decision.

        Oracle: The exact execution decision token frozen in the runner.

        Acceptance: Execution fails at the decision check and writes no result.

        Interpretation: Passing distinguishes implementation authority from execution.

        Limitations: The synthetic checkpoint is not a durable human record.
        """
        root, runner, auth_path, _ = self.make_execution_fixture(tmp_path)
        completed = self.run_execution_fixture(root, runner, auth_path)
        assert completed.returncode != 0
        assert "does not authorize Stage B execution" in completed.stderr
        assert not (auth_path.parent / "stage-b-result.json").exists()

    def test_artifact__execution_gate__rejects_resource_expansion(
        self, tmp_path: Path
    ) -> None:
        """Reject an envelope larger than the adopted matrix dimension.

        Evidence ID: SV-RM-DEFECT2D-B-014

        Requirement: Exact execution authority cannot expand frozen resources.

        Method: Make the synthetic checkpoint execution-specific but authorize
        dimension 65 instead of 64.

        Oracle: The adopted design's exact dimension-64 bound.

        Acceptance: Execution fails at the resource check and writes no result.

        Interpretation: Passing establishes this bounded resource refusal only.

        Limitations: It does not measure operating-system resource enforcement.
        """
        root, runner, auth_path, authorization = self.make_execution_fixture(tmp_path)
        checkpoint = root / ".pi/checkpoints/stage-b-execution.json"
        checkpoint_payload = self.read_json(checkpoint)
        checkpoint_payload["normalized_decision"] = (
            "AUTHORIZE_EXACT_STAGE_B_MULTIROUTE_EXECUTION"
        )
        checkpoint.write_text(
            json.dumps(checkpoint_payload, sort_keys=True) + "\n", encoding="utf-8"
        )
        authorization["checkpoint_sha256"] = self.sha256(checkpoint)
        resources = cast(dict[str, JsonValue], authorization["resource_envelope"])
        resources["maximum_matrix_dimension"] = 65
        auth_path.write_text(
            json.dumps(authorization, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        completed = self.run_execution_fixture(root, runner, auth_path)
        assert completed.returncode != 0
        assert "matrix dimension authorization differs" in completed.stderr
        assert not (auth_path.parent / "stage-b-result.json").exists()

    def test_artifact__result_schema__accepts_complete_toy_record(
        self, tmp_path: Path
    ) -> None:
        """Validate the complete synthetic record against the closed schema.

        Evidence ID: SV-RM-DEFECT2D-B-015

        Requirement: Retained Stage B data must have a versioned closed schema.

        Method: Validate the complete authored toy result with Draft 2020-12.

        Oracle: The maintained JSON Schema is the persistence contract.

        Acceptance: The validator emits no errors.

        Interpretation: Passing establishes structural conformance only.

        Limitations: Schema validity does not establish numerical correctness or
        authorize accepted-parent execution.
        """
        result = self.make_toy_result(tmp_path)
        schema = (
            self.repository_root()
            / "calculations/research-monograph/impurity-defect-2d"
            / "stage-b-result.schema.json"
        )
        completed = subprocess.run(
            [
                sys.executable,
                "-c",
                (
                    "import json,sys; from pathlib import Path; "
                    "from jsonschema import Draft202012Validator; "
                    "s=json.loads(Path(sys.argv[1]).read_text()); "
                    "r=json.loads(Path(sys.argv[2]).read_text()); "
                    "e=list(Draft202012Validator(s).iter_errors(r)); "
                    "raise SystemExit(1 if e else 0)"
                ),
                str(schema),
                str(result),
            ],
            check=False,
            capture_output=True,
            text=True,
        )
        assert completed.returncode == 0, completed.stderr

    def test_artifact__verifier_dependency__excludes_runner_import(self) -> None:
        """Keep independent reconstruction free of runner imports.

        Evidence ID: SV-RM-DEFECT2D-B-016

        Requirement: The verifier must own a distinct reconstruction route.

        Method: Exercise the maintained artifact with authored toy data and compare
        the retained or process behavior with the declared contract.

        Oracle: The frozen multi-route inventory, exact mutation, or independent
        command behavior stated by the requirement.

        Acceptance: Its source contains no runner import or dynamic loader.

        Interpretation: Passing establishes only the stated synthetic software
        behavior; failure identifies an artifact, oracle, or contract discrepancy.

        Limitations: The case does not execute the accepted parent or establish
        numerical verification, scientific validation, UQ, or execution authority.
        """
        _, verifier, _ = self.scripts()
        source = verifier.read_text(encoding="utf-8")
        assert "import run_stage_b" not in source
        assert "from run_stage_b" not in source
        assert "importlib" not in source
