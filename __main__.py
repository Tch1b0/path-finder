from time import time
import pygame
from utility.levels import LevelInterpreter
from utility.utility import *
from utility import find_path
import sys

# define constants
FIELD_COLORS = {
    FieldType.EMPTY: (0, 0, 0),
    FieldType.WALL: (150, 150, 150),
    FieldType.TARGET: (50, 50, 200),
    FieldType.VISITED: (50, 0, 0)
}
BOX_SIZE = 50

# parse the first argument or select the default one
if len(sys.argv) < 2:
    file_path = "./levels/first.lvl"
else:
    file_path = sys.argv[1]


game = LevelInterpreter(file_path).build_game_field()
window = pygame.display.set_mode([
    len(game.field[0])*BOX_SIZE,  # calculate and set width
    len(game.field)*BOX_SIZE      # calculate and set height
])


def render():
    """
    Render the pygame view
    """

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit(pygame.quit())

    for y, row in enumerate(game.field):
        for x, item in enumerate(row):
            if item not in FieldType.ALL:
                # item has to be Player
                pygame.draw.rect(window, (200, 30, 30),
                                 (x*BOX_SIZE, y*BOX_SIZE, BOX_SIZE, BOX_SIZE))
            else:
                pygame.draw.rect(
                    window, FIELD_COLORS[item], (x*BOX_SIZE, y*BOX_SIZE, BOX_SIZE, BOX_SIZE))

    pygame.display.update()


if __name__ == "__main__":
    # get the start time
    start = time()

    # solve maze
    find_path(game, render, 44)

    # get the end time
    end = time()

    # print the time needed to solve the maze
    print(f"Solved in {end-start:.3f} seconds")

    # keep displaying the (un)solved maze
    while True:
        render()
