import pygame.sprite
import os
from tanks.sprites import BrickWall, Bush, ConcreteWall, Water


def __load_image(name):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname)
    return image


def __load_sprites(level, group: pygame.sprite.Group):
    for row in range(len(level)):
        for col in range(len(level[row])):
            if level[row][col] == BrickWall.Char:
                BrickWall(col, row, group)
            if level[row][col] == Bush.Char:
                Bush(col, row, group)
            if level[row][col] == ConcreteWall.Char:
                ConcreteWall(col, row, group)
            if level[row][col] == Water.Char:
                Water(col, row, group)
    return 1


def load_level(filename, group: pygame.sprite.Group):
    level = [list(line.rstrip('\n')) for line in open(os.path.join('levels', filename))]
    __load_sprites(level, group)
    return 1
