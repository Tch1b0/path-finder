from __future__ import annotations
import re
from typing import Any
import math


class Coordinates():
    """
    Store simple coordinates
    """

    def __init__(self, x: int = 0, y: int = 0) -> None:
        self.x = x
        self.y = y

    def __str__(self) -> str:
        return f"({self.x}, {self.y})"

    def __add__(self, other) -> Coordinates:
        return Coordinates(self.x + other.x, self.y + other.y)

    def __sub__(self, other) -> Coordinates:
        return Coordinates(self.x - other.x, self.y - other.y)

    def __eq__(self, other: object) -> bool:
        return self.x == other.x and self.y == other.y

    def distance(self, other: Coordinates) -> float:
        return math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)

    @staticmethod
    def is_coordinate(other: str) -> bool:
        return re.match(r"(\d+), ?(\d+)", other)

    @classmethod
    def from_string(cls, string: str):
        x, y = [int(x) for x in string.split(",")]
        return cls(x, y)


class FieldType():
    EMPTY = 0
    WALL = 1
    START = 2
    TARGET = 3
    VISITED = 4
    ALL = [EMPTY, WALL, START, TARGET, VISITED]


class Directions():
    UP = Coordinates(0, -1)
    DOWN = Coordinates(0,  1)
    RIGHT = Coordinates(1,  0)
    LEFT = Coordinates(-1,  0)
    ALL = [UP, DOWN, LEFT, RIGHT]


class Player():
    def __init__(self, coords: Coordinates, game_field: GameField) -> None:
        self.coords = coords
        self.game_field = game_field

    def __str__(self) -> str:
        return f"Player at {str(self.coords)}"

    def __repr__(self) -> str:
        return f"<Player:{str(self.coords)}>"

    def set_coords(self, coords: Coordinates) -> None:
        """
        Set the Coordinates of the Player
        """

        self.game_field.move(self.coords, coords)

    def move(self, dir: Coordinates) -> bool:
        """
        Move the Player somewhere in the field
        Returns wether the move was successful or not
        """

        return self.game_field.request_move(self.coords, self.coords + dir)


class GameField():
    def __init__(self, size: tuple[int, int] = (5, 5)) -> None:
        self.field: list[list[Any]] = [
            [FieldType.EMPTY for _ in range(size[0])] for _ in range(size[1])]
        self.player_won = False

    def __str__(self) -> str:
        return str(self.field)

    def get_player(self) -> Player:
        """
        Get the Player from the field
        """

        for row in self.field:
            for col in row:
                if col not in FieldType.ALL:
                    return col

        return None

    def get_target(self) -> Coordinates:
        """
        Get the target from the field
        """

        for y, row in enumerate(self.field):
            for x, col in enumerate(row):
                if col == FieldType.TARGET:
                    return Coordinates(x, y)

        return None

    def spawn_player(self, coords: Coordinates) -> Player:
        """
        Spawn a new Player on the field
        """

        self.field[coords.y][coords.x] = (player := Player(coords, self))
        return player

    def spawn_target(self, coords: Coordinates) -> None:
        """
        Spawn a new target on the field
        """

        self.field[coords.y][coords.x] = FieldType.TARGET

    def spawn_wall(self, from_coord: Coordinates, to_coord: Coordinates):
        """
        Spawn a wall that stretches from one to another point

        NOTE: can't go diagonal and the first point must be lower than the right
        """

        if from_coord.x != to_coord.x:
            for x in range(from_coord.x, to_coord.x + 1):
                self.field[from_coord.y][x] = FieldType.WALL
        elif from_coord.y != to_coord.y:
            for y in range(from_coord.y, to_coord.y + 1):
                self.field[y][from_coord.x] = FieldType.WALL

    def move(self, old_coords: Coordinates, new_coords: Coordinates):
        """
        Move a certain item on the field somewhere else
        """

        if old_coords == new_coords:
            return

        old_item = self.field[new_coords.y][new_coords.x]
        new_item = self.field[old_coords.y][old_coords.x]
        self.field[new_coords.y][new_coords.x] = new_item
        if new_item not in FieldType.ALL:
            new_item: Player
            new_item.coords = new_coords
            self.field[old_coords.y][old_coords.x] = FieldType.VISITED
            if old_item == FieldType.TARGET:
                self.player_won = True
        else:
            self.field[old_coords.y][old_coords.x] = FieldType.EMPTY

    def request_move(self, old_coords: Coordinates, new_coords: Coordinates) -> bool:
        """
        Request a move for a certain item
        """

        if (new_coords.x < len(self.field[0]) and new_coords.x >= 0 and
            new_coords.y < len(self.field) and new_coords.y >= 0 and
            old_coords.distance(new_coords) == 1 and
                self.field[new_coords.y][new_coords.x] not in [FieldType.WALL]):
            self.move(old_coords, new_coords)
            return True
        else:
            return False


if __name__ == "__main__":
    c1 = Coordinates(2, 1)
    c2 = Coordinates(4, 3)
    print(c1 != c2)
