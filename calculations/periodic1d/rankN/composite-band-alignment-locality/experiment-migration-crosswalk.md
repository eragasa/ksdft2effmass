# Higher-rank experiment migration crosswalk

## Scope and baseline

The old experiment folder contained five files at the recorded source revision. This
record says where each file was assigned during the experiment-tree migration:

- the detailed calculation plan is copied exactly into this calculation folder;
- the two old scripts have maintained calculation-side replacements;
- the old README is incorporated into current documentation; and
- the old ignore rule is replaced by the calculation's current output and cache rules.

No experiment file has been deleted. The source revision is
`81f7c09a5edc50be698bd3a5f047438cd61d4eca`. Recording the move does not authorize a
scientific run and does not turn development output into retained evidence.

## Five-file partition

| Experiment source | Source SHA-256 | Calculation disposition |
|---|---|---|
| `.gitignore` | `a169f73e7e78f2837fcf552e0abfa6b0b162606ce488293e86481afff485921f` | Adapted policy. The source ignored `analysis/development/*.json`; the maintained producer writes `results/schema-free-development-summary.json`, and the calculation `.gitignore` ignores `results/` plus local Python caches. Repository-root policy covers the cache patterns. |
| `experimental-protocol.tex` | `160b61b2c2dc87e7628524c710c779f8e3b2c547f0a2d228615300aa06bdce0b` | Exact-byte copy at `protocol/experimental-protocol.tex`; authority and the historical verifier-name mapping are documented in `protocol/README.md`. |
| `README.md` | `5608ddd21db3f68110866ab63e25247e50b56765752e5f4c60e0b5ac97c00101` | Integrated into the calculation `README.md`, protocol README, this crosswalk, and the distributed `migration.md`; stale installed-package and dependency-pin claims are not repeated as current facts. |
| `run_development.py` | `2c548efc6ca144fdbd0bc93b92d719855a40107d5a7300a193ba73b049c7e9ef` | The first adapted counterpart had SHA-256 `11b7d09f5760f74e5f37d2070f5663fe19105a61ec53a65513995bca32112bc8` and used the calculation-local Workflow package. That migration-time script has been superseded by the direct maintained-owner composition, SHA-256 `d36995af843f8652f188b2352c69e2749617ba05aab0c5aacc341a2c3ad37cbd`; it does not import Workflow code. |
| `verify_d1_p0_g0_controls.py` | `d4aa8c0893b73dadf9ac5994c8a4e7484edbd15d4f68f6d1e274adb9e04357ca` | Adapted counterpart `verify_analytic_controls.py`, SHA-256 `3d090ac885a9d1c1cab9dc06ea31f048696bd85dd70d23b3969b0ea24cc8d77d`. It is byte-identical after removing only the source shebang; its bounded sanity-check role is unchanged. |

The partition is closed: one exact protocol copy, two adapted executable counterparts,
one integrated README, and one adapted ignore contract. The five source files were later
removed after separate authorization.

## Where the old script's imported code went

The experiment producer imported
`ksdft2effmass.campaigns.periodic_reduction.higher_rank_d1`. That installed package is
not present at the current revision. Its last complete tree is revision
`25161d7f55c708a464c18ea8d5d0fd6152ff86a6`, Git tree
`94f2f042322aa69969448ca77b8d47c163edef70`; deletion occurred in
`c5d34a93b4710a4a430738c404c775865d418d42`. The calculation-local `workflow/` was the
migration-time successor. It is now immutable historical provenance and is not a
maintained import, test, or execution boundary. Maintained behavior belongs to
`ksdft2effmass.periodic1d.higher_rank_alignment` and canonical upstream owners.

