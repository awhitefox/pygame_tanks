from pygame import Rect
from tanks.constants import *


def get_left():
    return (SCREEN_SIZE[0] - (MAP_SIZE[0] * CELL_SIZE)) // 2


def get_top():
    return (SCREEN_SIZE[1] - (MAP_SIZE[1] * CELL_SIZE)) // 2


def get_rect():
    return Rect(get_left(), get_top(), MAP_SIZE[0] * CELL_SIZE, MAP_SIZE[1] * CELL_SIZE)


def cell_to_screen(x, y):
    if not (0 <= x < MAP_SIZE[0] and 0 <= y < MAP_SIZE[1]):
        return None
    return get_left() + CELL_SIZE * x, get_top() + CELL_SIZE * y
