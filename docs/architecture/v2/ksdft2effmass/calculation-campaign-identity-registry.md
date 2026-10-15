# Calculation-campaign identity registry

## Status

This document is a pre-migration identity map. It does not move, rename, rewrite, or
reclassify retained calculation evidence. Existing paths, embedded identifiers,
checksums, manifests, and checkpoint references remain authoritative for the historical
artifacts that already use them.

The registry separates durable scientific identity from publication placement. Labels
such as `research-monograph`, `ICMSEP2026`, `paper_1`, Appendix G/H, M1--M4, HSH-1, and
Stage A/B/C remain useful historical or presentation aliases, but they are not permanent
campaign-family identities.

## Identity model

The maintained, publication-independent unit is an **experiment**. A calculation
campaign may orchestrate one or more experiments, but the campaign name is not the
scientific identity retained by a paper.

A maintained experiment uses four distinct identities:

1. **Experiment-family ID** — stable, unversioned identity for one scientific question
   and method boundary. The tables below currently call this the campaign-family ID for
   compatibility with existing package language; it is the experiment identity to be
   versioned.
2. **Experiment-version ID** — the family ID followed by `.vN`. Each version freezes one
   protocol, parameter and case inventory, input and result contracts, implementation
   dependency boundary, verification contract, and interpretation boundary.
3. **Run ID** — one execution or execution-free materialization of one experiment
   version; timestamps and attempt numbers belong here, not in the family ID.
4. **Evidence-package identity** — content digests, manifests, source revisions, and the
   immutable version locator for retained artifacts.

An experiment version is immutable once it has retained evidence or is cited. A changed
scientific question, parameter inventory, method, decisive tolerance, result schema,
verification obligation, or claim boundary creates the next experiment version. A
repeat execution under the same frozen version creates a new run ID, not a new
experiment version. Editorial corrections that do not change the contract may be
recorded against the same version without rewriting its evidence package.

Publication venue, manuscript appendix, milestone number, human checkpoint, evidence
status, and filesystem location are metadata. They must not be encoded as the only
scientific identity.

## Dependency direction

Computational experiments are independent research records. They must not import,
resolve, or derive identity from a paper, manuscript chapter, conference, figure number,
or publication directory.

The dependency direction is one way:

```text
experiment family
    -> immutable experiment version
        -> run and immutable evidence package
            <- cited by zero or more publications
```

A publication records which experiment version, run, evidence package, result fields,
and figures it uses. The experiment does not acquire the publication's identity in
return.
A separate reference index may answer both of these navigation questions without
coupling the records:

- which experiments support this publication; and
- which publications cite this experiment?

The reverse answer is bibliographic metadata, not campaign ownership. Removing,
renaming, splitting, or superseding a manuscript must not rename an experiment or
invalidate its provenance.

Historical packages currently located beneath `ICMSEP2026/` retain those paths and
embedded IDs as provenance aliases until consolidation. Their production successors use
publication-neutral family IDs and live outside any paper tree. Once an obsolete package
is removed from the maintained tree, its exact repository version and commit—not a
copied legacy directory—remain its durable locator.

Durable family IDs use the form

```text
ksdft2effmass.campaign.<program>.<system>.<question>
```

Reference-data and extraction records use `ksdft2effmass.reference` and
`ksdft2effmass.extraction` instead of pretending to be project calculations.

## Consolidated family map

### Foundational model-system campaigns

| Current locator or label | Permanent campaign-family ID | Scope note |
|---|---|---|
| `calculations/research-monograph/harmonic-oscillator/`; Appendix E | `ksdft2effmass.campaign.model-systems.harmonic-oscillator.common-space-comparison` | Analytical, finite-difference, and ladder-operator representations in one declared finite comparison space |
| `calculations/research-monograph/particle-in-box/`; Appendix D | `ksdft2effmass.campaign.model-systems.particle-in-box.finite-representation-diagnostics` | Residual meaning, grid and mode refinement, norm behavior, and model-class identifiability |
| `calculations/research-monograph/impurity-spin-spaces/`; Appendix I spin slice | `ksdft2effmass.campaign.operator-comparison.impurity.spin-space-compatibility` | Spinless, spin-degenerate, collinear, and spinor finite-space mappings and compatibility |

### One-dimensional periodic reduction and model adequacy

The historical `calculations/research-monograph/periodic-1d/` directory is an aggregate
suite, not one permanent production campaign. Its retained files map to the following
families.

