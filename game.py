from enum import IntEnum, Enum, auto
from random import randint
import pygame
import time

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


class ConstantsStr(Enum):
    COLOR_BLOCK_DEFAULT = images.empty_41
    STONE_TEXTURE = images.stone_41
    BOMB_TEXTURE = images.bomb_41
    PLAYER_TEXTURE=images.player
    CHAMPIONS_TEXTURE=images.champions_button
    NAME_OF_CHAMPIONS=images.names_of_champions


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


class StagesOfGameConstants(Enum):
    MENU = auto()
    CAMPIONS=auto()
    SELECTING_DIFFICULTY = auto()
    GAME = auto()
    END_OF_GAME = auto()
    WIN_OF_GAME = auto()


class Rotations(Enum):
    W = (0, -1)
    S = (0, 1)
    A = (-1, 0)
    D = (1, 0)


class PlayersClass:
    def __init__(self, x, y):
        self.player_x = x
        self.player_y = y
        self.looking_to = (0, 0)
        self.score = 0
        self.money = 0
        self.dig_speed = 1

    def move(self):
        x, y = self.looking_to
        if 0<=self.player_x + x<DIFF and 0<=self.player_y + y<DIFF:
            move_to=field[self.player_x + x][self.player_y + y]
            if not move_to.is_solid:
                self.player_x += x
                self.player_y += y


    def break_block(self):
        x, y = self.looking_to
        if 0<=self.player_x + x<DIFF and 0<=self.player_y + y<DIFF:
            break_what = field[self.player_x + x][
                self.player_y + y]
            if break_what.is_bombed:
                game_status.state = StagesOfGameConstants.END_OF_GAME
            elif break_what.is_solid and not break_what.is_flagget:
                break_what.is_solid = False
                
                
    def plase_flag(self):
        global count_of_flags
        x, y = self.looking_to
        if 0<=self.player_x + x<DIFF and 0<=self.player_y + y<DIFF:
            field_x_y=field[self.player_x + x][self.player_y + y]
            
            if (
                field_x_y.is_solid
                and not field_x_y.is_flagget
            ):
                field_x_y.is_flagget = True
                count_of_flags += 1
            elif (
                field_x_y.is_solid
                and field_x_y.is_flagget
            ):
                field_x_y.is_flagget = False
                count_of_flags -= 1

        
    def change_looking_to(self, rotation):
        # x,y=rotation.value
        # self.looking_to=(self.player_x+x,self.player_y+y)
        self.looking_to = rotation.value


class StatesOfGame:
    def __init__(self):
        self.state = StagesOfGameConstants.MENU

    def get_game_state(self, screen):
        if self.state == StagesOfGameConstants.MENU:
            screen.fill((40, 136, 235))
            screen.blit("game_button", (130, 60))
            
            screen.blit(ConstantsStr.CHAMPIONS_TEXTURE.value, (130, 250))

        if self.state==StagesOfGameConstants.CAMPIONS:
            screen.fill((40, 136, 235))
            screen.blit(ConstantsStr.NAME_OF_CHAMPIONS.value, (50, 25))
            screen.draw.text(str(TIMER_TIME[0] - (time.time() - TIMER_TIME[1])),(70, 45),fontsize=35, color="black")

        elif self.state == StagesOfGameConstants.SELECTING_DIFFICULTY:

            if selected_diff_on_keybord==0:
                screen.blit("select_diff_easy_selected", (Constants.PUT_BUTTONS_X, 52))
            else:
                screen.blit("select_diff_easy", (Constants.PUT_BUTTONS_X, 52))

            if selected_diff_on_keybord==1:
                screen.blit("select_diff_medium_selected", (Constants.PUT_BUTTONS_X, 220))
            else:
                screen.blit("select_diff_medium", (Constants.PUT_BUTTONS_X, 220))

            if selected_diff_on_keybord==2:
                screen.blit("select_diff_hard_selected", (Constants.PUT_BUTTONS_X, 388))
            else:
                screen.blit("select_diff_hard", (Constants.PUT_BUTTONS_X, 388))

        elif self.state == StagesOfGameConstants.GAME or self.state == StagesOfGameConstants.END_OF_GAME:
            field_update(screen, field, DIFF, SIZE_OF_BLOCK)
            


