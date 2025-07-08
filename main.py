import sys
import pygame
from settings import SETTINGS

class Game:
    def __init__(self):
        pygame.init()

        pygame.display.set_caption(SETTINGS["TITLE"])
        self.screen = pygame.display.set_mode((SETTINGS["WIDTH"], SETTINGS["HEIGHT"]))

        self.clock = pygame.time.Clock()
    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.update()
            self.clock.tick(SETTINGS["FPS"]) 

Game().run()