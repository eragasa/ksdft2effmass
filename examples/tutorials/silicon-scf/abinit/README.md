# ABINIT silicon SCF backend

**Status: planned; execution blocked.**

The official ABINIT basic3 tutorial contains the closest workflow correspondence, but
a project-owned portable ABINIT SCF input has not yet been selected. ABINIT 10.8.3 is
installed locally; source reuse terms, pseudopotential choice, exact input preflight,
and execution authorization remain unresolved.

This directory intentionally contains no fabricated input, expected value, or runtime
output. Implementing this backend must preserve the shared silicon-SCF learning
objective while documenting backend-specific units, pseudopotential representation,
basis cutoff, sampling, and output semantics. Numerical comparison with the QE backend
requires a separate explicit alignment contract.
