import pygame, sys
import numpy as np
from player import Player
from level import Level
from camera import Camera
from level import LevelManager
from button import Button
import time
 
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0,255,0)
gray=(119,118,110)
blue=(0,0,200)
bright_red=(255,0,0)
bright_green=(0,255,0)
bright_blue=(0,0,255)

# initialize pygame
pygame.init()
screen_size = (1280, 800)
TILE_SIZE = (32, 32)
width, height = pygame.display.Info().current_w, pygame.display.Info().current_h
BG = pygame.image.load("assets/images/Background.png")
 
# create a window
screen = pygame.display.set_mode(screen_size, pygame.RESIZABLE)
pygame.display.set_caption("Dimensional Drifters")
 
# clock is used to set a max fps
clock = pygame.time.Clock()
game_music = pygame.mixer.Sound("assets/sounds/StarRock.mp3")
jump_s = pygame.mixer.Sound("assets/sounds/jump.mp3")
door_s = pygame.mixer.Sound("assets/sounds/door.mp3")
portal_s = pygame.mixer.Sound("assets/sounds/portal.mp3")
button_s = pygame.mixer.Sound("assets/sounds/button.mp3")

# Gravity
GRAVITY = 3

# Set GameState
gamestate = 'menu'

# Create the level manager
lm1 = LevelManager(Level(screen_size, TILE_SIZE, "./Levels/level1 1.tmx", pygame.Color(235, 113, 26), "hecker", 3), Level(screen_size, TILE_SIZE, "./Levels/level1 2.tmx", pygame.Color(68, 235, 26), 'soldier', 5), Level(screen_size, TILE_SIZE, "./Levels/level1 3.tmx", pygame.Color(24, 107, 222), 'scientist', 3), Level(screen_size, TILE_SIZE, "./Levels/level1 4.tmx", pygame.Color(224, 43, 155), 'thief', 3))
lvl_dict = {"orange": 0, "green": 1, "blue": 2, "pink": 3}
def text_objects(text,font):
    textsurface=font.render(text,True,BLACK)
    return textsurface,textsurface.get_rect()

pause = False
last_time = time.time()

def paused():
    global pause
    pause=True
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:  
                play()
    BG_copy = BG.copy()
    BG_copy.set_alpha(25)
    screen.blit(BG_copy, (0, 0))
    MENU_TEXT = get_font(80).render("Game paused", True, "#FFBD00")
    MENU_RECT = MENU_TEXT.get_rect(center=(screen.get_width() / 2, screen.get_height() / 6))
    largetext = pygame.font.Font('freesansbold.ttf', 115)
    TextSurf, TextRect = text_objects("PAUSED", largetext)
    TextRect.center = ((1280 / 2), (800 / 2))
    screen.blit(MENU_TEXT, MENU_RECT)
    button("CONTINUE", 150, 450, 150, 50, GREEN, bright_green, "continue")
    button("RESTART", 350, 450, 150, 50, blue, bright_blue, "play")
    button("MAIN MENU", 550, 450, 200, 50, RED, bright_red, "menu")
    pygame.display.update()
    clock.tick(30)




def button(msg, x, y, w, h, ic, ac, action=None):
    global gamestate, lm1
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    # Check if mouse is over the button
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(screen, ac, (x, y, w, h))  # Draw button with active color
        if click[0] == 1 and action is not None:
            button_s.play()
            if action == "play":
                lm1 = LevelManager(Level(screen_size, TILE_SIZE, "./Levels/level1 1.tmx", pygame.Color(235, 113, 26), "hecker", 3), Level(screen_size, TILE_SIZE, "./Levels/level1 2.tmx", pygame.Color(68, 235, 26), 'soldier', 5), Level(screen_size, TILE_SIZE, "./Levels/level1 3.tmx", pygame.Color(24, 107, 222), 'scientist', 3), Level(screen_size, TILE_SIZE, "./Levels/level1 4.tmx", pygame.Color(224, 43, 155), 'thief', 3))
                gamestate = 'level'
            elif action == "quit":
                pygame.quit()
                sys.exit()
            elif action == "menu":
                gamestate = 'menu'
            elif action == "pause":
                gamestate = 'pause'
            elif action == "continue":
                gamestate = 'level'
    else:
        pygame.draw.rect(screen, ic, (x, y, w, h))  # Draw button with inactive color

    # Render button text
    small_text = pygame.font.Font('freesansbold.ttf', 20)
    text_surf, text_rect = text_objects(msg, small_text)
    text_rect.center = ((x + (w / 2)), (y + (h / 2)))
    screen.blit(text_surf, text_rect)

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

