"""Attribute the Gamma window-loss direction to existing excluded parent bands.

No window, retained subspace, calculator input or source operator is changed.
Fractions below are shares of one trial combination's squared parent-band
response, NOT occupations, charges, physical orbital populations or irreps.

The leading nine right-singular candidates F yield a certified lower bound on
sigma_9(C_window): sigma_min(C_window F)/||F||. A Rayleigh residual for the
tenth candidate then bounds its projector error using the separated second
Gram eigenvalue. For native error epsilon, Gram perturbation is at most
2*||C_window||*epsilon+epsilon^2. If gap>2*perturbation, the minimum-projector
change is bounded by perturbation/(gap-perturbation). Per-band squared-response
bounds also include parent-row input errors. All bound tests use Fractions;
serialized floating values are displays, not outward-rounded certificates.
"""
from __future__ import annotations

import hashlib
import importlib
import json
from fractions import Fraction
from importlib.metadata import version
from pathlib import Path

import numpy as np
from projectkoios.integrations.wannier90 import (
    Wannier90EigenvalueParser,
    Wannier90TrialOrbitalOverlapParser,
)
from projectkoios.physkit.units import PhysicalUnit

previous_path = Path('/tmp/ksd-silicon-trial-whitening.json')
previous_bytes = previous_path.read_bytes()
previous = json.loads(previous_bytes)
helper_path = Path('/tmp/ksd_silicon_trial_whitening.py')
assert hashlib.sha256(helper_path.read_bytes()).hexdigest() == previous['script_sha256']
from ksd_silicon_trial_whitening import exact, frobenius, gram_defect, minimum_bounds
from common_space.verification.gram_rank import _ExactMatrix
from common_space.verification.native_overlap import CommonSpaceNativeOverlapReconstruction
from common_space.verification.native_precision import CommonSpaceMatrixUncertainty

ROOT = Path('/Users/eugene/worktrees/ksdft2effmass-silicon-main-package-0matampv')
REQUEST = ROOT / 'calculations/Si/bulk/analysis/c6-b20-w21-slater-koster-definition-fit/common-space-diagnosis-request.json'


def squared_norm(matrix: _ExactMatrix) -> Fraction:
    return sum((z.real**2+z.imaginary**2 for row in matrix.rows for z in row), Fraction(0))


