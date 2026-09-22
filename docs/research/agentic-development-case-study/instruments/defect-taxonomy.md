# Defect taxonomy

| Code | Category | Meaning |
|---|---|---|
| A | Authority or approval failure | Missing, ambiguous, stale, or bypassed human or repository authority. |
| S | Scientific-semantic ambiguity | Unclear scientific meaning, convention, state space, unit, gauge, approximation, or validation claim. |
| N | Numerical-validation defect | Incorrect numerical invariant, tolerance, reference value, convergence behavior, or numerical error classification. |
| P | Public API or schema defect | Public interface, wire format, schema, fixture, or compatibility behavior violates the accepted contract. |
| I | Integration defect | Combined tree, imports, documentation, packaging, task routing, or cross-component behavior fails after individually plausible changes. |
| T | Test-coverage defect | Missing, misplaced, private-method-bound, or insufficient tests for accepted public behavior. |
| D | Documentation defect | Source, Sphinx, control-plane, or research documentation is stale, incomplete, misleading, or inconsistent. |
| R | Reproducibility or provenance defect | Missing durable evidence, manifests, fixtures, checksums, acceptance records, or state reconstruction support. |
| X | Cross-language conformance defect | Python/Rust or other implementation cannot conform to shared schemas, fixtures, or semantics. |

Use the taxonomy to classify observed defects. Do not infer scientific invalidity from a software defect unless the evidence supports that consequence.
