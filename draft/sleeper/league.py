"""Methods for retrieving league information."""

from dataclasses import dataclass
import json
from typing import Dict, Optional

from loguru import logger
import requests


LEAGUE_USERS_URI = "https://api.sleeper.app/v1/league/{league_id}/users"


@dataclass
class User:
    """Collection of user data."""

    user_id: str
    display_name: str
    team_name: Optional[str] = None


def get_users(league_id: str) -> Dict[str, User]:
    """Gets a list of users in the league in the form.

    :param league_id: Id of the league.
    :type league_id: str
    :return: Mapping of user ids to users.
    :rtype: Dict[str, User]
    """
    uri = LEAGUE_USERS_URI.format(league_id=league_id)
    logger.info(f"Getting teams from {uri}")

    response = requests.get(uri)
    response.raise_for_status()

    users = {}

    data = response.json()
    logger.debug(f"Users response: {json.dumps(data, sort_keys=True)}")

    for user_data in data:
        user = User(
            user_id=user_data["user_id"], display_name=user_data["display_name"]
        )
        user.team_name = user_data.get("metadata", {}).get("team_name", None)

    return users
