# Nickel collinear spin-bands tutorial preflight

## Status and claim boundary

This document contains the completed metadata and dry-run preflight that governed one
subsequently authorized **calculated tutorial execution**. Human response `A` resolved
checkpoint `QE-NICKEL-SPIN-BANDS-RUN-HC01` before local pseudopotential acquisition,
input staging, or scientific execution.

The retained result is a calculated tutorial observation and software-workflow evidence
only. Nickel is outside the project's supported material scope. The Workflow does not
establish a validated nickel magnetic moment, exchange splitting, band structure,
Fermi surface, numerical convergence, scientific validation, uncertainty
quantification, or scientific acceptance.

## Tutorial source and reuse boundary

The source is the Pranab Das nickel tutorial at repository commit
`8d0087d05271beb13b240930d4643bf345541c7b`:

- <https://pranabdas.github.io/espresso/hands-on/ni/>;
- `docs/hands-on/ni.mdx`, Git blob
  `62b1f348fa23ab69f04bbea3d158975c42feb457`, 997 bytes, SHA-256
  `4fde20f90d4101978a339a2f3b0f1e0108ba3afc46ac8f1ae2e1e0aa46b66a6d`;
- `src/ni/pw_scf_ni.in`, Git blob
  `3c6d0ff7c746b4025f5634bc7100ff49333726d9`, 592 bytes, SHA-256
  `cab09f99b0151261807da49f86b15bac674be245390a511e4e5f8b90cbe95327`;
- `src/ni/pw_bands_ni.in`, Git blob
  `8077f438740e3935f67085663928c12020842489`, 769 bytes, SHA-256
  `296d4cb34d5957c444efbee8de0e8609f3c0667cbe96869943d4379d922ab794`;
- `src/ni/bands_ni_up.in`, Git blob
  `f2463fd40ca652d5161cb91103fa9acbaf271fd8`, 102 bytes, SHA-256
  `63c670acf2fa6c6bb1f147058ad035d2e27b3021abb571a4fe02051814026cb9`;
- `src/ni/bands_ni_dn.in`, Git blob
  `783ddae744c86204289563b26a6414178a08e4bf`, 102 bytes, SHA-256
  `16880df9c8ccb79c0cf94c68bb4892ef5b29ba0200ec391c6ebee87f6be5e665`.

The pinned repository's `docs/license.md`, Git blob
`0bb057148fe7ccd3c4de2efccc47be377931aa56`, declares CC BY 4.0 for the work and
excludes third-party material. The preflight reuses only identified settings and does
not commit upstream input bytes. It makes no legal conclusion about which individual
files the declaration covers. Any execution authorization is limited to local-use
operational renderings with source attribution and no redistribution.

## Pseudopotential identity and licensing boundary

The tutorial names `ni_pbe_v1.4.uspp.F.UPF`. The pinned tutorial-repository blob
`f69c05e12924e92186a7517b97ed320d5d445987` and the official GBRV URL
<https://www.physics.rutgers.edu/gbrv/ni_pbe_v1.4.uspp.F.UPF> both stream as exactly
612,014 bytes with SHA-256
`f76b86ce60cde3d83dfcc8df79ba05478db573d158289f1b226919442d977d25`.
No copy is currently retained locally.

Bounded header inspection reports a scalar-relativistic PBE ultrasoft Ni
pseudopotential with nonlinear core correction, 18 valence electrons, Vanderbilt
generator version 7.3.6, author label `kfg`, and no nonzero suggested cutoff values.
These are source metadata, not evidence of suitability or convergence.

