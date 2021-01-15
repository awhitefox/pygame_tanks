import os.path
import pygame
from tanks.constants import PIXEL_RATIO
from tanks.directions import *
from tanks.grid import get_rect
from tanks.time import delta_time
from tanks.sprites import SpriteBase, GridSpriteBase, Shell
from tanks.images import load_image, cut_sheet
from tanks.sounds import load_sound


class Tank(SpriteBase):
    shoot_cooldown = 2.5
    shoot_sound = load_sound('tank_fire.flac')
    explosion_sound = load_sound('tank_explosion.flac')
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
        # resize rect because tank is smaller
        self.rect.inflate_ip(-2 * PIXEL_RATIO, -2 * PIXEL_RATIO)
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
                    if (isinstance(sprite, GridSpriteBase) and sprite.tank_obstacle) \
                            or isinstance(sprite, Tank):
                        return
                    if isinstance(sprite, Shell):
                        self.kill()
                        sprite.kill()
                        self.explosion_sound.play()
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
        self.shoot_sound.play()

    def _get_image(self):
        if self.direction == NORTH:
            return self.images[0]
        if self.direction == SOUTH:
            return self.images[2]
        if self.direction == WEST:
            return self.images[1]
        if self.direction == EAST:
            return self.images[3]


class TankControlScheme:
    def __init__(self, up, right, down, left, shoot):
        self._up = up
        self._right = right
        self._down = down
        self._left = left
        self._shoot = shoot

    def get_movement(self):
        if pygame.key.get_pressed()[self._up]:
            return NORTH
        elif pygame.key.get_pressed()[self._right]:
            return EAST
        elif pygame.key.get_pressed()[self._down]:
            return SOUTH
        elif pygame.key.get_pressed()[self._left]:
            return WEST

    def shoot_pressed(self) -> bool:
        return pygame.key.get_pressed()[self._shoot]

    @classmethod
    def default(cls):
        return cls(pygame.K_w, pygame.K_d, pygame.K_s, pygame.K_a, pygame.K_SPACE)

    @classmethod
    def alternative(cls):
        return cls(pygame.K_UP, pygame.K_RIGHT, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RETURN)
