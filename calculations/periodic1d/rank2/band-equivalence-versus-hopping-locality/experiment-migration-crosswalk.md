# Experiment-tree migration crosswalk

## Scope and baseline

This crosswalk assigns every tracked file under
`experiments/model-adequacy/periodic1d/band-equivalence-versus-hopping-locality/` at
baseline revision `c49aaf816702c321cdd649e2567af70da57246fe` to exactly one
calculation-side destination or provenance-only disposition. The baseline contains 40
files. SHA-256 identifies source bytes; it does not establish scientific validity,
convergence, publication acceptance, or retained-evidence status.

The destination owner is
`calculations/periodic1d/rank2/band-equivalence-versus-hopping-locality/`. No source file
may be removed until its disposition and applicable parity gate below are verified and
all maintained consumers have moved.

## File partition

| Experiment-relative source | Baseline SHA-256 | Calculation destination or disposition |
|---|---|---|
| `.gitignore` | `26b93cca510c4bd9eca7028e0c451befb03bf76d67efd975cf9413bf0a43dcdc` | Provenance-only; repository root `.gitignore` already owns every pattern. |
| `README.md` | `c0dc29f595fa21c239d9b426c404756c71e0e08c621b4dc7ea5e22fb2d9fe265` | Integration completed in `README.md`, `migration.md`, and this crosswalk; predecessor digest retained here. |
| `analysis/README.md` | `48be115415e029549ba2a4cdf7392858946444d0a054db04c4a60ec2eab9a9e8` | Path-adapted integration completed in `analysis/development/README.md`; predecessor digest retained here. |
| `analysis/amplitude-resolution.csv` | `e3ca18e0e636aa5623365b7e8acaf3837bef0f4344c1355f4565c7ab1016c29b` | `simulations/development/results/amplitude-resolution.csv` (exact duplicate). |
| `analysis/analyze.py` | `316537795cba86f638edc173e02062ba318392216862ae1c020365d2d0e954b1` | Adapted counterpart: `run_flat_development.py`. |
| `analysis/analyze_nonflat.py` | `b32e43ba25a9cdcbde7656a4d0ab5de74a83e69a95ba241e8bcb375777df8434` | Adapted counterpart: `run_nonflat_development.py`. |
| `analysis/analyze_parent_family.py` | `d523b7dbb49db7fc7d8d5963c34fbd8dccb764263da51ca3781a8fea3a62ce8c` | Adapted counterpart: `run_parent_family_development.py`. |
| `analysis/analyze_truncation.py` | `728788701a0b8e8e02c22e2212ed8a2327b0c4f46bdf2e15d71bcce8d5f52091` | Adapted counterpart: `run_truncation_development.py`. |
| `analysis/band-equivalence-locality-scientific-story.pdf` | `191d8fff0dbc777a6268c0e1e3dd481f8160da11bc9b5797510919ca9e57b2a8` | `analysis/development/figures/band-equivalence-locality-scientific-story.pdf` (exact duplicate). |
| `analysis/band-equivalence-locality-scientific-story.png` | `b323ab00db328a3e0ad4304781d9ac79f68396861b15e1e24dc183793fea05ce` | `analysis/development/figures/band-equivalence-locality-scientific-story.png` (exact duplicate). |
| `analysis/band-equivalence-versus-hopping-locality.pdf` | `0be6089cc08ee90cb67fddde3983c98bad2f481fffffa5f4833e1f933efe6053` | `analysis/development/figures/band-equivalence-versus-hopping-locality.pdf` (exact duplicate). |
| `analysis/band-equivalence-versus-hopping-locality.png` | `0aeb71efae8570e2e38a20a9e1825efaf9548fc7683754714a3cd9cb7ab4a7b9` | `analysis/development/figures/band-equivalence-versus-hopping-locality.png` (exact duplicate). |
| `analysis/hopping-power-map.csv` | `256d3750899af828b11ed1e96a471593e3bfe12a13e9920481fc4561df5f40e4` | `simulations/development/results/hopping-power-map.csv` (exact duplicate). |
| `analysis/journal-narrative.md` | `e48829fbeff136b977d88f32372ee6ecb098f06524d57d0bad225b9205a01dfe` | `analysis/development/journal-narrative.md` (exact duplicate). |
| `analysis/momentum-refinement.csv` | `d7ebcebde6fe1915f5841fe68d598f89d81a17379a7f8a0484ff96033f751f0f` | `simulations/development/results/momentum-refinement.csv` (exact duplicate). |
| `analysis/nonflat-amplitude-resolution.csv` | `72873cbaa911a20145700148b77b4deb885617c7f37c08c9e468aaadb2ef8d18` | `simulations/development/results/nonflat-amplitude-resolution.csv` (exact duplicate). |
| `analysis/nonflat-continuum.csv` | `d59c34e829025a66037fa97f7be6408ef6a40fc393f66c9a6da99e17034f38f9` | `simulations/development/results/nonflat-continuum.csv` (exact duplicate). |
| `analysis/nonflat-four-state-exploratory.pdf` | `35d5602eed7982a78e2bfe1d6ebecc42a77c95428445e59636c1a8bda1bb4b19` | `analysis/development/figures/nonflat-four-state-exploratory.pdf` (exact duplicate). |
| `analysis/nonflat-four-state-exploratory.png` | `1c643dfbe40940ab97d2765990e326a5c4753ce84e6c8b50fc0acee97fc9e438` | `analysis/development/figures/nonflat-four-state-exploratory.png` (exact duplicate). |
| `analysis/nonflat-hopping-power-map.csv` | `f48ddc94f6559853c1c9124cddae29d890f06f747bddfd36e72c3460817601a0` | `simulations/development/results/nonflat-hopping-power-map.csv` (exact duplicate). |
| `analysis/nonflat-momentum-refinement.csv` | `cd513a6fea1d4f28984e857f64c2995cf7fab493e9775ddef64ec1b4dc8c28d3` | `simulations/development/results/nonflat-momentum-refinement.csv` (exact duplicate). |
| `analysis/nonflat-selected-hopping-tails.csv` | `98c9c46430e4840ad7497a1a6f0a61591ef87e1acf68353bcb6d5054c8515857` | `simulations/development/results/nonflat-selected-hopping-tails.csv` (exact duplicate). |
| `analysis/parent-family-continuum.csv` | `1ab9a26544f70f2f53ad798f6ab61aa9f72b7f065f5dc3fa67ff84f8b5557597` | `simulations/development/results/parent-family-continuum.csv` (exact duplicate). |
| `analysis/parent-family-robustness-exploratory.pdf` | `68a5358e22652cf0fe92298cca9d082b4bfb702d62432b01b23e6fe7638810ac` | `analysis/development/figures/parent-family-robustness-exploratory.pdf` (exact duplicate). |
| `analysis/parent-family-robustness-exploratory.png` | `c1ca49fe78dd38619ee9abe94ca33b6b67037c7460586f67dd96ba3fdf681976` | `analysis/development/figures/parent-family-robustness-exploratory.png` (exact duplicate). |
| `analysis/parent-family-summary.csv` | `38427e90bf7d336210bdd7e0845e593b2a83d5d298530991bb30321fc0143ed6` | `simulations/development/results/parent-family-summary.csv` (exact duplicate). |
| `analysis/plot.py` | `37e12d242c6db5e64dcc2c6701cbfa5e0f6d60e9dc341d436eb90f51ac0f0c83` | Adapted counterpart: `analysis/development/plot.py`. |
| `analysis/plot_nonflat.py` | `fc3bd2db69fe373714f98a6deb0f539616964a4ccee1a9495a836b2e8921f88e` | Adapted counterpart: `analysis/development/plot_nonflat.py`. |
| `analysis/plot_parent_family.py` | `b4d0b146eb0d400b9c0ad28075c65dbb5a8bd8e66c1c885ee317cc939c512bee` | Adapted counterpart: `analysis/development/plot_parent_family.py`. |
| `analysis/plot_scientific_story.py` | `38cc2c224b512296fef9ed838f50b0fb5286ee66787ee1452edf4bd7be85965a` | Adapted counterpart: `analysis/development/plot_scientific_story.py`. |
| `analysis/plot_truncation.py` | `c31057999d984f4227b2cc90b2d20a5b040bfe75f748d71dfdcecd3d450114e5` | Adapted counterpart: `analysis/development/plot_truncation.py`. |
| `analysis/selected-hopping-tails.csv` | `5e81b380307d9af9f39efb477a97fef6904cd1642c1da2b230b66ad3364d8574` | `simulations/development/results/selected-hopping-tails.csv` (exact duplicate). |
| `analysis/truncation-band-consequences.pdf` | `56e2b48ea53daee593648f9b0f9aaa0ddcf80c45e12f761d75db3006955c6327` | `analysis/development/figures/truncation-band-consequences.pdf` (exact duplicate). |
| `analysis/truncation-band-consequences.png` | `1ebbdc96ec58c3b800734551b8f56a492bac6c5b74a46cabc62a504f0d4321ea` | `analysis/development/figures/truncation-band-consequences.png` (exact duplicate). |
| `analysis/truncation-consequences.csv` | `f5bfdf47c3e3163e95eb9105f648885654c0a5759ba37acff328a5a5d1b03f3e` | `simulations/development/results/truncation-consequences.csv` (exact duplicate). |
| `analysis/truncation-summary.csv` | `635e37b583fdc6b8f0e24c2077a85b7ccff80acfe6c7d3745de0a8b642ae87b9` | `simulations/development/results/truncation-summary.csv` (exact duplicate). |
| `experimental-protocol.bib` | `360e4a9e83f700650d1bb9319fcead9a2e39e737cf161c2a3d32ef43a3986202` | Exact move completed: `protocol/experimental-protocol.bib`. |
| `experimental-protocol.pdf` | `c367f0ea701ee39fffb5ab80ab0c1a0dcd4cd5850dff00b5b77f0ce630b5d74d` | Exact move completed: `protocol/experimental-protocol.pdf`. |
| `experimental-protocol.tex` | `3b1cff165ebd3ec803469d4df8cd40422f4bf80b73472ec220ca67ed1c982725` | Exact move completed: `protocol/experimental-protocol.tex`. |
| `smooth-threshold-continuum.csv` | `09452fb9a202c351b756681598e6910891f0208f73da2388e27fdf8638cbc9ae` | `simulations/development/inputs/smooth-threshold-continuum.csv` (exact duplicate). |

