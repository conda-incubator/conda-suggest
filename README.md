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

The above assumes that the mapfiles for the [`conda-forge`](https://conda-forge.org)
channel have also been installed.







