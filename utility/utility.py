from __future__ import annotations
from typing import Any
import math


class Coordinates():
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

class FieldStates():
    EMPTY   = 0
    WALL    = 1
    TARGET  = 2
    VISITED = 3
    ALL     = [EMPTY, WALL, TARGET, VISITED]

class Directions():
    UP    = Coordinates( 0, -1)
    DOWN  = Coordinates( 0,  1)
    RIGHT = Coordinates( 1,  0)
    LEFT  = Coordinates(-1,  0)
    ALL   = [UP, DOWN, LEFT, RIGHT]

class Player():
    def __init__(self, coords: Coordinates, game_field: GameField) -> None:
        self.coords = coords
        self.game_field = game_field
    
    def __str__(self) -> str:
        return f"Player at {str(self.coords)}"

    def __repr__(self) -> str:
        return f"<Player:{str(self.coords)}>"

    def set_coords(self, coords: Coordinates) -> None:
        self.game_field.move(self.coords, coords)

    def move(self, dir: Coordinates) -> bool:
        """
        Move the Player somewhere in the field
        Returns wether the move was successful or not
        """
        return self.game_field.request_move(self.coords, self.coords + dir)

class GameField():
    def __init__(self, size: tuple[int, int] = (5, 5)) -> None:
        self.field: list[list[Any]] = [[FieldStates.EMPTY for _ in range(size[0])] for _ in range(size[1])]
        self.player_won = False

    def __str__(self) -> str:
        return str(self.field)

    def get_player(self) -> Player:
        for row in self.field:
            for col in row:
                if col not in FieldStates.ALL:
                    return col

        return None

    def get_target(self) -> Coordinates:
        for y, row in enumerate(self.field):
            for x, col in enumerate(row):
                if col == FieldStates.TARGET:
                    return Coordinates(x, y)
        
        return None

    def spawn_player(self, coords: Coordinates) -> Player:
        self.field[coords.y][coords.x] = (player := Player(coords, self))
        return player

    def spawn_target(self, coords: Coordinates) -> None:
        self.field[coords.y][coords.x] = FieldStates.TARGET

    def spawn_wall(self, from_coord: Coordinates, to_coord: Coordinates):
        if from_coord.x != to_coord.x:
            for x in range(from_coord.x, to_coord.x + 1):
                self.field[from_coord.y][x] = FieldStates.WALL
        elif from_coord.y != to_coord.y:
            for y in range(from_coord.y, to_coord.y + 1):
                self.field[y][from_coord.x] = FieldStates.WALL

    def move(self, old_coords: Coordinates, new_coords: Coordinates):
        if old_coords == new_coords: return

        old_item = self.field[new_coords.y][new_coords.x]
        new_item = self.field[old_coords.y][old_coords.x]
        self.field[new_coords.y][new_coords.x] = new_item
        if new_item not in FieldStates.ALL:
            new_item: Player
            new_item.coords = new_coords
            self.field[old_coords.y][old_coords.x] = FieldStates.VISITED
            if old_item == FieldStates.TARGET:
                self.player_won = True
        else:
            self.field[old_coords.y][old_coords.x] = FieldStates.EMPTY


    def request_move(self, old_coords: Coordinates, new_coords: Coordinates) -> bool:
        """
        Request a move for a certain item
        """

        if (new_coords.x < len(self.field[0]) and new_coords.x >= 0 and
            new_coords.y < len(self.field) and new_coords.y >= 0 and
            old_coords.distance(new_coords) == 1 and
            self.field[new_coords.y][new_coords.x] not in [FieldStates.WALL]):
            self.move(old_coords, new_coords)
            return True
        else:
            return False

if __name__ == "__main__":
    c1 = Coordinates(2, 1)
    c2 = Coordinates(4, 3)
    print(c1 != c2)