class FieldObj:
    def __init__(self, texture_size):
        self.is_solid = True
        self.is_bombed = False
        self.is_flagget = False
        self.adjacent_mine_count = 0
        self.texture_size = texture_size

    def texture_give(self):
        if not self.is_solid:
            self.is_flagget = False
        if self.is_solid and not self.is_bombed:
            return self.texture_size[0]
        elif not self.is_solid and not self.is_bombed:
            return self.texture_size[1]
        if game_status.state==StagesOfGameConstants.END_OF_GAME:
            return self.texture_size[2]  # 2 если хотите видеть бомбы, 0 если нет
        return self.texture_size[0]


class ClassForDifficltySelect:
    @staticmethod
    def easy():
        global DIFF, BOMBS_ON_DIFF, TIMER_TIME, SIZE_OF_TEXTURE, SIZE_OF_BLOCK, field
        DIFF = Difficlty.EASY
        BOMBS_ON_DIFF = Difficlty.BOMBS_ON_EASY
        TIMER_TIME = [Difficlty.EASY**2 * 2, time.time(), True]
        SIZE_OF_TEXTURE = tuple(
            map(
                lambda i: pygame.transform.smoothscale(
                    i, (Difficlty.TEXTURES_ON_EASY, Difficlty.TEXTURES_ON_EASY)
                ),
                all_images,
            )
        )
        field = field_generate(DIFF, BOMBS_ON_DIFF)
        SIZE_OF_BLOCK = (min(WIDTH, HEIGHT) - Constants.ONE_CUBE_ON_PIXELS) // DIFF
        game_status.state = StagesOfGameConstants.GAME

    def medium():
        global DIFF, BOMBS_ON_DIFF, TIMER_TIME, SIZE_OF_TEXTURE, SIZE_OF_BLOCK, field
        DIFF = Difficlty.MEDIUM
        BOMBS_ON_DIFF = Difficlty.BOMBS_ON_MEDIUM
        TIMER_TIME = [Difficlty.MEDIUM**2 * 2, time.time(), True]
        SIZE_OF_TEXTURE = tuple(
            map(
                lambda i: pygame.transform.smoothscale(
                    i, (Difficlty.TEXTURES_ON_MEDIUM, Difficlty.TEXTURES_ON_MEDIUM)
                ),
                all_images,
            )
        )
        field = field_generate(DIFF, BOMBS_ON_DIFF)
        SIZE_OF_BLOCK = (min(WIDTH, HEIGHT) - Constants.ONE_CUBE_ON_PIXELS) // DIFF
        game_status.state = StagesOfGameConstants.GAME

    def hard():
        global DIFF, BOMBS_ON_DIFF, TIMER_TIME, SIZE_OF_TEXTURE, SIZE_OF_BLOCK, field
        DIFF = Difficlty.HARD
        BOMBS_ON_DIFF = Difficlty.BOMBS_ON_HARD
        TIMER_TIME = [Difficlty.HARD**2 * 2, time.time(), True]
        SIZE_OF_TEXTURE = tuple(
            map(
                lambda i: pygame.transform.smoothscale(
                    i, (Difficlty.TEXTURES_ON_HARD, Difficlty.TEXTURES_ON_HARD)
                ),
                all_images,
            )
        )
        field = field_generate(DIFF, BOMBS_ON_DIFF)
        SIZE_OF_BLOCK = (min(WIDTH, HEIGHT) - Constants.ONE_CUBE_ON_PIXELS) // DIFF
        game_status.state = StagesOfGameConstants.GAME


