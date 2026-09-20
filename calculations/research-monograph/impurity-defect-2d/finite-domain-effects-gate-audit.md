# Finite-domain effects predecessor-gate audit

## Status and scope

This is a read-only audit of the immutable accepted directional/nonlocal
numerical-verification package. No calculation, verifier rerun, artifact rewrite,
tolerance change, or external-root access was performed. Artifact identities below are
those retained by the accepted execution review and native-evidence manifest.

This audit establishes only whether the durable continuation gate is represented in
the accepted package. It does not establish scientific validation, uncertainty
quantification, finite-size convergence, or authority to implement or execute the
finite-domain study.

## Immutable evidence boundary

| Artifact | SHA-256 |
|---|---|
| Accepted result | `b5ff50b6a2494dc4314854fff61c830f7ca562543ab5a42c9e15b41087902cc4` |
| Independent verification log | `bf2d2b4bbc258259c41984bbd8ead112a8cdae0eedf9cce1f62b11d6b588c0ec` |
| Native-evidence manifest | `f07774e9208ac6767f5881b79707ac1ddc07bdfc1b199f3a545aa57c4847684a` |
| Package checksum catalog | `7481524db3e5d26c18986f6d4474d4f7d0d7e5a6d26e75973b3e78551c092b44` |

The accepted review records one consumed attempt ending in terminal `SUCCESS`, no
retry, 208 route evaluations, 104 gauge bridges, 1,040 model fits, 104 schedule
comparisons, 17 passing criteria, and independent-verifier `PASS`.

## Gate requirements

The durable gate requires a separately authorized calculated result that retains:

1. every frozen model class in its declared order;
2. residuals for accepted and rejected model classes;
3. failures rather than favorable-case filtering; and
4. the frozen classes and tolerances without outcome-driven changes.

## Audit findings

| Requirement | Retained evidence | Disposition |
|---|---|---|
| Frozen class order | Every route record contains five fits ordered as point scalar onsite, finite-support diagonal onsite, onsite plus isotropic nearest neighbor, onsite plus directional nearest neighbor, and finite-range nonlocal radius two. | PASS |
| Accepted and rejected residuals | Each of the 208 route records retains all five fits. Every fit retains maximum, Frobenius, spectral, shell, core-exterior, support, coefficient, rank, and acceptance fields. Rejected lower classes remain present. | PASS |
| Failure retention | The result retains failed candidate-class acceptance, all ten adverse controls, all criterion dispositions, and schedule comparisons. No class, route, schedule, or orientation is dropped to obtain a favorable result. | PASS |
| Model-selection agreement | All 208 selected classes equal their declared expected classes: 104 directional-nearest-neighbor selections and 104 finite-range-nonlocal selections. | PASS |
| Frozen thresholds | Result criteria retain `1e-11` for Hermiticity and alignment unitarity, `1e-10` for recovery, covariance, bridge, fit, exterior, and independent reconstruction, and exact zero for schedule difference, agreeing with the adopted design. | PASS |
| Independent reconstruction | The independent verifier reconstructed all 208 routes and 1,040 fits without importing the runner and reported maximum scalar difference `2.741586977772928e-15 E_G`. | PASS |

## Gate disposition

**Gate result: PASS.**

The immutable accepted package contains the model-class residual and failure evidence
required to design the finite-domain geometry and boundary-phase study. This gate
result authorizes no implementation or execution. A future implementation must consume
the accepted compact records without mutating them, retain failed and nonmonotone
finite-domain sequences, and preserve model classes and tolerances exactly.

## Limitations

- The gate does not prove area, shape, orientation, or boundary-phase convergence.
- Parent reconstruction and radius-18 truncation error remain inherited and separate.
- A no-bound-state result remains an outcome, not a process failure.
- The accepted package is numerical-verification evidence only.
