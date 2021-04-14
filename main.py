import logging
import os
import nathlib as nlib

version_name = "snapshot_001"
version_number = 1

try:
    os.remove('latest.log')
except FileNotFoundError:
    pass
nlib.start_logs("latest.log")
nlib.log("Launching game version {0} ...".format(version_name), "info")
# Importation des modules

# try:
print("------------------------------Pygame--Details--------------------------")
import pygame
print("-----------------------------------------------------------------------")
import sys
import webbrowser
import time
import random
import pickle
import math
import tkinter as tk
import tkinter.ttk as ttk
# import pygame.gfxdraw  # necessary as pygame doesn't load it by default !
import threading
from settings_window import open_settings
from math import cos, sin
from glob import glob

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
pygame.mixer.init()  # Sons de pygame.

# Definition de la fenetre

window_x = 1280
window_y = 720
screen = pygame.display.set_mode((window_x, window_y))
pygame.display.set_caption("NoMoskito!")
pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_ARROW)
clock = pygame.time.Clock()
FPS = 60
# ressources à charger
# img_spaceship = pygame.image.load("resources/resource_0").convert_alpha()
img_wait_bar_1 = pygame.image.load("resources/resource_0.png").convert_alpha()
img_icon = pygame.image.load("resources/resource_2.png").convert_alpha()
img_background = pygame.image.load("resources/resource_1.jpg").convert()
img_logo = pygame.image.load("resources/resource_4.png").convert_alpha()
img_btn_normal = pygame.image.load("resources/resource_5.png").convert()
img_btn_hovered = pygame.image.load("resources/resource_6.png").convert()
img_swatter_1 = pygame.image.load("resources/resource_8.png").convert_alpha()
img_pix_wait_bar = pygame.Surface((1, 13))
img_pix_wait_bar.fill((104, 255, 4))
img_blood_bar = pygame.image.load("resources/resource_9.png").convert_alpha()
btn_font = pygame.font.SysFont('Comic Sans MS', 30)
img_pix_blood_bar = pygame.Surface((38, 1))
img_pix_blood_bar.fill((255, 0, 0))

correction_angle = 90

pygame.display.set_icon(img_icon)

sprite_group = pygame.sprite.Group()

isMenu = True

# fichier lang

lang = lang_files_names[settings_list[0]]
default_lang = eval(lang)

play_btn_text = btn_font.render(default_lang[0], False, (153, 153, 0))
settings_btn_text = btn_font.render(default_lang[1], False, (153, 153, 0))


# definition du joueur

class Var:
    def __init__(self):
        super(Var, self).__init__()
        self.is_settings_to_save = False
        self.is_update_checked = False
        self.isMenu = True
        self.can_click = True
        self.click_delay = 388
        self.click_rate = 1
        self.blood = 590

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

class WaitBar(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.pix_image = img_pix_wait_bar
        self.image = img_wait_bar_1
        self.rect = self.image.get_rect()
        self.rect.x = 470
        self.rect.y = 10

    def update(self):
        if global_var.click_delay > 336:
            global_var.click_delay = 338
            global_var.can_click = True
        if not global_var.can_click:
            global_var.click_delay = global_var.click_delay + (global_var.click_rate / 2)
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
        for f in range(0, global_var.blood):
            screen.blit(self.pix_image, (self.rect.x + 3, self.rect.y + 592 - f))
        screen.blit(self.image, self.rect)


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
        self.size_w = 90
        self.size_h = 301

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
                self.size_w = 90
                self.size_h = 301
        screen.blit(self.image, (x - (self.rect.width / 2), y - (self.rect.height / 2)))

    def when_clicked(self):
        if (not self.isClicking) and global_var.can_click:
            self.isClicking = True
            global_var.click_delay = 0
            global_var.can_click = False


class Button(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = img_btn_normal
        self.rect = self.image.get_rect()  # Adapte le taille du personnage a la taille de l'image.
        self.velocity = [0, 0]
        self.rect.x = int(window_x / 2.5)
        self.rect.y = int(window_y / 2)
        self.isClicked = False
        self.maxX = 728
        self.minX = 512
        self.minY = 362
        self.maxY = 417
        self.type = 'play'
        self.inSpace = False

    def update(self):
        if self.maxX > mouse[0] > self.minX and self.minY < mouse[1] < self.maxY:
            self.isHovered = True
        else:
            self.isHovered = False
        if self.isHovered:
            pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_HAND)
        if self.isClicked:
            if self.type == 'play':
                global_var.isMenu = False
                self.isClicked = False
                self.inSpace = True
            elif self.type == 'settings':
                pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_WAIT)
                open_settings(global_var, default_lang, settings_list, version_name, lang_list, version_number)
                self.isClicked = False
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


# stars
# star_list = []
# for x in range(0, 1000):
#     star_list.append(Star())
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

# star = Star()
# player = Player()
# Definition de la fenetre
continuer = True
playBtnIsClicked = False
while continuer:
    mouse = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            continuer = False
        if event.type == pygame.K_DOWN:
            if event.key == pygame.K_ESCAPE:
                continuer = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            if not global_var.isMenu:
                swatter.when_clicked()
#            dx, dy = mx - player.rect.centerx, my - player.rect.centery
#            angle = math.degrees(math.atan2(-dy, dx))
#            print("Angle : " + str(90 - int(angle)))
            if 728 > mouse[0] > 512 and 362 < mouse[1] < 417 and global_var.isMenu:  # check if btn is clicked.
                play_btn.isClicked = True
            if 728 > mouse[0] > 512 and 436 < mouse[1] < 492 and global_var.isMenu:
                settings_btn.isClicked = True

    mx, my = pygame.mouse.get_pos()   # Rotation system
#    dx, dy = mx - player.rect.centerx, my - player.rect.centery
#    angle = math.degrees(math.atan2(-dy, dx)) - correction_angle
#    angle2 = math.degrees(math.atan2(-dy, dx))
#    rot_image = pygame.transform.rotate(player.image, angle)
#    rot_image_rect = rot_image.get_rect(center=player.rect.center)

    screen.blit(img_background, (0, 0))
    if global_var.isMenu:
        # When it's menu
        pygame.mouse.set_visible(True)
        play_btn.update()
        settings_btn.update()
        if not play_btn.isHovered and not settings_btn.isHovered:
            pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_ARROW)
        screen.blit(img_logo, (int(window_x / 5.2), int(window_y / 6)))  # logo

    else:
        if play_btn.inSpace:
            # When it's space
            pygame.mouse.set_visible(False)
            screen.blit(img_background, (0, 0))
            swatter.update()
            wait_bar.update()
            blood_bar.update()
            mx, my = pygame.mouse.get_pos()
#            dx, dy = mx - player.rect.centerx, my - player.rect.centery
#            angle = math.degrees(math.atan2(-dy, dx))
            # for x in range(0, 1000):
                # star_list[x].update(angle)
                # screen.blit(star_list[x].image, star_list[x].rect)
            # screen.blit(rot_image, rot_image_rect.topleft)  # spaceship
    pygame.display.update()
pygame.quit()
nlib.log("Game stopped !", "info")
