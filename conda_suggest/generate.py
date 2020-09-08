"""Generates the cache files (which should not be distributed) and the map files
(which should).
"""
import os
import re
import json
import tarfile

import tqdm


SUBDIRS = [
    "noarch",
    "linux-64",
    "osx-64",
    # "osx-arm64",
    "win-64",
    "linux-ppc64le",
    "linux-aarch64",
]
EXECUTABLE_RE = re.compile(b"(?:bin|Scripts)/([^/]*)")
DEFAULT_REMOVE_EXPRS = ("__pycache__",)


def _get_repodata_packages(channel, subdir):
    repodata_json = f"{channel}/{subdir}/repodata.json"
    print(f"Loading {repodata_json}")
    with open(repodata_json) as f:
        repodata = json.load(f)
    return repodata["packages"]


def _save_cache(cache, cachefile, display=True):
    if display:
        print(f"Saving cache to {cachefile}")
    with open(cachefile, "w") as f:
        json.dump(cache, f, sort_keys=True, indent=1)


def _add_info_entrypoints(executables, tf):
    try:
        fb = tf.extractfile("info/link.json")
    except KeyError:
        # no link.json in the file
        return
    link = json.load(fb)
    noarch = link.get("noarch", None)
    if noarch is None:
        return
    points = noarch.get("entry_points", ())
    for point in points:
        exe, _, _ = point.partition("=")
        executables.add(exe.strip())


def _add_artifact_to_cache(cache, pkg, channel, subdir, artifact):
    url = f"{channel}/{subdir}/{artifact}"
    name = pkg["name"]
    entry = {
        "package": name,
        "executables": [],
    }
    if not artifact.endswith(".tar.bz2"):
        # skip non-bz2 artifacts for now
        cache[artifact] = entry
        return
    executables = set()
    with tarfile.open(url, mode="r:bz2") as tf:
        # first read files
        fb = tf.extractfile("info/files")
        files = fb.read().splitlines()
        for f in files:
            m = EXECUTABLE_RE.match(f)
            if m is None:
                continue
            executables.add(m.group(1).decode())
        # next add entrypoints
        _add_info_entrypoints(executables, tf)
    entry["executables"] = sorted(executables)
    cache[artifact] = entry


def _get_channel_name(channel):
    return channel.rpartition("/")[2]


def make_cache(channel, subdir):
    """Reads and/or generates the cachefile and returns the cache"""
    # load cache
    channel_name = _get_channel_name(channel)
    cachefile = f"{channel_name}.{subdir}.cache.json"
    if os.path.exists(cachefile):
        print(f"Loading cache from {cachefile}")
        with open(cachefile) as f:
            cache = json.load(f)
    else:
        cache = {}
    # load repodata
    pkgs = _get_repodata_packages(channel, subdir)
    # add packages to cache
    needed = set(pkgs.keys()) - set(cache.keys())
    for i, artifact in enumerate(tqdm.tqdm(needed)):
        _add_artifact_to_cache(cache, pkgs[artifact], channel, subdir, artifact)
        if i % 100 == 99:
            # save the state occasionally
            _save_cache(cache, cachefile, display=False)
    _save_cache(cache, cachefile)
    return cache


def generate_map(cache, channel, subdir, remove_exprs=DEFAULT_REMOVE_EXPRS, write=True):
    """Creates the map file from the cache.

    Parameters
    ----------
    cache : dict
        Cache contents, as described in readme.
    channel : str
        Name of the channel
    subdir : str
        Name of the platform subdir
    remove_exprs : sequence of str, optional
        Regular expressions for which command name matches are removed from the
        map file.
    write : bool, optional
        Flag for whether to actually write the file or not.
    """
    print(f"Generating map file for {channel}/{subdir}")
    # create remove expr func
    rm_res = list(map(re.compile, remove_exprs))

    def filter(exe):
        return not any([rm_re.match(exe) for rm_re in rm_res])

    # generate file
    exe_pkg = set()
    for pkg in cache.values():
        exe_pkg.update({(exe, pkg["package"]) for exe in pkg["executables"]})
    lines = sorted(exe_pkg)
    lines = [f"{e}:{p}" for e, p in lines if filter(e)]
    if lines:
        lines[-1] += "\n"
    s = "\n".join(lines)
    if write:
        channel_name = _get_channel_name(channel)
        mapfile = f"{channel_name}.{subdir}.map"
        print(f"Writing map file {mapfile}")
        with open(mapfile, "w") as f:
            f.write(s)
    return s


def generate(channel, remove_exprs=DEFAULT_REMOVE_EXPRS):
    """Generates the map files, and the cache files incidentally."""
    for subdir in SUBDIRS:
        cache = make_cache(channel, subdir)
        generate_map(cache, channel, subdir, remove_exprs=remove_exprs)
