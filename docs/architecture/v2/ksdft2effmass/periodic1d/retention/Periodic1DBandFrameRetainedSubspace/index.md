# `Periodic1DBandFrameRetainedSubspace`

## Purpose and status

This implemented row-022 DataObject binds one parent-qualified one-dimensional
mathematical retained space to a gauge-dependent reciprocal-path frame representation.

## Public contract

Supported import:
`from ksdft2effmass.periodic1d import Periodic1DBandFrameRetainedSubspace`.
The binding retains a `ReciprocalBandFramePath1D` and a lowercase SHA-256 digest of only
the ordered frame matrices encoded as little-endian complex128 C-order bytes.

## Invariants and failure behavior

Exact public types are required. Scientific and represented ranks/ambient dimensions
must match and the parent dimension must be one. The digest syntax and observed matrix
bytes must match exactly. Type failures raise `TypeError`; dimensional or digest
failures raise `ValueError`.

## Gauge, content, and provenance boundary

A frame chooses coordinates for a retained subspace. Gauge changes can alter frame
bytes without changing the mathematical space. The digest authenticates observed
ordered frame-matrix content only; it excludes mesh and sewing-map bytes and is not an
independent production-provenance attestation. Endpoint sewing remains explicit in the
frame path.

## Code and evidence mapping

| Kind | Path or node | Established behavior |
|---|---|---|
| Code | `python/src/ksdft2effmass/periodic1d/retention.py:Periodic1DBandFrameRetainedSubspace` | Scientific/frame binding and digest check |
| Supporting code | `python/src/ksdft2effmass/solid_state/band_frames.py:ReciprocalBandFramePath1D` | Mesh-ordered orthonormal frames and sewing map |
| Test | `TestPeriodic1DBandFrameRetainedSubspace::test_construction__frame_path__binds_matching_dimensions` | Matching represented dimensions and authenticated content |
| Tests | Remaining class methods | Ambient mismatch, wrong content, malformed digest |
| Sphinx | `doc/sphinx/api/ksdft2effmass/periodic1d/retention.rst` | Public API and digest scope |
| Decision | `docs/architecture/v2/ksdft2effmass/periodic/band-frame-ownership-decision.md` | Mathematical-space versus gauge-frame ownership |

## Provenance and limitations

Original local work under the repository license. Synthetic tests establish dimension
and observed-content binding only. They do not establish frame smoothness, independent
source provenance, parent alignment, convergence, topology, scientific validation,
uncertainty, or acceptance. Broader frame/source metadata remains tracked separately in
the band-frame technical-debt record.
