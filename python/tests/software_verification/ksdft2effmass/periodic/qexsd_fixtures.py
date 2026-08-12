# ruff: noqa: E501
"""Controlled reduced QEXSD fixture bytes for software verification only."""

from __future__ import annotations

import hashlib
from pathlib import Path

CONTROLLED_QEXSD = b"""<?xml version='1.0'?>
<qes:espresso xmlns:qes='http://www.quantum-espresso.org/ns/qes/qes-1.0' Units='Hartree atomic units'>
  <general_info><xml_format NAME='QEXSD' VERSION='23.03.10'>QEXSD_23.03.10</xml_format><creator NAME='PWSCF' VERSION='7.2'>fixture</creator></general_info>
  <output>
    <atomic_species ntyp='1'><species name='Si'><mass>28.086</mass><pseudo_file>Si.UPF</pseudo_file></species></atomic_species>
    <atomic_structure nat='2'><atomic_positions><atom name='Si' index='1'>0 0 0</atom><atom name='Si' index='2'>1 1 1</atom></atomic_positions><cell><a1>1 0 0</a1><a2>0 1 0</a2><a3>0 0 1</a3></cell></atomic_structure>
    <basis_set><fft_grid nr1='4' nr2='5' nr3='6'/><fft_smooth nr1='4' nr2='5' nr3='6'/><fft_box nr1='4' nr2='5' nr3='6'/><reciprocal_lattice><b1>1 0 0</b1><b2>0 1 0</b2><b3>0 0 1</b3></reciprocal_lattice></basis_set>
    <total_energy><etot>-1.25</etot></total_energy>
    <band_structure><nbnd>2</nbnd><nks>2</nks>
      <ks_energies><k_point weight='0.25'>0 0 0</k_point><eigenvalues size='2'>-1 0</eigenvalues><occupations size='2'>1 1</occupations></ks_energies>
      <ks_energies><k_point weight='0.75'>0.5 0 0</k_point><eigenvalues size='2'>-0.5 0.5</eigenvalues><occupations size='2'>1 0</occupations></ks_energies>
    </band_structure>
  </output><exit_status>0</exit_status>
</qes:espresso>
"""


def controlled_source_bytes(content: bytes = CONTROLLED_QEXSD) -> tuple[str, int]:
    """Return the independent digest and count for controlled fixture bytes."""
    return hashlib.sha256(content).hexdigest(), len(content)


def actual_qexsd_path() -> Path:
    """Return the explicitly configured accepted source path; perform no discovery."""
    return Path(
        "/Users/eugene/projects/q-e-qe-7.2/tempdir/silicon.save/data-file-schema.xml"
    )