| Current locator or label | Permanent campaign-family ID | Scope note |
|---|---|---|
| Appendix G; monograph periodic-1D nominal isolated-band files; Conference Paper 1 M1 `isolated-band/` | `ksdft2effmass.campaign.periodic-reduction.periodic1d.single-band-fourier-reduction` | Parent refinement, one retained scalar band, complete hopping transform, truncation, fitting routes, and evaluation on disjoint coordinates; the historical name does not independently establish a spectral isolation gap |
| Appendix G periodic-1D stress files | `ksdft2effmass.campaign.periodic-reduction.periodic1d.isolated-band-robustness` | Potential, band, mesh, gauge, and fitting-route adverse controls |
| Appendix G composite files; Conference Paper 1 M2 `multiband-alignment/` | `ksdft2effmass.campaign.periodic-reduction.periodic1d.composite-band-alignment-and-locality` | Composite frames, pointwise/global alignment, matrix hoppings, and gauge-dependent locality |
| Appendix G retained Wannier90 attempts | `ksdft2effmass.campaign.periodic-reduction.periodic1d.wannier90-localization-comparison` | Bounded attempt history, preconditioning, localization, and independently retained comparison diagnostics |
| Conference Paper 1 parent `paper_1/` direct calculation | `ksdft2effmass.campaign.model-adequacy.periodic1d.scalar-admissible-set-demonstration` | Scalar identity-alignment quadratic sets with a common witness and exact-rational separation bound |
| Conference Paper 1 M3 `constrained-admissible-sets/` | `ksdft2effmass.campaign.model-adequacy.periodic1d.band-equivalence-versus-hopping-locality` | Historical finite-angle predecessor retained only as regression; the maintained family tests smooth band-equivalent representations using restricted-alignment matrix and hopping-locality diagnostics |
| M3 `constrained-admissible-sets-threshold-sensitivity/` | `ksdft2effmass.campaign.model-adequacy.periodic1d.admissible-set-threshold-sensitivity` | Explicitly post-hoc sensitivity of the sealed M3 quadratics; separate from the confirmatory family |

Historical aliases `M1`, `M2`, and `M3` describe a publication sequence. They may appear
in provenance and prose, but maintained APIs and future runs should use the permanent
family IDs.

### Two-dimensional periodic reduction and model adequacy

The historical `calculations/research-monograph/periodic-2d/` directory is also an
aggregate suite. Production campaigns should not reproduce that colocation as one
contract.

| Current locator or label | Permanent campaign-family ID | Scope note |
|---|---|---|
| Appendix H scalar files | `ksdft2effmass.campaign.periodic-reduction.periodic2d.scalar-band-reduction` | Separable/coupled parent refinement, scalar band reduction, hopping shells, and effective-mass diagnostics |
| Appendix H composite files | `ksdft2effmass.campaign.periodic-reduction.periodic2d.composite-band-gauge-and-locality` | Rank-three projected gauges, non-Abelian loops, finite-supercell spread, and block locality |
| Appendix H topological files | `ksdft2effmass.campaign.periodic-reduction.periodic2d.topological-obstruction-controls` | QWZ, Hofstadter, and Haldane topological and trivial controls |
| Appendix H topological phase-sweep files | `ksdft2effmass.campaign.periodic-reduction.periodic2d.topological-phase-boundaries` | Analytic and sampled phase-boundary checks; separate from the fixed-control campaign |
| Appendix H balanced Wannier90 files | `ksdft2effmass.campaign.periodic-reduction.periodic2d.wannier90-localization-comparison` | Balanced embedding and direct-versus-native localization comparison |
| Appendix H six-case Wannier90 study | `ksdft2effmass.campaign.periodic-reduction.periodic2d.wannier90-parameter-sensitivity` | Bounded mesh, cutoff, and inactive-embedding sensitivity; no convergence claim |
| `periodic-2d-optimizer-basin/` initial study | `ksdft2effmass.campaign.periodic-reduction.periodic2d.wannier90-optimizer-basin` | Multi-start endpoint and basin sensitivity for the original bounded study |
| `periodic-2d-optimizer-basin/` standalone expansion and continuations | `ksdft2effmass.campaign.periodic-reduction.periodic2d.wannier90-multistart-convergence` | Fixed-embedding multi-start and exact-checkpoint continuation study |
| standalone censored regression | `ksdft2effmass.campaign.periodic-reduction.periodic2d.wannier90-convergence-regression` | Post-hoc right-censored convergence-iteration analysis; separate analysis family |
| Conference Paper 1 draft M4 `two-dimensional-common-space/` | `ksdft2effmass.campaign.representation-comparison.periodic2d.common-finite-space` | Plane-wave and finite-difference representations transported to one declared finite comparison space |
| Conference Paper 1 draft HSH-1 `hopping-shell-hierarchy/` | `ksdft2effmass.campaign.model-adequacy.periodic2d.hopping-shell-hierarchy` | Nested two-dimensional hopping-shell adequacy and certificate plan |

