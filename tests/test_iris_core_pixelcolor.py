from iris_core import PixelColor


class TestPixelColor:
    def test_initialization_and_inheritance_properties(self):
        p_map = [[0, 0], [0, 1], [1, 0], [1, 1]]
        p = PixelColor(100, 100, 100, p_map)

        assert p.r == 100
        assert p.g == 100
        assert p.b == 100

    def test_initialization_methods(self):
        p_map = [[0, 0], [0, 1], [1, 0], [1, 1]]
        p = PixelColor(100, 100, 100, p_map)

        hsv = p.as_hsv()
        assert hsv[0] == 0
        assert hsv[1] == 0
        assert hsv[2] == 39

        assert p.as_hex() == "#646464"

    def test_pixel_number(self):
        p_map = [[0, 0], [0, 1], [1, 0], [1, 1]]
        p = PixelColor(100, 100, 100, p_map)

        assert p.number_of_pixels() == 4
