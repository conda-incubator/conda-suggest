"""Main entry point for conda-suggest."""
import sys
import argparse


def make_parser():
    """Makes the argument parser"""
    p = argparse.ArgumentParser("conda-suggest")
    subcmd = p.add_subparsers(dest="subcmd", help="subcommand to execute")
    # Generate commands
    gen = subcmd.add_parser("generate", help="create map files for a channel")
    gen.add_argument("channel", help="Name of the channel")
    # Find commands
    find = subcmd.add_parser("find", help="searches for the package an executable comes from")
    find.add_argument("exe", help="Name of executable to find")
    return p


def main(args=None):
    """Main entry point function for conda-suggest."""
    p = make_parser()
    ns = p.parse_args(args=args)
    if ns.subcmd == "find":
        from . import generate

        find.find(ns.exe)
    elif ns.subcmd == "generate":
        from . import generate

        generate.generate(ns.channel)


if __name__ == "__main__":
    main()
