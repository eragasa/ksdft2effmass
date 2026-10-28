# Rank-one Fourier-locality donor crosswalk

## Audit boundary

This crosswalk inventories behavior that may inform the compatible rank-one control. It
does not adopt a donor's scientific identity, numerical result, evidence status, wire,
or claim. The audit baseline is merged revision
`bc1601f3a50dda19b994eea474ca522f2d836c26` unless another revision is stated.

The successor must be written from the reviewed rank-one protocol and canonical source
owners. It must not import, copy, wrap, subclass, or execute a calculation-local
`workflow/` package.

## Exact donors

| Donor | Exact identity | Permitted role |
|---|---|---|
| Direct Mathieu1D package | tree `a4d7f6bca1e1253feb99b340ac6ff555971722a5` at `bc1601f3` | Typed-record, byte-owning verification, authenticated-projection, direct-script, and report mechanics only. |
| Current installed M1 owner | tree `084e4a02aa22513a1e11e0c1a484bf23677814d3` at `bc1601f3` | Behavioral baseline for transform, truncation, fit, Parseval, Hermiticity, and disjoint-evaluation composition. Its Action API and schema-v1 wire are scheduled for replacement. |
| Historical ICMSEP M1 package | tree `418999a90efa3001d2e50a2e7912f126bc30903f` at `c5d34a93b4710a4a430738c404c775865d418d42` | Exact finite-data and plot-channel parity reference only. Result SHA-256 `c7262e3527a58dfd8fe237fa495549c53a1a65f3e46a98ed6d40673f14b6a394`; figure-data SHA-256 `300ea7b2bd42b21cf52b079edcbab5f80850dbf4b760c78100e0ea744a139110`. |
| Rank-two controlled-family workflow | tree `9ba77fc1fea2ee4957678c70baaa00a7a08d3d46` at `bc1601f3` | Read-only convention and parent-candidate reference. It is development calculation code, not an import or implementation donor. |
| Canonical solid-state operations | tree `e62e325a53e876f270dfc149f9906d21105b413f` at `bc1601f3` | Reusable reciprocal mesh, Fourier transform, interpolation, truncation, and hopping records where meanings are unchanged. |
| Canonical analysis operations | tree `fe528544ce0502b01cfa746cb0e3014204d84157` at `bc1601f3` | Reusable fit, route-comparison, Parseval, Hermiticity, scalar-band-shape, and band-error behavior where meanings are unchanged. |

## Channel dispositions

`Adopt` means reuse an existing canonical operation with unchanged meaning. `Adapt`
means define a new rank-one owner while preserving the stated behavior. `Reject` means
the channel is outside this study. `Provenance-only` means exact historical bytes remain
an audit reference but are not runtime inputs.

