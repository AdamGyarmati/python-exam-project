import pygame
from utils.utils import HAND_SIZE, HAND_IMAGE, SCREEN_WIDTH, SCREEN_HEIGHT
from media_pipe_hand_tracking.cv2_mediapipe import CV2_MediaPipe


class Hand(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        image = pygame.image.load(HAND_IMAGE).convert_alpha()
        self.image = pygame.transform.scale(image, (HAND_SIZE, HAND_SIZE))
        self.rect = self.image.get_rect(center=(SCREEN_HEIGHT // 2, SCREEN_WIDTH // 2))
        self.media_pipe = CV2_MediaPipe()
        self.hand_coordinate_generator = self.media_pipe.get_hand_coordinate()

    def create_hand_coordinate_generator(self):
        """Létrehoz egy új hand_coordinate_generator-t."""
        self.hand_coordinate_generator = self.media_pipe.get_hand_coordinate()

    def update(self):
        """CV2 coordinate gives to the pygame rect x y"""
        try:
            coordinates = next(self.hand_coordinate_generator)
            if coordinates is not None:
                self.rect.center = coordinates
        except StopIteration:
            self.create_hand_coordinate_generator()

    def is_closed(self):
        return self.media_pipe.is_closed()
