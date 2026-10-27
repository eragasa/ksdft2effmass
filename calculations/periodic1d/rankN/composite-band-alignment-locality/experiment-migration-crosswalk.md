# Higher-rank experiment migration crosswalk

## Scope and baseline

The old experiment folder contains five files. This record says where each file belongs
now:

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
| `run_development.py` | `2c548efc6ca144fdbd0bc93b92d719855a40107d5a7300a193ba73b049c7e9ef` | Adapted counterpart `run_development.py`, SHA-256 `11b7d09f5760f74e5f37d2070f5663fe19105a61ec53a65513995bca32112bc8`. The only source differences are the import owner (`workflow` rather than the removed installed package) and output routing (`results/` rather than the experiment analysis directory). |
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
`c5d34a93b4710a4a430738c404c775865d418d42`. The calculation-local `workflow/` is the
maintained successor, not a compatibility import facade.

| Module | Historical SHA-256 | Current workflow SHA-256 | Relation |
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

“Reviewed successor” records a byte change after ownership consolidation; it does not by
itself assert numerical parity. Current focused tests and explicit script-parity checks
remain required before source removal.

## What the current calculation does

The current code evaluates `3`, `4`, `8`, and `16` retained states; rotation depths `1`,
`2`, `4`, and `8`; and four alignment choices. It constructs the model, chooses
alignments, follows the basis around the momentum grid, computes real-space hopping
matrices, measures truncation errors, and records failures explicitly. The development script writes only a replaceable summary.
The formula-check script is not an independent check of the full result.

The exact protocol candidate selects future input, result, verification, and provenance
wires, but those wires and strict schemas do not yet exist. The current workflow does not
use the PIAB1D/QHO1D shared byte-owning verification and authenticated-rendering
lifecycle. Migration of these five donor files does not close that implementation gap.

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
