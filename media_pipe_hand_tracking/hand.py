import pygame
from utils.utils import HAND_SIZE, HAND_IMAGE, SCREEN_WIDTH, SCREEN_HEIGHT
from media_pipe_hand_tracking.cv2_mediapipe import CV2_MediaPipe


class Hand(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        image = pygame.image.load(HAND_IMAGE).convert_alpha()
        self.image = pygame.transform.scale(image, (HAND_SIZE, HAND_SIZE))
        self._media_pipe = CV2_MediaPipe()
        self.rect = self.image.get_rect(center=(SCREEN_HEIGHT // 2, SCREEN_WIDTH // 2))

    def update(self):
        """CV2 coordinate gives to the pygame rect x y"""
        coordinates = self._media_pipe.get_hand_coordinate()
        if coordinates is not None:
            self.rect.center = coordinates

    def is_closed(self):
        return self._media_pipe.is_closed()
