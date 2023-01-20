from project.game import Game
import pygame
import pytest


pygame.init()
game = Game()


def test_convert_coords():
    coords = (250, 200)
    converted_coords = game.convert_coords(coords)
    assert converted_coords == (250, 400)


def test_calculate_distances():
    p1 = (20, 40)
    p2 = (50, 80)
    distance = game.calculate_distance(p1, p2)
    assert distance == 50


def test_calculate_angle():
    p1 = (20, 160)
    p2 = (160, 20)
    angle = game.calculate_angle(p1, p2) * 180 / 3.14
    assert pytest.approx(angle, 0.001) == -45


def test_game_load_level():
    game.level_number = 2
    game.load_level(game.level_number)
    assert game.shooted is False
    assert game.level_cleared is False
    assert len(game.enemies) == 2
    assert len(game.obstacles) == 4
    assert len(game.birds) == 1


def test_clear_space():
    game.clear_space()
    assert len(game.enemies) == 0
    assert len(game.obstacles) == 0
    assert len(game.birds) == 0


def test_restart_level():
    game.level_number = 2
    game.load_level(game.level_number)
    assert game.shooted is False
    assert game.level_cleared is False
    assert len(game.enemies) == 2
    assert len(game.obstacles) == 4
    assert len(game.birds) == 1
    game.clear_space()
    assert len(game.enemies) == 0
    assert len(game.obstacles) == 0
    assert len(game.birds) == 0
    game.restart_level()
    assert len(game.enemies) == 2
    assert len(game.obstacles) == 4
    assert len(game.birds) == 1


def test_limit_line():
    line = game.limit_line((100, 100), (320, 380), 100)
    assert pytest.approx(line[1][0], 0.015) == 160
    assert pytest.approx(line[1][1], 0.015) == 180
    line = game.limit_line((100, 100), (130, 140), 100)
    assert line[1][0] == 130
    assert line[1][1] == 140


pygame.quit()
