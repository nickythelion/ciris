__version__ = "1.0.0"

from dataclasses import dataclass
from typing import List, Optional, Tuple
from typing_extensions import Self, NewType

from typing import Tuple
from typing_extensions import Self


class Color:
    def __init__(self, h: int, s: int, v: int) -> None:
        """Creates a Color object. It uses HSV color scheme as its primary,
        thus its usage is required for direct initialization (c = Color(...)).
        For initializing the object using a different color space please use
        the appropriate initializer function

        Args:
            h (int): Hue (from 0 up tp 360)
            s (int): Saturation (from 0 up to 100)
            v (int): Value (from 0 up to 100)

        Raises:
            ValueError: if Hue is not in range [0..360]
            ValueError: if Saturation is not in range [0..100]
            ValueError: if Value is not in range [0..100]
        """

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

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(h={self.h}, s={self.s}, v={self.v})"

    def __str__(self) -> str:
        return self.__repr__()

    def __eq__(self, __o: object) -> bool:
        return isinstance(__o, Color) and (
            (self.h == __o.h) and (self.s == __o.s) and (self.v == __o.v)
        )

    def __ne__(self, __o: object) -> bool:
        return not self.__eq__(__o)

    def __hash__(self) -> int:
        hash_str = f"{self.h},{self.s},{self.v}"
        return hash(hash_str)

    @classmethod
    def from_rgb(cls, r: int, g: int, b: int) -> Self:
        """Initializes the Color class using RGB color space

        Args:
            r (int): Red
            g (int): Green
            b (int): Blue

        Raises:
            ValueError: if either of Red, Green or Blue is not in range [0..255]
        """

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
            hue = 60 * (0 + (g_clamp - b_clamp) / delta)
        elif c_max == g_clamp:
            hue = 60 * (2 + (b_clamp - r_clamp) / delta)
        elif c_max == b_clamp:
            hue = 60 * (4 + (r_clamp - g_clamp) / delta)

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
        """Creates the Color object using the HSV color space. This function
        is equivalent to direct initialization and was added for consistency

        Args:
            h (int): Hue
            s (int): Saturation
            v (int): Value
        """
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

        return cls(h, s, v)

    @classmethod
    def from_hex(cls, clr_hex: str) -> Self:
        """Creates the Color object using the HEX string

        Args:
            clr_hex (str): a hex-string (7-symbol). Other formats, such as a
            9-symbol string, which includes opacity, is not supported at the moment.
            The support may be added later, but for now any string that is not a 7-symbol
            hex will throw an error

        Raises:
            ValueError: is hex-string's format is unsupported
        """
        if len(clr_hex) != 7:
            raise ValueError(
                f"This function only accepts hex-strings in 6-digit format (e.g. #FFFFFF, #06AC9F). Other formats re not supported"
            )

        clr_hex = clr_hex.replace("#", "")

        chl_size = len(clr_hex) // 3  # Three channels: R, G, B

        clhrs = [
            clr_hex[ch : ch + chl_size]
            for ch in range(0, len(clr_hex), chl_size)
        ]

        r, g, b = (int(chl, base=16) for chl in clhrs)

        return cls.from_rgb(r, g, b)

    @classmethod
    def from_cmyk(cls, c: int, m: int, y: int, k: int) -> Self:
        """Creates the Color object using CMYK namespace.
        This function needs to be supplied with integers representing the percentages
        of the color channels. For example, if CMYK color is defined like cmyk(76%, 0%, 11%, 0%),
        then the functions' arguments will look like this: from_cmyk(76, 0, 11, 0)

        Args:
            c (int): Cyan
            m (int): Magenta
            y (int): Yellow
            k (int): Key

        Raises:
            ValueError: if either C, M, Y or K is not in range [0..100]
        """
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
        """Represents the current color in HSV color space

        Returns:
            Tuple[int, int, int]: a tuple containing Hue, Saturation and Value
        """
        return (
            self.h,
            self.s * 100,
            self.v * 100,
        )

    def as_rgb(self) -> "Tuple[int, int, int]":
        """Represents the current color in RGB color space

        Returns:
            Tuple[int, int, int]: a tuple containing Red, Green and Blue
        """
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
        """Represents the current color as a 7-symbol hex-string

        Returns:
            str: a hex-string
        """

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
        """Represents the current color in CMYK color space

        Returns:
            Tuple[int, int, int, int]: a tuple containing Cyan, Magenta, Yellow and Key
        """
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

    def hue_shift(self, amount: int) -> Self:
        """Shifts the color's hue by a specified amount.

        Args:
            amount (int): amount to shift hue by
        """

        new_hue = self.h + amount

        if new_hue > 360:
            new_hue = new_hue - 360

        if new_hue < 0:
            new_hue = 360 + new_hue

        self.h = new_hue

        return self

    def lighten(self, amount: int) -> Self:
        """Lightens the color by a specified percentage. For example,
        if you need to lighten a color by 25%, the function call will look like
        color_obj.lighten(25)

        Args:
            amount (int): the amount to lighten the color by
        """
        new_value = self.v + amount * 0.01

        if new_value > 1.0:
            new_value = 1.0

        if new_value < 0.0:
            new_value = 0.0

        self.v = new_value

        return self

    def darken(self, amount: int) -> Self:
        """Darkens the color by a specified percentage. For example,
        if you need to darken a color by 25%, the function call will look like
        color_obj.darken(25)

        Args:
            amount (int): the amount to darken the color by

        Args:
            amount (int): the amount to darken the color by
        """
        self.lighten(amount * -1)

        return self

    def invert(self) -> Self:
        """Inverts the current color"""
        self.hue_shift(180)

        return self

    def adjust_saturation(self, amount: int) -> Self:
        """Adjusts the color's saturation level.

        Args:
            amount (int): how much to adjust the level by. If the adjustment
            brings the saturation level out of range [0..100], then the level will be
            capped. For example, calling Color.adjust_saturation(-10000) on cyan
            will make the color a shade of gray.
        """
        new_s = self.s + amount * 0.01

        if new_s > 1.0:
            new_s = 1.0

        if new_s < 0.0:
            new_s = 0.0

        self.s = new_s

        return self

    def harmony_complementary(self) -> "HarmonyRule":
        """Applies the complementary color harmony rule to the color

        Returns:
            HarmonyRule: A HarmonyRule class describing the rule and containing
            all the colors
        """
        return HarmonyRule(
            "complementary",
            self,
            [
                Color.from_hsv(
                    self.h, int(self.s * 100), int(self.v * 100)
                ).hue_shift(180)
            ],
        )

    def harmony_split_complementary(self, phi: int = 150) -> "HarmonyRule":
        """Applies the split complementary color harmony rule to the color

        Arguments:
            phi (int): an offset that will be used. Default is 150 degrees

        Returns:
            HarmonyRule: A HarmonyRule class describing the rule and containing
            all the colors
        """

        return HarmonyRule(
            "split_complementary",
            self,
            [
                Color.from_hsv(
                    self.h, int(self.s * 100), int(self.v * 100)
                ).hue_shift(phi),
                Color.from_hsv(
                    self.h, int(self.s * 100), int(self.v * 100)
                ).hue_shift(360 - phi),
            ],
        )

    def harmony_triadic(self) -> "HarmonyRule":
        """Applies the triadic color harmony rule to the color

        Returns:
            HarmonyRule: A HarmonyRule class describing the rule and containing
            all the colors
        """
        return HarmonyRule(
            "triadic",
            self,
            [
                Color.from_hsv(
                    self.h, int(self.s * 100), int(self.v * 100)
                ).hue_shift(120),
                Color.from_hsv(
                    self.h, int(self.s * 100), int(self.v * 100)
                ).hue_shift(240),
            ],
        )

    def harmony_tetradic(self) -> "HarmonyRule":
        """Applies the tetradic color harmony rule to the color

        Returns:
            HarmonyRule: A HarmonyRule class describing the rule and containing
            all the colors
        """

        phi = 90

        return HarmonyRule(
            "tetradic",
            self,
            [
                Color.from_hsv(
                    self.h, int(self.s * 100), int(self.v * 100)
                ).hue_shift(phi),
                Color.from_hsv(
                    self.h, int(self.s * 100), int(self.v * 100)
                ).hue_shift(phi * 2),
                Color.from_hsv(
                    self.h, int(self.s * 100), int(self.v * 100)
                ).hue_shift(phi * 3),
            ],
        )

    # This function will return 2 secondary colors, but there's also a rule
    # for three secondary colors
    #
    # This might be implemented as a separate function in the future
    def harmony_analogous(self, phi: int = 30) -> "HarmonyRule":
        """Applies the analogous color harmony rule to the color. The resulting
        scheme consists of a base color and 2 derived colors, thus resulting in
        a 3-color palette

        Arguments:
            phi (int): an offset that will be used. Default is 30 degrees

        Returns:
            HarmonyRule: A HarmonyRule class describing the rule and containing
            3 total colors
        """

        return HarmonyRule(
            "analogous",
            self,
            [
                Color.from_hsv(
                    self.h, int(self.s * 100), int(self.v * 100)
                ).hue_shift(phi * -1),
                Color.from_hsv(
                    self.h, int(self.s * 100), int(self.v * 100)
                ).hue_shift(phi),
            ],
        )


@dataclass
class HarmonyRule:
    """A dataclass that represents a certain color harmony rule and contains
    all the colors that are related to it.

    Note that this class is a data container. It is only storing data. The actual
    calculation is done by Color.harmony_<harmony_type> methods.

    Attributes:
        rule_type: [str] -> An attribute that stores the type of the rule.
        The valid values are "complementary", "split_complementary", "triadic",
        "tetradic", "analogous"

        base_color: Color -> A Color object that was used to derive the secondary colors.
        secondary_colors: List[Colors] -> A list of colors that were derived from the base color according to
        the applied harmony rule

    """

    rule_type: str
    base_color: Color
    secondary_colors: List[Color]

    def get_base_color(self) -> Color:
        """Returns the base color of a harmony rule (the root color)

        Returns:
            Color: the Color object containing the base color info
        """
        return self.base_color

    def get_secondary_colors(self) -> List[Color]:
        """Returns the secondary colors of the harmony rule (the colors that
        were derived from the base color according to the rule)

        Returns:
            List[Color]: A list of Color objects that contain the secondary color info
        """
        return self.secondary_colors

    def get_harmony_rule_type(self) -> str:
        """Returns the type of harmony rule

        Returns:
            str: the type
        """
        return self.rule_type
