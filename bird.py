import pymunk
import pygame
from convert_coords import convert_coords


class Bird:
    def __init__(self, space):
        '''class represents a bird'''
        radius = 15

        bird_start_pos = (150, 200)
        body = pymunk.Body(body_type=pymunk.Body.STATIC)
        body.position = bird_start_pos
        self.start_position = convert_coords(bird_start_pos)
        shape = pymunk.Circle(body, radius)
        shape.mass = 10
        shape.elasticity = 0.9
        shape.friction = 0.4
        shape.collision_type = 1
        self.shape = shape
        self.body = body
        space.add(body, shape)

    def draw(self, screen):
        '''draws enemy on the screen'''
        pos = convert_coords(self.shape.body.position)
        pygame.draw.circle(screen, 'red', pos, 15)
