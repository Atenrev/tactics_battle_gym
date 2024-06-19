from abc import ABC

from .unit_controller import UnitController


class UnitPlayerBase(ABC):
    """
    UnitPlayer is the main class that handles the unit.
    """

    def __init__(self, uc: UnitController):
        self.uc = uc

    def run(self):
        """
        Run the game.
        """
        pass

        


