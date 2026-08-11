"""Deterministic collected-node projections from immutable Python evidence models."""

from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass

from .model import PythonTestModuleModel


@dataclass(frozen=True, slots=True)
class _PythonTestNodeFact:
    """One source-derived pytest node identity and its owning test function."""

    node_id: str
    module_path: str
    function_name: str
    parameter_id: str | None


class _PythonTestNodeProjector:
    """Project explicit static parameter identities without executing pytest."""

    __slots__ = ()

    def execute(
        self, models: tuple[PythonTestModuleModel, ...]
    ) -> tuple[_PythonTestNodeFact, ...]:
        """Return path-sorted node facts from conforming parsed module models."""
        if type(models) is not tuple or any(
            type(model) is not PythonTestModuleModel for model in models
        ):
            raise TypeError("models must contain PythonTestModuleModel values")
        facts: list[_PythonTestNodeFact] = []
        for model in models:
            for function in model.functions:
                if not function.is_test:
                    continue
                base = f"{model.path}::{function.name}"
                if not function.parameterizations:
                    facts.append(
                        _PythonTestNodeFact(base, model.path, function.name, None)
                    )
                    continue
                if len(function.parameterizations) != 1:
                    raise ValueError(
                        "canonical evidence uses one explicit parameterization per test"
                    )
                parameterization = function.parameterizations[0]
                identifiers = (
                    parameterization.decorator_ids
                    if parameterization.decorator_ids_present
                    else tuple(case.literal_id for case in parameterization.cases)
                )
                if not identifiers or any(identity is None for identity in identifiers):
                    raise ValueError(
                        "canonical parameterized evidence requires explicit literal IDs"
                    )
                literal_ids = tuple(identity for identity in identifiers if identity)
                counts = Counter(literal_ids)
                occurrences: defaultdict[str, int] = defaultdict(int)
                for literal_id in literal_ids:
                    parameter_id = literal_id
                    if counts[literal_id] > 1:
                        parameter_id += str(occurrences[literal_id])
                        occurrences[literal_id] += 1
                    facts.append(
                        _PythonTestNodeFact(
                            f"{base}[{parameter_id}]",
                            model.path,
                            function.name,
                            parameter_id,
                        )
                    )
        return tuple(sorted(facts, key=lambda fact: fact.node_id))
