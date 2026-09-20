"""Isolated runtime observations for public-import foundation generation."""

from __future__ import annotations

import hashlib
import os
import subprocess
from dataclasses import dataclass
from pathlib import Path
from tempfile import TemporaryDirectory

from python_public_import_foundation_model import (
    FoundationJsonCodec,
    JsonRecord,
    JsonValue,
    RuntimeAttribute,
    RuntimeDistribution,
    RuntimeEnvironment,
    RuntimeFailure,
    RuntimeFailureKind,
    RuntimeLoadedFile,
    RuntimeObservation,
    RuntimeObservationView,
    RuntimeSuccess,
)

from public_import_foundation.input_snapshot import (
    FoundationFormatError,
    FoundationInputManifestSerializer,
)


@dataclass(frozen=True, slots=True)
class PythonPackageRuntimeInspector:
    """Observe package attributes in a bounded fresh interpreter."""

    python_executable: Path
    repository_root: Path

    def environment(self) -> RuntimeEnvironment:
        """Return the exact interpreter and installed-distribution identity."""
        script = (
            "import importlib.metadata,json,sys;"
            "rows=sorted((d.metadata.get('Name',''),d.version) for d in importlib.metadata.distributions());"
            "print(json.dumps({'implementation':sys.implementation.name,'version':sys.version,'distributions':rows},sort_keys=True,separators=(',',':')))"
        )
        completed = subprocess.run(
            (str(self.python_executable), "-I", "-B", "-c", script),
            cwd=self.repository_root,
            env=self._environment(),
            check=False,
            capture_output=True,
        )
        if completed.returncode != 0:
            raise FoundationFormatError("cannot identify selected runtime environment")
        decoded = FoundationJsonCodec().decode(completed.stdout)
        runtime = FoundationInputManifestSerializer.record(decoded, "runtime")
        distributions: list[RuntimeDistribution] = []
        for value in FoundationInputManifestSerializer.array(
            runtime.get("distributions"), "runtime.distributions"
        ):
            pair = FoundationInputManifestSerializer.array(value, "distribution")
            if len(pair) != 2:
                raise FoundationFormatError(
                    "runtime distribution must contain exactly two fields"
                )
            distributions.append(
                RuntimeDistribution(
                    FoundationInputManifestSerializer.text(
                        pair[0], "distribution.name"
                    ),
                    FoundationInputManifestSerializer.text(
                        pair[1], "distribution.version"
                    ),
                )
            )
        executable_payload = self.python_executable.resolve().read_bytes()
        implementation = FoundationInputManifestSerializer.text(
            runtime.get("implementation"), "runtime.implementation"
        )
        version = FoundationInputManifestSerializer.text(
            runtime.get("version"), "runtime.version"
        )
        identity_payload: JsonRecord = {
            "distributions": [[item.name, item.version] for item in distributions],
            "executable_byte_count": len(executable_payload),
            "executable_sha256": hashlib.sha256(executable_payload).hexdigest(),
            "implementation": implementation,
            "source_root": "python/src",
            "version": version,
        }
        environment_sha256 = hashlib.sha256(
            FoundationJsonCodec().encode(identity_payload)
        ).hexdigest()
        return RuntimeEnvironment(
            executable_byte_count=len(executable_payload),
            executable_sha256=hashlib.sha256(executable_payload).hexdigest(),
            implementation=implementation,
            version=version,
            distributions=tuple(distributions),
            source_root="python/src",
            environment_sha256=environment_sha256,
        )

    def execute(self, package: str, environment_identity: str) -> RuntimeObservation:
        """Return sorted attribute/type-origin facts for one imported package."""
        script = """
import hashlib
import importlib
import json
import pathlib
import sys
sys.path.insert(0, sys.argv[2])
try:
    module = importlib.import_module(sys.argv[1])
    attributes = [
        {
            "defining_module": getattr(value, "__module__", None),
            "name": name,
            "value_type": f"{type(value).__module__}.{type(value).__qualname__}",
        }
        for name, value in vars(module).items()
    ]
    result = {"status": "success", "attributes": sorted(attributes, key=lambda row: row["name"])}
except Exception as exc:
    result = {
        "status": "failure",
        "exception_type": type(exc).__name__,
        "failure_kind": "import_exception",
        "message": str(exc),
    }
loaded = []
for module_name, loaded_module in sorted(sys.modules.items()):
    raw_path = getattr(loaded_module, "__file__", None)
    if not isinstance(raw_path, str):
        continue
    path = pathlib.Path(raw_path)
    try:
        payload = path.read_bytes()
    except OSError:
        continue
    loaded.append({
        "byte_count": len(payload),
        "module_name": module_name,
        "path": str(path.resolve()),
        "sha256": hashlib.sha256(payload).hexdigest(),
    })
result["loaded_files"] = loaded
print(json.dumps(result, sort_keys=True, separators=(",", ":")))
"""
        with TemporaryDirectory(prefix="public-import-runtime-") as temporary:
            completed = subprocess.run(
                (
                    str(self.python_executable),
                    "-I",
                    "-B",
                    "-c",
                    script,
                    package,
                    str(self.repository_root / "python/src"),
                ),
                cwd=temporary,
                env=self._environment(),
                check=False,
                capture_output=True,
                text=False,
            )
        if completed.returncode != 0:
            message = completed.stderr.decode("utf-8", errors="replace").strip()
            raise FoundationFormatError(
                f"runtime package import failed for {package}: {message}"
            )
        decoded = FoundationJsonCodec().decode(completed.stdout)
        value = FoundationInputManifestSerializer.record(
            decoded, f"runtime observation for {package}"
        )
        status = FoundationInputManifestSerializer.text(
            value.get("status"), "runtime status"
        )
        loaded_files = tuple(
            self._loaded_file(item)
            for item in FoundationInputManifestSerializer.array(
                value.get("loaded_files"), "loaded_files"
            )
        )
        if status == "success":
            observation: RuntimeSuccess | RuntimeFailure = RuntimeSuccess(
                attributes=tuple(
                    self._attribute(item)
                    for item in FoundationInputManifestSerializer.array(
                        value.get("attributes"), "attributes"
                    )
                ),
                loaded_files=loaded_files,
            )
        elif status == "failure":
            observation = RuntimeFailure(
                failure_kind=RuntimeFailureKind(
                    FoundationInputManifestSerializer.text(
                        value.get("failure_kind"), "failure_kind"
                    )
                ),
                exception_type=FoundationInputManifestSerializer.text(
                    value.get("exception_type"), "exception_type"
                ),
                message=FoundationInputManifestSerializer.text(
                    value.get("message"), "message"
                ),
                loaded_files=loaded_files,
            )
        else:
            raise FoundationFormatError(
                f"runtime observation for {package} has an invalid result"
            )
        return RuntimeObservation(
            package=package,
            view=RuntimeObservationView.FRESH_INTERPRETER_PACKAGE_ATTRIBUTES,
            environment_sha256=environment_identity,
            observation=observation,
        )

    @staticmethod
    def _attribute(value: JsonValue) -> RuntimeAttribute:
        if type(value) is not dict:
            raise FoundationFormatError("runtime attribute must be an object")
        row: JsonRecord = value
        defining = row.get("defining_module")
        return RuntimeAttribute(
            name=FoundationInputManifestSerializer.text(row.get("name"), "name"),
            value_type=FoundationInputManifestSerializer.text(
                row.get("value_type"), "value_type"
            ),
            defining_module=(
                None
                if defining is None
                else FoundationInputManifestSerializer.text(defining, "defining_module")
            ),
        )

    @staticmethod
    def _loaded_file(value: JsonValue) -> RuntimeLoadedFile:
        if type(value) is not dict:
            raise FoundationFormatError("loaded file must be an object")
        row: JsonRecord = value
        return RuntimeLoadedFile(
            module_name=FoundationInputManifestSerializer.text(
                row.get("module_name"), "module_name"
            ),
            path=FoundationInputManifestSerializer.text(row.get("path"), "path"),
            byte_count=FoundationInputManifestSerializer.integer(
                row.get("byte_count"), "byte_count"
            ),
            sha256=FoundationInputManifestSerializer.text(row.get("sha256"), "sha256"),
        )

    @staticmethod
    def _environment() -> dict[str, str]:
        return {
            "LANG": "C",
            "LC_ALL": "C",
            "PATH": os.defpath,
            "PYTHONDONTWRITEBYTECODE": "1",
            "PYTHONHASHSEED": "0",
            "TZ": "UTC",
        }
