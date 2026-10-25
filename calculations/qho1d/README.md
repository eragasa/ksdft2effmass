# QHO1D spatial-truncation calculation

This mutable calculation composes the canonical one-dimensional quantum harmonic
oscillator implementation in `ksdft2effmass.model_systems.qho1d`. It studies spatial
truncation: replacement of the real-line oscillator by a finite homogeneous-Dirichlet
box and centered finite-difference grid.

The `QHO1D` name is deliberately dimension-specific. No dimension-neutral `QHO`
implementation or 2D/3D extension is claimed.

## Status

This is a development calculation, not retained evidence, a publication manuscript, a
continuum-convergence proof, a physical uncertainty statement, or a scientific
validation result. The generated JSON beneath `analysis/development/` remains ignored
and replaceable. Report-local figure inputs and a compiled PDF snapshot are retained
for reproducible review, but they do not acquire evidentiary or validation status. The
historical retained package under
`calculations/research-monograph/harmonic-oscillator/` remains separate and preserves
its original provenance.

PIAB1D and QHO1D are consolidated under `calculations/` because both compose reusable
model-system and analysis code into concrete numerical studies. PIAB1D calibrates
spectral reduction; QHO1D exposes spatial-truncation, boundary, and discretization
channels.

## Files and output

- `input.json` declares the development sweep.
- `dev_analysis.py` calculates and independently verifies a candidate before writing
  the replaceable result.
- `dev_verification.py` independently verifies the existing development result.
- `dev_plots.py` verifies that result and writes replaceable report figures.
- `development_report/development_report.tex` is the LaTeX report focused on spatial
  truncation.
- `development_report/references.bib` owns the report-local bibliography.
- `development_report/README.md` records the retained figure identities and build chain.
- Report-local PNG inputs and `development_report.pdf` are retained review snapshots.
- Replaceable generated files are written under `analysis/development/` and ignored.

From `python/`:

```console
uv run python ../calculations/qho1d/dev_analysis.py
uv run python ../calculations/qho1d/dev_verification.py
uv run python ../calculations/qho1d/dev_plots.py
```

Compile the report from `calculations/qho1d/development_report/`:

```console
latexmk -pdf -interaction=nonstopmode -halt-on-error development_report.tex
```

Only the selected PDF is retained; LaTeX auxiliary files remain ignored.

## Comparison and diagnostic boundary

The current comparison forms

\[
J^{\mathsf T}H_{b,h}J-D_M,
\]

where `J` is the sampled-Hermite Gram-orthonormalized injection, `H_{b,h}` is the
finite Dirichlet-grid Hamiltonian, and `D_M` is the direct diagonal number-state
reference. The direct reference avoids the highest-state defect introduced by products
of already-truncated ladder matrices.

The reported discrepancy currently combines:

1. finite-box closure;
2. the two boundary-adjacent rows;
3. the interior centered-difference residual;
4. finite sampled-state Gram correction;
5. projection into retained coordinates; and
6. binary64 reconstruction and verification tolerance.

For an exactly isometric `J`,

\[
J^{\mathsf T}H_{b,h}J-D_M
=J^{\mathsf T}(H_{b,h}J-JD_M).
\]

This is a computable a-posteriori relation, not a continuum finite-box bound. The next
calculation should retain the boundary, interior, leakage, projector, and aligned
retained-operator channels separately rather than enlarge the undifferentiated sweep.