Historical aliases `Appendix H`, `M4`, and `HSH-1` remain publication or planning
labels, not production identities.

### Dimensionality and anisotropy model-adequacy progression

| Sequence role and current locator | Permanent campaign-family ID | Scope note |
|---|---|---|
| Isotropic 2-D; `docs/tasks/dev/experiments/isotropic2d/`; historical HSH-1 | `ksdft2effmass.campaign.model-adequacy.periodic2d.hopping-shell-hierarchy` | Existing square-symmetric retained scalar target; first stage and already listed in the periodic-2D table above |
| Isotropic 3-D; `docs/tasks/dev/experiments/isotropic3d/` | `ksdft2effmass.campaign.model-adequacy.periodic3d.isotropic-hopping-support-hierarchy` | Selected simple-cubic scalar control introducing the third periodic coordinate while preserving signed-permutation symmetry; protocol not frozen |
| Anisotropic 2-D; task not yet opened | `ksdft2effmass.campaign.model-adequacy.periodic2d.anisotropic-hopping-support-hierarchy` | Selected rectangular/sign-symmetric stress family removing axis-permutation equivalence in two dimensions; protocol not frozen |
| Anisotropic 3-D; `experiments/model-adequacy/periodic3d/anisotropic-hopping-support-hierarchy/` | `ksdft2effmass.campaign.model-adequacy.periodic3d.anisotropic-hopping-support-hierarchy` | Preserved controlled orthorhombic scalar parent and explicit anisotropic support classes; exact pre-version proposal and exploratory design note exist, with no silicon claim |

These are four independent experiment families ordered by the
[dimensionality and anisotropy ladder](../experiments/model-adequacy/dimensional-anisotropy-ladder.md),
not one version chain. Later 2-D and 3-D
[general-lattice-vector work](analysis/model_adequacy/general-lattice-vector-extension.md)
is a prospective capability-extraction phase and has no experiment-family identity
until concrete finite scientific questions and verification cases are selected.

The synthetic families are not predecessor versions of a bulk-silicon study. Any future
silicon admissible-set experiment receives a distinct family identity bound to its
material parent, represented basis, gauge, orbital/valley/spin structure, and
provenance.

### Impurity and defect campaigns

| Current locator or label | Permanent campaign-family ID | Scope note |
|---|---|---|
| `impurity-defect-1d/` | `ksdft2effmass.campaign.defect-extraction.periodic1d.matched-pristine-defect` | Matched pristine/defect construction with planted coordinate and energy-reference controls |
| `impurity-defect-1d-independent-route/` | `ksdft2effmass.campaign.defect-extraction.periodic1d.route-reconciliation` | Direct real-space and independently assembled Bloch-fiber routes |
| `impurity-defect-1d-blind-alignment/` | `ksdft2effmass.campaign.defect-extraction.periodic1d.blind-alignment` | Inference without access to authored alignment truth, followed by evaluation |
| `impurity-defect-1d-analytical-oracle/` | `ksdft2effmass.campaign.defect-extraction.periodic1d.finite-rank-resolvent-oracle` | Finite-rank Bloch-resolvent oracle and independent site-space eigensolve |
| `impurity-defect-1d-continuum-refinement/` | `ksdft2effmass.campaign.defect-reduction.periodic1d.continuum-refinement` | Separate continuum mesh/domain and lattice supercell/scale/defect-width axes |

The historical `impurity-defect-2d/` directory is a staged suite. Stage letters are
retained aliases, while permanent identities describe the question.

