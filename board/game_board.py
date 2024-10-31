import pygame
from utils.utils import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    GAMEBOARD_BACKGROUND,
    GAMEBOARD_SOUND,
    BLACK_COLOR,
    FONT_SIZE,
    GREEN_COLOR,
    WHITE_COLOR,
    HOVER_GREEN_COLOR,
)
from game_objects.game_object import GameObject
from board.score_board import ScoreBoard


class GameBoard:
    _instance = None

    def __new__(cls, name):
        """We don't need more than 1 gameboard, so we use singleton pattern."""
        if cls._instance is None:
            cls._instance = super(GameBoard, cls).__new__(cls)
        return cls._instance

    def __init__(self, name):
        self.initialized_module, self.failed_module = pygame.init()
        self.name = name
        pygame.display.set_caption(self.name)
        self.background = pygame.transform.scale(surface=pygame.image.load(GAMEBOARD_BACKGROUND), size=(SCREEN_WIDTH, SCREEN_HEIGHT))
        self.is_running = True
        self.screen = pygame.display.set_mode(size=(SCREEN_WIDTH, SCREEN_HEIGHT), flags=pygame.SHOWN, depth=32)
        self._game_objects_sprites = pygame.sprite.Group()
        self.score_board = ScoreBoard()
        self.sound = pygame.mixer.Sound(GAMEBOARD_SOUND)
        self.sound.play()
        self.font = pygame.font.Font(None, size=FONT_SIZE)

    def draw_start_screen(self, mouse_pos):
        button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 125, SCREEN_HEIGHT // 2 - 42, 250, 80)

        if button_rect.collidepoint(mouse_pos):
            current_button_color = HOVER_GREEN_COLOR
        else:
            current_button_color = GREEN_COLOR

        self.screen.blit(self.background, (0, 0))
        pygame.draw.rect(self.screen, current_button_color, button_rect, border_radius=15)
        start_text = self.font.render("Start Game", True, BLACK_COLOR)
        start_rect = start_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(start_text, start_rect)
        pygame.display.flip()
        return start_rect

    def draw_end_screen(self):
        self.screen.fill((0, 0, 0))  # Fekete háttér a vég képernyőhöz
        end_text = self.font.render(f"Game Over! Score: {int(self.score_board.score)}", True, WHITE_COLOR)  # Fehér szöveg
        text_rect = end_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(end_text, text_rect)
        pygame.display.flip()  # Frissítjük a képernyőt

    def update_screen(self):
        self.screen.blit(self.background, (0, 0))

        # Render timer text
        timer_text = self.score_board.get_time_text()
        self.screen.blit(timer_text, (SCREEN_WIDTH - 260, 10))  # Jobb felső sarok

        # Render score text
        score_text = self.score_board.get_score_text()
        self.screen.blit(score_text, (5, 5))  # Bal felső sarok

    def update_sprites(self):
        self._game_objects_sprites.update()

    def draw_sprites(self):
        self._game_objects_sprites.draw(self.screen)

    def display_sprites(self):
        pygame.display.flip()
        pygame.time.delay(10)

    def get_game_objects_sprites(self):
        """Make a copy of private game_objects_sprites"""
        return pygame.sprite.Group(self._game_objects_sprites)

    def add_game_object(self, game_object: GameObject):
        self._game_objects_sprites.add(game_object)

    def remove_game_object(self, game_object: GameObject):
        self._game_objects_sprites.remove(game_object)

    def check_score_board_timer_up(self, start_ticks):
        if self.score_board.get_remaining_time(start_ticks) <= 0:
            self.is_running = False
