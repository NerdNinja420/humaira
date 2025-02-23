from math import pi
from platform import system
from typing import Final

FPS: Final[int] = 60
EPS: Final[tuple[float, float]] = (1e-3, 1e-3)
FOV: Final[float] = pi * 0.1

if system() == "Linux":
    SCREEN_FACTOR = 150
    WIN_WIDTH: Final[int] = 16 * SCREEN_FACTOR
    WIN_HEIGHT: Final[int] = 9 * SCREEN_FACTOR
    GAB: Final[int] = int(WIN_WIDTH * 0.1)
    GAB_FACTOR: Final[float] = 0.02
    RES: Final[int] = 500
else:
    SCREEN_FACTOR = 80  # type: ignore
    WIN_WIDTH: Final[int] = 16 * SCREEN_FACTOR  # type: ignore
    WIN_HEIGHT: Final[int] = 9 * SCREEN_FACTOR  # type: ignore
    GAB: Final[int] = int(WIN_WIDTH * 0.1)  # type: ignore
    GAB_FACTOR: Final[float] = 0.02  # type: ignore
    RES: Final[int] = 200  # type: ignore


INFINITY: Final[float] = 1e30
PUSH_FACTOR: Final[float] = 1e-6
CIRCLE_RADIUS: Final[int] = int(GAB * 0.05)
GRID_CELL_COUNT: Final[int] = 10

CAMERA_CAMERAPLANE_DISTANCE: Final[float] = 1

DEFAULT_SCENE: list[list[int]] = [
    [0, 0, 0, 0, 0, 1, 0, 2, 2, 2, 0, 0],
    [0, 0, 0, 0, 0, 1, 0, 3, 0, 3, 0, 0],
    [0, 0, 0, 0, 0, 3, 0, 1, 0, 1, 0, 0],
    [0, 0, 2, 2, 3, 2, 0, 0, 0, 0, 0, 2],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 4],
]


RECT_SIZE_WIDTH_LIMITS: Final[tuple[float, float]] = (10, int(WIN_WIDTH / 3))
RECT_SIZE_HEIGHT_LIMITS: Final[tuple[float, float]] = (10, int(WIN_HEIGHT / 3))
RECT_POSITION_X_LIMITS: Final[tuple[float, float]] = (0, WIN_WIDTH - RECT_SIZE_WIDTH_LIMITS[1])
RECT_POSITION_Y_LIMITS: Final[tuple[float, float]] = (0, WIN_HEIGHT - RECT_SIZE_HEIGHT_LIMITS[1])

if system() == "Linux":
    FONT: Final[str] = "JetBrains Mono Nerd Font"
    FONT_SIZE_SCORE: Final[int] = 38
    FONT_SIZE_END_MSG: Final[int] = 100
else:
    FONT: Final[str] = "JetBrainsMono NF SemiBold"  # type: ignore
    FONT_SIZE_SCORE: Final[int] = 20  # type: ignore
    FONT_SIZE_END_MSG: Final[int] = 60  # type: ignore
