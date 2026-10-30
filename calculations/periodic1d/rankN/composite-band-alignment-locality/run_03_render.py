"""Refresh explicitly unverified development figure snapshots for report review."""

from __future__ import annotations

from pathlib import Path

from analysis.development import (
    HigherRankDevelopmentAdmittedCacheReader,
    HigherRankDevelopmentCacheReadRequest,
    HigherRankDevelopmentFigureDataProjector,
    HigherRankDevelopmentFigureProjectionRequest,
    HigherRankDevelopmentFigureRenderer,
    HigherRankDevelopmentFigureRenderRequest,
)


def main() -> int:
    """Render repeatedly from one integrity-admitted development cache."""
    calculation_root = Path(__file__).resolve().parent
    cache = HigherRankDevelopmentAdmittedCacheReader(
        HigherRankDevelopmentCacheReadRequest(
            cache_directory=calculation_root / "results" / "development-cache"
        )
    ).execute()
    data = HigherRankDevelopmentFigureDataProjector(
        HigherRankDevelopmentFigureProjectionRequest(cache.calculation_results)
    ).execute()
    output = calculation_root / "technical-report" / "development-figures"
    figures = HigherRankDevelopmentFigureRenderer(
        HigherRankDevelopmentFigureRenderRequest(
            data=data,
            output_directory=output,
        )
    ).execute()
    print(
        "lifecycle=replaceable-development-report-snapshots "
        "scientific_evidence=false cache_integrity_admitted=true "
        f"manifest_sha256={cache.manifest_sha256} "
        "calculation_infrastructure_sha256="
        f"{cache.manifest.calculation_infrastructure_sha256} "
        f"figure_count={len(figures)} output={output}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
