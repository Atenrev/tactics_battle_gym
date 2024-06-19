from typing import List, Optional, Tuple

from engine.direction import Direction
from engine.location import Location
from engine.team import Team
from engine.unit import Unit
from engine.unit_controller import UnitController
from engine.unit_player import UnitPlayerBase


class UnitPlayer(UnitPlayerBase):

    def __init__(self, uc: UnitController):
        self.uc = uc

    def play_random(self):
        # Move randomly
        if self.uc.unit.team == Team.RED:
            self.uc.move(Direction.from_index(2))
        else:
            self.uc.move(Direction.from_index(6))

    def find_centroid(self, units: List[Unit]) -> Location:
        centroid = [0, 0]

        for unit in units:
            loc = unit.location
            centroid[0] += loc.x
            centroid[1] += loc.y

        if len(units) > 0:
            centroid[0] //= len(units)
            centroid[1] //= len(units)

        return Location(centroid[0], centroid[1])

    def find_nearest_unit(self, units: List[Unit]) -> Tuple[Optional[Unit], int]:
        myloc = self.uc.get_current_location()
        nu = None
        mindist = 999999

        for unit in units:
            dist = unit.location.distance_squared(myloc)

            if nu is None or dist < mindist:
                nu = unit
                mindist = dist

        return nu, mindist

    def micro(self, ally_units: List[Unit], enemy_units: List[Unit]):
        myloc = self.uc.get_current_location()

        nearest_enemy, dist_to_nearest_enemy = self.find_nearest_unit(enemy_units)

        ally_centroid = self.find_centroid(ally_units)
        enemy_centroid = self.find_centroid(enemy_units)

        if (nearest_enemy is not None
            or dist_to_nearest_enemy > self.uc.unit.attack_range
            and nearest_enemy.health <= self.uc.unit.health):
            dir_to_go = myloc.direction_to(enemy_centroid)
            rotate_clockwise = True

            if ally_centroid.x < enemy_centroid.x:
                if myloc.y < ally_centroid.y:
                    rotate_clockwise = False
            elif enemy_centroid.x < ally_centroid.x:
                if ally_centroid.y < myloc.y:
                    rotate_clockwise = False

            for _ in range(16):
                if self.uc.unit.can_move_to_direction(dir_to_go):
                    break 

                if rotate_clockwise:
                    dir_to_go = dir_to_go.rotate_clockwise()
                else:
                    dir_to_go = dir_to_go.rotate_counter_clockwise()

            self.uc.move(dir_to_go)

        else:
            dir_to_go = Direction.from_index(8)
            
            if nearest_enemy is not None:
                dir_to_go = nearest_enemy.location.direction_to(myloc)

            rotate_clockwise = True

            for _ in range(16):
                if self.uc.unit.can_move_to_direction(dir_to_go):
                    break 

                if rotate_clockwise:
                    dir_to_go = dir_to_go.rotate_clockwise()
                else:
                    dir_to_go = dir_to_go.rotate_counter_clockwise()

            self.uc.move(dir_to_go)

    def attack_enemies(self, enemy_units: List[Unit]):            
        target = None

        for enemy in enemy_units:
            if self.uc.unit.can_attack_location(enemy.location):
                if target is None:
                    target = enemy.location
                    break

        if target is None:
            return

        self.uc.attack(target)

    def run(self):
        ally_units = self.uc.sense_ally_units()
        enemy_units = self.uc.sense_enemy_units()

        if len(enemy_units) == 0:
            self.play_random()
        else:
            self.micro(ally_units, enemy_units)

        self.attack_enemies(enemy_units)

            

        




        