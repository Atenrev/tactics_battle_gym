import logging
from typing import Any
from .game_log import GameLog
from .team import Team
from .unit import Unit
from .unit_controller import UnitController
from .world import World
from .unit_player import UnitPlayerBase


class WorldManager:
    """
    WorldManager is the main class that handles the world.
    It controls the creation of the world, the game loop, and the game logic.
    """

    def __init__(self, map_file: str, unit_player_class_1: UnitPlayerBase, unit_player_class_2: UnitPlayerBase, config: dict):
        self.unit_player_class_1 = unit_player_class_1
        self.unit_player_class_2 = unit_player_class_2
        self.config = config
        self.game_log = GameLog()
        self.init_world(map_file)
        
    def init_world(self, map_file: str):
        """
        Initializes the world.
        """
        self.units = []
        self.unit_players = []
        self.turn = 0
        self.game_over = False
        self.world = World(map_file, self)

    def run_game(self, render_method: Any = None):
        """
        Runs the game.
        """
        winner = None

        while not self.game_over and self.turn < self.config['max_turns']:
            if render_method is not None:
                render_method(self.world, self.game_log, self.turn)

            for unit_player in self.unit_players:
                unit_player.uc.unit.start_turn()
                unit_player.run()

            # If there are only units from one team left, the game is over.
            if len(self.get_units_by_team(Team.RED)) == 0:
                self.game_over = True
                winner = Team.BLUE
                logging.info('Blue team wins!')
            elif len(self.get_units_by_team(Team.BLUE)) == 0:
                self.game_over = True
                winner = Team.RED
                logging.info('Red team wins!')

            self.turn += 1
            self.game_log.new_turn()

        if winner is None:
            logging.info('Draw!')

        return winner

    def add_unit(self, unit: Unit, world: World):
        """
        Adds a unit to the unit queue.
        """
        world.add_unit(unit, unit.location)
        self.units.append(unit)
        unit_controller = UnitController(unit, world, self.game_log)

        if unit.team == Team.RED:
            upc = self.unit_player_class_1(unit_controller) 
        else:
            upc = self.unit_player_class_2(unit_controller)

        self.unit_players.append(upc)

    def remove_unit(self, unit: Unit):
        """
        Removes a unit from the unit queue.
        """
        index = self.units.index(unit)
        self.units.pop(index)
        self.unit_players.pop(index)
        self.world.remove_unit(unit)

    def get_units_by_team(self, team: Team) -> list:
        """
        Returns a list of units that are on the given team.
        """
        return [unit for unit in self.units if unit.team == team]