| Module | Historical SHA-256 | Migration-time workflow SHA-256 | Relation |
|---|---|---|---|
| `__init__.py` | `f91cc130bf9a41fcc79bdd5bded66f062d66d2d5257b0be5cb1c84fb7295cb23` | `95498502180143ef254544648c27c01fc84acca7346b2f458ad484ef57c66ea0` | reviewed successor |
| `_validation.py` | `ac2507ba0f2bbdad1d15c982eca91642d57e0ea64f3cf409dcd9919aafd68e7f` | `43db05ad01597cbf7625a8b72aab05215b709886896e2d98574e8921c4620d04` | reviewed successor |
| `alignment.py` | `8564c053a7bdd57144c418ffa05d0faa9eb93b543fa181cdcff6df375a194233` | `8e83d56eef667e93e61ce94816992e2014bd0eb751cc4fea358ad5f89a291b1a` | reviewed successor |
| `calculation.py` | `31d1baa48fbc240c369686977ca506243dde53f69afa06d8886402fd29f9f750` | same | exact |
| `case_calculation.py` | `652f1c88a7db4a6250840c6106e8cf8d9ebf38b2a2777a9c3e8bd1d722a4d591` | `367f5e34ad606d8d31fe53f69cfbce1cfc081fa26508b35740b39f49b8357c8a` | reviewed successor |
| `definition.py` | `22e22c7ce1eb53796bffab1ff5bf05c2d36ee64d33c97e157eaf6ecf9e8e8de4` | `f372c956a64ccdc1cf393dd2cd2a70f5ee5daa093ac8419d95ec29ba39d8be24` | reviewed successor |
| `model.py` | `fd553aae9d7e97286b812f64a6c532e8868304aa494c2ac63ed6bbb13c62bfff` | same | exact |
| `numerical_backend.py` | `bc26d7a3fbcef45f835d96940ec08eb968ed30c1335a654a8ca96a4c1d0f8c57` | `41f004f1578b18499f11a54e7e143a9b6f142e074a400b04da3991edbb187539` | reviewed successor |
| `procrustes.py` | `fa0b65c2e3aad695c4fde17493ba01717335377072c4f3ace3e347eb71c2903c` | same | exact |
| `records.py` | `fb3bc8bc13df34686875402ef36f05f5c2b8bb437cab869489d0706e2ebc2401` | `690a310b24293fc325fe626379c95344c1d6ed600498866023219663a9306b1d` | reviewed successor |
| `transport.py` | `764feceddd9c2cfdb828c5a7998e8d36e4520f4da2938352a7e6efc12f189f97` | same | exact |

“Reviewed successor” records a migration-time byte change after ownership consolidation;
it does not by itself assert numerical parity or current ownership. The table is retained
as provenance for the already completed source removal.

## What the current calculation does

The maintained package evaluates `3`, `4`, `8`, and `16` retained states; circuit depths
`1`, `2`, `4`, and `8`; and identity, global-unitary, pointwise-unitary, and
known-inverse-oracle gauge alignments. It constructs the analytic parent and attacked
fields, applies common closed-loop transport, calculates finite-periodic hopping blocks,
separates interpolation and truncation errors, evaluates refinement, and records bounded
failures explicitly. The direct development script composes maintained KSD, PhysKit, and
Optimization owners and writes only a replaceable non-evidence summary. The
formula-check script is not an independent check of the full result.

Strict typed calculation requests and results, canonical record bytes, a bounded
producer-independent reference for analytic-model and attack core invariants, and a
bounded direct-sum identity/known-inverse-oracle Fourier reference now exist. The latter
also compares shifted interpolation and support tails for both controls and exact support
for the oracle. Complete protocol-wide
numerical recomputation, byte-owning verification, retained-artifact schemas, complete
provenance, authenticated rendering, and retained execution do not. Migration of the
five donor files therefore does not close the authenticated lifecycle.

## Consumer migration

Maintained consumers must use calculation-owned paths before removal:

- `experiments/README.md` and `calculations/README.md` family navigation;
- Ragasa2026c v1 protocol and analytic-control links;
- `docs/publications/papers/experiment-to-paper-allocation.md`; and
- the proposed companion-contract locator in the mathematical-representation owner plan.

Historical path mentions may remain only when qualified by revision/digest and must not
be runtime, test, build, or publication inputs.

## Removal checks and execution

Removal required all five source hashes to match this record, the copied plan to match,
both script comparisons to pass, maintained documents to use calculation paths, local
tests and the document build to pass, and separate operator authorization.

All conditions passed. At `2026-10-27T12:05:11Z`, exactly the five manifest-listed files
were removed. Before deletion, the manifest, tracked-file, and filesystem-file sets were
identical, so no untracked file was removed. The files remain recoverable from
`81f7c09a5edc50be698bd3a5f047438cd61d4eca`. This authorization did not include commit,
push, merge, scientific execution, release, or publication.
