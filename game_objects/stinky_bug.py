from utils.utils import STINKY_BUG_IMAGE, STINKY_BUG_MIN_SIZE, STINKY_BUG_MAX_SIZE, STINKY_BUG_SOUND
from game_objects.game_object import GameObject, GameObjectMovement
import random


class StinkyBug(GameObject):
    def __init__(self):
        super().__init__(STINKY_BUG_IMAGE, STINKY_BUG_MIN_SIZE, STINKY_BUG_MAX_SIZE, STINKY_BUG_SOUND)
        self.speed = (
            abs(random.choice([-5, -6, -7, -8, -9]))
            if self.position == GameObjectMovement.DOWN or self.position == GameObjectMovement.RIGHT
            else random.choice([-5, -6, -7, -8, -9])
        )

    def update(self):
        if self.position == GameObjectMovement.DOWN or self.position == GameObjectMovement.UP:
            self.rect.y += self.speed
        else:
            self.rect.x += self.speed
