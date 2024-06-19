import random


class Direction:
    """
    Class for storing the direction of a move
    """
    NORTH = (0, -1)
    NORTH_WEST = (-1, -1)
    WEST = (-1, 0)
    SOUTH_WEST = (-1, 1)
    SOUTH = (0, 1)
    EAST = (1, 0)
    NORTH_EAST = (1, -1)
    SOUTH_EAST = (1, 1)
    ZERO = (0, 0)

    DIRECTIONS = (
        NORTH_EAST,
        EAST,
        SOUTH_EAST,
        SOUTH,
        SOUTH_WEST,
        WEST,
        NORTH_WEST,
        NORTH,
        ZERO
    )

    def __init__(self, dx: int, dy: int):
        self.dx = dx
        self.dy = dy

    @staticmethod
    def from_index(index: int) -> 'Direction':
        """
        Returns the direction from an index.
        """
        dx, dy = Direction.DIRECTIONS[index]
        return Direction(dx, dy)

    @staticmethod
    def random_direction():
        """
        Returns a random direction.
        """
        return Direction(random.choice([-1, 0, 1]), random.choice([-1, 0, 1]))

    @staticmethod
    def get_direction(start_location: 'Location', end_location: 'Location') -> 'Direction':
        """
        Returns the direction from start_location to end_location.
        """
        if start_location == end_location:
            return Direction(Direction.ZERO[0], Direction.ZERO[1])
        if start_location.x == end_location.x:
            if start_location.y > end_location.y:
                return Direction(Direction.NORTH[0], Direction.NORTH[1])
            else:
                return Direction(Direction.SOUTH[0], Direction.SOUTH[1])
        if start_location.y == end_location.y:
            if start_location.x > end_location.x:
                return Direction(Direction.WEST[0], Direction.WEST[1])
            else:
                return Direction(Direction.EAST[0], Direction.EAST[1])
        if start_location.x > end_location.x:
            if start_location.y > end_location.y:
                return Direction(Direction.NORTH_WEST[0], Direction.NORTH_WEST[1])
            else:
                return Direction(Direction.SOUTH_WEST[0], Direction.SOUTH_WEST[1])
        else:
            if start_location.y > end_location.y:
                return Direction(Direction.NORTH_EAST[0], Direction.NORTH_EAST[1])
            else:
                return Direction(Direction.SOUTH_EAST[0], Direction.SOUTH_EAST[1])

    def rotate_clockwise(self):
        """
        Rotates the direction clockwise.
        """
        index = Direction.DIRECTIONS.index(self)

        if index == len(Direction.DIRECTIONS) - 1:
            return self
        elif index == len(Direction.DIRECTIONS) - 2:
            return Direction(Direction.DIRECTIONS[0][0], Direction.DIRECTIONS[0][1])
        else:
            return Direction(Direction.DIRECTIONS[index + 1][0], Direction.DIRECTIONS[index + 1][1])

    def rotate_counter_clockwise(self):
        """
        Rotates the direction counter clockwise.
        """
        index = Direction.DIRECTIONS.index(self)

        if index == len(Direction.DIRECTIONS) - 1:
            return self
        elif index == 0:
            return Direction(Direction.DIRECTIONS[len(Direction.DIRECTIONS) - 2][0], Direction.DIRECTIONS[len(Direction.DIRECTIONS) - 2][1])
        else:
            return Direction(Direction.DIRECTIONS[index - 1][0], Direction.DIRECTIONS[index - 1][1])

    def __getitem__(self, key):
        if key == 0:
            return self.dx
        elif key == 1:
            return self.dy
        else:
            raise IndexError("Index out of range")

    def __eq__(self, other):
        return self.dx == other[0] and self.dy == other[1]

    def __str__(self):
        return f"Direction({self.dx}, {self.dy})"
