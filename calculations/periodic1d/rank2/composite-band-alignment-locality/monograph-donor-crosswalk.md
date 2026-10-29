# Research-monograph composite donor crosswalk

## Scope and recovery authority

This audit asks which parts of the removed research-monograph periodic-one-dimensional
composite calculation are scientifically relevant to the direct 64/257 rank-two
successor. The donor is a parity and provenance reference, not a runtime input, schema,
or compatibility API.

The recovery revision is
`c5d34a93b4710a4a430738c404c775865d418d42`. Its
`calculations/research-monograph/periodic-1d/` tree contains 39 files. The full sorted
path inventory has SHA-256
`af77724a1734d90cc546c4041a31220503d342be6b24fcfd5a175ef4fdb528c6`; the sorted
`<content-sha256><two spaces><path><newline>` inventory has SHA-256
`1e7ad1c665734ba03cfb5ab1a03b303a17166bee92848a30c21aae3796857832`.
Every entry named by the historical `SHA256SUMS` file was reproduced from the recovered
bytes. These hashes establish identity only.

## Exact composite-file inventory

The ten-file composite subset has sorted path-inventory SHA-256
`92e803e524399639e299eb86ae78d839fab401c12f2cc23b9b8c5be567f2ca9a` and sorted
path/content-inventory SHA-256
`ea6ff29d1d3940643b0ca634975505463cdb47e89f6ecc07039295f3f459f4fb`.

| Historical path basename | Git blob | SHA-256 |
|---|---|---|
| `README.md` | `c63667619d08ff78c61134129cfcbdf9c99c5fec` | `d957296b75e91c95c280a74ccf20081a4bbfb5c42e722e14fe3e352d77d4cbe7` |
| `SHA256SUMS` | `31955d35e4de2f14b309592c0191c8b6f67e5dc5` | `ab5d5076b7e8f2bdbe45764c870634e7b1460feb54026cb4ffb2cfd9e85d0027` |
| `composite-input.json` | `f8d940e9a4f7026df31c5ed623c465376848923a` | `2ce60a96b72747a820c68b05aa9dbe0beaecb5de03fd5e336c9c77cc7bf5fc20` |
| `composite-report.md` | `74de591572c4156e530d996b9919d22d0fb9a29d` | `12b70eaa134b9f7f0f39106d0d6eed047b3f108ef5ab449c687f0ce0dfb54ade` |
| `composite-result.json` | `b5940ecd940de98cd1fcbbaa4a34dff05a97bae9` | `9231057d96be5e7277e5d76d7272a9bad0a00b02996b7e989164ab619e19c02f` |
| `composite-summary.png` | `a7fa63cc2bcb0a04e02388f0b137fec3145f337f` | `41d0234e28e0c71da3a4f78a4a942568e2116df2c8728258d6163c3beeb2532d` |
| `plot_composite.py` | `1567af80118544434e3e18755c68ce26852b09b9` | `1d493d74a3c60e8ab96e3af09569752e9591c776073390aecadd38666c8ff0da` |
| `protocol.md` | `b17a85e9e395e5a356c5082c9e10cbba431517af` | `fa8d0fa13d8e6fc116622e8cd33205903b340f695cda411c75e89ac500fcd1a3` |
| `run_composite.py` | `6ac1d72b56ad81766d08240392a63cc4ae0f81b9` | `c0f67b6a37ccb85f838e5c27295a52b1e1bd8c29f7b4eb2d565fe56104af2a3e` |
| `verify_composite.py` | `e07c7b05225d1a447342f02caf77eccd865d6e03` | `6636f0aa3293cbde74a1d3dccebf75cf45a1ba0bad8b35bff6c9a12a61adad96` |

The historical importable donors were
`campaigns.periodic_1d.composite`, `composite_results`,
`composite_verification`, `composite_verified_workflows`,
`model.retained.composite`, `run.composite.{correlate,data,verify}`, and
`serialization.composite`. The successor imports none of them.

## Exact external-consumer inventory

