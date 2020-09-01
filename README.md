# conda-suggest
Suggest packages to install to obtain command line utilities.

## Quickstart

First, install conda-suggest via:

```sh
$ conda install -c conda-suggest
```

Then you can print a message for which packages to install to obtain a command
via conda-suggest. For example, say we want to know where `g++`, the GNU C++
compiler comes from. We would then run something like the following.

```sh
$ conda suggest message g++
Command 'g++' not found in the environment, but can be installed with any of:

    $ conda install -c conda-forge cxx-compiler
```

The above assumes that the map files for the [`conda-forge`](https://conda-forge.org)
channel have also been installed.

## Python API
You may also use conda-suggest programatically. For example:

```python
from conda_suggest.find import message, exact_find, substring_find

message("g++")
exact_find("python")
substring_find("xonsh")
```


## Map files
Conda-suggest works by looking for "map files" on the system. Map files are simple
text files where every line associates a command name with a package name separated
by a colon, i.e. `<command>:<package>\n`. For example:

```
zfp:zfp
zic:tzcode
zima:pint-pulsar
zip:zip
zipcmp:libzip
```

These map files must be lexicographically sorted, first by the command, and then by the package.
The map files are named according to the following scheme: `<channel-name>.<subdir>.map`.
The `message` command (and others) will load and search all map files on `$CONDA_SUGGEST_PATH`.
This environment variable will default to
`"~/.local/share/conda-suggest:<sys.exec_prefix>/share/conda-suggest"` or it's platform-specific
equivalent.

Users should install map files for all channels that they frequently use.

## Generating the Map Files & the Cache Files
Creating the map files can be a tedious job because it requires searching through all artifacts on
a channel. The `conda suggest generate` command automates this process for you. Currently this can
look through a channel's artifacts in a local directory:

```sh
$ conda suggest generate /path/to/mirrors/channel-name
```

To make restarts safe and fast, the above command produces "cache files" with the naming
scheme `<channel-name>.<subdir>.cache.json`. These are JSON files with the following layout:

```json
{
  "<artifact-filename>": {
    "executables": ["cmd0", "cmd1", ...],
    "package": "<package-name>"
  },
  ...
}
```

In the cache file, the artifact name is the same as the artifact filename in the
`repodata.json` for that channel & subdir combo. The package name is taken from the
equivalent repodata entry.

Generating these cache files can take a very long time and they tend to be quite large.
It is not recommended that you distribute these caches as part of any package. They are
intended for local use only. The map files are the intended distibutable result.

At some point in the future, we would like to be able to generate maps based off of a
remote `repodata.json` as well.
