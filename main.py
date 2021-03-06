import os
import tkinter.messagebox

import nathlib as nlib
import sys
import time

version_name = "snapshot_014"  # DO NOT FORGET TO CHANGE FILEMANAGER CONSTANTS !!!
version_number = 1
debug_mouse = False

try:
    os.remove('latest.log')
except Exception as e:
    nlib.log("Couldn't remove latest.log : {}".format(str(e)), "warn")
nlib.start_logs("latest.log")
nlib.log("Launching game version {0} ...".format(version_name), "info")


def exception_handler(type, value, traceback):
    nlib.log("{0}: {1}".format(repr(value).split("(")[0], value), "critical", 'main')
    from tkinter import Tk, messagebox
    root = Tk()
    root.withdraw()
    messagebox.showerror("An error occurred", "{}: {}".format(repr(value).split("(")[0], value))
    root.destroy()
    sys.exit()


enable_exception_handler = False
if enable_exception_handler:
    sys.excepthook = exception_handler
enable_hash_checking = False  # Should only be enabled when released !!!

if enable_hash_checking:
    import hashlib

    hashes = [["LICENSE", "d5dc6d638156797c63fffd4bc908a3ec380e37d051996284736c6222438f3c9a"],
              ["nathlib.py", "e85f2234f4a8907d56f73a984a39b6fbcb8aa54e5bc82b62f11ad684eed83fa3"],
              ["README.MD", "70c728ac19b13ff9a343743ee5cf821d8dfea5d253201efbabbfc284d3951702"],
              ["settings_window.py", "17ca489a5fea4fe8243f6c6a4eaeaae8a004e9e10c0516bb4889688d7f02ecf2"],
              ["scripts/util/FileManager.py", "1c2c2e18c473429a0d3c1ee607adc1055eed3efe64bb5b1776b0eaff9acae0a3"],
              ["scripts/util/default/lang/en_US.py", "e32c190196fcbb4e55d07e5bc99d9f665fd9b7f9bf1dd98d72ffd04f2d0481c1"]
        ,
              ["scripts/util/default/lang/fr_FR.py", "b105710bdec2b292ebb3b8fa8782601c3786c1f3b9cb4a9d9410926d2dce280c"]
              ]

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
import tkinter as tk
from tkinter import simpledialog
import pygame.gfxdraw  # necessary as pygame doesn't load it by default !
from settings_window import open_settings
import ptext

# except ImportError:
# print("[ERROR]: Failed to import modules !")
# from sys import exit

# exit()

try:
    from scripts.util.FileManager import *

    for x in range(0, lang_number):
        exec("from scripts.util.FileManager import " + lang_files_to_load[x])
except:
    nlib.log("Failed to load resources, aborting ...", "critical")
    sys.exit()

# Initialisation de Pygame

pygame.init()
pygame.font.init()
if settings_list[2]:
    pygame.mixer.init()  # Sons de pygame.

# Definition de la fen??tre

window_x = 1280
window_y = 720
if not settings_list[3]:
    screen = pygame.display.set_mode((window_x, window_y))
else:
    screen = pygame.display.set_mode((window_x, window_y), pygame.FULLSCREEN)
pygame.display.set_caption("NoMoskito!")
pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
clock = pygame.time.Clock()
FPS = 60

