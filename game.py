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
        x, y = 0, 0

        object_map = {
            '#': Wall,
            '@': Worker,
            '.': Dock,
            '$': Box,
            '*': BoxDocked,
            '+': WorkerDock
        }

        for row in self.matrix:
            for char in row:
                if char in object_map:
                    obj = object_map[char](x, y)
                    screen.blit(obj.image, obj.rect)
                x += 64
            x = 0
            y += 64

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
                    return i, j

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

    # Hàm cập nhật vị trí trong ma trận
    def update_position(self, old_x, old_y, new_x, new_y, symbol):
        self.matrix[old_x][old_y] = " "  # Xóa vị trí cũ
        self.matrix[new_x][new_y] = symbol  # Đặt ký tự mới tại vị trí mới

    # Di chuyển công nhân mà không đẩy thùng
    def next_move(self, x, y):
        cur_x, cur_y = self.getPosition()
        new_x, new_y = cur_x + x, cur_y + y
        self.update_position(cur_x, cur_y, new_x, new_y, "@")  # Cập nhật vị trí công nhân

    # Di chuyển và đẩy thùng
    def move_box(self, x, y):
        cur_x, cur_y = self.getPosition()
        cur_box_x, cur_box_y = cur_x + x, cur_y + y  # Vị trí của thùng
        new_box_x, new_box_y = cur_box_x + x, cur_box_y + y  # Vị trí mới của thùng

        # Kiểm tra nếu thùng có thể đẩy đến vị trí mới
        if self.canPushBox(new_box_x, new_box_y):
            # Di chuyển công nhân đến vị trí thùng và cập nhật vị trí thùng
            self.update_position(cur_x, cur_y, cur_box_x, cur_box_y, "@")
            if self.matrix[new_box_x][new_box_y] == " ":
                self.matrix[new_box_x][new_box_y] = "$"  # Đặt thùng vào vị trí trống
            elif self.matrix[new_box_x][new_box_y] == ".":
                self.matrix[new_box_x][new_box_y] = "*"  # Đặt thùng lên bến đỗ

    # Thực hiện di chuyển dựa trên trạng thái hiện tại
    def move(self, x, y, dock):
        # Lưu lại trạng thái hiện tại của ma trận để có thể hoàn tác
        self.stack_matrix.append(copy.deepcopy(self.matrix))
        cur_x, cur_y = self.getPosition()
        next_x, next_y = cur_x + x, cur_y + y

        # Kiểm tra xem công nhân có thể di chuyển mà không đẩy thùng
        if self.canMove(next_x, next_y):
            self.next_move(x, y)
        elif self.matrix[next_x][next_y] in ["*", "$"]:
            # Nếu có thùng ở vị trí tiếp theo, cố gắng di chuyển và đẩy thùng
            self.move_box(x, y)

        # Cập nhật lại trạng thái của các điểm đích
        for i, j in dock:
            if self.matrix[i][j] not in ["*", "@"]:
                self.matrix[i][j] = "."

    # Kiểm tra xem có thùng nào bị deadlock không
    def is_deadlock(self, box_x, box_y):
        # Kiểm tra nếu thùng bị kẹt ở góc giữa hai bức tường hoặc giữa bức tường và thùng khác
        if (self.matrix[box_x-1][box_y] in ['#', '$'] and self.matrix[box_x][box_y-1] in ['#', '$']) or \
           (self.matrix[box_x-1][box_y] in ['#', '$'] and self.matrix[box_x][box_y+1] in ['#', '$']) or \
           (self.matrix[box_x+1][box_y] in ['#', '$'] and self.matrix[box_x][box_y-1] in ['#', '$']) or \
           (self.matrix[box_x+1][box_y] in ['#', '$'] and self.matrix[box_x][box_y+1] in ['#', '$']):
            return True
        return False

    # Kiểm tra tất cả các thùng xem có thùng nào bị deadlock không
    def check_all_boxes_for_deadlock(self):
        for i, row in enumerate(self.matrix):
            for j, char in enumerate(row):
                if char == '$':  # Nếu gặp thùng
                    if self.is_deadlock(i, j):
                        return True  # Nếu có ít nhất một thùng bị deadlock, trả về True
        return False  # Không có thùng nào bị deadlock