# Periodic native-evidence presence audit

## Scope

This bounded read-only audit records filesystem presence observed at
`2026-09-19T23:55:22Z`, an Appendix G identity-authentication pass at
`2026-09-20T00:30:01Z`, and an interface-writer compatibility pass at
`2026-09-20T10:23:08Z`. None executed Wannier90, changed native files, opened Appendix
H archive contents, or transmitted unpublished artifacts. Filesystem presence, byte
identity, and writer compatibility are not scientific validation.

## Appendix G periodic-1D

The symbolic environment variables recorded by the retained execution contracts were
unset in the inspecting process:

- `WANNIER90_RUN_ROOT`;
- `WANNIER90_CONVERGENCE_RUN_ROOT`; and
- `WANNIER90_PRECONDITIONED_RUN_ROOT`.

A bounded search under the recorded external calculation hierarchy found these three
local directories:

- `/Users/eugene/calculations/ksdft2effmass/research-monograph/periodic-1d/wannier90-20260917T103931Z`;
- `/Users/eugene/calculations/ksdft2effmass/research-monograph/periodic-1d/wannier90-convergence-20260917T160456Z`; and
- `/Users/eugene/calculations/ksdft2effmass/research-monograph/periodic-1d/wannier90-preconditioned-20260917T162740Z`.

Each directory contained an `interface-manifest.json` and `low_pair` and `higher_pair`
subdirectories at the inspected depth.

### Appendix G identity authentication

The later bounded pass correlated the plausible roots with committed retained records
by comparing only file sizes and SHA-256 identities:

| Retained record | Bound local root | Identities checked | Mismatches |
|---|---|---:|---:|
| `wannier90-result.json` | `wannier90-20260917T103931Z` | 22 | 0 |
| `wannier90-convergence-attempt.json` | `wannier90-convergence-20260917T160456Z` | 5 | 0 |
| `wannier90-preconditioned-result.json` | `wannier90-preconditioned-20260917T162740Z` | 22 | 0 |

For the initial and preconditioned roots, every artifact identity in both retained
`low_pair` and `higher_pair` group inventories agreed in path-relative filename, byte
count, and SHA-256 digest. For the interrupted convergence attempt, all five explicitly
named native-output SHA-256 identities agreed. The pass did not reinterpret retained
numerical results, compare scientific observables, or rerun an extractor.

This establishes the observed local byte bindings for the listed retained records. A
bounded read-only compatibility check then supplied the authenticated initial and
preconditioned `_u.mat`, `_hr.dat`, and `.wout` bytes to the public parsers. All four
seed/root combinations parsed as 128 two-by-two gauge matrices, 129 two-by-two
Hamiltonian blocks, and two final localized-function observations. The retained
maximum converged iterations observed by the parser were 500 and 500 for the initial
roots, and 69 and 4,176 for the preconditioned roots. For both preconditioned seeds,
the interface parsers also retained a 128-by-2 eigenvalue table, 128 two-by-two
projection matrices, and 1,280 two-by-two neighbor overlaps organized as ten neighbors
for each of 128 k points. These are adaptation observations, not newly calculated
scientific results.

The subsequently extracted public native-artifact Workflow was then exercised
read-only with all eleven caller-supplied artifacts for each of the four initial and
preconditioned seed/root combinations. All 44 expected identities correlated exactly.
For every seed, the Workflow parsed the seven supported scientific text artifacts and
correlated 128 reciprocal points and two Wannier functions with the retained group.
The `.win`, `.chk`, standard-output, and standard-error bytes were authenticated but
not interpreted. This is software-compatibility evidence from existing artifacts, not
a new scientific calculation.

After deterministic public interface writers were extracted, a further read-only
compatibility pass used the authenticated preconditioned `low_pair` interface. The
public `.eig`, `.amn`, and `.mmn` parsers reconstructed typed records from retained
bytes; the new writers then reproduced all three files byte for byte, with `.mmn`
writing correlated against the parsed retained `.nnkp` record. A typed `.win` record
constructed from the retained explicit settings, cell, atom, projection line,
128-point x-directed mesh, and k-point order likewise reproduced the retained `.win`
bytes exactly. Its fractional reciprocal points agreed with parsed `.nnkp` coordinates
at zero absolute tolerance. No native file was changed, no `.nnkp` file was generated,
and no Wannier90 process ran. This establishes compatibility with those four retained
byte
representations only; it does not reconstruct the physical eigenvalues, projections,
or overlaps and does not strengthen the retained scientific claims.

The independent public Wilson verifier was then applied read-only to the same four
seed/root combinations with a phase tolerance of $10^{-10}$ radians, loop-unitarity
Frobenius tolerance of $10^{-10}$, and minimum active-overlap singular-value threshold
of $0.7$. All four groups passed. The largest direct-to-retained phase-set defect was
$8.89\times10^{-16}$ radians; the largest native-gauge-to-retained and gauge-covariance
defects were respectively $2.84\times10^{-12}$ and $2.84\times10^{-12}$ radians. The
minimum selected active-overlap singular value was $0.7083$, and the largest loop
unitarity defect was $7.90\times10^{-15}$. The integrated verified-native Workflow
subsequently returned a passing aggregate disposition for both the original and
preconditioned two-group records under those same controls. These are bounded
numerical-verification observations for the represented synthetic interface, not
topology, material
validation, or uncertainty quantification.

Identity and parser compatibility do not by themselves establish Wannier90 correctness,
numerical agreement between native and direct routes, or scientific validity. Public
adapters still consume explicit caller-supplied bytes and do not discover these roots.

## Appendix H periodic-2D

The following recorded local paths existed:

- `/Users/eugene/calculations/ksdft2effmass/research-monograph/periodic-2d/wannier90-20260918T090051Z`;
- `/Users/eugene/calculations/ksdft2effmass/research-monograph/periodic-2d/wannier90-balanced-20260918T091846Z`;
- `/Users/eugene/calculations/ksdft2effmass/research-monograph/periodic-2d/wannier90-study-20260918T101000Z`;
- `/Users/eugene/calculations/ksdft2effmass/research-monograph/periodic-2d/optimizer-basin-20260918T110000Z`; and
- `/Users/eugene/calculations/ksdft2effmass/research-monograph/periodic-2d/standalone-optimizer-20260918T121659Z`.

The following recorded archives existed as regular files:

| Archive | Observed size in bytes |
|---|---:|
| `periodic-2d-nondft-native-evidence-20260918T110000Z.tar.gz` | 3,043,738 |
| `periodic-2d-optimizer-basin-native-evidence-20260918T110000Z.tar.gz` | 63,801,989 |
| `periodic-2d-standalone-optimizer-native-evidence-20260918T121659Z.tar.gz` | 397,083,715 |

These local unpublished artifacts were not transmitted or modified. A later Appendix H
extraction must authenticate exact files against retained manifests before use.
