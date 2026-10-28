"""Static contract tests for direct Fourier-locality effect adapters."""

import ast
from pathlib import Path


class TestPeriodic1DFourierLocalityDirectScripts:
    """Establish the closed direct calculate, verify, and render adapter set."""

    @staticmethod
    def scripts() -> tuple[Path, ...]:
        repository = Path(__file__).resolve().parents[5]
        calculation = (
            repository / "calculations" / "periodic1d" / "rank1" / "fourier-locality"
        )
        return (
            calculation / "run_01_calculation.py",
            calculation / "run_02_verification.py",
            calculation / "run_03_render.py",
        )

    def test__scripts__are_direct_effect_adapters(self) -> None:
        scripts = self.scripts()

        assert all(path.is_file() for path in scripts)
        for path in scripts:
            source = path.read_text(encoding="utf-8")
            tree = ast.parse(source, filename=str(path))
            imported_modules = {
                alias.name
                for node in ast.walk(tree)
                if isinstance(node, ast.Import)
                for alias in node.names
            }
            imported_from = {
                node.module
                for node in ast.walk(tree)
                if isinstance(node, ast.ImportFrom) and node.module is not None
            }
            functions = {
                node.name
                for node in ast.walk(tree)
                if isinstance(node, ast.FunctionDef)
            }
            assert "argparse" not in imported_modules | imported_from
            assert "json" not in imported_modules | imported_from
            assert "main" not in functions
            assert "Workflow" not in source
            assert "workflow/" not in source
            compile(source, str(path), "exec")

    def test__scripts__declare_the_same_closed_execution(self) -> None:
        sources = [path.read_text(encoding="utf-8") for path in self.scripts()]

        assert all(
            'EXECUTION_ID = "direct-controlled-four-state-n256"' in source
            for source in sources
        )
        assert all(
            'CALCULATION_FAMILY = "periodic1d-rank1-fourier-locality"' in source
            for source in sources
        )
        assert all(
            "ksdft2effmass.periodic1d.controlled-four-state-parent.v1" in source
            for source in sources
        )
