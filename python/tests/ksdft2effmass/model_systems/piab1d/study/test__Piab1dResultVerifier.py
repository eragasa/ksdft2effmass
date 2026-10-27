r"""Software verification of independent PIAB1D result verification."""

import json
import subprocess
import sys
from collections.abc import Callable
from pathlib import Path
from typing import cast

import pytest

from ksdft2effmass.model_systems.piab1d import (
    JsonValue,
    Piab1dResidualStudyEvaluator,
    Piab1dResultVerifier,
    Piab1dStudyInputDeserializer,
    Piab1dStudyResultSerializer,
)

pytestmark = [pytest.mark.integration, pytest.mark.software_verification]
SUT = Piab1dResultVerifier


class TestPiab1dResultVerifier:
    """Own software evidence for the independent result verifier."""

    @staticmethod
    def repository_root() -> Path:
        return Path(__file__).resolve().parents[6]

    def authored_result(self, destination: Path) -> tuple[Path, Path]:
        root = self.repository_root()
        calculation = root / "calculations" / "piab1d"
        input_path = calculation / "input.json"
        definition = Piab1dStudyInputDeserializer().execute(input_path.read_bytes())
        result = Piab1dResidualStudyEvaluator().execute(definition)
        destination.write_bytes(
            Piab1dStudyResultSerializer().execute(
                result,
                input_path,
                calculation / "run_experiment.py",
                root,
            )
        )
        return destination, root

    def test_method__execute__accepts_current_version_two_result(
        self,
        tmp_path: Path,
    ) -> None:
        result, root = self.authored_result(tmp_path / "result.json")

        Piab1dResultVerifier().execute(result, root)

    def test_method__execute__rejects_inconsistent_quadrature_weights(
        self,
        tmp_path: Path,
    ) -> None:
        result, root = self.authored_result(tmp_path / "result.json")
        payload = cast(
            dict[str, JsonValue],
            json.loads(result.read_text(encoding="utf-8")),
        )
        quadrature = cast(dict[str, JsonValue], payload["quadrature"])
        weights = cast(list[JsonValue], quadrature["interior_weights"])
        weights[0] = 2.0
        result.write_text(
            json.dumps(payload, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )

        with pytest.raises(AssertionError):
            Piab1dResultVerifier().execute(result, root)

    @pytest.mark.parametrize(
        ("field", "mutator"),
        [
            ("spacing", lambda value: float(cast(float, value)) * 2.0),
            (
                "interior_full_grid_indices",
                lambda value: [99, *cast(list[JsonValue], value)[1:]],
            ),
        ],
    )
    def test_method__execute__rejects_inconsistent_quadrature_contract_fields(
        self,
        tmp_path: Path,
        field: str,
        mutator: Callable[[JsonValue], JsonValue],
    ) -> None:
        result, root = self.authored_result(tmp_path / "result.json")
        payload = cast(
            dict[str, JsonValue],
            json.loads(result.read_text(encoding="utf-8")),
        )
        quadrature = cast(dict[str, JsonValue], payload["quadrature"])
        quadrature[field] = mutator(quadrature[field])
        result.write_text(
            json.dumps(payload, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )

        with pytest.raises((AssertionError, ValueError)):
            Piab1dResultVerifier().execute(result, root)

    def test_method__execute__rejects_inconsistent_diagonal_mass_matrix(
        self,
        tmp_path: Path,
    ) -> None:
        result, root = self.authored_result(tmp_path / "result.json")
        payload = cast(
            dict[str, JsonValue],
            json.loads(result.read_text(encoding="utf-8")),
        )
        quadrature = cast(dict[str, JsonValue], payload["quadrature"])
        mass = cast(dict[str, JsonValue], quadrature["diagonal_mass_matrix"])
        diagonal = cast(list[JsonValue], mass["diagonal"])
        diagonal[0] = 2.0
        result.write_text(
            json.dumps(payload, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )

        with pytest.raises(AssertionError):
            Piab1dResultVerifier().execute(result, root)

    def test_method__execute__rejects_inconsistent_normalized_amplitudes(
        self,
        tmp_path: Path,
    ) -> None:
        result, root = self.authored_result(tmp_path / "result.json")
        payload = cast(
            dict[str, JsonValue],
            json.loads(result.read_text(encoding="utf-8")),
        )
        matrices = cast(dict[str, JsonValue], payload["matrices"])
        amplitudes = cast(
            list[JsonValue],
            matrices["retained_nodal_amplitudes_quadrature_normalized"],
        )
        first_row = cast(list[JsonValue], amplitudes[0])
        first_row[0] = float(cast(float, first_row[0])) + 1.0
        result.write_text(
            json.dumps(payload, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )

        with pytest.raises(AssertionError):
            Piab1dResultVerifier().execute(result, root)

    def test_method__execute__rejects_changed_dependency_revision(
        self,
        tmp_path: Path,
    ) -> None:
        result, root = self.authored_result(tmp_path / "result.json")
        payload = cast(
            dict[str, JsonValue],
            json.loads(result.read_text(encoding="utf-8")),
        )
        provenance = cast(dict[str, JsonValue], payload["provenance"])
        dependencies = cast(list[JsonValue], provenance["dependency_identities"])
        optimization = cast(dict[str, JsonValue], dependencies[0])
        optimization["revision"] = "0" * 40
        result.write_text(
            json.dumps(payload, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )

        with pytest.raises(ValueError, match="dependency identities"):
            Piab1dResultVerifier().execute(result, root)

    def test_method__execute__rejects_invalid_schema_under_optimized_python(
        self,
        tmp_path: Path,
    ) -> None:
        result, root = self.authored_result(tmp_path / "result.json")
        invalid = tmp_path / "invalid-result.json"
        invalid.write_bytes(
            result.read_bytes().replace(
                b'\n  "schema_version": 2,\n',
                b'\n  "schema_version": 999,\n',
                1,
            )
        )
        command = (
            "from pathlib import Path; "
            "from ksdft2effmass.model_systems.piab1d import "
            "Piab1dResultVerifier; "
            "Piab1dResultVerifier().execute(Path(__import__('sys').argv[1]), "
            "Path(__import__('sys').argv[2]))"
        )

        completed = subprocess.run(
            [sys.executable, "-O", "-c", command, str(invalid), str(root)],
            check=False,
            capture_output=True,
            text=True,
        )

        assert completed.returncode != 0
        assert "schema_version" in completed.stderr

    def test_artifact__dependency__excludes_particle_in_box_producer(self) -> None:
        root = self.repository_root()
        source = (
            root
            / "python"
            / "src"
            / "ksdft2effmass"
            / "model_systems"
            / "piab1d"
            / "study"
            / "verification.py"
        )
        source_text = source.read_text(encoding="utf-8")

        assert "from projectkoios.physkit.qm.piab1d" not in source_text
        assert "from projectkoios.numerics.quadrature" not in source_text
        assert "from .evaluation import" not in source_text
