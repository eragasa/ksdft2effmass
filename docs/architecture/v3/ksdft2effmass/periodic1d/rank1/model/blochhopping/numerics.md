# `Periodic1DRank1BlochHoppingModel` numerics

For fractional reciprocal coordinate $q$ and ordinary integer displacement $R$, the
wrapped PhysKit evaluator computes

\[
H(q)=\sum_R T_R\exp(+2\pi i qR).
\]

The KSD numerical control constructs $T_R$ from normalized onsite and positive-range
coefficients through the explicit scale $E_a=\hbar^2/(m_ea^2)$. Its independent
reference evaluates the scalar conjugate-support identity directly from those
constructor inputs,

\[
H(q)=E_a\left[t_0+2\sum_{R>0}\operatorname{Re}
\left(t_R e^{+2\pi i qR}\right)\right].
\]

## Numerical validation behavior

The numerical test compares the complete complex Bloch-value vector against the
independent closed-form sum at six reciprocal coordinates. One complex array
comparison simultaneously checks coefficient scaling, positive-exponent phases,
finite support, and cancellation of the imaginary component from conjugate support.
The absolute binary64 tolerance is `5.0e-15 * E_a`; no relative tolerance is used.

Specific pytest evidence:

- `tests/ksdft2effmass/periodic1d/rank1/test__Periodic1DRank1BlochHoppingEvaluation__closed_form_sum.py::TestPeriodic1DRank1BlochHoppingEvaluation::test__Periodic1DRank1BlochHoppingEvaluation__matches_closed_form_sum`

Passing this test establishes the stated finite numerical identity only. It does not
establish continuum convergence, parent-model adequacy, material validity, or retained
evidence promotion.

- [Model contract](index.md)
