import pygame
import sys 
 
pygame.init()

pygame.display.set_caption('JumpSolve Menu')
screen = pygame.display.set_mode((640,480))
word_font = pygame.font.Font(None,50)
clock = pygame.time.Clock()

def draw_text(text,font,x,y):
    img = font.render(text,True,"white")
    screen.blit(img,(x,y))


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
    
    pygame.draw.rect(screen,"red",pygame.Rect(40,30,120,60))       
    draw_text("Hello World",word_font,220,150)
    pygame.display.update()
    clock.tick(60)