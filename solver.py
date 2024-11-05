from main import load_map

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
        "U": (-1, 0),
        "D": (1, 0),
        "L": (0, -1),
        "R": (0, 1)
    }

    valid_moves = []

    for step, (y, x) in moves.items():
        if state.workerCanMove(y, x) or state.workerCanPushBox(y, x):
            valid_moves.append(step)

    return valid_moves

def isDeadlock(state):
    boxListPosition = state.boxPosition()

    deadlock_conditions = [
        # Góc trên bên trái
        lambda box_y, box_x: (
                state.getMatrixElement(box_y, box_x - 1) in ['#', '$', '*'] and
                state.getMatrixElement(box_y - 1, box_x) in ['#', '$', '*'] and
                state.getMatrixElement(box_y - 1, box_x - 1) in ['#', '$', '*']
        ),
        # Góc trên bên phải
        lambda box_y, box_x: (
                state.getMatrixElement(box_y, box_x + 1) in ['#', '$', '*'] and
                state.getMatrixElement(box_y - 1, box_x) in ['#', '$', '*'] and
                state.getMatrixElement(box_y - 1, box_x + 1) in ['#', '$', '*']
        ),
        # Góc dưới bên trái
        lambda box_y, box_x: (
                state.getMatrixElement(box_y, box_x - 1) in ['#', '$', '*'] and
                state.getMatrixElement(box_y + 1, box_x) in ['#', '$', '*'] and
                state.getMatrixElement(box_y + 1, box_x - 1) in ['#', '$', '*']
        ),
        # Góc dưới bên phải
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

mapp = load_map("level1")
solve = Solve(mapp)
solve.printState()
print(isDeadlock(solve))
print(validMove(solve))