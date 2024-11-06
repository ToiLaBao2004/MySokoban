import os
import pygame

sprites = {}

def load_sprites():
    path = os.path.join("assets", "sprites")

    if not os.path.exists(path):
        print(f"Thư mục {path} không tồn tại.")
        return

    for file in os.listdir(path):
        try:
            sprite_name = os.path.splitext(file)[0]

            sprites[sprite_name] = pygame.image.load(os.path.join(path, file))

        except pygame.error as e:
            print(f"Không thể tải hình ảnh {file}: {e}")

def get_sprite(name):
    sprite = sprites.get(name)

    if sprite is None:
        print(f"Không tìm thấy sprite: {name}")
    return sprite