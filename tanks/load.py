import random
import pygame.sprite
import os
from tanks.sprites import BrickWall, Bush, ConcreteWall, Water
from tanks.constants import *


def __load_image(name):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        raise Exception(f"Файл с изображением '{fullname}' не найден")
    image = pygame.image.load(fullname)
    return image


def __load_sprites(level, group: pygame.sprite.Group):
    for row in range(len(level)):
        for col in range(len(level[row])):
            if level[row][col] == str(BRICK):
                BrickWall(col, row, group)
                BrickWall.image = __load_image("brick.png")
            if level[row][col] == str(BUSH):
                Bush(col, row, group)
                Bush.image = __load_image("bush.png")
            if level[row][col] == str(CONCRETE):
                ConcreteWall(col, row, group)
                ConcreteWall.image = __load_image("concrete.png")
            if level[row][col] == str(WATER):
                Water(col, row, group)
                Water.image = __load_image("water.png")
    return 1


def load_level(filename, group: pygame.sprite.Group):
    level = [list(line.rstrip('\n')) for line in open(f"levels/{filename}")]
    __load_sprites(level, group)
    return 1


def create_random_level(filename):
    with open(f"levels/{filename}", "w") as f:
        for i in range(32):
            f.write("".join([str(random.randint(0, 4)) for _ in range(32)]))
            f.write("\n")
    return 1

