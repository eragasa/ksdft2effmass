# S100 diagnostic-completeness correction

The first successful S100 result was structurally valid and evaluated the unchanged
18-shell S90 family. Review before disposition found two omissions from the frozen
S90 reporting contract:

1. the monotone larger-shell envelope covered only four direct metrics rather than
   all frozen direct operator/spectrum summary metrics; and
2. the observable summary did not explicitly retain valley-energy spread changes,
   opposite-pair splitting changes, or curvature-stencil mass stability, although
   the underlying per-valley values were present.

The initial implementation and result are preserved with SHA-256 identities
`d96fcd6efb70748f613e6d35bf3ac1b9b66606d74642e95e9a3fd170dca3be58`
and `4a2e18d889ffc682acc2dc04cf37760aa1d662ac945d0ea8452eae814eb186de`,
respectively.

The final implementation adds the missing direct-metric envelopes and explicit
observable summaries. It does not change the source operator, shell masks, grids,
optimizer, curvature stencils, energy reference, or state-space alignment. It does
not select a radius or consume parent-oracle values.
