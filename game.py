from enum import IntEnum, StrEnum
from random import randint

WIDTH = 560
HEIGHT = 600


class Constants(IntEnum):
    ONE_CUBE_ON_PIXELS = 60  # 23
    CELL_SPACING = 1
    START_CUBES_X = 100
    CUBES_DRAW_WIDTH = 25
    CUBES_DRAW_HEIGHT = 80


class Constants_Str(StrEnum):
    COLOR_BLOCK_DEFAULT = "empty_41"
    STONE_TEXTURE = "stone_41"
    BOMB_TEXTURE = "bomb_41"


class Difficlty(IntEnum):
    EASY = 8
    MEDIUM = 12
    BOMBS_ON_MEDIUM = 10
    HARD = 16


class Player:
    def __init__(self, x, y):
        self.player_x = x
        self.player_y = y
        self.score = 0
        self.money = 0
        self.alive = True
        self.dig_speed = 1


class field_obj:
    def __init__(self):
        self.is_solid = True
        self.is_dombed = False

    def texture_give(self):
        if self.is_solid and not self.is_dombed:
            return Constants_Str.STONE_TEXTURE
        elif not self.is_solid and not self.is_dombed:
            return Constants_Str.COLOR_BLOCK_DEFAULT
        return Constants_Str.BOMB_TEXTURE


def field_generate(diff, bombs_on_diff):
    field = []
    for row in range(diff):
        in_field = []
        for col in range(diff):
            in_field.append(field_obj())
        field.append(in_field)
    bombs_to_plase = bombs_on_diff
    while bombs_to_plase:
        x = randint(0, bombs_on_diff)
        y = randint(0, bombs_on_diff)
        if not field[x][y].is_dombed:
            field[x][y].is_dombed = True
            bombs_to_plase -= 1
    return field


def field_update(screen_, field, count_field, size_of_block):
    from itertools import product

    for x, y in product(range(count_field), range(count_field)):

        cordinates = size_of_block + Constants.CELL_SPACING
        draw_x = cordinates * x + Constants.CUBES_DRAW_WIDTH
        draw_y = cordinates * y + Constants.CUBES_DRAW_HEIGHT

        screen_.blit(field[x][y].texture_give(), (draw_x, draw_y))


DIFF = Difficlty.MEDIUM
BOMBS_ON_DIFF = Difficlty.BOMBS_ON_MEDIUM
SIZE_OF_BLOCK = (min(WIDTH, HEIGHT) - Constants.ONE_CUBE_ON_PIXELS) // DIFF
field = field_generate(DIFF, BOMBS_ON_DIFF)


def draw():

    screen.clear()
    screen.fill((40, 136, 235))  # голубой задний фон

    field_update(screen, field, DIFF, SIZE_OF_BLOCK)


def on_mouse_down(pos, button):
    x, y = pos
    change_x = (x - Constants.CUBES_DRAW_WIDTH) // (
        SIZE_OF_BLOCK + Constants.CELL_SPACING
    )
    change_y = (y - Constants.CUBES_DRAW_HEIGHT) // (
        SIZE_OF_BLOCK + Constants.CELL_SPACING
    )
    if change_x < DIFF and change_y < DIFF:
        field[change_x][change_y].is_solid = False
