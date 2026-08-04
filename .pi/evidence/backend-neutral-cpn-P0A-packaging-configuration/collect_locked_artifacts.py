"""Collect the bounded P0A package identities from the repository uv lock."""

from __future__ import annotations

import argparse
import hashlib
import json
import tomllib
from pathlib import Path

SELECTED_PACKAGES = ("snakes", "myst-parser", "sphinx")
SNAKES_SDIST_HASH = (
    "sha256:af8c3046bfedf3e088b6bf37d451ad6aeeb79716f68a6253e44ddbd1c7e250f3"
)
MYST_WHEEL_HASH = (
    "sha256:9c91c52b3cdb4d94a6506e4fab4e2f296c7623a0da0dcbe6de1565c3dad67a8a"
)


def main() -> int:
    """Write deterministic selected-package and lock-hash evidence."""

    parser = argparse.ArgumentParser()
    parser.add_argument("--lock", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    lock_bytes = args.lock.read_bytes()
    lock = tomllib.loads(lock_bytes.decode("utf-8"))
    packages = {package["name"]: package for package in lock["package"]}

    selected = {}
    for name in SELECTED_PACKAGES:
        package = packages[name]
        selected[name] = {
            "version": package["version"],
            "source": package["source"],
            "sdist": package.get("sdist"),
            "wheels": package.get("wheels", []),
        }

    result = {
        "schema_version": 1,
        "task_id": "backend-neutral-cpn-P0A-packaging-configuration",
        "lock": {
            "path": "python/uv.lock",
            "sha256": hashlib.sha256(lock_bytes).hexdigest(),
            "format_version": lock["version"],
            "revision": lock["revision"],
            "requires_python": lock["requires-python"],
        },
        "selected_packages": selected,
        "p0_identity_matches": {
            "snakes_0_9_33_sdist_sha256": (
                selected["snakes"]["sdist"]["hash"] == SNAKES_SDIST_HASH
            ),
            "myst_parser_5_1_0_universal_wheel_sha256": any(
                wheel["hash"] == MYST_WHEEL_HASH
                for wheel in selected["myst-parser"]["wheels"]
            ),
        },
    }
    if not all(result["p0_identity_matches"].values()):
        raise SystemExit("locked artifacts do not match accepted P0 identities")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(f"wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
