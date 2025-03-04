from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from mod.objects.minimap import Map


class Coordinate:
    _map_ref: Map | None = None
    _msg: str = "Map reference is not set. Call Coordinate.set_map(map_instance) first."

    def __init__(self, x: float = 0, y: float = 0) -> None:
        if not self._map_ref:
            raise ValueError(self._msg)
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        return f"Coordinate(x='{self.x}', y='{self.y}')"

    def __iter__(self):
        yield self.get_x_pixel()
        yield self.get_y_pixel()

    def __add__(self, other: Coordinate) -> Coordinate:
        return self.__class__(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Coordinate) -> Coordinate:
        return self.__class__(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar: float) -> Coordinate:
        return self.__class__(self.x * scalar, self.y * scalar)

    def __truediv__(self, scalar: float) -> Coordinate:
        if scalar == 0:
            raise ValueError("Cannot divide by zero.")
        return self.__class__(self.x / scalar, self.y / scalar)

    def __neg__(self) -> Coordinate:
        return self.__class__(-self.x, -self.y)

    def __eq__(self, other: Coordinate) -> bool:  # type: ignore
        return self.x == other.x and self.y == other.y

    def abs(self) -> float:
        from math import sqrt

        return sqrt(self.x**2 + self.y**2)

    def normalize(self) -> Coordinate:
        return Coordinate(self.x / self.abs(), self.y / self.abs())

    def dot(self, other: Coordinate) -> float:
        return self.x * other.x + self.y * other.y

    def rot90(self) -> Coordinate:
        return Coordinate(-self.y, self.x)

    def get_x(self) -> float:
        return self.x

    def get_y(self) -> float:
        return self.y

    def get_x_pixel(self) -> int:
        return self._map_ref.to_pixel(self.x, self._map_ref.HORIZONTAL_GAB)  # type: ignore

    def get_y_pixel(self) -> int:
        return self._map_ref.to_pixel(self.y, self._map_ref.VERTICAL_GAB)  # type: ignore

    def clone(self) -> Coordinate:
        return self.__class__(self.x, self.y)

    @classmethod
    def set_map(cls, map_instance: Map) -> None:
        cls._map_ref = map_instance

    @classmethod
    def zero(cls) -> Coordinate:
        if not cls._map_ref:
            raise ValueError(cls._msg)

        return cls(0, 0)

    @classmethod
    def from_angle(cls, angle: float) -> Coordinate:
        if not cls._map_ref:
            raise ValueError(cls._msg)

        from math import cos, sin

        return cls(cos(angle), sin(angle))

    @classmethod
    def new(cls, x: float = 0, y: float = 0) -> Coordinate:
        if not cls._map_ref:
            raise ValueError(cls._msg)

        x_logical = cls._map_ref.to_grid(x, cls._map_ref.HORIZONTAL_GAB)
        y_logical = cls._map_ref.to_grid(y, cls._map_ref.HORIZONTAL_GAB)
        return cls(x_logical, y_logical)
