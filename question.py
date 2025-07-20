import pygame
import sys
import random
 
pygame.init()


question = {'QuestionBank/q1.png':"A",'QuestionBank/q2.png':"D",'QuestionBank/q3.png':"B",'QuestionBank/q4.png':"B",'QuestionBank/q5.png':"D",'QuestionBank/q6.png':"B",'QuestionBank/q7.png':"C"}

pygame.display.set_caption('JumpSolve Menu')
screen = pygame.display.set_mode((800,600))
word_font = pygame.font.Font(None,50)
clock = pygame.time.Clock()
points = 0


def draw_text(text,font,x,y):
    img = font.render(text,True,"white")
    screen.blit(img,(x,y))

def random_selection():
    global png
    global img
    png = random.choice(list(question.keys()))
    img = pygame.image.load(png)
    print(png)
    print(question[png])

random_selection()
img = pygame.image.load(png)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                if question[png] == "A":
                    print("Correct Answer")
                    points += 1
                    del question[png]
                    random_selection()
                    img = pygame.image.load(png)
                    
                    
            elif event.key == pygame.K_b:
                if question[png] == "B":
                    print("Correct Answer")
                    points += 1
                    del question[png]
                    random_selection()
                    img = pygame.image.load(png)
            elif event.key == pygame.K_c:
                print("C")
                if question[png] == "C":
                    print("Correct Answer")
                    points += 1
                    del question[png]
                    random_selection()
                    img = pygame.image.load(png)
            elif event.key == pygame.K_d:
                if question[png] == "D":
                    print("Correct Answer")
                    points +=1
                    del question[png]
                    random_selection()
                    img = pygame.image.load(png)
                    
    if points == 3:
        print("Congratulations")
        break
  

    screen.blit(img,[150,0])
    
    pygame.display.update()
    clock.tick(60)
    
