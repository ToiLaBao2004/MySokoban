import assets
import pygame.sprite
from layer import Layer

# Class BoxDocked kế thừa từ pygame.sprite.Sprite
class BoxDocked(pygame.sprite.Sprite):
    def __init__(self, x, y, *groups):
        # Xác định layer của đối tượng BoxDocked (hộp đã đến vị trí đích)
        self._layer = Layer.BOX_DOCK

        # Lấy hình ảnh sprite cho box đã đến vị trí đích từ thư viện assets
        self.image = assets.get_sprite("box_docked")

        # Nếu không tìm thấy sprite tương ứng, raise lỗi
        if self.image is None:
            raise ValueError("Không tìm thấy sprite cho 'box_docked'")

        # Xác định vị trí và kích thước của hình ảnh (tọa độ topleft là vị trí bắt đầu)
        self.rect = self.image.get_rect(topleft=(x, y))

        # Gọi hàm khởi tạo của lớp cha pygame.sprite.Sprite để thêm đối tượng vào nhóm
        super().__init__(*groups)