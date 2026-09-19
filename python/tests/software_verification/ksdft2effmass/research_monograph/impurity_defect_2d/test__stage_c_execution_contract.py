r"""Software verification of defect-2D Stage C execution-free contracts.

Evidence profile: routine

Bounded artifact scope: the execution-free directional/nonlocal runner,
independent verifier, closed toy-result schema, deterministic serialization,
model-class selection, gauge/symmetry/schedule controls, and adverse controls.

Facet and represented meaning

The artifact represents finite $8\times8$ scalar defect matrices in two twist
gauges and a frozen ordered hierarchy of local and nonlocal model classes. Every
test uses authored toy coefficients and no accepted periodic parent.

Intrinsic and cross-object scope

The artifact owns command boundaries, exact retained inventories, deterministic
wire behavior, independent reconstruction, and cross-route agreement. It does
not own an accepted-parent Stage C calculation or later-stage behavior.

VVUQ and scientific exclusions

This is software verification using synthetic test data. It establishes no
accepted-parent numerical result, material adequacy, scientific validation,
uncertainty quantification, execution authority, publication, or release status.
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


class TestStageCExecutionContract:
    """Own software verification of the authored-toy Stage C artifacts."""

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

    @classmethod
    def parent_fixture(cls) -> Path:
        """Return the maintained authored accepted-parent behavioral fixture.

        Evidence ID: Helper owns no identifier.
        """

        return (
            Path(__file__).resolve().parent
            / "resources/stage-c-accepted-parent-authored-fixture.json"
        )

    @classmethod
    def make_parent_result(cls, tmp_path: Path, name: str = "parent-toy.json") -> Path:
        """Run the parent-contract authored-fixture command in scratch space.

        Evidence ID: Helper owns no identifier.
        """

        stage = cls.stage_directory()
        output = tmp_path / name
        process = subprocess.run(
            [
                sys.executable,
                str(stage / "run_stage_c_parent.py"),
                "--accepted-parent-design",
                str(stage / "stage-c-accepted-parent-design.json"),
                "--authored-parent-fixture",
                str(cls.parent_fixture()),
                "--authored-parent-output",
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

    def test_artifact__parent_inventory__retains_exact_adopted_counts(
        self, tmp_path: Path
    ) -> None:
        """Retain every adopted parent-contract evaluation on authored data.

        Evidence ID: SV-RM-DEFECT2D-C-011

        Requirement: Execution-free implementation exercises the exact 208/104/1040/
        104 inventory without reading accepted parents.

        Method: Run the maintained parent-contract command against its authored fixture.

        Oracle: HC12 fixes the inventory and HC13 forbids accepted-parent reads.

        Acceptance: Exact counts are retained, all criteria pass, and the parent-read
        flag remains false.

        Interpretation: Passing verifies inventory-complete synthetic behavior only.

        Limitations: It is not an accepted-parent Stage C result.
        """

        payload = self.read_json(self.make_parent_result(tmp_path))
        inventory = cast(dict[str, JsonValue], payload["inventory"])
        summary = cast(dict[str, JsonValue], payload["summary"])
        assert inventory == {
            "bridge_records": 104,
            "execution_schedules": 2,
            "model_fit_records": 1040,
            "route_evaluations": 208,
            "schedule_comparisons": 104,
        }
        assert summary["all_criteria_passed"] is True
        assert payload["accepted_parent_read"] is False

    def test_artifact__parent_preprocessing__is_fresh_complete_and_consistent(
        self, tmp_path: Path
    ) -> None:
        """Reconstruct the anisotropic Fourier inventory in both schedules.

        Evidence ID: SV-RM-DEFECT2D-C-012

        Requirement: Each schedule independently reconstructs 225 coefficients and
        retains the same 61-term radius-18 compact inventory.

        Method: Inspect both schedule-local preprocessing records.

        Oracle: The adopted mesh is 15 by 15 and the compact mask contains 61 terms.

        Acceptance: Both pretruncation counts are 225, compact counts are 61, and
        compact identities agree.

        Interpretation: Passing verifies deterministic schedule-local preprocessing.

        Limitations: It does not measure accepted-parent truncation quality.
        """

        payload = self.read_json(self.make_parent_result(tmp_path))
        schedules = cast(list[JsonValue], payload["schedules"])
        preprocess = [
            cast(
                dict[str, JsonValue], cast(dict[str, JsonValue], value)["preprocessing"]
            )
            for value in schedules
        ]
        full = [
            cast(dict[str, JsonValue], value["pretruncation"]) for value in preprocess
        ]
        compact = [cast(dict[str, JsonValue], value["compact"]) for value in preprocess]
        assert [value["count"] for value in full] == [225, 225]
        assert [value["count"] for value in compact] == [61, 61]
        assert compact[0]["sha256"] == compact[1]["sha256"]

    def test_artifact__parent_models__hides_then_recovers_expected_classes(
        self, tmp_path: Path
    ) -> None:
        """Select every first accepted class without selector access to its oracle.

        Evidence ID: SV-RM-DEFECT2D-C-013

        Requirement: All five bases are evaluated before expected-class comparison.

        Method: Inspect every route record and its complete ordered fit list.

        Oracle: Directional and diagonal plants first pass their frozen distinct
        classes after five independent fits.

        Acceptance: Each record contains five fits and selected equals expected.

        Interpretation: Passing verifies ordered synthetic model selection.

        Limitations: No material model class is inferred.
        """

        payload = self.read_json(self.make_parent_result(tmp_path))
        schedules = cast(list[JsonValue], payload["schedules"])
        records = [
            cast(dict[str, JsonValue], record)
            for schedule_value in schedules
            for record in cast(
                list[JsonValue],
                cast(dict[str, JsonValue], schedule_value)["route_records"],
            )
        ]
        assert len(records) == 208
        assert all(
            len(cast(list[JsonValue], record["fits"])) == 5 for record in records
        )
        assert all(
            record["selected_model_class"] == record["expected_model_class"]
            for record in records
        )

    def test_artifact__parent_routes__preserves_bridges_and_schedules(
        self, tmp_path: Path
    ) -> None:
        """Preserve bridge equivalence and exact schedule invariance separately.

        Evidence ID: SV-RM-DEFECT2D-C-014

        Requirement: Parent, defect, candidate, and recovered bridges meet tolerance,
        while A-to-B and B-to-A schedules agree exactly.

        Method: Inspect all retained bridge and schedule comparison diagnostics.

        Oracle: Bridges are at most 1e-10 and every clean schedule difference is zero.

        Acceptance: All five bridge subjects pass and all 104 schedule records are
        exact zero.

        Interpretation: Passing verifies represented route equivalence and order
        independence, not two scientific estimates.

        Limitations: The bridge is not a vote or uncertainty estimate.
        """

        payload = self.read_json(self.make_parent_result(tmp_path))
        schedules = cast(list[JsonValue], payload["schedules"])
        bridges = [
            cast(dict[str, JsonValue], bridge)
            for schedule_value in schedules
            for bridge in cast(
                list[JsonValue],
                cast(dict[str, JsonValue], schedule_value)["bridge_records"],
            )
        ]
        assert len(bridges) == 104
        assert all(
            cast(float, bridge[f"{subject}_maximum_absolute"]) <= 1e-10
            for bridge in bridges
            for subject in ("parent", "defect", "full", "attacked", "recovered")
        )
        comparisons = cast(list[JsonValue], payload["schedule_comparisons"])
        assert len(comparisons) == 104
        assert all(
            cast(dict[str, JsonValue], value)["maximum_absolute"] == 0.0
            for value in comparisons
        )

    def test_artifact__parent_adverse_controls__meets_predeclared_floors(
        self, tmp_path: Path
    ) -> None:
        """Demonstrate every adopted adverse control including anisotropic floors.

        Evidence ID: SV-RM-DEFECT2D-C-015

        Requirement: Ten adverse controls fail closed or remain discriminating without
        accepted-parent tuning.

        Method: Compare first-schedule values with the predeclared synthetic floors.

        Oracle: The two anisotropic controls exceed 1e-3 and all earlier floors retain
        their adopted values.

        Acceptance: Eight numerical floors pass and both protocol violations retain
        exact fail-closed status codes.

        Interpretation: Passing verifies detection sensitivity on authored fixtures.

        Limitations: These floors are not accepted-parent observations.
        """

        payload = self.read_json(self.make_parent_result(tmp_path))
        schedules = cast(list[JsonValue], payload["schedules"])
        schedule = cast(dict[str, JsonValue], schedules[0])
        records = [
            cast(dict[str, JsonValue], value)
            for value in cast(list[JsonValue], schedule["adverse_controls"])
        ]
        values = {cast(str, value["control_id"]): value for value in records}
        floors = {
            "omit_energy_reference_correction": 1.0,
            "directional_as_isotropic": 0.03,
            "nonlocal_as_directional": 0.03,
            "omit_hermitian_reverse": 0.03,
            "compare_raw_gauges_without_bridge": 0.01,
            "hold_generic_twist_fixed_under_quarter_turn": 1e-6,
            "claim_D4_for_anisotropic_parent": 1e-3,
            "axis_swap_defect_without_parent_swap": 1e-3,
        }
        assert all(
            cast(float, values[identifier]["value"]) >= floor
            for identifier, floor in floors.items()
        )
        assert values["prealignment_subtraction"]["status"] == (
            "DEFECT_2D.SITE_MAP_UNRESOLVED"
        )
        assert values["construct_route_B_from_route_A"]["status"] == (
            "DEFECT_2D.ROUTE_INDEPENDENCE_VIOLATION"
        )

    def test_artifact__parent_schema__accepts_complete_closed_result(
        self, tmp_path: Path
    ) -> None:
        """Validate the complete parent-contract authored result against its schema.

        Evidence ID: SV-RM-DEFECT2D-C-016

        Requirement: Runtime output conforms to the closed Stage C result schema.

        Method: Apply the Draft 2020-12 validator to a fresh result.

        Oracle: `stage-c-result.schema.json` owns the exact wire shape.

        Acceptance: Schema iteration reports no errors.

        Interpretation: Passing establishes wire conformance only.

        Limitations: Schema conformance is not numerical or scientific validation.
        """

        payload = self.read_json(self.make_parent_result(tmp_path))
        schema = self.read_json(self.stage_directory() / "stage-c-result.schema.json")
        assert list(Draft202012Validator(schema).iter_errors(payload)) == []

    def test_artifact__parent_verifier__uses_independent_qr_reconstruction(
        self, tmp_path: Path
    ) -> None:
        """Reconstruct all records without runner imports or normal equations.

        Evidence ID: SV-RM-DEFECT2D-C-017

        Requirement: The independent verifier uses direct construction and QR while
        consuming no runner matrix or cache.

        Method: Inspect forbidden imports and execute the verifier as a separate
        process over retained scalar records.

        Oracle: The protocol forbids runner imports and normal equations.

        Acceptance: Source contains QR, no runner import, and reports 208 routes,
        1,040 fits, and PASS.

        Interpretation: Passing verifies the declared independent software oracle.

        Limitations: It remains synthetic verification rather than parent evidence.
        """

        stage = self.stage_directory()
        result = self.make_parent_result(tmp_path)
        source = (stage / "verify_stage_c_parent.py").read_text()
        assert "import run_stage_c" not in source
        assert "from run_stage_c" not in source
        assert "np.linalg.qr" in source
        assert "np.linalg.solve" in source
        process = subprocess.run(
            [
                sys.executable,
                str(stage / "verify_stage_c_parent.py"),
                "--accepted-parent-design",
                str(stage / "stage-c-accepted-parent-design.json"),
                "--authored-parent-fixture",
                str(self.parent_fixture()),
                "--result",
                str(result),
            ],
            cwd=self.repository_root(),
            check=False,
            capture_output=True,
            text=True,
        )
        assert process.returncode == 0, process.stderr
        report = cast(JsonValue, json.loads(process.stdout))
        assert isinstance(report, dict)
        assert report["verification"] == "PASS"
        assert report["reconstructed_route_records"] == 208
        assert report["reconstructed_model_fits"] == 1040
        assert report["normal_equations_used"] is False

    def test_artifact__parent_serialization__is_deterministic_and_bounded(
        self, tmp_path: Path
    ) -> None:
        """Serialize complete synthetic results deterministically within the envelope.

        Evidence ID: SV-RM-DEFECT2D-C-018

        Requirement: Identical immutable inputs produce identical bytes below 20 MiB.

        Method: Execute twice into distinct scratch paths and compare byte streams.

        Oracle: The adopted retention envelope permits at most 20 MiB.

        Acceptance: Files are identical and each is smaller than 20 MiB.

        Interpretation: Passing verifies deterministic compact retention.

        Limitations: Test runtime is not an accepted-parent resource measurement.
        """

        first = self.make_parent_result(tmp_path, "first-parent.json")
        second = self.make_parent_result(tmp_path, "second-parent.json")
        assert first.read_bytes() == second.read_bytes()
        assert first.stat().st_size < 20 * 1024 * 1024

    def test_artifact__parent_plotter__is_deterministic_and_refuses_overwrite(
        self, tmp_path: Path
    ) -> None:
        """Render retained scalar diagnostics without consuming matrices.

        Evidence ID: SV-RM-DEFECT2D-C-019

        Requirement: Plotting is deterministic, JSON-only, and overwrite-safe.

        Method: Render two SVGs, compare bytes, then target an existing output.

        Oracle: The plotting contract permits retained result JSON as its sole input.

        Acceptance: SVG bytes agree and overwrite invocation fails without mutation.

        Interpretation: Passing verifies deterministic diagnostic rendering.

        Limitations: The SVG is not scientific evidence beyond its source record.
        """

        stage = self.stage_directory()
        result = self.make_parent_result(tmp_path)
        first = tmp_path / "first.svg"
        second = tmp_path / "second.svg"
        command = [
            sys.executable,
            str(stage / "plot_stage_c_parent.py"),
            "--result",
            str(result),
            "--output",
        ]
        first_process = subprocess.run(
            [*command, str(first)], check=False, capture_output=True, text=True
        )
        second_process = subprocess.run(
            [*command, str(second)], check=False, capture_output=True, text=True
        )
        assert first_process.returncode == 0, first_process.stderr
        assert second_process.returncode == 0, second_process.stderr
        assert first.read_bytes() == second.read_bytes()
        original = first.read_bytes()
        overwrite = subprocess.run(
            [*command, str(first)], check=False, capture_output=True, text=True
        )
        assert overwrite.returncode != 0
        assert first.read_bytes() == original

    def test_artifact__parent_authority__rejects_claim_mutation_and_overwrite(
        self, tmp_path: Path
    ) -> None:
        """Fail closed on parent claims, design mutation, and occupied output.

        Evidence ID: SV-RM-DEFECT2D-C-020

        Requirement: HC13 permits only authored fixtures and scratch outputs that are
        not overwritten.

        Method: Mutate the fixture parent flag, mutate the adopted model order, then
        separately rerun at an existing output.

        Oracle: Accepted-parent reads remain unauthorized and serializer replacement
        is forbidden.

        Acceptance: All three invocations fail and preserve or omit output as
        appropriate.

        Interpretation: Passing verifies two fail-closed authority boundaries.

        Limitations: Software checks cannot grant future execution authority.
        """

        stage = self.stage_directory()
        fixture = self.read_json(self.parent_fixture())
        fixture["accepted_parent"] = True
        mutated = tmp_path / "parent-claiming-fixture.json"
        mutated.write_text(json.dumps(fixture, indent=2) + "\n")
        rejected = tmp_path / "rejected.json"
        base = [
            sys.executable,
            str(stage / "run_stage_c_parent.py"),
            "--accepted-parent-design",
            str(stage / "stage-c-accepted-parent-design.json"),
            "--authored-parent-fixture",
            str(mutated),
            "--authored-parent-output",
            str(rejected),
        ]
        process = subprocess.run(
            base,
            cwd=self.repository_root(),
            check=False,
            capture_output=True,
            text=True,
        )
        assert process.returncode != 0
        assert not rejected.exists()
        design = self.read_json(stage / "stage-c-accepted-parent-design.json")
        model_classes = cast(list[JsonValue], design["model_class_order"])
        model_classes[0], model_classes[1] = model_classes[1], model_classes[0]
        mutated_design = tmp_path / "mutated-adopted-design.json"
        mutated_design.write_text(json.dumps(design, indent=2) + "\n")
        design_rejected = tmp_path / "design-rejected.json"
        design_process = subprocess.run(
            [
                sys.executable,
                str(stage / "run_stage_c_parent.py"),
                "--accepted-parent-design",
                str(mutated_design),
                "--authored-parent-fixture",
                str(self.parent_fixture()),
                "--authored-parent-output",
                str(design_rejected),
            ],
            cwd=self.repository_root(),
            check=False,
            capture_output=True,
            text=True,
        )
        assert design_process.returncode != 0
        assert not design_rejected.exists()
        output = self.make_parent_result(tmp_path)
        original = output.read_bytes()
        overwrite = subprocess.run(
            [
                sys.executable,
                str(stage / "run_stage_c_parent.py"),
                "--accepted-parent-design",
                str(stage / "stage-c-accepted-parent-design.json"),
                "--authored-parent-fixture",
                str(self.parent_fixture()),
                "--authored-parent-output",
                str(output),
            ],
            cwd=self.repository_root(),
            check=False,
            capture_output=True,
            text=True,
        )
        assert overwrite.returncode != 0
        assert output.read_bytes() == original