# ressources ?? charger
shop_blood_bag = pygame.image.load("resources/blood_bag.png").convert_alpha()
shop_blood_bag = pygame.transform.scale(shop_blood_bag, (50, 50))
shop_blood_bottle = pygame.image.load("resources/blood_bottle.png").convert_alpha()
shop_blood_bottle = pygame.transform.scale(shop_blood_bottle, (80, 80))
shop_blood_barrel = pygame.image.load("resources/barrel_blood.png").convert_alpha()
shop_blood_barrel = pygame.transform.scale(shop_blood_barrel, (96, 96))
shop_blood_infusion = pygame.image.load("resources/blood_infusion.png").convert_alpha()
shop_blood_infusion = pygame.transform.scale(shop_blood_infusion, (176, 117))
swatter_pro = pygame.image.load("resources/swatter_pro.png").convert_alpha()
shop_swatter_pro = pygame.transform.scale(swatter_pro, (41, 275))
bzio_ruler = pygame.image.load("resources/imposant_ruler.png").convert_alpha()
shop_bzio_ruler = pygame.transform.scale(bzio_ruler, (128, 128))
img_heat_wave = pygame.image.load("resources/hot.png").convert_alpha()
shop_heat_wave = pygame.transform.scale(img_heat_wave, (17, 48))
img_spray = pygame.image.load("resources/anti_moskito_spray.png").convert_alpha()
shop_spray = pygame.transform.scale(img_spray, (38, 85))
img_lamp = pygame.image.load("resources/anti_moskito_lamp.png").convert_alpha()
shop_lamp = pygame.transform.scale(img_lamp, (66, 95))
img_wait_bar_1 = pygame.image.load("resources/resource_0.png").convert_alpha()
img_icon = pygame.image.load("resources/resource_2.png").convert_alpha()
img_background = pygame.image.load("resources/resource_1.jpg").convert()
img_logo = pygame.image.load("resources/resource_4.png").convert_alpha()
img_btn_normal = pygame.image.load("resources/resource_5.png").convert()
img_btn_hovered = pygame.image.load("resources/resource_6.png").convert()
img_swatter_1 = pygame.image.load("resources/resource_8.png").convert_alpha()
dark_img = pygame.image.load("resources/dark.png").convert_alpha()
init_img = pygame.image.load("resources/init.png").convert()
img_pix_wait_bar = pygame.Surface((1, 13))
img_pix_wait_bar.fill((104, 255, 4))
img_blood_bar = pygame.image.load("resources/resource_9.png").convert_alpha()
btn_font = pygame.font.Font("resources\\ComicSansMSM.ttf", 30)
img_pix_blood_bar = pygame.Surface((38, 1))
img_pix_blood_bar.fill((255, 0, 0))
img_moskito_list = [pygame.image.load("resources/mosquito_1.png").convert_alpha(),
                    pygame.image.load("resources/mosquito_2.png").convert_alpha(),
                    pygame.image.load("resources/mosquito_3.png").convert_alpha(),
                    pygame.image.load("resources/mosquito_4.png").convert_alpha()]

shop_bg = pygame.Surface((1180, 660))
pygame.gfxdraw.rectangle(shop_bg, shop_bg.get_rect(), (206, 237, 31))
pygame.gfxdraw.rectangle(shop_bg, pygame.rect.Rect(1, 1, 1178, 658), (206, 237, 31))
pygame.gfxdraw.rectangle(shop_bg, pygame.rect.Rect(2, 2, 1176, 656), (206, 237, 31))
pygame.gfxdraw.box(shop_bg, pygame.rect.Rect(3, 3, 1174, 654), (235, 248, 165))
pygame.gfxdraw.box(shop_bg, pygame.rect.Rect(3, 3, 1174, 50), (220, 242, 96))

sounds_moskitos_list = ["resources/sounds/Single_moskito_1.wav",
                        "resources/sounds/Single_moskito_2.wav",
                        "resources/sounds/Single_moskito_3.wav"]

img_tmp = pygame.Surface((4, 4))
img_tmp.fill((255, 255, 255))
font_a = pygame.font.Font("resources\\ComicSansMSM.ttf", 70)

correction_angle = 90

opaque = 1055

pygame.display.set_icon(img_icon)

sprite_group = pygame.sprite.Group()

isMenu = True

# fichier lang

lang = lang_files_names[settings_list[0]]
default_lang = eval(lang)

play_btn_text = btn_font.render(default_lang[0], True, (153, 153, 0))
settings_btn_text = btn_font.render(default_lang[1], True, (153, 153, 0))
font_a_text = font_a.render(default_lang[11], True, (153, 153, 0))


def get_bziocoins():
    return get_better_score()[2]


def save_blaziocoins(blaziocoins):
    a = get_better_score()
    overwrite_better_score(a[0], a[1], blaziocoins)


# definition du joueur
BLOOD = 590


class Var:
    def __init__(self):
        super(Var, self).__init__()
        self.change_fullscreen = False
        self.blaziocoins = get_bziocoins()
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
        return eval("self." + var_name)


global_var = Var()


# class Player(pygame.sprite.Sprite):
#     def __init__(self):
#         super().__init__()
#         self.image = img_spaceship
#         self.rect = self.image.get_rect()  # Adapte le taille du personnage a la taille de l'image.
#         self.velocity = [0, 0]
#         self.rect.x = int(window_x / 2.15)
#         self.rect.y = int(window_y / 2.15)


