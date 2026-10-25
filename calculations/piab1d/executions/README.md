# PIAB1D execution packages

`direct-core-n8-m3/` is retained as an explicitly unsealed development execution. It
contains completed calculation, independent verification, and rendering stages. Its
`UNSEALED.md` records the source revision and the limits on its use.

The directory is not a sealed evidence package. Its
`development-provenance.json` records source, dependency, command, artifact, and
verification identities without asserting a seal. The directory has no execution-wide
checksum catalog, source manifest, sealed provenance record, or evidence-package
identity. Sealing is a separate future action.

The existing top-level inputs, results, figures, scripts, and checksum catalog are
historical flat artifacts. They remain at their established paths and are not asserted
to constitute one atomic execution. A sealed successor execution must record its own
exact input, result, verification, rendering, provenance, and checksum relationships.
