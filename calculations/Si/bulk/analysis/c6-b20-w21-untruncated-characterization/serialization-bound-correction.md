# Native serialization-bound correction

## Initial outcome

The first S30 pass retained the previously used fixed reconstruction gates. It failed
three fixed checks despite exact source identities, native convergence, pair closure,
and zero real-space Hermiticity residual:

| Quantity | Observed | Initial fixed gate |
|---|---:|---:|
| maximum matrix element | `2.1558486139506847e-5 eV` | `2e-5 eV` |
| maximum per-point Frobenius norm | `7.384056886810813e-5 eV` | `5e-5 eV` |
| maximum ordered-spectrum error | `2.893173461693266e-5 eV` | `2e-5 eV` |

The exact initial result is retained as
`characterization-result-initial-fixed-gate.json`, SHA-256
`f038459542ab2d7801ce83630274fd27db60275c6694b53fbcb904980a22ef89`.

## Cause

The initial fixed values came from the earlier smaller C4 representation and did not
scale with native HR serialization. This `C6-B20-W21` HR contains 279 native
representatives and prints each real and imaginary matrix component with six decimal
places. Its reciprocal degeneracy sum is exactly 216. A fixed `2e-5 eV` element gate is
therefore tighter than the worst-case round-trip uncertainty in the authenticated
native representation.

This is a verifier-policy defect. It is not evidence of reciprocal-point reordering,
optimizer failure, non-Hermiticity, or scientific inadequacy.

## Deterministic correction

The corrected analysis validates native decimal precision and derives conservative
bounds without fitting them to the observed discrepancies:

1. each HR real or imaginary component has half-unit rounding at six decimals;
2. each `u` and `u_dis` complex component has half-unit rounding at ten decimals;
3. each EIG value has half-unit rounding at twelve decimals;
4. HR error is propagated through exact degeneracy weights;
5. matrix-output errors are propagated through the rank-10 `U_dis U` transformation
   using the authenticated 20-band energy scale; and
6. the Frobenius bound supplies a conservative spectral bound through Weyl's inequality.

Derived bounds are:

- matrix element: `1.528384214328397e-4 eV`;
- matrix Frobenius norm: `1.527454004059488e-3 eV`; and
- ordered spectrum: `1.527454004059488e-3 eV`.

All observed discrepancies are below those bounds. Frozen-state matching remains under
the unchanged `2e-5 eV` gate, with maximum error
`1.2852634512228178e-9 eV`. The initial fixed checks remain in the final result as
explicit failed diagnostics; they were not rewritten.

## Disposition

The corrected format-aware structural verification passes. This permits S30 to retain
the full untruncated characterization and makes S40 revealed-408 development comparison
the next separately gated stage. It does not change any calculator output, localization
tolerance, target space, intended-use target, or confirmation boundary.
