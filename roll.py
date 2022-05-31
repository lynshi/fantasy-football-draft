"""Creates a draft order randomly."""

import argparse
import json
import sys
from typing import List

from loguru import logger

from draft import sleeper, User
from draft.platforms import LeaguePlatform


def main(program_args: argparse.Namespace):
    if program_args.constraints:
        with open(program_args.constraints) as infile:
            constraints = json.load(infile)

        # Quick hack instead of building a checker from a general constraint language.
        def constraint_checker_builder():
            top_five_guaranteed = set(constraints["top_five_guaranteed"]["user_ids"])

            def _checker(pending_order: List[User]):
                for user in pending_order[5:]:
                    if user.user_id in top_five_guaranteed:
                        logger.trace(f"User {user} must have a pick in the top five")
                        return False

                return True

            return _checker

        constraint_checker = constraint_checker_builder()
    else:
        constraint_checker = lambda _: True

    logger.info(f"Selected platform: {LeaguePlatform(program_args.subparser)}")

    for i in range(args.num_rolls):
        logger.info(f"Roll number: {i}")

        if program_args.subparser == LeaguePlatform.SLEEPER.value:
            draft_order = sleeper.roll.roll_draft(
                list(sleeper.league.get_users(program_args.league_id).values()),
                constraint_checker=constraint_checker,
            )
        else:
            raise NotImplementedError(
                f"Unsupported league type {program_args.subparser}"
            )

    output = ""
    for user in draft_order:  # type: ignore
        output += f"{user.name}\n"
    with open(program_args.output_file, "w") as outfile:
        outfile.write(output[:-1])

    logger.success(f"Wrote draft order to {program_args.output_file}!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Creates a randomized draft order for a fantasy football league."
    )
    parser.add_argument("--log-level", type=str, required=False, default="INFO")
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

    def positive_int(arg: str) -> int:
        try:
            val = int(arg)
        except Exception:
            raise TypeError("--num-rolls must be a positive integer")

        if val <= 0:
            raise ValueError("--num-rolls must be a positive integer")

        return val

    parser.add_argument(
        "--num-rolls",
        type=positive_int,
        required=True,
        help="The number of times to roll the draft order. Only the last instance is recorded.",
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
