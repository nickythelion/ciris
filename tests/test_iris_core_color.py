import pytest
from iris_core import Color, PixelCoordinates, __version__


def test_version():
    assert __version__ == "0.1.0"


class TestColor:
    def test_color_initialization(self):
        p_map = [[0, 0], [0, 1], [1, 0], [1, 1]]
        c = Color(100, 100, 100, p_map)

        assert c.r == 100
        assert c.g == 100
        assert c.b == 100
        assert c.pixel_map[0].as_list() == [0, 0]

    def test_initialization_out_of_range_values(self):
        p_map = [[0, 0], [0, 1], [1, 0], [1, 1]]

        with pytest.raises(ValueError):
            c = Color(1000, 260, -100, p_map)

    def test_color_hex(self):

        p_map = [[0, 0], [0, 1], [1, 0], [1, 1]]

        color_black = "#000000"
        color_white = "#FFFFFF"
        color_random = "#34CF89"

        b = Color(0, 0, 0, p_map)
        w = Color(255, 255, 255, p_map)
        r = Color(52, 207, 137, p_map)

        assert b.as_hex() == color_black
        assert w.as_hex() == color_white
        assert r.as_hex() == color_random

    def test_color_rgb(self):
        p_map = [[0, 0], [0, 1], [1, 0], [1, 1]]

        c = Color(0, 0, 0, p_map)

        r, g, b = c.as_rgb()

        assert r == 0
        assert g == 0
        assert b == 0

    def test_color_hsv(self):
        random_hsv = (145, 59, 58)

        p_map = [[0, 0], [0, 1], [1, 0], [1, 1]]

        c = Color(61, 148, 97, p_map)

        hsv = c.as_hsv()

        assert hsv[0] == 145
        assert hsv[1] == 59
        assert hsv[2] == 58

    def test_color_pixel_number(self):
        p_map = [[0, 0], [0, 1], [1, 0], [1, 1]]

        c = Color(0, 0, 0, p_map)

        assert c.number_of_pixels() == 4
