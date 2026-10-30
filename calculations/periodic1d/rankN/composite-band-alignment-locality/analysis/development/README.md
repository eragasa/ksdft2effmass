# Development analysis

This package writes and reads canonical replaceable development-result cache bytes,
projects complete typed producer results into immutable plotting arrays, and renders the
fixed nine-figure inventory. It provides result-byte integrity and presentation reuse,
not scientific validation:

- each cached case uses canonical `BaseTypedRecord` bytes and a SHA-256 manifest;
- cache admission checks canonical decoding, exact byte round trips, digests, identities,
  and the complete 16-case inventory;
- cache admission explicitly records `scientific_evidence: false` and
  `independent_scientific_verification: false`;
- it does not independently recompute complete scientific quantities; and
- every image is labeled **DEVELOPMENT / UNVERIFIED — not publication evidence**.

The replaceable lifecycle is:

```text
run_01_calculation.py
  → results/development-cache/{manifest,case results}
run_02_verification.py
  → results/development-cache/admission.json
run_03_render.py
  → technical-report/development-figures/*.png
```

Calculation happens once for exact cache bytes and records the scientific calculation
infrastructure SHA-256 in the manifest. Integrity admission happens once for that
manifest digest. Rendering may then repeat without scientific recalculation; every
render still checks that the admission digest and cached case digests match. Plotting
sources are not part of the calculation-infrastructure identity.

Cache integrity does not establish scientific correctness. Scientific acceptance uses
the declared analytic invariants, refinement checks, and bounded independent reference
controls and remains a separate human decision. No authenticated-rendering or exhaustive
provenance package is required for repeated figure generation. The historical
`workflow/` tree is not imported.
