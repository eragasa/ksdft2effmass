#!/usr/bin/env python3
"""Compose the existing independent verifier for the adopted historical S30 case.

No producer numerical implementation is imported. Source declarations are the
already adopted input data; producer result bytes are only authenticated until
CommonSpaceVerificationRun has computed and retained its independent result.
This script is not execution authority and does not run CSD2 or calculators.
"""

from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from pathlib import Path

BULK = Path(__file__).resolve().parents[2]
REPOSITORY = BULK.parents[2]
sys.path.insert(0, str(BULK))

from common_space.verification.grid_verification import (  # noqa: E402
    CommonSpaceVerificationOutcome,
)
from common_space.verification.native_inputs import (  # noqa: E402
    CommonSpaceNativeInputContract,
    CommonSpaceNativeInputLoader,
    CommonSpaceProviderBinding,
    CommonSpaceProviderModuleIdentity,
    CommonSpaceTrialConvention,
)
from common_space.verification.native_precision import (  # noqa: E402
    CommonSpaceNativeRoundingModel,
)
from common_space.verification.source_admission import (  # noqa: E402
    CommonSpaceEvidenceRole,
    CommonSpaceReviewScope,
    CommonSpaceSourceAdmission,
    CommonSpaceSourceEvidence,
    CommonSpaceVerificationJson,
    JsonValue,
)
from common_space.verification.verification_io import (  # noqa: E402
    CommonSpaceProducerCorrelationRun,
    CommonSpaceVerificationRun,
)
from projectkoios.integrations.wannier90 import (  # noqa: E402
    Wannier90NativeArtifact,
    Wannier90NativeArtifactCorrelator,
    Wannier90NativeArtifactIdentity,
)


