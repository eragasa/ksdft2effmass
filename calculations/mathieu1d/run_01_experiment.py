"""Execute and retain immutable version-one local synthetic evidence."""

from __future__ import annotations

import csv
import hashlib
import importlib.metadata
import json
import platform
import subprocess
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from jsonschema import Draft202012Validator  # type: ignore[import-untyped]
from ksdft2effmass.model_systems.mathieu1d import (
    Mathieu1dStudyDefinition,
    Mathieu1dStudyEvaluator,
    Mathieu1dStudyInputDeserializer,
    Mathieu1dStudyInputSerializer,
    Mathieu1dStudyResult,
    Mathieu1dStudyResultSerializer,
    Mathieu1dStudyVerificationResult,
    Mathieu1dStudyVerificationSerializer,
    Mathieu1dStudyVerifier,
)
from ksdft2effmass.model_systems.mathieu1d.study import canonical_json_bytes
from projectkoios.physkit.units import ScalarQuantity

type JsonScalar = None | bool | int | float | str
type JsonValue = JsonScalar | list[JsonValue] | dict[str, JsonValue]

MATHIEU1D_STUDY_VERSION_ID = (
    "ksdft2effmass.campaign.periodic-reduction.periodic1d."
    "single-band-fourier-reduction.v1"
)
RUN_ID = f"{MATHIEU1D_STUDY_VERSION_ID}.run-20261014T184707Z"
EXPECTED_OPTIMIZATION_REVISION = "d9a82252faa1b41d82cce11149329aa91b84dff0"
EXPECTED_PHYSKIT_REVISION = "62ee89870db74b7b8b374c42add72701fd95d3a4"
HISTORICAL_REVISION = "9a65849d886d5be499b2664e2b653c3983fab06e"
HISTORICAL_PATH = "calculations/ICMSEP2026/conference/paper_1/isolated-band"
HISTORICAL_TREE = "418999a90efa3001d2e50a2e7912f126bc30903f"
CALCULATION_ROOT = Path(__file__).resolve().parent
INPUT_PATH = CALCULATION_ROOT / "input.json"

HISTORICAL_DIGESTS: dict[str, JsonValue] = {
    "input.json": "62899d4cd550db9d0bd69a8d97149ccfea312c6b20be9c395e8765734693bf65",
    "result.json": "c7262e3527a58dfd8fe237fa495549c53a1a65f3e46a98ed6d40673f14b6a394",
    "verification.json": (
        "9b37dc896a3a438a04dc19c46dd9d431230901ef82bfd9e7181ff5b7504b21a1"
    ),
    "SHA256SUMS": "64f16168fa05fefa902f8c2216b1e445c6a0ecd8e28dcebd75c73589833edf5f",
}


def definition() -> Mathieu1dStudyDefinition:
    """Decode the canonical version-one calculation input."""
    return Mathieu1dStudyInputDeserializer().execute(INPUT_PATH.read_bytes())


def sha256(path: Path) -> str:
    """Return one lowercase SHA-256 digest."""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def root() -> Path:
    """Return repository root from this fixed experiment location."""
    return Path(__file__).resolve().parents[2]


def source_paths(repository: Path) -> tuple[Path, ...]:
    """Return every in-scope source and exact dependency declaration."""
    experiment = Path(__file__).resolve().parent
    paths = [
        path
        for path in experiment.rglob("*.py")
        if ".venv" not in path.parts and "__pycache__" not in path.parts
    ]
    paths.extend(experiment.joinpath("schemas").glob("*.json"))
    paths.extend(
        (
            experiment / "README.md",
            experiment / "input.json",
            experiment / "runs/README.md",
            experiment / "protocol.md",
            experiment / "evidence-policy.md",
            repository / "python/pyproject.toml",
            repository / "python/uv.lock",
        )
    )
    return tuple(sorted(set(paths)))


