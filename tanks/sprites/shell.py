import pygame
from tanks import grid
from tanks.time import delta_time
from tanks.directions import NORTH, WEST, SOUTH, EAST, direction_to_vector
from tanks.sprites import GridSpriteBase, ShellExplosion
from tanks.images import load_image


class Shell(pygame.sprite.Sprite):
    """Класс снаряда, движется в заданном направлении"""
    sheet = load_image('shell.png')
    speed = 400
    layer = 1
    shootrange=10000

    def __init__(self, s_speed: int, x: float, y: float, direction: int, *groups: pygame.sprite.Group):
        super().__init__(*groups)
        rotate = 0
        self.x = x
        self.y = y
        self.direct = direction
        self.speed = s_speed
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
        self.initalpos = pygame.Vector2(self.rect.x, self.rect.y)

    def update(self) -> None:
        self.pos += self.vector_velocity * delta_time()
        distx=abs(self.pos.x-self.initalpos.x)
        disty=abs(self.pos.y-self.initalpos.y)
        print("def update(self) -> None:",distx,disty)
        if(max(distx,disty)>Shell.shootrange):
            self.kill()
            return

        
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y

        field = grid.get_rect()

        if self.pos.x + self.rect.size[0] > field.right or self.pos.x < field.left or self.pos.y + \
                self.rect.size[1] > field.bottom or self.pos.y < field.top:
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
                            elif sprite.shell_obstacle:
                                self.kill()
                        elif isinstance(sprite, Shell):
                            sprite.kill()
                            self.kill()
                        # if isinstance(sprite, GridSpriteBase) and sprite.mirroring:
                        #     if self.direct == NORTH:
                        #         self.rect.center = self.x - self.size[0] / 2, self.y
                        #         self.rotate = 180
                        #     if self.direct == SOUTH:
                        #         self.rect.center = self.x - self.size[0] / 2, self.y - self.size[1]
                        #     if self.direct == EAST:
                        #         self.rect.center = self.x - self.size[1], self.y - self.size[0] / 2
                        #         self.rotate = 90
                        #     if self.direct == WEST:
                        #         self.rect.center = self.x, self.y - self.size[0] / 2
                        #         self.rotate = -90
                            


    def kill(self) -> None:
        ShellExplosion(*self.pos, *self.groups())
        super().kill()


