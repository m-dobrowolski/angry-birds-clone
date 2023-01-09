from classes import Obstacle, Enemy

class Level:
    def __init__(self, space, enemies, obstacles):
        self.space = space
        self.enemies = enemies
        self.obstacles = obstacles

    def load_level(self, level):
        level_name = f'level{level}'
        load_level = getattr(self, level_name)
        load_level()

    def level1(self):
        obstacles = [
            Obstacle(self.space, (600, 150), 'column'),
            Obstacle(self.space, (600, 210), 'beam')
        ]
        enemies = [
            Enemy((600, 240), self.space)
        ]
        for obstacle in obstacles:
            self.obstacles.append(obstacle)
        for enemy in enemies:
            self.enemies.append(enemy)

    def level2(self):
        obstacles = [
            Obstacle(self.space, (600, 150), 'column'),
            Obstacle(self.space, (680, 150), 'column')
        ]
        enemies = [
            Enemy((640, 120), self.space)
        ]
        for obstacle in obstacles:
            self.obstacles.append(obstacle)
        for enemy in enemies:
            self.enemies.append(enemy)
