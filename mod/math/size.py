from __future__ import annotations

from .vector2 import Vector2
from typing import override


class Size(Vector2):
    def __init__(self, x: int = 0, y: int = 0) -> None:
        super().__init__(x, y)
        self.w = x
        self.h = y

    def __repr__(self) -> str:
        return f"Size(width='{self.x}', height='{self.y}')"

    @override
    @classmethod
    def rand(cls, limit_x: Vector2, limit_y: Vector2) -> Size:
        from random import randint

        x: int = randint(int(limit_x.x), int(limit_x.y))
        y: int = randint(int(limit_y.x), int(limit_y.y))
        return cls(x, y)
