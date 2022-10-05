import pytest
from iris_core import PixelCoordinates


class TestPixels:
    def test_initialization(self):
        p = PixelCoordinates(0, 1)

        assert p.x == 0
        assert p.y == 1

    def test_initialization_negative_numbers(self):

        with pytest.raises(ValueError):
            p = PixelCoordinates(-1, -1)