def write_source_manifest(destination: Path, repository: Path) -> None:
    """Bind dirty-worktree source bytes rather than claiming base-commit identity."""
    lines = [
        f"{sha256(path)}  {path.relative_to(repository).as_posix()}"
        for path in source_paths(repository)
    ]
    destination.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _json_object(wire: str | bytes, name: str) -> dict[str, JsonValue]:
    """Decode one JSON mapping under the recursive finite evidence boundary."""
    value: JsonValue = json.loads(wire)
    if not isinstance(value, dict):
        raise TypeError(f"{name} root must be a dict")
    return value


def _json_number(value: JsonValue, name: str) -> float:
    """Return one built-in JSON number while rejecting booleans."""
    if type(value) is int:
        return float(value)
    if type(value) is float:
        return value
    raise TypeError(f"{name} must be a JSON number")


def _gap_magnitude(value: ScalarQuantity | None, name: str) -> float:
    """Return one experiment-required sampled external-gap magnitude."""
    if value is None:
        raise ValueError(f"{name} must be retained")
    return value.magnitude


def installed_vcs_commit(distribution_name: str, expected: str) -> str:
    """Return and authenticate one installed VCS direct-url commit identity."""
    direct_url = importlib.metadata.distribution(distribution_name).read_text(
        "direct_url.json"
    )
    if direct_url is None:
        raise RuntimeError(f"{distribution_name} has no direct_url.json")
    document = _json_object(direct_url, f"{distribution_name} direct_url")
    vcs_info = document.get("vcs_info")
    if not isinstance(vcs_info, dict):
        raise TypeError(f"{distribution_name} has no VCS identity")
    vcs = vcs_info.get("vcs")
    commit_id = vcs_info.get("commit_id")
    if vcs != "git" or type(commit_id) is not str:
        raise RuntimeError(f"{distribution_name} has no exact Git commit identity")
    if commit_id != expected:
        raise RuntimeError(
            f"{distribution_name} commit {commit_id} does not match {expected}"
        )
    return commit_id


def parity_document(
    result: Mathieu1dStudyResult,
    historical: dict[str, JsonValue],
) -> dict[str, JsonValue]:
    """Compare successor channels with the retained historical result."""
    if type(result) is not Mathieu1dStudyResult:
        raise TypeError("result must be Mathieu1dStudyResult")
    defects: list[float] = []
    historical_plane = historical["plane_wave_convergence"]
    historical_fd = historical["finite_difference_convergence"]
    historical_ranges = historical["range_study"]
    if not isinstance(historical_plane, list) or not isinstance(historical_fd, list):
        raise TypeError("historical refinement channels must be lists")
    if not isinstance(historical_ranges, list):
        raise TypeError("historical range_study must be a list")
    for plane_wave_successor, predecessor in zip(
        result.plane_wave_refinement, historical_plane, strict=True
    ):
        if not isinstance(predecessor, dict):
            raise TypeError("historical plane-wave entry must be a dict")
        quantity = predecessor["maximum_absolute_error"]
        if not isinstance(quantity, dict):
            raise TypeError("historical plane-wave quantity must be a dict")
        defects.append(
            abs(
                plane_wave_successor.maximum_absolute_error.magnitude
                - _json_number(quantity["magnitude"], "plane-wave magnitude")
            )
        )
    for finite_difference_successor, predecessor in zip(
        result.finite_difference_refinement, historical_fd, strict=True
    ):
        if not isinstance(predecessor, dict):
            raise TypeError("historical finite-difference entry must be a dict")
        quantity = predecessor["maximum_absolute_error"]
        if not isinstance(quantity, dict):
            raise TypeError("historical finite-difference quantity must be a dict")
        defects.append(
            abs(
                finite_difference_successor.maximum_absolute_error.magnitude
                - _json_number(quantity["magnitude"], "finite-difference magnitude")
            )
        )
    for range_successor, predecessor in zip(
        result.reduction.range_study, historical_ranges, strict=True
    ):
        if not isinstance(predecessor, dict):
            raise TypeError("historical range entry must be a dict")
        for historical_key, successor_value in (
            (
                "training_maximum_absolute_error",
                range_successor.training_error.maximum_absolute_error.magnitude,
            ),
            (
                "withheld_maximum_absolute_error",
                range_successor.evaluation_error.maximum_absolute_error.magnitude,
            ),
            (
                "omitted_block_l2_norm",
                range_successor.truncation.omitted_block_l2_norm,
            ),
        ):
            quantity = predecessor[historical_key]
            if not isinstance(quantity, dict):
                raise TypeError("historical range quantity must be a dict")
            defects.append(
                abs(
                    successor_value
                    - _json_number(quantity["magnitude"], historical_key)
                )
            )
    maximum = max(defects, default=0.0)
    return {
        "schema": f"{MATHIEU1D_STUDY_VERSION_ID}.historical-parity.v1",
        "run_id": RUN_ID,
        "historical_revision": HISTORICAL_REVISION,
        "historical_path": HISTORICAL_PATH,
        "maximum_matched_channel_absolute_defect": maximum,
        "absolute_tolerance": 1.0e-12,
        "passes": maximum <= 1.0e-12,
        "improved_capabilities": {
            "strictly_positive_explicit_fitting_weights": True,
            "explicit_objective_construction_and_evaluation_roles": True,
            "caller_selected_hopping_ranges": True,
            "sampled_training_external_gap": _gap_magnitude(
                result.training_gap.external_minimum_gap,
                "training external gap",
            ),
            "sampled_evaluation_external_gap": _gap_magnitude(
                result.evaluation_gap.external_minimum_gap,
                "evaluation external gap",
            ),
            "rank_and_conditioning_retained_for_every_range": all(
                item.direct_fit.is_identified
                and item.direct_fit.design_condition_number is not None
                for item in result.reduction.range_study
            ),
            "independent_typed_verification": True,
            "canonical_versioned_wire_documents": True,
        },
        "claim_boundary": (
            "Parity is bounded numerical/software evidence and does not establish "
            "scientific validation or continuum isolation."
        ),
    }


