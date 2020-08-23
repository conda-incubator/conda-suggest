"""Main entry point for conda-suggest."""
import sys
import argparse


def make_parser():
    """Makes the argument parser"""
    p = argparse.ArgumentParser("conda-suggest")
    subcmd = p.add_subparsers(dest="subcmd", help="subcommand to execute")
    gen = subcmd.add_parser("generate", help="create map files for a channel")
    # Generate commands
    gen.add_argument("channel", help="Name of the channel")
    return p


def main(args=None):
    """Main entry point function for conda-suggest."""
    p = make_parser()
    ns = p.parse_args(args=args)
    if ns.subcmd == "generate":
        from . import generate

        generate.generate(ns.channel)


if __name__ == "__main__":
    main()
