"""Locate the Gamma trial-direction loss without changing the frozen window.

This is an authorized local diagnostic, not CSD2 symmetry attribution or a new
source selection. Native data use the maintained Simulations parsers. Numerical
bounds reuse the authenticated scratch whitening experiment's exact residual
methods. No Hamiltonian fit or calculator is invoked.
"""
from __future__ import annotations

import hashlib
import importlib
import json
import math
from fractions import Fraction
from importlib.metadata import version
from pathlib import Path

import numpy as np
from projectkoios.integrations.wannier90 import (
    Wannier90DisentanglementMatrixParser,
    Wannier90EigenvalueParser,
    Wannier90TrialOrbitalOverlapParser,
    Wannier90UnitaryMatrixParser,
)
from projectkoios.physkit.units import PhysicalUnit

# Verify the already-used scratch dependency before importing its bound methods.
prior = json.loads(Path('/tmp/ksd-silicon-trial-whitening.json').read_text())
helper_path = Path('/tmp/ksd_silicon_trial_whitening.py')
assert hashlib.sha256(helper_path.read_bytes()).hexdigest() == prior['script_sha256']
import ksd_silicon_trial_whitening as whitening
from common_space.verification.gram_rank import _ExactMatrix
from common_space.verification.native_overlap import CommonSpaceNativeOverlapReconstruction
from common_space.verification.native_precision import CommonSpaceMatrixUncertainty

ROOT = whitening.ROOT
BULK = ROOT / 'calculations/Si/bulk'
REQUEST = whitening.REQUEST


def authenticate(path: Path, byte_count: int, sha256: str) -> bytes:
    payload = path.read_bytes()
    assert len(payload) == byte_count and hashlib.sha256(payload).hexdigest() == sha256, path
    return payload


