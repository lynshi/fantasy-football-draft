"""Methods for getting draft history information."""

import json
from typing import Dict, List

from loguru import logger
import requests

from draft._user import User


DRAFT_URI = "https://api.sleeper.app/v1/draft/{draft_id}"


def get_draft_order(draft_id: str, *, users: Dict[str, User]) -> List[User]:
    """Gets the draft order in the specified draft.

    :param draft_id: Sleeper draft id.
    :type draft_id: str
    :param users: Mapping of user ids to User objects.
    :type users: Dict[str, User]
    :return: Users in the order in which they drafted.
    :rtype: List[User]
    """

    uri = DRAFT_URI.format(draft_id=draft_id)
    logger.info(f"Getting teams from {uri}")

    response = requests.get(uri)
    response.raise_for_status()

    data = response.json()
    logger.debug(f"Draft response: {json.dumps(data, sort_keys=True)}")

    draft_order_tuples = []
    for user_id, draft_position in data["draft_order"].items():
        draft_order_tuples.append((draft_position, user_id))

    draft_order = []
    for _, user_id in sorted(draft_order_tuples):
        draft_order.append(users[user_id])

    return draft_order
