import pygame
import sys
import random
 
pygame.init()


question = ['QuestionBank/q1.png']

pygame.display.set_caption('JumpSolve Menu')
screen = pygame.display.set_mode((640,480))
word_font = pygame.font.Font(None,50)
clock = pygame.time.Clock()
img = pygame.image.load('QuestionBank/q1.png','QuestionBank/q2.png','QuestionBank/q3.png')

def draw_text(text,font,x,y):
    img = font.render(text,True,"white")
    screen.blit(img,(x,y))

def random_selection():
    png = random.choice(question)
    print(png)
    pass


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
    
    #pygame.draw.rect(screen,"red",pygame.Rect(40,30,120,60))       
    #draw_text("Hello World",word_font,220,150)
    screen.blit(img,[0,0])
    
    pygame.display.update()
    clock.tick(60)