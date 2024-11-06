import assets
import pygame.sprite
from layer import Layer

class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, *groups):
        self._layer = Layer.WALL
        self.image = assets.get_sprite("wall")
        if self.image is None:
            raise ValueError("Không tìm thấy sprite cho 'wall'")
        self.rect = self.image.get_rect(topleft=(x, y))
        super().__init__(*groups)