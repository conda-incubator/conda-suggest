"""Tests the finding capabilites"""
import pytest

from conda_suggest.find import MAPFILES, exact_find


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

@pytest.mark.parametrize("exe,exp", [
    ("-pkg-config", {"pkg-config",}),
    ("zzxordir", {"zziplib",}),
    ("gcc", {"c-compiler", "fortran-compiler"}),
    ("not-a-command", set()),
])
def test_find_exact_linux(exe, exp, tmpdir):
    MAPFILES.clear()
    p = tmpdir.join("test.linux-64.map")
    p.write(LINUX_MAPFILE)
    obs = exact_find(exe, conda_suggest_path=str(tmpdir))
    obs_pkgs = {pkg for _, _, _, pkg in obs}
    assert exp == obs_pkgs
    MAPFILES.clear()
