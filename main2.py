import pygame
import numpy as np
from player import Player
from level import Level
from camera import Camera
from level import LevelManager
from pygame.locals import *

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

GRAVITY = 1

# Create the level manager
lm1 = LevelManager(Level(screen_size, TILE_SIZE, "./test2.tmx", pygame.Color(235, 113, 26), "hecker"), Level(screen_size, TILE_SIZE, "./test2.tmx", pygame.Color(68, 235, 26), 'soldier'), Level(screen_size, TILE_SIZE, "./test2.tmx", pygame.Color(24, 107, 222), 'water'), Level(screen_size, TILE_SIZE, "./test2.tmx", pygame.Color(224, 43, 155), 'climber'))
lvl_dict = {"orange": 0, "green": 1, "blue": 2, "pink": 3}

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

 
vertical_speed = 0
horizontal_speed = 0
onGround=False
running = True
while running:
    dt = clock.tick(60)
    lm1.levels[lm1.levelInd].c1.add_scroll(lm1.levels[lm1.levelInd].p1.getRect(), TILE_SIZE)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and onGround:
        vertical_speed = -50
        onGround = False
    elif keys[pygame.K_s]:
        vertical_speed = 1
    else:
        vertical_speed = GRAVITY
    if keys[pygame.K_a]:
        horizontal_speed = -1
    elif keys[pygame.K_d]:
        horizontal_speed = 1
    else:
        horizontal_speed = 0 

    lm1.levels[lm1.levelInd].p1.set_speed(np.array([horizontal_speed, vertical_speed]))


    # Gravity Physics
    if lm1.levels[lm1.levelInd].p1.speed[1] >= 6:
        lm1.levels[lm1.levelInd].p1.set_speed(np.array([lm1.levels[lm1.levelInd].p1.speed[0], lm1.levels[lm1.levelInd].p1.speed[1]]))
    else:
        lm1.levels[lm1.levelInd].p1.set_speed(np.array([lm1.levels[lm1.levelInd].p1.speed[0], lm1.levels[lm1.levelInd].p1.speed[1] + (GRAVITY * dt/1000)]))

    

    #clear the screen
    screen.fill(BLACK)    

    # Draw the level
    tile_rect = []
    obj_rect = []
    obj_dict = {}
    tile_layer = lm1.levels[lm1.levelInd].level.layers[0]
    obj_layer = lm1.levels[lm1.levelInd].level.layers[1]
    for x, y, surf in tile_layer.tiles():
        screen.blit(surf, dest=(x*TILE_SIZE[0] - lm1.levels[lm1.levelInd].c1.pos[0], y*TILE_SIZE[1] - lm1.levels[lm1.levelInd].c1.pos[1]))
        tile_rect.append(pygame.Rect(x*TILE_SIZE[0], y*TILE_SIZE[1], TILE_SIZE[0], TILE_SIZE[1]))

    lm1.levels[lm1.levelInd].p1.rectangle, collisions = move(lm1.levels[lm1.levelInd].p1.getRect(), lm1.levels[lm1.levelInd].p1.speed * lm1.levels[lm1.levelInd].p1.speedMultiplier, tile_rect)

    for obj in obj_layer:
        screen.blit(obj.image, dest=(obj.x - lm1.levels[lm1.levelInd].c1.pos[0], obj.y - lm1.levels[lm1.levelInd].c1.pos[1]))
        obj_rect.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
        obj_dict[obj.name] = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
    
    hit_list = collision_test(lm1.levels[lm1.levelInd].p1.rectangle, obj_rect)
    
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
            if event.key == pygame.K_k:
                if len(hit_list) > 0:
                    for key, value in obj_dict.items():
                        if hit_list[0].x == value.x and hit_list[0].y == value.y:
                            lm1.levels[lvl_dict[key]].p1.rectangle
                            hit_list_2 = collision_test(lm1.levels[lvl_dict[key]].p1.rectangle, obj_rect)
                            if len(hit_list_2) > 0:
                                for key2, value2 in obj_dict.items():
                                    if hit_list[0].x == value.x and hit_list[0].y == value.y:
                                        if lvl_dict[key2] == lm1.levelInd:
                                            lm1.swapPlayers(lvl_dict[key], lvl_dict[key2])
                                            break
                            break


                

    if collisions['bottom']:
        onGround=True
        lm1.levels[lm1.levelInd].p1.set_speed(np.array([lm1.levels[lm1.levelInd].p1.speed[0], 0]))



     
    # draw to the screen
    pygame.draw.rect(screen, lm1.levels[lm1.levelInd].color_identifier, lm1.levels[lm1.levelInd].p1.getRect().move(-lm1.levels[lm1.levelInd].c1.pos[0], 0))
 

    # flip() updates the screen to make our changes visible
    pygame.display.flip()
     


pygame.quit()