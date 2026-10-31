# Project Koios adoption and composition plan

## Status

**Calculation-specific adoption plan; no reusable software authority.** This document
states how the bulk-silicon calculation intends to consume Project Koios. Project Koios
owns reusable simulation behavior, provider binding, and executable route composition.
This calculation owns exact scientific values, the scientific campaign instantiation,
retained evidence, thresholds, route reconciliation, and acceptance.

No capability named here is treated as implemented unless it exists at the pinned
Project Koios revision and passes its own verification gates.

## Upstream revisions

The inspected implementation baseline is
[`projectkoios-simulations@bbb9f1d8110ed9fe3ea1873c2366073c98f48c71`](https://github.com/eragasa/projectkoios-simulations/tree/bbb9f1d8110ed9fe3ea1873c2366073c98f48c71).
It supplies reusable records and integrations that can support parts of the route, but
it does not contain a complete provider-neutral SCF-to-Wannier workflow.

The reviewed documentation-only architecture is pinned to ProjectKoios commit
`7ad5cad6576338945959a683f3cd407759e7c37c`. That commit descends from the inspected
baseline and specifies bulk qualification, generic non-spin spectral Wannierization,
provider boundaries, adapters, tools, compatibility, and migration treatment. It adds
no implementation under `src/`, reserves no production API, and grants no acquisition
or calculator authority. Publication, review, or later merge status does not convert
that documentation into implemented behavior; the immutable hash remains the
calculation's reviewed architecture pin.

Normative reusable behavior remains with these upstream authorities:

| Concern | Immutable upstream authority | Baseline status |
| --- | --- | --- |
| Single authorized calculator occurrence | [`projectkoios.simulations.execution`](https://github.com/eragasa/projectkoios-simulations/blob/bbb9f1d8110ed9fe3ea1873c2366073c98f48c71/docs/architecture/projectkoios/simulations/execution/index.md) | Implemented baseline |
| Calculator-neutral exact inputs | [`projectkoios.simulations.calculator_input`](https://github.com/eragasa/projectkoios-simulations/blob/bbb9f1d8110ed9fe3ea1873c2366073c98f48c71/docs/architecture/projectkoios/simulations/calculator_input/index.md) | Implemented baseline |
| Calculator-neutral evidence | [`projectkoios.simulations.evidence`](https://github.com/eragasa/projectkoios-simulations/blob/bbb9f1d8110ed9fe3ea1873c2366073c98f48c71/docs/architecture/projectkoios/simulations/evidence/index.md) | Implemented baseline |
| SCF convergence composition | [`simulations.workflows.pw_dft_scf`](https://github.com/eragasa/projectkoios-simulations/blob/bbb9f1d8110ed9fe3ea1873c2366073c98f48c71/docs/architecture/projectkoios/simulations/workflows/pw_dft_scf/index.md) | Implemented energy-grid foundations; structure/evidence-bound qualification and general k-point/coupled-cutoff identity remain incomplete |
| Neutral relaxation composition | [`simulations.workflows.pw_dft_relaxation`](https://github.com/eragasa/projectkoios-simulations/blob/bbb9f1d8110ed9fe3ea1873c2366073c98f48c71/docs/architecture/projectkoios/simulations/workflows/pw_dft_relaxation/index.md) | Partial projection handoff; no complete neutral lifecycle or zero-pressure assessor |
| QE SCF and saved state | [`integrations.quantumespresso.pw.scf`](https://github.com/eragasa/projectkoios-simulations/blob/bbb9f1d8110ed9fe3ea1873c2366073c98f48c71/docs/architecture/projectkoios/integrations/quantumespresso/pw/scf/index.md) | Partial route capability |
| QE fixed/variable-cell relaxation | [`integrations.quantumespresso.pw.relaxation`](https://github.com/eragasa/projectkoios-simulations/blob/bbb9f1d8110ed9fe3ea1873c2366073c98f48c71/docs/architecture/projectkoios/integrations/quantumespresso/pw/relaxation/index.md) | Provider projection/execution/parsing foundations exist; scientific qualification remains neutral-workflow policy |
| QE Wannier-oriented NSCF | [`integrations.quantumespresso.pw.nscf`](https://github.com/eragasa/projectkoios-simulations/blob/bbb9f1d8110ed9fe3ea1873c2366073c98f48c71/docs/architecture/projectkoios/integrations/quantumespresso/pw/nscf/index.md) | Implemented provider stage; tutorial declaration only |
| QE-to-Wannier converter | [`integrations.quantumespresso.pw2wannier90`](https://github.com/eragasa/projectkoios-simulations/blob/bbb9f1d8110ed9fe3ea1873c2366073c98f48c71/docs/architecture/projectkoios/integrations/quantumespresso/pw2wannier90/index.md) | Implemented provider stage with unresolved route inventory |
| Wannier90 native parsing | [`integrations.wannier90`](https://github.com/eragasa/projectkoios-simulations/blob/bbb9f1d8110ed9fe3ea1873c2366073c98f48c71/docs/architecture/projectkoios/integrations/wannier90/index.md) | Parser-only baseline; no subprocess behavior |

These links identify the inspected baseline, not a future implementation/conformance
pin.

## Planned upstream capabilities

The coordinated upstream design requires two provider-neutral capability owners:

```text
projectkoios.simulations.workflows.pw_dft_bulk_qualification
projectkoios.simulations.workflows.pw_dft_wannierization
```

Their reviewed documentation authorities at
`7ad5cad6576338945959a683f3cd407759e7c37c` are:

```text
docs/architecture/projectkoios/simulations/workflows/pw_dft_bulk_qualification/
docs/architecture/projectkoios/simulations/workflows/pw_dft_wannierization/
```

The bulk-qualification workflow composes structure-scoped joint cutoff/k-point
qualification, structural convergence, fresh confirmation on the resulting structure,
and a bounded re-relax/reconfirm feedback loop. Its terminal handoff is an exact
accepted pair \((S_*,Q_*)\). The separate Wannier workflow consumes that pair as the
qualified-parent predecessor and retains exactly five calculator occurrences.

The coordinated outward provider designs are planned at:

```text
docs/architecture/projectkoios/integrations/wannier90/preprocessing/
docs/architecture/projectkoios/integrations/wannier90/localization/
docs/architecture/projectkoios/integrations/quantumespresso/pw2wannier90/artifacts/
```

The first two specify unimplemented single-occurrence preprocessing and localization
surfaces while preserving the current parser-only status. The third separates the
implemented AMN/MMN/EIG converter path from a future explicit UNK-producing profile.
The upstream distribution must additionally provide outward `projectkoios.adapters`
mappings, `tools/pw_dft_bulk_qualification`, and `tools/pw_dft_wannierization` for
provider selection, operational configuration, complete route invocation, and
submission of separately admitted occurrences without integration-to-workflow imports.

Those capabilities may own reusable, policy-parameterized route state, occurrence requirements,
non-authorizing handoffs, neutral artifact-role requirements, parent/child lineage, and
software consistency outcomes. It must not own:

- silicon-specific settings or scientific thresholds;
- QE or Wannier90 classes and native suffixes;
- executable paths or reusable execution authority;
- application scheduling, retries, leases, or durable runtime state; or
- this calculation's evidence promotion or publication claims.

These paths are reviewed architecture authorities at the pinned documentation commit.
They remain unimplemented design contracts and must not be cited as production
behavior or importable APIs.

## Calculation-owned composition

This directory first owns the scientific instantiation of the bulk-qualification
sequence:

1. joint coupled-cutoff/k-point qualification on the selected exact provisional
   [`Si.PrimitiveUnitCell.RightHanded` \(S_0\)](seed-structure-decision.md);
2. structural convergence under provisional \(Q_0@S_0\);
3. fresh joint confirmation on the resulting structure; and
4. bounded re-relax/reconfirm feedback until \((S_*,Q_*)\) is accepted or the route
   terminates without acceptance.

It then owns the scientific instantiation of the exact five-occurrence Wannier route.
Project Koios owns both reusable executable compositions, provider binding, and
orchestration mechanics:

1. QE SCF parent consuming \((S_*,Q_*)\);
2. QE full-grid NSCF child;
3. Wannier90 preprocessing;
4. `pw2wannier90.x`; and
5. Wannier90 localization.

It also owns:

- accepted structure and pseudopotential identities;
- cutoffs, meshes, offsets, solver controls, band counts, windows, projections, and
  rank;
- external workspace, resource, timeout, warning, retry, and retention policies;
- construction and withheld sets;
- energy, gauge, cluster, and represented-operator alignment policy;
- numerical and scientific thresholds;
- independent-toolchain comparison;
- retained results and failure evidence; and
- authorization and evidence-promotion decisions.

Project Koios validates and executes reusable mechanics; it does not choose or promote
these values.

## Provider boundary

The neutral workflow must refer to generic artifact roles and exact artifact
references. Provider-native records remain outward:

- QE input, QEXSD, SCF/NSCF saved states, and `pw2wannier90.x` artifacts remain under
  `projectkoios.integrations.quantumespresso`;
- `.win`, `.nnkp`, `.eig`, `.amn`, `.mmn`, `_u.mat`, `_u_dis.mat`, `_hr.dat`, and
  native Wannier90 parsing remain under `projectkoios.integrations.wannier90`; and
- first-party reusable application/provider composition must be shipped by the
  ProjectKoios simulations repository outside the protected neutral core; this
  calculation supplies exact declarations but does not reimplement that composition.

The current AMN/MMN-only converter configuration and UNK-bearing provider manifest do
not describe one closed route. Project Koios must resolve them as separate
route-specific provider manifests before this calculation binds either profile. The
spectral profile must not inherit a globally mandatory UNK role. The Si-VC
component-operator profile must bind authenticated plane-wave coefficient evidence and
may require UNKs only when the frozen provider route actually produces and verifies
them as distinct sampled-wavefunction evidence. Any sample-to-coefficient transform is
a separate verified handoff. This calculation must not invent missing UNK files,
relabel samples as coefficients, or weaken artifact verification.

The current upstream Wannier90 authority explicitly excludes subprocess behavior.
Preprocessing and localization execution therefore remain unavailable until a reviewed
upstream architecture and implementation change is merged. A local script must not
silently substitute for that missing capability.

## Adoption sequence

### A0 — calculation documentation

- maintain the scientific, execution, verification, and readiness documents in this
  directory;
- state unresolved decisions without selecting values by convenience; and
- pin immutable upstream baseline links.

### A1 — upstream architecture

Project Koios documents the bulk-qualification workflow, SCF convergence and
relaxation owners, accepted-pair handoff, separate neutral Wannier route, outward
preprocessing/localization boundaries, adapters, and first-party tools. Completion
establishes design authority only, not implemented capability.

### A2 — upstream implementation and verification

Project Koios implements the reviewed bulk-qualification and Wannier workflows,
provider records/integrations, adapters, and first-party tools; verifies them with
synthetic/retained fixtures and fake executables; and merges a reviewed commit. No
production silicon calculation is required for this stage.

### A3 — dependency decision

This project reviews the upstream public surface and exact merged commit. Adding or
replacing a dependency in `python/pyproject.toml` and `python/uv.lock` requires explicit
human authorization under repository policy.

### A4 — exact calculation declarations

After dependency acceptance, this directory materializes exact simulation declarations
and records:

- upstream repository and full commit SHA;
- consumed public symbols and schema versions;
- local seed structure, cutoff/k-point policy, structural policy, feedback budget, and
  accepted-pair declaration identities;
- local Wannier-route declaration identities;
- exact executable and external-artifact identities; and
- compatibility verification evidence.

### A5 — bounded execution

Only a complete, separately authorized occurrence may run. Success does not activate a
successor or promote evidence automatically.

## Conformance record

A future calculation version must include an explicit record equivalent to:

```text
calculation declaration X
conforms to Project Koios contract Y
at exact revision Z
under local verification evidence V
```

The record must distinguish:

- **inspected baseline** — architecture/capability inventory only;
- **implemented dependency** — exact reviewed upstream revision installed and tested;
- **calculation composition** — local declarations validated against that dependency;
  and
- **scientific acceptance** — local numerical/scientific evidence accepted for a
  named use.

No status implies the next one.

## Prohibited duplication

This directory must not copy or redefine upstream public field inventories, validation
algorithms, generic path-safety rules, process failure taxonomy, or software test
matrix. Local documents may state stricter calculation requirements and identify
missing upstream behavior, but reusable semantics change only in Project Koios.
