import pygame
import sys 
from os.path import isfile, join

pygame.init()

pygame.display.set_caption('JumpSolve Menu')
screen = pygame.display.set_mode((800,600))

clock = pygame.time.Clock()

word_font = pygame.font.Font(None,50)

# Load background

def get_background(name):
    image = pygame.image.load(join("assets", "background", name))
    _, _, width, height = image.get_rect()
    tiles = []
    for x in range(0, 800, width):
        for y in range(0, 600, height):
            tiles.append(image.get_rect(topleft=(x, y)))
    
    return tiles, image
    

def draw(window, background, bg_image,player, objects):
    for tile in background:
        window.blit(bg_image, tile)

    for obj in objects:
        obj.draw(window)

    player.draw(window)

    pygame.display.update()

background, bg_image = get_background("Gray.png")  # Use your desired image

#Instructions for Menu. 

menu_text = word_font.render("Menu", False, "Black")
difficulty_text = word_font.render("Choose a Difficulty", False, "Black")
easy_text = word_font.render("Easy", False,"Black")
medium_text = word_font.render("Medium",False,"Black")
hard_text = word_font.render("Hard",False,"Black")


menu_rect = menu_text.get_rect(center=(800 // 2,25))
difficulty_rect = difficulty_text.get_rect(center=(800 // 2, 75))

# Adjusted option width and vertical spacing
OPTION_WIDTH = 350
OPTION_HEIGHT = 80
OPTION_X = (800 - OPTION_WIDTH) // 2
OPTION_Y_START = 140
OPTION_SPACING = 40

easy_selection = pygame.Rect(OPTION_X, OPTION_Y_START, OPTION_WIDTH, OPTION_HEIGHT)
medium_selection = pygame.Rect(OPTION_X, OPTION_Y_START + OPTION_HEIGHT + OPTION_SPACING, OPTION_WIDTH, OPTION_HEIGHT)
hard_selection = pygame.Rect(OPTION_X, OPTION_Y_START + 2 * (OPTION_HEIGHT + OPTION_SPACING), OPTION_WIDTH, OPTION_HEIGHT)

easy_rect = easy_text.get_rect(center=easy_selection.center)
medium_rect = medium_text.get_rect(center=medium_selection.center)
hard_rect = hard_text.get_rect(center=hard_selection.center)

def menu_screen():
    pygame.mixer.init()
    pygame.mixer.music.load("music/menu_background_music.mp3")  # Use your exported EarSketch file
    pygame.mixer.music.play(-1)  # Loop the music

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if easy_selection.collidepoint(event.pos):
                    pygame.mixer.music.stop()
                    return "Easy"
                elif medium_selection.collidepoint(event.pos):
                    pygame.mixer.music.stop()
                    return "Medium Selection"
                elif hard_selection.collidepoint(event.pos):
                    pygame.mixer.music.stop()
                    return "Hard"
        
        for tile in background:
            screen.blit(bg_image, tile)
        #Text Display
        screen.blit(menu_text, menu_rect)
        screen.blit(difficulty_text, difficulty_rect)
    
        #Selection Display with rounded corners and centered text
        pygame.draw.rect(screen, "blue", easy_selection, border_radius=30)
        screen.blit(easy_text, easy_rect)
        
        pygame.draw.rect(screen, "red", medium_selection, border_radius=30)
        screen.blit(medium_text, medium_rect)
        
        pygame.draw.rect(screen, "green", hard_selection, border_radius=30)
        screen.blit(hard_text, hard_rect)
        
        pygame.display.update()
        clock.tick(60)
