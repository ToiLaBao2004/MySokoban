class Solve:
    def __init__(self, matrix):
        self.matrix = matrix
        self.pathSolution = ""

    def getMatrix(self):
        return self.matrix

    def getMatrixElement(self, y, x):
        return self.matrix[y][x]

    def setMatrixElement(self, y, x, object_map):
        self.matrix[y][x] = object_map

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
        new_y, new_x = self.workerPosition()[0] + y, self.workerPosition()[1] + x
        return self.getMatrixElement(new_y, new_x) not in ['#', '$', '*']

    def getElementNextStep(self, y, x):
        new_y, new_x = self.workerPosition()[0] + y, self.workerPosition()[1] + x
        return self.getMatrixElement(new_y, new_x)

    def workerCanPushBox(self, y, x):
        return self.getElementNextStep(y, x) in ['*', '&'] and self.getElementNextStep(y + y, x + x) in ['.', ' ']

    def isComplete(self):
        for y in self.matrix:
            for x in y:
                if x == '$':
                    return False
        return True

    def moveBox(self, y_box, x_box, move_y, move_x):
        box_position = self.getMatrixElement(y_box, x_box)
        next_box_position = self.getMatrixElement(y_box + move_y, x_box + move_x)
        if box_position == '$':
            if next_box_position == ' ':
                self.setMatrixElement(y_box, x_box, ' ')
                self.setMatrixElement(y_box + move_y, x_box + move_x, '$')
            elif next_box_position == '.':
                self.setMatrixElement(y_box, x_box, ' ')
                self.setMatrixElement(y_box + move_y, x_box + move_x, '*')
        elif box_position == '*':
            if next_box_position == ' ':
                self.setMatrixElement(y_box, x_box, '.')
                self.setMatrixElement(y_box + move_y, x_box + move_x, '$')
            elif next_box_position == '.':
                self.setMatrixElement(y_box, x_box, '.')
                self.setMatrixElement(y_box + move_y, x_box + move_x, '*')