# class Star(pygame.sprite.Sprite):
#     def __init__(self):
#         super().__init__()
#         self.image = img_star
#         self.rect = self.image.get_rect()  # Adapte le taille du personnage a la taille de l'image.
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

class MoskitoSpawnHandler:
    def __init__(self):
        super(MoskitoSpawnHandler, self).__init__()
        self.time_spent = 0
        self.time_limit = 500
        self.moskito_list = []

    def update(self):
        self.time_spent = self.time_spent + 1
        _tmp = 1
        if global_var.blood < 295:
            _tmp = 2
        if global_var.blood < 196:
            _tmp = 3
        if global_var.blood < 147:
            _tmp = 4
        if self.time_spent > self.time_limit:
            self.time_spent = 0
            for moskito in range(0, random.randint(1, _tmp)):
                self.moskito_list.append(Moskito())
            self.time_limit = self.time_limit - (self.time_limit / 75)
        for y in range(0, len(self.moskito_list)):
            self.moskito_list[y].update()


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
            self.play_obj = pygame.mixer.Sound(sounds_moskitos_list[random.randint(0, 2)])
            self.play_obj.play(-1)

    def destroy(self):
        if not self.isDestroyed:
            self.isDestroyed = True
            global_var.moskitos_killed = global_var.moskitos_killed + 1
            global_var.renew_sound = True
            if global_var.enable_sound:
                try:
                    self.play_obj.stop()
                except:
                    nlib.log("Couldn't stop a moskito sound !", "warn")

    def shiver(self):  # = trembler
        a = random.randint(1, 4)
        if a == 1:
            self.rect.x = self.rect.x + 1
        elif a == 2:
            self.rect.x = self.rect.x - 1
        elif a == 3:
            self.rect.y = self.rect.y + 1
        elif a == 4:
            self.rect.y = self.rect.y - 1

    def manage_ai_task(self):
        if self.ai_task_list == {}:
            _tmp_a = 1
            if random.randint(0, 1) == 0:
                _tmp_a = -1
            _tmp_b = 1
            if random.randint(0, 1) == 0:
                _tmp_b = -1
            self.ai_task_list = {
                'movement': {'x': random.randint(0, 10) * _tmp_a, 'y': random.randint(0, 10) * _tmp_b,
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
        if not self.isDestroyed:
            self.limit_checker()
            self.shiver()
            self.manage_ai_task()
            self.rect.move_ip(*self.velocity)
            global_var.blood = global_var.blood - 0.05
            screen.blit(self.image, self.rect)
            if global_var.enable_sound:
                self.manage_sound()


def stop_sounds():
    for moskito in moskito_spawn_handler.moskito_list:
        try:
            moskito.play_obj.stop()
        except:
            pass


def pass_to_menu():
    global_var.isMenu = True
    pygame.mouse.set_visible(True)


def pass_to_playing():
    global_var.Playing = True
    pygame.mouse.set_visible(False)
    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)


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
            global_var.click_delay = global_var.click_delay + 1.5  # (388 / time_ * 0.03)
        for f in range(0, int(global_var.click_delay)):
            screen.blit(self.pix_image, (self.rect.x + 1 + f, self.rect.y + 1))
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
        for f in range(0, int(global_var.blood)):
            screen.blit(self.pix_image, (self.rect.x + 3, self.rect.y + 592 - f))
        screen.blit(self.image, self.rect)
        if global_var.blood < 0:
            stop_sounds()
            global_var.Playing = False
            global_var.Final_Menu = True
            global_var.best_score = get_better_score()
            pygame.mouse.set_visible(True)
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)