def get_font(size):
    return pygame.font.Font("assets/font1.ttf", size)

def options():
    global screen, gamestate
    OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

    screen.fill("white")

    OPTIONS_TEXT = get_font(45).render("This is the OPTIONS screen.", True, "Black")
    OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(screen.get_width() / 2, screen.get_height() / 3))
    screen.blit(OPTIONS_TEXT, OPTIONS_RECT)

    OPTIONS_BACK = Button(image=None, pos=(screen.get_width() / 2, screen.get_height() / 1.5), 
                        text_input="BACK", font=get_font(75), base_color="Black", hovering_color="GREEN")

    OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
    OPTIONS_BACK.update(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            button_s.play()
            if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                gamestate = 'menu'
        if event.type == pygame.VIDEORESIZE:
            screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
    pygame.display.update()


    

def main_menu():
    global gamestate, lm1, last_time
    screen.blit(BG, (0, 0))

    game_music.play()

    MENU_MOUSE_POS = pygame.mouse.get_pos()

    MENU_TEXT = get_font(80).render("Dimensional Drifters", True, "#FFBD00")
    MENU_RECT = MENU_TEXT.get_rect(center=(screen.get_width() / 2, screen.get_height() / 6))

    PLAY_BUTTON = Button(image=pygame.image.load("assets/images/Rect.png"), pos=(screen.get_width() / 2, (screen.get_height() / 2) - 150), 
                        text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="GREEN")
    OPTIONS_BUTTON = Button(image=pygame.image.load("assets/images/Rect.png"), pos=(screen.get_width() / 2, (screen.get_height() / 2)), 
                        text_input="OPTIONS", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
    QUIT_BUTTON = Button(image=pygame.image.load("assets/images/Rect.png"), pos=(screen.get_width() / 2, (screen.get_height() / 2) + 150), 
                        text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="RED")

    screen.blit(MENU_TEXT, MENU_RECT)

    for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
        button.changeColor(MENU_MOUSE_POS)
        button.update(screen)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            button_s.play()
            if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                game_music.stop()
                lm1 = LevelManager(Level(screen_size, TILE_SIZE, "./Levels/level1 1.tmx", pygame.Color(235, 113, 26), "hecker", 3), Level(screen_size, TILE_SIZE, "./Levels/level1 2.tmx", pygame.Color(68, 235, 26), 'soldier', 5), Level(screen_size, TILE_SIZE, "./Levels/level1 3.tmx", pygame.Color(24, 107, 222), 'scientist', 3), Level(screen_size, TILE_SIZE, "./Levels/level1 4.tmx", pygame.Color(224, 43, 155), 'thief', 3))
                last_time = time.time()
                gamestate = 'level'
            if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                gamestate = 'options'
            if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                pygame.quit()
                sys.exit()

    pygame.display.update()
 
 
vertical_speed = 0
horizontal_speed = 0
onGround=False
onWall  = False


def play():
    global screen, onGround, gamestate, onWall, pause, last_time
    
    now = time.time()
    dt = now - last_time
    dt *= 60
    last_time = time.time()

    lm1.levels[lm1.levelInd].c1.add_scroll(lm1.levels[lm1.levelInd].p1.getRect(), TILE_SIZE)

    
    keys = pygame.key.get_pressed()
    if not (lm1.levels[lm1.levelInd].completed):
        if (keys[pygame.K_w] or keys[pygame.K_SPACE])and (onGround or (lm1.levels[lm1.levelInd].p1.ability == 'thief' and onWall)):
            vertical_speed = -1.75
            jump_s.play()
            onGround = False
        else:
            vertical_speed = lm1.levels[lm1.levelInd].p1.speed[1]
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
        lm1.levels[lm1.levelInd].p1.set_speed(np.array([lm1.levels[lm1.levelInd].p1.speed[0], lm1.levels[lm1.levelInd].p1.speed[1] + (GRAVITY * dt/60)]))

    

    #clear the screen
    screen.fill(BLACK)    

    # Draw the level
    tile_rect = []
    teleporter_rect = []
    teleporter_dict = {}
    background_layer = lm1.levels[lm1.levelInd].level.layers[0]
    tile_layer = lm1.levels[lm1.levelInd].level.layers[1]
    obj_layer = lm1.levels[lm1.levelInd].level.layers[2]
    door_layer = lm1.levels[lm1.levelInd].level.layers[3]
    teleport_layer = lm1.levels[lm1.levelInd].level.layers[4]
    shard_layer = lm1.levels[lm1.levelInd].level.layers[5]


    for x, y, surf in background_layer.tiles():
        screen.blit(surf, dest=(x*TILE_SIZE[0] - lm1.levels[lm1.levelInd].c1.pos[0], y*TILE_SIZE[1] - lm1.levels[lm1.levelInd].c1.pos[1]))
    
    for x, y, surf in tile_layer.tiles():
        screen.blit(surf, dest=(x*TILE_SIZE[0] - lm1.levels[lm1.levelInd].c1.pos[0], y*TILE_SIZE[1] - lm1.levels[lm1.levelInd].c1.pos[1]))
        tile_rect.append(pygame.Rect(x*TILE_SIZE[0], y*TILE_SIZE[1], TILE_SIZE[0], TILE_SIZE[1]))
    

    for obj in obj_layer:
        screen.blit(obj.image, dest=(obj.x - lm1.levels[lm1.levelInd].c1.pos[0], obj.y - lm1.levels[lm1.levelInd].c1.pos[1]))
    
    for door in door_layer:
        screen.blit(door.image, dest=(door.x - lm1.levels[lm1.levelInd].c1.pos[0], door.y - lm1.levels[lm1.levelInd].c1.pos[1]))
        if door.properties['Passable'] != lm1.levels[lm1.levelInd].p1.ability and door.properties['Passable'] != 'all':
            tile_rect.append(pygame.Rect(door.x, door.y, door.width, door.height))

    for teleporter in teleport_layer:
        screen.blit(teleporter.image, dest=(teleporter.x - lm1.levels[lm1.levelInd].c1.pos[0], teleporter.y - lm1.levels[lm1.levelInd].c1.pos[1]))
        teleporter_rect.append(pygame.Rect(teleporter.x, teleporter.y, teleporter.width, teleporter.height))
        teleporter_dict[(int(teleporter.x), int(teleporter.y))] = teleporter

    if not(lm1.levels[lm1.levelInd].completed):
        for shard in shard_layer:
            screen.blit(shard.image, dest=(shard.x - lm1.levels[lm1.levelInd].c1.pos[0], shard.y - lm1.levels[lm1.levelInd].c1.pos[1]))
            shard_hit_list = collision_test(lm1.levels[lm1.levelInd].p1.rectangle, [pygame.Rect(shard.x, shard.y, shard.width, shard.height)])
            if len(shard_hit_list) > 0:
                lm1.levels[lm1.levelInd].completed = True
                if (lm1.checkCompleted()):
                    gamestate = 'completed'
    
    hit_list = collision_test(lm1.levels[lm1.levelInd].p1.rectangle, lm1.levels[lm1.levelInd].obj_rect)
    teleporter_hit_list = collision_test(lm1.levels[lm1.levelInd].p1.rectangle, teleporter_rect)
    lm1.levels[lm1.levelInd].p1.rectangle, collisions = move(lm1.levels[lm1.levelInd].p1.getRect(), lm1.levels[lm1.levelInd].p1.speed * lm1.levels[lm1.levelInd].p1.speedMultiplier * dt, tile_rect)


    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()
        if event.type == pygame.RESIZABLE:
            screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_j:
                lm1.prevLevel()
            if event.key == pygame.K_l:
                lm1.nextLevel()
            if event.key == pygame.K_k:
                if len(hit_list) > 0:
                    for key, values in lm1.levels[lm1.levelInd].obj_dict.items():
                        for value in values:
                            if hit_list[0].x == value.x and hit_list[0].y == value.y:
                                hit_list_2 = collision_test(lm1.levels[lvl_dict[key]].p1.rectangle, lm1.levels[lvl_dict[key]].obj_rect)
                                if len(hit_list_2) > 0:
                                    for key2, values2 in lm1.levels[lvl_dict[key]].obj_dict.items():
                                        for value2 in values2:
                                            if hit_list_2[0].x == value2.x and hit_list_2[0].y == value2.y:
                                                if lvl_dict[key2] == lm1.levelInd:
                                                    lm1.swapPlayers(lvl_dict[key], lvl_dict[key2])
                                                    break
                                break
            if event.key == pygame.K_e:
                if lm1.levels[lm1.levelInd].p1.ability == 'scientist':
                    for re in teleporter_hit_list:
                        for t in teleport_layer:
                            if teleporter_dict[(re.x, re.y)].properties['to'] == t.name:
                                lm1.levels[lm1.levelInd].p1.rectangle.x = t.x
                                lm1.levels[lm1.levelInd].p1.rectangle.y = t.y
                                portal_s.play()

            if event.key == pygame.K_ESCAPE:                
                pygame.display.update()
                gamestate = 'pause'
                clock.tick(60)


                

    if collisions['bottom']:
        onGround = True
        lm1.levels[lm1.levelInd].p1.set_speed(np.array([lm1.levels[lm1.levelInd].p1.speed[0], 0]))

    if collisions['left'] or collisions['right']:
        onWall = True
    else:
        onWall = False


    
    # draw to the screen
    screen.blit(lm1.levels[lm1.levelInd].p1.sprite, (lm1.levels[lm1.levelInd].p1.rectangle.x - lm1.levels[lm1.levelInd].c1.pos[0], lm1.levels[lm1.levelInd].p1.rectangle.y - lm1.levels[lm1.levelInd].c1.pos[1]))
    mask_outline = np.array(pygame.mask.from_surface(lm1.levels[lm1.levelInd].p1.sprite).outline())
    pygame.draw.polygon(screen, lm1.levels[lm1.levelInd].color_identifier, mask_outline + (lm1.levels[lm1.levelInd].p1.rectangle.x - lm1.levels[lm1.levelInd].c1.pos[0], lm1.levels[lm1.levelInd].p1.rectangle.y - lm1.levels[lm1.levelInd].c1.pos[1]), 3)

    # flip() updates the screen to make our changes visible
    pygame.display.flip()

def completed():
    global gamestate, lm1
    screen.blit(BG, (0, 0))


    COMPLETED_TEXT = get_font(80).render("Level Complete", True, "#FFBD00")
    COMPLETED_RECT = COMPLETED_TEXT.get_rect(center=(screen.get_width() / 2, screen.get_height() / 6))

    ENTER_TEXT = get_font(60).render("Press Enter to continue", True, "#FFBD00")
    ENTER_RECT = ENTER_TEXT.get_rect(center=(screen.get_width() / 2, screen.get_height() / 2))

    screen.blit(COMPLETED_TEXT, COMPLETED_RECT)
    screen.blit(ENTER_TEXT, ENTER_RECT)

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                gamestate = 'menu' 
    pygame.display.flip()
    clock.tick(60)
        

while True:
    if gamestate == 'menu':
        main_menu()
    if gamestate == 'options':
        options()
    if gamestate == 'level':
        play()
    if gamestate == 'pause':
        paused()
    if gamestate == 'completed':
        completed()
