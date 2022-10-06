__version__ = "0.1.0"

from typing import List, Tuple


class PixelCoordinates:
    def __init__(self, x: int, y: int) -> None:
        if x < 0 or y < 0:
            raise ValueError("Coordinates cannot be negative")

        self.x = x
        self.y = y

    def as_tuple(self) -> "Tuple[int, int]":
        """Returns the coordinates as a tuple of length 2

        Returns:
            Tuple[int, int]: A tuple containing the coordinates: the first
            one is X, the second one is Y
        """
        return (
            self.x,
            self.y,
        )

    def as_list(self) -> "List[int]":
        """Returns the coordinates as a list.
        This function is equivalent to list(PixelCoordinates.as_tuple())

        Returns:
            List[int]: _description_
        """
        return list(self.as_tuple())


class Color:
    def __init__(self, h: int, s: int, v: int) -> None:

        self.h = h
        self.s = s * 0.01  # Need to clamp the value in range [0..1]
        self.v = v * 0.01  # Need to clamp the value in range [0..1]

    @classmethod
    def from_rgb(cls, r: int, g: int, b: int):

        r_clamp = r / 255
        g_clamp = g / 255
        b_clamp = b / 255

        c_max = max(r_clamp, g_clamp, b_clamp)
        c_min = min(r_clamp, g_clamp, b_clamp)

        delta = c_max - c_min

        # Get Hue
        if c_max == c_min:
            hue = 0

        elif c_max == r_clamp:
            hue = (60 * ((b_clamp - r_clamp) / delta) + 360) % 360

        elif c_max == g_clamp:
            hue = (60 * ((b_clamp - r_clamp) / delta) + 120) % 360

        elif c_max == b_clamp:
            hue = (60 * ((r_clamp - g_clamp) / delta) + 240) % 360

        # Get  Saturation
        if c_max == 0:
            saturation = 0
        else:
            saturation = (delta / c_max) * 100

        # Get Value
        value = c_max * 100

        return cls(
            int(round(hue)),
            int(round(saturation)),
            int(round(value)),
        )

    @classmethod
    def from_hsv(cls, h: int, s: int, v: int):
        return cls(h, s, v)

    @classmethod
    def from_hex(cls, clr_hex: str):

        if len(clr_hex) != 7:
            raise ValueError(
                f"This function only accepts hex-strings in 6-digit format (e.g. #FFFFFF, #06AC9F). Other formats re not supported"
            )

        clr_hex = clr_hex.replace("#", "")

        chl_size = len(clr_hex) // 3  # Three channles: R, G, B

        clhrs = [
            clr_hex[ch : ch + chl_size]
            for ch in range(0, len(clr_hex), chl_size)
        ]

        r, g, b = (int(chl, base=16) for chl in clhrs)

        return cls.from_rgb(r, g, b)

    def as_hsv(self) -> "Tuple[int, int, int]":
        return (self.h, self.s * 100, self.v * 100)

    def as_rgb(self) -> "Tuple[int, int, int]":
        chroma = self.v * self.s

        h_dash = self.h / 60.0

        x_buf = chroma * (1 - abs(h_dash % 2 - 1))

        if 0 <= h_dash < 1:
            rgb_d = (chroma, x_buf, 0)

        if 1 <= h_dash < 2:
            rgb_d = (x_buf, chroma, 0)

        if 2 <= h_dash < 3:
            rgb_d = (0, chroma, x_buf)

        if 3 <= h_dash < 4:
            rgb_d = (0, x_buf, chroma)

        if 4 <= h_dash < 5:
            rgb_d = (x_buf, 0, chroma)

        if 5 <= h_dash < 6:
            rgb_d = (chroma, 0, x_buf)

        m = self.v - chroma

        r1, g1, b1 = rgb_d

        r, g, b = (r1 + m, g1 + m, b1 + m)

        return (
            round(r * 255),
            round(g * 255),
            round(b * 255),
        )

    def as_hex(self) -> str:
        def _convert_color_channel(val: int) -> str:
            HEXDIGITS = {
                0: "0",
                1: "1",
                2: "2",
                3: "3",
                4: "4",
                5: "5",
                6: "6",
                7: "7",
                8: "8",
                9: "9",
                10: "A",
                11: "B",
                12: "C",
                13: "D",
                14: "E",
                15: "F",
            }

            div = val / 16
            first = HEXDIGITS[int(div)]

            rem = int((div - int(div)) * 16)
            second = HEXDIGITS[rem]

            return f"{first}{second}"

        r, g, b = self.as_rgb()

        r_hex = _convert_color_channel(r)
        g_hex = _convert_color_channel(g)
        b_hex = _convert_color_channel(b)

        return f"#{r_hex}{g_hex}{b_hex}"


class PixelColor(Color):
    def __init__(
        self, r: int, g: int, b: int, pixels: List[List[int]]
    ) -> None:

        self.pixel_map = [PixelCoordinates(i[0], i[1]) for i in pixels]

        super().__init__(r, g, b)

    def number_of_pixels(self) -> int:
        """Returns the number of pixels that have the same color

        Returns:
            int: how many pixels sin an image have this color
        """
        return len(self.pixel_map)
