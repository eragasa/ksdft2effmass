# Legacy M2 source retirement

## Scope and authorization

After the direct composite-band alignment lifecycle and the constrained-admissible-set
consumer migration were completed and reviewed, the operator explicitly authorized
retirement of the installed M2 `periodic1d.multiband_alignment` surface. The retirement
removes ten tracked files: six installed M2 modules, the now-unused block-Hamiltonian toy
parent, the sole aggregate M2 test, and two obsolete Sphinx API pages. It also removes
the block-parent and eight M2 exports from the surviving `periodic1d` package root and
removes the retired pages from the controlled-study toctree.

The replacement is not a compatibility facade. The composite family owns immutable
configuration and result records, exact canonical bytes, request-bound analysis,
independent byte-owning verification, authenticated visualization data, and direct effect
adapters. M3 consumes authenticated canonical composite-result bytes and an explicit
composite verifier; it does not produce or decode M2 at runtime. Historical Architecture
v2 pages remain historical records.

## Scientific disposition

The direct composite successor adopts or explicitly adapts the M2 parent coefficients,
retained rank, fixed attack, pointwise and global alignment families, represented
operators, Fourier transforms, range inventory, and disjoint construction/evaluation
roles as recorded in `m2-parity.md` and `phase-3-split-audit.md`. It separately records
cyclic-conversion power, ordinary omitted-block norms, interpolation error, deliberate
truncation error, and total finite-range consequence.

The M2 schema-v1 wire, object-input verifier, empty-callable producer/verifier signatures,
generic block-parent service boundary, and aggregate test are provenance-only. Removing
them does not relabel the successor result as historical M2 evidence and does not alter
historical publication or evidence manifests.

This source retirement creates no retained execution, evidence seal, publication update,
scientific validation, release, or Formal certificate.

## Recovery authority

Every removed byte is recoverable from revision
`f7e5834c9425511d59a98fc564bc5b2000fca345`.

| Recovery property | Value |
|---|---|
| Removed file count | 10 |
| Installed `multiband_alignment/` tree | `9f5199e10324e5b1f46d18525b7738397ce62b2e` |
| Sorted path-inventory SHA-256 | `ab2e1a657e64e663b3069d89e48ac1592fece8a8aa2a4ec6bb623aee62f3aa3f` |
| Sorted path-and-content-digest SHA-256 | `e2051f0450a0c6a204334f521b7c701e38b31859f88ff819baae1c99e46eb104` |

The retired inventory is:

| Path | Git blob | SHA-256 |
|---|---|---|
| `doc/sphinx/api/ksdft2effmass/periodic1d/model.rst` | `675a79c46fc72568d0d025952541c58c27c72c3a` | `60179b322d13aa0857ab380ef1bdccc6f312e0809f2fe77e6b1ddb0ff6aac9cd` |
| `doc/sphinx/api/ksdft2effmass/periodic1d/multiband_alignment.rst` | `24bb5ff26a3e55e13ce385ab206aec8723dab447` | `e8dcb8eb0367f3fae10f327919b2cc425111ca1d79637cc13ce47301ad377c86` |
| `python/src/ksdft2effmass/periodic1d/model.py` | `68b0126ea0649ac74755bb6fb2eec844bbb06516` | `65eeebeea9fc7af3c073fc0518b3ca4f8884add5f20f7d6525374e2bda174bd0` |
| `python/src/ksdft2effmass/periodic1d/multiband_alignment/__init__.py` | `929f5b1ba4f0f05d982c9338ced6a9ee3b270dee` | `f60f3416955ef872375bd7b16a007bfc02a3b1ccaa0d40cd071fd73e949bbdbb` |
| `python/src/ksdft2effmass/periodic1d/multiband_alignment/calculate.py` | `335244820740fa601944327e2570a7851ed53354` | `0f18afe2b550b138dac67fa083a12983d6456f6c044034d73e4cc13ac68f53a6` |
| `python/src/ksdft2effmass/periodic1d/multiband_alignment/definition.py` | `058016f7f4194d2a4ff13c621fa7db99f00f56cc` | `e664c32f51ac2357d6d6e8da9b1b5c9f7fdcefe8dbc23a38d187f90b4f5f23d7` |
| `python/src/ksdft2effmass/periodic1d/multiband_alignment/results.py` | `91fa737954d391fcdbb7baefe30ce18e45e88107` | `d61138ded8797ae15b26c565f873de1e41f0b95cac03a9aa7751e042cb81e9a8` |
| `python/src/ksdft2effmass/periodic1d/multiband_alignment/serialization.py` | `f8ca63deb2719f02fe8f9627e8fd49f4670d4617` | `1466466e1eea6f8fba3bf839532b4f853fa265a9344ea07568e1b142011d1ffd` |
| `python/src/ksdft2effmass/periodic1d/multiband_alignment/verify.py` | `990ee34d1fbaaa9929508d83483ec5e6d00fcd79` | `afe0d4388051bf1d790773ce1c914e766e440d5851d9d38678f9e5f5604a648e` |
| `python/tests/software_verification/ksdft2effmass/periodic1d/test__Periodic1DMultibandAlignmentCalculator.py` | `faa1fcb8b2b4941bfe4dd04f34f893c9152ed6d4` | `88f224ef26c9e5b1564d362d630bad5922fd85481fd209d8cc60fdfa71890402` |

The modified aggregate surfaces are recoverable from the same revision:

| Path | Predecessor Git blob | Predecessor SHA-256 |
|---|---|---|
| `python/src/ksdft2effmass/periodic1d/__init__.py` | `3b09727859c44c0b2864166a29514aa8bb0fde80` | `43468f205740d393ad753d2c0f75ce653f2b20d2a885178c72670899bb4b79e8` |
| `doc/sphinx/api/controlled-periodic-studies.rst` | `44eee0793a925ccf25a2298d6b26ec62ac362142` | `024e8f1364c820ab16920d029b0a107eca202ea7c3730aee46719de282da659` |

For example:

```console
git show f7e5834c9425511d59a98fc564bc5b2000fca345:python/src/ksdft2effmass/periodic1d/multiband_alignment/results.py
```

Recovery establishes byte availability only. It does not reactivate the predecessor as
a supported API, wire, calculation identity, or evidence package.

## Package-aligned test ownership

The composite-alignment configuration, analyzer, result, independent verifier,
visualization, direct-script, public-surface, and parity tests replace the predecessor's
single aggregate test. The public-surface test rejects the retired package, block-parent
module, and former root exports rather than preserving aliases.
