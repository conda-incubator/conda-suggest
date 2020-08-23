"""Generates the cache files (which should not be distributed) and the map files
(which should).
"""
import re
import json
import tarfile

import tqdm
from ruamel.yaml import YAML


SUBDIRS = [
        "noarch",
        "linux-64",
        "osx-64",
        "osx-arm64",
        "win-64",
        "linux-ppc64le",
        "linux-aarch64",
]
EXECUTABLE_RE = re.compile(r"(?:bin|Scripts)/([^/]*)")


def _get_repodata_packages(channel, subdir):
    repodata_json = f"{channel}/{subdir}/repodata.json"
    print(f"Loading {repodata_json}")
    with open(repodata_json) as f:
        repodata = json.load(f)
    return repodata["packages"]


def _save_cache(cache, cachefile):
    print(f"Saving cache to {cachefile}")
    with open(cachefile, 'w') as f:
        json.dump(cache, f, sort_keys=True)


def _add_entrypoints(executables, root):
    build = root.get("build", None)
    if build is None:
        return
    points = build.get("entry_points", ())
    for point in points:
        exe, _, _ = exe.partition("=")
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
            executables.add(m.group(1))
        # next add entrypoints
        fb = tf.extractfile("info/recipe/meta.yaml")
        yaml = YAML(typ='safe')
        meta = yaml.load(fb)
        _add_entrypoints(executables, meta)
        outputs = meta.get("outputs", ())
        for output in outputs:
            if name != output.get("name", ""):
                # only look up entrypoints for this package
                continue
            _add_entrypoints(executables, output)
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
    for artifact in tqdm.tqdm(needed):
        try:
            _add_artifact_to_cache(cache, pkgs[artifact], channel, subdir, artifact)
        except:
            # If something fails, we still want to save the current state
            _save_cache(cache, cachefile)
            raise
    _save_cache(cache, cachefile)
    return cache


def generate(channel):
    """Generates the map files, and the cache files incidentally."""
    for subdir in SUBDIRS:
        cache = make_cache(channel, subdir)
        #generate_map(cache)
