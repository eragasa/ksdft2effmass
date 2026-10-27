# Experiments

This tree is a transitional migration source for cross-model and model-adequacy
numerical experiments. Every tracked file here is assigned to a distributed maintained
owner under `calculations/`; no new maintained experiment execution or protocol should
be added here. The repository-level mapping is recorded in
[`calculations/README.md`](../calculations/README.md), while each calculation owner keeps
its complete local inventory in `README.md` and actionable checklist in `migration.md`.

An experiment selects models, cases, sample roles, thresholds, metrics, protocols,
executable composition, interpretation boundaries, schemas, independent verification,
and retained evidence while consuming reusable capabilities from installed owner
libraries. Importable definitions, calculations, result records, schemas,
serialization, and verification belong under `python/src/ksdft2effmass/`. Calculation
roots retain protocols, explicit parameter selections, thin executable or plotting
entry points, and lifecycle-appropriate outputs. New or mutable calculations do not host
a second installable implementation package; immutable executions may preserve
hash-bound source and lock bytes as retained evidence.

Within the transitional `periodic-reduction/` tree, reusable scientific experiment
families are grouped first and dimensional realizations are children. Migration
preserves each stable family identity while moving the family/container documents to
their calculation-side owners. Empty implementation placeholders are not created, but a
calculation-side README and checklist may exist to own an explicit migration inventory.

Experiment code is not part of the public `ksdft2effmass` wheel. Installed packages
must never import this tree. Reusable behavior is extracted into its domain owner and
consumed from the experiment; experiment-specific behavior is not promoted merely
because it is parameterized. Executable composition roots follow the
[experiment script conventions](script-conventions.md); those mechanical conventions do
not transfer scientific controls or evidence status between families.

Every retained experiment must distinguish:

- stable experiment-family identity;
- immutable experiment-version identity;
- run identity;
- evidence-package identity and digests; and
- publication-side references.

Publication, conference, appendix, milestone, and historical stage labels are aliases,
not maintained experiment identities. Superseded material remains locatable through
exact Git versions and commits rather than duplicate `legacy/` or `historical/`
directories.

## Numerical-experiment index

This index covers every family currently represented in this transitional tree and
every architecture-selected family whose source directory intentionally does not yet
exist. Its lifecycle descriptions remain source material until their calculation-side
copies are reviewed. Historical packages remain evidence or design donors and are not
silently rewritten during migration.

Lifecycle status has the following bounded meaning:

- **Retained version** — an immutable experiment version and retained evidence package
  exist.
- **Immutable version, unexecuted** — a parity-reviewed version, protocol, schemas, and
  evidence policy exist, but no retained run or evidence-package identity exists.
- **Pre-version implementation** — typed experiment code and tests exist, but the
  remaining protocol, schema, or evidence gates block an immutable version.
- **Prospective protocol** — scientific controls or package structure are being designed;
  no complete implementation or immutable version exists.
- **Architecture only** — the family boundary is selected, but no exact protocol or
  source directory exists.
- **Preserved proposal** — exact advance design work is retained out of sequence and
  cannot advance to implementation until earlier stages close.

The periodic-1D **Band Equivalence versus Hopping Locality** experiment tests, in plain
terms, whether two
Hamiltonian representations can have identical Bloch bands while having different
operator errors and different real-space hopping ranges.

