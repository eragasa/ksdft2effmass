# Phase 2 numerical scope

The proposed node constructors perform no numerical transformation and allocate no second
matrix-field payload. They retain the supplied immutable field and validate structural
relations already observable through Phase 1 contracts.

Required checks would be:

- Bloch identity with a Bloch carrier role and momentum-domain operator field;
- cell-hopping identity with a cell-hopping role and translation-domain Fourier-block
  field;
- exact domain equality, not cardinality-only agreement;
- positive source and target dimensions equal to `identity.rank`; and
- preservation of field-owned immutable storage.

Array equality would not create or merge representation identities. A node equality
policy must be stated explicitly before implementation and must not infer scientific
equivalence from equal arrays.
