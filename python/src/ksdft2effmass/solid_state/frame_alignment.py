"""Gauge-invariant projectors and pointwise reciprocal-frame alignment."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import numpy.typing as npt

from ksdft2effmass.operators import ComplexMatrixQuantity, Unitless

from .band_frames import ReciprocalBandFramePath1D


@dataclass(frozen=True, slots=True, eq=False)
class BandProjectorPathResult1D:
    """Retain the gauge-invariant orthogonal projectors of one frame path."""

    source: ReciprocalBandFramePath1D
    projectors: tuple[ComplexMatrixQuantity, ...]

    def __post_init__(self) -> None:
        """Validate projector count, unit, shape, and exact source correlation."""
        if type(self.source) is not ReciprocalBandFramePath1D:
            raise TypeError("source must be ReciprocalBandFramePath1D")
        if not isinstance(self.projectors, tuple):
            raise TypeError("projectors must be a tuple")
        if len(self.projectors) != self.source.mesh.point_count:
            raise ValueError("projector count must equal source mesh point count")
        for frame, projector in zip(self.source.frames, self.projectors, strict=True):
            if type(projector) is not ComplexMatrixQuantity:
                raise TypeError("every projector must be ComplexMatrixQuantity")
            if not isinstance(projector.unit, Unitless):
                raise ValueError("projectors must be unitless")
            if projector.magnitude.shape != (
                self.source.ambient_dimension,
                self.source.ambient_dimension,
            ):
                raise ValueError("projector shape must match source ambient dimension")
            expected = frame.magnitude @ frame.magnitude.conj().T
            if not np.array_equal(projector.magnitude, expected):
                raise ValueError("projector must equal its source frame projector")


class BandProjectorPathConstructor1D:
    """Construct gauge-invariant orthogonal projectors from a band-frame path."""

    __slots__ = ()

    def execute(self, source: ReciprocalBandFramePath1D) -> BandProjectorPathResult1D:
        """Return ``F(k) F(k)^dagger`` at every reciprocal point."""
        if type(source) is not ReciprocalBandFramePath1D:
            raise TypeError("source must be ReciprocalBandFramePath1D")
        projectors = tuple(
            ComplexMatrixQuantity(
                frame.magnitude @ frame.magnitude.conj().T, Unitless()
            )
            for frame in source.frames
        )
        return BandProjectorPathResult1D(source, projectors)


@dataclass(frozen=True, slots=True, eq=False)
class BandFrameAlignmentResult1D:
    """Retain pointwise unitary alignment and separate gauge diagnostics."""

    reference: ReciprocalBandFramePath1D
    candidate: ReciprocalBandFramePath1D
    aligned: ReciprocalBandFramePath1D
    rotations: tuple[ComplexMatrixQuantity, ...]
    frame_maximum_frobenius_defect: float
    projector_maximum_frobenius_defect: float

    def __post_init__(self) -> None:
        """Validate path compatibility, unitary rotations, and represented defects."""
        for name, path in (
            ("reference", self.reference),
            ("candidate", self.candidate),
            ("aligned", self.aligned),
        ):
            if type(path) is not ReciprocalBandFramePath1D:
                raise TypeError(f"{name} must be ReciprocalBandFramePath1D")
        if (
            self.reference.mesh != self.candidate.mesh
            or self.reference.mesh != self.aligned.mesh
        ):
            raise ValueError("reference, candidate, and aligned meshes must agree")
        if (
            self.reference.ambient_dimension != self.candidate.ambient_dimension
            or self.reference.ambient_dimension != self.aligned.ambient_dimension
        ):
            raise ValueError("all frame ambient dimensions must agree")
        if (
            self.reference.rank != self.candidate.rank
            or self.reference.rank != self.aligned.rank
        ):
            raise ValueError("all frame ranks must agree")
        if not np.array_equal(
            self.reference.sewing_map.magnitude,
            self.candidate.sewing_map.magnitude,
        ) or not np.array_equal(
            self.reference.sewing_map.magnitude,
            self.aligned.sewing_map.magnitude,
        ):
            raise ValueError("reference, candidate, and aligned sewing maps must agree")
        if not isinstance(self.rotations, tuple):
            raise TypeError("rotations must be a tuple")
        if len(self.rotations) != self.reference.mesh.point_count:
            raise ValueError("rotation count must equal reciprocal point count")
        identity = np.eye(self.reference.rank, dtype=np.complex128)
        for rotation, candidate_frame, aligned_frame in zip(
            self.rotations,
            self.candidate.frames,
            self.aligned.frames,
            strict=True,
        ):
            if type(rotation) is not ComplexMatrixQuantity:
                raise TypeError("every rotation must be ComplexMatrixQuantity")
            if not isinstance(rotation.unit, Unitless):
                raise ValueError("rotations must be unitless")
            if rotation.magnitude.shape != identity.shape:
                raise ValueError("rotation shape must match retained frame rank")
            if not np.allclose(
                rotation.magnitude.conj().T @ rotation.magnitude,
                identity,
                rtol=0.0,
                atol=max(
                    self.reference.orthonormality_absolute_tolerance,
                    self.candidate.orthonormality_absolute_tolerance,
                ),
            ):
                raise ValueError("every alignment rotation must be unitary")
            if not np.array_equal(
                aligned_frame.magnitude,
                candidate_frame.magnitude @ rotation.magnitude,
            ):
                raise ValueError("aligned frames must apply the retained rotations")
        for name, value in (
            ("frame_maximum_frobenius_defect", self.frame_maximum_frobenius_defect),
            (
                "projector_maximum_frobenius_defect",
                self.projector_maximum_frobenius_defect,
            ),
        ):
            if type(value) is not float:
                raise TypeError(f"{name} must be a built-in float")
            if not np.isfinite(value) or value < 0.0:
                raise ValueError(f"{name} must be finite and nonnegative")
        frame_defect = float(
            max(
                np.linalg.norm(aligned.magnitude - reference.magnitude)
                for aligned, reference in zip(
                    self.aligned.frames, self.reference.frames, strict=True
                )
            )
        )
        projector_defect = float(
            max(
                np.linalg.norm(
                    reference.magnitude @ reference.magnitude.conj().T
                    - candidate.magnitude @ candidate.magnitude.conj().T
                )
                for reference, candidate in zip(
                    self.reference.frames, self.candidate.frames, strict=True
                )
            )
        )
        if frame_defect != self.frame_maximum_frobenius_defect:
            raise ValueError("frame_maximum_frobenius_defect must match aligned frames")
        if projector_defect != self.projector_maximum_frobenius_defect:
            raise ValueError(
                "projector_maximum_frobenius_defect must match source frames"
            )


class BandFrameAligner1D:
    """Align a candidate frame path pointwise to a reference by unitary Procrustes."""

    __slots__ = ()

    def execute(
        self,
        reference: ReciprocalBandFramePath1D,
        candidate: ReciprocalBandFramePath1D,
    ) -> BandFrameAlignmentResult1D:
        """Return aligned frames, rotations, and separate frame/projector defects."""
        if type(reference) is not ReciprocalBandFramePath1D:
            raise TypeError("reference must be ReciprocalBandFramePath1D")
        if type(candidate) is not ReciprocalBandFramePath1D:
            raise TypeError("candidate must be ReciprocalBandFramePath1D")
        if reference.mesh != candidate.mesh:
            raise ValueError("reference and candidate meshes must agree")
        if reference.ambient_dimension != candidate.ambient_dimension:
            raise ValueError("reference and candidate ambient dimensions must agree")
        if reference.rank != candidate.rank:
            raise ValueError("reference and candidate ranks must agree")
        if not np.array_equal(
            reference.sewing_map.magnitude, candidate.sewing_map.magnitude
        ):
            raise ValueError("reference and candidate sewing maps must agree")
        aligned_magnitudes: list[npt.NDArray[np.complex128]] = []
        rotation_magnitudes: list[npt.NDArray[np.complex128]] = []
        for reference_frame, candidate_frame in zip(
            reference.frames, candidate.frames, strict=True
        ):
            overlap = candidate_frame.magnitude.conj().T @ reference_frame.magnitude
            left, _, right_h = np.linalg.svd(overlap)
            rotation = left @ right_h
            rotation_magnitudes.append(rotation)
            aligned_magnitudes.append(candidate_frame.magnitude @ rotation)
        aligned = ReciprocalBandFramePath1D(
            reference.mesh,
            tuple(
                ComplexMatrixQuantity(frame, Unitless()) for frame in aligned_magnitudes
            ),
            candidate.sewing_map,
            max(
                reference.orthonormality_absolute_tolerance,
                candidate.orthonormality_absolute_tolerance,
            ),
        )
        rotations = tuple(
            ComplexMatrixQuantity(rotation, Unitless())
            for rotation in rotation_magnitudes
        )
        frame_defect = float(
            max(
                np.linalg.norm(aligned_frame.magnitude - reference_frame.magnitude)
                for aligned_frame, reference_frame in zip(
                    aligned.frames, reference.frames, strict=True
                )
            )
        )
        projector_defect = float(
            max(
                np.linalg.norm(
                    reference_frame.magnitude @ reference_frame.magnitude.conj().T
                    - candidate_frame.magnitude @ candidate_frame.magnitude.conj().T
                )
                for reference_frame, candidate_frame in zip(
                    reference.frames, candidate.frames, strict=True
                )
            )
        )
        return BandFrameAlignmentResult1D(
            reference,
            candidate,
            aligned,
            rotations,
            frame_defect,
            projector_defect,
        )
