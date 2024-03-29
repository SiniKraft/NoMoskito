import os
import pathlib
import sys
import time

import nathlib as nlib
from constants import *

debug_mouse = False

if os.path.isfile(LOG_PATH):
    try:
        os.remove(LOG_PATH)
    except Exception as e:
        nlib.log("Couldn't remove latest.log : {}".format(str(e)), "warn")
if not os.path.isfile(ENABLE_LOGS_PATH):
    with open(ENABLE_LOGS_PATH, "w") as file:
        file.write("# Enable logging ? \"yes\" or \"no\"\nDefaults to \"no\"to avoid unnecessary log file rewriting.\n"
                   "You should let this parameter to \"no\" unless you have an error.\nno")
enable_logs = LOG_PATH
with open(ENABLE_LOGS_PATH, "r") as file:
    if file.readlines()[3].startswith("no"):
        enable_logs = None

nlib.start_logs(enable_logs)

if not os.path.isfile(JOY_ID_PATH):
    with open(JOY_ID_PATH, "w") as file:
        file.write("0\n1\n1\n1\n# First 2 lines : X Axis id and Y Axis id\n# Last 2 lines : Invert them (*1) or (*-1)")
joystick_id0, joystick_id1 = (0, 1)
joy_multiplier = (1, 1)
with open(JOY_ID_PATH, "r") as file:
    try:
        splt = file.read().split("\n")
        joystick_id0, joystick_id1 = (int(splt[0]), int(splt[1]))
        joy_multiplier = (int(splt[2]), int(splt[3]))
    except Exception as e:
        nlib.log("Cannot load joystick id !\n" + str(e), "error")

nlib.log("Launching game version {0} ...".format(VERSION_STRING), "info")

print(joystick_id0, joystick_id1, joy_multiplier)

def exception_handler(_type, value, traceback):
    nlib.log("{0}: {1}\nTraceback : {2}".format(repr(value).split("(")[0], value, str(traceback)), "critical", 'main')
    from tkinter import Tk, messagebox
    _root = Tk()
    _root.attributes("-topmost", True)
    _root.withdraw()
    messagebox.showerror("An error occurred", "{}: {}".format(repr(value).split("(")[0], value))
    _root.destroy()
    sys.exit(1)


enable_exception_handler = False
if enable_exception_handler:
    sys.excepthook = exception_handler
enable_hash_checking = False  # Should only be enabled when released !!!

if enable_hash_checking:
    import hashlib
    hashes = []  # hashes = [["name.py", "hash"],]

    for _hash in hashes:

        sha256_hash = hashlib.sha256()
        with open(_hash[0], "rb") as f:
            # Read and update hash string value in blocks of 4K
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
            if sha256_hash.hexdigest() == _hash[1]:
                nlib.log("Successfully checked hash for '{0}'".format(_hash[0]), "info")
            else:
                nlib.log("File '{0}' got a different hash than expected !\nExpected '{1}',\nGot '{2}' !"
                         .format(_hash[0], _hash[1], sha256_hash.hexdigest()), "fatal")
                time.sleep(1)
                sys.exit()
else:
    nlib.log("Skipping hash checking !", "warn")

# Importation des modules

# try:
print("------------------------------Pygame--Details--------------------------")
import pygame

print("-----------------------------------------------------------------------")
import time
import random
import math
import pygame.gfxdraw  # necessary as pygame doesn't load it by default !
from settings_window import open_settings
import ptext
import operator
import zipfile
import io
import dialog as d

try:
    pygame.joystick.init()
    joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
except Exception as e:
    print(e)

# except ImportError:
# print("[ERROR]: Failed to import modules !")
# from sys import exit

# exit()

try:
    from scripts.util.FileManager import *
except Exception as e:
    nlib.log("Failed to load resources, aborting ... (%s)" % str(e), "critical")
    sys.exit(1)

# Initialisation de Pygame

pygame.init()
pygame.font.init()
if settings_list[2]:
    pygame.mixer.init()  # Sons de pygame.

# Window definition

window_x = 1280
window_y = 720
if not settings_list[3]:
    screen = pygame.display.set_mode((window_x, window_y))
else:
    screen = pygame.display.set_mode((window_x, window_y), pygame.FULLSCREEN | pygame.SCALED)
pygame.display.set_caption("NoMoskito!")
pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
clock = pygame.time.Clock()

pak = None
if isfile(RESOURCE_PAK_PATH):
    pak = zipfile.ZipFile(RESOURCE_PAK_PATH, 'r')
    segoeui = pygame.font.Font(io.BytesIO(pak.read(SUI_FILE_NAME)), 50)
else:
    segoeui = pygame.font.Font(SUI_PATH, 50)


def ComicSansMSM():
    return CSM_PATH


CSM_30 = pygame.font.Font(ComicSansMSM(), 30)
CSM_25 = pygame.font.Font(ComicSansMSM(), 25)
CSM_26 = pygame.font.Font(ComicSansMSM(), 26)
CSM_40 = pygame.font.Font(ComicSansMSM(), 40)
CSM_45 = pygame.font.Font(ComicSansMSM(), 45)
CSM_70 = pygame.font.Font(ComicSansMSM(), 70)


def load_image(filepath: str):
    if isfile(RESOURCE_PAK_PATH):
        return pygame.image.load(io.BytesIO(pak.read(filepath.replace(RESOURCES_PREFIX, "")))).convert_alpha()
    else:
        return pygame.image.load(filepath).convert_alpha()


# ressources à charger
shop_blood_bag = load_image("resources/blood_bag.png").convert_alpha()
shop_blood_bag = pygame.transform.scale(shop_blood_bag, (50, 50))
shop_blood_bottle = load_image("resources/blood_bottle.png").convert_alpha()
shop_blood_bottle = pygame.transform.scale(shop_blood_bottle, (80, 80))
shop_blood_barrel = load_image("resources/barrel_blood.png").convert_alpha()
shop_blood_barrel = pygame.transform.scale(shop_blood_barrel, (96, 96))
shop_blood_infusion = load_image("resources/blood_infusion.png").convert_alpha()
shop_blood_infusion = pygame.transform.scale(shop_blood_infusion, (176, 117))
swatter_pro = load_image("resources/swatter_pro.png").convert_alpha()
shop_swatter_pro = pygame.transform.scale(swatter_pro, (41, 275))
bzio_ruler = load_image("resources/imposant_ruler.png").convert_alpha()
bzio_ruler_in_game = load_image("resources/imposant_ruler_in_game.png").convert_alpha()
shop_bzio_ruler = pygame.transform.scale(bzio_ruler, (128, 128))
pause_bzio_ruler = pygame.transform.rotate(shop_bzio_ruler, 90)
img_heat_wave = load_image("resources/hot.png").convert_alpha()
shop_heat_wave = pygame.transform.scale(img_heat_wave, (17, 48))
img_spray = load_image("resources/anti_moskito_spray.png").convert_alpha()
shop_spray = pygame.transform.scale(img_spray, (38, 85))
img_lamp = load_image("resources/anti_moskito_lamp.png").convert_alpha()
shop_lamp = pygame.transform.scale(img_lamp, (66, 95))
img_wait_bar_1 = load_image("resources/resource_0.png").convert_alpha()
img_icon = load_image("resources/resource_2.png").convert_alpha()
img_background = load_image("resources/resource_1.jpg").convert()
img_logo = load_image("resources/resource_4.png").convert_alpha()
img_btn_normal = load_image("resources/resource_5.png").convert()
img_btn_hovered = load_image("resources/resource_6.png").convert()
img_swatter_1 = load_image("resources/resource_8.png").convert_alpha()
pause_swatter_1 = pygame.transform.scale(img_swatter_1, (41, 275))
dark_img = load_image("resources/dark.png").convert_alpha()
init_img = load_image("resources/init.png").convert()
img_info = load_image("resources/mosquito_info.png").convert_alpha()
img_question = load_image("resources/mosquito_question.png").convert_alpha()
img_error = load_image("resources/mosquito_error.png").convert_alpha()
img_ask_string = load_image("resources/mosquito_text.png").convert_alpha()
img_pix_wait_bar = pygame.Surface((1, 13))
img_pix_wait_bar.fill((104, 255, 4))
img_blood_bar = load_image("resources/resource_9.png").convert_alpha()
btn_font = CSM_30
img_pix_blood_bar = pygame.Surface((38, 1))
img_pix_blood_bar.fill((255, 0, 0))
img_moskito_list = [load_image("resources/mosquito_1.png").convert_alpha(),
                    load_image("resources/mosquito_2.png").convert_alpha(),
                    load_image("resources/mosquito_3.png").convert_alpha(),
                    load_image("resources/mosquito_4.png").convert_alpha()]

