"""Project-local control identities and persistence paths."""

from __future__ import annotations

import re
from pathlib import Path

CONTROL_SCHEMA_VERSION = 3
CONTROL_DATABASE_PATH = Path("harness/state/harness-control.sqlite3")
CONTROL_SQL_PATH = Path("harness/state/harness-control.sql")
PROJECTION_MANIFEST_PATH = Path("harness/state/projection-manifest.json")
_GENERATOR_ID = "harness.control.projection-generator.v1"
_EVIDENCE_CLASSES = {
    "software_verification": "software-verification",
    "numerical_verification": "numerical-verification",
    "scientific_validation": "scientific-validation",
    "uncertainty_quantification": "uncertainty-quantification",
}
_IDENTIFIER = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*(?:\.[a-z0-9]+(?:-[a-z0-9]+)*)+$")
_EVIDENCE_ID = re.compile(r"(?m)^Evidence ID:\s*(\S+)\s*$")
