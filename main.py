from project.game import Game
import pygame


def main():
    pygame.init()
    game = Game()
    game.play()
    pygame.quit()


if __name__ == '__main__':
    main()