| Donor channel | Disposition | Rank-one successor boundary |
|---|---|---|
| Half-open reduced momentum period and centered cell representatives | Adopt | Declare `q ∈ [-1/2, 1/2)`, forward negative exponent, inverse positive exponent, forward factor `1/N`, and centered Born--von Karman representatives. |
| Complete reciprocal-to-hopping transform and inverse reconstruction | Adopt | Use the canonical solid-state transformer and independently reconstruct coefficients and samples in the verifier. |
| Symmetric ordinary-lattice support truncation | Adopt | Keep truncation separate from the complete cyclic transform and exclude the cyclic Nyquist representative from ordinary support claims. |
| Equal-weight direct least-squares route | Adopt | Fit exactly the declared support on construction samples and compare it with transform-mediated truncation; do not average routes. |
| Mathieu range-indexed support/error--locality table | Adapt | Retain mediated training/evaluation errors, omitted-block L2 norm, direct-fit total error, and direct/mediated coefficient and sampled defects for the selected parent. Add the separate three-channel interpolation/truncation/total decomposition. Derive only the prospectively frozen per-mesh two-objective attained error--complexity mask; do not relabel direct-fit residuals as transform channels or claim the mask was serialized by the donor. |
| Parseval partition, hopping Hermiticity, scalar imaginary residual, and bandwidth/curvature diagnostics | Adopt | Preserve units and named diagnostics; qualification tolerances remain pending scientific freeze. |
| Disjoint staggered evaluation mesh | Adapt | Preserve construction/evaluation role separation, but freeze the exact construction and evaluation extents prospectively for this family. |
| M1 plane-wave and finite-difference parent refinement | Reject | These diagnose the Mathieu/cosine differential parent and are not a channel of the compatible controlled-family scalar result. |
| M1 `0.5 cos(x)` parent, cutoff inventory, and retained values | Reject | They remain Mathieu/M1 provenance and cannot define this family's parent or result. |
| M1 schema-v1 serializer, typed-object verifier input, Action signature, calculation identity, and evidence class | Reject | Replace with family-owned immutable records, canonical bytes, and a verifier that owns exact result bytes. |
| Historical M1 result, verification, PNG, CSV, report, and checksum package | Provenance-only | Use only to test mapped transform/truncation/fit/withheld data-channel semantics; do not redirect its claims or identity. |
| Mathieu1D configuration and result layouts | Reject | The rank-one control has no plane-wave/finite-difference refinement sections and no Mathieu calculation identity. |
| Mathieu1D `BaseTypedRecord`, verifier admission, authenticated projection, generic PNG renderer, and atomic direct stages | Adapt | Follow the behavior, but define rank-one-specific records, comparisons, projection, plot composition, and paths. |
| Rank-two phase/global/pointwise/known-inverse alignment channels | Reject | Scalar `U(1)` conjugation is operator-trivial. Record one exact applicability result; emit no duplicate numerical alignment channels. |
| Rank-two external-gap and frame-transport gates | Adapt | Retain a sampled first-to-second eigenvalue-gap qualification because the selected scalar field is derived from an ambient parent. Do not call this global isolation. Frame transport is never needed for the scalar represented operator. |
| Rank-two finite cyclic representation, ordinary truncation, disjoint evaluation, and separated interpolation/truncation/total errors | Adopt | Preserve the channel separation and units in family-owned result sections. |
| Formal certificate supplement | Reject for Phase 2 runtime | No formal request/result wire or checked certificate exists. Native-only rendering is the closed initial inventory. |

## Selected source ownership

If the scientific controls are approved, the successor source child is
`ksdft2effmass.periodic1d.fourier_locality`. It owns only the compatible rank-one
configuration, parent-field composition, correlated result sections, independent
verification composition, authenticated visualization projection, and deliberate public
exports.

Existing canonical owners retain reusable behavior:

- `ksdft2effmass.solidstate` owns reciprocal meshes, hopping transforms,
  interpolation, truncation, and hopping records;
- `ksdft2effmass.analysis` owns hopping diagnostics, fits, route comparisons, and
  scalar band-error behavior;
- `ksdft2effmass.model_systems` shared infrastructure owns byte admission,
  verification/projection correlation, and generic PNG encoding; and
- the calculation root owns scientific controls, thresholds, execution identity,
  evidence state, provenance, report composition, and the native figure inventory.

No compatibility facade or universal Periodic1D result is introduced.

## Consumer audit

At `bc1601f3`, the live `ksdft2effmass.periodic1d.isolated_band` surface has one direct
external Python consumer: its package-aligned software-verification module
`python/tests/software_verification/ksdft2effmass/periodic1d/test__Periodic1DIsolatedBandCalculator.py`.
Internal root re-exports and Sphinx pages remain migration obligations. The formerly
listed Mathieu1D consumers are absent after Phase 1.

The historical M1 publication path remains a Git-only provenance donor. No current
publication is silently redirected to the future rank-one control, and no donor result
will be presented as a result of this family.

## Audit conclusion

The reusable behavior and prohibited inheritance are now explicit. The scalar parent and exact energy reference are frozen in
[`scientific-control-decision.md`](scientific-control-decision.md), and the finite
numerical controls are frozen in
[`numerical-control-decision.md`](numerical-control-decision.md). The next gate is design
and review of the family-owned typed records, byte-owning independent verification, and
authenticated visualization projection before any stage script or execution exists.
