"""Canonical-byte contracts for periodic-3D calculation writers."""

from collections.abc import Callable
from pathlib import Path

import pytest

CalculationWriterSerializationAssertion = Callable[
    [str, Path, pytest.MonkeyPatch, Path], None
]

pytestmark = [pytest.mark.integration, pytest.mark.software_verification]

_PERIODIC3D_WRITER_PATHS = (
    *(
        f"{family}/run_development.py"
        for family in (
            "periodic3d/rank2/orthogonal/band-equivalence-locality",
            "periodic3d/rank2/nonorthogonal/band-equivalence-locality",
        )
    ),
    *(
        f"periodic3d/rank2/strain-locality/{script}"
        for script in (
            "run_development.py",
            "run_response_development.py",
            "run_scan_development.py",
        )
    ),
)


class TestPeriodic3DCalculationWriterSerialization:
    """Prevent byte and text regressions in periodic-3D development writers."""

    @pytest.mark.parametrize("relative_path", _PERIODIC3D_WRITER_PATHS)
    def test_writer_executes_and_emits_canonical_json_bytes(
        self,
        relative_path: str,
        tmp_path: Path,
        monkeypatch: pytest.MonkeyPatch,
        repository_root: Path,
        assert_calculation_writer_serialization: (
            CalculationWriterSerializationAssertion
        ),
    ) -> None:
        assert_calculation_writer_serialization(
            relative_path,
            tmp_path,
            monkeypatch,
            repository_root,
        )