def chekc_bombs_nearby(field, x, y):
    if 0 <= x + 1 < DIFF:
        field[x + 1][y].adjacent_mine_count += 1
    if 0 <= x - 1 < DIFF:
        field[x - 1][y].adjacent_mine_count += 1
    if 0 <= y + 1 < DIFF:
        field[x][y + 1].adjacent_mine_count += 1
    if 0 <= y - 1 < DIFF:
        field[x][y - 1].adjacent_mine_count += 1


def field_generate(diff, bombs_on_diff):
    from itertools import product

    field = []
    for _ in range(diff):
        in_field = []
        for _ in range(diff):
            in_field.append(FieldObj(SIZE_OF_TEXTURE))
        field.append(in_field)
    bombs_to_plase = bombs_on_diff
    while bombs_to_plase:
        x = randint(0, diff - 1)
        y = randint(0, diff - 1)
        if not field[x][y].is_bombed and (x != 0 and y != 0):
            field[x][y].is_bombed = True
            bombs_to_plase -= 1
    # место для добавлении механики чисел около бомб
    for x, y in product(range(DIFF.value), range(DIFF.value)):
        if field[x][y].is_bombed:
            chekc_bombs_nearby(field, x, y)
            WHERE_BOMBS.append((x, y))

    # место для добавлении механики чисел около бомб
    return field


def field_update(screen_, field, count_field, size_of_block):
    from itertools import product

    for x, y in product(range(count_field), range(count_field)):

        cordinates = size_of_block + Constants.CELL_SPACING
        draw_x = cordinates * x + Constants.CUBES_DRAW_WIDTH
        draw_y = cordinates * y + Constants.CUBES_DRAW_HEIGHT

        screen_.blit(field[x][y].texture_give(), (draw_x, draw_y))

        if field[x][y].is_flagget:
            screen_.draw.text("o", (draw_x, draw_y), fontsize=45, color="red")
        if not field[x][y].is_solid:
            screen_.draw.text(
                str(
                    field[x][y].adjacent_mine_count
                    if field[x][y].adjacent_mine_count
                    else ""
                ),
                (draw_x, draw_y),
                fontsize=40,
                color="white",
            )

    player_x = cordinates * player.player_x + Constants.CUBES_DRAW_WIDTH+DIFF
    if DIFF==Difficlty.MEDIUM:
        player_y = cordinates * player.player_y + Constants.CUBES_DRAW_WIDTH + size_of_block*1.5
    elif DIFF==Difficlty.EASY:
        player_y = cordinates * player.player_y + Constants.CUBES_DRAW_WIDTH + size_of_block
    else:
        player_x = cordinates * player.player_x + Constants.CUBES_DRAW_WIDTH+10
        player_y = cordinates * player.player_y + Constants.CUBES_DRAW_WIDTH + size_of_block*1.9
        
    screen_.blit(pygame.transform.smoothscale(ConstantsStr.PLAYER_TEXTURE.value,(15,25)if DIFF==Difficlty.MEDIUM or DIFF==Difficlty.HARD else (25,35)), (player_x, player_y))
    if game_status.state == StagesOfGameConstants.END_OF_GAME:
        screen_.draw.text("Game Over", (155, 265), color="black", fontsize=75)

    counter_flagget_bombs = 0
    for x, y in WHERE_BOMBS:
        if field[x][y].is_flagget:
            counter_flagget_bombs += 1
    if counter_flagget_bombs == count_of_flags and count_of_flags == BOMBS_ON_DIFF:
        game_status.state = StagesOfGameConstants.WIN_OF_GAME


