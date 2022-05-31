"""Gets users that consistently drafted in the bottom N positions in the specified drafts."""

import argparse
import sys
from typing import Dict, Set

from loguru import logger

from draft import sleeper, User


def main(program_args: argparse.Namespace):
    users: Dict[str, User] = {}
    bottom_pick_users: Set[str] = set()

    for draft_count, draft_id in enumerate(program_args.drafts):
        draft_order = sleeper.draft.get_draft_order(draft_id)
        for draft_pos_count, user in enumerate(draft_order):
            users[user.user_id] = user

            if (
                draft_count == 0
                and draft_pos_count >= len(draft_order) - program_args.n
            ):
                # On the first pass, add all users with a bottom-N pick.
                bottom_pick_users.add(user.user_id)
                logger.debug(
                    f"User {user} had a bottom {program_args.n} pick in draft {draft_id}"
                )
            else:
                # On subsequent passes, remove any users who didn't have a bottom-N pick.
                try:
                    bottom_pick_users.remove(user.user_id)
                    logger.debug(
                        f"User {user} did not have a bottom {program_args.n} pick in draft "
                        f"{draft_id}"
                    )
                except KeyError:
                    pass

    logger.success(
        f"Users who had a bottom {program_args.n} pick in the last {len(program_args.drafts)} "
        f"drafts: {[users[user_id].name for user_id in sorted(list(bottom_pick_users))]}"
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Gets users that consistently drafted in the bottom N positions in the "
        "specified drafts."
    )
    parser.add_argument("--log-level", type=str, required=False, default="INFO")
    parser.add_argument(
        "--drafts",
        type=str,
        required=False,
        action="extend",
        nargs="+",
        help="Ids of prior drafts",
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
        "-n",
        type=positive_int,
        required=True,
        help="Specify the value of N for the last N picks.",
    )

    args = parser.parse_args()

    logger.remove()
    logger.add(sys.stderr, level=args.log_level)

    main(args)
