from enum import IntEnum, auto

# Định nghĩa các lớp layer cho trò chơi
class Layer(IntEnum):
    # Các lớp sẽ được gán giá trị tự động (auto)
    FLOOR = auto()          # Layer của sàn (dưới cùng)
    DOCK = auto()           # Layer của vị trí đích (dock)
    WALL = auto()           # Layer của tường
    BOX = auto()            # Layer của hộp (box)
    BOX_DOCK = auto()       # Layer của hộp khi ở trên vị trí đích
    WORKER = auto()         # Layer của nhân vật chính (worker)
    WORKER_DOCK = auto()    # Layer của nhân vật chính khi ở trên vị trí đích