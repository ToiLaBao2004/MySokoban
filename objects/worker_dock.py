import assets
import pygame.sprite
from layer import Layer

# Class WorkerDock kế thừa từ pygame.sprite.Sprite
class WorkerDock(pygame.sprite.Sprite):
    def __init__(self, x, y, *groups):
        # Gán layer cho đối tượng WorkerDock (nhân vật chính khi ở vị trí đích) đúng với thứ tự hiển thị
        self._layer = Layer.WORKER_DOCK

        # Lấy hình ảnh sprite cho nhân vật chính khi ở vị trí đích (worker_dock) từ thư viện assets
        self.image = assets.get_sprite("worker_dock")

        # Nếu không tìm thấy sprite tương ứng, raise lỗi
        if self.image is None:
            raise ValueError("Không tìm thấy sprite cho 'worker_dock'")

        # Xác định vị trí và kích thước của hình ảnh (tọa độ topleft là vị trí bắt đầu)
        self.rect = self.image.get_rect(topleft=(x, y))

        # Gọi hàm khởi tạo của lớp cha pygame.sprite.Sprite để thêm đối tượng vào nhóm
        super().__init__(*groups)