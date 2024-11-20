import copy
import time
import queue
from collections import deque
import math
import random

class Solve:
    def __init__(self, matrix):
        self.matrix = matrix
        self.pathSolution = ""
        self.dockListPosition = self.dockPosition()
        self.heuristic = 0

    def __lt__(self,other):
        return self.heuristic < other.heuristic

    def getMatrix(self):
        return self.matrix

    def getMatrixElement(self, y, x):
        return self.matrix[y][x]

    def setMatrixElement(self, y, x, object_map):
        self.matrix[y][x] = object_map

    def getElementNextStep(self, y, x):
        new_y, new_x = self.workerPosition()[0] + y, self.workerPosition()[1] + x
        return self.getMatrixElement(new_y, new_x)

    def workerPosition(self):
        for y, row in enumerate(self.matrix):
            for x, char in enumerate(row):
                if char == '@':
                    return y, x

    def boxPosition(self):
        boxListPosition = []
        for y, row in enumerate(self.matrix):
            for x, char in enumerate(row):
                if char == '$':
                    boxListPosition.append((y, x))
        return boxListPosition

    def dockPosition(self):
        dockListPosition = []
        for y, row in enumerate(self.matrix):
            for x, char in enumerate(row):
                if char == '.':
                    dockListPosition.append((y, x))
        return dockListPosition
    
    def workerCanMove(self, y, x):
        return self.getElementNextStep(y, x) in [' ', '.']

    def workerCanPushBox(self, y, x):
        return self.getElementNextStep(y, x) in ['*', '$'] and self.getElementNextStep(y + y, x + x) in ['.', ' ']

    def isComplete(self):
        for y in self.matrix:
            for x in y:
                if x == '$':
                    return False
        return True

    def moveBox(self, y_box, x_box, move_y, move_x):
        box_element = self.getMatrixElement(y_box, x_box)
        next_box_element = self.getMatrixElement(y_box + move_y, x_box + move_x)
        if box_element == '$':
            if next_box_element == ' ':
                self.setMatrixElement(y_box, x_box, ' ')
                self.setMatrixElement(y_box + move_y, x_box + move_x, '$')
            elif next_box_element == '.':
                self.setMatrixElement(y_box, x_box, ' ')
                self.setMatrixElement(y_box + move_y, x_box + move_x, '*')
        elif box_element == '*':
            if next_box_element == ' ':
                self.setMatrixElement(y_box, x_box, '.')
                self.setMatrixElement(y_box + move_y, x_box + move_x, '$')
            elif next_box_element == '.':
                self.setMatrixElement(y_box, x_box, '.')
                self.setMatrixElement(y_box + move_y, x_box + move_x, '*')

    def move(self, y, x):
        if self.workerCanMove(y, x):
            worker_position = self.workerPosition()
            self.setMatrixElement(worker_position[0] + y, worker_position[1] + x, '@')
            self.setMatrixElement(worker_position[0], worker_position[1], ' ')
        elif self.workerCanPushBox(y, x):
            worker_position = self.workerPosition()
            self.moveBox(worker_position[0] + y, worker_position[1] + x, y, x)
            self.setMatrixElement(worker_position[0] + y, worker_position[1] + x, '@')
            self.setMatrixElement(worker_position[0], worker_position[1], ' ')

        for i, j in self.dockListPosition:
            if self.getMatrixElement(i, j) not in ['*', '@']:
                self.setMatrixElement(i, j, '.')

    def printState(self):
        for row in self.matrix:
            print(" ".join(row))
        print()

def validMove(state):
    moves = {
        'U': (-1, 0),
        'D': (1, 0),
        'L': (0, -1),
        'R': (0, 1)
    }

    valid_moves = []

    for step, (y, x) in moves.items():
        if state.workerCanMove(y, x) or state.workerCanPushBox(y, x):
            valid_moves.append(step)

    return valid_moves

def box_toDock(state):
    sum = 0
    box_list = state.boxPosition()
    dock_list = state.dockPosition()
    for box in box_list:
        min_distance = float('inf')
        for dock in dock_list:
            distance = (abs(dock[0] - box[0]) + abs(dock[1] - box[1]))
            if distance < min_distance:
                min_distance = distance
        sum += min_distance
    return sum

def worker_toBox(state):
    sum = 0
    box_list = state.boxPosition()
    woker_pos = state.workerPosition()
    for box in box_list:
        sum += abs(box[0] - woker_pos[0]) + abs(box[1] - woker_pos[1])
    return sum

