import pymunk
import pygame
WIDTH = 1000
HEIGHT = 600


def convert_coords(coords):
    '''converts coordinates from pymunk to pygame'''
    return int(coords[0]), int(HEIGHT - coords[1])


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
        shape.mass = 50
        shape.elasticity = 0.6
        shape.friction = 0.4
        self.shape = shape
        space.add(body, shape)

    def draw_obstacle(self, screen):
        '''draws obstacle on the screen'''
        points = []
        for vector in self.shape.get_vertices():
            x, y = vector.rotated(self.shape.body.angle) + self.shape.body.position
            points.append(convert_coords((int(x), int(y))))
        pygame.draw.lines(screen, 'black', True, points)

class Bird:
    def __init__(self, space):
        radius = 20

        bird_start_pos_pm = (150, 200)
        bird_start_pos_pg = convert_coords(bird_start_pos_pm)
        bird_rect = pygame.Rect(0, 0, radius*2, radius*2)
        bird_rect.center = bird_start_pos_pg
        self.bird_rect = bird_rect

        body = pymunk.Body(body_type=pymunk.Body.STATIC)
        body.position = bird_start_pos_pm
        shape = pymunk.Circle(body, radius)
        shape.mass = 10
        shape.elasticity = 0.9
        shape.friction = 0.4
        shape.collision_type = 1
        self.shape = shape
        space.add(body, shape)

    def draw(self, screen):
        self.bird_rect.center = convert_coords(self.shape.body.position)
        pygame.draw.circle(screen, 'black', self.bird_rect.center, 20)


class Enemy:
    def __init__(self, pos, space):
        radius = 20
        mass = 10

        body = pymunk.Body(body_type=pymunk.Body.DYNAMIC)
        body.position = pos
        self.body = body
        shape = pymunk.Circle(body, radius)
        shape.mass = mass
        shape.elasticity = 0.7
        shape.friction = 1
        shape.collision_type = 2
        self.shape = shape
        space.add(body, shape)

    def draw_enemy(self, screen):
        pos = convert_coords(self.shape.body.position)
        pygame.draw.circle(screen, 'green', pos, 20)
