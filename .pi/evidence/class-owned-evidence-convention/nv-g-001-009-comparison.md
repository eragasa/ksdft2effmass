# NV-G-001 through NV-G-009 convention comparison

Compared artifact:
`python/tests/numerical_verification/ksdft2effmass/operators/test__Geometry__linear_independence.py`
(SHA-256 `4a9fb4c8cb74e6e086149b88616680e611df435c7d1c714b8dfabb500653f86f`).
The closed Geometry numerical module was read only and remains unchanged.

## Structural comparison

- The module correctly declares numerical verification, the represented
  row-lattice matrix and singular-value-ratio contract, `NV-G-001` through
  `NV-G-009`, and explicit scientific-validation/UQ exclusions.
- Its historical module headings are not the new exact unified headings.
- Its test and helper docstrings already contain the seven exact fields in the
  required order with nonempty bodies.
- Its historical test names do not use
  `test_<surface>__<facet>__<behavior>`.
- Evidence identifiers remain unique and stable. The two parameterized tests use
  meaningful signed-scale IDs rather than ordinals.

These structural differences are inventory findings, not authorization to rename
or redocument accepted evidence.

## Semantic comparison

All nine cases state non-tautological public requirements, exercise the public
constructor, and use analytical oracles independent of the production SVD:
exact diagonal singular values, exact duplicated-row dependence, triangular
full-rank arguments, uniform-scale invariance, and row-permutation invariance.
`NV-G-005` independently fixes the public tolerance at exactly `1e-12` before
using it to form boundary inputs. Exact represented cells, signs, stored values,
exception categories, and warning behavior are asserted where applicable.
Strict equality, below/above threshold, signed extreme normal scales, and valid
versus invalid permutation partitions are explicit.

The module correctly limits interpretation: passing is numerical verification of
the stated binary64 policy over the tested regime; failure can also indicate an
evidence, contract, platform, or LAPACK issue. It does not claim physical or
crystallographic validity, scientific validation, UQ, Rust conformance, or a
scientifically selected tolerance.

## Review boundary

This comparison is not a semantic migration, a new validation result, or final
acceptance. The reusable structural validator must continue to report structure
only; oracle independence, mathematical correctness, tolerance adequacy, and
scientific meaning remain review- and human-authority questions.
