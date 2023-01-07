import pymunk
import pygame
WIDTH = 1000
HEIGHT = 600

def convert_coords(coords):
    '''converts coordinates from pymunk to pygame'''
    return int(coords[0]), int(HEIGHT - coords[1])

class Obstacle:
    def __init__(self, space, pos, type):  # type is column or beam
        self.type = type
        body = pymunk.Body(body_type=pymunk.Body.DYNAMIC)
        body.position = pos
        if type == 'column':
            shape = pymunk.Poly.create_box(body, (20, 100), radius=1)
        elif type == 'beam':
            shape = pymunk.Poly.create_box(body, (100, 20), radius=1)
        shape.mass = 50
        shape.elasticity = 0.6
        shape.friction = 0.4
        self.shape = shape
        space.add(body, shape)

    def draw_obstacle(self, screen):
        points = []
        for vector in self.shape.get_vertices():
            x, y = vector.rotated(self.shape.body.angle) + self.shape.body.position
            points.append(convert_coords((int(x), int(y))))
        pygame.draw.lines(screen, 'black', True, points)