shop_bg = pygame.Surface((1180, 660))
pygame.gfxdraw.rectangle(shop_bg, shop_bg.get_rect(), (206, 237, 31))
pygame.gfxdraw.rectangle(shop_bg, pygame.rect.Rect(1, 1, 1178, 658), (206, 237, 31))
pygame.gfxdraw.rectangle(shop_bg, pygame.rect.Rect(2, 2, 1176, 656), (206, 237, 31))
pygame.gfxdraw.box(shop_bg, pygame.rect.Rect(3, 3, 1174, 654), (235, 248, 165))
pygame.gfxdraw.box(shop_bg, pygame.rect.Rect(3, 3, 1174, 50), (220, 242, 96))
pause_bg = pygame.Surface((1280, 720))


shop_btn_ids = {"shop_btn_blood_2": 0,
                "shop_btn_blood_3": 1,
                "shop_btn_blood_4": 2,
                "shop_btn_blood_5": 3,
                "shop_btn_heat_wave": 6,
                "shop_btn_spray": 7,
                "shop_btn_lamp": 8}

sounds_moskitos_list = ["resources/sounds/Single_moskito_1.wav",
                        "resources/sounds/Single_moskito_2.wav",
                        "resources/sounds/Single_moskito_3.wav",
                        "resources/sounds/Single_moskito_4.wav"]

img_tmp = pygame.Surface((4, 4))
img_tmp.fill((255, 255, 255))
font_a = CSM_70

opaque = 655

if isfile(RESOURCE_PAK_PATH):
    spray_sound_obj = pygame.mixer.Sound(io.BytesIO(pak.read("sounds/Anti_Moskito_Spray.wav")))
    main_sound_obj = pygame.mixer.Sound(io.BytesIO(pak.read("sounds/Main_Menu_Music.wav")))
    shop_music_obj = pygame.mixer.Sound(io.BytesIO(pak.read("sounds/Shop_Music.wav")))
else:
    spray_sound_obj = pygame.mixer.Sound("resources/sounds/Anti_Moskito_Spray.wav")
    main_sound_obj = pygame.mixer.Sound("resources/sounds/Main_Menu_Music.wav")  # do not use mixer.music, so it loads
    # all in memory
    shop_music_obj = pygame.mixer.Sound("resources/sounds/Shop_Music.wav")

pygame.display.set_icon(img_icon)

sprite_group = pygame.sprite.Group()

anti_moskito_spray = 0
moskito_lamp_time = 0
is_heat_wave = False
using_controller = False
last_controller = 0
is_dialog = 0

isMenu = True

pause_btn_list = []

play_btn_text = btn_font.render(default_lang[0], True, (153, 153, 0))
settings_btn_text = btn_font.render(default_lang[1], True, (153, 153, 0))
font_a_text = font_a.render(default_lang[11], True, (153, 153, 0))


def get_bziocoins():
    return get_better_score()[2]


def get_inventory():
    a = get_better_score()
    return [a[4], a[3]]


def remove_item_from_inventory(inv_list, item_id: int):  # remove 1 item and return the result
    tmp_list = []
    found = False
    for _i in inv_list:
        tmp_list.append(_i)  # simple way to copy two lists in python :/
    for item in range(0, len(inv_list)):
        if inv_list[item] == item_id:
            if not found:
                tmp_list.pop(item)
                found = True
    return tmp_list


def save_bziocoins(bziocoins):
    a = get_better_score()
    overwrite_better_score(a[0], a[1], bziocoins, a[3], a[4])


def save_inventory(__inv, buy):  # buy = which swatter you bought.
    a = get_better_score()
    overwrite_better_score(a[0], a[1], a[2], buy, __inv)


def NewMoskitoSound():
    if isfile(RESOURCE_PAK_PATH):
        return pygame.mixer.Sound(io.BytesIO(pak.read(sounds_moskitos_list[random.randint(
            0, len(sounds_moskitos_list) - 1)].replace(RESOURCES_PREFIX, ""))))
    else:
        return pygame.mixer.Sound(sounds_moskitos_list[random.randint(0, len(sounds_moskitos_list) - 1)])


# definition du joueur
BLOOD = 600
blood_infusion = 0
blood_infusion_total = 0
blood_factor = 0
button_pressed = False

shop_hovered_id = -1


class Var:
    def __init__(self):
        super(Var, self).__init__()
        self.inventory = []
        self.change_fullscreen = False
        self.bziocoins = get_bziocoins()
        self.last_mouse = (0, 0)
        self.is_settings_to_save = False
        self.IsGamePaused = False
        self.is_update_checked = False
        self.isMenu = True
        self.can_click = True
        self.click_delay = 388
        self.click_rate = 1
        self.blood = BLOOD
        self.moskitos_killed = 0
        self.Playing = False
        self.Final_Menu = False
        self.chrono = 0  # ms
        self.latest_chrono = 0
        self.renew_sound = True
        self.enable_sound = settings_list[2]
        self.btn_hover_list = []
        self.btn_click_list = []
        self.Final_verdict = False
        self.shop = False
        self.best_score = [0, "nobody"]

    def set_value(self, var_name, var_value):
        if var_name == "is_settings_to_save":
            self.is_settings_to_save = var_value
        if var_name == "is_update_checked":
            self.is_update_checked = var_value

    def get_value(self, var_name):
        if self.shop:
            pass
        return eval("self." + var_name)


global_var = Var()
global_var.inventory = get_inventory()[0]

