import assets
import pygame.sprite
from layer import *

class Box(pygame.sprite.Sprite):
    def __init__(self, x, y, *groups):
        self._layer = Layer.BOX

        self.image = assets.get_sprite("box_docked")

        if self.image is None:
            raise ValueError("Không tìm thấy sprite cho 'box_docked'")

        self.rect = self.image.get_rect(topleft=(x, y))

        super().__init__(*groups)