def collision(sprite1, sprite2):
    """Used to check between 2 pygame sprites rects if they collides
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
        mouse2 = pygame.mouse.get_pos()
        self.image = img_swatter_1
        self.base_image = self.image
        self.rect = self.image.get_rect()
        self.rect.x = mouse2[0]
        self.rect.y = mouse2[1]
        self.isClicking = False
        self.time_ani = 0
        self.base_size_w = 90  # Swatter pro is 108
        self.base_size_h = 602  # Swatter pro is 718
        self.size_w = self.base_size_w
        self.size_h = self.base_size_h
        self.moskito_kill_radius = (90, 105)  # swatter pro is (108, 126)

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
        x, y = pygame.mouse.get_pos()
        if self.isClicking:
            self.time_ani = self.time_ani + 1
            if self.time_ani < 50:
                self.size_w = self.size_w - 1
                self.size_h = self.size_h - 3
                self.image = pygame.transform.scale(self.base_image, (self.size_w, self.size_h))
                self.update_rect()
            elif self.time_ani < 100:
                self.size_w = self.size_w + 1
                self.size_h = self.size_h + 3
                self.image = pygame.transform.scale(self.base_image, (self.size_w, self.size_h))
                self.update_rect()
            else:
                self.isClicking = False
                self.time_ani = 0
                self.size_w = self.base_size_w
                self.size_h = self.base_size_h
        screen.blit(self.image, (x - (self.rect.width / 2), y - (self.rect.height / 2)))
        self.update_rect()
        self.rect.x = x
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
        self.rect = self.image.get_rect()  # Adapte le taille du personnage a la taille de l'image.
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
                open_settings(global_var, default_lang, settings_list, version_name, lang_list, version_number)
                self.isClicked = False
                if global_var.change_fullscreen:
                    global_var.change_fullscreen = False
                    pygame.display.toggle_fullscreen()
        if self.type == 'play':
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
    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_WAIT)
    article_name = ""  # Ensure var is defined
    cost = 0
    if btn_type == "shop_btn_blood_2":
        cost = 100
        article_name = "Small Blood Bag"
    elif btn_type == "shop_btn_blood_3":
        cost = 150
        article_name = "Blood Bottle"
    elif btn_type == "shop_btn_blood_4":
        cost = 300
        article_name = "Huge Blood Bag"
    elif btn_type == "shop_btn_blood_5":
        cost = 800
        article_name = "Blood Infusion"
    elif btn_type == "shop_btn_swatter":
        cost = 1000
        article_name = "Swatter Pro"
    elif btn_type == "shop_btn_bzio":
        cost = 10000
        article_name = "Imposant Bzio Ruler"
    elif btn_type == "shop_btn_heat_wave":
        cost = 500
        article_name = "Heat Wave"
    elif btn_type == "shop_btn_spray":
        cost = 500
        article_name = "Anti Moskito Spray"
    elif btn_type == "shop_btn_lamp":
        cost = 750
        article_name = "Anti Moskito Lamp"
    _tk = tkinter.Tk()
    _tk.withdraw()
    _tk.iconbitmap("resources/icon.ico")
    if tkinter.messagebox.askyesno("Confirm buying ?", "Are you sure you want to buy %s ?" % article_name):
        if get_bziocoins() >= cost:
            pass
        else:
            tkinter.messagebox.showerror("Not enough money !", "You do not have enough \u20BF Coins")
    _tk.destroy()


class NewButton(pygame.sprite.Sprite):
    def __init__(self, pos_min, pos_max, text, btn_type, env="Menu", font_size=30):
        super().__init__()
        self.btn_type = btn_type
        self.isHovered = False
        self.env = env
        if not self.btn_type == "shop_close":
            self.text_image = ptext.getsurf(text, color=(153, 153, 0), fontname='resources\\ComicSansMSM.ttf',
                                            fontsize=font_size)
        else:
            self.text_image = pygame.font.Font("resources\\segoeui.ttf", 50).render(text, True, (153, 153, 0))
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
            global_var.blood = 590
            global_var.moskitos_killed = 0
            moskito_spawn_handler.time_spent = 0
            moskito_spawn_handler.time_limit = 500
            global_var.chrono = 0
            global_var.latest_chrono = 0
        elif self.btn_type == "shop_btn_blood_2" or self.btn_type == "shop_btn_blood_3" or self.btn_type == \
                "shop_btn_blood_4" or self.btn_type == "shop_btn_blood_5" or self.btn_type == "shop_btn_swatter" \
                or self.btn_type == "shop_btn_bzio" or self.btn_type == "shop_btn_heat_wave" or self.btn_type == \
                "shop_btn_spray" or self.btn_type == "shop_btn_lamp":
            buy_item(self.btn_type)
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    def update(self):
        mouse = pygame.mouse.get_pos()
        if self.pos_max[0] > mouse[0] > self.pos_min[0] and self.pos_min[1] < mouse[1] < self.pos_max[1]:
            self.isHovered = True
            screen.blit(self.hover_image, self.pos_min)
            if not opaque >= 0:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            self.isHovered = False
            screen.blit(self.image, self.pos_min)
        show_shop_btn_image(self.btn_type)
        screen.blit(self.text_image, (
            (self.pos_max[0] - self.pos_min[0]) / 2 + self.pos_min[0] - self.text_image_rect.centerx,
            (self.pos_max[1] - self.pos_min[1]) / 2 + self.pos_min[1] - self.text_image_rect.centery))


shop_btn = NewButton((512, 510), (728, 566), default_lang[10], "shop")
close_shop_btn = NewButton((1158, 37), (1223, 79), u"\u00D7", "shop_close", "Shop")
shop_btn_l = [NewButton((87, 116), (432, 212), "Healers", "", "Shop"),
              NewButton((87, 222), (432, 318), "Small blood bag (0.75L)\n100 \u20BF", "shop_btn_blood_2", "Shop"),
              NewButton((87, 328), (432, 424), "Blood bottle (1.5L)\n150 \u20BF", "shop_btn_blood_3", "Shop"),
              NewButton((87, 434), (432, 530), "Huge blood bag (4L)\n300 \u20BF", "shop_btn_blood_4", "Shop"),
              NewButton((87, 540), (432, 636), "Blood infusion (30s, 0.25 L/s)\n800 \u20BF", "shop_btn_blood_5", "Shop",
                        23),
              NewButton((462, 116), (807, 270), "Weapons", "", "Shop"),
              NewButton((462, 300), (807, 454), "Swatter Pro\n1000 \u20BF", "shop_btn_swatter", "Shop"),
              NewButton((462, 484), (807, 636), "Imposant bzio ruler\n10 000 \u20BF", "shop_btn_bzio", "Shop"),
              NewButton((837, 116), (1182, 231), "Satisfaction tools", "", "Shop"),
              NewButton((837, 251), (1182, 367), "Heat wave (-25% moskitos \nspawning during this game)\n500 \u20BF",
                        "shop_btn_heat_wave", "Shop", 25),
              NewButton((837, 387), (1182, 502), "Anti moskito spray (sus)\n(Kill all moskitos during 10s)\n500 \u20BF",
                        "shop_btn_spray", "Shop", 25),
              NewButton((837, 522), (1182, 636),
                        "Anti moskito lamp (Slow down\nmoskito speed by 70% during 30s)\n750 \u20BF",
                        "shop_btn_lamp", "Shop", 21)]

return_to_menu_btn = NewButton((490, 618), (790, 688), default_lang[17], "return_to_menu", "Final_Menu")


def manage_buttons():
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
    for element in global_var.btn_hover_list:
        if element.isHovered and element.env == current_env:
            _tmp = True
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

font_shop = pygame.font.Font("resources\\ComicSansMSM.ttf", 40).render(default_lang[10], True, (153, 153, 0))
font_rect = font_shop.get_rect()
font_rect.center = (window_x / 2, 50)


def show_popup():
    screen.blit(dark_img, (0, 0, 1280, 720))
    screen.blit(pygame.font.Font("resources\\ComicSansMSM.ttf", 40).render("A dialog box is opened", True, (153, 153, 0)
                                                                           ), (0, 0, 100, 100))


def calculate_distance(coord1, coord2, is_pygame_rect=True):
    if is_pygame_rect:
        return int(math.sqrt((coord2.centerx - coord1.centerx) ** 2 + (coord2.centery - coord1.centerx) ** 2))
    else:
        return int(math.sqrt((coord2[0] - coord1[0]) ** 2 + (coord2[1] - coord1[1]) ** 2))


# star = Star()
# player = Player()
# Definition de la fenetre
continuer = True
playBtnIsClicked = False
while continuer:
    clock.tick(250)
    t = clock.get_time()
    if global_var.isMenu:
        global_var.Playing = False

    if global_var.Playing:
        global_var.isMenu = False

    mouse = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            continuer = False
        if event.type == pygame.KEYDOWN:
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
                                moskito.play_obj.play(-1)
                        except Exception as e:
                            nlib.log(str(e), "warn")
                        pygame.mouse.set_pos(global_var.last_mouse)
                        time.sleep(0.03)
                        global_var.IsGamePaused = False
                        pygame.mouse.set_pos(global_var.last_mouse)
                        pygame.mouse.set_visible(False)
                    elif not global_var.IsGamePaused:
                        try:
                            for moskito in moskito_spawn_handler.moskito_list:
                                moskito.play_obj.stop()
                        except Exception as e:
                            nlib.log(str(e), "warn")
                        global_var.last_mouse = pygame.mouse.get_pos()
                        global_var.IsGamePaused = True
                        pygame.mouse.set_visible(True)
                else:
                    continuer = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if debug_mouse:
                mx, my = pygame.mouse.get_pos()
                nlib.log("Mouse x: %s y: %s" % (mx, my), "debug")
            if global_var.Playing:
                swatter.when_clicked()
            #            dx, dy = mx - player.rect.centerx, my - player.rect.centery
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

    # mx, my = pygame.mouse.get_pos()  # Rotation system
    #    dx, dy = mx - player.rect.centerx, my - player.rect.centery
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

    elif global_var.Playing:
        # When it's space
        if not global_var.IsGamePaused:
            moskito_spawn_handler.update()
            swatter.update()
            wait_bar.update()
            blood_bar.update()
            screen.blit(pygame.font.SysFont("Comic Sans MS", 30).render("Esc: Pause game", True, (0, 0, 0)), (850,
                                                                                                              0))
            global_var.chrono = global_var.chrono + t
        else:
            # _tmp_font = pygame.font.Font("resources\\ComicSansMSM.ttf", 45).render("Game Paused (Press Escape to resume)\nPress Space to quit",
            # True, (153, 153, 0))
            _tmp_font = ptext.getsurf("Game Paused (Press Escape to resume)\nPress Space to quit", color=(153, 153, 0),
                                      fontname='resources\\ComicSansMSM.ttf', fontsize=45)
            _tmp_rect = _tmp_font.get_rect()
            screen.blit(_tmp_font, ((window_x / 2 - _tmp_rect.centerx), (window_y / 2 - _tmp_rect.centery)))
    elif global_var.Final_Menu:
        screen.blit(font_a_text, (
            int(window_x / 2) - font_a_text.get_rect().centerx, int(window_y / 3) - font_a_text.get_rect().centery))
        _font = pygame.font.Font("resources\\ComicSansMSM.ttf", 45) \
            .render(default_lang[12].format(get_final_score()), True, (153, 153, 0))
        _font_2 = pygame.font.Font("resources\\ComicSansMSM.ttf", 45) \
            .render(default_lang[13].format(global_var.best_score[0], global_var.best_score[1]),
                    True, (153, 153, 0))
        _font_3 = pygame.font.Font("resources\\ComicSansMSM.ttf", 45) \
            .render("You win {0} \u20BF".format(int(get_final_score() * 0.75)),
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
            global_var.Final_verdict = True
            if get_final_score() > get_better_score()[0]:
                root = tk.Tk()
                root.withdraw()
                show_popup()
                overwrite_better_score(get_final_score(), str(simpledialog.askstring(
                    default_lang[14], default_lang[15])), global_var.blaziocoins)
                root.destroy()
            global_var.blaziocoins = global_var.blaziocoins + int(get_final_score() * 0.75)
            save_blaziocoins(global_var.blaziocoins)
        return_to_menu_btn.update()
        manage_buttons()
    elif global_var.shop:
        manage_buttons()
        screen.blit(shop_bg, pygame.rect.Rect(50, 30, 1180, 660))
        screen.blit(font_shop, font_rect)
        font_shop_2 = pygame.font.Font("resources\\ComicSansMSM.ttf", 40).render("{0} \u20BF".format(
            global_var.blaziocoins), True, (153, 153, 0))
        font_rect_2 = font_shop_2.get_rect()
        font_rect_2.center = (window_x / 1.3, 50)
        screen.blit(font_shop_2, font_rect_2)
        close_shop_btn.update()
        for element in shop_btn_l:
            element.update()
        # mx, my = pygame.mouse.get_pos()
    #            dx, dy = mx - player.rect.centerx, my - player.rect.centery
    #            angle = math.degrees(math.atan2(-dy, dx))
    # for x in range(0, 1000):
    # star_list[x].update(angle)
    # screen.blit(star_list[x].image, star_list[x].rect)
    # screen.blit(rot_image, rot_image_rect.topleft)  # spaceship
    if opaque >= 0:
        if opaque < 256:
            init_img.set_alpha(opaque)
        screen.blit(init_img, (0, 0))
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        opaque = opaque - 1.5
    pygame.display.update()
pygame.quit()
stop_sounds()
nlib.log("Game stopped !", "info")
sys.exit(0)
