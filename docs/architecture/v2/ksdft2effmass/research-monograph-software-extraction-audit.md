# Research-monograph software-extraction audit

## Scope

This read-only audit compares all twelve calculation directories under
`calculations/research-monograph/` and all maintained monograph chapters and appendices
under `docs/publications/research-monograph/` with the current public
`python/src/ksdft2effmass/` ownership surfaces. It inspected 135 Python files containing
51,975 lines. It did not execute a retained calculation, rerun a verifier, modify a
retained result, or inspect unpublished archive contents.

The audit asks whether demonstrated reusable software behavior has a public typed owner
and whether the corresponding campaign uses that owner. A frozen historical runner may
remain intentionally duplicated as evidence; that does not make it the supported
implementation. Plotting and manuscript-only exposition are not required to become
scientific library APIs.

Status meanings:

- **integrated**: reusable computation and campaign contracts have public owners; only
  frozen adapters or presentation code remain local;
- **partially extracted**: important lower-layer capabilities exist publicly, but
  campaign records, orchestration, verification, or demonstrated algorithms remain
  local;
- **not extracted**: the demonstrated reusable behavior has no corresponding public
  implementation; and
- **not presently applicable**: prose is explanatory, proposed, or literature-only and
  does not yet justify an executable API.

## Calculation-directory findings

| Calculation directory | Status | Public coverage | Material still local or missing |
|---|---|---|---|
| `harmonic-oscillator` | **integrated** | Public model-system, campaign input/result, evaluation, serialization, and verification objects | Historical plotting remains local presentation code |
| `particle-in-box` | **integrated** | Public analytical/finite-difference models plus residual, convergence, eigenpair, identifiability, norm-sweep, serialization, and verification campaign objects | Five local plotting scripts remain presentation code |
| `impurity-defect-1d` | **partially extracted** | Generic lattice models, represented operators, compatibility, gauge bridges, composition, route reconciliation, spectra, locality, and subspace diagnostics | Exact campaign input/result formats, parent loading, matched extraction Workflow, smoothness/metric controls, verifier, and serializer remain local |
| `impurity-defect-1d-independent-route` | **partially extracted** | Generic independent construction, alignment, compatibility, and route-reconciliation capabilities exist | Campaign route records, baseline loading, adversarial controls, real-space/Bloch route orchestration, serializer, and independent verifier remain local |
| `impurity-defect-1d-analytical-oracle` | **not extracted** | Generic eigensolver and represented-operator records are available | Finite-rank resolvent evaluation, rank-one root resolution, oracle contracts, campaign records, and independent verification remain local |
| `impurity-defect-1d-blind-alignment` | **not extracted** | Generic frame alignment exists, but it assumes supplied reference/candidate frames | Blind observation contracts, hidden-truth separation, inference policy, noise/gauge/stopping studies, inference Action, and campaign verification remain local |
| `impurity-defect-1d-continuum-refinement` | **not extracted** | Generic quantities, operator differences, spectra, and comparison primitives exist | Continuum refinement records, independent assembly/reconstruction, state comparison, refinement Workflow, serializer, and verifier remain local |
| `impurity-spin-spaces` | **not extracted** | Generic represented operators exist | Spin basis/frame records, spin rotations, embeddings, compatibility/difference Actions, campaign serialization, and verification remain local |
| `impurity-defect-2d` | **partially extracted** | Public 1D/2D/3D lattice contracts, twists, sparse operators, gauge bridges, route reconciliation, finite-domain diagnostics, and execution-free finite-domain planning exist | Historical Stage A/B/C campaign contracts and verifiers are not integrated; the proposed 2,430-case finite-domain campaign remains deliberately unexecuted |
| `periodic-1d` | **partially extracted** | Public periodic model/fiber, reciprocal mesh/sewing, frame transport/alignment, Wilson spectra/comparison, hopping transform/fit/diagnostic, localization, isolated/stress/composite schemas and retained Workflows, complete typed composite matrix/hopping/gap/gauge/range/route/identity results, independent retained isolated and composite verifiers with explicit unavailable channels and integrated verified Workflows, typed Wannier90 results, complete caller-supplied native-artifact authentication/parsing, an independent native Wilson verifier, and an integrated verified-native Workflow exist | The nonlocalization isolated-band calculation Workflow is public; composite calculation, gauge/localization calculation, an independent stress verifier, and deterministic `.win`/interface preparation remain local; historical scripts are frozen and deprecated |
| `periodic-2d` | **not extracted** | Dimension-generic quantities and some lattice/operator primitives can be reused | 2D parent models, plane-wave and real-space fibers, tensor-product checks, symmetry/degeneracy diagnostics, effective-mass tensors, non-Abelian gauge transport, topology controls, 2D hopping shells, campaign records, native comparison, and verification remain local |
| `periodic-2d-optimizer-basin` | **not extracted** | Native artifact records and generic numerical quantities are available | Basin definitions/classification, initial-gauge actions, bounded optimizer studies, continuation/resume records, censored convergence regression, archive verification, serializers, and independent reconstruction remain local |

