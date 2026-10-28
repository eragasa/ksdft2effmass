# Result numerics

## Reference-unit representation

Reduced momenta, energies divided by the declared reference energy, hopping
coefficients divided by that energy, error summaries, gap summaries, condition numbers,
and normalized refinement changes use `Unitless`. This is a represented reference-unit
convention, not an assertion that physical energies are dimensionless.

Public scalar values are built-in finite `float` or `int` values. Public numeric APIs
reject booleans and numeric strings. Vectors and matrices retain explicit PhysKit
quantity types, read-only binary64 arrays, shapes, and real or complex character.

## Fourier correlation

For centered construction representatives `R`, stored candidates are correlated with

\[
E(k)=\sum_R e^{2\pi i kR}t_R.
\]

The complete coefficient inventory has the construction-mesh extent. Each ordinary
support contains exactly `-R,...,R`. Both transform-mediated and direct-fit coefficient
vectors are evaluated independently on construction and withheld coordinates; a stored
candidate cannot be substituted from another route.

## Decisive comparisons

Application passage uses the recomputed withheld maximum error and the inclusive
configured threshold. A stored error within ordinary numerical comparison tolerance but
on the opposite side of the threshold is rejected. Sampled-gap passage and refinement
stability use the same fail-closed rule.

Nondominance and near-tie masks are recomputed over the attained ordered support table.
No interpolation across support or mesh size is implied.

## Wire

Explicit mappings preserve field names and tuple order. Re-decoding invokes all
constructor admission rules. SHA-256 subject identity is deliberately absent: the
byte-owning verifier hashes the exact admitted result bytes.
