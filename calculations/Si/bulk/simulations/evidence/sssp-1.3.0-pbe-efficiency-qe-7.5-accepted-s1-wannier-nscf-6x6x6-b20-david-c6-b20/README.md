# Accepted-S1 `C6-B20` 6x6x6 Davidson NSCF evidence

This directory retains compact evidence for the authorized broader-parent NSCF. The
operator explicitly authorized exactly one local QE 7.5 `pw.x -in pw.in` invocation
bound to [`authorization-request.json`](input/authorization-request.json), SHA-256
`33a36570545ef5e7e5ffcc3a5d7b3aea5ca461359f4f80c24491e2811562633e`. The occurrence
used 216 ordered Gamma-origin points, 20 bands, one process, a 600-second timeout, a
512 MiB retention ceiling, and zero retries. Relative to the accepted 12-band `C6`
NSCF, the exact input changed only `nbnd = 12` to `nbnd = 20`.

The invocation returned zero, printed `JOB DONE`, and completed in 42.31 seconds wall
time. The maintained extractor and KSD QEXSD parser found 216 k-points, 20 bands,
finite eigenvalues and occupations, consistent terminal/count declarations, and no
unconverged-eigenvalue warning. The ProjectKoios saved-state verifier authenticated 219
files totaling 93,658,989 bytes. The retained occurrence remained below the 512 MiB
bound. No retry occurred and the authorization is consumed.

QE reported `IEEE_INVALID_FLAG`, `IEEE_DIVIDE_BY_ZERO`, `IEEE_OVERFLOW_FLAG`, and
`IEEE_UNDERFLOW_FLAG` at process termination. Under the campaign policy these remain
diagnostics rather than blockers because native convergence succeeded, all parsed
values are finite, identities and invariants verify, and no corruption or explicit
unconverged-eigenvalue warning was found.

## Authenticated spectral inventory

The 20-band eigenvalue range is `[-5.8341319732, 30.2720123939] eV`. The ordered
k-points and weights match the earlier 12-band `C6` occurrence exactly. Its first 12
eigenvalues are reproduced within `4.14e-11 eV`, so the enlarged inventory preserves
the previously characterized low-band spectrum to that observed numerical difference.

Under the inherited outer window `[-5.85, 19.02] eV`, the 20-band inventory selects
10--14 states per point:

- 12 points contain 10 states;
- 62 points contain 11 states;
- 96 points contain 12 states;
- 24 points contain 13 states; and
- 22 points contain 14 states.

Bands 13 and 14 contribute 68 states in total under this window, at 46 and 22 points,
respectively. This resolves an omission that a 12-band inventory could not observe.
The minimum remains the prospective rank 10 at every point.

Under the previously prepared `C6-T1` window `[-6.0, 21.0] eV`, the enlarged inventory
selects 12 states at 48 points, 13 at 108 points, and 14 at 60 points. Bands 13 and 14
contribute 228 states in total. Band 15 has a minimum of `21.2571673143 eV`; therefore
no band 15--20 state enters either investigated window. This establishes inventory
coverage for those two windows, not scientific selection of either window.

The unchanged frozen window `[-5.85, 8.00] eV` still selects 4--6 states per point:
129 points with four, 84 with five, and three with six. No band 13--20 state enters the
frozen window.

## Identities

| Artifact | SHA-256 |
|---|---|
| external inventory | `daa08323c81d54d36308f14c5d17f20fab741907783651d770f878077d24eeea` |
| consumed authorization | `6ed3170283e53ac9acc18b90be69520dc8c9afba1c1b16d3998c34ae4be0f68d` |
| exact `pw.in` | `20a6ee6e55d632bb66b1afcaac91592bf49c73a3e53e275659d1ccb03e47e1f9` |
| QEXSD | `2e1b5e157142d18210d18710fb9f5f3e813b17d8331acf96e11af9b9d4f7ef8c` |
| saved-state manifest | `24ee9d483141ab54d099bc6e6403d0da46108cc7a30c5b019992da3a1d7ef3ac` |
| `nscf-result.json` | `aa09004b447770f1a6ae1e1096e36fa522752e691998937d3b8beb49a51a088a` |
| target-space analysis | `976b605c1095e93fc99500ec93df0e7f495229afe83a2d185c666c6429daf444` |
| campaign result | `d726d0d89c65ebcabe94f1374916a4650d6bce0015977fc60f8c3c4d3a294492` |

The complete authenticated occurrence remains outside Git at
`/Users/eugene/projects/ksdft2effmass/si-accepted-s1-wannier-nscf-6x6x6-b20-david-c6-b20-v1`.
[`external-artifact-inventory.json`](external-artifact-inventory.json) binds all 242
files totaling 185,692,471 bytes. Large wavefunction and density artifacts remain
outside Git.

## Scientific disposition

This is an eligible `C6-B20` NSCF handoff and authenticated target-space inventory. It
is not an outer-window selection, Wannier interface, represented operator, or
intended-use result. A separate scientific decision is required before preparing any
20-band Wannier90 preprocessing. Conversion, localization, `C6-B30`, `C8`, `C12`,
confirmation, and every retry require separate authorization.
