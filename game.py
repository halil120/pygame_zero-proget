from enum import IntEnum, StrEnum, Enum, auto
from random import randint
import pygame

HEIGHT = 600
WIDTH = 560
#       560 x 600   разрешение окна


class Constants(IntEnum):
    ONE_CUBE_ON_PIXELS = 60  # 23
    CELL_SPACING = 1
    START_CUBES_X = 100
    CUBES_DRAW_WIDTH = 25
    CUBES_DRAW_HEIGHT = 80
    CELL_SPACING_DIFF_BUTTONS = 26
    PUT_BUTTONS_X = 130


class Constants_Str(Enum):
    COLOR_BLOCK_DEFAULT = images.empty_41
    STONE_TEXTURE = images.stone_41
    BOMB_TEXTURE = images.bomb_41


class Difficlty(IntEnum):
    EASY = 8
    BOMBS_ON_EASY = 10
    TEXTURES_ON_EASY = 62

    MEDIUM = 12
    BOMBS_ON_MEDIUM = 12
    TEXTURES_ON_MEDIUM = 41

    HARD = 16
    BOMBS_ON_HARD = 25
    TEXTURES_ON_HARD = 31

    DEFAULT = 2
    DEFAULT_BOMBS = 1
    TEXTURES_ON_DEFAULT = 250


class Stages_of_game_constants(Enum):
    MENU = auto()
    SELECTING_DIFFICULTY = auto()
    GAME = auto()
    END_OF_GAME = auto()


class Player:
    def __init__(self, x, y):
        self.player_x = x
        self.player_y = y
        self.score = 0
        self.money = 0
        self.alive = True
        self.dig_speed = 1


class States_of_game:
    def __init__(self):
        self.state = Stages_of_game_constants.MENU

    def get_game_state(self, screen):
        if self.state == Stages_of_game_constants.MENU:
            screen.fill((40, 136, 235))
            screen.blit("game_button", (130, 60))

        elif self.state == Stages_of_game_constants.SELECTING_DIFFICULTY:

            screen.blit("select_diff_easy", (Constants.PUT_BUTTONS_X, 52))

            screen.blit("select_diff_medium", (Constants.PUT_BUTTONS_X, 220))

            screen.blit("select_diff_hard", (Constants.PUT_BUTTONS_X, 388))

        elif self.state == Stages_of_game_constants.GAME:
            field_update(screen, field, DIFF, SIZE_OF_BLOCK)


class field_obj:
    def __init__(self, texture_size):
        self.is_solid = True
        self.is_dombed = False
        self.texture_size = texture_size

    def texture_give(self):
        if self.is_solid and not self.is_dombed:
            return self.texture_size[0]
        elif not self.is_solid and not self.is_dombed:
            return self.texture_size[1]
        return self.texture_size[2]


def field_generate(diff, bombs_on_diff):
    field = []
    for row in range(diff):
        in_field = []
        for col in range(diff):
            in_field.append(field_obj(SIZE_OF_TEXTURE))
        field.append(in_field)
    bombs_to_plase = bombs_on_diff
    while bombs_to_plase:
        x = randint(0, diff - 1)
        y = randint(0, diff - 1)
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
        
        
def backfront(screen_):
    if game_status.state==Stages_of_game_constants.SELECTING_DIFFICULTY:
        screen_.fill((40, 136, 235))
    elif game_status.state==Stages_of_game_constants.GAME:
        screen_.fill((100, 100, 100))
    elif game_status.state==Stages_of_game_constants.END_OF_GAME:
        screen_.fill((0, 0, 0))
        screen_.draw.text('Game Over',(155,265),color='white',fontsize=75)



DIFF = Difficlty.DEFAULT
BOMBS_ON_DIFF = Difficlty.DEFAULT_BOMBS
SIZE_OF_TEXTURE = 20
SIZE_OF_BLOCK = 0
all_images = (
    Constants_Str.STONE_TEXTURE.value,
    Constants_Str.COLOR_BLOCK_DEFAULT.value,
    Constants_Str.BOMB_TEXTURE.value,
)
game_status = States_of_game()
SAZE_OF_PICTYRE = images.select_diff_medium.get_size()