@dataclass(frozen=True, slots=True)
class RetainedSiliconCommonSpaceVerification:
    """Single-case source composition, not another verification implementation."""

    @staticmethod
    def _object(value: JsonValue) -> dict[str, JsonValue]:
        if type(value) is not dict:
            raise ValueError("expected an explicit JSON object")
        return value

    @staticmethod
    def _list(value: JsonValue) -> list[JsonValue]:
        if type(value) is not list:
            raise ValueError("expected an explicit JSON array")
        return value

    @staticmethod
    def _text(value: JsonValue) -> str:
        if type(value) is not str or not value:
            raise ValueError("expected a nonempty JSON string")
        return value

    @staticmethod
    def _integer(value: JsonValue) -> int:
        if type(value) is not int:
            raise ValueError("expected a built-in integer, not a boolean or string")
        return value

    @classmethod
    def _identity(cls, value: JsonValue) -> Wannier90NativeArtifactIdentity:
        row = cls._object(value)
        return Wannier90NativeArtifactIdentity(
            name=cls._text(row["name"]),
            byte_count=cls._integer(row["byte_count"]),
            sha256=cls._text(row["sha256"]),
        )

    @staticmethod
    def _load(
        path: Path, expected: Wannier90NativeArtifactIdentity
    ) -> Wannier90NativeArtifact:
        if path.name != expected.name or path.is_symlink() or not path.is_file():
            raise ValueError(
                f"source is not its explicitly declared regular file: {path}"
            )
        artifact = Wannier90NativeArtifact(
            name=expected.name, payload=path.read_bytes()
        )
        Wannier90NativeArtifactCorrelator().execute(
            expected_identities=(expected,), artifacts=(artifact,)
        )
        return artifact

    @staticmethod
    def _repository_path(value: str) -> Path:
        path = Path(value)
        if path.is_absolute() or ".." in path.parts:
            raise ValueError("repository source must remain under the declared root")
        result = REPOSITORY / path
        if not result.resolve().is_relative_to(REPOSITORY.resolve()):
            raise ValueError("repository source escapes through a symlink")
        return result

    def prepare(self) -> CommonSpaceSourceAdmission:
        """Authenticate real evidence; do not regenerate assertions or prerequisites."""
        wire = CommonSpaceVerificationJson
        request_path = (
            BULK
            / "analysis/c6-b20-w21-slater-koster-definition-fit/common-space-diagnosis-request.json"
        )
        request_identity = Wannier90NativeArtifactIdentity(
            name=request_path.name,
            byte_count=5458,
            sha256="0dd0d97cdc6134a30073b9d54a54077bba93b579882ef709de47534ca59ff89e",
        )
        request_artifact = self._load(request_path, request_identity)
        request = self._object(wire.decode(request_artifact.payload))
        declaration_path = (
            BULK / "analysis/wannier-window-remedy/source-state-assertions.json"
        )
        declaration_identity = Wannier90NativeArtifactIdentity(
            name=declaration_path.name,
            byte_count=17424,
            sha256="c01997f800728dfb7ac1925e8719af22033d4437949c72a3294850dd87a3add3",
        )
        declaration = self._load(declaration_path, declaration_identity)
        state = self._object(wire.decode(declaration.payload))
        producer = BULK / "analysis/common-space-producer/run-001"
        completion_identity = Wannier90NativeArtifactIdentity(
            name="producer-completion.json",
            byte_count=810,
            sha256="0d03312dea85e6881fa432ee15f402ab9d0011e9312bfff749dcf2dc9d28c452",
        )
        completion_artifact = self._load(
            producer / completion_identity.name, completion_identity
        )
        completion = self._object(wire.decode(completion_artifact.payload))
        # These two expected result identities come from the pinned ACTUAL receipt,
        # never from decoding producer rank/spectrum/weight values.
        expected_results = {
            self._text(row["role"]): self._identity(row["identity"])
            for value in self._list(completion["completed_evidence"])
            for row in (self._object(value),)
        }
        declared_sources = self._object(request["sources"])
        paths: dict[str, Path] = {}
        for label, value in declared_sources.items():
            source = self._object(value)
            location, name = self._text(source["location"]), self._text(source["path"])
            if location == "repository":
                paths[label] = self._repository_path(name)
            elif location == "absolute" and Path(name).is_absolute():
                paths[label] = Path(name)
            else:
                raise ValueError("unsupported explicit source location")
        source_paths = {
            CommonSpaceEvidenceRole.request: request_path,
            CommonSpaceEvidenceRole.full_source: paths[
                "S30_untruncated_characterization"
            ],
            CommonSpaceEvidenceRole.full_support: paths[
                "S105_full_support_disposition"
            ],
            CommonSpaceEvidenceRole.blocked_alignment: paths["S110_blocked_result"],
            CommonSpaceEvidenceRole.protocol: paths["hopping_first_protocol"],
            CommonSpaceEvidenceRole.state_assertions: declaration_path,
            CommonSpaceEvidenceRole.producer_completion: producer
            / completion_identity.name,
            CommonSpaceEvidenceRole.producer_reconstruction: producer / "result.json",
            CommonSpaceEvidenceRole.symmetry_inventory: producer
            / "point-inventory.json",
        }
        identities = {
            self._text(row["role"]): self._identity(row["identity"])
            for value in self._list(state["source_ledger"])
            for row in (self._object(value),)
        }
        identities.update(expected_results)
        identities[CommonSpaceEvidenceRole.state_assertions.to_wire()] = (
            declaration_identity
        )
        identities[CommonSpaceEvidenceRole.producer_completion.to_wire()] = (
            completion_identity
        )
        evidence = tuple(
            CommonSpaceSourceEvidence(
                role=role,
                expected=identities[role.to_wire()],
                artifact=self._load(source_paths[role], identities[role.to_wire()]),
            )
            for role in CommonSpaceEvidenceRole
        )
        # Remaining source bindings are those of the unchanged adopted decision.
        # This authenticates them without importing producer source-association code.
        converter = Path(
            "/Users/eugene/projects/ksdft2effmass/si-accepted-s1-pw2wannier90-c6-b20-w21-aiida-precise-v1/run"
        )
        localization = Path(
            "/Users/eugene/projects/ksdft2effmass/si-accepted-s1-wannier90-localization-c6-b20-w21-aiida-precise-v1/run"
        )
        nscf = Path(
            "/Users/eugene/projects/ksdft2effmass/si-accepted-s1-wannier-nscf-6x6x6-b20-david-c6-b20-v1/run"
        )
        extra = (
            (
                converter / "silicon.eig",
                168480,
                "a54f31f8f72cd32b63ad78e47378cd0a8ce97474ad223606f88d48c97c890dd2",
            ),
            (
                localization / "silicon_hr.dat",
                1396475,
                "24a411c875b3e66bba37e28cc6bf2d95c38ef521c39f81fde40cd0bfa294ea55",
            ),
            (
                localization / "silicon_wsvec.dat",
                1365185,
                "f40fa7f81afaa9bcf9614c6e3c53c14db0db6b0b429b84bfd10f2e40474de1a0",
            ),
            (
                BULK
                / "simulations/evidence/sssp-1.3.0-pbe-efficiency-qe-7.5-accepted-s1-wannier-nscf-6x6x6-b20-david-c6-b20/input/pw.in",
                13911,
                "20a6ee6e55d632bb66b1afcaac91592bf49c73a3e53e275659d1ccb03e47e1f9",
            ),
            (
                nscf / "tmp/system.save/data-file-schema.xml",
                371723,
                "2e1b5e157142d18210d18710fb9f5f3e813b17d8331acf96e11af9b9d4f7ef8c",
            ),
            (
                nscf / "nscf-saved-state-manifest.json",
                44898,
                "24ee9d483141ab54d099bc6e6403d0da46108cc7a30c5b019992da3a1d7ef3ac",
            ),
            (
                BULK
                / "simulations/structures/Si.PrimitiveUnitCell.RightHanded.RelaxedS1.json",
                758,
                "d131107753512c53dc0a32b9e07e0081f8277d8eeafcb9fad5f1fc7f153ded03",
            ),
            (
                BULK
                / "simulations/evidence/wannier-localization/run-001/input/localization-input-manifest.json",
                1413,
                "523515dffc883abf1bc0ff3e1427eea13e85a12774a5ce2040e3dd43c396568e",
            ),
        )
        for path, count, digest in extra:
            self._load(
                path,
                Wannier90NativeArtifactIdentity(
                    name=path.name, byte_count=count, sha256=digest
                ),
            )
        decision = BULK / "protocol/decisions/s30-state-identification.md"
        # Its exact size is metadata here; its predeclared digest is the trust root.
        decision_payload = decision.read_bytes()
        self._load(
            decision,
            Wannier90NativeArtifactIdentity(
                name=decision.name,
                byte_count=len(decision_payload),
                sha256="3c74b8bbd684b0aac6d47d44fdc52920c6435ad1f21292b8983c4f91f64ecf51",
            ),
        )
        native_identities = tuple(
            self._identity(value) for value in self._list(state["native_identities"])
        )
        if len(native_identities) != 3:
            raise ValueError("all three native roles are required")
        points: list[tuple[float, float, float]] = []
        for value in self._list(state["ordered_fractional_kpoints"]):
            row = self._list(value)
            if len(row) != 3 or any(type(component) is not float for component in row):
                raise ValueError(
                    "declared native presentations require three built-in floats"
                )
            x, y, z = row
            assert type(x) is float and type(y) is float and type(z) is float
            points.append((x, y, z))
        provider = self._object(request["provider"])
        modules = dict(self._object(provider["modules"]))
        modules["projectkoios.integrations.wannier90.artifacts"] = (
            "f4f4736ef96093ecb5f06f7a5f27cd2a215e726b0b68146e4e9b83f99c6f4be8"
        )
        binding = CommonSpaceProviderBinding(
            distribution_version=self._text(provider["version"]),
            modules=tuple(
                CommonSpaceProviderModuleIdentity(
                    module_name=name, sha256=self._text(modules[name])
                )
                for name in CommonSpaceProviderBinding.REQUIRED_MODULES
            ),
        )
        contract = CommonSpaceNativeInputContract(
            trial_overlap_identity=native_identities[0],
            gauge_identity=native_identities[1],
            disentanglement_identity=native_identities[2],
            ordered_fractional_kpoints=tuple(points),
            parent_band_count=self._integer(state["parent_band_count"]),
            atomic_basis_order=tuple(
                self._text(value) for value in self._list(state["atomic_basis_order"])
            ),
            trial_convention=CommonSpaceTrialConvention.two_center_sp3s_star,
            geometry_identity=self._text(state["geometry_identity"]),
            energy_reference_identity=self._text(state["energy_reference_identity"]),
        )
        parsed = CommonSpaceNativeInputLoader(
            contract=contract,
            provider_binding=binding,
            artifacts=tuple(
                self._load(paths[label], identity)
                for label, identity in zip(
                    ("AMN", "gauge", "disentanglement"), native_identities, strict=True
                )
            ),
        ).execute()
        errors = tuple(
            wire.read_rational(value)
            for value in self._list(state["native_component_errors"])
        )
        if len(errors) != 3:
            raise ValueError("all native component bounds must be explicit")
        admission = CommonSpaceSourceAdmission(
            parsed_inputs=parsed,
            rounding_model=CommonSpaceNativeRoundingModel(
                amn_component_error=errors[0],
                gauge_component_error=errors[1],
                disentanglement_component_error=errors[2],
            ),
            frozen_rank_threshold=wire.read_rational(state["frozen_rank_threshold"]),
            review_scope=CommonSpaceReviewScope.retained,
            review_reference=self._text(state["review_reference"]),
            parent_band_state_identity=self._text(state["parent_band_state_identity"]),
            gauge_state_identity=self._text(state["gauge_state_identity"]),
            evidence=evidence,
        )
        admission.authenticate()
        return admission


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument(
        "--check-only",
        action="store_true",
        help="authenticate the complete real bundle; no numerical reconstruction",
    )
    mode.add_argument(
        "--output-root",
        type=Path,
        help="fresh output directory for the independent result and subsequent correlation",
    )
    arguments = parser.parse_args()
    output: Path | None = arguments.output_root
    if output is not None and (output.exists() or output.is_symlink()):
        raise FileExistsError("independent output root must not exist")
    admission = RetainedSiliconCommonSpaceVerification().prepare()
    print(
        "Authenticated all nine real evidence roles, adopted source bindings, and shared 216-point native records.",
        flush=True,
    )
    if arguments.check_only:
        print(
            "CHECK ONLY: no overlap, Gram, rank, direction or producer correlation computed."
        )
        return 0
    assert output is not None
    print(
        "Starting independent 216-point exact reconstruction / Gram enclosures / direction and unitary controls.",
        flush=True,
    )
    independent = CommonSpaceVerificationRun(
        admission=admission, output_root=output
    ).execute()
    print("Independent result retained:", independent.outcome.to_wire(), flush=True)
    outcome = CommonSpaceProducerCorrelationRun(
        independent=independent, output_root=output
    ).execute()
    print("Post-computation producer correlation:", outcome.to_wire(), flush=True)
    return (
        0 if outcome is CommonSpaceVerificationOutcome.rank_diagnosis_correlated else 2
    )


if __name__ == "__main__":
    raise SystemExit(main())
