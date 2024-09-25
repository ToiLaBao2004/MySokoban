import assets
import pygame.sprite
from layer import Layer

# Class Worker kế thừa từ pygame.sprite.Sprite
class Worker(pygame.sprite.Sprite):
    def __init__(self, x, y, *groups):
        # Gán layer cho đối tượng Worker (nhân vật chính) đúng với thứ tự hiển thị
        self._layer = Layer.WORKER

        # Lấy hình ảnh sprite cho nhân vật chính (worker) từ thư viện assets
        self.image = assets.get_sprite("worker")

        # Nếu không tìm thấy sprite tương ứng, raise lỗi
        if self.image is None:
            raise ValueError("Không tìm thấy sprite cho 'worker'")

        # Xác định vị trí và kích thước của hình ảnh (tọa độ topleft là vị trí bắt đầu)
        self.rect = self.image.get_rect(topleft=(x, y))

        # Gọi hàm khởi tạo của lớp cha pygame.sprite.Sprite để thêm đối tượng vào nhóm
        super().__init__(*groups)