# Wannier90 3.1.0 bundled tutorial campaign

## Purpose

This campaign maps every bundled example directory from the retained Wannier90 3.1.0 source distribution to a canonical Task. It is an inventory and control surface only: no Task is activated, no run workspace is created, and no scientific executable is authorized by this page.

Tutorial observations are learning evidence. They cannot establish project production convergence, numerical verification, scientific validation, or acceptance, and they cannot satisfy `bulk-silicon.wannier-reference`.

## Source identity

| Item | Identity |
|---|---|
| Release | Wannier90 3.1.0 |
| Retained archive | `/Users/eugene/projects/wannier90-3.1.0-installation/wannier90-3.1.0.tar.gz` |
| Archive SHA-256 | `40651a9832eb93dec20a8360dd535262c261c34e13c41b6755fa6915c936b254` |
| Examples files | 223 |
| Examples path-and-content manifest SHA-256 | `5e1bdab05760151d07c43307ae0d3d4d1e54aeffa92f7a143c1188da73b95514` |
| Inventory result | 32 numbered examples represented by 33 source directories because example16 has `-noqe` and `-withqe` variants |

The manifest digest is SHA-256 over lexicographically sorted lines of the form `<file-sha256>  <path-relative-to-examples>\n`. The extracted examples tree is byte-identical to all 223 corresponding files in the retained archive. Example32 exists in the release archive but is omitted from the release's examples README; it remains inventoried from the authoritative source-directory contents and is not inferred to have an undocumented scientific purpose beyond its inputs.

The retained source inputs and source-distribution `doc/compiled_docs/tutorial.pdf` and `doc/compiled_docs/solution_booklet.pdf` are authoritative. Private Project Koios documentation-derived notes are read in place only as `AUTOMATED_UNREVIEWED` learning and procedure aids. Their content and storage locations are not copied into Git. The notes cover all 32 numbered tutorials, with Tutorial 16 mapping to the two source-directory Tasks.

## Campaign controls

- Parent Task: [`wannier90.tutorials.v3_1_0`](../../tasks/simulation/wannier90.tutorials.v3_1_0.json).
- Generic umbrella: [`wannier90.tutorials`](../../tasks/simulation/wannier90.tutorials.json).
- Campaign review: [`wannier90.tutorials.v3_1_0.review`](../../tasks/simulation/wannier90.tutorials.v3_1_0.review.json).
- Example05 is the first blocked candidate; example11 depends on its disposition and remains a separately authorized second candidate.
- Example05's proposed five-stage route is SCF → 64-point uniform-grid NSCF → `wannier90.x -pp diamond` → `pw2wannier90.x` → `wannier90.x diamond`.
- The private Tutorial 11 note compresses away NSCF, preprocessing, and `pw2wannier90`; this is a known note omission, not authority to skip those stages. Tutorial 11 uses the complete SCF → uniform-grid NSCF → preprocessing → interface → localization route and requires a separate valence-only versus eight-function valence-plus-conduction/window decision.
- The remaining 31 source-directory Tasks are deliberately deferred, not active.
- Every invocation requires its own exact protected-execution authorization, limits, stage sequence, warning rule, retention plan, and stop conditions.
- The GPLv2 statement for the Wannier90 code is not treated as explicit pseudopotential or separately authored input-data terms. Terms remain an independent preflight requirement.
- The known GNU Fortran IEEE summary must remain visible and receive the operator-approved disposition for any applicable Quantum ESPRESSO stage.

## Task inventory

