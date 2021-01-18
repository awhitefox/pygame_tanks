import pygame
from tanks.constants import PIXEL_RATIO
from tanks.directions import *
from tanks.grid import get_rect
from tanks.time import delta_time
from tanks.sprites import GridSpriteBase, Shell
from tanks.images import load_image, cut_sheet
from tanks.sounds import load_sound


class Tank(pygame.sprite.Sprite):
    """Класс танка"""
    distance_to_animate = PIXEL_RATIO * 2
    shell_spawn_offset = PIXEL_RATIO
    shoot_cooldown = 2.5
    speed = 50

    shoot_sound = load_sound('tank_fire.flac')
    explosion_sound = load_sound('tank_explosion.flac')

    frames = cut_sheet(load_image('tanks.png'), 8, 2)

    def __init__(self, x: float, y: float, is_default_player: bool, *groups: pygame.sprite.Group):
        super().__init__(*groups)
        x, y = x + PIXEL_RATIO, y + PIXEL_RATIO  # center tank in 2x2 square
        self.distance = 0
        self.seconds_from_last_shot = self.shoot_cooldown
        self.frame = 0
        self.pos = pygame.Vector2(x, y)
        if is_default_player:
            self.control_scheme = TankControlScheme.default()
            self.images = self.frames[:8]
            self.direction = NORTH
        else:
            self.control_scheme = TankControlScheme.alternative()
            self.images = self.frames[8:]
            self.direction = SOUTH
        self.image = self._get_image()
        self.rect = self.image.get_rect()
        # resize rect because tank is smaller
        self.rect.inflate_ip(-2 * PIXEL_RATIO, -2 * PIXEL_RATIO)
        self.rect.x = x
        self.rect.y = y

        self.movement = None

        self.vector_velocity = pygame.Vector2(0, 0)

    def update(self) -> None:
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
                        return

        if new_rect.x + self.rect.size[0] > field.right or new_rect.x < field.left \
                or new_rect.y + self.rect.size[1] > field.bottom or new_rect.y < field.top:
            return

        self.distance += (new_pos - self.pos).length()
        self.pos = new_pos
        self.rect = new_rect

    def shoot(self) -> None:
        """Метод для инициализации выстрела"""
        off = self.shell_spawn_offset
        pos = None
        if self.direction == NORTH:
            pos = self.pos.x + (self.rect.w / 2), self.pos.y - off
        elif self.direction == SOUTH:
            pos = self.pos.x + (self.rect.w / 2), self.pos.y + self.rect.h + off
        elif self.direction == WEST:
            pos = self.pos.x - off, self.pos.y + self.rect.h / 2
        elif self.direction == EAST:
            pos = self.pos.x + self.rect.w + off, self.pos.y + self.rect.h / 2
        Shell(*pos, self.direction, *self.groups())
        self.shoot_sound.play()

    def kill(self) -> None:
        self.explosion_sound.play()
        super().kill()

    def _get_image(self) -> pygame.Surface:
        """Защищенный метод для получения картинки на основе направления куда смотрит танк"""
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


class TankControlScheme:
    """Класс схемы управления танком"""
    def __init__(self, up: int, right: int, down: int, left: int, shoot: int):
        self._up = up
        self._right = right
        self._down = down
        self._left = left
        self._shoot = shoot

    def get_movement(self) -> int:
        """Метод для получения направления на основе нажатой клавиши"""
        if pygame.key.get_pressed()[self._up]:
            return NORTH
        elif pygame.key.get_pressed()[self._right]:
            return EAST
        elif pygame.key.get_pressed()[self._down]:
            return SOUTH
        elif pygame.key.get_pressed()[self._left]:
            return WEST

    def shoot_pressed(self) -> bool:
        """Проверка на нажатие кнопки выстрела"""
        return pygame.key.get_pressed()[self._shoot]

    @classmethod
    def default(cls) -> 'TankControlScheme':
        """Создание объекта класса TankControlScheme с клавишами управления для 1-го игрока
        (WASD - движение, Spacebar - выстрел)"""
        return cls(pygame.K_w, pygame.K_d, pygame.K_s, pygame.K_a, pygame.K_SPACE)

    @classmethod
    def alternative(cls) -> 'TankControlScheme':
        """Создание объекта класса TankControlScheme с клавишами управления для 2-го игрока
        (движение стрелками, Enter - выстрел)"""
        return cls(pygame.K_UP, pygame.K_RIGHT, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RETURN)
