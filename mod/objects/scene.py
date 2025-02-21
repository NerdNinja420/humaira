from pygame import Surface

from mod.ext.constants import GAB_FACTOR


class Scene:
    def __init__(self, surface: Surface, grid: list[list[int]]) -> None:
        self.row = len(grid)
        self.col = max(len(row) for row in grid)
        self.grid = grid.copy()
        self.cell_size = min(
            (surface.get_width() - 2 * int(GAB_FACTOR * surface.get_width())) // self.col,
            (surface.get_height() - 2 * int(GAB_FACTOR * surface.get_width())) // self.row,
        )
        self.horizontal_gab = (surface.get_width() - (self.cell_size * self.col)) // 2
        self.vertical_gab = (surface.get_height() - (self.cell_size * self.row)) // 2

    def __repr__(self) -> str:
        return f"Scene(row='{self.row}', col='{self.col}')"

    def __getitem__(self, row: int) -> list[int]:
        return self.grid[row]

    def get_info(self) -> tuple[int, int, int, int, int]:
        return (self.row, self.col, self.cell_size, self.horizontal_gab, self.vertical_gab)
