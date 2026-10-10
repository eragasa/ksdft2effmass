# `Periodic1DAdmissibleSetThresholds`

## Purpose and contract

Immutable named pair of dimensionless RMS thresholds for one M3 case. `case_id` is a
nonempty built-in string. `spectral_rms_threshold` and `operator_rms_threshold` are
finite, strictly positive built-in floats; Booleans and numeric strings are rejected.

The thresholds define the sublevel sets in `EQ-M3-ADMISSIBLE-004`. They are benchmark
controls, not probabilities, confidence levels, material tolerances, or uncertainty
bounds.

Source: `.../admissible_sets/definition.py`; directly exercised by Boolean and retained
contract-tamper tests.
