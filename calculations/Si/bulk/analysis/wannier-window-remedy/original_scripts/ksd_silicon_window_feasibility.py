"""Pointwise algebraic preflight for the first cap interval admitting Gamma band 15.

A representative cap is the midpoint between the retained Gamma band-15
energy and the next larger energy anywhere on the 216-point construction
mesh. This tests one discrete membership class; it is not an optimized,
selected, production-qualified or modified Wannier input.

Let E be a candidate outer space, C its ten trial columns, and F the frozen
orthonormal parent-state frame, of dimension f<=10. If C has full column rank
and F†C has full row rank f, a ten-dimensional W inside E containing F exists
with W†C invertible. Indeed, K=ker(F†C) has dimension 10-f, CK is injective
and orthogonal to F, and W=F direct-sum span(CK) has the required property.
Only these rank conditions are evaluated; no witness W, Hamiltonian or fit is
constructed. This does not prove smoothness, periodicity, locality, symmetry,
optimizer convergence, a frozen raw-gate pass, or band-edge fidelity.
"""
from __future__ import annotations

import hashlib
import importlib
import json
import math
from collections import Counter
from fractions import Fraction
from importlib.metadata import version
from pathlib import Path

import numpy as np
from projectkoios.integrations.wannier90 import (
    Wannier90EigenvalueParser,
    Wannier90TrialOrbitalOverlapParser,
)
from projectkoios.physkit.units import PhysicalUnit

whitening_path = Path('/tmp/ksd-silicon-trial-whitening.json')
whitening_bytes = whitening_path.read_bytes()
whitening = json.loads(whitening_bytes)
helper = Path('/tmp/ksd_silicon_trial_whitening.py')
assert hashlib.sha256(helper.read_bytes()).hexdigest() == whitening['script_sha256']
from ksd_silicon_trial_whitening import exact, minimum_bounds, sanity_checks
from common_space.verification.gram_rank import _ExactMatrix
from common_space.verification.native_overlap import CommonSpaceNativeOverlapReconstruction
from common_space.verification.native_precision import CommonSpaceMatrixUncertainty

ROOT = Path('/Users/eugene/worktrees/ksdft2effmass-silicon-main-package-0matampv')
REQUEST = ROOT / 'calculations/Si/bulk/analysis/c6-b20-w21-slater-koster-definition-fit/common-space-diagnosis-request.json'


def stable_membership(value: float, lower: Fraction, upper: Fraction) -> bool:
    """Require membership to be invariant under the declared EIG rounding error."""
    exact_value = Fraction.from_float(value)
    error = Fraction(1, 2*10**12)+Fraction.from_float(math.ulp(value))/2
    if lower <= exact_value <= upper:
        assert exact_value-error > lower and exact_value+error < upper
        return True
    assert exact_value+error < lower or exact_value-error > upper
    return False