The baseline partition is closed: 25 source files originally had exact-byte
calculation-side duplicates, nine scripts had named adapted counterparts and a completed
parity audit, two README integrations are complete, three protocol files moved exactly as
one buildable maintained protocol set, and one local ignore file is provenance-only.

After the authorized dirty-source recovery and scientific-story correction, the 35 files
that physically remain in the experiment tree have these removal-time dispositions:

- 13 remain exact-byte duplicates of their calculation-owned destinations;
- 12 are superseded baseline predecessors whose current calculation destinations have
  different, explicitly recorded successor bytes;
- nine are adapted script predecessors; and
- one `.gitignore` is provenance-only.

[`experiment-removal-manifest.json`](experiment-removal-manifest.json) binds every current
source SHA-256, destination SHA-256 where applicable, disposition, and exact Git recovery
revision.

## Parity gates

### Exact-byte and superseded predecessors

Before removal, validate all 35 entries in `experiment-removal-manifest.json`. The 13
`exact_duplicate` entries must still match their destinations byte for byte. The 12
`superseded_predecessor` entries must retain their source SHA-256 at recovery revision
`011eee90f7be30770dd5fb2db844fe35633755fc` and their recorded successor destination
SHA-256. No numerical re-execution is needed to establish these byte and supersession
identities. These files remain development inputs, outputs, narratives, and figures;
neither byte identity nor supersession promotes them to retained evidence.

