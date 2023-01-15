from classes import Obstacle, Enemy


class NotExistantLevel(Exception):
    def __init__(self, lifes):
        super().__init__(f'Level {lifes} do not exist.')
        self.lifes = lifes


class Level:
    def __init__(self, space, enemies, obstacles):
        '''class representing levels of a game'''
        self.space = space
        self.enemies = enemies
        self.obstacles = obstacles
        self.lifes = 0
        self.levels = [1, 2, 3, 4, 5]

    def load_level(self, level):
        '''loads level'''
        if level not in self.levels:
            raise NotExistantLevel(level)
        level_name = f'level{level}'
        load_level = getattr(self, level_name)
        load_level()

    def _add_objects(self, obstacles, enemies):
        '''add objects to a game'''
        for obstacle in obstacles:
            self.obstacles.append(obstacle)
        for enemy in enemies:
            self.enemies.append(enemy)

    def level1(self):
        self.lifes = 2
        obstacles = [
            Obstacle(self.space, (800, 150), 'column'),
            Obstacle(self.space, (880, 150), 'column'),
            Obstacle(self.space, (840, 210), 'beam')
        ]
        enemies = [
            Enemy((840, 115), self.space)
        ]
        self._add_objects(obstacles, enemies)

    def level2(self):
        self.lifes = 3
        obstacles = [
            Obstacle(self.space, (680, 150), 'column'),
            Obstacle(self.space, (760, 150), 'column'),
            Obstacle(self.space, (840, 150), 'column'),
            Obstacle(self.space, (800, 210), 'beam')
        ]
        enemies = [
            Enemy((720, 115), self.space),
            Enemy((800, 115), self.space)
        ]
        self._add_objects(obstacles, enemies)

    def level3(self):
        self.lifes = 3
        obstacles = [
            Obstacle(self.space, (760, 150), 'column'),
            Obstacle(self.space, (840, 150), 'column'),
            Obstacle(self.space, (800, 210), 'beam'),
            Obstacle(self.space, (760, 270), 'column'),
            Obstacle(self.space, (840, 270), 'column'),
            Obstacle(self.space, (800, 330), 'beam'),
            Obstacle(self.space, (760, 390), 'column'),
            Obstacle(self.space, (840, 390), 'column'),
            Obstacle(self.space, (800, 450), 'beam'),
        ]
        enemies = [
            Enemy((800, 345), self.space),
            Enemy((800, 115), self.space)
        ]
        self._add_objects(obstacles, enemies)

    def level4(self):
        self.lifes = 3
        obstacles = [
            Obstacle(self.space, (680, 150), 'column'),
            Obstacle(self.space, (770, 150), 'column'),
            Obstacle(self.space, (720, 210), 'beam'),
            Obstacle(self.space, (860, 150), 'column'),
            Obstacle(self.space, (820, 210), 'beam'),
            Obstacle(self.space, (730, 270), 'column'),
            Obstacle(self.space, (810, 270), 'column'),
            Obstacle(self.space, (770, 330), 'beam'),
        ]
        enemies = [
            Enemy((720, 115), self.space),
            Enemy((820, 115), self.space),
            Enemy((770, 225), self.space),
        ]
        self._add_objects(obstacles, enemies)

    def level5(self):
        self.lifes = 4
        obstacles = [
            Obstacle(self.space, (580, 150), 'column'),
            Obstacle(self.space, (620, 210), 'beam'),
            Obstacle(self.space, (670, 150), 'column'),
            Obstacle(self.space, (770, 150), 'column'),
            Obstacle(self.space, (720, 210), 'beam'),
            Obstacle(self.space, (860, 150), 'column'),
            Obstacle(self.space, (820, 210), 'beam'),
            Obstacle(self.space, (580, 270), 'column'),
            Obstacle(self.space, (620, 330), 'beam'),
            Obstacle(self.space, (670, 270), 'column'),
            Obstacle(self.space, (770, 270), 'column'),
            Obstacle(self.space, (720, 330), 'beam'),
            Obstacle(self.space, (860, 270), 'column'),
            Obstacle(self.space, (820, 330), 'beam'),
        ]
        enemies = [
            Enemy((720, 115), self.space)
        ]
        self._add_objects(obstacles, enemies)
