import sys
import pygame
import os
import random
import math
from os import listdir
from os.path import isfile, join
from settings import PLAYER_SETTINGS, SETTINGS
from menu import menu_screen
from question import questions
 
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

def load_block(size):
    path = join("assets", "Environment", "terrain2.png")
    image = pygame.image.load(path).convert_alpha()
    surface = pygame.Surface((size, size), pygame.SRCALPHA, 32)
    rect = pygame.Rect(0, 0, size, size)
    surface.blit(image, (0, 0), rect)
    return pygame.transform.scale2x(surface)


class Player(pygame.sprite.Sprite):
    GRAVITY = 1
    SPRITES = load_spritesheet("Sprite", "1 Pink_Monster", 32, 32, True)
    ANIMATIONDELAY = 5


    def __init__(self, x, y, width, height):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.x_vel = 0
        self.y_vel = 0
        self.mask = None
        self.direction = "left"
        self.animation_count = 0
        self.fall_count = 0
        self.jump_count = 0

    def jump(self):
        if self.jump_count == 0:
            self.y_vel = -self.GRAVITY * 8
            self.animation_count = 0
            self.jump_count += 1
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

    def landed(self):
        self.fall_count = 0
        self.y_vel = 0
        self.jump_count = 0

    def hit_head(self):
        self.count = 0
        self.y_vel *= -1
        
    def loop(self, fps):
        self.y_vel += min(1, (self.fall_count / fps) * self.GRAVITY)
        self.move(self.x_vel, self.y_vel)
        self.fall_count += 1
        self.update_sprite()

    def update_sprite(self):
        spritesheet = "Pink_Monster_Idle_4"
        if self.y_vel < 0:
            if self.jump_count == 1:
                spritesheet = "Pink_Monster_Jump_8"
        elif self.x_vel != 0:
            spritesheet = "Pink_Monster_Run_6"
            
        spritesheetname = spritesheet + "_" + self.direction
        sprites = self.SPRITES[spritesheetname]
        spriteindex = (self.animation_count // self.ANIMATIONDELAY) % len(sprites)
        self.sprite = sprites[spriteindex]
        self.animation_count += 1
        self.update()
    
    def update(self):
        self.rect = self.sprite.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.sprite)



    def draw(self, win):
        win.blit(self.sprite, (self.rect.x, self.rect.y))


class Object(pygame.sprite.Sprite):
    def __init__(self,x,y,width,height,name=None):
        super().__init__()
        self.rect = pygame.Rect(x,y,width,height)
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.width = width
        self.height = height
        self.name = name

    def draw(self, win):
        win.blit(self.image, (self.rect.x, self.rect.y))

class Block(Object):
    def __init__(self,x,y,size):
        super().__init__(x, y, size, size)
        block = load_block(size)
        self.image.blit(block, (0, 0))
        self.mask = pygame.mask.from_surface(self.image)


def get_background(name):
    image = pygame.image.load(join("assets", "background", name))
    _, _, width, height = image.get_rect()
    tiles = []
    for x in range(0, SETTINGS["WIDTH"], width):
        for y in range(0, SETTINGS["HEIGHT"], height):
            tiles.append(image.get_rect(topleft=(x, y)))
    
    return tiles, image
    

def draw(window, background, bg_image,player, objects):
    for tile in background:
        window.blit(bg_image, tile)

    for obj in objects:
        obj.draw(window)

    player.draw(window)

    pygame.display.update()

def handle_vertical_collision(player, objects, dy):
    collidedobjects = []
    for obj in objects:
        if pygame.sprite.collide_mask(player, obj):
            if dy > 0:
                player.rect.bottom = obj.rect.top
                player.landed()
            elif dy < 0:
                player.rect.top = obj.rect.bottom
                player.hit_head()

        collidedobjects.append(obj)
    return collidedobjects

def handle_movement(player, objects):
    keys = pygame.key.get_pressed()
    player.x_vel = 0

    if keys[pygame.K_a]:
        player.move_left(PLAYER_SETTINGS["SPEED"])
    elif keys[pygame.K_d]:
        player.move_right(PLAYER_SETTINGS["SPEED"])

    handle_vertical_collision(player, objects, player.y_vel)

    

def main(window):
    menu_screen()
    clock = pygame.time.Clock()
    print(Player.SPRITES.keys())
    background, bg_image = get_background("Gray.png")

    block_size = 96

    player = Player(100,100,64,64)
    floor = [Block(i * block_size, SETTINGS["HEIGHT"] - block_size, block_size) for i in range(-SETTINGS["WIDTH"] // block_size, SETTINGS["WIDTH"] * 2 // block_size)]

    while True:
        clock.tick(SETTINGS["FPS"])
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.jump()
        
        player.loop(SETTINGS["FPS"])
        handle_movement(player, floor)
        draw(window, background, bg_image, player, floor)

if __name__ == "__main__":
    main(window)
    