| Historical stage label | Permanent campaign-family ID | Scope note |
|---|---|---|
| Stage A, `A_null_and_folding` | `ksdft2effmass.campaign.defect-extraction.periodic2d.null-and-folding-compatibility` | Null defect, folding, seams, Hermiticity, and represented-space compatibility |
| Stage B, `B_scalar_onsite_and_D4` | `ksdft2effmass.campaign.defect-extraction.periodic2d.scalar-onsite-alignment-and-covariance` | Scalar onsite extraction, known/blind maps, route bridges, schedule order, and D4 covariance |
| Stage C, `C_directional_and_nonlocal_model_classes` | `ksdft2effmass.campaign.defect-reduction.periodic2d.directional-and-nonlocal-model-hierarchy` | Directional/nonlocal plants, nested model classes, locality, symmetry, and accepted-parent adaptation |
| Proposed Stage D, `D_area_shape_and_boundary_phase` | `ksdft2effmass.campaign.defect-extraction.periodic2d.finite-domain-and-boundary-phase-refinement` | Area, shape, and boundary-phase effects; not completed merely by naming it |
| Proposed Stage E, `E_composite_degeneracy_and_coupled_parent` | `ksdft2effmass.campaign.defect-extraction.periodic2d.composite-degeneracy-and-coupled-parent` | Composite retained spaces, degeneracy, and coupled-parent controls; not completed merely by naming it |

Checkpoint labels `HCxx` record human decisions and execution authority. They are never
campaign IDs.

### Bulk-silicon records

| Current locator or label | Permanent identity | Record kind |
|---|---|---|
| `bulk-silicon/materials-project/` | `ksdft2effmass.reference.bulk-silicon.crystal-structure.materials-project-mp-149` | External reference data, not a project campaign |
| `qe-example01-si-scf-davidson/` | `ksdft2effmass.campaign.bulk-silicon.quantum-espresso.tutorial-scf-davidson` | Tutorial reproduction |
| `qe-example01-si-bands-davidson/` | `ksdft2effmass.campaign.bulk-silicon.quantum-espresso.tutorial-band-path-davidson` | Tutorial band-path calculation |
| `qe-7.5-si-scf-smoke-comparison/` | `ksdft2effmass.campaign.bulk-silicon.quantum-espresso.scf-smoke-version-comparison` | Bounded comparison of tutorial records |
| `production-convergence-preflight/` | `ksdft2effmass.campaign.bulk-silicon.quantum-espresso.cutoff-and-kmesh-convergence-preflight` | Provisional finite-setting study; the word `production` does not imply accepted production settings |
| `docs/computational/Si-bulk/wannier-component-locality/` | `ksdft2effmass.campaign.bulk-silicon.si-vc.wannier-component-locality` | Proposed, unexecuted computational campaign; no immutable version, retained run, or evidence package exists |
| Conference preview `silicon-wannier-kinetic-preview/` | `ksdft2effmass.extraction.bulk-silicon.wannier90.kinetic-hopping-preview` | Read-only publication extraction, not a production calculation |

## Historical aliases that must remain searchable

The identity registry must preserve at least these aliases in a future machine-readable
map:

- current repository-relative path;
- embedded `calculation_id`, `analysis_id`, `study_id`, and schema identifiers;
- publication labels such as M1--M4, HSH-1, Appendix D/E/G/H/I/J, and Paper 1;
- accepted checkpoint IDs and execution-authorization IDs;
- source Git commit and blob identities where already recorded; and
- package and artifact SHA-256 identities.

Existing retained JSON and checksum catalogs must not be edited merely to replace an
old label with a new family ID. The permanent identity is added by the maintained
registry and by future production protocols.

## Source and experiment boundary

A parameterized calculation is not thereby a reusable library Workflow. Concrete
experiment composition belongs outside `python/src/`, including frozen model and case
selection, protocol controls, experiment-specific result schemas and serializers,
independent evidence verification, figures, reports, manifests, and retained outputs.
Reusable model construction, transforms, fitting kernels, and diagnostics remain in
the installed packages.

The publication-independent experiment at
`experiments/periodic-reduction/single-band-fourier-reduction/periodic1d/` is the first
maintained implementation of this boundary. It consumes the model-independent
single-band reduction Workflow in `python/src/` rather than retaining a second
producer transform, truncation, fitting, or diagnostic implementation. The Workflow
accepts prepared objective-construction and evaluation samples, caller-supplied fitting
weights and ranges, publication-independent result semantics, and no experiment identity
or frozen evidence policy.

Immutable version
`ksdft2effmass.campaign.periodic-reduction.periodic1d.single-band-fourier-reduction.v1`
now has retained run `...v1.run-20261014T184707Z` and evidence package
`sha256:6e8d5db988df97d4b8cf7843b3baceb16e2eb70d2b03c729497a82251fca6377`.
Version-bound strict schemas, direct-formula independent verification, exact dirty-source
and dependency provenance, and historical parity are retained. Historical M1 evidence
remains outside this implementation, unchanged; successor provenance points to exact
revision `9a65849d886d5be499b2664e2b653c3983fab06e`, path
`calculations/ICMSEP2026/conference/paper_1/isolated-band/`, Git tree
`418999a90efa3001d2e50a2e7912f126bc30903f`, and predecessor file digests.

