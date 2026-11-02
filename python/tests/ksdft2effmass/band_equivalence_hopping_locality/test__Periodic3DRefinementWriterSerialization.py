"""Canonical-byte contracts for periodic-3D refinement writers."""

from collections.abc import Callable
from pathlib import Path

import pytest

CalculationWriterSerializationAssertion = Callable[
    [str, Path, pytest.MonkeyPatch, Path], None
]

pytestmark = [
    pytest.mark.integration,
    pytest.mark.expensive,
    pytest.mark.software_verification,
]

_PERIODIC3D_REFINEMENT_WRITER_PATHS = tuple(
    f"{family}/band_equivalence_hopping_locality/{script}"
    for family in (
        "periodic3d_rank2_simple_cubic",
        "periodic3d_rank2_fcc_diamond",
    )
    for script in ("run_refinement_01.py", "run_refinement_02.py")
)


class TestPeriodic3DRefinementWriterSerialization:
    """Exercise complete refinement writers outside the bounded routine gate."""

    @pytest.mark.parametrize("relative_path", _PERIODIC3D_REFINEMENT_WRITER_PATHS)
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