def backfront(screen_):
    if game_status.state == StagesOfGameConstants.SELECTING_DIFFICULTY:
        screen_.fill((40, 136, 235))
    elif game_status.state == StagesOfGameConstants.GAME:
        screen_.fill((100, 100, 100))
    elif game_status.state == StagesOfGameConstants.END_OF_GAME:
        records.append(TIMER_TIME[1])
        TIMER_TIME[2] = False
        screen_.fill((100, 100, 100))
        #screen_.draw.text("Game Over", (155, 265), color="white", fontsize=75)
    elif game_status.state == StagesOfGameConstants.WIN_OF_GAME:
        TIMER_TIME[2] = False
        screen_.fill((255, 255, 255))
        screen_.draw.text("You Win", (175, 265), color="black", fontsize=75)


def timer_on_skreen(screen_):
    if TIMER_TIME[2]:
        remaining = max(0, int(TIMER_TIME[0] - (time.time() - TIMER_TIME[1])))
        screen_.draw.text(str(remaining), (30, 10), fontsize=74)
        screen_.draw.text("time", (35, 55), fontsize=22)

DIFF = Difficlty.DEFAULT
BOMBS_ON_DIFF = Difficlty.DEFAULT_BOMBS
SIZE_OF_TEXTURE = 20
SIZE_OF_BLOCK = 0
WHERE_BOMBS = []
all_images = (
    ConstantsStr.STONE_TEXTURE.value,
    ConstantsStr.COLOR_BLOCK_DEFAULT.value,
    ConstantsStr.BOMB_TEXTURE.value,
)
game_status = StatesOfGame()
SAZE_OF_PICTYRE = images.select_diff_medium.get_size()
TIMER_TIME = [Difficlty.DEFAULT**2, None, False]
count_of_flags = 0
player = PlayersClass(0, 0)
selected_diff_on_keybord = 0
mouse_x,mouse_y=(10,10)
field = []
records=[]

def draw():
    screen.clear()

    backfront(screen)
    
    timer_on_skreen(screen)

    game_status.get_game_state(screen)

    screen.blit("cursor_mouse",(mouse_x-5,mouse_y-5))

def update():
    global mouse_y,mouse_x
    if TIMER_TIME[2] and time.time() - TIMER_TIME[1] >= TIMER_TIME[0]:
        TIMER_TIME[2] = False
    if (
        TIMER_TIME[2]
        and max(0, int(TIMER_TIME[0] - (time.time() - TIMER_TIME[1]))) == 0
    ):
        game_status.state = StagesOfGameConstants.END_OF_GAME
        
        
    mouse_x,mouse_y=pygame.mouse.get_pos()

    
            
        


def on_key_down(key):
    global selected_diff_on_keybord, player, WHERE_BOMBS, count_of_flags
    if game_status.state == StagesOfGameConstants.GAME:
        if key == keys.D:
            player.change_looking_to(Rotations.D)
        elif key == keys.A:
            player.change_looking_to(Rotations.A)
        elif key == keys.W:
            player.change_looking_to(Rotations.W)
        elif key == keys.S:
            player.change_looking_to(Rotations.S)
        elif key == keys.RETURN:
            player.break_block()
        elif key == keys.SPACE:
            player.move()
        elif key == keys.LSHIFT or key == keys.RSHIFT:
            player.plase_flag()

    elif (
        game_status.state == StagesOfGameConstants.END_OF_GAME
        or game_status.state == StagesOfGameConstants.WIN_OF_GAME
    ):
        WHERE_BOMBS = []
        count_of_flags = 0
        if key == keys.RETURN:

            selected_diff_on_keybord = 0
            game_status.state = StagesOfGameConstants.MENU

    elif game_status.state == StagesOfGameConstants.MENU:
        if key == keys.RETURN:
            game_status.state = StagesOfGameConstants.SELECTING_DIFFICULTY
            player = PlayersClass(0, 0)

    elif game_status.state == StagesOfGameConstants.SELECTING_DIFFICULTY:
        if key == keys.W:
            selected_diff_on_keybord = max(selected_diff_on_keybord - 1, 0)
        elif key == keys.S:
            selected_diff_on_keybord = min(selected_diff_on_keybord + 1, 2)

        if key == keys.RETURN:
            if selected_diff_on_keybord:
                if selected_diff_on_keybord - 1:
                    ClassForDifficltySelect.hard()
                else:
                    ClassForDifficltySelect.medium()
            else:
                ClassForDifficltySelect.easy()
    
    elif game_status.state == StagesOfGameConstants.CAMPIONS:
        if key == keys.SPACE:
            game_status.state = StagesOfGameConstants.MENU


