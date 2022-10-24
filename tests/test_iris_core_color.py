import pytest
from iris_core import Color, __version__


def test_version():
    assert __version__ == "0.1.0"


class TestColor:
    def test_init_from_hsv(self):
        """Tests the class' initializaton from HSV"""
        h, s, v = (171, 76, 100)

        c = Color.from_hsv(h, s, v)

        assert c.h == 171
        assert c.s == 0.76
        assert c.v == 1.0

    def test_init_from_hsv_bad_values(self):
        """Tests the error handling of HSV initiator if HSV values are bad"""
        h, s, v = (10000, -99, 1939)

        with pytest.raises(ValueError):
            c = Color.from_hsv(h, s, v)

    def test_init_from_rgb(self):
        """Tests the class' initializaton from RGB"""
        r, g, b = (61, 255, 226)

        c = Color.from_rgb(r, g, b)

        assert c.h == 171
        assert c.s == 0.76
        assert c.v == 1.0

    def test_init_from_rgb_bad_values(self):
        """Tests the error handling of RGB initiator if RGB values are bad"""
        r, g, b = (100, 555, -98)

        with pytest.raises(ValueError):
            c = Color.from_rgb(r, g, b)

    def test_init_from_hex(self):
        """Tests the class' initializaton from a hex string"""
        hex_str = "#3dffe2"

        c = Color.from_hex(hex_str)

        assert c.h == 171
        assert c.s == 0.76
        assert c.v == 1.0

    def test_init_from_hex_bad_str(self):
        """Tests the error handling of hex initiator if a string is bad"""
        bad_hex = "#FFFFFF00"

        with pytest.raises(ValueError):
            c = Color.from_hex(bad_hex)

    def test_init_from_cmyk(self):
        """Tests the class' initializaton from CMYK"""
        c, m, y, k = (76, 0, 11, 0)

        c = Color.from_cmyk(c, m, y, k)

        h, s, v = c.as_hsv()

        assert h == 171
        assert s == 76
        assert v == 100

    def test_init_from_cmyk_bad_values(self):
        """Tests the error handling of CMYK initiator if CMYK values are bad"""
        c, m, y, k = (101, -98, 77777, 64)

        with pytest.raises(ValueError):
            c = Color.from_cmyk(c, m, y, k)

    def test_color_as_hsv(self):
        """Tests the conversion to HSV"""
        h, s, v = (171, 76, 100)

        c = Color.from_hsv(h, s, v)

        h1, s1, v1 = c.as_hsv()

        assert h1 == 171
        assert s1 == 76
        assert v1 == 100

    def test_color_as_rgb(self):
        """Tests the conversion to RGB"""
        h, s, v = (171, 76, 100)

        c = Color.from_hsv(h, s, v)

        r, g, b = c.as_rgb()

        assert r == 61
        assert g == 255
        assert b == 226

    def test_color_as_hex(self):
        """Tests the conversion to hex string"""
        h, s, v = (171, 76, 100)

        c = Color.from_hsv(h, s, v)

        hex_s = c.as_hex()

        assert hex_s == "#3DFFE2"

    def test_color_as_cmyk(self):
        """Tests the conversion to CMYK"""
        h, s, v = (171, 76, 100)

        c = Color.from_hsv(h, s, v)

        c, m, y, k = c.as_cmyk()

        assert c == 76
        assert m == 0
        assert y == 11
        assert k == 0

    def test_color_hue_shift_positive(self):
        """Tests the correctness of positive hue shift"""
        h, s, v = (171, 76, 100)
        c = Color.from_hsv(h, s, v)

        c.hue_shift(21)

        assert c.as_hex() == "#3DD8FF"

    def test_color_hue_shift_negative(self):
        """Tests the correctness of negative hue shift"""
        h, s, v = (171, 76, 100)
        c = Color.from_hsv(h, s, v)

        c.hue_shift(-21)

        assert c.as_hex() == "#3DFF9E"

    def test_color_hue_shift_positive_loop_around(self):
        """Tests the correctness of positive hue shift where the hue loops
        around itself (>360)"""
        h, s, v = (171, 76, 100)
        c = Color.from_hsv(h, s, v)

        c.hue_shift(210)

        assert c.as_hex() == "#FF813D"

    def test_color_hue_shift_negative_loop_around(self):
        """Tests the correctness of negative hue shift where the hue loops
        around itself (<0)"""
        h, s, v = (171, 76, 100)
        c = Color.from_hsv(h, s, v)

        c.hue_shift(-210)

        assert c.as_hex() == "#FF3DBB"

    def test_color_lighten_in_bounds(self):
        """Tests the corectness of color lightening when the value is in [0..100] range"""
        h, s, v = (171, 76, 40)
        c = Color.from_hsv(h, s, v)

        c.lighten(50)

        assert c.as_hex() == "#37E6CB"

    def test_color_lighten_cap(self):
        """Tests the corectness of color lightening when the value is not in [0..100] range"""
        h, s, v = (171, 76, 50)
        c = Color.from_hsv(h, s, v)

        c.lighten(150)

        assert c.as_hex() == "#3DFFE2"

    def test_color_darken_in_bounds(self):
        """Tests the corectness of color darkening when the value is in [0..100] range"""
        h, s, v = (171, 76, 100)
        c = Color.from_hsv(h, s, v)

        c.darken(15)

        assert c.as_hex() == "#34D9C0"

    def test_color_darken_out_of_bound(self):
        """Tests the corectness of color darkening when the value is not in [0..100] range"""
        h, s, v = (171, 76, 100)
        c = Color.from_hsv(h, s, v)

        c.darken(150)

        assert c.as_hex() == "#000000"

    def test_color_invert(self):
        """Tests the correctness of color inversion"""
        h, s, v = (171, 76, 100)
        c = Color.from_hsv(h, s, v)

        c.invert()

        assert c.as_hex() == "#FF3D5A"

    def test_color_method_chaining(self):
        """Tests the correctness of color modifications if the methods are chained"""
        h, s, v = (171, 76, 100)

        new_color = (
            Color.from_hsv(h, s, v).darken(50).lighten(25).invert().as_hex()
        )

        assert new_color == "#BF2E44"

    def test_color_adjust_saturation(self):
        """Tests the correctness of saturation adjustment if the adjustment
        amount is in [-100..100] range"""
        h, s, v = (171, 76, 100)
        c = Color.from_hsv(h, s, v)

        c.adjust_saturation(-30)

        assert c.as_hex() == "#8AFFED"

    def test_color_adjust_saturation_capping(self):
        """Tests the correctness of saturation adjustment if the adjustment
        amount is not in [-100..100] range"""
        h, s, v = (171, 76, 100)
        c = Color.from_hsv(h, s, v)
        c1 = Color.from_hsv(h, s, v)

        c.adjust_saturation(10000)
        c1.adjust_saturation(-10000)

        assert c.as_hex() == "#00FFD9"
        assert c1.as_hex() == "#FFFFFF"

    # THIS COLOR BREAKS EVERYTHING
    def test_strange_color(self):
        """Tests the strange color that was the cause of conversion algorithms
        breaking (left here just in case)"""
        r, g, b = (252, 186, 3)

        c = Color.from_rgb(r, g, b)

        c, m, y, k = c.as_cmyk()

        assert c == 0
        assert m == 26
        assert y == 99
        assert k == 1

    def test_color_equality(self):
        """Tests whether the comparison between two objects works correctly"""
        c1 = Color.from_hsv(100, 50, 50)
        c2 = Color.from_rgb(85, 128, 64)
        c3 = Color.from_hsv(1, 1, 1)

        assert c1 == c2

        with pytest.raises(AssertionError):
            assert c1 == c3

    def test_color_hash(self):
        """Tests whether the hash() function hashes the Color object correctly"""
        c1 = Color.from_hsv(100, 50, 50)
        c2 = Color.from_rgb(85, 128, 64)
        c3 = Color.from_hsv(1, 1, 1)

        h1, h2, h3 = hash(c1), hash(c2), hash(c3)

        assert h1 == h2
        assert h1 != h3

    def test_color_lookup(self):
        """Tests whether looking up a color object in an array works correctly"""
        c1 = Color.from_hsv(100, 50, 50)
        c2 = Color.from_rgb(85, 128, 64)
        c3 = Color.from_hsv(1, 1, 1)
        c4 = Color.from_hex("#558040")
        c5 = Color.from_rgb(2, 2, 2)

        color_array = [c1, c2, c3]

        assert c4 in color_array
        assert c5 not in color_array

    def test_color_harmony_complementary(self):
        """Tests the complementary color harmony rule"""

        c = Color.from_hex("#000000")
        p = c.harmony_complementary()
