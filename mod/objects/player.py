from pygame import Surface
from mod.math.coordinate import Coordinate
from mod.ext.constants import CAMERA_CAMERAPLANE_DISTANCE, CIRCLE_RADIUS
from mod.ext.func import strokeLine, fillCircle


class Player:
    def __init__(self, position: tuple[float, float], direction: float) -> None:
        self.position = position
        self.direction = direction

    def get_fov_range(self) -> list[Coordinate]:
        position = Coordinate(*self.position)
        p = position + (Coordinate.from_angle(self.direction) * CAMERA_CAMERAPLANE_DISTANCE)

        r1 = p - ((p - position).rot90().normalize())
        r2 = p + ((p - position).rot90().normalize())

        return [r1, r2]

    def render(self, surface: Surface):
        position = Coordinate(*self.position)
        fillCircle(surface, position, CIRCLE_RADIUS)

        p = position + (Coordinate.from_angle(self.direction) * CAMERA_CAMERAPLANE_DISTANCE)
        r1, r2 = self.get_fov_range()

        strokeLine(surface, p, r1)
        strokeLine(surface, p, r2)
        strokeLine(surface, position, r1)
        strokeLine(surface, position, r2)

        # l = tan(FOV * 0.5) * CAMERA_CAMERAPLANE_DISTANCE
