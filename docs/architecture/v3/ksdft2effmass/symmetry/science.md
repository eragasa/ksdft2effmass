# Scientific meaning of symmetry

**Prospective framework design.** These pages select an incubation boundary, not a
physical symmetry convention, a completed calculation, or an implemented capability.

## Three separate claims

1. **Geometric symmetry:** an operation preserves a declared lattice/motif, with its
   translations and coordinate conventions. This does not supply an electronic action.
2. **Represented quantum action:** an operation acts on identified states with an
   explicit basis, metric, gauge and phase convention. A selected finite space must be
   checked for invariance; projection or disentanglement does not guarantee it.
3. **Symmetry of a model/operator:** an authenticated action satisfies the relevant
   covariance law for the declared operator. Geometric expectation, matching energies,
   labels or matrix dimensions do not establish that law.

A failure of subspace closure, a supported sector mismatch, an unresolved numerical
check, and unavailable representation data are different findings. None alone proves
that every possible reduced model is impossible or that the parent physical model is
inadequate. Missing parser capability is not proof that the underlying saved data lack
the information.

## Reciprocal space, phases and spin

At general momentum a symmetry relates different Bloch fibres. Little-group operations
preserve momentum modulo a reciprocal vector, so action qualification also needs the
appropriate reciprocal sewing. Translation parts of crystal operations can produce
momentum-dependent phases. A quotient of geometric operations is not automatically an
ordinary electronic representation of that quotient.

Nonsymmorphic/projective representations, spinful double-valued representations and
antiunitary actions therefore need explicit extensions beyond the initial ordinary,
complex-linear finite-group slice. Do not discard fractional translations, replace
antiunitary conjugation by a linear matrix, infer spin conventions from dimension, or
borrow scalar characters for a spinor/corepresentation problem. Gamma can be a first
integration case, but cannot alone validate general-momentum phase conventions.

A numerical proximity between differently printed coordinates or cell declarations
must not be silently turned into exact physical symmetry. Point-index relationships,
native coordinate presentations and physical wavevectors remain distinguishable.

## Connection to the silicon diagnosis

The current motivating consumer is the [common-space CSD2 protocol](../../../../../calculations/Si/bulk/research-protocol/controlled-reduction-protocol-hopping-first.tex).
The [CSD1-V checkpoint](../../../../../calculations/Si/bulk/analysis/common-space-verification/README.md)
verifies the rank diagnosis under its declared source/finite-input contract; it does not
identify a symmetry-sector cause. The geometric construction-index stars do not supply
parent, trial or Wannier representation matrices.

A silicon integration must identify operations and authenticate actions on the represented
parent/trial/retained spaces, including applicable overlap metrics and phase conventions,
before constructing sector projectors. The action of a physical symmetry need not close
on an arbitrary band cutoff or a disentangled Wannier subspace. Raw atomic-trial
coordinates need not be orthonormal, and their weights are not charges or populations.

The bounded compact-artifact inspection has not established the necessary actions.
Raw saved wavefunctions remain unparsed; no fundamental insufficiency of all retained
data has been demonstrated. A framework does not remove that source-extraction question.
If an actual CSD2 audit establishes insufficient retained symmetry data, the protocol
requires `INSUFFICIENT_RETAINED_SYMMETRY_DATA` and a stop, not guessed irreps or an
automatic successor. This documentation records no such completed disposition.

## Evidence and authority

General mathematical software can be developed against explicitly labeled synthetic
representations without claiming physical validation. Silicon is a consumer and a later
integration test, not the definition of every group, metric or state space supported by
the reusable core. Test success, authenticated bytes and numerical covariance checks
have distinct meanings; they do not establish review authorship or scientific acceptance.

The framework must not select a pseudopotential, change a physical model, manufacture
an invariant subspace, normalize away a failed rank gate, or choose a new Wannier window.
Parent-model, numerical/discretization and model-reduction errors remain separate under
the [retained-space and operator conventions](../../../v2/ksdft2effmass/periodic/retained-spaces-and-operators.md).
Native file ownership remains with Simulations; PhysKit primitives and eventual migration
must respect the [ownership boundary](index.md).

No scientific protocol, retained result, source assertion, calculation authority or
migration/publication authorization is amended by these four design pages.

See [schematics](schematics.md) for the proposed flow and [numerics](numerics.md) for
mathematical qualification requirements.
