# C6-B20-W21 Slater--Koster definition and fit

This directory records the separately authorized no-calculator S110 attempt against the
full-support source selected by S105, where `H_T = H_W`.

## Mandatory alignment gate

The reduction specification requires a documented common state space before a Wannier
operator can be subtracted from an `sp3s*` Slater--Koster operator. S110 tested the
TB-anchored projection construction

\[
B(k)=[U_{\mathrm{dis}}(k)U(k)]^\dagger A(k)T^\dagger,
\]

where `A` is the authenticated 20-by-10 AMN projection matrix and `T` is the exact
unitary transformation from Wannier90's eight `sp3` hybrids plus two radial `s`
projections to the two-site atomic order
`(s, px, py, pz, s*)`. Löwdin orthonormalization requires all ten singular values of
`B(k)` to be resolved at every source point.

The conservative native-format singular-value uncertainty bound is
`5.890206739032098e-7`, derived from the 12-decimal AMN precision, 10-decimal `u` and
`u_dis` precision, matrix dimensions, and authenticated AMN scale.

The gate fails at two source points:

| Ordered index | Fractional coordinates | Resolved rank | Minimum singular value |
|---:|---|---:|---:|
| 0 | `(0, 0, 0)` | 9 | `5.362000386100462e-13` |
| 12 | `(0, 1/3, 0)` | 9 | `2.0186562353866025e-7` |

At Gamma, the unresolved right-singular direction has approximately 80.5% combined
`s*` weight and 19.5% combined `s` weight, shared nearly equally across the two sites.
Thus the proposed ten-orbital atomic frame is not fully represented inside the retained
rank-10 Wannier subspace at every construction point. A unitary common-space map and
its operator residual are not defined under the declared contract.

This is an orbital-subspace overlap failure, not an established consequence of energy
degeneracy. Unitary changes of basis inside a degenerate retained subspace leave the
singular values of `B(k)` unchanged. A symmetry-enforced absence or cancellation remains
possible, but the retained calculation contains no little-group representation analysis
that would establish it, and the second deficient point is not Gamma. The bounded
interpretation and proposed successor sequence are documented in
[`common-space-rank-deficiency-diagnosis-and-successor.md`](common-space-rank-deficiency-diagnosis-and-successor.md).

## S110-independent diagnosis producer

The calculation now includes a separate CSD0/CSD1 producer that does not import
`run_definition_fit.py`:

- `common-space-diagnosis-request.json` binds the exact S30, S105, S110, AMN, `u`,
  `u_dis`, complete provider-parser source closure, geometry, basis, unit, and
  energy-reference identities;
- [`../../common_space/diagnostics/`](../../common_space/diagnostics/) owns the
  calculation-incubated producer that authenticates those identities and reconstructs
  the full 216-point singular-value field, normalized principal-angle diagnostics,
  Gamma deficient-direction weights, and a retained-subspace unitary-invariance control;
  higher-precision sensitivity and symmetry-related deficient-point inventory extensions
  remain unimplemented;
- `run_common_space_diagnosis.py` provides human-readable live stdout that distinguishes
  successful diagnostic execution from the scientifically blocked fit disposition.

Run it only with a fresh output directory:

```bash
cd python
uv run python \
  ../calculations/Si/bulk/analysis/c6-b20-w21-slater-koster-definition-fit/\
run_common_space_diagnosis.py \
  --output-root /tmp/c6-b20-w21-common-space-diagnosis
```

The entrypoint requires a nonexistent output root, then creates `result.json`,
`human-readable-summary.txt`, and `manifest.json` without overwriting existing paths.
This producer does not share S110's calculation implementation; it is not the
separately implemented CSD1 verifier required by the successor protocol.
The implementation and its tests do not constitute a retained CSD execution, independent
verification, a CSD2 symmetry attribution, a CSD3 human disposition, or scientific
authorization for a fit or calculator run.

## Disposition

Status: `blocked-orbital-alignment-rank-deficient-no-fit`.

The provisional nearest- and second-neighbor orthogonal `sp3s*` parameter inventories
and the balanced 108/108 fit/validation split are retained, but they were not activated.
That split remains reserved exclusively for a future separately authorized
Slater--Koster study and is not part of hopping Pareto characterization. No least-squares
solve ran, no parameter vector exists, and no Slater--Koster model was accepted. A
spectral-only fit is not substituted for the failed operator alignment. S50 remains
blocked.

The default disposition is to retain no Slater--Koster reduction from this source and
stop this branch. The current
[hopping-first post-S110 protocol](../../research-protocol/controlled-reduction-protocol-hopping-first.tex)
preserves the earlier continuation options but requires the protocol-only HF0--HF4
[channel-specific Pareto synthesis](../c6-b20-w21-hopping-pareto-synthesis/) before any
future fit. Its original no-calculator identity/gap run is preserved, and one authorized
portable v2 rerun retained `UNRESOLVED_DEVELOPMENT_EVALUATION`; the required 408-point
per-shell intervals remain unavailable, and S105 full support is preserved.
Reusable Slater--Koster foundations, spectral-only feasibility, a global-unitary rank-10
operator study, a separately defined rank-9 source, and a new
projection/target-space/localization route remain scientifically distinct. The proposed
first step is a no-calculator projector- and symmetry-level diagnosis. For a rank-10
operator comparison, the preferred successor is a prospectively frozen global-unitary
study; if projection-anchored site-resolved atomic semantics are mandatory, a newly
qualified Wannier source is required instead. Level 1 has
since been implemented as a
[software-verification-only reusable foundation](level-1-foundation-disposition.md).
It did not close the hopping-first gates, alter this blocked result, or produce a fitted
reduction model. No later level is authorized, and a future spectral-only study would
not satisfy S110's aligned-operator contract.

No automatic retry, target-space change, mesh escalation, or calculator execution is
authorized.

## Artifacts

| Artifact | SHA-256 |
|---|---|
| implementation | `64459edf6f03161d30c6b6beec3361fa5ad7085417ab2a038d4f6c7c632925b3` |
| blocked result | `b9b8403dfc8b24df01e1671f582697440e1a211d60e0e70c9b0f621dfa086e98` |

No 408-point or 402-point parent values and no calculator were consumed.
