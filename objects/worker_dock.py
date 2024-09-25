import assets
import pygame.sprite
from layer import *

class WorkerDock(pygame.sprite.Sprite):
    def __init__(self, x, y, *groups):
        self._layer = Layer.BOX

        self.image = assets.get_sprite("worker_dock")

        if self.image is None:
            raise ValueError("Không tìm thấy sprite cho 'worker_dock'")

        self.rect = self.image.get_rect(topleft=(x, y))

        super().__init__(*groups)