def write_figure_data(destination: Path, result: Mathieu1dStudyResult) -> None:
    """Write the range channels consumed by the successor figure."""
    if type(result) is not Mathieu1dStudyResult:
        raise TypeError("result must be Mathieu1dStudyResult")
    with destination.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(
            (
                "maximum_range",
                "training_maximum_absolute_error",
                "evaluation_maximum_absolute_error",
                "omitted_block_l2_norm",
                "direct_mediated_coefficient_defect",
                "design_rank",
                "design_condition_number",
            )
        )
        for item in result.reduction.range_study:
            writer.writerow(
                (
                    item.maximum_range,
                    format(
                        item.training_error.maximum_absolute_error.magnitude, ".17g"
                    ),
                    format(
                        item.evaluation_error.maximum_absolute_error.magnitude, ".17g"
                    ),
                    format(item.truncation.omitted_block_l2_norm, ".17g"),
                    format(
                        item.route_comparison.coefficient_l2_frobenius_defect.magnitude,
                        ".17g",
                    ),
                    item.direct_fit.design_rank,
                    format(item.direct_fit.design_condition_number or 0.0, ".17g"),
                )
            )


def write_figure(destination: Path, result: Mathieu1dStudyResult) -> None:
    """Generate a compact publication figure from the retained typed result."""
    if type(result) is not Mathieu1dStudyResult:
        raise TypeError("result must be Mathieu1dStudyResult")
    ranges = np.asarray(
        [item.maximum_range for item in result.reduction.range_study], dtype=np.int64
    )
    training = np.asarray(
        [
            item.training_error.maximum_absolute_error.magnitude
            for item in result.reduction.range_study
        ]
    )
    evaluation = np.asarray(
        [
            item.evaluation_error.maximum_absolute_error.magnitude
            for item in result.reduction.range_study
        ]
    )
    omitted = np.asarray(
        [item.truncation.omitted_block_l2_norm for item in result.reduction.range_study]
    )
    figure, axes = plt.subplots(1, 2, figsize=(8.4, 3.4), constrained_layout=True)
    axes[0].semilogy(ranges, training, "o-", label="training maximum")
    axes[0].semilogy(ranges, evaluation, "s--", label="evaluation maximum")
    axes[0].set(xlabel="maximum hopping range", ylabel="absolute error ($E_G$)")
    axes[0].legend(frameon=False)
    axes[1].semilogy(ranges, omitted, "o-", color="tab:purple")
    axes[1].set(xlabel="maximum hopping range", ylabel="omitted-block norm ($E_G$)")
    figure.suptitle("Single-band Fourier reduction v1")
    figure.savefig(destination, dpi=200)
    plt.close(figure)


