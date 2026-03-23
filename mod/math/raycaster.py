from math import ceil, copysign, floor

import pygame
from pygame import Surface

from mod.ext.constants import (
    INFINITY,
    PUSH_FACTOR,
    RES,
    WIN_HEIGHT,
    WIN_WIDTH,
)
from mod.math.coordinate import Coordinate
from mod.objects.minimap import Map
from mod.objects.player import Player
from mod.objects.scene import Scene


class Raycaster:
    def __init__(self, surface: Surface, map: Map, player: Player) -> None:
        self.surface = surface
        self.map = map
        self.player = player

    def __get_delta_t(self, p: float, dx: float) -> float:
        if dx > 0:
            return (ceil(p) - p) / dx
        elif dx < 0:
            return (floor(p) - p) / dx
        return INFINITY

    def __snap(self, p: float, delta: float) -> float:
        if delta > 0:
            return ceil(p) + copysign(PUSH_FACTOR, delta)
        if delta < 0:
            return floor(p) + copysign(PUSH_FACTOR, delta)
        return p + copysign(PUSH_FACTOR, delta)

    def __ray_step(self, p1: Coordinate, p2: Coordinate) -> Coordinate:
        d = p2 - p1

        tx = self.__get_delta_t(p2.x, d.x)
        ty = self.__get_delta_t(p2.y, d.y)

        if tx < ty:
            x = self.__snap(p2.x, d.x)
            y = p2.y + d.y * tx
        else:
            x = p2.x + d.x * ty
            y = self.__snap(p2.y, d.y)

        return Coordinate(x, y)

    def __cast_ray(self, p1: Coordinate, p2: Coordinate) -> Coordinate | None:
        p2 = self.__ray_step(p1, p2)  # Start at first intersection, not camera plane
        while self.map.is_insight(p2):
            if self.map.get_scene_cell(p2) >= 1:
                return p2
            p3 = self.__ray_step(p1, p2)
            p1, p2 = p2, p3
        return None

    def render(self):
        width = WIN_WIDTH / RES
        for x in range(RES):
            r1, r2 = self.player.get_fov_range()
            point_on_camera_plane = r1 + ((r2 - r1) * (x / RES))  # linear interpolation
            hit_point = self.__cast_ray(Coordinate(*self.player.position), point_on_camera_plane)
            if hit_point is not None:
                distance = hit_point - Coordinate(*self.player.position)
                perp_dist = Coordinate.from_angle(self.player.direction)
                height = WIN_HEIGHT / perp_dist.dot(distance)
                color = Scene.get_color(self.map.get_scene_cell(hit_point))
                pygame.draw.rect(
                    self.surface,
                    (*color, 255),
                    (x * width, (WIN_HEIGHT - height) * 0.5, width + 1, height),
                )
