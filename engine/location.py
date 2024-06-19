from .direction import Direction


class Location:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def distance_squared(self, other: 'Location') -> int:
        return (self.x - other.x) ** 2 + (self.y - other.y) ** 2

    def direction_to(self, other: 'Location') -> Direction:
        if self == other:
            return Direction(0, 0)
        else:
            return Direction.get_direction(self, other)

    def add_direction(self, direction: Direction) -> 'Location':
        return Location(self.x + direction.dx, self.y + direction.dy)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))

    def __str__(self):
        return f"Location({self.x}, {self.y})"