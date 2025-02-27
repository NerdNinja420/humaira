from __future__ import annotations
from enum import Enum


class Color(Enum):
    ROSEWATER = (245, 224, 220)
    FLAMINGO = (242, 205, 205)
    PINK = (245, 194, 231)
    MAUVE = (203, 166, 247)
    RED = (243, 139, 168)
    MAROON = (235, 160, 172)
    PEACH = (250, 179, 135)
    YELLOW = (249, 226, 175)
    GREEN = (166, 227, 161)
    TEAL = (148, 226, 213)
    SKY = (137, 220, 235)
    SAPPHIRE = (116, 199, 236)
    BLUE = (137, 180, 250)
    LAVENDER = (180, 190, 254)
    TEXT = (205, 214, 244)
    SUBTEXT1 = (186, 194, 222)
    SUBTEXT0 = (166, 173, 200)
    OVERLAY2 = (147, 153, 178)
    OVERLAY1 = (127, 132, 156)
    OVERLAY0 = (108, 112, 134)
    SURFACE2 = (88, 91, 112)
    SURFACE1 = (69, 71, 90)
    SURFACE0 = (49, 50, 68)
    BASE = (30, 30, 46)
    MANTLE = (24, 24, 37)
    CRUST = (17, 17, 27)
    HIT = (210, 15, 57)
    CHOSEN = (242, 205, 205)

    def __str__(self):
        return f"{self.name}({self.value})"

    def __iter__(self):
        return iter(self.value)

    def rgb(self):
        return self.value

    # Example usage:
    @classmethod
    def rand(cls) -> Color:
        from random import choice

        return choice(list(cls)[:14])

    @classmethod
    def range(
        cls,
        limits: list[tuple[int, int, int]],
        steps: int,
        reshape: int,
    ) -> list[list[tuple[int, int, int]]]:
        if steps < 2:
            raise ValueError(f"fucked up here, dude! :{steps}")

        if len(limits) < 2:
            raise ValueError(f"fucked up here, dude! :{len(limits)}")

        colors: list[tuple[int, int, int]] = []
        segments = len(limits) - 1
        steps_per_segment = steps // segments
        remainder_steps = steps % segments

        for segment in range(segments):
            start = limits[segment]
            end = limits[segment + 1]

            current_segment_steps = steps_per_segment + (1 if segment < remainder_steps else 0)
            for step in range(current_segment_steps):
                alpha = step / current_segment_steps
                r = round(start[0] + (end[0] - start[0]) * alpha)
                g = round(start[1] + (end[1] - start[1]) * alpha)
                b = round(start[2] + (end[2] - start[2]) * alpha)
                colors.append((r, g, b))

        return [colors[i : i + reshape] for i in range(0, len(colors), reshape)]


# if __name__ == "__main__":
#     from .constands import COLOR_LOWER, COLOR_MID, COLOR_UPPER

#     # print(*(Color.TEXT))
#     # print((*Color.TEXT,))
#     # print((*(1, 2, 3),))
#     print(Color.range([COLOR_LOWER, COLOR_MID, (155, 0, 55), COLOR_UPPER], 10, 11))