| Task | Source directory | Topic | Route | Files | Manifest SHA-256 | Status |
|---|---|---|---|---:|---|---|
| [`wannier90.tutorials.v3_1_0.example01`](../../tasks/simulation/wannier90.tutorials.v3_1_0.example01.json) | `examples/example01` | Gallium arsenide valence bands | supplied matrices → Wannier90 | 11 | `c0151bb5bc13fcecf4267cd96917faec527c53cffdb797ae0a344a15387a7823` | `deferred` |
| [`wannier90.tutorials.v3_1_0.example02`](../../tasks/simulation/wannier90.tutorials.v3_1_0.example02.json) | `examples/example02` | Lead four-state Fermi surface | supplied matrices → Wannier90 | 4 | `85e72e5cec1f85bdcef0b1ec7d7b1c0528bc665bfee8c4e0548e6b9be0cd4c93` | `deferred` |
| [`wannier90.tutorials.v3_1_0.example03`](../../tasks/simulation/wannier90.tutorials.v3_1_0.example03.json) | `examples/example03` | Silicon valence-plus-conduction interpolation | supplied matrices → Wannier90 | 4 | `72a4565368e03740e4b6ad9b561b38fda2a9718b79eade30817f25d14a124e2a` | `deferred` |
| [`wannier90.tutorials.v3_1_0.example04`](../../tasks/simulation/wannier90.tutorials.v3_1_0.example04.json) | `examples/example04` | Copper Fermi-surface interpolation | supplied matrices → Wannier90 | 4 | `b39c47a4b6ba9aeeead576f29f6f05ac52938c7ff7588fa68e060b581c1e94a8` | `deferred` |
| [`wannier90.tutorials.v3_1_0.example05`](../../tasks/simulation/wannier90.tutorials.v3_1_0.example05.json) | `examples/example05` | Diamond valence states | QE → pw2wannier90 → Wannier90 | 4 | `3994b438ccd2002eed09175c9a505d9babe08492cf5097711441321fdc382b2e` | `blocked` |
| [`wannier90.tutorials.v3_1_0.example06`](../../tasks/simulation/wannier90.tutorials.v3_1_0.example06.json) | `examples/example06` | Copper Fermi-surface workflow | QE → pw2wannier90 → Wannier90 | 4 | `077f1ef4ca53ee63eb60db5eb22990e4b6b5f6e46669c755e8fe58ab0734d513` | `deferred` |
| [`wannier90.tutorials.v3_1_0.example07`](../../tasks/simulation/wannier90.tutorials.v3_1_0.example07.json) | `examples/example07` | Silane valence states | QE → pw2wannier90 → Wannier90 | 4 | `441067041215e94043f2cfc765d853dbeed955e8a4d6051366d5de29e27b5c29` | `deferred` |
| [`wannier90.tutorials.v3_1_0.example08`](../../tasks/simulation/wannier90.tutorials.v3_1_0.example08.json) | `examples/example08` | Iron states around the Fermi level | QE → pw2wannier90 → Wannier90 | 6 | `9b2062a0125408ca7851b79c7e13ce7a6c507e7bd604ee3c86a41f63a1161f9e` | `deferred` |
| [`wannier90.tutorials.v3_1_0.example09`](../../tasks/simulation/wannier90.tutorials.v3_1_0.example09.json) | `examples/example09` | Barium titanate | QE → pw2wannier90 → Wannier90 | 4 | `1702f5021e1532090544b6c2f441277f55c851f9900585a3efe091a76fd17807` | `deferred` |
| [`wannier90.tutorials.v3_1_0.example10`](../../tasks/simulation/wannier90.tutorials.v3_1_0.example10.json) | `examples/example10` | Graphite | QE → pw2wannier90 → Wannier90 | 4 | `30691233a8125200e86b4f214949525c7526ee4033843cbee2d6bb529ca083fe` | `deferred` |
| [`wannier90.tutorials.v3_1_0.example11`](../../tasks/simulation/wannier90.tutorials.v3_1_0.example11.json) | `examples/example11` | Silicon Wannierization | QE → pw2wannier90 → Wannier90 | 4 | `29a2acef7afedb57b5fad1f84bd6cbe372741788a16e01a99cf9166207038ad2` | `blocked` |
| [`wannier90.tutorials.v3_1_0.example12`](../../tasks/simulation/wannier90.tutorials.v3_1_0.example12.json) | `examples/example12` | Benzene gamma-only workflow | QE → pw2wannier90 → Wannier90 | 4 | `3d8da71e3ecfc2715d11d81f0a495bb08ff7bd05963d582bb1b47e19422fe99c` | `deferred` |
| [`wannier90.tutorials.v3_1_0.example13`](../../tasks/simulation/wannier90.tutorials.v3_1_0.example13.json) | `examples/example13` | Carbon nanotube transport | QE → pw2wannier90 → Wannier90 | 4 | `3632566262b6d81476a3f8d556f65310e05f8aed314962eeb396f3982c1045e2` | `deferred` |
| [`wannier90.tutorials.v3_1_0.example14`](../../tasks/simulation/wannier90.tutorials.v3_1_0.example14.json) | `examples/example14` | Sodium-chain LCR transport | QE → pw2wannier90 → Wannier90 | 8 | `28a3c9772348279ce758185667ee53157aead44dede42a0fcf275e707cb2e855` | `deferred` |
| [`wannier90.tutorials.v3_1_0.example15`](../../tasks/simulation/wannier90.tutorials.v3_1_0.example15.json) | `examples/example15` | Carbon-nanotube LCR transport | QE → pw2wannier90 → Wannier90 | 8 | `1215e5ed9b41cb33d5ca708b8e9e94f028a711c29b363760d58eda2e9588f4db` | `deferred` |
| [`wannier90.tutorials.v3_1_0.example16-noqe`](../../tasks/simulation/wannier90.tutorials.v3_1_0.example16-noqe.json) | `examples/example16-noqe` | Silicon BoltzWann from supplied matrices | supplied matrices → Wannier90 | 4 | `b939ba17bf7a71d570c7111fd315cb3743c3d4af99b1942075592d435d74ff30` | `deferred` |
| [`wannier90.tutorials.v3_1_0.example16-withqe`](../../tasks/simulation/wannier90.tutorials.v3_1_0.example16-withqe.json) | `examples/example16-withqe` | Silicon BoltzWann with Quantum ESPRESSO | QE → pw2wannier90 → Wannier90 | 4 | `9775f60b6036df7e841e2a0997467db6350b8c8bf23cb16356b21372ab9fd17c` | `deferred` |
| [`wannier90.tutorials.v3_1_0.example17`](../../tasks/simulation/wannier90.tutorials.v3_1_0.example17.json) | `examples/example17` | Iron spin-orbit bands and Fermi contours | QE → pw2wannier90 → Wannier90 | 7 | `062bd5898524a50df006ad1f13b4870ac721915697557b756b21e80c7a7f67db` | `deferred` |
| [`wannier90.tutorials.v3_1_0.example18`](../../tasks/simulation/wannier90.tutorials.v3_1_0.example18.json) | `examples/example18` | Iron Berry curvature and anomalous Hall conductivity | QE → pw2wannier90 → Wannier90 | 4 | `760ac070fce3feb839dc1849e1904a9265bf275dad261a0cf71896e79ed4a3aa` | `deferred` |
| [`wannier90.tutorials.v3_1_0.example19`](../../tasks/simulation/wannier90.tutorials.v3_1_0.example19.json) | `examples/example19` | Iron orbital magnetization | QE → pw2wannier90 → Wannier90 | 4 | `1f69bac6d990d028005a6f421210dec31ee978c68388fd377ccf402109da2242` | `deferred` |
| [`wannier90.tutorials.v3_1_0.example20`](../../tasks/simulation/wannier90.tutorials.v3_1_0.example20.json) | `examples/example20` | Lanthanum vanadate regional disentanglement | QE → pw2wannier90 → Wannier90 | 12 | `adfc3137d649d3c33ff64dbba03b86c237c3f0bda944b8756d060c0abf84a30f` | `deferred` |
| [`wannier90.tutorials.v3_1_0.example21`](../../tasks/simulation/wannier90.tutorials.v3_1_0.example21.json) | `examples/example21` | Gallium arsenide symmetry-adapted Wannier functions | QE → pw2wannier90 → Wannier90 | 21 | `38d7f756a3f7cdbeb7c8bc85bf638f25f8023db05624bf5d63ea04679eda3bc4` | `deferred` |
| [`wannier90.tutorials.v3_1_0.example22`](../../tasks/simulation/wannier90.tutorials.v3_1_0.example22.json) | `examples/example22` | Copper symmetry-adapted Wannier functions | QE → pw2wannier90 → Wannier90 | 14 | `76b0f317789f084a36cc34741b5469bcdb9d23374ba3f19ad977285f551a7935` | `deferred` |
| [`wannier90.tutorials.v3_1_0.example23`](../../tasks/simulation/wannier90.tutorials.v3_1_0.example23.json) | `examples/example23` | Silicon G0W0 band interpolation | QE → pw2wannier90 → Wannier90 | 10 | `d5e36cbd5cae9f757e42f62541a27c4d259f806b53f14084b71946bfa1169eef` | `deferred` |
| [`wannier90.tutorials.v3_1_0.example24`](../../tasks/simulation/wannier90.tutorials.v3_1_0.example24.json) | `examples/example24` | Tellurium gyrotropic effects | QE → pw2wannier90 → Wannier90 | 26 | `082b3d3585f94af1f2eeeb938bd26b0e1d647c56b90e12f2306dfcd28b795537` | `deferred` |
| [`wannier90.tutorials.v3_1_0.example25`](../../tasks/simulation/wannier90.tutorials.v3_1_0.example25.json) | `examples/example25` | Gallium arsenide nonlinear shift current | QE → pw2wannier90 → Wannier90 | 4 | `1cc3dc41a9862fb19ec6263ba9f8d474f55e81fbe1ade148f772e2ac3fdbe311` | `deferred` |
| [`wannier90.tutorials.v3_1_0.example26`](../../tasks/simulation/wannier90.tutorials.v3_1_0.example26.json) | `examples/example26` | Gallium arsenide selective localization | QE → pw2wannier90 → Wannier90 | 4 | `d65f52b2e532e0fbd9ddfc28c3b19db148aa418976908461c0574c3de8684dc7` | `deferred` |
| [`wannier90.tutorials.v3_1_0.example27`](../../tasks/simulation/wannier90.tutorials.v3_1_0.example27.json) | `examples/example27` | Silicon SCDM automated localization | QE → pw2wannier90 → Wannier90 | 9 | `18f5c9d611494247f2c821c2641fdef2c33a0ce5451cffda4a6dfb84c0ea7baf` | `deferred` |
| [`wannier90.tutorials.v3_1_0.example28`](../../tasks/simulation/wannier90.tutorials.v3_1_0.example28.json) | `examples/example28` | Diamond Wannier-function plotting | QE → pw2wannier90 → Wannier90 | 4 | `e9ac6f9ad647655af49a8eca1c7011bf4364f6ccb1ed984b81d20204ca120a34` | `deferred` |
| [`wannier90.tutorials.v3_1_0.example29`](../../tasks/simulation/wannier90.tutorials.v3_1_0.example29.json) | `examples/example29` | Platinum spin Hall conductivity | QE → pw2wannier90 → Wannier90 | 4 | `c043cf6d0518f29463f436b332ca14a766ccc7809fd8e7810b4b12ab23d26114` | `deferred` |
| [`wannier90.tutorials.v3_1_0.example30`](../../tasks/simulation/wannier90.tutorials.v3_1_0.example30.json) | `examples/example30` | Gallium arsenide AC spin Hall conductivity | QE → pw2wannier90 → Wannier90 | 4 | `cd618ba05340a2fed6685e413df83b3c419f11906577e08d3ae2f49719ccfc2c` | `deferred` |
| [`wannier90.tutorials.v3_1_0.example31`](../../tasks/simulation/wannier90.tutorials.v3_1_0.example31.json) | `examples/example31` | Platinum spinor SCDM localization | QE → pw2wannier90 → Wannier90 | 4 | `8e30b41ce52e39f7f8fa80c047acd2e968c41675f38dfaefe408e442f2c6bf8a` | `deferred` |
| [`wannier90.tutorials.v3_1_0.example32`](../../tasks/simulation/wannier90.tutorials.v3_1_0.example32.json) | `examples/example32` | Tungsten automated projections | QE → pw2wannier90 → Wannier90 | 6 | `7f724f5ca6f70f85c45d93b318cd32022518ab048f3f2182deaa34bb383f04ed` | `deferred` |

