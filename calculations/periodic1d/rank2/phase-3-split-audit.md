# Phase 3 rank-two split audit

## Scope and evidence boundary

This audit is bound to merge revision
`78b4ed86a32069232cb7647c0525f7f782e9bed2`. It inventories the live installed M2
predecessor, its direct Python consumers, the historical Conference Paper 1 M2 package,
and the two scientifically distinct rank-two successors. It changes no scientific source,
result wire, historical Architecture v2 record, retained artifact, or publication input.

The two successor questions are intentionally different:

1. **Band equivalence versus hopping locality:** can pointwise isospectral rank-two
   represented Hamiltonians have different hopping locality when only one restricted
   global real rotation is admissible for comparison?
2. **Composite-band alignment and locality:** how do a declared pointwise Procrustes
   family and a distinct one-global-unitary family change represented operators and
   block-hopping locality for one fixed attacked frame path?

Shared parent coefficients, frame operations, and Fourier mechanics do not make these
one calculation, wire, threshold policy, evidence state, or conclusion.

## Live predecessor recovery inventory

The six-file installed package has Git tree
`081b4b13519fb57cb26652927db707a248c06f85`. The ten-row inventory below includes the
package, its two surviving aggregate/export modules, its sole aggregate test, and its
Sphinx API page.

| Path | Git blob | SHA-256 | Successor disposition |
|---|---|---|---|
| `doc/sphinx/api/ksdft2effmass/periodic1d/multiband_alignment.rst` | `24bb5ff26a3e55e13ce385ab206aec8723dab447` | `e8dcb8eb0367f3fae10f327919b2cc425111ca1d79637cc13ce47301ad377c86` | Replace with composite-family API documentation only after the direct public surface exists. |
| `python/src/ksdft2effmass/periodic1d/__init__.py` | `30f3c4c3a5988001eeb2210d7996945298a47537` | `9e0f838947cb9aa013ce1ca405922a9d7a4036f958e7165c691c603f2b0c7e67` | Remove only the eight M2 exports after composite and M3 consumers migrate; preserve unrelated exports. |
| `python/src/ksdft2effmass/periodic1d/model.py` | `68b0126ea0649ac74755bb6fb2eec844bbb06516` | `65eeebeea9fc7af3c073fc0518b3ca4f8884add5f20f7d6525374e2bda174bd0` | Replace `Periodic1DBlockHamiltonianToyModel` with family-owned exact parent data; removal is blocked by M2 and M3 callers. |
| `python/src/ksdft2effmass/periodic1d/multiband_alignment/__init__.py` | `929f5b1ba4f0f05d982c9338ced6a9ee3b270dee` | `f60f3416955ef872375bd7b16a007bfc02a3b1ccaa0d40cd071fd73e949bbdbb` | Composite-family predecessor; do not reproduce its aggregate import facade. |
| `python/src/ksdft2effmass/periodic1d/multiband_alignment/calculate.py` | `7f9d91358ec917e45626745759ed4940d90cdfd9` | `a22355c89700959e28fbabaa739644b77e24f8b735f118fec1fff977a2514cd2` | Behavioral donor for composite calculation; selected parent and reference/attack locality channels are adapted independently by the band-equivalence family. |
| `python/src/ksdft2effmass/periodic1d/multiband_alignment/definition.py` | `058016f7f4194d2a4ff13c621fa7db99f00f56cc` | `e664c32f51ac2357d6d6e8da9b1b5c9f7fdcefe8dbc23a38d187f90b4f5f23d7` | Replace with a composite-family typed configuration; do not preserve `parent_model` as a toy-model service boundary. |
| `python/src/ksdft2effmass/periodic1d/multiband_alignment/results.py` | `91fa737954d391fcdbb7baefe30ce18e45e88107` | `d61138ded8797ae15b26c565f873de1e41f0b95cac03a9aa7751e042cb81e9a8` | Split into concise composite-family typed result sections; band-equivalence uses its own records. |
| `python/src/ksdft2effmass/periodic1d/multiband_alignment/serialization.py` | `f8ca63deb2719f02fe8f9627e8fd49f4670d4617` | `1466466e1eea6f8fba3bf839532b4f853fa265a9344ea07568e1b142011d1ffd` | Schema-v1 encoder is provenance-only after migration; neither successor decodes it at runtime. |
| `python/src/ksdft2effmass/periodic1d/multiband_alignment/verify.py` | `990ee34d1fbaaa9929508d83483ec5e6d00fcd79` | `afe0d4388051bf1d790773ce1c914e766e440d5851d9d38678f9e5f5604a648e` | Numerical-method donor; each successor needs a separate byte-owning independent verifier. |
| `python/tests/software_verification/ksdft2effmass/periodic1d/test__Periodic1DMultibandAlignmentCalculator.py` | `faa1fcb8b2b4941bfe4dd04f34f893c9152ed6d4` | `88f224ef26c9e5b1564d362d630bad5922fd85481fd209d8cc60fdfa71890402` | Split into package-aligned composite tests and historical-package parity checks; do not move it wholesale. |