def isDeadlock(state):
    boxListPosition = state.boxPosition()

    deadlock_conditions = [
        # Goc tren ben trai
        lambda box_y, box_x: (
                state.getMatrixElement(box_y, box_x - 1) in ['#', '$', '*'] and
                state.getMatrixElement(box_y - 1, box_x) in ['#', '$', '*'] and
                state.getMatrixElement(box_y - 1, box_x - 1) in ['#', '$', '*']
        ),
        # Goc tren ben phai
        lambda box_y, box_x: (
                state.getMatrixElement(box_y, box_x + 1) in ['#', '$', '*'] and
                state.getMatrixElement(box_y - 1, box_x) in ['#', '$', '*'] and
                state.getMatrixElement(box_y - 1, box_x + 1) in ['#', '$', '*']
        ),
        # Goc duoi ben trai
        lambda box_y, box_x: (
                state.getMatrixElement(box_y, box_x - 1) in ['#', '$', '*'] and
                state.getMatrixElement(box_y + 1, box_x) in ['#', '$', '*'] and
                state.getMatrixElement(box_y + 1, box_x - 1) in ['#', '$', '*']
        ),
        # Goc duoi ben phai
        lambda box_y, box_x: (
                state.getMatrixElement(box_y, box_x + 1) in ['#', '$', '*'] and
                state.getMatrixElement(box_y + 1, box_x) in ['#', '$', '*'] and
                state.getMatrixElement(box_y + 1, box_x + 1) in ['#', '$', '*']
        ),
    ]

    for box in boxListPosition:
        y, x = box

        if any(condition(y, x) for condition in deadlock_conditions):
            return True

    return False

def bfs(game):
    start = time.time()
    node_generated = 0
    start_state = copy.deepcopy(game)
    node_generated += 1

    if isDeadlock(start_state):
        print("No Solution!")
        return "NoSol"

    queue = deque([start_state])
    visited = set()
    visited.add(tuple(map(tuple, start_state.getMatrix())))

    print("Processing BFS......")

    while queue:
        currState = queue.popleft()
        move = validMove(currState)
        for step in move:
            newState = copy.deepcopy(currState)
            node_generated += 1

            if step == 'U':
                newState.move(-1, 0)
            elif step == 'D':
                newState.move(1, 0)
            elif step == 'L':
                newState.move(0, -1)
            elif step == 'R':
                newState.move(0, 1)

            newState.pathSolution += step

            if newState.isComplete():
                end = time.time()
                print("Time to find solution:", round(end - start, 2), "seconds")
                print("Number of visited nodes:", node_generated)
                print("Solution:", newState.pathSolution, "Number steps:", len(newState.pathSolution))
                return newState.pathSolution

            if (tuple(map(tuple, newState.getMatrix())) not in visited) and (not isDeadlock(newState)):
                queue.append(newState)
                visited.add(tuple(map(tuple, newState.getMatrix())))

    print(node_generated)
    print("No Solution!")
    return "NoSol"

def dfs(game):
    start = time.time()
    node_generated = 0
    start_state = copy.deepcopy(game)
    node_generated += 1

    if isDeadlock(start_state):
        print("No Solution!")
        return "NoSol"

    stack = [start_state]
    visited = set()
    visited.add(tuple(map(tuple, start_state.getMatrix())))

    print("Processing DFS......")

    while stack:
        currState = stack.pop()
        move = validMove(currState)
        for step in move:
            newState = copy.deepcopy(currState)
            node_generated += 1

            if step == 'U':
                newState.move(-1, 0)
            elif step == 'D':
                newState.move(1, 0)
            elif step == 'L':
                newState.move(0, -1)
            elif step == 'R':
                newState.move(0, 1)

            newState.pathSolution += step

            if newState.isComplete():
                end = time.time()
                print("Time to find solution:", round(end - start, 2), "seconds")
                print("Number of visited nodes:", node_generated)
                print("Solution:", newState.pathSolution, "Number steps:", len(newState.pathSolution))
                return newState.pathSolution

            if (tuple(map(tuple, newState.getMatrix())) not in visited) and (not isDeadlock(newState)):
                stack.append(newState)
                visited.add(tuple(map(tuple, newState.getMatrix())))

    print(node_generated)
    print("No Solution!")
    return "NoSol"


