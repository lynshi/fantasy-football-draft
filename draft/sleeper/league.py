"""Methods for retrieving league information."""

import json
from typing import List

from loguru import logger
import requests


LEAGUE_USERS_URI = "https://api.sleeper.app/v1/league/{league_id}/users"


def get_teams(league_id: str) -> List[str]:
    """Gets a list of teams in the league in the form. If a team name is available, it is used;
    otherwise, the user's display name is returned.

    I'm not sure what the API response looks like for teams with co-owners, so I'm hoping such teams
    will have team names and the entries will be deduplicated.

    :param league_id: Id of the league.
    :type league_id: str
    :return: Set of team or user names.
    :rtype: Set[str]
    """
    uri = LEAGUE_USERS_URI.format(league_id=league_id)
    logger.info(f"Getting teams from {uri}")

    response = requests.get(uri)
    response.raise_for_status()

    team_names = set()

    data = response.json()
    logger.debug(f"Users response: {json.dumps(data, sort_keys=True)}")

    for user in data:
        team_name = user.get("metadata", {}).get("team_name", None)
        if team_name is not None:
            team_names.add(team_name)
            continue

        team_names.add(user["display_name"])

    return list(team_names)
