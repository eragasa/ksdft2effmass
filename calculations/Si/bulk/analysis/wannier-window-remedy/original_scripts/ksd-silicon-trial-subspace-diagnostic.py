"""Authorized diagnostic, not a retained CSD1/CSD1-V completion artifact.

A unitary change of trial coordinates does not change singular values or span:
C=A T†. Likewise span(U_dis U)=span(U_dis) for invertible U. No producer
reconstruction code or second native parser is used.

For a candidate left inverse L, exact rational arithmetic bounds
    d >= ||L X-I||_2, m >= ||L||_2.
If d<1, sigma_min(X)>=(1-d)/m. Subtract the declared input-error bound
using Weyl's inequality. These exact tests certify injectivity, NOT acceptance
at the separately frozen overlap threshold. Printed bounds/angles are floating
displays; principal angles are nominal SVD diagnostics, not angle enclosures.
"""
from __future__ import annotations

import hashlib
import importlib
import json
import math
import subprocess
from fractions import Fraction
from importlib.metadata import version
from pathlib import Path

import numpy as np
from numpy.typing import NDArray
from projectkoios.integrations.wannier90 import (
    Wannier90DisentanglementMatrixParser,
    Wannier90TrialOrbitalOverlapParser,
    Wannier90UnitaryMatrixParser,
)
from common_space.verification.gram_rank import _ExactMatrix
from common_space.verification.native_precision import (
    CommonSpaceMatrixUncertainty,
    CommonSpaceNativeRoundingModel,
    CommonSpaceOverlapUncertainty,
)

ROOT = Path('/Users/eugene/worktrees/ksdft2effmass-silicon-main-package-0matampv')
BULK = ROOT / 'calculations/Si/bulk'
REQUEST = BULK / 'analysis/c6-b20-w21-slater-koster-definition-fit/common-space-diagnosis-request.json'


def exact(values: NDArray[np.complex128]) -> _ExactMatrix:
    return _ExactMatrix.from_binary64(tuple(tuple(complex(value) for value in row) for row in values))


def frobenius_upper(matrix: _ExactMatrix) -> Fraction:
    squared = sum((entry.real**2 + entry.imaginary**2 for row in matrix.rows for entry in row), Fraction(0))
    return CommonSpaceMatrixUncertainty._sqrt_upper(squared)


def injectivity_lower(matrix: _ExactMatrix) -> Fraction:
    values = matrix.to_numpy()
    left, singular, right_adjoint = np.linalg.svd(values, full_matrices=False)
    if singular[-1] <= 0:
        return Fraction(0)
    candidate = (right_adjoint.conj().T / singular) @ left.conj().T
    inverse = exact(candidate)
    residual = inverse.multiply(matrix).subtract(_ExactMatrix.diagonal((Fraction(1),) * len(matrix.rows[0])))
    defect = frobenius_upper(residual)
    if defect >= 1:
        return Fraction(0)
    return (1 - defect) / frobenius_upper(inverse)


def minimum_upper(matrix: _ExactMatrix) -> Fraction:
    _, _, right_adjoint = np.linalg.svd(matrix.to_numpy(), full_matrices=False)
    vector = exact(np.asarray(right_adjoint[-1].conj()).reshape(-1, 1))
    # Frobenius norm of a single column equals its vector 2-norm.
    norm_squared = sum((entry.real**2 + entry.imaginary**2 for row in vector.rows for entry in row), Fraction(0))
    norm_lower = CommonSpaceMatrixUncertainty._sqrt_lower(norm_squared)
    assert norm_lower > 0
    return frobenius_upper(matrix.multiply(vector)) / norm_lower


