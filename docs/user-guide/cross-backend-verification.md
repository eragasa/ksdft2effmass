# Cross-backend verification

## Common-parent rule

Future paired QE and ABINIT cases must derive independently from the same
neutral periodic specification. QE input must not be translated into ABINIT
input. The neutral parent records the lattice and coordinate convention,
species and sites, periodic boundary conditions, exchange-correlation method,
charge/spin and relativistic treatment, pseudopotential requirements, $k$-point
sampling, band count, occupation/smearing intent, convergence intent, and
requested observables. Backend-native variables remain in their concrete
mappers.

## Tutorial-derived corpus

Upstream QE and ABINIT tutorials are behavioral references, not numerical
oracles. A future conformance corpus separates:

1. retained tutorial-output parser fixtures — **software verification**;
2. bounded tutorial-equivalent executable cases — **software verification
   (integration evidence)**;
3. matched and independently converged paired cases — **numerical
   verification**.

Scientific validation remains separate from all three layers. Any imported
future tutorial fixture must record source project, tutorial identifier, source
URL, upstream version or revision, retrieval date, license and attribution,
original checksum, local modifications, convergence status, and permitted VVUQ
classification. No tutorial file is copied during the architecture correction.

## Comparison controls

A paired comparison must state its pseudopotential matching level:
`EXACT_ARTIFACT`, `COMMON_GENERATION_LINEAGE`,
`MATCHED_PHYSICAL_SPECIFICATION`, or `UNMATCHED`. It must also declare method
profile, convergence protocols, comparison quantities, units, energy-reference
alignment, tolerances, and known confounders.

A backend disagreement is structured evidence to investigate, not proof that
one backend is wrong. Neither backend is an oracle. Semilocal evidence does not
qualify hybrid GKS execution.

## Status

The conformance corpus and ABINIT adapter are deferred until an accepted
end-to-end dopant result. They are not part of P0–P11, not implemented, not
verified, and not authorized for execution.

See [ABINIT](abinit.md), [PAW and pseudopotential capabilities](paw-and-pseudopotential-backends.md), and the [periodic integration architecture](https://github.com/eragasa/ksdft2effmass/blob/dev/docs/architecture/periodic-electronic-structure-integration.md).
