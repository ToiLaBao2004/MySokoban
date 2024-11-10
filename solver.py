import copy
import time
from collections import deque
import heapq

class Solve:
    def __init__(self, matrix):
        self.matrix = matrix
        self.pathSolution = ""
        self.dockListPosition = self.dockPosition()

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
    state_state = copy.deepcopy(game)
    node_generated += 1

    if isDeadlock(state_state):
        print("No Solution!")
        return "NoSol"

    queue = deque([state_state])
    visited = set()
    visited.add(tuple(map(tuple, state_state.getMatrix())))

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
    state_state = copy.deepcopy(game)
    node_generated += 1

    if isDeadlock(state_state):
        print("No Solution!")
        return "NoSol"

    stack = [state_state]
    visited = set()
    visited.add(tuple(map(tuple, state_state.getMatrix())))

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
    

def A(game):
    start = time.time()
    node_generated = 0
    initial_state = copy.deepcopy(game)
    node_generated += 1

    if isDeadlock(initial_state):
        print("No Solution!")
        return "NoSol"\
    
    priority_queue = []
    heapq.heappush(priority_queue, (0, initial_state))
    visited = set()
    visited.add(tuple(map(tuple, initial_state.getMatrix())))

    print("Processing A* Search......")

    while priority_queue:
        _, currState = heapq.heappop(priority_queue) # giá trị đầu tiên không được sử dụng

        if currState.isComplete():
            end = time.time()
            print("Time to find solution:", round(end - start, 2), "seconds")
            print("Number of visited nodes:", node_generated)
            print("Solution:", currState.pathSolution, "Number steps:", len(currState.pathSolution))
            return currState.pathSolution

        move = validMove(currState)
        for step in move:
            newState = copy.deepcopy(currState)
            node_generated += 1

            # Di chuyển dựa trên bước
            if step == 'U':
                newState.move(-1, 0)
            elif step == 'D':
                newState.move(1, 0)
            elif step == 'L':
                newState.move(0, -1)
            elif step == 'R':
                newState.move(0, 1)

            newState.pathSolution += step

            # Kiểm tra trạng thái mới có bị deadlock không và chưa từng được thăm
            if (tuple(map(tuple, newState.getMatrix())) not in visited) and (not isDeadlock(newState)):
                visited.add(tuple(map(tuple, newState.getMatrix())))
                
                # Tính toán hàm f(n) = g(n) + h(n)
                g = len(newState.pathSolution)  # Số bước từ trạng thái ban đầu đến trạng thái hiện tại
                h = heuristic(newState)  # Heuristic ước lượng chi phí đến đích
                f = g + h
                heapq.heappush(priority_queue, (f, newState))

    print(node_generated)
    print("No Solution!")
    return "NoSol"

def heuristic(state):
    box_positions = state.boxPosition()
    dock_positions = state.dockListPosition
    distance = 0
    
    # Tính tổng khoảng cách Manhattan từ mỗi hộp đến vị trí dock gần nhất
    for box_y, box_x in box_positions:
        min_dist = float('inf')
        for dock_y, dock_x in dock_positions:
            min_dist = min(min_dist, abs(box_y - dock_y) + abs(box_x - dock_x))
        distance += min_dist
    return distance
    
    
