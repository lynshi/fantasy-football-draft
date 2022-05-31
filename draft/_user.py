"""Model for a user."""

from dataclasses import dataclass
from typing import Optional


@dataclass
class User:
    """Collection of user data."""

    user_id: str
    name: str
    team_name: Optional[str] = None
