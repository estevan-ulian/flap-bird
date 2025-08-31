import pygame
import random
import uuid

from src.constants import WINDOW_HEIGHT, PIPE_HEIGHT, PIPE_WIDTH, PIPE_GAP, GAME_SPEED


class Pipe(pygame.sprite.Sprite):
    def __init__(self, inverted, xpos, ysize):
        pygame.sprite.Sprite.__init__(self)

        self.pipe_id = str(uuid.uuid4())

        self.image = pygame.image.load(
            'assets/sprites/pipe-green.png').convert_alpha()
        self.image = pygame.transform.scale(
            self.image, (PIPE_WIDTH, PIPE_HEIGHT))

        if inverted:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect = self.image.get_rect()
            self.rect[0] = xpos
            self.rect[1] = - (self.rect[3] - ysize)
            self.pipe_type = 'top'
        else:
            self.rect = self.image.get_rect()
            self.rect[0] = xpos
            self.rect[1] = WINDOW_HEIGHT - ysize
            self.pipe_type = 'bottom'

        self.mask = pygame.mask.from_surface(self.image)

    @staticmethod
    def get_random_pipes(xpos):
        """ Generate two pipes (one inverted) with a gap """
        size = random.randint(100, 300)
        pipe = Pipe(False, xpos, size)
        pipe_inverted = Pipe(True, xpos, WINDOW_HEIGHT - size - PIPE_GAP)
        return (pipe, pipe_inverted)

    def update(self):
        """ Move the pipes to the left """
        self.rect[0] -= GAME_SPEED
