import pygame
WIDTH = 1000
HEIGHT = 600


class Button:
    def __init__(self, message, font, pos, rect_pos=None):
        '''class representing a button'''
        self.surface = font.render(message, True, (64, 64, 64))
        self.rect = self.surface.get_rect(bottomright=pos)
        # background
        rect_bg = self.rect.move(-5, -5)
        rect_bg.height += 10
        rect_bg.width += 10
        self.rect_bg = rect_bg

    def draw(self, screen):
        '''drawing button on the screen'''
        pygame.draw.rect(screen, 'red', self.rect_bg)
        pygame.draw.rect(screen, 'white', self.rect)
        screen.blit(self.surface, self.rect)
