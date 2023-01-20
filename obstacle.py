import pymunk
import pygame
from convert_coords import convert_coords


class Obstacle:
    def __init__(self, space, pos, type):  # type is column or beam
        '''represent a column or a beam'''
        self.type = type
        body = pymunk.Body(body_type=pymunk.Body.DYNAMIC)
        body.position = pos
        if type == 'column':
            shape = pymunk.Poly.create_box(body, (20, 100), radius=1)
        elif type == 'beam':
            shape = pymunk.Poly.create_box(body, (100, 20), radius=1)
        shape.mass = 10
        shape.elasticity = 0.3
        shape.friction = 0.4
        shape.collision_type = 3
        self.shape = shape
        self.body = body
        space.add(body, shape)

    def draw_obstacle(self, screen):
        '''draws obstacle on the screen'''
        points = []
        vertices = self.shape.get_vertices()
        for vector in vertices:
            angle = self.shape.body.angle
            x, y = vector.rotated(angle) + self.shape.body.position
            points.append(convert_coords((int(x), int(y))))
        pygame.draw.lines(screen, 'black', True, points)