## Extraction and Koios return path

For each authorized Quantum ESPRESSO stage, ksdft2effmass owns the exact native output identity, manifest, streams, diagnostics, and semantic extraction. Compact QEXSD metadata must be retained before a later stage can overwrite shared save-state metadata. Supported QEXSD documents are serialized as canonical `KohnShamPlaneWaveCalculationRecord` JSON with explicit provenance and limitations; a missing or unsupported document receives an explicit disposition.

For each authorized Wannier90 stage, emitted `.eig`, `.amn`, `.mmn`, `.nnkp`, `.wout`, `_u.mat`, and `_hr.dat` files are inventoried and assessed against the existing typed parsers. Those parsers do not yet constitute a canonical cross-repository serialized Wannier result.

Koios may later ingest canonical semantic records as prior computational learning evidence for retrieval and review. That return path requires a separately accepted content-addressed handoff and private-locator policy because the current plane-wave JSON provenance includes an absolute `source_path`. Native workspaces and private absolute paths are never the handoff interface.

## Evidence boundaries

Any future run must preserve exact input and executable identities, pseudopotential or supplied-matrix provenance and terms, stage commands, standard streams, warnings, runtimes, exit states, and compact artifact inventories. Dense native outputs and mutable workspaces remain outside Git.

A completed tutorial demonstrates only the represented operational behavior under its retained conditions. It does not choose production projections or windows, prove basis or gauge alignment, establish effective-mass accuracy, or activate production successors.