field = []


def draw():
    screen.clear()
    
    backfront(screen)

    game_status.get_game_state(screen)


def on_mouse_down(pos, button):
    global DIFF, BOMBS_ON_DIFF, field, SIZE_OF_BLOCK, SIZE_OF_TEXTURE
    x, y = pos
    

    if game_status.state == Stages_of_game_constants.MENU:
        if 130 < x < 430 and 60 < y < 212:
            game_status.state = Stages_of_game_constants.SELECTING_DIFFICULTY

    elif game_status.state == Stages_of_game_constants.SELECTING_DIFFICULTY:
        
                    #danger gome
                    

        if (
            Constants.PUT_BUTTONS_X < x < SAZE_OF_PICTYRE[0] + Constants.PUT_BUTTONS_X
            and 52 < y < SAZE_OF_PICTYRE[1] + 52
        ):
            DIFF = Difficlty.EASY
            BOMBS_ON_DIFF = Difficlty.BOMBS_ON_EASY
            SIZE_OF_TEXTURE = tuple(
                map(
                    lambda i: pygame.transform.smoothscale(
                        i, (Difficlty.TEXTURES_ON_EASY, Difficlty.TEXTURES_ON_EASY)
                    ),
                    all_images,
                )
            )
            game_status.state = Stages_of_game_constants.GAME

        elif (
            Constants.PUT_BUTTONS_X < x < SAZE_OF_PICTYRE[0] + Constants.PUT_BUTTONS_X
            and 220 < y < SAZE_OF_PICTYRE[1] + 220
        ):
            DIFF = Difficlty.MEDIUM
            BOMBS_ON_DIFF = Difficlty.BOMBS_ON_MEDIUM
            SIZE_OF_TEXTURE = tuple(
                map(
                    lambda i: pygame.transform.smoothscale(
                        i, (Difficlty.TEXTURES_ON_MEDIUM, Difficlty.TEXTURES_ON_MEDIUM)
                    ),
                    all_images,
                )
            )
            game_status.state = Stages_of_game_constants.GAME

        elif (
            Constants.PUT_BUTTONS_X < x < SAZE_OF_PICTYRE[0] + Constants.PUT_BUTTONS_X
            and 388 < y < SAZE_OF_PICTYRE[1] + 388
        ):
            DIFF = Difficlty.HARD
            BOMBS_ON_DIFF = Difficlty.BOMBS_ON_HARD
            SIZE_OF_TEXTURE = tuple(
                map(
                    lambda i: pygame.transform.smoothscale(
                        i, (Difficlty.TEXTURES_ON_HARD, Difficlty.TEXTURES_ON_HARD)
                    ),
                    all_images,
                )
            )
            game_status.state = Stages_of_game_constants.GAME

                    #danger gome
                    

        field = field_generate(DIFF, BOMBS_ON_DIFF)
        SIZE_OF_BLOCK = (min(WIDTH, HEIGHT) - Constants.ONE_CUBE_ON_PIXELS) // DIFF

    elif game_status.state == Stages_of_game_constants.GAME:
        change_x = (x - Constants.CUBES_DRAW_WIDTH) // (
            SIZE_OF_BLOCK + Constants.CELL_SPACING
        )
        change_y = (y - Constants.CUBES_DRAW_HEIGHT) // (
            SIZE_OF_BLOCK + Constants.CELL_SPACING
        )
        
        field_x_y=field[change_x][change_y]
        if change_x < DIFF and change_y < DIFF and field_x_y.is_solid and not field_x_y.is_dombed:
            field_x_y.is_solid = False
        elif change_x < DIFF and change_y < DIFF and field_x_y.is_solid and field_x_y.is_dombed:
            game_status.state=Stages_of_game_constants.END_OF_GAME
            
    
    elif game_status.state == Stages_of_game_constants.END_OF_GAME:
        if button == mouse.LEFT or button == mouse.RIGHT:
            game_status.state =Stages_of_game_constants.MENU
        #screen.draw.text('u lose',(200,300),color='white')
        
