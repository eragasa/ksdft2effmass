# Readiness record

## Inspection boundary

This record describes a read-only inspection of Project Koios commit
`bbb9f1d8110ed9fe3ea1873c2366073c98f48c71` and selected machine-local resources.
Local paths and file observations are deployment facts, not portable requirements or
scientific acceptance. No scientific executable was run.

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
project PBE equilibrium lattice. This calculation has now selected
`Si.PrimitiveUnitCell`, byte size `680`, SHA-256
`6e048c7001f329459e85f321e7bd406f4dd871d6fabf8d12fa349a1623f87ccc`, only as the
provisional \(S_0\) recorded in
[`seed-structure-decision.md`](seed-structure-decision.md). This calculation's
historical predecessor used a provisional 10.20-bohr geometry, also not accepted as a
production PBE lattice.

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
- structure: `Si.PrimitiveUnitCell`, SHA-256
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
| Must fix | Bulk-qualification policy beyond the selected \(S_0\) is not frozen | Declare cutoff/k-point coordinates and criteria, structural cell mode/criteria, and feedback budget |
| Must fix | No stable accepted structure/settings pair exists | Implement the reusable ProjectKoios bulk-qualification route, then request separate authorization for the bounded campaign |
| Must fix | Accepted v0.5/stringent Si UPF2 bytes are absent | Perform a separately bounded acquisition and verification operation |
| Must fix | Local QE 7.5 does not provide the required independent comparator | Identify and bind a genuinely independent established QE/toolchain path |
| Must fix | Project Koios examples do not encode historical C48/K8 or future production intent | Keep exact campaign data here and use Project Koios records/integrations to validate it |
| Must fix | SCF-to-NSCF-to-Wannier artifact closure is incomplete | Complete the coordinated upstream spectral and component-operator route architecture and implementation without calculator execution |
| Must fix | Numerical, valley/mass, and Wannier acceptance protocols are not frozen | Complete this calculation's scientific declarations and independent-verification contracts |
| Must fix | Resource and warning policies are unbound | Measure or bound resources and prospectively classify warnings before authorization |
| No action required | Exact candidate QE 7.5 and Wannier90 bytes were located | Retain these observations as deployment candidates only |

## Readiness conclusion

The repository is suitable as the reusable software owner for future implementation,
but the calculation is not ready for an execution authorization request. The next work
is documentation review followed by software-only bulk-qualification and Wannier
artifact-route closure. Scientific inputs, exact campaign declarations,
independent-toolchain evidence, and authorization remain later gates.
