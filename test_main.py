from main import convert_coords, calculate_distance
from main import calculate_angle
import pytest

def test_convert_coords():
    coords = (250, 200)
    converted_coords = convert_coords(coords)
    assert converted_coords == (250, 400)

def test_calculate_distances():
    p1 = (20, 40)
    p2 = (50, 80)
    distance = calculate_distance(p1, p2)
    assert distance == 50

def test_calculate_angle():
    p1 = (20, 160)
    p2 = (160, 20)
    angle = calculate_angle(p1, p2) * 180 / 3.14
    assert pytest.approx(angle, 0.001) == 45


