from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from mod.objects.player import Player
    from mod.math.coordinate import Coordinate

from math import floor

import pygame
from pygame import Surface

from mod.ext.color import Color
from mod.objects.scene import Scene


class Map:
    def __init__(self, surface: Surface, scene: Scene, player: Player) -> None:
        self.surface = surface
        self.scene = scene
        self.player = player
        (
            self.grid_row,
            self.grid_col,
            self.grid_cell_size,
            self.HORIZONTAL_GAB,
            self.VERTICAL_GAB,
        ) = scene.get_info()

    def is_insight(self, p: Coordinate) -> bool:
        return 0 <= int(p.y) < self.grid_row and 0 <= int(p.x) < self.grid_col

    def get_cell(self, p: Coordinate) -> Coordinate:
        from mod.math.coordinate import Coordinate

        if not self.is_insight(p):
            raise ValueError(f"Coordinate must be insight defined map: `{p}`")

        return Coordinate(floor(p.x), floor(p.y))

    def get_scene_cell(self, p: Coordinate) -> int:
        if not self.is_insight(p):
            raise ValueError(f"Coordinate must be insight defined map: `{p}`")

        c = self.get_cell(p)
        return self.scene[int(c.y)][int(c.x)]

    def to_pixel(self, i: float, gab: int) -> int:
        return int(i * self.grid_cell_size + gab)

    def to_grid(self, pixel: float, gab: int) -> float:
        return (pixel - gab) / self.grid_cell_size

    def render_player(self):
        self.player.render(self.surface)

    def render_minimap(self):
        self.surface.fill((*Color.BASE,))

        for i in range(self.grid_row + 1):
            pos_y = self.to_pixel(i, self.VERTICAL_GAB)
            pygame.draw.line(
                self.surface,
                (*Color.RED,),
                (self.HORIZONTAL_GAB, pos_y),
                (self.HORIZONTAL_GAB + self.grid_cell_size * self.grid_col, pos_y),
            )

        for i in range(self.grid_col + 1):
            pos_x = self.to_pixel(i, self.HORIZONTAL_GAB)
            pygame.draw.line(
                self.surface,
                (*Color.RED,),
                (pos_x, self.VERTICAL_GAB),
                (pos_x, self.VERTICAL_GAB + self.grid_cell_size * self.grid_row),
            )

    def render_cells(self):
        for col in range(self.grid_col):
            for row in range(self.grid_row):
                if self.scene[row][col] >= 1:
                    x = self.to_pixel(col, self.HORIZONTAL_GAB) + 1
                    y = self.to_pixel(row, self.VERTICAL_GAB) + 1
                    w = self.grid_cell_size - 1
                    pygame.draw.rect(
                        self.surface,
                        (*Color.SURFACE2,),
                        ((x, y), (w, w)),
                    )
