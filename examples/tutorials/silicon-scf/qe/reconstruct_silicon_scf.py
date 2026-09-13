"""Reconstruct the retained QE example01 silicon SCF input by grouping tags.

This software example writes input text to standard output. It does not invoke
Quantum ESPRESSO or establish a new scientific result.
"""

from __future__ import annotations

import sys

from ksdft2effmass.integration.quantum_espresso import (
    QePwInputFile,
    QePwInputFileWriter,
)


class SiliconScfInputExample:
    """Own construction and writing of the retained tutorial input example."""

    @staticmethod
    def input_file() -> QePwInputFile:
        """Return the portable grouping-tag reconstruction of the tutorial input."""
        return QePwInputFile(
            (
                (
                    "&CONTROL",
                    (
                        "calculation = 'scf'",
                        "restart_mode = 'from_scratch'",
                        "prefix = 'silicon'",
                        "tstress = .true.",
                        "tprnfor = .true.",
                        "pseudo_dir = './pseudo/'",
                        "outdir = './scratch/'",
                    ),
                ),
                (
                    "&SYSTEM",
                    (
                        "ibrav = 2",
                        "celldm(1) = 10.20",
                        "nat = 2",
                        "ntyp = 1",
                        "ecutwfc = 18.0",
                    ),
                ),
                (
                    "&ELECTRONS",
                    (
                        "diagonalization = 'david'",
                        "mixing_mode = 'plain'",
                        "mixing_beta = 0.7",
                        "conv_thr = 1.0d-8",
                    ),
                ),
                ("ATOMIC_SPECIES", ("Si 28.086 Si.pz-vbc.UPF",)),
                (
                    "ATOMIC_POSITIONS alat",
                    ("Si 0.00 0.00 0.00", "Si 0.25 0.25 0.25"),
                ),
                (
                    "K_POINTS",
                    (
                        "10",
                        "0.1250000 0.1250000 0.1250000 1.00",
                        "0.1250000 0.1250000 0.3750000 3.00",
                        "0.1250000 0.1250000 0.6250000 3.00",
                        "0.1250000 0.1250000 0.8750000 3.00",
                        "0.1250000 0.3750000 0.3750000 3.00",
                        "0.1250000 0.3750000 0.6250000 6.00",
                        "0.1250000 0.3750000 0.8750000 6.00",
                        "0.1250000 0.6250000 0.6250000 3.00",
                        "0.3750000 0.3750000 0.3750000 1.00",
                        "0.3750000 0.3750000 0.6250000 3.00",
                    ),
                ),
            )
        )

    @classmethod
    def execute(cls) -> str:
        """Return deterministic QE input text for standard-output emission."""
        return QePwInputFileWriter().execute(cls.input_file())


if __name__ == "__main__":
    sys.stdout.write(SiliconScfInputExample.execute())
