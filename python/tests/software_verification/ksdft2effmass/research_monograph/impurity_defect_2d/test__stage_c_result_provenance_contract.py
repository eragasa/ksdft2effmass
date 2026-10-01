r"""Software verification of Stage C result-provenance contract.

Evidence profile: routine

Bounded artifact scope: closed-schema compatibility between immutable HC17 and later
authored provenance revisions.

Facet and represented meaning

The artifact is the shared closed result schema across immutable HC17 provenance and
later authored software-verification revisions.

Intrinsic and cross-object scope

This module owns compatibility of accepted and authored revision identities and
implementation-source inventories. It does not mutate retained HC17 bytes or rerun
accepted-parent computation.

VVUQ and scientific exclusions

This is software verification of provenance representation. Revision and schema
agreement do not establish numerical correctness, scientific validation, uncertainty
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


class TestStageCResultProvenanceContract:
    """Own software verification of Stage C result-provenance compatibility."""

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

    def test_artifact__result_schema__separates_hc17_and_development_revisions(
        self, tmp_path: Path
    ) -> None:
        """Keep accepted provenance frozen while allowing later authored revisions.

        Evidence ID: SV-RM-DEFECT2D-C-030

        Requirement: The immutable HC17 result remains bound to its authorized Git
        revision while post-HC17 authored verification records the current revision.

        Method: Validate the retained accepted result and one fresh authored result
        against the same closed schema, then compare their represented revisions.

        Oracle: Accepted execution provenance is fixed by HC17; authored software
        verification is not execution authority and must not claim the HC17 revision.

        Acceptance: Both records validate, HC17 retains its exact authorized
        revision and six historical implementation identities, and the authored
        result records a different lowercase object ID plus all sixteen current
        implementation-source identities.

        Interpretation: Passing verifies provenance compatibility across the
        post-HC17 module extraction without relabeling accepted evidence.

        Limitations: Revision identity does not establish numerical correctness or
        scientific validation.
        """

        stage = self.stage_directory()
        schema = self.read_json(stage / "stage-c-result.schema.json")
        accepted = self.read_json(stage / "stage-c-accepted-parent-result.json")
        authored = self.read_json(self.make_parent_result(tmp_path))
        validator = Draft202012Validator(schema)
        assert list(validator.iter_errors(accepted)) == []
        assert list(validator.iter_errors(authored)) == []
        accepted_provenance = cast(dict[str, JsonValue], accepted["provenance"])
        authored_provenance = cast(dict[str, JsonValue], authored["provenance"])
        accepted_repository = cast(
            dict[str, JsonValue], accepted_provenance["repository"]
        )
        authored_repository = cast(
            dict[str, JsonValue], authored_provenance["repository"]
        )
        accepted_revision = cast(str, accepted_repository["revision"])
        authored_revision = cast(str, authored_repository["revision"])
        accepted_implementations = cast(
            list[JsonValue], accepted_provenance["implementation_identities"]
        )
        authored_implementations = cast(
            list[JsonValue], authored_provenance["implementation_identities"]
        )
        authored_roles = tuple(
            cast(str, cast(dict[str, JsonValue], value)["role"])
            for value in authored_implementations
        )
        assert accepted_revision == "9def2718ee763faf2060eb692739600485de5c72"
        assert authored_revision != accepted_revision
        assert len(authored_revision) in (40, 64)
        assert set(authored_revision) <= set("0123456789abcdef")
        assert len(accepted_implementations) == 6
        assert authored_roles == (
            "runner_cli",
            "record_model",
            "record_deserializers",
            "operator_construction",
            "model_fitting",
            "schedule_executor",
            "result_evaluation",
            "execution_authorization",
            "retention",
            "result_context",
            "protected_workflow",
            "verifier_cli",
            "independent_verifier",
            "plotter",
            "result_schema",
            "execution_authorization_schema",
        )
