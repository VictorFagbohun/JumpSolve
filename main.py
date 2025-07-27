import sys
import pygame
import os
import random
import math
from os import listdir
from os.path import isfile, join
from settings import PLAYER_SETTINGS, SETTINGS, GAME_SETTINGS
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
        self.JUMP_POWER = PLAYER_SETTINGS["JUMP_HEIGHT"]

    def jump(self):
        if self.jump_count == 0:
            self.y_vel = -self.JUMP_POWER
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



    def draw(self, win, offset_x, offset_y):
        win.blit(self.sprite, (self.rect.x - offset_x, self.rect.y - offset_y))


class Object(pygame.sprite.Sprite):
    def __init__(self,x,y,width,height,name=None):
        super().__init__()
        self.rect = pygame.Rect(x,y,width,height)
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.width = width
        self.height = height
        self.name = name

    def draw(self, win, offset_x, offset_y):
        win.blit(self.image, (self.rect.x - offset_x, self.rect.y - offset_y))

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
    

def draw(window, background, bg_image,player, objects, offset_x, offset_y):
    for tile in background:
        window.blit(bg_image, tile)

    for obj in objects:
        obj.draw(window, offset_x, offset_y)

    player.draw(window, offset_x, offset_y)

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

def collide(player, objects, dx):
    player.move(dx, 0)
    player.update()
    collided_object = None
    for obj in objects:
        if pygame.sprite.collide_mask(player, obj):
            collided_object = obj
            break

    player.move(-dx, 0)
    player.update()
    return collided_object


def handle_movement(player, objects):
    keys = pygame.key.get_pressed()
    player.x_vel = 0
    collide_left = collide(player, objects, -PLAYER_SETTINGS["SPEED"] * 2)
    collide_right = collide(player, objects, PLAYER_SETTINGS["SPEED"] * 2)

    if keys[pygame.K_a] and not collide_left:
        player.move_left(PLAYER_SETTINGS["SPEED"])
    elif keys[pygame.K_d] and not collide_right:
        player.move_right(PLAYER_SETTINGS["SPEED"])

    handle_vertical_collision(player, objects, player.y_vel)

    

