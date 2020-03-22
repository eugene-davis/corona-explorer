# -*- coding: utf-8 -*-

"""
Console script for corona_explorer.
"""
import sys
import argparse
from .initialize import init


def parse_args(args):
    """
    Returns parsed command line arguments.
    """

    parser = argparse.ArgumentParser(description="Commandline interface for corona_explorer")

    subparsers = parser.add_subparsers()

    init_parser = subparsers.add_parser("init", description="Import data from open-covid project.")
    init_parser.add_argument("--force", action="store_true", help="Force recreation of DB if it exists")
    init_parser.add_argument(
        "--source",
        type=argparse.FileType("r"),
        default="open-covid-data/output/world.csv",
        help="Data source (csv) to read from",
    )
    init_parser.add_argument("--db", default="cases.db", help="Database location")
    init_parser.set_defaults(func=init)

    return parser.parse_args(args)


def main():
    """
    Console script for corona_explorer.
    """
    args = parse_args(sys.argv[1:])
    args.func(args)
    return 0


if __name__ == "__main__":
    sys.exit(main())