### Adapted analysis and plotting scripts

The completed nine-pair audit is recorded in
[`adapted-script-parity.md`](adapted-script-parity.md).

The four source analysis scripts import the removed installed
`ksdft2effmass.campaigns.model_adequacy.band_equivalence_locality.periodic1d` package and
are not a maintained executable route. Their calculation-side counterparts import the
calculation-local `workflow` owner and write into the calculation-owned development
layout. The five plotting counterparts likewise target the calculation layout. Recovery
introduced later development changes to several counterparts; the removal manifest
therefore classifies all nine source scripts as adapted predecessors rather than current
byte-equivalent implementations.

Before source-script removal:

1. classify every source-to-counterpart difference as import ownership, path adaptation,
   or numerical/semantic change;
2. reject any unexplained numerical or scientific change;
3. run the calculation-side focused tests;
4. reproduce outputs only in isolated scratch when needed, never by overwriting the
   tracked development snapshots; and
5. require named parity for flat, nonflat, parent-family, truncation, and rendering
   channels.

Passing tests and matching development artifacts establish software parity only, not
convergence or scientific validation. Reusable behavior required by the retained
lifecycle now resides in reviewed installed source owners, and the direct scripts do not
import `workflow/`. The remaining calculation-local donor still owns development-only
packaging and historical reproduction surfaces; its reviewed retirement is separate from
the completed unsealed direct lifecycle.

