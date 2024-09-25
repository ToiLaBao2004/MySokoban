from objects.box import Box
from objects.box_docked import BoxDocked
from objects.dock import Dock
from objects.floor import Floor
from objects.wall import Wall
from objects.worker import Worker
from objects.worker_dock import WorkerDock

class Game:
    def __init__(self, matrix):
        # Khởi tạo ma trận để lưu trữ trạng thái trò chơi
        self.matrix = matrix

    def load_size(self):
        # Tính toán kích thước màn hình dựa trên ma trận
        x = 0
        y = len(self.matrix)
        for row in self.matrix:
            if len(row) > x:
                x = len(row)
        return x * 64, y * 64  # Trả về kích thước màn hình (chiều rộng, chiều cao)

    def print_game(self, screen):
        # Vẽ trò chơi lên màn hình
        x = 0
        y = 0
        for row in self.matrix:
            for char in row:
                # Vẽ các đối tượng tương ứng với ký tự trong ma trận
                if char == '#':    # wall
                    wall = Wall(x, y)
                    screen.blit(wall.image, wall.rect)
                elif char == '@':  # worker
                    worker = Worker(x, y)
                    screen.blit(worker.image, worker.rect)
                elif char == '.':  # dock
                    dock = Dock(x, y)
                    screen.blit(dock.image, dock.rect)
                elif char == '$':  # box
                    box = Box(x, y)
                    screen.blit(box.image, box.rect)
                elif char == '*':  # box on dock
                    box_docked = BoxDocked(x, y)
                    screen.blit(box_docked.image, box_docked.rect)
                elif char == '+':  # worker on dock
                    worker_dock = WorkerDock(x, y)
                    screen.blit(worker_dock.image, worker_dock.rect)

                x += 64  # Di chuyển tọa độ x cho cột tiếp theo
            x = 0  # Reset tọa độ x về 0 cho hàng tiếp theo
            y += 64  # Di chuyển tọa độ y cho hàng tiếp theo

    @staticmethod  # Định nghĩa phương thức như phương thức tĩnh
    def fill_screen_with_floor(size, screen):
        screen_width, screen_height = size

        # Lặp qua các tọa độ trên màn hình để vẽ hình nền floor step = 64pixel
        for x in range(0, screen_width, 64):
            for y in range(0, screen_height, 64):
                floor = Floor(x, y)
                screen.blit(floor.image, floor.rect)  # Vẽ hình ảnh floor lên màn hình