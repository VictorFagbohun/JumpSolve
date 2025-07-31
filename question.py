import pygame
import sys
import random
import json
import asyncio

pygame.init()
pygame.display.set_caption('JumpSolve Menu')
screen = pygame.display.set_mode((800,600))
word_font = pygame.font.Font(None,50)
clock = pygame.time.Clock()

def load_questions_json(filename):
    with open(filename, "r") as f:
        return json.load(f)

seen_ids = []

async def questions(difficulty):
    global seen_ids
    points = 0

    # Choose file based on difficulty
    if difficulty == "Easy":
        questions_list = load_questions_json("json/easy_questions.json")
    elif difficulty == "Medium":
        questions_list = load_questions_json("json/medium_questions.json")
    elif difficulty == "Hard":
        questions_list = load_questions_json("json/hard_questions.json")
    else:
        print("Invalid difficulty")
        return

    def draw_text(text, font, x, y):
        img = font.render(text, True, "white")
        screen.blit(img, (x, y))

    def random_unseen_question():
        unseen = [q for q in questions_list if q["id"] not in seen_ids]
        if not unseen:
            return None
        chosen = random.choice(unseen)
        seen_ids.append(chosen["id"])
        return chosen

    current_question = random_unseen_question()
    if current_question:
        img = pygame.image.load(current_question["image"])
    
    else:
        img = None

    while current_question:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                # Check answer
                if event.unicode.upper() == current_question["answer"]:
                    print("Correct Answer")
                    points += 1
                    
                    # Show "Correct!" message briefly
                    correct_text = word_font.render("Correct!", True, (0, 255, 0))
                    screen.blit(correct_text, (screen.get_width()//2 - correct_text.get_width()//2, screen.get_height()//2 - correct_text.get_height()//2))
                    pygame.display.update()
                    await asyncio.sleep(1)  # Show message for 1 second
                    
                    if points == 1:
                        print("Congratulations")
                        return True
                    current_question = random_unseen_question()
                    if current_question:
                        img = pygame.image.load(current_question["image"])
                    else:
                        img = None
                        print("Congratulations")
                        return True

        if img:
            screen.blit(img, [150, 0])
        pygame.display.update()
        clock.tick(60)
        
        # Yield control to asyncio event loop
        await asyncio.sleep(0)
