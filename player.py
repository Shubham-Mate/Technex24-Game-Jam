import numpy as np
import pygame

class Player:
    
    def __init__(self, pos, size, spritePath, ability, sm):
        self.pos = pos
        self.size = size
        self.sprite_path = spritePath
        self.sprite = None
        self.speed = np.array([0, 0], dtype='int16')
        self.rectangle = pygame.Rect(pos[0], pos[1], size[0], size[1])
        self.speedMultiplier = sm
        self.ability = ability
        self.sprite = pygame.image.load(f"./Assets/Images/{ability}.png")

    def set_speed(self, speed):
        self.speed = speed

    def add_speed(self, speed):
        self.speed += speed

    def move (self):
        self.pos += self.speed * self.speedMultiplier
        self.rectangle = self.rectangle.move(self.speed[0]*self.speedMultiplier, self.speed[1]*self.speedMultiplier)

    def getRect(self):
        return self.rectangle