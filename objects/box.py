import assets
import pygame.sprite
from layer import Layer

# Class Box, kế thừa từ pygame.sprite.Sprite
class Box(pygame.sprite.Sprite):
    def __init__(self, x, y, *groups):
        # Xác định lớp của đối tượng Box
        self._layer = Layer.BOX

        # Lấy hình ảnh sprite cho box từ assets
        self.image = assets.get_sprite("box")

        # Nếu không tìm thấy hình ảnh, báo lỗi
        if self.image is None:
            raise ValueError("Không tìm thấy sprite cho 'box'")

        # Xác định vị trí và kích thước của hình ảnh
        self.rect = self.image.get_rect(topleft=(x, y))

        # Gọi hàm khởi tạo của lớp cha pygame.sprite.Sprite
        super().__init__(*groups)