# M2 calculator implementation

`execute()` constructs one parent sample path, derives raw eigenspaces, transports a
reference frame, applies the frozen attack, and computes pointwise and global alignment
channels before any locality comparison. Reference, attacked, and pointwise-aligned
represented operators are Fourier transformed separately.

`_attack_rotations` owns the experiment's finite gauge perturbation.
`_eigenframes`, supplied-unitary application in `_rotate_path`, and direct transforms
are prospective Numerics seams; `_global_rotation` and pointwise/transport
transformation selection are prospective Alignment seams. The
[owner-boundary review](../../../owner-boundary.md) requires explicit rank-deficient and
deterministic-completion behavior before extraction. `_range_result` preserves a common
spectrum target across three truncated models. `_external_gap_minimum` evaluates both
training and evaluation meshes without using the latter to change the frame.

No method calls Wannier90 or performs filesystem/network execution.
