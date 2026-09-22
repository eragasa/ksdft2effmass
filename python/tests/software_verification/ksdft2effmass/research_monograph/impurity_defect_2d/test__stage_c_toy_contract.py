r"""Software verification of Stage C execution-free toy contract.

Evidence profile: routine

Bounded artifact scope: authored toy runner, schema, verifier, serialization, authority,
and claim-boundary behavior.

Facet and represented meaning

The artifact represents authored finite 8 by 8 scalar defect matrices, ordered model-
class selection, gauge bridges, symmetry controls, and deterministic toy-result wire
behavior.

Intrinsic and cross-object scope

This module owns the toy command, its closed result schema, independent verifier
boundary, deterministic serialization, and fail-closed execution-free claim. Accepted-
parent behavior belongs to separate Stage C contract modules.

VVUQ and scientific exclusions

This is software verification using synthetic test data. It establishes no accepted-
parent numerical result, material adequacy, scientific validation, uncertainty
quantification, execution authority, publication, or release status.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import cast

import pytest
from jsonschema import Draft202012Validator  # type: ignore[import-untyped]

type JsonScalar = None | bool | int | float | str
type JsonValue = JsonScalar | list[JsonValue] | dict[str, JsonValue]

pytestmark = pytest.mark.software_verification


class TestStageCToyContract:
    """Own software verification of the execution-free Stage C toy artifact."""

    @staticmethod
    def repository_root() -> Path:
        """Return the repository containing the Stage C artifacts.

        Evidence ID: Helper owns no identifier.
        """

        return Path(__file__).resolve().parents[6]

    @classmethod
    def stage_directory(cls) -> Path:
        """Return the maintained defect-2D calculation directory.

        Evidence ID: Helper owns no identifier.
        """

        return (
            cls.repository_root() / "calculations/research-monograph/impurity-defect-2d"
        )

    @classmethod
    def make_toy_result(cls, tmp_path: Path, name: str = "toy.json") -> Path:
        """Run the maintained Stage C toy command in isolated scratch space.

        Evidence ID: Helper owns no identifier.
        """

        stage = cls.stage_directory()
        output = tmp_path / name
        process = subprocess.run(
            [
                sys.executable,
                str(stage / "run_stage_c.py"),
                "--design",
                str(stage / "stage-c-design.json"),
                "--toy-output",
                str(output),
            ],
            cwd=cls.repository_root(),
            check=False,
            capture_output=True,
            text=True,
        )
        if process.returncode != 0:
            raise RuntimeError(process.stderr)
        return output

    @staticmethod
    def read_json(path: Path) -> dict[str, JsonValue]:
        """Read one closed test-owned JSON object.

        Evidence ID: Helper owns no identifier.
        """

        value = cast(JsonValue, json.loads(path.read_text()))
        if not isinstance(value, dict):
            raise TypeError("expected a JSON object")
        return value

    @staticmethod
    def selection_pair(value: JsonValue) -> tuple[JsonValue, JsonValue]:
        """Return retained and expected model-class identities.

        Evidence ID: Helper owns no identifier.
        """

        record = cast(dict[str, JsonValue], value)
        return record["selected_model_class"], record["expected_model_class"]

    @staticmethod
    def adverse_pair(value: JsonValue) -> tuple[str, float]:
        """Return one adverse-control identity and finite value.

        Evidence ID: Helper owns no identifier.
        """

        record = cast(dict[str, JsonValue], value)
        return cast(str, record["control_id"]), cast(float, record["value"])

    def test_artifact__inventory__retains_exact_stage_c_toy_counts(
        self, tmp_path: Path
    ) -> None:
        """Retain every route, bridge, fit, and symmetry record.

        Evidence ID: SV-RM-DEFECT2D-C-001

        Requirement: The authored-toy result preserves the frozen Stage C inventory.

        Method: Execute the maintained toy runner and inspect its exact summary.

        Oracle: The authorized design fixes 16 route, 8 bridge, 16 symmetry, and
        80 fit records.

        Acceptance: Observe every exact count and no accepted-parent read.

        Interpretation: Passing establishes only inventory-complete software behavior.

        Limitations: This test does not establish accepted-parent numerical evidence,
        scientific validation, UQ, or execution authority.
        """

        payload = self.read_json(self.make_toy_result(tmp_path))
        summary = cast(dict[str, JsonValue], payload["summary"])
        assert summary["route_record_count"] == 16
        assert summary["bridge_record_count"] == 8
        assert summary["symmetry_record_count"] == 16
        assert summary["fit_record_count"] == 80
        assert payload["accepted_parent_read"] is False

    def test_artifact__model_classes__selects_first_exact_supported_class(
        self, tmp_path: Path
    ) -> None:
        """Select the frozen first passing directional or nonlocal class.

        Evidence ID: SV-RM-DEFECT2D-C-002

        Requirement: Every route and schedule applies the same ordered model hierarchy.

        Method: Read all route records produced from authored directional and diagonal
        bond plants.

        Oracle: The directional class is first for the directional plant and the
        radius-two class is first for the diagonal nonlocal plant.

        Acceptance: All sixteen records select their declared expected class.

        Interpretation: Passing verifies deterministic model-class selection only.

        Limitations: The selected class is not a physical material inference.
        """

        payload = self.read_json(self.make_toy_result(tmp_path))
        schedules = cast(list[JsonValue], payload["schedules"])
        first = cast(dict[str, JsonValue], schedules[0])
        second = cast(dict[str, JsonValue], schedules[1])
        assert first["fresh_spawned_process"] is True
        assert second["fresh_spawned_process"] is True
        first_records = cast(list[JsonValue], first["route_records"])
        second_records = cast(list[JsonValue], second["route_records"])
        first_pairs = [
            self.selection_pair(first_records[0]),
            self.selection_pair(first_records[1]),
            self.selection_pair(first_records[2]),
            self.selection_pair(first_records[3]),
            self.selection_pair(first_records[4]),
            self.selection_pair(first_records[5]),
            self.selection_pair(first_records[6]),
            self.selection_pair(first_records[7]),
        ]
        second_pairs = [
            self.selection_pair(second_records[0]),
            self.selection_pair(second_records[1]),
            self.selection_pair(second_records[2]),
            self.selection_pair(second_records[3]),
            self.selection_pair(second_records[4]),
            self.selection_pair(second_records[5]),
            self.selection_pair(second_records[6]),
            self.selection_pair(second_records[7]),
        ]
        assert first_pairs == [
            ("onsite_plus_directional_nearest_neighbor",) * 2,
            ("onsite_plus_directional_nearest_neighbor",) * 2,
            ("finite_range_nonlocal_radius_two",) * 2,
            ("finite_range_nonlocal_radius_two",) * 2,
            ("onsite_plus_directional_nearest_neighbor",) * 2,
            ("onsite_plus_directional_nearest_neighbor",) * 2,
            ("finite_range_nonlocal_radius_two",) * 2,
            ("finite_range_nonlocal_radius_two",) * 2,
        ]
        assert second_pairs == first_pairs

    def test_artifact__routes__preserves_bridge_symmetry_and_schedule_agreement(
        self, tmp_path: Path
    ) -> None:
        """Preserve gauge, oriented-symmetry, and order controls separately.

        Evidence ID: SV-RM-DEFECT2D-C-003

        Requirement: Correctly bridged routes, oriented D4 reconstructions, and both
        schedules satisfy their separate criteria.

        Method: Execute the toy workflow and inspect named criterion records.

        Oracle: The frozen design requires bridge and covariance defects at most
        1e-12 and an exactly zero schedule difference.

        Acceptance: Each named criterion passes and the schedule value is exact zero.

        Interpretation: Passing verifies represented software covariance and order
        independence, not physical symmetry.

        Limitations: The bridge is not an independent scientific estimate.
        """

        payload = self.read_json(self.make_toy_result(tmp_path))
        criteria = cast(list[JsonValue], payload["criteria"])
        bridge = cast(dict[str, JsonValue], criteria[1])
        symmetry = cast(dict[str, JsonValue], criteria[2])
        schedule = cast(dict[str, JsonValue], criteria[3])
        assert bridge["criterion"] == "gauge_bridge"
        assert bridge["passed"] is True
        assert symmetry["criterion"] == "D4_oriented_covariance"
        assert symmetry["passed"] is True
        assert schedule["criterion"] == "schedule_invariance"
        assert schedule["passed"] is True
        assert schedule["value"] == 0.0

    def test_artifact__adverse_controls__retains_discriminating_failures(
        self, tmp_path: Path
    ) -> None:
        """Retain wrong-class, non-Hermitian, and unbridged discrepancies.

        Evidence ID: SV-RM-DEFECT2D-C-004

        Requirement: Every frozen adverse control must remain quantitatively
        discriminating.

        Method: Compare retained values with independently hand-derived or frozen
        lower-bound expectations.

        Oracle: Isotropic directional residual is 0.07, diagonal residual is
        sqrt(2)*0.025, omitted-reverse defect is 0.04, and raw gauge mismatch exceeds
        0.01.

        Acceptance: Values meet the exact approximate or lower-bound contracts.

        Interpretation: Passing verifies detection of intentional protocol errors.

        Limitations: Adverse residuals are not physical uncertainties.
        """

        payload = self.read_json(self.make_toy_result(tmp_path))
        adverse = cast(list[JsonValue], payload["adverse_controls"])
        directional_id, directional_value = self.adverse_pair(adverse[0])
        nonlocal_id, nonlocal_value = self.adverse_pair(adverse[1])
        reverse_id, reverse_value = self.adverse_pair(adverse[2])
        bridge_id, bridge_value = self.adverse_pair(adverse[3])
        assert directional_id == "directional_as_isotropic"
        assert directional_value == pytest.approx(0.07, abs=1e-15)
        assert nonlocal_id == "nonlocal_as_directional"
        assert nonlocal_value == pytest.approx(2.0**0.5 * 0.025, abs=1e-15)
        assert reverse_id == "omit_hermitian_reverse"
        assert reverse_value == pytest.approx(0.04, abs=1e-15)
        assert bridge_id == "omit_gauge_bridge"
        assert bridge_value >= 0.01

    def test_artifact__independent_verifier__reconstructs_without_runner_import(
        self, tmp_path: Path
    ) -> None:
        """Reconstruct the toy result through a distinct maintained implementation.

        Evidence ID: SV-RM-DEFECT2D-C-005

        Requirement: The verifier must not import the runner and must reproduce the
        bounded result independently.

        Method: Inspect the verifier import surface, execute it as a separate process,
        and read its status lines.

        Oracle: The protocol forbids runner imports and requires reconstruction and
        criteria PASS.

        Acceptance: No runner import is present and both statuses are PASS.

        Interpretation: Passing verifies implementation independence at the declared
        software boundary.

        Limitations: Independence does not establish scientific validation.
        """

        stage = self.stage_directory()
        result = self.make_toy_result(tmp_path)
        source = (stage / "verify_stage_c.py").read_text()
        assert "import run_stage_c" not in source
        assert "from run_stage_c" not in source
        process = subprocess.run(
            [
                sys.executable,
                str(stage / "verify_stage_c.py"),
                "--design",
                str(stage / "stage-c-design.json"),
                "--toy-result",
                str(result),
            ],
            cwd=self.repository_root(),
            check=False,
            capture_output=True,
            text=True,
        )
        assert process.returncode == 0, process.stderr
        assert "defect_2d_stage_c_toy_reconstruction=PASS" in process.stdout
        assert "defect_2d_stage_c_toy_criteria=PASS" in process.stdout

    def test_artifact__schema__accepts_complete_toy_result(
        self, tmp_path: Path
    ) -> None:
        """Validate the complete toy result against the closed schema.

        Evidence ID: SV-RM-DEFECT2D-C-006

        Requirement: Runtime output conforms to the maintained Draft 2020-12 schema.

        Method: Validate one fresh toy result with Draft202012Validator.

        Oracle: `stage-c-toy-result.schema.json` is the wire-shape authority.

        Acceptance: Schema iteration reports no errors.

        Interpretation: Passing establishes wire conformance only.

        Limitations: Schema validity does not establish mathematical or physical
        correctness.
        """

        stage = self.stage_directory()
        payload = self.read_json(self.make_toy_result(tmp_path))
        schema = self.read_json(stage / "stage-c-toy-result.schema.json")
        assert list(Draft202012Validator(schema).iter_errors(payload)) == []

    def test_artifact__serialization__is_byte_deterministic(
        self, tmp_path: Path
    ) -> None:
        """Serialize identical authored inputs to identical bytes.

        Evidence ID: SV-RM-DEFECT2D-C-007

        Requirement: Toy serialization is independent of output pathname.

        Method: Execute the runner twice with the same immutable design.

        Oracle: Canonical sorted indented JSON has exact byte identity.

        Acceptance: Both files are byte-for-byte equal.

        Interpretation: Passing verifies deterministic serialization.

        Limitations: Determinism does not establish correctness of scientific meaning.
        """

        first = self.make_toy_result(tmp_path, "first.json")
        second = self.make_toy_result(tmp_path, "second.json")
        assert first.read_bytes() == second.read_bytes()

    def test_artifact__serialization__refuses_output_overwrite(
        self, tmp_path: Path
    ) -> None:
        """Refuse to overwrite an existing toy artifact.

        Evidence ID: SV-RM-DEFECT2D-C-008

        Requirement: The command must fail closed when the output already exists.

        Method: Create one result and invoke the command again at the same path.

        Oracle: The serializer contract forbids replacement of retained bytes.

        Acceptance: The second process is nonzero and the first bytes remain exact.

        Interpretation: Passing verifies overwrite protection.

        Limitations: The test does not authorize retention as scientific evidence.
        """

        stage = self.stage_directory()
        output = self.make_toy_result(tmp_path)
        original = output.read_bytes()
        process = subprocess.run(
            [
                sys.executable,
                str(stage / "run_stage_c.py"),
                "--design",
                str(stage / "stage-c-design.json"),
                "--toy-output",
                str(output),
            ],
            cwd=self.repository_root(),
            check=False,
            capture_output=True,
            text=True,
        )
        assert process.returncode != 0
        assert output.read_bytes() == original

    def test_artifact__authorization__rejects_execution_authority_mutation(
        self, tmp_path: Path
    ) -> None:
        """Reject a design mutated to claim execution authority.

        Evidence ID: SV-RM-DEFECT2D-C-009

        Requirement: The toy runner accepts only an execution-free design.

        Method: Set the design authorization flag true in isolated scratch JSON.

        Oracle: HC09 and the design both forbid accepted-parent execution authority.

        Acceptance: The runner exits nonzero and creates no output.

        Interpretation: Passing verifies fail-closed authority parsing.

        Limitations: The test cannot itself grant or revoke human authority.
        """

        stage = self.stage_directory()
        design = self.read_json(stage / "stage-c-design.json")
        design["execution_authorized_by_this_record"] = True
        mutated = tmp_path / "mutated-design.json"
        mutated.write_text(json.dumps(design, indent=2) + "\n")
        output = tmp_path / "result.json"
        process = subprocess.run(
            [
                sys.executable,
                str(stage / "run_stage_c.py"),
                "--design",
                str(mutated),
                "--toy-output",
                str(output),
            ],
            cwd=self.repository_root(),
            check=False,
            capture_output=True,
            text=True,
        )
        assert process.returncode != 0
        assert not output.exists()

    def test_artifact__claim_boundary__labels_toy_behavior_without_parent_result(
        self, tmp_path: Path
    ) -> None:
        """Retain the execution-free evidence label and no-parent disposition.

        Evidence ID: SV-RM-DEFECT2D-C-010

        Requirement: Authored behavior cannot be serialized as accepted-parent
        numerical evidence.

        Method: Inspect the exact result identity, evidence label, and parent-read flag.

        Oracle: The authorized Stage C design defines software verification only.

        Acceptance: The result has the authored-toy identity, synthetic label, and a
        false accepted-parent-read field.

        Interpretation: Passing verifies the retained claim boundary.

        Limitations: A label is not proof that future code cannot be changed.
        """

        payload = self.read_json(self.make_toy_result(tmp_path))
        assert payload["result_id"] == (
            "research-monograph.impurity-defect-2d.stage-c.authored-toy.v1"
        )
        assert payload["evidence_status"] == (
            "synthetic execution-free software-verification behavior"
        )
        assert payload["accepted_parent_read"] is False