The composite-band alignment and locality family has a completed owner-boundary review.
Its maintained migration preserves backend-qualified eigenvector-diagonal frames,
rejects rank-deficient pointwise and aggregate Procrustes inputs, and tracks the current
local numerical selection mechanisms as `TECH_DEBT`. That decision does not silently
move all current `periodic1d` or `campaigns` code. **Band Equivalence versus Hopping
Locality**, under
`experiments/model-adequacy/periodic1d/band-equivalence-versus-hopping-locality/`, is an active,
unversioned smooth-continuum redesign. It uses exact continuous harmonic alignment,
separates finite-mesh correlation from the analytic Bessel comparator, retains Fourier
locality diagnostics, and classifies nested-mesh stability as `converged` or
`unresolved`. The former draft `.v0` was retired without assignment. Historical 64/257
behavior is isolated as a regression fixture with exact source-evidence locators and
cannot determine maintained scientific controls. No maintained run or evidence-package
identity exists yet.

## Maintained layout and version retention

The maintained tree contains publication-independent experiment and reference material
outside the installed source tree. Periodic-reduction experiments use a family-first,
dimension-second layout:

```text
experiments/
├── periodic-reduction/
│   ├── single-band-fourier-reduction/
│   │   └── periodic1d/
│   └── composite-band-alignment-and-locality/
│       └── periodic1d/
├── model-adequacy/
│   ├── periodic1d/band-equivalence-versus-hopping-locality/
│   ├── periodic2d/hopping-shell-hierarchy/
│   └── periodic3d/anisotropic-hopping-support-hierarchy/
└── README.md
```

The organizational family directories do not erase the dimension from stable experiment
identities. Dimensional children and future domains such as `defect-extraction/` are
added only after their own maintained contracts exist; no empty placeholders are
maintained. Literature PDFs or other local reference caches are not experiment-family
roots.

The present `calculations/` paths remain historical locators until every migration gate
below passes. `experiments/` must not become an uncorrelated duplicate tree: a successor
is admitted only with an explicit alias, version, run, evidence, and replacement
relation to every prior maintained path.

There is no `legacy/`, `historical/`, or publication-specific experiment store in the
maintained tree. Git history is the legacy store. When an exploratory or superseded
package leaves the current tree, the alias registry records:

- the last repository version containing it;
- the exact commit and tree or blob identities;
- its repository-relative path at that version;
- package and artifact SHA-256 identities; and
- its replacement or disposition, if any.

A signed semantic-version tag is the preferred durable locator for a reviewed or
publication-facing snapshot. An exact commit may locate provisional development
material, but it must not be misrepresented as a reviewed release. Removing a package
from the current tree does not rewrite the version that contained it.

Aggregate exploratory suites therefore do not need to be copied into a historical
folder. Their exact former trees remain reachable at the mapped version, while current
production successors may become several independent campaigns.

Publication-side references should live under the publication owner, for example as a
small manifest containing experiment-family ID, experiment-version ID, run ID,
repository version and commit, evidence-package digest, consumed result fields, and
presentation artifacts. The experiment tree must not contain paper-specific copies of a
maintained experiment.

## Migration gates

Before removing or replacing any obsolete package in the maintained tree:

1. review and freeze the family map;
2. create a machine-readable alias registry;
3. inventory every path reference, checksum contract, checkpoint binding, external
   native-root reference, documentation link, and test fixture;
4. identify the exact existing version and commit that permanently retain the old path;
5. record the old path, Git object identity, byte size, SHA-256, and replacement or
   disposition;
6. ensure publication manifests resolve experiments by family, protocol, run, version,
   and evidence digest rather than by a mutable working-tree path;
7. remove obsolete copies only from the new tip, without rewriting the containing
   version or Git history;
8. update live navigation and production adapters separately from version-pinned old
   manifests;
9. replace paper-directory ownership of maintained calculations with publication-side
   references to independent experiment identities; and
10. verify that no publication claim, evidence status, checksum meaning, or execution
    authority changed as a side effect of consolidation.

The production rewrite starts only after these identity and provenance gates are
satisfied.
