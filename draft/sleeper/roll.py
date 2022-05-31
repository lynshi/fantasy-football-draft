"""Methods for constructing the draft order."""

from copy import deepcopy
import random
from typing import Callable, List

from loguru import logger

from draft._user import User


def roll_draft(
    users: List[User], *, constraint_checker: Callable[[List[User]], bool]
) -> List[User]:
    """Constructs a random draft order that satifies the constraints.

    The current, naive implementation just re-rolls until the constraint checker is satisfied.

    :param users: List of users in the league. If there are co-owners, they should be deduplicated
        by team.
    :type users: List[User]
    :param constraint_checker: Method for checking whether the draft order satisfies constraints.
        This should return True if all constraints are satisfied.
    :type constraint_checker: Callable[[List[str]], bool]
    :return: The draft order.
    :rtype: List[User]
    """

    num_attempts = 0
    draft_order = deepcopy(users)  # In case the original list matters.
    while True:
        random.shuffle(draft_order)
        if constraint_checker(draft_order) is True:
            return draft_order

        num_attempts += 1
        logger.debug(
            f"Created draft order does not satisfy all constraints. Attempt #{num_attempts}"
        )
