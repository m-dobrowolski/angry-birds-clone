import pygame
import pymunk
import math
from classes import Bird
from levels import Level

pygame.init()

WIDTH = 1000
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
font = pygame.font.Font(None, 50)
big_font = pygame.font.Font(None, 200)

enemies = []
obstacles = []
birds = []


def convert_coords(coords):
    '''converts coordinates from pymunk to pygame'''
    return int(coords[0]), int(HEIGHT - coords[1])


def calculate_distance(p1, p2):
    '''calculate distance between two points'''
    return math.sqrt((p2[1] - p1[1])**2 + (p2[0] - p1[0])**2)


def calculate_angle(p1, p2):
    '''calculates angle of shoot'''
    p1, p2 = convert_coords(p1), convert_coords(p2)
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


def collision_bird_obstacle(arbiter, space, data):
    bird_shape, obstacle_shape = arbiter.shapes
    if arbiter.total_impulse.length > 2500:  # popraw wartości
        for obstacle in obstacles:
            if obstacle_shape.body == obstacle.body:
                space.remove(obstacle.shape, obstacle.body)
                obstacles.remove(obstacle)


def collision_enemy_obstacle(arbiter, space, data):
    enemy_shape, obstacle_shape = arbiter.shapes
    if arbiter.total_impulse.length > 4000:
        for enemy in enemies:
            if enemy_shape.body == enemy.body:
                space.remove(enemy.shape, enemy.shape.body)
                enemies.remove(enemy)


def clear_space(space):
    # clearing space
    for enemy in enemies:
        space.remove(enemy.shape, enemy.body)
    enemies.clear()
    for obstacle in obstacles:
        space.remove(obstacle.shape, obstacle.body)
    obstacles.clear()
    for bird in birds:
        space.remove(bird.shape, bird.body)
    birds.clear()


