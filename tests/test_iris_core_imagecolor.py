from iris_core import ImageColor


class TestImageColor:
    def test_init_rgb(self):
        r, g, b = (252, 186, 3)

        p_map = [[0, 1], [1, 0]]
        i = ImageColor.from_rgb(r, g, b, p_map)

        assert i.color.as_hex() == "#fcba03".upper()

    def test_init_hex(self):
        h = "#fcba03"

        p_map = [[0, 1], [1, 0]]
        i = ImageColor.from_hex(h, p_map)

        r, g, b = i.color.as_rgb()

        assert r == 252
        assert g == 186
        assert b == 3

    def test_init_hsv(self):
        h, s, v = (44, 99, 99)

        p_map = [[0, 1], [1, 0]]
        i = ImageColor.from_hsv(h, s, v, p_map)

        c, m, y, k = i.color.as_cmyk()

        assert c == 0
        assert m == 26
        assert y == 99
        assert k == 1

    def test_init_cmyk(self):
        c, m, y, k = (0, 26, 99, 1)

        p_map = [[0, 1], [1, 0]]
        i = ImageColor.from_cmyk(c, m, y, k, p_map)

        assert i.color.as_hex() == "#fcba03".upper()
