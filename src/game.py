import pygame
from src.constants import WINDOW_WIDTH, WINDOW_HEIGHT, FPS, GROUND_WIDTH
from src.bird import Bird
from src.ground import Ground


class Game:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.background = pygame.image.load(
            'assets/sprites/background-day.png').convert_alpha()
        self.clock = pygame.time.Clock()

    def is_off_screen(self, sprite):
        return sprite.rect[0] < -sprite.rect[2]

    def start(self):
        background = pygame.transform.scale(
            self.background, (WINDOW_WIDTH, WINDOW_HEIGHT))
        
        bird_group = pygame.sprite.Group()
        bird = Bird(100, 200)
        bird_group.add(bird)

        ground_group = pygame.sprite.Group()
        for i in range(2):
            ground = Ground(GROUND_WIDTH * i)
            ground_group.add(ground)

        while True:
            # Set window title and icon
            pygame.display.set_caption("Flap Bird Game")
            pygame.display.set_icon(bird.images[0])

            # Frame rate
            self.clock.tick(FPS)

            # Quit event
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        bird.bump()

            # Draw background
            self.window.blit(background, (0, 0))
            
            if self.is_off_screen(ground_group.sprites()[0]):
                ground_group.remove(ground_group.sprites()[0])                
                last_ground = ground_group.sprites()[-1]
                new_ground = Ground(last_ground.rect.x + GROUND_WIDTH)
                ground_group.add(new_ground)

            # Draw ground           
            ground_group.draw(self.window)
            ground_group.update()

            # Draw bird
            bird_group.draw(self.window)
            bird_group.update()

            pygame.display.update()
