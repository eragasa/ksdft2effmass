# Experiments

This tree is the maintained destination for publication-independent numerical
experiments. An experiment selects models, cases, sample roles, thresholds, metrics,
protocols, executable composition, interpretation boundaries, schemas, independent
verification, and retained evidence while consuming reusable capabilities from
installed owner libraries. New maintained experiment execution must not be added under
publication-specific `calculations/` paths; those paths remain historical evidence and
design donors. Architecture mirrors
this source hierarchy under `docs/architecture/v2/experiments/`; every selected package,
subpackage, module, and public class uses `index.md`, `science.md`, `numerics.md`,
`implementation.md`, and `schematics.md`, with detail concentrated toward the
implementing `ClassName`.

Within `periodic-reduction/`, reusable scientific experiment families are grouped first
and dimensional realizations (`periodic1d/`, later `periodic2d/` or `periodic3d/`) are
children. A family container is organizational; each dimensional child retains its own
stable experiment-family identity. Empty dimensional placeholders are not created.

Experiment code is not part of the public `ksdft2effmass` wheel. Installed packages
must never import this tree. Reusable behavior is extracted into its domain owner and
consumed from the experiment; experiment-specific behavior is not promoted merely
because it is parameterized.

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

This index covers every family with a maintained directory in this tree and every
architecture-selected family whose source directory intentionally does not yet exist.
Historical packages under `calculations/` remain evidence or design donors and are not
duplicated here.

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
| `ksdft2effmass.campaign.periodic-reduction.periodic1d.single-band-fourier-reduction` | [`periodic-reduction/single-band-fourier-reduction/periodic1d/`](periodic-reduction/single-band-fourier-reduction/periodic1d/) | **Retained version** | Immutable `.v1`, strict schemas, independent reconstruction, exact predecessor provenance, retained runs, and content-addressed evidence exist. This is controlled synthetic evidence, not material validation. |
| `ksdft2effmass.campaign.periodic-reduction.periodic1d.composite-band-alignment-and-locality` | [`periodic-reduction/composite-band-alignment-and-locality/periodic1d/`](periodic-reduction/composite-band-alignment-and-locality/periodic1d/) | **Prospective protocol** | The rank-two alignment/locality successor and owner boundary are documented; no immutable version or maintained run exists. |
| `ksdft2effmass.campaign.model-adequacy.periodic1d.band-equivalence-versus-hopping-locality` (**Band Equivalence versus Hopping Locality**) | [`model-adequacy/periodic1d/band-equivalence-versus-hopping-locality/`](model-adequacy/periodic1d/band-equivalence-versus-hopping-locality/) | **Pre-version implementation** | Tests whether identical Bloch bands can conceal restricted-alignment matrix mismatch and different hopping locality. The smooth flat-parent analysis finds roundoff-level momentum refinement changes and increasing matrix/hopping mismatch, but the proposed amplitude ladder through $N_a=64$ fails a $10^{-8}$ uniform linear-interpolation target. A non-flat four-state realization using the same smooth family is prospective; historical 64/257 behavior is regression-only. No retained run or evidence-package identity exists. |
| `ksdft2effmass.campaign.model-adequacy.periodic2d.band-equivalence-versus-hopping-locality` | [`model-adequacy/periodic2d/band-equivalence-versus-hopping-locality/`](model-adequacy/periodic2d/band-equivalence-versus-hopping-locality/) | **Protocol plus bounded development refinement** | Orthogonal directed-hopping square extension with completed, independently verified `16 x 16`, `32 x 32`, and `64 x 64` local development calculations. Replaceable numerical artifacts are not retained in this source tranche. Full convergence, final retained schemas and tolerances, and retained evidence remain open. |
| `ksdft2effmass.campaign.model-adequacy.periodic2d-nonorthogonal.band-equivalence-versus-hopping-locality` | [`model-adequacy/periodic2d_nonorthog/band-equivalence-versus-hopping-locality/`](model-adequacy/periodic2d_nonorthog/band-equivalence-versus-hopping-locality/) | **Protocol plus bounded development refinement** | Graphene-inspired synthetic target and matched Bravais controls with completed, verified `16 x 16`, `32 x 32`, and `64 x 64` local development calculations; one pointwise shell decision changed on the first refinement. Replaceable numerical artifacts are not retained here. No graphene parametrization, convergence result, or retained evidence exists. |
| `ksdft2effmass.campaign.model-adequacy.periodic3d.band-equivalence-versus-hopping-locality` | [`model-adequacy/periodic3d/band-equivalence-versus-hopping-locality/`](model-adequacy/periodic3d/band-equivalence-versus-hopping-locality/) | **Protocol plus bounded development refinement** | Orthogonal directed-hopping simple-cubic extension with completed, independently verified `8 x 8 x 8`, `16 x 16 x 16`, and `32 x 32 x 32` local development calculations. Replaceable numerical artifacts are not retained here. Full convergence and retained evidence remain open. |
| `ksdft2effmass.campaign.model-adequacy.periodic3d-nonorthogonal.band-equivalence-versus-hopping-locality` | [`model-adequacy/periodic3d_nonorthog/band-equivalence-versus-hopping-locality/`](model-adequacy/periodic3d_nonorthog/band-equivalence-versus-hopping-locality/) | **Protocol plus bounded development refinement** | Silicon-inspired synthetic target and matched Bravais controls with completed, verified `8 x 8 x 8`, `16 x 16 x 16`, and `32 x 32 x 32` local development calculations. Replaceable numerical artifacts are not retained here. No silicon parametrization, convergence result, or retained evidence exists. |
| `ksdft2effmass.campaign.model-adequacy.periodic2d.gauge-locality-under-synthetic-strain` | [`model-adequacy/periodic2d/gauge-locality-under-synthetic-strain/`](model-adequacy/periodic2d/gauge-locality-under-synthetic-strain/) | **Protocol plus bounded M0/M1/M2 development** | Frozen flat-parent M0 plus separately labeled frozen four-state M1 and fixed radial-response M2 controls along a unit-area triangular-to-square-metric rhombic path. M2 produces a nonzero synthetic aligned perturbation; no convergence or material-strain claim exists. |
| `ksdft2effmass.campaign.model-adequacy.periodic3d.gauge-locality-under-synthetic-strain` | [`model-adequacy/periodic3d/gauge-locality-under-synthetic-strain/`](model-adequacy/periodic3d/gauge-locality-under-synthetic-strain/) | **Protocol plus bounded M0/M1/M2 development** | Frozen flat-parent M0 plus separately labeled frozen four-state M1 and fixed radial-response M2 controls along a unit-volume FCC-to-BCC Bain path, with a software-verified common-cell map. No convergence, material transition, or silicon claim exists. |
| `ksdft2effmass.campaign.model-adequacy.periodic2d.hopping-shell-hierarchy` | [`model-adequacy/periodic2d/hopping-shell-hierarchy/`](model-adequacy/periodic2d/hopping-shell-hierarchy/) | **Prospective protocol** | Parent binding, orbit/support inventory, sample roles, weights, thresholds, resolution, and flat package structure are selected. Conservative certificate methods, schemas, implementation, and retained evidence remain open. |
| `ksdft2effmass.campaign.model-adequacy.periodic3d.isotropic-hopping-support-hierarchy` | Intended `model-adequacy/periodic3d/isotropic-hopping-support-hierarchy/`; [architecture](../docs/architecture/v2/experiments/model-adequacy/periodic3d/isotropic-hopping-support-hierarchy/index.md) | **Architecture only** | The dimensional role and ownership boundary are selected; no exact parent protocol, source directory, immutable version, or result exists. |
| `ksdft2effmass.campaign.model-adequacy.periodic2d.anisotropic-hopping-support-hierarchy` | Intended `model-adequacy/periodic2d/anisotropic-hopping-support-hierarchy/`; [architecture](../docs/architecture/v2/experiments/model-adequacy/periodic2d/anisotropic-hopping-support-hierarchy/index.md) | **Architecture only** | The anisotropy-isolation role is selected; no exact protocol, task, source directory, immutable version, or result exists. |
| `ksdft2effmass.campaign.model-adequacy.periodic3d.anisotropic-hopping-support-hierarchy` | [`model-adequacy/periodic3d/anisotropic-hopping-support-hierarchy/`](model-adequacy/periodic3d/anisotropic-hopping-support-hierarchy/) | **Preserved proposal** | An exact orthorhombic pre-version proposal and disclosed exploratory threshold design exist. No implementation, schema, verifier, immutable version, retained run, or scientific result exists. |

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
uncertainty quantification, or publication evidence.
