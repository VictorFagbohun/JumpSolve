import pygame
import sys
import random
 
pygame.init()


easy_question = {'QuestionBank/easy/q1.png':"A",'QuestionBank/easy/q2.png':"D",'QuestionBank/easy/q3.png':"A",'QuestionBank/easy/q4.png':"C",'QuestionBank/easy/q5.png':"A",'QuestionBank/easy/q6.png':"C",'QuestionBank/easy/q7.png':"B", 'QuestionBank/easy/q8.png':"B",'QuestionBank/easy/q9.png':"C",'QuestionBank/easy/q10.png':"A",'QuestionBank/easy/q11.png':"C",'QuestionBank/easy/q12.png':"B"}
medium_question = {'QuestionBank/medium/q1.png':"C",'QuestionBank/medium/q2.png':"J",'QuestionBank/medium/q3.png':"H",'QuestionBank/medium/q4.png':"B",'QuestionBank/medium/q5.png':"G",'QuestionBank/medium/q6.png':"D",'QuestionBank/medium/q7.png':"G",'QuestionBank/medium/q8.png':"C",'QuestionBank/medium/q9.png':"C",'QuestionBank/medium/q10.png':"F",'QuestionBank/medium/q11.png':"C",'QuestionBank/medium/q12.png':"G"}
hard_question = {'QuestionBank/hard/q1.png':"D",'QuestionBank/hard/q2.png':"A",'QuestionBank/hard/q3.png':"C",'QuestionBank/hard/q4.png':"B",'QuestionBank/hard/q5.png':"C",'QuestionBank/hard/q6.png':"A",'QuestionBank/hard/q7.png':"C",'QuestionBank/hard/q8.png':"B",'QuestionBank/hard/q9.png':"A",'QuestionBank/hard/q10.png':"D",'QuestionBank/hard/q11.png':"D",'QuestionBank/hard/q12.png':"B"}



pygame.display.set_caption('JumpSolve Menu')
screen = pygame.display.set_mode((800,600))
word_font = pygame.font.Font(None,50)
clock = pygame.time.Clock()
points = 0


def draw_text(text,font,x,y):
    img = font.render(text,True,"white")
    screen.blit(img,(x,y))

def random_selection(question):
    global png
    global img
    png = random.choice(list(question.keys()))
    img = pygame.image.load(png)
    print(png)
    print(easy_question[png])

random_selection(easy_question)
img = pygame.image.load(png)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                if easy_question[png] == "A":
                    print("Correct Answer")
                    points += 1
                    del easy_question[png]
                    random_selection(easy_question)
                    img = pygame.image.load(png)
                    
                    
            elif event.key == pygame.K_b:
                if easy_question[png] == "B":
                    print("Correct Answer")
                    points += 1
                    del easy_question[png]
                    random_selection(easy_question)
                    img = pygame.image.load(png)
            elif event.key == pygame.K_c:
                print("C")
                if easy_question[png] == "C":
                    print("Correct Answer")
                    points += 1
                    del easy_question[png]
                    random_selection(easy_question)
                    img = pygame.image.load(png)
            elif event.key == pygame.K_d:
                if easy_question[png] == "D":
                    print("Correct Answer")
                    points +=1
                    del easy_question[png]
                    random_selection(easy_question)
                    img = pygame.image.load(png)
            elif event.key == pygame.K_f:
                if easy_question[png] == "F":
                    print("Correct Answer")
                    points += 1
                    del easy_question[png]
                    random_selection(easy_question)
                    img = pygame.image.load(png)
                
            elif event.key == pygame.K_g:
                if easy_question[png] == "G":
                    print("Correct Answer")
                    points += 1
                    del easy_question[png]
                    random_selection(easy_question)
                    img = pygame.image.load(png)
            elif event.key == pygame.K_h:
                print("C")
                if easy_question[png] == "H":
                    print("Correct Answer")
                    points += 1
                    del easy_question[png]
                    random_selection(easy_question)
                    img = pygame.image.load(png)
            elif event.key == pygame.K_j:
                if easy_question[png] == "J":
                    print("Correct Answer")
                    points +=1
                    del easy_question[png]
                    random_selection(easy_question)
                    img = pygame.image.load(png)
                    
    if points == 3:
        print("Congratulations")
        break
  

    screen.blit(img,[150,0])
    
    pygame.display.update()
    clock.tick(60)
    
