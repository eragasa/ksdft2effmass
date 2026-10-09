# `ksdft2effmass.periodic1d.campaign.extraction.matched`

## Responsibility

Canonical owner of the `PERIODIC-XWALK-065` matched known-map periodic-1D synthetic
defect-extraction family. The package owns closed input controls, authenticated parent
data loading, represented-operator compatibility, retained workflow result production,
and independent result verification.

## Modules

- [`compatibility`](compatibility/index.md)
- [`records`](records/index.md)
- [`serialization`](serialization/index.md)
- [`verification`](verification/index.md)
- [`workflow`](workflow/index.md)

## Represented-operator boundary

The local campaign envelope composes the general `OperatorRecord` produced through
the explicit row-030 metadata Action. Exact state labels, embedded cell vectors, energy
and coordinate conventions, and structured provenance are supplied before dense
comparison. No identity or geometry is inferred from dimensions, names, paths, hashes,
or spectra.

## Evidence and limitations

The retained input/result pair is synthetic known-map campaign evidence. Focused tests
check retained payload agreement, independent verification, canonical class identity,
former-route absence, mirrored layout, and general represented-operator composition.
They do not validate material physics, transferability, continuum convergence,
uncertainty quantification, or acceptance.
