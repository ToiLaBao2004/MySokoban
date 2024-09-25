from objects.box import Box
from objects.box_docked import BoxDocked
from objects.dock import Dock
from objects.floor import Floor
from objects.wall import Wall
from objects.worker import Worker

class Game:
    def __init__(self, matrix):
        self.matrix = matrix

    def load_size(self):
        x = 0
        y = len(self.matrix)
        for row in self.matrix:
            if len(row) > x:
                x = len(row)
        return x * 64, y * 64

    def print_game(self, screen):
        screen.fill((255, 226, 191))
        x = 0
        y = 0
        for row in self.matrix:
            for char in row:
                if char == ' ':         #floor
                    floor = Floor(x, y)
                    screen.blit(floor.image, floor.rect)
                elif char == '#':       #wall
                    wall = Wall(x, y)
                    screen.blit(wall.image, wall.rect)
                elif char == '@':       #worker
                    worker = Worker(x, y)
                    screen.blit(worker.image, worker.rect)
                elif char == '.':       #dock
                    dock = Dock(x, y)
                    screen.blit(dock.image, dock.rect)
                elif char == '$':       #box
                    box = Box(x, y)
                    screen.blit(box.image, box.rect)
                elif char == '*':       #box on dock
                    box_docked = BoxDocked(x, y)
                    screen.blit(box_docked.image, box_docked.rect)
                elif char == '+':       #worker on dock
                    worker_dock = Worker(x, y)
                    screen.blit(worker_dock.image, worker_dock.rect)
                x = x + 64
            x = 0
            y = y + 64