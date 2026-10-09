# `PeriodicFiniteDifferenceFiberHamiltonian1DConstructor`

**Defined in:** `ksdft2effmass.periodic1d.finite_differences`

## Role

Action constructing one sparse central-difference Hamiltonian from a parent-qualified
request, explicit half-open grid, and period tolerance.

## Seam convention

The directed wrapped edge is
`H[0,N-1] = -t exp(-2π i k)` and the reverse edge is its complex conjugate. This
orientation and grid order are retained exactly through `PERIODIC-XWALK-032`.

## Evidence

`test__PeriodicFiniteDifferenceFiberHamiltonian1DConstructor.py` checks the analytic
four-point stencil, both seam entries, Hermiticity, nonzero count, request identity,
and half-open coordinate order. It does not establish mesh convergence.
