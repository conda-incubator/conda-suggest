"""Finds possible packages to install for executables."""
import os
import glob
import bisect
import itertools


MAPFILES = {}


class Mapfile:
    """Provides a lazy-loading view of the map file as bisectable sequence."""

    def __init__(self, filename):
        self.filename = filename
        self.channel, _, rest = os.path.basename(filename).partition(".")
        self.subdir = rest[:-4]  # strips off '.map'
        # make entries list of (exe, pkg) tuples
        # This turns out to be the fastest way to create this tuple for
        # map files in our size range, runs in ~3.5 ms
        with open(filename) as f:
            s = f.read()
        self.entries = [line.partition(":")[::2] for line in s.splitlines()]

    #def _find_pkg_from_idx(self, exe, i):
    #    block = itertools.takewhile(lambda x: x[0] == exe, self._entries)
    #    pkgs = {entry[3] for entry in block}
    #    return pkgs

    def exact_find(self, exe):
        """Finds the set of packages for an executable"""
        # a space is less than all other real characters
        left = bisect_left((exe,  " "), self.entries)
        if left == len(self.entries) or self.entries[left][0] != exe:
            # Executable not found
            if self.subdir.startswith("win") and not exe.endswith(".exe") and not exe.endswith(".bat"):
                # also search extensions
                return self.exact_find(exe + ".exe") | self.exact_find(exe + ".bat")
            else:
                return set()
        # a tilde is greater than other real characters
        right = bisect_right((exe, "~"), self.entries, lo=left)
        return self.entries[left:right]


def get_mapfile(filename):
    """Gets a mapfile from the cache or makes a new one"""
    global MAPFILES
    mapfile = MAPFILES.get(filename, None)
    if mapfile is None:
        mapfile = MAPFILES[filename] = Mapfile(filename)
    return mapfile


def exact_find_in_mapfile(exe, filename):
    """Finds a list of (channel, subdir, executable, package) tuples in a mapfile from the executable."""
    mapfile = get_mapfile(filename)
    return {(mapfile.channel, mapfile.subdir, e, p) for e, p in mapfile.exact_find(exe)}


def exact_find(exe):
    """Finds the execuable names"""
    filenames = glob.glob("*.map")
    finds = set()
    for filename in filename:
        finds |= exact_find_in_mapfile(exe, filename)
    return finds
