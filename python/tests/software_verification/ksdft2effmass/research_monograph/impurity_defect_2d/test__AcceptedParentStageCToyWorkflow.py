r"""Software verification of ``AcceptedParentStageCToyWorkflow``.

Evidence profile: routine

Bounded artifact scope: authored parent inventory, preprocessing, fitting, routes,
schemas, verification, serialization, and authority behavior.

Facet and represented meaning

The artifact represents the frozen authored-parent inventory, preprocessing, model
hierarchy, route bridges, schedule controls, adverse controls, closed result shape, and
independent QR reconstruction.

Intrinsic and cross-object scope

The Workflow owns authored-parent command behavior and fail-closed authority
boundaries. Adapter, operation-package, plotting, source-ownership, and
accepted-provenance facets are verified separately.

VVUQ and scientific exclusions

This is software verification using authored synthetic records. It does not reopen
accepted parents or establish a calculated result, material adequacy, scientific
validation, uncertainty quantification, or execution authority.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import cast

import pytest
from jsonschema import Draft202012Validator  # type: ignore[import-untyped]
from stage_c_parent.workflows import AcceptedParentStageCToyWorkflow

type JsonScalar = None | bool | int | float | str
type JsonValue = JsonScalar | list[JsonValue] | dict[str, JsonValue]

pytestmark = pytest.mark.software_verification
SUT = AcceptedParentStageCToyWorkflow


class TestAcceptedParentStageCToyWorkflow:
    """Own verification of the authored Stage C parent Workflow."""

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
        """Run the authored-fixture Workflow in scratch space.

        Evidence ID: Helper owns no identifier.
        """

        stage = cls.stage_directory()
        output = tmp_path / name
        SUT().execute(
            stage / "stage-c-accepted-parent-design.json",
            cls.parent_fixture(),
            output,
        )
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
        wrapper_source = (stage / "verify_stage_c_parent.py").read_text()
        source = (stage / "stage_c_parent_verification/verifier.py").read_text()
        combined_source = wrapper_source + source
        assert "import run_stage_c" not in combined_source
        assert "from run_stage_c" not in combined_source
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
        with pytest.raises(ValueError, match="accepted-parent fixtures are forbidden"):
            SUT().execute(
                stage / "stage-c-accepted-parent-design.json",
                mutated,
                rejected,
            )
        assert not rejected.exists()
        design = self.read_json(stage / "stage-c-accepted-parent-design.json")
        model_classes = cast(list[JsonValue], design["model_class_order"])
        model_classes[0], model_classes[1] = model_classes[1], model_classes[0]
        mutated_design = tmp_path / "mutated-adopted-design.json"
        mutated_design.write_text(json.dumps(design, indent=2) + "\n")
        design_rejected = tmp_path / "design-rejected.json"
        with pytest.raises(
            ValueError, match="accepted-parent Stage C design identity is not adopted"
        ):
            SUT().execute(mutated_design, self.parent_fixture(), design_rejected)
        assert not design_rejected.exists()
        output = self.make_parent_result(tmp_path)
        original = output.read_bytes()
        with pytest.raises(FileExistsError):
            SUT().execute(
                stage / "stage-c-accepted-parent-design.json",
                self.parent_fixture(),
                output,
            )
        assert output.read_bytes() == original
