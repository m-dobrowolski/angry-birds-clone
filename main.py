import pygame
import pymunk
import math
from classes import Obstacle, Bird

pygame.init()

WIDTH = 1000
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))

def convert_coords(coords):
    '''converts coordinates from pymunk to pygame'''
    return int(coords[0]), int(HEIGHT - coords[1])


def calculate_distanes(p1, p2):
    return math.sqrt((p2[1] - p1[1])**2 + (p2[0] - p1[0])**2)


def calculate_angle(p1, p2):  # calculate  like p2 is (0, 0)
    return math.atan2((p2[1] - p1[1]), (p2[0] - p1[0]))


def create_ground(space):
    body = pymunk.Body(body_type=pymunk.Body.STATIC)
    body.position = (WIDTH/2, 50)
    shape = pymunk.Poly.create_box(body, (WIDTH, 100))
    shape.elasticity = 0.7
    shape.friction = 0.4
    space.add(body, shape)
    return shape


# def create_brid(space, pos):
#     radius = 20

#     body = pymunk.Body(body_type=pymunk.Body.STATIC)
#     body.position = pos
#     shape = pymunk.Circle(body, radius)
#     shape.mass = 10
#     shape.elasticity = 0.9
#     shape.friction = 0.4
#     space.add(body, shape)

#     return shape


def main(screen, WIDTH, HEIGHT):
    run = True

    FPS = 60
    step_time = 1/FPS
    clock = pygame.time.Clock()

    space = pymunk.Space()
    space.gravity = (0, -1000)

    # bird_start_pos_pm = (150, 200)
    # bird_start_pos_pg = convert_coords(bird_start_pos_pm)
    # bird = create_brid(space, bird_start_pos_pm)
    # bird_rect = pygame.Rect(
    #     bird_start_pos_pg[0] - 20, bird_start_pos_pg[1] - 20,
    #     40, 40
    # )

    ground = create_ground(space)
    ground_rect = pygame.Rect(0, HEIGHT - 100, WIDTH, 100)

    shooted = False
    stretched = False

    bird = Bird(space)

    obstacles = [
        Obstacle(space, (600, 150), 'column'),
        Obstacle(space, (600, 210), 'beam')
    ]

    while run:
        mouse_pos = pygame.mouse.get_pos()

        line = None
        if stretched is True:
            line = (bird.bird_rect.center, mouse_pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            if (not shooted and not stretched and
                    bird.bird_rect.collidepoint(mouse_pos)):
                if event.type == pygame.MOUSEBUTTONDOWN:
                    stretched = True
            if (not shooted and stretched):
                if event.type == pygame.MOUSEBUTTONUP:
                    stretched = False
                    shooted = True
                    bird.shape.body.body_type = pymunk.Body.DYNAMIC
                    angle = calculate_angle(*line)
                    force = calculate_distanes(*line) * 50
                    fx = math.cos(angle) * force
                    fy = math.sin(angle) * force
                    bird.shape.body.apply_impulse_at_local_point((-fx, fy), (0, 0))


        screen.fill('lightblue')

        # drawing a bird
        # bird_rect.center = convert_coords(bird.body.position)
        # pygame.draw.circle(screen, 'black', bird_rect.center, 20)
        bird.draw(screen)

        #drawing the ground
        pygame.draw.rect(screen, 'green', ground_rect)

        #drawing a line between a bird and mouse
        if line:
            pygame.draw.line(screen, 'red', line[0], line[1], 3)

        # drawing obstacles
        for obstacle in obstacles:
            obstacle.draw_obstacle(screen)


        pygame.display.update()

        space.step(step_time)
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main(screen, WIDTH, HEIGHT)