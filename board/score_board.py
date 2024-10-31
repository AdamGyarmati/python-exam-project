import pygame
from utils.utils import TIMER_DURATION, FONT_SIZE, RED_COLOR, WHITE_COLOR, MINUS_SECOND_FOR_BEE, PLUS_SECOND_FOR_STINKY_BUG


class ScoreBoard:
    def __init__(self):
        self.font = pygame.font.Font(None, size=FONT_SIZE)
        self.score = 0
        self.time_penalty = 0

    def get_remaining_time(self, start_ticks):
        elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000
        self.remaining_time = TIMER_DURATION - elapsed_time + self.time_penalty
        return self.remaining_time

    def get_time_text(self):
        return self.font.render(f"Time left: {self.remaining_time:.1f}s", True, RED_COLOR)

    def get_score_text(self):
        return self.font.render(f"Score: {int(self.score)}", True, WHITE_COLOR)

    def increment_score(self):
        self.score += 1

    def decrement_score(self):
        self.score -= 1

    def increment_remaining_time(self):
        self.time_penalty += PLUS_SECOND_FOR_STINKY_BUG

    def decrement_remaining_time(self):
        self.time_penalty -= MINUS_SECOND_FOR_BEE
