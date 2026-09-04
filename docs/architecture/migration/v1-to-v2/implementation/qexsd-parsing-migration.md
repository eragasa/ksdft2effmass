# QEXSD parsing migration

## Status and identity

**Human-accepted and administratively closed.** The human response
`accept and closeout` accepted the bounded implementation result for
`migration.v2.integration.quantumespresso.qexsd`. Canonical QEXSD source,
native-document, and parser ownership is
`ksdft2effmass.integration.quantumespresso.qexsd`.

No public v2 wire, neutral plane-wave contract, Workflow provenance variant, or
calculator process contract is selected here. The accepted result authorizes no
protected execution, scientific claim, or automatic successor activation.

## Canonical and legacy-path surfaces

The canonical public surface is:

- `QexsdSource`, owning explicit bytes and verified source identity;
- `QexsdDocument`, owning mechanically parsed native values and source labels; and
- `QuantumEspressoXsdDocumentParser`, owning syntax parsing into the native document.

The ActionObject name identifies the external calculator, XSD-conforming document,
and parsing responsibility. The former `QexsdDocumentParser` and
`ParseQexsdDocument` names are not exported. Legacy-path source, document, and parser
imports use the selected canonical names and forward to the same canonical classes,
so parser and native-record policy have one implementation owner.

`QexsdDocument` now rejects wrong semantic types with `TypeError` and correctly
typed invariant violations with `ValueError`. Its intrinsic checks cover canonical
source path and digest syntax, nonnegative byte count, optional producer version,
positive `alat`, vector and row shapes, species and atom declaration types and
references, declared atom/k-point/band counts, finite weights and observations,
positive FFT triplets, and process-status range. These are native record software
invariants, not backend-neutral physical interpretation.

The parser accepts exactly the observed QEXSD `23.03.10` and `25.05.21` formats
under the common QES 1.0 namespace. The latter is bound to the retained QE 7.5
silicon SCF smoke-test artifact. Unlisted versions still fail closed; accepting these
two artifacts does not establish exhaustive coverage of every document permitted by
either upstream schema.

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
parsing for both accepted QEXSD versions through the canonical objects, direct
native-record rejection, unchanged periodic and Kohn--Sham observations, and
byte-identical schema-version-1 serialization. Identity-bound extraction of the QE
7.5 smoke-test QEXSD also exercises the existing compatibility adapter. Existing
duplicate-key, configured-tolerance, aggregate-compatibility, and retained-artifact
tests remain compatibility evidence.

The developer-local retained-artifact path remains isolated from portable default
fixtures and is not a portable provenance reference.

## Residual limitations

The legacy aggregate adapter still contains mixed-owner compatibility composition by
design. It retires only after the downstream calculator, Workflow provenance, QEXSD
adaptation, and consumer cutover Tasks provide actual replacement results. No new v2
domain code should depend on that aggregate.
