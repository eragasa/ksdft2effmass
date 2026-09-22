"""Command-line boundary for one authorized Materials Project structure retrieval."""

from __future__ import annotations

import argparse
import os
from pathlib import Path
from typing import NoReturn

from mp_api.client import MPRester

from ksdft2effmass.integration.materials_project import (
    MaterialsProjectStructureJsonSerializer,
    MaterialsProjectStructureRequest,
    MaterialsProjectStructureRetriever,
)


class MaterialsProjectStructureCommand:
    """Own CLI parsing, credential ingress, retrieval, and exclusive output."""

    def execute(self, arguments: tuple[str, ...] | None = None) -> int:
        """Retrieve one MP structure and write one canonical metal-unit snapshot."""
        parser = argparse.ArgumentParser()
        parser.add_argument("material_id")
        parser.add_argument("output", type=Path)
        parser.add_argument("--conventional-unit-cell", action="store_true")
        namespace = parser.parse_args(arguments)
        api_key = os.environ.get("MP_API_KEY")
        if api_key is None or not api_key:
            self._fail("MP_API_KEY must be set; credentials are never written")
        request = MaterialsProjectStructureRequest(
            material_id=namespace.material_id,
            conventional_unit_cell=namespace.conventional_unit_cell,
        )
        with MPRester(api_key) as client:
            reference = MaterialsProjectStructureRetriever().execute(client, request)
        output: Path = namespace.output
        output.parent.mkdir(parents=True, exist_ok=True)
        with output.open("xb") as stream:
            stream.write(MaterialsProjectStructureJsonSerializer().execute(reference))
        return 0

    @staticmethod
    def _fail(message: str) -> NoReturn:
        raise ValueError(message)


def main() -> int:
    """Run the framework-owned command-line entry point."""
    return MaterialsProjectStructureCommand().execute()


if __name__ == "__main__":
    raise SystemExit(main())