The official [GBRV page](https://www.physics.rutgers.edu/gbrv/) identifies the library
as open source under its linked GNU General Public License version 3 text, SHA-256
`8ceb4b9ee5adedde47b31e975c1d90c73ad27b6b165a1dcd80c7c545eb65b903`.
It cites K. F. Garrity, J. W. Bennett, K. M. Rabe, and D. Vanderbilt,
*Computational Materials Science* **81**, 446 (2014), DOI
`10.1016/j.commatsci.2013.08.053`.

Checkpoint `QE-NICKEL-SPIN-BANDS-RUN-HC01` asks the human to authorize exact local
acquisition, staging, and execution under that declared license boundary. No
pseudopotential will be committed or redistributed.

## Exact scientific settings

The source describes one-atom FCC nickel with QE `ibrav=2` and
`celldm(1)=6.648` Bohr. Both `pw.x` stages retain:

- `nat=1`, `ntyp=1`, and atomic position Ni `(0,0,0)` in `alat` coordinates;
- collinear `nspin=2` and `starting_magnetization(1)=0.7`;
- `nbnd=10`, `ecutwfc=45 Ry`, and `ecutrho=360 Ry`;
- Marzari--Vanderbilt smearing with `degauss=0.01 Ry`;
- Davidson diagonalization, `conv_thr=1e-8 Ry`, and `mixing_beta=0.7`.

The SCF stage uses a shifted automatic `14x14x14` mesh with shift `(1,1,1)`. The
bands stage uses `K_POINTS crystal_b` with source-listed vertices
$\Gamma=(0,0,0)$, $L=(1/2,1/2,1/2)$, $W=(1/2,1/4,3/4)$,
$X=(1/2,0,1/2)$, $\Gamma$, and $K=(3/8,3/8,3/4)$. Its five segments request
20, 10, 10, 10, and 20 interpolated points according to QE's `crystal_b` semantics.
The actual generated point count will be observed rather than assumed.

The two `bands.x` inputs differ only in `spin_component`: 1 for the source-labeled
spin-up result and 2 for the source-labeled spin-down result. This component label is a
calculator convention; it does not define an independently rotated physical spin axis.

## Operational inputs and workspace plan

Execution, if authorized, will render four explicit operational inputs. Path-only
adaptations replace the source's shared `../pseudos` and `./tmp` locations with private
stage-local `./pseudo`, `./scratch`, and `../results` roles. The represented scientific
settings remain unchanged.

| Stage | Executable | Operational input bytes | Operational SHA-256 |
|---|---|---:|---|
| SCF | `pw.x` | 593 | `736bb614d5a5d11c5c03d5f693c401681bafd6e0a8a9cc488f32e1e515d78d2b` |
| Bands | `pw.x` | 712 | `a5b1e87bafb1f3ea7687c32ec4fa73a481fe8d6d9c996141b2f62e01acba871c` |
| Spin up | `bands.x` | 119 | `f475776e5186be9d7c83f2b96c081ce60cbc5db38853071812484415bd377508` |
| Spin down | `bands.x` | 121 | `2c98a8764090e90ae63344e2798836241a7cd404042c7ce371074d56ce52efbb` |

The preflight identity is
`qe-7.5-nickel-spin-bands-preflight-20260908T071537Z`. Its external record contains
metadata only. No source input, operational input, pseudopotential, or calculator state
is staged there.

An authorized execution will create a new external Workflow root with private
`01-scf`, `02-bands`, `03-bands-up`, and `04-bands-down` stage roots. Every stage will
have distinct inputs, streams, results, process records, and before/after snapshots.
The bands stage receives an identity-checked copy of the admitted SCF native state.
Each `bands.x` stage receives a separate identity-checked copy of the admitted bands
native state. No stage shares a mutable `outdir`.

## Executables, scale, and resource envelope

The proposed local QE 7.5 executables are:

| Executable | Bytes | SHA-256 |
|---|---:|---|
| `pw.x` | 9,673,048 | `87aa72158e2c103c63fce1deca977dc42ff4ba344519a9662aadb96d33eab910` |
| `bands.x` | 8,018,632 | `fef09fe9d9967dd432859fc6affc8f28c2acaedefc78f16409897f273488b443` |

The local machine reports 10 logical CPUs, 24 GiB memory, and approximately 105 GiB
free storage. The upstream commands request eight MPI ranks, but the proposed attempt
will instead use:

- four sequential executable invocations;
- one local process and `OMP_NUM_THREADS=1` for every stage;
- no MPI launcher, scheduler, remote, cluster, or cloud execution;
- five minutes each for SCF and bands, two minutes for each `bands.x` stage, and a
  15-minute complete-Workflow envelope;
- 1 GiB resident-memory observation boundary;
- 1 GiB total new-storage envelope; and
- no automatic retry.

The one-atom system has 18 pseudopotential valence electrons, 10 bands per collinear
spin channel, a $14^3$ SCF mesh, and a five-segment band path. The envelope is a
conservative estimate, not an observed runtime or memory result.

## Dependencies, failures, and expected outputs

The SCF result is required by the bands stage. The bands result is required by both
spin-selective postprocessors. A failed, timed-out, diagnostically incomplete, or
unadmitted predecessor leaves dependents explicitly unattempted. After a valid bands
result exists, the spin-up and spin-down postprocessors are independent siblings: both
are attempted once even if the other fails. No stage is retried without new
authorization.

A systemic identity, confinement, storage, memory-capture, stream-capture, or
snapshot-capture failure stops trustworthy further execution. Process completion,
calculator-reported SCF convergence, native-document exit state, dependency admission,
and Workflow completion remain separate facts.

Expected bounded observations include:

- SCF total energy, Fermi energy, total and absolute magnetization, convergence facts,
  and native state;
- bands-stage path coordinates, collinear spin labels, eigenvalue dimensions, and
  native state;
- separate `bands.x` process outputs and `filband`/GNU-format artifacts for component 1
  and component 2; and
- executable, input, pseudopotential, stream, snapshot, native-state, and admitted-copy
  identities plus timing and sampled resource observations.

Raw streams, charge density, wavefunctions, QEXSD trees, and dense native files will
remain external and uncommitted. Any compact observation will be proposed for
repository retention only after result review.

## Recorded execution outcome

The authorized external run
`qe-7.5-nickel-spin-bands-20260908T091550Z` attempted every stage exactly once. All
four processes returned zero, contained `JOB DONE.`, stayed within the 1-GiB sampled
resident-memory and storage envelopes, and completed in approximately 30.8 seconds in
total. The three native-state admissions agreed by content identity. The SCF process
reported convergence in 13 iterations; QEXSD reported 280 irreducible SCF k points,
71 band-path points, and 10 bands per collinear spin component. Both spin-selective
`bands.x` artifacts agreed with the corresponding QEXSD eigenvalues within the
postprocessor's 0.001-eV printed precision.

Every stderr stream contains the same 139-byte floating-point exception note. It is
retained and remains uncharacterized rather than being classified as harmless or
fatal.

The compact calculated observation is retained at
`examples/tutorials/nickel-spin-bands/qe/expected/qe75-calculated-observation.json`,
SHA-256 `4ab87fc9b88ca3feafc7ee6f719239e01d50ca03ce7d7048d3fe7cb3ec6e8a5f`.
Raw operational inputs, pseudopotential bytes, streams, native state, and calculator
artifacts remain external and uncommitted.

## Generic-design learning boundary

This Workflow tests requirements not exercised by the silicon parameter studies:
ordered dependency stages, immutable native-state admission and copying, a collinear
spin model, a magnetization seed versus calculated magnetization, spin-channel
spectra, and two independent postprocessors selecting different components of one
predecessor result. It does not itself accept a generic public contract.
