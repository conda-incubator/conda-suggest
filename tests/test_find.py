"""Tests the finding capabilites"""
import pytest


LINUX_MAPFILE = """-pkg-config:pkg-config
.appmode-post-link.sh:appmode
.appmode-pre-unlink.sh:appmode
.astrometry-post-link.sh:astrometry
.aws-parallelcluster-post-link.sh:aws-parallelcluster
HelloU3DWorld:u3d
HepMC2_reader_example.exe:hepmc3
HepMC3-config:hepmc3
HepMC3_fileIO_example.exe:hepmc3
IDTFConverter:u3d
IDTFGen:u3d
gcaps:ncl
gcc:c-compiler
gcc:fortran-compiler
zzdir:zziplib
zzxorcat:zziplib
zzxorcopy:zziplib
zzxordir:zziplib
"""


def test_find_exact_linux(tmpdir):
    pass