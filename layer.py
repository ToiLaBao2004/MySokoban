from enum import IntEnum, auto

class Layer(IntEnum):
    FLOOR = auto()
    DOCK = auto()
    WALL = auto()
    BOX = auto()
    BOX_DOCK = auto()
    WORKER = auto()
    WORKER_DOCK = auto()