The sorted path-inventory SHA-256 is
`22d3a2cb0151a6d6034b23b47d27d8332ab9a591afb9bb1db800d6287c46bd5d`.
The sorted `path<TAB>content-SHA-256` inventory SHA-256 is
`822acfd5b781236f0581b0b140ccd710866ebd37ab475b8df2aca04646555efa`.
Every row is recoverable through `git show <revision>:<path>` at the bound revision.

## Direct Python consumers and removal blocker

The M2 aggregate test is not the only consumer. The live M3 admissible-set predecessor
embeds the M2 definition and result, invokes its producer and verifier, and serializes a
nested baseline summary. These six files therefore block Phase 3 removal even after a
composite successor exists.

| Direct consumer | Git blob | SHA-256 | Dependency that must migrate |
|---|---|---|---|
| `python/src/ksdft2effmass/periodic1d/admissible_sets/calculate.py` | `fec891e96fd918de9c34bd604d0a3f94ba261acf` | `2320bc99b7eb3ccd16988fd3eaf54fa457f6f80742ec4ebc4552f6fa8921a17c` | Calls the M2 producer and reads reference/attacked transforms and both sample targets. |
| `python/src/ksdft2effmass/periodic1d/admissible_sets/definition.py` | `8cc860063df00c17d91bb08c919bab89bd49d088` | `6c34c34b1665ae041cf692c4fe9ada4779872dc599d81fd56e8f55fe34401384` | Embeds the exact M2 definition and its parent/rank controls. |
| `python/src/ksdft2effmass/periodic1d/admissible_sets/results.py` | `c6621f4182bb8c898ffcce2d9ca8b6896f6668c8` | `e8e59f1ae992c33836f466f476ba1dc2b3ae3f59296a8536141747a71d072727` | Embeds and correlates the complete M2 calculation result. |
| `python/src/ksdft2effmass/periodic1d/admissible_sets/serialization.py` | `d3a103327fc68f9a282c394a10d48f280bcebe2a` | `61fb1e7e8be6799a5bd4f075201832b32caa79db3a21f6413de6c6f45ee84879` | Encodes M2 definition fields and baseline diagnostic summaries into the M3 wire. |
| `python/src/ksdft2effmass/periodic1d/admissible_sets/verify.py` | `55a93e5e1efdc7cb91c6d85e1ef49c37459e570f` | `2d264ba87d29d2989deb67ea47f64ea16b5404673b40adca90de3ace368343a2` | Invokes the M2 verifier before reconstructing M3 quadratics and certificates. |
| `python/tests/software_verification/ksdft2effmass/periodic1d/test__Periodic1DConstrainedAdmissibleSetCalculator.py` | `0f812a2c30bf0d1d75f638a40e8d10aa2993255e` | `58885448d13af79c44a8517f3f125d6f7ed007ce60ae0b871eb6111513f7421d` | Constructs the M2 baseline used by the aggregate M3 tests. |

The consumer path-inventory SHA-256 is
`bdf400c5e1bd3cde8f55e14741d8fca3962699942e9eb35c7ea84802f7b7d9ce`.
The consumer path/content inventory SHA-256 is
`aea241fb8366e93e9de3fe4ec9c07a63b55d2462787bcc3a6081b3418b197518`.

Consequently, Phase 3 may add the direct composite successor but must keep the installed
M2 predecessor supported until Phase 4 migrates M3 to explicit authenticated upstream
result bytes and digests. A facade from the old M2 types to the new composite types would
hide rather than remove this dependency and is rejected.

