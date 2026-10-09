# `Periodic1DWannier90ResultJsonSerializer`

## Purpose and status

The explicit kind selects the supported version-one schema before adaptation. The
adapter then requires that kind to agree with
`interface_conventions.preconditioned`, preventing either valid retained variant from
being relabeled as the other.

Configured wire Action that strictly decodes one explicit result kind, rejects unknown fields, and emits canonical JSON.

This implemented row-061 `Action/Workflow` is defined by `ksdft2effmass.periodic1d.campaign.wannier90.results.Periodic1DWannier90ResultJsonSerializer` and is publicly imported from `ksdft2effmass.periodic1d.campaign`.

## Invariants and ownership

Intrinsic immutable invariants are validated by the record itself; request-dependent derivation, authentication, parsing, correlation, or numerical work remains with the owning Action. Exact types, ordered inventories, explicit identities, and documented finite numerical representations fail closed. Names, dimensions, ranks, spectra, paths, or filenames are not used to infer scientific identity or provenance.

## Scientific boundary and evidence

This class does not by itself establish calculator execution, physical-model identity, a retained mathematical state space, a represented operator, convergence, physical adequacy, scientific validation, UQ, or acceptance. See the [module dossier](../index.md) and [family evidence map](../../index.md) for exact source, pytest, Sphinx, provenance, and limitation mappings.
