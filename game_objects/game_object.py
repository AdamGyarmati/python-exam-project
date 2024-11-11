import pygame
import random
from enum import Enum, auto
from abc import ABC, abstractmethod
from utils.utils import SCREEN_WIDTH, SCREEN_HEIGHT


class GameObject(ABC, pygame.sprite.Sprite):
    def __init__(self, img_url: str, object_min_size, object_max_size, sound=None) -> None:
        super().__init__()
        image = pygame.image.load(img_url).convert_alpha()
        self._width_and_height = random.randint(object_min_size, object_max_size)
        self.image = pygame.transform.scale(image, (self._width_and_height, self._width_and_height))
        self._direction = random.choice([GameObjectMovement.DOWN, GameObjectMovement.LEFT, GameObjectMovement.RIGHT, GameObjectMovement.UP])
        self.is_alive = True
        self._sound = pygame.mixer.Sound(sound)
        self._background_sound = None
        self._init_rect()

    @abstractmethod
    def update(self):
        pass

    def play_sound(self):
        if self._sound:
            self._sound.play()

    def _init_rect(self):
        match self._direction:
            case GameObjectMovement.DOWN:
                self.rect = self.image.get_rect(center=(random.randint(self._width_and_height, SCREEN_WIDTH - self._width_and_height), -50))
            case GameObjectMovement.LEFT:
                self.rect = self.image.get_rect(
                    center=(SCREEN_WIDTH + 50, random.randint(self._width_and_height, SCREEN_HEIGHT - self._width_and_height))
                )
            case GameObjectMovement.UP:
                self.rect = self.image.get_rect(
                    center=(random.randint(self._width_and_height, SCREEN_WIDTH - self._width_and_height), SCREEN_HEIGHT + 50)
                )
            case GameObjectMovement.RIGHT:
                self.rect = self.image.get_rect(
                    center=(-50, random.randint(self._width_and_height, SCREEN_HEIGHT - self._width_and_height))
                )


class GameObjectMovement(Enum):
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()
    UP = auto()
