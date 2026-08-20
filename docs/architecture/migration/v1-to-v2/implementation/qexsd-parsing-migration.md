# QEXSD parsing migration

## Status and identity

This page records the bounded implementation result for
`migration.v2.integration.quantumespresso.qexsd`. Canonical QEXSD source,
native-document, and parser ownership is
`ksdft2effmass.integration.quantumespresso.qexsd`.

No public v2 wire, neutral plane-wave contract, Workflow provenance variant, or
calculator process contract is selected here.

## Canonical and compatibility surfaces

The canonical public surface is:

- `QexsdSource`, owning explicit bytes and verified source identity;
- `QexsdDocument`, owning mechanically parsed native values and source labels; and
- `QexsdDocumentParser`, owning syntax parsing into the native document.

The ActionObject name follows the accepted target-first grammar. The historical
`ParseQexsdDocument` import remains an identity-preserving transitional alias only
under `ksdft2effmass.io.quantum_espresso.qexsd`. Legacy source and document imports
forward to the same canonical classes, so parser and native-record policy have one
implementation owner.

`QexsdDocument` now rejects wrong semantic types with `TypeError` and correctly
typed invariant violations with `ValueError`. Its intrinsic checks cover canonical
source path and digest syntax, nonnegative byte count, optional producer version,
positive `alat`, vector and row shapes, species and atom declaration types and
references, declared atom/k-point/band counts, finite weights and observations,
positive FFT triplets, and process-status range. These are native record software
invariants, not backend-neutral physical interpretation.

## Compatibility adaptation

`ConstructQexsdKohnShamPlaneWaveRecord` remains at the historical path as the
schema-version-1 compatibility adapter. It consumes the canonical
`QexsdDocument`, constructs the already verified periodic and neutral Kohn--Sham
values, applies explicit compatibility validators, and emits the retained legacy
aggregate and canonical bytes unchanged.

The later `migration.v2.integration.quantumespresso.adaptation` Task owns separated
outputs for periodic values, Kohn--Sham observations, integration-native plane-wave
extraction, calculator process observations, and Workflow artifact provenance. This
Task does not pre-empt those contracts or fabricate unavailable provenance state.

## Dependency direction

Neutral `periodic` and `ksdft` packages import neither canonical integration nor the
legacy QEXSD path. Canonical parsing imports only its native records and standard
library owners. The compatibility path may depend on canonical integration and the
retained schema-version-1 aggregate, never the reverse.

## Verification

Software verification covers canonical export and defining-module identity, exact
legacy forwarding identity, forbidden neutral-package dependencies, controlled XML
parsing through the canonical objects, direct native-record rejection, unchanged
periodic and Kohn--Sham observations, and byte-identical schema-version-1
serialization. Existing duplicate-key, configured-tolerance, aggregate-compatibility,
and retained-artifact tests remain compatibility evidence.

The developer-local retained-artifact path remains isolated from portable default
fixtures and is not a portable provenance reference.

## Residual limitations

The legacy aggregate adapter still contains mixed-owner compatibility composition by
design. It retires only after the downstream calculator, Workflow provenance, QEXSD
adaptation, and consumer cutover Tasks provide actual replacement results. No new v2
domain code should depend on that aggregate.
