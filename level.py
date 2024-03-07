import pytmx
from pytmx.util_pygame import load_pygame

class Level:
    def __init__(self, screen_size, tile_size, level_name):
        self.screen_size = screen_size
        self.tile_size = tile_size
        self.level = load_pygame("test1.tmx")