def run() -> None:
    request_bytes = REQUEST.read_bytes()
    request = json.loads(request_bytes)
    assert request['sources'] == prior['source_identities']
    assert version(request['provider']['distribution']) == request['provider']['version']
    for name, expected in request['provider']['modules'].items():
        module = importlib.import_module(name)
        assert module.__file__ is not None
        assert hashlib.sha256(Path(module.__file__).read_bytes()).hexdigest() == expected
    sources = {}
    for role, declaration in request['sources'].items():
        path = ROOT / declaration['path'] if declaration['location'] == 'repository' else Path(declaration['path'])
        sources[role] = authenticate(path, declaration['byte_size'], declaration['sha256'])
    blocked = json.loads(sources['S110_blocked_result'])
    converter_record = blocked['bound_inputs']['converter_result']
    converter_path = BULK / 'simulations/evidence/sssp-1.3.0-pbe-efficiency-qe-7.5-accepted-s1-pw2wannier90-c6-b20-w21-aiida-precise/result/converter-result.json'
    converter = json.loads(authenticate(converter_path, converter_record['byte_size'], converter_record['sha256']))
    eig_record = converter['eig']
    characterized = json.loads(sources['S30_untruncated_characterization'])
    assert eig_record['sha256'] == characterized['sources']['eig']['sha256']
    eigenvalues = Wannier90EigenvalueParser().execute(
        authenticate(Path(eig_record['path']), eig_record['byte_size'], eig_record['sha256']), PhysicalUnit('eV'),
    ).eigenvalues.magnitude
    aq = Wannier90TrialOrbitalOverlapParser(payload=sources['AMN']).parse().matrices[0]
    dis = Wannier90DisentanglementMatrixParser().execute(sources['disentanglement'])
    gauge = Wannier90UnitaryMatrixParser().execute(sources['gauge'])
    assert tuple(dis.fractional_kpoints.magnitude[0]) == (0.0, 0.0, 0.0)
    assert np.array_equal(dis.fractional_kpoints.magnitude, gauge.fractional_kpoints.magnitude)
    assert eigenvalues.shape == (216, 20)
    preflight_path = BULK / 'simulations/evidence/wannier-localization/run-001/input/campaign-preflight.json'
    preflight = json.loads(preflight_path.read_text())
    win_path = preflight_path.parent / 'silicon.win'
    win_record = preflight['prepared_input']
    win_bytes = authenticate(win_path, win_record['byte_size'], win_record['sha256'])
    assert hashlib.sha256(win_bytes).hexdigest() == '6a6fe1b3193455038a0c4a14038f174f3c0e6244113ee9fb17ff1f42a145a2f3'
    bounds = tuple(preflight['candidate']['outer_window_ev'])
    assert bounds == (-6.0, 21.0)
    energies = np.asarray(eigenvalues[0])
    mask = (energies >= bounds[0]) & (energies <= bounds[1])
    indices = np.flatnonzero(mask).tolist()
    assert indices == list(range(len(indices))), 'Non-prefix window requires an explicit band-row remapping'
    d, u = np.asarray(dis.matrices[0].magnitude), np.asarray(gauge.matrices[0].magnitude)
    assert np.all(d[~mask] == 0), 'Retained frame has components outside declared outer window'
    margin = min(abs(float(e)-edge) for e in energies for edge in bounds)
    # Conditional on the retained S30 twelve-decimal EIG nearest-rounding model.
    eig_error = Fraction(1, 2*10**12) + max(Fraction.from_float(math.ulp(float(e)))/2 for e in energies)
    assert Fraction.from_float(margin) > eig_error
    c = whitening.exact(np.asarray(aq.magnitude)).multiply(CommonSpaceNativeOverlapReconstruction._atomic_transform().adjoint())
    windowed = _ExactMatrix(rows=tuple(c.rows[i] for i in indices))
    projected = whitening.exact(d).multiply(whitening.exact(u)).adjoint().multiply(c)
    trial_error = CommonSpaceMatrixUncertainty.from_parsed_matrix(matrix=aq, native_component_error=Fraction(1, 2*10**12))
    epsilon = trial_error.parsing_error_bound + trial_error.native_error_bound
    results = {}
    for name, matrix in [('full_parent_trials', c), ('outer_window_trials', windowed), ('retained_overlap', projected)]:
        singular = np.linalg.svd(matrix.to_numpy(), compute_uv=False)
        lower, upper = whitening.minimum_bounds(matrix)
        results[name] = {
            'row_count': len(matrix.rows), 'singular_values_nominal': singular.tolist(),
            'minimum_exact_arithmetic_lower_display': float(lower),
            'minimum_exact_arithmetic_upper_display': float(upper),
        }
        if name != 'retained_overlap':
            results[name]['minimum_lower_after_trial_input_error_display'] = float(max(Fraction(0), lower-epsilon))
            results[name]['minimum_upper_after_trial_input_error_display'] = float(upper+epsilon)
            results[name]['injective_under_declared_input_error'] = lower > epsilon
    result = {
        'scope': __doc__, 'window_unchanged_ev': bounds,
        'request_sha256': hashlib.sha256(request_bytes).hexdigest(),
        'helper_script_sha256': prior['script_sha256'],
        'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'eig_identity': eig_record, 'gamma_eigenvalues_ev': energies.tolist(),
        'included_parent_bands_one_based': [i+1 for i in indices],
        'closest_outer_window_boundary_distance_ev': margin,
        'trial_input_error_upper_display': float(epsilon),
        'input_error_model': 'nearest rounding: AMN and EIG twelve decimal places; correctly rounded binary64 parsing',
        'raw_gate_unchanged': request['retained_diagnosis_comparison']['native_uncertainty_bound'],
        'results': results,
    }
    path = Path('/tmp/ksd-silicon-gamma-window.json')
    with path.open('x') as stream:
        json.dump(result, stream, indent=2, allow_nan=False)
        stream.write('\n')
    print(json.dumps(result, indent=2, allow_nan=False))
    print('Output:', path)


if __name__ == '__main__':
    run()
