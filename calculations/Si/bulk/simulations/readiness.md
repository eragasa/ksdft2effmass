# Readiness record

## Inspection boundary

This record began as a read-only inspection of Project Koios commit
`bbb9f1d8110ed9fe3ea1873c2366073c98f48c71` and selected machine-local resources.
Local paths and file observations are deployment facts, not portable requirements or
scientific acceptance. It now also records the separately authorized finite-setting
campaigns and FCC-native volume-only relaxation retained under this calculation root;
those occurrences do not establish production acceptance or authorize successors.

## Repository capability status

| Surface | Present | Remaining gate |
| --- | --- | --- |
| Exact structure library | Yes | Select and accept a production lattice; existing 5.43 Å examples are not accepted production inputs |
| Exact simulation library | Yes | Add no production claim to existing SSSP example records; this calculation must own exact campaign declarations |
| Exact pseudopotential resolver | Yes | Acquire and catalog the accepted v0.5/stringent Si UPF2 bytes |
| QE SCF projection/extraction | Yes | Materialize the intended branch and close warning/toolchain policy |
| Reusable SCF convergence composition | Partial | Generalize exact k-point coordinates and coupled cutoff identity; bind every observation to structure, specification, occurrence, and evidence |
| Relaxation facts and QE execution | Partial | Add reusable zero-pressure assessment, neutral lifecycle composition, and mechanically qualified structure outcome |
| Bulk qualification and stable-pair feedback | No | Implement structure-scoped setting qualification, structural convergence, fresh confirmation, and bounded re-relax/reconfirm composition |
| SCF saved-state contracts | Yes | Demonstrate one canonical closed handoff consumed by the NSCF route |
| QE Wannier-oriented NSCF | Yes | Replace tutorial placeholders with separately owned exact declarations and a verified parent |
| `pw2wannier90.x` projection/runner | Yes | Separate the AMN/MMN spectral manifest from an optional UNK sampled-wavefunction profile and bind any coefficient transform independently |
| Wannier90 artifact parsers | Yes | Add preprocessing/localization execution and route-level artifact closure |
| First-party bulk-qualification composition | No | ProjectKoios must implement adapters plus `tools/pw_dft_bulk_qualification` without transferring \(Q_0@S_0\) to another structure |
| End-to-end Wannier route composition | No | ProjectKoios must implement outward `projectkoios.adapters` mappings and `tools/pw_dft_wannierization` provider binding and route invocation outside its protected core |
| Independent scientific verifier | No | Define and implement this calculation's verification contracts |
| Production authorization | No | Request only after every preflight field is complete |

## Existing silicon structures

Two reviewed example families use a nominal 5.43 Å two-atom diamond primitive cell.
They differ in direct-vector ordering and stable identity:

- `Si.PrimitiveUnitCell` in `examples/workflows/pw_dft_scf/structures/` uses
  `(a1, a2, a3) = ((1/2,1/2,0), (1/2,0,1/2), (0,1/2,1/2))` times 5.43 Å;
- `Si.primitive` in `examples/projectkoios/simulations/dft/pw/Si/primitive/` uses a
  cyclic ordering and binds its band paths to that order.

Both are explicit, useful examples. Neither record states that 5.43 Å is an accepted
project PBE equilibrium lattice. The ProjectKoios `Si.PrimitiveUnitCell` record is
left-handed. This calculation has derived and selected the right-handed
`Si.PrimitiveUnitCell.RightHanded`, byte size `692`, SHA-256
`7bef37dfe20ce58a137de942ec1fa0aa50d6e7049b0265790f12171bc834529a`, only as the
provisional \(S_0\) recorded in
[`seed-structure-decision.md`](seed-structure-decision.md). The derivation swaps the
first two direct vectors and corresponding fractional-coordinate components without
changing Cartesian geometry. This calculation's historical predecessor used a
provisional 10.20-bohr geometry, also not accepted as a production PBE lattice.

## Pseudopotential inventory

### Accepted future branch

The project pseudopotential specification selects PseudoDojo ONCVPSP v0.5 PBE
scalar-relativistic stringent UPF2. At inspection:

- `/Users/eugene/opt/pseudopotentials/catalog/pseudopotentials-v1.sqlite3` contained
  zero `source_entries` and zero `artifacts` rows;
- `artifacts/sha256/` contained no files; and
- `manifests/sets/` contained no set manifests.

Therefore no exact v0.5/stringent Si artifact is ready for composition.

### Historical standard branch

