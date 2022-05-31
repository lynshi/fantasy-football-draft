"""Methods for constructing the draft order."""

from copy import deepcopy
import random
from typing import Callable, List

from loguru import logger


def roll_draft(
    team_names: List[str], constraint_checker: Callable[[List[str]], bool]
) -> List[str]:
    """Constructs a random draft order that satifies the constraints.

    The current, naive implementation just re-rolls until the constraint checker is satisfied.

    :param team_names: List of teams in the league.
    :type team_names: List[str]
    :param constraint_checker: Method for checking whether the draft order satisfies constraints.
        This should return True if all constraints are satisfied.
    :type constraint_checker: Callable[[List[str]], bool]
    :return: The draft order.
    :rtype: List[str]
    """

    num_attempts = 0
    draft_order = deepcopy(team_names)  # In case the original list matters.
    while True:
        random.shuffle(draft_order)
        if constraint_checker(draft_order) is True:
            return draft_order

        num_attempts += 1
        logger.info(
            f"Created draft order does not satisfy all constraints. Attempt #{num_attempts}"
        )