## Historical M2 package

The historical package is absent from the live tree and remains recoverable from commit
`c5d34a93b4710a4a430738c404c775865d418d42` at tree
`19af0e6d222b1f41fcb7b2869e1fcd7c2f309cd9`. The tree contains 19 files. All 14 entries
in its primary `SHA256SUMS` manifest reproduce.

| Historical property | SHA-256 |
|---|---|
| `SHA256SUMS` | `019050d903e01b0f33af1c658af33af6e77653c733f96d661d38595adbfdf73f` |
| `input.json` | `0db445f3df37f08661f6078a9595ef1646adf9b036c5f94da316255c431c26c9` |
| `protocol.md` | `b04fa9505aafc167312181e938217b9b4b37316059d126ad3b253c8b65a89dc4` |
| `result.json` | `3bb30d20f73d2d4ae8ea55a493d50978c5094dbecfcd22237dd8c32760b0f3da` |
| `verification.json` | `5e134f8bdbd52067ae40c7086fe045ad8a836d30c17d629aa41f416dff4dd674` |
| `figure-data.csv` | `7dd16907773bf14dd0a91feaf0c5ffbb7a81a8934d6236d277259f4e45662bb3` |
| `multiband-alignment-summary.png` | `c5569d4dd6821fc195d56640507c2e0a78d12649143eed80b7aef51707d7ae6c` |

The result schema is
`ksdft2effmass.periodic1d.multiband-alignment-calculation-result.v1`; the verification
schema is `ksdft2effmass.periodic1d.multiband-alignment-verification.v1`. Their bytes are
parity references, not successor inputs or schemas.

## Publication reference inventory

Fourteen publication files directly name the exact historical M2 package or figure, or
include its dedicated S3 appendix. Generic discussion of multiband alignment in unrelated
prospective papers is excluded from this exact-artifact consumer set.

| Publication consumer | Git blob | SHA-256 |
|---|---|---|
| `docs/publications/papers/Ragasa2026a/v1/README.md` | `9691628ecad6dd4fa38ca86adcbda7c33c60af4e` | `13d39033bb8bedc7b7f1290c22ee5bde9613f3fdc121b508d83ab6a73d0e88fe` |
| `docs/publications/papers/Ragasa2026a/v1/appendices/A-evidence-and-provenance-boundary.md` | `0ac915c1b37acddec12fdc8a179a05d0a8306371` | `9aea52332185a6cbd690b82d48ee2a1639da2b8d33310492399365df34096ac0` |
| `docs/publications/papers/Ragasa2026a/v1/appendices/A-evidence-and-provenance-boundary.tex` | `029ddf02f00921356eb5638396a18dd22964b2bb` | `7b268f064746b99d095e39d0a8c3fa353d1b4aec573b27d7e93e2c20a57104da` |
| `docs/publications/papers/Ragasa2026a/v1/appendices/README.md` | `7286b95b38c328f2b2223a8abc3cac20ea0133cd` | `d35233e378af43b9a09220b609c42177ccb36bd02c46416b5ff98cc859ee80c0` |
| `docs/publications/papers/Ragasa2026a/v1/appendices/S3-M2-multiband-alignment-calculation.md` | `ccdaa727f03b45fb8e595997328ad25174e381a3` | `b7c34f58b49bca3511af2a9e202065d4164047cc3237fbe08462a5f718272af2` |
| `docs/publications/papers/Ragasa2026a/v1/appendices/S3-M2-multiband-alignment-calculation.tex` | `c3015ced033230df5695fe88cdac5933c4f935a6` | `37626fbd21fd9ede7dfad59c7da672fe06048745ad2cbd3c0f0c30ea73584732` |
| `docs/publications/papers/Ragasa2026a/v1/evidence-ledger.md` | `839148fe86d39c82a607aae20c664006175394f0` | `148d0f47b7a327b336ce1b6886fe0fb0759a977f95399ecb8fb9f96cf8f5457c` |
| `docs/publications/papers/Ragasa2026a/v1/manuscript.md` | `1de038871c0da4a4e733928534c57a239e4235d2` | `3711e806b841e498384119fd17a56a6880c879011fa78c341a64d439019a1d9b` |
| `docs/publications/papers/Ragasa2026a/v1/manuscript.tex` | `ea5cbb5d20adf5f8da686a7d9ccbd72be98a1607` | `11f8e051fb313f35e567f4ceff910c1bac860ab19c99aa14bc7d5afd425837bb` |
| `docs/publications/papers/Ragasa2026a/v1/supplementary-material.tex` | `5890c10dbe5d5cd2b27e89a33ada81d7aa32f585` | `4f3cfffdeb8edf0ff4005294d48d1511bd191eb3ad09eeb167e3126a4e12eb25` |
| `docs/publications/papers/Ragasa2026a/v2/manuscript.tex` | `07e397323d1cdd9e882ed7c8872d9251b2917b30` | `160b1b769d6cc1f7738ddfa7f3b23ef362856a7c93927eb67b2724d1bc288a8e` |
| `docs/publications/papers/Ragasa2026c/v1/manuscript.md` | `308b5898f494975e8b5610bb3cfc649c7b03cdf3` | `476ca8d33931189f061a624a60c9b26b17a9183da0d004c8badd4e0ee64c3cfe` |
| `docs/publications/papers/Ragasa2026c/v1/manuscript.tex` | `4f1bd997ca3296f64472c9788f2668de4d1767bc` | `baf453722d96cf5b0360a0b80bfa1580465a1db7fe91167583943db10701baf4` |
| `docs/publications/research-monograph/current-library-capability-crosswalk.md` | `8feb765166aa0534a6935b2852d8748cb99cd50d` | `bd2724cf29132ab3c426b868034d30d5468d0435d0f3cfb8acead071d9e1bcc6` |

