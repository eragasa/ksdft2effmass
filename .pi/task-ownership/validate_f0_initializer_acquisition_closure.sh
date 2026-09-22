#!/usr/bin/env bash
set -euo pipefail
export MYPYPATH=python/src:.pi/task-ownership
export PYTHONPATH=.pi/task-ownership:python/src
.pi/task-ownership/validate_f0_typed_domain_construction.sh
probe_source=$(cat <<'PY'
from __future__ import annotations

from public_import_foundation.input_snapshot import FoundationFormatError
from public_import_foundation.source_observation import PythonInitializerInspector


class InitializerAcquisitionProbe:
    """Exercise every accepted C3 initializer counterexample independently."""

    __slots__ = ()

    def execute(self) -> None:
        inspector = PythonInitializerInspector()
        declares, names, bindings = inspector.execute(
            "ksdft2effmass.probe",
            "probe/__init__.py",
            b"from ksdft2effmass.analysis import DftReferenceCalculationIdentity\n__all__ = ['DftReferenceCalculationIdentity']\n",
        )
        if (
            not declares
            or names != ("DftReferenceCalculationIdentity",)
            or tuple(item.local_name for item in bindings)
            != ("DftReferenceCalculationIdentity",)
        ):
            raise SystemExit("valid literal __all__ acquisition changed")
        cases: tuple[tuple[str, bytes, str], ...] = (
            (
                "globals subscript assignment",
                b"globals()['__all__'] = ['A']\n",
                "indirect __all__ access",
            ),
            (
                "vars subscript deletion",
                b"del vars()['__all__']\n",
                "indirect __all__ access",
            ),
            (
                "alias mutation",
                b"__all__ = ['A']\nalias = __all__\nalias.append('B')\n",
                "aliased __all__ access",
            ),
            (
                "direct mutation",
                b"__all__ = ['A']\n__all__.append('B')\n",
                "unrepresented __all__ mutation",
            ),
            (
                "conditional assignment",
                b"if flag:\n    __all__ = ['A']\n",
                "unrepresented __all__ assignment",
            ),
            (
                "globals namespace alias",
                b"ns = globals()\nns['__all__'] = ['A']\n",
                "namespace alias can mutate __all__",
            ),
            (
                "vars namespace alias",
                b"ns = vars()\nns['__all__'] = ['A']\n",
                "namespace alias can mutate __all__",
            ),
            (
                "namespace update",
                b"globals().update(__all__=['A'])\n",
                "namespace call can mutate __all__",
            ),
            (
                "namespace setitem",
                b"globals().__setitem__('__all__', ['A'])\n",
                "namespace call can mutate __all__",
            ),
            (
                "call argument escape",
                b"__all__ = ['A']\nmutate(__all__)\n",
                "unrepresented __all__ load or escape",
            ),
            (
                "named-expression escape",
                b"__all__ = ['A']\n(alias := __all__).append('B')\n",
                "unrepresented __all__ load or escape",
            ),
        )
        for label, source, expected in cases:
            try:
                inspector.execute(
                    "ksdft2effmass.probe", "probe/__init__.py", source
                )
            except FoundationFormatError as exc:
                if expected not in str(exc):
                    raise SystemExit(
                        f"{label} produced the wrong diagnostic: {exc}"
                    ) from exc
            else:
                raise SystemExit(f"initializer inspector accepted: {label}")
        print(f"initializer acquisition probes passed: {len(cases)} rejected")


InitializerAcquisitionProbe().execute()
PY
)
python/.venv/bin/python -m mypy --strict -c "$probe_source"
python/.venv/bin/python -c "$probe_source"
