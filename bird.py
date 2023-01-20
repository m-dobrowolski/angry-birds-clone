import pymunk
import pygame
from convert_coords import convert_coords


class Bird:
    def __init__(self, space):
        '''class represents a bird'''
        radius = 15

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
        self.body = body
        space.add(body, shape)

    def draw(self, screen):
        '''draws enemy on the screen'''
        self.bird_rect.center = convert_coords(self.shape.body.position)
        pygame.draw.circle(screen, 'black', self.bird_rect.center, 15)