# class Player(pygame.sprite.Sprite):
#     def __init__(self):
#         super().__init__()
#         self.image = img_spaceship
#         self.rect = self.image.get_rect()
#         self.velocity = [0, 0]
#         self.rect.x = int(window_x / 2.15)
#         self.rect.y = int(window_y / 2.15)


# class Star(pygame.sprite.Sprite):
#     def __init__(self):
#         super().__init__()
#         self.image = img_star
#         self.rect = self.image.get_rect()
#         self.velocity = [0, 0]
#         self.rect.x = random.randint(0, window_x)
#         self.rect.y = random.randint(0, window_y)
#
#     def walk_with_degrees(self, degree, distance):
#         self.rect.y = int(self.rect.y + (distance * sin(degree)))
#         self.rect.x = int(self.rect.x + (distance * cos(degree)))
#
#     def update(self, angle_in):
#         self.walk_with_degrees(angle_in, 1)
FPS_COUNT = 0


class MoskitoSpawnHandler:
    def __init__(self):
        super(MoskitoSpawnHandler, self).__init__()
        self.time_spent = 0
        self.time_limit = 600
        self.moskito_list = []

    def update(self):
        self.time_spent = self.time_spent + 4
        _tmp = 1
        if global_var.blood < 295:
            _tmp = 2
        if global_var.blood < 196:
            _tmp = 3
        if global_var.blood < 147:
            _tmp = 4
        if global_var.blood < 196 and is_heat_wave:
            _tmp = 2
        if global_var.blood < 147 and is_heat_wave:
            _tmp = 3
        if self.time_spent > self.time_limit:
            self.time_spent = 0
            for _ in range(0, random.randint(1, _tmp)):
                self.moskito_list.append(Moskito())
            self.time_limit = self.time_limit - (self.time_limit / 85)
        for msk in self.moskito_list:
            msk.update()


