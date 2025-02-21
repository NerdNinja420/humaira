from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from mod.math.coordinate import Coordinate


import pygame
from pygame import Surface

from mod.ext.color import Color


def strokeLine(surface: Surface, start: Coordinate, end: Coordinate):
    pygame.draw.line(surface, (*Color.SKY,), (*start,), (*end,))


def fillCircle(surface: Surface, start: Coordinate, radius: int):
    pygame.draw.circle(surface, (*Color.FLAMINGO,), (*start,), radius)
