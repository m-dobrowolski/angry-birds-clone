import pygame
import pymunk

pygame.init()

WIDTH = 1000
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))

def convert_coords(coords):
    '''converts coordinates from pymunk to pygame'''
    return int(coords[0]), int(HEIGHT - coords[1])


# def draw(screen, bird):
#     screen.fill('lightblue')

#     pygame.draw.circle(screen, 'black', bird.body.position, 20)

#     pygame.display.update()

def create_ground(space):
    body = pymunk.Body(body_type=pymunk.Body.STATIC)
    body.position = (WIDTH/2, 50)
    shape = pymunk.Poly.create_box(body, (WIDTH, 100))
    space.add(body, shape)
    return shape


def create_brid(space, pos):
    radius = 20

    body = pymunk.Body(body_type=pymunk.Body.DYNAMIC)
    body.position = pos
    shape = pymunk.Circle(body, radius)
    shape.mass = 10
    space.add(body, shape)

    return shape


def main(screen, WIDTH, HEIGHT):
    run = True

    FPS = 60
    step_time = 1/FPS
    clock = pygame.time.Clock()

    space = pymunk.Space()
    space.gravity = (0, -1000)

    bird = create_brid(space, (100, 200))

    ground = create_ground(space)
    ground_rect = pygame.Rect(0, HEIGHT - 100, WIDTH, 100)

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        screen.fill('lightblue')

        # drawing a bird
        bird_pos = convert_coords(bird.body.position)
        pygame.draw.circle(screen, 'black', bird_pos, 20)

        #drawing the ground
        pygame.draw.rect(screen, 'green', ground_rect)

        pygame.display.update()

        space.step(step_time)
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main(screen, WIDTH, HEIGHT)