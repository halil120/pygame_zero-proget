from enum import IntEnum, Enum, auto
from random import randint
import pygame
import time
import json
from pathlib import Path

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
    PLAYER_TEXTURE = images.player
    CHAMPIONS_TEXTURE = images.champions_button
    NAME_OF_CHAMPIONS = images.names_of_champions


DIFFICLTY={
'EASY' : {'field_size': 8,
        'bombs':10,
        'textures':62,
        'mulpt_player':1.0},

'MEDIUM' : {'field_size': 12,
        'bombs':11,
        'textures':41,
        'mulpt_player':1.5},
'HARD' : {'field_size': 16,
            'bombs':25,
            'textures':31,
            'mulpt_player':1.9},
}     


class StagesOfGameConstants(Enum):
    MENU = auto()
    CAMPIONS = auto()
    SELECTING_DIFFICULTY = auto()
    GAME = auto()
    END_OF_GAME = auto()
    WIN_OF_GAME = auto()
    ENTER_NAME = auto()


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

    def move(self):
        x, y = self.looking_to
        if 0 <= self.player_x + x < C_F_G_B.size_field and 0 <= self.player_y + y < C_F_G_B.size_field:
            move_to = field[self.player_x + x][self.player_y + y]
            if not move_to.is_solid:
                self.player_x += x
                self.player_y += y

    def break_block(self):
        x, y = self.looking_to
        if 0 <= self.player_x + x < C_F_G_B.size_field and 0 <= self.player_y + y < C_F_G_B.size_field:
            break_what = field[self.player_x + x][self.player_y + y]
            if break_what.is_bombed:
                game_status.state = StagesOfGameConstants.END_OF_GAME
            elif break_what.is_solid and not break_what.is_flagget:
                break_what.is_solid = False

    def plase_flag(self):
        global count_of_flags
        x, y = self.looking_to
        if 0 <= self.player_x + x < C_F_G_B.size_field and 0 <= self.player_y + y < C_F_G_B.size_field:
            field_x_y = field[self.player_x + x][self.player_y + y]

            if field_x_y.is_solid and not field_x_y.is_flagget:
                field_x_y.is_flagget = True
                count_of_flags += 1
            elif field_x_y.is_solid and field_x_y.is_flagget:
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
        global text_put_pixel
        if self.state == StagesOfGameConstants.MENU:
            screen.fill((40, 136, 235))
            screen.blit("game_button", (130, 60))

            screen.blit(ConstantsStr.CHAMPIONS_TEXTURE.value, (130, 250))

        if self.state == StagesOfGameConstants.CAMPIONS:
            screen.fill((40, 136, 235))
            screen.blit(ConstantsStr.NAME_OF_CHAMPIONS.value, (50, 25))
            read_records()

        elif self.state == StagesOfGameConstants.SELECTING_DIFFICULTY:

            if selected_diff_on_keybord == 0:
                screen.blit("select_diff_easy_selected", (Constants.PUT_BUTTONS_X, 52))
            else:
                screen.blit("select_diff_easy", (Constants.PUT_BUTTONS_X, 52))

            if selected_diff_on_keybord == 1:
                screen.blit(
                    "select_diff_medium_selected", (Constants.PUT_BUTTONS_X, 220)
                )
            else:
                screen.blit("select_diff_medium", (Constants.PUT_BUTTONS_X, 220))

            if selected_diff_on_keybord == 2:
                screen.blit("select_diff_hard_selected", (Constants.PUT_BUTTONS_X, 388))
            else:
                screen.blit("select_diff_hard", (Constants.PUT_BUTTONS_X, 388))

        elif (
            self.state == StagesOfGameConstants.GAME
            or self.state == StagesOfGameConstants.END_OF_GAME
        ):
            field_update(screen, field, C_F_G_B.size_field, C_F_G_B.size_block)

        elif self.state == StagesOfGameConstants.ENTER_NAME:
            draw_name_input(screen)
        

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
        if game_status.state == StagesOfGameConstants.END_OF_GAME:
            return self.texture_size[2]  
        return self.texture_size[2]   # 2 если хотите видеть бомбы, 0 если нет


class ClassForDifficltySelect:
    global_diff=None
    @staticmethod
    def diff_selector(diff):
        global C_F_G_B,field,TIMER_TIME,game_status
        SIZE_FIELD=DIFFICLTY[diff]['field_size']
        BOMBS_COUNT=DIFFICLTY[diff]['bombs']
        TEXTURE_SIZE=tuple(pygame.transform.smoothscale(i,(DIFFICLTY[diff]['textures'],DIFFICLTY[diff]['textures'])) for i in all_images)
        SIZE_OF_BLOCK = (min(WIDTH, HEIGHT) - Constants.ONE_CUBE_ON_PIXELS) // SIZE_FIELD
        global_diff=diff
        
        C_F_G_B=Constants_For_Game_Bild(SIZE_FIELD,BOMBS_COUNT,TEXTURE_SIZE,SIZE_OF_BLOCK,DIFFICLTY[diff]['mulpt_player'])
        field = field_generate(SIZE_FIELD, BOMBS_COUNT)
        TIMER_TIME = [SIZE_FIELD**2 * 2, time.time(), True]
        game_status.state = StagesOfGameConstants.GAME
        