Nineteen historical files outside the donor directory contain the exact periodic-1D
composite paths or experiment identity. Their sorted path inventory has SHA-256
`cf0a32eafbf763a350583bef6bf28e45b4c43cf1b2e270d0e87a878ff7caccf2`; their sorted
path/content inventory has SHA-256
`9e67d59ffc4fa0cb4ebd38417b69965a52fb0bb05ae339c522500fd4b2727100`.

- six immutable `.pi/checkpoints/research-monograph-periodic-1d-*.json` records;
- eight impurity-defect-1D input, result, and protocol records;
- the research-monograph Appendix G source;
- one blind-alignment baseline-loader test; and
- three historical periodic-1D campaign serializer tests.

These consumers remain bound to historical bytes. This implementation does not redirect
them to the direct successor and does not authorize a publication or evidence-manifest
migration.

## Frozen donor controls

The donor experiment is `research-monograph.periodic-1d.composite.v1`. It uses a cosine
plane-wave parent with cutoff 15, construction size 128, withheld size 257, retained
pairs `low_pair=[0,1]` and `higher_pair=[2,3]`, ranges
`(0,1,2,3,4,6,8,12)`, direct-route range 4, controlled-gauge amplitude 0.73,
rough-gauge amplitude 1.1, and external-gap threshold `1e-8`.

## Scientific-channel disposition

| Donor channel | Disposition | Direct-successor treatment |
|---|---|---|
| Rank-two retained spectral frames and sampled external gap | **adapted** | Retains only the lowest rank-two space of the exact four-state parent and uses the M2 threshold `0.5 E_ref`; it does not adopt the plane-wave parent or higher pair. |
| Polar neighbor transport and closure information | **adopted** | The successor performs polar transport with identity sewing and stores the minimum overlap singular value and closure eigenphases. |
| Controlled/rough right-unitary gauge contrast | **adapted** | Replaced by the exact M2 attack `0.30 + 0.65 sin(2πk) + 0.30 sin(4πk)` and the names reference, attacked, and pointwise-aligned. |
| Pointwise Procrustes recovery | **adopted** | Recomputed with Optimization's right-action unitary selection and independently reconstructed with direct singular-value decomposition. |
| Smooth/rough represented reciprocal Hamiltonians | **adapted** | Stored as reference, attacked, pointwise-aligned, and one-global-unitary represented operators on 64 construction points. |
| Complete block Fourier transforms and reconstruction residuals | **adopted** | Applied to reference, attacked, and pointwise channels with centered representatives `[-32,31]`. |
| Symmetric range study and withheld spectral error | **adapted** | Uses the shared ranges through 8 on the exact 257-point staggered evaluation inventory; range 12 is rejected because it belongs to the 128-point donor. |
| Wilson-loop eigenphases and controlled-gauge Wilson set defects | **rejected** | The direct M2 successor is an alignment/locality calculation, not a Wilson-loop study. Closure phases are transport diagnostics only. |
| Direct-route coefficient and training-operator defects | **rejected** | No separately fitted direct route is part of the bounded successor result. |
| `higher_pair` retained group | **rejected** | The successor is fixed to the lowest two states of one exact four-state parent. |
| Plane-wave cutoff, cosine strength, physical period, and recoil units | **rejected** | They identify a different parent and unit convention. |
| Historical input/result/report/PNG bytes and internal identity hashes | **provenance-only** | They remain exact recovery and publication references and are never decoded by successor runtime code. |
| Campaign workflow, serializer, and schema-v1 layouts | **provenance-only** | Replaced by immutable typed records, canonical typed JSON, direct scripts, and verifier-owned projection authentication. |

## Closed implementation consequence

The monograph audit does not enlarge the fixed M2 successor. The direct result keeps the
parent spectra, four frame paths, pointwise and global transformations, four represented
operator paths, three complete Fourier transforms, diagnostics, and three-channel range
study. It deliberately omits campaign status prose, development sweeps, higher retained
groups, Wilson channels, direct fitting, and historical schemas.
