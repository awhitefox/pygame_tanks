import os.path
import pygame
from tanks.constants import PIXEL_RATIO
from typing import List


def load_image(filename: str) -> pygame.Surface:
    """Возвращает изображение, загруженное из указанного файла и увеличенное в соответствии с
    PIXEL_RATIO. Поиск файла происходит в папке ./data/"""
    image = pygame.image.load(os.path.join('data', filename))
    rect = image.get_rect()
    return pygame.transform.scale(image, (rect.w * PIXEL_RATIO, rect.h * PIXEL_RATIO))


def cut_sheet(sheet: pygame.Surface, columns: int, rows: int) -> List[pygame.Surface]:
    """Разделяет переданное изображение на кадры."""
    frames = []
    w, h = sheet.get_width() // columns, sheet.get_height() // rows
    for j in range(rows):
        for i in range(columns):
            frames.append(sheet.subsurface(pygame.Rect(w * i, h * j, w, h)))
    return frames
