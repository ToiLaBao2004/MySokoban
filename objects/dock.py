import assets
import pygame.sprite
from layer import Layer

# Định nghĩa class Dock kế thừa từ pygame.sprite.Sprite
class Dock(pygame.sprite.Sprite):
    def __init__(self, x, y, *groups):
        # Gán layer cho đối tượng Dock (vị trí đích của hộp)
        self._layer = Layer.DOCK

        # Lấy hình ảnh sprite cho dock từ thư viện assets
        self.image = assets.get_sprite("dock")

        # Nếu không tìm thấy sprite tương ứng, raise lỗi
        if self.image is None:
            raise ValueError("Không tìm thấy sprite cho 'dock'")

        # Xác định vị trí và kích thước của hình ảnh (tọa độ topleft là vị trí bắt đầu)
        self.rect = self.image.get_rect(topleft=(x, y))

        # Gọi hàm khởi tạo của lớp cha pygame.sprite.Sprite để thêm đối tượng vào nhóm
        super().__init__(*groups)