import pygame
from tanks import grid
from tanks.time import delta_time
from tanks.directions import NORTH, WEST, SOUTH, EAST, direction_to_vector
from tanks.sprites import load_image, GridSpriteBase
from tanks.sounds import load_sound


class Shell(pygame.sprite.Sprite):
    """Класс снаряда, движется в заданном направлении"""
    explosion_sound = load_sound('shell_explosion.wav')
    sheet = load_image('shell.png')
    speed = 400

    def __init__(self, x: float, y: float, direction: int, *groups: pygame.sprite.Group):
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

    def update(self) -> None:
        self.pos += self.vector_velocity * delta_time()
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y

        field = grid.get_rect()

        if self.pos.x + self.rect.size[0] > field.right or self.pos.x < field.left or self.pos.y + self.rect.size[1] > field.bottom or self.pos.y < field.top:
            self.explosion_sound.play()
            self.kill()
            return

        for group in self.groups():
            for sprite in group:
                if sprite is not self:
                    if self.rect.colliderect(sprite.rect):
                        if isinstance(sprite, GridSpriteBase):
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