def run() -> None:
    sanity_checks()
    # Negative control: a frozen direction orthogonal to all trials must not certify.
    bad_frozen_overlap = exact(np.zeros((2, 1), dtype=np.complex128))
    try:
        minimum_bounds(bad_frozen_overlap)
    except AssertionError:
        pass
    else:
        raise AssertionError('zero frozen overlap incorrectly certified')
    request_bytes = REQUEST.read_bytes()
    request = json.loads(request_bytes)
    assert request['sources'] == whitening['source_identities']
    assert version(request['provider']['distribution']) == request['provider']['version']
    for name, expected in whitening['module_sha256'].items():
        module = importlib.import_module(name)
        assert module.__file__ is not None
        assert hashlib.sha256(Path(module.__file__).read_bytes()).hexdigest() == expected
    payloads = {}
    for role, declaration in request['sources'].items():
        path = ROOT / declaration['path'] if declaration['location'] == 'repository' else Path(declaration['path'])
        payload = path.read_bytes()
        assert len(payload) == declaration['byte_size'] and hashlib.sha256(payload).hexdigest() == declaration['sha256']
        if role == 'AMN':
            payloads[role] = payload
    excluded_path = Path('/tmp/ksd-silicon-gamma-excluded-bands.json')
    excluded_bytes = excluded_path.read_bytes()
    excluded = json.loads(excluded_bytes)
    assert excluded['request_sha256'] == hashlib.sha256(request_bytes).hexdigest()
    assert excluded['source_identities'] == request['sources']
    eig_source = excluded['eig_identity']
    eig_payload = Path(eig_source['path']).read_bytes()
    assert len(eig_payload) == eig_source['byte_size'] and hashlib.sha256(eig_payload).hexdigest() == eig_source['sha256']
    eig = Wannier90EigenvalueParser().execute(eig_payload, PhysicalUnit('eV')).eigenvalues.magnitude
    amn = Wannier90TrialOrbitalOverlapParser(payload=payloads['AMN']).parse()
    assert eig.shape == (216, 20)
    assert (amn.kpoint_count, amn.band_count, amn.trial_orbital_count) == (216, 20, 10)
    gamma_band15 = Fraction.from_float(float(eig[0, 14]))
    next_energy = min(Fraction.from_float(float(value)) for value in eig.flat if Fraction.from_float(float(value)) > gamma_band15)
    cap = (gamma_band15+next_energy)/2
    low, old_cap = Fraction(-6), Fraction(21)
    frozen_low, frozen_cap = Fraction(-117, 20), Fraction(8)
    transform = CommonSpaceNativeOverlapReconstruction._atomic_transform()
    records = []
    candidate_counts: Counter[int] = Counter()
    old_counts: Counter[int] = Counter()
    frozen_counts: Counter[int] = Counter()
    added_total = 0
    added_indices = []
    band15_admitted = []
    eigen_boundary_clearance = None
    frozen_boundary_clearance = None
    valence_all_frozen = True
    conduction_all_outer = True
    conduction_frozen_count = 0
    for index in range(216):
        energies = [float(value) for value in eig[index]]
        candidate = tuple(i for i, value in enumerate(energies) if stable_membership(value, low, cap))
        old = tuple(i for i, value in enumerate(energies) if stable_membership(value, low, old_cap))
        frozen = tuple(i for i, value in enumerate(energies) if stable_membership(value, frozen_low, frozen_cap))
        assert set(old) <= set(candidate) and set(frozen) <= set(candidate)
        assert 0 < len(frozen) <= 10 <= len(candidate) <= 20
        aq = amn.matrices[index]
        c = exact(np.asarray(aq.magnitude)).multiply(transform.adjoint())
        candidate_c = _ExactMatrix(rows=tuple(c.rows[i] for i in candidate))
        frozen_c = _ExactMatrix(rows=tuple(c.rows[i] for i in frozen))
        trial_lower, _ = minimum_bounds(candidate_c)
        frozen_lower, _ = minimum_bounds(frozen_c.adjoint())
        uncertainty = CommonSpaceMatrixUncertainty.from_parsed_matrix(matrix=aq, native_component_error=Fraction(1, 2*10**12))
        epsilon = uncertainty.parsing_error_bound+uncertainty.native_error_bound
        trial_margin, frozen_margin = trial_lower-epsilon, frozen_lower-epsilon
        assert trial_margin > 0 and frozen_margin > 0, index
        added = tuple(i for i in candidate if i not in old)
        candidate_counts[len(candidate)] += 1
        old_counts[len(old)] += 1
        frozen_counts[len(frozen)] += 1
        added_total += len(added)
        if added:
            added_indices.append(index)
        if 14 in candidate:
            band15_admitted.append(index)
        valence_all_frozen &= set(range(4)) <= set(frozen)
        conduction_all_outer &= 4 in candidate
        conduction_frozen_count += int(4 in frozen)
        for value in energies:
            ev = Fraction.from_float(value)
            error = Fraction(1, 2*10**12)+Fraction.from_float(math.ulp(value))/2
            clearance = min(abs(ev-low), abs(ev-cap))-error
            frozen_clearance = min(abs(ev-frozen_low), abs(ev-frozen_cap))-error
            eigen_boundary_clearance = clearance if eigen_boundary_clearance is None else min(eigen_boundary_clearance, clearance)
            frozen_boundary_clearance = frozen_clearance if frozen_boundary_clearance is None else min(frozen_boundary_clearance, frozen_clearance)
        records.append({
            'ordered_index': index,
            'fractional_coordinates': [round(index//36/6, 10), round((index//6)%6/6, 10), round(index%6/6, 10)],
            'candidate_outer_bands_one_based': [i+1 for i in candidate],
            'newly_admitted_bands_one_based': [i+1 for i in added],
            'unchanged_frozen_bands_one_based': [i+1 for i in frozen],
            'trial_minimum_singular_value_nominal': float(np.linalg.svd(candidate_c.to_numpy(), compute_uv=False)[-1]),
            'trial_minimum_lower_after_input_error_display': float(trial_margin),
            'frozen_overlap_minimum_singular_value_nominal': float(np.linalg.svd(frozen_c.to_numpy(), compute_uv=False)[-1]),
            'frozen_overlap_minimum_lower_after_input_error_display': float(frozen_margin),
            'pointwise_transverse_frozen_preserving_space_exists_under_rounding': trial_margin > 0 and frozen_margin > 0,
        })
    assert eigen_boundary_clearance is not None and frozen_boundary_clearance is not None
    result = {
        'scope': __doc__,
        'request_sha256': hashlib.sha256(request_bytes).hexdigest(),
        'source_identities': request['sources'], 'eig_identity': eig_source,
        'excluded_band_result_sha256': hashlib.sha256(excluded_bytes).hexdigest(),
        'whitening_result_sha256': hashlib.sha256(whitening_bytes).hexdigest(),
        'helper_script_sha256': whitening['script_sha256'],
        'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'rounding_model': 'nearest AMN/EIG twelve decimal places and correctly rounded binary64 parsing; positive margins use exact rational tests',
        'first_tested_cap_membership_class_edge_displays_ev': [float(gamma_band15), float(next_energy)],
        'test_only_outer_window_representative_ev': [-6, float(cap)],
        'unchanged_actual_outer_window_ev': [-6, 21],
        'unchanged_frozen_window_ev': [-5.85, 8],
        'unchanged_actual_raw_gate': request['retained_diagnosis_comparison']['native_uncertainty_bound'],
        'old_outer_count_histogram': dict(sorted(old_counts.items())),
        'candidate_outer_count_histogram': dict(sorted(candidate_counts.items())),
        'unchanged_frozen_count_histogram': dict(sorted(frozen_counts.items())),
        'added_parent_states': added_total, 'changed_point_indices': added_indices,
        'band15_admitted_point_indices': band15_admitted,
        'candidate_eigenvalue_boundary_clearance_lower_display_ev': float(eigen_boundary_clearance),
        'frozen_eigenvalue_boundary_clearance_lower_display_ev': float(frozen_boundary_clearance),
        'pointwise_trial_independence_and_frozen_compatibility_count': len(records),
        'minimum_candidate_trial_sigma_nominal': min(r['trial_minimum_singular_value_nominal'] for r in records),
        'minimum_candidate_trial_sigma_lower_after_error_display': min(r['trial_minimum_lower_after_input_error_display'] for r in records),
        'minimum_frozen_overlap_sigma_nominal': min(r['frozen_overlap_minimum_singular_value_nominal'] for r in records),
        'minimum_frozen_overlap_sigma_lower_after_error_display': min(r['frozen_overlap_minimum_lower_after_input_error_display'] for r in records),
        'sampled_band_edge_coverage_only': {
            'valence_bands_1_through_4_frozen_at_all_construction_points': valence_all_frozen,
            'lowest_conduction_band_inside_candidate_outer_at_all_construction_points': conduction_all_outer,
            'lowest_conduction_band_frozen_point_count': conduction_frozen_count,
            'not_assessed': ['Off-mesh behavior', 'Smooth or symmetry-compatible retained frame', 'New Wannier band-edge fidelity or effective masses', 'New raw-overlap gate', 'Production-qualified PseudoDojo parent'],
        },
        'points': records,
    }
    path = Path('/tmp/ksd-silicon-window-feasibility.json')
    with path.open('x') as stream:
        json.dump(result, stream, indent=2, allow_nan=False)
        stream.write('\n')
    summary = {key: value for key, value in result.items() if key not in ('points', 'source_identities', 'eig_identity', 'scope')}
    print(json.dumps(summary, indent=2, allow_nan=False))
    print('Output:', path)


if __name__ == '__main__':
    run()
