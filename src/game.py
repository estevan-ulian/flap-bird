import pygame
from src.constants import WINDOW_WIDTH, WINDOW_HEIGHT, FPS, GROUND_WIDTH
from src.bird import Bird
from src.ground import Ground
from src.pipe import Pipe


class Game:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.background = pygame.image.load(
            'assets/sprites/background-day.png').convert_alpha()
        self.clock = pygame.time.Clock()

        self.MENU = 0
        self.PLAYING = 1
        self.GAME_OVER = 2
        self.game_state = self.MENU

        self.title_image = pygame.image.load(
            'assets/sprites/message.png').convert_alpha()

        pygame.font.init()
        self.font_large = pygame.font.Font(None, 28)
        self.font_small = pygame.font.Font(None, 18)

        pygame.mixer.init()
        self.menu_music = pygame.mixer.Sound('assets/audio/menu.mp3')
        self.is_menu_music_playing = False

        self.gaming_music = pygame.mixer.Sound('assets/audio/gaming.ogg')
        self.is_gaming_music_playing = False

        self.gameover_music = pygame.mixer.Sound('assets/audio/game-over.mp3')
        self.is_gameover_music_playing = False

    def is_off_screen(self, sprite):
        return sprite.rect[0] < -sprite.rect[2]

    def draw_start_screen(self, background):
        self.window.blit(background, (0, 0))

        title_rect = self.title_image.get_rect()
        title_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 3)
        self.window.blit(self.title_image, title_rect)

        instruction_text = self.font_small.render(
            "Pressione ESPAÇO para começar", True, (255, 255, 255))
        instruction_rect = instruction_text.get_rect()
        instruction_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 80)
        text_bg = pygame.Surface(
            (instruction_rect.width + 20, instruction_rect.height + 10))
        text_bg.fill((0, 0, 0))
        text_bg.set_alpha(128)
        text_bg_rect = text_bg.get_rect()
        text_bg_rect.center = instruction_rect.center

        self.window.blit(text_bg, text_bg_rect)
        self.window.blit(instruction_text, instruction_rect)

        controls_text = self.font_small.render(
            "Pressione 'ESPAÇO' para voar", True, (255, 255, 255))
        controls_rect = controls_text.get_rect()
        controls_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 110)

        controls_bg = pygame.Surface(
            (controls_rect.width + 20, controls_rect.height + 10))
        controls_bg.fill((0, 0, 0))
        controls_bg.set_alpha(128)
        controls_bg_rect = controls_bg.get_rect()
        controls_bg_rect.center = controls_rect.center

        self.window.blit(controls_bg, controls_bg_rect)
        self.window.blit(controls_text, controls_rect)

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

        pipe_group = pygame.sprite.Group()

        while True:
            pygame.display.set_caption("Flap Bird Game")
            pygame.display.set_icon(bird.images[0])
            self.clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if self.game_state == self.MENU:
                            self.game_state = self.PLAYING
                            bird.rect.x = 100
                            bird.rect.y = 200
                            bird.speed = 0
                            pipe_group.empty()
                            for i in range(2):
                                pipes = Pipe.get_random_pipes(
                                    WINDOW_WIDTH * i + 800)
                                pipe_group.add(pipes[0])
                                pipe_group.add(pipes[1])
                        elif self.game_state == self.PLAYING:
                            bird.bump()
                        elif self.game_state == self.GAME_OVER:
                            if self.is_menu_music_playing:
                                self.menu_music.stop()
                                self.is_menu_music_playing = False
                            if self.is_gaming_music_playing:
                                self.gaming_music.stop()
                                self.is_gaming_music_playing = False
                            if self.is_gameover_music_playing:
                                self.gameover_music.stop()
                                self.is_gameover_music_playing = False
                            self.game_state = self.MENU

            match self.game_state:
                case self.MENU:
                    if not self.is_menu_music_playing:
                        self.menu_music.play(loops=-1)
                        self.is_menu_music_playing = True
                    self.draw_start_screen(background)
                case self.PLAYING:
                    if self.is_menu_music_playing:
                        self.menu_music.stop()
                        self.is_menu_music_playing = False

                    if not self.is_gaming_music_playing:
                        self.gaming_music.play(loops=-1)
                        self.is_gaming_music_playing = True

                    self.window.blit(background, (0, 0))
                    if self.is_off_screen(ground_group.sprites()[0]):
                        ground_group.remove(ground_group.sprites()[0])
                        last_ground = ground_group.sprites()[-1]
                        new_ground = Ground(last_ground.rect.x + GROUND_WIDTH)
                        ground_group.add(new_ground)

                    if self.is_off_screen(pipe_group.sprites()[0]):
                        pipe_group.remove(pipe_group.sprites()[0])
                        pipe_group.remove(pipe_group.sprites()[0])
                        pipes = Pipe.get_random_pipes(WINDOW_WIDTH * 2)
                        pipe_group.add(pipes[0])
                        pipe_group.add(pipes[1])

                    ground_group.update()
                    bird_group.update()
                    pipe_group.update()

                    bird_group.draw(self.window)
                    pipe_group.draw(self.window)
                    ground_group.draw(self.window)

                    if (pygame.sprite.groupcollide(bird_group, ground_group, False, False, pygame.sprite.collide_mask)) or (pygame.sprite.groupcollide(bird_group, pipe_group, False, False, pygame.sprite.collide_mask)):
                        pygame.mixer.Sound(
                            'assets/audio/hit.ogg').play(loops=0, maxtime=0, fade_ms=0)
                        if self.is_gaming_music_playing:
                            self.gaming_music.stop()
                            self.is_gaming_music_playing = False
                        self.game_state = self.GAME_OVER
                case self.GAME_OVER:
                    if not self.is_gameover_music_playing:
                        self.gameover_music.play(loops=-1)
                        self.is_gameover_music_playing = True

                    self.window.blit(background, (0, 0))
                    self.window.blit(background, (0, 0))
                    bird_group.draw(self.window)
                    pipe_group.draw(self.window)
                    ground_group.draw(self.window)

                    game_over_text = self.font_large.render(
                        "GAME OVER", True, (255, 255, 255))
                    game_over_rect = game_over_text.get_rect()
                    game_over_rect.center = (
                        WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)

                    restart_text = self.font_small.render(
                        "Pressione ESPAÇO para voltar ao menu", True, (255, 255, 255))
                    restart_rect = restart_text.get_rect()
                    restart_rect.center = (
                        WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 40)

                    text_bg = pygame.Surface(
                        (max(game_over_rect.width, restart_rect.width) + 40, 80))
                    text_bg.fill((0, 0, 0))
                    text_bg.set_alpha(180)
                    text_bg_rect = text_bg.get_rect()
                    text_bg_rect.center = (
                        WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 10)

                    self.window.blit(text_bg, text_bg_rect)
                    self.window.blit(game_over_text, game_over_rect)
                    self.window.blit(restart_text, restart_rect)

            pygame.display.update()
