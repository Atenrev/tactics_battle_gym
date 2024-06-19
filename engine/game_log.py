import enum

from dataclasses import dataclass
from typing import List, Optional

from .location import Location


class GameActionType(enum.Enum):
    """Enum for game action types."""
    MOVE = 1
    ATTACK = 2
    HEAL = 3


@dataclass
class GameAction:
    """
    Class representing a game action.
    """
    action_type: GameActionType
    unit_id: int
    subject_location: Optional[Location]
    target_location: Optional[Location]


class GameLog:
    """
    Game log class that stores game actions.
    """

    def __init__(self):
        self.actions: List[List[GameAction]] = [[]]

    def new_turn(self):
        self.actions.append([])

    def add_action(self, action: GameAction):
        self.actions[-1].append(action)