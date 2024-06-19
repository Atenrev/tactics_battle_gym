from engine.unit_controller import UnitController
from engine.unit_player import UnitPlayerBase


class UnitPlayer(UnitPlayerBase):
    def __init__(self, uc: UnitController):
        self.uc = uc

    def run(self):
        pass

        




        