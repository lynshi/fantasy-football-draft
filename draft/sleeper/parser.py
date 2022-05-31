"""Parser for command-line arguments for Sleeper leagues."""

import argparse


def add_subparser(sleeper_parser: argparse.ArgumentParser):
    """Adds arguments for the argument parser for Sleeper leagues.

    :param sleeper_parser: Argument parser.
    :type sleeper_parser: argparse.ArgumentParser
    """

    sleeper_parser.add_argument(
        "--league-id", type=str, required=True, help="Id of the league"
    )