def main(screen):
    run = True

    FPS = 60
    step_time = 1/FPS
    clock = pygame.time.Clock()

    space = pymunk.Space()
    space.gravity = (0, -600)

    create_ground(space)
    ground_rect = pygame.Rect(0, HEIGHT - 100, WIDTH, 100)

    shooted = False
    stretched = False
    level_cleared = False

    bird = Bird(space)
    birds.append(bird)
    lifes = 3  # 3 birds to shoot

    # enemy = Enemy((600, 240), space)
    # enemies.append(enemy)

    # obstacles.append(Obstacle(space, (600, 150), 'column'),)
    # obstacles.append(Obstacle(space, (600, 210), 'beam'))

    level = Level(space, enemies, obstacles)
    level_number = 1
    level.load_level(level_number)

    space.add_collision_handler(1, 2).post_solve = collision_bird_enemy
    space.add_collision_handler(1, 3).post_solve = collision_bird_obstacle
    space.add_collision_handler(2, 3).post_solve = collision_enemy_obstacle

    # restart level button
    message = 'Restart level'
    reset_surface = font.render(message, True, (64, 64, 64))
    reset_rect = reset_surface.get_rect(bottomright=(WIDTH - 10, HEIGHT - 10))
    reset_rect_background = reset_rect.move(-5, -5)
    reset_rect_background.height += 10
    reset_rect_background.width += 10

    # restart game button
    message = 'Restart game'
    reset_game_surface = font.render(message, True, (64, 64, 64))
    reset_game_rect = reset_game_surface.get_rect(
        bottomright=(reset_rect_background.left - 15, HEIGHT - 10)
    )
    reset_game_rect_background = reset_game_rect.move(-5, -5)
    reset_game_rect_background.height += 10
    reset_game_rect_background.width += 10

    # you've won message
    message = 'YOU\'VE WON!'
    win_surf = big_font.render(message, True, (64, 64, 64))
    win_rect = win_surf.get_rect(center=(WIDTH/2, HEIGHT/3))

    # level cleared message
    message = 'Level cleared!'
    lvl_cleared_surf = big_font.render(message, True, (64, 64, 64))
    lvl_cleared_rect = lvl_cleared_surf.get_rect(center=(WIDTH/2, HEIGHT/3))

    # next level button
    message = 'Next level'
    next_lvl_surf = font.render(message, True, (64, 64, 64))
    next_lvl_rect = next_lvl_surf.get_rect(
        bottomright=(reset_game_rect_background.left - 15, HEIGHT - 10)
    )
    next_lvl_rect_background = next_lvl_rect.move(-5, -5)
    next_lvl_rect_background.height += 10
    next_lvl_rect_background.width += 10

    while run:
        mouse_pos = pygame.mouse.get_pos()

        # adding bird to shoot
        if lifes and shooted:
            shooted = False
            bird = Bird(space)
            birds.append(bird)

        # coords of a line if exist
        line = None
        if stretched is True:
            line = (bird.bird_rect.center, mouse_pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_n:
                    # cheat, used to load next level (press 'n')
                    clear_space(space)
                    lifes = 3
                    level_number += 1
                    # trying to load level
                    try:
                        level.load_level(level_number)
                        bird = Bird(space)
                        birds.append(bird)
                    except AttributeError:
                        level_number = 0
            if lifes:
                if not stretched and bird.bird_rect.collidepoint(mouse_pos):
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        stretched = True
            if stretched:
                if event.type == pygame.MOUSEBUTTONUP:
                    # shooting a bird
                    lifes -= 1
                    stretched = False
                    shooted = True
                    bird.body.body_type = pymunk.Body.DYNAMIC
                    angle = calculate_angle(*line)
                    force = calculate_distance(*line) * 50
                    fx = math.cos(angle) * force
                    fy = math.sin(angle) * force
                    bird.body.apply_impulse_at_local_point((-fx, -fy), (0, 0))
            if event.type == pygame.MOUSEBUTTONDOWN:
                if reset_rect.collidepoint(mouse_pos):
                    # restarting level
                    level_cleared = False
                    clear_space(space)

                    # reseting lifes                            # to change in the future
                    lifes = 3

                    # trying to load level
                    try:
                        level.load_level(level_number)
                        bird = Bird(space)
                        birds.append(bird)
                    except AttributeError:
                        level_number = 0
                if reset_game_rect.collidepoint(mouse_pos):
                    # restarting game
                    level_cleared = False
                    clear_space(space)
                    lifes = 3
                    level_number = 1
                    level.load_level(level_number)
                    bird = Bird(space)
                    birds.append(bird)
                if (level_cleared is True and
                        next_lvl_rect.collidepoint(mouse_pos)):

                    # next level button
                    clear_space(space)
                    lifes = 3
                    level_number += 1

                    # trying to load level
                    try:
                        level.load_level(level_number)
                        bird = Bird(space)
                        birds.append(bird)
                    except AttributeError:
                        level_number = 0
                    level_cleared = False

        screen.fill('lightblue')

        # drawing a bird
        for bird in birds:
            bird.draw(screen)

        # drawing an enemy
        for enemy in enemies:
            enemy.draw_enemy(screen)

        # drawing the ground
        pygame.draw.rect(screen, 'green', ground_rect)

        # displaying birds left to shoot
        if level_number != 0:
            display_lifes(screen, lifes)

        # drawing a line between a bird and mouse
        if line:
            pygame.draw.line(screen, 'red', line[0], line[1], 3)

        # drawing obstacles
        for obstacle in obstacles:
            obstacle.draw_obstacle(screen)

        # drawing restart level button
        if level_number != 0:
            pygame.draw.rect(screen, 'red', reset_rect_background)
            pygame.draw.rect(screen, 'white', reset_rect)
            screen.blit(reset_surface, reset_rect)

        # drawing restart game button
        pygame.draw.rect(screen, 'red', reset_game_rect_background)
        pygame.draw.rect(screen, 'white', reset_game_rect)
        screen.blit(reset_game_surface, reset_game_rect)

        # displaying you've won message
        if level_number == 0:
            screen.blit(win_surf, win_rect)

        if len(enemies) == 0:
            level_cleared = True
            lifes = 0

        # level cleared message
        if level_cleared is True and level_number != 0:
            clear_space(space)
            screen.blit(lvl_cleared_surf, lvl_cleared_rect)
            # next level button
            pygame.draw.rect(screen, 'red', next_lvl_rect_background)
            pygame.draw.rect(screen, 'white', next_lvl_rect)
            screen.blit(next_lvl_surf, next_lvl_rect)

        pygame.display.update()

        space.step(step_time)
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main(screen)
