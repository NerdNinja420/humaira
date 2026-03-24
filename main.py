from math import pi

import pygame
import numpy as np
from pygame.locals import QUIT

from mod.ext.color import Color
from mod.objects.scene import Scene
from mod.objects.minimap import Map
from mod.objects.player import Player
from mod.math.raycaster import Raycaster
from mod.math.raycaster_numba import render_numba
from mod.math.coordinate import Coordinate
from mod.ext.constants import (
    MINIMAP_SIZE,
    WIN_HEIGHT,
    WIN_WIDTH,
    DEFAULT_SCENE,
    GAB_FACTOR,
    FPS,
    CAMERA_CAMERAPLANE_DISTANCE,
    PUSH_FACTOR,
    RES,
)


def handle_movement(r: Raycaster):
    keys = pygame.key.get_pressed()

    if keys[pygame.K_w]:
        pos = Coordinate.from_angle(r.player.direction) * 0.1
        new_x = r.player.position[0] + pos.x
        new_y = r.player.position[1] + pos.y
        r.player.position = (new_x, new_y)

    if keys[pygame.K_s]:
        pos = Coordinate.from_angle(r.player.direction) * 0.1
        new_x = r.player.position[0] - pos.x
        new_y = r.player.position[1] - pos.y
        r.player.position = (new_x, new_y)

    if keys[pygame.K_a]:
        r.player.direction -= pi * 0.02

    if keys[pygame.K_d]:
        r.player.direction += pi * 0.02


def main():
    pygame.init()
    WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    MINIMAP_SURFACE = pygame.transform.scale(pygame.Surface((WIN_WIDTH, WIN_HEIGHT)), MINIMAP_SIZE)
    RENDERING_SURFACE = pygame.Surface((WIN_WIDTH, WIN_HEIGHT))
    CLOCK = pygame.time.Clock()

    PLAYER = Player((7.5, 5.5), pi * 1.25)
    SCENE = Scene(MINIMAP_SURFACE, DEFAULT_SCENE)
    MAP = Map(MINIMAP_SURFACE, SCENE, PLAYER)

    RAYCASTER = Raycaster(RENDERING_SURFACE, MAP, PLAYER)

    Coordinate.set_map(MAP)
    RENDERING_SURFACE.fill((*Color.BASE,))

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                return

        RENDERING_SURFACE.fill((*Color.BASE,))
        
        colors = [
            Color.RED.value,
            Color.PINK.value,
            Color.MAROON.value,
            Color.SKY.value,
        ]
        
        grid_np = np.array(SCENE.grid, dtype=np.int64)
        
        rects = render_numba(
            grid_np,
            SCENE.row, SCENE.col,
            PLAYER.position[0], PLAYER.position[1], PLAYER.direction,
            CAMERA_CAMERAPLANE_DISTANCE,
            RES,
            WIN_WIDTH, WIN_HEIGHT,
            PUSH_FACTOR,
            colors
        )
        
        RENDERING_SURFACE.fill((*Color.BASE,))
        
        for x, y, w, h, r, g, b in rects:
            pygame.draw.rect(RENDERING_SURFACE, (r, g, b), (int(x), int(y), int(w), int(h)))
        
        handle_movement(RAYCASTER)

        MAP.render_minimap()
        MAP.render_cells()
        MAP.render_player()

        WIN.blit(RENDERING_SURFACE, (0, 0))
        WIN.blit(
            MINIMAP_SURFACE,
            (int(MINIMAP_SURFACE.get_width() * GAB_FACTOR), int(MINIMAP_SURFACE.get_width() * GAB_FACTOR)),
        )

        pygame.display.update()
        CLOCK.tick(FPS)
        print(f"\rFPS: {CLOCK.get_fps():.1f}", end="")


if __name__ == "__main__":
    main()
