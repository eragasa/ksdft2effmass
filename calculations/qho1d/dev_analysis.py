"""Calculate and verify the replaceable QHO1D development result."""

from __future__ import annotations

from pathlib import Path
from tempfile import TemporaryDirectory

from ksdft2effmass.model_systems.qho1d import (
    Qho1dResultVerifier,
    Qho1dStudyEvaluator,
    Qho1dStudyInputDeserializer,
    Qho1dStudyResultSerializer,
)

CALCULATION_ROOT = Path(__file__).resolve().parent
REPOSITORY_ROOT = CALCULATION_ROOT.parents[1]
INPUT_PATH = CALCULATION_ROOT / "input.json"
OUTPUT_PATH = CALCULATION_ROOT / "analysis" / "development" / "qho1d-result.json"


def main() -> int:
    """Calculate, independently verify, and write one development result."""
    definition = Qho1dStudyInputDeserializer().execute(INPUT_PATH.read_bytes())
    result = Qho1dStudyEvaluator().execute(definition)
    payload = Qho1dStudyResultSerializer().execute(
        result=result,
        input_path=INPUT_PATH,
        script_path=Path(__file__),
        repository_root=REPOSITORY_ROOT,
    )
    with TemporaryDirectory(prefix="ksdft2effmass-qho1d-") as temporary:
        candidate = Path(temporary) / OUTPUT_PATH.name
        candidate.write_bytes(payload)
        Qho1dResultVerifier().execute(candidate, REPOSITORY_ROOT)
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_bytes(payload)
    print(
        "calculation=qho1d lifecycle=development verification=pass "
        f"output={OUTPUT_PATH}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
