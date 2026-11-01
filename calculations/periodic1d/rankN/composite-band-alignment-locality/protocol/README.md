# Planned higher-rank one-dimensional study

This directory contains the detailed plan for a synthetic one-dimensional calculation
that has not been run as retained evidence. The calculation asks how increasing the
number of retained states and the depth of momentum-dependent basis rotations changes
the range of the resulting real-space hopping matrices.

The protocol's short labels mean:

- **D1:** one spatial dimension;
- **P0:** the retained subspace is fixed rather than moving with momentum; and
- **G0:** the basis rotations are real orthogonal rotations.

The direct typed producer now enters through the rank-$N$ rank-first alignment-study
specification and binds the explicit reduced-convention geometry
$a_0=1\,\mathrm{bohr}$. Development-cache format v2 retains that geometry independently
of the unchanged case-result wires. Canonical calculation caching, integrity verification,
and the fixed nine-view renderer are implemented. A publication-oriented six-figure
storyboard now selects a compact narrative from the same admitted cache without changing
the scientific producer or replacing the detailed nine-view diagnostic inventory. The
figures remain calculated, integrity-admitted, unsealed results pending independent
scientific acceptance, but presentation changes can be rendered repeatedly without
recalculation.

| File | SHA-256 |
|---|---|
| [`experimental-protocol.tex`](experimental-protocol.tex) | `2c1a5e7e2ee476ff27151f3ed6d9c02abc25ca7a577b30a40a4ce45199231a8e` |

The TeX file originated from
`experiments/periodic-reduction/higher-rank-composite-band-alignment-and-locality/experimental-protocol.tex`
at predecessor revision `81f7c09a5edc50be698bd3a5f047438cd61d4eca`. The maintained
calculation-owned protocol now uses descriptive gauge-alignment identities and includes
scientific-flow and typed-lifecycle schematics; it is no longer byte-identical to that
historical donor. Its current SHA-256 is
`2c1a5e7e2ee476ff27151f3ed6d9c02abc25ca7a577b30a40a4ce45199231a8e`.

The plan specifies the one-dimensional cases, numerical controls, resource limits, and
scientific interpretation. Storyboard rationale, evidence boundaries, encoding rules,
and intended placement are recorded in
[`publication-figure-storyboard.md`](publication-figure-storyboard.md). Regenerate the
vector PDFs and 600-dpi PNG review files from `python/` with:

```console
uv run python \
  ../calculations/periodic1d/rankN/composite-band-alignment-locality/protocol/render_publication_storyboard.py
```

The renderer reads only the integrity-admitted `results/development-cache/` inventory and
writes the closed figure set under `figures/storyboard/`. Its references to
`verify_d1_p0_g0_controls.py` name the old
finite-grid formula-check script; the maintained replacement is
[`../verify_analytic_controls.py`](../verify_analytic_controls.py). The direct lifecycle
uses `run_01_calculation.py`, `run_02_verification.py`, and `run_03_render.py`. The cache
manifest records exact result-byte identities and the single
`calculation_infrastructure_sha256` provenance value. Cache integrity is not scientific
validation.

Build only in scratch so tracked review inputs are not overwritten:

```console
build_dir="$(mktemp -d /tmp/ksd-higher-rank-protocol.XXXXXX)"
latexmk -pdf -interaction=nonstopmode -halt-on-error \
  -outdir="${build_dir}" experimental-protocol.tex
```

A successful build establishes document buildability only. It does not create an
immutable version, authorize execution, or establish numerical or scientific validation.