def main(window):
    # Get difficulty from menu
    difficulty = menu_screen()
    
    # Updated difficulty settings
    DIFFICULTY_SETTINGS = {
        "Easy": {
            "gap_increase": 8,           # Blocks closer together for Easy
            "base_jump": 4.0,
            "jump_multiplier": 1.2,      # Use old Medium settings
            "question_diff": "Easy",
            "gravity": 0.7,
            "max_jump_upgrades": 12
        },
        "Medium": {
            "gap_increase": 12,          # Use old Easy settings
            "base_jump": 3.0,
            "jump_multiplier": 1.25,
            "question_diff": "Medium",
            "gravity": 0.7,
            "max_jump_upgrades": 10
        },
        "Hard": {
            "gap_increase": 18,          # Use old Medium settings
            "base_jump": 3.0,
            "jump_multiplier": 1.2,
            "question_diff": "Hard", 
            "gravity": 0.9,
            "max_jump_upgrades": 12
        }
    }
    settings = DIFFICULTY_SETTINGS[difficulty]

    # Game initialization
    pygame.mixer.music.load("music/game.mp3")
    pygame.mixer.music.play(-1)

    clock = pygame.time.Clock()
    background, bg_image = get_background("Gray.png")

    block_size = 64
    objects = []
    start_x = 100
    start_y = SETTINGS["HEIGHT"] - block_size * 2
    current_gap = block_size * 2
    question_every = 3

    # Generate platforms with exponential gap scaling
    for i in range(GAME_SETTINGS[difficulty]):
        if i > 0 and i % question_every == 0:
            # Exponential gap growth
            #current_gap *= 1.05  # 15% wider each question platform
            current_gap += settings["gap_increase"]  # Plus flat increase
            
        x = start_x + i * current_gap
        y = start_y - i * (block_size * 0.8)
        objects.append(Block(x, y, block_size))

    # Player setup with supercharged jump system
    first_platform = objects[0]
    player = Player(
        first_platform.rect.x + (first_platform.width // 2) - 32,
        first_platform.rect.y - 64,
        64, 64
    )
    player.GRAVITY = settings["gravity"]
    player.JUMP_POWER = settings["base_jump"]
    jump_upgrades = 0
    
    # Game state
    offset_x = 0
    offset_y = 0
    scroll_area_width = SETTINGS["WIDTH"] // 3  # More responsive camera
    scroll_area_height = SETTINGS["HEIGHT"] // 3
    death_threshold = SETTINGS["HEIGHT"] + 300  # More forgiving death boundary
    game_over = False
    question_active = False
    next_question_idx = question_every

    while True:
        clock.tick(SETTINGS["FPS"])
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not game_over and not question_active:
                    player.jump()
                if event.key == pygame.K_r and game_over:
                    from question import seen_ids
                    seen_ids.clear()  # Reset seen_ids when restarting  
                    return main(window)

        
        if not game_over:
            if not question_active:
                player.loop(SETTINGS["FPS"])
                handle_movement(player, objects)
                
                # Check platform collisions and trigger question after landing
                for i, platform in enumerate(objects):
                    # Check if player is landing on the platform
                    if player.rect.bottom >= platform.rect.top and \
                       player.rect.bottom <= platform.rect.top + 15 and \
                       player.rect.right > platform.rect.left and \
                       player.rect.left < platform.rect.right and \
                       player.y_vel >= 0:

                        player.landed()  # Ensure player lands

                        # Check if player is centered on the block
                        player_center_x = player.rect.centerx
                        block_center_x = platform.rect.centerx
                        block_half_width = platform.rect.width // 2

                        # Only trigger question if player is within the middle 40% of the block
                        if abs(player_center_x - block_center_x) < block_half_width * 0.4:
                            if i >= next_question_idx:
                                question_active = True
                                next_question_idx += question_every

                                # Supercharged jump upgrade system
                                answered_correctly = questions(settings["question_diff"])
                                if answered_correctly and jump_upgrades < settings["max_jump_upgrades"]:
                                    jump_upgrades += 1
                                    player.JUMP_POWER = settings["base_jump"] * (settings["jump_multiplier"] ** jump_upgrades)

                                    # Visual feedback
                                    font = pygame.font.SysFont(None, 36)
                                    upgrade_text = font.render(f"JUMP UPGRADE! ({player.JUMP_POWER:.1f})", True, (0, 255, 0))
                                    window.blit(upgrade_text, (SETTINGS["WIDTH"]//2 - upgrade_text.get_width()//2, 50))
                                    pygame.display.update()
                                    pygame.time.delay(500)

                                    print(f"JUMP POWER: {player.JUMP_POWER:.1f} (Upgrade {jump_upgrades}/{settings['max_jump_upgrades']})")

                                question_active = False
                                break
                
                # Death check
                if player.rect.y > death_threshold:
                    game_over = True
                
                # Camera control - more aggressive tracking
                target_offset_x = player.rect.x - SETTINGS["WIDTH"] // 3
                target_offset_y = player.rect.y - SETTINGS["HEIGHT"] // 3
                
                # Smooth camera movement
                offset_x += (target_offset_x - offset_x) * 0.1
                offset_y += (target_offset_y - offset_y) * 0.1

        draw(window, background, bg_image, player, objects, offset_x, offset_y)
        
        if game_over:
            # Enhanced game over screen
            overlay = pygame.Surface((SETTINGS["WIDTH"], SETTINGS["HEIGHT"]), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 200))
            window.blit(overlay, (0, 0))
            
            font_large = pygame.font.SysFont(None, 72)
            font_medium = pygame.font.SysFont(None, 48)
            
            game_over_text = font_large.render("GAME OVER", True, (255, 50, 50))
            restart_text = font_medium.render("Press R to restart", True, (255, 255, 255))
            stats_text = font_medium.render(f"Reached Jump Level: {jump_upgrades} (Power: {player.JUMP_POWER:.1f})", True, (200, 200, 255))
            
            window.blit(game_over_text, (SETTINGS["WIDTH"]//2 - game_over_text.get_width()//2, 
                                       SETTINGS["HEIGHT"]//2 - 100))
            window.blit(restart_text, (SETTINGS["WIDTH"]//2 - restart_text.get_width()//2, 
                                     SETTINGS["HEIGHT"]//2))
            window.blit(stats_text, (SETTINGS["WIDTH"]//2 - stats_text.get_width()//2, 
                                   SETTINGS["HEIGHT"]//2 + 60))
            
            pygame.display.update()

if __name__ == "__main__":
    pygame.init()
    window = pygame.display.set_mode((SETTINGS["WIDTH"], SETTINGS["HEIGHT"]))
    pygame.display.set_caption(SETTINGS["TITLE"])
    main(window)