def on_mouse_down(pos, button):
    global DIFF, BOMBS_ON_DIFF, field, SIZE_OF_BLOCK, SIZE_OF_TEXTURE, TIMER_TIME, WHERE_BOMBS, count_of_flags, player, selected_diff_on_keybord,records
    x, y = pos

    if game_status.state == StagesOfGameConstants.MENU:
        if 130 < x < 430 and 60 < y < 212:
            selected_diff_on_keybord = 0
            game_status.state = StagesOfGameConstants.SELECTING_DIFFICULTY
            player = PlayersClass(0, 0)
            
        elif 130<x<430 and 250<y<402:
            game_status.state = StagesOfGameConstants.CAMPIONS
    elif game_status.state == StagesOfGameConstants.SELECTING_DIFFICULTY:

        # danger gome

        if (
            Constants.PUT_BUTTONS_X < x < SAZE_OF_PICTYRE[0] + Constants.PUT_BUTTONS_X
            and 52 < y < SAZE_OF_PICTYRE[1] + 52
        ):
            ClassForDifficltySelect.easy()

        elif (
            Constants.PUT_BUTTONS_X < x < SAZE_OF_PICTYRE[0] + Constants.PUT_BUTTONS_X
            and 220 < y < SAZE_OF_PICTYRE[1] + 220
        ):
            ClassForDifficltySelect.medium()

        elif (
            Constants.PUT_BUTTONS_X < x < SAZE_OF_PICTYRE[0] + Constants.PUT_BUTTONS_X
            and 388 < y < SAZE_OF_PICTYRE[1] + 388
        ):
            ClassForDifficltySelect.hard()

            # danger gome

    elif game_status.state == StagesOfGameConstants.GAME:

        change_x = (x - Constants.CUBES_DRAW_WIDTH) // (
            SIZE_OF_BLOCK + Constants.CELL_SPACING
        )
        change_y = (y - Constants.CUBES_DRAW_HEIGHT) // (
            SIZE_OF_BLOCK + Constants.CELL_SPACING
        )
        if 0 <= change_x < DIFF and 0 <= change_y < DIFF:
            field_x_y = field[change_x][change_y]
            if (
                change_x < DIFF
                and change_y < DIFF
                and field_x_y.is_solid
                and not field_x_y.is_bombed
                and not field_x_y.is_flagget
                and button == mouse.LEFT
            ):
                field_x_y.is_solid = False
                field_x_y.is_flagget = False
            elif (
                change_x < DIFF
                and change_y < DIFF
                and field_x_y.is_solid
                and not field_x_y.is_flagget
                and button == mouse.RIGHT
            ):
                field_x_y.is_flagget = True
                count_of_flags += 1
            elif (
                change_x < DIFF
                and change_y < DIFF
                and field_x_y.is_solid
                and field_x_y.is_flagget
                and button == mouse.RIGHT
            ):
                field_x_y.is_flagget = False
                count_of_flags -= 1
            elif (
                change_x < DIFF
                and change_y < DIFF
                and field_x_y.is_solid
                and field_x_y.is_bombed
                and not field_x_y.is_flagget
                and button == mouse.LEFT
            ):
                game_status.state = StagesOfGameConstants.END_OF_GAME

    elif (
        game_status.state == StagesOfGameConstants.END_OF_GAME
        or game_status.state == StagesOfGameConstants.WIN_OF_GAME
    ):
        WHERE_BOMBS = []
        count_of_flags = 0
        if button == mouse.LEFT or button == mouse.RIGHT:
            game_status.state = StagesOfGameConstants.MENU
