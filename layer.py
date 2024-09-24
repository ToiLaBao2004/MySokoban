from enum import IntEnum, auto

class Layer(IntEnum):
    BOX = auto()
    BOX_DOCK = auto()
    DOCK = auto()
    FLOOR = auto()
    WALL = auto()
    WORKER = auto()
    WORKER_DOCK = auto()