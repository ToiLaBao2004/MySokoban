import pygame
import assets
from game import Game

# Khởi tạo ma trận trò chơi từ chuỗi
A = """  #####
###   #
# $ # ##
# #  . #
#    # #
## #   #
 #@   ###
 #####"""

# Chuyển đổi chuỗi thành danh sách các danh sách (ma trận)
matrix = [list(row) for row in A.splitlines()]

# Tải các sprite từ thư viện assets
assets.load_sprites()

# Khởi tạo pygame và tạo đối tượng LayeredUpdates cho các sprite
pygame.init()
sprites = pygame.sprite.LayeredUpdates()

# Đặt tiêu đề cho cửa sổ trò chơi
pygame.display.set_caption("Sokoban")

# Khởi tạo đối tượng Game với ma trận đã tạo
gameSokoban = Game(matrix)

# Tính toán kích thước màn hình và tạo cửa sổ
size = gameSokoban.load_size()
screen = pygame.display.set_mode(size)

Game.fill_screen_with_floor(size, screen)

# Biến điều khiển vòng lặp trò chơi
running = True

# Vòng lặp chính của trò chơi
while running:
    # Vẽ trò chơi lên màn hình
    gameSokoban.print_game(screen)

    # Cập nhật màn hình
    pygame.display.flip()

    # Xử lý các sự kiện từ pygame
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Nếu người dùng đóng cửa sổ
            running = False  # Kết thúc vòng lặp

# Thoát khỏi pygame khi trò chơi kết thúc
pygame.quit()