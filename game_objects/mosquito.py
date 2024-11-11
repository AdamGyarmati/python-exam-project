from utils.utils import MOSQUITO_MIN_SIZE, MOSQUITO_MAX_SIZE, MOSQUITO_SOUND, MOSQUITO_IMAGE
from game_objects.game_object import GameObject, GameObjectMovement
import random


class Mosquito(GameObject):
    def __init__(self):
        super().__init__(MOSQUITO_IMAGE, MOSQUITO_MIN_SIZE, MOSQUITO_MAX_SIZE, MOSQUITO_SOUND)
        self._speed = (
            abs(random.choice([-1, -2, -3, -4, -5]))
            if self._direction == GameObjectMovement.DOWN or self._direction == GameObjectMovement.RIGHT
            else random.choice([-1, -2, -3, -4, -5])
        )
        self._sound.set_volume(0.1)

    def update(self):
        if self._direction == GameObjectMovement.DOWN or self._direction == GameObjectMovement.UP:
            self.rect.y += self._speed
        else:
            self.rect.x += self._speed
