import pygame
from utility.levels import LevelInterpreter
from utility.utility import *
from utility import find_path
import sys

field_colors = {
    FieldStates.EMPTY: (0,0,0),
    FieldStates.WALL: (150, 150, 150),
    FieldStates.TARGET: (50, 50, 200),
    FieldStates.VISITED: (50, 0, 0)
}

if len(sys.argv) < 2:
    file_path = "./levels/first.lvl"
else:
    file_path = sys.argv[1]

BOX_SIZE = 50

field: GameField = LevelInterpreter(file_path).build_game_field()

window_size = [len(field.field[0])*BOX_SIZE, len(field.field)*BOX_SIZE]
window = pygame.display.set_mode(window_size)

def render():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit(pygame.quit())

    for y, row in enumerate(field.field):
        for x, item in enumerate(row):
            if item not in FieldStates.ALL:
                # item has to be Player
                pygame.draw.rect(window, (200, 30, 30), (x*BOX_SIZE, y*BOX_SIZE, BOX_SIZE, BOX_SIZE))
            else:
                pygame.draw.rect(window, field_colors[item], (x*BOX_SIZE, y*BOX_SIZE, BOX_SIZE, BOX_SIZE))

    pygame.display.update()

if __name__ == "__main__":
    find_path(field, render, 44)
    while True:
        render()