def write_report(
    destination: Path,
    result: Mathieu1dStudyResult,
    verification: Mathieu1dStudyVerificationResult,
    parity_passes: bool,
) -> None:
    """Write a concise human-readable evidence summary."""
    if type(result) is not Mathieu1dStudyResult:
        raise TypeError("result must be Mathieu1dStudyResult")
    if type(verification) is not Mathieu1dStudyVerificationResult:
        raise TypeError("verification has the wrong type")
    last = result.reduction.range_study[-1]
    cutoff_five = result.plane_wave_refinement[1].maximum_absolute_error.magnitude
    finite_difference_31 = result.finite_difference_refinement[
        0
    ].maximum_absolute_error.magnitude
    finite_difference_255 = result.finite_difference_refinement[
        -1
    ].maximum_absolute_error.magnitude
    reconstruction = (
        result.reduction.complete_transform.reconstruction_maximum_frobenius_error
    )
    training_gap = _gap_magnitude(
        result.training_gap.external_minimum_gap, "training external gap"
    )
    evaluation_gap = _gap_magnitude(
        result.evaluation_gap.external_minimum_gap, "evaluation external gap"
    )
    text = f"""# Retained single-band Fourier-reduction run

- Version: `{MATHIEU1D_STUDY_VERSION_ID}`
- Run: `{RUN_ID}`
- Evidence class: controlled local synthetic numerical verification
- Independent verification: `{"pass" if verification.passes else "fail"}`
- Historical matched-channel parity: `{"pass" if parity_passes else "fail"}`

The historical controls were reproduced without external calculators. The cutoff-5
plane-wave discrepancy is `{cutoff_five:.17g}` `E_G`; the 31/255-point
finite-difference discrepancies are `{finite_difference_31:.17g}` and
`{finite_difference_255:.17g}` `E_G`. The complete transform reconstruction defect is
`{reconstruction:.17g}` `E_G`.
At range eight the disjoint evaluation maximum error is
`{last.evaluation_error.maximum_absolute_error.magnitude:.17g}` `E_G`.

The successor additionally retains positive objective weights, explicit training and
evaluation roles, caller-selected ranges, sampled external gaps
(`{training_gap:.17g}` and `{evaluation_gap:.17g}` `E_G`), per-range rank and
conditioning, exact conventions and units, canonical versioned documents, and an
independent direct-formula verifier. The maximum independent energy and squared-energy
defects are `{verification.energy_maximum_absolute_defect.magnitude:.17g}` and
`{verification.squared_energy_maximum_absolute_defect.magnitude:.17g}`.

No sampled gap is promoted to a continuum isolation certificate, no hopping range is
selected as scientifically adequate, and no material validation or uncertainty
quantification is claimed.
"""
    destination.write_text(text, encoding="utf-8")


def validate_document(experiment_root: Path, name: str, wire: bytes) -> None:
    """Require canonical bytes and strict draft-2020-12 schema validity."""
    document = _json_object(wire, f"{name} document")
    if canonical_json_bytes(document) != wire:
        raise ValueError(f"{name} document is not canonical")
    schema = _json_object(
        (experiment_root / "schemas" / f"{name}.schema.json").read_text(
            encoding="utf-8"
        ),
        f"{name} schema",
    )
    Draft202012Validator.check_schema(schema)
    Draft202012Validator(schema).validate(document)


