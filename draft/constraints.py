"""Module for draft order constraints."""


from typing import Callable, List, Set

from draft._user import User


def build_ensure_top_n_pick(
    n: int, restricted_users: Set[str]
) -> Callable[[List[User]], bool]:
    """Builds a method that ensures the specified users are given a pick in the top N positions.

    :param n: _description_
    :type n: int
    :param restricted_users: _description_
    :type restricted_users: Set[str]
    :return: _description_
    :rtype: Callable[[List[User]], bool]
    """

    def _ensure_top_n_pick(proposed_order: List[User]) -> bool:
        for user in proposed_order[n:]:
            if user.user_id in restricted_users:
                return False

        return True

    return _ensure_top_n_pick
