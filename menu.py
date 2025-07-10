import pygame
import sys 
 
pygame.init()

pygame.display.set_caption('JumpSolve Menu')
screen = pygame.display.set_mode((640,480))

clock = pygame.time.Clock()

test_font = pygame.font.Font(None,50)

test_surface = pygame.Surface((320,200))
test_surface.fill('blue')

menu_text = test_font.render("Menu", False, "White")
difficulty_text = test_font.render("Choose a Difficulty", False, "White")

menu_rect = menu_text.get_rect(center=(640 // 2,25))
difficulty_rect = difficulty_text.get_rect(center=(640 // 2, 75))


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
           pygame.quit()
           sys.exit()
       
    screen.blit(test_surface,(160,0))
    screen.blit(menu_text,menu_rect)
    screen.blit(difficulty_text,difficulty_rect)
    
    
    pygame.display.update()
    clock.tick(60)