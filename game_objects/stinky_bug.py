from utils.utils import STINKY_BUG_IMAGE, STINKY_BUG_MIN_SIZE, STINKY_BUG_MAX_SIZE, STINKY_BUG_SOUND
from game_objects.game_object import GameObject, GameObjectMovement
import random


class StinkyBug(GameObject):
    def __init__(self):
        super().__init__(STINKY_BUG_IMAGE, STINKY_BUG_MIN_SIZE, STINKY_BUG_MAX_SIZE, STINKY_BUG_SOUND)
        self._speed = (
            abs(random.choice([-5, -6, -7, -8, -9]))
            if self._direction == GameObjectMovement.DOWN or self._direction == GameObjectMovement.RIGHT
            else random.choice([-5, -6, -7, -8, -9])
        )
        self._sound.set_volume(0.3)

    def update(self):
        if self._direction == GameObjectMovement.DOWN or self._direction == GameObjectMovement.UP:
            self.rect.y += self._speed
        else:
            self.rect.x += self._speed