def astar(game):
    start = time.time()
    node_generated = 0
    start_state = copy.deepcopy(game)
    node_generated += 1
    start_state.heuristic = worker_toBox(start_state) + box_toDock(start_state)
    
    if isDeadlock(start_state):
        print("No Solution!")
        return "NoSol"
    
    open_list = queue.PriorityQueue()
    open_list.put(start_state)
    close_list = set()
    print("Processing A*......")
    
    while not open_list.empty():
        cur_state = open_list.get()
        move = validMove(cur_state)
        close_list.add(tuple(map(tuple, cur_state.getMatrix())))
        
        for step in move:
            new_state = copy.deepcopy(cur_state)
            node_generated += 1

            if step == 'U':
                new_state.move(-1, 0)
            elif step == 'D':
                new_state.move(1, 0)
            elif step == 'L':
                new_state.move(0, -1)
            elif step == 'R':
                new_state.move(0, 1)

            new_state.pathSolution += step
            new_state.heuristic = worker_toBox(new_state) + box_toDock(new_state)

            if new_state.isComplete():
                end = time.time()
                print("Time to find solution:", round(end - start, 2), "seconds")
                print("Number of visited nodes:", node_generated)
                print("Solution:", new_state.pathSolution, "Number steps:", len(new_state.pathSolution))
                return new_state.pathSolution

            if (tuple(map(tuple, new_state.getMatrix())) not in close_list) and not isDeadlock(new_state):
                open_list.put(new_state)

    print(node_generated)
    print("No Solution!")
    return "NoSol"


def backtracking(game):
    start = time.time()
    node_generated = 0
    start_state = copy.deepcopy(game)
    visited = set()

    if isDeadlock(start_state):
        print("No Solution!")
        return "NoSol"

    print("Processing backtracking*......")
    
    def solve(state):
        nonlocal node_generated

        # Nếu hoàn thành, trả về đường đi
        if state.isComplete():
            return state.pathSolution

        # Lưu trạng thái vào visited
        visited.add(tuple(map(tuple, state.getMatrix())))

        # Thử từng bước đi khả dụng
        for step in validMove(state):
            newState = copy.deepcopy(state)
            node_generated += 1

            # Thực hiện bước đi
            if step == 'U':
                newState.move(-1, 0)
            elif step == 'D':
                newState.move(1, 0)
            elif step == 'L':
                newState.move(0, -1)
            elif step == 'R':
                newState.move(0, 1)

            newState.pathSolution += step

            # Kiểm tra deadlock hoặc trạng thái đã ghé qua
            if tuple(map(tuple, newState.getMatrix())) in visited or isDeadlock(newState):
                continue

            # Đệ quy tìm giải pháp từ trạng thái mới
            solutionPath = solve(newState)
            if solutionPath:  # Nếu tìm được giải pháp, trả về
                return solutionPath

        # Không tìm thấy đường đi, quay lui
        return None

    # Bắt đầu giải bài toán
    solution = solve(start_state)
    end = time.time()

    if solution:
        print("Time to find solution:", round(end - start, 2), "seconds")
        print("Number of visited nodes:", node_generated)
        print("Solution:", solution, "Number steps:", len(solution))
        return solution
    else:
        print("No Solution!")
        return "NoSol"
    
def simulated_annealing(game, initial_temperature=1000, cooling_rate=0.95, max_iterations=1000):
    start = time.time()
    node_generated = 0

    # Sao chép trạng thái ban đầu
    current_state = copy.deepcopy(game)
    node_generated += 1

    # Đặt nhiệt độ ban đầu
    temperature = initial_temperature

    # Đường đi tốt nhất và heuristic ban đầu
    best_path = ""
    best_heuristic = worker_toBox(current_state) + box_toDock(current_state)

    print("Processing Simulated Annealing......")

    for _ in range(max_iterations):
        # Kiểm tra nếu đã hoàn thành
        if current_state.isComplete():
            end = time.time()
            print("Time to find solution:", round(end - start, 2), "seconds")
            print("Number of visited nodes:", node_generated)
            print("Solution:", best_path, "Number steps:", len(best_path))
            return best_path

        # Lấy tất cả các nước đi hợp lệ
        moves = validMove(current_state)
        if not moves:
            break

        # Chọn ngẫu nhiên một bước đi
        step = random.choice(moves)
        next_state = copy.deepcopy(current_state)
        node_generated += 1

        # Thực hiện bước đi
        if step == 'U':
            next_state.move(-1, 0)
        elif step == 'D':
            next_state.move(1, 0)
        elif step == 'L':
            next_state.move(0, -1)
        elif step == 'R':
            next_state.move(0, 1)

        # Tính heuristic của trạng thái tiếp theo
        next_heuristic = worker_toBox(next_state) + box_toDock(next_state)

        # Tính toán xác suất chọn trạng thái kém hơn
        delta = next_heuristic - best_heuristic
        if delta < 0 or random.uniform(0, 1) < math.exp(-delta / temperature):
            current_state = next_state
            best_path += step
            best_heuristic = next_heuristic

        # Giảm nhiệt độ
        temperature *= cooling_rate

    print("No Solution Found!")
    return "NoSol"