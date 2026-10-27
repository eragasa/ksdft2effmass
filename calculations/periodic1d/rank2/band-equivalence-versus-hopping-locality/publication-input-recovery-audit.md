# Ragasa2026a missing-input recovery audit and disposition

## Scope

The initial read-only audit concerned the five PDF inputs named by the Ragasa2026a version-3
main manuscript and supplement but absent from the 40-file experiment migration
partition at baseline revision `c49aaf816702c321cdd649e2567af70da57246fe`:

- `range-inflation-preview.pdf`;
- `truncation-error-channel-decomposition.pdf`;
- `frame-sewing-diagnostics.pdf`;
- `hamiltonian-spectral-diagnostics.pdf`; and
- `sampled-range-decision-map.pdf`.

The audit identified candidate bytes and their immediate generation graph. The operator
subsequently authorized the recommended complete-source recovery. This document now
records both the read-only audit and that recovery disposition. The recovery assigns
calculation-side development ownership; it does not establish retained evidence,
authorize publication, or validate the scientific claims displayed in the figures.

## Git-history result

A filename search through every local Git ref found no committed occurrence of any of
the five PDFs. They therefore have no immutable Git revision, tree, or blob identity and
cannot be recovered from repository history.

A separate dirty primary worktree contained untracked candidate PDFs and PNGs at the
historical experiment path. The observed worktree state was:

- branch: `work/monograph-current-library-capabilities`;
- `HEAD`: `4835e7bf9161729cc8f0537bcc13db083896a6ae`;
- disposition of all five PDFs and PNGs: untracked;
- primary worktree handling: read only; no file was modified.

The commit identifies only the base of that dirty worktree. It does not identify the
candidate bytes, their untracked scripts, or their modified and untracked tabular
inputs.

## Candidate-byte inventory

| Candidate | Observed SHA-256 | Status |
|---|---|---|
| `range-inflation-preview.pdf` | `08b0ad0959d083aa0e36b8f3531aed853d40f71df7b291c4235dc15fdcc542e4` | Untracked candidate; one-page PDF |
| `truncation-error-channel-decomposition.pdf` | `13e48321309f56d08191cc0ae81b9940f46bbe89842a8701dc469ace217285a0` | Untracked candidate; one-page PDF |
| `frame-sewing-diagnostics.pdf` | `14e149980b2c8553d408fa0b14c9e104f04716315ae66cae09b05d0139cc56b8` | Untracked candidate; one-page PDF |
| `hamiltonian-spectral-diagnostics.pdf` | `d2481b139153b6a33c8e15544b90f4bb37f2103f65e840f3b3dd339750346ffd` | Untracked candidate; one-page PDF |
| `sampled-range-decision-map.pdf` | `cdcc4a1b5f6ca5bdb72c7ffe5d10ffee77196e83576aca17d396d3d3a185cb3e` | Untracked candidate; one-page PDF |
| `range-inflation-preview.png` | `7badbd53cbffdae86de6c8190267a453eabd76e1c0654c9e00d7634d220af9df` | Untracked candidate |
| `truncation-error-channel-decomposition.png` | `538d5cd9c6d02f1570d3ecbff5b4edc66761b4c1a88187d71e34665098ea45ae` | Untracked candidate |
| `frame-sewing-diagnostics.png` | `4a83d7a710834d4c2aa2c3b62c815853a1da8a937b1f0c0dc1c876788bdca5e7` | Untracked candidate |
| `hamiltonian-spectral-diagnostics.png` | `f50691f6b707a59b1c0ea7248e9acdd3eebf447765773721354680436252326e` | Untracked candidate |
| `sampled-range-decision-map.png` | `7a923f0f2a06baa6e6268408faf49156df3ce833c9044af274628652d29eb4c0` | Untracked candidate |

These digests identify the observed local bytes only. They do not establish when the
files were produced, which runtime originally produced them, or whether they are
publication-ready.

## Immediate generation graph

All paths in this section are relative to the historical experiment directory in the
dirty primary worktree.