The sorted publication-consumer path-inventory SHA-256 is
`149ceec4f0588b2d19790a0dd33389d40ebec1e25593ecf9f69c84eb17b6c4d2`.
The corresponding path/content inventory SHA-256 is
`710869fe530cc15a4ad4cdc01cfddba37286ee6a6a8b43c418f7a013996fedf3`.

These publication documents remain bound to the exact Git-only package. They must not be
redirected to either successor without separate publication authority and an explicit
evidence-manifest migration. Missing live assets must not be reconstructed from
unauthenticated development outputs.

## Scientific channel split

`Adopted` means unchanged scientific meaning within the named successor. `Adapted` means
the mechanism or coefficient base is useful but the family owns different controls or
interpretation. `Rejected` means the channel is outside that successor. `Provenance-only`
means exact historical bytes remain references but are not runtime inputs.

| M2 channel | Composite alignment/locality | Band equivalence/locality |
|---|---|---|
| Exact four-state onsite and nearest-neighbor coefficient base | Adopted with the fixed 64/257 protocol and explicit parent identity. | Adapted as the nonflat parent coefficient base and parent-scale family; it is not historical M2 evidence. |
| Lowest-two-state retained space and sampled retained/excluded gap | Adopted with backend, basis, unit, energy-reference, and finite-sample qualification. | Adapted under the band's own mesh/refinement and qualification controls. |
| Polar frame transport and periodic closure | Adopted as part of the fixed attacked-path construction. | Adapted as a construction/qualification mechanism, not an alignment conclusion. |
| Fixed attack `0.30 + 0.65 sin(2πk) + 0.30 sin(4πk)` | Adopted exactly. | Rejected; the band-equivalence family owns `a sin(2πq)` and its amplitude inventory. |
| Pointwise Procrustes recovery | Adopted as one declared feasible family. | Rejected as an admissible comparison transformation; allowing it would undo the deliberate locality comparison. |
| One global complex unitary | Adopted as a separate aggregate feasible family. | Adapted to the narrower one-global-real-rotation comparison and its own positive-splitting rule. |
| Reference, attacked, pointwise-aligned represented operators | Adopted with explicit state-space alignment and separate channels. | Reference/comparison channels adapted; pointwise-aligned output rejected. |
| Complete Fourier block families and reconstruction | Adopted for reference, attacked, and pointwise channels. | Adapted for reference/comparison families with explicit cyclic/Nyquist handling. |
| Ranges `0,1,2,3,4,6,8` and 64/257 construction/evaluation roles | Adopted exactly for composite parity. | Rejected as controls; the band-equivalence family owns dense cutoffs, refinement meshes, and its disjoint evaluation rule. |
| Omitted-block norms and construction/evaluation spectral errors | Adapted into explicit cyclic-conversion power, ordinary omitted-block norms, and separately reported interpolation, truncation, and total Hamiltonian and sorted-band consequences. | Adapted independently into the band-equivalence family's corresponding channels and controls. |
| Schema-v1 result and object-input verifier | Provenance-only; replaced by canonical typed bytes and a byte-owning verifier. | Provenance-only. |
| Historical result, verification, CSV, and PNG | Provenance-only parity references. | Provenance-only donor references; never relabeled as band-equivalence results. |

