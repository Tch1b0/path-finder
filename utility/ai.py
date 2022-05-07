from typing import Callable
from utility.utility import Coordinates, Directions, GameField, Player


def find_path(
        game_field: GameField,
        render: Callable[[], None],
        max_depth: int,
        depth: int = 0,
        avoid_move: Coordinates = None,
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
        if avoid_move and current_pos + direction == avoid_move:
            continue

        # reset the coords of the player
        player.set_coords(current_pos)

        # move the player and skip if the movement failed
        if not player.move(direction):
            continue

        # return when the player has won
        if game_field.player_won:
            return True

        # check if the max_depth isn't reached and call this function
        if depth != max_depth:
            tmp = find_path(game_field, render, max_depth,
                            depth + 1, current_pos, player)
            if tmp:
                render()
                return True

        render()
    return False
