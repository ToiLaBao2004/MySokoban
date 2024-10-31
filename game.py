from objects.box import Box
from objects.box_docked import BoxDocked
from objects.dock import Dock
from objects.floor import Floor
from objects.wall import Wall
from objects.worker import Worker
from objects.worker_dock import WorkerDock
import copy

class Game:
    def __init__(self, matrix, stack_matrix):
        # Khởi tạo ma trận để lưu trữ map trò chơi
        self.matrix = matrix
        self.stack_matrix = stack_matrix

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
                if char == '#':  # tường
                    wall = Wall(x, y)
                    screen.blit(wall.image, wall.rect)
                elif char == '@':  # công nhân
                    worker = Worker(x, y)
                    screen.blit(worker.image, worker.rect)
                elif char == '.':  # bến đỗ
                    dock = Dock(x, y)
                    screen.blit(dock.image, dock.rect)
                elif char == '$':  # thùng
                    box = Box(x, y)
                    screen.blit(box.image, box.rect)
                elif char == '*':  # thùng trên bến đỗ
                    box_docked = BoxDocked(x, y)
                    screen.blit(box_docked.image, box_docked.rect)
                elif char == '+':  # công nhân trên bến đỗ
                    worker_dock = WorkerDock(x, y)
                    screen.blit(worker_dock.image, worker_dock.rect)

                x += 64  # Di chuyển tọa độ x cho cột tiếp theo

            x = 0  # Reset tọa độ x về 0 cho hàng tiếp theo
            y += 64  # Di chuyển tọa độ y cho hàng tiếp theo

    @staticmethod  # Định nghĩa phương thức như phương thức tĩnh
    def fill_screen_with_floor(size, screen):
        screen_width, screen_height = size

        # Lặp qua các tọa độ trên màn hình để vẽ hình nền floor, step = 64 pixel
        for x in range(0, screen_width, 64):
            for y in range(0, screen_height, 64):
                floor = Floor(x, y)
                screen.blit(floor.image, floor.rect)  # Vẽ hình ảnh floor lên màn hình

    # Kiểm tra xem trò chơi đã hoàn thành chưa
    def is_completed(self, dock):
        for i, j in dock:
            if self.matrix[i][j] != "*":
                return False
        return True

    # Lấy vị trí của người chơi
    def getPosition(self):
        for i, row in enumerate(self.matrix):
            for j, char in enumerate(row):
                if char == "@":
                    return (i, j)

    # Lấy danh sách các điểm đích đến của thùng
    def listDock(self):
        dock = []
        for i, row in enumerate(self.matrix):
            for j, char in enumerate(row):
                if char == ".":
                    dock.append((i, j))
        return dock

    # Kiểm tra xem người chơi có thể đi vào ô đó hay không
    def canMove(self, x, y):
        return self.matrix[x][y] not in ["#", "$", "*"]

    # Kiểm tra xem thùng có thể được đẩy vào ô đó hay không
    def canPushBox(self, x, y):
        return self.matrix[x][y] not in ["#", "$", "*"]

    # Di chuyển khi không đẩy thùng
    def next_move(self, x, y):
        cur_x, cur_y = self.getPosition()
        new_x, new_y = cur_x + x, cur_y + y
        self.matrix[new_x][new_y] = "@"  # Cập nhật vị trí của công nhân
        self.matrix[cur_x][cur_y] = " "  # Xóa vị trí cũ của công nhân

    # Di chuyển và đẩy thùng
    def move_box(self, x, y):
        cur_peopleX, cur_peopleY = self.getPosition()
        cur_boxX, cur_boxY = cur_peopleX + x, cur_peopleY + y

        if self.canPushBox(cur_boxX + x, cur_boxY + y):
            self.matrix[cur_boxX][cur_boxY] = "@"  # Đặt công nhân vào vị trí mới của thùng

            new_boxX, new_boxY = cur_boxX + x, cur_boxY + y
            if self.matrix[new_boxX][new_boxY] == " ":
                self.matrix[new_boxX][new_boxY] = "$"  # Đặt thùng vào vị trí trống

            elif self.matrix[new_boxX][new_boxY] == ".":
                self.matrix[new_boxX][new_boxY] = "*"  # Đặt thùng lên bến đỗ

            self.matrix[cur_peopleX][cur_peopleY] = " "  # Xóa vị trí cũ của công nhân

    def move(self, x, y, dock):
        self.stack_matrix.append(copy.deepcopy(self.matrix))  # Lưu lại trạng thái hiện tại của ma trận
        cur_x, cur_y = self.getPosition()

        if self.canMove(cur_x + x, cur_y + y):
            self.next_move(x, y)  # Di chuyển công nhân nếu có thể
        elif self.matrix[cur_x + x][cur_y + y] in ["*", "$"]:
            self.move_box(x, y)  # Di chuyển và đẩy thùng nếu có thể

        for i, j in dock:
            if self.matrix[i][j] not in ["*", "@"]:
                self.matrix[i][j] = "."  # Cập nhật trạng thái bến đỗ