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
        f"{family}/band_equivalence_hopping_locality/run_nominal_calculation.py"
        for family in (
            "periodic3d_rank2_simple_cubic",
            "periodic3d_rank2_fcc_diamond",
        )
    ),
    *(
        f"periodic3d_rank2_bain_path/band_equivalence_hopping_locality/{script}"
        for script in (
            "run_geometry_control.py",
            "run_response_controls.py",
            "run_path_scan.py",
        )
    ),
)


class TestPeriodic3DCalculationWriterSerialization:
    """Prevent byte and text regressions in bounded periodic-3D writers."""

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
