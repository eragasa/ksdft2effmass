"""Guard the common mechanics of executable experiment composition roots."""

from __future__ import annotations

import ast
from pathlib import Path


class TestExperimentScriptConventions:
    """Require every current and future experiment entry point to conform."""

    _REPOSITORY = Path(__file__).resolve().parents[5]
    _EXPERIMENTS = _REPOSITORY / "experiments"

    @classmethod
    def _entrypoints(cls) -> dict[str, tuple[ast.Module, ast.FunctionDef]]:
        entrypoints: dict[str, tuple[ast.Module, ast.FunctionDef]] = {}
        for path in sorted(cls._EXPERIMENTS.rglob("*.py")):
            relative = path.relative_to(cls._EXPERIMENTS)
            if "tests" in relative.parts or "src" in relative.parts:
                continue
            module = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
            mains = tuple(
                node
                for node in module.body
                if isinstance(node, ast.FunctionDef) and node.name == "main"
            )
            if len(mains) > 1:
                raise AssertionError(f"multiple main functions: {relative}")
            if mains:
                entrypoints[relative.as_posix()] = (module, mains[0])
        return entrypoints

    @staticmethod
    def _has_system_exit_main_guard(module: ast.Module) -> bool:
        for node in module.body:
            if not isinstance(node, ast.If):
                continue
            if not (
                isinstance(node.test, ast.Compare)
                and isinstance(node.test.left, ast.Name)
                and node.test.left.id == "__name__"
            ):
                continue
            for descendant in ast.walk(node):
                if not isinstance(descendant, ast.Raise):
                    continue
                exception = descendant.exc
                if not isinstance(exception, ast.Call):
                    continue
                if not (
                    isinstance(exception.func, ast.Name)
                    and exception.func.id == "SystemExit"
                    and len(exception.args) == 1
                ):
                    continue
                argument = exception.args[0]
                if (
                    isinstance(argument, ast.Call)
                    and isinstance(argument.func, ast.Name)
                    and argument.func.id == "main"
                    and not argument.args
                    and not argument.keywords
                ):
                    return True
        return False

    @staticmethod
    def _returns_zero(main: ast.FunctionDef) -> bool:
        return any(
            isinstance(node, ast.Return)
            and isinstance(node.value, ast.Constant)
            and type(node.value.value) is int
            and node.value.value == 0
            for node in ast.walk(main)
        )

    def test_every_entrypoint_has_the_standard_process_contract(self) -> None:
        """Require documented integer roots that terminate through SystemExit."""
        entrypoints = self._entrypoints()
        assert entrypoints
        for path, (module, main) in entrypoints.items():
            assert ast.get_docstring(module), path
            assert isinstance(main.returns, ast.Name), path
            assert main.returns.id == "int", path
            assert self._returns_zero(main), path
            assert self._has_system_exit_main_guard(module), path
