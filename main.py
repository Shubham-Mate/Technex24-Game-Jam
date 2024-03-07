import pygame
import numpy as np
from player import Player
from level import Level
 
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

# Create a player
p1 = Player(np.array([0, 0], dtype='float32'), np.array([32, 32]), "dummy")
GRAVITY = 3

# Create the level
l1 = Level(screen_size, TILE_SIZE, "./test1.tmx")


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
    print(hit_list)
    for tile in hit_list:
        if movement[0] > 0:
            rect.right = tile.left
            collision_types['right'] = True
        elif movement[0] < 0:
            rect.left = tile.right
            collision_types['left'] = True
    rect.y += movement[1]
    hit_list = collision_test(rect, tiles)
    print(hit_list)
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
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.RESIZABLE:
            screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        p1.set_speed(np.array([0, -1]))
        #p1.move()
    if keys[pygame.K_s]:
        p1.set_speed(np.array([0, 1]))
        #p1.move()
    if keys[pygame.K_a]:
        p1.set_speed(np.array([-1, 0]))
        #p1.move()
    if keys[pygame.K_d]:
        p1.set_speed(np.array([1, 0]))
        #p1.move()
     

    # Gravity Physics
    if p1.speed[0] >= 6:
        p1.set_speed(np.array([p1.speed[0], p1.speed[1]]))
    else:
        p1.set_speed(np.array([p1.speed[0], p1.speed[1] + (GRAVITY * dt/1000)]))

    

    #clear the screen
    screen.fill(BLACK)    

    # Draw the level
    tile_rect = []
    for layer in l1.level.layers:
        for x, y, surf in layer.tiles():
            screen.blit(surf, dest=(x*TILE_SIZE[0], y*TILE_SIZE[1]))
            tile_rect.append(pygame.Rect(x*TILE_SIZE[0], y*TILE_SIZE[1], TILE_SIZE[0], TILE_SIZE[1]))

    p1.rectangle, collisions = move(p1.getRect(), p1.speed * p1.speedMultiplier, tile_rect)

    if collisions['bottom']:
        p1.set_speed(np.array([p1.speed[0], 0]))


     
    # draw to the screen
    pygame.draw.rect(screen, pygame.Color(255, 255, 255), p1.getRect())
 

    # flip() updates the screen to make our changes visible
    pygame.display.flip()
     
    # how many updates per second
 
pygame.quit()