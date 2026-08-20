"""Private repository-level validation of project Pi agent descriptors."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from ..configuration import PiHarnessConfigurationDeserializer

_ALLOWED_FIELDS = frozenset(
    {
        "acceptanceRole",
        "clientAvatar",
        "clientName",
        "description",
        "inheritProjectContext",
        "inheritSkills",
        "name",
        "package",
        "skillPath",
        "skills",
        "systemPromptMode",
        "tools",
    }
)
_ALLOWED_TOOLS = frozenset({"bash", "edit", "read", "write"})
_REQUIRED_FIELDS = frozenset(
    {
        "acceptanceRole",
        "description",
        "inheritProjectContext",
        "inheritSkills",
        "name",
        "systemPromptMode",
        "tools",
    }
)


@dataclass(frozen=True, slots=True)
class _AgentDefinitionValidationFinding:
    """One deterministic project-agent descriptor finding."""

    code: str
    path: str
    message: str


@dataclass(frozen=True, slots=True)
class _AgentDefinitionValidationResult:
    """Closed structural result for one explicit project-agent inventory."""

    status: str
    descriptor_count: int
    enabled_count: int
    findings: tuple[_AgentDefinitionValidationFinding, ...]


class _PiHarnessAgentDefinitionSetValidator:
    """Validate one explicit repository agent root and its project settings."""

    __slots__ = ()

    @staticmethod
    def _confined(root: Path, path: Path, field: str) -> Path:
        if not isinstance(path, Path) or not path.is_absolute():
            raise ValueError(f"{field} must be an absolute pathlib.Path")
        if path.is_symlink():
            raise ValueError(f"{field} must not be a symlink")
        resolved = path.resolve(strict=True)
        if resolved != path:
            raise ValueError(f"{field} must be canonical")
        if resolved != root and root not in resolved.parents:
            raise ValueError(f"{field} must be beneath repository_root")
        return resolved

    @staticmethod
    def _frontmatter(payload: bytes) -> dict[str, str]:
        try:
            text = payload.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("descriptor must contain UTF-8") from exc
        if not text.startswith("---\n"):
            raise ValueError("descriptor must start with frontmatter")
        end = text.find("\n---\n", 4)
        if end < 0:
            raise ValueError("descriptor frontmatter must be closed")
        result: dict[str, str] = {}
        for line in text[4:end].splitlines():
            if not line or ":" not in line:
                raise ValueError("frontmatter lines must be nonempty key-value pairs")
            key, value = (part.strip() for part in line.split(":", 1))
            if not key or key in result:
                raise ValueError("frontmatter keys must be nonempty and unique")
            result[key] = value
        return result

    @staticmethod
    def _finding(
        code: str, path: str, message: str
    ) -> _AgentDefinitionValidationFinding:
        return _AgentDefinitionValidationFinding(code, path, message)

    def execute(
        self,
        repository_root: Path,
        agent_root: Path,
        settings_path: Path,
        skill_roots: tuple[Path, ...],
        allowed_external_override_names: tuple[str, ...] = (),
    ) -> _AgentDefinitionValidationResult:
        """Return complete structural findings without modifying repository state."""
        if not isinstance(repository_root, Path) or not repository_root.is_absolute():
            raise ValueError("repository_root must be an absolute pathlib.Path")
        if repository_root.is_symlink():
            raise ValueError("repository_root must not be a symlink")
        root = repository_root.resolve(strict=True)
        if root != repository_root:
            raise ValueError("repository_root must be canonical")
        agents = self._confined(root, agent_root, "agent_root")
        settings = self._confined(root, settings_path, "settings_path")
        if not agents.is_dir():
            raise ValueError("agent_root must be a directory")
        if not settings.is_file():
            raise ValueError("settings_path must be a regular file")
        if type(skill_roots) is not tuple or not skill_roots:
            raise ValueError("skill_roots must be a nonempty tuple")
        skills: set[str] = set()
        for index, skill_root in enumerate(skill_roots):
            selected = self._confined(root, skill_root, f"skill_roots[{index}]")
            if not selected.is_dir():
                raise ValueError("skill roots must be directories")
            for skill_directory in sorted(selected.iterdir()):
                if skill_directory.is_symlink():
                    raise ValueError(
                        "skill roots must not contain symlinked directories"
                    )
                if not skill_directory.is_dir():
                    continue
                entry = skill_directory / "SKILL.md"
                if entry.is_symlink():
                    raise ValueError("skill entries must not be symlinks")
                if entry.is_file():
                    skills.add(skill_directory.name)
        if type(allowed_external_override_names) is not tuple or any(
            type(name) is not str or not name
            for name in allowed_external_override_names
        ):
            raise TypeError("allowed_external_override_names must contain strings")

        findings: list[_AgentDefinitionValidationFinding] = []
        runtime_paths: dict[str, str] = {}
        enabled_count = 0
        descriptors = tuple(sorted(agents.glob("*.md")))
        configuration = PiHarnessConfigurationDeserializer().execute(
            settings.read_bytes()
        )
        disabled = set(configuration.disabled_agent_runtime_names)

        for descriptor in descriptors:
            relative = descriptor.relative_to(root).as_posix()
            if descriptor.is_symlink() or not descriptor.is_file():
                findings.append(
                    self._finding(
                        "AGENT.PATH_INVALID",
                        relative,
                        "descriptor must be a regular nonsymlink file",
                    )
                )
                continue
            try:
                fields = self._frontmatter(descriptor.read_bytes())
            except ValueError as exc:
                findings.append(
                    self._finding("AGENT.FRONTMATTER_INVALID", relative, str(exc))
                )
                continue
            unknown = tuple(sorted(set(fields) - _ALLOWED_FIELDS))
            missing = tuple(sorted(_REQUIRED_FIELDS - set(fields)))
            if unknown:
                findings.append(
                    self._finding(
                        "AGENT.FIELD_UNKNOWN",
                        relative,
                        "unknown frontmatter fields: " + ", ".join(unknown),
                    )
                )
            if missing:
                findings.append(
                    self._finding(
                        "AGENT.FIELD_MISSING",
                        relative,
                        "missing frontmatter fields: " + ", ".join(missing),
                    )
                )
                continue
            name = fields["name"]
            package = fields.get("package", "")
            runtime_name = f"{package}.{name}" if package else name
            if descriptor.stem != name:
                findings.append(
                    self._finding(
                        "AGENT.FILENAME_MISMATCH",
                        relative,
                        "descriptor filename must equal name plus .md",
                    )
                )
            prior = runtime_paths.get(runtime_name)
            if prior is not None:
                findings.append(
                    self._finding(
                        "AGENT.RUNTIME_DUPLICATE",
                        relative,
                        f"runtime name duplicates {prior}",
                    )
                )
            else:
                runtime_paths[runtime_name] = relative
            role = fields["acceptanceRole"]
            tools = tuple(
                item.strip() for item in fields["tools"].split(",") if item.strip()
            )
            unknown_tools = tuple(sorted(set(tools) - _ALLOWED_TOOLS))
            if len(tools) != len(set(tools)) or unknown_tools:
                findings.append(
                    self._finding(
                        "AGENT.TOOLS_INVALID",
                        relative,
                        "tools must be unique members of the supported vocabulary",
                    )
                )
            if role not in {"writer", "read-only"}:
                findings.append(
                    self._finding(
                        "AGENT.ROLE_INVALID", relative, "unsupported acceptanceRole"
                    )
                )
            elif role == "read-only" and set(tools) & {"edit", "write"}:
                findings.append(
                    self._finding(
                        "AGENT.ROLE_TOOL_MISMATCH",
                        relative,
                        "read-only agents must not expose edit or write",
                    )
                )
            elif role == "writer" and not {"edit", "write"}.issubset(tools):
                findings.append(
                    self._finding(
                        "AGENT.ROLE_TOOL_MISMATCH",
                        relative,
                        "writer agents must expose edit and write",
                    )
                )
            for field in ("inheritProjectContext", "inheritSkills"):
                if fields[field] not in {"true", "false"}:
                    findings.append(
                        self._finding(
                            "AGENT.BOOLEAN_INVALID",
                            relative,
                            f"{field} must be true or false",
                        )
                    )
            if fields["systemPromptMode"] not in {"append", "replace"}:
                findings.append(
                    self._finding(
                        "AGENT.PROMPT_MODE_INVALID",
                        relative,
                        "systemPromptMode must be append or replace",
                    )
                )
            selected_skills = tuple(
                item.strip()
                for item in fields.get("skills", "").split(",")
                if item.strip()
            )
            for skill in selected_skills:
                if skill not in skills:
                    findings.append(
                        self._finding(
                            "AGENT.SKILL_MISSING",
                            relative,
                            f"selected skill is unavailable: {skill}",
                        )
                    )
            if runtime_name not in disabled:
                enabled_count += 1

        allowed_overrides = set(runtime_paths) | set(allowed_external_override_names)
        for runtime_name in sorted(disabled - allowed_overrides):
            findings.append(
                self._finding(
                    "AGENT.OVERRIDE_STALE",
                    settings.relative_to(root).as_posix(),
                    f"disabled override has no project descriptor: {runtime_name}",
                )
            )
        ordered = tuple(
            sorted(set(findings), key=lambda item: (item.code, item.path, item.message))
        )
        return _AgentDefinitionValidationResult(
            "FAIL" if ordered else "PASS", len(descriptors), enabled_count, ordered
        )
