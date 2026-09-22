r"""Software verification of retained paired-silicon CPN architecture-probe report.

Evidence profile: routine

Bounded artifact scope: retained paired-silicon CPN architecture-probe report.

Facet and represented meaning

Deterministic example adaptation, CPN replay, and comparison reporting over the
two committed compact observations without retired calculator probe records.

Intrinsic and cross-object scope

The checked-in report bytes are the exact oracle for the bounded example. The
example must require no native run state or scientific executable.

VVUQ and scientific exclusions

This is orchestration software verification only. It establishes no numerical
comparison, parent-model agreement, scientific validation, or acceptance.
"""

import ast
import os
import subprocess
import sys
from pathlib import Path

import pytest

pytestmark = pytest.mark.software_verification


class TestRetainedSiliconBandProbe:
    """Own the retained tutorial's report and calculator-independent adaptation."""

    def test_artifact__retained_probe__reproduces_committed_report(self) -> None:
        """Evidence ID: SV-RETAINED-SILICON-BAND-PROBE-001

        Requirement: The committed QE and ABINIT compact observations alone reproduce
        the retained CPN replay and fail-closed comparison report.

        Method: Run the deterministic Python example in a captured local subprocess.

        Oracle: The committed architecture-probe JSON supplies the exact expected bytes.

        Acceptance: The script exits successfully, writes no diagnostic stream, and
        its stdout bytes equal the committed expected JSON bytes exactly.

        Interpretation: Failure identifies adapter, replay, comparison, or report drift.

        Limitations: The compact inputs cannot support numerical backend comparison.
        """
        repository_root = Path(__file__).resolve().parents[5]
        script = repository_root / (
            "examples/tutorials/silicon-bands/scripts/compare_retained_observations.py"
        )
        expected = repository_root / (
            "examples/tutorials/silicon-bands/expected/internal-cpn-architecture-probe.json"
        )
        environment = os.environ.copy()
        source_root = str(repository_root / "python/src")
        environment["PYTHONPATH"] = os.pathsep.join(
            filter(None, (source_root, environment.get("PYTHONPATH", "")))
        )

        completed = subprocess.run(
            [sys.executable, str(script)],
            cwd=repository_root,
            env=environment,
            check=True,
            capture_output=True,
        )

        assert completed.stderr == b""
        assert completed.stdout == expected.read_bytes()

    def test_artifact__dependency__adapts_without_calculator_imports(self) -> None:
        """Evidence ID: SV-RETAINED-SILICON-BAND-PROBE-002

        Requirement: The retained tutorial adapts logical replay and analysis facts
        without importing calculator input/output records or a replacement facade.

        Acceptance: The example's static absolute imports contain no calculator
        package dependency.

        Limitations: This checks static imports, not arbitrary dynamic import code.
        """
        script = Path(__file__).resolve().parents[5] / (
            "examples/tutorials/silicon-bands/scripts/compare_retained_observations.py"
        )
        tree = ast.parse(script.read_text(encoding="utf-8"))
        imports = tuple(
            alias.name
            for node in ast.walk(tree)
            if isinstance(node, ast.Import)
            for alias in node.names
        ) + tuple(
            node.module
            for node in ast.walk(tree)
            if isinstance(node, ast.ImportFrom) and node.module is not None
        )
        assert not any(
            name == "ksdft2effmass.calculators"
            or name.startswith("ksdft2effmass.calculators.")
            for name in imports
        )