| Experiment family | Maintained locator | Lifecycle status | Current evidence boundary |
|---|---|---|---|
| `ksdft2effmass.campaign.periodic-reduction.periodic1d.single-band-fourier-reduction` | [`calculations/mathieu1d/`](../calculations/mathieu1d/) | **Migrated retained version** | The historical experiment donor was removed after exact-manifest review. Immutable `.v1`, strict schemas, independent reconstruction, exact predecessor provenance, retained runs, and content-addressed evidence remain with the calculation owner. This is controlled synthetic evidence, not material validation. |
| `ksdft2effmass.campaign.periodic-reduction.periodic1d.composite-band-alignment-and-locality` | [`calculations/periodic1d/rank2/composite-band-alignment-locality/`](../calculations/periodic1d/rank2/composite-band-alignment-locality/) | **Migrated prospective protocol** | All three experiment-tree files now reside with the calculation owner; no immutable version or maintained run exists. |
| `ksdft2effmass.campaign.periodic-reduction.periodic1d.higher-rank-composite-band-alignment-and-locality` | [`calculations/periodic1d/rankN/composite-band-alignment-locality/`](../calculations/periodic1d/rankN/composite-band-alignment-locality/) | **Planned one-dimensional higher-rank study** | The plan fixes a one-dimensional synthetic model with a nonmoving retained subspace, real basis rotations, four retained-state counts, four rotation depths, and four alignment choices. Development code exists, but no stable result format, independent full-result check, retained run, or evidence package exists. Two- and three-dimensional variants remain separate future work. |
| `ksdft2effmass.campaign.model-adequacy.periodic1d.band-equivalence-versus-hopping-locality` (**Band Equivalence versus Hopping Locality**) | [`calculations/periodic1d/rank2/band-equivalence-versus-hopping-locality/`](../calculations/periodic1d/rank2/band-equivalence-versus-hopping-locality/) | **Calculation-owned development family** | The protocol, implementation, development artifacts, migration manifests, and channel inventory reside under `calculations/`; the 35-file experiment donor was removed after explicit authorization and remains Git-recoverable. The flat amplitude rule is direct, the nonflat claim is pointwise, adaptive refinement is reserved for a future claim, and no retained run or evidence-package identity exists. |
| `ksdft2effmass.campaign.model-adequacy.periodic2d.band-equivalence-versus-hopping-locality` | [`model-adequacy/periodic2d/band-equivalence-versus-hopping-locality/`](model-adequacy/periodic2d/band-equivalence-versus-hopping-locality/) | **Protocol plus bounded development refinement** | Orthogonal directed-hopping square extension with completed, independently verified `16 x 16`, `32 x 32`, and `64 x 64` local development calculations. Replaceable numerical artifacts are not retained in this source tranche. Full convergence, final retained schemas and tolerances, and retained evidence remain open. |
| `ksdft2effmass.campaign.model-adequacy.periodic2d-nonorthogonal.band-equivalence-versus-hopping-locality` | [`model-adequacy/periodic2d_nonorthog/band-equivalence-versus-hopping-locality/`](model-adequacy/periodic2d_nonorthog/band-equivalence-versus-hopping-locality/) | **Protocol plus bounded development refinement** | Graphene-inspired synthetic target and matched Bravais controls with completed, verified `16 x 16`, `32 x 32`, and `64 x 64` local development calculations; one pointwise shell decision changed on the first refinement. Replaceable numerical artifacts are not retained here. No graphene parametrization, convergence result, or retained evidence exists. |
| `ksdft2effmass.campaign.model-adequacy.periodic3d.band-equivalence-versus-hopping-locality` | [`model-adequacy/periodic3d/band-equivalence-versus-hopping-locality/`](model-adequacy/periodic3d/band-equivalence-versus-hopping-locality/) | **Protocol plus bounded development refinement** | Orthogonal directed-hopping simple-cubic extension with completed, independently verified `8 x 8 x 8`, `16 x 16 x 16`, and `32 x 32 x 32` local development calculations. Replaceable numerical artifacts are not retained here. Full convergence and retained evidence remain open. |
| `ksdft2effmass.campaign.model-adequacy.periodic3d-nonorthogonal.band-equivalence-versus-hopping-locality` | [`model-adequacy/periodic3d_nonorthog/band-equivalence-versus-hopping-locality/`](model-adequacy/periodic3d_nonorthog/band-equivalence-versus-hopping-locality/) | **Protocol plus bounded development refinement** | Silicon-inspired synthetic target and matched Bravais controls with completed, verified `8 x 8 x 8`, `16 x 16 x 16`, and `32 x 32 x 32` local development calculations. Replaceable numerical artifacts are not retained here. No silicon parametrization, convergence result, or retained evidence exists. |
| `ksdft2effmass.campaign.model-adequacy.periodic2d.gauge-locality-under-synthetic-strain` | [`model-adequacy/periodic2d/gauge-locality-under-synthetic-strain/`](model-adequacy/periodic2d/gauge-locality-under-synthetic-strain/) | **Protocol plus bounded M0/M1/M2 development** | Frozen flat-parent M0 plus separately labeled frozen four-state M1 and fixed radial-response M2 controls along a unit-area triangular-to-square-metric rhombic path. M2 produces a nonzero synthetic aligned perturbation; no convergence or material-strain claim exists. |
| `ksdft2effmass.campaign.model-adequacy.periodic3d.gauge-locality-under-synthetic-strain` | [`model-adequacy/periodic3d/gauge-locality-under-synthetic-strain/`](model-adequacy/periodic3d/gauge-locality-under-synthetic-strain/) | **Protocol plus bounded M0/M1/M2 development** | Frozen flat-parent M0 plus separately labeled frozen four-state M1 and fixed radial-response M2 controls along a unit-volume FCC-to-BCC Bain path, with a software-verified common-cell map. No convergence, material transition, or silicon claim exists. |
| `ksdft2effmass.campaign.model-adequacy.periodic2d.hopping-shell-hierarchy` | [`calculations/periodic2d/rank1/hopping-shell-hierarchy/`](../calculations/periodic2d/rank1/hopping-shell-hierarchy/) | **Migrated prospective protocol** | All seven experiment-tree design files now reside with the calculation owner. Conservative certificate methods, schemas, implementation, and retained evidence remain open. |
| `ksdft2effmass.campaign.model-adequacy.periodic3d.isotropic-hopping-support-hierarchy` | No maintained source directory | **Architecture only** | The dimensional role and ownership boundary are selected; no exact parent protocol, source directory, immutable version, or result exists. |
| `ksdft2effmass.campaign.model-adequacy.periodic2d.anisotropic-hopping-support-hierarchy` | No maintained source directory | **Architecture only** | The anisotropy-isolation role is selected; no exact protocol, task, source directory, immutable version, or result exists. |
| `ksdft2effmass.campaign.model-adequacy.periodic3d.anisotropic-hopping-support-hierarchy` | [`calculations/periodic3d/rank1/anisotropic-hopping-support-hierarchy/`](../calculations/periodic3d/rank1/anisotropic-hopping-support-hierarchy/) | **Migrated preserved proposal** | All three experiment-tree files now reside with the calculation owner. No implementation, schema, verifier, immutable version, retained run, or scientific result exists. |

Publication use is recorded separately in the
[experiment-to-paper allocation](../docs/publications/papers/experiment-to-paper-allocation.md).
That ledger does not alter the lifecycle status or evidence identity stated here.

## Cross-protocol development compositions

[`model-adequacy/band-equivalence-dimensional-comparison/`](model-adequacy/band-equivalence-dimensional-comparison/)
compares identically defined diagnostics from the four Paper 2 dimensional protocols.
It is a thin composition root rather than an experiment family and does not own or
transfer family-specific tolerances, convergence dispositions, runs, or evidence. Its
plots remain replaceable development outputs.

Mutable coordination for the first two sequence stages lives under
`docs/tasks/dev/experiments/isotropic2d/` and
`docs/tasks/dev/experiments/isotropic3d/`. Task paths are not experiment, run, or evidence
identities. General full-rank lattice-vector extraction remains a post-sequence
architecture direction rather than a numerical experiment.

Creating source or passing tests under this tree does not authorize protected
calculator execution and does not establish scientific validation, convergence,
uncertainty quantification, or publication evidence. After migration, exact Git history
and retained manifests preserve old experiment paths; the live tree is removed only
after every distributed checklist passes and deletion is separately authorized.
