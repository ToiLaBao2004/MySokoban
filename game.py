from objects.box import Box
from objects.box_docked import BoxDocked
from objects.dock import Dock
from objects.floor import Floor
from objects.wall import Wall
from objects.worker import Worker
import copy

class Game:
    def __init__(self, matrix, stack_matrix):
        self.matrix = matrix
        self.stack_matrix = stack_matrix

    def load_size(self):
        x = 0
        y = len(self.matrix)
        for row in self.matrix:
            if len(row) > x:
                x = len(row)
        return x * 64, y * 64

    def print_game(self, screen):
        x, y = 0, 0

        object_map = {
            '#': Wall,
            '@': Worker,
            '.': Dock,
            '$': Box,
            '*': BoxDocked,
        }

        for row in self.matrix:
            for char in row:
                if char in object_map:
                    obj = object_map[char](x, y)
                    screen.blit(obj.image, obj.rect)
                x += 64
            x = 0
            y += 64

    @staticmethod
    def fill_screen_with_floor(size, screen):
        screen_width, screen_height = size

        for x in range(0, screen_width, 64):
            for y in range(0, screen_height, 64):
                floor = Floor(x, y)
                screen.blit(floor.image, floor.rect)

    def is_completed(self, dock):
        for i, j in dock:
            if self.matrix[i][j] != "*":
                return False
        return True

    def getPosition(self):
        for i, row in enumerate(self.matrix):
            for j, char in enumerate(row):
                if char == "@":
                    return i, j

    def listDock(self):
        dockList = []
        for i, row in enumerate(self.matrix):
            for j, char in enumerate(row):
                if char == ".":
                    dockList.append((i, j))
        return dockList

    def canMove(self, x, y):
        return self.matrix[x][y] not in ["#", "$", "*"]

    def canPushBox(self, x, y):
        return self.matrix[x][y] not in ["#", "$", "*"]

    def update_position(self, old_x, old_y, new_x, new_y, symbol):
        self.matrix[old_x][old_y] = " "
        self.matrix[new_x][new_y] = symbol

    def next_move(self, x, y):
        cur_x, cur_y = self.getPosition()
        new_x, new_y = cur_x + x, cur_y + y
        self.update_position(cur_x, cur_y, new_x, new_y, "@")

    def move_box(self, x, y):
        cur_x, cur_y = self.getPosition()
        cur_box_x, cur_box_y = cur_x + x, cur_y + y
        new_box_x, new_box_y = cur_box_x + x, cur_box_y + y

        if self.canPushBox(new_box_x, new_box_y):
            self.update_position(cur_x, cur_y, cur_box_x, cur_box_y, "@")
            if self.matrix[new_box_x][new_box_y] == " ":
                self.matrix[new_box_x][new_box_y] = "$"
            elif self.matrix[new_box_x][new_box_y] == ".":
                self.matrix[new_box_x][new_box_y] = "*"

    def move(self, y, x, dock):
        self.stack_matrix.append(copy.deepcopy(self.matrix))
        cur_x, cur_y = self.getPosition()
        next_x, next_y = cur_x + y, cur_y + x

        if self.canMove(next_x, next_y):
            self.next_move(y, x)
        elif self.matrix[next_x][next_y] in ["*", "$"]:
            self.move_box(y, x)

        for i, j in dock:
            if self.matrix[i][j] not in ["*", "@"]:
                self.matrix[i][j] = "."

    def is_deadlock(self, box_x, box_y):
        if (self.matrix[box_x-1][box_y] in ['#', '$'] and self.matrix[box_x][box_y-1] in ['#', '$']) or \
           (self.matrix[box_x-1][box_y] in ['#', '$'] and self.matrix[box_x][box_y+1] in ['#', '$']) or \
           (self.matrix[box_x+1][box_y] in ['#', '$'] and self.matrix[box_x][box_y-1] in ['#', '$']) or \
           (self.matrix[box_x+1][box_y] in ['#', '$'] and self.matrix[box_x][box_y+1] in ['#', '$']):
            return True
        return False

    def check_all_boxes_for_deadlock(self):
        for i, row in enumerate(self.matrix):
            for j, char in enumerate(row):
                if char == '$':
                    if self.is_deadlock(i, j):
                        return True
        return False