## Parity and ownership gaps

### Composite-band alignment and locality

Before direct implementation is complete, this family still needs:

- one small immutable typed configuration containing genuine inputs and the exact parent
  coefficients, not `Periodic1DBlockHamiltonianToyModel`;
- explicit construction/evaluation coordinates, parent identity, basis, right-action,
  unit, energy-reference, backend, rank-cutoff, and failure conventions;
- PhysKit spectral decomposition and canonical represented-operator/Fourier owners rather
  than a local eigensolver facade;
- reviewed Optimization Procrustes ownership for both pointwise and aggregate selection,
  with disclosed absolute/relative rank cutoffs and fail-closed rank deficiency;
- concise typed result sections and canonical JSON bytes without schema-v1 decoding;
- producer-independent byte-owning verification of parent samples, frames, alignments,
  represented operators, transforms, truncations, and withheld errors;
- a verifier-owned authenticated visualization projection and closed figure inventory;
- direct calculate → verify → render scripts and package-aligned tests; and
- named 64/257 parity against the historical M2 channels without creating retained
  evidence.

### Band equivalence versus hopping locality

This family has a much broader development graph but still needs:

- extraction of reusable behavior from the calculation-local `workflow/` tree into
  cohesive reviewed source owners without importing or copying that tree;
- closure of its primary configuration, channel inventory, thresholds, maintained version,
  and execution/evidence policy;
- replacement of calculation-local eigensystem, transport, Fourier, and serialization
  mechanics with canonical owners;
- resolution of the deferred exact-identity gate used before snapping restricted-alignment
  correlations near `±1`;
- a bounded direct result design that does not turn every development sweep and plotting
  table into one universal wire;
- separate byte-owning verification and authenticated rendering for every decisive primary
  channel; and
- no activation of pandas as a project dependency without separate authorization.

## Recommended order and removal gates

Implement **composite-band alignment and locality first**. It is the direct scientific
successor of the live M2 package, has one fixed 64/257 control, and can establish the
rank-two typed calculate → independently verify → authenticated render lifecycle without
absorbing the larger band-equivalence development graph.

The first implementation slice should:

1. freeze the exact composite configuration and family identity;
2. implement the direct source/result/verifier/projection/renderer owners from canonical
   PhysKit, Optimization, and KSD operations;
3. establish named software/numerical parity with selected historical M2 channels;
4. add direct stage scripts and package-aligned tests; and
5. stop before retained execution, publication changes, or predecessor removal.

The band-equivalence successor should follow as a separate implementation slice after its
exact-identity and primary-wire decisions close.

The installed `multiband_alignment` package, its root exports, block toy-parent, aggregate
test, and Sphinx page become removal candidates only when all of these gates pass:

- the direct composite successor passes its own parity and review gates;
- Phase 4 migrates every M3 definition, producer, result, verifier, serializer, and test
  dependency to authenticated upstream bytes/digests;
- publication references remain bound to exact historical artifacts or receive separately
  authorized manifest migrations;
- exact recovery hashes are recorded at the final removal revision; and
- destructive removal receives separate authorization.

This audit creates no retained execution, seal, release, publication update, scientific
validation, or Formal certificate.

## Retirement completion

Phase 4 later migrated all six direct M3 consumer surfaces to authenticated canonical
composite-result bytes and explicit verification dependencies. After the replacement
passed its focused and bounded checks, the operator explicitly authorized retirement of
the installed M2 package, its generic block-parent record, aggregate test, root exports,
and Sphinx pages without a compatibility facade.

The final pre-removal inventory and exact recovery revision are recorded in
[`composite-band-alignment-locality/legacy-retirement.md`](composite-band-alignment-locality/legacy-retirement.md).
The historical M2 package, checksums, publication references, and evidence manifests
remain bound to their original bytes and were not redirected to the successor.
