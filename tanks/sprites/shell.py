import os.path
import pygame
from tanks import grid
from tanks.time import delta_time
from tanks.directions import NORTH, WEST, SOUTH, EAST, direction_to_vector
from tanks.sprites import load_image, SpriteBase, GridSpriteBase
from tanks.sounds import load_sound


class Shell(SpriteBase):
    explosion_sound = load_sound('shell_explosion.wav')
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

        field = grid.get_rect()

        if self.pos.x > field.right or self.pos.x < field.left or self.pos.y > field.bottom or \
                self.pos.y < field.top:
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
