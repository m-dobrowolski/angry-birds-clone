from project.levels import Level, NotExistantLevel
import pymunk
import pytest


def test_level_loading():
    space = pymunk.Space()
    enemies = []
    obstacles = []
    level = Level(space, enemies, obstacles)
    level_number = 3
    level.load_level(level_number)
    assert len(enemies) == 2
    assert len(obstacles) == 9


def test_level_loading_lvl_not_exist():
    space = pymunk.Space()
    enemies = []
    obstacles = []
    level = Level(space, enemies, obstacles)
    level_number = 0
    with pytest.raises(NotExistantLevel):
        level.load_level(level_number)
