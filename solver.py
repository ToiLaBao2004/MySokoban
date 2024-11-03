from collections import deque

class Solver:
    def __init__(self, matrix):
        self.matrix = matrix

    def getPosition(self, state):
        for i, row in enumerate(state):
            for j, char in enumerate(row):
                if char == "@":
                    return i, j
        return None  # Trả về None nếu không tìm thấy

    def isComplete(self, state):
        return all(char != "$" for row in state for char in row)  # Kiểm tra tất cả các hộp

    def printState(self, state):
        # Hàm để in ra trạng thái giúp kiểm tra
        for row in state:
            print(" ".join(row))
        print()  # Thêm một dòng trống để dễ đọc

    def is_deadlock(self, state, box_x, box_y):
        # Kiểm tra xem hộp có bị kẹt hay không
        adjacent = [
            (box_x-1, box_y), (box_x+1, box_y),
            (box_x, box_y-1), (box_x, box_y+1)
        ]
        walls = sum(1 for x, y in adjacent if state[x][y] in ['#', '$'])
        return walls >= 2  # Nếu có 2 hoặc nhiều bức tường/hộp xung quanh

    def getNeighbor(self, state):
        neighbors = []
        cur_x, cur_y = self.getPosition(state)

        # Danh sách các dock trong trạng thái hiện tại
        dockList = [(i, j) for i, row in enumerate(state) for j, char in enumerate(row) if char == '.']

        # Các hướng di chuyển: lên, xuống, trái, phải
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        for dx, dy in directions:
            new_x, new_y = cur_x + dx, cur_y + dy

            # Kiểm tra xem có thể di chuyển đến vị trí (new_x, new_y) không
            if state[new_x][new_y] in [' ', '.']:  # Di chuyển đến ô trống hoặc dock
                new_state = self.updateState(state, cur_x, cur_y, new_x, new_y, dockList)
                neighbors.append(new_state)
            elif state[new_x][new_y] in ['$', '*']:  # Kiểm tra nếu có thể đẩy hộp
                box_x, box_y = new_x + dx, new_y + dy
                if state[box_x][box_y] in [' ', '.']:  # Kiểm tra vị trí sau hộp
                    new_state = self.updateState(state, cur_x, cur_y, new_x, new_y, dockList, box_x, box_y)
                    if not self.is_deadlock(new_state, box_x, box_y):
                        neighbors.append(new_state)

        return neighbors

    def updateState(self, state, cur_x, cur_y, new_x, new_y, dockList, box_x=None, box_y=None):
        new_state = [list(row) for row in state]  # Tạo bản sao sâu của trạng thái
        new_state[new_x][new_y] = '@'  # Cập nhật vị trí mới cho nhân vật
        new_state[cur_x][cur_y] = ' '  # Cập nhật vị trí cũ thành ô trống
        if box_x is not None and box_y is not None:  # Nếu có hộp được đẩy
            new_state[box_x][box_y] = '$' if state[box_x][box_y] == ' ' else '*'

        # Đảm bảo rằng dock không bị ghi đè
        for i, j in dockList:
            if new_state[i][j] not in ['*', '@']:
                new_state[i][j] = '.'

        return new_state

    def bfs(self):
        start_state = [list(row) for row in self.matrix]
        queue = deque([(start_state, [])])  # Hàng đợi lưu trữ các cặp (trạng thái, đường dẫn tới trạng thái)
        visited = set()
        visited.add(frozenset(tuple(row) for row in start_state))

        while queue:
            current_state, path = queue.popleft()

            if self.isComplete(current_state):
                return path

            for neighbor in self.getNeighbor(current_state):
                state_frozenset = frozenset(tuple(row) for row in neighbor)
                if state_frozenset not in visited:
                    visited.add(state_frozenset)
                    queue.append((neighbor, path + [neighbor]))

        return None  # Trả về None nếu không có giải pháp