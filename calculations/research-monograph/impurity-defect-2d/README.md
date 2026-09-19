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
The defect-2D task remains active and selected. The original execution-free
Stage B implementation exposed a twist-gauge incompatibility and is retained as
negative design evidence. The human response ``recommendation authorized``
resolved `RM-IMPURITY-DEFECT-2D-STAGE-B-TWIST-GAUGE-HC04` by adopting the
multi-route, data-complete execution-free replacement. The two independent
matrix constructors, explicit bridge, fresh-process A-then-B and B-then-A
schedules, closed result schema, independent verifier, SVG plotter, and authored
toy tests are implemented. All sixteen software-verification tests pass. HC05
and HC06 produced retained pre-result failures. HC07 authorized one schema-
corrected attempt, which completed in 2.50 seconds and produced the calculated
synthetic `stage-b-result.json`. All 72 known-map route evaluations, 36 bridge
records, and 2,304 blind candidate rows are retained. The runner reports no
failed criterion; the independent Fourier/seam verifier reports reconstruction
and criteria PASS with maximum difference $7.845\times10^{-13}$. This exact
Stage B evidence is human-accepted through
`RM-IMPURITY-DEFECT-2D-STAGE-B-ACCEPTANCE-HC08`, which authorizes managed
closeout of this exact boundary only. No rerun is authorized. Stages C--E
remain undesigned at stage detail, unimplemented, and unauthorized; automatic
successor activation is false.

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
- `stage-b-design.json` — superseded single-route scalar-onsite design retained
  as historical negative evidence of the twist-gauge incompatibility.
- `stage-b-protocol.md` — mathematical conventions, identifiability boundary,
  covariance ownership, criteria, and independent-verification requirements.
- `stage-b-preflight.md` — design, behavioral-test, authority, and resource
  gates for any future implementation or execution request.
- `stage-b-adversarial-review.md` — evidence-backed adversarial findings and
  corrected design disposition.
- `run_stage_b.py` — adopted multi-route implementation with exact future
  execution authorization, independent constructors, fresh-process schedules,
  complete candidate retention, and an accepted-parent-free toy command.
- `verify_stage_b.py` — independent reconstruction that does not import the
  runner.
- `plot_stage_b.py` — deterministic retained-data-only SVG plotting.
- `stage-b-result.schema.json` — closed version-1 retained-result contract.
- `stage-b-native-evidence-manifest.json` — immutable execution-time manifest
  contract whose SHA-256 identity is bound by `stage-b-result.json` provenance.
- `stage-b-native-evidence-final-manifest.json` — finalized artifact identities,
  counts, retained failure history, acceptance, dense-matrix disposition, and
  calculated-evidence boundary.
- `stage-b-result.json` — calculated synthetic data-complete Stage B result.
- `stage-b-verification.log` — independent Fourier/seam reconstruction and
  criterion disposition.
- `stage-b-summary.svg` — deterministic retained-data-only summary plot.
- `stage-b-report.md` — bounded interpretation, reproduction, and limitations.
- `stage-b-implementation-blocker.md` — exact conflict between twist reduction,
  finite-matrix gauge, and bare-permutation covariance.
- `stage-b-multiroute-design.json` — adopted two-constructor, one-bridge,
  two-schedule execution-free design.
- `stage-b-multiroute-protocol.md` — uniform-link, seam, gauge-bridge, and route
  order equations and stopping rules.
- `stage-b-multiroute-preflight.md` — implemented inventories, measured toy
  envelope, behavioral gates, and the still-closed execution boundary.
- `stage-b-multiroute-adversarial-review.md` — adversarial design findings,
  including the clean and deliberately stateful route-order toy controls.
- `stage-b-implementation-review.md` — adversarial implementation findings,
  corrections, measured toy envelope, and bounded review outcome.
- `stage-b-execution-authorization.json` — consumed HC05 authorization for the
  failed first invocation.
- `stage-b-execution.log`, `stage-b-retry-execution.log`, and
  `stage-b-execution-failure.md` — retained pre-result invocation and parent-
  schema failures with bounded interpretations.
- `stage-b-retry-execution-authorization.json` — consumed HC06 retry
  authorization.
- `.pi/checkpoints/research-monograph-impurity-defect-2d-stage-b-execution.json`
  — pending exact accepted-parent execution decision; it is not authority while
  pending.
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
uv run python -m json.tool \
  ../calculations/research-monograph/impurity-defect-2d/stage-b-design.json \
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
uv run python \
  ../calculations/research-monograph/impurity-defect-2d/run_stage_b.py \
  --execution-free-toy-output /tmp/stage-b-toy.json
uv run python \
  ../calculations/research-monograph/impurity-defect-2d/verify_stage_b.py \
  --result /tmp/stage-b-toy.json --repository-root /tmp
uv run python \
  ../calculations/research-monograph/impurity-defect-2d/plot_stage_b.py \
  --result /tmp/stage-b-toy.json --output /tmp/stage-b-toy.svg
```

Verify identities from the design directory with
`shasum -a 256 -c SHA256SUMS`. Checksums establish file identity, while the
verifier establishes agreement under the frozen finite Stage A contract. Neither
establishes material validation, uncertainty quantification, or permission to
execute another stage.
