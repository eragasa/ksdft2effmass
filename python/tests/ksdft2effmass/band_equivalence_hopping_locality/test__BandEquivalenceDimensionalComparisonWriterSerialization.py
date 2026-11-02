"""Canonical-byte contract for the dimensional-comparison writer."""

from collections.abc import Callable
from pathlib import Path

import pytest

CalculationWriterSerializationAssertion = Callable[
    [str, Path, pytest.MonkeyPatch, Path], None
]

pytestmark = [pytest.mark.integration, pytest.mark.software_verification]


class TestBandEquivalenceDimensionalComparisonWriterSerialization:
    """Keep cross-dimensional writing separate from dimensional calculations."""

    def test_writer_executes_and_emits_canonical_json_bytes(
        self,
        tmp_path: Path,
        monkeypatch: pytest.MonkeyPatch,
        repository_root: Path,
        assert_calculation_writer_serialization: (
            CalculationWriterSerializationAssertion
        ),
    ) -> None:
        assert_calculation_writer_serialization(
            "band-equivalence-dimensional-comparison/plot_shell_scale_decision_landscapes.py",
            tmp_path,
            monkeypatch,
            repository_root,
        )
