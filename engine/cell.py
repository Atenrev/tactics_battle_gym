from engine.location import Location
from engine.unit import Unit

from typing import Optional


class Cell:
    """
    Class representing a cell in the grid.
    """

    def __init__(self, location: Location):
        self.location = location
        self.__obstacle = False
        self.__unit = None

    def add_obstacle(self):
        self.__obstacle = True

    def has_obstacle(self) -> bool:
        return self.__obstacle

    def set_unit(self, unit: Optional[Unit]):
        self.__unit = unit

    def get_unit(self) -> Optional[Unit]:
        return self.__unit

    def hit(self, attacker: Unit):
        if self.__unit is not None:
            self.__unit.receive_damage(attacker.attack)