r"""Software verification of ``StageCParentSvgPlotter``.

Evidence profile: routine

Bounded artifact scope: deterministic retained-result SVG rendering and exclusive-output
refusal.

Facet and represented meaning

The artifact represents deterministic SVG rendering from retained scalar Stage C JSON
for authored-parent and accepted-shaped synthetic records.

Intrinsic and cross-object scope

The plotter owns rendering determinism, accepted-flag rendering, and exclusive-output
refusal. It does not own Stage C calculation or result verification.

VVUQ and scientific exclusions

This is software verification of rendering behavior. The SVG and accepted-shaped
synthetic input are not accepted scientific evidence, validation, uncertainty
quantification, publication, or release status.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import cast

import pytest

from ksdft2effmass.campaigns.research_monograph import StageCParentSvgPlotter

type JsonScalar = None | bool | int | float | str
type JsonValue = JsonScalar | list[JsonValue] | dict[str, JsonValue]

pytestmark = pytest.mark.software_verification
SUT = StageCParentSvgPlotter


class TestStageCParentSvgPlotter:
    """Own software verification of the Stage C retained-result plotter."""

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
    def adapter_fixture(cls) -> Path:
        """Return the maintained authored multi-record adapter fixture.

        Evidence ID: Helper owns no identifier.
        """

        return (
            Path(__file__).resolve().parent
            / "resources/stage-c-accepted-parent-adapter-authored-fixture.json"
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

        result = self.make_parent_result(tmp_path)
        first = tmp_path / "first.svg"
        second = tmp_path / "second.svg"
        SUT().execute(result, first)
        SUT().execute(result, second)
        assert first.read_bytes() == second.read_bytes()
        original = first.read_bytes()
        with pytest.raises(FileExistsError):
            SUT().execute(result, first)
        assert first.read_bytes() == original

    def test_artifact__plotter__accepts_retained_parent_and_writes_exclusively(
        self, tmp_path: Path
    ) -> None:
        """Render an accepted-shaped synthetic result without replacement.

        Evidence ID: SV-RM-DEFECT2D-C-028

        Requirement: The complete protected workflow can plot an accepted-parent
        result, and a preexisting target is preserved by exclusive creation.

        Method: Mark an authored scratch result as accepted-shaped, render it, then
        invoke the plotter against a sentinel output.

        Oracle: Plotting consumes retained scalar JSON only and uses exclusive text
        creation rather than check-then-write.

        Acceptance: The accepted title is rendered and sentinel bytes are unchanged
        after a failing invocation.

        Interpretation: Passing verifies accepted-flag support and atomic refusal.

        Limitations: Mutating the flag creates test data, not accepted evidence.
        """

        payload = self.read_json(self.make_adapter_result(tmp_path))
        payload["accepted_parent_read"] = True
        source = tmp_path / "accepted-shaped-synthetic.json"
        source.write_text(json.dumps(payload, indent=2) + "\n")
        output = tmp_path / "accepted.svg"
        SUT().execute(source, output)
        assert "Stage C accepted-parent retained result" in output.read_text()
        sentinel = tmp_path / "sentinel.svg"
        sentinel.write_bytes(b"preserve-me")
        with pytest.raises(FileExistsError):
            SUT().execute(source, sentinel)
        assert sentinel.read_bytes() == b"preserve-me"
