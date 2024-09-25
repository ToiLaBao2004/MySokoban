import os
import pygame

# Tạo dictionary để lưu trữ các sprite đã load
sprites = {}

# Hàm load tất cả sprite từ thư mục 'assets/sprites'
def load_sprites():
    # Xác định đường dẫn đến thư mục chứa sprite
    path = os.path.join("assets", "sprites")

    # Kiểm tra xem thư mục có tồn tại hay không
    if not os.path.exists(path):
        print(f"Thư mục {path} không tồn tại.")
        return

    # Duyệt qua tất cả các file trong thư mục sprite
    for file in os.listdir(path):
        try:
            # Lấy tên file không bao gồm phần mở rộng
            sprite_name = os.path.splitext(file)[0]

            # Load sprite bằng pygame và lưu vào dictionary 'sprites'
            sprites[sprite_name] = pygame.image.load(os.path.join(path, file))

        # Bắt lỗi nếu không thể load hình ảnh bằng pygame
        except pygame.error as e:
            print(f"Không thể tải hình ảnh {file}: {e}")

# Hàm trả về sprite theo tên
def get_sprite(name):
    # Lấy sprite từ dictionary dựa theo tên
    sprite = sprites.get(name)

    # Nếu không tìm thấy sprite, in thông báo lỗi
    if sprite is None:
        print(f"Không tìm thấy sprite: {name}")
    return sprite