| Source | SHA-256 | Git state | Role |
|---|---|---|---|
| `analysis/plot_range_inflation_preview.py` | `15f89d6e25634413b85d6d9b5050bc9748bdd150042d7a2fa5a3f36b4cf8dff4` | Untracked | Produces the range-inflation PDF and PNG from `truncation-consequences.csv`. |
| `analysis/plot_error_channel_decomposition.py` | `c481b433e23046021628bf0bc33ee8c80ddd428ca7329657b49635d1f4459088` | Untracked | Produces the error-channel PDF and PNG from `truncation-consequences.csv`. |
| `analysis/package_diagnostics.py` | `e6e51ca5f9f1e21266ad67694fe21d581a384fbb8bf4bd9c1bb9014fd22dcc69` | Untracked | Produces the three diagnostic PDF/PNG pairs and two derived CSVs. |
| `src/band_equivalence_hopping_locality/analysis.py` | `b227962352684f141beb306834c1cd1ed1ad2ad8b2a9b7de2d636b64b5006bd2` | Untracked | Loads and validates the 14-table diagnostic bundle. |
| `src/band_equivalence_hopping_locality/analysis_plot.py` | `cadc39d9d187154f680229309f0e49796f8fd83a85c1cf2c8d144f98046f3a79` | Untracked | Renders the three diagnostic figures. |

The diagnostic bundle consumed these exact table bytes:

| Table | SHA-256 | Git state relative to `4835e7bf...` |
|---|---|---|
| `analysis/amplitude-resolution.csv` | `e3ca18e0e636aa5623365b7e8acaf3837bef0f4344c1355f4565c7ab1016c29b` | Tracked and unchanged |
| `analysis/hopping-power-map.csv` | `256d3750899af828b11ed1e96a471593e3bfe12a13e9920481fc4561df5f40e4` | Tracked and unchanged |
| `analysis/momentum-refinement.csv` | `d7ebcebde6fe1915f5841fe68d598f89d81a17379a7f8a0484ff96033f751f0f` | Tracked and unchanged |
| `analysis/nonflat-amplitude-resolution.csv` | `72873cbaa911a20145700148b77b4deb885617c7f37c08c9e468aaadb2ef8d18` | Tracked and unchanged |
| `analysis/nonflat-continuum.csv` | `d59c34e829025a66037fa97f7be6408ef6a40fc393f66c9a6da99e17034f38f9` | Tracked and unchanged |
| `analysis/nonflat-hopping-power-map.csv` | `f48ddc94f6559853c1c9124cddae29d890f06f747bddfd36e72c3460817601a0` | Tracked and unchanged |
| `analysis/nonflat-momentum-refinement.csv` | `cd513a6fea1d4f28984e857f64c2995cf7fab493e9775ddef64ec1b4dc8c28d3` | Tracked and unchanged |
| `analysis/nonflat-selected-hopping-tails.csv` | `98c9c46430e4840ad7497a1a6f0a61591ef87e1acf68353bcb6d5054c8515857` | Tracked and unchanged |
| `analysis/parent-family-continuum.csv` | `1ab9a26544f70f2f53ad798f6ab61aa9f72b7f065f5dc3fa67ff84f8b5557597` | Tracked and unchanged |
| `analysis/parent-family-summary.csv` | `aa249ec7b19b8126e906f10ee657e79998c81980e6531440d2da2c0359c1aeb9` | Modified; differs from the migration baseline |
| `analysis/selected-hopping-tails.csv` | `5e81b380307d9af9f39efb477a97fef6904cd1642c1da2b230b66ad3364d8574` | Tracked and unchanged |
| `analysis/truncation-consequences.csv` | `84c1769c98d737f2e65e53c1ea105cca9c01e7f36c39713112c6649a2f92c40c` | Modified; differs from the migration baseline |
| `analysis/truncation-refinement.csv` | `bf3b3c80cc7b9ee37da00ad02735368a9b1b5b281d5af56098f77a2cc0d09b20` | Untracked |
| `analysis/truncation-summary.csv` | `5c18c4d8506f0a4e54b921cb7d508862c9ed8067bf879a1fe5e403a8a15a7575` | Modified; differs from the migration baseline |

The package action produced these derived tables byte-exactly during the audit:

- `diagnostic-catalog.csv`:
  `a9f4d39af6fe682f4964ef0c3c9bc2f4a7ddc1595700faae1589681ea2bf0e5c`;
- `sampled-range-decisions.csv`:
  `724f6ea95cd798b643efcfe7ae728f9dc9f019a27ebaf90b4279c7f2a11e1848`.

## Scratch reproducibility check

The complete dirty experiment directory was copied to temporary scratch; the primary
worktree remained untouched. The three generation routes were run with:

- CPython 3.14.6;
- NumPy 2.5.1;
- pandas 3.0.6;
- Matplotlib 3.11.1; and
- Ghostscript 10.04.0 for PDF raster comparison.

The five scratch-generated PNG pixel arrays were exactly equal to the five observed
candidate PNG pixel arrays. Their raw PNG bytes differed because the observed candidates
identify Matplotlib 3.11.2 in PNG metadata while the scratch runtime used Matplotlib
3.11.1. The five scratch-generated PDFs likewise differed as raw files, but each
Ghostscript 150-dpi rendering was byte-exact against its observed candidate PDF. This is
rendering parity from the observed dirty source graph, not recovery of an authenticated
original execution environment.

The initial audit did not run a scientific producer, change any table, or establish that
the source tables themselves came from a retained calculate → independently verify
lifecycle.

## Authorized recovery

The operator authorized the recommended complete-source recovery. The calculation owner
now contains:

- the structured nonflat and truncation implementation, strict serializers, schemas,
  and independent verifiers under [`workflow/`](workflow/);
- the producer, refinement, packaging, and rendering effect adapters;
- all 14 source tables, the two derived diagnostic tables, the five formerly missing
  figure pairs, and four other changed development figure pairs;
- the four analysis narratives and focused software-verification tests; and
- [`recovered-development-source-manifest.json`](recovered-development-source-manifest.json),
  which binds 55 exact-byte copies and 23 explicit path/ownership/style adaptations to the
  dirty donor state and gives six source-only dispositions.

The dirty donor `pyproject.toml` and `uv.lock` are identified in the manifest but were
not activated: adding a direct pandas dependency remains a separately protected
dependency action. Pandas 3.0.6 was already present in the locked project development
environment used for the bounded recovery checks.

After adaptation, 33 focused tests passed. The parent-family producer reproduced both of
its tables byte-exactly. A combined full producer rerun exceeded a 900-second command
window during the truncation sweep; the recovered donor graph had already produced the
complete table and figure inventory in the initial scratch audit. The calculation-owned
diagnostic packager reproduced the 110-row catalog and 660-decision table byte-exactly.
All five recovered PNG pixel arrays and all five 150-dpi Ghostscript PDF renderings were
again exact against the observed predecessor candidates. Removal-readiness review found
that the dirty scientific-story pair duplicated the separately qualified historical
presentation copy. The maintained scientific-story PDF, PNG, and plotter were restored
to their pre-recovery calculation identities. The rejected dirty PDF and PNG remain
exactly Git-recoverable from recovery revision
`011eee90f7be30770dd5fb2db844fe35633755fc`; the dirty plotter has an exact recorded
source hash and a Git-recoverable calculation-path-adapted candidate. All three have
explicit source-only dispositions.

The Ragasa2026a version-3 manuscript and supplement now consume the five PDFs from
`analysis/development/figures/` under this calculation owner rather than from the
experiment tree. Scratch `latexmk` builds completed for both 21-page PDFs. The main
source retains undefined `Ragasa2026b`--`d` citations and the supplement retains two
undefined Marzari citations; these bibliography issues are independent of the recovered
figure-input blocker.

## Disposition and remaining gates

The five files are now **maintained development publication inputs** with exact
calculation-side bytes and predecessor identities. They are not retained evidence. The
recovery does not authenticate the unknown original Matplotlib 3.11.2 execution, freeze
a protocol, create a retained calculate → independently verify → render execution, or
establish scientific validation.

A clean manuscript build may use the recovered calculation-owned PDFs. Any claim that
they are retained evidence remains blocked until the family has a reviewed direct typed
lifecycle, frozen inputs and tolerances, an authorized retained execution, complete
provenance, and retained-package verification.
