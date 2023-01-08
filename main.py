import pygame
import pymunk
import math
from classes import Obstacle, Bird, Enemy

pygame.init()

WIDTH = 1000
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
font = pygame.font.Font(None, 50)

enemies = []

def convert_coords(coords):
    '''converts coordinates from pymunk to pygame'''
    return int(coords[0]), int(HEIGHT - coords[1])


def calculate_distanes(p1, p2):
    return math.sqrt((p2[1] - p1[1])**2 + (p2[0] - p1[0])**2)


def calculate_angle(p1, p2):  # calculate  like p2 is (0, 0)
    return math.atan2((p2[1] - p1[1]), (p2[0] - p1[0]))


def display_lifes(screen, lifes):
    message = f'Birds left: {lifes}'
    lifes_surface = font.render(message, True, (64, 64, 64))
    lifes_rect = lifes_surface.get_rect(bottomleft=(20, HEIGHT - 20))
    screen.blit(lifes_surface, lifes_rect)


def create_ground(space):
    body = pymunk.Body(body_type=pymunk.Body.STATIC)
    body.position = (WIDTH/2, 50)
    shape = pymunk.Poly.create_box(body, (WIDTH, 100))
    shape.elasticity = 0.7
    shape.friction = 0.4
    space.add(body, shape)
    return shape

def collision_bird_enemy(arbiter, space, data):
    bird_shape, enemy_shape = arbiter.shapes
    for enemy in enemies:
        if enemy_shape.body == enemy.body:
            space.remove(enemy.shape, enemy.shape.body)
            enemies.remove(enemy)

def main(screen, WIDTH, HEIGHT):
    run = True

    FPS = 60
    step_time = 1/FPS
    clock = pygame.time.Clock()

    space = pymunk.Space()
    space.gravity = (0, -1000)

    ground = create_ground(space)
    ground_rect = pygame.Rect(0, HEIGHT - 100, WIDTH, 100)

    shooted = False
    stretched = False

    bird = Bird(space)
    birds = [bird]
    lifes = 3  # 3 birds to shoot

    enemy = Enemy((600, 240), space)
    enemies.append(enemy)

    obstacles = [
        Obstacle(space, (600, 150), 'column'),
        Obstacle(space, (600, 210), 'beam')
    ]

    space.add_collision_handler(1, 2).post_solve=collision_bird_enemy

    while run:
        mouse_pos = pygame.mouse.get_pos()

        if lifes and shooted:
            shooted = False
            bird = Bird(space)
            birds.append(bird)

        line = None
        if stretched is True:
            line = (bird.bird_rect.center, mouse_pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            if lifes:
                if not stretched and bird.bird_rect.collidepoint(mouse_pos):
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        stretched = True
            if stretched:
                if event.type == pygame.MOUSEBUTTONUP:
                    lifes -= 1
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
        for bird in birds:
            bird.draw(screen)

        # drawing an enemy
        for enemy in enemies:
            enemy.draw_enemy(screen)

        #drawing the ground
        pygame.draw.rect(screen, 'green', ground_rect)

        #displaying birds left to shoot
        display_lifes(screen, lifes)

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