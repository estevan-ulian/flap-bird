import pygame
from src.constants import SCORE_PIPE_INCREMENT, SCORE_TIME_BONUS, WINDOW_WIDTH, WINDOW_HEIGHT, FPS, GROUND_WIDTH
from src.bird import Bird
from src.ground import Ground
from src.pipe import Pipe
from src.score import Score


class Game:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.background = pygame.image.load(
            'assets/sprites/background-day.png').convert_alpha()
        self.clock = pygame.time.Clock()

        self.title_image = pygame.image.load(
            'assets/sprites/message.png').convert_alpha()

        # Game States
        self.MENU = 0
        self.PLAYING = 1
        self.GAME_OVER = 2
        self.game_state = self.MENU

        # Game Fonts
        pygame.font.init()
        self.font_large = pygame.font.Font(None, 28)
        self.font_small = pygame.font.Font(None, 18)

        # Game Sounds
        pygame.mixer.init()
        self.menu_music = pygame.mixer.Sound('assets/audio/menu.mp3')
        self.is_menu_music_playing = False

        self.gaming_music = pygame.mixer.Sound('assets/audio/gaming.ogg')
        self.is_gaming_music_playing = False

        self.gameover_music = pygame.mixer.Sound('assets/audio/game-over.mp3')
        self.is_gameover_music_playing = False

        self.score_manager = Score()
        self.current_score = 0
        self.game_start_time = 0
        self.last_time_bonus = 0
        self.pipes_passed = set()

    def is_off_screen(self, sprite):
        """ Check if a sprite is off the screen to the left """
        return sprite.rect[0] < -sprite.rect[2]

    def check_pipe_passed(self, bird, pipe_group):
        """ Check if the bird has passed a pipe to update the score """
        for pipe in pipe_group.sprites():
            if hasattr(pipe, 'pipe_type') and pipe.pipe_type == 'top':
                pipe_id = pipe.pipe_id
                if bird.rect.x > pipe.rect.x + pipe.rect.width and pipe_id not in self.pipes_passed:
                    self.pipes_passed.add(pipe_id)
                    self.current_score += SCORE_PIPE_INCREMENT
                    pygame.mixer.Sound('assets/audio/point.ogg').play(loops=0)

    def check_time_bonus(self):
        """ Check if 5 seconds have passed to give a time bonus """
        current_time = pygame.time.get_ticks()
        elapsed_time = (current_time - self.game_start_time) // 1000

        if elapsed_time >= self.last_time_bonus + 5:
            self.current_score += SCORE_TIME_BONUS
            self.last_time_bonus = elapsed_time

    def get_game_time(self):
        """ Get the elapsed game time in MM:SS format """
        if self.game_start_time == 0:
            return "00:00"
        current_time = pygame.time.get_ticks()
        elapsed_time = (current_time - self.game_start_time) // 1000
        minutes = elapsed_time // 60
        seconds = elapsed_time % 60
        return f"{minutes:02d}:{seconds:02d}"

    def draw_score_and_time(self):
        """ Draw the current score and elapsed time on the screen """
        score_text = self.font_large.render(
            f"Score: {self.current_score}", True, (255, 255, 255))
        score_bg = pygame.Surface(
            (score_text.get_width() + 20, score_text.get_height() + 10))
        score_bg.fill((0, 0, 0))
        score_bg.set_alpha(128)

        self.window.blit(score_bg, (10, 10))
        self.window.blit(score_text, (20, 15))

        time_text = self.font_small.render(
            f"Tempo: {self.get_game_time()}", True, (255, 255, 255))
        time_bg = pygame.Surface(
            (time_text.get_width() + 20, time_text.get_height() + 10))
        time_bg.fill((0, 0, 0))
        time_bg.set_alpha(128)

        self.window.blit(time_bg, (10, 45))
        self.window.blit(time_text, (20, 50))

    def draw_start_screen(self, background):
        """ Draw the start screen with title, instructions and top 3 scores """
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

        top3_scores = self.score_manager.show()
        if top3_scores:
            top3_title = self.font_small.render(
                "Top 3 maiores pontuações:", True, (255, 255, 255))
            top3_title_rect = top3_title.get_rect()
            top3_title_rect.center = (
                WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 150)

            title_bg = pygame.Surface(
                (top3_title_rect.width + 20, top3_title_rect.height + 10))
            title_bg.fill((0, 0, 0))
            title_bg.set_alpha(128)
            title_bg_rect = title_bg.get_rect()
            title_bg_rect.center = top3_title_rect.center

            self.window.blit(title_bg, title_bg_rect)
            self.window.blit(top3_title, top3_title_rect)

            for i, score_data in enumerate(top3_scores):
                score_text = self.font_small.render(
                    f"{i+1}. {score_data[1]} pts - {score_data[2]}", True, (255, 255, 255))
                score_rect = score_text.get_rect()
                score_rect.center = (
                    WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 175 + i * 20)

                score_bg = pygame.Surface(
                    (score_rect.width + 20, score_rect.height + 5))
                score_bg.fill((0, 0, 0))
                score_bg.set_alpha(128)
                score_bg_rect = score_bg.get_rect()
                score_bg_rect.center = score_rect.center

                self.window.blit(score_bg, score_bg_rect)
                self.window.blit(score_text, score_rect)

    def start(self):
        """ Main game loop """
        background = pygame.transform.scale(
            self.background, (WINDOW_WIDTH, WINDOW_HEIGHT))

        bird_group = pygame.sprite.Group()
        bird = Bird()
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
                        match self.game_state:
                            case self.MENU:
                                self.game_state = self.PLAYING
                                bird.rect.x = 100
                                bird.rect.y = 200
                                bird.speed = 0
                                self.current_score = 0
                                self.game_start_time = pygame.time.get_ticks()
                                self.last_time_bonus = 0
                                self.pipes_passed.clear()
                                pipe_group.empty()
                                for i in range(2):
                                    pipes = Pipe.get_random_pipes(
                                        WINDOW_WIDTH * i + 800)
                                    pipe_group.add(pipes[0])
                                    pipe_group.add(pipes[1])
                            case self.PLAYING:
                                bird.bump()
                            case self.GAME_OVER:
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
                        old_pipe_1 = pipe_group.sprites()[0]
                        old_pipe_2 = pipe_group.sprites()[1]
                        if hasattr(old_pipe_1, 'pipe_id'):
                            self.pipes_passed.discard(old_pipe_1.pipe_id)
                        if hasattr(old_pipe_2, 'pipe_id'):
                            self.pipes_passed.discard(old_pipe_2.pipe_id)

                        pipe_group.remove(old_pipe_1)
                        pipe_group.remove(old_pipe_2)
                        pipes = Pipe.get_random_pipes(WINDOW_WIDTH * 2)
                        pipe_group.add(pipes[0])
                        pipe_group.add(pipes[1])

                    ground_group.update()
                    bird_group.update()
                    pipe_group.update()

                    self.check_pipe_passed(bird, pipe_group)

                    self.check_time_bonus()

                    bird_group.draw(self.window)
                    pipe_group.draw(self.window)
                    ground_group.draw(self.window)

                    self.draw_score_and_time()

                    if (pygame.sprite.groupcollide(bird_group, ground_group, False, False, pygame.sprite.collide_mask)) or (pygame.sprite.groupcollide(bird_group, pipe_group, False, False, pygame.sprite.collide_mask)):
                        pygame.mixer.Sound(
                            'assets/audio/hit.ogg').play(loops=0, maxtime=0, fade_ms=0)
                        if self.is_gaming_music_playing:
                            self.gaming_music.stop()
                            self.is_gaming_music_playing = False
                        self.score_manager.save(self.current_score)
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
                        WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 30)

                    current_score_text = self.font_small.render(
                        f"Você pontuou: {self.current_score}", True, (255, 255, 255))
                    current_score_rect = current_score_text.get_rect()
                    current_score_rect.center = (
                        WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 10)

                    highest_score = self.score_manager.get_highest_score()
                    highest_score_text = self.font_small.render(
                        f"Maior pontuação: {highest_score}", True, (255, 255, 255))
                    highest_score_rect = highest_score_text.get_rect()
                    highest_score_rect.center = (
                        WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 30)

                    restart_text = self.font_small.render(
                        "Pressione ESPAÇO para voltar para a tela inicial", True, (255, 255, 255))
                    restart_rect = restart_text.get_rect()
                    restart_rect.center = (
                        WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 60)

                    text_bg = pygame.Surface(
                        (max(game_over_rect.width, restart_rect.width, current_score_rect.width, highest_score_rect.width) + 40, 120))
                    text_bg.fill((0, 0, 0))
                    text_bg.set_alpha(180)
                    text_bg_rect = text_bg.get_rect()
                    text_bg_rect.center = (
                        WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 15)

                    self.window.blit(text_bg, text_bg_rect)
                    self.window.blit(game_over_text, game_over_rect)
                    self.window.blit(current_score_text, current_score_rect)
                    self.window.blit(highest_score_text, highest_score_rect)
                    self.window.blit(restart_text, restart_rect)

            pygame.display.update()
