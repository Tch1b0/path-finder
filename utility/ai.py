from typing import Callable
from utility.utility import Coordinates, Directions, GameField, Player

def find_path(
    game_field: GameField, 
    render: Callable[[],None],
    max_depth: int,
    depth: int = 0,
    avoid_move: Coordinates = None,
    player: Player = None) -> bool:

    if not player:
        player = game_field.get_player()

    current_pos = player.coords
    for direction in Directions.ALL:
        if avoid_move and current_pos + direction == avoid_move:
            continue
        player.set_coords(current_pos)

        if not player.move(direction):
            continue

        if game_field.player_won:
            return True

        if depth != max_depth:
            tmp = find_path(game_field, render, max_depth, depth + 1, current_pos, player)
            if tmp:
                render()
                return True

        render()
    return False