### Documentation and protocol

The two README donors have been integrated while preserving their family identity,
development status, direct flat analytic rule, pointwise nonflat scope, refinement
limitations, nonclaims, commands, and complete channel inventory in calculation-owned
documentation. The three full protocol
files moved together without byte changes into [`protocol/`](protocol/); they remain a
prospective pre-version protocol and do not become immutable merely by moving.

The local `.gitignore` is not copied because the repository root already ignores
`__pycache__/`, `.pytest_cache/`, `.mypy_cache/`, `.ruff_cache/`, `.venv/`, and Python
bytecode. Its baseline path and digest above provide predecessor recovery.

## Maintained consumers

The following consumers were inventoried before experiment-directory removal:

- `experiments/README.md`, `calculations/README.md`, and the source README navigation;
- `docs/architecture/v2/ksdft2effmass/band-equivalence-versus-hopping-locality-experiment.md`;
- `docs/architecture/v2/ksdft2effmass/calculation-campaign-identity-registry.md`;
- `docs/publications/papers/experiment-to-paper-allocation.md`;
- `docs/publications/papers/Ragasa2026a/v3/manuscript.tex`, which consumes the analytic
  CSV and scientific-story PDF;
- `docs/publications/papers/Ragasa2026a/v3/supplementary.tex`, which consumes
  calculation-owned development figures; and
- `docs/publications/conferences/ICMSEP2026/presentation/README.md`, whose retained asset
  has SHA-256 `9e88e334c7b6c3ae25fbd264428d128d2ba17f16121ed8613c2412c886c1e9be`
  and is not byte-identical to the current source/destination scientific-story PDF
  (`191d8fff...`). That asset remains a distinct presentation copy with a historical
  copy-time locator and an explicit calculation-side successor locator.

Navigation, architecture, registry, allocation, and all existing tracked Ragasa2026a
input/figure consumers now use calculation-owned paths. The source README navigation has
been removed after its content integration.

The Ragasa2026a v3 sources also named five files that were absent from the 40-file source
partition and from every Git ref: `range-inflation-preview.pdf`,
`truncation-error-channel-decomposition.pdf`, `frame-sewing-diagnostics.pdf`,
`hamiltonian-spectral-diagnostics.pdf`, and `sampled-range-decision-map.pdf`. After the
read-only audit, the operator authorized complete-source recovery. The full producing
graph, predecessor figure bytes, explicit adaptations, and dependency dispositions are
now bound by
[`recovered-development-source-manifest.json`](recovered-development-source-manifest.json),
and all five manuscript consumers use calculation-owned paths. The recovered files are
maintained development inputs, not retained evidence.

A post-recovery repository search found no experiment-tree path in the Ragasa2026a v3
sources. The only exact references to this historical experiment path outside the source
tree and migration records are immutable predecessor locators in architecture/provenance
documentation and the original-copy locator for the distinct ICMSEP2026 presentation
asset. None is a runtime, test, documentation-build, or publication input.

## Removal gate and execution

Removal of the experiment directory required all of the following:

- all 40 baseline rows retain exactly one verified destination or provenance-only disposition, and all 35 remaining source files pass `experiment-removal-manifest.json`;
- adapted-script differences, channel parity, nested ownership, and artifact/schema paths are recorded;
- the three-file protocol donor is recovered under the calculation owner and protocol authority is explicit;
- historical M2, monograph-composite, and finite-angle donors have exact Git/digest dispositions;
- every maintained consumer uses a calculation path or an explicit immutable predecessor
  reference;
- the five formerly unresolved publication inputs retain their reviewed complete-source
  recovery disposition and predecessor identities;
- no installed source, test, documentation build, or publication build depends on the
  experiment path; and
- deletion receives separate operator authorization.

All gates passed. After explicit authorization, exactly the 35 manifest-bound files were
removed at `2026-10-27T06:37:02Z`. Preflight proved that the manifest, tracked-file, and
filesystem-file sets were identical and that every source hash matched. No other
periodic-1D family was removed. The deleted bytes remain exactly recoverable from
`011eee90f7be30770dd5fb2db844fe35633755fc`; deletion authorization did not include any
Git commit, push, pull request, or merge.