The historical artifact remains available at:

```text
/Users/eugene/opt/pseudodojo/1.0/pbe/nc-sr-04-standard/Si/Si.upf
```

Observed identity:

- byte size: `225602`;
- SHA-256: `39822757f53f36e3bf3bfb779356152a8d3f21199c7db9dd5a931e5d18c45282`;
- UPF 2.0.1, ONCVPSP 3.3.0, PBE, norm-conserving,
  scalar-relativistic, four valence electrons according to retained provenance.

This exact file may support a bounded historical-method comparator. It is not the
accepted v0.5/stringent production artifact.

### Existing Project Koios SSSP branch

Current SCF examples bind:

- filename: `Si.pbe-n-rrkjus_psl.1.0.0.UPF`;
- byte size: `1299382`;
- SHA-256: `ae3aefd0811f9499dbc4a72f1f9ae02ef4fc7f3568bf6f559b68668719c69e2b`;
- PBE, USPP, scalar relativistic, four valence electrons.

Matching local bytes exist beneath SSSP 1.3.0 efficiency and precision views. This
branch is an example/possible separately authorized QE comparator, not the primary
common baseline.

## Executable inventory

### Quantum ESPRESSO 7.5

Observed files:

| Program | Path | Byte size | SHA-256 |
| --- | --- | ---: | --- |
| `pw.x` | `/Users/eugene/projects/q-e-qe-7.5/build/bin/pw.x` | 9673048 | `87aa72158e2c103c63fce1deca977dc42ff4ba344519a9662aadb96d33eab910` |
| `pw2wannier90.x` | `/Users/eugene/projects/q-e-qe-7.5/build/bin/pw2wannier90.x` | 8379632 | `61c8255b0745df2a5dec3c55e600b1f8b87039b564004997ac45cfee42cf2c8c` |
| bundled `wannier90.x` | `/Users/eugene/projects/q-e-qe-7.5/build/bin/wannier90.x` | 988680 | `91d0f7e522b0c36dbf72d6c3ae82d20f551316ce9d624cbc4618d0d1551928f1` |

The QE source checkout identifies tag `qe-7.5` and revision
`770a0b2d12928a67048e2f3da8d10d057e52179e`. The build is a Release MPI build,
uses Homebrew OpenMPI and FFTW, and links Apple's Accelerate framework for BLAS/LAPACK.
`pw.x` and `pw2wannier90.x` are not on the observed `PATH`.

The `pw.x` identity exactly matches the calculator recorded by the retained 36-point
Project Koios silicon SCF grid. That grid records successful exits and SCF convergence
but also records IEEE invalid, divide-by-zero, overflow, and underflow warnings for
every observation. Availability and repeatability therefore do not close the
independent-toolchain or warning-disposition gates.

The previously referenced QE 7.2 path
`/Users/eugene/projects/q-e-qe-7.2/build/bin/pw.x` was absent at inspection. Diagnostic
QE 7.2 builds remain elsewhere but are investigation artifacts, not an automatically
accepted production installation.

### Wannier90 3.1.0

The observed `PATH` resolves:

```text
/Users/eugene/.local/bin/wannier90.x
  -> /Users/eugene/projects/wannier90-3.1.0-local/bin/wannier90.x
```

Observed target identity:

- byte size: `891048`;
- SHA-256: `c826f817f807cf069e16d6e529a52ddc15d2f677101065908bcb2030d7f7d1dd`;
- Mach-O arm64;
- linked against Homebrew OpenBLAS, OpenMPI, GCC Fortran, and `libquadmath`.

The path and directory name identify a candidate 3.1.0 deployment. A future
execution declaration must still bind the exact executable, source/build provenance,
and dynamic-library inventory; this observation does not accept it.

## Retained Project Koios SCF evidence

The repository retains 36 silicon SCF observations under:

```text
examples/projectkoios/integrations/quantumespresso/pw/scf/Si/primitive/
  convergence/joint/evidence/
```

The closed manifest binds:

- calculator: exact QE 7.5 `pw.x` above;
- pseudopotential: exact SSSP USPP above;
- structure: left-handed parent `Si.PrimitiveUnitCell`, SHA-256
  `6e048c7001f329459e85f321e7bd406f4dd871d6fabf8d12fa349a1623f87ccc`;
- 30 initial-grid plus 6 adaptive-extension coordinates;
- mesh densities 2 through 14 over the retained grid;
- wavefunction cutoffs 15 through 40 Ry and charge-density ratio 8; and
- exact input, output, error, and execution records.

