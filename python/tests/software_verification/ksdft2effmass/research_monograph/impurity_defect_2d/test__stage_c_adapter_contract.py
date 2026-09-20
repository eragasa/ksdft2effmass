r"""Software verification of Stage C accepted-parent adapter contract.

Evidence profile: routine

Bounded artifact scope: authored adapter conversion, wire schemas, independent
verification, authority rejection, and identity-bound serialization.

Facet and represented meaning

The artifact represents conversion of five authored source records into the compact
Stage C parent representation, with exact provenance, closed authorization and result
schemas, and deterministic identity-bound bytes.

Intrinsic and cross-object scope

This module owns execution-free adapter conversion, independent adapter verification,
pre-read authority rejection, and serialization identity behavior. It does not own
complete package retention.

VVUQ and scientific exclusions

This is software verification using authored synthetic records. It opens no accepted
parent and establishes no accepted-parent execution, scientific validation, uncertainty
quantification, publication, or release status.
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


class TestStageCAdapterContract:
    """Own software verification of the execution-free Stage C adapter artifact."""

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
    def adapter_fixture(cls) -> Path:
        """Return the maintained authored multi-record adapter fixture.

        Evidence ID: Helper owns no identifier.
        """

        return (
            Path(__file__).resolve().parent
            / "resources/stage-c-accepted-parent-adapter-authored-fixture.json"
        )

    @classmethod
    def authorization_fixture(cls) -> Path:
        """Return the nonexecuting future-authorization wire fixture.

        Evidence ID: Helper owns no identifier.
        """

        return (
            Path(__file__).resolve().parent
            / "resources/stage-c-execution-authorization-authored-fixture.json"
        )

    @classmethod
    def make_adapter_result(
        cls, tmp_path: Path, name: str = "adapter-toy.json"
    ) -> Path:
        """Run the accepted-parent adapter against authored records only.

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
                "--authored-adapter-fixture",
                str(cls.adapter_fixture()),
                "--authored-adapter-output",
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

    def test_artifact__adapter__converts_authored_parent_records_with_provenance(
        self, tmp_path: Path
    ) -> None:
        """Exercise the accepted-parent adapter without accepted-parent reads.

        Evidence ID: SV-RM-DEFECT2D-C-021

        Requirement: Five authored source records traverse the same compact-parent
        adapter while preserving execution-free status and exact source identities.

        Method: Run adapter-fixture mode and inspect the retained provenance and
        criteria summary.

        Oracle: HC15 fixes five source roles, HC16 fixes the external native root,
        and the adopted design fixes the complete Stage C criteria.

        Acceptance: The result has the adapter-authored identity, five ordered input
        identities, the exact native root, false parent-read status, and all criteria
        passing.

        Interpretation: Passing verifies adapter conversion on synthetic records.

        Limitations: The test reads no accepted parent and grants no execution.
        """

        payload = self.read_json(self.make_adapter_result(tmp_path))
        provenance = cast(dict[str, JsonValue], payload["provenance"])
        repository = cast(dict[str, JsonValue], provenance["repository"])
        identities = cast(list[JsonValue], provenance["input_identities"])
        summary = cast(dict[str, JsonValue], payload["summary"])
        assert payload["result_id"] == (
            "research-monograph.impurity-defect-2d.stage-c."
            "accepted-parent-adapter-authored-fixture.v1"
        )
        assert payload["accepted_parent_read"] is False
        assert provenance["source_mode"] == ("authored_accepted_parent_adapter_fixture")
        assert len(identities) == 5
        assert repository["native_artifact_root"] == (
            "/Users/eugene/projects/ksdft2effmass"
        )
        assert summary["all_criteria_passed"] is True

    def test_artifact__adapter_schema__accepts_closed_result_and_authorization(
        self, tmp_path: Path
    ) -> None:
        """Validate both closed Stage C adapter wire contracts.

        Evidence ID: SV-RM-DEFECT2D-C-022

        Requirement: Adapter-authored results and future execution authorizations use
        closed Draft 2020-12 schemas with frozen outputs and resource ceilings.

        Method: Apply each maintained schema to its corresponding authored record.

        Oracle: `stage-c-result.schema.json` and
        `stage-c-execution-authorization.schema.json` own the wire shapes.

        Acceptance: Both validators report no errors.

        Interpretation: Passing establishes wire conformance only.

        Limitations: Schema validity does not authorize execution or prove provenance.
        """

        stage = self.stage_directory()
        result_schema = self.read_json(stage / "stage-c-result.schema.json")
        authorization_schema = self.read_json(
            stage / "stage-c-execution-authorization.schema.json"
        )
        result = self.read_json(self.make_adapter_result(tmp_path))
        authorization = self.read_json(self.authorization_fixture())
        assert list(Draft202012Validator(result_schema).iter_errors(result)) == []
        assert (
            list(Draft202012Validator(authorization_schema).iter_errors(authorization))
            == []
        )

    def test_artifact__adapter_verifier__reconstructs_authored_sources_independently(
        self, tmp_path: Path
    ) -> None:
        """Independently reconstruct adapter-authored parent behavior.

        Evidence ID: SV-RM-DEFECT2D-C-023

        Requirement: The verifier independently converts the five authored records,
        rebuilds anisotropic energies and hoppings, and reconstructs every fit.

        Method: Execute the verifier in adapter-fixture mode as a separate process.

        Oracle: The adopted contract requires inverse-Fourier and QR reconstruction
        without runner imports, matrices, or caches.

        Acceptance: Verification reports PASS, 208 routes, 1,040 fits, no runner
        import, no normal equations, and false accepted-parent-read status.

        Interpretation: Passing verifies an independent synthetic adapter oracle.

        Limitations: It is not verification of accepted-parent contents.
        """

        stage = self.stage_directory()
        result = self.make_adapter_result(tmp_path)
        process = subprocess.run(
            [
                sys.executable,
                str(stage / "verify_stage_c_parent.py"),
                "--accepted-parent-design",
                str(stage / "stage-c-accepted-parent-design.json"),
                "--authored-adapter-fixture",
                str(self.adapter_fixture()),
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
        assert report["runner_imported"] is False
        assert report["normal_equations_used"] is False
        assert report["accepted_parent_read"] is False

    def test_artifact__authorization__rejects_nonexecuting_fixture_before_parent_read(
        self,
    ) -> None:
        """Fail before accepted inputs when execution authority is not exact.

        Evidence ID: SV-RM-DEFECT2D-C-024

        Requirement: Post-HC17 execution mode still requires the exact canonical
        authorization path and must preserve the immutable retained result when a
        different schema-valid authorization is supplied.

        Method: Capture the canonical retained result bytes, then invoke execution
        mode with the authored authorization at its maintained fixture path rather
        than the consumed HC17 authorization path.

        Oracle: HC17 binds one exact consumed authorization and immutable result;
        the authored fixture is not accepted execution authority.

        Acceptance: The command fails, names the authorization-path mismatch, and
        the canonical retained result bytes remain exactly unchanged.

        Interpretation: Passing verifies fail-closed pre-read authority ordering and
        byte-preserving refusal without rerun or overwrite.

        Limitations: Rejection proves authority-path enforcement and result
        immutability, not another accepted-parent execution.
        """

        stage = self.stage_directory()
        output = stage / "stage-c-accepted-parent-result.json"
        retained_result = output.read_bytes()
        process = subprocess.run(
            [
                sys.executable,
                str(stage / "run_stage_c_parent.py"),
                "--accepted-parent-design",
                str(stage / "stage-c-accepted-parent-design.json"),
                "--execution-authorization",
                str(self.authorization_fixture()),
                "--repository-root",
                str(self.repository_root()),
                "--output",
                str(output),
            ],
            cwd=self.repository_root(),
            check=False,
            capture_output=True,
            text=True,
        )
        assert process.returncode != 0
        assert "execution authorization path differs" in process.stderr
        assert output.read_bytes() == retained_result

    def test_artifact__adapter_serialization__is_deterministic_and_identity_bound(
        self, tmp_path: Path
    ) -> None:
        """Retain deterministic bytes and reject mutated source identity.

        Evidence ID: SV-RM-DEFECT2D-C-025

        Requirement: Identical authored adapter records serialize identically, report
        their exact byte count, and a wrong Stage B identity fails before output.

        Method: Run twice, compare bytes and retained byte count, then mutate only the
        authored Stage B stage identity and rerun to a new scratch path.

        Oracle: The adapter contract fixes source identities and overwrite-safe
        deterministic serialization.

        Acceptance: Clean bytes agree exactly, output_bytes equals file size, and the
        mutated invocation fails without creating output.

        Interpretation: Passing verifies deterministic adapter and identity behavior.

        Limitations: Synthetic identity checks do not authenticate future authority.
        """

        first = self.make_adapter_result(tmp_path, "adapter-first.json")
        second = self.make_adapter_result(tmp_path, "adapter-second.json")
        assert first.read_bytes() == second.read_bytes()
        payload = self.read_json(first)
        provenance = cast(dict[str, JsonValue], payload["provenance"])
        observation = cast(dict[str, JsonValue], provenance["execution_observation"])
        assert observation["output_bytes"] == first.stat().st_size
        fixture = self.read_json(self.adapter_fixture())
        sources = cast(dict[str, JsonValue], fixture["sources"])
        stage_b = cast(
            dict[str, JsonValue],
            sources["accepted_stage_b_parent_and_route_evidence"],
        )
        stage_b["stage_id"] = "wrong_stage"
        mutated = tmp_path / "mutated-adapter-fixture.json"
        mutated.write_text(json.dumps(fixture, indent=2) + "\n")
        rejected = tmp_path / "mutated-adapter-result.json"
        stage = self.stage_directory()
        process = subprocess.run(
            [
                sys.executable,
                str(stage / "run_stage_c_parent.py"),
                "--accepted-parent-design",
                str(stage / "stage-c-accepted-parent-design.json"),
                "--authored-adapter-fixture",
                str(mutated),
                "--authored-adapter-output",
                str(rejected),
            ],
            cwd=self.repository_root(),
            check=False,
            capture_output=True,
            text=True,
        )
        assert process.returncode != 0
        assert not rejected.exists()