class Constants_For_Game_Bild:
    def __init__(self,size_field,count_bombs,size_picture,size_block,center_player_mult=1):
        self.size_field=size_field
        self.count_bombs=count_bombs
        self.size_picture=size_picture
        self.size_block=size_block
        self.center_player_mult=center_player_mult
        self.center_player=None
        
    def make_center_player(self,cord,pl_x,pl_y,x_plus):
        player_x = cord * pl_x + Constants.CUBES_DRAW_WIDTH + x_plus
        player_y = (cord * pl_y+ Constants.CUBES_DRAW_WIDTH+ self.size_block * self.center_player_mult)
        return player_x,player_y




def chekc_bombs_nearby(field, x, y):
    if 0 <= x + 1 < C_F_G_B.size_field:
        field[x + 1][y].adjacent_mine_count += 1
    if 0 <= x - 1 < C_F_G_B.size_field:
        field[x - 1][y].adjacent_mine_count += 1
    if 0 <= y + 1 < C_F_G_B.size_field:
        field[x][y + 1].adjacent_mine_count += 1
    if 0 <= y - 1 < C_F_G_B.size_field:
        field[x][y - 1].adjacent_mine_count += 1


def field_generate(diff, bombs_on_diff):
    global C_F_G_B
    from itertools import product

    field = []
    for _ in range(diff):
        in_field = []
        for _ in range(diff):
            in_field.append(FieldObj(C_F_G_B.size_picture))
        field.append(in_field)
    bombs_to_plase = bombs_on_diff
    
    while bombs_to_plase:
        x = randint(0, diff - 1)
        y = randint(0, diff - 1)
        if not field[x][y].is_bombed and (x != 0 and y != 0) and field[x][y].adjacent_mine_count<1:
            field[x][y].is_bombed = True
            bombs_to_plase -= 1
            chekc_bombs_nearby(field,x,y)
            
    # место для добавлении механики чисел около бомб
    for x, y in product(range(C_F_G_B.size_field), range(C_F_G_B.size_field)):
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
                    field[x][y].adjacent_mine_count//2
                    if field[x][y].adjacent_mine_count
                    else ""
                ),
                (draw_x, draw_y),
                fontsize=40,
                color="white",
            )

    player_x,player_y=C_F_G_B.make_center_player(cordinates,player.player_x,player.player_y,13)

    screen_.blit(
        pygame.transform.smoothscale(
            ConstantsStr.PLAYER_TEXTURE.value,
            (
                (15, 25)
                if ClassForDifficltySelect.global_diff == 'MEDIUM' or 'HARD'
                else (25, 35)
            ),
        ),
        (player_x, player_y),
    )
    
    if game_status.state == StagesOfGameConstants.END_OF_GAME:
        screen_.draw.text("Game Over", (155, 265), color="black", fontsize=75)

    counter_flagget_bombs = 0
    for x, y in WHERE_BOMBS:
        if field[x][y].is_flagget:
            counter_flagget_bombs += 1
    if counter_flagget_bombs == count_of_flags and count_of_flags == C_F_G_B.count_bombs:
        game_status.state = StagesOfGameConstants.WIN_OF_GAME


def backfront(screen_):
    global records
    if game_status.state == StagesOfGameConstants.SELECTING_DIFFICULTY:
        screen_.fill((40, 136, 235))
    elif game_status.state == StagesOfGameConstants.GAME:
        screen_.fill((100, 100, 100))
    elif game_status.state == StagesOfGameConstants.END_OF_GAME:
        TIMER_TIME[2] = False
        screen_.fill((100, 100, 100))
        # screen_.draw.text("Game Over", (155, 265), color="white", fontsize=75)
    elif game_status.state == StagesOfGameConstants.WIN_OF_GAME:
        TIMER_TIME[2] = False
        screen_.fill((255, 255, 255))
        screen_.draw.text("You Win", (175, 265), color="black", fontsize=75)
    elif game_status.state == StagesOfGameConstants.ENTER_NAME:
        screen_.fill((40, 136, 235))


