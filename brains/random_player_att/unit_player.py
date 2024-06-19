from typing import List

from engine.direction import Direction
from engine.unit import Unit
from engine.unit_controller import UnitController
from engine.unit_player import UnitPlayerBase


class UnitPlayer(UnitPlayerBase):
    def __init__(self, uc: UnitController):
        self.uc = uc

    def play_random(self):
        # Move randomly
        self.uc.move(Direction.random_direction())

    def attack_enemies(self, enemy_units: List[Unit]):
        for enemy in enemy_units:
            if self.uc.unit.can_attack_location(enemy.location):
                self.uc.attack(enemy.location)

    def run(self):
        self.play_random()
        self.attack_enemies(self.uc.sense_enemy_units())

        




        