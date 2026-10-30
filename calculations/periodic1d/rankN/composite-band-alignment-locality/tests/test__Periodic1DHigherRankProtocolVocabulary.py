"""Contract tests for maintained protocol terminology and schematics."""

from __future__ import annotations

import re
from pathlib import Path

import pytest

pytestmark = pytest.mark.software_verification


class TestPeriodic1DHigherRankProtocolVocabulary:
    """Keep gauge alignments distinct from diagnostic error channels."""

    def test__protocol__uses_descriptive_gauge_alignment_inventory(self) -> None:
        protocol = (
            Path(__file__).resolve().parents[1]
            / "protocol"
            / "experimental-protocol.tex"
        ).read_text(encoding="utf-8")

        for wire_value in (
            "identity",
            "global-unitary",
            "pointwise-unitary",
            "known-inverse-oracle",
        ):
            assert f"\\path{{{wire_value}}}" in protocol
        assert re.search(r"\bA[0-3]\b", protocol) is None
        without_error_channels = re.sub(
            r"error(?:-| )channels?",
            "",
            protocol,
            flags=re.IGNORECASE,
        )
        remaining = re.search(r"\bchannels?\b", without_error_channels, re.IGNORECASE)
        assert remaining is None

    def test__protocol__contains_scientific_and_typed_lifecycle_schematics(
        self,
    ) -> None:
        protocol = (
            Path(__file__).resolve().parents[1]
            / "protocol"
            / "experimental-protocol.tex"
        ).read_text(encoding="utf-8")

        assert "\\label{fig:scientific-flow}" in protocol
        assert "\\label{fig:typed-lifecycle}" in protocol
        assert "Global-unitary" in protocol
        assert "select at $M=2049$; reuse" in protocol
        assert "typed unresolved status; downstream values absent" in protocol
