import pygame
import pymunk
import math
from project.bird import Bird
from project.levels import Level, NotExistantLevel
from project.button import Button


class Game:
    def __init__(self):
        '''initializes a game'''
        self.width = 1000
        self.height = 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.font = pygame.font.Font(None, 50)
        self.big_font = pygame.font.Font(None, 200)
        self.enemies = []
        self.obstacles = []
        self.birds = []
        self.bird = None
        self.lifes = 0
        self.shooted = False
        self.stretched = False
        self.level_cleared = False
        self.space = pymunk.Space()
        self.space.gravity = (0, -600)
        self.level = Level(self.space, self.enemies, self.obstacles)
        self.level_number = 1  # if level number == 0, you've won the game

    def load_level(self, level_num):
        '''clears space and loads level'''
        self.shooted = False
        self.level_cleared = False
        self.clear_space()
        try:
            self.level.load_level(level_num)
            self.lifes = self.level.lifes
            self.bird = Bird(self.space)
            self.birds.append(self.bird)
        except NotExistantLevel:
            self.level_number = 0

    def convert_coords(self, coords):
        '''converts coordinates from pymunk to pygame'''
        return int(coords[0]), int(self.height - coords[1])

    def calculate_distance(self, p1, p2):
        '''calculate distance between two points'''
        return math.sqrt((p2[1] - p1[1])**2 + (p2[0] - p1[0])**2)

    def calculate_angle(self, p1, p2):
        '''calculates angle of shoot'''
        return math.atan2((p2[1] - p1[1]), (p2[0] - p1[0]))

    def display_lifes(self):
        '''display lifes on the screen'''
        message = f'Birds left: {self.lifes}'
        lifes_surface = self.font.render(message, True, (64, 64, 64))
        lifes_rect = lifes_surface.get_rect(bottomleft=(20, self.height - 20))
        self.screen.blit(lifes_surface, lifes_rect)

    def create_ground(self):
        '''create static ground'''
        body = pymunk.Body(body_type=pymunk.Body.STATIC)
        body.position = (self.width/2, 50)
        shape = pymunk.Poly.create_box(body, (self.width, 100))
        shape.elasticity = 0.7
        shape.friction = 0.4
        shape.collision_type = 4
        self.space.add(body, shape)
        return shape

    def collision_bird_enemy(self, arbiter, space, data):
        '''handles collision between bird and enemy'''
        bird_shape, enemy_shape = arbiter.shapes
        for enemy in self.enemies:
            if enemy_shape.body == enemy.body:
                space.remove(enemy.shape, enemy.shape.body)
                self.enemies.remove(enemy)

    def collision_bird_obstacle(self, arbiter, space, data):
        '''handles collision between bird and obstacle'''
        bird_shape, obstacle_shape = arbiter.shapes
        if arbiter.total_impulse.length > 3000:
            for obstacle in self.obstacles:
                if obstacle_shape.body == obstacle.body:
                    space.remove(obstacle.shape, obstacle.body)
                    self.obstacles.remove(obstacle)

    def collision_enemy_obstacle(self, arbiter, space, data):
        '''handles collision between enemy and obstacle'''
        enemy_shape, obstacle_shape = arbiter.shapes
        if arbiter.total_impulse.length > 5000:
            for enemy in self.enemies:
                if enemy_shape.body == enemy.body:
                    space.remove(enemy.shape, enemy.shape.body)
                    self.enemies.remove(enemy)

    def collision_enemy_ground(self, arbiter, space, data):
        '''handles collision between enemy and ground'''
        enemy_shape, ground_shape = arbiter.shapes
        if arbiter.total_impulse.length > 5000:
            for enemy in self.enemies:
                if enemy_shape.body == enemy.body:
                    space.remove(enemy.shape, enemy.shape.body)
                    self.enemies.remove(enemy)

    def clear_space(self):
        '''clears every object on the screen'''
        for enemy in self.enemies:
            self.space.remove(enemy.shape, enemy.body)
        self.enemies.clear()
        for obstacle in self.obstacles:
            self.space.remove(obstacle.shape, obstacle.body)
        self.obstacles.clear()
        for bird in self.birds:
            self.space.remove(bird.shape, bird.body)
        self.birds.clear()

    def shoot_bird(self, line):
        '''shoots bird with force calculated from line length'''
        self.lifes -= 1
        self.stretched = False
        self.shooted = True
        self.bird.body.body_type = pymunk.Body.DYNAMIC
        line_converted = (self.convert_coords(line[0]),
                          self.convert_coords(line[1]))
        angle = self.calculate_angle(*line_converted)
        force = self.calculate_distance(*line_converted) * 60
        fx = math.cos(angle) * force
        fy = math.sin(angle) * force
        self.bird.body.apply_impulse_at_local_point((-fx, -fy), (0, 0))

    def restart_level(self):
        '''restarts level'''
        self.load_level(self.level_number)

    def limit_line(self, center_pos, mouse_pos, length):
        '''limits line to specific length'''
        if self.calculate_distance(center_pos, mouse_pos) > length:
            angle = self.calculate_angle(center_pos, mouse_pos)
            x_pos, y_pos = center_pos
            x_pos += length * math.cos(angle)
            y_pos += length * math.sin(angle)
            end_point = (x_pos, y_pos)
            line = (center_pos, end_point)
        else:
            line = (center_pos, mouse_pos)
        return line

    def add_collision(self):
        '''adding collision handlers to simulation'''
        self.space.add_collision_handler(1, 2).post_solve = (
            self.collision_bird_enemy)
        self.space.add_collision_handler(1, 3).post_solve = (
            self.collision_bird_obstacle)
        self.space.add_collision_handler(2, 3).post_solve = (
            self.collision_enemy_obstacle)
        self.space.add_collision_handler(2, 4).post_solve = (
            self.collision_enemy_ground)

    def draw(self, screen, ground_rect, line, restart_level_button,
             restart_game_button, next_lvl_button, win_surf, win_rect,
             lvl_cleared_surf, lvl_cleared_rect):
        '''drawing objects on the screen'''

        # filling background
        screen.fill('lightblue')

        # drawing birds
        for bird in self.birds:
            bird.draw(screen)

        # drawing enemies
        for enemy in self.enemies:
            enemy.draw_enemy(screen)

        # drawing the ground
        pygame.draw.rect(screen, 'green', ground_rect)

        # displaying birds left to shoot
        if self.level_number != 0:
            self.display_lifes()

        # drawing a line between a bird and mouse
        if line:
            pygame.draw.line(screen, 'red', line[0], line[1], 3)

        # drawing obstacles
        for obstacle in self.obstacles:
            obstacle.draw_obstacle(screen)

        # drawing restart level button
        if self.level_number != 0:
            restart_level_button.draw(screen)

        # drawing restart game button
        restart_game_button.draw(screen)

        # displaying you've won message
        if self.level_number == 0:
            screen.blit(win_surf, win_rect)

        if len(self.enemies) == 0:
            self.level_cleared = True
            self.lifes = 0

        # level cleared message
        if self.level_cleared is True and self.level_number != 0:
            self.clear_space()
            screen.blit(lvl_cleared_surf, lvl_cleared_rect)
            # next level button
            next_lvl_button.draw(screen)

        pygame.display.update()

    def play(self):
        run = True
        height = self.height
        width = self.width
        FPS = 60
        step_time = 1/FPS
        clock = pygame.time.Clock()

        # creating ground
        self.create_ground()
        ground_rect = pygame.Rect(0, height - 100, width, 100)

        # loading first level
        self.load_level(self.level_number)

        # adding collision
        self.add_collision()

        # restart level button
        message = 'Restart level'
        pos = (width - 10, height - 10)
        restart_level_button = Button(message, self.font, pos)

        # restart game button
        message = 'Restart game'
        pos = (restart_level_button.rect.left - 20, height - 10)
        restart_game_button = Button(message, self.font, pos)

        # you've won message
        message = 'YOU\'VE WON!'
        win_surf = self.big_font.render(message, True, (64, 64, 64))
        win_rect = win_surf.get_rect(center=(width/2, height/3))

        # next level button
        message = 'Next level'
        pos = (restart_game_button.rect.left - 20, self.height - 10)
        next_lvl_button = Button(message, self.font, pos)

        # level cleared message
        message = 'Level cleared!'
        lvl_cleared_surf = self.big_font.render(message, True, (64, 64, 64))
        lvl_cleared_rect = lvl_cleared_surf.get_rect(center=(width/2,
                                                     height/3))
        # shooting rect
        x_pos, y_pos = self.bird.start_position
        shooting_rect = pygame.Rect(x_pos, y_pos, 30, 30)
        shooting_rect.move_ip(-15, -15)

        while run:
            mouse_pos = pygame.mouse.get_pos()

            # adding bird to shoot
            if self.lifes and self.shooted:
                self.shooted = False
                self.bird = Bird(self.space)
                self.birds.append(self.bird)

            # coords of a line if it exist, used to calculate force of shoot
            line = None
            if self.stretched is True:
                line = self.limit_line(shooting_rect.center, mouse_pos,
                                       120)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    break
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_n:
                        # cheat, used to load next level (press 'n')
                        self.level_number += 1
                        self.load_level(self.level_number)
                if self.lifes:
                    if (not self.stretched and
                            shooting_rect.collidepoint(mouse_pos)):
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            # switching stretched to true when bird pressed
                            self.stretched = True
                if self.stretched:
                    if event.type == pygame.MOUSEBUTTONUP:
                        # shooting a bird
                        self.shoot_bird(line)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if restart_level_button.rect.collidepoint(mouse_pos):
                        # restarting level
                        self.load_level(self.level_number)
                    if restart_game_button.rect.collidepoint(mouse_pos):
                        # restarting game
                        self.level_number = 1
                        self.load_level(self.level_number)

                    if (self.level_cleared is True and
                            next_lvl_button.rect.collidepoint(mouse_pos) and
                            self.level_number != 0):
                        # next level
                        self.level_number += 1
                        self.load_level(self.level_number)

            self.draw(
                self.screen, ground_rect, line, restart_level_button,
                restart_game_button, next_lvl_button, win_surf, win_rect,
                lvl_cleared_surf, lvl_cleared_rect
            )

            self.space.step(step_time)
            clock.tick(FPS)