All observations report return code zero, native completion, and SCF convergence. All
also retain the four IEEE warning classes. The manifest explicitly limits the evidence
to finite-grid total-energy observations and excludes force, stress, band, NSCF,
Wannier, effective-mass, dopant, and defect convergence. It also states that the local
prototype source used to produce the grid lacks a committed identity.

This evidence can exercise authentication, parsing, replay, and comparison software.
It cannot be transferred into this calculation's production acceptance.

## Retained right-handed finite-setting evidence

This calculation retains compact records for the authorized Gamma-centered k-point
campaign under
[`evidence/sssp-1.3.0-pbe-efficiency-qe-7.5-right-handed-gamma-kpoint/`](evidence/sssp-1.3.0-pbe-efficiency-qe-7.5-right-handed-gamma-kpoint/).
The calculation-owned `kpoints_convergence_atol = 1.0 meV/atom` rule compares with K12
and selects K10 as the smallest passing sampled mesh.

The authorized cutoff campaign at Gamma-centered K10 is retained under
[`evidence/sssp-1.3.0-pbe-efficiency-qe-7.5-right-handed-gamma-k10-encut/`](evidence/sssp-1.3.0-pbe-efficiency-qe-7.5-right-handed-gamma-k10-encut/).
Its `encut_convergence_atol = 1.0 meV/atom` rule compares with 60 Ry and selects
42/336 Ry as the wavefunction/density cutoff pair. The earlier shifted campaign remains
retained but is superseded for downstream setting selection.

QE no longer reports a negative lattice determinant. The finite-setting occurrences
used `ibrav=0` and retained its generic symmetry advisory. Every successful occurrence
also retained invalid, divide-by-zero, overflow, and underflow IEEE flags. These flags
are retained as native QE diagnostics rather than treated as automatic blockers when
the occurrence completes, converges, and produces finite observations.

## Retained FCC-native volume-only relaxation

One separately authorized QE 7.5 occurrence used the exact right-handed seed,
Gamma-centered K10, 42/336 Ry, `ibrav=2`, and `cell_dofree='ibrav'`. The native
cubic-FCC representation preserves the declared scalar volume-only scope. The exact
input, stdout, stderr, execution record, QEXSD, compact interpretation, and external
artifact inventory are retained under
[`evidence/sssp-1.3.0-pbe-efficiency-qe-7.5-right-handed-gamma-k10-c42-vc-relax-ibrav2/`](evidence/sssp-1.3.0-pbe-efficiency-qe-7.5-right-handed-gamma-k10-c42-vc-relax-ibrav2/).

The occurrence returned zero, reached the QE terminal marker, and reported electronic
and BFGS convergence. The existing KSD QEXSD parser read QEXSD version `25.05.21` with
exit status zero; ProjectKoios confirmed stdout/QEXSD terminal and atom-count
consistency. The provisional result has conventional lattice parameter
`5.469182093640207 angstrom`, optimizer-terminal pressure `0.01 kbar`, final-SCF
pressure `0.09 kbar`, and zero reported optimizer-terminal maximum force. It is
retained as provisional \(S_1\), SHA-256
`d131107753512c53dc0a32b9e07e0081f8277d8eeafcb9fad5f1fc7f153ded03`, pending fresh
k-point and cutoff confirmation.

The first confirmation stage has compact preflight under
[`preflight/s1-gamma-c42-kpoint-confirmation/`](preflight/s1-gamma-c42-kpoint-confirmation/):
Gamma-centered K6/K8/K10/K12 at fixed 42/336 Ry, with the existing `1.0 meV/atom`
K12-reference rule. The exact four-invocation packet was authorized and completed with
zero retries. All four SCFs returned zero and converged. The absolute K10–K12 energy
difference is `0.29027746276710786 meV/atom`, so the calculation-owned rule again
selects K10. Compact evidence is retained under
[`evidence/sssp-1.3.0-pbe-efficiency-qe-7.5-right-handed-s1-gamma-c42-kpoint-confirmation/`](evidence/sssp-1.3.0-pbe-efficiency-qe-7.5-right-handed-s1-gamma-c42-kpoint-confirmation/).

The separately authorized cutoff stage ran five new K10 occurrences and reused the
exact C42 occurrence without rerunning it. All five new occurrences returned zero and
converged, with no retries. The C42–C60 difference is
`0.6180386100993474 meV/atom`, so the calculation-owned rule again selects 42/336 Ry.
Evidence is retained under
[`evidence/sssp-1.3.0-pbe-efficiency-qe-7.5-right-handed-s1-gamma-k10-cutoff-confirmation/`](evidence/sssp-1.3.0-pbe-efficiency-qe-7.5-right-handed-s1-gamma-k10-cutoff-confirmation/).

