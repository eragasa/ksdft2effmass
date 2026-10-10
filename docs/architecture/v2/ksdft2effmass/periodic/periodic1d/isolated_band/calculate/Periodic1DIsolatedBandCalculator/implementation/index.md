# M1 calculator implementation

`execute()` is a thin orchestration boundary around typed domain Actions. Parent
constructors receive physical reciprocal coordinates; selected scalar spectra become
`ReciprocalOperatorSamples1D`; the complete transform owns the periodic representative
ordering; each range constructs both mediated and direct-fit models against the same
training/evaluation targets.

Private `_calculate_range` is the main policy owner. It must preserve training/evaluation
roles and correlate truncation, errors, Parseval, direct fit, route comparison, and band
shape before result construction. `_plane_wave_spectrum` and
`_finite_difference_spectrum` own the two finite discretization routes but not their
scientific acceptance.

No method reads/writes retained files or dispatches external tools.
