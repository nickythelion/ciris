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

    def test_color_hue_shift_positive(self):
        h, s, v = (171, 76, 100)
        c = Color.from_hsv(h, s, v)

        c.hue_shift(21)

        assert c.as_hex() == "#3DD8FF"

    def test_color_hue_shift_negative(self):
        h, s, v = (171, 76, 100)
        c = Color.from_hsv(h, s, v)

        c.hue_shift(-21)

        assert c.as_hex() == "#3DFF9E"

    def test_color_hue_shift_positive_loop_around(self):
        h, s, v = (171, 76, 100)
        c = Color.from_hsv(h, s, v)

        c.hue_shift(210)

        assert c.as_hex() == "#FF813D"

    def test_color_hue_shift_negative_loop_around(self):
        h, s, v = (171, 76, 100)
        c = Color.from_hsv(h, s, v)

        c.hue_shift(-210)

        assert c.as_hex() == "#FF3DBB"

    def test_color_lighten_in_bounds(self):
        h, s, v = (171, 76, 40)
        c = Color.from_hsv(h, s, v)

        c.lighten(50)

        assert c.as_hex() == "#37E6CB"

    def test_color_lighten_cap(self):
        h, s, v = (171, 76, 50)
        c = Color.from_hsv(h, s, v)

        c.lighten(150)

        assert c.as_hex() == "#3DFFE2"

    def test_color_darken_in_bounds(self):
        h, s, v = (171, 76, 100)
        c = Color.from_hsv(h, s, v)

        c.darken(15)

        assert c.as_hex() == "#34D9C0"

    def test_color_darken_out_of_bound(self):
        h, s, v = (171, 76, 100)
        c = Color.from_hsv(h, s, v)

        c.darken(150)

        assert c.as_hex() == "#000000"

    def test_color_invert(self):
        h, s, v = (171, 76, 100)
        c = Color.from_hsv(h, s, v)

        c.invert()

        assert c.as_hex() == "#FF3D5A"

    def test_color_method_chaining(self):
        h, s, v = (171, 76, 100)

        new_color = (
            Color.from_hsv(h, s, v).darken(50).lighten(25).invert().as_hex()
        )

        assert new_color == "#BF2E44"
