import numpy as np

from engine.direction import Direction
from engine.location import Location
from engine.team import Team
from engine.unit_controller import UnitController
from engine.unit_player import UnitPlayerBase
from reinforcement.genetic_manager import GeneticManager
from reinforcement.net import Net


class UnitPlayer(UnitPlayerBase):
    def __init__(self, uc: UnitController):
        self.uc = uc
        genetic_manager = GeneticManager.get_instance()

        if genetic_manager is not None:
            self.net = genetic_manager.get_current_net()
        else:
            self.net = Net(**{
                'input_nodes': 118,
                'hidden_nodes': 16,
                'output_nodes': 9,
            })
            self.net.load("models/best_net_32.npy")

    def attack_enemies(self, enemies):
        if self.uc.unit.team == Team.BLUE:
            fitness_multiplier = 1
        else:
            fitness_multiplier = -0.75

        for enemy in enemies:
            if self.uc.unit.can_attack_location(enemy.location):
                self.uc.attack(enemy.location)

                if self.uc.sense_unit_at_location(enemy.location) is None:
                    self.net.fitness += 10 * fitness_multiplier
                else:
                    self.net.fitness += 1 * fitness_multiplier

    def play_random(self):
        # Move randomly
        enemies = self.uc.sense_enemy_units()
        self.attack_enemies(enemies)
        self.uc.move(Direction.random_direction())
        self.attack_enemies(enemies)

    def play_net(self):
        # Sense the world
        visible_locations = self.uc.get_visible_locations()
        visible_locations = []

        for x in range(-5, 6):
            for y in range(-5, 6):
                curr_loc = self.uc.get_current_location()
                loc = Location(curr_loc.x + x, curr_loc.y + y)
                
                if self.uc.unit.location.distance_squared(loc) <= self.uc.unit.vision_range:
                    visible_locations.append(loc)

        # Prepare net inputs
        inputs = [self.uc.unit.health / self.uc.unit.max_health]

        for location in visible_locations:
            if not self.uc.unit.world.is_accessible(location):
                inputs.append(0)
                continue

            unit = self.uc.sense_unit_at_location(location)

            if unit is None:
                inputs.append(0)
            elif unit.team == self.uc.unit.team:
                inputs.append(unit.health / unit.max_health + 1)
            else:
                inputs.append(-unit.health / unit.max_health)

        # Run the net
        outputs = self.net.forward(inputs)

        # Choose the best direction
        best_direction = int(np.argmax(outputs))


        enemies = self.uc.sense_enemy_units()
        self.attack_enemies(enemies)

        # Move
        self.uc.move(Direction.from_index(best_direction))
        
        # if best_direction != Direction.DIRECTIONS.index(Direction.ZERO) and self.uc.unit.can_move():
        #     self.net.fitness += 0.5

        self.attack_enemies(enemies)

    def run(self):
        if self.uc.unit.team == Team.BLUE:
            self.play_net()
        else:
            self.play_random()

        




        