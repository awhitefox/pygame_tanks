from pygame import Rect
from tanks.constants import *
from typing import Optional, Tuple


def get_rect() -> Rect:
    """Возвращает прямоугольник, которым задается игровое поле."""
    left = (SCREEN_SIZE[0] - (MAP_SIZE[0] * CELL_SIZE)) // 2
    top = (SCREEN_SIZE[1] - (MAP_SIZE[1] * CELL_SIZE)) // 2
    return Rect(left, top, MAP_SIZE[0] * CELL_SIZE, MAP_SIZE[1] * CELL_SIZE)


def cell_to_screen(x: int, y: int) -> Optional[Tuple[int, int]]:
    """Преобразует координаты на сетке игрового поля в координаты на экране. Если точка не
    принадлежит игровому полю, возвращает None."""
    if not (0 <= x < MAP_SIZE[0] and 0 <= y < MAP_SIZE[1]):
        return None
    rect = get_rect()
    return rect.left + CELL_SIZE * x, rect.top + CELL_SIZE * y
