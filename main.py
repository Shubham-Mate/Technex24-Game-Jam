import pygame
import numpy as np
from player import Player
from level import Level
from camera import Camera
from level import LevelManager
 
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
 
# initialize pygame
pygame.init()
screen_size = (1280, 800)
TILE_SIZE = (32, 32)
width, height = pygame.display.Info().current_w, pygame.display.Info().current_h
 
# create a window
screen = pygame.display.set_mode(screen_size, pygame.RESIZABLE)
pygame.display.set_caption("pygame Test")
 
# clock is used to set a max fps
clock = pygame.time.Clock()

GRAVITY = 3

# Create the level manager
lm1 = LevelManager(Level(screen_size, TILE_SIZE, "./test1.tmx", pygame.Color(235, 113, 26)), Level(screen_size, TILE_SIZE, "./test1.tmx", pygame.Color(68, 235, 26)), Level(screen_size, TILE_SIZE, "./test1.tmx", pygame.Color(24, 107, 222)), Level(screen_size, TILE_SIZE, "./test1.tmx", pygame.Color(224, 43, 155)))


def collision_test(rect, tiles):
    hit_list = []
    for tile in tiles:
        if rect.colliderect(tile):
            hit_list.append(tile)
    return hit_list

def move(rect, movement, tiles):
    collision_types = {'top': False, 'bottom': False, 'right': False, 'left': False}
    rect.x += movement[0]
    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
        if movement[0] > 0:
            rect.right = tile.left
            collision_types['right'] = True
            lm1.levels[lm1.levelInd].c1.set_scroll_speed(np.array([0, 0]))
        elif movement[0] < 0:
            rect.left = tile.right
            collision_types['left'] = True
            lm1.levels[lm1.levelInd].c1.set_scroll_speed(np.array([0, 0]))
    rect.y += movement[1]
    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
        if movement[1] > 0:
            rect.bottom = tile.top
            collision_types['bottom'] = True
        elif movement[1] < 0:
            rect.top = tile.bottom
            collision_types['top'] = True
    return rect, collision_types

 
 
running = True
while running:
    dt = clock.tick(60)
    lm1.levels[lm1.levelInd].c1.add_scroll(lm1.levels[lm1.levelInd].p1.getRect(), TILE_SIZE)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.RESIZABLE:
            screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_j:
                lm1.prevLevel()
            if event.key == pygame.K_l:
                lm1.nextLevel()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        lm1.levels[lm1.levelInd].p1.set_speed(np.array([0, -1]))

    if keys[pygame.K_s]:
        lm1.levels[lm1.levelInd].p1.set_speed(np.array([0, 1]))

    if keys[pygame.K_a]:
        lm1.levels[lm1.levelInd].p1.set_speed(np.array([-1, 0]))

    if keys[pygame.K_d]:
        lm1.levels[lm1.levelInd].p1.set_speed(np.array([1, 0]))

    print(lm1.levelInd)

    # Gravity Physics
    if lm1.levels[lm1.levelInd].p1.speed[1] >= 6:
        lm1.levels[lm1.levelInd].p1.set_speed(np.array([lm1.levels[lm1.levelInd].p1.speed[0], lm1.levels[lm1.levelInd].p1.speed[1]]))
    else:
        lm1.levels[lm1.levelInd].p1.set_speed(np.array([lm1.levels[lm1.levelInd].p1.speed[0], lm1.levels[lm1.levelInd].p1.speed[1] + (GRAVITY * dt/1000)]))

    

    #clear the screen
    screen.fill(BLACK)    

    # Draw the level
    tile_rect = []
    for layer in lm1.levels[lm1.levelInd].level.layers:
        for x, y, surf in layer.tiles():
            screen.blit(surf, dest=(x*TILE_SIZE[0] - lm1.levels[lm1.levelInd].c1.pos[0], y*TILE_SIZE[1] - lm1.levels[lm1.levelInd].c1.pos[1]))
            tile_rect.append(pygame.Rect(x*TILE_SIZE[0], y*TILE_SIZE[1], TILE_SIZE[0], TILE_SIZE[1]))

    lm1.levels[lm1.levelInd].p1.rectangle, collisions = move(lm1.levels[lm1.levelInd].p1.getRect(), lm1.levels[lm1.levelInd].p1.speed * lm1.levels[lm1.levelInd].p1.speedMultiplier, tile_rect)

    if collisions['bottom']:
        lm1.levels[lm1.levelInd].p1.set_speed(np.array([lm1.levels[lm1.levelInd].p1.speed[0], 0]))


     
    # draw to the screen
    pygame.draw.rect(screen, pygame.Color(255, 255, 255), lm1.levels[lm1.levelInd].p1.getRect().move(-lm1.levels[lm1.levelInd].c1.pos[0], 0))
 

    # flip() updates the screen to make our changes visible
    pygame.display.flip()
     
    # how many updates per second


pygame.quit()