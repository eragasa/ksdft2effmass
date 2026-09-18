# Controlled two-dimensional defect-extraction design

This directory contains the version-1 design and completed Stage A evidence for
the active defect-2D monograph exercise. It extends the accepted one-dimensional
impurity contracts only where the geometry is genuinely two-dimensional:
boundary seams, $D_4$/$D_2$ covariance, directional defects, independent area
and shape sequences, anisotropy, and degenerate-projector alignment.

**Status:** the version-1 design and the exact bounded Stage A null-and-folding
evidence are human-accepted. Checkpoint
`RM-IMPURITY-DEFECT-2D-STAGE-A-ACCEPTANCE-HC02` authorizes managed closeout of
that exact boundary. All numerical criteria and independent reconstruction pass.
The defect-2D task remains active and selected, but Stages B--E remain
unimplemented and unauthorized; automatic successor activation is false.

The proposed evidence class is controlled synthetic software and numerical
verification. The package does not perform or claim DFT, production Wannier90,
material transfer, silicon or dopant validation, spin-space revalidation,
uncertainty quantification, or publication readiness.

## Contents

- `study-design.json` — exact parents, stages, plants, maps, metrics,
  tolerances, adverse controls, structured stops, authorization boundary, and
  planning envelope.
- `protocol.md` — represented spaces, equations, stage semantics, acceptance
  rules, and independent-verification contract.
- `preflight.md` — authorization boundary, resource estimate, and staged gates.
- `run_stage_a.py` — fail-closed Stage A runner; invocation requires a separate
  exact execution-authorization record.
- `verify_stage_a.py` — independent Kronecker-seam reconstruction that does not
  import the runner.
- `adversarial-review.md` — attack-oriented design assessment and finding
  dispositions.
- `stage-a-implementation-review.md` — first-pass findings, remediation, and
  execution-readiness re-review.
- `stage-a-execution-authorization.json` — exact checkpoint, artifact, output,
  repository, and resource binding for the completed one-run authority.
- `stage-a-result.json` — calculated synthetic Stage A metrics, seam controls,
  stops, criteria, and provenance.
- `stage-a-execution.log` — bounded local process resource measurement.
- `stage-a-verification.log` — independent reconstruction and criterion
  disposition.
- `stage-a-report.md` — result interpretation, reproduction, and limitations.
- `SHA256SUMS` — identities of the design, implementation, authority, result,
  verification, report, and retained test contract.

The runner constructed all eight frozen cases once and refused overwrite. The
independent verifier used the separate Kronecker route and reported
`reconstruction=PASS`, `criteria=PASS`, with maximum reconstructed metric
difference $3.473\times10^{-16}$. This result is bounded synthetic numerical
verification, not material validation or authority for another stage.

## Verifying the retained evidence

From `python/`:

```bash
uv run python -m json.tool \
  ../calculations/research-monograph/impurity-defect-2d/study-design.json \
  >/dev/null
uv run ruff check \
  ../calculations/research-monograph/impurity-defect-2d/run_stage_a.py \
  ../calculations/research-monograph/impurity-defect-2d/verify_stage_a.py
uv run mypy --strict \
  ../calculations/research-monograph/impurity-defect-2d/run_stage_a.py \
  ../calculations/research-monograph/impurity-defect-2d/verify_stage_a.py
uv run python \
  ../calculations/research-monograph/impurity-defect-2d/verify_stage_a.py \
  --result \
  ../calculations/research-monograph/impurity-defect-2d/stage-a-result.json \
  --repository-root /Users/eugene/repos/ksdft2effmass
```

Verify identities from the design directory with
`shasum -a 256 -c SHA256SUMS`. Checksums establish file identity, while the
verifier establishes agreement under the frozen finite Stage A contract. Neither
establishes material validation, uncertainty quantification, or permission to
execute another stage.
