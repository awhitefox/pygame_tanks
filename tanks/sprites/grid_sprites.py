import pygame
from tanks.grid import cell_to_screen
from tanks.images import load_image


class GridSpriteBase(pygame.sprite.Sprite):
    """Базовый класс спрайта, расположенного по сетке, используется для наследования."""
    sheet = None
    char = None
    destroyable = False
    tank_obstacle = True
    shell_obstacle = True
    layer = 0

    def __init__(self, grid_x: int, grid_y: int, *groups: pygame.sprite.Group):
        super().__init__(*groups)
        self.image = self.sheet
        self.rect = pygame.Rect(*cell_to_screen(grid_x, grid_y), *self.image.get_size())


class ConcreteWall(GridSpriteBase):
    sheet = load_image('concrete.png')
    char = '#'


class BrickWall(GridSpriteBase):
    sheet = load_image('brick.png')
    char = '%'
    destroyable = True


class Bush(GridSpriteBase):
    sheet = load_image('bush.png')
    char = '*'
    tank_obstacle = False
    shell_obstacle = False
    layer = 1


class Water(GridSpriteBase):
    sheet = load_image('water.png')
    char = '~'
    shell_obstacle = False


class Spike(GridSpriteBase):
    sheet = load_image('spike.png')
    char = 'x'
    shell_obstacle = False
