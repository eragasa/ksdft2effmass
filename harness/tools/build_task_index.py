#!/usr/bin/env python3
# ruff: noqa: E501
"""Rebuild the disposable bootstrap Task SQLite index from explicit JSON inputs."""

from __future__ import annotations

import argparse
import json
import sqlite3
from pathlib import Path
from typing import Any


def load_object(path: Path) -> dict[str, Any]:
    """Read one explicitly selected JSON object."""
    value = json.loads(path.read_text(encoding="utf-8"))
    if type(value) is not dict:
        raise TypeError(f"{path} must contain a JSON object")
    return value


def cycle_count(edges: list[tuple[str, str, str]]) -> int:
    """Count strongly connected components containing a directed cycle."""
    graph: dict[str, list[str]] = {}
    for source, target, _kind in edges:
        graph.setdefault(source, []).append(target)
        graph.setdefault(target, [])
    index = 0
    indices: dict[str, int] = {}
    low: dict[str, int] = {}
    stack: list[str] = []
    on_stack: set[str] = set()
    count = 0

    def visit(node: str) -> None:
        nonlocal index, count
        indices[node] = low[node] = index
        index += 1
        stack.append(node)
        on_stack.add(node)
        for target in graph[node]:
            if target not in indices:
                visit(target)
                low[node] = min(low[node], low[target])
            elif target in on_stack:
                low[node] = min(low[node], indices[target])
        if low[node] == indices[node]:
            component = []
            while True:
                member = stack.pop()
                on_stack.remove(member)
                component.append(member)
                if member == node:
                    break
            if len(component) > 1 or any(
                source == target == component[0] for source, target, _ in edges
            ):
                count += 1

    for node in sorted(graph):
        if node not in indices:
            visit(node)
    return count