def timer_on_skreen(screen_):
    if TIMER_TIME[2]:
        remaining = max(0, int(TIMER_TIME[0] - (time.time() - TIMER_TIME[1])))
        screen_.draw.text(str(remaining), (30, 10), fontsize=74)
        screen_.draw.text("time", (35, 55), fontsize=22)


def read_records():
    text_put_pixel = 45
    with open("records.json", "r", encoding="utf-8") as file:
        screen.draw.text("EASY", (60, text_put_pixel), fontsize=35, color="black")
        text_put_pixel += 25
        records_loaded = json.load(file)

        easy = sorted(records_loaded["easy"], key=lambda i: i["time"])
        medium = sorted(records_loaded["medium"], key=lambda i: i["time"])
        hard = sorted(records_loaded["hard"], key=lambda i: i["time"])

        for i in range(3):
            if len(records_loaded["easy"]) > i:
                unformated_str=easy[i]
                screen.draw.text(
                    f'  {unformated_str['name']} {unformated_str['time']}', (60, text_put_pixel), fontsize=35, color="black"
                )
                text_put_pixel += 25
        screen.draw.text("MEDIUM", (60, text_put_pixel), fontsize=35, color="black")
        text_put_pixel += 25
        for i in range(3):
            if len(records_loaded["medium"]) > i:
                unformated_str=medium[i]
                screen.draw.text(
                    f'  {unformated_str['name']} {unformated_str['time']}', (60, text_put_pixel), fontsize=35, color="black"
                )
                text_put_pixel += 25
        screen.draw.text("HARD", (60, text_put_pixel), fontsize=35, color="black")
        text_put_pixel += 25
        for i in range(3):
            if len(records_loaded["hard"]) > i:
                unformated_str=hard[i]
                screen.draw.text(
                    f'  {unformated_str['name']} {unformated_str['time']}', (60, text_put_pixel), fontsize=35, color="black"
                )
                text_put_pixel += 25


def save_in_json():
    with open("records.json", "r", encoding="utf-8") as file:
        records_loaded = json.load(file)
    records_loaded[DICT_FOR_FNC[selected_diff_on_mouse]].append(
        {
            "name": player_name,
            "time": str(TIMER_TIME[0]-(max(0, int(TIMER_TIME[0] - (time.time() - TIMER_TIME[1]))))),
        }
    )
    with open("records.json", "w", encoding="utf-8") as file:
        json.dump(records_loaded, file, ensure_ascii=False, indent=2)


