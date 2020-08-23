"""Finds possible packages to install for executables."""
import os
import glob


def find_in_mapfile(exe, mapfile):
    """Finds an (executable, package) tuple in a mapfile from the executable."""
    filesize = os.path


def find(exe):
    """Finds the execuable names"""
    mapfiles = glob.glob("*.map")
    for mapfile in mapfiles:
        find_in_mapfile(exe, mapfile)
