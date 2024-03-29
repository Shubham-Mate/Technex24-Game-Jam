import pytmx
from player import Player
from camera import Camera
import numpy as np
from pytmx.util_pygame import load_pygame

class Level:
    def __init__(self, screen_size, tile_size, level_name, color, ability, sm):
        self.screen_size = screen_size
        self.tile_size = tile_size
        self.level = load_pygame(level_name)
        self.p1 = Player(np.array([40*32, 5*32], dtype='int16'), np.array([32, 48]), "dummy", ability, sm)
        self.c1 = Camera(0, 0)
        self.color_identifier = color


class LevelManager:
    def __init__(self, l1, l2, l3, l4):
        self.levels = [l1, l2, l3, l4]
        self.levelInd = 0

    def nextLevel(self):
        self.levelInd += 1
        if self.levelInd >= 4:
            self.levelInd = 0

    def prevLevel(self):
        self.levelInd -= 1
        if self.levelInd <= -1:
            self.levelInd = 3

    def swapPlayers(self, ind1, ind2):
        temp1 = self.levels[ind1].p1
        temp2 = self.levels[ind2].p1
        temp1_rect = temp1.rectangle
        temp2_rect = temp2.rectangle
        self.levels[ind1].p1 = self.levels[ind2].p1
        self.levels[ind2].p1 = temp1
        self.levels[ind1].p1.rectangle = temp1_rect
        self.levels[ind2].p1.rectangle = temp2_rect

    

