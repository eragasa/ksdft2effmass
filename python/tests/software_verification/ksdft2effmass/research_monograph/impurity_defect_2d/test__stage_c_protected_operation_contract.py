r"""Software verification of Stage C authored protected operation.

Evidence profile: routine

Bounded artifact scope: authored complete-package success, terminal failure, one-attempt
consumption, and byte-preserving no-retry behavior.

Facet and represented meaning

The artifact represents one complete authored operation package, including attempt
journal, result, verifier log, plot, report, native-evidence manifest, and finalized
checksums.

Intrinsic and cross-object scope

This module owns success and failure package retention, one-attempt consumption, and no-
retry byte preservation for authored records. Accepted-parent execution remains outside
this test artifact.

VVUQ and scientific exclusions

This is software verification of synthetic operation behavior. It grants no protected-
execution authority and establishes no accepted-parent result, scientific validation,
uncertainty quantification, publication, or release status.
"""

from __future__ import annotations

import hashlib
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


class TestStageCProtectedOperationContract:
    """Own software verification of authored Stage C operation retention."""

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
    def make_operation_package(
        cls, tmp_path: Path, name: str = "operation-package"
    ) -> Path:
        """Run the complete protected operation with authored records only.

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
                "--authored-operation-fixture",
                str(cls.adapter_fixture()),
                "--authored-operation-directory",
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

    def test_artifact__protected_operation__retains_complete_package_once(
        self, tmp_path: Path
    ) -> None:
        """Produce and consume one complete authored operation package.

        Evidence ID: SV-RM-DEFECT2D-C-026

        Requirement: One protected operation owns an attempt journal, result,
        verification log, SVG, report, manifest, and finalized checksum catalog.

        Method: Run the exact operation inventory with authored records, verify every
        retained identity, then invoke the same package path again.

        Oracle: The authorization contract fixes ordered operations and exclusive
        retained outputs; the checksum catalog owns the five finalized products.

        Acceptance: Seven outputs exist, verification passes, checksums agree, the
        journal ends in SUCCESS, and rerun fails without changing any byte.

        Interpretation: Passing verifies complete production and durable consumption.

        Limitations: The package is authored software verification, not execution.
        """

        package = self.make_operation_package(tmp_path)
        names = {
            "stage-c-accepted-parent-attempt.jsonl",
            "stage-c-accepted-parent-result.json",
            "stage-c-accepted-parent-verification.log",
            "stage-c-accepted-parent-summary.svg",
            "stage-c-accepted-parent-report.md",
            "stage-c-accepted-parent-native-evidence-manifest.json",
            "stage-c-accepted-parent-SHA256SUMS",
        }
        assert {path.name for path in package.iterdir() if path.is_file()} == names
        events = [
            cast(dict[str, JsonValue], json.loads(line))
            for line in (package / "stage-c-accepted-parent-attempt.jsonl")
            .read_text()
            .splitlines()
        ]
        assert [event["event"] for event in events] == ["STARTED", "TERMINAL"]
        assert events[1]["status"] == "SUCCESS"
        success_identities = cast(list[JsonValue], events[1]["output_identities"])
        assert len(success_identities) == 6
        verification = self.read_json(
            package / "stage-c-accepted-parent-verification.log"
        )
        assert verification["verification"] == "PASS"
        result = self.read_json(package / "stage-c-accepted-parent-result.json")
        schema = self.read_json(self.stage_directory() / "stage-c-result.schema.json")
        assert list(Draft202012Validator(schema).iter_errors(result)) == []
        provenance = cast(dict[str, JsonValue], result["provenance"])
        authorization = self.read_json(self.authorization_fixture())
        assert provenance["operation_inventory"] == authorization["operation_inventory"]
        checksum_lines = (
            (package / "stage-c-accepted-parent-SHA256SUMS").read_text().splitlines()
        )
        assert checksum_lines == [
            (f"{hashlib.sha256((package / name).read_bytes()).hexdigest()}  {name}")
            for name in (
                "stage-c-accepted-parent-result.json",
                "stage-c-accepted-parent-verification.log",
                "stage-c-accepted-parent-summary.svg",
                "stage-c-accepted-parent-report.md",
                "stage-c-accepted-parent-native-evidence-manifest.json",
            )
        ]
        original: dict[str, bytes] = {
            name: (package / name).read_bytes() for name in names
        }
        stage = self.stage_directory()
        retry = subprocess.run(
            [
                sys.executable,
                str(stage / "run_stage_c_parent.py"),
                "--accepted-parent-design",
                str(stage / "stage-c-accepted-parent-design.json"),
                "--authored-operation-fixture",
                str(self.adapter_fixture()),
                "--authored-operation-directory",
                str(package),
            ],
            cwd=self.repository_root(),
            check=False,
            capture_output=True,
            text=True,
        )
        assert retry.returncode != 0
        assert {name: (package / name).read_bytes() for name in names} == original

    def test_artifact__protected_operation__retains_failure_and_forbids_retry(
        self, tmp_path: Path
    ) -> None:
        """Consume the attempt before authored source validation can fail.

        Evidence ID: SV-RM-DEFECT2D-C-027

        Requirement: A parser or invariant failure after authority validation must be
        retained as terminal FAILURE and consume the one-attempt authority.

        Method: Corrupt only the authored Stage B identity, invoke the complete
        operation, then retry the same package with the valid fixture.

        Oracle: The attempt journal is exclusively created before source conversion.

        Acceptance: The first call fails with STARTED then terminal FAILURE; the
        second call also fails, changes no journal bytes, and creates no result.

        Interpretation: Passing verifies durable failure and no favorable rerun.

        Limitations: Process termination outside Python can retain STARTED without a
        terminal event, but that journal still consumes the attempt.
        """

        fixture = self.read_json(self.adapter_fixture())
        sources = cast(dict[str, JsonValue], fixture["sources"])
        stage_b = cast(
            dict[str, JsonValue],
            sources["accepted_stage_b_parent_and_route_evidence"],
        )
        stage_b["stage_id"] = "wrong_stage"
        mutated = tmp_path / "invalid-operation-fixture.json"
        mutated.write_text(json.dumps(fixture, indent=2) + "\n")
        package = tmp_path / "failed-package"
        stage = self.stage_directory()
        base = [
            sys.executable,
            str(stage / "run_stage_c_parent.py"),
            "--accepted-parent-design",
            str(stage / "stage-c-accepted-parent-design.json"),
            "--authored-operation-directory",
            str(package),
        ]
        failed = subprocess.run(
            [*base, "--authored-operation-fixture", str(mutated)],
            cwd=self.repository_root(),
            check=False,
            capture_output=True,
            text=True,
        )
        assert failed.returncode != 0
        journal = package / "stage-c-accepted-parent-attempt.jsonl"
        journal_bytes = journal.read_bytes()
        events = [
            cast(dict[str, JsonValue], json.loads(line))
            for line in journal.read_text().splitlines()
        ]
        assert [event["event"] for event in events] == ["STARTED", "TERMINAL"]
        assert events[1]["status"] == "FAILURE"
        failure_error = cast(dict[str, JsonValue], events[1]["error"])
        assert len(cast(str, failure_error["sha256"])) == 64
        assert not (package / "stage-c-accepted-parent-result.json").exists()
        retry = subprocess.run(
            [*base, "--authored-operation-fixture", str(self.adapter_fixture())],
            cwd=self.repository_root(),
            check=False,
            capture_output=True,
            text=True,
        )
        assert retry.returncode != 0
        assert journal.read_bytes() == journal_bytes
        assert not (package / "stage-c-accepted-parent-result.json").exists()