def run() -> None:
    # Analytical sanity checks for the bound, before opening scientific inputs.
    identity = exact(np.eye(2, dtype=np.complex128))
    assert 0 < injectivity_lower(identity) <= 1
    assert minimum_upper(identity) >= 1
    singular = exact(np.ones((2, 2), dtype=np.complex128))
    assert injectivity_lower(singular) == 0

    request_bytes = REQUEST.read_bytes()
    request = json.loads(request_bytes)
    assert version(request['provider']['distribution']) == request['provider']['version']
    providers: dict[str, str] = {}
    for name, expected in request['provider']['modules'].items():
        module = importlib.import_module(name)
        assert module.__file__ is not None
        observed = hashlib.sha256(Path(module.__file__).read_bytes()).hexdigest()
        assert observed == expected, name
        providers[name] = observed
    # Authenticate the additional shared correlation module against the locked revision.
    name = 'projectkoios.integrations.wannier90.artifacts'
    module = importlib.import_module(name)
    assert module.__file__ is not None
    locked = subprocess.check_output([
        'git', '-C', '/Users/eugene/repos/projectkoios-simulations', 'show',
        '841f5e34afd0a83c9a63da10c41a9d513c1caa80:src/python/projectkoios/integrations/wannier90/artifacts.py',
    ])
    assert Path(module.__file__).read_bytes() == locked
    providers[name] = hashlib.sha256(locked).hexdigest()
    payloads: dict[str, bytes] = {}
    for role, declaration in request['sources'].items():
        path = ROOT / declaration['path'] if declaration['location'] == 'repository' else Path(declaration['path'])
        payload = path.read_bytes()
        assert len(payload) == declaration['byte_size']
        assert hashlib.sha256(payload).hexdigest() == declaration['sha256'], role
        if role in ('AMN', 'gauge', 'disentanglement'):
            payloads[role] = payload
    amn = Wannier90TrialOrbitalOverlapParser(payload=payloads['AMN']).parse()
    gauge = Wannier90UnitaryMatrixParser().execute(payloads['gauge'])
    dis = Wannier90DisentanglementMatrixParser().execute(payloads['disentanglement'])
    assert (amn.kpoint_count, amn.band_count, amn.trial_orbital_count) == (216, 20, 10)
    assert (gauge.kpoint_count, gauge.wannier_count) == (216, 10)
    assert (dis.kpoint_count, dis.band_count, dis.wannier_count) == (216, 20, 10)
    points = np.asarray(gauge.fractional_kpoints.magnitude)
    assert np.array_equal(points, dis.fractional_kpoints.magnitude)
    expected = np.asarray([(round(i/6, 10), round(j/6, 10), round(k/6, 10)) for i in range(6) for j in range(6) for k in range(6)])
    assert np.array_equal(points, expected)
    precision = request['native_precision']
    model = CommonSpaceNativeRoundingModel.from_nearest_decimal_places(
        amn=precision['AMN_decimal_places'], gauge=precision['gauge_decimal_places'],
        disentanglement=precision['disentanglement_decimal_places'],
    )
    threshold = Fraction.from_float(request['retained_diagnosis_comparison']['native_uncertainty_bound'])
    records = []
    selected = []
    for index in range(216):
        a_quantity = amn.matrices[index]
        d_quantity = dis.matrices[index]
        u_quantity = gauge.matrices[index]
        a = np.asarray(a_quantity.magnitude)
        d = np.asarray(d_quantity.magnitude)
        u = np.asarray(u_quantity.magnitude)
        qa, sa, _ = np.linalg.svd(a, full_matrices=False)
        qd, sd, _ = np.linalg.svd(d, full_matrices=False)
        exact_a = exact(a)
        a_bound = CommonSpaceMatrixUncertainty.from_parsed_matrix(matrix=a_quantity, native_component_error=model.amn_component_error)
        native_a_error = a_bound.parsing_error_bound + a_bound.native_error_bound
        lower_a = injectivity_lower(exact_a)
        assert lower_a > native_a_error, f'Trial independence unresolved at {index}'
        assert sd[-1] > 0
        cosines = np.linalg.svd(qd.conj().T @ qa, compute_uv=False)
        angles = np.degrees(np.arccos(np.clip(cosines, 0, 1)))
        projected = (d @ u).conj().T @ a
        sb = np.linalg.svd(projected, compute_uv=False)
        record = {
            'ordered_index': index, 'fractional_coordinates': points[index].tolist(),
            'trial_sigma_min_nominal': float(sa[-1]),
            'trial_sigma_min_exact_arithmetic_lower_display': float(lower_a),
            'trial_input_error_upper_display': float(native_a_error),
            'trial_injective_under_declared_rounding': lower_a > native_a_error,
            'overlap_sigma_min_nominal': float(sb[-1]),
            'overlap_rank_at_frozen_threshold_nominal': int(np.count_nonzero(sb > float(threshold))),
            'principal_angles_degrees_nominal': angles.tolist(),
        }
        if index in (0, 12):
            exact_b = exact(d).multiply(exact(u)).adjoint().multiply(exact_a)
            lower_b = injectivity_lower(exact_b)
            upper_b = minimum_upper(exact_b)
            error = CommonSpaceOverlapUncertainty(
                amn=a_bound,
                gauge=CommonSpaceMatrixUncertainty.from_parsed_matrix(matrix=u_quantity, native_component_error=model.gauge_component_error),
                disentanglement=CommonSpaceMatrixUncertainty.from_parsed_matrix(matrix=d_quantity, native_component_error=model.disentanglement_component_error),
            ).combined_error_bound
            record['overlap_sigma_min_exact_arithmetic_lower_display'] = float(lower_b)
            record['overlap_sigma_min_exact_arithmetic_upper_display'] = float(upper_b)
            record['overlap_input_error_upper_display'] = float(error)
            record['parsed_overlap_injectivity_proved'] = lower_b > 0
            record['overlap_injective_under_declared_rounding'] = lower_b > error
            record['overlap_below_frozen_threshold_even_with_input_error'] = upper_b + error < threshold
            record['overlap_sigma_min_lower_after_input_error_display'] = float(max(Fraction(0), lower_b - error))
            selected.append(record)
        records.append(record)
    result = {
        'scope': 'authorized local trial-independence and nominal-principal-angle diagnostic; not retained protocol completion or scientific acceptance',
        'native_rounding_assumption': 'nearest absolute decimal rounding: AMN 12 places, U and U_dis 10; correctly rounded binary64 parsing',
        'angle_status': 'nominal SVD diagnostics only; no certified angle intervals or exact-orthogonality inference',
        'arithmetic_method': 'exact rational left-inverse residual and Frobenius bounds; Weyl input-error subtraction; unitary trial-coordinate change leaves singular values and span unchanged',
        'request_sha256': hashlib.sha256(request_bytes).hexdigest(),
        'source_identities': request['sources'], 'provider_modules': providers,
        'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'numpy_version': np.__version__, 'frozen_overlap_threshold': float(threshold),
        'trial_independence_proved_point_count': len(records), 'selected_points': selected,
        'points': records,
    }
    output = Path('/tmp/ksd-silicon-trial-subspace-diagnostic.json')
    with output.open('x') as stream:
        json.dump(result, stream, indent=2, allow_nan=False)
        stream.write('\n')
    print('Trial independence proved under the declared rounding model at all 216 points.')
    print('Minimum nominal trial singular value:', min(record['trial_sigma_min_nominal'] for record in records))
    print('Minimum exact lower trial bound after native uncertainty:', min(record['trial_sigma_min_exact_arithmetic_lower_display'] - record['trial_input_error_upper_display'] for record in records))
    for record in selected:
        print(json.dumps(record, indent=2, allow_nan=False))
    print('Output:', output)


if __name__ == '__main__':
    run()
