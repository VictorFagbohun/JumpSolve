import pygame
import sys 
 
pygame.init()

pygame.display.set_caption('JumpSolve Menu')
screen = pygame.display.set_mode((640,480))

clock = pygame.time.Clock()

word_font = pygame.font.Font(None,50)

#Instructiosn for Menu. 

menu_text = word_font.render("Menu", False, "White")
difficulty_text = word_font.render("Choose a Difficulty", False, "White")
easy_text = word_font.render("Easy", False,"White")
medium_text = word_font.render("Medium",False,"White")
hard_text = word_font.render("Hard",False,"White")


menu_rect = menu_text.get_rect(center=(640 // 2,25))
difficulty_rect = difficulty_text.get_rect(center=(640 // 2, 75))
easy_rect = easy_text.get_rect(center=(640 // 2, 150))
medium_rect = medium_text.get_rect(center=(640 // 2,250 ))
hard_rect = hard_text.get_rect(center=(640 // 2, 350))



easy_selection = pygame.Rect(160,125,320,150)


medium_selection = pygame.Rect(160,225,320,100)


hard_selection = pygame.Rect(160,325,320,100)

def menu_screen():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if easy_selection.collidepoint(event.pos):
                    #pygame.quit()
                    return "Easy"
                   
                elif medium_selection.collidepoint(event.pos):
                    #pygame.quit()
                    return "Medium Selection"
                  
                elif hard_selection.collidepoint(event.pos):
                    #pygame.quit()
                    return "Hard"
                    
            
        
        screen.fill("black")
        
        #Text Display
        screen.blit(menu_text,menu_rect)
        screen.blit(difficulty_text,difficulty_rect)
    
        #Selection Display
        pygame.draw.rect(screen,"blue",easy_selection)
        screen.blit(easy_text,easy_rect)
        
        pygame.draw.rect(screen,"red",medium_selection)
        screen.blit(medium_text,medium_rect)
        
        pygame.draw.rect(screen,"green",hard_selection)
        screen.blit(hard_text,hard_rect)
        
        
        
        pygame.display.update()
        clock.tick(60)
