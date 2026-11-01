"""Admit canonical development-cache bytes without claiming scientific verification."""

from __future__ import annotations

from pathlib import Path

from analysis.development.cache import (
    HigherRankDevelopmentCacheIntegrityVerifier,
    HigherRankDevelopmentCacheReadRequest,
)


def main() -> int:
    """Verify cache byte integrity and complete case inventory exactly once."""
    cache_directory = Path(__file__).resolve().parent / "results" / "development-cache"
    admission = HigherRankDevelopmentCacheIntegrityVerifier(
        HigherRankDevelopmentCacheReadRequest(cache_directory=cache_directory)
    ).execute()
    print(
        "lifecycle=replaceable-development-cache-integrity-admission "
        "scientific_evidence=false independent_scientific_verification=false "
        f"manifest_sha256={admission.manifest_sha256}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
