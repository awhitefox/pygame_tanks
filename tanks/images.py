import os.path
import pygame
from tanks.constants import PIXEL_RATIO


def load_image(name):
    image = pygame.image.load(os.path.join('data', name))
    rect = image.get_rect()
    return pygame.transform.scale(image, (rect.w * PIXEL_RATIO, rect.h * PIXEL_RATIO))


def cut_sheet(sheet, columns, rows):
    frames = []
    w, h = sheet.get_width() // columns, sheet.get_height() // rows
    for j in range(rows):
        for i in range(columns):
            frames.append(sheet.subsurface(pygame.Rect(w * i, h * j, w, h)))
    return frames
