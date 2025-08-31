import pygame
import random

from src.constants import WINDOW_HEIGHT, PIPE_HEIGHT, PIPE_WIDTH, PIPE_GAP, GAME_SPEED


class Pipe(pygame.sprite.Sprite):
    def __init__(self, inverted, xpos, ysize):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load(
            'assets/sprites/pipe-green.png').convert_alpha()
        self.image = pygame.transform.scale(
            self.image, (PIPE_WIDTH, PIPE_HEIGHT))

        if inverted:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect = self.image.get_rect()
            self.rect[0] = xpos
            self.rect[1] = - (self.rect[3] - ysize)
        else:
            self.rect = self.image.get_rect()
            self.rect[0] = xpos
            self.rect[1] = WINDOW_HEIGHT - ysize

        self.mask = pygame.mask.from_surface(self.image)

    @staticmethod
    def get_random_pipes(xpos):
        size = random.randint(100, 300)
        pipe = Pipe(False, xpos, size)
        pipe_inverted = Pipe(True, xpos, WINDOW_HEIGHT - size - PIPE_GAP)
        return (pipe, pipe_inverted)

    def update(self):
        self.rect[0] -= GAME_SPEED