def run() -> None:
    request_bytes = REQUEST.read_bytes()
    request = json.loads(request_bytes)
    assert request['sources'] == previous['source_identities']
    assert version(request['provider']['distribution']) == request['provider']['version']
    for name, expected in previous['module_sha256'].items():
        module = importlib.import_module(name)
        assert module.__file__ is not None
        assert hashlib.sha256(Path(module.__file__).read_bytes()).hexdigest() == expected, name
    for declaration in request['sources'].values():
        path = ROOT / declaration['path'] if declaration['location'] == 'repository' else Path(declaration['path'])
        payload = path.read_bytes()
        assert len(payload) == declaration['byte_size'] and hashlib.sha256(payload).hexdigest() == declaration['sha256']
    amn_source = request['sources']['AMN']
    aq = Wannier90TrialOrbitalOverlapParser(payload=Path(amn_source['path']).read_bytes()).parse().matrices[0]
    c = exact(np.asarray(aq.magnitude)).multiply(CommonSpaceNativeOverlapReconstruction._atomic_transform().adjoint())
    window_result_bytes = Path('/tmp/ksd-silicon-gamma-window.json').read_bytes()
    window_result = json.loads(window_result_bytes)
    assert window_result['request_sha256'] == hashlib.sha256(request_bytes).hexdigest()
    eig_identity = window_result['eig_identity']
    payload = Path(eig_identity['path']).read_bytes()
    assert len(payload) == eig_identity['byte_size'] and hashlib.sha256(payload).hexdigest() == eig_identity['sha256']
    energies = Wannier90EigenvalueParser().execute(payload, PhysicalUnit('eV')).eigenvalues.magnitude[0]
    included = np.flatnonzero((energies >= -6) & (energies <= 21))
    assert included.tolist() == list(range(14))
    window = _ExactMatrix(rows=c.rows[:14])
    _, _, vh = np.linalg.svd(window.to_numpy(), full_matrices=False)
    vector = exact(np.asarray(vh[-1].conj()).reshape(-1, 1))
    frame = exact(np.asarray(vh[:9].conj().T))
    lower_nine, _ = minimum_bounds(window.multiply(frame))
    lower_second = (lower_nine/(1+gram_defect(frame)))**2
    norm_squared = squared_norm(vector)
    gram = window.adjoint().multiply(window)
    image = gram.multiply(vector)
    rayleigh_entry = vector.adjoint().multiply(image).rows[0][0]
    assert rayleigh_entry.imaginary == 0
    rayleigh = rayleigh_entry.real/norm_squared
    residual = image.subtract(vector.multiply(_ExactMatrix.diagonal((rayleigh,))))
    residual_bound = CommonSpaceMatrixUncertainty._sqrt_upper(squared_norm(residual)/norm_squared)
    gap = lower_second-rayleigh
    assert gap > 0
    arithmetic_projector_error = residual_bound/gap
    uncertainty = CommonSpaceMatrixUncertainty.from_parsed_matrix(matrix=aq, native_component_error=Fraction(1, 2*10**12))
    epsilon = uncertainty.parsing_error_bound+uncertainty.native_error_bound
    gram_input_error = 2*frobenius(window)*epsilon+epsilon**2
    assert gap > 2*gram_input_error
    input_projector_error = gram_input_error/(gap-gram_input_error)
    projector_error = arithmetic_projector_error+input_projector_error
    assert projector_error < 1
    response = c.multiply(vector)
    excluded = []
    lower_responses = []
    upper_responses = []
    nominal_responses = []
    for index in range(14, 20):
        row = _ExactMatrix(rows=(c.rows[index],))
        row_norm_squared = squared_norm(row)
        row_norm_upper = CommonSpaceMatrixUncertainty._sqrt_upper(row_norm_squared)
        amplitude = response.rows[index][0]
        nominal = (amplitude.real**2+amplitude.imaginary**2)/norm_squared
        error = row_norm_squared*projector_error+2*row_norm_upper*epsilon+epsilon**2
        lower = max(Fraction(0), nominal-error)
        upper = nominal+error
        lower_responses.append(lower)
        upper_responses.append(upper)
        nominal_responses.append(nominal)
        excluded.append({
            'parent_band_one_based': index+1, 'energy_ev': float(energies[index]),
            'squared_trial_response_nominal': float(nominal),
            'squared_trial_response_lower_display': float(lower),
            'squared_trial_response_upper_display': float(upper),
        })
    total_nominal = sum(nominal_responses, Fraction(0))
    for record, nominal in zip(excluded, nominal_responses, strict=True):
        record['share_of_excluded_squared_response_nominal'] = float(nominal/total_nominal)
    dominant = int(np.argmax([float(value) for value in nominal_responses]))
    other_upper = sum((value for i, value in enumerate(upper_responses) if i != dominant), Fraction(0))
    share_lower = lower_responses[dominant]/(lower_responses[dominant]+other_upper)
    recovery = []
    for count in (14, 15, 18, 20):
        restricted = _ExactMatrix(rows=c.rows[:count])
        lower, upper = minimum_bounds(restricted)
        recovery.append({
            'included_parent_band_count_at_gamma': count,
            'minimum_trial_singular_value_nominal': float(np.linalg.svd(restricted.to_numpy(), compute_uv=False)[-1]),
            'minimum_lower_after_input_error_display': float(max(Fraction(0), lower-epsilon)),
            'minimum_upper_after_input_error_display': float(upper+epsilon),
            'trial_independence_resolved_under_rounding': lower > epsilon,
        })
    nominal_weights = tuple((row[0].real**2+row[0].imaginary**2)/norm_squared for row in vector.rows)
    groups = {'s': (0, 5), 'p': (1, 2, 3, 6, 7, 8), 's_star': (4, 9)}
    result = {
        'scope': __doc__,
        'request_sha256': hashlib.sha256(request_bytes).hexdigest(),
        'whitening_result_sha256': hashlib.sha256(previous_bytes).hexdigest(),
        'window_result_sha256': hashlib.sha256(window_result_bytes).hexdigest(),
        'helper_script_sha256': previous['script_sha256'],
        'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'source_identities': request['sources'], 'eig_identity': eig_identity,
        'rounding_model': 'nearest absolute decimal rounding: AMN/EIG twelve decimal places; correctly rounded binary64 parsing',
        'frozen_window_unchanged_ev': [-6, 21],
        'frozen_raw_threshold_unchanged': request['retained_diagnosis_comparison']['native_uncertainty_bound'],
        'minimum_direction_gram_gap_lower_display': float(gap),
        'minimum_direction_arithmetic_projector_error_upper_display': float(arithmetic_projector_error),
        'minimum_direction_native_projector_error_upper_display': float(input_projector_error),
        'trial_coordinate_group_weights_nominal': {name: float(sum((nominal_weights[i] for i in indices), Fraction(0))) for name, indices in groups.items()},
        'excluded_band_responses': excluded,
        'dominant_excluded_band_one_based': 15+dominant,
        'dominant_band_share_lower_under_bounds_display': float(share_lower),
        'algebraic_inclusion_checks_not_window_selections': recovery,
        'nonclaims': ['No irrep or symmetry-protection attribution.', 'No tracking of band 15 across reciprocal space.', 'Restoring trial independence at Gamma does not establish that a final rank-ten Wannier subspace retains it.', 'No new window, source, fit, calculator run or production qualification.'],
    }
    path = Path('/tmp/ksd-silicon-gamma-excluded-bands.json')
    with path.open('x') as stream:
        json.dump(result, stream, indent=2, allow_nan=False)
        stream.write('\n')
    print(json.dumps(result, indent=2, allow_nan=False))
    print('Output:', path)


if __name__ == '__main__':
    run()
