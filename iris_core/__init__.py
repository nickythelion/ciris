__version__ = "0.1.0"

from typing import List, Tuple
from typing_extensions import Self


class PixelCoordinates:
    def __init__(self, x: int, y: int) -> None:
        if x < 0 or y < 0:
            raise ValueError("Pixel coordinates cannot be negative")

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

        if not (0 <= h <= 360):
            raise ValueError(
                f"Expected Hue to be in range [0..360], but got {h}"
            )

        if not (0 <= s <= 100):
            raise ValueError(
                f"Expected Saturation to be in range [0..100], but got {s}"
            )

        if not (0 <= v <= 100):
            raise ValueError(
                f"Expected Value to be in range [0..100], but got {v}"
            )

        self.h = h
        self.s = s * 0.01  # Need to clamp the value in range [0..1]
        self.v = v * 0.01  # Need to clamp the value in range [0..1]

    @classmethod
    def from_rgb(cls, r: int, g: int, b: int) -> Self:

        if not (0 <= r <= 255) or not (0 <= g <= 255) or not (0 <= b <= 255):
            raise ValueError(
                f"Expected R, G, B channel values to be in range [0..255], but got {r}, {g}, {b}"
            )

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
    def from_hsv(cls, h: int, s: int, v: int) -> Self:
        return cls(h, s, v)

    @classmethod
    def from_hex(cls, clr_hex: str) -> Self:

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

    @classmethod
    def from_cmyk(cls, c: int, m: int, y: int, k: int) -> Self:
        if (
            not (0 <= c <= 100)
            or not (0 <= m <= 100)
            or not (0 <= y <= 100)
            or not (0 <= k <= 100)
        ):
            raise ValueError(
                f"Expected C, M, Y, K to be in range [0..100], bu got {c}, {m}, {y}, {k}"
            )

        c = c * 0.01
        m = m * 0.01
        y = y * 0.01
        k = k * 0.01

        r = 255 * (1 - c) * (1 - k)
        g = 255 * (1 - m) * (1 - k)
        b = 255 * (1 - y) * (1 - k)

        return cls.from_rgb(r, g, b)

    def as_hsv(self) -> "Tuple[int, int, int]":
        return (
            self.h,
            self.s * 100,
            self.v * 100,
        )

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

    def as_cmyk(self) -> "Tuple[int, int, int, int]":

        r, g, b = self.as_rgb()

        r_dash, g_dash, b_dash = r / 255, g / 255, b / 255

        k = 1 - max(r_dash, g_dash, b_dash)
        c = (1 - r_dash - k) / (1 - k)
        m = (1 - g_dash - k) / (1 - k)
        y = (1 - b_dash - k) / (1 - k)

        return (
            int(round(c, 2) * 100),
            int(round(m, 2) * 100),
            int(round(y, 2) * 100),
            int(round(k, 2) * 100),
        )


class PixelColor(Color):
    def __init__(
        self, h: int, s: int, v: int, pixels: List[List[int]]
    ) -> None:

        self.pixel_map = [PixelCoordinates(i[0], i[1]) for i in pixels]

        super().__init__(h, s, v)

    def number_of_pixels(self) -> int:
        """Returns the number of pixels that have the same color

        Returns:
            int: how many pixels sin an image have this color
        """
        return len(self.pixel_map)
