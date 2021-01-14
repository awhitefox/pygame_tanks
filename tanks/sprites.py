import os.path

import pygame

from tanks.TankControlScheme import TankControlScheme
from tanks.constants import PIXEL_RATIO
from tanks.directions import *
from tanks.grid import cell_to_screen, get_rect
from tanks.time import delta_time


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


class SpriteBase(pygame.sprite.Sprite):
    sheet = None

    def __init__(self, x, y, *groups):
        super().__init__(*groups)
        self.image = self.sheet
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(x, y)


class GridSprite(SpriteBase):
    char = None
    destroyable = False
    tank_obstacle = True
    shell_obstacle = True
    layer = 0

    def __init__(self, grid_x, grid_y, *groups):
        super().__init__(*cell_to_screen(grid_x, grid_y), *groups)


class ConcreteWall(GridSprite):
    sheet = load_image('concrete.png')
    char = '#'


class BrickWall(GridSprite):
    sheet = load_image('brick.png')
    char = '%'
    destroyable = True


class Bush(GridSprite):
    sheet = load_image('bush.png')
    char = '*'
    tank_obstacle = False
    shell_obstacle = False
    layer = 1


class Water(GridSprite):
    sheet = load_image('water.png')
    char = '~'
    shell_obstacle = False


class Spike(GridSprite):
    sheet = load_image('spike.png')
    char = 'x'
    shell_obstacle = False


class Shell(SpriteBase):
    sheet = load_image('shell.png')
    speed = 400

    def __init__(self, x, y, direction, *groups):
        rotate = 0
        self.vector_velocity = direction_to_vector(direction, self.speed)
        size = self.sheet.get_size()
        if direction == WEST:
            x -= size[0] * 1.5 - 1
            y -= size[1] / 2
            rotate = 90
        if direction == NORTH:
            x -= size[0] / 2
            y -= size[1] + 1
        if direction == SOUTH:
            y += 1
            x -= size[0] / 2
            rotate = 180
        if direction == EAST:
            x += 1
            y -= size[1] / 2
            rotate = -90
        self.pos = pygame.Vector2(x, y)
        super().__init__(x, y, *groups)
        self.image = pygame.transform.rotate(self.image, rotate)

    def update(self):
        self.pos += self.vector_velocity * delta_time()
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y

        field = get_rect()

        if self.pos.x > field.right or self.pos.x < field.left or self.pos.y > field.bottom or self.pos.y < field.top:
            self.kill()
            return

        for group in self.groups():
            for sprite in group:
                if sprite is not self:
                    if self.is_collided_with(sprite):
                        if isinstance(sprite, GridSprite):
                            if sprite.destroyable:
                                sprite.kill()
                                self.kill()
                            elif sprite.shell_obstacle:
                                self.kill()
                        elif isinstance(sprite, Shell):
                            self.kill()
                            sprite.kill()

    def is_collided_with(self, sprite):
        return self.rect.colliderect(sprite.rect)


class Tank(SpriteBase):
    shoot_cooldown = 2.5
    sheet = load_image('tanks.png')
    speed = 50
    frames = cut_sheet(sheet, 8, 1)

    def __init__(self, x, y, is_default_control_scheme, *groups):
        x, y = x + PIXEL_RATIO, y + PIXEL_RATIO  # center tank in 2x2 square
        super().__init__(x, y, *groups)
        self.seconds_from_last_shot = self.shoot_cooldown
        if is_default_control_scheme:
            self.images = self.frames[:4]
            self.direction = NORTH
        else:
            self.images = self.frames[4:]
            self.direction = SOUTH
        self.image = self._get_image()
        self.rect = self.image.get_rect()
        self.rect.inflate_ip(-2 * PIXEL_RATIO, -2 * PIXEL_RATIO)  # resize rect because tank is smaller
        self.rect.x = x
        self.rect.y = y
        self.movement = None

        if is_default_control_scheme:
            self.control_scheme = TankControlScheme.default()
        else:
            self.control_scheme = TankControlScheme.alternative()

        self.pos = pygame.Vector2(x, y)
        self.vector_velocity = pygame.Vector2(0, 0)
        self.flag = True

    def update(self):

        field = get_rect()

        self.movement = self.control_scheme.get_movement()
        self.seconds_from_last_shot += delta_time()

        if self.control_scheme.shoot_pressed():
            if self.seconds_from_last_shot >= self.shoot_cooldown:
                self.shoot()
                self.seconds_from_last_shot = 0
                return

        if self.movement is not None:
            self.direction = self.movement
        self.image = self._get_image()

        velocity_vec = direction_to_vector(self.movement, self.speed) * delta_time()

        new_pos = self.pos + velocity_vec
        new_rect = pygame.Rect(new_pos.x, new_pos.y, *self.rect.size)

        for group in self.groups():
            for sprite in group:
                if sprite is not self and new_rect.colliderect(sprite.rect):
                    if (isinstance(sprite, GridSprite) and sprite.tank_obstacle) or isinstance(sprite, Tank):
                        return
                    if isinstance(sprite, Shell):
                        self.kill()
                        sprite.kill()
                        return

        if new_rect.x + self.rect.size[0] > field.right or new_rect.x < field.left \
            or new_rect.y + self.rect.size[1] > field.bottom or new_rect.y < field.top:
            return

        self.pos = new_pos
        self.rect = new_rect

    def shoot(self):
        if self.direction == NORTH:
            Shell(self.pos.x + (self.rect.size[0] / 2) - 1, self.pos.y, NORTH, *self.groups())
        elif self.direction == SOUTH:
            Shell(self.pos.x + (self.rect.size[0] / 2) - 1, self.pos.y + self.rect.size[1], SOUTH, *self.groups())
        elif self.direction == WEST:
            Shell(self.pos.x, self.pos.y + self.rect.size[1] / 2, WEST, *self.groups())
        elif self.direction == EAST:
            Shell(self.pos.x + self.rect.size[0], self.pos.y + self.rect.size[1] / 2, EAST, *self.groups())

    def _get_image(self):
        if self.direction == NORTH:
            return self.images[0]
        if self.direction == SOUTH:
            return self.images[2]
        if self.direction == WEST:
            return self.images[1]
        if self.direction == EAST:
            return self.images[3]
