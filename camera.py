import numpy as np
class Camera:
    def __init__(self, x, y):
        self.pos = np.array([x, y], dtype = 'float32')
        self.scroll_speed = np.array([0, 0], dtype = 'float32')
        self.speed_multiplier = 2

    def set_scroll_speed(self, sp):
        self.scroll_speed = sp

    def scroll(self):
        self.pos += self.scroll_speed * self.speed_multiplier

    def add_scroll(self, p_rect, TILE_SIZE):
        self.pos[0] += (p_rect.x - self.pos[0] - (TILE_SIZE[0]/2) - 640 + 100)/20
        self.pos[0] = max(self.pos[0], 0)