from .direction import Direction
from .location import Location
from .unit_types.unit_type import UnitType
from .team import Team


class Unit:
    def __init__(self, unit_type: UnitType, team: Team, location: Location, world: 'World', world_manager: 'WorldManager'):
        self.id = world.next_unit_id()
        self.unit_type = unit_type
        self.team = team
        self.location = location
        self.world = world
        self.world_manager = world_manager
        self.health = unit_type.MAX_HEALTH
        self.current_movement_cooldown = unit_type.MOVEMENT_COOLDOWN
        self.current_attack_cooldown = unit_type.ATTACK_COOLDOWN

    @property
    def vision_range(self) -> int:
        return self.unit_type.VISION_RANGE

    @property
    def movement_cooldown(self) -> float:
        return self.unit_type.MOVEMENT_COOLDOWN

    @property
    def max_health(self) -> int:
        return self.unit_type.MAX_HEALTH

    @property
    def attack(self) -> int:
        return self.unit_type.ATTACK

    @property
    def attack_range(self) -> int:
        return self.unit_type.ATTACK_RANGE

    @property
    def min_attack_range(self) -> int:
        return self.unit_type.MIN_ATTACK_RANGE

    @property
    def attack_cooldown(self) -> float:
        return self.unit_type.ATTACK_COOLDOWN

    def start_turn(self):
        self.current_movement_cooldown = max(
            0.0, self.current_movement_cooldown - 1.0)
        self.current_attack_cooldown = max(
            0.0, self.current_attack_cooldown - 1.0)

    def run(self):
        pass

    def get_unit_player(self) -> 'UnitPlayer':
        """
        Returns the unit player that controls this unit.
        The unit player is defined in a separate package inside the brains/ folder.
        """
        pass

    def receive_damage(self, damage: int):
        self.health = max(0, self.health - damage)

        if self.health == 0:
            self.kill()

    def kill(self):
        self.world_manager.remove_unit(self)

    def is_alive(self) -> bool:
        return self.health > 0

    def is_in_range(self, location: Location) -> bool:
        return self.location.distance_squared(location) <= self.attack_range

    def can_sense_location(self, location: Location) -> bool:
        return (self.location.distance_squared(location) <= self.vision_range
                and not self.world.is_out_of_bounds(location))

    def can_move(self) -> bool:
        return self.current_movement_cooldown < 1.0

    def can_move_to_direction(self, direction: Direction) -> bool:
        new_location = self.location.add_direction(direction)

        if not self.world.is_accessible(new_location):
            return False

        return (self.can_move() and not self.world.is_occupied(new_location))

    def add_movement_cooldown(self):
        self.current_movement_cooldown += self.movement_cooldown

    def can_attack(self) -> bool:
        return self.current_attack_cooldown < 1.0

    def can_attack_location(self, location: Location) -> bool:
        if self.world.is_out_of_bounds(location):
            return False

        return self.is_in_range(location) and self.can_attack()

    def add_attack_cooldown(self):
        self.current_attack_cooldown += self.attack_cooldown

    def __eq__(self, other) -> bool:
        return self.id == other.id
