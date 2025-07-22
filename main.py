import sys
import pygame
import os
import random
import math
from os import listdir
from os.path import isfile, join
from settings import PLAYER_SETTINGS, SETTINGS
from menu import menu_screen
 
pygame.init()
pygame.display.set_caption(SETTINGS["TITLE"])

window = pygame.display.set_mode((SETTINGS["WIDTH"], SETTINGS["HEIGHT"]))

def flip(sprites):
    return [pygame.transform.flip(sprite, True, False) for sprite in sprites]

def load_spritesheet(dir1, dir2, width, height, direction = False):
    path = join("assets", dir1, dir2)
    images = [f for f in listdir(path) if isfile(join(path, f))]
    
    #debug code
    for image in images:
        print(f"\nLoading {image}:")
        print(f"File exists: {os.path.exists(join(path, image))}")
        print(f"File size: {os.path.getsize(join(path, image))} bytes")

        try:     
            test_load = pygame.image.load(join(path, image))
            print(f"Dimensions: {test_load.get_size()}")
            print(f"Transparency: {test_load.get_flags() & pygame.SRCALPHA}")
        except Exception as e:
            print(f"ERROR loading {image}: {str(e)}")
    # end of debug code


    all_sprites = {}

    for image in images:
        spritesheet = pygame.image.load(join(path, image)).convert_alpha()
  
        sprites = []
        for i in range(spritesheet.get_width() // width):
            surface = pygame.Surface((width, height), pygame.SRCALPHA, 32)
            rect = pygame.Rect(i * width, 0, width, height)
            surface.blit(spritesheet, (0, 0), rect)
            sprites.append(pygame.transform.scale2x(surface))

        if direction:
            all_sprites[image.replace(".png", "") + "_right"] = sprites
            all_sprites[image.replace(".png", "") + "_left"] = flip(sprites)
        else:
            all_sprites[image.replace(".png", "")] = sprites

            

    

    return all_sprites


class Player(pygame.sprite.Sprite):
    GRAVITY = 1
    SPRITES = load_spritesheet("Sprite", "1 Pink_Monster", 32, 32, True)


    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.x_vel = 0
        self.y_vel = 0
        self.mask = None
        self.direction = "left"
        self.animation_count = 0
        self.fall_count = 0

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    def move_left(self, vel):
        self.x_vel = -vel
        if self.direction != "left":
            self.direction = "left"
            self.animation_count = 0
    
    def move_right(self, vel):
        self.x_vel = vel
        if self.direction != "right":
            self.direction = "right"
            self.animation_count = 0

    def loop(self, fps):
        #self.y_vel += min(1, (self.fall_count / fps) * self.GRAVITY)
        self.move(self.x_vel, self.y_vel)
        self.fall_count += 1

    def draw(self, win):
        self.sprite = self.SPRITES["Pink_Monster_Idle_4_" + self.direction][0]
        win.blit(self.sprite, (self.rect.x, self.rect.y))




def get_background(name):
    image = pygame.image.load(join("assets", "background", name))
    _, _, width, height = image.get_rect()
    tiles = []
    for x in range(0, SETTINGS["WIDTH"], width):
        for y in range(0, SETTINGS["HEIGHT"], height):
            tiles.append(image.get_rect(topleft=(x, y)))
    
    return tiles, image
    

def draw(window, background, bg_image,player):
    for tile in background:
        window.blit(bg_image, tile)

    player.draw(window)

    pygame.display.update()

def handle_movement(player, SETTINGS, PLAYER_SETTINGS):
    keys = pygame.key.get_pressed()
    player.x_vel = 0

    if keys[pygame.K_a]:
        player.move_left(PLAYER_SETTINGS["SPEED"])
    elif keys[pygame.K_d]:
        player.move_right(PLAYER_SETTINGS["SPEED"])

def main(window):
    clock = pygame.time.Clock()
    print(Player.SPRITES.keys())
    background, bg_image = get_background("Gray.png")

    player = Player(100,100,64,64)

    while True:
        clock.tick(SETTINGS["FPS"])
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        player.loop(SETTINGS["FPS"])
        handle_movement(player, SETTINGS, PLAYER_SETTINGS)
        draw(window, background, bg_image, player)

if __name__ == "__main__":
    main(window)
    
