from typing import Callable
from utility.utility import Coordinates, Directions, GameField, Player


def find_path(
        game_field: GameField,
        render: Callable[[], None],
        max_depth: int,
        depth: int = 0,
        moves: list[Coordinates] = [],
        player: Player = None) -> bool:
    """
    Find a path(as the Player) through the GameField.
    """

    if not player:
        player = game_field.get_player()

    # save current position, so it can be reset to this position later on
    current_pos = player.coords

    # go through EVERY direction
    for direction in Directions.ALL:
        # skip if the step would lead backwards
        if moves and current_pos + direction == moves[-1]:
            continue

        # reset the coords of the player
        player.set_coords(current_pos)

        # move the player and skip if the movement failed
        if not player.move(direction):
            continue

        # return when the player has won
        if game_field.player_won:
            return moves + [current_pos]

        # check if the max_depth isn't reached and call this function
        if depth != max_depth:
            tmp = find_path(game_field, render, max_depth,
                            depth + 1, moves + [current_pos], player)
            if tmp:
                render()
                return tmp

        render()
    return False
