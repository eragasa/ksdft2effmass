# M2 calculator implementation

`execute()` constructs one parent sample path, derives raw eigenspaces, transports a
reference frame, applies the frozen attack, and computes pointwise and global alignment
channels before any locality comparison. Reference, attacked, and pointwise-aligned
represented operators are Fourier transformed separately.

`_eigenframes`, `_attack_rotations`, `_rotate_path`, and `_global_rotation` own the
finite frame policy. `_range_result` preserves a common spectrum target across three
truncated models. `_external_gap_minimum` evaluates both training and evaluation meshes
without using the latter to change the frame.

No method calls Wannier90 or performs filesystem/network execution.
