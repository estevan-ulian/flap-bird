import pygame
from src.constants import WINDOW_WIDTH, WINDOW_HEIGHT


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Flap Bird Game")
        self.window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

    def start(self):
        pass
