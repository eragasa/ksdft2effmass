"""Authorized trial-metric whitening experiment; no protocol gate or fit.

Whiten C=A T† and D=U_dis using polar factors calculated by SVD, not
normal-equation inversion. span(D U)=span(D) is used only after certifying
that U remains invertible under its declared input error.

For an uncertain full-column-rank X, let epsilon bound ||Delta X||_2 and
ell<=sigma_min(X), with epsilon<ell. Then projector distance is bounded by
eta=epsilon/(ell-epsilon). Equal-rank orthonormal frames can be aligned by
unitaries with frame distance <=2*eta. Thus singular values of their cross
matrix move by at most 2*(eta_C+eta_D). This bounds intrinsic normalized
singular values, NOT the coordinatewise change of one chosen polar gauge.

Exact products Qtilde=X H use binary64 candidate whiteners H. Their Gram
residuals d=||Qtilde†Qtilde-I||_F bound distance to their exact polar frames
by d (when d<1). The cross-product arithmetic correction is bounded by
 d_C+d_D+d_C*d_D. Candidate SVD inverses supply exact residual lower bounds;
a normalized smallest-vector witness supplies an exact upper bound.
No tolerance is used in those rational inequalities. Floating displays are
not outward-rounded certificates. No normalized acceptance threshold is set.
"""
from __future__ import annotations

import hashlib
import importlib
import json
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
from common_space.verification.native_overlap import CommonSpaceNativeOverlapReconstruction
from common_space.verification.native_precision import (
    CommonSpaceMatrixUncertainty,
    CommonSpaceNativeRoundingModel,
)

ROOT = Path('/Users/eugene/worktrees/ksdft2effmass-silicon-main-package-0matampv')
REQUEST = ROOT / 'calculations/Si/bulk/analysis/c6-b20-w21-slater-koster-definition-fit/common-space-diagnosis-request.json'


def exact(values: NDArray[np.complex128]) -> _ExactMatrix:
    return _ExactMatrix.from_binary64(tuple(tuple(complex(v) for v in row) for row in values))


def frobenius(matrix: _ExactMatrix) -> Fraction:
    squared = sum((z.real**2 + z.imaginary**2 for row in matrix.rows for z in row), Fraction(0))
    return CommonSpaceMatrixUncertainty._sqrt_upper(squared)


def gram_defect(matrix: _ExactMatrix) -> Fraction:
    return frobenius(matrix.adjoint().multiply(matrix).subtract(_ExactMatrix.diagonal((Fraction(1),) * len(matrix.rows[0]))))


def minimum_bounds(matrix: _ExactMatrix) -> tuple[Fraction, Fraction]:
    left, singular, right = np.linalg.svd(matrix.to_numpy(), full_matrices=False)
    assert singular[-1] > 0
    inverse = exact((right.conj().T / singular) @ left.conj().T)
    residual = inverse.multiply(matrix).subtract(_ExactMatrix.diagonal((Fraction(1),) * len(matrix.rows[0])))
    defect = frobenius(residual)
    lower = Fraction(0) if defect >= 1 else (1-defect)/frobenius(inverse)
    vector = exact(np.asarray(right[-1].conj()).reshape(-1, 1))
    norm_squared = sum((z.real**2 + z.imaginary**2 for row in vector.rows for z in row), Fraction(0))
    norm_lower = CommonSpaceMatrixUncertainty._sqrt_lower(norm_squared)
    assert norm_lower > 0
    return lower, frobenius(matrix.multiply(vector))/norm_lower


def whitener(values: NDArray[np.complex128]) -> NDArray[np.complex128]:
    _, singular, right = np.linalg.svd(values, full_matrices=False)
    assert singular[-1] > 0
    return (right.conj().T / singular) @ right