def draw_name_input(screen):
    screen.draw.text("Enter name:",center=(WIDTH // 2, 190),fontsize=40,color="white")

    screen.blit('neme_entering_picture',(100, 240))
    
    screen.draw.text(player_name,(115, 250),fontsize=35,color="black")

    screen.draw.text("Enter - Save",center=(WIDTH // 2, 330),fontsize=25,color="white")


WHERE_BOMBS = []
MAX_NAME_LENGHT=12
all_images = (
    ConstantsStr.STONE_TEXTURE.value,
    ConstantsStr.COLOR_BLOCK_DEFAULT.value,
    ConstantsStr.BOMB_TEXTURE.value,
)
game_status = StatesOfGame()
SAZE_OF_PICTYRE = images.select_diff_medium.get_size()
TIMER_TIME = [0, None, False]
count_of_flags = 0
player = PlayersClass(0, 0)
player_name=''


selected_diff_on_mouse = 0
selected_diff_on_keybord = 0

mouse_x, mouse_y = (10, 10)
DICT_FOR_FNC = {0: "easy", 1: "medium", 2: "hard"}

records_path = Path("records.json")
default_records = {"easy": [], "medium": [], "hard": []}
if not records_path.exists():
    with records_path.open("w", encoding="utf-8") as file:
        json.dump(default_records, file, ensure_ascii=False, indent=2)


def draw():
    screen.clear()

    backfront(screen)

    timer_on_skreen(screen)

    game_status.get_game_state(screen)

    screen.blit("cursor_mouse", (mouse_x - 5, mouse_y - 5))


def update():
    global mouse_y, mouse_x
    if TIMER_TIME[2] and time.time() - TIMER_TIME[1] >= TIMER_TIME[0]:
        TIMER_TIME[2] = False
    if (
        TIMER_TIME[2]
        and max(0, int(TIMER_TIME[0] - (time.time() - TIMER_TIME[1]))) == 0
    ):
        game_status.state = StagesOfGameConstants.END_OF_GAME

    mouse_x, mouse_y = pygame.mouse.get_pos()


def on_key_down(key,unicode):
    global selected_diff_on_keybord, player, WHERE_BOMBS, count_of_flags,player_name,MAX_NAME_LENGHT
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
        if game_status.state == StagesOfGameConstants.WIN_OF_GAME:
            game_status.state = StagesOfGameConstants.ENTER_NAME
        else:
            if key == keys.RETURN:

                selected_diff_on_keybord = 0
                game_status.state = StagesOfGameConstants.MENU
        WHERE_BOMBS = []
        count_of_flags = 0
            
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
                    ClassForDifficltySelect.diff_selector('HARD')
                else:
                    ClassForDifficltySelect.diff_selector('MEDIUM')
            else:
                ClassForDifficltySelect.diff_selector('EASY')

    elif game_status.state == StagesOfGameConstants.CAMPIONS:
        if key == keys.SPACE:
            game_status.state = StagesOfGameConstants.MENU
            
            
    elif game_status.state == StagesOfGameConstants.ENTER_NAME:
        
        if key == keys.BACKSPACE:
            player_name = player_name[:-1]

        elif key == keys.RETURN:
            save_in_json()
            game_status.state = StagesOfGameConstants.MENU

        elif unicode and len(player_name) < MAX_NAME_LENGHT:
            player_name += unicode


def on_mouse_down(pos, button):
    global count_of_flags, player, selected_diff_on_keybord, selected_diff_on_mouse,WHERE_BOMBS
    x, y = pos

    if game_status.state == StagesOfGameConstants.MENU:
        if 130 < x < 430 and 60 < y < 212:
            selected_diff_on_keybord = 0
            selected_diff_on_mouse = 0
            game_status.state = StagesOfGameConstants.SELECTING_DIFFICULTY
            player = PlayersClass(0, 0)

        elif 130 < x < 430 and 250 < y < 402:
            game_status.state = StagesOfGameConstants.CAMPIONS

    elif game_status.state == StagesOfGameConstants.CAMPIONS and button == mouse.RIGHT:
        game_status.state = StagesOfGameConstants.MENU

    elif game_status.state == StagesOfGameConstants.SELECTING_DIFFICULTY:

        # danger gome

        if (
            Constants.PUT_BUTTONS_X < x < SAZE_OF_PICTYRE[0] + Constants.PUT_BUTTONS_X
            and 52 < y < SAZE_OF_PICTYRE[1] + 52
        ):
            ClassForDifficltySelect.diff_selector('EASY')

        elif (
            Constants.PUT_BUTTONS_X < x < SAZE_OF_PICTYRE[0] + Constants.PUT_BUTTONS_X
            and 220 < y < SAZE_OF_PICTYRE[1] + 220
        ):
            selected_diff_on_mouse += 1
            ClassForDifficltySelect.diff_selector('MEDIUM')

        elif (
            Constants.PUT_BUTTONS_X < x < SAZE_OF_PICTYRE[0] + Constants.PUT_BUTTONS_X
            and 388 < y < SAZE_OF_PICTYRE[1] + 388
        ):
            selected_diff_on_mouse += 2
            ClassForDifficltySelect.diff_selector('HARD')

            # danger gome

    elif game_status.state == StagesOfGameConstants.GAME:

        change_x = (x - Constants.CUBES_DRAW_WIDTH) // (
            C_F_G_B.size_block + Constants.CELL_SPACING
        )
        change_y = (y - Constants.CUBES_DRAW_HEIGHT) // (
            C_F_G_B.size_block + Constants.CELL_SPACING
        )
        if 0 <= change_x < C_F_G_B.size_field and 0 <= change_y < C_F_G_B.size_field:
            field_x_y = field[change_x][change_y]
            if (
                change_x < C_F_G_B.size_field
                and change_y < C_F_G_B.size_field
                and field_x_y.is_solid
                and not field_x_y.is_bombed
                and not field_x_y.is_flagget
                and button == mouse.LEFT
            ):
                field_x_y.is_solid = False
                field_x_y.is_flagget = False
            elif (
                change_x < C_F_G_B.size_field
                and change_y < C_F_G_B.size_field
                and field_x_y.is_solid
                and not field_x_y.is_flagget
                and button == mouse.RIGHT
            ):
                field_x_y.is_flagget = True
                count_of_flags += 1
            elif (
                change_x < C_F_G_B.size_field
                and change_y < C_F_G_B.size_field
                and field_x_y.is_solid
                and field_x_y.is_flagget
                and button == mouse.RIGHT
            ):
                field_x_y.is_flagget = False
                count_of_flags -= 1
            elif (
                change_x < C_F_G_B.size_field
                and change_y < C_F_G_B.size_field
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
        if game_status.state == StagesOfGameConstants.WIN_OF_GAME:
            game_status.state = StagesOfGameConstants.ENTER_NAME
        else:
            if button == mouse.LEFT or button == mouse.RIGHT:
                game_status.state = StagesOfGameConstants.MENU
        WHERE_BOMBS = []
        count_of_flags = 0