class Moskito(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        if random.randint(0, 10) > 7:
            _tmp = random.randint(80, 160)
        else:
            _tmp = random.randint(140, 160)
        self.image = pygame.transform.scale(img_moskito_list[random.randint(0, 3)], (_tmp, _tmp))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(1, 1280)
        self.rect.y = random.randint(1, 720)
        self.ai_task_list = {}
        self.velocity = [0, 0]
        self.isDestroyed = False
        if global_var.enable_sound:
            self.play_obj = NewMoskitoSound()
            self.play_obj.play(-1)

    def destroy(self):
        if not self.isDestroyed:
            self.isDestroyed = True
            global_var.moskitos_killed = global_var.moskitos_killed + 1
            global_var.renew_sound = True
            if using_controller:
                try:
                    joysticks[last_controller].rumble(1.0, 1.0, 10)
                except:
                    pass
            if global_var.enable_sound:
                try:
                    self.play_obj.stop()
                except Exception as e_:
                    nlib.log("Couldn't stop a moskito sound : %s" % str(e_), "warn")

    def shiver(self):  # = trembler
        a = random.randint(1, 4)
        if a == 1:
            self.rect.x = self.rect.x + 2
        elif a == 2:
            self.rect.x = self.rect.x - 2
        elif a == 3:
            self.rect.y = self.rect.y + 2
        elif a == 4:
            self.rect.y = self.rect.y - 2

    def manage_ai_task(self):
        if self.ai_task_list == {}:
            _tmp_a = 1
            if random.randint(0, 1) == 0:
                _tmp_a = -1
            _tmp_b = 1
            if random.randint(0, 1) == 0:
                _tmp_b = -1
            self.ai_task_list = {
                'movement': {'x': random.randint(0, 10) * _tmp_a * 4, 'y': random.randint(0, 10) * _tmp_b * 4,
                             'time': 0},
                'down_and_up': {'x': 0, 'y': 0, 'direction': 'up', 'time': 0}
            }
        self.velocity = [self.ai_task_list['movement']['x'], self.ai_task_list['movement']['y']]

    def manage_sound(self):
        pass
        # if self.should_renew_sound:
        #     try:
        #         if not self.play_obj.is_playing():
        #             try:
        #                 self.wave_obj.play()
        #             except:
        #                 nlib.log("Couldn't renew sound for a moskito !", "error")
        #                 self.should_renew_sound = False
        #     except:
        #         pass

    def limit_checker(self):
        if not self.ai_task_list == {}:  # Security measure to prevent eventual crash !!!
            changer = ''
            changer2 = ''
            if self.rect.x > 1150:
                self.rect.x = 1149
                changer = 'x'
            if self.rect.x < 0:
                self.rect.x = 1
                changer = 'x'
            if self.rect.y > 580:
                self.rect.y = 579
                changer2 = 'y'
            if self.rect.y < 0:
                self.rect.y = 1
                changer2 = 'y'
            if changer == 'x':
                self.ai_task_list['movement']['x'] = self.ai_task_list['movement']['x'] * -1
            if changer2 == 'y':
                self.ai_task_list['movement']['y'] = self.ai_task_list['movement']['y'] * -1

    def update(self):  # Moskito AI
        global FPS_COUNT
        global moskito_lamp_time
        if not self.isDestroyed:
            self.limit_checker()
            self.shiver()
            self.manage_ai_task()
            if moskito_lamp_time > 0:
                if FPS_COUNT == 3:
                    FPS_COUNT = 0
                    self.rect.move_ip(*self.velocity)
                else:
                    FPS_COUNT = FPS_COUNT + 1
            else:
                self.rect.move_ip(*self.velocity)
            global_var.blood = global_var.blood - 0.2
            screen.blit(self.image, self.rect)
            if global_var.enable_sound:
                self.manage_sound()


def stop_sounds():
    for moskit in moskito_spawn_handler.moskito_list:
        try:
            moskit.play_obj.stop()
        except Exception as ignored:
            if ignored:
                pass
            pass


def pass_to_menu():
    if global_var.enable_sound:
        main_sound_obj.play(-1)
        shop_music_obj.stop()
    global_var.click_delay = 338
    swatter.isClicking = False
    swatter.time_ani = 0
    swatter.size_w = swatter.base_size_w
    swatter.size_h = swatter.base_size_h
    global_var.isMenu = True
    pygame.mouse.set_visible(True)


def pass_to_playing():
    global is_heat_wave
    global_var.Playing = True
    pygame.mouse.set_visible(False)
    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
    is_heat_wave = False


class WaitBar(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.pix_image = img_pix_wait_bar
        self.image = img_wait_bar_1
        self.rect = self.image.get_rect()
        self.rect.x = 470
        self.rect.y = 10

    def update(self, time_=None):
        if global_var.click_delay > 336:
            global_var.click_delay = 338
            global_var.can_click = True
        if not global_var.can_click:
            # global_var.click_delay = global_var.click_delay + (global_var.click_rate / 2)
            global_var.click_delay = global_var.click_delay + 5  # (388 / time_ * 0.03)
        for _f in range(0, int(global_var.click_delay)):
            screen.blit(self.pix_image, (self.rect.x + 1 + _f, self.rect.y + 1))
        screen.blit(self.image, self.rect)


class BloodBar(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.pix_image = img_pix_blood_bar
        self.image = img_blood_bar
        self.rect = self.image.get_rect()
        self.rect.x = 1230
        self.rect.y = 100

    def update(self):
        for f_ in range(0, int(global_var.blood)):
            screen.blit(self.pix_image, (self.rect.x + 3, self.rect.y + 599 - f_))
        screen.blit(self.image, self.rect)
        screen.blit(CSM_26.render(str(round(global_var.blood / 100.0, 1))
                                                                               + "L", True, (210, 0, 0)), (1225, 50))
        if global_var.blood < 0:
            stop_sounds()
            global_var.Playing = False
            global_var.Final_Menu = True
            global_var.best_score = get_better_score()
            pygame.mouse.set_visible(True)
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)


def collision(sprite1, sprite2):
    """Used to check between 2 pygame sprites rects if they collide
    Usage : if collision(sprite1.rect, sprite2.rect): [...]"""
    if sprite2.right * 10 < sprite1.left:
        return False
    if sprite2.bottom * 10 < sprite1.top:
        return False
    if sprite2.left * 10 > sprite1.right:
        return False
    if sprite2.top * 10 > sprite1.bottom:
        return False
    return True


class Swatter(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        if settings_list[4] == 0:
            self.image = img_swatter_1
            self.base_image = self.image
            self.rect = self.image.get_rect()
            self.base_size_w = 90
            self.base_size_h = 602
            self.size_w = self.base_size_w
            self.size_h = self.base_size_h
            self.moskito_kill_radius = (90, 105)
        elif settings_list[4] == 1:
            self.image = swatter_pro
            self.base_image = self.image
            self.rect = self.image.get_rect()
            self.base_size_w = 108
            self.base_size_h = 718
            self.size_w = self.base_size_w
            self.size_h = self.base_size_h
            self.moskito_kill_radius = (108, 126)
        elif settings_list[4] == 2:
            self.image = bzio_ruler_in_game
            self.base_image = self.image
            self.rect = self.image.get_rect()
            self.base_size_w = 72
            self.base_size_h = 540
            self.size_w = self.base_size_w
            self.size_h = self.base_size_h
            self.moskito_kill_radius = (72, 200)
        mouse2 = pygame.mouse.get_pos()
        self.rect.x = mouse2[0]
        self.rect.y = mouse2[1]
        self.isClicking = False
        self.time_ani = 0

    def destroy_nearby_moskitos(self):
        self.rect.width = self.moskito_kill_radius[0]
        self.rect.height = self.moskito_kill_radius[1]
        for i in range(0, len(moskito_spawn_handler.moskito_list)):
            a = pygame.sprite.GroupSingle(moskito_spawn_handler.moskito_list[i])
            if pygame.sprite.spritecollide(self, a, False):
                moskito_spawn_handler.moskito_list[i].destroy()
            a.remove(moskito_spawn_handler.moskito_list[i])

    def update_rect(self):
        self.rect = self.image.get_rect()

    def update(self):
        if not using_controller:
            x_, y = pygame.mouse.get_pos()
        else:
            x_, y = (int((((joysticks[last_controller].get_axis(joystick_id0)*joy_multiplier[0]) + 1.0)/2.0) * 1280.0),
                     int((((joysticks[last_controller].get_axis(joystick_id1)*joy_multiplier[1]) + 1.0) / 2.0) * 720.0))
        if self.isClicking:
            self.time_ani = self.time_ani + 4
            if self.time_ani < 50:
                self.size_w = self.size_w - 4
                self.size_h = self.size_h - 12
                self.image = pygame.transform.scale(self.base_image, (self.size_w, self.size_h))
                self.update_rect()
            elif self.time_ani < 100:
                self.size_w = self.size_w + 4
                self.size_h = self.size_h + 12
                self.image = pygame.transform.scale(self.base_image, (self.size_w, self.size_h))
                self.update_rect()
            else:
                self.isClicking = False
                self.time_ani = 0
                self.size_w = self.base_size_w
                self.size_h = self.base_size_h
        screen.blit(self.image, (x_ - (self.rect.width / 2), y - (self.rect.height / 2)))
        self.update_rect()
        self.rect.x = x_
        self.rect.y = y
        if 30 < self.time_ani < 70:
            self.destroy_nearby_moskitos()

    def when_clicked(self):
        if (not self.isClicking) and global_var.can_click:
            self.isClicking = True
            global_var.click_delay = 0
            global_var.can_click = False


class Button(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.env = "Menu"
        self.image = img_btn_normal
        self.rect = self.image.get_rect()  # Get Shape from image
        self.velocity = [0, 0]
        self.rect.x = int(window_x / 2.5)
        self.rect.y = int(window_y / 2)
        self.isHovered = False
        self.isClicked = False
        self.maxX = 728
        self.minX = 512
        self.minY = 362
        self.maxY = 417
        self.type = 'play'
        global_var.btn_hover_list.append(self)

    def update(self):
        if self.maxX > mouse[0] > self.minX and self.minY < mouse[1] < self.maxY:
            self.isHovered = True
        else:
            self.isHovered = False
        if self.isHovered:
            if not opaque >= 0:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        if self.isClicked:
            if self.type == 'play' and global_var.isMenu:
                global_var.moskitos_killed = 0
                moskito_spawn_handler.moskito_list = []
                global_var.blood = BLOOD
                global_var.isMenu = False
                self.isClicked = False
                pass_to_playing()
                global_var.isMenu = False
            elif self.type == 'settings':
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_WAIT)
                show_popup()
                open_settings(global_var, default_lang, settings_list, VERSION_STRING, lang_list, VERSION_NUM)
                self.isClicked = False
                if global_var.change_fullscreen:
                    global_var.change_fullscreen = False
                    pygame.display.toggle_fullscreen()
        if self.type == 'play':
            if using_controller:
                if button_pressed:
                    self.isClicked = True
            if self.isHovered:
                screen.blit(img_btn_hovered, (int(window_x / 2.5), int(window_y / 2)))
            else:
                screen.blit(img_btn_normal, (int(window_x / 2.5), int(window_y / 2)))
            screen.blit(play_btn_text, (int(window_x / 2.2), int(window_y / 1.97)))
        elif self.type == 'settings':
            if self.isHovered:
                screen.blit(img_btn_hovered, (int(window_x / 2.5), int(window_y / 1.65)))
            else:
                screen.blit(img_btn_normal, (int(window_x / 2.5), int(window_y / 1.65)))
            screen.blit(settings_btn_text, (int(window_x / 2.35), int(window_y / 1.637)))


def show_shop_btn_image(btn_type):
    if btn_type == "shop_btn_blood_2":
        screen.blit(shop_blood_bag, (376, 262))
    elif btn_type == "shop_btn_blood_3":
        screen.blit(shop_blood_bottle, (366, 336))
    elif btn_type == "shop_btn_blood_4":
        screen.blit(shop_blood_barrel, (350, 435))
    elif btn_type == "shop_btn_blood_5":
        screen.blit(shop_blood_infusion, (256, 525))
    elif btn_type == "shop_btn_swatter":
        screen.blit(shop_swatter_pro, (757, 173))
    elif btn_type == "shop_btn_bzio":
        screen.blit(shop_bzio_ruler, (655, 524))
    elif btn_type == "shop_btn_heat_wave":
        screen.blit(shop_heat_wave, (1150, 313))
    elif btn_type == "shop_btn_spray":
        screen.blit(shop_spray, (1135, 408))
    elif btn_type == "shop_btn_lamp":
        screen.blit(shop_lamp, (1112, 526))


def buy_item(btn_type):
    global continuer
    global is_dialog
    if is_dialog == 0:
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_WAIT)
        article_name = ""  # Ensure var is defined
        cost = 0
        item_id = 0
        conf_buy = True
        if btn_type == "shop_btn_blood_2":
            cost = 100
            article_name = default_lang[18]
            item_id = 0
        elif btn_type == "shop_btn_blood_3":
            cost = 150
            article_name = default_lang[19]
            item_id = 1
        elif btn_type == "shop_btn_blood_4":
            cost = 300
            article_name = default_lang[20]
            item_id = 2
        elif btn_type == "shop_btn_blood_5":
            cost = 800
            article_name = default_lang[21]
            item_id = 3
        elif btn_type == "shop_btn_swatter":
            cost = 1000
            article_name = default_lang[22]
            item_id = 4
        elif btn_type == "shop_btn_bzio":
            cost = 5000
            article_name = default_lang[23]
            item_id = 5
        elif btn_type == "shop_btn_heat_wave":
            cost = 500
            article_name = default_lang[24]
            item_id = 6
        elif btn_type == "shop_btn_spray":
            cost = 500
            article_name = default_lang[25]
            item_id = 7
        elif btn_type == "shop_btn_lamp":
            cost = 750
            article_name = default_lang[26]
            item_id = 8
        if item_id == 4:
            conf_buy = False
            if get_inventory()[1] == 0:
                conf_buy = True
            elif get_inventory()[1] > 0:
                is_dialog = 20
                continuer = d.show(screen, segoeui, CSM_40, default_lang, default_lang[27], default_lang[28], img_error)
        elif item_id == 5:
            conf_buy = False
            if get_inventory()[1] == 0:
                is_dialog = 20
                continuer = d.show(screen, segoeui, CSM_40, default_lang, default_lang[27], default_lang[29], img_error)
            elif get_inventory()[1] == 1:
                conf_buy = True
            else:
                is_dialog = 20
                continuer = d.show(screen, segoeui, CSM_40, default_lang, default_lang[27], default_lang[28], img_error)

        if conf_buy:
            is_dialog = 30
            continuer, _ret = d.askyesno(screen, CSM_40, default_lang, default_lang[30], default_lang[31]
                                         .format(article_name), img_question)
            if _ret:
                if get_bziocoins() >= cost:
                    save_bziocoins(get_bziocoins() - cost)
                    if not (item_id == 4 or item_id == 5):
                        _inv = get_inventory()
                        _inv[0].append(item_id)
                        save_inventory(_inv[0], _inv[1])
                    else:
                        _inv = get_inventory()
                        if item_id == 4:
                            _inv[1] = 1
                        else:
                            _inv[1] = 2
                        save_inventory(_inv[0], _inv[1])
                    is_dialog = 20
                    continuer = d.show(screen, segoeui, CSM_40, default_lang, default_lang[32], default_lang[33],
                                       img_info)
                else:
                    is_dialog = 20
                    continuer = d.show(screen, segoeui, CSM_40, default_lang, default_lang[34], default_lang[35],
                                       img_error)
        global_var.bziocoins = get_bziocoins()
        global_var.inventory = get_inventory()[0]


class NewButton(pygame.sprite.Sprite):
    def __init__(self, pos_min, pos_max, text, btn_type, env="Menu", font_size=30):
        super().__init__()
        self.btn_type = btn_type
        self.isHovered = False
        self.env = env
        if not self.btn_type == "shop_close":
            self.text_image = ptext.getsurf(text, color=(153, 153, 0), fontname="ComicSansMSM.ttf",
                                            fontsize=font_size)
        else:
            self.text_image = segoeui.render(text, True, (153, 153, 0))
        self.text_image_rect = self.text_image.get_bounding_rect()
        self.text_image = self.text_image.convert_alpha()
        # self.text_image_rect.center = ((pos_max[0] - pos_min[0]) / 2, (pos_max[1] - pos_min[1]) / 2)
        self.pos_min = pos_min
        self.pos_max = pos_max
        self.image = pygame.Surface((pos_max[0] - pos_min[0], pos_max[1] - pos_min[1]))
        self.rect = self.image.get_rect()
        pygame.gfxdraw.rectangle(self.image, self.rect, (206, 237, 31))
        pygame.gfxdraw.rectangle(self.image, pygame.rect.Rect(1, 1, pos_max[0] - pos_min[0] - 2, pos_max[1] - pos_min[1]
                                                              - 2), (206, 237, 31))
        pygame.gfxdraw.rectangle(self.image, pygame.rect.Rect(2, 2, pos_max[0] - pos_min[0] - 4, pos_max[1] - pos_min[1]
                                                              - 4), (206, 237, 31))
        pygame.gfxdraw.box(self.image, pygame.rect.Rect(3, 3, pos_max[0] - pos_min[0] - 6, pos_max[1] - pos_min[1]
                                                        - 6), (235, 248, 165))
        self.hover_image = pygame.Surface((pos_max[0] - pos_min[0], pos_max[1] - pos_min[1]))
        self.hover_image.blit(self.image, (0, 0, 0, 0))
        pygame.gfxdraw.box(self.hover_image, pygame.rect.Rect(3, 3, pos_max[0] - pos_min[0] - 6, pos_max[1] - pos_min[1]
                                                              - 6), (220, 242, 96))
        global_var.btn_hover_list.append(self)
        global_var.btn_click_list.append(self)

    def custom_action(self):
        if self.btn_type == "shop":
            global_var.isMenu = False
            global_var.shop = True
            if global_var.enable_sound:
                shop_music_obj.play(-1)
        elif self.btn_type == "shop_close":
            if global_var.shop:
                pass_to_menu()
                global_var.shop = False
        elif self.btn_type == "return_to_menu":
            pass_to_menu()
            global_var.playing = False
            global_var.Final_Menu = False
            global_var.Final_verdict = False
            moskito_spawn_handler.moskito_list = []
            global_var.blood = BLOOD
            global_var.moskitos_killed = 0
            moskito_spawn_handler.time_spent = 0
            moskito_spawn_handler.time_limit = 600
            global_var.chrono = 0
            global_var.latest_chrono = 0
        elif self.btn_type == "shop_btn_blood_2" or self.btn_type == "shop_btn_blood_3" or self.btn_type == \
                "shop_btn_blood_4" or self.btn_type == "shop_btn_blood_5" or self.btn_type == "shop_btn_swatter" \
                or self.btn_type == "shop_btn_bzio" or self.btn_type == "shop_btn_heat_wave" or self.btn_type == \
                "shop_btn_spray" or self.btn_type == "shop_btn_lamp":
            buy_item(self.btn_type)
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    def update(self):
        mouse_ = pygame.mouse.get_pos()
        if self.pos_max[0] > mouse_[0] > self.pos_min[0] and self.pos_min[1] < mouse_[1] < self.pos_max[1]:
            self.isHovered = True
            screen.blit(self.hover_image, self.pos_min)
            if not opaque >= 0:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            self.isHovered = False
            screen.blit(self.image, self.pos_min)
        if using_controller and button_pressed:
            if self.btn_type == "return_to_menu":
                self.custom_action()
        show_shop_btn_image(self.btn_type)
        screen.blit(self.text_image, (
            (self.pos_max[0] - self.pos_min[0]) / 2 + self.pos_min[0] - self.text_image_rect.centerx,
            (self.pos_max[1] - self.pos_min[1]) / 2 + self.pos_min[1] - self.text_image_rect.centery))


shop_btn = NewButton((512, 510), (728, 566), default_lang[10], "shop")
close_shop_btn = NewButton((1158, 37), (1223, 79), u"\u00D7", "shop_close", "Shop")
shop_btn_l = [NewButton((87, 116), (432, 212), default_lang[36], "", "Shop"),
              NewButton((87, 222), (432, 318), default_lang[37], "shop_btn_blood_2", "Shop"),
              NewButton((87, 328), (432, 424), default_lang[38], "shop_btn_blood_3", "Shop"),
              NewButton((87, 434), (432, 530), default_lang[39], "shop_btn_blood_4", "Shop"),
              NewButton((87, 540), (432, 636), default_lang[40], "shop_btn_blood_5", "Shop", 23),
              NewButton((462, 116), (807, 270), default_lang[41], "", "Shop"),
              NewButton((462, 300), (807, 454), default_lang[42], "shop_btn_swatter", "Shop"),
              NewButton((462, 484), (807, 636), default_lang[43], "shop_btn_bzio", "Shop"),
              NewButton((837, 116), (1182, 231), default_lang[44], "", "Shop"),
              NewButton((837, 251), (1182, 367), default_lang[45], "shop_btn_heat_wave", "Shop", 25),
              NewButton((837, 387), (1182, 502), default_lang[46], "shop_btn_spray", "Shop", 25),
              NewButton((837, 522), (1182, 636), default_lang[47], "shop_btn_lamp", "Shop", 21)]

return_to_menu_btn = NewButton((490, 618), (790, 688), default_lang[17], "return_to_menu", "Final_Menu")


class PauseButton(pygame.sprite.Sprite):
    def __init__(self, image: pygame.Surface, xy, _id: int):
        super(PauseButton, self).__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.bigger_image = pygame.transform.scale(image, (self.rect.width + 10, self.rect.height + 10))
        self.bigger_image_rect = self.bigger_image.get_rect()
        self.rect.x, self.rect.y = xy
        self.bigger_image_rect.x, self.bigger_image_rect.y = self.rect.x - 5, self.rect.y - 5
        self.id = _id
        pause_btn_list.append(self)

    def on_click(self):
        global blood_infusion
        global blood_infusion_total
        global blood_factor
        global anti_moskito_spray
        global moskito_lamp_time
        global is_heat_wave
        global FPS
        global swatter
        global continuer
        global is_dialog
        allowed = True
        if allowed:
            pass
        if is_dialog == 0:
            if self.id != 9 and self.id != 4 and self.id != 5:
                if self.id in get_inventory()[0]:  # check if item is present in inventory
                    is_dialog = 60
                    continuer, allowed = d.askyesno(screen, CSM_40, default_lang, default_lang[48], default_lang[49],
                                                    img_question)
                else:  # or deny use !
                    is_dialog = 20
                    continuer = d.show(screen, segoeui, CSM_40, default_lang, default_lang[50], default_lang[51],
                                       img_error)
                    allowed = False
            else:
                allowed = False
                if self.id == 9 or (self.id == 4 and get_inventory()[1] > 0) or (self.id == 5 and get_inventory()[1]
                                                                                 > 1):
                    is_dialog = 20
                    continuer = d.show(screen, segoeui, CSM_40, default_lang, default_lang[32], default_lang[52],
                                       img_info)
                    if self.id == 9:
                        settings_list[4] = 0
                    elif self.id == 4:
                        settings_list[4] = 1
                    elif self.id == 5:
                        settings_list[4] = 2
                    nlib.save(settings_list, "settings.ini")
                    swatter = Swatter()
                else:
                    is_dialog = 20
                    continuer = d.show(screen, segoeui, CSM_40, default_lang, default_lang[50], default_lang[53],
                                       img_error)
            if allowed:
                _inv = get_inventory()
                _inv[0] = remove_item_from_inventory(_inv[0], self.id)
                save_inventory(_inv[0], _inv[1])
                global_var.inventory = _inv[0]
                if self.id == 0:
                    global_var.blood += 75
                elif self.id == 1:
                    global_var.blood += 150
                elif self.id == 2:
                    global_var.blood += 400
                elif self.id == 3:
                    blood_infusion = 1800  # time
                    blood_infusion_total = 1800
                    blood_factor = 0.417
                elif self.id == 6:
                    is_heat_wave = True
                elif self.id == 7:
                    anti_moskito_spray = 180
                elif self.id == 8:
                    moskito_lamp_time = 1800
                if global_var.blood > BLOOD:
                    global_var.blood = BLOOD

    def update(self):
        global is_dialog
        count = operator.countOf(global_var.inventory, self.id)
        _x, _y = pygame.mouse.get_pos()
        base_x = self.rect.x
        x_penal = 0
        if self.id == 2:
            base_x = 390
            x_penal = 40
        elif self.id == 5:
            base_x = 998
            x_penal = 92
        if base_x < _x < base_x + self.rect.width - x_penal and self.rect.y < _y < self.rect.y + self.rect.height:
            screen.blit(self.bigger_image, self.bigger_image_rect)
            if pygame.mouse.get_pressed()[0]:
                if is_dialog == 0:
                    self.on_click()
        else:
            screen.blit(self.image, self.rect)
        if count != 0:
            _x_decal, _y_decal = (5, 5)
            if self.id == 1:
                _x_decal, _y_decal = (15, 15)
            screen.blit(CSM_30.render(str(count), True, (0, 0, 0)), (
                self.rect.x + self.rect.width - _x_decal, self.rect.y + self.rect.height - _y_decal))


PauseButton(shop_blood_bag, (208, 570), 0)
PauseButton(shop_blood_bottle, (288, 550), 1)
PauseButton(shop_blood_barrel, (368, 548), 2)
PauseButton(shop_blood_infusion, (453, 546), 3)
PauseButton(shop_heat_wave, (630, 580), 6)
PauseButton(shop_spray, (684, 546), 7)
PauseButton(shop_lamp, (752, 542), 8)
PauseButton(pause_swatter_1, (855, 395), 9)
PauseButton(shop_swatter_pro, (926, 395), 4)
PauseButton(pause_bzio_ruler, (949, 533), 5)


def manage_buttons():
    global shop_hovered_id
    _tmp = False
    if global_var.isMenu:
        current_env = "Menu"
    elif global_var.Playing:
        current_env = "Playing"
    elif global_var.shop:
        current_env = "Shop"
    elif global_var.Final_Menu:
        current_env = "Final_Menu"
    else:
        current_env = ""
    shop_hovered_id = -1
    for el_ in global_var.btn_hover_list:
        if el_.isHovered and el_.env == current_env:
            _tmp = True
            if current_env == "Shop":
                if el_.btn_type in shop_btn_ids:
                    shop_hovered_id = shop_btn_ids[el_.btn_type]
    if _tmp:
        if not opaque >= 0:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
    else:
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)


def get_final_score():
    return int((global_var.moskitos_killed * 1.5) * (global_var.latest_chrono * 0.0001))


# stars
# star_list = []
# for x in range(0, 1000):
#     star_list.append(Star())
moskito_spawn_handler = MoskitoSpawnHandler()
blood_bar = BloodBar()
swatter = Swatter()
play_btn = Button()
wait_bar = WaitBar()
settings_btn = Button()
settings_btn.maxX = 728
settings_btn.maxY = 492
settings_btn.minX = 512
settings_btn.minY = 436
settings_btn.type = 'settings'

font_shop = CSM_40.render(default_lang[10], True, (153, 153, 0))
font_rect = font_shop.get_rect()
font_rect.center = (window_x / 2, 50)


def show_popup():
    screen.blit(dark_img, (0, 0, 1280, 720))
    screen.blit(CSM_40.render("A dialog box is opened", True, (153, 153, 0)), (0, 0, 100, 100))


def calculate_distance(coord1, coord2, is_pygame_rect=True):
    if is_pygame_rect:
        return int(math.sqrt((coord2.centerx - coord1.centerx) ** 2 + (coord2.centery - coord1.centerx) ** 2))
    else:
        return int(math.sqrt((coord2[0] - coord1[0]) ** 2 + (coord2[1] - coord1[1]) ** 2))


# star = Star()
# player = Player()
# Window definition
continuer = True
playBtnIsClicked = False
while continuer:
    if is_dialog > 0:
        is_dialog = is_dialog - 1
    button_pressed = False
    clock.tick(FPS)
    t = clock.get_time()
    if global_var.isMenu:
        global_var.Playing = False
    else:
        main_sound_obj.stop()

    if global_var.Playing:
        global_var.isMenu = False

    mouse = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            continuer = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_c:
                if global_var.shop:
                    continuer, ret = d.askstring(screen, segoeui, CSM_40, default_lang, default_lang[81],
                                                 default_lang[81], img_ask_string)
                    if not isfile(os.path.join(pathlib.Path.home(), "nm_code.raw")):
                        with open(os.path.join(pathlib.Path.home(), "nm_code.raw"), "wb") as fil:
                            pickle.dump([], fil)
                            fil.close()  # create the file if it does not exist
                    with open(os.path.join(pathlib.Path.home(), "nm_code.raw"), "rb") as _fil:
                        code_pick = pickle.load(_fil)
                    fnd = False
                    for each in code_pick:
                        if each == ret:
                            fnd = True
                    if fnd:
                        is_dialog = 20
                        continuer = d.show(screen, segoeui, CSM_40, default_lang, default_lang[82], default_lang[82],
                                           img_error)
                    else:
                        try:
                            codes: dict = nlib.get_json_from_url("https://raw.githubusercontent.com/SiniKraft/"
                                                                 "NoMoskito/master/codes.json")
                            if codes.get(ret) is not None:
                                # code found
                                with open(os.path.join(pathlib.Path.home(), "nm_code.raw"), "wb") as fil:
                                    code_pick.append(ret)
                                    pickle.dump(code_pick, fil)
                                global_var.bziocoins = global_var.bziocoins + codes[ret]["BZIOC"]
                                save_bziocoins(global_var.bziocoins)
                                for x in range(0, 10):
                                    if str(x) in list(codes[ret].keys()):
                                        _inv = get_inventory()
                                        for i in range(0, int(codes[ret][str(x)])):
                                            _inv[0].append(x)
                                        save_inventory(_inv[0], _inv[1])
                                        global_var.inventory = _inv[0]
                            else:
                                is_dialog = 20
                                continuer = d.show(screen, segoeui, CSM_40, default_lang, default_lang[83],
                                                   default_lang[83], img_error)
                        except Exception as _e_:
                            is_dialog = 20
                            continuer = d.show(screen, segoeui, CSM_40, default_lang, default_lang[83],
                                               default_lang[83] + "\n" + str(_e_), img_error)
            if event.key == pygame.K_SPACE:
                if global_var.IsGamePaused:
                    global_var.IsGamePaused = False
                    global_var.Playing = False
                    pass_to_menu()
            if event.key == pygame.K_F11:
                settings_list[3] = not settings_list[3]
                nlib.save(settings_list, "settings.ini")
                pygame.display.toggle_fullscreen()
            if event.key == pygame.K_ESCAPE:
                if global_var.Playing:
                    if global_var.IsGamePaused:
                        try:
                            for moskito in moskito_spawn_handler.moskito_list:
                                if not moskito.isDestroyed:
                                    moskito.play_obj.play(-1)
                        except Exception as e:
                            nlib.log(str(e), "warn")
                        pygame.mouse.set_pos(global_var.last_mouse)
                        time.sleep(0.03)
                        global_var.IsGamePaused = False
                        pygame.mouse.set_pos(global_var.last_mouse)
                        pygame.mouse.set_visible(False)
                        if anti_moskito_spray == 180:
                            spray_sound_obj.play(0)
                    elif not global_var.IsGamePaused:
                        try:
                            for moskito in moskito_spawn_handler.moskito_list:
                                moskito.play_obj.stop()
                        except Exception as e:
                            nlib.log(str(e), "warn")
                        global_var.last_mouse = pygame.mouse.get_pos()
                        global_var.IsGamePaused = True
                        pygame.mouse.set_visible(True)
                        inv = get_inventory()[0]
                        inv_counts = list(map(lambda letter: {letter: inv.count(letter)}, set(inv)))
                        inv_counts = dict(j for i in inv_counts for j in i.items())
                        pause_bg = screen.copy()
                        # Provide inv_counts a dict containing number of items with this form : {0: 4, 8: 3, ...}
                else:
                    continuer = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            using_controller = False
            if debug_mouse:
                mx, my = pygame.mouse.get_pos()
                nlib.log("Mouse x: %s y: %s" % (mx, my), "debug")
            if global_var.Playing:
                swatter.when_clicked()
            #            dx, dy = mx - player.rect.center_x, my - player.rect.center_y
            #            angle = math.degrees(math.atan2(-dy, dx))
            #            print("Angle : " + str(90 - int(angle)))
            if 728 > mouse[0] > 512 and 362 < mouse[1] < 417 and global_var.isMenu:  # check if btn is clicked.
                play_btn.isClicked = True
            if 728 > mouse[0] > 512 and 436 < mouse[1] < 492 and global_var.isMenu:
                settings_btn.isClicked = True

            for btn in global_var.btn_click_list:
                # if btn.pos_max[0] > mouse[0] > btn.pos_min[0] and btn.pos_min[1] < mouse[1] < btn.pos_max[1]:
                if btn.isHovered:
                    btn.custom_action()
                    btn.isHovered = False  # Remove a large bug !
        if event.type == pygame.JOYBUTTONDOWN:
            using_controller = True
            button_pressed = True
            last_controller = event.joy
            if global_var.Playing:
                swatter.when_clicked()
        if event.type == pygame.JOYAXISMOTION:
            using_controller = True
            last_controller = event.joy
        if event.type == pygame.MOUSEMOTION:
            using_controller = False

            # mx, my = pygame.mouse.get_pos()  # Rotation system
    #    dx, dy = mx - player.rect.center_x, my - player.rect.center_y
    #    angle = math.degrees(math.atan2(-dy, dx)) - correction_angle
    #    angle2 = math.degrees(math.atan2(-dy, dx))
    #    rot_image = pygame.transform.rotate(player.image, angle)
    #    rot_image_rect = rot_image.get_rect(center=player.rect.center)
    if not global_var.Playing and not global_var.chrono == 0:
        global_var.latest_chrono = global_var.chrono
        global_var.chrono = 0
    if not global_var.IsGamePaused:
        screen.blit(img_background, (0, 0))
    if global_var.isMenu:
        manage_buttons()
        shop_btn.update()
        # When it's menu
        play_btn.update()
        settings_btn.update()
        # if not play_btn.isHovered and not settings_btn.isHovered:
        #     pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        screen.blit(img_logo, (int(window_x / 5.2), int(window_y / 6)))  # logo
        if should_show_popup:
            if opaque == -1:
                continuer = d.trailer(screen, segoeui, CSM_40)
                should_show_popup = False

    elif global_var.Playing:
        if not global_var.IsGamePaused:
            if blood_infusion != 0:
                blood_infusion = blood_infusion - 1
                global_var.blood = global_var.blood + blood_factor
                if global_var.blood > BLOOD:
                    global_var.blood = BLOOD
                screen.blit(CSM_30.render(
                    "%s%%" % str(int(blood_infusion / blood_infusion_total * 100)), True, (255, 0, 0)), (1200, 0))
            if moskito_lamp_time > 0:
                moskito_lamp_time = moskito_lamp_time - 1
                screen.blit(shop_lamp, (10, 10))
                screen.blit(CSM_25.render(
                    "%ss" % str(int(moskito_lamp_time / 60)), True, (0, 0, 0)), (25, 45))
            if is_heat_wave:
                screen.blit(shop_heat_wave, (15, 658))
            moskito_spawn_handler.update()
            swatter.update()
            wait_bar.update()
            blood_bar.update()
            screen.blit(CSM_30.render(default_lang[54], True, (0, 0, 0)),
                        (850, 0))
            global_var.chrono = global_var.chrono + t
            if anti_moskito_spray > 0:
                anti_moskito_spray -= 1
                for moskito in moskito_spawn_handler.moskito_list:
                    moskito.destroy()
        else:  # it's pause
            screen.blit(pause_bg, (0, 0))
            _tmp_font = ptext.getsurf(default_lang[55], color=(153, 153, 0), fontname="ComicSansMSM.ttf", fontsize=45)
            _tmp_rect = _tmp_font.get_rect()
            screen.blit(_tmp_font, ((window_x / 2 - _tmp_rect.centerx), (window_y / 2 - _tmp_rect.centery)))
            for el in pause_btn_list:
                el.update()

    elif global_var.Final_Menu:
        screen.blit(font_a_text, (
            int(window_x / 2) - font_a_text.get_rect().centerx, int(window_y / 3) - font_a_text.get_rect().centery))
        _font = CSM_45 \
            .render(default_lang[12].format(get_final_score()), True, (153, 153, 0))
        _font_2 = CSM_45 \
            .render(default_lang[13].format(global_var.best_score[0], global_var.best_score[1]),
                    True, (153, 153, 0))
        _font_3 = CSM_45 \
            .render(default_lang[56].format(int(get_final_score() * 0.75)),
                    True, (153, 153, 0))
        screen.blit(_font, (
            int(window_x / 2) - _font.get_rect().centerx,
            int(window_y / 2) - _font.get_rect().centery))
        screen.blit(_font_2, (
            int(window_x / 2) - _font_2.get_rect().centerx,
            int(window_y / 1.6) - _font_2.get_rect().centery))
        screen.blit(_font_3, (
            int(window_x / 2) - _font_2.get_rect().centerx,
            int(window_y / 1.3) - _font_2.get_rect().centery))
        if not global_var.Final_verdict:
            global_var.bziocoins = get_bziocoins()
            global_var.Final_verdict = True
            is_heat_wave = False
            if get_final_score() > get_better_score()[0]:
                continuer, _ns = d.askstring(screen, segoeui, CSM_40, default_lang, default_lang[14], default_lang[15],
                                             img_ask_string)
                overwrite_better_score(get_final_score(), str(_ns), global_var.bziocoins)
            global_var.bziocoins = global_var.bziocoins + int(get_final_score() * 0.75)
            save_bziocoins(global_var.bziocoins)
        return_to_menu_btn.update()
        manage_buttons()
    elif global_var.shop:
        manage_buttons()
        screen.blit(shop_bg, pygame.rect.Rect(50, 30, 1180, 660))
        screen.blit(font_shop, font_rect)
        font_shop_2 = CSM_40.render("{0} \u20BF".format(
            global_var.bziocoins), True, (153, 153, 0))
        screen.blit(CSM_25.render(default_lang[80], True, (153, 153, 0)), (10, 685))
        font_rect_2 = font_shop_2.get_rect()
        font_rect_2.center = (window_x / 1.3, 50)
        screen.blit(font_shop_2, font_rect_2)
        if shop_hovered_id != -1:
            font_hover_2 = CSM_40.render(default_lang[57].format(operator.countOf(
                global_var.inventory, shop_hovered_id)), True, (153, 153, 0))
            screen.blit(font_hover_2, (65, 25))
        close_shop_btn.update()
        for element in shop_btn_l:
            element.update()
        # mx, my = pygame.mouse.get_pos()
    #            dx, dy = mx - player.rect.center_x, my - player.rect.center_y
    #            angle = math.degrees(math.atan2(-dy, dx))
    # for x in range(0, 1000):
    # star_list[x].update(angle)
    # screen.blit(star_list[x].image, star_list[x].rect)
    # screen.blit(rot_image, rot_image_rect.top_left)  # spaceship
    if opaque >= 0:
        if opaque < 256:
            init_img.set_alpha(opaque)
        screen.blit(init_img, (0, 0))
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        opaque = opaque - 6
        if opaque < 0:
            if global_var.enable_sound:
                main_sound_obj.play(-1)
    pygame.display.update()
pygame.quit()
if isfile(RESOURCE_PAK_PATH):
    pak.close()
stop_sounds()
nlib.log("Game stopped !", "info")
sys.exit(0)  # useful when converting to .exe : make process stop instead of running forever in background !
