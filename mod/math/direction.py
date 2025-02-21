from __future__ import annotations
from enum import Enum, auto


class Direction(Enum):
    RIGHT = auto()
    LEFT = auto()
    UP = auto()
    DOWN = auto()
    NONE = auto()

    @classmethod
    def get_from_num(cls, n: int) -> Direction:
        match n:
            case 0:
                return cls.RIGHT
            case 1:
                return cls.LEFT
            case 2:
                return cls.UP
            case 3:
                return cls.DOWN
            case _:
                return cls.NONE

    @classmethod
    def show_directions(cls):
        print("Available directions (choose a number):")
        for j, b in enumerate(Direction):
            print(f"{b.name + ':':<10} ({j})")
