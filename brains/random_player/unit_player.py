
from engine.direction import Direction
from engine.unit_controller import UnitController
from engine.unit_player import UnitPlayerBase


class UnitPlayer(UnitPlayerBase):
    def __init__(self, uc: UnitController):
        self.uc = uc

    def play_random(self):
        # Move randomly
        self.uc.move(Direction.random_direction())

    def run(self):
        self.play_random()

        




        