def main() -> int:
    """Execute, independently verify, and retain one no-overwrite package."""
    repository = root()
    experiment_root = Path(__file__).resolve().parent
    optimization_revision = installed_vcs_commit(
        "projectkoios-optimization", EXPECTED_OPTIMIZATION_REVISION
    )
    physkit_revision = installed_vcs_commit(
        "projectkoios-physkit", EXPECTED_PHYSKIT_REVISION
    )
    destination = experiment_root / "runs" / RUN_ID
    destination.mkdir(parents=True, exist_ok=False)
    controls = definition()
    result = Mathieu1dStudyEvaluator().execute(controls)
    verification = Mathieu1dStudyVerifier().execute(result)
    if not verification.passes:
        raise RuntimeError("independent verification failed")

    input_wire = Mathieu1dStudyInputSerializer().execute(controls)
    result_wire = Mathieu1dStudyResultSerializer().execute(result)
    verification_wire = Mathieu1dStudyVerificationSerializer().execute(verification)
    for name, wire in (
        ("input", input_wire),
        ("result", result_wire),
        ("verification", verification_wire),
    ):
        validate_document(experiment_root, name, wire)
        (destination / f"{name}.json").write_bytes(wire)
    historical_path = repository / HISTORICAL_PATH / "result.json"
    historical = _json_object(
        historical_path.read_text(encoding="utf-8"), "historical result"
    )
    parity = parity_document(result, historical)
    (destination / "parity.json").write_bytes(canonical_json_bytes(parity))
    write_figure_data(destination / "figure-data.csv", result)
    write_figure(destination / "single-band-fourier-reduction-summary.png", result)
    parity_passes = parity.get("passes")
    if type(parity_passes) is not bool:
        raise TypeError("parity passes must be a built-in bool")
    write_report(destination / "report.md", result, verification, parity_passes)
    write_source_manifest(destination / "source.sha256", repository)

    git_head = subprocess.run(
        ("git", "rev-parse", "HEAD"),
        cwd=repository,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    git_status = subprocess.run(
        ("git", "status", "--short"),
        cwd=repository,
        check=True,
        capture_output=True,
        text=True,
    ).stdout
    provenance: dict[str, JsonValue] = {
        "schema": f"{MATHIEU1D_STUDY_VERSION_ID}.provenance.v1",
        "run_id": RUN_ID,
        "recorded_at_utc": "2026-10-14T18:47:07Z",
        "repository": {
            "git_head": git_head,
            "worktree_was_dirty": bool(git_status),
            "source_manifest": "source.sha256",
            "source_manifest_sha256": sha256(destination / "source.sha256"),
        },
        "dependencies": {
            "projectkoios_optimization_git_revision": optimization_revision,
            "projectkoios_physkit_git_revision": physkit_revision,
            "ksdft2effmass_version": importlib.metadata.version("ksdft2effmass"),
            "numpy_version": np.__version__,
            "scipy_version": importlib.metadata.version("scipy"),
        },
        "runtime": {
            "python": platform.python_version(),
            "implementation": platform.python_implementation(),
            "platform": platform.platform(),
            "executable": str(Path(sys.executable).relative_to(repository)),
        },
        "execution_boundary": (
            "Local deterministic synthetic in-process numerical work only; no "
            "external calculator, scheduler, remote resource, or material data."
        ),
        "historical_predecessor": {
            "alias": "M1",
            "git_revision": HISTORICAL_REVISION,
            "repository_relative_path": HISTORICAL_PATH,
            "git_tree": HISTORICAL_TREE,
            "sha256": HISTORICAL_DIGESTS,
            "disposition": (
                "preserved-unchanged-and-superseded-for-live-publication-citation"
            ),
        },
    }
    (destination / "provenance.json").write_bytes(canonical_json_bytes(provenance))

    retained_files = tuple(
        sorted(
            path
            for path in destination.iterdir()
            if path.name not in {"SHA256SUMS", "evidence-package-identity.txt"}
        )
    )
    manifest = "".join(f"{sha256(path)}  {path.name}\n" for path in retained_files)
    (destination / "SHA256SUMS").write_text(manifest, encoding="utf-8")
    evidence_identity = f"sha256:{sha256(destination / 'SHA256SUMS')}"
    (destination / "evidence-package-identity.txt").write_text(
        evidence_identity + "\n", encoding="utf-8"
    )
    print(RUN_ID)
    print(evidence_identity)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
