# Bulk-silicon execution contract

## Status

**Prospective calculation policy; no authorization.** This document defines the exact
bulk-silicon route requirements that must be supplied to authoritative Project Koios
simulation contracts. It does not redefine Project Koios process mechanics and must not
be treated as a runnable command recipe.

Executable invocation, pseudopotential acquisition, remote computation, and production
calculations remain protected actions.

## Upstream execution authority

Reusable one-process behavior belongs to
[`projectkoios.simulations.execution`](https://github.com/eragasa/projectkoios-simulations/blob/bbb9f1d8110ed9fe3ea1873c2366073c98f48c71/docs/architecture/projectkoios/simulations/execution/index.md).
Provider staging and native artifact behavior belong to the exact QE and Wannier90
integration contracts identified in [`architecture-plan.md`](architecture-plan.md).

This calculation adds exact scientific values, bounded invocation counts, workspace and
retention policy, resource bounds, warning/stop policy, predecessor gates, and explicit
authorization. If Project Koios cannot enforce a required rule, that rule remains a
capability gap rather than implied current behavior.

## Route occurrence inventory

A complete candidate route contains five separately identified occurrences:

| Order | Occurrence | Program | Required predecessor |
| ---: | --- | --- | --- |
| 1 | SCF parent | QE `pw.x` | Accepted exact calculation declaration |
| 2 | Full-grid NSCF | QE `pw.x` | Verified SCF saved-state handoff |
| 3 | Wannier preprocessing | `wannier90.x -pp` | Accepted exact Wannier declaration |
| 4 | QE/Wannier conversion | `pw2wannier90.x` | Verified NSCF handoff and authenticated `.nnkp` |
| 5 | Wannier localization | `wannier90.x` | Verified converter/interface handoff |

Each occurrence has a separate authorization decision unless one authorization packet
explicitly enumerates a finite ordered set and maximum invocation count. Configuration,
test selection, environment variables, or predecessor success never grant authority.
No occurrence may activate its successor automatically.

The current Project Koios baseline lacks a complete authoritative implementation of
occurrences 3 and 5. They cannot be run through ad hoc local substitutes and then
presented as conforming Project Koios evidence.

## Calculation preflight record

Before requesting authorization, the calculation version must freeze:

### Scientific identity

- exact physical branch and structure role: provisional seed \(S_0\), structural
  candidate, confirmation structure, or accepted \(S_*\), as applicable;
- exact structure bytes, source, status, and basis convention;
- exact pseudopotential source entry, native file identity, metadata, and license
  boundary;
- exchange-correlation, relativity, spin, charge, and occupation branch;
- stage-specific cutoffs, meshes, offsets, symmetry policy, solver controls, band
  count, windows, projections, rank, and energy convention; and
- predecessor calculation and handoff identities.

### Software identity

- Project Koios repository URL and exact implemented-dependency revision;
- consumed public symbols and schema versions;
- exact clean calculation repository revision;
- exact executable paths, byte sizes, SHA-256 identities, program versions, and
  source/build provenance; and
- retained dynamic-library/toolchain inventory.

An inspected baseline or version string is not an implemented-dependency identity.

### Operational bounds

- exact occurrence count for fixed routes or a frozen maximum plus conditional
  invocation inventory for bounded bulk-qualification feedback;
- retry policy, normally no retries;
- output, scratch, and retained-artifact roots outside the source repository;
- wall-time, processor/thread, memory, and storage bounds;
- stdout/stderr and environment-retention policy;
- warning, timeout, failure, and stop policy; and
- expected compact and external native outputs.

The current plan supplies no prospective resource numbers. They must be measured or
conservatively bounded before authorization; invented estimates are prohibited.

### Authority

- exact authorization identifier;
- authorized occurrence IDs and maximum invocations;
- approved executable and input identities;
- authorization expiry or single-use semantics where applicable; and
- confirmation that evidence promotion and successor activation are excluded.

## Workspace and retention policy

Every calculation version receives a new external root. It must not overwrite an
existing successful or failed occurrence. Bulk qualification and the later Wannier
route have distinct roots and occurrence namespaces. Conceptually:

```text
<external-bulk-qualification-root>/
├── qualification-manifest.json
├── seed-setting-grid/
├── iterations/
│   ├── 001-structural-convergence/
│   ├── 002-final-setting-confirmation/
│   └── ... new relaxation/confirmation pairs when the setting changes
├── accepted-structure-setting-pair/
└── verification/

<external-wannier-route-root>/
├── route-manifest.json
├── staged-inputs/
├── occurrences/
│   ├── 001-scf/
│   ├── 002-nscf/
│   ├── 003-wannier-preprocess/
│   ├── 004-pw2wannier90/
│   └── 005-wannier-localization/
└── verification/
```

The exact schema remains to be frozen by this calculation. Native wavefunctions,
densities, restart state, scratch, and large dense matrices remain external. This
repository retains only policy-approved compact inputs, checksums, software identities,
settings, status summaries, verification records, and compact results. External files
remain content-addressed by retained manifests.

Historical workspaces and provenance records must not be repurposed for new route
versions.

## Bulk-qualification predecessor

Before the five-occurrence Wannier route can be materialized, Project Koios must
produce a verified, non-authorizing accepted-pair handoff with this exact order:

1. separately admitted SCF occurrences over the declared coupled-cutoff/k-point grid
   on exact seed structure \(S_0\), yielding only \(Q_0@S_0\);
2. a separately admitted structural occurrence under \(Q_0\), yielding a candidate
   mechanically qualified structure \(S_1\);
3. separately admitted SCF confirmation occurrences on \(S_1\), yielding
   \(Q_1@S_1\); and
4. a deterministic accept, re-relax/reconfirm, inconclusive, or budget-exhausted
   decision.

An accepted correlated grid selects its highest tested mesh/cutoff corner. The
variable-cell assessment requires finite maximum force, scalar pressure, and a
complete finite stress tensor; exact thresholds and budgets must still be frozen
before authorization.

Changed settings create a new structural occurrence and changed structures create a
new confirmation study. Predecessor success never authorizes the successor. The
terminal handoff must bind the exact accepted \((S_*,Q_*)\), every contributing
occurrence and artifact identity, the feedback history, and the scientific disposition.
It then emits a new parent-SCF requirement. No confirmation occurrence is reused as the
Wannier-route parent under this architecture.

## Stage-specific Wannier-route requirements

### SCF parent

The declaration must bind the accepted bulk-qualification pair \((S_*,Q_*)\), exact
Si pseudopotential, cutoffs, reciprocal mesh and shift, occupation, symmetry,
electronic tolerance, solver policy, and exact `pw.x` identity.

The retained result must include exact rendered input, process evidence, parsed native
completion and SCF-convergence facts, structured warnings, and a closed SCF saved-state
handoff. Success authenticates this occurrence but does not re-establish or broaden the
accepted lattice/settings scope, pseudopotential, or toolchain.

### Full-grid NSCF

The declaration must bind the verified SCF parent, source-ordered unreduced k-points and
weights, band count, spin convention, solver policy, and exact `pw.x` identity. The
route must reject a symmetry-reduced list.

The retained result must bind QEXSD, observed dimensions, warnings, and a closed NSCF
saved-state handoff for conversion. Structure, pseudopotential, prefix, and parent
identity must agree with SCF.

### Wannier preprocessing

Before authorization, this calculation must freeze exact `.win` content or its exact
deterministic source within the accepted generic non-spin spectral subset, seedname,
unit cell, reciprocal mesh, rank, projections, windows, spin convention, and executable
identity.

The retained result must authenticate `.nnkp` and verify the declared cell, k-points,
neighbors, dimensions, and seedname. Preprocessing success does not validate windows
or projections.

### `pw2wannier90.x`

The declaration must bind the verified NSCF handoff, authenticated `.nnkp`, exact
converter input and executable, and one route-specific output inventory accepted by
Project Koios architecture.

The calculation must not require UNK artifacts from an AMN/MMN-only spectral route or
accept artifacts by basename. A component-operator occurrence additionally requires
the prospectively frozen plane-wave coefficient carrier; UNK files are required only
if that selected provider route declares and verifies them as sampled-wavefunction
evidence, with any sample-to-coefficient transform declared separately. Exact
interface outputs and their dimensional correlation form the localization handoff.

### Wannier localization

The declaration must bind exact `.win`, verified interface handoff, exact executable,
restart policy, expected outputs, and timeout/resource bounds. Ordinary localization
consumes EIG/AMN/MMN plus the verified topology; converter-produced UNKs remain
correlated sibling evidence for component analysis and are not staged into the
localization occurrence unless an explicitly reviewed native plotting or transport
mode consumes them.

The retained result must distinguish process completion from localization convergence
and retain `.wout`, `_hr.dat`, centers, spreads, iteration summary, warnings, and route
lineage. It must additionally retain `_u.mat` and `_u_dis.mat` exactly when the declared
construction requires their corresponding transformations. Incidental native files are
not retained evidence unless separately declared and authenticated. A completed
localization is a candidate representation, not an accepted one.

## Calculation failure policy

Any missing authorization, placeholder, identity mismatch, unsafe or overlapping
workspace, predecessor disagreement, dimension mismatch, or pre-existing output root
stops before calculator startup.

After startup, a timeout, signal, nonzero return code, missing required output, missing
native completion marker, parse failure, nonconvergence, or undeclared required
artifact produces a retained failure occurrence and stops the route. Partial native
outputs remain failure evidence and are never relabeled as successful artifacts.

A retry is a new occurrence. It must have a new identity and explicit authorization
coverage. It must not replace the failed occurrence.

## Warning policy

Warnings remain structured observations even when the return code is zero. The future
calculation declaration must prospectively classify:

- IEEE invalid, divide-by-zero, overflow, and underflow flags;
- OpenCL, MPI, BLAS/LAPACK, and dynamic-loader diagnostics;
- QE convergence and diagonalization warnings;
- Wannier disentanglement and localization warnings; and
- parser or dimensional inconsistencies.

The historical OpenCL-startup trap and `ZHEGVX` divide-by-zero diagnosis do not settle
the effect of warnings on future observables. Evidence promotion requires the
independent comparison in [`verification-plan.md`](verification-plan.md).

## First future authorization packet

The first protected request should be a Stage-0 historical-method comparator, not a
production or full Wannier route. Before requesting it, freeze:

- purpose: compare provisional C48/K8 observables, residuals, and warnings;
- branch: historical PBE scalar-relativistic standard Si UPF, not v0.5/stringent;
- exact historical provisional geometry;
- 48/192 Ry and shifted `8 x 8 x 8` mesh;
- one SCF and, only if required by the frozen comparison, one linked diagnostic NSCF;
- an independently identified established QE/toolchain;
- no retries; and
- exact process, observable, residual, warning, and compact-comparison outputs.

The exact invocation count must be frozen before authorization. This is a
historical-method comparator only. Mixed cutoff-mesh interaction, the v0.5 production
parent, valley search, and the Wannier route require separate future packets.

## Authorization meaning

Authorization permits only the enumerated protected operation. It does not ask the
operator to certify software correctness or scientific validity, accept resulting
evidence, authorize a successor, or permit publication.
