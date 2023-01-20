import pymunk
import pygame
from project.convert_coords import convert_coords


class Enemy:
    def __init__(self, pos, space):
        '''class represents an enemy'''
        radius = 15
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
        '''draws an enemy on the screen'''
        pos = convert_coords(self.shape.body.position)
        pygame.draw.circle(screen, 'green', pos, 15)
