"""Consume the specifically adopted S30 declaration before producer arithmetic."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path

from projectkoios.integrations.wannier90 import (
    Wannier90NativeArtifact,
    Wannier90NativeArtifactIdentity,
)

from common_space.verification.native_inputs import (
    CommonSpaceNativeInputContract,
    CommonSpaceNativeInputLoader,
    CommonSpaceParsedNativeInputs,
    CommonSpaceProviderBinding,
    CommonSpaceProviderModuleIdentity,
    CommonSpaceTrialConvention,
)

from .diagnosis import (
    BULK,
    CommonSpaceDiagnosisRequest,
    FileIdentity,
    FileSourceDeclaration,
    HumanReadableProgressReporter,
    JsonObject,
    authenticate_file,
    read_request,
    require_float,
    require_list,
    require_object,
    require_string,
)
from .point_inventory import ADOPTED_GEOMETRY

_DECISION_DIGEST = ADOPTED_GEOMETRY.removeprefix("s30-source-geometry:sha256:")
_DECLARATION_DIGEST = "c01997f800728dfb7ac1925e8719af22033d4437949c72a3294850dd87a3add3"
_CONVERTER = "/Users/eugene/projects/ksdft2effmass/si-accepted-s1-pw2wannier90-c6-b20-w21-aiida-precise-v1/run/"
_LOCALIZATION = "/Users/eugene/projects/ksdft2effmass/si-accepted-s1-wannier90-localization-c6-b20-w21-aiida-precise-v1/run/"
_NSCF = "/Users/eugene/projects/ksdft2effmass/si-accepted-s1-wannier-nscf-6x6x6-b20-david-c6-b20-v1/run/"
_EVIDENCE = "calculations/Si/bulk/simulations/evidence/"

# These are exactly the eight additional bindings in the adopted decision, not
# discovery rules or observed-hash trust roots. The other eight are request+sources.
_ADDITIONAL_BINDINGS: tuple[tuple[str, str, int, str], ...] = (
    (
        "EIG-explicit-relocation",
        _CONVERTER + "silicon.eig",
        168480,
        "a54f31f8f72cd32b63ad78e47378cd0a8ce97474ad223606f88d48c97c890dd2",
    ),
    (
        "HR",
        _LOCALIZATION + "silicon_hr.dat",
        1396475,
        "24a411c875b3e66bba37e28cc6bf2d95c38ef521c39f81fde40cd0bfa294ea55",
    ),
    (
        "WSvec",
        _LOCALIZATION + "silicon_wsvec.dat",
        1365185,
        "f40fa7f81afaa9bcf9614c6e3c53c14db0db6b0b429b84bfd10f2e40474de1a0",
    ),
    (
        "NSCF-input",
        _EVIDENCE
        + "sssp-1.3.0-pbe-efficiency-qe-7.5-accepted-s1-wannier-nscf-6x6x6-b20-david-c6-b20/input/pw.in",
        13911,
        "20a6ee6e55d632bb66b1afcaac91592bf49c73a3e53e275659d1ccb03e47e1f9",
    ),
    (
        "NSCF-XML",
        _NSCF + "tmp/system.save/data-file-schema.xml",
        371723,
        "2e1b5e157142d18210d18710fb9f5f3e813b17d8331acf96e11af9b9d4f7ef8c",
    ),
    (
        "NSCF-saved-state-manifest",
        _NSCF + "nscf-saved-state-manifest.json",
        44898,
        "24ee9d483141ab54d099bc6e6403d0da46108cc7a30c5b019992da3a1d7ef3ac",
    ),
    (
        "S1-nominal-geometry",
        "calculations/Si/bulk/simulations/structures/Si.PrimitiveUnitCell.RightHanded.RelaxedS1.json",
        758,
        "d131107753512c53dc0a32b9e07e0081f8277d8eeafcb9fad5f1fc7f153ded03",
    ),
    (
        "localization-input-manifest",
        _EVIDENCE
        + "wannier-localization/run-001/input/localization-input-manifest.json",
        1413,
        "523515dffc883abf1bc0ff3e1427eea13e85a12774a5ce2040e3dd43c396568e",
    ),
)


@dataclass(frozen=True, slots=True, kw_only=True)
class AuthenticatedSiliconSourceAssociation:
    """Authenticated declaration plus shared immutable native records, not admission."""

    declaration: FileIdentity
    decision: FileIdentity
    additional_sources: tuple[FileIdentity, ...]
    parsed_inputs: CommonSpaceParsedNativeInputs

    def __post_init__(self) -> None:
        if (
            type(self.declaration) is not FileIdentity
            or type(self.decision) is not FileIdentity
        ):
            raise TypeError(
                "source association requires exact immutable file identities"
            )
        if type(self.additional_sources) is not tuple or any(
            type(item) is not FileIdentity for item in self.additional_sources
        ):
            raise TypeError("additional sources must be an immutable identity tuple")
        if type(self.parsed_inputs) is not CommonSpaceParsedNativeInputs:
            raise TypeError("native inputs must be shared immutable parsed records")

    def to_json(self) -> JsonObject:
        return {
            "declaration": self.declaration.to_json(),
            "decision": self.decision.to_json(),
            "additional_source_bindings": [
                item.to_json() for item in self.additional_sources
            ],
            "geometry_identity": self.parsed_inputs.contract.geometry_identity,
            "scope": "adopted complete fixed S30 model, native retained-space association at 216 source indices only",
            "native_provider_binding": [
                {"module_name": item.module_name, "sha256": item.sha256}
                for item in self.parsed_inputs.provider_binding.modules
            ],
            "assumptions": "Reviewed lineage, modeled backend frames, native rounding and source-to-build assumptions remain explicit in the unchanged adopted decision. No exact nominal/native geometry equality or off-mesh KS embedding is asserted.",
        }


@dataclass(frozen=True, slots=True, kw_only=True)
class AdoptedSiliconSourceAssociation:
    """Authenticate the existing adopted declaration, never manufacture one.

    This deliberately single-source action does not accept new scientific roots,
    create a complete verifier admission, or interpret a review flag as authority.
    Native parsing/records alone are shared with verification; no verifier overlap,
    precision, comparison, serialization or Gram implementation is called here.
    """

    declaration_path: Path

    def execute(
        self,
        *,
        request: CommonSpaceDiagnosisRequest,
        request_path: Path,
        reporter: HumanReadableProgressReporter,
    ) -> AuthenticatedSiliconSourceAssociation:
        authenticate_file(
            FileSourceDeclaration(
                label="request",
                location="absolute",
                declared_path=str(request_path.absolute()),
                byte_size=5458,
                sha256="0dd0d97cdc6134a30073b9d54a54077bba93b579882ef709de47534ca59ff89e",
            ),
            reporter,
        )
        if request != read_request(path=request_path):
            raise ValueError(
                "producer request differs from the authenticated declaration"
            )
        declaration = authenticate_file(
            FileSourceDeclaration(
                label="source-state-assertions",
                location="absolute",
                declared_path=str(self.declaration_path.absolute()),
                byte_size=17424,
                sha256=_DECLARATION_DIGEST,
            ),
            reporter,
        )
        decision_path = BULK / "protocol/decisions/s30-state-identification.md"
        # The fixed digest, not a newly computed digest, is the trust root.
        if decision_path.is_symlink() or not decision_path.is_file():
            raise ValueError("adopted source decision must be an explicit regular file")
        decision_payload = decision_path.read_bytes()
        if hashlib.sha256(decision_payload).hexdigest() != _DECISION_DIGEST:
            raise ValueError("adopted source decision bytes differ")
        decision = FileIdentity(
            label="adopted-source-decision",
            path=str(decision_path),
            byte_size=len(decision_payload),
            sha256=_DECISION_DIGEST,
        )
        additional = tuple(
            authenticate_file(
                FileSourceDeclaration(
                    label=label,
                    location="absolute" if Path(path).is_absolute() else "repository",
                    declared_path=path,
                    byte_size=size,
                    sha256=digest,
                ),
                reporter,
            )
            for label, path, size, digest in _ADDITIONAL_BINDINGS
        )
        for source in request.file_sources:
            authenticate_file(source, reporter)
        # All decision/request/data identities precede declaration/native parsing.
        data = require_object(
            json.loads(self.declaration_path.read_bytes()), "source declaration"
        )
        if data["geometry_identity"] != ADOPTED_GEOMETRY:
            raise ValueError("source declaration geometry differs from adopted meaning")
        points = tuple(
            tuple(
                require_float(value, "declared point component")
                for value in require_list(row, "declared point")
            )
            for row in require_list(
                data["ordered_fractional_kpoints"], "declared points"
            )
        )
        if any(len(point) != 3 for point in points):
            raise ValueError("source declaration point dimension differs")
        # Fixed-length tuples are built explicitly, without an unspecified cast.
        declared_points = tuple((row[0], row[1], row[2]) for row in points)
        by_label = {source.label: source for source in request.file_sources}
        native = tuple(by_label[label] for label in ("AMN", "gauge", "disentanglement"))
        identities = tuple(
            Wannier90NativeArtifactIdentity(
                name=Path(item.declared_path).name,
                byte_count=item.byte_size,
                sha256=item.sha256,
            )
            for item in native
        )

        def wire_identity(item: Wannier90NativeArtifactIdentity) -> JsonObject:
            return {
                "name": item.name,
                "byte_count": item.byte_count,
                "sha256": item.sha256,
            }

        expected_ledger = [
            {
                "role": role,
                "identity": wire_identity(
                    Wannier90NativeArtifactIdentity(
                        name=path.name, byte_count=size, sha256=digest
                    )
                ),
            }
            for role, path, size, digest in (
                (
                    "development-request",
                    request_path,
                    5458,
                    "0dd0d97cdc6134a30073b9d54a54077bba93b579882ef709de47534ca59ff89e",
                ),
                *(
                    (
                        role,
                        by_label[label].resolve(),
                        by_label[label].byte_size,
                        by_label[label].sha256,
                    )
                    for role, label in zip(
                        (
                            "S30-full-source",
                            "S105-full-support",
                            "S110-blocked-result",
                            "hopping-first-protocol",
                        ),
                        (
                            "S30_untruncated_characterization",
                            "S105_full_support_disposition",
                            "S110_blocked_result",
                            "hopping_first_protocol",
                        ),
                        strict=True,
                    )
                ),
            )
        ]
        threshold = Fraction.from_float(
            request.retained_comparison.native_uncertainty_bound
        )
        if (
            data["native_identities"] != [wire_identity(item) for item in identities]
            or data["source_ledger"] != expected_ledger
            or data["atomic_basis_order"] != list(request.state_space.basis_order)
            or data["frozen_rank_threshold"]
            != [hex(threshold.numerator), hex(threshold.denominator)]
        ):
            raise ValueError(
                "source declaration differs from producer source/basis/threshold contract"
            )
        modules = {item.module_name: item.sha256 for item in request.provider_modules}
        modules["projectkoios.integrations.wannier90.artifacts"] = (
            "f4f4736ef96093ecb5f06f7a5f27cd2a215e726b0b68146e4e9b83f99c6f4be8"
        )
        precision = request.native_precision
        errors = (
            Fraction(1, 2 * 10**places)
            for places in (
                precision.amn_decimal_places,
                precision.gauge_decimal_places,
                precision.disentanglement_decimal_places,
            )
        )
        if data["native_component_errors"] != [
            [hex(value.numerator), hex(value.denominator)] for value in errors
        ]:
            raise ValueError("source declaration native rounding model differs")
        binding = CommonSpaceProviderBinding(
            distribution_version=request.provider_version,
            modules=tuple(
                CommonSpaceProviderModuleIdentity(
                    module_name=name,
                    sha256=modules[name],
                )
                for name in CommonSpaceProviderBinding.REQUIRED_MODULES
            ),
        )
        parsed = CommonSpaceNativeInputLoader(
            contract=CommonSpaceNativeInputContract(
                trial_overlap_identity=identities[0],
                gauge_identity=identities[1],
                disentanglement_identity=identities[2],
                ordered_fractional_kpoints=declared_points,
                parent_band_count=request.state_space.parent_band_count,
                atomic_basis_order=request.state_space.basis_order,
                trial_convention=CommonSpaceTrialConvention.two_center_sp3s_star,
                geometry_identity=ADOPTED_GEOMETRY,
                energy_reference_identity=require_string(
                    data["energy_reference_identity"], "energy reference"
                ),
            ),
            provider_binding=binding,
            artifacts=tuple(
                Wannier90NativeArtifact(
                    name=identity.name, payload=source.resolve().read_bytes()
                )
                for source, identity in zip(native, identities, strict=True)
            ),
        ).execute()
        return AuthenticatedSiliconSourceAssociation(
            declaration=declaration,
            decision=decision,
            additional_sources=additional,
            parsed_inputs=parsed,
        )
