# Periodic electronic-structure backends

## Current domain

The integration layer is limited to periodic KS/GKS electronic-structure
calculations for crystalline solids that produce Bloch-band representations
suitable for band analysis, tight-binding reduction, and Wannierization.
Molecular-orbital and finite-system calculations are outside the current domain.
This is not a universal DFT API.

The neutral boundary records periodic lattice, reciprocal-space, $k$-point,
band, occupation, energy-reference, spin, convergence, pseudopotential/PAW
provenance, and downstream-capability information. It keeps independent the
electronic-structure method, core treatment, numerical representation, backend,
and available products. In particular, PAW is not a backend or superclass.

## Directional adapters

```text
neutral periodic specification
    -> capability negotiation
    -> concrete backend mapper and serializer
    -> immutable execution request

backend artifacts
    -> concrete parser
    -> semantic result adapter
    -> PeriodicElectronicStructureDataset
```

The neutral specification contains no QE or ABINIT variable names. QE input is
not translated into another backend's input. Downstream direct-TB and Wannier
consumers depend on neutral dataset capabilities and provenance rather than a
backend name.

## Status

- **Quantum ESPRESSO:** planned initial production backend; bounded P0 is closed
  and human-accepted as `CONDITIONAL_PASS`, and P0A packaging/configuration is
  closed and human-accepted. P1 has implemented only the backend-neutral CPN
  contract, which is closed and human-accepted. P2 is active and its
  provenance/external-tool implementation is provisional pending correction
  review, replacement replay, parent verification, and human acceptance. H5 and
  P3–P11 remain inactive. The QE adapter, concrete workflows, and external,
  production, or scientific execution remain unauthorized.
- **ABINIT:** planned, deferred conformance backend after the first accepted
  end-to-end dopant result; not installed or verified.
- **Hybrid GKS:** planned, deferred; no runtime support is claimed.
- **Molecular packages:** outside scope.

Architecture designed for several backends is not demonstrated backend
neutrality. A public demonstrated-neutrality claim requires future ABINIT
conformance evidence.

See the authoritative [periodic integration architecture](https://github.com/eragasa/ksdft2effmass/blob/dev/docs/architecture/periodic-electronic-structure-integration.md), [Quantum ESPRESSO](quantum-espresso.md), [ABINIT](abinit.md), and [cross-backend verification](cross-backend-verification.md).
