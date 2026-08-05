# Unresolved accepted H1/H3 resource-contract conflict

## Conflict

Accepted H1 makes the following relational states invalid at DataObject construction/deserialization:

- `ResourceReference` forbids self-dependency: `.pi/evidence/pi-harness-incubation/H1/field-and-wire-contract.md:80-92`; current implementation `python/src/ksdft2effmass/harness/pi/resources.py:48-76`.
- `ResourceManifest.resources` must be nonempty, ID-sorted, ID-unique, and path-unique: `.pi/evidence/pi-harness-incubation/H1/field-and-wire-contract.md:98-109`; current implementation `resources.py:79-111`.
- H1 wire failure returns `FAIL` and no record for invariant failure: `.pi/evidence/pi-harness-incubation/H1/contract-surface.md:102`.

At the same time, accepted H1 assigns relational diagnostics to `ValidateResourceManifest`, including duplicate ID/path and forbidden overlay replacement: `.pi/evidence/pi-harness-incubation/H1/contract-surface.md:104-105`; `.pi/evidence/pi-harness-incubation/H1/path-and-resource-resolution-contract.md:140-151,185-190`. The implementation action contains these checks, including `PIH.RESOURCE.OVERLAY_REPLACEMENT`, at `resources.py:170-335`.

Accepted H3 fixtures require those action-level outcomes:

- `harness/pi/fixtures/resource-resolution/oracle-index.json:13-29` requires `PIH.RESOURCE.DUPLICATE_ID` and `PIH.RESOURCE.DUPLICATE_PATH`.
- `harness/pi/fixtures/resource-resolution/oracle-index.json:49-65` requires `PIH.RESOURCE.OVERLAY_REPLACEMENT` for duplicate local ID/path.
- Concrete invalid manifests are in `cases/duplicate-resource-id.json:10-52` and `cases/duplicate-resource-path.json:10-52`; their expected action codes are at lines 142-146.
- Overlay fixtures place the duplicate/reused reference in a local manifest: `cases/local-overlay-duplicate-id.json:42-64,154-158` and `cases/local-overlay-duplicate-path.json:42-64,154-158`.
- H3 separately confirms strict self-dependency wire rejection as `PIH.WIRE.INVALID_VALUE` with no downstream record: `harness/pi/fixtures/semantic-invariants/oracle-index.json:46-56`.

## Consequence

Strict `DeserializeJsonRecord` must construct the selected accepted DataObject. For duplicate manifest ID/path or self-dependency, that constructor raises on an accepted H1 invariant. Deserialization must therefore return `PIH.WIRE.INVALID_VALUE` and `record = None`. `ValidateResourceManifest` cannot receive the invalid manifest and cannot emit the fixture-required `PIH.RESOURCE.DUPLICATE_ID`, `PIH.RESOURCE.DUPLICATE_PATH`, or, where a local manifest is itself constructor-invalid, `PIH.RESOURCE.OVERLAY_REPLACEMENT`.

No H2-only correction can satisfy both boundaries without either changing an accepted H1 public constructor/wire contract, changing accepted H3 fixtures/oracles, or fabricating/mutating an invalid frozen object. Fabricating invalid state would not verify the public contract and is not an acceptable correction.

## Defensible resolution options (none selected)

1. **Move relational validity to actions in a new accepted contract revision.** Keep field/type invariants in constructors but permit duplicate/self-relational represented records long enough for `ValidateResourceManifest` to emit action codes. This changes H1 constructor and wire behavior and requires synchronized schemas, fixtures, Python/Rust mappings, and compatibility review.
2. **Retain strict H1 constructors and revise H3 expectations.** Treat these fixtures as wire-invalid and require `PIH.WIRE.INVALID_VALUE` with no record; remove claims that the action receives them. This changes accepted H3 public resources/oracles and reduces action-code reachability.
3. **Introduce a separately versioned raw manifest input boundary.** Decode structural wire data into an explicitly non-public/non-validated representation, then validate into `ResourceManifest`. This adds a contract/interface and serialization boundary and requires a new accepted H1 version plus new H3 resources; it cannot be introduced by H2 alone.

Human/public-contract authority must select and authorize a synchronized H1/H3 correction. This record selects no option and makes no acceptance claim.
