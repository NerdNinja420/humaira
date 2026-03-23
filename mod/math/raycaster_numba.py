from numba import njit
import numpy as np
from math import ceil, floor, copysign, cos, sin, inf


@njit(cache=True)
def get_delta_t(p: float, dx: float) -> float:
    if dx > 0:
        return (ceil(p) - p) / dx
    elif dx < 0:
        return (floor(p) - p) / dx
    return inf


@njit(cache=True)
def snap(p: float, delta: float, push_factor: float) -> float:
    if delta > 0:
        return ceil(p) + copysign(push_factor, delta)
    if delta < 0:
        return floor(p) + copysign(push_factor, delta)
    return p + copysign(push_factor, delta)


@njit(cache=True)
def cast_ray_single(
    px: float, py: float,
    dx: float, dy: float,
    grid: np.ndarray,
    grid_rows: int, grid_cols: int,
    push_factor: float
) -> tuple:
    p1x, p1y = px, py
    p2x, p2y = px + dx, py + dy

    while 0 <= int(p2y) < grid_rows and 0 <= int(p2x) < grid_cols:
        cell_y = int(p2y)
        cell_x = int(p2x)
        
        if grid[cell_y, cell_x] >= 1:
            return p2x, p2y, grid[cell_y, cell_x]

        ddx = p2x - p1x
        ddy = p2y - p1y

        tx = get_delta_t(p2x, ddx)
        ty = get_delta_t(p2y, ddy)

        if tx < ty:
            p3x = snap(p2x, ddx, push_factor)
            p3y = p2y + ddy * tx
        else:
            p3x = p2x + ddx * ty
            p3y = snap(p2y, ddy, push_factor)

        p1x, p1y = p2x, p2y
        p2x, p2y = p3x, p3y

    return -1.0, -1.0, 0


@njit(cache=True)
def render_numba(
    grid: np.ndarray,
    grid_rows: int, grid_cols: int,
    player_x: float, player_y: float, player_dir: float,
    camera_plane_dist: float,
    res: int,
    win_width: int, win_height: int,
    push_factor: float,
    colors: list
) -> tuple:
    result = []

    dir_x = cos(player_dir)
    dir_y = sin(player_dir)
    
    perp_x = -dir_y
    perp_y = dir_x
    
    p_x = player_x + dir_x * camera_plane_dist
    p_y = player_y + dir_y * camera_plane_dist
    
    r1_x = p_x - perp_x
    r1_y = p_y - perp_y
    r2_x = p_x + perp_x
    r2_y = p_y + perp_y
    
    delta_x = (r2_x - r1_x) / res
    delta_y = (r2_y - r1_y) / res

    width = win_width / res

    for x in range(res):
        rd_x = r1_x + delta_x * x
        rd_y = r1_y + delta_y * x

        hit_x, hit_y, wall_type = cast_ray_single(
            player_x, player_y, rd_x, rd_y,
            grid, grid_rows, grid_cols, push_factor
        )

        if hit_x >= 0:
            vx = hit_x - player_x
            vy = hit_y - player_y
            dist = dir_x * vx + dir_y * vy

            if dist > 0.01:
                height = win_height / dist
                color_idx = min(int(wall_type) - 1, len(colors) - 1)
                r, g, b = colors[color_idx]
                result.append((x * width, (win_height - height) * 0.5, width + 1, height, r, g, b))

    return result