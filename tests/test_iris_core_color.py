import pytest
from iris_core import Color, PixelCoordinates, __version__


def test_version():
    assert __version__ == "0.1.0"


class TestColor:
    def test_color_initialization(self):

        c = Color(100, 100, 100)

        assert c.r == 100
        assert c.g == 100
        assert c.b == 100

    def test_initialization_out_of_range_values(self):

        with pytest.raises(ValueError):
            c = Color(1000, 260, -100)

    def test_color_hex(self):

        color_black = "#000000"
        color_white = "#FFFFFF"
        color_random = "#34CF89"

        b = Color(0, 0, 0)
        w = Color(255, 255, 255)
        r = Color(52, 207, 137)

        assert b.as_hex() == color_black
        assert w.as_hex() == color_white
        assert r.as_hex() == color_random

    def test_color_rgb(self):

        c = Color(0, 0, 0)

        r, g, b = c.as_rgb()

        assert r == 0
        assert g == 0
        assert b == 0

    def test_color_hsv(self):
        random_hsv = (145, 59, 58)

        c = Color(61, 148, 97)

        hsv = c.as_hsv()

        assert hsv[0] == random_hsv[0]
        assert hsv[1] == random_hsv[1]
        assert hsv[2] == random_hsv[2]
