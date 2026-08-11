import Mathlib.Data.Complex.Basic
import Mathlib.LinearAlgebra.Matrix.ConjTranspose

set_option linter.style.header false

/-!
# Gauge-equivariant finite-matrix lemmas

This module contains the Lean encoding of frozen prover-neutral contract
`PRF-05.01`. It establishes only the declared finite-dimensional matrix
identity; it does not establish scientific validity or physical admissibility
of a retained frame.
-/

namespace Ksdft2Effmass

/--
`PRF-05.01`: rotating an orthonormal retained frame by a unitary matrix leaves
its ambient-space projector unchanged.

The assumptions `_hM`, `_hMD`, and `_hV` retain the contract's dimension and
orthonormal-frame interpretation. The bare matrix identity uses only
`hG_mul_conjTranspose`; `_hG_conjTranspose_mul` retains the contract's complete
unitarity assumptions.
-/
theorem projector_invariant_under_unitary_frame_rotation
    {D M : Nat}
    (_hM : 1 <= M)
    (_hMD : M <= D)
    (V : Matrix (Fin D) (Fin M) Complex)
    (G : Matrix (Fin M) (Fin M) Complex)
    (_hV : Matrix.conjTranspose V * V = 1)
    (_hG_conjTranspose_mul : Matrix.conjTranspose G * G = 1)
    (hG_mul_conjTranspose : G * Matrix.conjTranspose G = 1) :
    (V * G) * Matrix.conjTranspose (V * G) =
      V * Matrix.conjTranspose V := by
  -- Taking the adjoint reverses the product:
  -- `conjTranspose (V * G) = conjTranspose G * conjTranspose V`.
  rw [Matrix.conjTranspose_mul]
  calc
    -- Reassociate the four factors so that
    -- `G * Matrix.conjTranspose G` becomes an adjacent subexpression.
    V * G * (Matrix.conjTranspose G * Matrix.conjTranspose V) =
        V * (G * (Matrix.conjTranspose G * Matrix.conjTranspose V)) :=
      Matrix.mul_assoc V G
        (Matrix.conjTranspose G * Matrix.conjTranspose V)
    _ = V * ((G * Matrix.conjTranspose G) * Matrix.conjTranspose V) := by
      rw [Matrix.mul_assoc G (Matrix.conjTranspose G) (Matrix.conjTranspose V)]
    _ = V * (G * Matrix.conjTranspose G) * Matrix.conjTranspose V :=
      (Matrix.mul_assoc V (G * Matrix.conjTranspose G)
        (Matrix.conjTranspose V)).symm
    -- Unitarity replaces `G * Matrix.conjTranspose G` by the identity,
    -- leaving `V * Matrix.conjTranspose V`.
    _ = V * Matrix.conjTranspose V := by
      simp [hG_mul_conjTranspose]

end Ksdft2Effmass
