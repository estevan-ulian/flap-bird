import pygame
from src.constants import WINDOW_WIDTH, WINDOW_HEIGHT, SPEED, GRAVITY


class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)

        self.images = [
            pygame.image.load(
                'assets/sprites/redbird-upflap.png'),
            pygame.image.load(
                'assets/sprites/redbird-midflap.png'),
            pygame.image.load(
                'assets/sprites/redbird-downflap.png'),
        ]
        self.current_image = 0
        self.image = pygame.image.load(
            'assets/sprites/redbird-upflap.png')
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect[0] = WINDOW_WIDTH / 3
        self.rect[1] = WINDOW_HEIGHT / 2
        self.speed = SPEED

    def update(self):
        self.current_image = (self.current_image + 1) % len(self.images)
        self.image = self.images[self.current_image]
        self.rect[1] += self.speed
        self.speed += GRAVITY

    def bump(self):
        self.speed = -SPEED
        pygame.mixer.Sound(
            'assets/audio/wing.ogg').play(loops=0,   maxtime=0, fade_ms=0)
