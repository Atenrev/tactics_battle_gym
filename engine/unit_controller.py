import logging
from abc import ABC
from typing import List, Optional
from .direction import Direction
from .game_log import GameAction, GameActionType, GameLog
from .location import Location
from .unit import Unit


class UnitController(ABC):
    def __init__(self, unit: Unit, world: 'World', game_log: GameLog):
        self.unit = unit
        self.world = world
        self.game_log = game_log

    def get_current_location(self) -> Location:
        return self.unit.location

    def move(self, direction: Direction):
        logging.debug(
            f'{self.unit.id} at {self.unit.location} is trying to move {direction}')

        if self.unit.can_move_to_direction(direction):
            target_location = self.unit.location.add_direction(direction)
            self.game_log.add_action(GameAction(
                GameActionType.MOVE, self.unit.id, self.unit.location, target_location))
            self.world.move_unit(self.unit, direction)
            self.unit.add_movement_cooldown()

    def attack(self, location: Location):
        logging.debug(
            f'{self.unit.id} at {self.unit.location} is trying to attack {location}')

        if self.unit.can_attack_location(location):
            self.game_log.add_action(GameAction(
                GameActionType.ATTACK, self.unit.id, self.unit.location, location))
            cell = self.world.get_cell(location)
            cell.hit(self.unit)
            self.unit.add_attack_cooldown()

    def sense_unit_at_location(self, location: Location) -> Optional[Unit]:
        return self.world.get_unit_at_location(location)

    def sense_units(self) -> List[Unit]:
        units = []

        for unit in self.world.units:
            if unit == self.unit:
                continue

            if self.unit.location.distance_squared(unit.location) <= self.unit.vision_range:
                units.append(unit)

        return units

    def sense_ally_units(self) -> List[Unit]:
        units = []

        for unit in self.world.units:
            if unit == self.unit:
                continue

            if (unit.team == self.unit.team
                    and self.unit.location.distance_squared(unit.location) <= self.unit.vision_range):
                units.append(unit)

        return units

    def sense_enemy_units(self) -> List[Unit]:
        units = []

        for unit in self.world.units:
            if unit == self.unit:
                continue

            if (unit.team != self.unit.team
                    and self.unit.location.distance_squared(unit.location) <= self.unit.vision_range):
                units.append(unit)

        return units

    def sense_obstacles(self) -> List[Location]:
        obstacles = []

        for obstacle in self.world.obstacles:
            if self.unit.location.distance_squared(obstacle) <= self.unit.vision_range:
                obstacles.append(obstacle)

        return obstacles

    def get_visible_locations(self) -> List[Location]:
        return [cell.location for row in self.world.grid for cell in row
                if self.unit.can_sense_location(cell.location)]