from math import pi

import pygame
from pygame.locals import QUIT

from mod.ext.color import Color
from mod.objects.scene import Scene
from mod.objects.minimap import Map
from mod.objects.player import Player
from mod.math.raycaster import Raycaster
from mod.math.coordinate import Coordinate
from mod.ext.constants import (
    MINIMAP_SIZE,
    WIN_HEIGHT,
    WIN_WIDTH,
    DEFAULT_SCENE,
    GAB_FACTOR,
    FPS,
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

    r.surface.fill((*Color.BASE,))
    r.render()


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

        MAP.render_minimap()
        MAP.render_cells()
        MAP.render_player()

        WIN.blit(RENDERING_SURFACE, (0, 0))
        WIN.blit(
            MINIMAP_SURFACE,
            (MINIMAP_SURFACE.get_width() * GAB_FACTOR, MINIMAP_SURFACE.get_width() * GAB_FACTOR),
        )

        RAYCASTER.render()
        handle_movement(RAYCASTER)

        pygame.display.update()
        CLOCK.tick(FPS)


if __name__ == "__main__":
    main()
