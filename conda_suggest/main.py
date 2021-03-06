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
    gen.add_argument("--remove-exprs", help="Regular expressions for which "
        "command name matches are removed from the map file", nargs="+",
        default=None, dest="remove_exprs", metavar="EXPR")
    # Find commands
    msg = subcmd.add_parser(
        "message",
        help="searches for the package an executable comes from and prints a "
        "'command-not-found' message.",
    )
    msg.add_argument("exe", help="Name of executable to find")
    return p


def main(args=None):
    """Main entry point function for conda-suggest."""
    p = make_parser()
    ns = p.parse_args(args=args)
    if ns.subcmd == "message":
        from . import find

        find.message(ns.exe)
    elif ns.subcmd == "generate":
        from . import generate

        if ns.remove_exprs is None:
            ns.remove_exprs = generate.DEFAULT_REMOVE_EXPRS
        generate.generate(ns.channel, remove_exprs=ns.remove_exprs)


if __name__ == "__main__":
    main()
