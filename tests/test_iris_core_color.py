import pytest
from iris_core import Color, PixelCoordinates, __version__


def test_version():
    assert __version__ == "0.1.0"


class TestColor:
    def test_init_from_hsv(self):
        h, s, v = (171, 76, 100)

        c = Color.from_hsv(h, s, v)

        assert c.h == 171
        assert c.s == 0.76
        assert c.v == 1.0

    def test_init_from_hsv_bad_values(self):
        h, s, v = (10000, -99, 1939)

        with pytest.raises(ValueError):
            c = Color(h, s, v)

    def test_init_from_rgb(self):
        r, g, b = (61, 255, 226)

        c = Color.from_rgb(r, g, b)

        assert c.h == 171
        assert c.s == 0.76
        assert c.v == 1.0

    def test_init_from_rgb(self):
        r, g, b = (100, 555, -98)

        with pytest.raises(ValueError):
            c = Color.from_rgb(r, g, b)

    def test_init_from_hex(self):
        hex_str = "#3dffe2"

        c = Color.from_hex(hex_str)

        assert c.h == 171
        assert c.s == 0.76
        assert c.v == 1.0

    def test_init_from_hex_bad_str(self):
        bad_hex = "#FFFFFF00"

        with pytest.raises(ValueError):
            c = Color.from_hex(bad_hex)

    def test_init_from_cmyk(self):
        c, m, y, k = (76, 0, 11, 0)

        c = Color.from_cmyk(c, m, y, k)

        h, s, v = c.as_hsv()

        assert h == 171
        assert s == 76
        assert v == 100

    def test_init_from_cmyk_bad_values(self):
        c, m, y, k = (101, -98, 77777, 64)

        with pytest.raises(ValueError):
            c = Color.from_cmyk(c, m, y, k)

    def test_color_as_hsv(self):
        h, s, v = (171, 76, 100)

        c = Color.from_hsv(h, s, v)

        h1, s1, v1 = c.as_hsv()

        assert h1 == 171
        assert s1 == 76
        assert v1 == 100

    def test_color_as_rgb(self):
        h, s, v = (171, 76, 100)

        c = Color.from_hsv(h, s, v)

        r, g, b = c.as_rgb()

        assert r == 61
        assert g == 255
        assert b == 226

    def test_color_as_hex(self):
        h, s, v = (171, 76, 100)

        c = Color.from_hsv(h, s, v)

        hex_s = c.as_hex()

        assert hex_s == "#3DFFE2"

    def test_color_as_cmyk(self):
        h, s, v = (171, 76, 100)

        c = Color.from_hsv(h, s, v)

        c, m, y, k = c.as_cmyk()

        assert c == 76
        assert m == 0
        assert y == 11
        assert k == 0
