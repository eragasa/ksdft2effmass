"""Compatibility Task-model exports and local-result graph validation.

Architecture-v2 Task values, serializers, and registry queries are owned by
:mod:`ksdft2effmass.harness.task`. This module retains one-way compatibility exports
and the transitional project-local graph validator until normalized Harness
validation replaces its local result contract.
"""

from __future__ import annotations

from ... import task as _task
from .models import LocalIssue, LocalValidationResult

ArchivedTaskSource = _task.ArchivedTaskSource
HarnessTask = _task.HarnessTask
HarnessTaskDeserializer = _task.HarnessTaskDeserializer
HarnessTaskRegistry = _task.HarnessTaskRegistry
HarnessTaskSerializer = _task.HarnessTaskSerializer
_require_tuple = _task._require_tuple


class HarnessTaskGraphValidator:
    """Validate structural relations among explicitly supplied Tasks.

    Results use existing project-local :class:`LocalValidationResult` and
    ``PIHL.TASK.*`` issue codes.  Codes are ordered lexically by the existing
    result contract; no lifecycle, chain-selection, or repository policy is
    inferred.
    """

    __slots__ = ()

    def execute(self, tasks: tuple[HarnessTask, ...]) -> LocalValidationResult:
        """Return deterministic findings for one complete explicit Task graph.

        Parameters
        ----------
        tasks
            Exact nonempty tuple treated as the complete graph.

        Returns
        -------
        LocalValidationResult
            ``PASS`` or lexically ordered issues using ``PIHL.TASK.DUPLICATE_ID``,
            ``PARENT_MISSING``, ``PARENT_CYCLE``, ``PREREQUISITE_MISSING``,
            ``PREREQUISITE_CYCLE``, ``SUPERSESSION_MISSING``,
            ``SUPERSESSION_CYCLE``, ``INTAKE_PATH_DUPLICATE``, and
            ``DOCUMENTATION_PATH_DUPLICATE`` under the ``PIHL.TASK`` namespace.

        Raises
        ------
        TypeError
            If the tuple or a member has the wrong semantic type.
        ValueError
            If the explicit Task tuple is empty.

        Notes
        -----
        Issue precedence is lexical ``(code, path-or-empty, detail)`` order. Status
        meaning, chain selection, activation, repository discovery, and I/O are
        excluded.
        """
        _require_tuple(tasks, "tasks")
        if not tasks:
            raise ValueError("tasks must be nonempty")
        if any(type(task) is not HarnessTask for task in tasks):
            raise TypeError("tasks must contain HarnessTask")
        issues: list[LocalIssue] = []
        by_id: dict[str, HarnessTask] = {}
        for task in tasks:
            if task.task_id in by_id:
                issues.append(LocalIssue("PIHL.TASK.DUPLICATE_ID", None, task.task_id))
            else:
                by_id[task.task_id] = task
        for task in tasks:
            if task.parent_task_id is not None and task.parent_task_id not in by_id:
                issues.append(
                    LocalIssue(
                        "PIHL.TASK.PARENT_MISSING",
                        task.documentation_path
                        or (
                            task.archived_source.path if task.archived_source else None
                        ),
                        task.parent_task_id,
                    )
                )
            task_path = task.documentation_path or (
                task.archived_source.path if task.archived_source else None
            )
            for dependency in task.task_prerequisite_ids:
                if dependency not in by_id:
                    issues.append(
                        LocalIssue(
                            "PIHL.TASK.PREREQUISITE_MISSING",
                            task_path,
                            dependency,
                        )
                    )
            for replacement in task.superseded_by_task_ids:
                if replacement not in by_id:
                    issues.append(
                        LocalIssue(
                            "PIHL.TASK.SUPERSESSION_MISSING",
                            task_path,
                            replacement,
                        )
                    )
        for attribute, code in (
            ("intake_path", "PIHL.TASK.INTAKE_PATH_DUPLICATE"),
            ("documentation_path", "PIHL.TASK.DOCUMENTATION_PATH_DUPLICATE"),
        ):
            seen: dict[str, str] = {}
            for task in tasks:
                path = getattr(task, attribute)
                if path is None:
                    continue
                if path in seen:
                    issues.append(
                        LocalIssue(code, path, f"{seen[path]},{task.task_id}")
                    )
                else:
                    seen[path] = task.task_id
        issues.extend(self._cycle_issues(by_id, relation="parent"))
        issues.extend(self._cycle_issues(by_id, relation="prerequisite"))
        issues.extend(self._cycle_issues(by_id, relation="supersession"))
        ordered = tuple(
            sorted(set(issues), key=lambda x: (x.code, x.path or "", x.detail))
        )
        return LocalValidationResult("FAIL" if ordered else "PASS", ordered)

    @staticmethod
    def _cycle_issues(
        by_id: dict[str, HarnessTask], *, relation: str
    ) -> list[LocalIssue]:
        code = {
            "parent": "PIHL.TASK.PARENT_CYCLE",
            "prerequisite": "PIHL.TASK.PREREQUISITE_CYCLE",
            "supersession": "PIHL.TASK.SUPERSESSION_CYCLE",
        }[relation]
        graph = {}
        for task_id, task in by_id.items():
            targets: tuple[str, ...]
            if relation == "parent":
                targets = (task.parent_task_id,) if task.parent_task_id in by_id else ()
            elif relation == "prerequisite":
                targets = tuple(x for x in task.task_prerequisite_ids if x in by_id)
            else:
                targets = tuple(x for x in task.superseded_by_task_ids if x in by_id)
            graph[task_id] = targets
        cycles: set[tuple[str, ...]] = set()
        completed: set[str] = set()
        for root in sorted(graph):
            if root in completed:
                continue
            path: list[str] = [root]
            positions = {root: 0}
            stack: list[tuple[str, int]] = [(root, 0)]
            while stack:
                node, child_index = stack[-1]
                children = graph[node]
                if child_index >= len(children):
                    completed.add(node)
                    stack.pop()
                    positions.pop(node)
                    path.pop()
                    continue
                child = children[child_index]
                stack[-1] = (node, child_index + 1)
                if child in positions:
                    cycle = path[positions[child] :]
                    rotations = [
                        tuple(cycle[index:] + cycle[:index])
                        for index in range(len(cycle))
                    ]
                    cycles.add(min(rotations))
                elif child not in completed:
                    positions[child] = len(path)
                    path.append(child)
                    stack.append((child, 0))
        return [LocalIssue(code, None, ",".join(cycle)) for cycle in sorted(cycles)]
