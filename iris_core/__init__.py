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
    def __init__(
        self,
        r: int,
        g: int,
        b: int,
    ) -> None:

        if not (0 <= r <= 255) or not (0 <= g <= 255) or not (0 <= b <= 255):
            raise ValueError(
                "expected RGB channel values to be in [0..255] range"
            )

        self.r = r
        self.g = g
        self.b = b

    def as_hex(self) -> str:
        """Converts RGB to hex

        Returns:
            str: a hex representation of the color
        """

        def _convert(val: int) -> str:
            """Converts a color RGB channel value into its corresponding
            color hex value

            Args:
                val (int): color channel value [0...255]

            Returns:
                str: a hex value of that color channel
            """
            HEX_DIGMAP = {10: "A", 11: "B", 12: "C", 13: "D", 14: "E", 15: "F"}

            val_div = val / 16

            first = (
                HEX_DIGMAP[int(val_div)]
                if int(val_div) > 9
                else str(int(val_div))
            )

            rem = int((val_div - int(val_div)) * 16)

            second = HEX_DIGMAP[rem] if rem > 9 else str(rem)

            return f"{first}{second}"

        r_hex = _convert(self.r)
        g_hex = _convert(self.g)
        b_hex = _convert(self.b)

        return f"#{r_hex}{g_hex}{b_hex}"

    def as_rgb(self) -> "Tuple[int, int, int]":
        """Returns the RGB representation of the color

        Returns:
            Tuple[int, int, int]: _description_
        """
        return (
            self.r,
            self.g,
            self.b,
        )

    def as_hsv(self) -> "Tuple[int, int, int]":
        """Returns the HSV representation of the color

        Returns:
            Tuple[int, int, int]: a tuple containing hue (0 - 360), saturation (0 - 100), value (0 - 100)
        """

        r_clamp = self.r / 255
        g_clamp = self.g / 255
        b_clamp = self.b / 255

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

        return (
            round(hue),
            round(saturation),
            round(value),
        )


class PixelColor(Color):
    def __init__(
        self, r: int, g: int, b: int, pixels: List[List[int]]
    ) -> None:

        self.pixel_map = [PixelCoordinates(i[0], i[1]) for i in pixels]

        super().__init__(r, g, b)

    def number_of_pixels(self) -> int:
        """Returns the number of pixels that have the same color

        Returns:
            int: _description_
        """
        return len(self.pixel_map)
