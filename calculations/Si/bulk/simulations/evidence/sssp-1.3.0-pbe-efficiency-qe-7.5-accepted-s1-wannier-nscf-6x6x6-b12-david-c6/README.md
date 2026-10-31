# Accepted-S1 `C6` 6x6x6 Davidson NSCF evidence

This directory retains compact evidence for the first construction-mesh successor NSCF.
The operator explicitly authorized exactly one local QE 7.5 `pw.x` invocation bound to
[`authorization-request.json`](input/authorization-request.json), SHA-256
`eefee784368f186246f13da0dd97591dd1f0ec1d09c564262f1a2f3699c41a28`.
The occurrence used 216 ordered Gamma-origin points, 12 bands, one process, a 600-second
timeout, a 512 MiB retention ceiling, and zero retries.

The invocation returned zero, printed `JOB DONE`, and completed in 28.04 seconds wall
time. The maintained extractor found 216 k-points, 12 bands, finite eigenvalues and
occupations, consistent terminal/count declarations, and no unconverged-eigenvalue
warning. The saved-state verifier authenticated 219 files totaling 58,433,245 bytes.
The external occurrence contains 240 files totaling 114,309,723 bytes, below the bound.
No retry occurred and the authorization is consumed.

QE reported `IEEE_INVALID_FLAG`, `IEEE_DIVIDE_BY_ZERO`, `IEEE_OVERFLOW_FLAG`, and
`IEEE_UNDERFLOW_FLAG` at process termination. Under the campaign policy these remain
diagnostics rather than blockers because native convergence succeeded, all parsed
values are finite, identities and invariants verify, and no corruption or explicit
unconverged-eigenvalue warning was found.

## Fixed-window inventory consequence

The NSCF eigenvalue range is `[-5.8341319732, 20.8036050385] eV`. With the unchanged
outer window `[-5.85, 19.02] eV`, the selected outer-space count is 10--12 per point:

- 142 points contain all 12 bands;
- 62 points contain 11 bands;
- 12 points contain exactly the rank-minimum 10 bands;
- 86 high-energy states across 74 points lie above the fixed outer maximum.

The unchanged frozen window `[-5.85, 8.00] eV` selects 4--6 states per point: 129 points
with four, 84 with five, and three with six. Thus the fixed windows remain dimensionally
eligible for rank 10, but the refined mesh no longer has all 12 parent bands inside the
outer window at every point. This is a consequence of changing the mesh while holding
the numerical window fixed; it must be retained in later attribution. Changing the
window would define a different scientific construction.

## Identities

| Artifact | SHA-256 |
|---|---|
| external inventory | `9321e56499ecb71b88f2d645c25e74431b1937576710077372b27b9e6713de81` |
| consumed authorization | `60871927128930c269f932da4444a8b397481f8168a66d0e4c2e6c2fd6bb2d0f` |
| exact `pw.in` | `dc5b913b0133b53968c1858dc984b408fcdc163b1fa654511f73c7098baa9bf3` |
| QEXSD | `865f8e749b2e2280a7ea093effc36b524f78f88ab9a9baf70e028ac7a8e42023` |
| saved-state manifest | `28df04c1bf314371d6138bfe41b564147354253c6d609b465c7ebd4778c617b8` |
| `nscf-result.json` | `890d853344b7f3cbb51d5b07fab538ad06f21ca6e589bed86d15dcf65654bd46` |
| window analysis | `5c52c505741c0d85c4643d872576cd04347786e885504b23df944275a07b3def` |
| campaign result | `191725ffca433ab7e983a8b825747f489fd94493ec68d8a2c9cb58fd3a697abd` |

The complete authenticated occurrence remains outside Git at
`/Users/eugene/projects/ksdft2effmass/si-accepted-s1-wannier-nscf-6x6x6-b12-david-c6-v1`.
[`external-artifact-inventory.json`](external-artifact-inventory.json) binds every
retained file.

## Scientific disposition

This is an eligible `C6` NSCF handoff, not a Wannier operator or an intended-use result.
Wannier90 preprocessing, `pw2wannier90.x`, localization, `C8`, `C12`, confirmation, and
all retries require separate authorization.
