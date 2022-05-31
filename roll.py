"""Creates a draft order randomly."""

import argparse
import json
import sys

from loguru import logger

from draft import sleeper
from draft.platforms import LeaguePlatform


def main(program_args: argparse.Namespace):
    if program_args.constraints:
        with open(program_args.constraints) as infile:
            constraints = json.load(infile)
    else:
        constraints = {}

    if program_args.subparser == LeaguePlatform.SLEEPER.value:
        draft_order = sleeper.roll.roll_draft(
            sleeper.league.get_teams(program_args.league_id), lambda x: True
        )
    else:
        raise NotImplementedError(f"Unsupported league type {program_args.subparser}")

    output = ""
    for team_name in draft_order:
        output += f"{team_name}\n"
    with open(program_args.output_file, "w") as outfile:
        outfile.write(output[:-1])

    logger.success(f"Wrote draft order to {program_args.output_file}!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Creates a randomized draft order for a fantasy football league."
    )
    parser.add_argument("--log-level", type=str, required=False, default="DEBUG")
    parser.add_argument(
        "--output-file",
        type=str,
        required=False,
        help="Path to the output file",
        default="draft_order.txt",
    )
    parser.add_argument(
        "--constraints",
        type=str,
        required=False,
        default=None,
        help="Path to a JSON file containing constraints, if any.",
    )

    subparsers = parser.add_subparsers(
        help="Select the league platform", dest="subparser"
    )
    subparsers.required = True

    sleeper_parser = subparsers.add_parser(
        LeaguePlatform.SLEEPER.value, help="Gets league data from Sleeper"
    )
    sleeper.parser.add_subparser(sleeper_parser)

    args = parser.parse_args()

    logger.remove()
    logger.add(sys.stderr, level=args.log_level)

    main(args)
