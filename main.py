from math import floor, ceil, copysign, pi

import pygame
from pygame import Surface
from pygame.locals import QUIT

from mod.objects.player import Player
from mod.objects.scene import Scene
from mod.objects.minimap import Map
from mod.math.coordinate import Coordinate
from mod.ext.color import Color

# from mod.ext.func import fillCircle, strokeLine
from mod.ext.constants import (
    FPS,
    GAB_FACTOR,
    WIN_WIDTH,
    WIN_HEIGHT,
    PUSH_FACTOR,
    INFINITY,
    DEFAULT_SCENE,
)


def get_delta_t(p: float, dx: float) -> float:
    if dx > 0:
        return (ceil(p) - p) / dx
    elif dx < 0:
        return (floor(p) - p) / dx
    return INFINITY


def snap(p: float, delta: float) -> float:
    if delta > 0:
        return ceil(p) + copysign(PUSH_FACTOR, delta)
    if delta < 0:
        return floor(p) + copysign(PUSH_FACTOR, delta)
    return p + copysign(PUSH_FACTOR, delta)


def ray_step(p1: Coordinate, p2: Coordinate) -> Coordinate:
    d = p2 - p1

    tx = get_delta_t(p2.x, d.x)
    ty = get_delta_t(p2.y, d.y)

    if tx < ty:
        x = snap(p2.x, d.x)
        y = p2.y + d.y * tx
    else:
        x = p2.x + d.x * ty
        y = snap(p2.y, d.y)

    return Coordinate(x, y)


def cast_ray(map: Map, p1: Coordinate, p2: Coordinate) -> Coordinate | None:
    p3 = ray_step(p1, p2)
    while map.is_insight(p2):
        if map.get_scene_cell(p2) == 1:
            return p2

        p1 = p2
        p2 = p3
        p3 = ray_step(p1, p2)

    return None


def render(surface: Surface, map: Map, player: Player):
    RES = 500
    width = ceil(WIN_WIDTH / RES)
    for x in range(RES):
        r1, r2 = player.get_fov_range()
        point_on_camera_plane = r1 + ((r2 - r1) * (x / RES))  # linear interpolation
        hit_point = cast_ray(map, Coordinate(*player.position), point_on_camera_plane)
        if hit_point is not None:
            # distance = (hit_point - Coordinate(*player.position)).abs()
            # height = max(0, min(WIN_HEIGHT, WIN_HEIGHT / (distance)))
            v = hit_point - Coordinate(*player.position)
            d = Coordinate.from_angle(player.direction)
            height = WIN_HEIGHT / d.dot(v)
            pygame.draw.rect(
                surface,
                (*Color.SKY, 255),
                (x * width, (WIN_HEIGHT - height) * 0.5, width + 1, height),
            )


def main():
    pygame.init()
    WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    MINIMAP_SURFACE = pygame.transform.scale(
        pygame.Surface((WIN_WIDTH, WIN_HEIGHT)), (WIN_WIDTH // 3, WIN_HEIGHT // 3)
    )
    RENDERING_SURFACE = pygame.Surface((WIN_WIDTH, WIN_HEIGHT))
    CLOCK = pygame.time.Clock()

    PLAYER = Player((7.5, 5.5), pi * 1.25)
    SCENE = Scene(MINIMAP_SURFACE, DEFAULT_SCENE)
    MAP = Map(MINIMAP_SURFACE, SCENE, PLAYER)

    Coordinate.set_map(MAP)
    RENDERING_SURFACE.fill((*Color.BASE,))

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    pos = Coordinate.from_angle(PLAYER.direction) * 0.5
                    new_x = PLAYER.position[0] + pos.x
                    new_y = PLAYER.position[1] + pos.y
                    PLAYER.position = (new_x, new_y)

                    RENDERING_SURFACE.fill((*Color.BASE,))
                    render(RENDERING_SURFACE, MAP, PLAYER)

                if event.key == pygame.K_s:
                    pos = Coordinate.from_angle(PLAYER.direction) * 0.5
                    new_x = PLAYER.position[0] - pos.x
                    new_y = PLAYER.position[1] - pos.y
                    PLAYER.position = (new_x, new_y)

                    RENDERING_SURFACE.fill((*Color.BASE,))
                    render(RENDERING_SURFACE, MAP, PLAYER)
                if event.key == pygame.K_a:
                    PLAYER.direction += pi * 0.1

                    RENDERING_SURFACE.fill((*Color.BASE,))
                    render(RENDERING_SURFACE, MAP, PLAYER)
                if event.key == pygame.K_d:
                    PLAYER.direction -= pi * 0.1

                    RENDERING_SURFACE.fill((*Color.BASE,))
                    render(RENDERING_SURFACE, MAP, PLAYER)

        MAP.render_minimap()
        MAP.render_cells()
        MAP.render_player()

        WIN.blit(RENDERING_SURFACE, (0, 0))
        WIN.blit(
            MINIMAP_SURFACE,
            (MINIMAP_SURFACE.get_width() * GAB_FACTOR, MINIMAP_SURFACE.get_width() * GAB_FACTOR),
        )
        render(RENDERING_SURFACE, MAP, PLAYER)

        pygame.display.update()
        CLOCK.tick(FPS)


if __name__ == "__main__":
    main()
