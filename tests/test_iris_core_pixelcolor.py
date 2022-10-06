from iris_core import PixelColor


class TestPixelColor:
    def test_initialization_and_inheritance_properties(self):
        p_map = [[0, 0], [0, 1], [1, 0], [1, 1]]
        h, s, v = (171, 76, 100)

        p = PixelColor(h, s, v, p_map)

        assert p.h == 171
        assert p.s == 0.76
        assert p.v == 1.0

    def test_initialization_methods(self):
        p_map = [[0, 0], [0, 1], [1, 0], [1, 1]]
        h, s, v = (171, 76, 100)

        p = PixelColor(h, s, v, p_map)

        h, s, v = p.as_hsv()
        assert h == 171
        assert s == 76
        assert v == 100

        assert p.as_hex() == "#3DFFE2"

        r, g, b = p.as_rgb()
        assert r == 61
        assert g == 255
        assert b == 226

    def test_init_different_namespaces(self):
        p_map = [[0, 0], [0, 1], [1, 0], [1, 1]]

        c, m, y, k = (76, 0, 11, 0)
        r, g, b = (61, 255, 226)
        hex_str = "#3dffe2"
        h, s, v = (171, 76, 100)

        c = PixelColor.from_cmyk(c, m, y, k, p_map)
        c = PixelColor.from_hex(hex_str, p_map)
        c = PixelColor.from_hsv(h, s, v, p_map)
        c = PixelColor.from_rgb(r, g, b, p_map)

    def test_pixel_number(self):
        p_map = [[0, 0], [0, 1], [1, 0], [1, 1]]
        h, s, v = (171, 76, 100)

        p = PixelColor(h, s, v, p_map)

        assert p.number_of_pixels() == 4
