from utils.utils import MOSQUITO_MIN_SIZE, MOSQUITO_MAX_SIZE, MOSQUITO_SOUND, MOSQUITO_IMAGE
from game_objects.game_object import GameObject, GameObjectMovement
import random


class Mosquito(GameObject):
    def __init__(self):
        super().__init__(MOSQUITO_IMAGE, MOSQUITO_MIN_SIZE, MOSQUITO_MAX_SIZE, MOSQUITO_SOUND)
        self.speed = (
            abs(random.choice([-1, -2, -3, -4, -5]))
            if self.direction == GameObjectMovement.DOWN or self.direction == GameObjectMovement.RIGHT
            else random.choice([-1, -2, -3, -4, -5])
        )
        self.sound.set_volume(0.1)

    def update(self):
        if self.direction == GameObjectMovement.DOWN or self.direction == GameObjectMovement.UP:
            self.rect.y += self.speed
        else:
            self.rect.x += self.speed
