from __future__ import annotations


class Vector2:
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        return f"Vector2(x='{self.x}', y='{self.y}')"

    def __add__(self, other: Vector2) -> Vector2:
        return self.__class__(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Vector2) -> Vector2:
        return self.__class__(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar: float) -> Vector2:
        return self.__class__(self.x * scalar, self.y * scalar)

    def __truediv__(self, scalar: float) -> Vector2:
        if scalar == 0:
            raise ValueError("Cannot divide by zero.")
        return self.__class__(self.x / scalar, self.y / scalar)

    def __neg__(self) -> Vector2:
        return self.__class__(-self.x, -self.y)

    def __eq__(self, other: Vector2) -> bool:  # type: ignore
        return self.x == other.x and self.y == other.y

    def __iter__(self):
        yield self.x
        yield self.y

    def abs(self) -> float:
        from math import sqrt

        return sqrt(self.x**2 + self.y**2)

    def normalize(self) -> Vector2:
        return Vector2(self.x / self.abs(), self.y / self.abs())

    def dot(self, other: Vector2) -> float:
        return self.x * other.x + self.y * other.y

    def clone(self) -> Vector2:
        return self.__class__(self.x, self.y)

    @classmethod
    def zero(cls) -> Vector2:
        return cls(0, 0)

    @classmethod
    def rand(cls, limit_x: Vector2, limit_y: Vector2) -> Vector2:
        from random import randint

        x: int = randint(int(limit_x.x), int(limit_x.y))
        y: int = randint(int(limit_y.x), int(limit_y.y))
        return cls(x, y)
