"""Import boundary for the calculation-local Vogl control package."""

from __future__ import annotations

import sys
from pathlib import Path

CONTROL_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CONTROL_ROOT))
