#!/usr/bin/env bash
set -euo pipefail
export MYPYPATH=python/src:.pi/task-ownership
export PYTHONPATH=.pi/task-ownership:python/src
.pi/task-ownership/validate_f0_initializer_acquisition_closure.sh
probe_source=$(cat <<'PY'
from __future__ import annotations

import hashlib
import sys
from pathlib import Path
from tempfile import TemporaryDirectory

from python_public_import_foundation_model import RuntimeSuccess
from public_import_foundation.input_snapshot import FoundationFormatError
from public_import_foundation.runtime_observation import PythonPackageRuntimeInspector


class RuntimeFileCompletenessProbe:
    """Exercise unreadable and non-file-backed runtime-module boundaries."""

    __slots__ = ()

    def execute(self) -> None:
        with TemporaryDirectory(prefix="runtime-file-completeness-") as temporary:
            repository = Path(temporary)
            source_root = repository / "python" / "src"
            broken_package = source_root / "broken_probe"
            broken_package.mkdir(parents=True)
            (broken_package / "__init__.py").write_text(
                "import sys\n"
                "import types\n"
                "broken = types.ModuleType('broken_probe.unreadable')\n"
                "broken.__file__ = '/deterministic/nonexistent/module.py'\n"
                "sys.modules[broken.__name__] = broken\n"
            )
            sentinel = repository / "candidate-output.json"
            sentinel.write_bytes(b"sentinel\n")
            inspector = PythonPackageRuntimeInspector(
                python_executable=Path(sys.executable).resolve(),
                repository_root=repository,
            )
            environment = inspector.environment()
            try:
                inspector.execute(
                    "broken_probe", environment.environment_sha256
                )
            except FoundationFormatError as exc:
                expected = (
                    "runtime package import failed for broken_probe: "
                    "unreadable loaded module file: broken_probe.unreadable"
                )
                if str(exc) != expected:
                    raise SystemExit(f"wrong unreadable-file diagnostic: {exc}") from exc
            else:
                raise SystemExit("unreadable string __file__ was silently omitted")
            if sentinel.read_bytes() != b"sentinel\n":
                raise SystemExit("runtime failure changed pre-existing output")

            safe_package = source_root / "safe_probe"
            safe_package.mkdir()
            (safe_package / "__init__.py").write_text(
                "import sys\n"
                "import types\n"
                "virtual = types.ModuleType('safe_probe.virtual')\n"
                "sys.modules[virtual.__name__] = virtual\n"
            )
            observation = inspector.execute(
                "safe_probe", environment.environment_sha256
            )
            if type(observation.observation) is not RuntimeSuccess:
                raise SystemExit("non-file-backed module changed success outcome")
            loaded = observation.observation.loaded_files
            keys = tuple((item.module_name, item.path) for item in loaded)
            if keys != tuple(sorted(set(keys))):
                raise SystemExit("loaded-file rows are not sorted and unique")
            if any(item.module_name == "safe_probe.virtual" for item in loaded):
                raise SystemExit("non-file-backed module entered the file view")
            for item in loaded:
                payload = Path(item.path).read_bytes()
                if len(payload) != item.byte_count or hashlib.sha256(
                    payload
                ).hexdigest() != item.sha256:
                    raise SystemExit(
                        f"loaded-file identity cannot be reproduced: {item.module_name}"
                    )
        print("runtime file completeness probes passed")


RuntimeFileCompletenessProbe().execute()
PY
)
python/.venv/bin/python -m mypy --strict -c "$probe_source"
python/.venv/bin/python -c "$probe_source"
