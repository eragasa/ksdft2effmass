# Initial S100 analysis environment failure

The first authorized S100 launch invoked no calculator and produced no evaluation
artifact. Dynamic loading of the authenticated S30 implementation stopped with:

```text
ModuleNotFoundError: No module named 'projectkoios.integrations'
```

The KSD virtual environment provided the owner-supplied
`projectkoios.numerics.numpy.typing` and PhysKit namespaces, but its installed
ProjectKoios package did not expose the retained Wannier90 integration source tree
needed by S30 reconstruction.

The correction extends the already-imported `projectkoios` package search path with
the exact retained ProjectKoios tranche source package. S100 authenticates and binds
the source identities of the Wannier90 package initializer and the parsing,
Hamiltonian-block, interface-data, unitary-matrix, and disentanglement-matrix modules
before reconstruction. No calculator, mask, source operator, tolerance, or oracle
value changed.
