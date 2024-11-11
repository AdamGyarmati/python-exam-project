from utils.utils import BEE_IMAGE, BEE_SOUND, BEE_MIN_SIZE, BEE_MAX_SIZE, BEE_BACKGROUND_SOUND, SCREEN_WIDTH, SCREEN_HEIGHT
from game_objects.game_object import GameObject, GameObjectMovement
import random, math
import pygame


class Bee(GameObject):
    def __init__(self):
        super().__init__(BEE_IMAGE, BEE_MIN_SIZE, BEE_MAX_SIZE, BEE_SOUND)
        self._speed = (
            abs(random.choice([-1, -2, -3, -4, -5]))
            if self._direction == GameObjectMovement.DOWN or self._direction == GameObjectMovement.RIGHT
            else random.choice([-1, -2, -3, -4, -5])
        )
        self.background_sound = pygame.mixer.Sound(BEE_BACKGROUND_SOUND)
        self.background_sound.set_volume(2)
        self._background_sound_playing = False
        self._sound.set_volume(0.3)
        self._wave_offset = 0

    def update(self):
        if self._direction == GameObjectMovement.DOWN or self._direction == GameObjectMovement.UP:
            self.rect.y += self._speed
            self._wave_offset += 0.1
            self.rect.x += int(10 * math.sin(self._wave_offset))
        else:
            self.rect.x += self._speed
            self._wave_offset += 0.1
            self.rect.y += int(10 * math.sin(self._wave_offset))

        self.play_background_sound()

    def play_background_sound(self):
        if self.rect.left < SCREEN_WIDTH and self.rect.right > 0 and self.rect.top < SCREEN_HEIGHT and self.rect.bottom > 0:
            # Start or continue playing the sound
            if self.background_sound and not self._background_sound_playing:
                self.background_sound.play(-1)  # -1 for looping
                self._background_sound_playing = True
        else:
            # Stop playing the sound if object is out of screen
            if self.background_sound and self._background_sound_playing:
                self.background_sound.stop()
                self._background_sound_playing = False