def write_report(connection: sqlite3.Connection, path: Path) -> None:
    """Write deterministic direct-SQL structural observations."""
    def scalar(sql: str) -> int:
        row = connection.execute(sql).fetchone()
        if row is None:
            raise ValueError("scalar SQL query returned no row")
        return int(row[0])
    statuses = connection.execute(
        "SELECT status, COUNT(*) FROM tasks GROUP BY status ORDER BY status"
    ).fetchall()
    repeated_titles = connection.execute(
        "SELECT title, COUNT(*) FROM tasks GROUP BY title HAVING COUNT(*) > 1 "
        "ORDER BY title"
    ).fetchall()
    repeated_objectives = connection.execute(
        "SELECT objective, COUNT(*) FROM tasks GROUP BY objective HAVING COUNT(*) > 1 "
        "ORDER BY objective"
    ).fetchall()
    edges = connection.execute(
        "SELECT source, target, kind FROM task_edges ORDER BY kind, source, target"
    ).fetchall()
    missing_prerequisites = scalar(
        "SELECT COUNT(*) FROM task_edges e WHERE e.kind='prerequisite' "
        "AND (NOT EXISTS (SELECT 1 FROM tasks t WHERE t.task_id=e.source) "
        "OR NOT EXISTS (SELECT 1 FROM tasks t WHERE t.task_id=e.target))"
    )
    lines = [
        "# Task bootstrap rationalization",
        "",
        "This report contains structural observations from direct SQL queries over the disposable derived index. Intake artifacts are non-executable and cannot independently activate work.",
        "",
        f"- Total Tasks: {scalar('SELECT COUNT(*) FROM tasks')}",
        "- Status counts: "
        + ", ".join(f"`{status}` = {count}" for status, count in statuses),
        f"- Root Tasks: {scalar('SELECT COUNT(*) FROM tasks WHERE parent_task_id IS NULL')}",
        f"- Orphan Tasks: {scalar('SELECT COUNT(*) FROM tasks t WHERE parent_task_id IS NOT NULL AND NOT EXISTS (SELECT 1 FROM tasks p WHERE p.task_id=t.parent_task_id)')}",
        f"- Missing parents: {scalar('SELECT COUNT(*) FROM tasks t WHERE parent_task_id IS NOT NULL AND NOT EXISTS (SELECT 1 FROM tasks p WHERE p.task_id=t.parent_task_id)')}",
        f"- Missing prerequisites: {missing_prerequisites}",
        f"- Self-edges: {scalar('SELECT COUNT(*) FROM task_edges WHERE source=target')}",
        f"- Duplicate edges: {scalar('SELECT COUNT(*) FROM (SELECT source,target,kind,COUNT(*) n FROM task_edges GROUP BY source,target,kind HAVING n>1)')}",
        f"- Directed cycle components: {cycle_count(edges)}",
        f"- Tasks with no graph relationships: {scalar('SELECT COUNT(*) FROM tasks t WHERE NOT EXISTS (SELECT 1 FROM task_edges e WHERE e.source=t.task_id OR e.target=t.task_id)')}",
        f"- Tasks with migration issues: {scalar('SELECT COUNT(DISTINCT task_id) FROM migration_issues')}",
        f"- Archived-source coverage: {scalar('SELECT COUNT(*) FROM archived_sources')} of {scalar('SELECT COUNT(*) FROM tasks')}",
        f"- Intake coverage: {scalar('SELECT COUNT(*) FROM tasks WHERE intake_path IS NOT NULL')} of {scalar('SELECT COUNT(*) FROM tasks')}",
        f"- Repeated exact titles: {len(repeated_titles)} groups",
        f"- Repeated exact objective text: {len(repeated_objectives)} groups",
    ]
    if repeated_titles:
        lines.extend(["", "## Repeated exact titles", ""])
        lines.extend(f"- {count} × {title}" for title, count in repeated_titles)
    if repeated_objectives:
        lines.extend(["", "## Repeated exact objective text", ""])
        lines.extend(
            f"- {count} occurrences: `{objective}`"
            for objective, count in repeated_objectives
        )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repository-root", type=Path, required=True)
    parser.add_argument("--task-directory", type=Path, required=True)
    parser.add_argument("--graph-path", type=Path, required=True)
    parser.add_argument("--issue-path", type=Path, required=True)
    parser.add_argument("--output-database", type=Path, required=True)
    parser.add_argument("--report-path", type=Path, required=True)
    args = parser.parse_args()
    root = args.repository_root.resolve()
    task_directory = (root / args.task_directory).resolve()
    graph = load_object((root / args.graph_path).resolve())
    issue_document = load_object((root / args.issue_path).resolve())
    task_paths = sorted(task_directory.glob("*.json"), key=lambda path: path.name)
    tasks = [(path, load_object(path)) for path in task_paths]
    output = (root / args.output_database).resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.unlink(missing_ok=True)
    connection = sqlite3.connect(output)
    try:
        connection.executescript(
            """
            PRAGMA foreign_keys = ON;
            CREATE TABLE tasks (
                task_id TEXT PRIMARY KEY, json_path TEXT NOT NULL UNIQUE,
                title TEXT NOT NULL, status TEXT NOT NULL, status_detail TEXT,
                parent_task_id TEXT, explicit_activation_required INTEGER NOT NULL,
                objective TEXT NOT NULL, intake_path TEXT
            ) WITHOUT ROWID;
            CREATE TABLE task_edges (
                source TEXT NOT NULL, target TEXT NOT NULL, kind TEXT NOT NULL,
                PRIMARY KEY (source, target, kind)
            ) WITHOUT ROWID;
            CREATE TABLE archived_sources (
                task_id TEXT PRIMARY KEY, path TEXT NOT NULL UNIQUE, sha256 TEXT NOT NULL
            ) WITHOUT ROWID;
            CREATE TABLE migration_issues (
                issue_index INTEGER PRIMARY KEY, task_id TEXT NOT NULL, field TEXT NOT NULL,
                source_paths_json TEXT NOT NULL, issue TEXT NOT NULL,
                candidate_value_json TEXT NOT NULL
            );
            """
        )
        for path, task in tasks:
            connection.execute(
                "INSERT INTO tasks VALUES (?,?,?,?,?,?,?,?,?)",
                (
                    task["task_id"],
                    path.relative_to(root).as_posix(),
                    task["title"],
                    task["status"],
                    task.get("status_detail"),
                    task.get("parent_task_id"),
                    int(task["explicit_activation_required"]),
                    task["objective"],
                    task.get("intake_path"),
                ),
            )
            archived = task.get("archived_source")
            if archived is not None:
                connection.execute(
                    "INSERT INTO archived_sources VALUES (?,?,?)",
                    (task["task_id"], archived["path"], archived["sha256"]),
                )
        for edge in graph["edges"]:
            connection.execute(
                "INSERT INTO task_edges VALUES (?,?,?)",
                (edge["source"], edge["target"], edge["kind"]),
            )
        for index, issue in enumerate(issue_document["issues"]):
            connection.execute(
                "INSERT INTO migration_issues VALUES (?,?,?,?,?,?)",
                (
                    index,
                    issue["task_id"],
                    issue["field"],
                    json.dumps(issue["source_paths"], separators=(",", ":")),
                    issue["issue"],
                    json.dumps(issue["candidate_value"], separators=(",", ":")),
                ),
            )
        connection.commit()
        write_report(connection, (root / args.report_path).resolve())
    finally:
        connection.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
