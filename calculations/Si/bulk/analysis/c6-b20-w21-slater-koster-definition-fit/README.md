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

## Disposition

Status: `blocked-orbital-alignment-rank-deficient-no-fit`.

The provisional nearest- and second-neighbor orthogonal `sp3s*` parameter inventories
and the balanced 108/108 fit/validation split are retained, but they were not activated.
No least-squares solve ran, no parameter vector exists, and no Slater--Koster model was
accepted. A spectral-only fit is not substituted for the failed operator alignment.
S50 prediction freeze remains blocked.

The default disposition is to retain no Slater--Koster reduction from this source and
stop this branch. The current
[post-S110 protocol](../../research-protocol/controlled-reduction-protocol-post-s110.tex)
orders separately authorized continuations by increasing implementation difficulty:
reusable Slater--Koster foundations, spectral-only feasibility, a global-unitary
rank-10 operator study, a separately defined rank-9 source, and a new
projection/target-space/localization route. None is an automatic retry, and the
spectral-only study does not satisfy S110's aligned-operator contract.

No automatic retry, target-space change, mesh escalation, or calculator execution is
authorized.

## Artifacts

| Artifact | SHA-256 |
|---|---|
| implementation | `64459edf6f03161d30c6b6beec3361fa5ad7085417ab2a038d4f6c7c632925b3` |
| blocked result | `b9b8403dfc8b24df01e1671f582697440e1a211d60e0e70c9b0f621dfa086e98` |

No 408-point or 402-point parent values and no calculator were consumed.