def sanity_checks() -> None:
    c = np.asarray([[2, 0], [0, 0.5], [0, 0]], dtype=np.complex128)
    d = np.asarray([[1, 0], [0, 1], [0, 0]], dtype=np.complex128)
    qc, qd = c @ whitener(c), d @ whitener(d)
    np.testing.assert_allclose(qd.conj().T @ qc, np.eye(2), atol=1e-14, rtol=0)
    tilted = np.asarray([[0.5, 0], [0, 1], [np.sqrt(0.75), 0]], dtype=np.complex128)
    nominal = np.linalg.svd((tilted @ whitener(tilted)).conj().T @ qc, compute_uv=False)
    np.testing.assert_allclose(nominal, [1, 0.5], atol=1e-14, rtol=0)
    lower, upper = minimum_bounds(exact(np.diag(np.asarray([1, 0.5], dtype=np.complex128))))
    assert 0 < lower <= Fraction(1, 2) <= upper


def run() -> None:
    sanity_checks()
    request_bytes = REQUEST.read_bytes()
    request = json.loads(request_bytes)
    assert version(request['provider']['distribution']) == request['provider']['version']
    module_identities: dict[str, str] = {}
    for name, expected in request['provider']['modules'].items():
        module = importlib.import_module(name)
        assert module.__file__ is not None
        observed = hashlib.sha256(Path(module.__file__).read_bytes()).hexdigest()
        assert observed == expected, name
        module_identities[name] = observed
    for name in ('common_space.verification.gram_rank', 'common_space.verification.native_overlap', 'common_space.verification.native_precision'):
        module = importlib.import_module(name)
        assert module.__file__ is not None
        module_identities[name] = hashlib.sha256(Path(module.__file__).read_bytes()).hexdigest()
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
    assert np.array_equal(points, np.asarray([(round(i/6, 10), round(j/6, 10), round(k/6, 10)) for i in range(6) for j in range(6) for k in range(6)]))
    precision = request['native_precision']
    model = CommonSpaceNativeRoundingModel.from_nearest_decimal_places(amn=precision['AMN_decimal_places'], gauge=precision['gauge_decimal_places'], disentanglement=precision['disentanglement_decimal_places'])
    frozen_threshold = request['retained_diagnosis_comparison']['native_uncertainty_bound']
    transform = CommonSpaceNativeOverlapReconstruction._atomic_transform()
    records = []
    for index in range(216):
        aq, dq, uq = amn.matrices[index], dis.matrices[index], gauge.matrices[index]
        a, d, u = (np.asarray(q.magnitude) for q in (aq, dq, uq))
        ea, ed, eu = exact(a), exact(d), exact(u)
        ec = ea.multiply(transform.adjoint())
        c = ec.to_numpy()
        hc, hd = whitener(c), whitener(d)
        qc, qd = ec.multiply(exact(hc)), ed.multiply(exact(hd))
        dc, dd, du = gram_defect(qc), gram_defect(qd), gram_defect(eu)
        assert dc < 1 and dd < 1 and du < 1
        ab = CommonSpaceMatrixUncertainty.from_parsed_matrix(matrix=aq, native_component_error=model.amn_component_error)
        db = CommonSpaceMatrixUncertainty.from_parsed_matrix(matrix=dq, native_component_error=model.disentanglement_component_error)
        ub = CommonSpaceMatrixUncertainty.from_parsed_matrix(matrix=uq, native_component_error=model.gauge_component_error)
        epsilon_c = ab.parsing_error_bound + ab.native_error_bound
        epsilon_d = db.parsing_error_bound + db.native_error_bound
        epsilon_u = ub.parsing_error_bound + ub.native_error_bound
        lower_c, _ = minimum_bounds(ec)
        # If ||X†X-I||_2<=d<1, sigma_min(X)>=sqrt(1-d)>=1-d.
        lower_d = max(Fraction(0), 1-gram_defect(ed))
        lower_u = 1-du
        assert lower_c > epsilon_c and lower_d > epsilon_d and lower_u > epsilon_u
        native_normalized_error = 2*(epsilon_c/(lower_c-epsilon_c) + epsilon_d/(lower_d-epsilon_d))
        arithmetic_normalized_error = dc + dd + dc*dd
        normalized = qd.adjoint().multiply(qc)
        lower_n, upper_n = minimum_bounds(normalized)
        total_error = native_normalized_error + arithmetic_normalized_error
        stable_lower = max(Fraction(0), lower_n-total_error)
        nominal = np.linalg.svd(normalized.to_numpy(), compute_uv=False)
        trial_singular = np.linalg.svd(c, compute_uv=False)
        raw = np.linalg.svd((d @ u).conj().T @ c, compute_uv=False)
        record = {
            'ordered_index': index, 'fractional_coordinates': points[index].tolist(),
            'trial_whitener_norm_nominal': float(1/trial_singular[-1]),
            'trial_whitener_norm_upper_under_input_error_display': float(1/(lower_c-epsilon_c)),
            'trial_whitening_condition_nominal': float(trial_singular[0]/trial_singular[-1]),
            'trial_whitened_gram_defect_upper_display': float(dc),
            'retained_whitened_gram_defect_upper_display': float(dd),
            'normalized_sigma_min_nominal': float(nominal[-1]),
            'normalized_condition_number_nominal': float(nominal[0]/nominal[-1]),
            'raw_inverse_amplification_nominal': float(1/raw[-1]),
            'normalized_inverse_amplification_nominal': float(1/nominal[-1]),
            'native_normalized_sigma_error_upper_display': float(native_normalized_error),
            'arithmetic_normalized_sigma_error_upper_display': float(arithmetic_normalized_error),
            'normalized_sigma_lower_after_all_bounds_display': float(stable_lower),
            'normalized_sigma_upper_after_all_bounds_display': float(upper_n+total_error),
            'normalized_injectivity_resolved_under_rounding': stable_lower > 0,
            'normalized_inverse_amplification_upper_under_bounds_display': float(1/stable_lower) if stable_lower > 0 else None,
            'normalized_inverse_times_error_upper_display': float(total_error/stable_lower) if stable_lower > 0 else None,
            'raw_rank_at_unchanged_frozen_threshold_nominal': int(np.count_nonzero(raw > frozen_threshold)),
        }
        records.append(record)
        if index in (0, 12):
            print(json.dumps(record, indent=2, allow_nan=False), flush=True)
    result = {
        'scope': 'authorized local trial-metric whitening diagnostic; no normalized acceptance criterion, fit, source change or protocol completion',
        'rounding_model': 'nearest absolute decimal rounding: AMN 12, U and U_dis 10 decimal places; correctly rounded binary64 parsing',
        'method': __doc__, 'source_identities': request['sources'],
        'request_sha256': hashlib.sha256(request_bytes).hexdigest(),
        'module_sha256': module_identities, 'numpy_version': np.__version__,
        'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'frozen_raw_threshold_unchanged': frozen_threshold,
        'normalized_unresolved_indices': [r['ordered_index'] for r in records if not r['normalized_injectivity_resolved_under_rounding']],
        'raw_deficient_indices': [r['ordered_index'] for r in records if r['raw_rank_at_unchanged_frozen_threshold_nominal'] < 10],
        'points': records,
    }
    output = Path('/tmp/ksd-silicon-trial-whitening.json')
    with output.open('x') as stream:
        json.dump(result, stream, indent=2, allow_nan=False)
        stream.write('\n')
    print('Normalized injectivity unresolved indices:', result['normalized_unresolved_indices'])
    print('Raw deficient indices at unchanged threshold:', result['raw_deficient_indices'])
    print('Largest trial-whitener nominal norm:', max(r['trial_whitener_norm_nominal'] for r in records))
    print('Largest normalized arithmetic correction:', max(r['arithmetic_normalized_sigma_error_upper_display'] for r in records))
    print('Output:', output)


if __name__ == '__main__':
    run()
