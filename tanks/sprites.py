import os.path

import pygame

from tanks.TankControlScheme import TankControlScheme
from tanks.constants import PIXEL_RATIO
from tanks.directions import *
from tanks.grid import cell_to_screen, get_rect
from tanks.time import delta_time
pygame.mixer.init()


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


class Shell(pygame.sprite.Sprite):
    explosion_sound = pygame.mixer.Sound(os.path.join('data', 'shell_explosion.wav'))
    sheet = load_image('shell.png')
    speed = 400

    def __init__(self, x, y, direction, *groups):
        super().__init__(*groups)
        rotate = 0
        self.vector_velocity = direction_to_vector(direction, self.speed)
        size = self.sheet.get_size()
        self.rect = pygame.Rect(0, 0, 0, 0)
        if direction == NORTH:
            self.rect.center = x - size[0] / 2, y - size[1]
        if direction == EAST:
            self.rect.center = x, y - size[0] / 2
            rotate = -90

        if direction == SOUTH:
            self.rect.center = x - size[0] / 2, y
            rotate = 180

        if direction == WEST:
            self.rect.center = x - size[1], y - size[0] / 2
            rotate = 90

        self.image = pygame.transform.rotate(self.sheet, rotate)
        self.rect.size = self.image.get_size()
        self.pos = pygame.Vector2(self.rect.x, self.rect.y)

    def update(self):
        self.pos += self.vector_velocity * delta_time()
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y

        field = get_rect()

        if self.pos.x + self.rect.size[0] > field.right or self.pos.x < field.left or self.pos.y + self.rect.size[1] > field.bottom or self.pos.y < field.top:
            self.explosion_sound.play()
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
                                self.explosion_sound.play()
                            elif sprite.shell_obstacle:
                                self.kill()
                                self.explosion_sound.play()
                        elif isinstance(sprite, Shell):
                            self.kill()
                            sprite.kill()
                            self.explosion_sound.play()

    def is_collided_with(self, sprite):
        return self.rect.colliderect(sprite.rect)


class Tank(SpriteBase):
    distance_to_animate = PIXEL_RATIO * 2
    shoot_cooldown = 2.5
    shoot_sound = pygame.mixer.Sound(os.path.join('data', "tank_fire.flac"))
    explosion_sound = pygame.mixer.Sound(os.path.join('data', "tank_explosion.flac"))
    sheet = load_image('tanks.png')
    speed = 50
    frames = cut_sheet(sheet, 8, 2)

    def __init__(self, x, y, is_default_control_scheme, *groups):
        self.distance = 0
        x, y = x + PIXEL_RATIO, y + PIXEL_RATIO  # center tank in 2x2 square
        super().__init__(x, y, *groups)
        self.seconds_from_last_shot = self.shoot_cooldown
        self.frame = 0
        self.pos = pygame.Vector2(x, y)
        if is_default_control_scheme:
            self.images = self.frames[:8]
            self.direction = NORTH
        else:
            self.images = self.frames[8:]
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

        self.vector_velocity = pygame.Vector2(0, 0)

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
                        self.explosion_sound.play()
                        return

        if new_rect.x + self.rect.size[0] > field.right or new_rect.x < field.left \
                or new_rect.y + self.rect.size[1] > field.bottom or new_rect.y < field.top:
            return

        self.distance += (new_pos - self.pos).length()
        self.pos = new_pos
        self.rect = new_rect

    def shoot(self):
        if self.direction == NORTH:
            Shell(self.pos.x + (self.rect.w / 2), self.pos.y, NORTH, *self.groups())
        elif self.direction == SOUTH:
            Shell(self.pos.x + (self.rect.w / 2), self.pos.y + self.rect.h, SOUTH, *self.groups())
        elif self.direction == WEST:
            Shell(self.pos.x, self.pos.y + self.rect.h / 2, WEST, *self.groups())
        elif self.direction == EAST:
            Shell(self.pos.x + self.rect.w, self.pos.y + self.rect.h / 2, EAST, *self.groups())
        self.shoot_sound.play()
    
    def _get_image(self):
        frame = 0
        if self.distance > self.distance_to_animate:
            self.frame += 1 if self.frame % 2 == 0 else -1
            self.distance = 0

        if self.direction == NORTH:
            frame = 0
        elif self.direction == SOUTH:
            frame = 4
        elif self.direction == WEST:
            frame = 2
        elif self.direction == EAST:
            frame = 6

        if self.frame % 2 == 1:
            frame += 1
        self.frame = frame
        return self.images[self.frame]
