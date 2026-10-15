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

### One-dimensional periodic reduction

The historical `calculations/research-monograph/periodic-1d/` directory is an aggregate
suite, not one permanent production campaign. Its retained files map to the following
families.

| Current locator or label | Permanent campaign-family ID | Scope note |
|---|---|---|
| Appendix G; monograph periodic-1D nominal isolated-band files; Conference Paper 1 M1 `isolated-band/` | `ksdft2effmass.campaign.periodic-reduction.periodic1d.single-band-fourier-reduction` | Parent refinement, one retained scalar band, complete hopping transform, truncation, fitting routes, and evaluation on disjoint coordinates; the historical name does not independently establish a spectral isolation gap |
| Appendix G periodic-1D stress files | `ksdft2effmass.campaign.periodic-reduction.periodic1d.isolated-band-robustness` | Potential, band, mesh, gauge, and fitting-route adverse controls |
| Appendix G composite files; Conference Paper 1 M2 `multiband-alignment/` | `ksdft2effmass.campaign.periodic-reduction.periodic1d.composite-band-alignment-and-locality` | Composite frames, pointwise/global alignment, matrix hoppings, and gauge-dependent locality |
| Appendix G retained Wannier90 attempts | `ksdft2effmass.campaign.periodic-reduction.periodic1d.wannier90-localization-comparison` | Bounded attempt history, preconditioning, localization, and independently retained comparison diagnostics |

Historical aliases `M1` and `M2` describe a publication sequence. They may appear
in provenance and prose, but maintained APIs and future runs should use the permanent
family IDs.

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
accepts prepared training and evaluation samples, caller-supplied fitting weights and
ranges, publication-independent result semantics, and no experiment identity or frozen
evidence policy.

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
move all current `periodic1d` or `campaigns` code..

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
└── README.md
```

The organizational family directories do not erase the dimension from stable experiment
identities. Two- and three-dimensional children are added only after their own contracts
exist; no empty dimensional placeholders are maintained.

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
