import pygame


class TankControlScheme:

    def __init__(self, up, right, down, left, shoot):
        self._up = up
        self._right = right
        self._down = down
        self._left = left
        self._shoot = shoot

    def up_pressed(self) -> bool:
        return pygame.key.get_pressed()[self._up]

    def right_pressed(self) -> bool:
        return pygame.key.get_pressed()[self._right]

    def down_pressed(self) -> bool:
        return pygame.key.get_pressed()[self._down]

    def left_pressed(self) -> bool:
        return pygame.key.get_pressed()[self._left]

    def shoot_pressed(self) -> bool:
        return pygame.key.get_pressed()[self._shoot]

    @classmethod
    def default(cls):
        return cls(pygame.K_w, pygame.K_d, pygame.K_s, pygame.K_a, pygame.K_SPACE)

    @classmethod
    def alternative(cls):
        return cls(pygame.K_UP, pygame.K_RIGHT, pygame.K_DOWN, pygame.K_LEFT, pygame.K_KP_ENTER)