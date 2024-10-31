from utils.utils import MOSQUITO_MIN_SIZE, MOSQUITO_MAX_SIZE, MOSQUITO_SOUND, MOSQUITO_IMAGE
from game_objects.game_object import GameObject, GameObjectMovement
import random


class Mosquito(GameObject):
    def __init__(self):
        super().__init__(MOSQUITO_IMAGE, MOSQUITO_MIN_SIZE, MOSQUITO_MAX_SIZE, MOSQUITO_SOUND)
        self.speed = (
            abs(random.choice([-1, -2, -3, -4, -5]))
            if self.position == GameObjectMovement.DOWN or self.position == GameObjectMovement.RIGHT
            else random.choice([-1, -2, -3, -4, -5])
        )

    def update(self):
        if self.position == GameObjectMovement.DOWN or self.position == GameObjectMovement.UP:
            self.rect.y += self.speed
        else:
            self.rect.x += self.speed
