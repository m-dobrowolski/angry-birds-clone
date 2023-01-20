# i added this function in other file because it is used in multiple files

WIDTH = 1000
HEIGHT = 600


def convert_coords(coords):
    '''converts coordinates from pymunk to pygame'''
    return int(coords[0]), int(HEIGHT - coords[1])
