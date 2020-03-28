# -*- coding: utf-8 -*-

"""
Console script for corona_explorer.
"""
import sys
import argparse
from .initialize import init
from .export import export
from .graph import graph


def parse_args(args):
    """
    Returns parsed command line arguments.
    """

    parser = argparse.ArgumentParser(description="Commandline interface for corona_explorer")

    parser.add_argument("--db", default="cases.db", help="Database location")

    subparsers = parser.add_subparsers()

    init_parser = subparsers.add_parser("init", description="Import data from open-covid project.")
    init_parser.add_argument("--force", action="store_true", help="Force recreation of DB if it exists")
    init_parser.add_argument(
        "--source",
        type=argparse.FileType("r"),
        default="open-covid-data/output/data.csv",
        help="Data source (csv) to read from",
    )
    init_parser.set_defaults(func=init)

    export_parser = subparsers.add_parser("export", description="Export the data to a file")
    export_parser.add_argument("countries", type=str, nargs="+", help="Countries to export data for.")
    export_parser.add_argument("--export-path", type=str, default="./export", help="Location to export data to.")
    export_parser.set_defaults(func=export)

    graph_parser = subparsers.add_parser("graph", description="Create and export graphs")
    graph_parser.add_argument("countries", type=str, nargs="+", help="Countries to create graphs for.")
    graph_parser.add_argument(
        "--model-type",
        default="scatter-plot",
        type=str,
        choices=["scatter-plot", "linear-regression"],
        help="Model type to use.",
    )
    graph_parser.add_argument("--scale", default="log", type=str, choices=["log", "linear"], help="Y-axis scale to use")
    graph_parser.add_argument("--graph-path", type=str, default="./graph", help="Location to write graphs to.")
    graph_parser.set_defaults(func=graph)

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