Only the harmonic-oscillator and particle-in-box directories currently import the
public package from their non-plot historical adapters. The other ten directories have
zero public-package imports in their retained Python files. This is expected for frozen
evidence, but confirms that their campaign layers have not been replaced by versioned
public integrations.

## Appendix findings

| Appendix | Status | Finding |
|---|---|---|
| A — notation and status | **partially extracted** | Units, represented operators, frames, gauges, and evidence terminology have owners, but there is no single executable notation contract and none is required merely for prose |
| B — Hilbert–Schmidt/Frobenius geometry | **partially extracted** | Basic represented Frobenius norms and residuals exist; the planned norm family remains incomplete and its ten extraction tasks are inactive |
| C — operator spaces, compression, alignment | **partially extracted** | Operator records, orthogonal spectral subspaces, compression, compatibility, differencing, and frame alignment exist; broader downfolding and cross-representation contracts remain incomplete |
| D — particle in a box | **integrated** | Demonstrated reusable models, residual distinctions, parameter studies, campaign records, and verification are public |
| E — harmonic oscillator | **integrated** | Demonstrated ladder/spatial constructions, comparison, campaign serialization, and verification are public |
| F — bulk-silicon reduction routes | **not presently complete** | Much of the text is proposed work; generic alignment and hopping machinery exists, but no accepted silicon parent/operator evidence exists to extract |
| G — one-dimensional reduction | **partially extracted** | Reusable lower layers and native readers are public; campaign schemas, complete orchestration, `.win` preparation, and campaign verification remain outstanding |
| H — two-dimensional Wannier reduction | **not extracted** | The demonstrated 2D, topology, shell, native-study, and optimizer capabilities remain in calculation packages |
| I — impurity benchmarks | **partially extracted** | Generic defect lattice/operator machinery exists, but spin-space and four specialized defect-1D campaigns are not public integrations |
| J — two-dimensional defect extraction | **partially extracted** | Generic Stage C and finite-domain planning capabilities exist; historical Stage A/B/C campaign surfaces and future execution remain separate |
| K — envelope theory | **not presently applicable** | This is literature interpretation and proposed mathematical/scientific direction; executable contracts require accepted specifications and demonstrated calculations |
| L — candidate literature | **not presently applicable** | This is a prospective literature register, not software behavior |

## Chapter findings

Chapters 1–20 are primarily conceptual, evidentiary, architectural, proposed-method,
or proof-status prose. They should not be converted wholesale into software. Existing
public operator, provenance, Workflow, and analysis records cover portions of Chapters
2, 3, 6, 7, 10, 11, and 15. The bulk-silicon, doped-silicon, continuum, structured
learning, transferability, and most proof chapters explicitly describe proposed or
incomplete work; absence of production APIs for those claims is therefore correct.

## Conclusion

The answer is **no**: the monograph calculations are not fully extracted and integrated.
Two calculation directories are integrated, four are partially extracted, and six are
not extracted. The specialized defect-1D, spin, periodic-2D, and optimizer capabilities
still require versioned public campaign work. Appendix H is the largest demonstrated
reusable gap.

The safe migration order is:

1. complete Appendix G campaign records, serializers, interface preparation, Workflows,
   and independent verification;
2. extract the common defect-1D campaign substrate, then the independent-route,
   analytical-oracle, blind-alignment, and continuum-refinement deltas;
3. extract spin-space contracts;
4. define and implement the Appendix H 2D/topology/hopping-shell substrate;
5. extract optimizer-basin and continuation diagnostics; and
6. integrate the historical Stage A/B/C defect-2D campaign contracts without changing
   retained evidence or authorizing finite-domain execution.

Each migration should add a new versioned public surface and leave authenticated
historical runners unchanged and deprecated for new execution.
