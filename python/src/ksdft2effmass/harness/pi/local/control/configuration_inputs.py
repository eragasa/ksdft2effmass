"""Exact repository input resolution for the canonical HarnessConfiguration."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from ....configuration import (
    _HARNESS_CONFIGURATION_SOURCE_PATH,
    HarnessConfiguration,
    HarnessConfigurationResolver,
    HarnessConfigurationSourceJsonDeserializer,
)
from ..input_selection import _RepositoryInputSelector


@dataclass(frozen=True, slots=True)
class _HarnessConfigurationInputs:
    """One resolved value from the exact harness and Pi source payloads."""

    configuration: HarnessConfiguration


class _HarnessConfigurationInputResolver:
    """Resolve canonical repository configuration without consumer-specific work."""

    __slots__ = ()

    def execute(self, repository_root: Path) -> _HarnessConfigurationInputs:
        """Read and resolve only the two exact canonical configuration sources."""
        if not isinstance(repository_root, Path) or not repository_root.is_absolute():
            raise ValueError("repository_root must be an absolute pathlib.Path")
        root = repository_root.resolve(strict=True)
        if not root.is_dir():
            raise ValueError("repository_root must be an existing directory")
        selector = _RepositoryInputSelector()
        source_path = Path(_HARNESS_CONFIGURATION_SOURCE_PATH)
        source_payload = selector.file(
            root, source_path, subject="harness configuration"
        ).read_bytes()
        source = HarnessConfigurationSourceJsonDeserializer().execute(source_payload)
        pi_settings_path = Path(source.pi_settings_path)
        pi_settings_payload = selector.file(
            root, pi_settings_path, subject="Pi settings"
        ).read_bytes()
        resolution = HarnessConfigurationResolver().execute(
            _HARNESS_CONFIGURATION_SOURCE_PATH,
            source_payload,
            source.pi_settings_path,
            pi_settings_payload,
        )
        if resolution.status != "resolved" or resolution.configuration is None:
            codes = ", ".join(finding.code for finding in resolution.findings)
            raise ValueError(f"harness configuration resolution failed: {codes}")
        return _HarnessConfigurationInputs(resolution.configuration)