## Existing NSCF and Wannier examples

The retained silicon NSCF and four-file Wannier90 example11 inputs are citation-bound
tutorial inputs from Wannier90 3.1.0. The NSCF materialization template contains
placeholder paths and an all-zero parent-manifest identity. It uses a `4 x 4 x 4` grid,
12 bands, 25 Ry, and `Si.pbe-n-van.UPF`; those values are tutorial provenance, not the
future production route.

No matching SCF saved state, materialized production NSCF declaration, generated
`.nnkp`, converter output, localization output, or accepted silicon Wannier evidence is
present.

## Current readiness findings

| Disposition | Problem | Smallest next action |
| --- | --- | --- |
| No action required | Fresh S1 confirmation selected the same K10/42/336 Ry tuple and the operator accepted the exact pair under the calculation-owned rules | Preserve `accepted-stable-pair.json`; do not transfer the separate generic ProjectKoios policy result |
| No action required | The original `ibrav=0` volume-only occurrence failed before SCF | Preserve it as failed setup evidence; the separately authorized FCC-native route corrected the incompatibility without broadening the cell degrees of freedom |
| No action required | The stable pair, separate parent SCF, and eligible Davidson NSCF handoff exist with authenticated saved-state lineage | Preserve every occurrence identity and require separate authority for each downstream calculator |
| Must fix | Accepted v0.5/stringent Si UPF2 bytes are absent | Perform a separately bounded acquisition and verification operation |
| Must fix | Local QE 7.5 does not provide the required independent comparator | Identify and bind a genuinely independent established QE/toolchain path |
| Must fix | Project Koios examples do not encode historical C48/K8 or future production intent | Keep exact campaign data here and use Project Koios records/integrations to validate it |
| No action required | The revised Davidson NSCF returned zero with consistent finite 64-point/12-band QEXSD data and no `c_bands` diagnostics | Preserve it as the candidate handoff; do not relabel the blocked CG occurrence |
| No action required | The authorized preprocessing occurrence produced a verified 64-point, rank-10 NNKP topology | Preserve its exact identity as the candidate converter input; do not infer downstream adequacy |
| No action required | The authorized converter produced finite 64-point/12-band AMN/MMN/EIG artifacts with exact NNKP-neighbor and QEXSD-eigenvalue correlation | Preserve their identities as the candidate localization interface; do not infer localization adequacy |
| Must fix | The retained ProjectKoios tranche lacks the planned first-party preprocessing execution provider and currently needs a PhysKit converter-name compatibility alias | Preserve the recorded gap; use the protected single-attempt executor for this qualification occurrence and repair the reusable boundary separately |
| No action required | The first-candidate grid, bands, rank, projections, window policy, disentanglement, ordering, and evidence profile are approved | Preserve `wannier-interface-decision.md`; do not report the candidate as production-adequate |
| No action required | QE emits four IEEE flag classes after otherwise successful occurrences | Retain the native diagnostics; revisit only if they accompany non-finite results, failed convergence, or corrupted output |
| No action required | Exact candidate QE 7.5 and Wannier90 bytes were located | Retain these observations as deployment candidates only |

## Readiness conclusion

The right-handed Gamma-centered finite-setting campaigns and the FCC-native
zero-pressure relaxation are complete and compactly retained. K10 and 42/336 Ry were
selected on \(S_0\), and the relaxation produced provisional \(S_1\). The fresh
k-point and cutoff axes on S1 again selected K10 and 42/336 Ry, respectively, and the
operator accepted that exact structure/settings pair under the declared
calculation-owned rules. A new separately authorized parent SCF completed and retained
an authenticated saved state; confirmation SCFs were not reused. The immediate gate is
a new calculation-owned disentanglement decision, if one is selected. The first
rank-reducing ProjectKoios provider is implemented and verified. Its first occurrence
failed both optimization gates; the separately authorized conditioned and damped
revision fixed Wannierisation but still exhausted 1000 disentanglement iterations at a
fractional delta of `3.815e-6`, above the declared `1.0e-10` tolerance. No retry
authorization is in force. The blocked CG occurrence also remains retained under its
original identity.
The downstream artifact route and broader independent verification remain incomplete.
