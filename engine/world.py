import pygame

from typing import List, Optional
from .cell import Cell
from .direction import Direction
from .location import Location
from .team import Team
from .unit import Unit
from .unit_types.archer import Archer


class World:
    """
    A class that represents the world.
    """

    def __init__(self, map_file: str, world_manager: 'WorldManager'):
        self.width: int = 0
        self.height: int = 0
        self.grid: List[List[Cell]] = []
        self.obstacles: List[Location] = []
        self.__unit_id = 0
        self.world_manager = world_manager
        self.load_map(map_file)

    @property
    def units(self) -> list:
        return self.world_manager.units

    def load_map(self, map_file: str):
        """
        Loads a map from a file.

        The file should be a text file with the following format:
        - The first line should be the width and height of the map.
        - The following lines are the locations of obstacles and units.
            The first character of each line is either 'O' (obstacle) or 'U' (unit).
            The second character is the x-coordinate of the location.
            The third character is the y-coordinate of the location.
            The fourth character is the team of the unit.
            The fifth character is the unit type of the unit.

        Args:
            map_file: The file to load the map from.         
        """
        # TODO: move to map_loader.py
        with open(map_file, 'r', encoding="utf-8") as f:
            lines = f.readlines()
            width, height = [int(x) for x in lines[0].split()]
            self.width = width
            self.height = height
            self.grid = [[Cell(Location(x, y))
                          for y in range(height)] for x in range(width)]

            for line in lines[1:]:
                line = line.strip().split()

                if line[0] == 'O':
                    self.grid[int(line[1])][int(line[2])].add_obstacle()
                    self.obstacles.append(Location(int(line[1]), int(line[2])))
                elif line[0] == 'U':
                    unit_type = line[4]
                    team = line[3]
                    location = Location(int(line[1]), int(line[2]))

                    if unit_type == 'A':
                        unit_type = Archer
                    else:
                        raise Exception("Unknown unit type: " + unit_type)

                    if team == 'R':
                        team = Team.RED
                    elif team == 'B':
                        team = Team.BLUE
                    elif team == 'N':
                        team = Team.NEUTRAL
                    else:
                        raise Exception("Unknown team: " + team)

                    new_unit = Unit(unit_type, team, location, self, self.world_manager)
                    self.world_manager.add_unit(new_unit, self)

    def get_cell(self, location: Location) -> Cell:
        return self.grid[location.x][location.y]

    def has_obstacle(self, location: Location) -> bool:
        """
        Checks if a location has an obstacle.
        """
        return self.grid[location.x][location.y].has_obstacle()

    def is_out_of_bounds(self, location: Location) -> bool:
        """
        Checks if a location is out of bounds.

        Args:
            location: The location to check.

        Returns:
            True if the location is out of bounds, False otherwise.
        """
        return (location.x < 0 or location.x >= self.width
                or location.y < 0 or location.y >= self.height)

    def is_accessible(self, location: Location) -> bool:
        """
        Checks if a location is accessible.
        
        Args:
            location: The location to check.

        Returns:
            True if the location is accessible, False otherwise.
        """
        return not self.is_out_of_bounds(location) and not self.has_obstacle(location)

    def is_occupied(self, location: Location) -> bool:
        """
        Checks if a location is occupied.

        Args:
            location: The location to check.
        
        Returns:
            True if the location is occupied, False otherwise.
        """
        return self.grid[location.x][location.y].get_unit() is not None

    def add_unit(self, unit: Unit, location: Location):
        """
        Adds a unit at a location.
        """
        self.grid[location.x][location.y].set_unit(unit)

    def get_unit_at_location(self, location: Location) -> Optional[Unit]:
        """
        Returns the unit at a location.
        """
        return self.grid[location.x][location.y].get_unit()

    def next_unit_id(self) -> int:
        """
        Returns the next unit id.
        """
        self.__unit_id += 1
        return self.__unit_id

    def remove_unit(self, unit: Unit):
        """
        Removes a unit from the world.
        """
        self.grid[unit.location.x][unit.location.y].set_unit(None)

    def move_unit(self, unit: Unit, direction: Direction):
        """
        Moves a unit to a new direction.
        """
        new_location = unit.location.add_direction(direction)

        if self.is_out_of_bounds(new_location):
            return

        if self.is_accessible(new_location) and not self.is_occupied(new_location):
            self.grid[unit.location.x][unit.location.y].set_unit(None)
            self.grid[new_location.x][new_location.y].set_unit(unit)
            unit.location = new_location

    def print_map(self):
        """
        Prints the map to the console.
        """
        for row in self.grid:
            for cell in row:
                if cell.has_obstacle():
                    print('O', end='')
                elif cell.get_unit() is not None:
                    print(cell.get_unit().team.value, end='')
                else:
                    print(' ', end='')
            print()
